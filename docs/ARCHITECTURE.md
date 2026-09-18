# Architecture

`app.py` starts the local HTTP server, initializes the SQLite journal and runs a small showcase observation loop.

`fox/engine.py` contains the signal rule and is intentionally readable.

`fox/providers.py` contains the deterministic showcase provider and a read-only DEX Screener adapter.

`web/index.html` is the FOXBRAIN interface. The visual brain remains a browser-side procedural canvas.

The system has no wallet signer and no order-execution path in this release.
