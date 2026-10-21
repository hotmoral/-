# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare watched branch: `timing-defense-cloudflare-do-poc`
- current tested cf.3 HEAD: `abb2d428df546c257181278ba6bd0814e0471c93`
- health generation: `0.36-cf.3`

Last fully closed checkpoint:
- v0.35 HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- branch `timing-defense-cloudflare-v035-pass-20261021`
- health `0.35-cf.7`

Preserved checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V036_AUTOMATION_PASS_2026-10-21.md`
- `CLOUDFLARE_V036_AUTOMATED_VALIDATION_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_DECISION_2026-10-21.md`
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
- `CLOUDFLARE_V035_PASS_2026-10-21.md`

---

# Closed Cloudflare truth through v0.35
## v0.31/v0.32 — PASS
- room create/join,
- nickname/class/slot/AI FILL,
- READY / READY cancel,
- host-only START,
- synchronized future start,
- waiting-room reconnect,
- Samsung Browser short-landscape layout.

## v0.33 — PASS
- authoritative shared Stage 1 world,
- synchronized monster HP/death and BASE HP,
- cross-device attacks affect the same state,
- EXP / charge synchronization,
- shared clear.

## v0.34 — PASS
- remote human projectile visible,
- local immediate impact presentation,
- server HP/EXP/coin/kills authority retained,
- acceptable monster smoothing.

## v0.35 — PASS
Validated Android + PC through cf.7:
- Stage 1 -> Team Shop -> Stage 2,
- authoritative purchase / coin / rank flow,
- shop `처리중…` feedback + duplicate-tap protection,
- all-human shop READY and host NEXT,
- synchronized Stage 2 intro/input/combat,
- authoritative GRUNT/RUNNER state and clear,
- authoritative result board,
- reconnect,
- Rogue CHARGE palette/flicker correction,
- remote human timing-projectile visual parity.

The exact v0.35 checkpoint remains immutable unless a regression investigation explicitly references it.

---

# v0.36 Slice A — AUTOMATED PASS / DEVICE SMOKE PENDING
Slice A scope:
- Stage 1–2 only,
- no Stage 3,
- approved N1/N2 parity restoration,
- server-authoritative Lv6 consequences for all five human classes,
- action/cast identity + secondary hit metadata,
- authoritative secondary-event presentation.

### Numerical decisions
N1 — **APPROVED / IMPLEMENTED / AUTOMATED PASS**
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

N2 — **APPROVED / IMPLEMENTED / AUTOMATED PASS**
`AI damage × (1 + (stage - 1) * 0.035)`

N3 — **DEFERRED / MANDATORY FUTURE DISCUSSION**
Experimental combo-milestone extra attacks are not implemented and are not discarded. Do not silently port, remove, freeze or rebalance them.

### Lv6 authority implemented
- Knight: +12% damage.
- Rogue: one authoritative 55% second dagger after +55 ms; same-target allowed with nearest fallback.
- Tank: +30% knockback.
- Archer: up to two strict-line secondary hits at 52%; no seeking/off-line retarget.
- Mage: up to three nearby splash hits at 50%.

### cf.2 integration hardening
Code audit found and fixed before device closure:
1. Rogue legacy local Lv6 secondary projectile could execute client gameplay mutation in network mode; it is now blocked so server state is the gameplay authority.
2. New Lv6 secondary VFX initially had an independent event floor; it now inherits the v0.35 resume floor so historical secondary effects are not replayed after reconnect.

### cf.3 automated validation — PASS
User executed the deployed one-click suite in Samsung Browser and supplied screenshot evidence:
- `SERVER · PASS · 10/10`
- `CLIENT · PASS · 4/4`
- `MULTICLIENT · PASS · 9/9`
- `FINAL · PASS`

The suite covers:
- N1/N2,
- all five Lv6 authority boundaries,
- action identity / hit indices,
- stale/duplicate seq rejection,
- Rogue local-network mutation block,
- reconnect event-floor / duplicate secondary VFX prevention,
- two real WebSocket clients against deployed Durable Object,
- READY/START/shared Stage1/reconnect/Shop/Stage2 synchronization.

Exact tested deployment:
- branch `timing-defense-cloudflare-do-poc`
- HEAD `abb2d428df546c257181278ba6bd0814e0471c93`
- preserved automated-pass branch `timing-defense-cloudflare-v036-automation-pass-20261021`

Do not require manual phone verification of exact numerical values or all five classes.

---

# Immediate boundary
Do **not** start Stage 3 yet.

Only one v0.36 Slice A gate remains: a short real-device game smoke for browser/render/touch behavior that simulation cannot fully prove:
- current assets load,
- Timing Square touch responds,
- no obvious duplicate projectile, stale VFX replay, flicker or visual corruption,
- Stage 1 -> Team Shop -> Stage 2 is visibly usable.

If smoke PASS:
- declare v0.36 Slice A full PASS,
- preserve exact full-PASS deployment branch,
- synchronize status/handoff,
- disable/remove candidate-only debug controls as appropriate,
- open Slice B: Stage 3 only.

## Slice B after Slice A PASS
- two humans first,
- Stage 2 clear -> Team Shop -> host NEXT -> Stage 3,
- exact legacy Stage 3: 12 enemies / 980 ms / GRUNT 44% / RUNNER 34% / BRUTE 22%,
- authoritative BRUTE,
- Stage 3 clear -> Team Shop,
- Stage 4 blocked.

## Later slices
- larger party baseline: 3H / 4H / 2H+2AI / 3H+1AI,
- Stage 4 SHIELD,
- Stage 5–6 boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with automated forced-level tests before natural progression depends on them.

---

# Frozen combat / balance governance
- Rhythm: `X -> X -> X -> X+Y`.
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line trajectory; no seeking/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP only from valid timing events; passive grants no EXP.
- Current combo presentation remains frozen unless explicitly changed.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` — N3 mandatory future review.

Numerical workflow remains:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.

## Current truth boundary
Safe claims:
- Cloudflare PoC through v0.35 are device-PASS for their scoped gates,
- exact v0.35 PASS is preserved,
- post-v0.35 preflight is complete,
- N1/N2 were explicitly approved, implemented and automatically validated,
- v0.36 cf.3 server/client/multiclient automated suite PASS,
- exact cf.3 automated-pass deployment is preserved.

Do not claim yet:
- v0.36 Slice A full device PASS,
- Stage 3–10 multiplayer parity,
- complete Lv6+ multiplayer authority beyond Slice A,
- final persistence/security/anti-cheat architecture,
- final numerical balance.

## Deferred UX item
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred. Handle later as a shared responsive-safety layer rather than per-device patches.
