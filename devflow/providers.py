from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Protocol


class CapabilityClass(str, Enum):
    READ_ONLY = "read_only"
    SHARED_REVERSIBLE = "shared_reversible"
    CONSEQUENTIAL = "consequential"


class ProviderErrorCode(str, Enum):
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    RATE_LIMITED = "RATE_LIMITED"
    TIMEOUT = "TIMEOUT"
    PROVIDER_UNAVAILABLE = "PROVIDER_UNAVAILABLE"
    INVALID_INPUT = "INVALID_INPUT"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    UNSUPPORTED_CAPABILITY = "UNSUPPORTED_CAPABILITY"


@dataclass(slots=True)
class ProviderError:
    code: str
    message: str
    retryable: bool = False
    details: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class ProviderResult:
    ok: bool
    provider: str
    operation: str
    timestamp: str
    data: dict[str, Any] = field(default_factory=dict)
    evidence: list[dict[str, Any]] = field(default_factory=list)
    resource_id: str | None = None
    request_id: str | None = None
    error: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class Provider(Protocol):
    id: str
    version: str

    def capabilities(self) -> set[str]: ...
    def connect(self) -> None: ...
    def health(self) -> ProviderResult: ...
    def read(self, operation: str, input: dict[str, Any]) -> ProviderResult: ...
    def execute(self, operation: str, input: dict[str, Any], approval_context: dict[str, Any] | None = None) -> ProviderResult: ...
    def evidence(self, operation: str, result: ProviderResult) -> list[dict[str, Any]]: ...


def supports(provider: Provider, capability: str) -> bool:
    return capability in provider.capabilities()


def require_capability(provider: Provider, capability: str) -> None:
    if not supports(provider, capability):
        raise ValueError(f"{ProviderErrorCode.UNSUPPORTED_CAPABILITY.value}: {provider.id} lacks {capability}")
