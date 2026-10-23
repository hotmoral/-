# Timing Defense — Session Handoff

Updated: 2026-10-23 KST

## Recovery rule
Never reconstruct current state from chat, memory, copied SHA values or this file alone.
Always fetch live remote first.

Read/check in this order:
1. live branch `timing-defense-workspace` HEAD
2. `PROJECT_STATUS.md`
3. `NEXT_WORK.md`
4. `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
5. `legacy-game-structure/data/system_dependency_calibration_order_v0_8.yaml`
6. `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`
7. `legacy-game-structure/88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`
8. `legacy-game-structure/89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
9. `legacy-game-structure/data/p4c2_lv26_bounded_feedback_v0_1.json`
10. `legacy-game-structure/90_P4D1_LV31_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md`
11. `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`
12. `SKILL_PLAN_LV6_31.md`
13. `legacy-game-structure/20_LV31_MASTERY_PLAY_WINDOW_V0_1.md`
14. `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
15. `legacy-game-structure/45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
16. `legacy-game-structure/23_SKILL_MONSTER_NOVELTY_COLLISION_AUDIT_V0_1.md`
17. `legacy-game-structure/26_MODEL_A_T1_T4_MACRO_SKELETON_V0_1.md`
18. current production source/branch head and calibration-harness head
19. older P4-A/P4-B/P3 evidence only as needed for causal context/revalidation triggers

Then follow document 86's structural-spine and current-phase rules.

Important:
- `legacy-game-structure/README.md` is a corpus/history map, not current execution authority when its old `NEXT` conflicts with live status/v0.8.
- do not re-run closed P1/P2/P3/P4-C1/C2 solely because a new session starts.
- proposal 90 is **not approved/frozen** merely because it exists.
- production remains unchanged unless separately authorized.

Live remote always wins.

---

# Branch checkpoints at this handoff sync

Planning:
- branch `timing-defense-workspace`
- final exact HEAD must be re-fetched after all sync commits; copied SHA is only a checkpoint.

Production:
- branch `timing-defense-cloudflare-do-poc`
- last verified HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- gameplay/numerical changes unauthorized.

Calibration harness:
- branch `timing-defense-skilled-v2-harness-v01`
- last verified HEAD `063a9ac9986ba9a8028beb31a5b4c733c9bfa863`
- no P4-C/D planning work changed it.

---

# Current phase / exact boundary

```text
P4-C1 = USER_APPROVED_STRUCTURAL_COMPLETE
P4-C2 = COMPLETE / PASS_WITH_WATCHES
P4-D1 proposal 90 = PROPOSED / AWAITING USER APPROVAL
P4-D1 structural freeze = NO
P4-D2 = BLOCKED_PENDING_P4D1_USER_APPROVAL
production changes = UNAUTHORIZED
```

Current exact next action:
**user decision on proposal 90 Option A**.

---

# R2 / EXP state remains unchanged

Current pure per-valid-turn EXP is a **provisional diagnostic baseline only**.

Not frozen:
- final pure-per-turn semantics;
- Stage Quality Budget / Option D;
- exact XP_CREDIT vector/thresholds;
- exact A6/A11/A16/A21/A26/A31;
- player-visible scale;
- hidden class/Tier/player-count correction.

Mandatory P10R after credible current-roster multiplayer scaling remains active.

Active original watches:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

---

# P4-C1 approved Lv26 structure

Authority:
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`

Approval meaning:
- structural execution semantics are the active P4 contract;
- roadmap coefficients are provisional simulation inputs, **not production numerical freeze**;
- later evidence may transparently reopen them, but no silent semantic drift.

Key approved rules:

## Global
- Lv26 remains P2 effect rules, never a generic power scalar.
- generated effects belong to one root action.
- no extra EXP/charge/combo; no independent N3; no recursive class-skill generator tree.
- default generated damage crit policy = parent-roll inherited.
- per-target mitigation remains explicit.

## Knight
- additional penetration coefficient 0.85 -> 1.00 at Lv26.
- no extra penetration count.
- extra-target knockback ladder `1.15 / 1.30 / 1.45` provisional.

## Rogue
- max one Chain Throw per qualifying PERFECT-containing root action.
- deterministic nearest non-primary target; no primary fallback; one retarget if original secondary dies.

## Tank
- Heavy creates one Ground-Impact-footprint Stage-local Aftershock.
- provisional 1.5s / movement×0.75.
- same-family slow nonstacking.
- SUPPORTER×Aftershock compose as separate movement multipliers.
- CHARGER WINDUP and SIEGER firing timers are not slowed.

## Archer
- PERFECT +2 additional penetration targets.
- Lv16 remains the existing armor-ignore/100%-preservation transform.
- Triple Shot arrows inherit the extension.
- strict locked-line/no homing preserved.

## Mage
- root immediate package hitting >=2 distinct enemies can create up to2 one-generation chain hits.
- death/spawn consequences resolve before chain target selection.
- newborn SPLITTER children can be eligible if alive/not root-hit.
- no recursive Burst/Resonance/Chain tree.

---

# P4-C2 evidence and interpretation

Authority:
- `89_P4C2_LV26_BOUNDED_PROVISIONAL_POWER_FEEDBACK_V0_1.md`
- `data/p4c2_lv26_bounded_feedback_v0_1.json`

Method boundary:
- paired formula-fidelity sensitivity lane uses historical five-monster pressure vocabulary only;
- it is directional Lv21→Lv26 evidence, not current 9-roster production balance;
- accepted run used named substreams `STAGE/JUDGMENT/COMBAT_PROC/AI` after rejecting an earlier shared-RNG reconstruction that introduced causal noise;
- 13,440 paired comparison rows.

Central sensitivity direction:

```text
Knight  local actions -0.71%, damage +7.66%
Rogue   local actions -2.49%, damage +12.05%
Tank    local actions +0.29%, damage +1.01%
Archer  local actions -4.05%, damage +4.42%
Mage    local actions -3.75%, damage +6.70%
```

Meaning:
- offensive Lv26 generally causes more kill efficiency and fewer later local timing/EXP opportunities;
- Tank control can slightly extend target lifetime/opportunity;
- no final EXP conclusion follows.

Current-roster structural probes:
- Knight/Archer: screen/backline erasure watch.
- Tank: Aftershock can prolong SIEGER pre-standoff exposure, potentially reducing first-shot opportunity without changing fire cadence.
- Mage: strongest watch. SPLITTER children spawn immediately at parent death; approved Lv26 chain selects afterward. GREAT+ Heavy chain can one-shot provisional 120-HP child test anchors, so TEACH/STANDARD SPLITTER transformation readability must later be checked.

Additional watches:

```text
LV26_T4_ROLE_EXPRESSION_WATCH
LV26_MAGE_SPLITTER_ORDERING_WATCH
LV26_TANK_MOVEMENT_COMPOSITION_WATCH
```

P4-C2 verdict:
`COMPLETE / PASS_WITH_WATCHES`.
No current reason to reopen P4-C1.
No numerical freeze authorized.

### Replayability boundary
P4-C2 report and machine-readable summary are committed, but this bounded directional pass does not currently expose a committed one-command exact replay runner.
Do not later promote P4-C2 into exact numerical-freeze/regression authority without first materializing an exact committed replay runner and re-running it.
This limitation does **not** block current P4-D1 structural analysis because P4-C2 is being consumed only as bounded directional evidence.

---

# P4-D1 recovered authority

`SKILL_PLAN_LV6_31.md` establishes the final identities, while `PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md` classifies all Lv31 implementation-critical details as `UNRESOLVED`.

Roadmap:
- Knight — Heaven-Splitting Slash: huge double wave / broad penetration / major knockback.
- Rogue — Dagger Storm: 8 tracking daggers over roughly 0.5s.
- Tank — Absolute Barrier: battlefield-wide shockwave + 250 wall shield for 6s candidate.
- Archer — Sky-Piercing Arrow: huge/high-speed strict-line battlefield penetration without target cap + armor ignore.
- Mage — Arcane Collapse: large magic circle + three-stage blast + chained secondary explosions.

User-confirmed mastery structure:

```text
Lv31 target acquisition = Stage41..45
Stage46..49 = post-Lv31 mastery-use band
Stage50 = final application, not first use/tutorial
```

Stage41–45 must remain viable both for players who have just unlocked Lv31 and those still at Lv26 or below.

---

# Proposal 90 — recommended Option A

## Global: P×P final-template replacement with lower-kit continuity
Recommended because fully additive interpretation causes generator explosion, while wiping all lower-kit behavior breaks progression continuity.

Rule:
- Lv31 P×P builds the final class attack template instead of stacking duplicate Lv21/Lv26 same-action generators.
- lower passive/scalar transforms continue where semantically relevant.
- lower duplicate hit generators are suppressed unless explicitly incorporated.
- one root action owns the package; no extra EXP/charge/combo/N3; deterministic attribution; per-target mitigation.

## Knight K-B — bounded broad double wave
- two sequential broad crescent waves.
- Knight Heavy corridor, not Archer unlimited strict ray.
- each wave primary + up to3 additional penetrations.
- second wave remains in same authoritative corridor; no unrelated free homing.
- Lv16/Lv26 transforms remain.
- provisional P4-D2 sensitivity only: second wave 0.50/0.65/0.80; delay 100/140/180ms; extra final KB 1.25/1.35/1.50.

## Rogue R-B — 8-dagger persistent-target storm
- replaces Double Dagger/Blade Barrage/Chain Throw generators for P×P root.
- exactly 8 scheduled tracking daggers.
- continue hitting current target while alive; deterministic retarget after death.
- no same-target cap; boss dagger scalar .70.
- provisional start: 70ms interval, 0.45 each.

## Tank T-B — control-first battlefield wave + barrier
- battlefield-wide shockwave with reduced damage / strong knockback rather than full global DPS.
- one ordinary local Lv26 Aftershock retained at root impact location; no battlefield-wide slow.
- shared barrier non-additive; Lv31 must not be downgraded by same-root/later weaker Lv16 guard.
- provisional sensitivity: damage .40/.50/.60; knockback 2.0/2.5/3.0; roadmap 250/6s candidate.

## Archer A-B — one unlimited strict-line final arrow
- replaces Triple Shot for P×P.
- exactly one locked ray; each intersected enemy hit at most once; no target-count cap.
- no homing/bending/off-line retarget.
- armor ignore + 100% penetration preservation.
- do not widen gameplay corridor just because visual arrow is huge.

## Mage M-B — direct impact + bounded three-stage circle + one final chain
- replaces Greater Orb/Burst/Resonance/Chain generators for P×P root.
- primary gets one normal root direct impact.
- fixed impact-location magic circle resolves three AoE stages; primary excluded from these AoE stages to preserve crowd-specialist role.
- after stage3 only, at most one bounded Lv26-style chain generation.
- no recursive effect tree.
- provisional sensitivity: stages 0/+180/+360ms; 0.55 each; radius 1.00/1.25/1.50× Lv21 Greater Orb; final chain .35/max2.

---

# Why Option A is recommended

Cross-class identity remains distinct:

```text
Knight = broad bounded two-pass frontline disruption
Rogue  = target-persistent rapid multihit execution
Tank   = battlefield control + wall protection
Archer = one strict-line unlimited-depth deletion
Mage   = fixed-area staged density collapse + bounded chain
```

It also keeps exact values reversible during P4-D2 while locking the higher-cost additive-vs-replacement composition decision before downstream calibration.

Main future watches:
- `LV31_POWER_CLIFF_TOO_HIGH`
- `LV31_CLASS_CLEAR_RATE_DIVERGENCE`
- `LV31_ROLE_EXPRESSION_ERASURE`
- Mage/SPLITTER transform erasure
- Archer/SIEGER screen erasure
- Tank/SIEGER pre-expression erasure
- Knight/CHARGER interrupt saturation
- Stage46–49 mastery becoming trivial rather than meaningful.

---

# Required user decision

```text
A — approve proposal 90 Option A package
B — modify one or more global/class clauses
C — request additional analysis
D — reject/reopen one or more Lv31 identities
```

Approval means **structural direction + provisional P4-D2 test inputs**, not production numerical freeze.

Only after approval:
- create approved P4-D1 contract;
- run P4-D2 bounded mastery/power feedback;
- keep production untouched.

---

# Do not yet

- mark proposal 90 approved without explicit user decision;
- start P4-D2;
- change/deploy production gameplay;
- freeze Lv31 exact numeric values;
- freeze final EXP / activate Stage Quality Budget;
- add hidden class/Tier XP correction;
- author exact Stage46–50 content;
- begin P5 early.

This handoff boundary intentionally stops at the **P4-D1 user decision gate**.
