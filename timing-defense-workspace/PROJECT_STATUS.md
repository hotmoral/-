# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.27**
- Public URL: `https://timing-defense-v011.onrender.com/v027.html`
- Live source HEAD: `6208e5d4665ca6acb6ebbd1105c50c0551c03630`
- Render deploy: `dep-dbbhfp3rjlhs73e9nvp0` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Stage 1–10 run with EXP / level / coin / shop.
- Class skills implemented through Lv21; Lv26/Lv31 planned.
- AI teammates use internal timing/EXP/level/skills without visible AI Timing Squares.

## Frozen combat / role rules
- Knight = stable generalist / penetration / strong heavy.
- Rogue = fast multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line penetration; no bending or seeking.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Simulation does not self-authorize numerical rebalance.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`, ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

**Regression guard:** combo display/size/position/animation must remain unchanged from the current approved state unless the user explicitly requests otherwise.

---

# Presentation / UX progression
## v0.24
- Five-level six-axis radar added.
- Radar axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`.
- Approved profile values:
  - Knight `4/2/3/3/4/2`
  - Rogue `2/5/5/1/1/1`
  - Tank `2/1/1/5/1/3`
  - Archer `3/2/4/1/5/2`
  - Mage `4/2/2/1/1/5`
- Skill roadmap changed to `3 × 2`.
- Rogue HUD became charcoal/black + silver.

## v0.25
- Character-select vertical space reclaimed.
- Radar labels enlarged.
- Richer class role/detail copy restored.

## v0.26
See `V026_HUD_LAYOUT_REPORT.md`.
- Skill card layout changed to icon + name / `습득 LV N`, full-width description below.
- Class name moved above hero head.
- Combat title removed while combo remained untouched.
- BASE HP moved to a formal top-center gauge.
- Top-right HUD = icon + STAGE → icon + LV → icon + KILLS.
- Home base received fortified structure art.
- Combat six-skill strip now reuses the character-select skill artwork.

---

# v0.27 — current
See `V027_DEVICE_FIX_WAITING_UX_REPORT.md`.

## Character select fixes
- Skill names never wrap.
- `습득 LV N` never wraps.
- Skill/card fonts are slightly reduced to preserve one-line headers.
- Radar canvas preserves its native `330:280` aspect ratio, preventing vertical squash.
- Radar data and animation are unchanged.
- Carousel swipe replaced with pointer capture + horizontal-intent detection for Android reliability.
- Arrow navigation remains fixed and separate.

## End-run board
- PLAYER / CLASS overlap fixed structurally.
- Player/CPU name is single-line.
- Class is a compact same-row badge instead of a second line.
- Four-player row spacing recalculated.
- RETRY / LOBBY separation improved.

## TEAM waiting-room UX
TEAM start now opens a real UI state rather than a temporary text flash.

Shared:
- nickname/class preserved,
- AI FILL position/class preserved,
- P1 local player,
- P2/P3/P4 = AI FILL or HUMAN SLOT,
- local READY toggle,
- back to PLAY SETTING,
- START disabled until real network authority exists.

FRIEND:
- INVITE affordance, truthful “network not connected” feedback.

LINK:
- ROOM LINK affordance, no fake URL generation.

RANDOM:
- SEARCH / CANCEL SEARCH UI state,
- explicitly marked `NETWORK NOT CONNECTED`,
- no fake match success.

---

# Network truth boundary
Actual multiplayer is **not yet implemented**.
Do not claim remote connectivity until two independent clients join the same authoritative room and share synchronized game state.

TEAM slot rule:
- SOLO AI: 0–3
- TEAM AI FILL: 0–2, preserving at least one human slot.

---

# Next boundary
1. Device-test v0.27 on the same Android landscape device.
2. Verify skill title/level one-line behavior.
3. Verify radar proportions.
4. Verify swipe and arrow navigation together.
5. Verify result rows no longer overlap.
6. Verify TEAM waiting screens for FRIEND/LINK/RANDOM.
7. Fix only implementation/visual defects from validation.
8. Then design and implement actual multiplayer room/network architecture.
9. Later return to Lv26/Lv31 implementation, full-run pressure simulation, and final balance freeze.

## Still unresolved / not production-frozen
- actual room authority / backend transport,
- invite-link security contract,
- random matchmaking queue,
- disconnect/reconnect/reconciliation,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL synchronization rules,
- Lv26/Lv31 implementation coefficients,
- final passive/HP/combo coefficients,
- final E/X pressure values and tier structure,
- final result-board metric policy.
