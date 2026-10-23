# Timing Defense — P4-D2 Lv31 Current-Roster Pressure Response Probe V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED DETERMINISTIC DIAGNOSTIC / P4-D2 CONTINUES / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority:
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`
- `93_P4D2_FIRST_PASS_LV31_POWER_ENVELOPE_AND_PRESSURE_TARGETS_V0_1.md`
- `../MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`
- `data/model_a_representative_recipes_v0_1.yaml`
- `../combat_exact_v016.py` — formula-fidelity reference only
- `63_HIGH_MASTERY_H0_OBSERVED_TRACE_REPORT_V0_1.md`
- `64_HIGH_MASTERY_H3_OBSERVED_TRACE_REPORT_V0_1.md`

Replay assets:
- `../../tools/run_p4d2_lv31_pressure_probe_v0_1.py`
- `data/p4d2_lv31_pressure_probe_fixture_v0_1.json`
- `data/p4d2_lv31_pressure_probe_summary_v0_1.json`

---

# 0. Admission question

Can the stronger user-approved Lv31 direction produce a class-distinct, bounded pressure reset against the **current nine-monster roster**, and does any current provisional Lv31 magnitude contradict the requirement that Lv31 be a genuine final-power escalation rather than a regression?

Answer:

**YES, with one material numeric correction required for Archer before the next stateful pass.**

Classification:

```text
Knight  = strong candidate / continue stateful pressure test
Rogue   = 16-dagger center remains strong candidate
Tank    = structure viable / stateful CHARGER-SIEGER control test required
Archer  = structure PASS / 1.00 per-target magnitude REVISE
Mage    = strong density candidate / SPLITTER chronology watch remains
Overall = P4-D2 CONTINUES / NO FREEZE
```

No class identity is reopened by this result.

---

# 1. Why a new probe was necessary

The older `PRESSURE_RECIPES_V1.md` uses only the historical five-monster vocabulary:

```text
GRUNT / RUNNER / BRUTE / SHIELD / FLYER
```

It cannot be promoted into current Stage46 evidence because the current V1 foundation also includes:

```text
CHARGER / SPLITTER / SUPPORTER / SIEGER
```

Therefore this P4-D2 pass does **not** reuse the old five-monster recipe results as current balance evidence.

Instead it uses:
- the current nine-roster provisional capability anchors;
- deterministic diagnostic pressure snapshots inspired by current T4 role motifs;
- no RNG;
- no exact Stage46 authoring claim.

This preserves the authority boundary established in P4-C2.

---

# 2. Replayability improvement over P4-C2

P4-C2 exposed a replayability caveat: its directional report was committed, but it did not expose one exact committed runner suitable for later byte-level regression authority.

P4-D2 fixes that process defect early.

One-command probe:

```bash
cd timing-defense-workspace
python tools/run_p4d2_lv31_pressure_probe_v0_1.py \
  --fixture legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json \
  --json-out /tmp/p4d2_lv31_probe.json > /dev/null
sha256sum /tmp/p4d2_lv31_probe.json
```

Expected full JSON SHA-256 for V0.1:

```text
efdb369a6053bb83fcecb057ea733f4bdcabb56a333575dddf2dd4b87913e27d
```

The committed summary contains the same digest and key metrics.

This does **not** make the numerical values production authority. It only makes this bounded diagnostic exactly reproducible.

---

# 3. Diagnostic snapshots

Three pressure states are used.

## `S46_LINE_DEPTH_12`
Purpose:
- Archer strict-line depth;
- Knight/Rogue line clearing;
- protected SUPPORTER/SIEGER exposure;
- durable aligned targets.

Initial:
- 12 live bodies;
- raw remaining HP 5510;
- one-event wall-budget proxy 1265.

## `S46_DENSITY_CLUSTER_12`
Purpose:
- Mage density collapse;
- Rogue retargeting;
- SPLITTER chronological child spawning.

Initial:
- 12 live bodies;
- raw remaining HP 5290;
- wall-budget proxy 1235.

## `S46_FORTRESS_OVERLAP_14`
Purpose:
- durable front;
- protected SUPPORTER/SIEGER;
- mixed geometry;
- accumulated late-run pressure.

Initial:
- 14 live bodies;
- raw remaining HP 6195;
- wall-budget proxy 1400.

The counts are **simultaneous pressure snapshots**, not instructions to spawn 12–14 monsters in one instant or one 4-second window. Stage46 must still preserve visual readability through staggered accumulation.

---

# 4. Package-continuity findings

## 4.1 Knight
Historical/formula-fidelity P×P root after the known Lv6/Lv16/Lv21 transforms:

```text
600 × 1.12 × 1.18 × 1.20 = 951.552
```

Lv26 ideal one-wave four-target corridor:

```text
951.552 × 4 = 3806.208 raw package
```

Lv31 center with two full-strength bounded passes:

```text
951.552 × 4 × 2 = 7612.416
```

Thus the `second wave = 1.00` center is a clean ~2× ideal corridor-package escalation before actual death/retarget/geometry effects.

Snapshot result at center:
- line depth: population reset 50.0%, HP reset 55.0%;
- density cluster: population reset 50.0%;
- fortress overlap: population reset 42.9%, HP reset 54.0%.

The second-wave `1.25` candidate often saturates against current provisional ordinary HP and does not improve the static kill count over `1.00`.

Interpretation:
- do not freeze 1.00 yet;
- do not reduce Knight because 1.25 saturates in this fixture;
- the next useful discriminator is **replenishment between wave 1 and wave 2 / CHARGER-SIEGER state interaction**, not more static HP arithmetic.

## 4.2 Rogue
Approved Lv26 P×P package, without ordinary proc-crit:

```text
root 1.00
+ four Blade Barrage follow-ups 4×0.45
+ one Lv26 Chain Throw 0.45
= 3.25 root-basis units
= 1950 raw at P×P base 600
```

Lv31 Dagger Storm candidates:

| Daggers | coefficient units | raw package | vs Lv26 P×P |
|---:|---:|---:|---:|
| 12 | 5.40 | 3240 | 1.66× |
| **16** | **7.20** | **4320** | **2.22×** |
| 20 | 9.00 | 5400 | 2.77× |

This is the more relevant comparison than the earlier Lv21-only 2.80 package comparison.

16-dagger center snapshot response:
- line depth: 50.0% population reset / 49.5% HP reset;
- density cluster: 58.3% / 49.9%;
- fortress overlap: 42.9% / 48.4%.

The count axis remains meaningfully differentiable:
- 12 is visibly weaker;
- 20 is materially more destructive;
- 16 remains a defensible center rather than an arbitrary maximum.

**No evidence from this probe supports reducing the projectile count for performance reasons.**
Performance remains a later 2P/3P/4P engineering stress watch.

## 4.3 Tank
At center probe:

```text
shockwave damage = 0.75 root basis
knockback = ×2.5 CRITICAL basis
barrier candidate = 250 / 6s
```

Snapshot response:
- line depth: 41.7% population reset / 70.2% HP reset;
- density cluster: 50.0% / 73.0%;
- fortress overlap: 42.9% / 72.4%.

For surviving bodies, ×2.5 knockback creates about `1.24–1.28s` mean **base-translation** time gain in these snapshots.

This is only a lower-level control proxy. It does not replace stateful capability semantics:
- CHARGER positive knockback during WINDUP may cancel the windup;
- SIEGER may be pushed out of siege positioning and forced to reposition;
- SUPPORTER movement composition may alter effective translation;
- the 250/6s wall barrier adds protection not represented by HP-reset metrics.

Therefore Tank is **not underpowered** based on lower raw kill count. The next required evidence is stateful control impact.

## 4.4 Archer — material correction found
This is the strongest finding of the pass.

At Lv26, a P×P Archer has:
- Lv11 root multiplier `×1.10`;
- Lv16 armor ignore + 100% penetration preservation;
- Lv26 up to 5 total targets per arrow;
- Lv21 Triple Shot coefficients `1.00 + 0.65 + 0.65 = 2.30`.

For a durable aligned target struck by all three arrows, the Lv26 package is therefore:

```text
2.30 root-basis units per target
```

And for an ideal five-target aligned line:

```text
5 × 2.30 = 11.50 root-target units
660 × 11.50 = 7590 raw
```

Proposal-93's initial Lv31 candidate of one unlimited arrow at `1.00` per target creates a contradiction:

```text
Lv31 durable-target burst / Lv26 Triple Shot durable-target burst
= 1.00 / 2.30
= 43.5%
```

At `1.00`, Lv31 needs approximately **12 aligned targets** merely to match the ideal five-target Lv26 total package.

That means the final skill can feel weaker than Lv26 in ordinary 5–8-deep lines, despite the nominal unlimited penetration.

This violates the newly approved power-fantasy direction.

### P4-D2 correction
Do **not** change Archer's structure.
Keep:
- one huge strict-line arrow;
- unlimited target count;
- armor ignore;
- no homing/bending;
- one hit per intersected live target.

Reopen magnitude only.

Next candidate scan:

| Lv31 per-target coeff | vs Lv26 durable-target burst | depth to match Lv26 ideal five-target package |
|---:|---:|---:|
| 1.00 | 43.5% | 12 |
| 1.50 | 65.2% | 8 |
| 2.00 | 87.0% | 6 |
| **2.30** | **100%** | **5** |

`2.30` is the preferred continuity center for the next probe because:

```text
2.30 = 1.00 + 0.65 + 0.65
```

It compresses the existing Triple Shot's aligned per-target package into **one huge final arrow**, then gains its Lv31 escalation from unlimited line depth.

At 2.30:
- depth5 = parity with ideal Lv26 five-target package;
- depth8 = 1.60× that package;
- depth12 = 2.40×.

This is a magnitude correction, **not** a structural reopen and **not** a frozen production coefficient.

Snapshot line-depth result reinforces the direction:
- 1.00: 66.7% population reset / 86.9% HP reset;
- 2.30: 83.3% population reset / 95.6% HP reset;
- protected SUPPORTER/SIEGER are erased in the aligned showcase as intended.

Fortress geometry demonstrates the opposite constraint: when only a limited subset is on the locked ray, raising 1.00→2.30 does not magically solve off-line threats. This preserves class geometry and prevents Archer from becoming generic screen-wide AoE.

## 4.5 Mage
Center probe:

```text
three stages × 0.75 root basis
+ one direct primary impact
+ at most one bounded final chain generation
```

Density-cluster response:
- 83.3% population reset;
- 82.7% HP reset;
- chronological SPLITTER death → child spawn → later-stage child hits occurs deterministically.

Fortress overlap:
- 64.3% population reset;
- 73.8% HP reset.

Strict line snapshot:
- only 8.3% population reset.

This is desirable class differentiation: Mage is spectacular in density but poor when the authored geometry does not put bodies inside the fixed collapse area.

A second important finding:
- on the current provisional ordinary-monster HP anchors, `0.55 / 0.75 / 1.00` often produce the **same static kill count** once three stages are allowed;
- therefore this snapshot cannot identify the final damage coefficient cleanly.

Do not infer that 0.55 is automatically sufficient.
The next discriminator must be:
- replenishment during the three stages;
- harder bodies;
- radius/geometry;
- SPLITTER child chronology;
- survival into later stages.

---

# 5. Cross-class pressure-reset shape

Using the current centers (`Knight second wave 1.0`, `Rogue16`, `Tank .75/×2.5`, `Archer2.30`, `Mage .75`):

| Snapshot | Knight pop reset | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| LINE_DEPTH_12 | 50.0% | 50.0% | 41.7% | **83.3%** | 8.3% |
| DENSITY_CLUSTER_12 | 50.0% | 58.3% | 50.0% | 33.3% | **83.3%** |
| FORTRESS_OVERLAP_14 | 42.9% | 42.9% | 42.9% | 28.6% | **64.3%** |

Tank additionally buys ~1.2–1.3s base-translation time on surviving bodies plus wall shielding, so its value is understated by kill-count-only comparison.

This is a useful result:
- classes are not converging to one generic global nuke;
- Archer dominates line depth;
- Mage dominates density;
- Rogue produces geometry-agnostic sequential cleanup;
- Knight breaks a bounded frontline corridor;
- Tank converts impossible pressure into time and wall safety.

Stage46+ should therefore use **mixed sequential pressure geometry**, not one permanent geometry that disproportionately validates only one class.

---

# 6. High-mastery P×P cadence → Stage46 temporal implication

Observed real-device high-mastery anchors:

H0:
```text
16 completed P×P / ~71.8s
≈ one P×P every 4.49s
```

H3 turnover-density:
```text
14 completed P×P / ~65.649s
≈ one P×P every 4.69s
```

Both traces were 100% PERFECT upper-tail stress evidence, not ordinary-skilled population fits.

Nevertheless they give an important Stage46 stress bound:

> If even a 100%-P×P high-mastery player receives a complete reset and the battlefield takes much longer than one Heavy/P×P cycle to become dangerous again, Stage46 will be too easy for the intended `continuous mastery` fantasy.

Therefore the next temporal probe should start around a **non-frozen 4–5s dangerous-pressure reaccumulation envelope** after a successful final-skill reset.

Interpretation:
- Stage46: high mastery can repeatedly reset just in time;
- one missed P×P should create serious backlog;
- Stage47: one miss may still be recoverable with a strong next reset;
- Stage48–49: repeated misses should usually create burial cascade;
- Stage50: final skill remains necessary but full-kit reading/management decides the clear.

This does **not** freeze spawn cadence or a 4–5s timer. It is a bounded next-probe envelope derived from actual upper-tail P×P cadence.

---

# 7. What NOT to do after this result

Do not:
- nerf Rogue 16 daggers because 64–80 future multiplayer projectiles sound large;
- freeze Archer 2.30 as production damage immediately;
- raise every monster's HP uniformly to absorb Lv31;
- reduce Mage because the cluster snapshot is spectacular;
- judge Tank from kill count alone;
- turn Stage46 into a code-level Lv31 gate;
- reuse old five-monster pressure recipes as current nine-roster balance evidence;
- freeze final EXP from this pass.

The approved design philosophy remains:

```text
strong, finite, attributable Lv31 power
<->
late-run pressure that actually requires that power
```

---

# 8. Next exact P4-D2 boundary

The static/current-roster package-response layer is now sufficiently defined to move to a **stateful temporal pressure probe**.

Next probe must test:
1. 4–5s pressure reaccumulation candidate envelope;
2. successful P×P reset vs one missed vs two consecutive missed P×P opportunities;
3. CHARGER WINDUP cancellation / re-arm under Knight/Tank knockback;
4. SIEGER standoff / first-shot / reposition opportunity;
5. SPLITTER parent → child chronology during Mage collapse;
6. SUPPORTER acceleration composition;
7. Archer `2.30` as a non-frozen continuity center;
8. Rogue 12/16/20 count bracket with 16 center;
9. backlog slope with Lv26-only vs Lv31 center package;
10. no exact Stage46 authoring or production patch.

P4-D2 remains **ACTIVE**.
P4-E remains blocked.
Production remains unchanged.
