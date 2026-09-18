from __future__ import annotations

import argparse
import json
import sqlite3
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from fox.engine import signal_from_prices
from fox.providers import ShowcaseProvider, DexScreenerProvider

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "foxbrain.sqlite3"


def init_db() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            """
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at REAL NOT NULL,
                mode TEXT NOT NULL,
                market TEXT NOT NULL,
                symbol TEXT NOT NULL,
                signal TEXT NOT NULL,
                fast REAL,
                slow REAL,
                reason TEXT NOT NULL
            )
            """
        )
        db.commit()


def observation_loop(stop: threading.Event) -> None:
    """Small local showcase loop: deterministic, inspectable, no order execution."""
    provider = ShowcaseProvider()
    prices: list[float] = []
    while not stop.is_set():
        quote = provider.next_quote()
        prices.append(quote["price"])
        prices = prices[-20:]
        result = signal_from_prices(prices)

        if result["signal"] != "WARMUP":
            with sqlite3.connect(DB_PATH) as db:
                db.execute(
                    """
                    INSERT INTO signals
                    (created_at, mode, market, symbol, signal, fast, slow, reason)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        time.time(),
                        "showcase",
                        "Solana",
                        quote["symbol"],
                        result["signal"],
                        result["fast"],
                        result["slow"],
                        result["reason"],
                    ),
                )
                db.commit()
        stop.wait(4)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / "web"), **kwargs)

    def do_GET(self):
        if self.path == "/api/health":
            body = json.dumps(
                {
                    "ok": True,
                    "project": "FOXBRAIN",
                    "mode": "showcase",
                    "execution": "manual_only",
                }
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def main() -> None:
    parser = argparse.ArgumentParser(description="FOXBRAIN local observation terminal")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    init_db()
    stop = threading.Event()
    worker = threading.Thread(target=observation_loop, args=(stop,), daemon=True)
    worker.start()

    server = ThreadingHTTPServer(("127.0.0.1", args.port), Handler)
    print(f"FOXBRAIN running at http://127.0.0.1:{args.port}")
    print("Showcase observation loop is active. Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        stop.set()
        server.server_close()


if __name__ == "__main__":
    main()
