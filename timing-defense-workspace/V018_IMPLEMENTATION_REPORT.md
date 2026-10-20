# Timing Defense — v0.18 Auto / PERFECT Combo Experimental Implementation

Updated: 2026-10-20 KST
Status: **PLAYABLE A/B EXPERIMENT LIVE — numerical values remain provisional**

## Public build
- URL: `https://timing-defense-v011.onrender.com/v018.html`
- Live source HEAD: `bacc0b86e356e003bdf697187ff6ea313130fc73`
- Render deploy: `dep-dbbcntjbc2fs73anb9rg` / LIVE

## Files
- `timing-defense-v011/v018-combo-ui.js`
- `timing-defense-v011/v018-auto-combo.js`
- `timing-defense-v011/v018.html`

## Combo implementation
- Counter appears from **1 COMBO** near the Timing Square.
- Only PERFECT increments it.
- GOOD / NORMAL / MISS reset it to zero.
- Heavy X and Y are counted separately.
- Counter is unbounded.
- Visual tiers: 1–4 / 5–9 / 10–19 / 20–29 / 30+.
- Visual intensity caps at 30+, numeric count does not.
- No hidden PERFECT-window shrink or sweep acceleration at high combo.

### Persistent timing-attack bonus — experimental
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap

The attack that reaches the threshold receives the new tier when that final judgment is PERFECT. A GOOD/NORMAL breaker receives no combo bonus.

### Milestone follow-up — experimental
Triggered at:
- 5,
- 10,
- 20,
- 30,
- every +10 after 30.

Raw-equivalent budget used by the first playable experiment:
- 5: 60
- 10: 90
- 20: 150
- 30+: 210 cap

Class expression:
- Knight: blade follow-up with secondary frontline break opportunity.
- Rogue: multi-dagger burst.
- Tank: local shockwave-style multi-target follow-up.
- Archer: straight-line follow-up with one additional line target opportunity.
- Mage: compact secondary explosion.

The milestone does **not** consume or reset the combo.

## Passive basic attack — experimental
- Local player passive attack: 40 raw damage every 2.0 s while combat has a target.
- No timing judgment.
- No EXP.
- No charge.
- No crit/proc crit.
- No skill trigger.
- No combo contribution.
- Knockback is suppressed.
- Uses class weapon/projectile presentation, but remains mechanically weaker than active timing attacks.

## Enemy compensation — experimental
- Non-boss spawned monsters receive +10% HP.
- Bosses are not automatically given the same +10% in this A/B build.
- This is deliberately not 1:1 compensation for passive DPS; the new system is supposed to leave some genuine observation breathing room.

## Prior v8 evidence supporting this A/B
- Continuous Lv6 team checks showed only small clear-rate uplift.
- A forced 2-second observation pause every 12 seconds recovered most of the lost clear probability when passive 40/2s + HP10% was enabled.
- Passive-only stage checks were 0% at 3P/4P and only ~12% at 2P with very low surviving wall HP.
- Combo power added very little average DPS at Average/Skilled because high streaks are rare.

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

## Validation completed
- `node --check` PASS for `v018-combo-ui.js`.
- `node --check` PASS for `v018-auto-combo.js`.
- Loader dependency check PASS.
- Render deploy is LIVE at exact source HEAD.

## Not claimed
No direct rendered visual/device inspection was performed in the implementation tool lane. Render LIVE verifies publication/build, not final visual correctness.

## Immediate device checklist
1. Confirm `1 COMBO` appears near Timing Square without covering charge pips.
2. Confirm X and Y PERFECT on heavy each increment once.
3. Confirm GOOD/NORMAL/MISS resets immediately.
4. Confirm passive projectile is visibly weaker and fires roughly every 2 s.
5. Confirm passive attack gives no EXP/charge/combo.
6. Confirm ordinary monsters feel only modestly tougher, not sponge-like.
7. Confirm milestone follow-ups at 5/10/20 can be distinguished by class.
8. Confirm 30+ presentation remains readable and does not obscure Timing Square.
9. Confirm previous v0.17 AI growth, spacing and faded Timing Square remain intact.

## Balance governance
This is an A/B experiment, not a permanent balance freeze.
Do not change numbers merely from one strong/weak impression. Collect play evidence, compare to v8 expectations, report, discuss, then freeze or revise.
