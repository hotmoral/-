# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_25.yaml`
- radar identity source `CHARACTER_PROFILE_RADAR_V1.md`
- class identity gate `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- machine identity contract `legacy-game-structure/data/p5_class_identity_radar_invariants_v0_1.yaml`
- A2 contract `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- all-class shop result `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- Fortification correction `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
- right-edge travel preflight `legacy-game-structure/127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
- escorted combat search `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 APPROVED / CLASS IDENTITY RADAR GATE ACTIVE / SOURCE-PATCHED RIGHT-EDGE RUNNER WITH IDENTITY METRICS NEXT**

No user decision is pending.

Working analysis centers only:

```text
Stage49 spend capacity = 50% full-shop reference
CLEAR/KILL income = 70/30
cross-class effect diagnostic center = 40% legacy-relative
```

None are production freezes.

---

# Fixed class-identity rule

The character-selection radar is now a balance guard, not just presentation.

```text
5-axis specialty -> must remain a real reason the class succeeds
1-axis weakness  -> must remain a real limitation after skill/shop growth
```

Do not turn the radar values into literal combat coefficients.

Current identity status:

```text
Knight = mostly aligned; verify penetration causality and defense-heavy viability
Rogue  = mostly aligned; verify Lv31 does not become broad wave cleanup
Tank   = control identity confirmed; solo-clear weakness not yet measured correctly
Archer = line identity present; post-shop generalist creep HIGH watch
Mage   = density identity strongly present; late-pressure margin still watched
```

Tank-specific rule from user direction:

```text
Tank solo parity is not required.
Tank should be excellent at keeping the wall alive but poor at actually finishing enemies alone.
A high-mastery Tank may eventually clear, but late solo should be near-impractical under normal tempo or materially slower/frustrating than damage classes.
No absolute hard class lockout is required.
```

Therefore `survived 60s` is not a Tank clear-pass condition.

---

# Fixed encounter-entry rule

```text
ALL ENEMIES APPEAR FROM THE NORMAL RIGHT EDGE.
NO MID-FIELD POP-IN.
```

Current Stage46–49 direction remains:

```text
Stage46: power revelation / recovery room
Stage47: transition
Stage48: first protected role pulse
Stage49: stronger escorted second pulse
```

Do not simply spawn SIEGER much earlier without escort; extra exposure can make it easier.

---

# Exact next analysis

## 1. Integrate identity metrics into the source-patched Stage46–49 runner

Runner requirements:
- every mob physically starts at normal `spawnX=0.92`;
- earlier role pressure uses schedule-only `spawnLeadSeconds`;
- wall current/max HP and damage deficit carry Stage46→49;
- preserve no-target/no-bank, Rogue cadence sensitivity, Tank barrier non-downgrade and Tank Iron Wall on SIEGER;
- current cross-class shop families remain ATK/FORT/DEF until KNOCK/CRIT policy lanes are ready.

Add outputs:

```text
stageClearTime
unfinishedAtHorizon
totalKills
totalDamage
endActiveBacklog
uniqueTargetsPerRootPackage
secondaryDamageShare
penetrationHitCount
penetrationDamageShare
controlDisplacementOrSlowTime
wallContactsPrevented
formationTag / alignmentTag / densityTag
```

## 2. Run class-identity paired probes before further Stage49 tuning

### Knight
`aligned/frontline vs dispersed/off-axis`
- confirm penetration/frontline breaking is a major reason for success;
- ensure defense-heavy Knight remains viable under successful mastery.

### Rogue
`one durable normal vs broad weak/multi-direction wave`
- confirm fast multihit/durable execution;
- detect if Lv31 retargeting turns AOE1/PEN1 into broad cleanup.

### Tank
`wall survival vs actual solo completion`
- measure clear time, unfinished rate and backlog;
- do not count survival alone as success;
- expect materially worse enemy-removal throughput than damage classes.

### Archer
`aligned line vs staggered/scatter/off-corridor`
- line alignment must materially change performance;
- attack-heavy shop must not erase geometry dependence.

### Mage
`clustered durable vs distributed durable`
- cluster payoff must remain much better;
- distributed durable must remain a real weakness.

## 3. Only after identity outputs exist, refine Stage49 packet chronology

Current HIGH watches:

```text
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH
P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH
P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH
P5_TANK_SURVIVAL_NOT_CLEAR_WATCH
P5_TANK_SOLO_CLEAR_THROUGHPUT_WATCH
P5_ROGUE_WAVE_CLEANUP_LEAKAGE_WATCH
P5_ARCHER_LINE_DEPENDENCE_WATCH
P5_MAGE_DENSITY_DEPENDENCE_WATCH
P5_KNIGHT_PENETRATION_CAUSALITY_WATCH
```

Repair order remains:
1. simulator fidelity;
2. encounter timing/geometry;
3. package semantics;
4. shop interaction;
5. scalar values last.

## 4. After class identity + right-edge pressure reconverge

Then:
- exact committed replay of pending P4/P5 runners;
- KNOCK cross-class parity/inheritance lane;
- CRIT/CRITDMG attack-template policy lane;
- purchase-policy combat feedback;
- timing-event count / EXP / Lv milestone reach feedback;
- final multiplayer normalization at P10;
- final EXP convergence at P10R.

---

# Do not yet

- treat Tank wall survival as solo-clear success;
- force all classes to equal clear time or DPS;
- implement mid-field monster spawning;
- freeze current `spawnLeadSeconds`, pressure cycles or packet compositions;
- globally nerf shop ATK;
- add hidden Archer shop penalties;
- nerf Lv31 power to solve one stress case;
- turn Rogue into a broad AoE clearer;
- remove Mage cluster/distribution asymmetry;
- make Archer formation-agnostic;
- freeze exact coin/reward/price/rank/effect values;
- modify/deploy production gameplay.

P6 remains blocked pending P5 closure.
