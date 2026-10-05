from __future__ import annotations

from typing import Any

DEFAULT_WEIGHTS = {
    "security": 16, "architecture": 10, "code_quality": 10, "maintainability": 8,
    "duplication": 5, "dead_code": 4, "testing": 10, "performance": 8,
    "server_load": 5, "seo": 5, "accessibility": 3, "database": 5,
    "devops": 4, "observability": 3, "resilience": 2, "dependencies": 1,
    "documentation": 1,
}


def weighted_score(categories: list[dict[str, Any]], weights: dict[str, int] | None = None) -> float | None:
    weights = weights or DEFAULT_WEIGHTS
    total_weight = 0.0
    points = 0.0
    for c in categories:
        score = c.get("score")
        if score is None:
            continue
        w = float(weights.get(c["id"], c.get("weight", 1)))
        total_weight += w
        points += float(score) * w
    if not total_weight:
        return None
    return round(points / total_weight, 1)


def evidence_confidence(categories: list[dict[str, Any]]) -> float:
    applicable = [c for c in categories if c.get("applicable", True)]
    if not applicable:
        return 0.0
    weighted = 0.0
    total = 0.0
    for c in applicable:
        w = float(DEFAULT_WEIGHTS.get(c["id"], 1))
        total += w
        weighted += float(c.get("confidence", 0)) * w
    return round(weighted / total, 1) if total else 0.0


def cap_for_critical_security(score: float | None, findings: list[dict]) -> float | None:
    if score is None:
        return None
    if any(f.get("severity") == "critical" and f.get("category") == "security" for f in findings):
        return min(score, 49.0)
    return score
