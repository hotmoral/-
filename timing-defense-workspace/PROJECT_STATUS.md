# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning authority

Active phase:
**Bounded Simulation Authoring after Master Campaign Layer-0 PASS**

Primary integrated authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Supporting current docs:
- `legacy-game-structure/30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`
- `legacy-game-structure/28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `legacy-game-structure/29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
- `legacy-game-structure/22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
- `legacy-game-structure/25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
- `legacy-game-structure/18_MONSTER_ROSTER_EXTENSIBILITY_AMENDMENT_2026-10-22.md`
- `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`

Machine-readable candidate:
- `legacy-game-structure/data/model_a_campaign_spine_v0_1.yaml`
- validator `tools/validate_campaign_spine.py`

---

# Core structural truth

- 5 classes progress through Tiers independently.
- Same Tier/Stage combat content is shared across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account growth.
- achievements = targeted cross-class growth.
- recoverable soft walls are intentional.
- hard class lockout forbidden.
- current 9-monster V1 roster is not lifetime final roster.
- higher Tiers introduce new monsters; T1 does not force all 9.
- future Tier/monster expansion remains open.
- non-T1 intended-entry SKILLED_V2 full-clear must normally be <60%.
- combo40 is skilled-achievable, not extreme-only.
- **Lv31 target unlock window = Stage41–45.**

---

# Current Model A bounded spine

```text
T1 G/R/B              Foundation / Timing & Frontline
T2 +SH/F              Mitigation / Geometry
T3 +C/SP              Burst / Transformation
T4 +SUP/SI            Formation / Siege
T5+ future            Expansion
```

Status:
**STATIC MASTER AUDIT PASS + LAYER-0 VALIDATOR PASS**

Validator result:
```text
RESULT=PASS errors=0 warnings=0
```

Meaning:
- Model A is the default simulation spine.
- 4 launch Tiers are not production-frozen.

Fallback Model B remains available if T4 lower-layer testing fails.

---

# Current player-power candidate

- Lv6 5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36
- Lv31 **41–45**

Late grammar:
```text
31–39 pressure / soft wall
40     2★ boundary
41–45  Lv31 Ascension
46–49  post-Lv31 mastery
50     Tier Final
```

Exact EXP formula remains open.

---

# Novelty / Boss policy

- pedagogic novelty and repeated run power-spike novelty are tracked separately.
- T1 boss-only novelty LOW.
- Stage10 boss optional checkpoint.
- Stage30 optional boss-signature preview slot.
- Stage50 final boss candidate.
- mandatory Stage50 boss grammar cannot be completely unpreviewed.
- T4 boss-only novelty LOW because SUP/SI + Lv31 already consume novelty budget.

---

# Difficulty/meta finding

Full-clear probability alone is insufficient.
Failure location must be tracked because it determines star progression.

Preferred soft-wall structure:
- late failure often yields 1★/2★,
- other classes provide growth,
- return to blocked class,
- clear probability rises.

Avoid making the normal difficulty model mostly Stage1–19 0★ failures.

First Tier-unlock simulation hypothesis:
- `CLEAR_LOCK` (Stage50 clear required to unlock same class next Tier).
- not frozen.

---

# Parked / superseded

Historical only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

---

# Current exact work

Now allowed:
1. Tier-specific encounter archetype availability
2. formation/cadence availability by Tier
3. pressure/complexity frequency envelopes -> bounded candidate ranges
4. representative deterministic encounter recipes
5. static readability/entity checks
6. Layer-A encounter micro-simulation

Not allowed yet:
- production coefficient freeze
- exact 200-Stage schedule
- live campaign patch
- final star/achievement values
- boss/shop cadence freeze
- detailed 3P/4P production balance

No production numbers are frozen by the current planning tranche.
