# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**
7. v0.37 Slice B Stage 3 + BRUTE — **PASS**

Exact v0.37 Slice B full-PASS checkpoint:
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Read:
- `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`
- `PROJECT_STATUS.md`
- `SESSION_HANDOFF.md`
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`

## Numerical decisions
- N1 exact legacy EXP — **PASS / frozen for migration parity**.
- N2 exact AI stage multiplier `1 + (stage - 1) * 0.035` — **PASS / frozen for migration parity**.
- N3 combo-milestone extra attacks — **DEFERRED / MANDATORY FUTURE DISCUSSION**. Do not silently port, remove, freeze or rebalance.

## Closed Slice B — v0.37 / Stage 3
Automated validation:
- SERVER 21/21 PASS
- v0.36 CLIENT REGRESSION 4/4 PASS
- STAGE3 CLIENT 6/6 PASS
- MULTICLIENT 10/10 PASS
- FINAL PASS

Device smoke:
- Samsung Browser single-device peer harness PASS,
- Stage 1 -> Shop -> Stage 2 -> Shop -> Stage 3,
- BRUTE rendered/moved correctly with existing large BRUTE visual,
- timing input usable,
- Stage 3 clear -> Team Shop,
- Stage 4 locked.

Exact Stage 3 contract now closed:
- 12 enemies / 980 ms,
- GRUNT 44% / RUNNER 34% / BRUTE 22%,
- BRUTE base HP 900 / speed .040 / wall 180 / knock resist .38 / armor 1 / reward 14,
- Stage 3 ordinary BRUTE HP 1247 under existing approved HP rules.

## Active next slice — Slice C / larger-party baseline
Status: **READY FOR PREFLIGHT + AUTOMATION EXPANSION**

Do **not** start Stage 4 yet.

Target party combinations:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

### Required audit before implementation
1. Verify fixed P1–P4 slot ownership under all supported mixes.
2. Verify host identity does not drift after reconnect or simulated peers.
3. Verify READY/START semantics with 3–4 humans.
4. Verify Team Shop READY/NEXT with 3–4 humans and human+AI mixes.
5. Audit AI FILL occupancy semantics; do not silently introduce dynamic AI displacement.
6. Audit result-board participant ordering/count for 3–4 total participants.
7. Audit event delivery volume:
   - human timing events,
   - passive events,
   - AI events,
   - Lv6 secondary events,
   - reconnect event-floor suppression.
8. Determine whether the current fixed event tail remains loss-safe at four-participant concurrency.

### Automation requirement
Expand the multi-client harness before any manual repeated play.

The harness should cover at minimum:
- 3H,
- 4H,
- 2H+2AI,
- 3H+1AI,
- READY -> START,
- synchronized Stage 1 combat,
- at least one reconnect,
- Team Shop READY/NEXT,
- Stage 2 entry,
- result/participant consistency,
- event-ID monotonicity and no silent event loss across the tested rate.

If event delivery is not demonstrably loss-safe, fix the delivery kernel before Stage 4 rather than compensating in client damage authority.

### Manual validation policy
After automation passes:
- use simulated peers so one phone remains sufficient where practical,
- run one short Samsung Browser render/input smoke,
- do not ask for repetitive manual party-size or exact-number verification already covered by automation.

## Following slices
### Stage 4 — SHIELD / armor
Only after Slice C closes.

### Stage 5–6
- checkpoint boss,
- FLYER,
- authoritative Y geometry required before FLYER/geometric skill interactions.

### Stage 7–9
- mixed-roster stress.

### Stage 10
- final boss and final result semantics.

### Lv11/16/21 authority
Use forced-level deterministic tests before natural progression depends on each milestone.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
