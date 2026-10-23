# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Always fetch live remote first. Do not reconstruct current state from chat, memory or copied SHA alone.

Read/check in this order:
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CHARACTER_PROFILE_RADAR_V1.md`
5. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. `legacy-game-structure/data/system_dependency_calibration_order_v0_28.yaml`
7. `legacy-game-structure/136_P5_IDENTITY_AWARE_STAGE46_49_INTEGRATED_RUNNER_PREFLIGHT_V0_1.md`
8. `legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json`
9. `tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py`
10. `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
11. `legacy-game-structure/132_P5_TANK_CONTROL_CLEAR_PARETO_DIRECTION_V0_1.md`
12. `legacy-game-structure/133_P5_ROGUE_DAGGER_STORM_BROAD_CLEANUP_BREAKPOINT_V0_1.md`
13. `legacy-game-structure/134_P5_KNIGHT_PENETRATION_ROBUST_IDENTITY_PROBE_V0_1.md`
14. `legacy-game-structure/131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
15. `legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json`
16. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
17. `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
18. `legacy-game-structure/127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
19. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
20. current production/harness heads

Live remote always wins.
Do not rerun closed P1/P2/P3/P4 or the class-identity diagnostic group wholesale because of session restart.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch exact live HEAD after recovery; never trust the handoff SHA as current truth.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged by current P5 planning work.

---

# Current exact phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 = USER_APPROVED
P5 right-edge Stage46-49 direction = PROMISING DIRECTIONAL
P5 class identity radar gate = ACTIVE
P5 class identity diagnostic group = DIRECTIONALLY CLOSED / EXACT COMMITTED REPLAY WATCH
P5 integrated Stage46-49 runner = AUTHORED / STATIC PREFLIGHT COMPLETE
P5 integrated runner checkout-exact execution = NEXT
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.
No numerical value is frozen.

---

# Stable P5 A2 truth

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP + matched current increase
ATK/CRIT/CRITDMG/KNOCK personal
FORTIFICATION/DEF purchases contribute to shared wall
six categories retained
NO_ROUTINE FULL-SHOP MAXOUT BY STAGE49
```

Working diagnostics only:

```text
full-shop Rank10 reference = 16360
spend capacity center = 50%
income source center = 70/30
cross-class ATK/FORT/DEF diagnostic magnitude = 40% legacy-relative
```

The new integrated runner uses a fixed representative late-segment shop snapshot across Stage46–49 only to isolate identity/chronology/wall-deficit behavior.
Do not reinterpret that as a frozen purchase history.

---

# Class identity authority — do not reopen without trigger

Radar:

```text
Knight  ATK4 CRIT2 AGI3 KNOCK3 PEN4 AOE2
Rogue   ATK2 CRIT5 AGI5 KNOCK1 PEN1 AOE1
Tank    ATK2 CRIT1 AGI1 KNOCK5 PEN1 AOE3
Archer  ATK3 CRIT2 AGI4 KNOCK1 PEN5 AOE2
Mage    ATK4 CRIT2 AGI2 KNOCK1 PEN1 AOE5
```

Interpretation:
- radar values are identity/readability levels, not literal hidden coefficients;
- high axes must remain real causes of success;
- low axes must remain real limitations after growth;
- `SURVIVAL != CLEAR`.

Closed directional conclusions:

```text
Knight = refined durable alignment pair supports penetration/frontline identity; no buff evidence
Rogue  = multihit/durable identity intact; broad-cleanup one-dagger breakpoint HIGH watch
Tank   = control identity intact; 0.75 battlefield-wide damage makes solo clear too fast
Archer = line dependence strongly present; prior Stage49 problem is chronology/frontmost-sensitive
Mage   = cluster/density dependence strongly present
```

Tank diagnostic range only:

```text
0.20 / 0.25 / 0.30
working center 0.25
```

Do not alter Tank knockback/slow/barrier/Iron Wall as the first repair.

Rogue active guard:

```text
ROGUE_STORM_SINGLE_DAGGER_ORDINARY_ONESHOT_NOT_ROUTINE
```

At the 40% center even `DEFENSE_HEAVY atk6` narrowly crosses fresh GRUNT HP320 with one dagger (~321.84), so the new runner measures distinct targets hit/killed per storm.
Approved deterministic retarget remains unchanged.

---

# New integrated runner assets

```text
tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py
legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json
legacy-game-structure/136_P5_IDENTITY_AWARE_STAGE46_49_INTEGRATED_RUNNER_PREFLIGHT_V0_1.md
```

Encoded contracts:

```text
physical spawnX = 0.92 only
mid-field pop-in forbidden
spawnLeadSeconds changes schedule time only
Stage46->47->48->49 wall current/max/absolute deficit carried
Tank 0.20/0.25/0.30 only; control package unchanged
Rogue distinct targets hit/killed per Dagger Storm
GRUNT/RUNNER/SHIELD fresh one-dagger breakpoint telemetry
Knight refined aligned/dispersed regression
Archer aligned-line/scatter regression
Mage cluster/distributed regression
```

---

# Source-patch fidelity correction

Existing P5 all-class shop runner v0.1/v0.2 uses:

```python
src = inspect.getsource(stage46.simulate)
```

but then attempts to replace the ATK damage line that actually lives in module-level `stage46.hit()`.
That is not a sound exact-execution patch path.

The new integrated runner does not modify the old historical artifacts.
Instead it:
- applies ATK through a guarded wrapper around the original `stage46.hit()`;
- source-patches only lines actually owned by `simulate()`;
- preserves the existing Tank Iron Wall / Lv31 barrier non-downgrade fidelity corrections;
- preserves deterministic Rogue retarget.

This runner-fidelity correction does not invalidate the earlier independent directional results.

---

# Stage-boundary model / watch

The inherited P4/P5 recipes are bounded 60-second stress windows, not exact production stage scripts.
The first integrated lane carries wall state across those windows but does not transplant living diagnostic mobs between synthetic boundaries.

Active watch:

```text
P5_STAGE_BOUNDARY_BACKLOG_DISCARD_BIAS
```

`endActive` is always retained in output.
If it is material, do not treat the resulting Stage49 reserve as an exact stage-clear reserve; raise stage-boundary/backlog fidelity before numerical freeze.

---

# Encounter direction remains

```text
ALL ENEMIES ENTER FROM NORMAL RIGHT EDGE
NO MID-FIELD POP-IN
```

Late progression direction:

```text
Stage46 = power revelation
Stage47 = transition / recovery room
Stage48 = first protected role pulse
Stage49 = stronger escorted second pulse
```

Do not resume isolated Stage49 tuning before the integrated runner is executed and interpreted.

---

# Validation completed in the latest session

Completed:
- live workspace/production/harness recovery and SHA verification;
- canonical/handoff cross-check;
- class-identity closure preserved without wholesale re-run;
- existing source-patch issue isolated;
- integrated fixture authored;
- integrated runner authored;
- local Python syntax compile of the authored runner content passed;
- new preflight doc authored;
- active dependency plan advanced to v0.28;
- production/harness unchanged.

Not claimed:

```text
checkout-exact import/run PASS
exact output hash
Tank coefficient selection
Stage46-49 numerical closure
Stage49 chronology retune
```

Current local container cannot resolve `github.com`, so a checkout-equivalent execution result must not be invented from the directional reconstruction.

---

# Exact next boundary for the next session

1. fetch live branch and confirm no relevant commit supersedes this handoff;
2. checkout-equivalent import/run `tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py`;
3. if a guarded patch fails, repair simulator fidelity only and rerun;
4. verify deterministic repeat/output;
5. review Tank 0.20/0.25/0.30 survival-vs-clear behavior across Stage46–49;
6. review Rogue distinct-target cleanup plus fresh ordinary one-shot events;
7. confirm Knight/Archer/Mage targeted regression directions;
8. inspect `endActive` at all synthetic stage boundaries and resolve backlog-bias fidelity if material;
9. only after that refine Stage49 escort/frontmost chronology;
10. later exact-admit other pending P4/P5 runners, KNOCK parity, CRIT/CRITDMG policy, real shop acquisition timing/EXP feedback, P10/P10R.

No production change is authorized.
No user decision is pending.
