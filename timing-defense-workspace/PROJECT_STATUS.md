# Timing Defense — Project Status

Updated: 2026-10-20 KST

## Canonical locations
- Repository: `hotmoral/-`
- Live branch: `timing-defense-live-v011`
- Planning / balance / handoff branch: `timing-defense-workspace`
- Current public LIVE prototype: **v0.30**
- Public URL: `https://timing-defense-v011.onrender.com/v030.html`
- Live source HEAD: `a235bf2dc0bd5bb5138b4bd89d81512345ec6713`
- Render deploy: `dep-dbbhud8n74is73cp0rug` / LIVE

## Core playable scope
- Landscape timing-action side defense.
- Rhythm: `X → X → X → X+Y`.
- Classes: Knight / Rogue / Tank / Archer / Mage.
- Monsters: GRUNT / RUNNER / BRUTE / SHIELD / FLYER.
- Stage 1–10 run with EXP / level / coin / shop.
- Class skills implemented through Lv21; Lv26/Lv31 planned.
- AI teammates use internal timing/EXP/level/skills without visible AI Timing Squares.

## Frozen role / combat direction
- Knight = stable generalist / penetration / strong heavy.
- Rogue = fast multihit / crit / durable-normal execution; same-target dagger hits uncapped.
- Tank = knockback / wall protection / team specialist.
- Archer = strict straight-line penetration; no bending/seeking.
- Mage = density/AoE specialist.
- Boss dagger scalar `0.70`.
- Boss knockback scalar `0.40`.
- EXP remains tied to valid timing events; passive attacks grant no EXP.
- Simulation findings must be reported/discussed before numerical rebalance.
- Combo display/size/position/animation is approved and must not change without explicit user request.

Experimental, not production-frozen:
- passive `40 raw / 2.0 s`, ordinary non-boss HP +10%,
- combo persistent candidate `5/8/12/15%`,
- combo milestone raw-equivalent `60/90/150/210` cap.

## Approved class radar
Axes: `공격력 / 치명타 / 민첩성 / 넉백 / 관통 / 광역`

Profiles:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

Five visual levels. Equal levels are allowed. Radar is class-identity presentation, not a literal raw-stat dump.

---

# Presentation / UX state

## v0.24–v0.26 foundation
- Animated five-level radar.
- Skill roadmap `3 × 2`.
- Rich class role/detail copy.
- Rogue HUD charcoal/black + silver.
- Skill cards = icon + name / `습득 LV N` + full-width description.
- Hero class name above the character.
- Combat title removed; combo untouched.
- BASE HP formal top-center gauge.
- Top-right HUD order: STAGE → LV → KILLS.
- Fortified home-base visual.
- Combat six-skill strip reuses lobby skill artwork.

## v0.27 desired UX features
Read `V027_DEVICE_FIX_WAITING_UX_REPORT.md`.

Desired features retained by v0.30:
- skill names stay one line,
- `습득 LV N` stays one line,
- radar preserves `330:280` aspect ratio,
- Android swipe uses pointer capture + horizontal-intent detection,
- arrows remain fixed,
- result board uses same-row class badge to avoid PLAYER / CLASS collision,
- TEAM waiting UX exists for FRIEND / LINK / RANDOM without fake networking.

## v0.27 regression found after device audit
A concrete infinite MutationObserver loop exists in the skill-level normalizer:
- observer watches lobby subtree child changes,
- callback writes `.textContent` even when the text is already identical,
- that write can retrigger the same observer indefinitely.

The earlier v0.26 normalizer had an equality guard; v0.27 lost it.

This regression is now treated as the primary root cause of the severe partial-render/freeze state first observed after v0.27.

## v0.28 / v0.29 status
These viewport-repair experiments are **superseded and not loaded by v0.30**.
They attempted to repair a half-width symptom before the v0.27 observer loop was identified. Do not continue numerical/physical viewport forcing from those versions unless new evidence requires it.

---

# v0.30 — current recovery build
Read `V030_ROOT_CAUSE_RECOVERY_REPORT.md`.

Files:
- `timing-defense-v011/v030-safety.js`
- `timing-defense-v011/v030.html`

Loader strategy:
1. load the known v0.26 foundation,
2. load `v030-safety.js`,
3. load existing v0.27 UX patch.

`v030-safety.js` intercepts only the redundant v0.27 `normalizeSkillLevels` MutationObserver before it is created. The already-safe v0.26 normalizer remains responsible for `습득 LV N` text.

Orientation:
- game remains landscape-only,
- portrait uses a simple maximum-z-index blocking gate,
- v0.30 does not rewrite viewport meta width,
- does not force numeric screen widths,
- does not resize lobby/canvas from physical screen metrics.

No combat, combo, balance, radar values, projectile travel timing, or networking semantics changed.

---

# Network truth boundary
Actual multiplayer is **not yet implemented**.
Do not claim remote connectivity until two independent clients join one authoritative room and share synchronized game state.

TEAM slot rule:
- SOLO AI: 0–3
- TEAM AI FILL: 0–2, preserving at least one human slot.

FRIEND / LINK / RANDOM currently provide local waiting UX only.

---

# Immediate next boundary
1. Device-test v0.30 on the same Samsung Browser / Android landscape device.
2. Confirm direct landscape load fills the full content width and remains responsive.
3. Verify skill title/level one-line behavior, radar proportions, arrows, and horizontal swipe.
4. Rotate portrait → confirm only orientation gate.
5. Rotate back → confirm full-width lobby returns without viewport manipulation.
6. Verify result rows and TEAM waiting screens.
7. If any visual defect remains, fix from the clean v0.30 chain only.
8. After UI/runtime stability is confirmed, move to actual multiplayer architecture.
9. Later continue Lv26/Lv31 and full-run pressure/balance simulation.

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
