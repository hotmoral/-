# Timing Defense — P4-D1 Lv31 Power-Fantasy & Stage46 Mastery-Gate Approved Contract V0.1

Date: 2026-10-23 KST  
Status: **USER APPROVED STRUCTURAL DIRECTION / P4-D2 AUTHORIZED / NO PRODUCTION NUMERICAL FREEZE**

Supersedes the conservative interpretation of:
- `90_P4D1_LV31_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md`

Depends on:
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
- `89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `90_P4D1_LV31_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md`

---

# 0. User-approved correction to P4-D1 philosophy

The Lv31 final milestone must not be balanced by pre-emptively shrinking its spectacle or output merely so that the existing late-game pressure can absorb it.

Approved direction:

> Keep Lv31 visibly and mechanically explosive. Preserve a bounded, attributable effect graph, but let the final skill feel like the peak of each class fantasy. Then make the Stage46+ late-run pressure regime strong enough that this power is actually required and satisfying to use.

This means:
- `bounded effect graph` does **not** mean `low event count`;
- preventing uncontrolled recursive proc trees does **not** justify removing the class's defining spectacle;
- performance risk is an engineering validation target, not a reason to nerf the design before measurement;
- P4-D2 should primarily ask whether the late-game encounter pressure can **absorb and require** Lv31 power, not whether Lv31 can be made small enough to fit the old pressure envelope.

---

# 1. Approved Stage46+ mastery-gate direction

The late-run structure is strengthened from a generic mastery band into a deliberate **Lv31 Mastery Gate / late-run pressure regime**.

Target experiential flow:

```text
Stage41..45  = Lv31 acquisition / transition band
Stage46      = major pressure-regime step-up
Stage46..47  = power revelation: Lv31 should feel dramatically necessary and satisfying
Stage48..49  = mastery pressure: maintaining timing quality / combo / P×P opportunities becomes part of survival
Stage50      = final application of the whole run kit, not first Lv31 use
```

Structural acceptance:
- Stage46+ may be authored so that a Lv31-less player is gradually or rapidly buried because monster inflow/pressure exceeds ordinary Lv26 clearing capacity;
- near-zero Lv31-less clear probability is **allowed as an authored outcome**;
- however there is no code-level `level >= 31` entry lock and no artificial hard class lockout;
- exceptional outlier play may still survive if the actual combat system permits it, but it is not a required balance path;
- the gate must arise from real combat pressure and the player's ability to produce/maintain P×P CRITICAL opportunities.

This intentionally makes combo/timing maintenance part of the late-run difficulty.

---

# 2. Acquisition fairness requirement

A strong Stage46 mastery gate is only fair if intended skilled players normally possess Lv31 before that pressure step.

Therefore P4-D2/P4-E must measure the full acquisition distribution rather than assume a fixed percentage.

User direction:
- `90% by Stage46` is considered too lenient as a design target for intended skilled play;
- test a much higher possession envelope around Stage46 entry;
- candidate sensitivity checkpoints may include `97% / 98% / 99%`, but **none is numerically frozen here**.

The eventual threshold must satisfy:
- missing Lv31 at Stage46 is primarily explained by prior timing/combo/progression performance, not arbitrary class identity;
- offensive classes must not miss Lv31 merely because higher kill speed removed too many EXP opportunities;
- team composition/player count must not create unfair Stage46 gate misses;
- these fairness constraints keep all existing P4/P10R EXP watches active.

If acquisition fairness cannot be achieved, the Stage46 pressure gate must not be numerically frozen until the EXP/timebase cause is resolved.

---

# 3. Global Lv31 composition rule remains bounded but not timid

The safe part of proposal 90 remains approved:
- one Lv31 P×P root action owns one deterministic final-skill package;
- lower passive/scalar identity can carry into the final package;
- duplicate/redundant lower same-action generators may be absorbed into the Lv31 package rather than recursively stacking;
- generated hits create no extra EXP/charge/combo and do not independently trigger N3;
- no recursive Lv31 generation;
- parent/source attribution and P2 per-target mitigation remain authoritative;
- no free manual target selection is introduced.

Clarification:
- the final package itself may contain many visible, real hits/projectiles if that is the class fantasy;
- event count should be bounded and explicit, not artificially minimized;
- P4-D2 may increase the provisional magnitude/range if the Stage46+ pressure regime needs it.

---

# 4. Rogue Lv31 — Dagger Storm correction

Rogue's defining progression is multihit / thrown-weapon escalation. Lv31 must be the **peak** of that fantasy, not a conservative replacement that barely exceeds Lv21.

The old `exactly 8 daggers` recommendation from proposal 90 is **not approved as the working center**.

Approved structural identity:
- P×P creates one deterministic `Dagger Storm` final-skill package;
- the package contains a high but finite number of **real thrown daggers**;
- daggers are visibly/simulationally distinct projectiles/hits, not a hidden single damage scalar;
- while a current target survives, remaining daggers may keep concentrating on it;
- after death/removal, remaining daggers deterministically retarget to the nearest valid enemy and continue;
- same-target hit cap remains absent;
- boss dagger scalar remains applicable per realized boss hit;
- one root ordinary proc-crit result is inherited unless later evidence explicitly authorizes another policy;
- lower Rogue generator identity is absorbed into the storm package rather than recursively producing additional dagger trees.

P4-D2 projectile-count sensitivity:

```text
12 daggers / 16 daggers / 20 daggers
```

Working center:

```text
16 daggers
```

This is `P4D2_PROVISIONAL_SIMULATION_INPUT`, not a production numerical freeze.

P4-D2 must also test:
- storm duration/cadence sufficient to read as a barrage rather than instantaneous scalar damage;
- target-persistence vs retarget behavior;
- normal-target execution fantasy;
- 2P/3P/4P future event-volume/performance risk as an engineering watch, not a pre-emptive nerf trigger.

---

# 5. Other classes — power-fantasy interpretation

Proposal 90's role separation remains useful, but P4-D2 must not start from a `make the final skill modest` assumption.

## Knight
Heaven-Splitting Slash should create an unmistakable frontline-breaking event. Two-pass broad-wave structure remains a good bounded template, but second-wave damage/knockback and corridor pressure may be pushed upward if required for the Stage46+ regime.

## Tank
Absolute Barrier should visibly reset battlefield pressure through control and wall protection. It may be extremely strong at pressure reset without becoming generic Mage-style damage. The design target is `survive the impossible wave by controlling it`, not merely a small defensive increment.

## Archer
Sky-Piercing Arrow should genuinely erase a deep aligned line. Unlimited strict-line target count is a feature of the final fantasy, not something to suppress merely because it is strong. Counter-pressure should come from formation geometry and later wave composition rather than arbitrary target caps.

## Mage
Arcane Collapse should make dense populations collapse spectacularly. Recursion remains bounded for determinism/attribution, but the bounded three-stage/chain package may be allowed to erase large clusters. SPLITTER role-expression remains a watch, not an automatic Mage nerf order.

---

# 6. Revised P4-D2 question

Old overly conservative framing:

> Is Lv31 too strong for Stage46..50?

Approved framing:

> Does each Lv31 final skill deliver a compelling class-defining power spike, and can Stage46..50 be authored so that this power is necessary, readable, skill-gated through P×P/combo maintenance, and still leaves meaningful mastery decisions?

P4-D2 must evaluate both sides of the equation:

```text
Lv31 power magnitude
<->
Stage46+ encounter pressure capacity
```

Do not tune only one side in isolation.

---

# 7. Required P4-D2 measurements / watches

Keep:
- `LV31_CLASS_CLEAR_RATE_DIVERGENCE`
- `LV31_ROLE_EXPRESSION_ERASURE`
- `LV31_MAGE_SPLITTER_TRANSFORM_ERASURE`
- `LV31_ARCHER_SIEGER_SCREEN_ERASURE`
- `LV31_TANK_SIEGER_PRE_EXPRESSION_ERASURE`
- `LV31_KNIGHT_CHARGER_INTERRUPT_SATURATION`
- all P4-B/P4-C2 EXP opportunity watches

Add/reframe:
- `LV31_POWER_FANTASY_UNDERSHOOT`
- `STAGE46_LV31_ACQUISITION_FAIRNESS`
- `STAGE46_LV31_ABSENCE_BURIAL_BEHAVIOR`
- `STAGE46_PRESSURE_INSUFFICIENT_FOR_LV31`
- `PXP_COMBO_MAINTENANCE_MASTERY_PRESSURE`
- `ROGUE_DAGGER_STORM_EVENT_VOLUME_PERFORMANCE_WATCH`

`LV31_POWER_CLIFF_TOO_HIGH` is not a blanket failure condition anymore.
A large power cliff is intentional. It fails only when it cannot be absorbed by fair Stage46+ authoring, destroys class differentiation, breaks deterministic/runtime constraints, or makes Stage46..50 trivial despite the pressure redesign.

---

# 8. What remains provisional

Not frozen here:
- exact Stage46 Lv31 possession threshold (`97/98/99%` are candidate checkpoints only);
- exact Stage46..50 monster counts/HP/speeds/compositions;
- exact Lv31 damage coefficients/radii/knockback/durations;
- Rogue final dagger count (12/16/20 sensitivity; 16 working center only);
- final EXP semantics and A31;
- multiplayer EXP/timebase treatment;
- production performance implementation;
- exact launch Stage authoring.

No production gameplay code is authorized by this contract.

---

# 9. Decision state

User direction has approved:
1. **do not pre-emptively nerf Lv31 power fantasy**;
2. **keep final-skill effect graphs finite/deterministic rather than recursive/unbounded**;
3. **make Stage46+ pressure rise sharply enough that Lv31/P×P is functionally required for intended late-run survival**;
4. **allow Lv31-less players to be buried by actual combat pressure, without a code-level level gate**;
5. **treat combo/P×P maintenance as part of late-run mastery difficulty**;
6. **Rogue Dagger Storm must culminate in many real thrown projectiles; test 12/16/20 with 16 as the working center**;
7. **performance concerns are to be measured/engineered, not used as an unmeasured design-nerf justification**.

Therefore:

```text
P4-D1 structural direction = USER APPROVED WITH MODIFICATION
P4-D2 bounded mastery/power/pressure feedback = AUTHORIZED
production numerical freeze = NO
production implementation = UNAUTHORIZED
```
