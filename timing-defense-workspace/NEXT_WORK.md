# Timing Defense — Next Work Boundary

Updated: 2026-10-25 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_48.yaml`;
5. read `170_T1_STAGE49_50_STAGGER1800_AUTHORING_CANDIDATE_STATIC_PREFLIGHT_V0_1.md`;
6. inspect candidate `legacy-game-structure/data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`;
7. read `169_T1_STAGE49_50_CLASS_ROTATION_AND_SUSTAIN_DIAGNOSTIC_RESULT_V0_1.md` and compact diagnostic summary;
8. inspect v0.2 base recipe;
9. preserve `168` pressure/duration result and `167` exact baseline result;
10. preserve runner contract/implementation `165/166`, settlement bridge, Mage Lv31 fidelity bridge and Archer diagnostic width bridge;
11. preserve T1 skeleton/static authority `160-164` and P6 closure `156`;
12. verify production/harness heads.

Do not rerun closed P6, the full T1 skeleton audit, baseline exact-source diagnostics, the completed order/sustain search, or the completed static authoring preflight without a concrete trigger.

---

# Current phase

```text
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
baseline representative recipe = STATIC PASS / EXACT-SOURCE EXECUTED
micro-sim runner = EXACT-SOURCE ADMISSION PASS AFTER SETTLEMENT CORRECTION
v0.2 pressure-shape candidate = STATIC PASS / DYNAMIC DIAGNOSTIC ONLY
Stage41 relief = RECONFIRMED
v0.2 Stage46-50 Lv31 absence = TOO SAFE
pressure duration lever = SUPPORTED
uniform pulse repetition = CLASS-SKEWED / NOT ADOPTED
Stage49-50 class-rotation diagnostic = PASS_WITH_WATCH
DIAGNOSTIC CENTER = STAGGER_1800_STAGE50_CLUSTER_ONLY
Stage49-50 authoring candidate = MATERIALIZED / STATIC PASS
objective-pressure rotation = STILL SKEWED TOWARD TANK
CURRENT = MATERIALIZED CANDIDATE NARROW EXACT DYNAMIC ADMISSION
full 50-Stage exact recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Exact diagnostic center to preserve

Phase gap:
```text
5500 ms
```

Order:
```text
Stage49: DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE
Stage50: DURABLE_SCATTER -> FRONTLINE -> CLUSTER -> LINE -> LINE_REPRISE
```

Important Stage49/Stage50 distinction:

```text
Stage49 CLUSTER
= distinct-grammar burst
= GRUNT/RUNNER/GRUNT/RUNNER/BRUTE/GRUNT
= offsets 0/120/240/360/480/600 ms within phase

Stage50 CLUSTER
= DURABLE_CORE_3
= BRUTE/GRUNT/BRUTE/GRUNT/BRUTE/GRUNT
= offsets 0/360/720/1080/1440/1800 ms within phase
```

Do not apply Stage50 sustain morphology to Stage49.

Diagnostic exact run:
```text
run 40153142570
artifact 12583341810
head 5eb71a861b1226887a8ec09dce98641c0dfff817
artifact sha256 ab31640122bd1d00179d5af62104368cb46ad4e5d4137fb8922d561ebbfcacf5
fidelityErrors = []
```

Role-facing Lv31 OFF->ON diagnostic direction:
```text
Knight +43.03%
Rogue  +30.07%
Tank   +27.37% + 3 unresolved reduced
Archer +1.72%
Mage   +9.42%
```

Tank objective protection:
```text
OFF wall damage 1358
ON wall damage 164
```

Residual watch:
```text
material wall pressure appears only in Tank cases in this exact sample
```
Do not turn this into an equal-wall-damage target.

---

# Static authoring-candidate PASS — doc170

Candidate:
`legacy-game-structure/data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`

Exact static run:
```text
run      40156618986
artifact 12585015454
head     4a06adbb523dd63e0a2a5fefb31fbb2553c0e4d1
artifact sha256 ac2d233af17dd0f5415169d7daec38bfc472c3409bfe626ea756d8e986bd1676
```

Identity:
```text
candidate sha256    c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3
materialized sha256 de1b5944c560da9c0ea33f6e4dbc88bd898ee66f772a802274c96db4c711b33c
base recipe sha256  3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
```

Result:
```text
status = PASS
errors = []
warnings = []
metadataPreservedFromV02 = true
Stage49 = authored24 / max4s6 / max6s11 / y 0.18..0.82
Stage50 = authored30 / max4s6 / max6s9 / y 0.18..0.82
```

Materialization deliberately preserves v0.2/skeleton metadata. Diagnostic-probe-only metadata broadening was not promoted into authoring authority.

---

# Fidelity cautions

Mage Lv31 bridge is a semantic fidelity correction, not a numerical freeze.

Archer Lv31 `yTolerance=0.20` is diagnostic only. Do not encode 0.20 in the authoring recipe or production authority.

Settlement bridge remains required until equivalent engine correction is independently validated.

---

# Exact next bounded task

Run a **narrow exact-source Stage49-50 dynamic admission** on the materialized candidate.

The admission must prove:

```text
1. exact candidate/base/source identity;
2. materialized Stage49/50 spawn lists match the intended diagnostic center;
3. Stage46-48 remain v0.2 and provide the same persistent-state lead-in;
4. Lv31 OFF/ON use identical deterministic entry state;
5. deterministic replay PASS;
6. settlement/lifecycle continuity PASS;
7. no transient/enemy carry leakage;
8. Archer diagnostic width bridge remains diagnostic only;
9. Mage Lv31 fidelity bridge remains semantic-only;
10. five-class role-facing direction is consistent with doc169;
11. Tank objective-protection signal is retained;
12. objective-pressure skew is not materially worsened by materialization;
13. no class/monster/shop/EXP/P×P scalar mutation;
14. no production or full-T1 authoring adoption.
```

For reproduction comparison, prefer exact same seeds:
```text
101,211,307,409,503
```

If materialized data differs dynamically from the diagnostic-generated candidate, classify the mismatch before changing any encounter/scalar value.

---

# What comes after dynamic admission

If narrow dynamic admission reproduces the intended shape:
- close the Stage49-50 authoring-candidate evidence unit;
- report candidate as dynamically admitted but still **not adopted**;
- evaluate whether the residual Tank-only wall-pressure watch requires another encounter-shape iteration or is acceptable as class-specific objective-protection evidence before any wider T1 recipe authoring.

Do **not** jump directly to full Stage1-50 exact recipe freeze.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 CANDIDATE SCOPE ONLY
PRESERVE STAGE5 / STAGE18 / STAGE41
PRESERVE STAGE46-48 LEAD-IN FOR DYNAMIC ADMISSION
NO FULL-50 EXACT AUTHORING YET
NO CLASS BUFF/NERF FROM THIS SLICE
SURVIVAL != CLEAR
TANK KILL PARITY NOT REQUIRED
AUTHORED 4s DENSITY <= 8
NO MONSTER/CLASS SCALAR CHANGE
NO SHOP/EXP/P×P PROBABILITY CHANGE
NO FLAT SHOP->EXP MULTIPLIER
FINAL EXP ROUTING = P10R
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```
