# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_24.yaml`
- A2 contract `legacy-game-structure/116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- all-class shop result `legacy-game-structure/124_P5_ALL_CLASS_FIXED_RANK_SHOP_COMBAT_PREFLIGHT_V0_1.md`
- Fortification correction `legacy-game-structure/125_P5_FORTIFICATION_DAMAGE_DEFICIT_INVARIANCE_CORRECTION_V0_1.md`
- old spatial proof `legacy-game-structure/126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md`
- right-edge travel preflight `legacy-game-structure/127_P5_STAGE46_49_RIGHT_EDGE_TRAVEL_LEAD_PREFLIGHT_V0_1.md`
- escorted combat search `legacy-game-structure/128_P5_STAGE46_49_RIGHT_EDGE_ESCORTED_TRAVEL_COMBAT_SEARCH_V0_1.md`
- right-edge lead fixture `legacy-game-structure/data/p5_stage46_49_right_edge_lead_fixture_v0_1.json`
- escorted direction fixture `legacy-game-structure/data/p5_stage46_49_right_edge_escorted_direction_fixture_v0_1.json`

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 APPROVED / RIGHT-EDGE ESCORTED LATE-PRESSURE DIRECTION PROMISING / PACKET CHRONOLOGY REFINEMENT NEXT**

No user decision is pending.

Working analysis centers only:

```text
Stage49 spend capacity = 50% full-shop reference
CLEAR/KILL income = 70/30
cross-class effect diagnostic center = 40% legacy-relative
```

None are production freezes.

---

# Fixed implementation-facing rule

The prior Stage49 `spawnX=.48/.65` work was a spatial diagnostic only.

Actual game direction:

```text
ALL ENEMIES APPEAR FROM THE NORMAL RIGHT EDGE.
NO MID-FIELD POP-IN.
```

Difficulty may use:
- earlier schedule time;
- frontmost escort/protection;
- band/line relationship;
- overlapping first/second role pulses.

Do not implement the old spatial proxy as teleporting/mid-field spawn.

---

# Current Stage46–49 direction

```text
Stage46: power revelation; keep recovery room
Stage47: transition; still relatively forgiving
Stage48: first protected role pulse
Stage49: stronger escorted second pulse
```

First directional cadence search:

```text
46 ~5.8s
47 ~5.3s
48 ~4.9s
49 ~4.6s
```

These are not launch values.

Travel-lead kinematic reference only:

```text
old SIEGER x.48 ~= 9.78s travel from x.92
old durable x.65 = 6.75s travel from x.92
```

But a naked SIEGER must NOT simply be spawned 9–10s early; it gets extra ordinary attacks and often becomes easier.

---

# Exact next analysis

## 1. Source-patched normal-right-edge runner

Build a runner that:
- creates every mob at the normal `spawnX=0.92`;
- represents earlier role entry using `spawnLeadSeconds` / schedule time only;
- uses a warmup/reference offset rather than negative-time fake spawns;
- carries current wall HP across Stage46→49;
- preserves no-target/no-bank, Rogue cadence sensitivity, Tank barrier non-downgrade and Tank Iron Wall on SIEGER;
- keeps ATK/FORT/DEF as the current cross-class shop lane.

## 2. Refine Stage49 packet chronology

Current HIGH watches:

```text
P5_ATK_HEAVY_ARCHER_REPEATED_FAILURE_MARGIN_WATCH
P5_DEFENSE_HEAVY_KNIGHT_OVERPRESSURE_WATCH
P5_RIGHT_EDGE_ESCORT_PACKET_CHRONOLOGY_WATCH
```

Goal:
- attack-heavy Archer must not repeatedly miss finals and still enter Stage50 healthy;
- fixing Archer must not make defense-heavy Knight a trap build during successful mastery.

Repair order:
1. relative timing;
2. frontmost escort composition;
3. band/line alignment;
4. second-pulse spacing;
5. durability sensitivity;
6. player/shop coefficient changes last.

## 3. Admission behavior

Target shape:

```text
all-success -> all classes/build directions survive and feel powerful
one miss -> recoverable
two misses -> recoverable in Stage46-47; Stage48-49 may be harsher but readable
repeated failure -> severe carried wall loss or burial before/at Stage50
```

Identical mistake budgets are not required.

## 4. After right-edge pressure reconverges

Then:
- exact committed replay of current pending P4/P5 runners;
- ATK/DEF acquisition timing + inherited wall deficit;
- KNOCK cross-class parity/inheritance lane;
- CRIT/CRITDMG attack-template policy lane;
- shop feedback into timing action count / EXP / Lv milestone reach.

Final multiplayer normalization remains P10; final EXP convergence remains P10R.

---

# Do not yet

- implement mid-field monster spawning;
- freeze current `spawnLeadSeconds`, pressure cycles or packet compositions;
- globally nerf shop ATK;
- add hidden Archer shop penalties;
- nerf Lv31 power to solve this stress case;
- blanket-inflate SIEGER/FLYER HP;
- freeze 50% spend capacity, 70/30 income or 40% effect scale;
- freeze exact coin/reward/price/rank/effect values;
- solve final multiplayer before P10;
- freeze final EXP before P10R;
- modify/deploy production gameplay.

P6 remains blocked pending P5 closure.
