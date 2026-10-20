# Timing Defense — Next Work Boundary

## Current boundary after live v0.17 + v8

Do **not** freeze auto-attack, combo-reward or enemy-HP values from first impressions.

Required governance:
`implement experiment → simulate/observe → classify intended breathing-room vs role effect vs balance defect → report → discuss → explicit decision → freeze numerical values`

## Current live state
- Public version: **v0.17**
- URL: `https://timing-defense-v011.onrender.com/v017.html`
- Live source HEAD: `8f46b2460f0d16b6103e0f10bec0b5206aa93ae6`
- Render deploy: `dep-dbbc3emq1p3s73c29csg` / LIVE

v0.17 implemented only the already-approved low-risk/system changes:
- Timing Square remains visible at reduced opacity between attacks,
- four-player vertical spacing widened slightly,
- AI teammates now gain internal EXP/levels and use Lv6/11/16/21 skills,
- AI receives no visible Timing Square.

Auto-attack and combo rewards are **not yet live-enabled**.

---

# v8 design/simulation state

See `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

## Passive auto-attack leading candidate
First experiment:
- 40 raw damage,
- every 2.0 s,
- no EXP,
- no charge,
- no crit,
- no skill proc,
- no combo contribution,
- minimal/zero knockback.

Current leading ordinary-monster HP compensation candidate: **+8%**, not frozen.

Reason:
- passive 40/2.0 contributes ~13.9% / 10.8% / 8.8% of Average / Skilled / Expert baseline timing DPS,
- +8% HP still leaves a small real net relief instead of mathematically erasing the new system.

## PERFECT combo frozen semantics
- only consecutive PERFECT judgments count,
- GOOD/NORMAL/MISS break combo,
- normal attacks = +1 opportunity,
- heavy X and Y = +1 each,
- fully PERFECT 1→4 sequence = +5,
- counter is unbounded,
- milestones never consume/reset the counter,
- stage/shop downtime does not itself break it,
- no hidden timing-window/sweep-speed penalty at high combo.

## Combo visual direction
- 1–4 small counter,
- 5+ hit-side combo number,
- stronger presentation at 10 and 20,
- 30+ may use a capped maximum visual tier,
- numeric count continues 31/32/40/50+ indefinitely.

## Combo mechanical rewards
Still unfrozen.
Next simulation should compare at least three reward-strength families:
- conservative,
- medium,
- aggressive.

Prefer one-off class-specific milestone attacks/effects over an endlessly stacking permanent damage multiplier.

---

# Immediate next execution slice

## 1. v0.17 device/readability check
Check:
- faded Timing Square is readable but clearly inactive,
- charge indicator remains useful during recovery,
- four-character spacing exposes enough of each full-body silhouette/weapon,
- AI level/skill behavior does not produce obvious formula or targeting errors.

Fix defects only.

## 2. Auto-attack + combo simulation block
Build an exact experimental simulator on top of the v0.16/v0.17 combat formulas.

Required comparison profiles:
- no timing input / passive only,
- Average,
- Skilled,
- Expert.

Required auto-attack grid around the leading candidate:
- damage 35 / 40 / 45,
- interval 1.8 / 2.0 / 2.2 s,
- ordinary HP compensation 0 / 5 / 8 / 10 / 12%.

Goals:
- passive-only must not reliably clear intended content,
- Average gets some real but limited breathing room,
- Skilled should remain comfortably better than Average,
- auto-attack must not erase class roles or timing mastery.

## 3. Combo reward simulation
Measure:
- milestone reach frequency,
- average added damage per run,
- high-roll contribution at 10/20/30+,
- whether one class benefits disproportionately from milestone mechanics.

Do **not** artificially lower simulated PERFECT probability merely because combo is high. Psychological pressure is for human testing, not a hidden game modifier.

## 4. Report before live numerical patch
Only after the above should the first playable auto/combo balance build be chosen.

---

# Accepted encounter state remains unchanged
Pressure grammar:
- S = Swarm,
- E = Elite/Heavy,
- X = Special/Mixed.

Current candidate Swarm bursts:
- line 2P/3P/4P = 8 / 11 / 14,
- cluster = 7 / 10 / 13,
- scatter = 9 / 12 / 16.

Current P95 4-second spawn density reference:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

Do not retune pressure recipes until auto-attack/combo effects are measured.

## Still not frozen
- final auto-attack damage/interval,
- final HP compensation,
- exact combo milestone rewards,
- final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final tier number/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- human multiplayer cadence/network behavior,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients.
