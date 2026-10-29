"""Pure economy helpers for Idle Clicker.

No Tkinter import: recommendations and progress estimates can be tested offline.
Advisory only: never buys an upgrade automatically.
"""
from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class PurchaseAdvice:
    name: str
    cost: float
    extra_cps: float
    seconds_until_affordable: float | None
    payback_seconds: float


def cost_of_next(base_cost: float, growth: float, owned: int) -> float:
    """Cost of one additional unit. Invalid / overflowing data are unavailable."""
    if (
        not math.isfinite(base_cost) or base_cost <= 0
        or not math.isfinite(growth) or growth < 1
        or type(owned) is not int or owned < 0
    ):
        return math.inf
    try:
        value = base_cost * growth ** owned
    except (OverflowError, ValueError):
        return math.inf
    return float(round(value)) if math.isfinite(value) else math.inf


def recommend_purchase(upgrades, owned: dict, gold: float, cps: float,
                       prestige_multiplier: float = 1.0) -> PurchaseAdvice | None:
    """Rank options by deterministic payback; never claim speculative future gains.

    upgrades: tuples (name, base_cost, growth, per-unit CPS).
    Waiting time assumes current CPS is stable and zero manual clicks.
    Ranking looks at purchase payback alone and reports waiting separately.
    """
    if not all(math.isfinite(v) for v in (gold, cps, prestige_multiplier)):
        return None
    if gold < 0 or cps < 0 or prestige_multiplier <= 0:
        return None
    options = []
    for name, base, growth, unit_cps in upgrades:
        if not isinstance(name, str) or not name or not math.isfinite(unit_cps) or unit_cps <= 0:
            continue
        cost = cost_of_next(base, growth, owned.get(name, 0))
        gain = unit_cps * prestige_multiplier
        if not math.isfinite(cost) or not math.isfinite(gain) or gain <= 0:
            continue
        seconds = 0.0 if cost <= gold else (cost - gold) / cps if cps > 0 else None
        payback = cost / gain
        if math.isfinite(payback) and (seconds is None or math.isfinite(seconds)):
            options.append(PurchaseAdvice(name, cost, gain, seconds, payback))
    return min(options, key=lambda item: (item.payback_seconds, item.cost, item.name)) if options else None


def describe_advice(advice: PurchaseAdvice | None, fmt=None) -> str:
    """Display enough context to avoid presenting ROI as a guaranteed gain."""
    if advice is None:
        return "Conseil : données économiques indisponibles."
    if fmt is None:
        fmt = lambda value: str(round(value, 2))
    if advice.seconds_until_affordable is None:
        eta = "à financer par clics (CPS nul)"
    elif advice.seconds_until_affordable == 0:
        eta = "achetable maintenant"
    else:
        eta = f"accessible dans ≈ {format_duration(advice.seconds_until_affordable)} sans clic"
    return (f"Meilleur retour CPS : {advice.name} ({fmt(advice.cost)} or, "
            f"+{fmt(advice.extra_cps)} CPS) · {eta} · "
            f"amortissement ≈ {format_duration(advice.payback_seconds)}")


def format_duration(seconds: float) -> str:
    if not math.isfinite(seconds) or seconds < 0:
        return "inconnu"
    if seconds < 60:
        return f"{max(1, math.ceil(seconds))} s"
    if seconds < 3600:
        return f"{max(1, math.ceil(seconds / 60))} min"
    if seconds < 86400:
        return f"{max(1, math.ceil(seconds / 3600))} h"
    return f"{max(1, math.ceil(seconds / 86400))} j"
