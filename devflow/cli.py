from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
import yaml

from . import __version__
from .audit import audit_project
from .config import build_config, load_config, save_config
from .config_schema import config_summary, migrate_config_file, validate_config
from .findings import load_findings, normalize_legacy_finding, reconcile_findings, save_findings, update_finding_status
from .gates import evaluate_gate
from .detector import detect_stack
from .doctor import doctor_project, doctor_markdown
from .docs_audit import audit_docs, docs_markdown
from .secrets_scan import scan_secrets, secrets_markdown, should_fail
from .report import audit_markdown, stack_review_markdown
from .scoring import weighted_score, evidence_confidence
from .stackfit import evaluate_stack_fit
from .trace import ensure_ops, sync_trace, next_work_id, add_work
from .stellar import StellarError, bind_project, call_tool as stellar_call_tool, choose_next_task, stellar_config, write_stellar_snapshot
from .utils import slugify

ALIASES = {
    "/nuevo-proyecto": "nuevo-proyecto", "init": "nuevo-proyecto",
    "/auditar": "auditar", "audit": "auditar",
    "/puntuar": "puntuar", "score": "puntuar",
    "/revisar-stack": "revisar-stack", "stack-review": "revisar-stack",
    "/planificar": "planificar", "plan": "planificar",
    "/traza": "traza", "trace": "traza",
    "/estado": "estado", "status": "estado",
    "/detectar": "detectar", "detect": "detectar",
    "/doctor": "doctor",
    "/docs": "docs",
    "/secretos": "secretos", "secrets": "secretos",
    "/stellar-status": "stellar-status",
    "/proyectos": "stellar-projects", "projects": "stellar-projects",
    "/roles": "roles",
    "/miembros": "miembros", "members": "miembros",
    "/decision": "decision", "decision": "decision",
    "/kanban": "kanban",
    "/siguiente": "siguiente", "next": "siguiente",
    "/validar": "validate", "validate": "validate",
    "/findings": "findings", "findings": "findings",
    "/gate": "gate", "gate": "gate",
}


def _target(value: str) -> Path:
    return Path(value).expanduser().resolve()


def _ask(label: str, default: str, choices: list[str] | None = None) -> str:
    options = f" [{'/'.join(choices)}]" if choices else ""
    raw = input(f"{label}{options} ({default}): ").strip()
    value = raw or default
    if choices and value not in choices:
        print(f"Valor no reconocido; usando {default}.")
        return default
    return value


def cmd_init(args) -> int:
    root = _target(args.target); root.mkdir(parents=True, exist_ok=True)
    detected = detect_stack(root)
    name = args.name or root.name
    if args.non_interactive:
        answers = {
            "stage": args.stage or "mvp", "type": args.type or detected.get("project_type", "fullstack"),
            "criticality": args.criticality or "medium", "traffic": args.traffic or "unknown",
            "budget": args.budget or "lean", "backend": args.backend or detected.get("backend", "none"),
            "frontend": args.frontend or detected.get("frontend", "none"), "database": args.database or detected.get("database", "none"),
            "edge": args.edge, "orchestration": args.orchestration,
        }
    else:
        print("\nDevFlow /nuevo-proyecto — usa Enter para aceptar la detección/default.\n")
        name = _ask("Nombre", name)
        answers = {
            "stage": _ask("Etapa", "mvp", ["prototype","mvp","growth","production","legacy"]),
            "type": _ask("Tipo", detected.get("project_type", "fullstack"), ["frontend","backend","fullstack","api","mobile","infra","monorepo","unknown"]),
            "criticality": _ask("Criticidad", "medium", ["low","medium","high","critical"]),
            "traffic": _ask("Tráfico esperado", "unknown"),
            "budget": _ask("Perfil de presupuesto", "lean", ["lean","balanced","flexible"]),
            "backend": _ask("Backend", detected.get("backend", "none"), ["fastapi","go","nodejs","quarkus","php","none","other"]),
            "frontend": _ask("Frontend", detected.get("frontend", "none"), ["angular","nextjs","react","javascript","none","other"]),
            "database": _ask("Base de datos", detected.get("database", "none"), ["postgresql","mariadb","sqlite","none","other"]),
            "edge": _ask("Edge", "cloudflare" if "cloudflare" in detected.get("infra",[]) else "none", ["cloudflare","none","other"]),
            "orchestration": _ask("Orquestación", "k3s" if "k3s" in detected.get("infra",[]) else "kubernetes" if "kubernetes" in detected.get("infra",[]) else "none", ["none","k3s","kubernetes","other"]),
        }
    cfg = build_config(name, detected, answers)
    path = root / ".devflow.yml"
    if path.exists() and not args.force:
        print(f"ERROR: {path} ya existe. Usa --force solo si deseas reemplazarlo.")
        return 2
    save_config(root, cfg, overwrite=args.force)
    ensure_ops(root)
    sync_trace(root)
    print(f"DevFlow inicializado en {root}")
    print(f"Stack detectado: backend={detected['backend']} frontend={detected['frontend']} db={detected['database']}")
    if answers.get("stage") in {"prototype","mvp"} and answers.get("budget") == "lean" and answers.get("orchestration") in {"kubernetes","k3s"}:
        print("ADVERTENCIA: orquestación Kubernetes/k3s en MVP lean requiere justificación de carga/operación.")
    return 0


def _require_config(root: Path) -> dict:
    cfg = load_config(root)
    if not cfg:
        raise SystemExit("No existe .devflow.yml. Ejecuta `devflow /nuevo-proyecto` primero.")
    return cfg


def cmd_detect(args) -> int:
    root = _target(args.target)
    print(yaml.safe_dump(detect_stack(root), sort_keys=False, allow_unicode=True))
    return 0


def cmd_audit(args) -> int:
    root = _target(args.target); cfg = _require_config(root)
    result = audit_project(root, cfg)

    project_slug = cfg.get("project", {}).get("slug") or root.name
    raw_findings = result.get("findings", [])
    current = [
        item if item.get("fingerprint") else normalize_legacy_finding(item, project_slug)
        for item in raw_findings
    ]
    merged, finding_stats = reconcile_findings(load_findings(root), current)
    save_findings(root, merged)
    merged_by_fp = {item.get("fingerprint"): item for item in merged if item.get("fingerprint")}
    result["findings"] = [
        merged_by_fp.get(item.get("fingerprint"), item)
        for item in current
    ]
    result["finding_reconciliation"] = finding_stats
    result["finding_history_file"] = "ops/findings.json"

    reports = root / "ops" / "reports"; reports.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    json_path = reports / f"audit-{stamp}.json"
    md_path = reports / f"audit-{stamp}.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(audit_markdown(result), encoding="utf-8")
    (reports / "latest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    (reports / "latest.md").write_text(audit_markdown(result), encoding="utf-8")
    sync_trace(root)
    print(f"Health: {result['project_health_score']}/100")
    print(f"Stack Fit: {result['stack_fit_score']}/100")
    print(f"Evidence Confidence: {result['evidence_confidence']}/100")
    print(f"Findings: new={finding_stats['new']} persistent={finding_stats['persistent']} fixed={finding_stats['fixed']} regressed={finding_stats['regressed']}")
    print(f"Report: {md_path}")
    return 0


def cmd_score(args) -> int:
    root = _target(args.target); _require_config(root)
    latest = root / "ops" / "reports" / "latest.json"
    if not latest.exists() or args.refresh:
        return cmd_audit(argparse.Namespace(target=str(root)))
    result = json.loads(latest.read_text(encoding="utf-8"))
    print(json.dumps({
        "project_health_score": result.get("project_health_score"),
        "stack_fit_score": result.get("stack_fit_score"),
        "evidence_confidence": result.get("evidence_confidence"),
        "unknowns": result.get("unknowns", []),
    }, indent=2, ensure_ascii=False))
    return 0


def cmd_stack(args) -> int:
    root = _target(args.target); cfg = _require_config(root)
    detected = detect_stack(root); fit = evaluate_stack_fit(detected, cfg)
    reports = root / "ops" / "reports"; reports.mkdir(parents=True, exist_ok=True)
    out = reports / "stack-review.md"
    out.write_text(stack_review_markdown(detected, fit), encoding="utf-8")
    print(f"Stack Fit: {fit['score']}/100 — {fit['recommendation']}")
    for w in fit["warnings"]: print(f"WARN: {w}")
    print(f"Report: {out}")
    return 0


def cmd_plan(args) -> int:
    root = _target(args.target); cfg = _require_config(root)
    prefix = cfg.get("trace", {}).get("id_prefix", "DEV")
    wid = next_work_id(root, prefix)
    acceptance = args.acceptance or []
    external_ref = None

    if getattr(args, "stellar", False):
        try:
            stellar = stellar_config(root)
            remote = stellar_call_tool(root, "create_roadmap_task", {
                "project_id": int(stellar["project_id"]),
                "title": args.title,
                "description": (args.description or args.title) + (
                    "\n\nAcceptance criteria:\n" + "\n".join(f"- {item}" for item in acceptance)
                    if acceptance else ""
                ),
                "priority": args.priority,
                "status": "pending",
                "task_key": wid,
            })
            task = remote.get("task") or remote.get("roadmap_task") or remote
            external_ref = task.get("id") if isinstance(task, dict) else None
            print(f"StellarCode task created: {wid}" + (f" (id={external_ref})" if external_ref else ""))
        except StellarError as exc:
            print(f"ERROR: {exc}")
            return 5

    description = args.description or args.title
    if external_ref:
        description += f"\n\nStellarCode task id: {external_ref}"
    add_work(root, wid, args.title, args.type, args.priority, description, acceptance)
    print(f"Created {wid}: {args.title}")
    return 0


def cmd_trace(args) -> int:
    root = _target(args.target); _require_config(root)
    info = sync_trace(root, args.environment)
    print(f"Trace synchronized: branch={info['branch']} revision={info['revision']} dirty={info['dirty']}")
    if getattr(args, "stellar", False):
        try:
            stellar = stellar_config(root)
            identity = stellar_call_tool(root, "get_mcp_identity", {"project_id": int(stellar["project_id"])})
            board = stellar_call_tool(root, "list_project_tasks", {"project_id": int(stellar["project_id"])})
            path = write_stellar_snapshot(root, {"identity": identity, "tasks": board.get("tasks", [])})
            print(f"Stellar snapshot: {path}")
        except StellarError as exc:
            print(f"WARN: Stellar sync failed: {exc}")
            return 5
    return 0


def _write_named_report(root: Path, prefix: str, result: dict, markdown: str) -> tuple[Path, Path]:
    reports = root / "ops" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    json_path = reports / f"{prefix}-{stamp}.json"
    md_path = reports / f"{prefix}-{stamp}.md"
    json_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    (reports / f"{prefix}-latest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    (reports / f"{prefix}-latest.md").write_text(markdown, encoding="utf-8")
    return json_path, md_path


def cmd_doctor(args) -> int:
    root = _target(args.target)
    result = doctor_project(root)
    _, md_path = _write_named_report(root, "doctor", result, doctor_markdown(result))
    print(f"Readiness: {result['readiness_score']}/100 — {'READY' if result['ready'] else 'BLOCKED'}")
    print(f"Free disk: {result['free_disk_gb']} GB")
    for blocker in result["blockers"]:
        print(f"BLOCKER: {blocker['name']} — {blocker['detail']}")
    for warning in result["warnings"]:
        print(f"WARN: {warning['name']} — {warning['detail']}")
    print(f"Report: {md_path}")
    return 2 if args.strict and not result["ready"] else 0


def cmd_docs(args) -> int:
    root = _target(args.target)
    result = audit_docs(root)
    _, md_path = _write_named_report(root, "docs", result, docs_markdown(result))
    print(f"Documentation: {result['documentation_score']}/100")
    for finding in result["findings"]:
        print(f"{finding['severity'].upper()}: {finding['id']} — {finding['message']}")
    print(f"Report: {md_path}")
    if args.min_score is not None and result["documentation_score"] < args.min_score:
        return 3
    return 0


def cmd_secrets(args) -> int:
    root = _target(args.target)
    result = scan_secrets(root)
    _, md_path = _write_named_report(root, "secrets", result, secrets_markdown(result))
    counts = result["counts"]
    print(f"Secret Hygiene: {result['secret_hygiene_score']}/100")
    print(f"Findings: critical={counts['critical']} high={counts['high']} medium={counts['medium']} low={counts['low']}")
    for finding in result["findings"][:20]:
        loc = f"{finding['file']}:{finding['line']}" if finding.get("line") else finding["file"]
        print(f"{finding['severity'].upper()}: {finding['id']} — {loc} — {finding['preview']}")
    if len(result["findings"]) > 20:
        print(f"... {len(result['findings']) - 20} more findings in report")
    print(f"Report: {md_path}")
    return 4 if should_fail(result, args.fail_on) else 0


def cmd_stellar_bind(args) -> int:
    root = _target(args.target); _require_config(root)
    try:
        path = bind_project(root, args.project_id, args.url, args.token_env)
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5
    print(f"StellarCode bound: project_id={args.project_id}")
    print(f"Config: {path}")
    print(f"Token env: {args.token_env}")
    return 0


def cmd_stellar_status(args) -> int:
    root = _target(args.target)
    try:
        stellar = stellar_config(root)
        identity = stellar_call_tool(root, "get_mcp_identity", {"project_id": int(stellar["project_id"])})
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5
    user = identity.get("user", {})
    print("STELLARCODE MCP")
    print(f"User: {user.get('name') or user.get('email') or 'unknown'}")
    print(f"Global role: {user.get('global_role') or 'unknown'}")
    print(f"Project ID: {identity.get('project_id')}")
    print(f"Project role: {identity.get('project_role') or 'global_admin'}")
    print(f"Client: {identity.get('client') or 'unknown'}")
    permissions = identity.get("permissions", [])
    if permissions:
        print("Permissions:")
        for permission in permissions:
            print(f"  - {permission}")
    return 0


def cmd_stellar_projects(args) -> int:
    root = _target(args.target)
    try:
        projects = stellar_call_tool(root, "list_my_projects", {}, require_project=False).get("projects", [])
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5
    if not projects:
        print("No accessible StellarCode projects.")
        return 0
    for project in projects:
        print(f"{project.get('id')} | {project.get('title','')} | {project.get('status','unknown')} | role={project.get('role','unknown')} | progress={project.get('progress','-')}")
    return 0


def cmd_roles(args) -> int:
    root = _target(args.target)
    try:
        roles = stellar_call_tool(root, "list_project_roles", {}, require_project=False).get("roles", [])
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5
    for role in roles:
        permissions = role.get("permissions", [])
        if isinstance(permissions, str):
            permissions = [permissions]
        print(f"{role.get('role_key')} — {role.get('name') or ''}")
        for permission in permissions:
            print(f"  - {permission}")
    return 0


def cmd_members(args) -> int:
    root = _target(args.target)
    try:
        stellar = stellar_config(root)
        project_id = int(stellar["project_id"])

        if args.action == "list":
            members = stellar_call_tool(root, "list_project_members", {"project_id": project_id}).get("members", [])
            for member in members:
                print(f"{member.get('user_id')} | {member.get('name') or member.get('email')} | {member.get('role')}")
            return 0

        if args.user_id is None:
            print("ERROR: member mutation requires --user-id")
            return 2

        if args.action == "add":
            if not args.role:
                print("ERROR: miembros add requires --role")
                return 2
            result = stellar_call_tool(root, "add_project_member", {
                "project_id": project_id,
                "user_id": args.user_id,
                "role": args.role,
            })
            print(f"Member {args.user_id} added/updated as {args.role}")
            return 0 if result.get("ok", True) else 5

        if args.action == "role":
            if not args.role:
                print("ERROR: miembros role requires --role")
                return 2
            result = stellar_call_tool(root, "update_project_member_role", {
                "project_id": project_id,
                "user_id": args.user_id,
                "role": args.role,
            })
            print(f"Member {args.user_id} role -> {args.role}")
            return 0 if result.get("ok", True) else 5

        if args.action == "remove":
            result = stellar_call_tool(root, "remove_project_member", {
                "project_id": project_id,
                "user_id": args.user_id,
            })
            print(f"Member {args.user_id} removed={result.get('removed', True)}")
            return 0 if result.get("ok", True) else 5

        return 2
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5


def cmd_decision(args) -> int:
    root = _target(args.target)
    try:
        stellar = stellar_config(root)
        project_id = int(stellar["project_id"])
        if args.action == "list":
            decisions = stellar_call_tool(root, "list_project_decisions", {"project_id": project_id}).get("decisions", [])
            for item in decisions:
                print(f"{item.get('id')} | [{item.get('status','accepted')}] {item.get('title','')}")
            return 0

        if not args.title or not args.decision_text:
            print("ERROR: decision add requires --title and --decision")
            return 2
        result = stellar_call_tool(root, "add_project_decision", {
            "project_id": project_id,
            "title": args.title,
            "context": args.context,
            "decision": args.decision_text,
            "consequences": args.consequences,
            "status": args.status,
        })
        record = result.get("decision") or {}
        print(f"Decision recorded: {record.get('id','?')} — {args.title}")
        return 0 if result.get("ok", True) else 5
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5


def cmd_kanban(args) -> int:
    root = _target(args.target)
    try:
        stellar = stellar_config(root)
        project_id = int(stellar["project_id"])
        if args.action == "move":
            if args.task_id is None or not args.status:
                print("ERROR: kanban move requires --task-id and --status")
                return 2
            result = stellar_call_tool(root, "update_task_status", {"task_id": args.task_id, "status": args.status})
            print(f"Task {args.task_id} -> {args.status}")
            return 0 if result.get("ok", True) else 5

        board = stellar_call_tool(root, "list_project_tasks", {"project_id": project_id})
        tasks = board.get("tasks", [])
        print(f"KANBAN project={project_id} tasks={len(tasks)}")
        for task in tasks:
            key = task.get("task_key") or task.get("id")
            owner = task.get("assigned_to_name") or "-"
            print(f"[{task.get('status','unknown')}] [{task.get('priority','medium')}] {key} {task.get('title','')} @ {owner}")
        return 0
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5


def cmd_next(args) -> int:
    root = _target(args.target)
    try:
        stellar = stellar_config(root)
        board = stellar_call_tool(root, "list_project_tasks", {"project_id": int(stellar["project_id"])})
    except StellarError as exc:
        print(f"ERROR: {exc}")
        return 5
    task = choose_next_task(board.get("tasks", []))
    if not task:
        print("No actionable StellarCode task found.")
        return 0
    key = task.get("task_key") or task.get("id")
    print(f"Next: {key} — {task.get('title','')}")
    print(f"Status={task.get('status')} Priority={task.get('priority')}")
    return 0


def cmd_validate(args) -> int:
    root = _target(args.target)
    cfg = _require_config(root)
    errors = validate_config(cfg)
    if errors:
        for error in errors:
            print(f"ERROR {error['path']}: {error['message']}")
        return 6
    print(f"Config valid (schema={config_summary(cfg)['schema_version']})")
    return 0


def cmd_config(args) -> int:
    root = _target(args.target)
    if args.action == "show":
        cfg = _require_config(root)
        print(yaml.safe_dump(config_summary(cfg), sort_keys=False, allow_unicode=True))
        return 0
    if args.action == "migrate":
        try:
            result = migrate_config_file(root, check=args.check)
        except (FileNotFoundError, ValueError) as exc:
            print(f"ERROR: {exc}")
            return 6
        mode = "would migrate" if args.check and result["changed"] else "migrated" if result["changed"] else "already current"
        print(f"Config {mode}: schema {result['from']} -> {result['to']}")
        if args.check and result.get("diff"):
            print(result["diff"])
        if not args.check:
            errors = validate_config(result["config"])
            if errors:
                for error in errors:
                    print(f"ERROR {error['path']}: {error['message']}")
                return 6
        return 0
    return 2


def cmd_findings(args) -> int:
    root = _target(args.target)
    findings = load_findings(root)
    if args.action == "list":
        selected = findings
        if args.status:
            selected = [f for f in selected if f.get("status") == args.status]
        if args.severity:
            selected = [f for f in selected if f.get("severity") == args.severity]
        for finding in selected:
            print(f"{finding.get('id')} | {finding.get('severity')} | {finding.get('status')} | {finding.get('category')} | {finding.get('title')}")
        print(f"Total: {len(selected)}")
        return 0

    if not args.id or not args.status:
        print("ERROR: findings status requires --id and --status")
        return 2
    updated = update_finding_status(root, args.id, args.status, args.reason, args.approved_by, args.expires_at)
    if not updated:
        print(f"ERROR: finding not found: {args.id}")
        return 7
    print(f"{updated['id']} -> {updated['status']}")
    return 0


def cmd_gate(args) -> int:
    root = _target(args.target)
    cfg = _require_config(root)
    latest = root / "ops" / "reports" / "latest.json"
    audit = json.loads(latest.read_text(encoding="utf-8")) if latest.exists() else None
    evidence = {
        "tests": args.tests,
        "build": args.build,
        "rollback": args.rollback,
        "healthcheck": args.healthcheck,
        "verified_ci": args.verified_ci,
    }
    result = evaluate_gate(args.gate, cfg, audit, evidence)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0 if result.result in {"pass", "warn"} else 8


def cmd_status(args) -> int:
    root = _target(args.target); cfg = _require_config(root)
    detected = detect_stack(root)
    latest = root / "ops" / "reports" / "latest.json"
    audit = json.loads(latest.read_text(encoding="utf-8")) if latest.exists() else None
    from .utils import git_info
    git = git_info(root)
    print(f"Project: {cfg.get('project',{}).get('name', root.name)}")
    print(f"Git: {git['branch']} @ {git['revision']} dirty={git['dirty']}")
    print(f"Detected: backend={detected['backend']} frontend={detected['frontend']} db={detected['database']}")
    if audit:
        print(f"Health={audit.get('project_health_score')} StackFit={audit.get('stack_fit_score')} Confidence={audit.get('evidence_confidence')}")
    else:
        print("Audit: not generated. Run `devflow /auditar`.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="devflow", description="DevFlow Core CLI")
    p.add_argument("--version", action="version", version=f"devflow {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    init = sub.add_parser("nuevo-proyecto", help="Inicializa/adopta DevFlow")
    init.add_argument("--target", default="."); init.add_argument("--name"); init.add_argument("--force", action="store_true")
    init.add_argument("--non-interactive", action="store_true")
    init.add_argument("--stage"); init.add_argument("--type"); init.add_argument("--criticality"); init.add_argument("--traffic"); init.add_argument("--budget")
    init.add_argument("--backend"); init.add_argument("--frontend"); init.add_argument("--database"); init.add_argument("--edge"); init.add_argument("--orchestration")
    init.set_defaults(func=cmd_init)

    d = sub.add_parser("detectar", help="Detecta stack"); d.add_argument("--target", default="."); d.set_defaults(func=cmd_detect)
    doc = sub.add_parser("doctor", help="Diagnostica entorno y readiness"); doc.add_argument("--target", default="."); doc.add_argument("--strict", action="store_true"); doc.set_defaults(func=cmd_doctor)
    docs = sub.add_parser("docs", help="Audita documentación del proyecto"); docs.add_argument("--target", default="."); docs.add_argument("--min-score", type=float); docs.set_defaults(func=cmd_docs)
    sec = sub.add_parser("secretos", help="Busca posibles secretos sin mostrar valores completos"); sec.add_argument("--target", default="."); sec.add_argument("--fail-on", choices=["never","critical","high","medium","low"], default="never"); sec.set_defaults(func=cmd_secrets)
    a = sub.add_parser("auditar", help="Auditoría estática integral"); a.add_argument("--target", default="."); a.set_defaults(func=cmd_audit)
    s = sub.add_parser("puntuar", help="Muestra score actual"); s.add_argument("--target", default="."); s.add_argument("--refresh", action="store_true"); s.set_defaults(func=cmd_score)
    sr = sub.add_parser("revisar-stack", help="Evalúa Stack Fit"); sr.add_argument("--target", default="."); sr.set_defaults(func=cmd_stack)
    pl = sub.add_parser("planificar", help="Crea work item trazable"); pl.add_argument("title"); pl.add_argument("--target", default="."); pl.add_argument("--type", default="feature"); pl.add_argument("--priority", choices=["low","medium","high","critical"], default="medium"); pl.add_argument("--description", default=""); pl.add_argument("--acceptance", action="append"); pl.add_argument("--stellar", action="store_true", help="Crea primero la tarea en StellarCode MCP"); pl.set_defaults(func=cmd_plan)
    tr = sub.add_parser("traza", help="Sincroniza traza con Git"); tr.add_argument("--target", default="."); tr.add_argument("--environment", default="local"); tr.add_argument("--stellar", action="store_true", help="Sincroniza snapshot del Kanban/identidad"); tr.set_defaults(func=cmd_trace)
    sb = sub.add_parser("stellar-bind", help="Vincula el proyecto local con StellarCode MCP"); sb.add_argument("--target", default="."); sb.add_argument("--project-id", type=int, required=True); sb.add_argument("--url", default="https://api.stellarcodelabs.lat/mcp"); sb.add_argument("--token-env", default="STELLARCODE_TOKEN"); sb.set_defaults(func=cmd_stellar_bind)
    ss = sub.add_parser("stellar-status", help="Muestra identidad y permisos efectivos en StellarCode"); ss.add_argument("--target", default="."); ss.set_defaults(func=cmd_stellar_status)
    sp = sub.add_parser("stellar-projects", help="Lista proyectos accesibles al usuario StellarCode"); sp.add_argument("--target", default="."); sp.set_defaults(func=cmd_stellar_projects)
    rl = sub.add_parser("roles", help="Lista roles y permisos de proyecto"); rl.add_argument("--target", default="."); rl.set_defaults(func=cmd_roles)
    mb = sub.add_parser("miembros", help="Gestiona miembros y roles del proyecto vinculado"); mb.add_argument("action", nargs="?", choices=["list","add","role","remove"], default="list"); mb.add_argument("--target", default="."); mb.add_argument("--user-id", type=int); mb.add_argument("--role", choices=["owner","admin","manager","developer","reviewer","viewer"]); mb.set_defaults(func=cmd_members)
    dc = sub.add_parser("decision", help="Lista o registra decisiones ADR-style en StellarCode"); dc.add_argument("action", nargs="?", choices=["list","add"], default="list"); dc.add_argument("--target", default="."); dc.add_argument("--title"); dc.add_argument("--decision", dest="decision_text"); dc.add_argument("--context"); dc.add_argument("--consequences"); dc.add_argument("--status", choices=["proposed","accepted","superseded","rejected"], default="accepted"); dc.set_defaults(func=cmd_decision)
    kb = sub.add_parser("kanban", help="Consulta o mueve tareas del Kanban StellarCode"); kb.add_argument("action", nargs="?", choices=["list","move"], default="list"); kb.add_argument("--target", default="."); kb.add_argument("--task-id", type=int); kb.add_argument("--status", choices=["pending","in_progress","review","completed","blocked"]); kb.set_defaults(func=cmd_kanban)
    nx = sub.add_parser("siguiente", help="Recomienda la siguiente tarea del Kanban StellarCode"); nx.add_argument("--target", default="."); nx.set_defaults(func=cmd_next)
    vd = sub.add_parser("validate", help="Valida .devflow.yml contra el contrato actual"); vd.add_argument("--target", default="."); vd.set_defaults(func=cmd_validate)
    cf = sub.add_parser("config", help="Muestra o migra configuración DevFlow"); cf.add_argument("action", choices=["show","migrate"]); cf.add_argument("--target", default="."); cf.add_argument("--check", action="store_true"); cf.set_defaults(func=cmd_config)
    fd = sub.add_parser("findings", help="Consulta o actualiza lifecycle de findings"); fd.add_argument("action", nargs="?", choices=["list","status"], default="list"); fd.add_argument("--target", default="."); fd.add_argument("--id"); fd.add_argument("--status", choices=["open","acknowledged","planned","in_progress","fixed","verified","closed","accepted_risk","false_positive","suppressed"]); fd.add_argument("--severity", choices=["critical","high","medium","low","info"]); fd.add_argument("--reason"); fd.add_argument("--approved-by"); fd.add_argument("--expires-at"); fd.set_defaults(func=cmd_findings)
    gt = sub.add_parser("gate", help="Evalúa quality gate determinista"); gt.add_argument("gate", choices=["pull_request","staging","production","release"]); gt.add_argument("--target", default="."); gt.add_argument("--tests", action=argparse.BooleanOptionalAction, default=None); gt.add_argument("--build", action=argparse.BooleanOptionalAction, default=None); gt.add_argument("--rollback", action=argparse.BooleanOptionalAction, default=None); gt.add_argument("--healthcheck", action=argparse.BooleanOptionalAction, default=None); gt.add_argument("--verified-ci", dest="verified_ci", action=argparse.BooleanOptionalAction, default=None); gt.set_defaults(func=cmd_gate)
    st = sub.add_parser("estado", help="Resumen de estado"); st.add_argument("--target", default="."); st.set_defaults(func=cmd_status)
    return p


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv:
        argv[0] = ALIASES.get(argv[0], argv[0].lstrip("/") if argv[0].startswith("/") else argv[0])
        argv[0] = ALIASES.get(argv[0], argv[0])
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))
