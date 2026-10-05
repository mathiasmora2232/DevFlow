from __future__ import annotations

from typing import Any


def _alignment(actual: str, pref: dict) -> tuple[int | None, str]:
    if not actual or actual == "none":
        return None, "No aplica/no detectado"
    primary = pref.get("primary")
    alternatives = pref.get("alternatives", []) or []
    if actual == primary:
        return 100, "Coincide con el estándar primario"
    if actual in alternatives:
        return 85, "Está dentro de las alternativas aceptadas"
    return 70, "Fuera del estándar preferido, pero no implica mala calidad"


def evaluate_stack_fit(detected: dict, config: dict) -> dict[str, Any]:
    stack = config.get("stack", {})
    components = []
    for key in ["backend", "frontend", "database"]:
        score, reason = _alignment(detected.get(key, "none"), stack.get(key, {}))
        components.append({"component": key, "actual": detected.get(key, "none"), "score": score, "reason": reason})

    component_scores = [x["score"] for x in components if x["score"] is not None]
    personal_alignment = round(sum(component_scores) / len(component_scores), 1) if component_scores else 70.0

    infra = set(detected.get("infra", []))
    project = config.get("project", {})
    stage = project.get("stage", "mvp")
    budget = project.get("budget_profile", "lean")
    proportionality = 90.0
    warnings = []
    if stage in {"prototype", "mvp"} and budget == "lean" and ("kubernetes" in infra or "k3s" in infra):
        proportionality -= 20
        warnings.append("Orquestación Kubernetes/k3s puede ser prematura para un MVP lean; justificar necesidad real.")
    if "docker" in infra:
        proportionality += 3
    proportionality = max(0, min(100, proportionality))

    dimensions = {
        "personal_alignment": personal_alignment,
        "team_familiarity": 80.0,
        "project_fit": proportionality,
        "operating_cost": 85.0 if budget == "lean" else 80.0,
        "delivery_speed": 85.0,
        "ecosystem_and_support": 85.0,
        "migration_cost": 80.0,
        "future_flexibility": 85.0,
    }
    weights = {
        "personal_alignment": 25, "team_familiarity": 15, "project_fit": 25,
        "operating_cost": 10, "delivery_speed": 10, "ecosystem_and_support": 5,
        "migration_cost": 5, "future_flexibility": 5,
    }
    total = sum(dimensions[k] * weights[k] for k in weights) / sum(weights.values())
    if total >= 80: recommendation = "keep"
    elif total >= 65: recommendation = "keep_with_improvements"
    elif total >= 45: recommendation = "evaluate_partial_migration"
    else: recommendation = "migration_candidate"
    return {
        "score": round(total, 1), "recommendation": recommendation,
        "dimensions": dimensions, "components": components, "warnings": warnings,
    }
