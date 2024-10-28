# Genin402 Privacy — Project Context

## What is this

Solana privacy transfer agent. Analyzes on-chain transfer configurations through 5 stealth-focused metrics, scoring how well a transfer is protected from chain analysis.

Built for privacy-conscious users who need to evaluate transfer setups before executing them on Solana.

## Stack

- **Python 3.10+** — Core engine, 106+ tests
- **FastAPI** — REST oracle at `/analyze` and `/analyze/batch`
- **TypeScript** — CLI
- **Vue 3 + Vite** — Privacy shield dashboard

## Verdict Tiers

| Tier | Score | Meaning |
|------|-------|---------|
| ANBU | 90+ | Shadow ops level — virtually untraceable |
| JONIN | 75-89 | High stealth — well-routed and shielded |
| CHUNIN | 60-74 | Decent privacy — some exposure risk |
| GENIN | 40-59 | Basic obfuscation — trackable with effort |
| ACADEMY | 20-39 | Minimal privacy — mostly transparent |
| CIVILIAN | 0-19 | No protection — fully on-chain exposed |

## Cloak Status

- `dark` — privacy_score ≥ 75
- `grey` — privacy_score ≥ 55
- `dim` — privacy_score ≥ 35
- `exposed` — everything else

## Key Files

| Path | Role |
|------|------|
| genin402/models.py | ShadowTransfer, Genin402Metrics, ShadowReport |
| genin402/engine.py | PrivacyEngine — analyze() + analyze_batch() |
| genin402/analyzers/shadow_analyzer.py | 10-pattern stealth check |
| genin402/analyzers/route_analyzer.py | Route entropy scoring |
| genin402/analyzers/shield_analyzer.py | 402-gate + mixer shield |
| genin402/agents/stealth_agent.py | trace_resistance (Claude Haiku) |
| genin402/agents/route_agent.py | shadow_depth (Claude Haiku) |
| genin402/server.py | FastAPI REST |
