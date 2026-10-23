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
6. `legacy-game-structure/data/system_dependency_calibration_order_v0_27.yaml`
7. `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
8. `legacy-game-structure/132_P5_TANK_CONTROL_CLEAR_PARETO_DIRECTION_V0_1.md`
9. `legacy-game-structure/133_P5_ROGUE_DAGGER_STORM_BROAD_CLEANUP_BREAKPOINT_V0_1.md`
10. `legacy-game-structure/134_P5_KNIGHT_PENETRATION_ROBUST_IDENTITY_PROBE_V0_1.md`
11. `legacy-game-structure/131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
12. `legacy-game-structure/data/p5_class_identity_refinement_fixture_v0_1.json`
13. `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
14. `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
15. `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
16. `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
17. current production/harness heads

Live remote always wins.
Do not rerun closed P1/P2/P3/P4 or the class-identity diagnostic group wholesale because of session restart.

---

# Branch checkpoints

Planning:
- `timing-defense-workspace`
- fetch exact live HEAD after recovery.

Production:
- `timing-defense-cloudflare-do-poc`
- last verified `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- `timing-defense-skilled-v2-harness-v01`
- last verified `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- unchanged by P5 planning work.

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
P5 = ACTIVE / IDENTITY-AWARE STAGE46-49 INTEGRATION NEXT
P6 = BLOCKED_PENDING_P5
production = UNCHANGED / UNAUTHORIZED
```

No user decision is currently pending.

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

No exact numerical value is frozen.

---

# Class identity authority

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

Tank user direction:
- solo parity is not required;
- survival/control should be excellent;
- enemy-removal throughput should be poor;
- late solo may be near-impractical or materially slower/frustrating;
- no absolute hard code-level class lockout is required.

---

# Class identity group closure

## Knight

First pair was chronology-fragile, not proof of a Knight defect.
Refined five-durable-body pair changes only alignment and avoids one-shot thresholds.
Directional reference:

```text
BALANCED40: aligned 9.20s / dispersed 12.575s
DEFENSE_HEAVY40: aligned 11.45s / dispersed 12.575s
NO_SHOP: aligned 12.575s / dispersed 15.95s
```

Classification:
`DIRECTIONALLY ALIGNED / NO STRUCTURAL IDENTITY DEFECT ESTABLISHED`.

## Rogue

Core multihit/durable execution identity remains valid.
Broad-cleanup breakpoint is real when one storm dagger starts one-shotting fresh GRUNT-like bodies.
Current approximate shop-effect thresholds:

```text
BALANCED atk8     ~0.289
ATTACK_HEAVY atk9 ~0.257
ROLE_AWARE atk10  ~0.231
```

Current 0.40 diagnostic center is above them.
Active guard:
`ROGUE_STORM_SINGLE_DAGGER_ORDINARY_ONESHOT_NOT_ROUTINE`.
Do not remove approved deterministic retargeting as the first repair.

## Tank

Current provisional Lv31 shockwave damage `0.75` produces damage-class-like direct clear speed:

```text
Tank 8.079s
non-Tank median ~7.830s
ratio ~1.03x
```

This violates the intended poor solo-throughput weakness.
Preserve knockback/slow/barrier/control.
First integrated diagnostic damage range only:

```text
0.20 / 0.25 / 0.30
working center = 0.25
```

Reference finite-packet clears:

```text
0.30 -> 14.829s
0.25 -> 18.209s
0.20 -> 21.578s
```

Very low damage can create dangerous backlog; do not freeze from finite packet alone.

## Archer

Line identity strongly preserved:

```text
aligned ~3.58s
scatter ~8.08s
```

Old Stage49 attack-heavy issue is localized to packet/frontmost chronology.
No global Archer nerf.

## Mage

Density identity strongly preserved:

```text
cluster ~3.78s
distributed ~8.08s
```

No structural Mage redesign.

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

Do not resume isolated Stage49 tuning before identity-aware Stage46→49 integration.

---

# Exact next boundary for the next session

1. build an identity-aware source-patched Stage46→49 normal-right-edge runner;
2. carry wall current HP / max HP / absolute deficit across all four stages;
3. scan Tank Lv31 damage contribution `0.20 / 0.25 / 0.30` while keeping control/barrier unchanged;
4. add Rogue Dagger Storm distinct-target hit/kill count + ordinary one-shot breakpoint telemetry;
5. include Knight refined alignment, Archer line and Mage density metrics as regression guards;
6. then refine Stage49 escort/frontmost chronology without breaking class identities;
7. exact-admit pending identity/P4/P5 runners when a byte-equivalent execution lane is available;
8. later KNOCK cross-class parity, CRIT/CRITDMG attack-template policy, shop→EXP/Lv feedback, P10/P10R.

No production change is authorized.
No user decision is pending.
