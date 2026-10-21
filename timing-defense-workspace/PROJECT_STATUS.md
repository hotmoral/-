# Timing Defense — Project Status

Updated: 2026-10-21 KST

## Active architecture lane
Primary architecture:
**Cloudflare Workers + Durable Objects event-driven multiplayer.**

Public deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare watched branch: `timing-defense-cloudflare-do-poc`
- current candidate watched HEAD: `8b1e2890ea582bd1ddaeae89157a82500adf40a0`
- expected candidate health: `0.36-cf.1`

Last fully validated checkpoint:
- v0.35 HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- branch `timing-defense-cloudflare-v035-pass-20261021`
- health `0.35-cf.7`

Closed Cloudflare validation gates:
1. isolated Durable Objects viability PoC — **PASS**
2. real-game v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**

Preserved migration checkpoints:
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 Stage 1 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 render PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 cf.3 Stage 2 flow PASS: `timing-defense-cloudflare-v035-cf3-stage2-flow-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`

Read first:
- `NEXT_WORK.md`
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
- shared clear,
- no duplicate local gameplay authority observed.

## v0.34 render parity — PASS
- remote human projectile visible,
- local immediate impact presentation,
- server HP/EXP/coin/kills authority retained,
- no duplicate presentation damage,
- acceptable monster smoothing.

## v0.35 — PASS
Validated through cf.7:
- Stage 1 -> Team Shop -> Stage 2,
- authoritative purchase / coin / rank flow,
- immediate shop `처리중…` feedback + duplicate-tap protection,
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
Canonical audit:
`CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`

Recovered boundaries:
- exact legacy Stage 3–10 plans/compositions/gaps/scaling,
- BRUTE / SHIELD / FLYER and Stage 5/10 boss contracts,
- four-slot / human+AI room semantics,
- Stage-2-specific Cloudflare hardcoding requiring generic Stage-N replacement,
- Lv6–21 playable legacy authority boundary,
- Lv26/Lv31 remain design-roadmap only,
- event-volume risk for 3–4 participants + multi-hit skills.

S/E/X pressure grammar and concrete recipes remain candidate future encounter data, not migration replacement values.

---

# v0.36 Slice A — ACTIVE CANDIDATE
Status:
**IMPLEMENTED / WATCHED BRANCH TRIGGERED / LIVE & DEVICE VALIDATION PENDING**

Implementation branch:
- `timing-defense-cloudflare-v036-lv6-authority`
- HEAD `ce3ea7f168fce26f6e76556cd73fea9fb08dce99`

Watched deployment branch:
- `timing-defense-cloudflare-do-poc`
- HEAD `8b1e2890ea582bd1ddaeae89157a82500adf40a0`
- loader generation `cf0362`

### Explicit numerical decisions
N1 — **APPROVED parity restoration**:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

N2 — **APPROVED parity restoration**:
`AI damage × (1 + (stage - 1) * 0.035)`

N3 — **DEFERRED / MANDATORY FUTURE DISCUSSION**:
- experimental combo milestone extra attacks are not implemented in Slice A,
- N3 is not discarded,
- do not silently port, remove, freeze or rebalance it without explicit discussion and decision.

### Slice A scope
No Stage 3 is enabled.

Server-authoritative Lv6 human consequences:
- Knight: +12% damage; projectile enlargement remains presentation.
- Rogue: 55% second dagger after +55 ms; same-target allowed with nearest fallback.
- Tank: +30% knockback.
- Archer: up to two strict-line secondary hits at 52% damage; no seeking/off-line retarget.
- Mage: up to three nearby splash hits at 50% damage.

Infrastructure:
- action/cast identity on primary + secondary hits,
- hit indices / skill metadata,
- scheduled Rogue secondary-hit queue,
- authoritative Archer/Mage target selection,
- secondary-skill client presentation driven by authoritative events,
- host-only candidate Lv5/Lv6 debug endpoint,
- `?v036debug=1` validation controls.

Internal syntax and isolated contract checks passed for N1/N2 and all five Lv6 boundaries. These checks are not a substitute for real Durable Object/device validation.

Candidate URL:
`https://timing-defense-do-poc.sktjsek.workers.dev/?v036debug=1&fix=cf0362`

Expected health markers:
- `version: 0.36-cf.1`
- `n1: legacy-heavy-xp-restored`
- `n2: legacy-ai-stage-damage-scaling-restored`
- `n3: deferred-explicit-discussion-required`

---

# Immediate boundary
Do **not** start Stage 3 yet.

Slice A must first pass:
1. public health confirmation,
2. real Durable Object N1/N2 verification,
3. Lv5 vs Lv6 differential verification for all five classes,
4. two-human Stage 1–2 multiplayer regression,
5. no duplicate gameplay damage from prediction/presentation,
6. reconnect / Team Shop / Stage 2 result regression smoke.

Only after Slice A PASS:
- preserve an exact Slice A checkpoint,
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
- N1/N2 were explicitly approved and implemented in the v0.36 candidate,
- v0.36 internal contract checks passed,
- v0.36 watched candidate has been triggered for deployment.

Do not claim yet:
- v0.36 Slice A device PASS,
- Stage 3–10 multiplayer parity,
- complete Lv6+ multiplayer authority beyond the Slice A scope,
- final production persistence/security/anti-cheat architecture,
- final numerical balance.

## Deferred UX item
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred. Handle later as a shared responsive-safety layer rather than per-device patches.
