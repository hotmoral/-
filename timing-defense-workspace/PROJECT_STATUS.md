# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare watched branch: `timing-defense-cloudflare-do-poc`
- current cf.3 candidate watched HEAD: `abb2d428df546c257181278ba6bd0814e0471c93`
- expected candidate health: `0.36-cf.3`

Last fully validated checkpoint:
- v0.35 HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- branch `timing-defense-cloudflare-v035-pass-20261021`
- health `0.35-cf.7`

Closed Cloudflare validation gates:
1. isolated Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Preserved migration checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`

Read first:
- `NEXT_WORK.md`
- `CLOUDFLARE_V036_AUTOMATED_VALIDATION_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_DECISION_2026-10-21.md`
- `CLOUDFLARE_V036_SLICE_A_CANDIDATE_2026-10-21.md`
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
- `CLOUDFLARE_V035_PASS_2026-10-21.md`

---

# Cloudflare validated truth

## v0.31/v0.32 — PASS
Validated Android + PC:
- FRIEND room create/join,
- nickname/class/slot/AI FILL,
- READY / READY cancel,
- all-human READY gate,
- host-only START,
- synchronized future start,
- waiting-room refresh/reconnect,
- Samsung Browser short-landscape layout.

## v0.33 Stage 1 — PASS
- authoritative shared Stage 1 world,
- synchronized monster HP/death and BASE HP,
- cross-device attacks affect the same state,
- EXP / charge synchronization,
- shared clear.

## v0.34 render parity — PASS
- remote human projectile visible,
- local immediate impact presentation,
- server HP/EXP/coin/kills authority retained,
- acceptable monster smoothing.

## v0.35 — PASS
Validated through cf.7:
- Stage 1 -> Team Shop -> Stage 2,
- authoritative purchase / coin / rank flow,
- shop `처리중…` feedback + duplicate-tap protection,
- all-human shop READY and host NEXT,
- synchronized Stage 2 intro/input/combat,
- authoritative GRUNT/RUNNER state and clear,
- authoritative contribution result board,
- reconnect,
- Rogue CHARGE palette/flicker correction,
- remote human timing-projectile visual parity.

The exact v0.35 checkpoint remains immutable unless a regression investigation explicitly references it.

---

# Post-v0.35 preflight — COMPLETE
Recovered boundaries:
- exact legacy Stage 3–10 plans/compositions/gaps/scaling,
- BRUTE / SHIELD / FLYER and Stage 5/10 boss contracts,
- four-slot / human+AI semantics,
- Stage-2-specific hardcoding requiring generic Stage-N replacement,
- playable legacy skill authority through Lv21,
- Lv26/Lv31 remain design-roadmap only,
- event-volume risk for larger parties + multi-hit skills.

S/E/X pressure grammar remains future candidate data, not migration replacement values.

---

# v0.36 Slice A — ACTIVE CF.3 CANDIDATE
Status:
**IMPLEMENTED / AUTOMATED VALIDATION HARNESS DEPLOYED TO WATCHED BRANCH / PUBLIC SUITE RUN PENDING**

Implementation branch:
- `timing-defense-cloudflare-v036-lv6-authority`
- HEAD `458d468f68c95c569ff57f1e2fd5a4bd20d21e4a`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- HEAD `abb2d428df546c257181278ba6bd0814e0471c93`
- loader generation `cf0363`

### Explicit numerical decisions
N1 — **APPROVED / IMPLEMENTED**:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

N2 — **APPROVED / IMPLEMENTED**:
`AI damage × (1 + (stage - 1) * 0.035)`

N3 — **DEFERRED / MANDATORY FUTURE DISCUSSION**:
- experimental combo-milestone extra attacks are not implemented in Slice A,
- N3 is not discarded,
- do not silently port, remove, freeze or rebalance it without explicit discussion and decision.

### Slice A authoritative Lv6 scope
No Stage 3 is enabled.

- Knight: +12% damage.
- Rogue: one authoritative 55% second dagger after +55 ms; same-target allowed with nearest fallback.
- Tank: +30% knockback.
- Archer: up to two strict-line secondary hits at 52%; no seeking/off-line retarget.
- Mage: up to three nearby splash hits at 50%.

Infrastructure:
- primary/secondary shared action identity,
- hit indices / skill metadata,
- scheduled Rogue secondary queue,
- server-owned Archer/Mage target selection,
- client secondary presentation from authoritative events,
- candidate-only host Lv5/Lv6 debug endpoint.

### cf.2 hardening found by code audit
Before asking for device validation, two integration risks were identified and patched:
1. Rogue's legacy local Lv6 secondary projectile could still execute client `visualImpact()` in network mode; cf.2 removes that local mutator so server events remain the only gameplay authority.
2. The new Lv6 secondary-VFX layer initially had an independent event floor; cf.2 makes it inherit the v0.35 resume floor so historical effects are not replayed after reconnect.

---

# v0.36 automated validation policy
Manual class-by-class device testing is no longer the primary oracle.

Automated layers now deployed:
1. `GET /api/diagnostics/v036-slice-a`
   - executes actual patched server prototype in isolated state,
   - N1/N2, all five Lv6 boundaries, duplicate seq, Stage1->Shop->Stage2.
2. `/v036-client-selftest.html`
   - executes actual `v036-lv6-authority.js` in a controlled browser fixture,
   - Rogue local mutation block + reconnect event-floor behavior.
3. `/v036-multiclient-sim.html`
   - two real WebSocket clients against the deployed Durable Object,
   - READY/START/shared combat/Rogue secondary/stale seq/resume/reconnect/Shop/Stage2.
4. `/v036-validation-suite.html`
   - one-click aggregate of the three layers above.

Exact EXP/damage/knockback/target selection are owned by automated validation, not by visual inspection on a phone.

---

# Immediate boundary
Do **not** start Stage 3 yet.

Slice A must first pass:
1. public health = `0.36-cf.3`,
2. aggregate `/v036-validation-suite.html` = **PASS**,
3. one final short real-device smoke only for browser/render/touch behavior that code cannot fully prove:
   - current asset loads,
   - timing touch responds,
   - no obvious duplicate projectile/flicker/visual corruption,
   - Stage1 -> Shop -> Stage2 visibly usable.

The model-side environment cannot directly access the public `workers.dev` host, so the aggregate public suite must be launched from a normal browser.

Only after Slice A PASS:
- preserve exact Slice A checkpoint,
- sync status/handoff,
- open Slice B: Stage 3 only, two humans first.

---

# Frozen combat / balance governance
- Rhythm: `X -> X -> X -> X+Y`.
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit / durable-normal execution; same-target dagger hits uncapped.
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
- N1/N2 were explicitly approved and implemented,
- cf.2 integration hardening is implemented,
- cf.3 automated validation harness is on the watched deployment branch.

Do not claim yet:
- v0.36 Slice A PASS,
- Stage 3–10 multiplayer parity,
- complete Lv6+ multiplayer authority beyond Slice A,
- final production persistence/security/anti-cheat architecture,
- final numerical balance.

## Deferred UX item
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred. Handle later as a shared responsive-safety layer rather than per-device patches.
