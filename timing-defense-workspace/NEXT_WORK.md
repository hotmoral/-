# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P4-B EXP OPPORTUNITY STABILIZATION DECISION

Completed chain:

```text
P0 Foundation
 -> all-20 / SKILLED_V2_CENTRAL closure
 -> P1 Run-State Lifecycle
 -> P2 Modifier / Attribution Pipeline
 -> P3 Persistent 10-Stage Kernel PASS
 -> P4 EXP methodology USER APPROVED
 -> P4-A Marker-Only 50-Stage Inverse Design PASS
 -> P4-B Lv6→Lv21 combat-feedback diagnostic COMPLETE
 -> universal pure-per-turn window conflict identified
```

Current dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_5.yaml`

Current P4 evidence:
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4b_combat_feedback_divergence_v0_1.json`

Current decision proposal:
- `legacy-game-structure/82_P4B_EXP_STABILIZATION_DECISION_PROPOSAL_V0_1.md`

---

# P4-B finding

Activating current Lv6 and exact v0.16 Lv11/Lv16/Lv21 parity candidates changes the number of valid EXP-producing timing turns substantially by class.

Structural pattern:

```text
Rogue / Archer / Mage early offensive efficiency
 -> fewer later timing turns
 -> slower later EXP

Tank Lv6–16 defensive/control identity
 -> retains more timing turns
 -> faster later EXP
```

P3 independently supports the early direction/magnitude for Rogue and Archer.

With pure additive per-turn EXP and one universal curve, refitting the six thresholds alone does not keep the current common milestone windows jointly feasible.
The confirmed Lv31 Stage41–45 target is the critical blocker.

P4-B classification:

```text
P4B_UNIVERSAL_PURE_PER_TURN_WINDOW_CONFLICT
```

No automatic fix is authorized.

---

# EXACT NEXT DECISION

Choose progression direction before P4-C Lv26 work.

## A — Pure per-turn EXP, accept wider/class-dependent skill reach
- preserves current EXP semantics;
- would require reopening the common Lv31 Stage41–45 direction or accepting material class exceptions.

## B — Class-specific XP/threshold correction
- numerically easy;
- hidden and hard to maintain;
- not recommended.

## C — Encounter-authoring-only correction
- use HP/count/cadence/formation/pressure to manage pacing;
- should remain a local gameplay tool;
- not sufficient as the sole general correction because all classes share the same Stage.

## D — Class-neutral Stage Quality Budget + raw-turn hybrid — RECOMMENDED
Concept:

```text
StageCredit
= λ × SUM(valid turn-quality credits)
+ (1-λ) × class-neutral Stage progression budget × mean timing quality
```

Purpose:
- timing quality still drives faster growth;
- efficient classes are not punished by losing most EXP opportunities;
- a limited raw-turn component may preserve healthy self-damping;
- no hidden class/Tier XP multiplier;
- Tier encounter identities remain free to differ.

Exact `λ`, budget values, display timing and visible EXP are NOT proposed as frozen values.

---

# If D is approved

Next bounded package becomes `P4-B2 STAGE_QUALITY_BUDGET_BLEND_COMPARISON`.

First candidate comparison only:

```text
λ = 0.00 / 0.10 / 0.25 / 0.50
```

Measure:
- Lv6/11/16/21/26/31 P25/P50/P75/P90;
- class/Tier spread;
- timing-quality sensitivity;
- remaining self-damping;
- Stage-budget smoothness;
- T1–T4 encounter identity preservation;
- Mage feedback sensitivity.

Then return a second numerical recommendation before selecting any provisional blend.

---

# Do not yet

- start P4-C Lv26 simulation contract
- modify/deploy production v0.45 gameplay
- approve Stage Quality Budget without user decision
- freeze P4-A anchors
- freeze visible EXP values
- add hidden class-specific or Tier-specific XP multipliers
- nerf class skills to manufacture equal attack counts
- homogenize Tier Stage flow for EXP
- invent Lv26/Lv31 power proxies
- freeze tail percentile gates
- freeze shop/Base HP/permanent progression/boss/multiplayer values
- author exact 200 launch Stages
