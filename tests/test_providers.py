import pytest

from devflow.providers import ProviderRegistry, require_capability, supports


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


def test_provider_registry_requires_capability():
    registry = ProviderRegistry()
    registry.register(DemoProvider())
    assert registry.get("demo").id == "demo"
    assert registry.require("demo", "git.repo.read").id == "demo"
    with pytest.raises(ValueError, match="UNSUPPORTED_CAPABILITY"):
        registry.require("demo", "deploy.execute")
