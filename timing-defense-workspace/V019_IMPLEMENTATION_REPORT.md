# Timing Defense — v0.19 UX / Targeting / Team Results Implementation Report

Date: 2026-10-20 KST
Status: **LIVE implementation / no numerical balance retune**

## Public build
- Version: `v0.19`
- URL: `https://timing-defense-v011.onrender.com/v019.html`
- Live source HEAD: `0e51e172dc1ea11a78e67eb62c557d9ac4c373bc`
- Render deploy: `dep-dbbd6duq1p3s73c659cg` / LIVE

## User playtest signal entering v0.19
The v0.18 device test reported:
- passive basic attack created real battlefield-reading breathing room,
- PERFECT combo count produced effective psychological tension,
- overall game feel improved,
- persistent boxed combo HUD felt too static,
- four-character spacing still felt too tight,
- attacks appeared to hit enemies before they were visible,
- the final clear screen was promising and should expose per-player contribution/rank data.

No v0.18 combat coefficient was changed in v0.19.

---

# 1. Visible-target integrity

Problem:
monsters spawn beyond the right edge, while legacy `nearestMonster()` could target any alive monster. Therefore local/AI/passive attacks could appear to fire at enemies not yet visible; off-screen kills could also produce normal kill rewards.

v0.19 rule:
- an enemy becomes targetable only after its aim point enters the viewport,
- `nearestMonster()` ignores not-yet-visible enemies,
- `visualImpact()` rejects damage to off-screen/not-yet-visible enemies,
- this also prevents pierce/AoE spill from killing unseen enemies beyond the right edge,
- timing inputs may still launch an empty forward attack if no target is visible, but that attack does not damage or award kill coin to an unseen enemy.

This is treated as a gameplay-integrity/UX correction, not a balance patch.

---

# 2. Wider four-character presentation

v0.17 spacing:
`.285 / .405 / .525 / .645`

v0.19 candidate spacing:
`.255 / .405 / .555 / .705`

Character scale remains `.41`.

Intent:
- expose full-body silhouettes and weapons more clearly,
- reduce visual stacking of four characters,
- accept that prototype bottom mode controls are temporary and should not dictate production spacing.

---

# 3. Combo presentation changed from persistent HUD to transient impact-style pop

v0.19 keeps the exact combo semantics and v0.18 mechanical rewards, but replaces the visual behavior.

New presentation:
- no persistent rectangular combo box,
- every accepted PERFECT shows the current value near the Timing Square,
- the text appears briefly, slightly tilted, scales/pops in, then fades out,
- presentation duration is about 460 ms,
- no combo text remains permanently between hits,
- visual strength still escalates at 5 / 10 / 20 / 30+,
- 30+ visual strength may plateau while the numeric streak remains unbounded.

Examples:
`1 COMBO!`, `7 COMBO!`, `20 COMBO!`, `37 COMBO!`.

Existing v0.18 milestone reward floats are suppressed in v0.19 to avoid duplicate combo text around the square.

Mechanical combo values remain unchanged:
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap
- milestone follow-ups at 5 / 10 / 20 / 30 / every +10 after 30
- budgets 60 / 90 / 150 / 210 cap

---

# 4. End-run team contribution board

On Stage 10 clear or game over, v0.19 draws a team result table in slot order:
1. YOU
2. CPU 1
3. CPU 2
4. CPU 3

Displayed metrics:
- `KILLS`
- `DMG`
- `COIN` (kill-reward coin contribution for comparison)
- `LV`
- `MAX COMBO`

Every metric receives an explicit rank.
Visual rank language:
- 1st = gold highlight / strongest outline,
- 2nd = silver,
- 3rd = bronze,
- 4th = muted blue-gray.

Level ties use EXP progress as a secondary ranking value; other categories use stable secondary measures so every present player receives an explicit 1..N rank.

Contribution instrumentation tracks:
- damage dealt by slot,
- kill attribution by slot,
- kill-coin value by slot,
- AI PERFECT count / streak / max streak from its internal timing rolls,
- local max combo from the actual PERFECT combo state.

The board is intended both as player-facing social feedback and as a QA/balance observability tool.

---

# 5. Files

Live branch additions:
- `timing-defense-v011/v019-combo-pop.js`
- `timing-defense-v011/v019-ux-results.js`
- `timing-defense-v011/v019.html`

v0.19 intentionally reuses `v018-auto-combo.js`; no passive/combo numerical coefficients were altered.

---

# 6. Validation

Before push:
- `node --check v019-combo-pop.js` = PASS
- `node --check v019-ux-results.js` = PASS

Deployment:
- Render deploy `dep-dbbd6duq1p3s73c659cg` = LIVE

Important visual caveat:
Render LIVE verifies publication/build, not mobile visual quality. Device/browser QA is still required for spacing, combo pop placement, and result-table density.

---

# 7. Next boundary

Device-check v0.19 for:
1. attacks no longer damaging/rewarding unseen enemies,
2. four-character spacing/full-body readability,
3. combo pop timing, size, tilt and overlap with charge/EXP/skill UI,
4. result-board legibility on the user's landscape Android browser,
5. rank highlighting and whether KILLS/DMG/COIN/LV/MAX COMBO are the right first five summary fields.

Fix implementation/visual defects first. Do not retune passive/combo/monster HP coefficients from this UX patch alone.
