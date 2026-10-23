# Timing Defense — P5 Run Coin / Shop Authority Recovery V0.1

Date: 2026-10-23 KST  
Status: **AUTHORITY RECOVERY COMPLETE / MATERIAL STRUCTURAL DECISIONS IDENTIFIED / NO VALUES APPROVED / NO PRODUCTION CHANGE**

Authority / evidence:
- `70_SYSTEM_DEPENDENCY_AND_CALIBRATION_ORDER_REVIEW_V0_1.md`
- `72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`
- `74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `01_META_PROGRESSION.md`
- `05_LEGACY_EVIDENCE_MAP.md`
- `06_SIMULATION_CALIBRATION_PLAN.md`
- `../../DESIGN_DECISIONS.md`
- `../../V035_RECONNECT_SHOP_STAGE2_REPORT.md`
- production source `timing-defense-cloudflare-do-poc` at `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production predecessor `timing-defense-server/server.js`
- production inheritance chain `timing-defense-cloudflare-poc/src/v035-entry.js -> ... -> v045-sieger-entry.js`

---

# 0. Purpose

P5 must not copy prototype shop values into the 50-Stage production design by inertia.

This review separates:
- user-approved structural truth;
- legacy implemented/reference behavior;
- current live implementation behavior;
- unresolved production decisions.

No shop value or cadence is approved by this document.

---

# 1. Authority matrix

| Topic | Current recovered state | Authority classification | P5 consequence |
|---|---|---|---|
| run coin exists | run-local progression layer | USER_CONFIRMED_STRUCTURE | keep |
| shop ranks exist | persist across Stage/shop, reset new Tier attempt | USER_APPROVED P1 | keep |
| coin resets on new Tier attempt | yes | USER_APPROVED P1 | keep |
| shop purchase is run-only | yes | USER_CONFIRMED_STRUCTURE | keep |
| stage transition heals automatically | no | USER_APPROVED P1 | keep |
| explicit shop healing | allowed but undecided | OPEN | P5 decision |
| shop after every Stage | implemented through legacy Stage1-3 | LEGACY_IMPLEMENTED_REFERENCE / OPEN for 50 Stage | P5 decision |
| personal human coin | implemented | LEGACY_IMPLEMENTED_REFERENCE, consistent with concept | strong candidate |
| monster kill coin | only killing human receives monster reward in legacy/current inherited shop kernel | LEGACY IMPLEMENTATION ONLY | do not auto-promote |
| Stage-clear coin | every human receives `55 + stage*12` in v0.35 kernel | LEGACY IMPLEMENTATION ONLY | candidate source, values open |
| ATK category | +8%/rank prototype | category repeated; value open | category candidate |
| CRIT category | +2pp/rank prototype | category repeated; value open | category candidate |
| CRIT DMG category | +15% proc multiplier bonus/rank prototype | category repeated; value open | category candidate |
| WALL HP category | +100 max and current / rank prototype | category repeated; heal semantic open | material decision |
| DEF category | +2.5pp shared DR/rank, all human ranks summed, prototype cap60% | category repeated; multiplayer ownership/cap open | material decision |
| KNOCKBACK category | +10%/rank prototype | implemented, P2 scalar family exists | category candidate |
| max rank10 | implemented | LEGACY VALUE | finite cap required, exact cap open |
| cost curve `[40..625]` | implemented with category multipliers | LEGACY VALUE | simulation seed only, no freeze |
| per-human independent buying | yes | LEGACY IMPLEMENTED and architecture-compatible | strong candidate |
| all-human READY | yes | LEGACY IMPLEMENTED | UX/flow candidate, not balance authority |
| host NEXT | yes | LEGACY IMPLEMENTED | final UX not required for P5 balance contract |
| AI shop ownership | AI does not purchase human shop ranks in prototype | LEGACY IMPLEMENTED / later P10 concern | defer unless needed |

---

# 2. Stable upstream constraints

## 2.1 P1 run-state

Within one Tier attempt:
- coin persists;
- shop ranks persist;
- BaseHP/max persist;
- no Stage-boundary auto-heal;
- retry from run failure resets Stage1 / Lv1 / EXP0 / coin0 / shop ranks0 / BaseHP full.

Therefore P5 cannot make shop transition itself a hidden heal/reset.
Any repair must be an explicit purchased/rewarded mechanic.

## 2.2 P2 modifier semantics

RUN SHOP sources belong in the same typed stat families as account/permanent sources:

```text
ATK      -> attackPct / attackFlat family
CRIT     -> critChancePp
CRIT DMG -> critDamageBonus
WALL HP  -> wallHpFlat / wallHpPct
DEF      -> generic wallDamageReductionPp
KNOCK    -> knockbackPct
```

Ordinary same-stat percentage sources are additive by default, not automatically multiplicative merely because they are shop effects.

Unique class/team defense remains separate from generic DEF.

---

# 3. Current implementation truth

The v0.35 shop implementation is real, authoritative for its prototype slice, and inherited into later capability slices.

Implemented grammar:

```text
UPGRADE_KEYS = atk / crit / critdmg / hp / def / knock
finite 10 ranks each
escalating costs
individual human coin and ranks
shop READY per human
all humans READY -> canNext
```

Current/inherited combat mapping includes:

```text
ATK: attack raw × (1 + rank*.08)
CRIT: proc chance += rank*.02
CRIT DMG: proc multiplier += rank*.15
KNOCK: knockback base × (1 + rank*.10)
DEF: sum human DEF ranks -> shared generic wall DR, prototype cap .60
HP: +100 shared max AND +100 current HP immediately
```

The latest SIEGER capability path still reads summed human DEF shop ranks when computing wall-shot damage, confirming that the shop grammar remains live in the v0.45 inheritance chain.

However, all exact values/production ownership semantics remain unfrozen.

---

# 4. Material contradiction / risk A — last-hit coin economy

Current legacy kill reward:

```text
monster dies
-> killing human only receives monster reward coin
```

This is dangerous under the now-approved class asymmetry.

Feedback loop:

```text
offensive class gets more last hits
-> more personal coin
-> more ATK/CRIT investment
-> higher kill share
-> still more coin
```

Tank/control/support contribution can improve team survival while earning fewer kill coins.

This risks:
- class-economy unfairness;
- snowball;
- kill-steal incentives;
- team-composition-dependent shop reach;
- contamination of P4 EXP/skill reach through shop feedback.

Therefore `killer-only coin` must **not** be promoted to P5 production structure without an explicit user decision.

---

# 5. Material contradiction / risk B — WALL HP is also healing

Current implementation:

```text
buy HP
-> baseHpMax +=100
-> baseHp +=100 up to max
```

This is not merely `wallHpFlat`; it is also an explicit repair event.

P1 allows explicit shop healing, but did not approve its amount/cadence.

In a 50-Stage attrition run this matters greatly:
- max-only HP has little immediate value if no repair source exists;
- max+current HP creates a deliberate recovery lever;
- too-cheap repair can erase accumulated Stage attrition and the Stage49->50 reserve pressure;
- too-weak repair can make HP investment unattractive after damage is already taken.

P5 must explicitly choose the semantic before tuning values.

---

# 6. Material contradiction / risk C — shared DEF/HP and player-count scaling

Current prototype:

```text
DEF ranks from all humans add into one shared generic wall DR bucket
HP purchases from any human directly increase one shared wall max/current state
```

This is structurally coherent with a shared wall, but it creates player-count leverage:
- more humans can collectively buy more shared defense/HP;
- personal offensive purchases remain player-specific;
- the marginal value of a defensive purchase can depend on team size and composition.

This does not mean the shared contribution model is wrong.
It means exact values/caps cannot be frozen in P5 without P10 multiplayer scaling.

Recommended scope boundary:
- P5 may define ownership/composition semantics;
- P10/P10R handles final player-count scaling and timebase/economy convergence.

---

# 7. Material decision / risk D — shop cadence across 50 stages

Legacy implementation evolved from Stage1 shop to Stage1-3 shop-after-every-clear.
This is real usability/architecture evidence.

But the legacy evidence map explicitly classifies:

```text
whether a 50-Stage production run needs a shop after every Stage = OPEN_DECISION
```

A 50-Stage Tier changes the pacing cost dramatically.

Tradeoff:

```text
EVERY_STAGE
+ high control / frequent adaptation / clear spend feedback
- up to 49 repeated shop interruptions / multiplayer wait friction

CHECKPOINT_ONLY
+ faster flow
- long stretches where coin has no tactical use / weaker run-growth feedback

EVERY_STAGE_AVAILABLE_BUT_FAST_CONTINUE
+ preserves continuous tactical growth
+ purchase is optional
+ can minimize interruption with lightweight intermission
- still requires careful multiplayer ready/timeout UX later
```

P5 requires a material direction before simulation.

---

# 8. Category recovery result

The six-category prototype is structurally coherent with P2 and current class identities:

```text
ATK
CRIT CHANCE
CRIT DAMAGE
WALL HP / FORTIFICATION
DEFENSE
KNOCKBACK
```

No seventh category is currently required to begin P5.

Reasons:
- covers offensive scalar, crit specialization, shared attrition survival and control;
- maps directly to approved P2 stat families;
- exposes different class utility rather than forcing one generic damage stat;
- existing code/UI already proves the grammar is implementable.

Exact values, rank cap and costs remain open.

---

# 9. Rank / cost structural recommendation

Keep structural form only:

```text
finite ranks per category
monotonically rising marginal cost
no infinite compounding
no automatic reset between Stages
reset at new Tier attempt
```

Use legacy:

```text
rank cap10
BASE_COST [40,65,100,145,200,265,340,425,520,625]
category multipliers
```

only as first simulation seeds, not approval.

---

# 10. Exact unresolved P5 decisions

The authority recovery reduces the immediate user decision gate to three linked structural choices:

1. **shop cadence / interruption model**;
2. **coin credit ownership for monster deaths**;
3. **WALL HP purchase repair semantic**.

Shared DEF/HP contribution to the common wall is recommended structurally but exact multiplayer scaling remains deferred.

Everything else can proceed as bounded candidate/simulation work once these three choices are approved.

---

# 11. No production change

This recovery does not modify:
- production source;
- shop values;
- coin rewards;
- Stage flow;
- multiplayer behavior.

P5 remains design/simulation only until a later explicit implementation authorization.
