# Timing Defense — v0.20 Implementation Report

Date: 2026-10-20 KST
Status: **PUBLIC LIVE**

## Canonical live state
- Live branch: `timing-defense-live-v011`
- Live HEAD: `d5c0e5cb90e8e5aa99c7420beb96202563f07e46`
- Public page: `https://timing-defense-v011.onrender.com/v020.html`
- Render deploy: `dep-dbbdpd49v7es73esaet0` / LIVE

Files added:
- `timing-defense-v011/v020-flow-ui.js`
- `timing-defense-v011/v020-results.js`
- `timing-defense-v011/v020.html`

Static validation:
- `node --check v020-flow-ui.js` PASS
- `node --check v020-results.js` PASS

No passive/combo/class/monster numerical balance coefficient was changed in this patch.

---

## 1. Turn-boundary visible-target gating

v0.19 prevented damage to enemies still outside the right viewport but still allowed empty timing turns and EXP generation.

v0.20 changes the combat contract:

- A **new** Timing Square turn begins only if at least one valid visible target exists.
- If no valid target is visible at a turn boundary, the square enters `targetWait` and its sweep does not run.
- Passive and AI attacks also wait instead of attacking/earning progression into empty space.
- Attack input no longer force-spawns an invisible enemy; scheduled stage spawning owns enemy creation.

### Critical continuity rule
If a Timing Square turn already started while a visible target existed, that turn is locked as valid.

Therefore, if AI/passive/team damage removes the final visible monster while the needle is already moving:
- the current X turn is not cancelled,
- on the fourth attack the X→Y sequence may finish completely,
- the player may still tap and receive the normal timing judgment/EXP for that already-valid turn,
- after the turn finishes, if no target is visible, the next turn waits.

This avoids mid-sweep stop/start behavior that could look like latency or dropped input.

Stage clear/shop transition is also deferred until such an already-started local turn finishes or naturally times out.

Waiting for a target does **not** reset PERFECT combo. Only an actual non-PERFECT timing judgment does.

---

## 2. Stage-start gate

Every stage now has a short centered intro before combat begins.

Flow:
`stage selected → STAGE N / READY → intro fades → combat/spawning begins → Timing Square waits until first visible enemy`

Current intro duration: approximately `1050 ms`.

During the intro:
- no stage movement/spawn progression,
- no AI attack,
- no passive attack,
- no Timing Square input/sweep.

Combo state is preserved across the intro.

---

## 3. Judgment-text relocation

Combat judgment text such as GOOD / PERFECT / CRITICAL / heavy-result text is no longer drawn as the large centered result text.

It is rendered smaller beside the EXP gauge / right side of the Timing Square so:
- the whole word remains visible,
- it does not compete with the Timing Square,
- it does not collide with the combo pop or main combat center.

Skill-acquisition notices remain separate.

---

## 4. Top UI cleanup

- Test-mode descriptor text is removed; title is now simply `TIMING DEFENSE`.
- Class-selection controls are moved upward to reduce battlefield obstruction.

---

## 5. Party spacing

v0.20 slot-Y candidate:
`.265 / .425 / .585 / .745`

Character scale remains `.41`.

Compared with v0.19, teammates are spread farther apart and lower slots step downward slightly so full-body silhouettes and weapons remain easier to read.

---

## 6. Result-board refinement

The v0.19 metric set remains:
- KILLS
- DMG
- COIN
- LV
- MAX COMBO

Rows remain in actual character-slot order:
1. YOU
2. CPU 1
3. CPU 2
4. CPU 3

v0.20 presentation changes:
- clearer column alignment,
- more consistent header/row spacing,
- alternating subtle row bands,
- no heavy rectangle around every metric cell,
- compact rank medallion beside each value,
- 1st/2nd/3rd/4th remain gold/silver/bronze/muted,
- first-place value receives the strongest emphasis.

The purpose remains category-by-category contribution visibility rather than forcing one global MVP.

---

## 7. Unchanged experimental combat values

Still unchanged from v0.18:
- passive: `40 raw / 2.0 s`,
- non-boss HP A/B compensation: `+10%`,
- combo persistent bonus: `+5 / +8 / +12 / +15%`,
- combo milestone budgets: `60 / 90 / 150 / 210 cap`,
- combo number unbounded,
- milestone power capped at the 30-tier strength.

These remain experimental, not production-frozen.

---

## Next validation boundary

Human/device check should focus on:
1. no new timing turn starts without a visible monster,
2. an already-moving turn continues if the last monster disappears mid-turn,
3. fourth-attack X→Y is never cancelled midway for target disappearance,
4. no empty-turn EXP farming is possible,
5. target-wait does not break combo,
6. Stage N intro fully finishes before gameplay begins,
7. judgment text does not overlap EXP/Timing Square/combo,
8. widened party spacing remains usable on short landscape screens,
9. result board is materially cleaner on the Android browser.

Implementation defects may be corrected immediately. Numerical balance changes still require report/discussion first.
