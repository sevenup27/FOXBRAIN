# FOXBRAIN

[FOXBRAIN](https://foxbrain.live) is an experimental market observation terminal for Solana and Robinhood Chain, built around a fox-inspired interface and a transparent rule-based signal engine.

**Version 0.1 — local visual prototype with a working observation loop.**

The running interface uses an animated orange point-cloud brain, an interactive fox visual, market radar, signal display, execution trace and roadmap. The brain is procedural visualization, not a biological reconstruction.

FOXBRAIN is a software character and an observation tool. It does not reproduce a fox's biological brain. This release does not contain a trained neural network, wallet connection or automatic order execution.

## Start in one command

Requires Python 3.11+ and a modern browser. Showcase mode uses only the Python standard library.

1. Download or clone this project.
2. Open a terminal in the folder containing `app.py`.
3. Run:

```bash
python app.py
```

On Windows:

```bash
py -3 app.py
```

On macOS/Linux:

```bash
python3 app.py
```

4. Open **http://127.0.0.1:8000**
5. Stop with `Ctrl+C`.

If port 8000 is busy:

```bash
python app.py --port 8001
```

The development server binds to your computer only. Do not expose it directly to the public internet.

## Included and working

- FOXBRAIN observation interface with the fox-inspired visual direction.
- Interactive animated point-cloud brain: automatic rotation, drag rotation and controlled zoom.
- Market radar for Solana and Robinhood Chain interface states.
- BUY / SELL / WAIT baseline signals using five- and twenty-sample moving averages.
- Local showcase observation loop with deterministic generated prices.
- SQLite signal journal stored locally in `data/`.
- `/api/health` endpoint for a simple runtime check.
- Read-only DEX Screener provider adapter for future/live integration.
- No wallet connection and no automatic trade execution.
- Mobile layout and reduced-motion-friendly visual behavior.
- Tests for the signal engine.

## Live market configuration

Edit `config.json` and restart the server.

`chain_id` is the provider's string identifier, not necessarily a numeric EVM chain ID.

`pair_address` is a DEX pool/pair address, not a token mint.

For live integration, use a verified DEX Screener pair and verify the returned chain and token symbol before using its observations. The adapter is read-only.

The Robinhood Chain entry is intentionally unconfigured by default. This project does not claim that a working Robinhood Chain feed is available out of the box. An unsupported or blank pair should remain an explicit configuration state rather than being replaced with another blockchain.

## Signal rule

Fast = mean of the latest 5 prices.

Slow = mean of the latest 20 prices.

```text
Fast / Slow - 1 > 0.003  -> BUY
Fast / Slow - 1 < -0.003 -> SELL
otherwise                 -> WAIT
```

These are repeated observations, not executed orders or guaranteed entry/exit instructions. The engine has no position awareness, transaction-cost model or demonstrated profitability.

Showcase samples are explicitly generated.

## Structure

```text
app.py
fox/
  engine.py              Inspectable signal rules
  providers.py           Showcase + read-only quote adapter
web/
  index.html              FOXBRAIN interface
assets/
  fox.jpg                 Project fox visual
config.json               Public market configuration
data/                     Local SQLite journal (ignored by Git)
tests/
  test_engine.py
docs/
  QUICKSTART_RU.md
start.bat
start.sh
.github/workflows/
  tests.yml
.gitignore
README.md
```

## Test

```bash
python -m unittest discover -s tests -v
```

## Publish the source on GitHub

Create an empty repository named `FOXBRAIN` in your GitHub account. In this folder run:

```bash
git init
git add .
git commit -m "Initial FOXBRAIN observation terminal"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

Replace `YOUR_REPOSITORY_URL` with your repository URL.

`data/` is excluded by `.gitignore`, so local databases are not published.

No license is selected in this starter package. Choose a license as the project owner before inviting downstream reuse.

## Next releases

1. Connect a verified live market source for the selected Solana pairs.
2. Verify an actual Robinhood Chain pair and provider support.
3. Add persistent market history and paper positions.
4. Add transaction costs, slippage and performance comparisons.
5. Document and evaluate any learning-based model independently.
6. Consider optional execution adapters only after simulation and explicit wallet setup.

## References

- Quote API: https://docs.dexscreener.com/api/reference
- Robinhood Chain: https://docs.robinhood.com/chain/

The fox visual and procedural brain are interface artwork. The point cloud is not a scientific reconstruction of a fox brain. No endorsement by Robinhood or Solana is implied.

## About

Experimental market observation terminal for Solana and Robinhood Chain, featuring a fox-inspired interface, rule-based signals, interactive visualization and transparent runtime logs.
