# Timing Defense — P6-B2 FRESH_FORWARD_P6 Authority & Fidelity Contract V0.1

Date: 2026-10-24 KST  
Status: **USER-APPROVED METHODOLOGY / INPUT AUTHORITY LOCK / EXECUTION AUTHORIZED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

User approval:
- explicit continuation approval received at `2026-10-23T22:54:24Z` (`2026-10-24 07:54:24 KST`)

Canonical base at contract creation:
- branch: `timing-defense-workspace`
- HEAD: `9b66888fcaf0348487903faeaf272a91caef3c35`

Depends on:
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
- `103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `119_P5_CLEAR_KILL_INCOME_MIX_SENSITIVITY_V0_1.md`
- `121_P4D2_TANK_IRON_WALL_SIEGER_FIDELITY_CORRECTION_V0_1.md`
- `123_P5_ALL_CLASS_SHOP_COMBAT_METHOD_FIDELITY_REVIEW_V0_1.md`
- `124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- `152_P6_SHOP_ATK_EXP_OPPORTUNITY_BIDIRECTIONAL_FEEDBACK_RESULT_V0_1.md`
- `153_P6_B2_P4B_RECONSTRUCTION_FIDELITY_BOUNDARY_RESULT_V0_1.md`

Machine/data inputs:
- `data/p4a_marker_opportunity_corpus_v0_1.json`
- `data/model_a_representative_recipes_v0_1.yaml`
- `data/skilled_v2_central_sequence_candidate_v0_1.yaml`
- `data/p5_shop_economy_spend_capacity_fixture_v0_1.json`
- `tools/run_p5_shop_economy_spend_capacity_probe_v0_1.py`
- `tools/simulate_class_aware_layer_a.py` — physical/monster/geometry skeleton only; its old Lv6/N3 skill layer is not current skill authority

---

# 0. Why this contract exists

P6-B2 Method A attempted to recover the lost historical P4-B dedicated runner before injecting P5 shop history. The best recovered global approximation missed the predeclared exact-equivalence gate because its maximum stage error was `4`, above the allowed `3`.

Therefore:

```text
OLD_P4B_DEDICATED_RUNNER = NOT_RECOVERED
REVERSE_FIT_TO_ARCHIVED_P4B_TARGETS = FORBIDDEN
FAILED_P4B_APPROXIMATION_SHOP_INJECTION = FORBIDDEN
```

The user approved moving forward with a fresh model built only from currently surviving authority and diagnostic inputs.

This contract is written before fresh-forward result interpretation so the model cannot be tuned after seeing the answer merely to reproduce archived P4-B outputs.

---

# 1. Primary question

The first FRESH_FORWARD_P6 lane asks:

> Conditional on a Stage being entered, how do current class skill semantics plus a stagewise diagnostic shop trajectory change the number of root timing actions actually required, and therefore change provisional EXP opportunity and skill-reach timing?

Primary causal chain:

```text
Stage encounter opportunity
-> deterministic SKILLED_V2_CENTRAL root judgments
-> current unlocked skill package
-> diagnostic shop modifiers
-> actual removal/control sequence
-> actual root timing-action count
-> provisional EXP awards
-> later skill unlock state
-> later Stage action opportunity
```

This is an endogenous progression loop. Action count is not a fixed exogenous Stage constant once skill/shop power changes.

---

# 2. Scope split — mandatory

## 2.1 Lane A: CONDITIONAL_ON_STAGE_ACCESS_OPPORTUNITY

This is the primary fresh-forward lane.

It may measure:
- root timing actions;
- judgment consumption;
- Heavy frequency and Heavy result tier;
- provisional EXP awards;
- level / milestone reach;
- shop rank at each Stage;
- shop-induced action compression on the same entered Stage path;
- class-specific skill-induced action compression;
- encounter-family sensitivity where source geometry exists.

It must not claim that the player would necessarily survive to that Stage in a real campaign.

## 2.2 Lane B: SURVIVAL_EXTENSION

This effect is real and already independently established by P6-B1:

```text
shop power can prevent an earlier failure
-> later Stage becomes reachable
-> total later root actions / EXP can increase
```

The first FRESH_FORWARD_P6 runner must NOT fabricate a new full-campaign survival model merely to merge this effect into Lane A.

Until a survival-capable current-authority kernel is separately admitted:

```text
SURVIVAL_EXTENSION = INDEPENDENT_CAUSAL_EVIDENCE
NOT = IMPLIED_BY_CONDITIONAL_STAGE_ACCESS_LANE
```

---

# 3. Input authority ladder

## 3.1 Stage opportunity / encounter input

Primary synthetic workload backbone:
- `p4a_marker_opportunity_corpus_v0_1.json`
- status remains `SYNTHETIC_CALIBRATION_FIXTURE_NOT_PRODUCTION_AUTHORING`

Concrete recipe/geometry expansion:
- `model_a_representative_recipes_v0_1.yaml`
- status remains `DESIGNED_NOT_AUTHORITATIVE`

These are bounded diagnostic inputs. They do not freeze Tier1 Stage1–50 production content.

## 3.2 Physical / monster runtime skeleton

`simulate_class_aware_layer_a.py` may be reused/refactored only for currently compatible mechanics such as:
- physical spawn and movement;
- per-monster HP/armor/wall anchors supplied by its companion data;
- strict-line / area target geometry primitives;
- FLYER motion;
- CHARGER phase behavior;
- SPLITTER child spawning;
- SUPPORTER aura;
- SIEGER standoff/shot state.

Its built-in player-power implementation is specifically NOT promoted as current authority because it implements an older Lv6 + N3 layer.

## 3.3 Run state

Use current approved run-state semantics:
- level/EXP/shop ranks persist within attempt;
- combo persists across Stage/shop/target-wait downtime unless broken by judgment;
- charge persists across Stage/shop/intermission;
- Heavy X→Y resolves completely before Stage settlement;
- new attempt resets run-local state.

For Lane A, Stage access itself is externally conditioned. Do not convert forced access into a survival claim.

## 3.4 Judgment process

Use `SKILLED_V2_CENTRAL` as a deterministic diagnostic candidate:
- target long-run prior P/G/N = `.70/.20/.10`;
- Heavy consumes two judgments;
- P×P maps to CRITICAL / Lv31 final eligibility under the active mastery semantics.

Its status remains provisional and not production-frozen.

## 3.5 EXP

Use the current provisional one-valid-timing-turn credit family from P4:

```text
NORMAL    1.000
GOOD      1.500
PERFECT   2.250
HEAVY     1.250
HEAVY+    1.750
GREAT     2.250
SUPER     2.875
CRITICAL  3.500
```

Invariants:
- ordinary completed root timing turn = one EXP award;
- Heavy X+Y consumes two judgments but gives exactly one EXP award;
- generated skill hits give zero independent EXP;
- N3 gives zero independent EXP;
- no kill EXP;
- no raw-damage EXP;
- no hidden class catch-up multiplier.

All credit values remain provisional. FRESH_FORWARD_P6 does not freeze them.

## 3.6 Skill authority

Priority order:
1. latest user-approved structural/amendment contract;
2. exact earlier parity formula where still compatible and not superseded;
3. explicitly labeled diagnostic coefficient where structure exists but final number is open;
4. unresolved behavior remains open and must not be invented as production truth.

Specific rules:
- Lv6 current/frozen semantics remain usable;
- Lv11–21 recovered legacy formulas may be used as parity references where not superseded;
- Lv26 structure follows document 88; its coefficients remain provisional;
- Lv31 structure follows documents 91 and later amendments/corrections;
- Archer Lv31 = wide straight corridor, unlimited depth inside corridor, armor-ignore continuity; exact width/damage remain provisional;
- Tank active stronger Lv31 barrier must not be downgraded by a later Lv16 guard;
- Tank Iron Wall applies to SIEGER wall-shot paths if wall survival is ever modeled.

Generated child effects remain root-owned and do not recursively generate EXP/charge/combo unless an explicit contract says otherwise.

## 3.7 Shop trajectory

Structural shop semantics come from the user-approved P5-A2 contract.

For the first fresh-forward diagnostic:
- economy mix center: `CLEAR_KILL_70_30` working center;
- spend capacity: `CENTER50`;
- policy: `BALANCED`;
- resulting stagewise ranks come from the existing economy-only P5 runner;
- all of this remains diagnostic, not final economy authority.

Primary cross-class shop-effect lane:
- `ATK +8% per rank` may be used only as the existing diagnostic sensitivity anchor because ATK has valid cross-class kernel coverage.

Do not silently generalize:
- CRIT / CRITDMG require explicit effect-policy handling;
- KNOCK has an active cross-class kernel coverage gap;
- FORT/DEF are survival-path effects and are not to be folded into Lane-A action compression as fake generic offense.

---

# 4. Modifier/attribution requirements

Follow the approved modifier pipeline:

```text
authoritative action + target
-> timing/Heavy/P×P state
-> class + unlocked skill hit plan
-> persistent/run scalar stats
-> parent raw power
-> explicit action transforms
-> crit policy if applicable
-> hit coefficients + geometry
-> per-target mitigation/state
-> realized damage/control
-> death/spawn/secondary consequences
-> isolated post-action procs
```

No generic `powerScalar` may replace class effect rules such as:
- penetration count/decay;
- armor ignore;
- splash/chain;
- tracking projectiles;
- slow/control zones;
- wall shields;
- strict-line targeting;
- Lv31 final packages.

The fresh runner must preserve deterministic attribution sufficient to explain which root action and which modifier/skill caused a material hit/control event.

---

# 5. Predeclared validation — no target fitting

## 5.1 Static/source fidelity

Required before interpretation:
- input files parse and validate;
- each Stage maps to declared P4-A opportunity data;
- recipe expansion uses only declared recipe IDs;
- same seed/input produces exact-byte-identical output;
- Heavy consumes two judgments but one EXP award;
- generated skill/N3 hits produce zero EXP;
- shop ranks are stagewise/persistent, not retroactively applied from a Stage49 snapshot.

## 5.2 Independent P3 early-Lv6 directional check

Without fitting coefficients to this check, the fresh implementation should preserve the known early direction:

```text
Knight = approximately neutral root-action change
Tank   = approximately neutral root-action change
Rogue  = reduced root-action count
Archer = reduced root-action count
Mage   = reduced root-action count
```

This is directional validation, not a numerical calibration target.

## 5.3 Archived P4-B comparison

The archived Lv6/Lv11/Lv16/Lv21 response envelope may be printed after execution as independent historical comparison.

It must NOT be used to:
- fit per-recipe multipliers;
- fit stage-boundary tables;
- alter coefficients until old milestone stages match;
- relax a gate after results.

Mismatch is evidence about model difference, not permission to reverse-fit lost history.

## 5.4 P6-B1 shop-direction check

For paired identical entered-Stage packets and identical judgment streams:
- ATK_ON should not create extra root work solely through nominal attack power;
- ordinary expectation is equal-or-fewer root actions for the matched same-stage packet;
- any exception caused by discrete skill/target chronology must be reported, not hidden.

This check does not imply campaign survival monotonicity.

---

# 6. First execution boundary

First bounded execution should prioritize the minimum informative matrix:

```text
P4-A CENTRAL fixtures first
5 classes
paired deterministic seeds
SHOP_OFF vs diagnostic stagewise ATK_ON
current progression state through the pre-Lv31 spine
actual root action count -> provisional EXP -> milestone reach
```

Lv31/Stage46+ may be cross-checked against the already more mature P5/P6 late-run runner rather than forcing the P4-A synthetic lane to become a replacement late-game survival authority.

Output must distinguish:
- `conditionalStageAccess` metrics;
- `survivalClaim = false`;
- `shopTrajectoryStatus = diagnostic`;
- `expCreditsStatus = provisional`;
- `skillNumericStatus = mixed/frozen-structural-provisional as applicable`.

---

# 7. Explicit non-authority

This approval does NOT authorize:
- final EXP curve/value freeze;
- final shop effect coefficient freeze;
- final shop price/income/economy freeze;
- class buff/nerf;
- Tank damage buff;
- P×P probability change;
- exact Lv26/Lv31 numeric production values;
- exact Tier count;
- monster unlock ladder;
- exact Tier1 roster;
- exact Tier1 Stage1–50 production authoring;
- production gameplay changes/deployment.

---

# 8. Stop conditions

Stop before adoption if execution requires any of the following:
- inventing a new full-campaign survival model;
- selecting a new shop/EXP/skill coefficient as final;
- changing class identity to force parity;
- changing P×P probability;
- choosing Tier count/unlock ladder;
- editing production gameplay.

At such a boundary:

> 여기부터는 결정이 필요한 부분이라 적용하지 않고 멈춘다.

---

# 9. Current classification

```text
FRESH_FORWARD_P6 = USER_APPROVED_EXECUTION_METHOD
INPUT_AUTHORITY_LOCK = RECORDED
OLD_P4B_REVERSE_FIT = FORBIDDEN
PRIMARY_LANE = CONDITIONAL_ON_STAGE_ACCESS_OPPORTUNITY
SURVIVAL_EXTENSION = SEPARATE_EXISTING_EVIDENCE
SHOP_NUMERIC_FREEZE = NO
EXP_NUMERIC_FREEZE = NO
TIER_AUTHORING = DEFERRED
PRODUCTION_CHANGE = NO
```
