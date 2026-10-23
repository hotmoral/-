# Timing Defense — P4-B R2 Approved Routing Contract V0.1

Date: 2026-10-23 KST  
Status: **USER APPROVED / STRUCTURAL ROUTING ACTIVE / NO NUMERICAL FREEZE**

Depends on:
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
- `84_P4B_EXP_DECISION_REASSESSMENT_PROPOSAL_V0_1.md`

User decision:
- **R2 APPROVED**

---

# 1. Approved routing

The current pure per-valid-turn EXP semantic remains the **provisional diagnostic baseline only**.

It is not frozen as final.

The project will separate:
1. player-skill identity / power-spine contract work, from
2. final EXP convergence under authoritative multiplayer scaling.

Approved route:

```text
P4-C1  Lv26 structural skill-contract decision
 -> P4-C2 Lv26 bounded provisional power feedback
 -> P4-D1 Lv31 structural skill-contract decision
 -> P4-D2 Lv31 bounded mastery/power feedback
 -> P4-E  provisional player-power-spine closure WITH EXP WATCHES
 -> P5/P6/P7/P8
 -> P10 current-roster multiplayer combat scaling baseline
 -> P10R mandatory EXP / multiplayer timebase reconvergence
 -> only after P10R may downstream permanent-progression work rely on converged EXP behavior
```

---

# 2. EXP semantics under R2

Still active as provisional diagnostic baseline:
- valid completed local timing turn is the EXP source;
- Heavy X+Y produces one combined-tier EXP award;
- timing quality changes credit gained;
- calibration uses dimensionless `XP_CREDIT`;
- universal EXP curve remains the preferred target;
- hidden class-specific and Tier-specific EXP multipliers remain disallowed without a new explicit user decision.

Not approved/frozen:
- pure per-turn EXP as final launch semantics;
- Stage Quality Budget / Option D;
- exact quality-credit values;
- exact milestone thresholds;
- player-visible EXP scale;
- player-count EXP correction;
- exact class-specific reach exceptions.

---

# 3. Mandatory active watches

Keep all simultaneously:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

No one watch may be used to erase another.

Future progression judgments must compare, where applicable:
- Stage-based skill reach;
- wall-clock skill reach;
- clear/fail probability;
- retry cost;
- wall attrition;
- homogeneous vs mixed teams;
- same-class different-teammate sensitivity;
- player-count scaling sensitivity.

---

# 4. P4-C1 boundary

The immediate next package is:

`P4-C1 — LV26 STRUCTURAL SKILL-CONTRACT DECISION`

Scope:
- review all five Lv26 skill identities;
- recover legacy/former intended mechanics exactly where evidence exists;
- distinguish authoritative / parity-candidate / unresolved semantics;
- analyze interactions with Lv6/Lv11/Lv16/Lv21 and monster roles;
- compare meaningful implementation alternatives where unresolved;
- present recommendation + risks + reversibility;
- require user approval before structural freeze or P4-C2 power execution.

Do not:
- invent generic Lv26 power proxies;
- use provisional EXP reach as final evidence;
- numerically freeze Lv26 coefficients without their own decision gate;
- start Lv31 structural freeze early;
- change production gameplay.

---

# 5. P10R mandatory reconvergence

After a credible current-roster 2P/3P/4P combat-scaling baseline exists, EXP convergence must be reopened before permanent progression depends on it.

P10R must compare at minimum:
- Solo;
- 2P / 3P / 4P;
- homogeneous teams;
- mixed teams;
- same class under different teammates;
- Stage-based reach;
- wall-clock reach;
- clear/fail/retry-adjusted progression;
- team-composition sensitivity;
- player-count sensitivity;
- whether pure per-turn remains acceptable;
- whether a class-neutral visible stabilizer such as Stage Quality Budget is actually necessary.

---

# 6. Freeze policy

This approval freezes **routing and semantic status**, not numerical balance.

Frozen by this decision:
- R2 routing is active;
- pure per-turn EXP is provisional baseline, not final;
- Option D is deferred, not approved;
- P10R recheck is mandatory before permanent progression may depend on final EXP convergence;
- P4-C1 is next.

Still open:
- Lv26 exact mechanics/numbers;
- Lv31 exact mechanics/numbers;
- final EXP semantics;
- exact EXP values/thresholds;
- multiplayer combat scaling;
- shop/economy/Base HP;
- star/achievement numerical power;
- bosses/exact campaign authoring;
- production numerical implementation.

Production remains untouched.