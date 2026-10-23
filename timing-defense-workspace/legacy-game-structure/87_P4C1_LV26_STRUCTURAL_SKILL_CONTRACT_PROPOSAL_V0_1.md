# Timing Defense — P4-C1 Lv26 Structural Skill Contract Proposal V0.1

Date: 2026-10-23 KST  
Status: **PROPOSED / AWAITING USER APPROVAL / NO STRUCTURAL FREEZE / NO P4-C2 EXECUTION**

Depends on:
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `22_PLAYER_POWER_SPINE_LV6_31_V0_1.md`
- `23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
- `26_MODEL_A_T1_T4_MACRO_SKELETON_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
- `../SKILL_PLAN_LV6_31.md`
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
- `../DESIGN_DECISIONS.md`
- `../V016_IMPLEMENTATION_REPORT.md`
- `../BALANCE_SIM_REPORT_V7_V016_EXACT.md`
- `../MONSTER_CAPABILITY_CONTRACT_V1.md`
- `../CLOUDFLARE_V043_SPLITTER_CAPABILITY_PASS_2026-10-22.md`
- `../CLOUDFLARE_V044_SUPPORTER_CAPABILITY_PASS_2026-10-22.md`
- `../CLOUDFLARE_V045_SIEGER_CAPABILITY_PASS_2026-10-22.md`
- legacy/current source evidence including `timing-defense-v011/v016-core.js` and current Cloudflare `v036-entry.js` / later capability chain.

---

# 0. Decision question

P4-C1 must decide the exact **structural semantics** of the five Lv26 skills before any Lv26 power-feedback simulation is allowed.

The question is not whether the Lv26 roadmap names/identities exist. They do.

The unresolved question is:

> How exactly do the designed Lv26 effects compose with Lv6/Lv11/Lv16/Lv21, targeting, crit inheritance, penetration, knockback, movement state, death/spawn ordering and monster role-expression without inventing generic power proxies or creating uncontrolled recursive effects?

This proposal recommends preserving all five roadmap identities while closing only the missing execution semantics needed for deterministic P4-C2 simulation.

User approval is required before any recommendation below becomes `USER_APPROVED_DIRECTION` or `STRUCTURAL_FROZEN`.

---

# 1. Evidence and authority classification

Current evidence classification:

| Class | Lv26 roadmap identity | Current authority before this decision | Numeric roadmap values |
|---|---|---|---|
| Knight | penetration damage decay removed; next-enemy knockback scales per penetration | `DESIGNED-NOT-AUTHORITATIVE` | +15% knockback step = candidate-only |
| Rogue | PERFECT adds tracking dagger to nearest secondary enemy | `DESIGNED-NOT-AUTHORITATIVE` | 45% = candidate-only |
| Tank | Heavy leaves temporary enemy slow zone | `DESIGNED-NOT-AUTHORITATIVE` | 1.5s / -25% movement = candidate-only |
| Archer | PERFECT penetration count +2; rear penetration remains full damage | `DESIGNED-NOT-AUTHORITATIVE` | +2 = candidate-only |
| Mage | explosion hitting >=2 enemies propagates secondary explosions to up to 2 enemies | `DESIGNED-NOT-AUTHORITATIVE` | 35% / up to 2 = candidate-only |

Important:
- Lv6 is current Cloudflare combat authority.
- Lv11/Lv16/Lv21 exact v0.16 mechanics remain simulation parity candidates, not current production authority.
- P4-C1 approval must not silently promote Lv11/Lv16/Lv21 to production authority.
- Lv26 roadmap values may be admitted as **P4-C2 provisional simulation inputs** without becoming production numerical freeze.

---

# 2. Proposed global Lv26 effect rules

These rules apply to generated Lv26 effects unless a class section explicitly overrides them.

## 2.1 Effect-rule classification
All five Lv26 mechanics remain P2 **effect rules**, not generic scalar-stat proxies.

Examples:
- penetration decay/count;
- tracking secondary dagger;
- temporary slow zone;
- chain propagation.

Do not replace any of them with a generic `Lv26 +X% power` simulator shortcut.

## 2.2 Root-action ownership
Every Lv26 effect is owned by one valid local root timing action.

Generated Lv26 hits/effects:
- keep `parentActionId` / source-player / source-class attribution;
- do not generate additional EXP;
- do not generate charge;
- do not increment combo;
- do not recursively create another Lv26 effect from themselves;
- do not recursively create Lv6/Lv11/Lv16/Lv21 generators unless a class section explicitly says so;
- do not independently trigger N3.

The root action may still trigger N3 through the already-frozen combo contract independently of Lv26.

## 2.3 PERFECT-containing action semantics
Where a Lv26 skill says `PERFECT`, use the existing legacy composition rule:
- normal PERFECT qualifies;
- Heavy qualifies when either X or Y judgment is PERFECT.

This preserves the existing `containsPerfect` family used by Lv16 parity behavior instead of creating a second hidden timing definition.

## 2.4 Crit inheritance
For generated damage effects derived from a parent attack, default recommendation:

`PARENT_ROLL_INHERITED`

Meaning:
- the parent ordinary proc-crit decision is resolved once;
- generated Lv26 damage derives from that parent outgoing basis;
- generated Lv26 hits do not roll a second ordinary proc crit.

This matches the legacy Lv6/Lv21 generated-hit pattern more closely than independent re-rolls and avoids multiplicative proc growth.

## 2.5 Per-target mitigation
Each realized generated hit applies the target's own mitigation/armor/boss scalar independently under P2.

Armor ignore applies only where an already-defined Archer PERFECT contract explicitly grants it.

## 2.6 Target selection
No Lv26 skill introduces free manual target selection.
Deterministic target selection uses authoritative battlefield state and stable tie-breaking.

## 2.7 Numerical status
If this proposal is approved, retain the roadmap numbers unchanged only as:

`P4C2_PROVISIONAL_SIMULATION_INPUT`

They remain cheap to change after measured P4-C2 evidence and are **not `NUMERIC_FROZEN`**.

---

# 3. Knight Lv26 — FRONTLINE COLLAPSE

Roadmap:
- penetration no longer decays in damage;
- each penetration increases knockback against the next enemy by +15%.

Existing composition:
- Lv11 creates +1 normal / +2 Heavy penetration at 85% secondary damage;
- Lv16 PERFECT-containing action gives +18% damage and +20% knockback;
- Lv21 Heavy allows up to 3 additional penetrations and +20% Heavy damage; legacy extra penetration remains 85%.

## 3.1 Proposed structural contract

1. Lv26 changes the Knight penetration-hit coefficient from legacy `0.85` to `1.00` for all Lv11/Lv21-generated penetration targets.
2. Lv26 does **not** increase penetration count.
3. Primary target knockback remains the action's ordinary effective knockback.
4. Each successful passage through an already-struck enemy increases the knockback multiplier for the next penetration target by an additive +15 percentage points of the action-specific knockback basis:

```text
primary target: ×1.00 Lv26 step
extra target #1: ×1.15
extra target #2: ×1.30
extra target #3: ×1.45
```

5. The Lv26 step resets on every root action; it is not a persistent combo or run stat.
6. Lv16 PERFECT knockback transform, when active, composes before the Lv26 penetration-step multiplier; target/boss knock resistance applies afterward.
7. Penetration hits use `PARENT_ROLL_INHERITED`; no independent crit re-roll.

## 3.2 Alternatives considered

### K-A — first extra target gets no Lv26 knockback increase
Would make the first actual penetration receive no benefit despite the wording that penetration increases knockback against the next enemy.
Not recommended.

### K-B — multiplicative compounding `1.15^n`
Creates unnecessary nonlinear growth and future stacking sensitivity.
Not recommended without evidence.

### K-C — add penetration count at Lv26
Not present in the roadmap and overlaps Archer identity.
Rejected as invention.

## 3.3 Main risks / watches
- Lv21 Heavy becomes full-damage across up to 3 extra targets, which can materially reduce screen lifetime.
- T4 SUPPORTER/SIEGER role exposure may shrink.
- increased knockback may strongly alter CHARGER interruption and SIEGER repositioning.

These are P4-C2 measurement obligations, not reasons to alter the structural identity now.

Reversibility:
- +15% step magnitude = cheap to tune later;
- indexing/stack semantics = medium cost after simulator/runtime adoption, so decide now.

Recommendation: **APPROVE as proposed.**

---

# 4. Rogue Lv26 — CHAIN THROW

Roadmap:
- PERFECT creates an additional tracking dagger against the nearest secondary enemy;
- damage = 45%.

Existing composition:
- Lv6 Double Dagger already uses a delayed second dagger and current Cloudflare fallback targeting infrastructure;
- Lv11 adds native proc-crit chance;
- Lv16 changes qualifying recovery cadence;
- Lv21 Heavy creates main 100% + four 45% follow-up daggers;
- same-target dagger cap is intentionally absent, with boss dagger scalar used instead.

## 4.1 Proposed structural contract

1. A qualifying PERFECT-containing **root action creates exactly one Lv26 Chain Throw dagger**.
2. It is created once per root action, not once per Lv6/Lv21 dagger hit.
3. Preferred target at generation is the nearest live enemy to the authoritative primary impact position, excluding the root primary target.
4. Tie-break is deterministic by distance then stable entity ID/order.
5. If no secondary enemy exists, the Lv26 dagger is not generated; there is no fallback onto the primary target.
6. If the preferred secondary target dies before the tracking dagger resolves, it may retarget once using the same nearest-secondary rule against current authoritative state, still excluding the root primary target.
7. If no valid secondary target exists at resolution, the dagger expires with no hit.
8. Damage coefficient `0.45` is admitted only as a P4-C2 provisional input.
9. Crit policy = `PARENT_ROLL_INHERITED`; no new ordinary proc-crit roll.
10. Rogue boss dagger scalar applies normally if the realized chain target is a boss.
11. The Chain Throw dagger cannot itself generate Double Dagger, Blade Barrage, another Chain Throw, EXP, charge or combo.

## 4.2 Alternatives considered

### R-A — fallback to the primary target
Would convert a secondary-target expansion skill into a hidden single-target DPS increase and blur Rogue's intended branching identity.
Not recommended.

### R-B — one Chain Throw per Lv21 follow-up dagger
Creates a multiplicative generator tree at Lv21+26 and greatly increases event volume.
Rejected.

### R-C — manually choose the secondary target
Conflicts with the core system-driven targeting model.
Rejected.

## 4.3 Main risks / watches
- tracking can opportunistically reach SUPPORTER/SIEGER depending on battlefield geometry, but must not become guaranteed manual backline assassination.
- extra secondary removal can reduce later local timing-turn opportunities and remains part of the active EXP divergence watch.

Reversibility:
- 45% magnitude = cheap;
- one-per-root / fallback semantics = medium cost later, so decide now.

Recommendation: **APPROVE as proposed.**

---

# 5. Tank Lv26 — AFTERSHOCK ZONE

Roadmap:
- Heavy leaves a 1.5s zone;
- enemies in zone move 25% slower.

Existing composition:
- Lv6 increases knockback;
- Lv11 protects the shared wall and is non-stacking across Tanks;
- Lv16 refreshes a non-stacking wall shield;
- Lv21 Heavy becomes broad Ground Impact with strong control.

Current monster movement authority also matters:
- SUPPORTER aura is a server-authoritative movement-rate modifier and is non-stacking within its family;
- CHARGER has ADVANCE/WINDUP/CHARGE state-specific movement;
- SIEGER has ADVANCE then stationary WINDUP/COOLDOWN/shot cadence.

## 5.1 Proposed structural contract

1. Every completed Heavy root action at Lv26 creates one authoritative Stage-local Aftershock Zone.
2. Zone center = the authoritative primary Ground Impact location.
3. Zone footprint inherits the current Ground Impact footprint/geometry contract rather than inventing a second unrelated radius family.
4. Candidate duration = 1.5s.
5. Candidate movement multiplier while covered = `0.75`.
6. Scope = `TEMPORARY / STAGE_LOCAL`.
7. The zone expires at its timer or at `STAGE_SETTLED`, whichever comes first; it is never banked into the next Stage/shop.
8. Mid-Stage reconnect/snapshot must restore a still-live zone from authoritative start/end/owner/geometry state.
9. Aftershock slow uses one non-stacking effect family across overlapping zones/Tanks. Multiple covering zones may extend coverage in time/space, but a target receives at most one -25% magnitude at a time.
10. Cross-family movement composition with SUPPORTER is explicit and deterministic:

```text
phase translational speed
× SUPPORTER movement multiplier if active
× AFTERSHOCK movement multiplier if covered
```

11. FLYER authoritative Y oscillator is not re-timed by Aftershock; the slow modifies the forward/translational movement axis, matching the current SUPPORTER composition model.
12. CHARGER:
   - slow affects ADVANCE and CHARGE translational movement;
   - does not change WINDUP timer;
   - does not itself count as a knockback interrupt/cancel.
13. SIEGER:
   - slow affects ADVANCE/reposition movement;
   - does not alter WINDUP/COOLDOWN/shot cadence or shot damage.
14. Aftershock Zone deals no damage unless a later separate decision changes the skill identity.

## 5.2 Alternatives considered

### T-A — stack -25% for every Tank/zone
Creates duplicate-class control runaway and is inconsistent with the project's existing non-stacking defensive/support family design.
Rejected.

### T-B — invent a new independent zone radius now
Creates a new geometry parameter before evidence and increases rework.
Not recommended; inherit Ground Impact geometry first.

### T-C — slow cancels CHARGER windup/charge
Would turn movement slow into a hidden interrupt and conflict with the existing CHARGER knockback-interrupt contract.
Rejected.

## 5.3 Main risks / watches
- control can extend target lifetime and therefore increase timing-turn/EXP opportunity even while improving survival.
- T4 SIEGER approach/reposition time and SUPPORTER aura exposure can change materially.
- duplicate-Tank team compositions need later P10 validation even with non-stacking magnitude.

Reversibility:
- 1.5s / 25% = cheap numerical candidates;
- stage scope / stacking / monster-phase composition = medium-to-expensive later, so decide now.

Recommendation: **APPROVE as proposed.**

---

# 6. Archer Lv26 — IMPALING SHOT

Roadmap:
- PERFECT penetration count +2;
- preserves 100% rear-target damage.

Existing composition reveals a real redundancy:
- Lv6 already gives up to 2 additional strict-line penetration targets;
- Lv16 PERFECT already sets armor ignore **and preserves 100% penetration damage**;
- Lv21 Heavy creates three locked-line arrows, and the legacy side arrows inherit the Lv6/Lv16 penetration rules.

Therefore, under the existing Lv16 parity semantics, the Lv26 phrase `preserves 100% rear-target damage` does not add a new mechanical transform on a PERFECT action. It repeats an already-active guarantee.

This is a documentation/roadmap overlap, not a reason to invent another damage bonus.

## 6.1 Proposed structural contract

1. On a PERFECT-containing Archer root action, Lv26 adds `+2` to that arrow's maximum additional penetration count.
2. Existing Lv16 armor-ignore and `piercePreserve=100%` remain unchanged.
3. The Lv26 `100% rear-target damage` phrase is treated as a reaffirmation that the new deeper penetrations also inherit Lv16 full-damage preservation; it does **not** create a second damage multiplier.
4. With Lv6+Lv26, a qualifying arrow can therefore hit the primary plus up to 4 additional strict-line targets.
5. On Lv21 Triple Shot, all three arrows inherit the +2 in the same way they already inherit Lv6/Lv16 penetration semantics.
6. Each arrow remains trajectory-locked and non-seeking; target loss does not bend or retarget the line.
7. Penetration hits use parent crit result without a new proc-crit roll.
8. Lv16 armor ignore applies per realized qualifying target under the existing rule.
9. No Lv26 generic damage bonus is added.

## 6.2 Alternatives considered

### A-A — invent an extra rear-target damage bonus because the roadmap repeats 100%
Would silently redesign the skill and double-count an effect already supplied by Lv16.
Rejected.

### A-B — apply +2 only to the center arrow of Triple Shot
Reduces burst power, but introduces a special exception inconsistent with the existing compositional rule where Lv21 side arrows inherit Lv6/Lv16 penetration behavior.
Not recommended without evidence.

### A-C — reopen Lv16 so 100% preservation moves from Lv16 to Lv26
Would unnecessarily rewrite an exact legacy parity milestone and alter the whole Lv16/Lv21 power spine.
Rejected for this gate.

## 6.3 Main risks / watches
- Lv21+Lv26 PERFECT Triple Shot can create very high strict-line throughput.
- T4 screened SUPPORTER/SIEGER role-expression may be shortened dramatically in aligned formations.
- this is a power/authoring watch, not justification for off-line retargeting or hidden damage decay.

Reversibility:
- +2 count = cheap candidate magnitude;
- whether all three arrows inherit it = medium cost after implementation, so decide now.

Recommendation: **APPROVE as proposed, explicitly record the Lv16/Lv26 redundancy rather than inventing a new effect.**

---

# 7. Mage Lv26 — CHAIN EXPLOSION

Roadmap:
- when an explosion catches at least 2 enemies;
- secondary explosions propagate to up to 2 enemies;
- damage = 35%.

This is the highest recursion/event-order risk in P4-C1.

Relevant current behavior:
- Mage root hit can kill a SPLITTER parent;
- children are inserted immediately at the death timestamp;
- current Mage Lv6 splash then enumerates the current monster list in the same action;
- newborn children can therefore be affected by a later effect stage of that root action.

This is valid current ordering and must not be confused with retroactively repeating the already-resolved parent-killing hit.

## 7.1 Proposed bounded structural contract

1. Lv26 trigger is evaluated **once per root Mage action**.
2. The qualifying `root explosion package` is the immediate primary impact plus its immediate Lv6/Lv11 Arcane Burst damage for that action.
3. Trigger condition is met when at least 2 distinct enemies receive damage from that immediate root package, including the primary target.
4. Lv16 delayed Resonance does not independently trigger Lv26.
5. Lv26-generated chain hits do not trigger another Lv26 generation.
6. After the immediate root package and its death/spawn consequences resolve, select up to 2 current live enemies not already damaged by the immediate root package.
7. Selection order = nearest to the original impact center with deterministic stable tie-break.
8. Newly spawned SPLITTER children may be selected if they exist at this post-root selection point and were not already in the root-hit set. This is a forward secondary effect, not retroactive damage.
9. Each selected target receives exactly one 35% Chain Explosion hit.
10. For Lv26, the propagated explosion is a bounded target-centered secondary hit, not a new recursive AoE generator. It may use explosion presentation/VFX, but it does not damage an unbounded neighborhood.
11. The two chain targets cannot duplicate one another.
12. If fewer than 2 eligible targets exist, only the available targets are hit; there is no same-target fallback.
13. Crit policy = `PARENT_ROLL_INHERITED`; no independent proc-crit re-roll.
14. Each chain target applies its own armor/mitigation/boss scalar.
15. Chain hits do not create Arcane Burst, Resonance, another Chain Explosion, EXP, charge or combo.
16. Lv21 Greater Orb affects the root explosion's actual damage/radius and therefore can make the `>=2` trigger more likely, but does not turn the Lv26 propagated hits into ×1.6 AoE blasts.

## 7.2 Alternatives considered

### M-A — every propagated target becomes a full AoE center
More spectacular, but creates target-multiplication and overlap questions immediately, increases SPLITTER child-erasure risk and approaches the later Lv31 cascading-explosion identity.
Not recommended for Lv26 first closure.

### M-B — allow Resonance and chain explosions to trigger more chains
Creates recursive generation and event-volume instability contrary to the project's bounded deterministic capability rules.
Rejected.

### M-C — freeze chain targets before root damage/death resolution
Avoids newborn-child interaction, but conflicts with current Mage/SPLITTER action-order precedent and produces stale target sets after deaths.
Not recommended.

### M-D — require two secondary splash targets, excluding the primary, before activation
Would require at least three total immediate victims and relies on an implementation-facing distinction that is difficult for players to read.
Not recommended; use two distinct root-package victims total.

## 7.3 Main risks / watches
- SPLITTER children can become post-death chain targets under the proposed event order.
- dense packs may still lose population quickly even without recursive AoE.
- Mage already showed SPLITTER role-expression sensitivity in prior all-20 evidence.
- stronger density removal can further reduce timing-turn opportunity under the active EXP watch.

These must be explicit P4-C2 targeted fixtures.

Reversibility:
- 35% / max 2 = cheap candidate numbers;
- single-generation and target-reuse rules = expensive to change after downstream calibration, so decide now.

Recommendation: **APPROVE the bounded one-generation target-propagation contract.**

---

# 8. Cross-class / monster / campaign consistency review

## 8.1 P1 lifecycle
PASS under proposal.
- only Tank creates a persistent-in-time object;
- it is explicitly Stage-local and obeys `STAGE_SETTLED`;
- no Lv26 effect changes run reset/persist semantics.

## 8.2 P2 modifier/effect pipeline
PASS under proposal.
- all Lv26 mechanics remain effect rules;
- parent action attribution retained;
- generated hit crit policy explicit;
- target mitigation remains per target;
- no hidden scalar proxy introduced.

## 8.3 P3 deterministic persistent kernel semantics
PASS structurally.
P4-C2 must add deterministic fixtures for:
- Tank zone snapshot/resume and Stage settlement;
- Rogue target death/retarget;
- Mage death/spawn/chain ordering;
- penetration attribution for Knight/Archer.

## 8.4 Monster role-expression
No unavoidable structural contradiction found, but the proposal creates meaningful watches:
- Knight/Archer may shorten screened backline role windows;
- Rogue may opportunistically reach secondary special units;
- Tank changes CHARGER/SIEGER timing without hard-canceling them;
- Mage remains the highest SPLITTER population-expression risk.

TEACH encounters must continue to provide minimum role expression before skilled counterplay removes the threat.

## 8.5 T4 Stage31–39
The current macro skeleton intentionally provides:

```text
31–33 combined SUP/SI low-moderate
34–36 Lv26 transition observation
37–39 post-Lv26 high-pressure synthesis
```

The proposal is compatible with this structure and gives P4-C2 an explicit place to measure screen lifetime, aura uptime, SIEGER opportunity and class-specific late-power shifts.

## 8.6 Lv26 -> Lv31 runway
No proposal turns Lv26 into a replacement for the intended Lv31 identity:
- Knight Lv31 can still escalate to battlefield-scale double wave;
- Rogue Lv31 remains rapid 8-dagger storm rather than one secondary dagger;
- Tank Lv31 remains field-wide shock/barrier rather than local zone;
- Archer Lv31 remains unlimited battlefield-line penetration rather than +2 count;
- Mage Lv31 remains multi-stage/cascading collapse rather than bounded one-generation propagation.

This separation is important for preserving Stage41–45 Lv31 ascension value.

## 8.7 Future T5+ extensibility
No Lv26 contract assumes the lifetime roster is only the current nine monsters.
All targeting/control semantics operate on capability-agnostic authoritative enemy state.
Future monsters will still need their own role-expression and interaction audit.

## 8.8 EXP / multiplayer feedback
No EXP semantics are changed here.
P4-C2 may measure how Lv26 changes action opportunity under the current provisional per-valid-turn baseline.
Final EXP convergence remains deferred to P10R.

---

# 9. Recommended option set

## Option A — preserve roadmap identities and approve the bounded compositional contracts above
**Recommended.**

Benefits:
- smallest semantic change from existing design;
- respects Lv6–21 composition and P2/P3 authority;
- closes deterministic ambiguity before simulation;
- catches Archer redundancy without inventing extra power;
- bounds Mage/Rogue generator trees;
- keeps numeric values reversible.

## Option B — literal roadmap only, leave execution ambiguities open until P4-C2
Not viable for trustworthy simulation.
The simulator would have to silently choose targeting/stack/recursion rules, violating the user decision gate.

## Option C — redesign/expand Lv26 for larger spectacle now
Examples would include Archer extra rear-damage bonus, Rogue per-dagger chain generation or Mage recursive AoE chains.
Not recommended: no evidence requires a redesign, it increases novelty/power coupling and raises rework cost before P4-C2 evidence exists.

---

# 10. Approval scope requested

Requested user approval is intentionally narrow.

Approve **Option A** as the P4-C1 structural direction, including:
- global root-action / no-recursion / attribution rules;
- Knight full-damage penetration + additive +15% next-target knockback-step semantics;
- Rogue exactly-one secondary tracking dagger with no primary fallback;
- Tank Ground-Impact-footprint Stage-local non-stacking slow-zone semantics and explicit monster-phase composition;
- Archer PERFECT +2 penetration inheritance across all Triple Shot arrows, with the existing Lv16 100% preservation treated as already satisfied rather than duplicated;
- Mage one-generation, max-two, non-root-hit target propagation with no recursive AoE chain.

Also authorize the existing roadmap values only as **P4-C2 provisional simulation inputs**:
- Knight +15% step;
- Rogue 45%;
- Tank 1.5s / 25% slow;
- Archer +2;
- Mage 35% / max 2.

This approval would **not** authorize:
- production implementation;
- numerical production freeze;
- Lv11/Lv16/Lv21 production migration;
- Lv31 mechanics;
- final EXP semantics/thresholds;
- Stage Quality Budget;
- shop/BaseHP/stars/achievements/boss/multiplayer values;
- exact campaign authoring.

---

# 11. Required next step after approval

Only after explicit user approval:
1. record a P4-C1 approved structural contract;
2. mark P4-C1 structurally complete;
3. admit the roadmap values as bounded P4-C2 simulation inputs only;
4. execute P4-C2 deterministic Lv26 feedback with targeted interaction fixtures;
5. keep all R2 EXP watches active;
6. report before advancing to P4-D1.

Until approval:

```text
P4-C1 = PROPOSED / AWAITING USER APPROVAL
P4-C2 = BLOCKED
production changes = UNAUTHORIZED
```
