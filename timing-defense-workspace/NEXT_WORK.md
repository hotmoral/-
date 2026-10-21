# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Architecture gate status
Two Cloudflare migration gates are now closed:
1. isolated Workers + Durable Objects viability PoC — **PASS**,
2. real-game v0.31/v0.32 waiting-room parity — **PASS**.

Read before execution:
1. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
2. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
3. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
4. `PROJECT_STATUS.md`
5. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`

Public Cloudflare deployment:
- `https://timing-defense-do-poc.sktjsek.workers.dev`

Validated Cloudflare waiting-room properties:
- real game lobby loads,
- FRIEND room creation / invite join,
- participant nickname/class/slot parity,
- AI FILL slot reservation,
- READY and READY-cancel propagation,
- all-human READY gate,
- non-host START unavailable,
- host-only START,
- one shared future start time,
- synchronized starting/running boundary,
- WAITING refresh/reconnect preserving room/session/slot,
- host refresh preserving host ownership,
- v0.32 Samsung Browser short-landscape layout fix retained.

## Current production baseline
- Latest implemented legacy game prototype: **v0.35**.
- Last Android + PC device-PASS legacy production multiplayer baseline: **v0.34**.
- Cloudflare v0.31/v0.32 waiting-room parity is now device-PASS.
- Render static/backend services remain suspended for **Monthly Quota Exceeded**.
- Live source branch remains `timing-defense-live-v011` at last verified HEAD `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a` unless later verification proves otherwise.

## Balance / UI guard
Do not numerically patch or production-freeze attack damage, monster HP, passive interval, combo coefficients, EXP, shop costs, knockback, stage count/gaps or class balance during this architecture migration.

Required numerical workflow remains:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.

Current combo display/size/position/animation remains approved and frozen unless explicitly requested.

---

# Immediate execution group — v0.33 authoritative Stage 1 parity migration

Do not add Team Shop or Stage 2 yet.

## A. Source-of-truth recovery before implementation
Read existing v0.33 production implementation and reports directly from `timing-defense-live-v011` / workspace.

Recover exact semantics for:
- shared run id / seed,
- shared start state / timing boundary,
- Stage 1 monster count and spawn schedule,
- monster id/type/x/y/HP/maxHP,
- BASE HP / max HP,
- human player authoritative state,
- timing-result action payload and action-sequence contract,
- NORMAL / GOOD / PERFECT and heavy-result resolution,
- EXP / level / charge / combo / kills / coin / damage,
- passive attack interval and damage,
- AI attack timing and consequences,
- enemy wall-hit consequences,
- event ordering / recent event payload,
- Stage 1 clear condition.

Do not infer numerical behavior from memory if code differs.

## B. Migration implementation boundary
Port only v0.33 Stage 1 authoritative consequences onto the existing Cloudflare Durable Object room.

Server/DO owns:
- run identity / seed / status / startAt / combatAt,
- Stage 1 spawn identity and authoritative enemy state,
- BASE HP,
- player combat progression state,
- action-sequence validation,
- passive/AI consequences,
- Stage 1 clear determination,
- ordered combat events.

Client owns:
- local Timing Square input/judgment capture,
- rendering/interpolation,
- presentation-only projectile VFX.

Preserve:
- already-PASS v0.31/v0.32 room/session/slot/host/READY/START contract,
- no numerical balance changes,
- no shop/Stage 2 migration in this slice.

## C. Event-driven architecture requirement
Do not recreate the old continuous 50 ms position integration by default.

Prefer:
- authoritative timestamps,
- deterministic position derived from spawn time / speed / current server time,
- alarms or bounded event scheduling for state transitions that require server-side action,
- state snapshots / ordered events when consequences occur.

Only introduce frequent active execution if measurements demonstrate it is necessary for correctness.

## D. Public device validation gate
Android + PC must validate:
1. same room/READY/START behavior remains intact,
2. both clients enter the same Stage 1 run,
3. same run id/seed/start state,
4. same monster identities and HP,
5. attack from PC reduces the same monster HP on Android,
6. attack from Android reduces the same monster HP on PC,
7. no duplicate client-authoritative damage,
8. BASE HP is identical on both clients,
9. monster death/kill state is identical,
10. EXP/LV/charge/combo/coin candidate state remains authoritative and synchronized,
11. passive/AI consequences appear identically,
12. Stage 1 clear occurs once and is shared,
13. WAITING parity does not regress,
14. Samsung Browser remains usable.

## E. Closure rule
This slice closes only when:
- public Cloudflare deployment succeeds,
- Android + PC authoritative Stage 1 parity is device-PASS,
- reproducible migration defects are fixed,
- no balance values were silently changed,
- canonical docs are synchronized.

A PASS authorizes the next slice only: v0.34 render smoothing / remote projectile parity.

---

# Following migration slice — only after v0.33 Stage 1 PASS
Port v0.34 presentation behavior:
- object reconciliation by server monster id,
- client interpolation toward authoritative targets,
- bounded extrapolation,
- snap on large discontinuity,
- remote human / AI / passive projectile VFX synthesized from authoritative events,
- no duplicate damage from presentation projectiles.

Then device-test Android movement quality and remote projectile visibility.

---

# v0.35 parity migration — only after v0.34 parity PASS
Port:
- production reconnect/session recovery semantics,
- Stage 1 -> Team Shop,
- authoritative coin/ranks/purchase validation,
- shop READY,
- all-human READY gate,
- host-only NEXT,
- synchronized Stage 2 GRUNT/RUNNER combat,
- bounded Stage 2 clear.

Then device-test through Stage 2 and reconnect.

---

# Following game implementation — only after Cloudflare v0.35 parity PASS
1. Generalize the authoritative stage/shop state machine through Stage 10.
2. Add GRUNT / RUNNER / BRUTE / SHIELD / FLYER plus Stage 5/10 bosses.
3. Validate DUO / TRIPLE / FULL room/shop/READY/NEXT behavior.
4. Move Lv6/Lv11/Lv16/Lv21 multiplayer skill consequences under server authority.
5. Strengthen revision/desync diagnostics and reconciliation.
6. Decide durable room lifetime, cleanup and invite-token policy.
7. Implement Lv26/Lv31 only after networking stabilizes.
8. Rerun Solo/2P/3P/4P simulations before numerical freeze.

## Current truth boundary
Safe claims:
- legacy v0.34 Android + PC authoritative Stage 1 is device-PASS,
- legacy v0.34 smoothing and remote projectile VFX are device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks,
- Render outage is a hosting quota suspension, not proven gameplay regression,
- Cloudflare isolated PoC is public two-client device-PASS,
- Cloudflare v0.31/v0.32 waiting-room parity is public Android + PC device-PASS.

Do not claim:
- Cloudflare v0.33 Stage 1 parity yet,
- Cloudflare v0.34 render parity yet,
- Cloudflare v0.35 parity,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final production persistence/security/balance semantics.
