# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory, copied SHA values or this file alone.
Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_15.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
9. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
11. `legacy-game-structure/99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
12. `legacy-game-structure/100_P4D2_STAGE48_49_CADENCE_CORRECTED_DIRECTIONAL_FEEDBACK_V0_1.md`
13. `legacy-game-structure/101_P4D2_ARMORED_DURABLE_PROXY_PRESSURE_PROBE_V0_1.md`
14. `legacy-game-structure/102_P4D2_DURABLE_TEMPORAL_PRESSURE_DIRECTIONAL_PROBE_V0_1.md`
15. `legacy-game-structure/103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`
16. `legacy-game-structure/104_P4D2_STAGE49_TANK_TIME_BUDGET_ROLE_PULSE_PREFLIGHT_V0_1.md`
17. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_3.py`
18. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_2.py` — historical pre-barrier-correction replay only
19. `legacy-game-structure/data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json`
20. `legacy-game-structure/data/p4d2_armored_durable_proxy_fixture_v0_1.json`
21. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
22. `SKILL_PLAN_LV6_31.md`
23. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
24. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
25. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
26. current production/harness heads
27. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Historical proposal90 is superseded where it conflicts with approved docs91/96, but its Tank T-B shared-barrier non-downgrade clause remains applicable unless explicitly superseded.
The armored durable proxy is diagnostic only and is not an approved new monster.
The BRUTE carrying/using SHIELD-like protection idea is parked for future monster identity/design work only.
Do not rerun closed P1/P2/P3/P4-C1/C2 solely because a session restarted.

Live remote always wins.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- exact final HEAD must be re-fetched after sync.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- current planning work did not change it.

---

# Current exact phase / boundary

```text
P4-C1 = USER_APPROVED_STRUCTURAL_COMPLETE
P4-C2 = COMPLETE / PASS_WITH_WATCHES
P4-D1 = USER_APPROVED_WITH_MODIFICATION
P4-D2 Stage46 pressure existence = CANDIDATE ENVELOPE FOUND
P4-D2 Archer wider gameplay corridor = USER APPROVED
P4-D2 cadence/no-target methodology = CORRECTED
P4-D2 durable static pressure axis = SUPPORTED
P4-D2 durable temporal direction = SUPPORTED DIRECTIONALLY
P4-D2 Tank barrier-family fidelity defect = CONFIRMED / V0.3 PREPARED
P4-D2 Stage49 Tank time-budget role module = PROMISING
P4-D2 exact v0.3 replay + full rotating grammar integration = NEXT
P4-E = BLOCKED_PENDING_P4D2
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.

---

# User-approved late-run direction

```text
Lv31 must be spectacular and class-defining
+
finite / deterministic / attributable effect graph
+
Stage46+ pressure rises enough to require/absorb Lv31 power
```

- Lv31-less intended-skilled players may be buried by real combat pressure.
- no code-level Lv31 requirement.
- combo/P×P maintenance is an intended late-game difficulty axis.

```text
41..45 acquisition/transition
46 major pressure jump
46..47 power revelation
48..49 mastery pressure
50 final application
```

---

# Current Lv31 centers — provisional only

```text
Knight  second wave1.00
Rogue   16 daggers × .45
Tank    shockwave.75 / KB×2.5 / barrier250-for-6s candidate
Archer  per-target2.30 / wider straight corridor / MID_ADJACENT diagnostic center
Mage    stages.75 / radius1.25
```

Do not silently freeze these.

---

# Mandatory methodology fidelity

## Rogue cadence

```text
recovery390ms ->312ms
exact delta=-78ms
COMMON_1P125_NO_BANK
ROGUE_RECOVERY_DELTA_78MS_NO_BANK ->1.047s sensitivity
NO_TARGET_OPPORTUNITIES_DO_NOT_BANK
```

`1.047s` is not production cadence authority.

## Tank barrier family

```text
shared non-additive barrier family
Lv31 barrier250/6s candidate
Lv16 guard80/3s
active Lv31 barrier cannot be downgraded by weaker Lv16 guard
```

Old Stage46/v0.2 runner violated this by replacing `250` with `80` on the next ordinary PERFECT.

Therefore:

```text
v0.2 Tank miss-severity = historical pre-correction evidence only
v0.3 = required class-fairness runner
```

Directional corrected examples:

```text
Distributed durable / two misses: 1584 ->1924
Strong durable role pulse: one1301->1661 / two1073->1497
Durable+SUPPORTER/SIEGER: one1226->1661 / two1092->1480
```

Exact v0.3 repository-checkout execution/hash is still pending.

---

# Durable pressure direction

`ARMORED_DURABLE_PROXY` is diagnostic only.

Current center:

```text
HP1600
armor multiplier.55
knock resistance.65
```

Class separation:

```text
Knight removes65.4%
Rogue kills one with16 daggers
Tank removes15.5% but pushes
Archer removes94.9% through armor ignore
Mage primary removes24.8%
```

Mage authoring lever:

```text
distributed durable 60s -> wall80
clustered durable 60s -> wall2000
```

Tank control ablation:

```text
control present -> wall2000 / no durable wall contacts
push removed -> wall816 /16 durable wall contacts
```

Do not convert this into extreme HP+armor+knock-resist hard countering.

---

# Stage49 Tank time-budget module

Role-specific candidate only:

```text
one durable every second pressure cycle
+
three readable SIEGER threats every second cycle
+
role pulse after initial reset
```

All-success directional wall:

```text
Knight2000
Rogue2000
Tank2000
Archer1325
Mage1850
```

Tank sustained missed-final sensitivity:

```text
2 misses1855
3 misses1785
4 misses1370
5 misses831
6 misses121
```

Interpretation:
- Tank's larger mistake budget is acceptable class identity;
- sustained failure eventually exhausts the time budget;
- Mage margin is healthier than earlier over-aggressive pulse;
- Archer off-corridor SIEGER exposure remains a geometry watch;
- this module is not the entire Stage49 recipe.

---

# Full Stage49 rotation concept

Fairness comes from complementary grammar rotation, not identical class taxes.

```text
durable/SIEGER time-budget pulse -> Tank/Mage/Archer pressure
frontline/breach -> Knight pressure
persistent durable allocation -> Rogue storm allocation
cluster window -> Mage recovery/power expression
aligned line window -> Archer power expression
scatter/off-axis window -> geometry pressure
```

Rotate Archer-aligned and off-axis SIEGER pulses.
Do not make off-corridor punishment constant.

---

# Archer watch

`LV31_ARCHER_SUCCESS_MONOTONICITY_CHRONOLOGY_WATCH = HIGH`.

Inspect:
1. SPLITTER death/child timing;
2. target/band order;
3. capability exposure;
4. encounter ordering;
5. only then skill numbers.

Do not reverse approved wider corridor from current evidence.

---

# Exact next work

1. execute `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_3.py` in repo checkout;
2. establish exact v0.3 replay hash;
3. supersede v0.2 Tank class-fairness values;
4. integrate the Tank time-budget module into the full Stage49 rotating diagnostic grammar;
5. alternate Archer-aligned/off-axis role geometry;
6. preserve Mage cluster-recovery windows;
7. ensure complementary grammars still create Knight/Rogue late mastery pressure;
8. continue Archer chronology investigation;
9. reassess P4-D2 provisional closure with explicit watches.

No user decision is pending unless a material class-identity or monster-identity change appears.

---

# Do not yet

- promote durable proxy or BRUTE+SHIELD visual idea to an actual monster;
- freeze proxy HP/armor/knock values;
- freeze exact role-module count/cadence/geometry;
- freeze Rogue16 daggers;
- freeze Archer2.30 or exact corridor width;
- freeze Stage48–49 mistake budgets;
- freeze Stage46 possession at97/98/99%;
- change/deploy production gameplay;
- freeze final EXP;
- start P5 before P4-E closure.
