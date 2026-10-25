# Timing Defense — Next Work Boundary

Updated: 2026-10-26 KST

## Mandatory recovery order
1. fetch live `timing-defense-workspace` HEAD;
2. read `PROJECT_STATUS.md`;
3. read `SESSION_HANDOFF.md`;
4. read active `legacy-game-structure/data/system_dependency_calibration_order_v0_56.yaml`;
5. read `179_T1_WIDER_EXACT_AUTHORING_WAVE_A4_AND_FULL_STATIC_CLOSURE_V0_1.md`;
6. inspect `data/t1_wider_exact_authoring_wave_a4_candidate_v0_1.yaml`;
7. read docs178/177/176 and A3/A2/A1 candidates only as needed;
8. preserve Wave A plan doc175/data plan;
9. preserve user-approved Stage49-50 baseline doc174 and evidence169-173;
10. verify production/harness live heads.

Do not rerun closed Stage49-50 diagnostics, Wave A plan preflight, or A1-A4 static gates without a concrete trigger.

---

# Current phase

```text
Stage49-50 structural authoring baseline = USER APPROVED WITH WATCHES
Wider T1 Wave A plan = STATIC PREFLIGHT PASS
A1 [1,4,8] = MATERIALIZED / STATIC PASS / NOT ADOPTED
A2 [15,19] = MATERIALIZED / STATIC PASS / NOT ADOPTED
A3 [24,25,29,30,31] = MATERIALIZED / STATIC PASS / NOT ADOPTED
A4 [33,37,38] = MATERIALIZED / STATIC PASS / NOT ADOPTED
Full Wave A accumulated materialization = STATIC PASS / NOT ADOPTED
full 50-Stage exact recipe freeze = DEFERRED
production gameplay semantics = UNCHANGED / UNAUTHORIZED
CURRENT = FULL WAVE A STATIC ADOPTION DECISION GATE
```

---

# Full Wave A exact static evidence

```text
A1 candidate SHA256 = 44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d
A2 candidate SHA256 = 2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d
A3 candidate SHA256 = 30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6
A4 candidate SHA256 = 93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36
full accumulated SHA256 = 28b23f1f6332785009028ae9e531912c7dc2fb54da3a3a2db1536569b743774b
```

Exact runs:
```text
A1 40193818274 / artifact 12599510840 / PASS
A2 40200875375 / artifact 12601174423 / PASS
A3 40205404257 / artifact 12603138180 / PASS
A4 40210214458 / artifact 12605184344 / PASS
```

A4 final static facts:
```text
Stage33 G12 / F03 / CD04 / max4=8 / max6=12 / ySpan=0.07
Stage37 G4+R4 / F08 / CD04 / max4=8 / two axes
Stage38 G6+B2 / F02 / CD03 / max4=7 / ySpan=0.06
Stage39 anchor authored14 / F08 / CD05 / C3 / max4=8 / ySpan=0.22
Stage40 anchor preserved
```

A4 first run `40210087895` failed only because validator used equal monster-type cardinality as a false complexity proxy for Stage38 vs Stage39. The candidate did not change; the guard was corrected and final run passed.

All representative base objects and A1-A3 candidate objects were preserved in the cumulative materialization.

---

# Important lifecycle constraint

Do **not** run A1+A2+A3+A4 targets as one persistent-state sequence. They are noncontiguous and skip real stages.

Dynamic execution remains deferred until either:
- contiguous authored context is deliberately built; or
- a separately specified non-persistent diagnostic contract is explicitly authorized.

---

# Exact next decision

User approval is now required before promoting the exact Wave A spawn candidates from evidence to authoring authority.

Decision wording:
```text
ADOPT FULL WAVE A EXACT SPAWN CANDIDATES
AS CANONICAL T1 AUTHORING BASELINE WITH WATCHES
```

If approved, the following become authoring baseline only:
- exact monster counts;
- exact spawn timestamps;
- exact Y positions;
- formation/cadence realization for the 13 Wave A target stages.

Approval does **not** mean:
- production deployment;
- class or monster scalar freeze;
- shop/EXP/P×P change;
- Archer width freeze;
- Mage Lv31 numerical freeze;
- full Stage1-50 exact recipe freeze.

After adoption, next work is **not** to fill all remaining stages blindly. First design the smallest bounded contiguous-coverage wave that can eventually support lifecycle-faithful dynamic execution.

If not approved, hold at full Wave A static PASS and revise only against concrete feedback.

---

# Fixed guards

```text
LIVE REMOTE WINS
NO REPEAT OF CLOSED WORK WITHOUT TRIGGER
STAGE49-50 BASELINE USER APPROVED WITH WATCHES
A1-A4 STATIC PASS / NOT ADOPTED
FULL WAVE A STATIC MATERIALIZATION PASS
NO FAKE NONCONTIGUOUS PERSISTENT DYNAMIC CHAIN
NO FULL-50 EXACT AUTHORING YET
AUTHORED 4s DENSITY <= 8
NO CLASS OR MONSTER SCALAR CHANGE
NO SHOP/EXP/P×P CHANGE
NO PRODUCTION GAMEPLAY CHANGE WITHOUT APPROVAL
```