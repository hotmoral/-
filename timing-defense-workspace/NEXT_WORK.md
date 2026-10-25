# Timing Defense — Next Work Boundary

Updated: 2026-10-25 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_52.yaml`;
5. read `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md`;
6. read `174_T1_STAGE49_50_STRUCTURAL_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`;
7. inspect `legacy-game-structure/data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`;
8. inspect approved Stage49-50 candidate `legacy-game-structure/data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml` only as needed;
9. preserve docs169-173 and representative v0.2 evidence without rerunning unless a concrete trigger appears;
10. preserve runner fidelity bridges and T1 skeleton/P6 authority;
11. verify production/harness heads.

Do not rerun closed Stage49-50 diagnostics or the completed Wave A plan preflight without a concrete trigger.

---

# Current phase

```text
T1 Stage1-50 signature skeleton = STATIC PASS_WITH_WATCHES
Stage49-50 structural authoring baseline = USER APPROVED WITH WATCHES
Stage49-50 exact evidence chain = CLOSED WITH WATCHES
Wider T1 Wave A plan = STATIC PREFLIGHT PASS
CURRENT = WAVE A EXACT SPAWN RECIPE MATERIALIZATION DECISION GATE
Wave A recipes materialized = NO
full 50-Stage exact recipe freeze = DEFERRED
production = UNCHANGED / UNAUTHORIZED
```

---

# Approved Stage49-50 baseline

Path:
`legacy-game-structure/data/t1_stage49_50_stagger1800_authoring_candidate_v0_1.yaml`

SHA256:
`c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3`

Approval source:
`174_T1_STAGE49_50_STRUCTURAL_AUTHORING_BASELINE_USER_APPROVED_V0_1.md`

This is structural authoring authority only. Numerical and production boundaries remain unfrozen.

---

# Wave A bounded plan

Plan:
`legacy-game-structure/data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`

Plan SHA256:
`da383188a61f0488769b87e5767286ece7840d15262ebb07ed8c449173a6b806`

New target stages:
```text
1,4,8,
15,19,
24,25,29,30,31,
33,37,38
```

Context-only stages:
```text
5,18,20,39,40,41,49,50
```

Slices:
```text
A1 = [1,4,8]
A2 = [15,19]
A3 = [24,25,29,30,31]
A4 = [33,37,38]
```

Purpose is to bridge high-risk structural transitions before any broad full-50 authoring fill.

---

# Wave A static preflight

Final exact run:
```text
run      40189296422
artifact 12597413342
head     a2817325b87fe4796d7f3c10c860835e30513df0
artifact sha256 d7a18825573c798484995d4ce107ff5d161365c1ad4e4bb5f134bee861d28643
status   PASS
errors   []
warnings []
```

Exact identities:
```text
skeleton = 4bc8af12324cee744f1bcb55e3261f41012e741c97fbcdbd8f5dadd6a297bf4c
representative v0.2 = 3b42c207a662e91ccf90d4fc0cc31950e6330453c7ba74d214760649409f65bf
adopted Stage49-50 = c1bd5f45fb3cbdff6efa45b90f34e20bbc303a94d089564abf62523e15425bc3
```

All target signatures match the skeleton.
All selected semantic guards passed.
No target overlaps existing representative authored stages.

The earlier failed runs were caused by a validator schema assumption (`recipes` vs `stageOverrides`), not a plan contradiction. The validator was minimally fixed and the exact rerun passed.

---

# Current decision required

Recommended:
```text
MATERIALIZE WAVE A EXACT SPAWN RECIPE CANDIDATES SLICE-BY-SLICE
```

If approved, execute only A1 first:
```text
Stages 1,4,8
```

Then immediately run a static recipe gate before any A2 authoring.

A1 authoring guards:
- exact skeleton signature/formation/cadence/complexity/pressure must be preserved;
- Stage5 remains unchanged as the RUNNER-teach context anchor;
- Stage8 remains the first G+R mixed bridge;
- only GRUNT/RUNNER legal for A1;
- right-edge entry only, no midfield pop-in;
- authored 4s density <= 8;
- no monster/class/shop/EXP/P×P scalar mutation;
- no production change;
- no dynamic execution until A1 static gate passes.

If A1 static gate fails, classify source/schema/structure cause before changing any gameplay value.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 BASELINE USER APPROVED WITH WATCHES
WAVE A PLAN ONLY / 13 NEW TARGETS
SLICE-BY-SLICE MATERIALIZATION
A1 BEFORE A2 BEFORE A3 BEFORE A4
STATIC GATE BEFORE NEXT SLICE
NO FULL-50 EXACT AUTHORING YET
NO CLASS BUFF/NERF FROM THIS WORK
SURVIVAL != CLEAR
TANK KILL PARITY NOT REQUIRED
AUTHORED 4s DENSITY <= 8
NO MONSTER/CLASS SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```
