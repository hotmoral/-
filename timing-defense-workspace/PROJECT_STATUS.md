# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Latest implemented prototype: **v0.35**
- Previous device-validated prototype: **v0.34**
- Old Render game URL: `https://timing-defense-v011.onrender.com/v035.html` — **SUSPENDED / Monthly Quota Exceeded**
- Old Render multiplayer backend: `https://timing-defense-mp.onrender.com` — **SUSPENDED / Monthly Quota Exceeded**
- Last successful v0.35 static deploy: `dep-dbblp8s9v7es73flhq40`
- Last successful v0.35 backend deploy: `dep-dbblpauq1p3s73d1v2mg`
- Current live-branch portable-host preparation HEAD: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

Important: v0.35 was built/deployed successfully, then both Render services were suspended around 12:39 UTC because the monthly quota was exceeded. This is a hosting outage, not a confirmed v0.35 gameplay/runtime regression. Read `V035_RENDER_QUOTA_OUTAGE_REPORT.md`.

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Solo prototype: Stage 1–10 with EXP / level / coin / shop.
- Multiplayer prototype code: real shared waiting room + authoritative Stage 1 -> team shop -> Stage 2 bounded slice.
- Local/solo skills implemented through Lv21; Lv26/Lv31 planned.
- Multiplayer Lv6+ skill authority is not complete.

## Frozen combat / balance governance
- Knight = stable generalist / penetration / strong heavy.
- Rogue = multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line penetration; no seeking/bending.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Simulation findings must be reported/discussed before numerical rebalance.
- Combo display/size/position/animation is approved and must not change without explicit user request.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`,
- ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

Approved class radar axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

---

# Stable UI/runtime foundation
- Animated class radar and 3×2 skill roadmap.
- Rogue HUD charcoal/black + silver.
- BASE HP top-center; top-right STAGE → LV → KILLS.
- Combat title removed; combo untouched.
- Landscape-only orientation gate.
- v0.30 blocks the v0.27 self-retriggering MutationObserver regression.
- v0.28/v0.29 viewport forcing is superseded and not loaded.
- v0.32 fixed FRIEND/LINK lower-content clipping.

---

# Multiplayer milestones

## v0.31 / v0.32 — waiting room: device validated
Two independent clients verified:
- real FRIEND/LINK room create/join,
- participant nickname/class/slot sharing,
- READY propagation,
- host-only START after all humans READY,
- shared RUN STARTING state,
- Samsung Browser waiting-room layout pass.

## v0.33 — authoritative Stage 1: device validated
Read `V033_MULTIPLAYER_COMBAT_SLICE_REPORT.md`.

Server owns run/world state and resolves human timing actions, passive attacks and AI FILL attacks. User validation on Android + PC confirmed that a remote PC attack reduces the same monster HP on Android.

## v0.34 — smoothing / remote VFX: device validated
Read `V034_MULTIPLAYER_RENDER_SMOOTHING_REPORT.md`.

User confirmed:
- Android monster movement became smoother,
- remote player projectiles became visible.

Server authority remained unchanged; rendering is visual-only interpolation/VFX.

## v0.35 — reconnect + authoritative team shop + Stage 2
Read `V035_RECONNECT_SHOP_STAGE2_REPORT.md` and `V035_RENDER_QUOTA_OUTAGE_REPORT.md`.

Implemented:
- 180 s in-memory reconnect/session grace,
- reload recovery through `/resume` and authoritative run snapshot,
- old-event replay suppression on immediate recovery,
- authoritative Stage 1 -> team shop transition,
- per-human server-owned coin/ranks/purchases,
- shop READY toggle and all-human READY gate,
- host-only NEXT STAGE,
- synchronized future Stage 2 start,
- authoritative Stage 2 GRUNT/RUNNER combat slice,
- Stage 2 bounded endpoint at `stage2-clear`.

Shop uses the existing upgrade/cost grammar without numerical rebalance. Human offensive ranks are resolved by the server. WALL HP and DEF currently map to the shared base as a prototype team-wall rule; this mapping is not production-frozen.

Android + PC device validation did **not** complete because Render suspended both services for `Monthly Quota Exceeded` after successful deployment.

Portable-host recovery files now exist on the live branch:
- `timing-defense-v011/v035-host-adapter.js`
- `timing-defense-v011/v035-portable.html`
- `timing-defense-server/portable-host.js`

These allow the game and authoritative Node backend to be deployed together on a replacement full-stack Node host.

---

# Multiplayer truth boundary
Safe today:
- real authoritative shared room/READY/START validated through v0.34,
- real authoritative Stage 1 combat validated,
- remote smoothing/projectiles validated on Android + PC,
- v0.35 reconnect/team-shop/Stage-2 code exists and passed local API/integration checks,
- portable hosting recovery path is prepared.

Do not claim device-PASS for v0.35 until replacement hosting is live and Android + PC validation is completed.
Do not claim:
- durable recovery after backend restart,
- Stage 3–10 multiplayer,
- full multiplayer Lv6+ skill consequences,
- persistent/horizontally-scaled room storage,
- final production shop ownership/shared-wall policy.

---

# Immediate next boundary
1. Move v0.35 to a replacement full-stack Node host; Render cannot currently serve it because the monthly quota is exhausted.
2. Validate the replacement host's root/static/API/SSE paths.
3. Android + PC validate v0.35 Stage 1 -> shared shop.
4. Confirm independent purchases/ranks/coins stay synchronized.
5. Confirm READY both clients and host-only NEXT.
6. Confirm both enter synchronized Stage 2 and share GRUNT/RUNNER HP/deaths/BASE HP.
7. Refresh one client during Stage 1, shop and Stage 2; verify same slot/run recovery without old-shot replay.
8. Fix only reproducible v0.35 network/runtime/UI defects.
9. Generalize the same authoritative stage/shop contract through Stage 3–10.
10. Move Lv6/Lv11/Lv16/Lv21 multiplayer skill consequences under server authority.
11. Then implement Lv26/Lv31 and rerun Solo/2P/3P/4P simulations before numerical freeze.

## Still unresolved / not production-frozen
- replacement production/prototype host,
- durable multiplayer storage / server-restart recovery,
- horizontal scaling strategy,
- invite-link security/token policy,
- Stage 3–10 authority,
- production team shop/shared-wall ownership rules,
- complete Lv6+ multiplayer skill authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation details,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X pressure/tier values,
- final result-board metric policy.
