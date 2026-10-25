# Timing Defense — Next Work Boundary

Updated: 2026-10-25 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_54.yaml`;
5. read `177_T1_WIDER_EXACT_AUTHORING_WAVE_A2_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
6. inspect `legacy-game-structure/data/t1_wider_exact_authoring_wave_a2_candidate_v0_1.yaml`;
7. read `176_T1_WIDER_EXACT_AUTHORING_WAVE_A1_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md` only as needed;
8. read `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md` and inspect `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`;
9. preserve user-approved Stage49-50 baseline under doc174 and evidence 169-173;
10. preserve representative v0.2/base runner evidence only as needed;
11. verify production/harness live heads.

Do not rerun closed Stage49-50 diagnostics, Wave A plan preflight, A1 static preflight, or A2 static preflight without a concrete trigger.

---

# Current phase

```text
Stage49-50 structural authoring baseline = USER APPROVED WITH WATCHES
Wider T1 Wave A plan = STATIC PREFLIGHT PASS
A1 Stage1/4/8 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A2 Stage15/19 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A3 Stage24/25/29/30/31 = NOT STARTED / NEXT
A4 Stage33/37/38 = NOT STARTED
full 50-Stage exact recipe freeze = DEFERRED
Timing Defense production gameplay semantics = UNCHANGED / UNAUTHORIZED
CURRENT = WAVE A3 EXACT SPAWN RECIPE MATERIALIZATION GATE
```

---

# Closed Wave A evidence

## A1
Candidate:
`legacy-game-structure/data/t1_wider_exact_authoring_wave_a1_candidate_v0_1.yaml`

```text
run 40193818274
artifact 12599510840
PASS / errors=[] / warnings=[]
Stage1 max4=3
Stage4 max4=6
Stage8 max4=6
```

A1 remains candidate-only / not adopted / no dynamic execution.

## A2
Candidate:
`legacy-game-structure/data/t1_wider_exact_authoring_wave_a2_candidate_v0_1.yaml`

```text
run 40200875375
artifact 12601174423
head ff240f4859fce0e993406b6253fe9edb3ba6631e
PASS / errors=[] / warnings=[]
Stage15 = BRUTE3 / max4=2
Stage19 = BRUTE2+RUNNER4 / max4=5
Stage18 preserved=true
Stage20 preserved=true
```

Local progression:
```text
Stage15 pure BRUTE teach
-> Stage18 G+B first mix
-> Stage19 B+R stagger/reorder
-> Stage20 G+R+B synthesis
```

A2 remains candidate-only / not adopted / no dynamic execution.

The same A2 source commit triggered an unrelated Cloudflare harness build check failure; the GitHub Actions A2 preflight itself passed. Treat external Cloudflare build state separately.

---

# Important lifecycle constraint

Do not run noncontiguous Wave A stages as a persistent-state sequence.
A static slice passing does not authorize fake chains that skip un-authored stages.

Dynamic work is deferred until:
- contiguous authored context exists; or
- a separate standalone diagnostic contract is explicitly authorized and labeled non-persistent.

---

# Exact next bounded task — A3

Materialize only:
```text
Stage24
E01 / G / F03 / CD04 / C1 / BASELINE,FLOOD
purpose = GRUNT baseline high-pressure / density

Stage25
E01 / G / F04 / CD01 / C0 / BASELINE
purpose = Lv21 first-time reward buffer / recovery

Stage29
E02+E03 / G+R+B / F08 / CD05 / C2 / RUSH,BULWARK
purpose = late/limited split-axis synthesis

Stage30
E01+E03 / G+B / F01 / CD03 / C1 / BASELINE
purpose = Checkpoint B mid synthesis / optional boss-preview slot only

Stage31
E03 / G+B / F02 / CD04 / C1 / BULWARK
purpose = first Pressure/Soft-Wall focused durable pressure
```

A3 has no separately declared Wave A context-only anchor stages, so the gate must preserve:
- the exact skeleton signatures above;
- every existing representative recipe object;
- A1 and A2 candidates untouched;
- Stage39/40/41 and approved Stage49/50 authority untouched.

A3 authoring must check:
- only GRUNT/RUNNER/BRUTE legal;
- Stage25 remains a genuine recovery/buffer relative to Stage24 and Stage29;
- Stage29 F08 remains clear split-axis, not visual clutter or midfield pop-in;
- Stage30 is a checkpoint synthesis without a new mandatory mechanic;
- Stage31 enters soft-wall pressure via known G+B durable grammar, not a scalar jump;
- exact skeleton formation/cadence/complexity/pressure preserved;
- right-edge entry `x=0.92` only;
- authored 4s density <= 8;
- no monster/class scalar mutation;
- no shop/EXP/P×P mutation;
- no production change;
- run A3 static recipe gate immediately after materialization;
- do not start A4 before A3 static PASS.

If A3 static gate fails, classify validator/source/structure cause before changing encounter content.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 BASELINE USER APPROVED WITH WATCHES
A1 STATIC PASS / NOT ADOPTED
A2 STATIC PASS / NOT ADOPTED
A3 NEXT / A4 HOLD
STATIC GATE BEFORE NEXT SLICE
NO FAKE NONCONTIGUOUS PERSISTENT DYNAMIC CHAIN
NO FULL-50 EXACT AUTHORING YET
AUTHORED 4s DENSITY <= 8
NO CLASS OR MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```