# Timing Defense — P4-B EXP Decision Reassessment Proposal V0.1

Date: 2026-10-23 KST  
Status: **PROPOSED / AWAITING USER DECISION / NO EXP SEMANTIC CHANGE AUTHORIZED**

Depends on:
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `82_P4B_EXP_STABILIZATION_DECISION_PROPOSAL_V0_1.md`
- `83_P4B_MULTIPLAYER_TIMEBASE_PRECHECK_V0_1.md`
- `data/p4b_multiplayer_timebase_precheck_v0_1.json`

---

# 0. What changed

Document 82 recommended Option D (`Stage Quality Budget + raw-turn hybrid`) after a solo-focused P4-B divergence.

Document 83 added missing multiplayer and wall-clock perspectives and found:
- shared team combat compresses solo class divergence;
- mixed-team members still do not gain EXP at exactly the same rate;
- the same class can gain EXP at different rates depending on teammates;
- player-count encounter scaling changes per-player EXP opportunity;
- Stage throughput has a spawn/cadence floor, so time normalization does not automatically cancel the difference;
- high EXP opportunity can coexist with worse clear/failure performance.

Therefore Option D is no longer recommended for **immediate approval**.
It remains a possible later solution if current-roster multiplayer evidence still shows unacceptable progression bias.

---

# 1. Decision that should NOT be made yet

Do not yet decide:
- pure per-turn EXP is final;
- Stage Quality Budget is required;
- class/Tier XP multipliers are needed;
- exact skill-reach exceptions by class;
- exact player-count progression correction.

The current full 9-monster 2P/3P/4P scaling model is not authoritative enough to support those final decisions.

---

# 2. Revised alternatives

## R1 — approve Option D now

Change EXP semantics now to a Stage Quality Budget hybrid and calibrate the blend.

### Pros
- directly addresses solo attack-opportunity bias.

### Cons
- multiplayer precheck shows the solo effect is partially compressed;
- could normalize a problem that later multiplayer scaling naturally reduces;
- adds a new progression system before team scaling is known.

### Assessment
**Not recommended now.**

---

## R2 — keep pure per-turn EXP as provisional baseline, split skill-contract work from final EXP convergence — RECOMMENDED

Meaning:

```text
pure per-valid-turn EXP
= last user-approved diagnostic baseline
= NOT final numerical/semantic freeze
```

Proceed with the parts of P4 that do not require pretending final multiplayer progression is known:
1. review/approve exact Lv26 skill contract;
2. measure Lv26 power feedback provisionally;
3. review/approve exact Lv31 skill contract;
4. measure Stage46–49 mastery/power behavior provisionally;
5. close P4 only as a **provisional power-spine candidate with explicit EXP watches**.

Then after a credible current-roster multiplayer combat-scaling baseline exists, reopen EXP convergence before permanent progression is allowed to depend on it.

Required later recheck:

```text
current-roster 2P/3P/4P scaling
 -> Solo vs homogeneous vs mixed team
 -> Stage reach + wall-clock reach + fail/retry cost
 -> same-class teammate dependence
 -> player-count dependence
 -> decide whether pure per-turn remains acceptable
    or whether class-neutral stabilization is actually needed
```

### Pros
- preserves the last approved semantics without prematurely freezing them;
- avoids circularly blocking all later skill design on an EXP question that depends on later multiplayer scaling;
- keeps Lv26/Lv31 class identity work moving;
- allows later evidence to decide whether D is necessary;
- no hidden class/Tier correction.

### Cons
- P4 milestone reach remains provisional rather than numerically closed;
- later multiplayer evidence may force a return to P4 EXP anchors;
- downstream packages must label EXP-dependent outputs as provisional until reconvergence.

### Assessment
**Recommended.**

---

## R3 — declare pure per-turn EXP final now

### Assessment
**Not recommended.**

Solo divergence and team-composition/player-count dependencies are both unresolved.
Keeping the current rule as a provisional baseline is different from freezing it as final.

---

# 3. Proposed dependency split if R2 is approved

The key is to avoid a circular dependency.

P4 cannot wait for P10 in its entirety, because P10 itself sits downstream of P4/P5/P6/P8.
Therefore split **skill power definition** from **final progression convergence**.

Proposed routing:

```text
P4-C1  Lv26 structural decision
 -> P4-C2 Lv26 provisional feedback
 -> P4-D1 Lv31 structural decision
 -> P4-D2 Lv31 provisional mastery feedback
 -> P4-E  provisional player-power-spine closure WITH EXP WATCH
 -> P5/P6/P7/P8
 -> P10 current-roster multiplayer scaling baseline
 -> P10R EXP / multiplayer opportunity reconvergence
 -> only then allow permanent-progression layers to rely on the converged EXP spine
```

`P10R` would explicitly re-evaluate:
- Solo;
- 2P/3P/4P;
- homogeneous and mixed teams;
- Stage-based reach;
- wall-clock reach;
- clear/fail/retry-adjusted progression;
- team composition sensitivity;
- player-count scaling sensitivity;
- whether Option D or another visible class-neutral stabilizer is necessary.

No exact numerical freeze still occurs before P17.

---

# 4. What remains authoritative under R2

R2 would **not** undo the user-approved P4 methodology except where evidence requires later reconvergence.

Still authoritative:
- EXP comes from valid completed local timing turns for the provisional baseline;
- quality tiers matter;
- Heavy X+Y gives one combined-tier award;
- one universal curve is the target;
- no hidden class-specific XP multiplier;
- no hidden Tier XP multiplier;
- Tier identity must not be homogenized for EXP;
- Lv31 Stage41–45 remains the target direction to re-test, not silently abandon.

Not frozen:
- exact thresholds;
- exact quality vector;
- final EXP source semantics after multiplayer reconvergence;
- final player-count treatment;
- exact Lv26/Lv31 mechanics until their gates close.

---

# 5. Recommendation

Approve **R2**.

Rationale:

> The evidence now shows two real effects rather than one: solo class efficiency changes personal timing-opportunity, while multiplayer converts part of that effect into team-wide Stage-duration/opportunity changes. Because current multiplayer scaling is not yet authoritative, changing EXP semantics now would be premature. Keep pure per-turn EXP as a provisional measurement baseline, continue bounded skill-contract work, and force an explicit multiplayer/timebase reconvergence before permanent progression or numerical freeze can depend on the EXP spine.

This is reversible and keeps the project moving without disguising the unresolved dependency.

---

# 6. User decision requested

- **R1** — adopt Stage Quality Budget direction now;
- **R2 (recommended)** — retain pure per-turn as provisional baseline, continue Lv26/Lv31 structural work, defer final EXP convergence to a mandatory multiplayer/timebase recheck;
- **R3** — freeze pure per-turn as final now.

No route is activated by this proposal until user approval.
