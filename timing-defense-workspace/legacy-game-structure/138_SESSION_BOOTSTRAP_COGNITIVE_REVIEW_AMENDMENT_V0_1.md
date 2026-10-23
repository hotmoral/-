# Timing Defense — Session Bootstrap Cognitive Review Amendment V0.1

Date: 2026-10-23 KST  
Status: **ACTIVE OPERATING AMENDMENT / USER-DIRECTED / NO GAMEPLAY OR NUMERICAL AUTHORITY**

Amends:
- `86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- `08_STRUCTURE_CONSISTENCY_GOVERNANCE.md`
- `71_USER_APPROVAL_DECISION_GATE_GOVERNANCE_V0_1.md`

## 0. Why this amendment exists

The project is highly coupled. A new session must not recover only the latest micro-task and then tune locally.
The assistant must recover the **reasoning frame** that connects campaign structure, run state, class identity, skills, shop, encounter chronology, wall attrition, EXP opportunity, meta progression and downstream work.

The user must not have to repeatedly explain this operating method in every new session.

This amendment is mandatory bootstrap guidance for future sessions.

---

## 1. Required mental model before local work

Before touching a current micro-problem, reconstruct the common coordinate system:

```text
Tier
× Stage 1..50
× content novelty / monster availability
× run-local player power
× shop/economy
× persistent wall/run state
× class identity
× meta progression
```

Do not treat skills, shop, encounters, EXP, wall state, stars or achievements as isolated systems.

Current campaign-design method remains:

```text
shallow whole-system alignment
-> close high-dependency semantics
-> bounded candidate authoring
-> deterministic probe/simulation
-> classify cause
-> re-check affected upstream/downstream invariants
-> deepen only the necessary layer
```

This is progressive deepening / iterative convergence, not pure waterfall and not uncontrolled simultaneous tuning.

---

## 2. Mandatory new-session cognition sequence

After fetching live canonical state, the assistant must internally walk through this sequence before proposing local changes.

### A. What is the product-level purpose of the current slice?
Examples:
- what experience should this Stage band create?
- what class fantasy or progression loop is being tested?
- is the current task evidence gathering, structural design, numerical calibration, or production implementation?

### B. Which upstream truths constrain it?
At minimum, check only materially relevant items among:
- Master Campaign Spine / Tier and Stage macro flow;
- P1 run-state lifecycle;
- P2 modifier/effect semantics;
- P3 `STAGE_SETTLED` transition;
- P4 player-power / EXP feedback;
- class radar identity invariants;
- current P5 shop structure;
- monster role-expression and frontmost targeting truth.

### C. Which downstream systems consume the result?
Ask whether this step can affect:
- later Stage chronology;
- wall deficit entering later Stages;
- shop allocation value;
- attack count and EXP opportunity;
- Lv31 reach/use window;
- class soft-wall interpretation;
- P6 joint convergence;
- future star/achievement or multiplayer calibration.

### D. Is the observed problem structural, semantic, chronological, class-identity, economy, simulator-fidelity, or numerical?
Do not patch before classifying the layer.

Default repair order when applicable:

```text
source/simulator fidelity
-> lifecycle / state semantics
-> encounter geometry / chronology / frontmost order
-> class/package semantics
-> shop interaction / feedback
-> exact scalar values last
```

### E. Can a small bounded diagnostic answer the question?
Prefer the cheapest discriminating probe.
Do not reopen a whole closed tranche unless a concrete trigger exists.

### F. Does the proposed action require user approval?
If it would adopt or freeze an important structural, content, numerical, economy, balance or production decision, stop after analysis/recommendation and ask the user first.

Diagnostic work and unambiguous measurement/instrumentation fixes may proceed without a separate approval if they do not change game semantics.

---

## 3. Mandatory cross-system review lenses for every material slice

Before closing a meaningful result, explicitly check:

1. **Purpose** — did the work solve the intended gameplay/progression question, not merely move a metric?
2. **Upstream consistency** — did it preserve already-approved lifecycle, targeting, modifier and campaign rules?
3. **Downstream impact** — what later package now needs recheck, if any?
4. **Feedback loops** — especially encounter pressure ↔ attack count ↔ EXP ↔ skill reach, shop power ↔ kill speed ↔ EXP opportunity, and persistent wall attrition across Stages.
5. **Class identity** — high radar axes remain causal strengths; low axes remain real limitations; `SURVIVAL != CLEAR`.
6. **Content identity** — difficulty is not created by indiscriminate HP/count inflation; role monsters must get readable role opportunity.
7. **Determinism / attribution** — the cause is reproducible and not hidden by another system.
8. **Scope / cost** — avoid exact downstream tuning while an upstream premise remains open.
9. **Authority** — distinguish OBSERVED / DERIVED / CANDIDATE / PROPOSED / USER_APPROVED / FROZEN / PRODUCTION_AUTHORIZED.
10. **Handoff** — if phase, blocker, evidence, watch or next boundary changed, synchronize handoff material before ending the tranche.

---

## 4. Anti-silo rule

The following workflow is forbidden:

```text
inspect skill in isolation
-> tune skill
-> later inspect shop in isolation
-> tune shop
-> later inspect encounter in isolation
-> sum the results
```

Instead, whenever one layer materially changes, ask which linked layers must be recomputed or at least sanity-checked.

Examples:
- shop damage may reduce timing-turn count and shift EXP/skill reach;
- Fortification changes current and max wall HP while preserving purchased repair semantics;
- encounter chronology changes which class specialty is actually useful;
- a Stage48 change changes the wall deficit and pressure entering Stage49;
- stronger permanent power can reduce EXP opportunities and alter the run-level curve.

---

## 5. Anti-repetition rule

Deep thinking does not mean repeating everything.

Do **not** rerun a closed PASS/APPROVED/FROZEN group merely because a new session started.
Reopen only with a concrete trigger such as:
- relevant source/branch changed;
- new commit altered an input;
- new coupled layer requires an explicit feedback recheck;
- deterministic hash/replay diverged;
- runtime/source mismatch appeared;
- an active WATCH became material;
- new evidence contradicts an accepted assumption.

Use existing evidence otherwise.

---

## 6. Important-decision discipline — mandatory

The user explicitly requires:

> Important decisions must not be silently applied. Analyze first, explain simply, then obtain user approval before adoption.

This includes, but is not limited to:
- adopting a new Stage packet as working direction;
- changing class/monster/shop/EXP numerical values;
- changing encounter content policy;
- selecting a Tank scalar or similar balance coefficient;
- changing an approved structural contract;
- production gameplay changes.

Before asking for approval, perform enough analysis to provide:
- the actual decision question;
- why it is needed now;
- constraints;
- evidence;
- alternatives/tradeoffs;
- recommendation;
- side effects/reversibility;
- what remains open.

Do not interrupt the user for every diagnostic step.

---

## 7. Communication rule

Explain current findings to the user in plain Korean first.

Preferred format:

```text
무엇이 문제인가
-> 왜 그런가
-> 그래서 다음에 무엇을 확인할 것인가
-> 무엇은 아직 결정/적용하지 않았는가
```

Technical names/numbers may follow when useful, but they must not replace the simple causal explanation.

---

## 8. Mandatory handoff quality gate

At every meaningful work-group boundary, synchronize as applicable:
- `PROJECT_STATUS.md`
- `NEXT_WORK.md`
- `SESSION_HANDOFF.md`
- active dependency YAML when state/order changed
- current result/contract document

A new session must be able to recover without the user repeating:
- the whole-structure reasoning method;
- the diagnose-before-patch rule;
- the important-decision approval rule;
- the plain-language reporting preference;
- the exact next diagnostic boundary.

If the next session would need the user to explain those again, the handoff is incomplete.

---

## 9. Current P5 application example

For the active Stage48 issue, the correct reasoning chain is:

```text
Stage48 purpose = first protected post-Lv31 role pulse
-> SIEGER must receive meaningful readable role uptime
-> all enemies still enter from normal right edge
-> frontmost targeting/chronology determines whether SIEGER is protected
-> class identity must remain visible
-> wall deficit carries from Stage46/47 and into Stage49
-> STAGE_SETTLED must be respected
-> shop growth can alter kill-order breakpoints
-> diagnose chronology before monster/class scalar changes
-> any working-packet adoption requires user approval
```

This example is illustrative of the method, not a frozen Stage48 design.

---

## 10. Armored-durable late-stage candidate intent — preserve across sessions

The `ARMORED_DURABLE_PROXY` / BRUTE+SHIELD-like temporary package must **not** be remembered only as a SIEGER escort experiment.
Its original user-directed design intent is broader:

```text
late-game Mage / Archer can erase ordinary high-count waves too quickly
+ Stage48 needs a way to create protected role pressure around SIEGER
-> investigate a limited armored-durable pressure package
```

Therefore future reasoning must preserve both purposes when evaluating this candidate:

1. **Late-stage anti-wave-clear pressure** — provide a durable/mitigated body that prevents Mage/Archer mass-clear strength from trivially ending late encounters while still respecting class identity and the no-hard-lockout rule.
2. **Protected-role support** — potentially create enough frontline persistence for SIEGER or other backline/objective-role monsters to express their intended behavior.

Do not misclassify the candidate as merely "extra HP for SIEGER escort" and then discard it because ordinary BRUTE/SHIELD chronology alone fails.
Also do not silently promote it into a tenth ordinary archetype or a production monster.

Current authority is only:

```text
DESIGN-INTENT CANDIDATE / DIAGNOSTIC REFERENCE
NOT USER-APPROVED ROSTER CHANGE
NOT PRODUCTION AUTHORITY
NOT NUMERICALLY FROZEN
```

When this candidate becomes decision-relevant, compare at least:

```text
ordinary BRUTE/SHIELD encounter composition
vs limited armored-durable elite/package
vs SIEGER standoff/chronology changes
```

and judge them on the coupled objectives:
- SIEGER role uptime;
- Mage/Archer late-stage clear speed;
- Knight/Rogue/Tank identity and fairness;
- wall pressure / Stage46→49 continuity;
- shop/EXP feedback;
- readability and encounter diversity;
- risk of creating a hard class lockout or generic HP sponge.

Any adoption as an elite recipe, monster variant, roster change, or production value requires explicit user approval first.
