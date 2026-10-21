# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**

Exact v0.36 Slice A full-PASS checkpoint:
- branch `timing-defense-cloudflare-v036-slice-a-pass-20261021`
- HEAD `c540119f469cff6795a74a3867c26f4c67de9071`

## Numerical decisions
- N1 exact legacy EXP — **PASS / frozen for migration parity**.
- N2 exact AI stage multiplier `1 + (stage - 1) * 0.035` — **PASS / frozen for migration parity**.
- N3 combo-milestone extra attacks — **DEFERRED / MANDATORY FUTURE DISCUSSION**. Do not silently port, remove, freeze or rebalance.

## Active slice — v0.37 Slice B / Stage 3
Status: **IMPLEMENTED / WATCHED BRANCH TRIGGERED / AUTOMATED LIVE VALIDATION PENDING**

Read:
- `CLOUDFLARE_V037_SLICE_B_CANDIDATE_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_PASS_2026-10-21.md`
- `PROJECT_STATUS.md`
- `SESSION_HANDOFF.md`

Candidate refs:
- implementation branch `timing-defense-cloudflare-v037-stage3`
- watched branch `timing-defense-cloudflare-do-poc`
- candidate HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`
- expected health `0.37-cf.1`
- loader cache generation `cf0372`

### Exact Stage 3 contract
- 12 enemies
- 980 ms gap
- GRUNT 44% / RUNNER 34% / BRUTE 22%
- BRUTE: HP 900 / speed .040 / wall damage 180 / knock resist .38 / armor 1.00 / reward 14
- existing HP rules retained: stage factor `1 + (stage-1)*0.13` and ordinary non-boss `×1.10`
- Stage 3 ordinary BRUTE HP = 1247

### Flow
- Stage 1 clear -> Team Shop
- Stage 2 clear -> Team Shop
- Stage 2 host NEXT -> Stage 3
- Stage 3 clear -> Team Shop
- Stage 4 blocked by server and candidate UI

### Pre-deployment audit defect caught and fixed
The old Stage 1–2 wall loop closes over a GRUNT/RUNNER-only type table. BRUTE would otherwise fall back to GRUNT wall damage 90. v0.37 now processes Stage 3 wall contacts with the exact three-type table. Automated tests include BRUTE wall damage 180 and DEF rank 4 -> 162.

## Immediate validation gate
Do **not** start Stage 4 or Slice C yet.

First run the one-click deployed suite:
- `/v037-validation-suite.html`

It must pass:
1. v0.36 deterministic server regression,
2. Stage 3 deterministic plan/BRUTE/flow tests,
3. exact Stage 3 wall tests,
4. v0.36 client regression,
5. generic Stage 3 client transition/input + Stage4 UI lock,
6. two real WebSocket clients through Stage1 -> Shop -> Stage2 -> Shop -> Stage3 -> Shop -> Stage4 blocked, including reconnect.

If automated suite PASS:
- run one short Samsung Browser smoke using `?peerbot=1` so no PC is required,
- inspect only render/input/BRUTE visual behavior and Stage 3 shop usability,
- do not manually re-check exact numerical values.

If smoke PASS:
- declare v0.37 Slice B full PASS,
- preserve exact Stage 3 PASS checkpoint,
- synchronize status/handoff,
- then open Slice C larger-party baseline.

## Following bounded slice — Slice C
- 3 humans
- 4 humans
- 2 humans + 2 AI
- 3 humans + 1 AI
- READY/host/reconnect/shop/event-volume validation
- extend automated multi-client harness before manual repeated play

## Later
- Stage 4: SHIELD / armor
- Stage 5–6: boss + FLYER + authoritative Y geometry
- Stage 7–9: mixed-roster stress
- Stage 10: final boss/final result
- Lv11/16/21 authority with automated forced-level tests before natural progression depends on them

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
