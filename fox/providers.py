from __future__ import annotations

import json
import random
import urllib.request


class ShowcaseProvider:
    """Deterministic local quote source. No network access."""

    def __init__(self, start: float = 0.00002341):
        self.price = start
        self.i = 0

    def next_quote(self) -> dict:
        self.i += 1
        # Repeating deterministic movement keeps showcase runs reproducible.
        step = [0.0012, 0.0008, -0.0004, 0.0010, -0.0002][self.i % 5]
        self.price *= 1 + step
        return {"symbol": "$BONK/USDC", "price": self.price}


class DexScreenerProvider:
    """Read-only DEX Screener pair adapter.

    Pass a full pair URL or pair endpoint URL. This adapter never places orders.
    """

    def __init__(self, url: str, timeout: int = 10):
        self.url = url
        self.timeout = timeout

    def quote(self) -> dict:
        req = urllib.request.Request(
            self.url,
            headers={"User-Agent": "FOXBRAIN/0.1"},
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            payload = json.load(response)

        pairs = payload.get("pairs") or []
        if not pairs:
            raise RuntimeError("No matching pair returned by provider.")

        pair = pairs[0]
        price = float(pair["priceUsd"])
        return {
            "symbol": pair.get("baseToken", {}).get("symbol", "UNKNOWN"),
            "price": price,
            "volume24h": pair.get("volume", {}).get("h24"),
            "liquidity": pair.get("liquidity", {}).get("usd"),
        }
