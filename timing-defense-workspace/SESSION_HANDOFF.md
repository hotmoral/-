# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current execution status
Cloudflare Workers + Durable Objects migration now has two closed public device-validation gates:
- isolated architecture viability PoC — **PASS**,
- real-game v0.31/v0.32 waiting-room parity — **PASS**.

The next implementation boundary is **v0.33 authoritative Stage 1 parity migration onto Durable Object + WebSocket**.

Do not resume the old Render-replacement Node-host lane as the primary path unless Cloudflare migration later fails by evidence.

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Cloudflare deployment pointer branch: `timing-defense-cloudflare-do-poc`
- v0.31/v0.32 parity implementation branch: `timing-defense-cloudflare-v031-parity`
- preserved PoC PASS checkpoint: `timing-defense-cloudflare-do-poc-pass-20261021`
- Latest implemented legacy production prototype: **v0.35**
- Last Android + PC device-PASS legacy production prototype: **v0.34**
- Last verified legacy live HEAD before Cloudflare migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- Public Cloudflare URL: `https://timing-defense-do-poc.sktjsek.workers.dev`
- Validated v0.31/v0.32 deployment pointer HEAD: `e6db85f22f04b2566960c98867c19cebf8fc1a4b`

Workspace remains canonical for design decisions, migration boundaries, balance governance and new-session recovery.

---

# Hosting incident classification
Old Render services were suspended after successful v0.35 deployments because of **Monthly Quota Exceeded**.

Therefore:
- the old Render outage is not evidence that v0.35 gameplay/runtime failed,
- do not patch production gameplay solely because the Render URLs are down,
- the portable Node wrapper remains a fallback only.

Read:
- `V035_RENDER_QUOTA_OUTAGE_REPORT.md`
- `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`

---

# Cloudflare architecture / migration gates

## Durable Objects isolated PoC — PASS
Read `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`.

Validated publicly with two independent clients:
- Worker/static page,
- SQLite-backed Durable Object room,
- WebSocket Hibernation,
- shared authoritative diagnostic state,
- refresh/reconnect preserving room/session/slot/state,
- event-driven operation without the legacy 50 ms always-on loop.

## v0.31 / v0.32 real-game parity — PASS
Read `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`.

Validated on Android Samsung Browser + independent PC:
- actual Timing Defense lobby/waiting-room UI loads,
- FRIEND room create/invite join,
- participant nickname/class/slot parity,
- AI FILL slot reservation,
- READY propagation both ways,
- READY cancel propagation,
- all-human READY gate,
- non-host START unavailable,
- host-only START,
- one shared future start gate,
- synchronized `RUN GATE OPEN`,
- WAITING refresh/reconnect preserving room/session/slot,
- host refresh preserving host ownership,
- other client remaining online,
- v0.32 Samsung Browser short-landscape layout fix retained.

This closes waiting-room parity and authorizes only the v0.33 Stage 1 migration slice.

---

# Validated legacy gameplay/network foundation

## v0.31 / v0.32 — Android + PC device validated
- real FRIEND/LINK room create/join,
- nickname/class/slot sharing,
- READY propagation,
- host-only START after all humans READY,
- shared future start gate,
- Samsung Browser short-landscape waiting-room clipping fix.

## v0.33 — Android + PC device validated
- shared authoritative Stage 1,
- server-owned enemy/base state,
- server-resolved human timing attacks,
- remote PC attack reduces the same monster HP on Android.

## v0.34 — Android + PC device validated
- smoother Android monster motion,
- remote human projectile VFX,
- authoritative HP state preserved.

This remains the last device-validated legacy production behavior baseline.

## v0.35 — implemented, not production device-PASS
Implemented and locally API/integration checked:
- same-server reconnect/session recovery,
- Stage 1 -> Team Shop,
- per-human coin/rank/purchase authority,
- shop READY synchronization,
- all-human READY gate,
- host-only NEXT STAGE,
- synchronized Stage 2 GRUNT/RUNNER combat,
- Stage 2 bounded clear.

Device validation was interrupted by the Render quota suspension.

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
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Balance gaps must be reported/discussed before numerical patching.
- Current combo display/size/position/animation is approved; do not change unless explicitly requested.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

Approved radar axes: 공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

---

# Exact next work boundary — v0.33 Stage 1 parity
Do not add Team Shop or Stage 2 yet.

1. Re-read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md` and the exact v0.33 live/server/client implementation from GitHub.
2. Recover the authoritative Stage 1 run contract before coding.
3. Port shared run id / seed / startAt / combatAt.
4. Port Stage 1 spawn identity and schedule.
5. Port authoritative monster HP/death and BASE HP.
6. Port monotonic human action sequence and timing-result actions.
7. Port passive/AI consequences.
8. Port EXP / LV / coin / charge / combo / kills / damage state.
9. Preserve already-PASS v0.31/v0.32 room/session/slot/host/READY/START behavior.
10. Prefer time-derived authoritative movement state over an always-on 50 ms loop where safe.
11. Public Android + PC device-test shared Stage 1 state and cross-device damage.
12. Fix only reproducible parity defects; make no silent numerical balance changes.
13. Synchronize canonical docs on PASS.
14. Only then port v0.34 smoothing/extrapolation and remote projectile presentation.
15. Then port v0.35 reconnect/Team Shop/Stage 2.
16. Only after Cloudflare v0.35 parity device-PASS, proceed to Stage 3–10 and Lv6+ multiplayer authority.

---

# Truth boundary
Safe claims:
- legacy v0.34 real two-client authoritative Stage 1 is device-PASS,
- legacy v0.34 Android smoothing and remote projectile VFX are device-PASS,
- legacy v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks,
- Render quota incident is confirmed,
- Cloudflare isolated public two-client PoC is device-PASS,
- Cloudflare v0.31/v0.32 waiting-room parity is public Android + PC device-PASS including READY cancel, host-only START, future start gate and WAITING refresh/reconnect.

Do not claim:
- Cloudflare v0.33 authoritative Stage 1 parity yet,
- Cloudflare v0.34 render smoothing/projectile parity yet,
- Cloudflare v0.35 device-PASS,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer skill authority,
- final persistence/security/shop/shared-wall semantics,
- final numerical balance.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md`
5. `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`
6. `CLOUDFLARE_V031_V032_PARITY_PASS_2026-10-21.md`
7. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
8. `V035_RENDER_QUOTA_OUTAGE_REPORT.md`
9. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
10. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
11. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
12. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
13. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
14. `DESIGN_DECISIONS.md`
15. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
16. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
17. `SKILL_PLAN_LV6_31.md`
18. `TIER_PRESSURE_GRAMMAR_V1.md`
19. `PRESSURE_RECIPES_V1.md`
20. `SIMULATION_METHOD.md`
