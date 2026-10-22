# Timing Defense — P4 Full Player-Power Spine / EXP Model Proposal V0.1

Date: 2026-10-23 KST  
Status: **PROPOSED / AWAITING USER APPROVAL / NO NUMERICAL FREEZE**

Depends on:
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`
- `../DESIGN_DECISIONS.md`
- `../SKILL_PLAN_LV6_31.md`
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `data/p4_exp_preproposal_diagnostics_v0_1.json`
- `../tools/analyze_p4_exp_baseline_from_p3.py`

---

# 0. Decision boundary

P4 must produce a **provisional 50-Stage run-level / skill-reach spine** before real shop leverage and permanent progression are introduced.

The immediate task is not to guess one EXP formula.
It is to choose the smallest calibration structure that can:
- place Lv6/11/16/21/26/31 in intended Stage windows;
- remain shared across all five classes;
- remain viable across T1–T4 encounter identities;
- preserve timing quality as the source of faster progression;
- expose rather than hide the feedback `more power -> fewer required attacks -> fewer EXP opportunities`;
- remain recalibratable after shop/permanent power are added later.

This proposal does **not** freeze any final EXP number, Stage schedule, Lv26/Lv31 production skill, or production implementation.

---

# 1. Canonical constraints already present

## 1.1 Run reset / progression
- every Tier attempt starts at Lv1 / EXP0;
- level/EXP persist through Stages inside the attempt;
- run-local state resets on a new attempt.

## 1.2 EXP philosophy
Current product history and canonical decisions establish:
- EXP is tied to valid local timing play;
- passive attacks do not generate player EXP;
- empty timing turns do not generate EXP;
- a valid already-started timing turn may still resolve/reward if the target disappears mid-turn;
- better timing quality should produce more EXP;
- legacy analysis did not automatically compensate a faster-killing class merely because it needed fewer attacks.

## 1.3 Reach windows
Current calibration windows:

```text
Lv6   Stage 5–7    candidate
Lv11  Stage11–14   candidate
Lv16  Stage18–21   candidate
Lv21  Stage25–28   candidate
Lv26  Stage32–36   candidate
Lv31  Stage41–45   USER-CONFIRMED structural direction
```

Stage46–49 is the explicit post-Lv31 mastery-use band.
Stage50 must not be the first meaningful Lv31 use.

## 1.4 Authority boundary
- Lv6 = current authoritative mechanics.
- Lv11/Lv16/Lv21 = exact v0.16 legacy-parity candidates, not current production authority.
- Lv26 = designed but not authoritative; exact simulation contract needs explicit approval.
- Lv31 = role direction exists, exact production mechanics remain unresolved.

---

# 2. Preproposal diagnostic evidence

Reproducible diagnostic:
- `tools/analyze_p4_exp_baseline_from_p3.py`
- `data/p4_exp_preproposal_diagnostics_v0_1.json`

The diagnostic intentionally uses the approved P3 synthetic first-10 fixture and therefore is **not launch-balance evidence**.
It is sufficient to reject clearly incompatible legacy progression scale and expose feedback direction.

## 2.1 Legacy absolute curve is too fast
Legacy prototype:

```text
levelNeed(level) = 60 + 12 × (level - 1)
```

Cumulative thresholds:

```text
Lv6    420
Lv11  1140
Lv16  2160
Lv21  3480
Lv26  5100
Lv31  7020
```

Legacy completed-turn grants:

```text
NORMAL    8
GOOD     12
PERFECT  18
HEAVY    10
HEAVY+   14
GREAT    18
SUPER    23
CRITICAL 28
```

When those exact legacy absolute thresholds are replayed against the current P3 central-skilled first-10 fixture, observed unlock-stage distribution is:

```text
Lv6   P25/P50/P75 = 2 / 2 / 3
Lv11  P25/P50/P75 = 6 / 6 / 7
Lv16  P25/P50/P75 = 10 / 10 / 10
```

This is structurally incompatible with the current 50-Stage target windows.
Therefore the old absolute `levelNeed()` curve is rejected as a P4 authority candidate.

## 2.2 Relative quality shape is separable from absolute scale
The same legacy grant vector can be normalized by `NORMAL=1.0`:

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

Under the current streak-aware central model and the existing every-fourth-action Heavy grammar, expected legacy-shaped reward per completed turn is approximately:

```text
old Average iid       13.625 old units
old Skilled iid       15.780
current Central       17.875
all-PERFECT           20.500
```

Implication:
- current Central receives about +31% vs the old Average reference;
- all-PERFECT is only about +15% above current Central.

This is a useful initial reward-shape candidate because timing quality matters materially without making perfect mastery several times faster than intended-entry skilled play.
It is still only a candidate.

## 2.3 Skill-power feedback is already material at Lv6
P3 forced-Lv6 vs LV1 continuity, first-10 synthetic fixture:

```text
Knight  timing-event opportunity  ~ -0.2%
Rogue                             ~ -20.2%
Tank                                0.0%
Archer                            ~ -18.9%
Mage                              ~ -14.7%
```

The direction is expected:
- offensive/multihit power kills enemies faster;
- fewer local timing turns are required;
- later EXP opportunity falls.

This feedback must be measured, not silently patched away.
It can act as natural self-damping, but it becomes a defect if a class or later permanent-power state is pushed structurally outside the intended skill windows.

---

# 3. Decision A — EXP source semantics

## A1 — valid local timing-turn EXP only
**RECOMMENDED.**

Primary P4 baseline:
- EXP comes from a valid completed local timing turn;
- no player kill EXP;
- no raw damage EXP;
- no passive/AI EXP;
- no flat Stage-clear EXP;
- no hidden class-specific catch-up EXP;
- an already-valid started turn may resolve/reward according to the existing no-target rule;
- an empty/no-target turn cannot farm EXP.

Why:
- preserves the established timing-progression identity;
- keeps progression attributable to player timing;
- does not double-reward already-strong damage/kill paths;
- retains the previously accepted self-damping relationship between kill speed and future EXP opportunity;
- has the fewest hidden correction layers.

## A2 — timing EXP + kill/damage EXP
Not recommended for P4 baseline.

Problem:
- high-DPS/AOE classes get both faster kills and extra progression;
- increases snowball and class divergence;
- makes attribution harder.

## A3 — timing EXP + automatic Stage top-up/catch-up
Not recommended initially.

This can stabilize reach but would partially erase the currently accepted event-opportunity consequence.
Keep only as a later fallback if a universal timing-turn curve cannot satisfy the structural reach windows.

**Recommendation:** approve A1 as P4 baseline semantics; do not permanently forbid a later evidence-driven stabilizer.

---

# 4. Decision B — EXP award unit and Heavy semantics

The legacy implementation awarded EXP once when a local attack turn resolved.
A Heavy turn contains X and Y judgments but produces one combined attack tier.

## B1 — one EXP award per completed valid timing turn
**RECOMMENDED.**

Normal turn:
```text
NORMAL / GOOD / PERFECT -> one quality reward
```

Heavy turn:
```text
X + Y -> combined HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL
      -> one quality reward
```

Why:
- preserves existing product behavior and one visible `+EXP` event per resolved attack;
- treats Heavy as one stronger two-axis turn instead of automatically doubling progression every fourth attack;
- still rewards P×P strongly through CRITICAL quality;
- reduces one unnecessary degree of freedom.

## B2 — award X and Y independently
Not recommended for the first P4 candidate.

It changes established Heavy progression semantics and creates an automatic Heavy XP multiplier independent of actual Stage design.
It can be reconsidered only if B1 cannot produce acceptable skill-reach behavior.

---

# 5. Decision C — timing-quality reward shape

Absolute EXP display numbers are scale-arbitrary: multiplying every grant and every threshold by the same constant changes nothing about reach.
Therefore P4 should not tune both at once.

## C1 — use normalized `XP_CREDIT` for calibration
**RECOMMENDED.**

Primary candidate relative vector:

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

This preserves the legacy relative shape while discarding the obsolete absolute scale.

For sensitivity only, P4 may compare a gentler and a stronger quality vector, but the legacy-shape vector is the primary candidate.
A sensitivity lane passing does not freeze it.

Final player-visible integer EXP scale is deferred until reach structure is accepted.

Why:
- separates meaningful balance (relative mastery reward) from arbitrary UI unit size;
- reduces parameter count;
- current Central vs perfect separation is meaningful but not explosive under this shape.

---

# 6. Decision D — level-threshold representation

## D1 — reuse one global closed-form `levelNeed()` now
Not recommended.

The six skill windows are not known to fit a simple linear/quadratic formula, and forcing a formula first reverses the intended inverse-design process.

## D2 — independently tune all 30 level thresholds
Not recommended.

Too many degrees of freedom, hard to audit, easy to overfit synthetic Stage content.

## D3 — six cumulative milestone anchors + monotonic interpolation
**RECOMMENDED.**

Represent cumulative credit threshold as:

```text
A6
A11
A16
A21
A26
A31
```

where each `Axx` is fitted to the corresponding Stage window.
Intermediate levels between milestone anchors are generated by transparent monotonic interpolation, initially piecewise-linear in cumulative threshold space.

Example conceptual form only:

```text
T(1)=0
T(6)=A6
T(11)=A11
...
T(31)=A31
```

No `Axx` numerical value is approved by this proposal.

If accepted later, the six-anchor curve may be compressed into a simpler closed form only after P6/P11 feedback loops are checked.

Advantages:
- six knobs correspond exactly to six meaningful progression milestones;
- much lower overfit risk than 30 independent values;
- does not force an unsuitable formula;
- easy to refit when shop/permanent power shifts event counts.

---

# 7. Decision E — 50-Stage calibration corpus

A single synthetic 50-Stage schedule would invite overfitting.
Exact 200-Stage launch authoring is intentionally downstream.

## E1 — one T1 synthetic Tier only
Not recommended.

All Tiers restart Lv1, while T2–T4 combat identities change event opportunity.
A universal EXP curve must survive all current Tier identities.

## E2 — exact T1–T4 production schedules now
Not allowed by current dependency order.

## E3 — bounded multi-schedule T1–T4 synthetic corpus
**RECOMMENDED.**

For each T1/T2/T3/T4:
- generate multiple legal 50-Stage synthetic schedules;
- respect current monster availability, teaching windows, pressure ranges, complexity ranges and anti-repetition rules;
- reuse admitted representative encounter anchors instead of inventing production coefficients;
- include lower / central / upper plausible timing-opportunity schedules so one exact content sequence cannot define the EXP curve;
- pair the same schedule across classes and player seeds.

Initial bounded target:
```text
4 Tiers × 3 synthetic schedule envelopes = 12 fifty-Stage fixtures
```

The number 3 is a calibration coverage choice, not production content count.
If static generation cannot produce meaningful envelope separation without violating current ranges, stop and report rather than invent new Stage authority.

---

# 8. Decision F — skill authority inside P4

P4 should not invent late-skill damage merely to finish a graph.

Recommended phased integration:

## F0 — reach/opportunity inverse-design lane
- skill milestones may first be treated as unlock markers;
- purpose = derive initial milestone-anchor thresholds from event-opportunity distributions;
- not a final P4 result.

## F1 — current/legacy-authority feedback lane
After the initial curve exists:
- Lv6: use current authoritative mechanics;
- Lv11/Lv16/Lv21: use exact v0.16 parity candidates as **simulation-only candidate authority**;
- measure how those power spikes change later event opportunity and refit anchors if needed.

Approval of this P4 use does **not** make Lv11–21 production-frozen.

## F2 — Lv26 decision gate
- do not invent a generic numeric power scalar;
- first quantify the Stage32–36 reach surface and how much downstream Lv31 reach depends on Lv26 power;
- then analyze the current designed Lv26 identities and return a separate user decision packet for a simulation contract;
- only after approval, rerun the Stage32–45 feedback loop.

## F3 — Lv31 decision gate
- Lv31 reach itself can be measured before Lv31 power is applied;
- but `post-unlock power slope`, Stage46–49 mastery use and Stage50 effect cannot be closed until a bounded Lv31 simulation contract is separately approved;
- no invented Lv31 scalar proxy.

Therefore P4 is deliberately multi-gate rather than a one-shot formula fit.

---

# 9. Decision G — percentile calibration policy

Existing canonical documents require P25/P50/P75/P90 recording but intentionally leave exact tail cutoffs open.

**RECOMMENDATION:**

First 50-Stage calibration pass:
- optimize/fit against `P50 unlock Stage` for each milestone;
- require the Lv31 P50 to lie inside the user-confirmed Stage41–45 window;
- use the other milestone windows as candidate targets, not irreversible constraints;
- always record P25/P50/P75/P90, class, Tier and schedule-envelope distributions;
- do **not** freeze P75/P90 acceptance cutoffs before observing the first full distribution.

After the first evidence set:
- propose explicit tail acceptance thresholds;
- particularly inspect how many paths first receive Lv31 after Stage45 and whether Stage49–50 becomes first meaningful use.

This avoids arbitrary percentile policy while preserving the user-confirmed Lv31 structural requirement.

---

# 10. Decision H — universal curve / no hidden class correction

**RECOMMENDED:** one universal run-level EXP curve for all five classes and all current Tiers.

Do not introduce:
- class-specific EXP multipliers;
- Tier-specific hidden XP multipliers;
- automatic catch-up solely because a class kills faster.

If one class unlocks materially later:
1. inspect whether its offensive power reduced timing opportunities;
2. inspect encounter composition / target availability;
3. inspect the milestone threshold / skill spike interaction;
4. classify whether the difference is healthy self-damping or structural lockout;
5. only then consider a visible/general stabilizer, not a hidden per-class patch.

The P3 Lv6 result already shows this feedback is real:
Rogue/Archer/Mage lose roughly 15–20% first-10 timing-event opportunity after their offensive Lv6 effects activate, whereas Tank/Knight are nearly unchanged in that fixture.
This is evidence to monitor, not automatic authorization to compensate it.

---

# 11. P4 internal work order after approval

Recommended sequence:

```text
P4-A  build bounded T1–T4 50-Stage synthetic corpus
      + XP_CREDIT reward model
      + six milestone threshold anchors
      + skill-marker inverse design

P4-B  integrate Lv6 + Lv11/16/21 simulation candidates
      -> remeasure event opportunity
      -> refit/check Lv6..26 reach
      -> class/Tier/schedule envelope distribution

P4-C  analyze Lv26 designed mechanics
      -> user decision gate
      -> approved simulation contract
      -> rerun Stage32..45 / Lv31 reach

P4-D  analyze Lv31 mechanics
      -> user decision gate
      -> approved simulation contract
      -> Stage46..49 mastery / pre-post power slope

P4-E  percentile/tail review
      -> explicit user decision on final P4 candidate curve
      -> only then close P4 and unlock P5
```

P4-A/B simulations are candidate generation and diagnostics, not numerical production freeze.

---

# 12. Search / confirmation efficiency

Do not start with huge Monte Carlo.

Use a two-pass deterministic approach:
1. bounded search sample to fit anchors and expose structural defects;
2. larger paired-seed confirmation only after a candidate survives.

All comparisons must pair:
- Tier fixture version;
- class;
- player-model seed;
- reward-shape candidate;
- skill-authority lane.

Exact diagnostic sample count is an engineering/test-quality choice and does not need to become a product rule.

---

# 13. Failure classifications to use

P4 should distinguish at least:
- `LEGACY_EXP_SCALE_TOO_FAST`
- `MILESTONE_MEDIAN_EARLY`
- `MILESTONE_MEDIAN_LATE`
- `LATE_LV31_DISTRIBUTION`
- `INSUFFICIENT_LV31_PLAY_WINDOW`
- `SKILL_POWER_EVENT_OPPORTUNITY_FEEDBACK_HIGH`
- `CLASS_REACH_DIVERGENCE`
- `TIER_REACH_DIVERGENCE`
- `SYNTHETIC_SCHEDULE_OVERFIT`
- `LV26_AUTHORITY_BLOCKER`
- `LV31_AUTHORITY_BLOCKER`
- `CATCHUP_STABILIZER_EVIDENCE_REQUIRED`

A failure must not automatically cause monster HP or EXP compensation changes.
It first requires attribution.

---

# 14. Explicitly remains OPEN

Approval of this proposal would not approve:
- any exact EXP amount shown to the player;
- exact `A6/A11/A16/A21/A26/A31` thresholds;
- final relative XP quality weights;
- exact percentile tail cutoffs;
- class/Tier-specific reach tolerance;
- any kill/damage/Stage-clear EXP;
- any catch-up/stabilizer layer;
- exact Stage schedules;
- final Lv11–21 production authority;
- Lv26 mechanics;
- Lv31 mechanics;
- shop/economy;
- permanent star/achievement values;
- production deployment.

---

# 15. Requested user approval package

Approve or modify the following P4 directions:

1. **P4 baseline EXP remains valid completed local timing-turn based only**; no kill/damage/passive/flat Stage-clear EXP and no hidden class compensation.
2. **One EXP award per completed timing turn**; Heavy X+Y resolves to one combined quality reward, preserving current/legacy turn semantics.
3. Use **dimensionless XP_CREDIT** during calibration, with the legacy relative quality vector as the primary candidate and gentler/stronger vectors only as sensitivity lanes; do not preserve legacy absolute scale.
4. Replace the old closed-form `levelNeed()` with **six cumulative milestone anchors + transparent monotonic interpolation** for the P4 candidate.
5. Calibrate against a **T1–T4 multi-schedule synthetic corpus**, initially 3 legal opportunity-envelope fixtures per Tier, not one schedule and not exact launch authoring.
6. Use **Lv6 authoritative + Lv11/16/21 exact legacy-parity mechanics as simulation-only feedback candidates** after the marker-only inverse-design pass; keep Lv26 and Lv31 behind separate later P4 user gates.
7. First fit **P50** into milestone windows, record P25/P50/P75/P90, and defer exact tail acceptance cutoffs until the first 50-Stage evidence exists; Lv31 Stage41–45 remains the hard structural direction.
8. Keep **one universal EXP curve** across classes/Tiers; treat kill-speed-driven EXP reduction as measured self-damping unless evidence shows structural failure. Any stabilizer/catch-up system requires a later evidence-backed user decision.

Only after approval should P4-A/B simulator/data implementation begin.
