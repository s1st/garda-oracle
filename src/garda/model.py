"""Pure-Python scorer for the frozen Ora/Peler logistics (no sklearn/numpy).

Mirrors the walchensee shadow-classifier pattern: coefficients live in
``coeffs.py`` (auto-generated), scoring is a dot product, and the dashboard
gets a verdict plus the top signed feature contributions for the tooltip.
"""
from __future__ import annotations

import math
from typing import Any

from .coeffs import ORA, PELER
from .features import FEATURE_DETAILS, FEATURE_LABELS
from .i18n import format_number, language

_BLOCKS: dict[str, dict[str, Any]] = {"ora": ORA, "peler": PELER}


def score(regime: str, features: dict[str, float]) -> float:
    """Platt-calibrated probability (calibrated on forecast-feature data)."""
    b = _BLOCKS[regime]
    z = b["intercept"]
    for name, mu, sd, w in zip(b["features"], b["mean"], b["std"], b["coef"]):
        z += w * ((features[name] - mu) / sd)
    z = b["platt_a"] * z + b["platt_b"]
    return 1.0 / (1.0 + math.exp(-z))


def verdict(regime: str, prob: float) -> str:
    b = _BLOCKS[regime]
    if prob >= b["threshold_go"]:
        return "GO"
    if prob >= b["threshold_maybe"]:
        return "MAYBE"
    return "NO_GO"


def top_drivers(
    regime: str, features: dict[str, float], n: int = 3, *, lang: str = "de"
) -> list[dict]:
    """Top-n contributions to the logit, signed (+ pushes toward wind)."""
    b = _BLOCKS[regime]
    lang = language(lang)
    labels = FEATURE_LABELS[lang]
    details = FEATURE_DETAILS[lang]
    contribs = []
    for name, mu, sd, w in zip(b["features"], b["mean"], b["std"], b["coef"]):
        c = w * ((features[name] - mu) / sd)
        unit, explanation = details.get(
            name, ("", "Dieser Wetterfaktor fließt in die statistische Vorhersage ein.")
        )
        value = features[name]
        contribs.append({"feature": name, "label": labels.get(name, name),
                         "contribution": round(c, 3), "value": round(value, 1),
                         "value_display": f"{format_number(lang, value, 1)} {unit}".strip(),
                         "explanation": explanation})
    contribs.sort(key=lambda d: -abs(d["contribution"]))
    return contribs[:n]


def classify(regime: str, features: dict[str, float], *, lang: str = "de") -> dict:
    p = score(regime, features)
    all_drivers = top_drivers(
        regime, features, n=len(_BLOCKS[regime]["features"]), lang=lang
    )
    return {"regime": regime, "probability": round(p, 3), "verdict": verdict(regime, p),
            "drivers": all_drivers[:3], "other_drivers": all_drivers[3:]}
