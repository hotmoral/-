# Timing Defense — Session Handoff

Updated: 2026-10-21 KST

## Current execution status
Cloudflare Workers + Durable Objects architecture viability PoC is **PASS**.

Do not resume the old Render-replacement Node-host lane as the primary path unless Cloudflare migration later fails by evidence.

The next implementation boundary is **v0.31/v0.32 waiting-room parity migration onto Durable Object + WebSocket**.

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Cloudflare experimental branch: `timing-defense-cloudflare-do-poc`
- Latest implemented production prototype: **v0.35**
- Last Android + PC device-PASS production prototype: **v0.34**
- Last verified production live HEAD before Cloudflare migration: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- Public Cloudflare PoC: `https://timing-defense-do-poc.sktjsek.workers.dev`

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

# Cloudflare Durable Objects PoC — PASS
Read `CLOUDFLARE_DO_POC_PASS_2026-10-21.md`.

Validated publicly with two independent clients:
- Worker/static page loads,
- `/api/health` reports the intended architecture,
- SQLite-backed Durable Object room creation,
- WebSocket Hibernation transport,
- `apac-ne` location hint,
- room join,
- participant/host state sharing,
- READY propagation,
- host START,
- one authoritative diagnostic monster,
- shared HP `300 -> 200 -> 100 -> 0`,
- synchronized `CLEAR`,
- refresh/reconnect preserving the same shared room/session/slot/state,
- post-refresh continued interaction,
- event-driven operation without the legacy 50 ms always-on loop.

This is an architecture PASS only. It is **not** v0.35 parity.

The experimental PoC did not modify the production/live branch.

---

# Validated production gameplay/network foundation

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

This remains the last device-validated production behavior baseline.

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

# Exact next work boundary
Do not add Stage 1 combat to Cloudflare before closing waiting-room parity.

1. Re-read v0.31/v0.32 implementation and reports from GitHub; do not reconstruct semantics from memory if code differs.
2. Port the production room/session/slot/host/READY/START contract onto Durable Object + WebSocket.
3. Preserve FRIEND/LINK behavior, nickname/class/slot sharing, all-human READY gate and host-only START.
4. Preserve one shared authoritative future start time / starting state.
5. Preserve v0.32 Samsung Browser waiting-room layout fixes.
6. Public Android + PC device-test the waiting-room flow including reconnect and READY cancel.
7. Fix only reproducible parity defects.
8. Synchronize canonical docs when this slice is PASS.
9. Only then port v0.33 authoritative Stage 1 consequences.
10. Use event/time-derived movement where safe instead of recreating the legacy 50 ms always-on loop.
11. Preserve v0.34 smoothing/projectile behavior as presentation-only behavior.
12. Then port v0.35 reconnect/Team Shop/Stage 2.
13. Only after Cloudflare v0.35 parity device-PASS, proceed to Stage 3–10 and Lv6+ multiplayer authority.

---

# Truth boundary
Safe claims:
- v0.34 real two-client authoritative Stage 1 is device-PASS,
- v0.34 Android smoothing and remote projectile VFX are device-PASS,
- v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks,
- Render quota incident is confirmed,
- Cloudflare Workers + Durable Objects isolated public two-client PoC is device-PASS including refresh/reconnect.

Do not claim:
- production v0.31 parity on Cloudflare yet,
- v0.35 Cloudflare device-PASS,
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
6. `V035_RENDER_QUOTA_OUTAGE_REPORT.md`
7. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
8. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
9. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
10. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
11. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
12. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
13. `DESIGN_DECISIONS.md`
14. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
15. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
16. `SKILL_PLAN_LV6_31.md`
17. `TIER_PRESSURE_GRAMMAR_V1.md`
18. `PRESSURE_RECIPES_V1.md`
19. `SIMULATION_METHOD.md`
