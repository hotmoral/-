# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production executable checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical implementation remains frozen during planning/calibration

## Operating / recovery authority
Mandatory session-recovery and cross-stage consistency protocol:
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`

Every material phase must be checked against upstream invariants, downstream consumers, active feedback loops, authority/supersession, scope/cost, production boundaries and handoff impact. Already-closed PASS/APPROVED work is not repeated without a concrete revalidation trigger.

---

# Current phase

**P4 — FULL PLAYER POWER SPINE CANDIDATE / P4-C1 STRUCTURAL REVIEW COMPLETE / USER DECISION PENDING**

Completed evidence/decision chain:

```text
P0 Foundation / role expression PASS_WITH_WATCHES
 -> SKILLED_V2_CENTRAL all-20 540/540 PASS
 -> P1 Run-State Lifecycle STRUCTURAL COMPLETE
 -> P2 Modifier Pipeline / Power Attribution STRUCTURAL COMPLETE
 -> P3 Ten-Stage Persistent Run Kernel STRUCTURAL PASS
 -> P4 methodology USER APPROVED
 -> P4-A Marker-Only Inverse Design PASS
 -> P4-B Solo Lv6→Lv21 Combat Feedback diagnostic COMPLETE
 -> P4-B Multiplayer / Timebase bounded precheck COMPLETE
 -> R2 revised routing USER APPROVED
 -> P4-C1 live/legacy/source evidence recovery COMPLETE
 -> P4-C1 cross-stage consistency review COMPLETE
 -> proposal 87 PROPOSED / AWAITING USER APPROVAL
```

Active dependency plan:
- `legacy-game-structure/data/system_dependency_calibration_order_v0_6.yaml`

R2 authority:
- `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`

Current P4-C1 proposal:
- `legacy-game-structure/87_P4C1_LV26_STRUCTURAL_SKILL_CONTRACT_PROPOSAL_V0_1.md`
- status: **PROPOSED / AWAITING USER APPROVAL / NO STRUCTURAL FREEZE**

P4-C2 remains blocked until explicit user approval.

---

# Stable structural truth

- 5 classes progress independently through Tiers.
- same Tier/Stage combat content across classes.
- Tier = 50 Stages.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / clear50=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intended; hard class lockout forbidden.
- Model A bounded simulation roster ladder:

```text
T1 G/R/B
T2 +SH/F
T3 +C/SP
T4 +SUP/SI
T5+ future
```

- current 9 monsters are V1 foundation, not lifetime roster cap.
- combo40 belongs inside ordinary skilled play.
- Lv31 target unlock window = Stage41–45 direction to re-test, not final numerical guarantee.
- Stage46–49 = post-Lv31 mastery; Stage50 = final application.
- EXP must not force every Tier into the same encounter-flow shape.
- final progression decisions must consider Stage reach, wall-clock reach, fail/retry and multiplayer context together.
- material unresolved design choices require explicit user approval.

---

# Closed lower layers

## P1
Authority: `legacy-game-structure/72_RUN_STATE_LIFECYCLE_APPROVED_CONTRACT_V0_1.md`

## P2
Authority:
- `legacy-game-structure/74_MODIFIER_PIPELINE_AND_POWER_ATTRIBUTION_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/data/modifier_pipeline_contract_v0_1.yaml`

## P3
Authority/evidence:
- `legacy-game-structure/76_TEN_STAGE_PERSISTENT_RUN_KERNEL_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/77_P3_TEN_STAGE_PERSISTENT_RUN_EXECUTION_REPORT_V0_1.md`

Result:
```text
30 / 30 primary 10-Stage runs PASS
8 / 8 targeted fixtures PASS
```

No P1/P2/P3 reopening was required for P4-C1; the existing contracts were consumed as upstream invariants.

---

# P4 approved methodology / R2

Authority:
- `legacy-game-structure/79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `legacy-game-structure/85_P4B_R2_APPROVED_ROUTING_CONTRACT_V0_1.md`

Provisional diagnostic EXP baseline only:
- valid completed local timing turn is the EXP source;
- Heavy X+Y gives one combined-tier award;
- timing quality matters;
- `XP_CREDIT` is dimensionless calibration space;
- one universal EXP curve remains preferred;
- no hidden class/Tier multiplier;
- encounter identity must not be homogenized to fit EXP.

R2 explicitly means this baseline is **not final EXP freeze**.
Option D / Stage Quality Budget remains not approved.
Mandatory final EXP/multiplayer-timebase reconvergence remains P10R.

Active watches:

```text
SOLO_PROGRESSION_DIVERGENCE_WATCH
TEAM_COMPOSITION_XP_OPPORTUNITY_WATCH
PLAYER_COUNT_SCALING_XP_DEPENDENCY
MULTIPLAYER_TIMEBASE_COMPRESSION_PARTIAL_NOT_COMPLETE
```

---

# P4-C1 evidence result

Recovered authority boundary:
- Lv6 = current Cloudflare combat authority.
- Lv11/Lv16/Lv21 = exact v0.16 legacy parity candidates for simulation; not current production authority.
- Lv26 = all five identities exist in `SKILL_PLAN_LV6_31.md` but remain `DESIGNED-NOT-AUTHORITATIVE` before this decision.

Material structural findings:

1. **Knight** — roadmap maps cleanly to Lv11/Lv21 penetration: remove legacy 85% penetration decay and define bounded per-penetration knockback escalation.
2. **Rogue** — one-per-root secondary dagger must be explicit; per-dagger recursion would create a generator tree at Lv21+26.
3. **Tank** — slow zone must be Stage-local, non-stacking in magnitude, and explicitly compose with SUPPORTER/CHARGER/SIEGER movement states.
4. **Archer** — real overlap found: Lv16 already preserves 100% PERFECT penetration damage, so Lv26's repeated `100% rear-target damage` phrase must not silently become a second damage bonus. Proposal treats it as inheritance/reaffirmation and makes +2 penetration the actual new Lv26 mechanic.
5. **Mage** — highest recursion/order risk. Current Mage/SPLITTER behavior proves same-action death/spawn ordering is material. Proposal bounds Lv26 to one generation and max two new targets with no recursive chain.

No unavoidable contradiction with P1/P2/P3, Monster Capability V1, role-expression contract, Model A late-band grammar or future T5+ extensibility was found under proposal 87.

New P4-C2 recheck obligations if approved:
- Knight/Archer screen and T4 backline role-expression;
- Rogue secondary tracking/fallback behavior;
- Tank zone snapshot/settlement and movement-state composition;
- Mage SPLITTER death/spawn/chain ordering;
- T4 SUPPORTER/SIEGER uptime/first-shot opportunity;
- class-specific timing-turn opportunity / progression feedback.

---

# Current user decision boundary

```text
P4-C1 — APPROVE / MODIFY / REJECT proposal 87 Option A
```

Recommended Option A:
- preserve all five roadmap identities;
- approve the bounded compositional semantics in proposal 87;
- admit roadmap numeric values only as `P4C2_PROVISIONAL_SIMULATION_INPUT`;
- do not numerically freeze them for production.

Until explicit user approval:

```text
P4-C1 structural freeze = NO
P4-C2 execution = BLOCKED
P4-D1 = BLOCKED
production changes = UNAUTHORIZED
```

---

# Approved route after P4-C1 decision

```text
P4-C1 user decision
 -> P4-C2 Lv26 provisional feedback
 -> P4-D1 Lv31 structural decision
 -> P4-D2 Lv31 provisional mastery feedback
 -> P4-E provisional player-power-spine closure WITH EXP WATCHES
 -> P5/P6/P7/P8
 -> P10 current-roster multiplayer scaling baseline
 -> P10R mandatory EXP / multiplayer-timebase reconvergence
 -> only after P10R may permanent-progression layers rely on converged EXP behavior
```

---

# Still not frozen

- Lv26 production numerical values / implementation
- Lv31 exact mechanics/numbers
- final EXP acquisition semantics
- exact XP_CREDIT vector
- exact A6/A11/A16/A21/A26/A31
- intermediate-level formula
- player-visible EXP scale
- player-count progression treatment
- percentile tail acceptance gates
- production monster coefficients / exact 200 Stages
- shop/economy / Base HP
- star/achievement numerical power
- boss values
- multiplayer combat/progression scaling
- production numerical implementation

No production gameplay source was changed by P4-C1 review/proposal work.
