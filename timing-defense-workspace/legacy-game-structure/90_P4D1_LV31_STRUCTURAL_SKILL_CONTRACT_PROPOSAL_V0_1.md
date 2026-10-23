# Timing Defense — P4-D1 Lv31 Structural Skill Contract Proposal V0.1

Date: 2026-10-23 KST  
Status: **PROPOSED / AWAITING USER APPROVAL / NO STRUCTURAL FREEZE / NO P4-D2 EXECUTION**

Depends on:
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
- `89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
- `20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `../SKILL_PLAN_LV6_31.md`
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `../DESIGN_DECISIONS.md`

---

# 0. Decision question

Lv31 is the final run-level class milestone and is intentionally acquired around Stage41–45 so it can be used repeatedly through Stage46–49 before the Stage50 final.

The five roadmap identities exist, but all five remain implementation-critical `UNRESOLVED` at Lv31.

The decision now required is:

> How should each P×P CRITICAL final skill replace/compose with the already-approved Lv6–26 kit so that it feels like a final-class payoff without creating an uncontrolled additive effect tree, erasing class differentiation, or making Stage46–50 structurally trivial?

This proposal recommends **Option A — top-level P×P final-template replacement with lower-kit continuity**.

All new exact coefficients below are either inherited from already-known values or marked `P4D2_PROVISIONAL_SIMULATION_INPUT`. User approval would freeze the structural execution semantics only, not production balance numbers.

---

# 1. Global composition problem

If Lv31 is interpreted as simply additive on top of every lower generator, the P×P action can expand uncontrollably:

- Rogue: Lv21 five-dagger barrage + Lv26 Chain Throw + Lv31 eight-dagger storm;
- Archer: Lv21 triple shot where all three arrows gain unlimited battlefield penetration;
- Mage: Greater Orb + Arcane Burst + Resonance + Lv26 Chain Explosion + three-stage Arcane Collapse + more chains;
- Tank: Ground Impact + Aftershock + battlefield shockwave + overlapping shield refresh paths;
- Knight: existing heavy wave + Lv26 penetration package + two new full waves.

That would make it difficult to attribute power, tune the Stage46–50 mastery band, and preserve monster-role expression.

---

# 2. Global alternatives

## Option A — P×P final-template replacement with lower-kit continuity — **RECOMMENDED**

When a Lv31 player lands P×P:
- construct the class's Lv31 final attack template instead of the ordinary Lv21/Lv26 Heavy payload;
- persistent/passive lower-level modifiers continue to apply where semantically relevant;
- lower same-action hit generators that would duplicate the final template are suppressed unless explicitly incorporated into that class's final template;
- generated final-skill hits remain owned by one root action;
- no generated hit grants EXP/charge/combo or independently triggers N3;
- no recursive Lv31 generation;
- one root ordinary proc-crit decision is used where the class template allows crit, with generated damage using `PARENT_ROLL_INHERITED` unless explicitly overridden;
- P2 per-target mitigation remains authoritative.

Benefits:
- final skills feel transformational;
- power remains attributable;
- avoids hidden multiplicative explosions;
- supports bounded P4-D2 sensitivity testing;
- retains lower-kit identity instead of pretending Lv31 starts a new character.

## Option B — fully additive Lv31
Keep all Lv21/Lv26 generators and add Lv31 on top.

Not recommended:
- largest power-cliff risk;
- highest role-erasure risk;
- difficult to tune and explain;
- especially unsafe for Rogue/Archer/Mage.

## Option C — complete replacement, no lower-kit inheritance
Lv31 ignores most earlier class mechanics on P×P.

Not recommended:
- easier technically, but loses progression continuity;
- makes earlier milestones feel partially invalidated at the most important timing result.

Recommendation: **Option A**.

---

# 3. Common Lv31 root-action rules under Option A

1. Trigger only on the existing Heavy `P×P = CRITICAL` condition.
2. One P×P root action produces at most one final-skill package.
3. Final packages create no extra EXP, charge or combo.
4. Final packages do not independently trigger N3.
5. Generated damage uses deterministic parent/source attribution.
6. No free manual target selection is introduced.
7. Existing class scalar/passive effects remain where they do not duplicate the final hit generator.
8. P4-D2 must measure both combat power and **meaningful post-unlock play**, not only damage.
9. Any exact new coefficient not already independently frozen remains provisional.

---

# 4. Knight — Heaven-Splitting Slash

Roadmap identity:
`P×P CRITICAL -> huge double blade wave / broad penetration / major knockback`.

## Material ambiguity
- are the two waves both full-strength?
- do they use unlimited penetration?
- may the second wave retarget freely?
- how much stronger is “major knockback”?

## Alternatives

### K-A — two full-strength unlimited waves
Rejected as default.
It approaches Archer's unlimited-line identity while creating a very large power cliff.

### K-B — bounded broad double-wave — **RECOMMENDED**
- the root P×P attack is represented by **two sequential broad crescent waves**;
- both waves use Knight's existing broad Heavy corridor/formation logic, not Archer's strict unlimited battlefield ray;
- each wave retains the approved Lv26 Heavy penetration ceiling: primary + up to 3 additional targets;
- the second wave may hit enemies that are still/already newly present in the same authoritative corridor, but does not freely home to a new unrelated backline target;
- first wave uses the root outgoing basis;
- second wave is a scheduled echo derived from the same root and inherits the root crit result;
- Lv16 PERFECT damage/knockback transforms and Lv26 penetration-preservation/knockback ladder remain part of the final template;
- final-skill extra knockback multiplier is parameterized for P4-D2 rather than frozen now.

P4-D2 starting sensitivity candidates:
- second-wave coefficient: `0.50 / 0.65 / 0.80` of root outgoing basis;
- wave separation: `100 / 140 / 180 ms`;
- final knockback multiplier on top of existing Knight action basis: `1.25 / 1.35 / 1.50`.

These ranges are **simulation inputs, not approval of exact values**.

Why recommended:
- “double blade wave” is literal;
- Knight remains broad/frontline-oriented;
- Archer retains unique unlimited strict-line identity;
- second-wave timing can be tuned without changing the structural idea.

---

# 5. Rogue — Dagger Storm

Roadmap identity:
`P×P CRITICAL -> 8 rapid tracking daggers over roughly 0.5s`.

## Material ambiguity
- whether Blade Barrage and Chain Throw also fire;
- per-dagger damage;
- target lock vs per-dagger arbitrary retarget;
- exact schedule.

## Alternatives

### R-A — add 8 on top of Lv21 barrage
Not recommended; 13+ generated dagger events before other effects is an unnecessary event/power explosion.

### R-B — eight-dagger final replacement with target persistence — **RECOMMENDED**
- P×P replaces Lv21 Blade Barrage / Lv6 Double Dagger / Lv26 Chain Throw generators for that root action;
- exactly 8 Dagger Storm daggers are scheduled;
- first dagger targets the authoritative root primary target;
- while that target remains alive, later daggers continue to it, preserving Rogue's durable-normal execution identity;
- after target death/removal, remaining daggers retarget deterministically to the nearest live valid enemy and continue;
- same-target hit cap remains absent;
- boss dagger scalar `0.70` applies to each realized boss hit;
- root ordinary proc-crit is resolved once; storm daggers inherit it rather than rerolling eight times;
- Lv16 PERFECT recovery reward still applies because P×P contains PERFECT.

P4-D2 starting candidate:
- 8 daggers evenly spaced across ~0.49s (`70ms` intervals);
- per-dagger coefficient `0.45` as a provisional continuity anchor from the existing barrage follow-up family.

The 0.45 value is not numerically frozen by structural approval.

Why recommended:
- preserves “storm” readability;
- retains Rogue single-durable-target identity;
- avoids random target spraying and excessive generator stacking.

---

# 6. Tank — Absolute Barrier

Roadmap identity:
`P×P CRITICAL -> battlefield-wide shockwave + 250 wall shield for 6s`.

## Material ambiguity
- shockwave damage and knockback;
- whether Ground Impact/Aftershock are additive;
- shield interaction with Lv16 Perfect Guard and multiple Tanks.

## Alternatives

### T-A — full root damage to every enemy + additive shields
Not recommended. It turns Tank into a battlefield DPS burst and creates shield-stacking ambiguity.

### T-B — control-first battlefield wave + nonstacking barrier — **RECOMMENDED**
- P×P final template emits one battlefield-wide authoritative shockwave against all current live attackable enemies;
- shockwave is **control-first**, with reduced damage and strong knockback rather than full-damage global AoE;
- target/boss knockback resistance still applies; existing boss knockback scalar remains relevant;
- one normal approved Lv26 Aftershock Zone is retained at the primary/root Ground Impact location as part of the final template; the slow does not become battlefield-wide;
- the final template suppresses duplicate ordinary Ground Impact hit generation beyond these explicit effects;
- wall barrier uses one non-additive shared shield family;
- the same root's Lv16 Perfect Guard must not overwrite/downgrade the Lv31 barrier;
- a later weaker Lv16 guard cannot reduce an active stronger Lv31 barrier;
- repeated Lv31 barriers refresh according to the same nonstacking family rather than adding shield values together.

P4-D2 starting sensitivity candidates:
- shockwave damage coefficient: `0.40 / 0.50 / 0.60` of root outgoing basis;
- shockwave knockback multiplier: `2.0 / 2.5 / 3.0` before target resistance;
- roadmap shield `250 / 6s` retained as provisional primary candidate, not production freeze.

Why recommended:
- final skill strongly expresses Tank's control/wall-protection role;
- avoids competing with Mage as global AoE DPS;
- composes cleanly with Lv16/Lv26 and multiplayer shared-wall semantics.

---

# 7. Archer — Sky-Piercing Arrow

Roadmap identity:
`P×P CRITICAL -> huge high-speed arrow / battlefield line penetration without target-count limit / armor ignore`.

## Material ambiguity
- whether Triple Shot still creates three unlimited arrows;
- gameplay collision width;
- damage coefficient and speed significance.

## Alternatives

### A-A — Triple Shot becomes three unlimited battlefield arrows
Not recommended. This triples an already-unbounded line effect and creates extreme screen deletion.

### A-B — one unlimited strict-line final arrow — **RECOMMENDED**
- P×P replaces Lv21 Triple Shot for that root action;
- exactly one Sky-Piercing Arrow is launched along the authoritative locked root ray;
- every live enemy whose authoritative hit geometry intersects that ray may be hit once, ordered along the ray;
- no target-count cap;
- no homing, bending or off-line retargeting;
- armor is ignored;
- penetration damage remains 100% with no decay;
- root outgoing damage basis remains `1.00` per realized target unless P4-D2 later supports a change;
- “huge / high-speed” is presentation/time-of-flight language initially; **do not widen the gameplay collision corridor merely because the sprite is larger** without separate evidence.

Why recommended:
- exactly preserves Archer's strict-line identity;
- unlimited count is already a major final-skill upgrade;
- avoids accidental overlap with Knight's broad wave or Mage AoE.

P4-D2 primary watch:
- aligned screen deletion / protected SUPPORTER-SIEGER exposure;
- role-expression loss in deep formations.

---

# 8. Mage — Arcane Collapse

Roadmap identity:
`P×P CRITICAL -> large magic circle / three-stage blast / chained secondary explosions`.

P4-C2 already showed that Mage chain ordering can erase newly spawned SPLITTER children under strong Heavy results, so Lv31 must be bounded more carefully rather than recursively layering every existing Mage generator.

## Alternatives

### M-A — existing Greater Orb + Burst + Resonance + Chain, then add three more blasts/chains
Rejected as default. It maximizes recursive/event-volume and SPLITTER role-expression risk.

### M-B — one direct root impact + bounded three-stage collapse + one final chain generation — **RECOMMENDED**
- P×P replaces the ordinary Lv21 Greater Orb immediate explosion, Lv16 Resonance generator and Lv26 Chain generator for that root action;
- the original authoritative primary target receives one normal root direct impact so the final skill does not reduce single-target baseline damage;
- a magic circle is fixed at the authoritative root impact location;
- three scheduled AoE blast stages resolve from that fixed circle;
- the original primary target is excluded from the three AoE stages, preserving Mage's crowd-specialist identity rather than multiplying boss DPS;
- non-primary enemies may be hit by multiple stages if they remain in the circle;
- death/spawn consequences resolve chronologically after each stage;
- after the third stage only, at most one Lv26-style chain generation is allowed;
- final chain chooses up to 2 live enemies not already hit by the final collapse package where possible; no same-target fallback;
- newborn SPLITTER children may be eligible only according to chronological live-state/previous-hit rules;
- chain cannot recursively produce further collapse/burst/resonance/chain effects.

P4-D2 starting sensitivity candidates:
- blast times: `0 / +180 / +360 ms` relative to circle activation, reusing the existing delayed-effect cadence family;
- each AoE stage coefficient: `0.55` of root outgoing basis as a simple first candidate derived from the existing Resonance coefficient;
- magic-circle radius sensitivity: `1.00 / 1.25 / 1.50 ×` the current Lv21 Greater Orb radius;
- final chain retains Lv26 provisional `0.35 / max 2` for the first bounded pass.

None of those exact values are production-frozen by approval.

Why recommended:
- preserves the three-stage visual/mechanical identity;
- prevents a recursive proc graph;
- keeps direct boss damage at baseline while concentrating extra value on density;
- directly addresses the P4-C2 SPLITTER watch.

---

# 9. Cross-class differentiation check

Under recommended Option A:

- Knight = **broad bounded two-pass frontline disruption**;
- Rogue = **target-persistent rapid multihit execution**;
- Tank = **battlefield control + shared-wall protection**;
- Archer = **single strict-line unlimited-depth deletion**;
- Mage = **fixed-area multi-stage density collapse + bounded chain**.

This preserves distinct class geometry/decision identity instead of turning every Lv31 into generic screen-wide damage.

---

# 10. Monster-role / mastery-band guards

If approved, P4-D2 must explicitly test:

1. `LV31_POWER_CLIFF_TOO_HIGH`
2. `LV31_CLASS_CLEAR_RATE_DIVERGENCE`
3. `LV31_ROLE_EXPRESSION_ERASURE`
4. `LV31_MAGE_SPLITTER_TRANSFORM_ERASURE`
5. `LV31_ARCHER_SIEGER_SCREEN_ERASURE`
6. `LV31_TANK_SIEGER_PRE_EXPRESSION_ERASURE`
7. `LV31_KNIGHT_CHARGER_INTERRUPT_SATURATION`
8. whether Stage46–49 still provides meaningful mastery instead of immediate trivialization.

Stage41–45 must remain viable both before and after Lv31 unlock because players are crossing the milestone within that band.

---

# 11. EXP / progression implications

P4-C2 confirmed that offensive power generally reduces later local timing-action opportunities, while Tank control can move in the opposite direction.

Lv31 is expected to amplify this feedback.
Therefore approval of this structural package would **not** freeze:
- final pure-per-turn EXP;
- exact A31;
- class progression compensation;
- player-count treatment.

All R2 watches and mandatory P10R reconvergence remain active.

---

# 12. Recommendation

Approve **Option A package**:

1. P×P final-template replacement with lower-kit continuity;
2. Knight K-B bounded double wave;
3. Rogue R-B eight-dagger target-persistent storm;
4. Tank T-B control-first global shockwave + nonstacking barrier + one local Aftershock;
5. Archer A-B one strict-line unlimited arrow;
6. Mage M-B direct impact + bounded three-stage circle + one final chain generation.

Approve the listed numerical values/ranges only as `P4D2_PROVISIONAL_SIMULATION_INPUT`, not production numerical freeze.

---

# 13. Risks and reversibility

## Main risks
- Knight two-pass wave may still over-interrupt stateful enemies.
- Rogue 8×0.45 candidate may be too high/low against durable normals.
- Tank battlefield knockback may delay SIEGER expression or create excessive Stage duration.
- Archer unlimited ray may erase screened backline in aligned formations.
- Mage multi-stage circle may still erase SPLITTER population transformation.

## Reversibility
High for:
- coefficients;
- delays;
- radius;
- knockback magnitude;
- shield value/duration.

Medium for:
- target/retarget policy;
- whether Mage chains only after stage 3;
- whether Tank retains one local Aftershock.

More expensive later:
- changing additive-vs-replacement composition after P4-D2/P5/P6 have been calibrated around it.

This is why the composition model should be decided now while exact numbers remain provisional.

---

# 14. Requested user decision

P4-D1 recommendation is **Option A package** above.

If approved:
- create the Lv31 approved structural contract;
- keep all exact new numbers provisional;
- proceed to `P4-D2 — LV31 BOUNDED MASTERY / POWER FEEDBACK`;
- do not touch production gameplay.

If not approved, change only the identified class/global clause and keep P4-D2 blocked until the revised structure is explicitly approved.
