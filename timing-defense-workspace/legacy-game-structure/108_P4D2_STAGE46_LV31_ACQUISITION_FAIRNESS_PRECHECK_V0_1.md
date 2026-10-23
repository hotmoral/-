# Timing Defense — P4-D2 Stage46 Lv31 Acquisition Fairness Precheck V0.1

Date: 2026-10-23 KST  
Status: **PRECHECK COMPLETE / CURRENT PURE-PER-TURN BASELINE NOT SUFFICIENT FOR 97-99% FREEZE / R2 DEFERRAL CONFIRMED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority / context:
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `data/p4a_marker_inverse_design_summary_v0_1.json`
- `data/p4b_combat_feedback_divergence_v0_1.json`

---

# 0. Question

Stage46 is allowed to become a strong Lv31 mastery gate only if intended-skilled players normally possess Lv31 before entering that pressure regime.

Candidate possession checkpoints previously retained for sensitivity were:

```text
97% / 98% / 99%
```

This precheck asks whether current evidence is sufficient to select/freeze one of those values.

Answer:

**NO. Current evidence is sufficient to show that the marker-only opportunity spine can place Lv31 in the desired 41-45 band, but it is also sufficient to show that the provisional pure-per-valid-turn EXP baseline becomes class-divergent once actual skill power changes action opportunity.**

Therefore no 97/98/99 Stage46 possession percentage may be frozen in P4-D2.

---

# 1. Marker-only P4-A signal

P4-A intentionally ignored class skill-power feedback and solved only the synthetic opportunity marker problem.

At the midpoint Lv31 candidate anchor `987.84375`, CENTRAL P50 reach was:

```text
T1  Stage43
T2  Stage43
T3  Stage45
T4  Stage41
```

P90 CENTRAL reach was:

```text
T1  Stage43
T2  Stage44
T3  Stage45
T4  Stage42
```

This supports the structural feasibility of:

```text
Stage41..45 = Lv31 acquisition / transition
Stage46     = pressure step-up
```

under a marker-only opportunity model.

However, P4-A explicitly warned that combat power can reduce later timing-event opportunity and that the marker anchor is not final EXP authority.

---

# 2. P4-B feedback invalidates direct percentile promotion

P4-B inserted bounded lower-skill combat-power feedback and found major class divergence.

Representative full-feedback P50 Lv31 reach examples at the old P4-A midpoint were:

```text
Knight: T1 51 / T2 51 / T3 51 / T4 51
Rogue : T1 51 / T2 51 / T3 51 / T4 51
Tank  : T1 51 / T2 51 / T3 51 / T4 51
Archer: T1 51 / T2 51 / T3 51 / T4 51
Mage  : T1 51 / T2 51 / T3 51 / T4 51
```

The old midpoint itself is therefore unusable once feedback is admitted.

More importantly, even after searching for a better universal pure-per-turn threshold, P4-B still found Lv31 class/Tier conflicts.

Best universal pure-per-turn Lv31 search:

```text
threshold approx 656.5
max window miss = 5 stages
class-tier misses = 8
```

Representative conflicts included:

```text
Mage T3 about Stage50
Mage T2 about Stage49
Tank T1/T3 about Stage36
Tank T2/T4 about Stage37
Knight T3 about Stage46
```

So the current provisional EXP semantic can make defensive/control classes reach Lv31 far too early while some offensive classes reach it far too late.

This is the opposite of a fair 97-99% Stage46 acquisition gate.

---

# 3. Why this is not repaired inside P4-D2

The divergence is a feedback-loop problem:

```text
combat power
-> kill speed
-> number of later timing opportunities
-> EXP opportunity
-> skill reach
-> more combat power
```

P4-B also showed that reducing the feedback strength artificially does not robustly remove the conflict, and hidden class/Tier EXP compensation is not authorized.

R2 therefore explicitly routes final EXP convergence to P10R after credible multiplayer combat scaling exists.

P10R must compare:
- solo;
- 2P/3P/4P;
- homogeneous/mixed teams;
- same class under different teammates;
- Stage-based reach;
- wall-clock reach;
- fail/retry-adjusted progression;
- player-count and composition sensitivity.

Thus attempting to freeze Stage46 possession at 97/98/99 now would violate the approved routing.

---

# 4. P4-D2 decision

Classification:

```text
STAGE41_45_LV31_ACQUISITION_BAND_STRUCTURALLY_FEASIBLE = YES
CURRENT_PURE_PER_TURN_EXP_CAN_PROVE_97_98_99_STAGE46_FAIRNESS = NO
97_PERCENT_FREEZE = NOT_AUTHORIZED
98_PERCENT_FREEZE = NOT_AUTHORIZED
99_PERCENT_FREEZE = NOT_AUTHORIZED
HIDDEN_CLASS_XP_PATCH = NOT_AUTHORIZED
P10R_RECONVERGENCE_REQUIRED = YES
```

P4-D2 may therefore use the Stage46 mastery-gate direction as a **combat-structure target**, but it may not numerically freeze the gate or claim acquisition fairness from current EXP evidence.

---

# 5. P4-D2 / P4-E boundary

This result does not require reopening P4-B.

It confirms the already-approved R2 route:

```text
P4-D2
-> provisional combat/mastery pressure closure with explicit EXP watch
-> P4-E provisional player-power-spine closure WITH EXP WATCHES
-> P5..P10
-> P10R mandatory EXP/timebase reconvergence
```

The Stage46 combat gate must remain numerically provisional until P10R demonstrates that intended-skilled acquisition is fair across class/team/player-count conditions.

Keep active:
- `STAGE46_LV31_ACQUISITION_FAIRNESS`
- `SOLO_PROGRESSION_DIVERGENCE_WATCH`
- `TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH`
- `PLAYER_COUNT_SCALING_XP_DEPENDENCY`
- `MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE`

---

# 6. What P4-D2 may close without

P4-D2 does **not** need to invent a final EXP correction before closing its combat-structure work.

It may close provisionally if:
- Lv31 skill identities are structurally coherent;
- Stage46+ pressure can absorb/require Lv31;
- Stage48-49 mastery pressure is fair at encounter-grammar level;
- known simulator fidelity defects are classified;
- acquisition fairness remains an explicit deferred watch rather than being falsely declared solved.

No production implementation is authorized by this precheck.
