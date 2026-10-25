# Timing Defense — Project Status

Updated: 2026-10-25 KST

## Production / harness
- production branch `timing-defense-cloudflare-do-poc`
- verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- calibration harness `timing-defense-skilled-v2-harness-v01`
- verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- production gameplay/numerical changes remain unauthorized.

## Canonical authority chain
Live remote always wins.

Current late-T1 chain:
- P6 closure: `156_P6_STRUCTURAL_CLOSURE_WITH_WATCHES_V0_1.md`
- four-Tier adoption/correction: `158` / `160`
- T1 Stage1-50 skeleton/static audit: `161` / `162`
- representative-slice preflight/materialization: `163` / `164`
- micro-sim contract/adapter: `165` / `166`
- exact baseline result: `167_T1_TRANSITION_SLICE_EXACT_SOURCE_MICROSIM_RESULT_V0_1.md`
- v0.2 pressure/Lv31-absence/duration result: `168_T1_PRESSURE_SHAPE_V0_2_LV31_ABSENCE_AND_DURATION_SENSITIVITY_RESULT_V0_1.md`
- Stage49-50 class-rotation result: `169_T1_STAGE49_50_CLASS_ROTATION_AND_SUSTAIN_DIAGNOSTIC_RESULT_V0_1.md`
- authoring static preflight: `170_T1_STAGE49_50_STAGGER1800_AUTHORING_CANDIDATE_STATIC_PREFLIGHT_V0_1.md`
- authoring dynamic admission: `171_T1_STAGE49_50_STAGGER1800_AUTHORING_CANDIDATE_DYNAMIC_ADMISSION_V0_1.md`
- rejected Stage50 cluster-final diagnostic: `172_T1_STAGE50_CLUSTER_FINAL_CONSEQUENCE_TRANSLATION_DIAGNOSTIC_V0_1.md`
- Mage P×P/settlement-tail attribution: `173_T1_MAGE_STAGE50_PXP_AND_SETTLEMENT_TAIL_ATTRIBUTION_V0_1.md`
- candidate: `legacy-game-structure/data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`
- active plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_51.yaml`

---

# Current phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 shop = USER APPROVED
P5 class identity group = DIRECTIONALLY CLOSED
P5->P6 fidelity bridge = EXACT TEMP PASS
P6 = USER_APPROVED STRUCTURAL CLOSED WITH WATCHES
Initial campaign = FOUR TIER / USER APPROVED
Monster availability ladder = USER APPROVED
T1 roster = GRUNT / RUNNER / BRUTE / USER APPROVED
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
baseline representative recipe = STATIC PASS / EXACT-SOURCE EXECUTED
transition micro-sim runner = IMPLEMENTED / EXACT-SOURCE ADMISSION PASS
settlement ordering defect = FOUND / CORRECTED / SUPERSEDED
v0.2 pressure-shape candidate = DIAGNOSTIC ONLY / EXACT-SOURCE EXECUTED
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration lever = SUPPORTED
uniform late repetition = CLASS-SKEWED / NOT ADOPTED
Stage49-50 class-rotation diagnostic = PASS_WITH_WATCH
Stage49-50 authoring candidate = STATIC PASS / DYNAMIC REPRODUCTION PASS_WITH_WATCHES
Stage50 CLUSTER-final variant = REJECTED
Mage small Stage50 settle inversion = VALID DELAYED-PACKAGE TAIL ATTRIBUTED
CURRENT = STAGE49-50 AUTHORING ADOPTION DECISION GATE
candidate adopted = NO / USER APPROVAL REQUIRED
full exact T1 Stage1-50 recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Fixed campaign authority

```text
T1 = GRUNT / RUNNER / BRUTE
T2 = + SHIELD / FLYER
T3 = + CHARGER / SPLITTER
T4 = + SUPPORTER / SIEGER
T5+ = future expansion
```

Tier identities:
```text
T1 Foundation / Timing & Frontline
T2 Mitigation / Geometry
T3 Burst / Transformation
T4 Formation / Siege
```

Historical GRUNT-mix contradiction remains closed:
```text
obsolete = GRUNT first mixed Stage4-6
canonical = GRUNT first mixed Stage8-12
```

---

# T1 structural authority

Skeleton/static audit:
```text
structural FAIL = 0
PASS_WITH_WATCHES
pressure = BASELINE22 / FLOOD8 / RUSH16 / BULWARK16
complexity = C0 8 / C1 25 / C2 15 / C3 2 / C4 0
rolling 10-Stage class opportunity = 41/41 PASS
```

Late-T1 signatures:
```text
Stage49 = E02+E03 / R+B / F08 / CD05 / C2 / RUSH+BULWARK
Stage50 = SYNTH E01+E02+E03 / G+R+B / MULTI / CD03 / C3 / BASELINE
```

---

# Runner fidelity authority

Correct settlement ordering:
```text
authored spawns complete
+ zero live Stage-owned enemy
+ authorized delayed combat-event queue drained
=> STAGE_SETTLED
=> Stage-local passive residue clears
```

Settlement bridge:
`tools/run_t1_transition_slice_microsim_settlement_fix_v0_1.py`

Mage Lv31 diagnostic fidelity bridge restores inherited Y-radius semantics and full-package hit exclusion. This is semantic fidelity correction only, not numerical freeze.

Archer Lv31 diagnostic bridge uses `yTolerance=0.20` only to model the approved materially wider corridor. Exact width remains unfrozen and is not encoded into authoring data.

---

# Stage49-50 admitted candidate

Candidate:
`legacy-game-structure/data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`

SHA256:
`c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3`

Grammar:
```text
phase gap = 5500 ms

Stage49:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE

Stage50:
DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE
```

Important CLUSTER distinction:
```text
Stage49 CLUSTER
= GRUNT/RUNNER/GRUNT/RUNNER/BRUTE/GRUNT
= offsets 0/120/240/360/480/600 ms
= distinct-grammar burst

Stage50 CLUSTER
= BRUTE/GRUNT/BRUTE/GRUNT/BRUTE/GRUNT
= offsets 0/360/720/1080/1440/1800 ms
= DURABLE_CORE_3 / STAGGER_1800
```

Probe-only metadata broadening was not promoted. Stage49/50 metadata remains aligned with canonical skeleton/v0.2 authority.

---

# Exact evidence chain

## Static authoring legality — doc170
```text
run      40156618986
artifact 12585015454
head     4a06adbb523dd63e0a2a5fefb31fbb2553c0e4d1
artifact sha256 ac2d233af17dd0f5415169d7daec38bfc472c3409bfe626ea756d8e986bd1676
```

Result:
```text
PASS / errors=[] / warnings=[]
metadataPreservedFromV02 = true
Stage49 authored24 / max4s6 / max6s11 / y0.18..0.82
Stage50 authored30 / max4s6 / max6s9 / y0.18..0.82
```

## Dynamic materialization reproduction — doc171
```text
run      40156895093
artifact 12585270921
head     cd5d28ac6748a65b8e46c8c664954223a8cf5ef3
artifact sha256 9f1ca98b624c31ffce1beefc5ca8dc17cbcdd2309d2db8abec7eb92cb66ebe8c
fidelityErrors = []
Stage49/50 spawn equivalence = true / true
```

Lv31 OFF->ON role-facing reproduction:
```text
Knight +43.0303%
Rogue  +30.0662%
Tank   +27.3684% + 3 unresolved reduced
Archer +1.7241%
Mage   +9.4216%
```

Objective protection:
```text
OFF wall damage 1358
ON  wall damage 164
OFF mean final Base HP 1945.68
ON  mean final Base HP 1993.44
fail/incomplete 0 / 0
```

## Stage50 CLUSTER-final chronology probe — doc172
```text
run      40157211995
artifact 12585421260
head     fd88ab0d5deb2cb483c6931aa4ba16293a472620
artifact sha256 e988398a06990cd16e7b8dbe004ed2ee287f9c2be01dcd4acef167f818101f6b
```

Variant:
```text
DS -> FRONTLINE -> LINE -> LINE_REPRISE -> CLUSTER
```

Result:
```text
fidelity/static PASS
Mage CLUSTER OFF 4728ms = ON 4728ms / 0% improvement
Mage whole-window mastery delta remains -0.472s
variant = REJECTED
```

Therefore simply moving CLUSTER to Stage termination does not improve Mage consequence translation.

## Mage P×P / settlement-tail attribution — doc173
```text
run      40157463857
artifact 12584527727
head     d2fc1c3e85b32012edcfdf8f7db49032ea802671
artifact sha256 78ae92b8f948a0824d94a33dc34091c6f74eb904645bfe4a5de016a289338c8a
fidelityErrors = []
```

Current admitted Stage50 CLUSTER:
```text
P×P occurs in CLUSTER in 4/5 seeds
ON primary target from CLUSTER = 4/4
mean Lv31 unique targets = 4.0
mean Lv31 damage = 1342.5
mean CLUSTER-origin targets hit = 4.0
```

Rejected CLUSTER-final:
```text
mean Lv31 unique targets = 3.25
mean Lv31 damage = 1078.75
```

Mage Stage50 mean settle:
```text
OFF 26.800s
ON  26.908s
apparent ON slowdown = 0.108s
```

Attribution:
- four seeds settle 180ms later on ON because the authorized staged Lv31 delayed package remains in the combat-event queue;
- one seed gains 180ms at combat level;
- net `(4×180 - 180)/5 = 108ms`.

Therefore:
```text
MAGE_STAGE50_SETTLE_INVERSION = VALID_DELAYED_PACKAGE_TAIL_EFFECT_IN_THIS_SAMPLE
NOT EVIDENCE OF LV31 ROLE/DAMAGE FAILURE
```

Do not weaken settlement fidelity by discarding delayed events to improve this metric.

---

# Current assessment

```text
static authoring legality = PASS
exact materialization fidelity = PASS
dynamic reproduction = PASS
five-class role-facing direction = POSITIVE
Mage Stage50 role expression = REAL
Mage small settle inversion = EXPLAINED BY VALID SETTLEMENT TAIL
CLUSTER-final alternative = REJECTED
objective wall pressure = STILL TANK-SKEWED
Archer role signal = MODEST POSITIVE
scalar change required = NOT SHOWN
candidate authoring adoption = NOT YET
```

Further local Stage49-50 chronology/scalar search is not justified by current evidence.

---

# Active watches

```text
T1_RUNNER_LV6_PEDAGOGIC_COLLISION_WATCH
T1_BRUTE_LV16_CALIBRATION_COLLISION_WATCH
T1_RUNNER_HIGH_PRESSURE_LV16_TAIL_WATCH
FRESH_FORWARD_ABSOLUTE_MAGNITUDE_WATCH
TANK_CONTROL_DEFENSE_TO_OBJECTIVE_PROTECTION_WATCH
T4_SUPPORTER_SIEGER_LEARNING_DENSITY_WATCH
TEMP_BRANCH_PUSH_TRIGGERS_HARNESS_CLOUDFLARE_BUILD_WATCH
T1_STAGE49_50_OBJECTIVE_PRESSURE_ROTATION_WATCH
```

Residual Stage49-50 watch means current exact sample has material wall pressure concentrated in Tank cases. It does **not** require equal wall damage across classes; Tank objective-protection identity is expected to be more visible there.

---

# Current decision gate

Recommended decision:
```text
ADOPT current Stage49-50 candidate as the canonical T1 structural authoring baseline WITH WATCHES
```

If approved, adoption means only:
```text
STRUCTURAL AUTHORING BASELINE
+ existing watches
```

It explicitly does **not** mean:
```text
production gameplay change
numerical freeze
Archer yTolerance=0.20 freeze
Mage Lv31 numerical freeze
monster/class/shop/EXP/P×P scalar freeze
full T1 Stage1-50 exact recipe freeze
```

If approved, next bounded step is:
```text
PREPARE WIDER T1 EXACT AUTHORING PLAN + STATIC PREFLIGHT
```
not immediate full-50 production freeze.

If not approved, continue Stage49-50 diagnosis only against the specific rejection reason.
