# Timing Defense — Simulation & Calibration Plan V0.2

Date: 2026-10-22 KST  
Status: **PRE-IMPLEMENTATION ANALYSIS PLAN / MODEL A LAYER-0 PASSED**

## 1. 목적

Production 승격 전 campaign을 여러 층으로 나눠 deterministic하게 검증한다.

Current top input:
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `data/model_a_campaign_spine_v0_1.yaml`

Pipeline:
```text
Master Spine
 -> Layer-0 structural validator
 -> encounter authoring envelope
 -> Layer-A micro sim
 -> synthetic Tier slices
 -> full Tier sim
 -> class soft-wall map
 -> stars/meta recovery
 -> achievement bridges
 -> account sim
 -> multiplayer expansion
 -> report
 -> explicit freeze
 -> live implementation
```

---

# 2. Layer-0 — Campaign Spine validation

Current status:
**PASS**

Evidence:
`30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`

Result:
```text
errors=0 warnings=0
```

Validated structurally:
- 4-Tier Model A candidate
- cumulative roster
- future expansion open
- skill window ordering
- Lv31 Stage41–45
- late-band ordering
- star contract
- boss preview policy
- pressure-attribution spacing

Layer-0 PASS does not freeze production values.

---

# 3. Layer A0 — Encounter authoring-envelope static validation

Before combat simulation, generate Tier-specific candidate envelopes.

Inputs:
- Tier monster availability
- E01–E20 archetype requirements
- pressure envelope
- complexity envelope
- formation vocabulary
- cadence vocabulary
- skill reach windows

Outputs:
- valid archetypes by Tier
- invalid/unavailable archetypes by Tier
- candidate occurrence ranges
- formation/cadence availability
- representative recipe set
- authored/effective entity bounds
- static 4s/6s density warnings

No production HP/speed freeze required.

---

# 4. Layer A — Encounter micro simulation

Purpose:
한 encounter가 실제 frontmost targeting에서 어떤 문제를 만드는지 확인.

Inputs:
- composition
- formation
- spawn order
- cadence
- candidate movement/capability values
- class/skill state

Metrics:
- frontline block time
- target reorder count
- backline exposure
- peak active
- authored/effective entity count
- 4s/6s density
- kill order
- wall pressure
- class opportunity

Special:
- SUPPORTER aura uptime / screened uptime
- SIEGER shot count / screened firing uptime
- CHARGER windup/complete/interrupt
- SPLITTER children / active/frontline occupancy
- FLYER geometry exposure

---

# 5. Layer B — Stage simulation

Inputs:
- Stage encounter sequence
- run level/EXP
- shop upgrades
- class
- mastery profile
- team size
- meta-power state

Outputs:
- clear/fail
- clear time
- wall/base HP
- damage/kills
- EXP/level
- skill reach
- coin/spend capacity
- actual monster frequency
- peak active
- 4s/6s density
- capability uptime

---

# 6. Layer C — 50 Stage Tier simulation

Required outputs:
- fail histogram by Stage
- 0★ / 1★ / 2★ / 3★ distribution
- full-Tier clear probability
- level/skill distributions
- Lv6/11/16/21/26/31 P25/P50/P75/P90
- post-skill meaningful Stage/event count
- coin/upgrades
- encounter repetition
- class opportunity coverage

Critical boundaries:
- 19→20
- 39→40
- 40→41 Lv31 Ascension entry
- 45→46 post-Lv31 mastery entry
- 49→50 final

---

# 7. Difficulty target — USER-CONFIRMED

General non-T1:
```text
P(full clear Stage1→50 | intended-entry SKILLED_V2_CENTRAL) < 0.60
```

Interpretation:
- 60% is upper bound, not target mean
- T1 may be higher
- overgrown replay excluded
- class rates may differ
- hard class lockout forbidden

Clear rate alone is insufficient.
Fail-location distribution must be evaluated because it drives star progression.

---

# 8. Mastery profiles

Required:
- LEARNING
- AVERAGE
- SKILLED_V2_CONSERVATIVE
- SKILLED_V2_CENTRAL
- SKILLED_V2_STRONG
- HIGH_MASTERY_STRESS

SKILLED_V2:
- combo40 is not an extreme-tail event
- context-sensitive timing degradation
- combo survival
- heavy/P×P usage
- turnover recovery

Canonical protocol:
`24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`

Do not reduce profile to one iid PERFECT/GOOD/NORMAL vector.

---

# 9. Player power targets

First calibration candidate:
- Lv6 5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36
- Lv31 **41–45**

USER-CONFIRMED:
Lv31 target window Stage41–45.

Late band:
```text
41–45 Lv31 Ascension
46–49 post-Lv31 mastery
50 final
```

Metrics:
- unlock distribution
- post-unlock Stage/event count
- pre/post power slope
- class divergence

---

# 10. Skill authority modes

Current truth:
- Lv6 authoritative
- Lv11/16/21 exact legacy parity candidates
- Lv26 designed-not-authoritative
- Lv31 design unresolved numerically

Simulation modes:
- CURRENT_AUTHORITY
- LEGACY_PARITY_CANDIDATE
- FUTURE_SKILL_PLACEHOLDER

Late Tier production freeze cannot rely only on Lv6 mode.

---

# 11. Layer D — Meta/account progression

Paths:
- FIRST_CLASS
- BALANCED_FIVE_CLASS
- STAR_STACKED
- FAVORITE_CLASS_FIRST
- WEAK_CLASS_RECOVERY
- ACHIEVEMENT_FOCUSED_SOLO
- HIGH_MASTERY

Outputs:
- stars over time
- permanent milestones
- class clear order
- repeat attempts
- soft-wall recovery events
- dominant route
- snowball
- graph reachability

### Soft-wall requirement
Normal difficulty should not rely mainly on Stage1–19 0★ failures.
Blocked class should usually have a reasonable route to 1★/2★ and account contribution.

Tier unlock first simulation hypothesis:
`CLEAR_LOCK`.
Not frozen.

---

# 12. Stars / achievements

Stars:
- broad foundation
- reward ladder only after soft-wall simulation

Achievements:
- targeted cross-class bridge
- reward edges only after class soft-wall map exists

Required order:
```text
soft-wall map
 -> stars-only recovery
 -> achievement edge candidate
 -> combined account simulation
```

---

# 13. Boss simulation policy

Placeholder only:
- Stage10 checkpoint boss optional
- Stage30 optional boss-signature preview
- Stage50 final boss candidate

If Stage50 has mandatory unique decision grammar, earlier preview required.

T4 boss-only novelty LOW by default.

---

# 14. Layer E — Multiplayer

Only after solo/shared campaign spine is stable.

2/3/4P checks:
- entity/readability
- kill-speed scaling
- wall pressure
- class composition
- AI/human mix
- specialist starvation

Scaling priority:
1. event budget
2. composition
3. specialist count
4. cadence/overlap
5. limited durability adjustment

Avoid blanket HP inflation first.

---

# 15. Determinism

Same:
- campaign spine version
- MonsterRegistry version
- Tier/Stage data version
- seed
- class/team
- mastery profile
- meta profile
- shop policy
must reproduce the same result.

Report:
- data hash/version
- seed range
- run count
- model mode
- mastery profile version

---

# 16. Failure classifications

## Campaign/novelty
- CAMPAIGN_SPINE_EMPTY_TIER
- NOVELTY_OVERLOAD
- NOVELTY_STARVATION
- SKILL_MONSTER_ATTRIBUTION_COLLISION

## Difficulty/player model
- TOO_EASY_FOR_SKILLED
- SKILLED_PROFILE_TOO_WEAK
- SKILLED_PROFILE_TOO_STRONG
- COMBO40_MODELED_AS_OUTLIER
- DIFFICULTY_GATE_PROFILE_UNSTABLE

## Skill windows
- SKILL_REACH_TOO_EARLY
- SKILL_REACH_TOO_LATE
- SKILL_WINDOW_COMPRESSED
- LV26_WINDOW_COMPRESSED
- INSUFFICIENT_LV31_PLAY_WINDOW
- LATE_LV31_DISTRIBUTION
- LV31_POWER_CLIFF_TOO_HIGH
- LV31_CLASS_CLEAR_RATE_DIVERGENCE

## Encounter
- TOO_MANY_ENTITIES
- FRONTLINE_SCREEN_TOO_LONG
- SIEGE_UPTIME_TOO_HIGH
- CHARGE_WINDOW_UNREADABLE
- REPLICATION_EXPLOSION
- DURABILITY_SPIKE
- CADENCE_COMPRESSION
- CLASS_STARVATION
- HARD_CLASS_LOCKOUT

## Meta/economy
- SHOP_SNOWBALL
- PERMANENT_STAT_SNOWBALL
- ACHIEVEMENT_ROUTE_DEADLOCK
- DOMINANT_PROGRESSION_ROUTE
- STAR_BOUNDARY_CLIFF

## Multiplayer
- TEAM_SCALING_DEFECT

Do not hide one cause with a global HP/count patch.

---

# 17. Current execution order

Completed:
1. Master Campaign Spine
2. 4/5/6 comparison
3. Model A novelty/roster/power/meta static audit
4. machine-readable Model A
5. Layer-0 validator PASS

Next:
6. Tier encounter archetype availability
7. Tier formation/cadence vocabulary
8. bounded pressure/complexity frequency ranges
9. representative deterministic recipes
10. static readability/entity checks
11. Layer-A micro sim
12. synthetic Tier slices
13. full Tier sim
14. 5-class soft-wall map
15. stars-only recovery
16. achievement bridge model
17. account sim
18. multiplayer expansion
19. report / explicit freeze
20. live implementation

---

# 18. Freeze gate

Not automatically frozen by simulation:
- final launch Tier count
- exact Tier unlock
- production monster values
- exact encounter frequency
- exact EXP formula
- star reward values
- achievement graph/value
- boss cadence/design
- shop cadence/economy
- Lv26/31 production skill coefficients

Simulation is decision support; explicit production approval remains required.
