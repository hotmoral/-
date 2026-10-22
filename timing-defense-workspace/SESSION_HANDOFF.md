# Timing Defense — Session Handoff

Updated: 2026-10-22 KST

## Canonical recovery rule
Always re-read live `timing-defense-workspace` HEAD first.
Live remote wins over memory/chat/handoff.

## Current executable checkpoint
- last validated executable: v0.45 SIEGER FULL PASS
- deployment HEAD: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- health: `0.45-cf.1`
- no gameplay/numerical implementation authorized after v0.45

---

# CRITICAL CURRENT DIRECTION

The large Master Campaign Spine tranche has completed its static/Layer-0 admission work.

Current phase:
**Bounded Simulation Authoring**

Read first:
1. `PROJECT_STATUS.md`
2. `NEXT_WORK.md`
3. `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
4. `legacy-game-structure/30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`
5. `legacy-game-structure/28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
6. `legacy-game-structure/29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
7. `legacy-game-structure/22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
8. `legacy-game-structure/24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
9. `legacy-game-structure/25_MODEL_A_META_PROGRESS_VOLUME_AND_SOFT_WALL_ENVELOPE_V0_1.md`
10. `legacy-game-structure/08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
11. `legacy-game-structure/06_SIMULATION_CALIBRATION_PLAN.md`
12. `legacy-game-structure/04_MONSTER_ENCOUNTER_MODEL.md`

Machine-readable:
- `legacy-game-structure/data/model_a_campaign_spine_v0_1.yaml`
- `tools/validate_campaign_spine.py`

---

# USER-CONFIRMED PROGRESSION TRUTH

- 5 classes: Knight / Rogue / Tank / Archer / Mage.
- Each class progresses through Tiers independently.
- Same Tier/Stage combat content is shared across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars are non-spendable broad account permanent growth.
- achievements are targeted cross-class permanent growth.
- one class may hit a recoverable soft wall.
- other-class stars/achievements should help that class later.
- hard class lockout is forbidden.
- current 9 ordinary monsters are V1 capability foundation, not lifetime final roster.
- T1 should not expose all 9.
- higher Tiers should introduce new monster types.
- future T5/T6/T7+ Tier/monster expansion must remain open.
- non-T1 intended-entry SKILLED_V2 full-Tier clear probability should normally be <60%.
- combo40 is achievable skilled play, not high-mastery-only.
- **Lv31 target unlock window = Stage41–45.**
- Stage46–49 should provide repeated Lv31 use/mastery.
- Stage50 should use an already-familiar Lv31 skill.

---

# MASTER CAMPAIGN RESULT

Current default bounded simulation spine:

```text
MODEL A
T1: GRUNT / RUNNER / BRUTE
T2: + SHIELD / FLYER
T3: + CHARGER / SPLITTER
T4: + SUPPORTER / SIEGER
T5+: future expansion
```

Status:
- Static Master Audit: PASS
- Layer-0 validator: PASS
- validation output: `errors=0 warnings=0`

This is NOT final production Tier freeze.
It is the default spine for lower-layer simulation.

Fallback Model B:
```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP
T5 +SI
```
Use only if Model A T4 evidence fails.

---

# MODEL A TIER IDENTITIES

## T1 — Foundation / Timing & Frontline
- G/R/B
- BASELINE high
- RUSH/BULWARK medium
- C0/C1 dominant

## T2 — Mitigation / Geometry
- +SH/F
- BULWARK high
- AERIAL medium-high
- C1/C2 dominant

## T3 — Burst / Transformation
- +C/SP
- BREACH high
- REPLICATE high
- FLOOD/RUSH medium-high
- C2 dominant, C3 meaningful late

## T4 — Formation / Siege
- +SUP/SI
- SUPPORT/SIEGE high at Tier-identity level
- BULWARK medium-high as screen support
- C2/C3 late dominant; C4 bounded mainly 46–50

HIGH does not mean simultaneous in every Stage.

---

# MODEL A INTRODUCTION WINDOWS

Range candidates, not exact production locks.

## T1
- G teach1–2 / mixed4–6 / pressure21–29
- R teach5–7 / mixed8–12 / first high21–24
- B teach15–17 / mixed18–20 / first high21–23

## T2
- SH teach5–7 / mixed8–12 / first high21–24
- F teach15–17 / mixed18–22 / first high28–31

## T3
- C teach5–7 / mixed8–14 / first high21–24
- SP teach15–17 / mixed18–22 / first high28–31

## T4
- SUP teach11–13 / mixed14–19 / first high29–31
- SI teach22–24 / mixed25–29 / first high37–39

No new core ordinary teaching in Stage41+.

---

# PLAYER POWER SPINE

First calibration candidate:
- Lv6 Stage5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36
- Lv31 **41–45**

Only Lv31 is user-confirmed as a target window.
Others are calibration candidates.

Late-band contract:
```text
31–39 pressure / soft-wall build
40     2★ gate
41–45  LV31 ASCENSION WINDOW
46–49  POST-LV31 MASTERY
50     TIER FINAL
```

Important distinction:
- class T1 skill unlocks can be pedagogic novelty.
- same-class T2+ unlocks are mostly repeated run-local power spikes.
- monster-learning collision and power-attribution collision are separate checks.

---

# SKILLED_V2

Do not reuse old weak skilled profile.

Profiles for calibration:
- LEARNING
- AVERAGE
- SKILLED_V2_CONSERVATIVE
- SKILLED_V2_CENTRAL
- SKILLED_V2_STRONG
- HIGH_MASTERY_STRESS

SKILLED_V2 must model:
- combo40 as non-outlier skilled performance
- context-sensitive timing degradation
- combo survival
- heavy/P×P usage
- target-turnover recovery

General non-T1 gate:
```text
P(Stage1→50 full clear | intended-entry SKILLED_V2_CENTRAL) < 0.60
```

T1 may be easier.

---

# SOFT-WALL / META FINDING

Clear probability alone is insufficient.
Fail location controls star/meta progression.

Preferred normal soft-wall shape:
```text
late fail -> 1★/2★
 -> progress other classes
 -> gain broad/targeted permanent growth
 -> return
 -> old wall becomes attainable
```

Avoid a normal campaign where hard classes mostly fail Stage1–19 for 0★.
That creates dead progression lanes and excessive retry volume.

First Tier-unlock simulation hypothesis:
`CLEAR_LOCK` = Stage50 clear required to unlock same class next Tier.
This is OPEN, not user-frozen.

---

# BOSS PLACEHOLDER POLICY

Not boss design freeze.

- Stage10 = checkpoint, boss optional
- around Stage30 = optional boss-signature preview slot
- Stage50 = Tier Final boss candidate
- mandatory Stage50 boss decision grammar must be previewed earlier
- T4 boss-only novelty budget LOW

---

# MACHINE VALIDATION

Data:
`legacy-game-structure/data/model_a_campaign_spine_v0_1.yaml`

Validator:
`tools/validate_campaign_spine.py`

Current report:
`legacy-game-structure/30_LAYER0_MODEL_A_VALIDATION_REPORT_V0_1.md`

Result:
```text
PASS errors=0 warnings=0
```

Two candidate windows were moved after automatic attribution warnings:
- T1 BRUTE first-high 24–29 -> 21–23
- T4 SUPPORTER first-high 31–33 -> 29–31

GRUNT baseline is exempt from capability-novelty collision warning.

---

# PARKED / SUPERSEDED ACTIVE CANDIDATES

Historical evidence only:
- `09_TIER_LADDER_CANDIDATE_V0_1.md`
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `14_T1_2P_AUTHORING_ENVELOPE_V0_1.md`
- `17_MASTER_CAMPAIGN_MATRIX_V0_1.md`

Do not resume them as current authority.

---

# EXACT NEXT BOUNDARY

The upstream Master Campaign structure is closed enough for bounded encounter authoring.

Next tranche:
1. map E01–E20 encounter archetypes to Model A Tier roster availability,
2. define which archetypes are unavailable/invalid before their required monsters unlock,
3. define Tier-specific formation vocabulary,
4. define Tier-specific cadence vocabulary,
5. convert pressure LOW/MED/HIGH to bounded candidate frequency ranges,
6. convert complexity envelopes to bounded frequency ranges,
7. author representative deterministic recipes only,
8. static authored/effective entity and 4s/6s readability checks,
9. Layer-A micro simulation,
10. revise envelope before exact 50-Stage schedules.

Do NOT yet:
- freeze production monster coefficients,
- author exact 200 launch stages,
- change live gameplay code,
- freeze permanent star values,
- freeze achievement reward edges/values,
- freeze boss/shop cadence,
- start detailed 3P/4P production balance.

---

# Handoff discipline

New session must:
1. check live `timing-defense-workspace` HEAD,
2. read this handoff,
3. read PROJECT_STATUS / NEXT_WORK,
4. read Matrix V0.2 + Layer0 report + authoring windows + pressure envelope,
5. verify no newer remote changes,
6. continue only from the exact encounter-authoring boundary.

Current tranche modifies planning/corpus/analysis tooling only.
No live gameplay code or production balance value was changed.
