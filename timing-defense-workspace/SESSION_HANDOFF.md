# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Always fetch live remote first. Do not reconstruct current state from chat/memory/copied SHA alone.

Read/check in this order:
1. live `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `CHARACTER_PROFILE_RADAR_V1.md`
5. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
6. `legacy-game-structure/data/system_dependency_calibration_order_v0_27.yaml`
7. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
8. `legacy-game-structure/130_P5_CLASS_IDENTITY_FINITE_PACKET_PROBE_PREFLIGHT_V0_1.md`
9. `legacy-game-structure/131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
10. `legacy-game-structure/data/p5_class_identity_radar_invariants_v0_1.yaml`
11. `legacy-game-structure/data/p5_class_identity_radar_probe_fixture_v0_1.json`
12. `tools/run_p5_class_identity_radar_probe_v0_1.py`
13. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
14. `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
15. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
16. current production/harness heads

Do not rerun closed P1/P2/P3/P4 wholesale because of session restart.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch live HEAD on recovery.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged by P5 work.

---

# Current phase

```text
P0 = PASS_WITH_WATCHES
P1 = USER_APPROVED_STRUCTURAL_COMPLETE
P2 = USER_APPROVED_STRUCTURAL_COMPLETE
P3 = STRUCTURAL_PASS_COMPLETE
P4 = PROVISIONAL_STRUCTURAL_COMPLETE_WITH_WATCHES
P5 A2 = USER_APPROVED
P5 right-edge Stage46-49 direction = PROMISING DIRECTIONAL
P5 radar identity gate = ACTIVE
P5 finite-packet identity runner/fixture = AUTHORED
P5 first identity result = DIRECTIONAL RECONSTRUCTION COMPLETE / EXACT COMMITTED EXECUTION PENDING
P5 = CLASS_IDENTITY_RECONVERGENCE_ACTIVE
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is pending.

---

# Class identity rule

Radar remains:

```text
Knight  4/2/3/3/4/2
Rogue   2/5/5/1/1/1
Tank    2/1/1/5/1/3
Archer  3/2/4/1/5/2
Mage    4/2/2/1/1/5
```

Axes: ATK / CRIT / AGILITY / KNOCK / PEN / AOE.
These are identity/readability levels, not literal coefficients.

Critical governance:

```text
high axes must cause visible success
low axes must remain real limitations
SURVIVAL != CLEAR
```

Tank user direction:
- solo parity is not required;
- survival/control should be excellent;
- enemy-removal throughput should be poor;
- late solo may be near-impractical or materially slower/frustrating;
- no absolute hard class lockout.

---

# First directional identity findings

Authority:
- independent deterministic reconstruction of current semantics;
- exact committed one-command runner execution still pending;
- no numerical freeze.

## Tank
Same mixed finite packet:

```text
Knight 8.079s
Rogue 7.581s
Tank 8.079s
Archer 6.953s
Mage 8.079s
non-Tank median ~7.830s
Tank ratio ~1.03x
```

This directionally confirms a negative-identity defect: Tank currently kills too quickly.

Likely root axis is current provisional Lv31 battlefield-wide damage contribution.
Approved contract requires Absolute Barrier to reset pressure through control/wall protection without becoming generic Mage-style damage.

Damage-only sensitivity while preserving control/barrier:

```text
.75 -> 8.079s
.50 -> 10.333s
.40 -> 12.575s
.35 -> 13.702s
.30 -> 14.829s
.25 -> 18.209s
.20 -> 21.578s
.15 -> 23.832s
.10 -> 29.454s
```

No value is approved. Very low damage can break current late-pressure survival, so next is a control-vs-clear Pareto search.

## Archer
Aligned line `~3.58s`; scatter `~8.08s`.
Line dependence remains strong even in ATTACK_HEAVY direction.
Old Stage49 Archer issue is localized mainly to packet/frontmost chronology.

## Mage
Cluster `~3.78s`; distributed `~8.08s`.
Density identity strongly preserved.

## Rogue
Shop ATK creates a distinct Lv31 dagger breakpoint.
At roughly 30%-legacy diagnostic scale, provisional dagger damage crosses GRUNT HP:

```text
600*.45 = 270
270*(1+.192) ~= 321.84
GRUNT HP = 320
```

Approved retargeting then lets remaining daggers serially clean weak bodies.
New HIGH watch:
`P5_ROGUE_DAGGER_GRUNT_ONESHOT_BREAKPOINT_WATCH`.
Do not remove retargeting yet.

## Knight
First pair is not robust enough because target-death/second-wave chronology becomes non-monotonic across ATK scales.
Do not change Knight yet; refine the probe.

---

# Current classifications

```text
Knight = STRUCTURALLY PLAUSIBLE / PROBE REFINEMENT REQUIRED
Rogue = CORE IDENTITY PRESENT / SHOP-DRIVEN BROAD-CLEANUP BREAKPOINT HIGH WATCH
Tank = CONTROL IDENTITY PRESENT / NEGATIVE SOLO-THROUGHPUT DEFECT DIRECTIONALLY CONFIRMED
Archer = LINE DEPENDENCE STRONGLY CONFIRMED / STAGE49 CHRONOLOGY WATCH LOCALIZED
Mage = DENSITY DEPENDENCE STRONGLY CONFIRMED
```

---

# Fixed encounter/shop boundaries

- A2 shop semantics remain approved; exact values open.
- Working diagnostics only: full-shop16360, spend50%, income70/30, effect40%.
- Cross-class shop lane = ATK/FORT/DEF.
- KNOCK and CRIT/CRITDMG deferred.
- all enemies enter normal right edge; no mid-field pop-in.
- Stage46 power revelation -> Stage47 transition -> Stage48 protected role pulse -> Stage49 escorted second pulse.
- do not resume exact Stage49 packet tuning before identity reconvergence.

---

# Exact next boundary

1. Tank control-vs-clear Pareto search preserving knock/slow/barrier while scanning lower Lv31 damage contribution;
2. measure Tank wall survival + backlog + direct clear time together;
3. Rogue distinct-target-per-storm and one-shot breakpoint scan;
4. Knight robust penetration-causality fixture refinement;
5. exact committed identity runner execution when a byte-equivalent execution lane is available;
6. integrate identity metrics into Stage46–49 source-patched right-edge runner;
7. then resume Stage49 chronology refinement;
8. later KNOCK parity, CRIT/CRITDMG, EXP/Lv feedback, P10/P10R.

No production change is authorized.
