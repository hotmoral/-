# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized during planning/calibration

---

# ACTIVE PHASE — P4-B LV6_TO_LV21 COMBAT FEEDBACK INTEGRATION

Completed chain:

```text
P0 Foundation
 -> all-20 / SKILLED_V2_CENTRAL closure
 -> P1 Run-State Lifecycle
 -> P2 Modifier / Attribution Pipeline
 -> P3 Persistent 10-Stage Kernel PASS
 -> P4 EXP methodology USER APPROVED
 -> P4-A Marker-Only 50-Stage Inverse Design PASS
```

Current dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_4.yaml`

Current P4 authority/evidence:
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `legacy-game-structure/data/p4a_marker_opportunity_corpus_v0_1.json`
- `legacy-game-structure/data/p4a_marker_inverse_design_summary_v0_1.json`
- `tools/run_p4a_marker_inverse_design_v0_1.py`
- `tools/validate_p4a_marker_inverse_design_v0_1.py`

---

# P4-A CLOSED FOR MARKER-ONLY SCOPE

Evidence:

```text
12 synthetic 50-Stage fixtures
× 100 deterministic player streams
= 1,200 marker-only Tier runs
```

Static corpus checks PASS.

Marker-only CENTRAL T1–T4 supports non-empty common threshold intervals for all six milestones.
Therefore Tier-specific XP multipliers are not structurally required at this layer.

First candidate anchors only:

```text
A6    130.59375
A11   251.84375
A16   389.40625
A21   562.18750
A26   747.87500
A31   987.84375
```

These are P4-B starting points, not frozen EXP requirements.

Important P4-A lesson:
- the initial Lv16/Lv21 mismatch was corrected by bounded encounter-opportunity redistribution in T2/T4 rather than hidden EXP correction;
- EXP must not homogenize Tier encounter identity;
- LOW/HIGH opportunity stress envelopes remain intentionally wider than target milestone windows.

---

# EXACT NEXT TASK — P4-B

Goal:
measure the feedback loop:

```text
skill unlock
 -> class power / control change
 -> kill speed / target availability change
 -> completed local timing-turn count changes
 -> later XP accumulation changes
 -> later skill reach shifts
```

P4-B permitted simulation authority:

## Lv6
Use current authoritative mechanics.

## Lv11 / Lv16 / Lv21
Use exact v0.16 mechanics as **simulation-only parity candidates**.
This does not promote their values into production authority.

## Lv26 / Lv31
Power remains OFF.
They remain reach markers only until their separate P4-C/P4-D user gates.

---

# P4-B required outputs

At minimum measure by class/Tier:
- P25/P50/P75/P90 unlock Stage for Lv6/11/16/21/26/31;
- completed local timing-turn counts before/after each unlock;
- change from P4-A marker-only opportunity;
- class-specific kill-speed / opportunity shift;
- pre/post unlock power slope;
- whether the six universal milestone-anchor intervals remain jointly feasible;
- if not, which class/Tier/milestone causes the conflict;
- whether the cause is encounter workload distribution or skill power.

Use paired deterministic seeds wherever comparisons are made.

---

# P4-B decision discipline

If P4-B exposes divergence, do NOT automatically add class/Tier XP multipliers.

Inspect in this order:
1. exact skill mechanic / simulation parity correctness;
2. encounter opportunity and Tier identity;
3. whether gameplay-natural Stage adjustments could solve the problem without homogenization;
4. whether candidate anchor refit alone is sufficient;
5. only if structural failure remains, prepare a new stabilizer/catch-up decision packet.

No new material correction semantics may be silently introduced.

---

# Do not yet

- modify/deploy production v0.45 gameplay
- freeze the P4-A midpoint anchors
- freeze player-visible EXP numbers
- promote Lv11–21 parity candidates to production authority
- invent Lv26/Lv31 power proxies
- add hidden class-specific or Tier-specific EXP multipliers
- freeze tail percentile gates
- freeze shop/Base HP/permanent progression/boss/multiplayer values
- author exact 200 launch Stages

After P4-B evidence, the next unresolved material gate is **P4-C Lv26 simulation contract**.
