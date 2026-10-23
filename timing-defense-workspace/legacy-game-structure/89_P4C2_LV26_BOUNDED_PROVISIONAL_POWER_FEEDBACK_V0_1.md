# Timing Defense — P4-C2 Lv26 Bounded Provisional Power Feedback V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED DIAGNOSTIC COMPLETE / PASS WITH WATCHES / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `../combat_exact_v016.py`
- `../pressure_recipe_sim_v1.py`
- `../CLOUDFLARE_V042_CHARGER_CAPABILITY_PASS_2026-10-22.md`
- `../CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`
- `../CLOUDFLARE_V044_SUPPORTER_CAPABILITY_PASS_2026-10-22.md`
- `../CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`

Machine-readable evidence:
- `data/p4c2_lv26_bounded_feedback_v0_1.json`

---

# 0. Admission question

Does the user-approved Lv26 structural package create a bounded, interpretable power step suitable for continuing the Player Power Spine, without immediately exposing a structural contradiction with earlier skills, current monster capabilities, role-expression rules, or the active EXP feedback watches?

Answer:

**YES — PASS WITH WATCHES.**

P4-C2 does **not** prove that the current Lv26 coefficients are final balance values.
It also does not prove current 2P/3P/4P production balance or final EXP convergence.

---

# 1. Two-lane evidence design

To avoid mixing old and current authority, P4-C2 deliberately separates two questions.

## Lane A — paired formula-fidelity sensitivity
Purpose:
- measure the direction and rough magnitude of `Lv21 -> Lv26` combat / action-opportunity feedback using the existing exact-v0.16 style combat lane;
- keep Stage recipe and random scenario paired between levels;
- test whether Lv26 creates additional EXP-opportunity self-damping directionally.

Boundary:
- the historical pressure generator contains the old five-monster vocabulary;
- therefore these results are **not current nine-roster production balance**;
- old `T1..T4` labels in this lane are historical pressure labels, not current Model-A T4 SUPPORTER/SIEGER calibration.

## Lane B — current nine-roster targeted structural probes
Purpose:
- test the approved Lv26 semantics directly against current CHARGER / SPLITTER / SUPPORTER / SIEGER capability rules and role-expression constraints;
- detect structural collisions cheaply before attempting a later full current-roster integration.

No production source was changed in either lane.

---

# 2. RNG correction before accepting Lane A

The first paired reconstruction inherited the historical diagnostic's broad single-RNG style. That allowed a small combat-duration change to shift later judgment/proc/AI draws, creating avoidable causal noise.

That first result was **not admitted as final P4-C2 evidence**.

The accepted rerun uses deterministic named substreams consistent with P3 governance:

```text
STAGE
JUDGMENT
COMBAT_PROC
AI
```

Lv21 and Lv26 use the same base scenario seed and corresponding named substream seeds.
This reduces false attribution from downstream RNG-stream displacement.

---

# 3. Paired execution volume

Accepted paired sensitivity volume:

```text
2 quality-sensitivity profiles
× 2P/3P/4P historical pressure lanes
× T1..T4 historical pressure labels
× all local-class/team placements in the bounded lane
× 24 paired seeds per cell
= 13,440 Lv21/Lv26 paired comparison rows
```

Profiles:
- `legacySkilled40P` — direction cross-check against the older skilled shape;
- `central70P_sensitivity` — 70/20/10 quality sensitivity aligned with the current design-prior quality mix, but **not a claim that historical cadence is now fitted SKILLED_V2_CENTRAL authority**.

---

# 4. Central-70% PERFECT sensitivity result

| Class | Local timing actions | Damage | Stage duration | Remaining wall HP | Clear-rate delta |
|---|---:|---:|---:|---:|---:|
| Knight | **-0.71%** | **+7.66%** | -0.25% | +6.20% | +2.01 pp |
| Rogue | **-2.49%** | **+12.05%** | -0.84% | +16.50% | +5.36 pp |
| Tank | **+0.29%** | **+1.01%** | +0.30% | +1.36% | -0.30 pp |
| Archer | **-4.05%** | **+4.42%** | -2.47% | +3.28% | +0.15 pp |
| Mage | **-3.75%** | **+6.70%** | -2.21% | +8.48% | +0.97 pp |

Important interpretation:
- offensive Lv26 effects generally increase combat efficiency and reduce later local timing-action opportunities;
- this extends the already-known P4-B self-damping mechanism rather than contradicting it;
- Tank behaves differently: control slightly extends target lifetime / Stage time and produces a small **increase** in local timing opportunities;
- therefore Lv26 does not make class progression opportunity converge automatically.

The Tank clear-rate change is essentially flat in this bounded lane. The individual paired outcomes can flip in both directions because slowing targets changes target-order / hit-allocation paths even with named RNG streams. This is not evidence of a Tank nerf.

Legacy-skilled direction check also stayed consistent:
- Knight actions -0.29%, damage +8.16%
- Rogue -0.94%, +9.86%
- Tank +0.47%, +1.46%
- Archer -2.74%, +6.42%
- Mage -2.60%, +10.19%

The direction therefore does not depend on only the 70% PERFECT sensitivity lane.

---

# 5. Per-class Lv26 observations

## Knight
The 0.85 -> 1.00 penetration coefficient is a `+17.65%` increase on each affected secondary penetration hit before target mitigation, while the approved knockback ladder is `1.15 / 1.30 / 1.45` for extra targets.

Observed bounded result:
- meaningful damage improvement;
- modest action-opportunity reduction;
- no evidence that a new penetration-count rule is needed.

Main current-roster watch:
- screen lifetime;
- CHARGER WINDUP interrupt frequency;
- SIEGER reposition / first-shot opportunity.

## Rogue
At the current 70% PERFECT design-prior quality mix, the theoretical fraction of root actions containing at least one PERFECT is:

```text
(3 × 0.70 + [1 - (1 - 0.70)^2]) / 4
= 0.7525
```

The approved one-per-root bound therefore matters. It prevents a Lv21 Blade Barrage -> many Chain Throws event tree.

In the bounded historical lane, Lv26 averaged about `25.15` Chain Throw hits per Stage-like row and produced the largest damage gain among the five classes.

Watch:
- secondary-target availability;
- opportunistic backline reach;
- additional EXP-opportunity self-damping.

## Tank
The accepted current capability composition gives:

```text
SUPPORTER 1.18 × AFTERSHOCK 0.75 = 0.885
```

So an enemy simultaneously supported and slowed translates at 88.5% of its unspecialized base movement rate.

Current CHARGER provisional capability anchors:
- ADVANCE `.060` -> slowed `.045` -> supporter+slow `.0531`
- CHARGE `.210` -> slowed `.1575` -> supporter+slow `.18585`
- WINDUP remains `650ms`

The CHARGE state therefore remains a clear burst-speed state; Aftershock does not erase the CHARGER state-machine identity by converting it into an interrupt.

Current SIEGER provisional approach:
- `.045` -> slowed `.03375` -> supporter+slow `.039825`
- WINDUP `800ms` unchanged
- repeat cadence `2200ms` unchanged

Key watch:
slowing SIEGER approach/reposition gives the player more time to kill it **before** it reaches standoff, which can reduce first-shot role-expression opportunity even though the firing cadence itself is untouched.

This must be checked later in current-roster authored pressure, not patched now by changing SIEGER HP.

## Archer
Perfect Impaling Shot changes maximum additional strict-line targets per qualifying arrow from `2` to `4`.

Ideal fully aligned target-capacity comparison:

```text
primary + 2 additional = 3 slots
primary + 4 additional = 5 slots
=> +66.7% maximum line-depth capacity
```

This is geometry-sensitive, not a blanket +66.7% damage multiplier.

Bounded historical lane was already close to clear-rate saturation, so its small clear-rate change is not useful for balancing the skill.
The meaningful current-roster watch is protected backline/screen deletion, especially SUPPORTER/SIEGER formations.

## Mage
This produced the strongest current-roster role-expression watch.

Current SPLITTER capability-test child HP anchor is `120`.
Under the approved 35% one-generation chain and legacy Lv21 Heavy +20% Mage transform, a chain hit is approximately:

| Parent tier basis | Chain hit | 120-HP child |
|---|---:|---|
| NORMAL | 35 | survives |
| GOOD | 49 | survives |
| PERFECT | 70 | survives |
| HEAVY | 76 | survives |
| HEAVY+ | 97 | survives |
| GREAT | **126** | can die |
| SUPER | **168** | can die |
| CRITICAL | **252** | can die |

Because current authoritative ordering inserts SPLITTER children immediately at parent death, the approved Lv26 rule can select those newborn children after root-package death/spawn consequences.

Therefore, in a qualifying dense action:

```text
root package kills SPLITTER parent
+ hits another enemy
-> children spawn
-> Lv26 Chain Explosion target selection
-> GREAT/SUPER/CRITICAL heavy chain can immediately remove 120-HP test-anchor children
```

This is **not an uncontrolled recursive bug**; generation remains bounded to one.
But it can erase SPLITTER transformation consequence in designated role-expression encounters.

Classification:
`LV26_MAGE_SPLITTER_ORDERING_WATCH = HIGH`

Do not solve this by immediately nerfing Mage or inflating SPLITTER HP.
Later current-roster authoring/calibration should first check whether TEACH/STANDARD SPLITTER encounters preserve a meaningful transformation opportunity. MASTERY encounters may legitimately allow faster preemption.

---

# 6. EXP interpretation

P4-C2 reinforces, rather than resolves, the R2 progression issue.

Observed direction:

```text
offensive Lv26 power
-> faster target removal
-> fewer local timing turns
-> less later pure-per-turn EXP opportunity
```

Tank can produce the opposite local effect by extending enemy lifetime through control.

Therefore:
- do not freeze pure-per-turn EXP as final;
- do not add class-specific hidden XP compensation now;
- keep all R2 watches;
- mandatory P10R reconvergence remains necessary after credible current-roster multiplayer scaling.

---

# 7. Cross-stage consistency review

## Upstream
- P1 lifecycle preserved.
- P2 effect/attribution semantics preserved.
- P3 Stage-local temporary boundary preserved.
- no generic Lv26 scalar proxy introduced.

## Encounter / role expression
No structural FAIL requiring P4-C1 reopen was found.
High watches:
- Mage/SPLITTER transformation consequence;
- Archer/Knight screen-depth reduction;
- Tank effect on SIEGER pre-expression exposure.

## Downstream
P5/P6 must later re-test Lv26 feedback once shop power changes kill speed.
P8/P9 must re-check late soft-wall behavior.
P10 must test duplicate-class/mixed-team current-roster scaling.
P10R remains mandatory for final EXP convergence.

## Scope
No exact launch Stage was authored.
No monster or skill production coefficient was frozen.
No production gameplay source changed.

---

# 8. Verdict

`P4-C2 = COMPLETE / PASS_WITH_WATCHES`

No evidence currently justifies reopening the approved Lv26 structural contract.
No evidence justifies freezing the provisional Lv26 coefficients as production numbers.

Active watches now include:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
LV26_T4_ROLE_EXPRESSION_WATCH
LV26_MAGE_SPLITTER_ORDERING_WATCH
LV26_TANK_MOVEMENT_COMPOSITION_WATCH
```

Next dependency boundary:

`P4-D1 — LV31 STRUCTURAL SKILL-CONTRACT DECISION`

P4-D1 may now recover/analyze the five Lv31 identities and prepare a user decision packet.
It must not silently freeze Lv31 semantics or begin P4-D2 before explicit user approval.
