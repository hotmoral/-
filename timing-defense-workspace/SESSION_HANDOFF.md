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
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_13.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
9. `legacy-game-structure/91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
10. `legacy-game-structure/95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
11. `legacy-game-structure/96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
12. `legacy-game-structure/99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
13. `legacy-game-structure/100_P4D2_STAGE48_49_CADENCE_CORRECTED_DIRECTIONAL_FEEDBACK_V0_1.md`
14. `legacy-game-structure/101_P4D2_ARMORED_DURABLE_PROXY_PRESSURE_PROBE_V0_1.md`
15. `legacy-game-structure/data/p4d2_armored_durable_proxy_fixture_v0_1.json`
16. `tools/run_p4d2_armored_durable_proxy_probe_v0_1.py`
17. `tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_2.py`
18. `legacy-game-structure/data/p4d2_stage48_49_dynamic_rotating_grammar_fixture_v0_1.json`
19. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
20. `SKILL_PLAN_LV6_31.md`
21. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
22. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
23. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
24. current production/harness heads
25. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Historical proposal90 is superseded where it conflicts with approved docs91/96.
The old Stage48 dynamic runner v0.1 is common-cadence preflight only and is not class-fairness authority.
The armored durable proxy is diagnostic only and is not an approved new monster.
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
P4-D2 Stage48–49 cadence-corrected directional feedback = COMPLETE / EXACT V0.2 REPLAY PENDING
P4-D2 armored durable pressure axis = SUPPORTED STATIC DIAGNOSTIC
P4-D2 temporal durable role-pressure probe = NEXT
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

# Cadence/no-target fidelity correction

Recovered Rogue Lv16:

```text
recovery390ms ->312ms
exact delta=-78ms
```

Diagnostic lanes:

```text
COMMON_1P125_NO_BANK
ROGUE_RECOVERY_DELTA_78MS_NO_BANK ->1.047s sensitivity
NO_TARGET_OPPORTUNITIES_DO_NOT_BANK
```

`1.047s` is not production cadence authority.
Do not treat Assassin Rhythm as blanket20% whole-cycle speed.

Cadence-corrected directional feedback:
- Rogue one isolated missed final becomes recoverable;
- two consecutive misses bury across all four tested starts;
- Tank/Mage remain much more tolerant in the current rotation;
- naive universal pressure increase is rejected as the first repair layer.

Expected exact v0.2 full-output SHA remains:

```text
63da011ac97fd809168d8ffc9c3a9721c9962a2ae3c3496aa91e0d2de0b592f8
```

Do not promote it to exact replay authority until committed-runner checkout execution matches.

---

# Armored durable pressure probe

User hypothesis: late high-HP/high-armor threats may pressure Tank/Mage without nerfing their final skills.

`ARMORED_DURABLE_PROXY` is diagnostic only.
It combines BRUTE-like HP + SHIELD-like mitigation with moderate knock resistance.

Diagnostic center:

```text
HP1600
armor multiplier.55
knock resistance.65
```

Sensitivity:

```text
HP1400/1600/1800
armor.65/.55/.50
```

Single durable, one Lv31 final:

```text
Knight removes65.4% / leaves~553
Rogue kills with16 daggers
Tank removes15.5% / leaves~1353 + pushes~.0764
Archer removes94.9% / leaves~82 due armor ignore
Mage primary removes24.8% / leaves~1204
```

Three clustered vs distributed durable reset fraction:

```text
clustered:
Knight43.6 Rogue48.8 Tank15.5 Archer63.3 Mage45.4%

distributed:
Knight21.8 Rogue48.8 Tank15.5 Archer31.6 Mage29.7%
```

Interpretation:
- durable pressure is a promising Tank/Mage late-pressure lever;
- Rogue execution identity remains strong;
- Archer armor-ignore identity remains strong while corridor geometry matters;
- Tank still has a control answer because knock resistance is not extreme;
- Mage retains clustering payoff and loses efficiency when the durable pressure is intentionally separated.

Classification:

```text
DURABLE_PRESSURE_AXIS=SUPPORTED
NEW_MONSTER_APPROVED=NO
NUMERICAL_FREEZE=NO
```

Hard-counter safeguard:
- do not stack extreme HP+armor+knock resistance;
- Tank displacement must remain valid;
- Mage needs clusterable windows;
- future actual monster/variant identity requires a separate decision/telegraph gate.

---

# Exact next work

1. build temporal durable-pressure fixture while preserving cadence/no-target corrections;
2. isolated durable after successful reset;
3. distributed durable arrivals across successive reset windows;
4. durable frontline + timed SUPPORTER/SIEGER second pulse;
5. durable frontline + CHARGER window;
6. measure Tank time bought by knockback/barrier;
7. measure Mage clustered vs separated recovery;
8. verify Knight/Rogue are not unfairly killed before Tank/Mage receive pressure;
9. keep exact Stage48 v0.2 replay and Archer chronology follow-up active;
10. reassess P4-D2 provisional closure.

No user decision is pending unless temporal durable pressure requires a material new-monster or class-identity choice.

---

# Do not yet

- promote armored durable proxy to an actual monster;
- freeze proxy HP/armor/knock values;
- freeze Rogue16 daggers;
- freeze Archer2.30 or exact corridor width;
- freeze Stage48–49 mistake budgets;
- freeze Stage46 possession at97/98/99%;
- change/deploy production gameplay;
- freeze final EXP;
- start P5 before P4-E closure.
