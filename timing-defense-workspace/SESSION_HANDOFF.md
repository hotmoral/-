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

Active slice:
- **v0.36 Slice A — automated validation PASS / final short device smoke pending**

Public URL:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

## Preserved checkpoints
- PoC PASS: `timing-defense-cloudflare-do-poc-pass-20261021`
- v0.31/v0.32 PASS: `timing-defense-cloudflare-v031-v032-pass-20261021`
- v0.33 PASS: `timing-defense-cloudflare-v033-pass-20261021`
- v0.34 PASS: `timing-defense-cloudflare-v034-pass-20261021`
- v0.35 full PASS: `timing-defense-cloudflare-v035-pass-20261021`
- v0.36 automated PASS: `timing-defense-cloudflare-v036-automation-pass-20261021`

Exact v0.35 validated HEAD:
`b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`

Exact v0.36 automated-tested deployment HEAD:
`abb2d428df546c257181278ba6bd0814e0471c93`

Watched deployment branch:
`timing-defense-cloudflare-do-poc`

## Read first
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_V036_AUTOMATION_PASS_2026-10-21.md`
5. `CLOUDFLARE_V036_AUTOMATED_VALIDATION_2026-10-21.md`
6. `CLOUDFLARE_V036_SLICE_A_DECISION_2026-10-21.md`
7. `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`
8. `CLOUDFLARE_V035_PASS_2026-10-21.md`
9. `DESIGN_DECISIONS.md`
10. `SKILL_PLAN_LV6_31.md`
11. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`

## v0.35 PASS baseline
Android + PC established:
- shared authoritative Stage 1 and Stage 2,
- Team Shop purchase/coin/rank authority,
- shop pending feedback and duplicate-tap protection,
- all-human READY + host NEXT,
- authoritative Stage 2 clear/results,
- reconnect,
- Rogue CHARGE visual fix,
- remote human timing projectile parity.

Do not reopen v0.35 without regression evidence.

## Post-v0.35 preflight conclusions
- Stage 3–10 exact legacy encounter contracts were recovered.
- Do not replace them with future S/E/X pressure recipes during migration.
- Stage-2-specific server/client assumptions must be generalized before later stages.
- BRUTE/SHIELD/FLYER, Stage 5/10 bosses and authoritative Y geometry are not yet migrated.
- room/READY/shop/session foundations are reusable for 3–4 slots, but larger-party event volume must be tested automatically.
- playable legacy skill authority baseline is Lv6/11/16/21.
- Lv26/Lv31 remain design-roadmap only.

## Explicit numerical decisions
### N1 — APPROVED / IMPLEMENTED / AUTOMATED PASS
Timing EXP exact table:
- NORMAL 8
- GOOD 12
- PERFECT 18
- HEAVY 10
- HEAVY+ 14
- GREAT 18
- SUPER 23
- CRITICAL 28

### N2 — APPROVED / IMPLEMENTED / AUTOMATED PASS
AI stage multiplier:
`1 + (stage - 1) * 0.035`

### N3 — DEFERRED / MANDATORY FUTURE DISCUSSION
N3 is the experimental combo-milestone extra-attack system.
It is **not discarded** and not part of Slice A.
Do not silently port, remove, freeze or rebalance it; explicit discussion is required later.

## v0.36 Slice A implementation
No Stage 3 is enabled.

Server-authoritative Lv6 consequences:
- Knight: +12% damage.
- Rogue: +55 ms authoritative second dagger at 55%, same target allowed with nearest fallback.
- Tank: +30% knockback.
- Archer: up to two strict-line 52% secondary hits, no seeking.
- Mage: up to three nearby 50% splash hits.

Infrastructure:
- action/cast identity,
- secondary hit indices and skill metadata,
- scheduled Rogue secondary queue,
- authoritative Archer/Mage target selection,
- secondary presentation from server events.

### cf.2 hardening
Code audit caught two integration risks before final device closure:
1. legacy Rogue local secondary could still execute client gameplay mutation in network mode; this was blocked,
2. new Lv6 secondary VFX initially used an independent event floor; it now inherits the v0.35 resume floor to prevent historical replay after reconnect.

## v0.36 cf.3 automated validation — PASS
User ran the public one-click suite in Samsung Browser and supplied screenshot evidence:
- `SERVER · PASS · 10/10`
- `CLIENT · PASS · 4/4`
- `MULTICLIENT · PASS · 9/9`
- `FINAL · PASS`

Automated suite covers:
- N1/N2 exact values,
- all five Lv6 authority boundaries,
- action identity / hit indices,
- stale/duplicate `seq` rejection,
- Rogue local mutation block,
- reconnect event-floor / duplicate VFX prevention,
- two real WebSocket clients against deployed Durable Object,
- READY/START/shared Stage1/resume/reconnect/Shop/Stage2 synchronization.

Manual class-by-class phone verification is no longer required for exact numerical behavior.

## Immediate next boundary
Do **not** start Stage 3 yet.

Only one Slice A gate remains: one short actual-game device smoke limited to browser/render/touch behavior the simulation cannot fully prove:
- game assets load,
- Timing Square touch responds,
- no obvious duplicate projectile, stale VFX replay, flicker or visual corruption,
- Stage 1 -> Team Shop -> Stage 2 is visibly usable.

If that smoke PASS:
1. declare v0.36 Slice A full PASS,
2. preserve the exact full-PASS branch from the tested deployment HEAD,
3. synchronize canonical status/handoff,
4. disable/remove candidate-only debug controls as appropriate,
5. open Slice B only.

## Slice B after Slice A PASS
Stage 3 only, two humans first:
- Stage 2 clear -> Team Shop,
- host NEXT -> Stage 3,
- exact legacy Stage 3: `12 enemies / 980 ms / GRUNT 44% / RUNNER 34% / BRUTE 22%`,
- authoritative BRUTE,
- Stage 3 clear -> Team Shop,
- Stage 4 remains blocked.

## Following slices
- larger-party baseline: 3H / 4H / 2H+2AI / 3H+1AI,
- Stage 4 SHIELD,
- Stage 5–6 boss + FLYER + Y geometry,
- Stage 7–9 mixed-roster stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with automated forced-level tests before progression relies on them.

## Deferred UX
Heterogeneous phone-size/aspect-ratio responsive safety remains deferred until after the current migration authority work. Implement later as a shared responsive-safety layer, not per-device patches.

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

## Truth boundary
Safe:
- Cloudflare PoC through v0.35 device-PASS,
- exact v0.35 PASS preserved,
- N1/N2 approved, implemented and automatically validated,
- v0.36 cf.3 server/client/multiclient automated suite PASS,
- exact v0.36 automated-pass deployment preserved.

Not yet safe:
- v0.36 Slice A full device PASS,
- Stage 3–10 multiplayer parity,
- Lv6+ authority beyond Slice A,
- final persistence/security/anti-cheat architecture,
- final numerical balance.
