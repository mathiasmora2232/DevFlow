import json
import os
import stat
import threading
from datetime import datetime, timedelta, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import pytest
import yaml

from devflow.cli import install_session_hook, main
from devflow.stellar import StellarError, stellar_token
from devflow.stellar_auth import (
    StellarAuthError,
    auth_status,
    load_credentials,
    load_pending,
    login_urls,
    resolve_token,
    save_credentials,
    start_login,
    wait_for_approval,
)


@pytest.fixture(autouse=True)
def isolated_home(tmp_path, monkeypatch):
    home = tmp_path / "devflow-home"
    monkeypatch.setenv("DEVFLOW_HOME", str(home))
    for name in ("STELLARCODE_TOKEN", "STELLAR_MCP_TOKEN", "STELLAR_ENV", "STELLAR_API_URL", "STELLAR_WEB_URL", "CUSTOM_TOKEN"):
        monkeypatch.delenv(name, raising=False)
    return home


def _future(hours=24):
    return datetime.now(timezone.utc) + timedelta(hours=hours)


def test_credentials_roundtrip_is_private_and_compatible(isolated_home):
    path = save_credentials("tok.abc", "https://api.example/mcp", _future())
    assert path == isolated_home / "stellar.env"
    text = path.read_text()
    assert "export STELLAR_MCP_TOKEN='tok.abc'" in text  # same format as StellarCode `npm run devflow:login`
    if os.name == "posix":
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
    creds = load_credentials()
    assert creds["token"] == "tok.abc"
    assert creds["mcp_url"] == "https://api.example/mcp"


def test_resolution_prefers_env_then_file_and_ignores_expired(monkeypatch):
    assert resolve_token().token is None
    save_credentials("from-file", "https://api.example/mcp", _future())
    assert resolve_token().source.startswith("file:")
    monkeypatch.setenv("STELLAR_MCP_TOKEN", "from-env")
    assert resolve_token().token == "from-env"
    monkeypatch.setenv("CUSTOM_TOKEN", "custom")
    assert resolve_token("CUSTOM_TOKEN").token == "custom"
    monkeypatch.delenv("STELLAR_MCP_TOKEN")
    monkeypatch.delenv("CUSTOM_TOKEN")
    save_credentials("old", "https://api.example/mcp", _future(-1))
    res = resolve_token()
    assert res.token is None and res.expired_path
    assert auth_status()["reason"] == "expired"


def test_stellar_token_uses_login_store_and_explains_how_to_login():
    with pytest.raises(StellarError, match="devflow stellar-login"):
        stellar_token({"auth": {"token_env": "STELLARCODE_TOKEN"}})
    save_credentials("stored", "https://api.example/mcp", _future())
    assert stellar_token({"auth": {"token_env": "STELLARCODE_TOKEN"}}) == "stored"


def test_login_urls_send_unauthenticated_users_through_login_with_redirect():
    urls = login_urls("https://app.example/", "/admin/integrations/mcp/conectar?code=ABCD2345")
    assert urls["approve_url"] == "https://app.example/admin/integrations/mcp/conectar?code=ABCD2345"
    assert urls["login_url"] == "https://app.example/login?redirect=%2Fadmin%2Fintegrations%2Fmcp%2Fconectar%3Fcode%3DABCD2345"


class FakeHttp:
    def __init__(self, poll_responses):
        self.poll_responses = list(poll_responses)
        self.calls = []

    def __call__(self, url, body):
        self.calls.append((url, body))
        if url.endswith("/iniciar"):
            return 201, {"device_code": "d" * 64, "user_code": "ABCD-2345", "verification_path": "/admin/integrations/mcp/conectar?code=ABCD2345", "expires_in": 600, "interval": 2}
        return self.poll_responses.pop(0)


def test_device_flow_stores_token_after_approval():
    http = FakeHttp([(202, {"estado": "pendiente"}), (200, {"estado": "aprobada", "token": "jwt.x.y", "mcp_url": "https://api.example/mcp", "expires_in_hours": 12, "writes_enabled": True})])
    pending = start_login(api_url="https://api.example", web_url="https://app.example", client_name="DevFlow test", hours=99, http=http)
    assert http.calls[0][1] == {"nombre": "DevFlow test", "horas": 24}
    assert load_pending()["user_code"] == "ABCD-2345"
    sleeps = []
    result = wait_for_approval(pending, http=http, sleep=sleeps.append)
    assert result["status"] == "approved" and result["writes_enabled"] is True
    assert sleeps == [2]
    assert load_credentials()["token"] == "jwt.x.y"
    assert load_pending() is None


def test_device_flow_timeout_keeps_pending_and_denial_raises():
    http = FakeHttp([(202, {"estado": "pendiente"})])
    pending = start_login(api_url="https://api.example", web_url="https://app.example", client_name="x", http=http)
    result = wait_for_approval(pending, http=http, timeout=0, sleep=lambda _: None)
    assert result["status"] == "pending" and "device_code" not in result
    assert load_pending() is not None

    http.poll_responses = [(403, {"estado": "denegada"})]
    with pytest.raises(StellarAuthError, match="denied"):
        wait_for_approval(pending, http=http, sleep=lambda _: None)
    assert load_pending() is None


class _FakeStellar(BaseHTTPRequestHandler):
    polls = 0

    def log_message(self, *args):
        pass

    def do_POST(self):
        length = int(self.headers.get("content-length") or 0)
        json.loads(self.rfile.read(length) or b"{}")
        if self.path == "/api/mcp-connect/iniciar":
            status, body = 201, {"device_code": "e" * 64, "user_code": "WXYZ-6789", "verification_path": "/admin/integrations/mcp/conectar?code=WXYZ6789", "expires_in": 600, "interval": 1}
        elif self.path == "/api/mcp-connect/token":
            type(self).polls += 1
            status, body = (200, {"estado": "aprobada", "token": "jwt.real", "mcp_url": "http://stellar.test/mcp", "expires_in_hours": 24, "writes_enabled": False})
        else:
            status, body = 404, {"error": "not found"}
        raw = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)


@pytest.fixture
def fake_stellar():
    server = HTTPServer(("127.0.0.1", 0), _FakeStellar)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}"
    server.shutdown()


def test_cli_agent_two_step_login_and_bind(tmp_path, fake_stellar, capsys):
    project = tmp_path / "proj"
    project.mkdir()
    (project / ".devflow.yml").write_text(yaml.safe_dump({"version": 2, "project": {"name": "Demo"}}), encoding="utf-8")

    assert main(["stellar-login", "--target", str(project), "--api", fake_stellar, "--web", "https://app.test", "--no-wait", "--json"]) == 0
    ticket = json.loads(capsys.readouterr().out)
    assert ticket["status"] == "pending"
    assert ticket["user_code"] == "WXYZ-6789"
    assert ticket["login_url"].startswith("https://app.test/login?redirect=")
    assert "device_code" not in ticket

    assert main(["/inicio", "--hook", "--target", str(project)]) == 0
    assert "Login pendiente: código WXYZ-6789" in capsys.readouterr().out

    assert main(["stellar-login", "--wait", "--target", str(project), "--project-id", "77"]) == 0
    out = capsys.readouterr().out
    assert "Conectado a StellarCode" in out and "jwt.real" not in out
    cfg = yaml.safe_load((project / ".devflow.yml").read_text(encoding="utf-8"))
    assert cfg["stellarcode"]["project_id"] == 77
    assert "jwt.real" not in (project / ".devflow.yml").read_text(encoding="utf-8")

    assert main(["stellar-auth", "--target", str(project)]) == 0
    assert main(["logout"]) == 0
    assert main(["stellar-auth", "--target", str(project)]) == 6


def test_inicio_prints_agent_protocol_when_logged_out(tmp_path, capsys):
    assert main(["inicio", "--hook", "--target", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "AGENT LOGIN PROTOCOL" in out and "stellar-login --no-wait --json" in out


def test_install_session_hook_is_idempotent(tmp_path):
    settings = tmp_path / ".claude" / "settings.json"
    settings.parent.mkdir()
    settings.write_text(json.dumps({"permissions": {"allow": ["Bash(ls:*)"]}}))
    path, created = install_session_hook(tmp_path)
    assert created
    _, created_again = install_session_hook(tmp_path)
    assert not created_again
    data = json.loads(path.read_text())
    assert data["permissions"]["allow"] == ["Bash(ls:*)"]
    assert len(data["hooks"]["SessionStart"]) == 1
    assert "devflow inicio --hook" in data["hooks"]["SessionStart"][0]["hooks"][0]["command"]
