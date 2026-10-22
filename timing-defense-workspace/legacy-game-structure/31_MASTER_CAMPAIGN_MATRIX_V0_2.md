# Timing Defense — Master Campaign Matrix V0.2

Date: 2026-10-22 KST  
Status: **ACTIVE BOUNDED SIMULATION SPINE / NOT PRODUCTION FREEZE**

Supersedes for active planning:
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Evidence/detail remains in:
- `19_MODEL_A_B_CLASS_ROLE_AND_VOLUME_AUDIT_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `21_MODEL_A_NOVELTY_BUDGET_AND_BOSS_PLACEHOLDERS_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
- `25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
- `26_MODEL_A_T1_T4_MACRO_SKELETON_V0_1.md`
- `27_MODEL_A_STATIC_MASTER_AUDIT_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
- `30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`

Machine-readable:
- `data/model_a_campaign_spine_v0_1.yaml`
- validator: `../tools/validate_campaign_spine.py`

---

# 0. Current decision boundary

Model A has passed static master audit and Layer-0 structural validation.

Therefore:
> **Model A is now the default bounded simulation spine.**

This does NOT mean:
- launch Tier count final freeze
- monster production values freeze
- boss design freeze
- EXP formula freeze
- star/achievement reward freeze

Model B remains the predefined fallback if T4 lower-layer testing fails.

---

# 1. Campaign topology

## Model A
```text
Initial campaign: T1 -> T2 -> T3 -> T4
Future: T5 -> T6 -> T7 -> ...
```

5 classes share Stage content but keep independent Tier records.

Current V1 ordinary roster is not lifetime final roster.
Future Tier/monster expansion remains open.

---

# 2. Monster availability

| Tier | New monsters | Available after unlock | Identity |
|---|---|---|---|
| T1 | GRUNT / RUNNER / BRUTE | 3 | Foundation / Timing & Frontline |
| T2 | SHIELD / FLYER | 5 | Mitigation / Geometry |
| T3 | CHARGER / SPLITTER | 7 | Burst / Transformation |
| T4 | SUPPORTER / SIEGER | 9 | Formation / Siege |
| T5+ | future | 10+ | expansion |

---

# 3. Player power spine

First calibration reach windows:

| Milestone | Candidate Stage window |
|---|---|
| Lv6 | 5–7 |
| Lv11 | 11–14 |
| Lv16 | 18–21 |
| Lv21 | 25–28 |
| Lv26 | 32–36 |
| Lv31 | **41–45** |

Lv31 Stage41–45 is user-confirmed direction.
Other milestone ranges remain calibration candidates.

---

# 4. Common late-band grammar

```text
31–39  Pressure / soft-wall build
40     2★ Star Gate B
41–45  Lv31 Ascension Window
46–49  Post-Lv31 Mastery
50     Tier Final / 3★
```

Rules:
- no new core ordinary capability in 41–50
- no unpreviewed mandatory boss-only mechanic at 50
- Stage50 is not Lv31 tutorial

---

# 5. Monster authoring windows

## T1
- G teach 1–2 / mixed 4–6 / pressure 21–29
- R teach 5–7 / mixed 8–12 / first high 21–24
- B teach 15–17 / mixed 18–20 / first high 21–23

## T2
- SH teach 5–7 / mixed 8–12 / first high 21–24
- F teach 15–17 / mixed 18–22 / first high 28–31

## T3
- C teach 5–7 / mixed 8–14 / first high 21–24
- SP teach 15–17 / mixed 18–22 / first high 28–31

## T4
- SUP teach 11–13 / mixed 14–19 / first high 29–31
- SI teach 22–24 / mixed 25–29 / first high 37–39

These are range candidates, not exact production Stage locks.

---

# 6. Pressure identities

## T1
- BASELINE HIGH
- RUSH MED
- BULWARK MED
- FLOOD LOW–MED

## T2
- BULWARK HIGH
- AERIAL MED–HIGH
- BASELINE/RUSH supporting

## T3
- BREACH HIGH
- REPLICATE HIGH
- FLOOD/RUSH MED–HIGH

## T4
- SUPPORT HIGH
- SIEGE HIGH
- BULWARK MED–HIGH
- other prior families return at MED/LOW–MED

HIGH means Tier-level identity, not every Stage simultaneous pressure.

---

# 7. Complexity identities

- T1: C0/C1 dominant; C4 unnecessary
- T2: C1/C2 dominant; C3 limited
- T3: C2 dominant; C3 meaningful; C4 rare late
- T4: C2/C3 dominant late; C4 bounded mainly 46–50

Higher Tier != constant chaos.
Focused C1/C2 extreme stages remain valid late-game content.

---

# 8. Boss placeholder policy

- Stage10: checkpoint, boss optional
- around Stage30: optional boss-signature preview slot
- Stage50: Tier Final boss candidate

If final boss has a mandatory unique decision grammar, it must be previewed earlier.

T4 boss-only novelty budget is LOW because SUP/SI + late Lv31 already create strong novelty load.

---

# 9. Difficulty authority

User-confirmed general target:

```text
P(full Tier clear Stage1→50 | intended-entry SKILLED_V2_CENTRAL) < 0.60
```

Applies to non-T1 by default.
T1 may be easier.

Important:
- combo40 is skilled-achievable, not extreme-only
- overgrown replay excluded from difficulty gate
- class clear rates may differ
- hard class lockout forbidden

---

# 10. Soft-wall authority

Preferred soft-wall shape:
```text
late fail -> 1★/2★ acquired
 -> other classes progress
 -> permanent growth
 -> return
 -> blocked class advances/clears
```

Do not generate difficulty mainly by repeated Stage1–19 failure.
That creates 0★ dead lanes and excessive retry volume.

Tier unlock first simulation hypothesis:
- `CLEAR_LOCK`: previous Tier Stage50 clear required for same class next Tier.

This remains OPEN, not frozen.

---

# 11. SKILLED_V2 calibration

Use:
- LEARNING
- AVERAGE
- SKILLED_V2_CONSERVATIVE
- SKILLED_V2_CENTRAL
- SKILLED_V2_STRONG
- HIGH_MASTERY_STRESS

Do not use one iid timing percentage vector as the whole player model.
Measure pressure degradation, combo survival, heavy/P×P usage and target-turnover recovery.

---

# 12. Layer-0 admission evidence

Machine-readable validator result after two attribution-window refinements:

```text
RESULT=PASS errors=0 warnings=0
```

Refinements:
- T1 BRUTE first-high 24–29 -> 21–23
- T4 SUPPORTER first-high 31–33 -> 29–31
- GRUNT baseline exempt from capability-attribution collision warnings

---

# 13. Model B fallback trigger

Switch Model A -> Model B only if lower-layer evidence shows T4 cannot remain readable/stable because of:
- SUP/SI learning density
- support/siege uptime interaction
- Lv26/Lv31 power-spike instability
- class opportunity collapse

Model B:
- T4 +SUPPORTER
- T5 +SIEGER

Do not split preemptively without evidence.

---

# 14. Exact next layer

Master-spine design is sufficiently closed for bounded simulation authoring.

Next:
1. define Tier-specific encounter archetype availability under current monster roster
2. convert qualitative pressure envelopes into candidate frequency bands/count ranges
3. define formation/cadence availability by Tier
4. create deterministic encounter recipes without production HP/speed freeze
5. Layer-A micro-sim
6. synthetic Tier slices
7. full Tier simulations
8. 5-class soft-wall map
9. stars-only recovery
10. achievement bridge modeling

Still no live gameplay patch.
