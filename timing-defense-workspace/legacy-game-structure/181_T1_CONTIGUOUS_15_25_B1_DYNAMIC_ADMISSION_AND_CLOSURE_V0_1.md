# Timing Defense — T1 Contiguous Stage15–25 B1 Dynamic Admission and Closure V0.1

Date: 2026-10-26 KST  
Status: **B1 PASS_WITH_WATCHES / STAGE16–17 NOT ADOPTED / USER DECISION GATE NEXT / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `111_P4E_PROVISIONAL_PLAYER_POWER_SPINE_CLOSURE_WITH_EXP_WATCHES_V0_1.md`
- `167_T1_TRANSITION_SLICE_EXACT_SOURCE_MICROSIM_RESULT_V0_1.md`
- `174_T1_STAGE49_50_STRUCTURAL_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`
- `180_T1_WAVE_A_EXACT_SPAWN_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`
- `data/t1_contiguous_15_25_b1_stage16_17_candidate_v0_1.yaml`

---

# 0. Question

Can the two missing bounded recipes, Stage16 and Stage17, complete a real contiguous Stage15→25 exact-recipe window and execute through the existing settlement-corrected skilled-player micro-sim without skipped-Stage lifecycle fabrication?

Answer:

**YES, as dynamic admission evidence. B1 = PASS_WITH_WATCHES.**

This does not adopt Stage16/17 content. Their exact spawn authoring remains candidate-only until a separate user decision.

---

# 1. Static input authority

B1 candidate:
`legacy-game-structure/data/t1_contiguous_15_25_b1_stage16_17_candidate_v0_1.yaml`

Live exact candidate SHA256 used by the dynamic run:
`b9abc507c5ccdc20bc19c5681ba92cead920326fa9d04c1acf5b2ed90ff91465`

The same-run static preflight reproduced a contiguous exact Stage15–25 window with:

```text
status = PASS
errors = []
warnings = []
authorityPreserved = true
contiguous15to25 = true
materialized Stage set = 15..25 inclusive
```

Live exact materialized byte SHA256:
`f769dd79e750882a6b7a75dad18bfdbc514da546b183587ec2ed909e50b2ed0f`

Stage16 candidate:
```text
BRUTE ×4
0 / 1400 / 2800 / 4200ms
F02 / CD02 / C1 / BULWARK
```

Stage17 candidate:
```text
GRUNT ×5
0 / 300 / 600 / 3000 / 3300ms
F01 / CD03 / C1 / BASELINE
```

Existing exact authority was preserved for Stage15,18,19,20,21,22,23,24,25.

---

# 2. Lv16 / Lv21 activation authority recovery

The current power-spine authority does **not** freeze an exact activation Stage for Lv16 or Lv21.

Document79 defines calibration-candidate reach bands:

```text
Lv16 = Stage18–21
Lv21 = Stage25–28
```

Document111 reaffirms that these lower milestone windows remain calibration candidates, not final EXP authority. Only the late Lv31 band has stronger structural confirmation.

Therefore B1 did not choose one hidden EXP threshold or one exact activation Stage.

Bounded dynamic sensitivity variants:

```text
Lv16 reaches before Stage18  vs before Stage21
×
Lv21 ACTIVE at Stage25 entry vs still AFTER Stage25
```

This covers the relevant boundary states inside the Stage15–25 window without pretending to freeze Stage26–28 content or EXP.

Stage15 begins with `[Lv6,Lv11]` active because the existing Stage18 paired-diagnostic contract already uses `[6,11]` as its prior state. This is inherited diagnostic context, not a new EXP freeze.

---

# 3. Dynamic runner contract

Runner:
- existing exact T1 transition micro-sim semantics;
- settlement correction remains active;
- persistent run state carries across every Stage15→25 boundary;
- no Stage is skipped;
- delayed combat-event queue must drain before `STAGE_SETTLED`;
- Stage-local residue clears only at the settled boundary.

Persistent continuity checked for:
```text
Base HP / Base Max HP / wall deficit
combo / charge
judgment RNG / combat-proc RNG
```

Seeds:
```text
101, 211, 307, 409, 503
```

Classes:
```text
Knight / Rogue / Tank / Archer / Mage
```

Variants × classes × seeds:
```text
4 × 5 × 5 = 100 persistent cases
```

---

# 4. Exact-source execution

Final admitted run:

```text
workflow run  40254326926
artifact      12622340036
exact HEAD    e5b12a2c386de719c97dc020aeef9ffdbd9b1b3a
artifact SHA256
2f940ebea4c8b2be008e937d45e46f10595ec106b847f49af5ce1dc1b77b3acf
```

Admission:

```text
status = PASS_DYNAMIC_DIAGNOSTIC_ONLY
exactMaterializedIdentity = true
persistentStateContinuity = true
deterministicReplay = true
settlementAndCarryInvariants = true
fidelityErrors = []
continuityErrors = []
replayErrors = []
invariantErrors = []
pass = true
```

Execution coverage:

```text
100 / 100 cases completed through Stage25
1100 Stage rows executed
terminal failure rows = 0
```

---

# 5. Superseded first-run identity failure

First dynamic workflow run:

```text
run      40254173222
artifact 12621508214
```

The static re-materialization step passed, but the v0.1 dynamic runner failed closed before combat interpretation because it contained a copied historical materialized byte SHA (`7295...`) that did not match the live exact same-run serialization (`f769...`).

Classification:

`B1_DYNAMIC_V01_STALE_MATERIALIZED_BYTE_IDENTITY_GUARD_FALSE_FAILURE`

No candidate recipe, combat rule, skill rule, lifecycle rule, or balance parameter was changed in response.

V0.2 only pinned the live exact materialized byte identity and reran the unchanged v0.1 combat/admission implementation.

The v0.1 failure is superseded and carries no balance conclusion.

---

# 6. Stage16 / Stage17 continuous behavior

Across all variants, Stage15–17 produced zero wall damage and no terminal failure.

Mean root timing-action counts by class are invariant to the later milestone variants in this prefix:

```text
             S15    S16    S17
Knight       9.0    8.6    5.0
Rogue        9.0    9.0    5.2
Tank        13.0   16.6    8.6
Archer      10.0    9.0    5.8
Mage        10.0    9.0    6.0
```

Interpretation:
- Stage16 does not create an objective-survival failure;
- Tank reads the extra durable body most strongly, consistent with its lower kill throughput;
- Stage17 is a clear decompression/recovery step for every class before Stage18's G+B first mix;
- no evidence requires changing the Stage16/17 candidate before an adoption decision.

---

# 7. Lv16 collision in real contiguous state

Comparing `Lv16@18` against `Lv16@21` while holding the Lv21 boundary condition matched shows the known class-asymmetric opportunity loss persists.

Mean `early - late` root timing-action delta at Stage18:

```text
Knight  -0.2
Rogue    0.0
Tank     0.0
Archer  -2.0
Mage    -2.6
```

Mean Stage18 settle-time delta:

```text
Knight  -0.220s
Rogue   -0.555s
Tank     0.000s
Archer  -2.200s
Mage    -2.680s
```

At Stage20, mean action delta remains class-asymmetric:

```text
Knight  -0.8
Rogue   +0.2
Tank     0.0
Archer  -1.8
Mage    -1.0
```

No Stage18 or Stage20 wall damage occurred in any case.

Interpretation:
- `T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH` remains materially justified;
- the collision is primarily timing-opportunity / kill-speed compression here, not immediate wall survival;
- this does not justify hidden EXP correction, class nerfs, or an exact Lv16 reach freeze.

---

# 8. Stage21–24 pressure and objective skew

Objective wall pressure first appears in this contiguous window at Stage21 and remains concentrated in Tank cases.

Tank mean wall damage:

```text
Stage21  17.2
Stage22  97.6
Stage23  81.6
Stage24  33.0
```

Knight / Rogue / Archer / Mage mean wall damage across Stage21–24:

```text
0.0 in this bounded sample
```

All 100 cases still complete Stage25; Tank mean final Base HP is `1770.6 / 2000`, while the other four classes remain at `2000 / 2000` in this bounded sample.

Interpretation:
- the historical Stage20–23 undershoot concern is not erased;
- objective-pressure expression remains class-skewed;
- equal wall damage is not a requirement because Tank's class identity is control/defense/objective protection rather than kill parity;
- nevertheless the asymmetry remains useful downstream evidence and must not be silently treated as fully calibrated.

Retain existing objective-pressure / Tank watches. No scalar change is authorized by this result.

---

# 9. Stage25 relief and Lv21 boundary

Stage25 produces:

```text
wall damage = 0
for all 100 cases
```

For Tank, mean Stage24→25 wall-damage change is:

```text
33.0 -> 0.0
Δ = -33.0
```

Thus Stage25's intended reward-buffer/objective-pressure relief is supported in the real contiguous lifecycle window.

Turning Lv21 on at Stage25 entry changes wall damage by `0` for every class in this sample. The measurable Stage25 local action/settle effect is mostly neutral; Mage shows approximately:

```text
mean actions   -0.4
mean settle    -0.422s
```

with the other classes approximately neutral on this Stage25 comparison.

Interpretation:
- Stage25 relief does not depend on forcing Lv21 active at Stage25;
- this sample does not numerically freeze Lv21 power or reach;
- Stage25 remains compatible with the Lv21 Stage25–28 calibration-candidate band.

---

# 10. B1 verdict

```text
B1 Stage16/17 materialization = STATIC PASS
Stage15-25 contiguous exact window = ESTABLISHED
persistent lifecycle dynamic admission = PASS
all cases through Stage25 = 100/100
terminal failures = 0
Stage17 recovery = SUPPORTED
Stage25 objective-pressure relief = SUPPORTED
Lv16 timing-opportunity collision = RECONFIRMED / WATCH
Stage21-24 objective pressure = CLASS-SKEWED / WATCH
B1 = PASS_WITH_WATCHES
Stage16/17 candidate adoption = NO
production change = NO
numerical freeze = NO
full T1 exact recipe freeze = NO
```

No evidence in this workgroup requires revising Stage16 or Stage17 before the authoring-adoption decision.

---

# 11. Next decision boundary

The B1 evidence workgroup is closed.

The next package is a user decision gate only:

`T1_B1_STAGE16_17_AUTHORING_ADOPTION_DECISION_GATE`

Question:

> Adopt the exact Stage16 and Stage17 spawn recipes as canonical T1 authoring baseline WITH WATCHES?

If approved, this means exact Stage16/17 spawn count, timestamp, type and Y placement become authoring authority.

It still does **not** authorize:
- production deployment;
- monster/class scalar freeze;
- final EXP or exact Lv16/Lv21 reach freeze;
- shop/P×P changes;
- full T1 Stage1–50 exact recipe freeze.

No further authoring work should start in this session. The recommended next action is to hand off to a fresh GPT session at this clean decision boundary.
