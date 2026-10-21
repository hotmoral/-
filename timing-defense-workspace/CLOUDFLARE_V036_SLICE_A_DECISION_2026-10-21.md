# Timing Defense — Cloudflare v0.36 Slice A Decision

Date: 2026-10-21 KST
Status: **N1/N2 APPROVED / SLICE A IMPLEMENTATION ACTIVE**

## Approved numerical parity restoration
The user explicitly approved both preflight parity findings before Slice A implementation.

### N1 — exact legacy timing EXP
Restore the legacy table:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

This is classified as parity restoration, not a new balance experiment.

### N2 — exact legacy AI stage damage scaling
Restore:
`AI damage × (1 + (stage - 1) * 0.035)`

This is classified as parity restoration, not a new balance experiment.

## N3 — mandatory future discussion, NOT discarded
N3 means the experimental PERFECT-combo milestone bonus attacks from legacy v0.18:
- milestone raw-equivalent budgets 60 / 90 / 150 / 210,
- class-shaped extra attacks at combo milestones,
- recurring maximum-tier milestone behavior after 30.

The existing persistent combo percentage bonus remains separate.

**User decision:** N3 must not be forgotten, removed, or silently decided. It is a required future discussion/review item. Do not port, freeze, delete, or rebalance N3 without an explicit discussion and decision.

## Slice A implementation boundary
Implementation branch:
`timing-defense-cloudflare-v036-lv6-authority`

Baseline:
`b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d` (`timing-defense-cloudflare-v035-pass-20261021`)

Scope:
- preserve Stage 1–2 flow,
- N1 exact EXP parity,
- N2 AI stage-damage parity,
- authoritative Lv6 consequences for all five human classes,
- action/cast identity + secondary-hit metadata,
- candidate-only host Lv5/Lv6 debug endpoint for bounded validation,
- remote secondary-skill presentation without client damage authority.

Lv6 server consequences:
- Knight: +12% damage; projectile enlargement remains presentation.
- Rogue: 55% second dagger, delayed 55 ms; same target allowed and nearest-target fallback retained.
- Tank: +30% knockback.
- Archer: up to two strict-line penetrations at 52% secondary damage.
- Mage: up to three nearby splash targets at 50% damage.

Non-goals:
- no Stage 3 yet,
- no Lv11+,
- no 3–4-player validation yet,
- no N3 milestone attacks,
- no S/E/X production encounter data,
- no new balance tuning.

## Closure gate
Do not call Slice A PASS until:
1. source/audit checks pass,
2. N1 and N2 are measured in candidate state,
3. forced Lv5 vs Lv6 checks prove each class effect boundary,
4. existing Stage 1–2 multiplayer regression remains clean,
5. no duplicate authoritative damage is observed from local prediction.
