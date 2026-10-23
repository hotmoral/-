# Timing Defense — P4-D2 V0.3 Replay Failure & V0.4 Runner Correction V0.1

Date: 2026-10-23 KST  
Status: **V0.3 EXACT ADMISSION FAILED / V0.4 CORRECTION PREPARED / NO GAME-RULE CHANGE / NO PRODUCTION CHANGE**

Authority / context:
- `99_P4D2_TEMPORAL_CADENCE_FIDELITY_REVIEW_V0_1.md`
- `103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`
- `../../tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py`
- `../../tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_3.py`
- `../../tools/run_p4d2_stage48_49_dynamic_grammar_probe_v0_4.py`

---

# 0. Finding

The committed v0.3 replay runner cannot be admitted because its own source-patch guard fails against the live Stage46 kernel before simulation begins.

This is a **runner implementation defect**, not a gameplay/balance defect.

No production rule changes are authorized by this document.

---

# 1. Exact defect

The Stage46 kernel contains two shield-consumption sites:

1. SIEGER shot absorption;
2. wall-contact absorption.

They use different source indentation because they occur at different nesting depths.

v0.3 instead searched for one exact source string:

```text
20-space indentation + stats["shield"] -= absorb
```

and required:

```text
count == 2
```

The live kernel has that exact indentation at the SIEGER site only.
The wall-contact site uses the shallower indentation.

Therefore:

```text
v0.3 expected count = 2
live count          = 1
-> RuntimeError before replay
```

Classification:

```text
V03_EXACT_REPLAY_ADMISSION = FAIL_SOURCE_PATCH_GUARD
```

Do not publish or freeze any v0.3 output hash.

---

# 2. v0.4 correction

`run_p4d2_stage48_49_dynamic_grammar_probe_v0_4.py` preserves all intended v0.3 semantics but patches the two shield-consumption sites independently:

```text
SIEGER-shot absorb site -> exact deeper-indentation guard, count1
wall-contact absorb site -> exact shallower-indentation guard, count1
```

Both sites clear `shieldSource` only when the shield is fully depleted.

The structural Tank barrier rule remains:

```text
active Lv31 barrier may not be downgraded by weaker Lv16 Perfect Guard
```

This is the same contract fidelity correction already established in document103.

---

# 3. Reconstruction fidelity check

A local source-equivalent reconstruction was validated before using it for new Stage49 directional work.

It reproduced the canonical v0.2 directional evidence on the previously published metrics, including:

```text
all-success endWall:
Knight 895
Rogue common 520
Rogue recovered-78ms lane 1850
Tank 2000
Archer 1575
Mage 2000
```

It also reproduced:
- canonical one-miss ranges;
- canonical two-consecutive-miss ranges;
- Rogue recovered-lane burial time range `53.1..56.375s`;
- all-finals-missed burial times:
  - Knight `28.875s`
  - Rogue `26.7s`
  - Tank `31.2s`
  - Archer `47.525s`
  - Mage `59.8s`.

Therefore the reconstruction is suitable for **directional** follow-up while exact committed-runner checkout execution remains pending.

Important boundary:
- this does **not** convert a reconstruction hash into exact committed-runner replay authority;
- exact v0.4 one-command execution remains required before regression/freeze use.

---

# 4. Governance impact

Supersession:

```text
v0.2 = historical pre-Tank-barrier-correction result
v0.3 = failed replay runner; do not admit
v0.4 = current prepared fidelity runner
```

No need to reopen:
- user-approved Lv31 identities;
- durable-pressure direction;
- Rogue cadence correction;
- Archer wider-corridor approval.

Next work may continue using v0.4 semantics directionally, but numerical freeze remains prohibited.
