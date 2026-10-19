# Timing Defense — Balance Simulation V6: Concrete Spawn Recipes / Co-op Pressure Envelope

Date: 2026-10-20 KST  
Status: **REPORT ONLY — no live gameplay values changed**

## Goal

Convert v5 S/E/X pressure grammar into concrete current-roster encounter recipes and check:

- 2/3/4-player scaling,
- short-window battlefield density,
- role-opportunity preservation,
- Average→Skilled response,
- whether a first concrete recipe set is coherent enough to continue.

Concrete recipes are documented separately in `PRESSURE_RECIPES_V1.md`.

---

## 1. Important correction before calibration

A first fixed-Lv21 “all attacks resolve immediately” combat model made almost every multi-player stage trivial.

That result was rejected as a difficulty verdict because it omitted or idealized:
- actual projectile lifetime,
- current nearest-target behavior,
- recovery timing,
- real AI cadence,
- skill implementation differences,
- future human-network timing,
- progression state.

The live prototype was re-read before continuing.

Current live facts used to improve the diagnostic boundary include:
- projectiles have class-specific lifetimes around 0.14–0.28 s,
- local recovery waits about 390 ms after hit resolution,
- live AI attack intervals differ by class,
- live AI uses lower fixed timing-result probabilities,
- monsters move continuously toward the wall,
- live spawning caps simultaneous active monsters at 10 in the current Stage 1–10 implementation.

Therefore v6 separates:
1. **structural recipe/readability calibration**, which is reliable now, from
2. **absolute final co-op clear-rate calibration**, which is still bounded by unresolved multiplayer/skill assumptions.

---

## 2. Concrete Swarm sizes

Candidate burst sizes:

| Form | 2P | 3P | 4P |
|---|---:|---:|---:|
| S-line | 8 | 11 | 14 |
| S-cluster | 7 | 10 | 13 |
| S-scatter | 9 | 12 | 16 |

The earlier more aggressive candidate reached 20+ enemies in one event and produced excessive peak density. It was reduced.

This is an important design result:
**team-size scaling should not solve 4-player difficulty by simply dumping 20–30 ordinary enemies at once.**

---

## 3. Concrete Special/Mixed recipes

Current X recipes add role-bearing units rather than only raw bodies.

Examples:

### X-line
- 2P: SHIELD1 + RUNNER3 + FLYER2
- 3P: SHIELD2 + RUNNER4 + FLYER2 + BRUTE1
- 4P: SHIELD2 + RUNNER5 + FLYER3 + BRUTE2

### X-cluster
- 2P: SHIELD1 + GRUNT3 + FLYER2
- 3P: SHIELD2 + GRUNT4 + FLYER3 + BRUTE1
- 4P: SHIELD2 + GRUNT5 + FLYER4 + BRUTE2

### X-split
- 2P: SHIELD1 + RUNNER3 + FLYER2
- 3P: SHIELD2 + RUNNER5 + FLYER3 + BRUTE1
- 4P: SHIELD2 + RUNNER6 + FLYER4 + BRUTE2

This makes player-count scaling mainly appear as:
- extra anchors,
- extra fast threats,
- extra split pressure,
- extra durable normals.

That matches the chosen philosophy better than a blanket global HP multiplier.

---

## 4. E should use an effective-durability budget, not one absurd health bar

The stress model needed strong E budgets to remain relevant against larger teams.

Median event threat index in the current stress envelope:

| Players | S event | E event | X event |
|---|---:|---:|---:|
| 2 | ~7.3–7.6 | **12.1** | ~7.9–9.3 |
| 3 | ~10.2–10.5 | **21.6** | ~22.1–24.9 |
| 4 | ~13.4–13.5 | **32.0** | ~35.8–39.1 |

This does **not** mean a 4-player Champion should literally receive 5× HP.

Production realization should distribute the budget between:
- moderate HP growth,
- armor / damage reduction,
- second or third durable target,
- BRUTE/SHIELD composition,
- timing overlap.

This avoids bullet-sponge fatigue while keeping Rogue/Tank utility relevant.

---

## 5. Readability result

Across five prototype 50-stage tiers, 250 generated stages per team size:

| Players | Mean enemies/stage | P95 enemies/stage | Mean 4-s peak | P95 4-s peak | P95 6-s peak |
|---|---:|---:|---:|---:|---:|
| 2 | 34.1 | 47.5 | 7.9 | **11** | 13.5 |
| 3 | 57.0 | 79.0 | 11.9 | **15** | 19 |
| 4 | 71.2 | 99.0 | 14.6 | **18** | 24 |

The short-window peak stayed far below the earlier overpacked candidate.

This gives a first authoring constraint:

> Keep normal production recipes near or below the current P95 short-window density; exceed it only for intentionally exceptional “chaos” stages.

---

## 6. Role-opportunity result

Concrete recipes preserve the v5 role-rotation behavior.

Campaign-wide structural opportunity:

| Recipe set | Knight | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| 2P | 20.5% | 19.0% | 20.2% | 21.1% | 19.2% |
| 3P | 20.4% | 19.0% | 20.7% | 21.2% | 18.8% |
| 4P | 20.4% | 19.1% | 20.5% | 21.2% | 18.8% |

Tier identities still rotate:
- T2: Rogue rises under durability pressure,
- T3: Archer rises under line/swarm pressure,
- T4: Tank rises under split/special pressure.

The concrete monster recipes therefore did **not** collapse the abstract role grammar.

---

## 7. Combat-envelope diagnostic

Because true human multiplayer cadence and Lv11–21 implementation do not exist yet, v6 uses two bounds rather than pretending one number is final.

### Lower-bound-ish diagnostic
One human local player + teammates approximating **current live AI cadence/result quality**, using the concrete recipes.

7,000 runs across:
- all unique 2/3/4-player class combinations,
- every possible local member within the composition,
- T1–T5,
- Average and Skilled local profiles.

Aggregate:

| Players | Average clear | Skilled clear | Avg wall HP (Average) | Avg wall HP (Skilled) |
|---|---:|---:|---:|---:|
| 2 | 100.0% | 100.0% | 1886 | 1975 |
| 3 | **88.4%** | **94.9%** | 1150 | 1522 |
| 4 | **68.3%** | **83.0%** | 769 | 1125 |

Hardest prototype identity was T4 Crossfire:

| Players | Average | Skilled |
|---|---:|---:|
| 3 | 77.7% | 90.3% |
| 4 | 48.0% | 77.5% |

This is useful because it shows the recipes can create real defensive pressure without relying on 30+ simultaneous ordinary enemies.

### Upper-bound-ish diagnostic
When every teammate is modeled as a fully capable human using the current **candidate Lv21** kit and idealized class targeting, representative multi-player slices still saturate near 100%.

That is not evidence that the recipes are too weak. It shows that **final co-op difficulty cannot be frozen before real Lv11–21 implementation and the multiplayer teammate/cadence model exist**.

The true production result should fall between these bounds.

---

## 8. Mastery signal remains visible

Even inside the conservative AI-teammate bound:
- 3P aggregate clear rises from 88.4% → 94.9%,
- 4P rises from 68.3% → 83.0%,
- T4 4P rises from 48.0% → 77.5%.

So the pressure recipes do not erase the intended Average→Skilled mastery advantage.

No difficulty compensation is recommended from this alone.

---

## 9. Decision from v6

The concrete-recipe concept is coherent enough to continue.

Supported:
1. S burst counts can be kept readable.
2. X can carry most multiplayer scaling through composition rather than raw count.
3. E can create Rogue/Tank moments without requiring every enemy to become tougher.
4. Tier-local class peaks survive concrete roster conversion.
5. 4-player pressure can be meaningful while short-window spawn density remains controlled.
6. Mastery still matters.

Not frozen:
- final E HP/armor package,
- final X hardened multipliers,
- final stage duration,
- final human multiplayer cadence,
- final 2/3/4-player difficulty targets,
- exact Lv11–21 combat formulas before implementation.

No live class, monster, stage, EXP, shop or boss value was changed.

---

## 10. Next boundary

Before further numeric co-op difficulty tuning, the highest-value implementation step is now the previously planned **Lv6–21 multi-skill playable block**, because final team-pressure calibration depends heavily on the exact real skill behavior.

That implementation candidate should include:
- Lv6 / Lv11 / Lv16 / Lv21 for all five classes,
- exact straight-line Archer collision,
- multi-skill HUD strip,
- boss dagger scalar 0.70,
- boss knockback scalar 0.40,
- already agreed Mage/Tank candidate behavior.

After implementation:
1. extract exact formulas back into the simulator,
2. run the concrete pressure recipes again,
3. compare real human-play feel only on the suspicious stages/pressure windows,
4. discuss before changing live balance numbers.
