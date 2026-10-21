# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current execution status
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Closed public/device gates:
- Durable Objects viability PoC — **PASS**
- v0.31/v0.32 waiting-room parity — **PASS**
- v0.33 authoritative Stage 1 — **PASS**
- v0.34 render/remote projectile parity — **PASS**
- v0.35 reconnect / Team Shop / Stage 2 — **PASS**
- v0.36 Slice A N1/N2 + Lv6 authority — **FULL PASS**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- tested full-PASS HEAD `c540119f469cff6795a74a3867c26f4c67de9071`

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`
- v0.36 Slice A full PASS: `timing-defense-cloudflare-v036-slice-a-pass-20261021`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V036_SLICE_A_PASS_2026-10-21.md`
5. `CLOUDFLARE_V036_AUTOMATION_PASS_2026-10-21.md`
6. `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
7. `CLOUDFLARE_V035_PASS_2026-10-21.md`
8. `DESIGN_DECISIONS.md`
9. `SKILL_PLAN_LV6_31.md`
10. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`

## v0.36 Slice A closure
Scope remained Stage 1–2 only.

### N1 — APPROVED / IMPLEMENTED / PASS
Timing EXP exact table:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

### N2 — APPROVED / IMPLEMENTED / PASS
AI stage multiplier:
`1 + (stage - 1) * 0.035`

### N3 — DEFERRED / MANDATORY FUTURE DISCUSSION
N3 is the experimental combo-milestone extra-attack system.
It is not discarded and was not included in Slice A.
Do not silently port, remove, freeze or rebalance it.

### Lv6 authority validated
- Knight +12% authoritative damage.
- Rogue one authoritative +55 ms second dagger at 55%, same-target allowed with nearest fallback.
- Tank +30% authoritative knockback.
- Archer up to two strict-line 52% secondary hits, no seeking.
- Mage up to three nearby 50% splash hits.

### Automated validation PASS
Samsung Browser one-click suite:
- `SERVER 10/10 PASS`
- `CLIENT 4/4 PASS`
- `MULTICLIENT 9/9 PASS`
- `FINAL PASS`

Coverage includes exact N1/N2, all five Lv6 boundaries, actionId/hitIndex, stale seq rejection, Rogue local mutation block, reconnect event-floor handling, two real WebSocket clients, READY/START/shared Stage1/reconnect/Shop/Stage2.

### Final Samsung Browser smoke PASS
A candidate-only peerbot simulated a second human over the real room WebSocket/API path so the user did not need a physical PC.

An initial peerbot harness defect was detected from user evidence:
- simulated peer socket was captured by the main bridge and could overwrite local slot/session,
- debug overlays could cover READY/START/NEXT.

The harness was corrected:
- peer socket uses the original native WebSocket constructor and no longer mutates the main bridge,
- local debug level control pins the original local session/slot,
- peer/debug overlays are combat-only and avoid normal CTA controls.

Final recording confirmed:
- local remains `ROGUE`,
- debug control visibly shows `ROGUE LV6` with LV6 selected,
- `SIM-PC` remains a separate `ARCHER` human participant,
- timing input works,
- no obvious projectile duplication storm, flicker or visual corruption,
- Stage 1 Team Shop is usable,
- Stage 2 completes,
- result board separately lists local Rogue and SIM-PC Archer with authoritative contribution data.

Exact full-PASS branch:
`timing-defense-cloudflare-v036-slice-a-pass-20261021`

Exact full-PASS HEAD:
`c540119f469cff6795a74a3867c26f4c67de9071`

## Immediate next boundary — Slice B
Stage 3 only, two humans first.

Scope:
- Stage 2 clear -> Team Shop,
- host NEXT -> Stage 3,
- exact legacy Stage 3: `12 enemies / 980 ms / GRUNT 44% / RUNNER 34% / BRUTE 22%`,
- authoritative BRUTE,
- Stage 3 clear -> Team Shop,
- Stage 4 blocked.

Required method:
- generalize Stage-N flow rather than stacking more Stage-2 special cases,
- preserve v0.36 Slice A authority and N1/N2,
- extend deterministic and multi-client automated tests before device smoke,
- use manual device testing only for browser/render/input smoke.

## Following slices
- larger party baseline: 3H / 4H / 2H+2AI / 3H+1AI,
- Stage 4 SHIELD,
- Stage 5–6 boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed-roster stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with automated forced-level tests before natural progression relies on them.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred. Implement later as a shared responsive-safety layer rather than device-specific patches.

## Frozen governance
- Rhythm: `X -> X -> X -> X+Y`.
- Knight stable generalist / penetration / strong heavy.
- Rogue multihit / crit; same-target dagger hits uncapped.
- Tank knockback / wall protection / team specialist.
- Archer strict straight-line trajectory; no seeking/bending.
- Mage density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP only from valid timing events; passive gives no EXP.
- Current combo display/size/position/animation remains frozen unless explicitly changed.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` — N3 mandatory future review.

No numerical change without:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
