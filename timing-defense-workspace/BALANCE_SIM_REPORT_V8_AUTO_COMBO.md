# Timing Defense — v8 Auto-Attack + PERFECT Combo Diagnostic

Updated: 2026-10-20 KST
Status: **DESIGN / SIMULATION ONLY for auto-attack and combo numbers; no live auto-attack/combo balance patch yet**

## Purpose
Evaluate the newly approved directions:
1. passive/basic auto-attack so the player can briefly read the battlefield without combat becoming completely idle,
2. an unbounded consecutive-PERFECT combo counter whose rising visible number increases psychological pressure,
3. avoid making auto-attack strong enough to clear content by itself,
4. keep timing play as the primary damage source.

Low-risk UX/system work is separated from balance work. v0.17 implements AI internal growth, persistent/faded Timing Square, and slightly wider party spacing, but **does not yet enable auto-attack or combo rewards**.

---

# 1. Auto-attack baseline math

Current timing-only expected raw single-target output before class skills/upgrades:

| Profile | Expected normal hit | Expected heavy | 4-attack cycle time | Approx timing DPS |
|---|---:|---:|---:|---:|
| Average | 142.0 | 307.3 | 5.10 s | 143.8 |
| Skilled | 160.0 | 379.8 | 4.66 s | 184.5 |
| Expert | 177.8 | 466.9 | 4.39 s | 227.9 |

Candidate auto-attack `40 damage every 2.0 s` = **20 DPS**.

That is approximately:
- 13.9% of Average timing DPS,
- 10.8% of Skilled timing DPS,
- 8.8% of Expert timing DPS.

This is strong enough to make a short observation pause less punishing, but far below enough to replace active timing attacks.

## Candidate enemy-HP compensation

With auto-attack 40 / 2.0 s:

| Global HP candidate | Average effective pace | Skilled effective pace | Expert effective pace |
|---|---:|---:|---:|
| +8% | +5.5% easier | +2.6% easier | +0.7% easier |
| +10% | +3.6% easier | +0.8% easier | -1.1% harder |
| +12% | +1.7% easier | -1.0% harder | -2.9% harder |
| +15% | -0.9% harder | -3.6% harder | -5.4% harder |

Interpretation:
- +10% almost mathematically cancels the Skilled benefit and leaves too little of the intended breathing-room effect.
- +8% leaves a small but real margin at all skill levels.
- Therefore **40 damage / 2.0 s + roughly +8% global ordinary-monster HP** is the leading first playable experiment, not a frozen production value.

Do not compensate 1:1 for every auto-attack point. The system is intentionally supposed to create a small amount of real breathing room.

## Auto-attack semantic candidate
- independent basic projectile every ~2.0 s,
- initial raw damage = 40,
- no timing judgment,
- no CRIT/proc-crit,
- no charge generation,
- no PERFECT combo contribution,
- no skill trigger,
- no EXP,
- minimal or zero knockback,
- ordinary class weapon visual may be used, but presentation must remain weaker than a timing attack.

The no-EXP rule preserves the already accepted principle that timing participation drives run leveling.

---

# 2. PERFECT combo semantics — frozen direction

Combo is **unbounded**.

- Only a PERFECT timing input increments the combo.
- GOOD / NORMAL / MISS break it to zero.
- Attacks 1–3 provide one possible combo increment each.
- The fourth attack provides two independent increments: X and Y.
- Therefore one completely PERFECT 1→4 sequence adds **5 combo**.
- Reaching 5 / 10 / 20 / 30 / 40 etc. never consumes or resets the combo.
- Stage/shop downtime does not itself count as a miss; the combo should only break on an actual non-PERFECT timing judgment unless later explicitly changed.

Most important design rule:
**Do not secretly shrink timing windows, accelerate the sweep, or reduce PERFECT probability as combo rises.**
The extra difficulty should come from player tension caused by the visible streak and increasing stakes, not hidden dynamic cheating.

---

# 3. How rare are high combos?

Monte Carlo diagnostic assuming independent PERFECT probability per timing judgment.
This is not a human psychology model; real streaks may cluster and pressure may increase mistakes.

## Rough 150-judgment run segment

| Player accuracy | Reach 5 | Reach 10 | Reach 20 | Reach 30 | Reach 40 |
|---|---:|---:|---:|---:|---:|
| Average P20 | 3.7% | ~0.002% | ~0 | ~0 | ~0 |
| Skilled P40 | 60.9% | 0.8% | ~0 | ~0 | ~0 |
| Expert P65 | ~100% | 50.9% | 0.8% | 0.016% | ~0 |
| Master-like P80 | 100% | 98.5% | 27.5% | 2.9% | 0.3% |

## Rough 300-judgment long run

| Player accuracy | Reach 5 | Reach 10 | Reach 20 | Reach 30 | Reach 40 |
|---|---:|---:|---:|---:|---:|
| Average P20 | 7.1% | ~0 | ~0 | ~0 | ~0 |
| Skilled P40 | 84.7% | 1.8% | ~0 | ~0 | ~0 |
| Expert P65 | 100% | 76.6% | 1.8% | 0.03% | ~0 |
| Master-like P80 | 100% | ~100% | 49.7% | 6.6% | 0.7% |

This supports the design intuition:
- 5 combo is a reachable learned-player event,
- 10 is meaningful,
- 20 is already exceptional unless the player is extremely accurate,
- 30/40 naturally become high-tension bragging moments rather than routine rotation.

The unbounded counter therefore has value even if mechanical reward strength eventually plateaus.

---

# 4. Combo visual-pressure ladder

Candidate presentation hierarchy:

### 1–4
- small persistent combo number near the Timing Square only.

### 5–9
- combo number begins appearing at the struck monster on PERFECT hits,
- mild class-color glow.

### 10–19
- larger hit-side `10 COMBO`, `11 COMBO` etc.,
- stronger pulse / brief accent,
- persistent HUD counter becomes more prominent.

### 20–29
- stronger impact ring / typography / class-color flare,
- still no screen-obscuring full-screen effect.

### 30+
- maximum visual tier may plateau here,
- **the numeric combo itself continues indefinitely**: 31, 32, 40, 50, ...
- the player must always be able to see exactly what streak is at risk.

This uses the combo number itself as pressure. The game should not artificially sabotage the player's timing.

---

# 5. Mechanical combo reward — not frozen yet

Do not use an ever-growing permanent damage multiplier. That would create runaway balance and make the streak mandatory rather than exciting.

The safer design space is **milestone-triggered one-off class rewards** while the counter keeps climbing.

Candidate test family for the next combat simulation:
- 5 combo: small next-hit or class echo reward,
- 10 combo: meaningful class-specific follow-up,
- 20 combo: stronger class-specific follow-up,
- 30 combo and then every +10: high-tier follow-up; mechanical strength may plateau while visuals/numeric tension continue.

Possible class language:
- Knight: extra blade wave / stronger frontline break,
- Rogue: bonus dagger burst,
- Tank: shockwave / protection pulse,
- Archer: bonus straight-line shot,
- Mage: secondary explosion.

Exact coefficients remain intentionally unfrozen until combat simulation measures how often each milestone actually contributes damage.

---

# 6. Current implementation boundary

Already authorized and implemented separately in v0.17:
- AI teammates gain their own EXP and levels internally,
- AI timing outcomes are internally simulated; no extra Timing Squares are drawn,
- AI can unlock/use Lv6/11/16/21 class mechanics,
- 1–4 Timing Square continuity: after input the square remains visible at reduced opacity rather than vanishing,
- charge UI therefore remains visually anchored,
- party vertical spacing widened slightly for character silhouette readability.

Not yet live-enabled:
- passive auto-attack,
- PERFECT combo counter/rewards,
- enemy HP compensation for auto-attack.

These remain behind the report/discuss boundary until the next exact combat test confirms candidate values.

---

# 7. Leading next-test candidate

For the next simulation/playable experiment, start with:
- auto-attack: **40 raw damage every 2.0 s**,
- auto-attack has no EXP/charge/crit/skill/combo,
- ordinary monster HP baseline: **+8% candidate**, with boss/elite compensation evaluated separately instead of blindly applying the same percentage,
- combo: unlimited counter, only consecutive PERFECT,
- no dynamic timing-window penalty from combo,
- visual escalation tiers at 5 / 10 / 20 / 30+, numeric counter never capped,
- mechanical milestone rewards simulated in conservative/medium/aggressive variants before selection.

No production balance value is frozen by this document.
