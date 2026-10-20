# Timing Defense — Balance Simulation V8: Passive Basic Attack + PERFECT Combo

Date: 2026-10-20 KST  
Status: **REPORT / CALIBRATION ONLY** — passive basic attack, enemy HP compensation, and combo power rewards are not live-balance-frozen.

## 1. Frozen / agreed behavior entering v8

- PERFECT streak counter is unbounded: 1, 2, 3 … 30 … 40 … continues until a non-PERFECT judgment or MISS.
- Fourth attack has two judgments; P+P contributes +2 combo.
- GOOD / NORMAL / MISS resets the PERFECT streak.
- Combo count must be visible from **1 COMBO**, not only at milestones.
- Display should sit near the Timing Square.
- Visual intensity may cap at 30+, while the numeric counter continues upward without a cap.
- Combo height must never secretly shrink the PERFECT zone or speed up the sweep.
- Passive basic attacks must not earn EXP, charge, combo, crit, or skill procs.

## 2. Combo rarity Monte Carlo

Independent judgment model, no artificial high-combo difficulty penalty. Therefore high-streak rates below are an **upper bound**; real human tension may reduce them.

### Chance of reaching a streak at least once within ~150 judgment opportunities

| Timing profile | 5 combo | 10 combo | 20 combo | 30 combo | 40 combo |
|---|---:|---:|---:|---:|---:|
| Average P20 | 3.6% | <0.01% | ~0% | ~0% | ~0% |
| Skilled P40 | 61.0% | 0.87% | ~0% | ~0% | ~0% |
| Expert P65 | ~100% | 50.6% | 0.83% | 0.014% | ~0% |
| Master-test P80 | 100% | 98.4% | 27.8% | 3.23% | 0.30% |

This supports the intended psychology:
- 5 combo is a realistic learned-player event,
- 10 combo is already notable for Skilled,
- 20+ is mainly expert/master territory,
- 30/40 is rare enough to become a memorable pressure event.

## 3. Combo reward candidate tested

The balanced candidate keeps **power capped even though the counter is not capped**.

Persistent timing-attack bonus while the streak survives:
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap

Milestone class attack budget used for stress testing:
- 5: small class echo (~60 raw-equivalent in the reward-only model)
- 10: medium class proc (~90)
- 20: large class proc (~150)
- 30+: maximum class proc (~210), repeated again at 40 / 50 / 60 … without increasing the proc strength further

Approximate mean total damage uplift over 120 attacks (~150 judgment opportunities), including the small 5-combo proc:

| Profile | Mean combo-power uplift |
|---|---:|
| Average | ~0.01% |
| Skilled | ~0.26% |
| Expert | ~1.99% |
| Master-test P80 | ~4.74% |

Interpretation:
- reward power does not materially inflate ordinary Average/Skilled balance,
- expert players receive a meaningful but not runaway edge,
- the primary value of 20/30/40 combo remains psychological pressure, visual prestige and rare burst moments rather than permanent DPS snowballing.

## 4. Passive basic attack candidate

Three bands were explored around the agreed idea. The best first playable A/B candidate is:

- **40 raw damage every 2.0 s**
- enemy HP compensation candidate: **+10%**
- no EXP
- no charge
- no combo contribution
- no crit
- no class skill proc
- no meaningful knockback

At no-skill timing baseline, raw timing DPS is approximately:
- Average: 143.8 DPS
- Skilled: 184.5 DPS
- Expert: 227.9 DPS

40 / 2.0 s contributes 20 passive DPS, equal to roughly:
- 13.9% of Average timing DPS,
- 10.8% of Skilled,
- 8.8% of Expert.

After +10% enemy HP compensation, simple raw-DPS headroom versus the pre-passive baseline is approximately:
- Average: +3.6%
- Skilled: +0.8%
- Expert: -1.1% before combo rewards.

This is intentionally much less than full 1:1 compensation: the passive system must leave some real breathing room.

## 5. Exact-AI-bound combat check at Lv6

Fixed Lv6 team members using the current v0.17 skill-equivalent AI logic. Same-seed comparison, current S/E/X concrete pressure generator.

### Continuous active play

| Team | Profile | Current baseline | Passive40/2s + HP10% + balanced combo | Δ clear |
|---|---|---:|---:|---:|
| 3P | Average | 67.9% | 72.4% | +4.5pp |
| 3P | Skilled | 79.2% | 80.9% | +1.7pp |
| 4P | Average | 54.2% | 56.4% | +2.2pp |
| 4P | Skilled | 58.8% | 62.2% | +3.4pp |

The candidate is stronger, but not by enough to erase pressure or mastery separation.

## 6. “Look at the battlefield” test

To directly test the design goal, the local player was forced to stop timing input for **2 seconds every 12 seconds** (~16.7% observation downtime).

Lv6 exact-AI-bound confirmation:

| Team | Profile | No pause / current | 2s pause / current | 2s pause + passive40/2s + HP10% |
|---|---|---:|---:|---:|
| 3P | Average | 63.7% | 61.3% | **65.7%** |
| 3P | Skilled | 76.7% | 72.7% | **75.9%** |
| 4P | Average | 56.8% | 54.4% | **57.2%** |
| 4P | Skilled | 63.0% | 60.8% | **64.2%** |

This is the strongest positive v8 result.

Without a passive attack, deliberately looking away from the Timing Square costs clear probability. With 40/2s passive fire plus +10% HP compensation, most of that penalty is recovered without producing a large overall difficulty collapse.

In other words, the passive attack is doing the job it was proposed for: **buying attention bandwidth, not replacing the timing game**.

## 7. Passive-only sanity check

Under the current concrete pressure samples with **all timing attacks disabled** and only 40/2s passive fire:
- 3P individual-stage clear: 0% in the confirmation sample,
- 4P individual-stage clear: 0%,
- 2P individual-stage clear: ~12.2%.

The 2P exceptions occur mostly because the wall barely survives after enemies reach it, not because passive DPS is sufficient. Among those 2P stage clears, surviving wall HP averaged only ~357 / 2000 (median ~360).

Because the real run carries wall damage forward, this does **not** imply passive-only run completion. A full-run progression simulation is still required before freezing the final passive value.

## 8. v8 recommendation

### Safe to implement immediately
- combo counter from **1 COMBO**,
- counter positioned near Timing Square,
- visual tiers: 1–4 / 5–9 / 10–19 / 20–29 / 30+,
- 30+ visual intensity cap while number remains unbounded.

### Candidate for next playable A/B, not frozen
- passive attack = **40 / 2.0 s**,
- enemy HP = **+10%** starting compensation,
- combo persistent bonuses = **5 / 8 / 12 / 15%** at 5/10/20/30,
- class milestone proc at 5/10/20/30 and every 10 after 30, with power capped at the 30 tier.

### Do not do
- no hidden high-combo timing-window shrink,
- no sweep-speed punishment at high combo,
- no combo reset at 20/30 merely to control power,
- no passive EXP / charge / skill activation,
- no exact passive-DPS-for-HP compensation that deletes the intended breathing room.

## 9. Implementation state

A v0.18 source patch has been added for the **visible counter only**. It does not yet apply combo damage rewards or passive basic attacks.

The counter:
- appears at 1 COMBO,
- updates on each accepted PERFECT judgment,
- counts both X and Y on the heavy attack separately,
- resets on GOOD / NORMAL / MISS,
- renders near the Timing Square,
- scales visual weight at 5 / 10 / 20 / 30,
- keeps numerical count unbounded above 30.

Passive basic attack and numerical combo rewards remain pending explicit post-report implementation.
