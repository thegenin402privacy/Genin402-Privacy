<div align="center">
<img src="https://capsule-render.vercel.app/api?type=cylinder&color=6d28d9,4c1d95&height=160&section=header&text=GENIN402&fontSize=64&fontColor=e9d5ff&animation=fadeIn&desc=privacy%20agent%20%E2%80%94%20solana%20stealth%20transfer%20engine&descSize=14&descAlignY=72&fontAlignY=42" />

```
  ░▒▓ 402-GATE ACTIVE ▓▒░   ░▒▓ SHADOW ROUTING ON ▓▒░   ░▒▓ CHAIN ANALYSIS BLOCKED ▓▒░
```

[![Tests](https://github.com/genin402privacy/Genin402/actions/workflows/test.yml/badge.svg)](https://github.com/genin402privacy/Genin402/actions)
![Python](https://img.shields.io/badge/python-3.10%2B-6d28d9?style=flat-square&logo=python&logoColor=white)
![TypeScript](https://img.shields.io/badge/typescript-5.3-4c1d95?style=flat-square&logo=typescript&logoColor=white)
![Vue](https://img.shields.io/badge/vue-3.4-7c3aed?style=flat-square&logo=vue.js&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-a78bfa?style=flat-square)

**`CA: GN402 — TBA`**

</div>

---

```
every transfer leaves a trace.
genin402 measures how much of yours survives.
```

Solana is a public ledger. Every hop, every amount, every wallet interaction is visible forever. Genin402 is a privacy scoring engine — it takes a transfer configuration and tells you how well it's actually shielded from chain analysis tools, block explorers, and wallet trackers.

The 402 in the name isn't a status code. It's a payment gate protocol — a routing layer that sits between your intent and your execution. Genin402 measures whether that gate is holding.

---

## `> VERDICT SYSTEM`

```
ANBU      [90-100]  shadow ops — untraceable
JONIN     [75-89 ]  high stealth — well-routed
CHUNIN    [60-74 ]  decent coverage — exposure risk
GENIN     [40-59 ]  basic obfuscation — trackable
ACADEMY   [20-39 ]  minimal protection — mostly open
CIVILIAN  [0-19  ]  no shield — fully on-chain
```

---

## `> CLOAK STATUS`

```
■ DARK      score ≥ 75   → deep cover, chain analysis stalled
░ GREY      score ≥ 55   → partial coverage, some gaps
▒ DIM       score ≥ 35   → thin cover, determined analysis wins
□ EXPOSED   score < 35   → open book, nothing hiding
```

---

## `> SCORING ENGINE`

Five metrics. Each scored 0–100. Weighted into a single privacy score.

```
stealth_score     ██████░░░░  0.25   shadow pattern depth
route_entropy     ██████░░░░  0.25   hop complexity + split routing
payment_shield    █████░░░░░  0.20   402 gate + mixer pool coverage
trace_resistance  █████░░░░░  0.20   decoy noise + obfuscation layers
shadow_depth      ███░░░░░░░  0.10   layering effectiveness
```

### stealth_score — 10 binary patterns

| Pattern | Trigger |
|---------|---------|
| `multi_hop` | hop_count ≥ 5 |
| `pool_routed` | mixer_pools_used ≥ 2 |
| `decoy_flood` | decoy_tx_count ≥ 10 |
| `gate_active` | payment_gate_active == 1 |
| `split_route` | route_splits ≥ 3 |
| `time_shifted` | time_delay_blocks ≥ 20 |
| `dummy_outputs` | dummy_outputs ≥ 5 |
| `memo_dark` | memo_obfuscated == 1 |
| `program_masked` | token_program_obscured == 1 |
| `fee_noise` | fee_randomized == 1 |

---

## `> INSTALL`

```bash
pip install genin402
```

## `> QUICK START`

```python
from genin402 import PrivacyEngine, ShadowTransfer

engine = PrivacyEngine()

transfer = ShadowTransfer(
    wallet_address="7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
    transfer_amount_sol=25.0,
    hop_count=7,
    mixer_pools_used=3,
    decoy_tx_count=15,
    payment_gate_active=1,
    route_splits=4,
    time_delay_blocks=35,
    dummy_outputs=7,
    memo_obfuscated=1,
    token_program_obscured=1,
    fee_randomized=1,
)

report = engine.analyze(transfer)
print(report.verdict)        # JONIN
print(report.privacy_score)  # 81.4
print(report.cloak_status)   # dark
print(report.shadows)        # ['multi_hop', 'pool_routed', ...]
```

## `> BATCH`

```python
reports = engine.analyze_batch([t1, t2, t3])
# sorted by privacy_score descending
```

---

## `> REST API`

```bash
uvicorn genin402.server:app --reload
```

```
POST /analyze          → ShadowReport
POST /analyze/batch    → list[ShadowReport]
GET  /health           → { "status": "ok" }
```

---

## `> CLI`

```bash
cd ts && npm install && npm run build
node dist/cli.js analyze <wallet_address>
node dist/cli.js batch <w1> <w2> <w3>
```

---

## `> DASHBOARD`

```bash
cd dashboard && npm install && npm run dev
# → http://localhost:3000
```

---

## `> DOCKER`

```bash
docker-compose up
# API  → :8000
# UI   → :3000
```

---

## `> DEVELOPMENT`

```bash
git clone https://github.com/genin402privacy/Genin402.git
cd Genin402
pip install -e ".[dev]"
pytest tests/ -v          # 106+ tests
```

---

## `> ARCHITECTURE`

```
ShadowTransfer (input)
    │
    ├─ ShadowAnalyzer    → stealth_score    (10-pattern binary)
    ├─ RouteAnalyzer     → route_entropy    (hop + split + delay)
    ├─ ShieldAnalyzer    → payment_shield   (402 gate + mixer)
    ├─ StealthAgent      → trace_resistance (decoy + obfuscation)
    └─ RouteAgent        → shadow_depth     (layering complexity)
         │
         ▼
    PrivacyEngine → ShadowReport
         │
    verdict + privacy_score + cloak_status + shadows
```

---

<div align="center">
<img src="https://capsule-render.vercel.app/api?type=cylinder&color=4c1d95,6d28d9&height=80&section=footer&reversal=true" />
</div>
