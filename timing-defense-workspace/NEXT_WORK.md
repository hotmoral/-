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

Read:
- `CLOUDFLARE_V036_SLICE_A_PASS_2026-10-21.md`
- `PROJECT_STATUS.md`
- `SESSION_HANDOFF.md`
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`

## Explicit numerical decisions
### N1 — APPROVED / IMPLEMENTED / PASS
Exact legacy timing EXP:
NORMAL 8 / GOOD 12 / PERFECT 18 / HEAVY 10 / HEAVY+ 14 / GREAT 18 / SUPER 23 / CRITICAL 28.

### N2 — APPROVED / IMPLEMENTED / PASS
Exact legacy AI stage multiplier:
`1 + (stage - 1) * 0.035`.

### N3 — DEFERRED, MANDATORY FUTURE DISCUSSION
Experimental combo-milestone extra attacks remain unresolved by design.
They are not discarded and must not be silently ported, removed, frozen or rebalanced.

## Active next slice — Slice B
Status: **READY TO IMPLEMENT**

Scope only:
- add Stage 3,
- keep Stage 1–2 behavior unchanged,
- two-human path first,
- Stage 2 clear -> Team Shop,
- host NEXT -> Stage 3,
- exact legacy Stage 3: 12 enemies / 980 ms,
- composition: GRUNT 44% / RUNNER 34% / BRUTE 22%,
- authoritative BRUTE,
- Stage 3 clear -> Team Shop,
- Stage 4 remains blocked.

### Required implementation work
1. Generalize Stage-N flow currently hardcoded around Stage 2.
2. Add BRUTE server data/authority:
   - legacy exact HP/speed/base damage/knockback resistance and reward values,
   - correct Stage 3 HP scaling,
   - no new behavior invented beyond legacy contract.
3. Update public run/state/events/results to carry Stage 3 generically.
4. Preserve shop authority, READY and host NEXT semantics.
5. Extend deterministic self-test and real multi-WebSocket simulator before device validation.
6. Add automated Stage 2 -> Shop -> Stage 3 -> Shop regression.
7. Final device work should remain a short render/input smoke only.

## Validation policy
Use:
`code audit -> deterministic server tests -> client/event tests -> multi-client simulation -> short real-device smoke`.

Do not ask for manual class-by-class or exact-number visual verification when automation can establish the result.

## Following bounded slices
### Slice C — larger-party baseline
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI,
- READY/host/reconnect/shop/result/event-volume verification,
- extend automated multi-client harness first.

### Later
- Stage 4: SHIELD / armor,
- Stage 5–6: boss + FLYER + authoritative Y geometry,
- Stage 7–9: mixed-roster stress,
- Stage 10: final boss/final result,
- Lv11/16/21 authority with automated forced-level tests before natural progression depends on them.

## Deferred UX item
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
