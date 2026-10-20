# Timing Defense — Next Work Boundary

## Current boundary after public v0.18 auto/combo A/B

Do **not** production-freeze passive-attack, combo-reward, or enemy-HP values from first impressions.

Required governance:
`implement A/B → observe/simulate → classify intended breathing-room vs role effect vs defect → report → discuss → explicit decision → production freeze`

## Current public state
- Public LIVE version: **v0.18**
- URL: `https://timing-defense-v011.onrender.com/v018.html`
- Live source HEAD: `bacc0b86e356e003bdf697187ff6ea313130fc73`
- Render deploy: `dep-dbbcntjbc2fs73anb9rg` / LIVE

## v0.18 experimental systems
### Passive basic attack
- 40 raw damage / 2.0 s.
- no EXP / charge / crit / skill proc / combo contribution.
- knockback suppressed.
- non-boss spawned monsters +10% HP.

### PERFECT combo
- visible from 1 COMBO near Timing Square.
- only PERFECT increments.
- GOOD/NORMAL/MISS reset.
- heavy X/Y count separately.
- unbounded counter.
- visual tiers at 5 / 10 / 20 / 30+.
- no high-combo timing-window shrink or sweep-speed punishment.

Persistent timing damage candidate currently playable:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestone class follow-ups:
- 5 / 10 / 20 / 30 / every +10 thereafter.
- first playable raw-equivalent budgets = 60 / 90 / 150 / 210 cap.

See `V018_IMPLEMENTATION_REPORT.md` and `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`.

---

# Immediate next execution slice

## 1. Device/readability check v0.18
Check:
- `1 COMBO` appears immediately on first PERFECT,
- combo sits near Timing Square without covering charge pips, EXP gauge, or skill strip,
- heavy X PERFECT and Y PERFECT each add exactly +1,
- GOOD/NORMAL/MISS reset immediately,
- 5/10/20/30 visual escalation is noticeable but not obstructive,
- 30+ number remains readable while visual intensity plateaus.

## 2. Passive attack behavior check
Check:
- cadence feels roughly 2.0 s,
- passive projectile is visibly secondary to timing attacks,
- no EXP appears from passive hits,
- no charge is generated,
- no combo changes,
- no skill proc/crit occurs,
- no meaningful knockback occurs,
- ordinary enemies do not become sponge-like from +10% HP.

## 3. Milestone follow-up check
Verify class identity:
- Knight = blade/frontline break,
- Rogue = multi-dagger burst,
- Tank = local shockwave,
- Archer = straight-line follow-up,
- Mage = compact secondary explosion.

Check especially 5 / 10 / 20 because 30+ is intentionally rare in normal testing.

## 4. Full-run progression simulation
Before production-freezing passive/HP numbers, model:
- wall HP carried between stages,
- actual local EXP/level growth,
- AI EXP/level growth,
- shop progression where relevant,
- passive-only / Average / Skilled / Expert,
- solo / 2P / 3P / 4P where the model is valid.

Primary acceptance intent:
- passive-only must not sustain normal run completion,
- Average should gain genuine observation bandwidth,
- Skilled remains clearly superior to Average,
- Expert/high-combo reward remains exciting but does not become mandatory,
- class role separation survives.

## 5. Report before coefficient changes
Do not alter:
- 40 / 2.0 s,
- +10% ordinary HP,
- 5/8/12/15%,
- 60/90/150/210 milestone budgets,
solely from one surprising result. Report cause and discuss first.

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

Current P95 4-second spawn-density reference:
- 2P ≈ 11,
- 3P ≈ 15,
- 4P ≈ 18.

Do not retune these merely because v0.18 adds passive/combo systems.

## Still not production-frozen
- final passive attack damage/interval,
- final ordinary/elite/boss HP compensation,
- exact combo persistent bonus coefficients,
- exact milestone proc coefficients/final visuals,
- final E HP/armor package,
- final X hardened multipliers,
- exact stage duration,
- final tier number/names/order,
- multiplayer shop/economy ownership,
- duplicate-class policy,
- human multiplayer cadence/network behavior,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients.
