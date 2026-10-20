# Timing Defense — Next Work Boundary

## Current boundary after public v0.19 UX/integrity patch

Do **not** production-freeze passive-attack, combo-reward, or enemy-HP values from first impressions.

Required governance:
`implement A/B → observe/simulate → classify intended breathing-room vs role effect vs defect → report → discuss → explicit decision → production freeze`

## Current public state
- Public LIVE version: **v0.19**
- URL: `https://timing-defense-v011.onrender.com/v019.html`
- Live source HEAD: `0e51e172dc1ea11a78e67eb62c557d9ac4c373bc`
- Render deploy: `dep-dbbd6duq1p3s73c659cg` / LIVE

## v0.18 combat A/B retained
### Passive basic attack
- 40 raw damage / 2.0 s.
- no EXP / charge / crit / skill proc / combo contribution.
- knockback suppressed.
- non-boss spawned monsters +10% HP.

### PERFECT combo power
Persistent timing damage candidate:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone class follow-ups:
- 5 / 10 / 20 / 30 / every +10 thereafter.
- budgets 60 / 90 / 150 / 210 cap.

These values are unchanged in v0.19.

---

# v0.19 changes to validate

## 1. Visible-target integrity
Check:
- no monster is damaged before its aim point enters the viewport,
- local/AI/passive attacks do not earn kill coin from unseen enemies,
- Archer pierce and Mage/Tank/other splash do not leak damage beyond the right edge,
- empty forward attacks when no visible target do not feel confusing.

If empty attacks still feel wrong, discuss whether timing attacks should hold/fire visually without resolving damage; do not silently change attack rhythm.

## 2. Wider four-character spacing
Current candidate slot Y:
`.255 / .405 / .555 / .705`

Check:
- full body and weapons are clearer,
- bottom character is not uncomfortably low,
- Timing Square remains readable after local slot moved slightly upward,
- temporary prototype controls may overlap but should not dictate production layout.

## 3. Transient combo pop
Current v0.19 presentation:
- visible on every PERFECT from `1 COMBO!`,
- near Timing Square,
- no persistent rectangular box,
- slight tilt + pop/scale + fade,
- approx 460 ms lifetime,
- stronger at 5 / 10 / 20 / 30+,
- 30+ visual intensity caps while number remains unbounded.

Check:
- does not cover charge pips,
- does not obscure PERFECT area/sweep line,
- readable during rapid consecutive PERFECTs,
- 10/20/30 escalation is noticeable but not distracting.

## 4. End-run team contribution board
Rows follow character order:
1. YOU
2. CPU 1
3. CPU 2
4. CPU 3

Current fields:
- KILLS
- DMG
- COIN (kill-reward contribution)
- LV
- MAX COMBO

Every category has explicit rank styling:
1st gold / 2nd silver / 3rd bronze / 4th muted.

Check:
- all five columns readable on landscape Android,
- 1st-place cells are obvious at a glance,
- row order maps intuitively to characters,
- COIN label is understandable as kill-coin contribution rather than current wallet after shop spending,
- whether PERFECT count or another role-specific metric should replace/add to an existing column later.

---

# Immediate execution after device feedback

1. Fix v0.19 implementation/visual defects only.
2. Do not retune 40/2.0s, +10% HP, 5/8/12/15%, or 60/90/150/210 solely from UX observations.
3. Run the full-run progression model with:
   - wall HP carried stage-to-stage,
   - local EXP/level growth,
   - AI EXP/level growth,
   - shop progression where valid,
   - passive-only / Average / Skilled / Expert,
   - solo / 2P / 3P / 4P where the model is valid.
4. Report before production-freezing passive/combo coefficients.

Primary acceptance intent:
- passive-only must not sustain normal run completion,
- Average gains genuine observation bandwidth,
- Skilled remains clearly superior,
- Expert/high-combo rewards remain exciting but non-mandatory,
- class role separation survives.

---

# Accepted encounter state remains unchanged

Pressure grammar:
- S = Swarm
- E = Elite/Heavy
- X = Special/Mixed

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14
- cluster = 7 / 10 / 13
- scatter = 9 / 12 / 16

Current P95 4-second spawn-density reference:
- 2P ≈ 11
- 3P ≈ 15
- 4P ≈ 18

Do not retune these merely because v0.18/v0.19 adds passive/combo systems.

## Still not production-frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- exact combo persistent bonus coefficients,
- exact milestone proc coefficients/final visuals,
- final result-board fields/presentation,
- final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final tier number/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- human multiplayer cadence/network behavior,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients.
