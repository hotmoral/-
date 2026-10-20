# Timing Defense — Next Work Boundary

## Current boundary after public v0.20 turn-gating / layout polish

Do **not** production-freeze passive-attack, combo-reward, or enemy-HP values from first impressions.

Required governance:
`implement A/B → observe/simulate → classify intended breathing-room vs role effect vs defect → report → discuss → explicit decision → production freeze`

## Current public state
- Public LIVE version: **v0.20**
- URL: `https://timing-defense-v011.onrender.com/v020.html`
- Live source HEAD: `d5c0e5cb90e8e5aa99c7420beb96202563f07e46`
- Render deploy: `dep-dbbdpd49v7es73esaet0` / LIVE

## v0.20 rules to validate

### 1. Turn-boundary target gating
- New Timing Square turn starts only if a valid on-screen monster exists.
- If none exists, square enters target-wait and does not sweep.
- AI/passive attacks also wait.
- Empty timing turns cannot generate EXP.
- Attack input no longer force-spawns invisible enemies.

Critical continuity rule:
- a turn that already started with a visible target remains valid even if that target disappears during the moving needle,
- current normal X can finish,
- fourth-attack X→Y can finish completely,
- already-valid turn may still award its normal judgment/EXP,
- only the next turn waits if no target is visible.

Target-wait itself does **not** reset PERFECT combo.

Test specifically by allowing AI/passive damage to kill the final visible monster while the local needle is already moving. The square must not snap-stop or cancel the current X/Y sequence.

### 2. Stage intro gate
Flow:
`STAGE N / READY → fade out → combat begins`.

Current intro ≈ 1050 ms.
During intro there should be no spawn/movement, AI/passive attack, sweep, or timing input.

### 3. Judgment text
GOOD / PERFECT / CRITICAL / heavy-result text is moved to the right side of the square beside the EXP gauge and reduced in size.

Check:
- complete word visible,
- no overlap with EXP/LV,
- no overlap with combo pop,
- still readable peripherally.

### 4. Party layout
Current slot Y:
`.265 / .425 / .585 / .745`

Scale remains `.41`.
Check full-body/weapon readability, especially on shorter landscape screens.

### 5. Top UI
- title should read only `TIMING DEFENSE`,
- class selector is moved upward,
- selector must not collide with stats or stage-intro text.

### 6. End-run contribution board
Rows:
YOU / CPU1 / CPU2 / CPU3.

Columns:
KILLS / DMG / COIN / LV / MAX COMBO.

v0.20 removes heavy per-cell boxes and uses cleaner alignment + small rank medallions.
Check:
- rank at a glance,
- values do not overlap badges,
- headers align with columns,
- 1st place is clearly strongest without overwhelming the table.

---

# Experimental combat values retained unchanged

Passive:
- 40 raw / 2.0 s,
- no EXP / charge / crit / skill / combo,
- non-boss HP +10%.

Combo persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone follow-ups:
- 5 / 10 / 20 / 30 / every +10 thereafter,
- budgets 60 / 90 / 150 / 210 cap.

Do not retune these solely from UX observations.

---

# Immediate execution after device feedback

1. Fix v0.20 implementation/visual defects only.
2. If turn-boundary gating is correct, run the full-run progression model with:
   - wall HP carried stage-to-stage,
   - local EXP/level growth,
   - AI EXP/level growth,
   - shop progression where valid,
   - passive-only / Average / Skilled / Expert,
   - solo / 2P / 3P / 4P where the model is valid.
3. Re-run pressure recipes only after the full-run model is stable.
4. Report before production-freezing passive/combo/HP coefficients.

Primary acceptance intent:
- passive-only must not sustain normal run completion,
- Average gains genuine observation bandwidth,
- Skilled remains clearly superior,
- Expert/high-combo reward remains exciting but non-mandatory,
- class role separation survives,
- target-wait removes empty EXP without creating apparent input lag.

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

## Still not production-frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- exact combo persistent coefficients,
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
