# Timing Defense — Next Work Boundary

Updated: 2026-10-25 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_55.yaml`;
5. read `178_T1_WIDER_EXACT_AUTHORING_WAVE_A3_MATERIALIZATION_AND_STATIC_PREFLIGHT_V0_1.md`;
6. inspect `legacy-game-structure/data/t1_wider_exact_authoring_wave_a3_candidate_v0_1.yaml`;
7. read docs177/176 and A2/A1 candidates only as needed for prior-slice preservation;
8. read `175_T1_WIDER_EXACT_AUTHORING_WAVE_A_PLAN_AND_STATIC_PREFLIGHT_V0_1.md` and inspect `data/t1_wider_exact_authoring_wave_a_plan_v0_1.yaml`;
9. preserve user-approved Stage49-50 baseline under doc174 and evidence 169-173;
10. preserve representative v0.2/base runner evidence only as needed;
11. verify production/harness live heads.

Do not rerun closed Stage49-50 diagnostics, Wave A plan preflight, or A1/A2/A3 static gates without a concrete trigger.

---

# Current phase

```text
Stage49-50 structural authoring baseline = USER APPROVED WITH WATCHES
Wider T1 Wave A plan = STATIC PREFLIGHT PASS
A1 Stage1/4/8 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A2 Stage15/19 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A3 Stage24/25/29/30/31 = MATERIALIZED / STATIC PASS / NOT ADOPTED
A4 Stage33/37/38 = NOT STARTED / NEXT
full 50-Stage exact recipe freeze = DEFERRED
production gameplay semantics = UNCHANGED / UNAUTHORIZED
CURRENT = WAVE A4 EXACT SPAWN RECIPE MATERIALIZATION GATE
```

---

# Closed Wave A evidence

## A1
```text
candidate SHA256 44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d
run 40193818274 / artifact 12599510840
PASS / errors=[] / warnings=[]
```

## A2
```text
candidate SHA256 2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d
run 40200875375 / artifact 12601174423
PASS / errors=[] / warnings=[]
Stage18/20 preserved=true
```

## A3
```text
candidate SHA256 30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6
run 40205404257 / artifact 12603138180
head 2eb99491bb555e2f15ddc2dbe94429db31abebf7
PASS / errors=[] / warnings=[]
accumulated materialized SHA256 a401d619151681befeac38a1b15d0b56c4b9ae2162901eede60e77a737a6bd69
base/A1/A2 preserved=true
```

A3 static facts:
```text
Stage24 G8 / max4=8 / F03 cluster burst
Stage25 G4 / max4=3 / F04 recovery scatter
Stage29 G3+R3+B3 / max4=6 / F08 split axes
Stage30 G5+B2 / max4=6 / F01 checkpoint waves
Stage31 G6+B2 / max4=8 / F02 durable-front burst
```

First A3 run `40205234927` failed only because validator counted distinct small Y jitter values as geometry complexity. Stage31 actual ySpan was `0.06`. Validator was corrected to use axis width; candidate data did not change.

A1/A2/A3 remain candidate evidence only: no content adoption, dynamic execution, numerical freeze, or production mutation.

---

# Important lifecycle constraint

Do not run noncontiguous Wave A stages as a persistent-state sequence. Static PASS does not authorize fake lifecycle chains that skip real stages.

Dynamic work remains deferred until:
- contiguous authored context exists; or
- a separate standalone diagnostic contract is explicitly authorized and labeled non-persistent.

---

# Exact next bounded task — A4

Materialize only:
```text
Stage33
E01 / G / F03 / CD04 / C2 / BASELINE,FLOOD
purpose = density pressure / Mage expression

Stage37
E02 / G+R / F08 / CD04 / C2 / RUSH
purpose = bounded split-axis tempo

Stage38
E01+E03 / G+B / F02 / CD03 / C1 / BULWARK
purpose = mixed durable focused challenge / bridge into Stage39
```

Exact context anchors that must remain unchanged:
```text
Stage39 = E02+E03 / R+B / F08 / CD05 / C3 / RUSH,BULWARK
Stage40 = SYNTH G+R+B / F01+F03 / CD03 / C2 / BASELINE
```

A4 static gate must verify:
- only GRUNT/RUNNER/BRUTE legal;
- Stage33 is materially density-oriented F03/CD04 without new monster grammar;
- Stage37 uses bounded F08 split-axis tempo, distinct from Stage29 three-type synthesis and simpler than Stage39 C3 peak;
- Stage38 uses known G+B durable grammar and forms a readable bridge into Stage39 rather than duplicating its F08 peak;
- Stage39/40 exact anchors preserved;
- A1/A2/A3 exact candidate SHA identities preserved;
- all existing representative recipes unchanged;
- exact skeleton formation/cadence/complexity/pressure preserved;
- right-edge `x=0.92`, no midfield pop-in;
- authored 4s density <= 8;
- no scalar/shop/EXP/P×P/production mutation;
- run A4 static gate immediately after materialization.

If A4 static gate fails, classify validator/source/structure cause before changing encounter content.

After A4 PASS, do **not** automatically fill all remaining T1 stages. First close the full Wave A static group and decide the next bounded authoring/dynamic boundary from canonical evidence.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 BASELINE USER APPROVED WITH WATCHES
A1/A2/A3 STATIC PASS / NOT ADOPTED
A4 NEXT
STATIC GATE BEFORE NEW BOUNDARY
NO FAKE NONCONTIGUOUS PERSISTENT DYNAMIC CHAIN
NO FULL-50 EXACT AUTHORING YET
AUTHORED 4s DENSITY <= 8
NO CLASS OR MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```