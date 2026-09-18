from __future__ import annotations

from statistics import mean


def signal_from_prices(prices: list[float]) -> dict:
    """Transparent baseline: latest 5 samples vs latest 20 samples."""
    if len(prices) < 20:
        return {
            "signal": "WARMUP",
            "fast": None,
            "slow": None,
            "reason": f"Need 20 samples; have {len(prices)}.",
        }

    fast = mean(prices[-5:])
    slow = mean(prices[-20:])
    delta = fast / slow - 1 if slow else 0.0

    if delta > 0.003:
        signal = "BUY"
        reason = "MA5 > MA20 by more than 0.3%."
    elif delta < -0.003:
        signal = "SELL"
        reason = "MA5 < MA20 by more than 0.3%."
    else:
        signal = "WAIT"
        reason = "MA5 and MA20 remain within the 0.3% band."

    return {
        "signal": signal,
        "fast": fast,
        "slow": slow,
        "delta": delta,
        "reason": reason,
    }
