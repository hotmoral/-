# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory, copied SHA values, or this file alone.
Always fetch live remote first.

Read/check in this order:
1. branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_6.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/87_P4C1_LV26_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md`
8. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
9. `SKILL_PLAN_LV6_31.md`
10. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
11. `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
12. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
13. `legacy-game-structure/23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
14. `legacy-game-structure/26_MODEL_A_T1_T4_MACRO_SKELETON_V0_1.md`
15. `legacy-game-structure/69_SKILLED_V2_CENTRAL_ALL20_EXECUTION_REPORT_V0_1.md`
16. `BALANCE_SIM_REPORT_V7_V016_EXACT.md` and legacy `v016-core.js` as parity/source evidence
17. current production source/branch head and calibration-harness branch head
18. historical P4-B diagnostic chain `81 -> 83 -> 84` only as needed for EXP-context recovery

Then follow document 86's structural-spine and current-phase review rules.

Important:
- `legacy-game-structure/README.md` is a useful corpus/history map but contains older execution-order / `NEXT` references. Do not treat those as current authority when they conflict with live status, latest approved routing or the active dependency plan.
- Do not re-run closed P1/P2/P3 or prior PASS/APPROVED checks merely because a new session started. Revalidate only under document-86 triggers.
- proposal 87 is **not approved/frozen** merely because it exists.

Live remote always wins.

---

# Branch checkpoints at this handoff sync

Planning branch:
- `timing-defense-workspace`
- exact final HEAD must be re-fetched after all sync commits.

Production branch:
- `timing-defense-cloudflare-do-poc`
- verified during P4-C1 review: `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized.

Calibration harness branch:
- `timing-defense-skilled-v2-harness-v01`
- last verified checkpoint: `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- no P4-C1 work required a harness change.

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE**

R2 routing is USER APPROVED.

Current internal state:

```text
P4-C1 evidence recovery = COMPLETE
P4-C1 cross-stage review = COMPLETE
P4-C1 proposal 87 = PROPOSED / AWAITING USER APPROVAL
P4-C1 structural freeze = NOT YET
P4-C2 = BLOCKED_PENDING_USER_APPROVAL
```

Do not start P4-C2 before the user explicitly approves or modifies proposal 87.

---

# R2 meaning remains unchanged

Current pure per-valid-turn EXP remains a **provisional diagnostic baseline only**.

Still provisionally true for measurement:
- valid completed local timing turn gives EXP;
- Heavy X+Y gives one combined-tier award;
- timing quality matters;
- `XP_CREDIT` is dimensionless calibration space;
- one universal EXP curve remains preferred;
- no hidden class/Tier XP multipliers.

Not approved/frozen:
- pure per-turn as final launch EXP semantics;
- Stage Quality Budget / prior Option D;
- exact XP values or milestone thresholds;
- player-visible EXP scale;
- player-count EXP correction.

Mandatory active watches:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

Future progression analysis must continue to consider Stage reach, wall-clock reach, clear/fail/retry, wall attrition, team composition and player-count effects together.

---

# P4-C1 evidence recovered

Authority boundary:
- Lv6 = current Cloudflare combat authority.
- Lv11/Lv16/Lv21 = exact v0.16 legacy parity candidates for simulation only; not current production authority.
- all Lv26 roadmap identities = `DESIGNED-NOT-AUTHORITATIVE` before this user decision.

Roadmap Lv26 identities:
- Knight — Frontline Collapse: remove penetration damage decay; next-target knockback +15% per penetration.
- Rogue — Chain Throw: PERFECT adds nearest-secondary tracking dagger at 45%.
- Tank — Aftershock Zone: Heavy leaves 1.5s zone, movement -25%.
- Archer — Impaling Shot: PERFECT penetration +2 and rear penetration 100%.
- Mage — Chain Explosion: root explosion catching >=2 propagates up to 2 secondary explosions at 35%.

Source-level findings:
- legacy v0.16 implements combat only through Lv21.
- Archer Lv16 already gives PERFECT armor ignore + 100% preserved penetration damage; therefore Lv26's repeated 100% clause is mechanically redundant unless deliberately redesigned.
- current Mage/SPLITTER ordering allows a SPLITTER parent to die, children to spawn, then a later same-root-action Mage effect stage to see those children. This ordering is real current behavior and makes Lv26 chain-generation semantics material.
- SUPPORTER movement is authoritative/non-stacking and composes with CHARGER phase movement.
- SIEGER shot cadence is distinct from approach movement; movement effects must not silently alter firing cadence.

---

# Proposal 87 recommendation — Option A

Preserve the roadmap identities and close only the missing deterministic semantics.

## Global
- Lv26 mechanics remain P2 effect rules; no generic Lv26 power scalar.
- one root local timing action owns each generated Lv26 effect.
- generated Lv26 effects do not add EXP/charge/combo and do not recursively generate class-skill trees.
- generated damage uses parent crit result without a second ordinary proc-crit roll by default.
- mitigation/armor/boss transforms remain per target.
- no manual targeting is introduced.

## Knight
Recommended:
- Lv26 converts legacy extra penetration coefficient 85% -> 100%.
- does not add penetration count.
- primary target uses base action knockback; extra penetration targets use additive step multipliers `1.15 / 1.30 / 1.45` for extra targets #1/#2/#3.
- Lv16 PERFECT knockback transform composes before the Lv26 step; target resistance after it.

## Rogue
Recommended:
- exactly one Chain Throw dagger per qualifying PERFECT-containing root action, not per dagger/hit.
- nearest live non-primary enemy relative to primary impact is preferred target.
- no secondary target -> no dagger; no primary fallback.
- if preferred target dies before resolution, allow one deterministic secondary retarget; still no primary fallback.
- 45% remains provisional simulation input.

## Tank
Recommended:
- each completed Heavy creates one authoritative Stage-local zone centered on Ground Impact.
- inherit Ground Impact footprint rather than invent independent zone geometry now.
- 1.5s / -25% are provisional simulation inputs.
- same-family slow magnitude is non-stacking across zones/Tanks.
- SUPPORTER speed and Aftershock slow compose deterministically as separate movement-rate effects.
- CHARGER slow affects ADVANCE/CHARGE movement but does not cancel WINDUP/charge by itself.
- SIEGER slow affects approach/reposition movement, not windup/cooldown/fire cadence.
- zone clears at expiry or `STAGE_SETTLED`; reconnect restores it if still live mid-Stage.

## Archer
Recommended:
- PERFECT adds +2 maximum additional penetration targets.
- existing Lv16 armor-ignore + 100% penetration preservation remains the only 100%-preservation transform; do not invent a second Lv26 damage bonus.
- all three Lv21 Triple Shot arrows inherit +2 because legacy side arrows already inherit Lv6/Lv16 penetration semantics.
- locked-line/no-homing/no-retarget rule remains.

## Mage
Recommended:
- evaluate Lv26 once per root Mage action.
- root immediate primary + Arcane Burst package hitting >=2 distinct enemies qualifies; primary counts.
- Resonance does not independently trigger Lv26.
- after immediate root package/death/spawn consequences, select up to 2 current live enemies not already hit by that root package.
- newly spawned SPLITTER children may be eligible if alive and not already root-hit; this is forward secondary resolution, not retroactive parent damage.
- each selected target receives one 35% chain hit.
- no recursive AoE chain, no same-target fallback, no chain-generated Arcane Burst/Resonance/another Chain Explosion.
- 35% / max 2 remain provisional simulation inputs.

---

# Why Option A is recommended

- smallest change from the existing skill roadmap;
- preserves role identities instead of equalizing DPS;
- aligns with P2 effect/attribution semantics;
- respects P3 Stage settlement and deterministic state requirements;
- bounds Rogue/Mage generator growth;
- catches Archer's real Lv16/Lv26 semantic overlap early instead of double-counting damage;
- leaves numerical coefficients cheap to tune after P4-C2 evidence;
- keeps Lv31 identities meaningfully above Lv26;
- does not overfit to the current nine-monster roster.

Alternatives rejected or not recommended:
- leave ambiguities open and let the simulator choose silently;
- per-dagger Rogue Chain Throw generation;
- stacked Tank slow magnitude;
- extra Archer rear-damage bonus invented from redundant wording;
- recursive Mage chain/AoE generation.

---

# Required user action

User must explicitly choose one:

```text
A — approve proposal 87 Option A as P4-C1 structural direction
B — modify one or more class rules
C — request additional analysis before decision
D — reject/reopen one or more Lv26 identities
```

Approval of A would also authorize the existing roadmap values only as `P4C2_PROVISIONAL_SIMULATION_INPUT`, **not numerical production freeze**.

After approval, create a separate approved P4-C1 contract before executing P4-C2.

---

# Required P4-C2 watches after approval

- Knight/Archer T4 screen/backline role-expression and SIEGER/SUPPORTER exposure.
- Rogue secondary-target behavior and attack-opportunity feedback.
- Tank zone state, snapshot/resume, Stage settlement, CHARGER/SIEGER/SUPPORTER movement interactions.
- Mage SPLITTER death/spawn/chain order and population-expression preservation.
- all five classes' timing-turn opportunity change under the provisional EXP baseline.
- T4 Stage34–36 transition and 37–39 post-Lv26 high-pressure synthesis.

P4-C2 is diagnostic only and must not claim final EXP balance.

---

# Stable game truths

- 5 classes; independent class Tier progression.
- same Tier/Stage combat content across classes.
- 1 Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad permanent account growth.
- achievements = targeted/cross-class permanent progression.
- recoverable soft walls intended; hard class lockout forbidden.
- Model A bounded roster ladder: T1 G/R/B; T2 +SH/F; T3 +C/SP; T4 +SUP/SI; T5+ future.
- current 9 monsters are foundation, not lifetime roster.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45 direction.
- Stage46–49 post-Lv31 mastery; Stage50 final application.
- actual timing input is constant-speed line sweep across Timing Square; player taps to register coordinate.
- ordinary difficulty should mainly come from encounter pressure/complexity, not simply shrinking PERFECT zone or increasing sweep speed.

---

# Do not yet

- mark proposal 87 approved without explicit user decision;
- start P4-C2;
- change/deploy production v0.45 gameplay;
- activate Stage Quality Budget;
- freeze pure per-turn EXP as final;
- add hidden class/Tier EXP multipliers;
- freeze exact EXP anchors;
- begin Lv31 structural freeze;
- freeze exact shop/BaseHP/permanent-progression/boss/multiplayer values;
- author exact 200 launch Stages.

This handoff boundary intentionally stops **at the P4-C1 user decision gate after substantive structural review**.
