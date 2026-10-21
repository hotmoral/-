# Timing Defense — Cloudflare v0.37 Slice B Candidate

Date: 2026-10-21 KST
Status: **IMPLEMENTED / WATCHED BRANCH TRIGGERED / AUTOMATED LIVE VALIDATION PENDING**

## Frozen baseline
v0.36 Slice A full PASS remains preserved:
- branch `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- HEAD `c540119f469cff6795a74a3867c26f4c67de9071`

## Candidate refs
Implementation branch:
- `timing-defense-cloudflare-v037-stage3`

Cloudflare watched branch:
- `timing-defense-cloudflare-do-poc`
- candidate HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Expected health:
- `version: 0.37-cf.1`
- scope `stage1-stage3-brute-team-shop`
- Stage 4 `blocked`
- N3 remains `deferred-explicit-discussion-required`

## Exact Stage 3 contract
- 12 enemies
- 980 ms base spawn gap
- GRUNT 44%
- RUNNER 34%
- BRUTE 22%

BRUTE legacy exact:
- HP 900
- speed .040
- size 1.34
- wall damage 180
- knock resist .38
- armor 1.00
- kill reward 14

Existing HP rules retained:
- stage multiplier `1 + (stage-1)*0.13`
- ordinary non-boss experiment `×1.10`
- Stage 3 ordinary BRUTE HP = 1247

## Flow
- Stage 1 clear -> Team Shop
- Stage 2 clear -> Team Shop
- host NEXT from Stage 2 -> Stage 3
- Stage 3 clear -> Team Shop
- Stage 4 entry blocked by server and candidate UI

## Authority work
- BRUTE X movement / wall arrival uses .040 speed.
- BRUTE damage/reward/knockback use exact type values.
- BRUTE wall contact uses 180 base damage and existing shared DEF reduction.
- Stage 3 spawn selection is server authoritative.
- v0.36 Lv6 authority remains active against BRUTE, including Tank knockback and geometric skill metadata.
- Stage 2/3 presentation/input uses one generic stage guard rather than a new Stage-3-only input patch.

## Audit defect caught before deployment
The old Stage 1–2 wall loop closes over a GRUNT/RUNNER-only type table. Without an adapter, BRUTE wall damage would have fallen back to GRUNT 90. The candidate pre-processes Stage 3 wall contacts with the exact Stage 3 type table; focused tests cover BRUTE 180 and DEF rank 4 -> 162.

## Automated validation
One-click suite:
`/v037-validation-suite.html`

Layers:
1. v0.36 deterministic server regression.
2. Stage 3 deterministic server tests: plan/thresholds/HP, BRUTE movement/damage/reward/knockback/N2, Stage2->Shop->Stage3, Stage3->Shop, Stage4 block.
3. Focused Stage 3 wall tests.
4. v0.36 client regression.
5. Stage 3 generic client flow + Stage4 UI lock.
6. Two real WebSocket clients: Stage1 -> Shop -> Stage2 -> Shop -> Stage3 -> Shop -> Stage4 blocked, with reconnect.

## Device policy
Do not request manual exact-number verification. If automation passes, use `?peerbot=1` for one short Samsung Browser Stage 3 render/input/BRUTE smoke with one physical phone.

## Explicit non-goals
- no Stage 4/SHIELD
- no larger-party expansion
- no Lv11+
- no responsive-safety work
- no N3 decision or implementation
- no new numerical balance changes
