# Timing Defense — Next Work Boundary

Updated: 2026-10-25 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_53.yaml`;
5. read `176_T1_WIDER_EXACT_AUTHORING_WAVE_A1_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
6. inspect `legacy-game-structure/data/t1_wider_exact_authoring_wave_a1_candidate_v0_1.yaml`;
7. read `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md` and inspect `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`;
8. preserve user-approved Stage49-50 baseline under doc174 and its evidence 169-173;
9. preserve representative v0.2/base runner evidence only as needed;
10. verify production/harness live heads.

Do not rerun closed Stage49-50 diagnostics, Wave A plan preflight, or A1 static preflight without a concrete trigger.

---

# Current phase

```text
Stage49-50 structural authoring baseline = USER APPROVED WITH WATCHES
Wider T1 Wave A plan = STATIC PREFLIGHT PASS
A1 Stage1/4/8 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A2 Stage15/19 = NOT STARTED / NEXT
A3 = NOT STARTED
A4 = NOT STARTED
full 50-Stage exact recipe freeze = DEFERRED
production gameplay semantics = UNCHANGED / UNAUTHORIZED
CURRENT = WAVE A2 EXACT SPAWN RECIPE MATERIALIZATION GATE
```

---

# Wave A plan

```text
A1 = [1,4,8]
A2 = [15,19]
A3 = [24,25,29,30,31]
A4 = [33,37,38]
```

Context-only anchors:
```text
5,18,20,39,40,41,49,50
```

Rule:
```text
one slice materialized
-> static recipe gate
-> only then next slice
```

No full-T1 fill in this phase.

---

# A1 closed static evidence

Candidate:
`legacy-game-structure/data/t1_wider_exact_authoring_wave_a1_candidate_v0_1.yaml`

SHA256:
`44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d`

Recipes:
```text
Stage1
E01 / G / F01 / CD01 / C0 / BASELINE
G @ 0,1600,3200,4800ms / y0.46

Stage4
E01 / G / F01 / CD03 / C0 / BASELINE
G @ 0,250,500 and 2800,3050,3300ms / y0.46

Stage8
E02 / G+R / F01 / CD03 / C1 / RUSH
G,R @ 0,250
G,R @ 1700,1950
G,R @ 3400,3650
R @ 5100
all y0.46
```

Stage5 RUNNER teach is unchanged exact context.

Final static evidence:
```text
run      40193818274
artifact 12599510840
head     44793b082481df5bbff64eea383ed3240166dee4
artifact sha256 231e3b97d32baa158eff069f4897ae889cb280e5aa0aa591d1a11cd7040b141a
status PASS
errors=[]
warnings=[]
```

```text
Stage1 max4=3
Stage4 max4=6
Stage8 max4=6
existing representative stages preserved=true
Stage5 preserved=true
```

The earlier run `40193721046` is classified `VALIDATOR_MISUSE_NO_CANDIDATE_CONTENT_FAILURE`; candidate data did not change before the green rerun.

A1 is still **candidate evidence**, not accepted/frozen content.

---

# Important lifecycle constraint

Do not run `[1,4,5,8]` as a persistent-state sequential dynamic chain.
It skips Stages2/3/6/7 and would not represent the real Tier lifecycle.

Dynamic execution is deferred until either:
- contiguous authored context exists; or
- a separate standalone diagnostic contract is explicitly authorized and does not pretend to be persistent-run evidence.

---

# Exact next bounded task — A2

Materialize only:
```text
Stage15
E03 / B / F01 / CD01 / C1 / BULWARK
purpose = BRUTE first teach

Stage19
E03+E02 / B+R / F02 / CD05 / C2 / BULWARK
purpose = first target-order/stagger contrast before Stage20 gate
```

Context anchors that must remain unchanged:
```text
Stage18 = first G+B mixed / Lv16 collision watch
Stage20 = Star Gate A synthesis
```

A2 authoring must check:
- only GRUNT/RUNNER/BRUTE legal;
- Stage15 BRUTE-only teach remains readable;
- Stage19 uses already-taught B+R and does not introduce a new core grammar;
- F01/CD01 Stage15 and F02/CD05 Stage19 remain exact skeleton metadata;
- right-edge entry `x=0.92` only;
- no midfield pop-in;
- authored 4s density <= 8;
- no monster/class scalar mutation;
- no shop/EXP/P×P mutation;
- no production change;
- Stage18/20 exact anchor preservation;
- run A2 static recipe gate immediately after materialization;
- do not start A3 before A2 static PASS.

If A2 static gate fails, classify validator/source/structure cause before changing encounter content.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 BASELINE USER APPROVED WITH WATCHES
A1 STATIC PASS / NOT ADOPTED
A2 NEXT / A3-A4 HOLD
STATIC GATE BEFORE NEXT SLICE
NO FAKE NONCONTIGUOUS PERSISTENT DYNAMIC CHAIN
NO FULL-50 EXACT AUTHORING YET
AUTHORED 4s DENSITY <= 8
NO CLASS OR MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```
