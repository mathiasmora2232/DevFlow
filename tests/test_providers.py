import pytest

from devflow.providers import require_capability, supports


class DemoProvider:
    id = "demo"
    version = "1"

    def capabilities(self):
        return {"git.repo.read"}


def test_provider_capability_check():
    provider = DemoProvider()
    assert supports(provider, "git.repo.read")
    assert not supports(provider, "deploy.execute")


def test_require_capability_rejects_unsupported():
    with pytest.raises(ValueError, match="UNSUPPORTED_CAPABILITY"):
        require_capability(DemoProvider(), "deploy.execute")
