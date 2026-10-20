# Timing Defense — Session Handoff

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live source branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Latest implemented prototype: **v0.35**
- Previous device-validated prototype: **v0.34**
- Old Render game URL: `https://timing-defense-v011.onrender.com/v035.html` — **SUSPENDED / Monthly Quota Exceeded**
- Old Render backend: `https://timing-defense-mp.onrender.com` — **SUSPENDED / Monthly Quota Exceeded**
- Last successful v0.35 static deploy: `dep-dbblp8s9v7es73flhq40`
- Last successful v0.35 backend deploy: `dep-dbblpauq1p3s73d1v2mg`
- Current live source HEAD: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Workspace is canonical for design decisions, simulation interpretation, execution boundary and new-session recovery.

---

# CRITICAL CURRENT INCIDENT

v0.35 itself was not proven broken.

Render events show both services were suspended after successful deployment:
- backend `srv-dbbimre1egvs73861d80`: `service_suspended` at `2026-10-20T12:39:35Z`
- static site `srv-dbb1c9mi0phs73b5bao0`: `service_suspended` at `2026-10-20T12:39:36Z`
- actor/reason on both: **`Monthly Quota Exceeded`**

Therefore:
- do **not** treat the unreachable v0.35 URL as a gameplay/runtime regression,
- do **not** spend time patching v0.35 client/server code solely because the old link is down,
- replacement hosting is the immediate execution boundary.

Read `V035_RENDER_QUOTA_OUTAGE_REPORT.md` before doing anything else.

---

# Portable hosting preparation already completed

The live branch has already been prepared to move away from the old Render static+backend split.

Files:
- `timing-defense-v011/v035-host-adapter.js`
- `timing-defense-v011/v035-portable.html`
- `timing-defense-server/portable-host.js`

Purpose:
- serve the game frontend and authoritative Node backend from one full-stack Node host,
- proxy `/health` and `/api/*` to the authoritative server,
- rewrite the old hard-coded Render backend endpoint to same-origin when running on the replacement host.

Portable-host commit:
- `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`
- message: `Add portable full-stack host wrapper for Timing Defense`

Local checks already recorded as PASS:
- Node syntax checks,
- portable root/static routing,
- `/health` proxy to v0.35 backend.

Do not duplicate this preparation unless live repository verification shows a mismatch.

---

# Validated gameplay/network foundation

## v0.31 / v0.32
Two independent clients device-validated:
- real FRIEND/LINK room create/join,
- nickname/class/slot sharing,
- READY propagation,
- host-only START after all humans READY,
- shared RUN STARTING state,
- Samsung Browser waiting-room clipping fixed.

## v0.33
Android + PC device-validated:
- shared authoritative Stage 1,
- remote PC attack reduces the same monster HP on Android.

## v0.34
Android + PC device-validated:
- monster motion smoother on Android,
- remote human projectile visible,
- server-authoritative HP state preserved.

This is the last device-validated public behavior baseline.

---

# v0.35 implemented scope — not yet device-PASS

Read `V035_RECONNECT_SHOP_STAGE2_REPORT.md`.

Implemented:
- 180 s same-server reconnect/session grace,
- same room URL reload via `/resume`,
- authoritative snapshot recovery,
- suppression of historic combat-event replay after resume,
- authoritative Stage 1 -> Team Shop,
- per-human coin/ranks/purchase validation,
- READY lock/unlock,
- all-human READY gate,
- host-only NEXT STAGE,
- synchronized future Stage 2 start,
- Stage 2 authoritative GRUNT/RUNNER combat,
- Stage 2 bounded endpoint at `stage2-clear`.

Local API/integration checks passed before the hosting outage.
Android + PC device validation did not complete because Render suspended both services.

---

# Frozen combat / balance governance
- Rhythm: `X → X → X → X+Y`.
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line penetration; no seeking/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Balance gaps must be reported/discussed before numerical patching.
- Current combo display/size/position/animation is approved and must not change without explicit request.

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

# Truth boundary
Safe claims:
- v0.34 real two-client authoritative Stage 1 is device-PASS,
- v0.34 Android smoothing and remote projectile VFX are device-PASS,
- v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks,
- portable replacement-host wrapper exists and passed local routing/health checks.

Do not claim:
- v0.35 device-PASS,
- current Render availability,
- durable recovery after backend process restart,
- Stage 3–10 multiplayer,
- full Lv6+ multiplayer skill authority,
- persistent/horizontally-scaled room storage,
- final production shop/shared-wall semantics.

---

# Exact next work boundary

The next session should **not** start new gameplay features first.

1. Read canonical docs and verify live HEAD.
2. Confirm the Render outage evidence and do not retry old Render URLs as the primary recovery plan while quota remains exhausted.
3. Deploy `portable-host.js` + v0.35 portable frontend to a replacement full-stack Node host.
4. Validate on the new host:
   - root page,
   - static JS/assets,
   - `/health`,
   - room create/join,
   - SSE room stream,
   - CORS/same-origin behavior.
5. Then Android + PC device-test v0.35:
   - Stage 1,
   - Team Shop,
   - purchases,
   - READY propagation,
   - host-only NEXT,
   - synchronized Stage 2,
   - refresh/reconnect during Stage 1/shop/Stage 2.
6. Fix only reproducible v0.35 defects.
7. Only after v0.35 device-PASS, generalize the authoritative stage/shop state machine through Stage 3–10.
8. Then move Lv6/Lv11/Lv16/Lv21 multiplayer effects server-side.
9. Later implement Lv26/Lv31 and rerun Solo/2P/3P/4P simulations before numerical freeze.

---

# New-session read order
1. `SESSION_HANDOFF.md`
2. `PROJECT_STATUS.md`
3. `V035_RENDER_QUOTA_OUTAGE_REPORT.md`
4. `V035_RECONNECT_SHOP_STAGE2_REPORT.md`
5. `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`
6. `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`
7. `V032_WAITING_LAYOUT_HOTFIX_REPORT.md`
8. `V031_MULTIPLAYER_FOUNDATION_REPORT.md`
9. `V030_ROOT_CAUSE_RECOVERY_REPORT.md`
10. `DESIGN_DECISIONS.md`
11. `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`
12. `BALANCE_SIM_REPORT_V7_V016_EXACT.md`
13. `SKILL_PLAN_LV6_31.md`
14. `TIER_PRESSURE_GRAMMAR_V1.md`
15. `PRESSURE_RECIPES_V1.md`
16. `SIMULATION_METHOD.md`
17. `NEXT_WORK.md`
