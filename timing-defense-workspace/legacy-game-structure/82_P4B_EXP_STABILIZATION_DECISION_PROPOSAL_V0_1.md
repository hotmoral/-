# Timing Defense — P4-B EXP Stabilization Decision Proposal V0.1

Date: 2026-10-23 KST  
Status: **PROPOSED / AWAITING USER APPROVAL / NO NEW EXP SEMANTICS AUTHORIZED**

Depends on:
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `80_P4A_MARKER_ONLY_INVERSE_DESIGN_EXECUTION_REPORT_V0_1.md`
- `81_P4B_LV6_LV21_COMBAT_FEEDBACK_EXECUTION_REPORT_V0_1.md`
- `data/p4b_combat_feedback_divergence_v0_1.json`

---

# 0. Decision question

P4-B found that pure additive EXP from every valid timing turn creates a structural class progression split:

```text
offensive skill becomes efficient
 -> fewer attacks needed
 -> fewer EXP-producing turns
 -> later skill unlocks delayed

control/defensive skill does not reduce attacks
 -> more EXP-producing turns remain
 -> later skill unlocks earlier
```

The confirmed `Lv31 Stage41–45` target cannot currently be jointly maintained across classes/Tiers by universal thresholds alone.

Decision required:

> What progression rule should preserve timing mastery and one universal curve without forcing every Tier encounter flow to become the same or suppressing class identity?

---

# 1. Option A — keep pure per-turn EXP and accept class-specific reach bands

Rule remains unchanged:

```text
Stage XP = SUM(valid turn quality credits)
```

Then the progression system accepts that different classes naturally unlock skills at substantially different Stages.

### Pros
- simplest rule;
- no new progression layer;
- direct action-to-EXP relationship remains exact;
- preserves the strongest form of natural self-damping.

### Cons
- current bounded evidence places Tank much earlier and Mage/Rogue/Archer later;
- best universal pure-turn fit still gives Tank Lv31 around the high-30s in several Tiers and Mage around the high-40s/50 in some Tiers;
- conflicts with the user-confirmed Lv31 Stage41–45 mastery runway;
- class skill learning cadence becomes an unintended consequence of DPS/control identity.

### Assessment
**Not recommended unless the Lv31 Stage41–45 common direction is deliberately reopened.**

---

# 2. Option B — class-specific thresholds or EXP multipliers

Example shape:

```text
Tank threshold multiplier > 1
Mage/Rogue/Archer threshold multiplier < 1
```

or separate A6/A11/... values per class.

### Pros
- precise control;
- straightforward numerical fit;
- minimal encounter changes.

### Cons
- directly abandons the approved universal-curve direction;
- hidden correction is hard to explain to players;
- future shop/permanent power changes would require repeated class corrections;
- makes progression telemetry harder to interpret because class combat strength and class XP rules are entangled.

### Assessment
**Not recommended.** Keep only as a fallback if general visible rules fail later.

---

# 3. Option C — solve only through encounter authoring

Use natural levers:
- monster quantity;
- HP/durability/armor where role-consistent;
- spawn cadence;
- formation;
- density/geometry;
- pressure composition.

### Pros
- keeps EXP semantics unchanged;
- can improve individual Stage pacing and Tier identity;
- consistent with the user requirement that Tiers should not all have identical flow.

### Cons
- same Stage is shared by every class, so adding workload generally adds opportunity to everyone;
- early class asymmetry is systematic, not only Stage-local;
- Rogue Lv6 already needs only about 54–75% of Lv1 actions across the current representative vocabulary while Tank remains near 100%;
- authoring every Tier specifically to cancel progression differences risks suppressing the very class strengths the encounters should showcase;
- cannot be relied on as the sole general solution.

### Assessment
**Recommended as a local balancing tool, not the primary progression stabilizer.**

---

# 4. Option D — class-neutral Stage Quality Budget + raw-turn hybrid

Recommended direction.

Conceptual form:

```text
StageCredit
= λ × SUM(actual valid-turn quality credits)
+ (1 - λ) × StageProgressionBudget × MeanTimingQuality
```

where:
- `λ` is one global blend parameter, not class/Tier specific;
- `StageProgressionBudget` is class-neutral and based on the run progression spine, not on how many attacks a particular class needed;
- `MeanTimingQuality` comes only from valid completed local timing turns;
- NORMAL/GOOD/PERFECT/Heavy quality remains meaningful;
- no-target/passive/AI actions still generate no mastery sample;
- exact formula/scale/blend remains open.

### Intuition
A player who kills efficiently should not lose most of the progression opportunity simply because the class skill did its job.
A player who needs more attacks can retain a limited raw-turn catch-up component, but extra attack count no longer dominates total EXP.

### Pros
- class-neutral;
- one universal EXP curve can remain the target;
- timing quality remains the progression signal;
- preserves some natural self-damping if `λ > 0`;
- does not require all Tiers to have the same monster count/HP/flow;
- allows encounter authoring to optimize gameplay identity rather than secretly compensating XP;
- remains compatible with later shop/permanent-power feedback because efficient damage does not automatically erase most XP opportunity.

### Cons
- changes the currently approved pure-per-turn baseline;
- requires a Stage-level progression budget concept;
- exact combat UI/when-to-display-or-settle XP needs later product treatment;
- multiplayer creates later questions about minimum sample/contribution/AFK behavior and must be audited at P10/P16;
- over-normalization could make longer/harder Stages feel under-rewarded unless the budget spine is authored transparently.

### Current bounded sensitivity
A reduced-order test found:

```text
100% raw-turn       -> worst common-window miss about 5 Stages
75% raw             -> about 3
50% raw             -> about 2
25% raw             -> a few ~1-Stage misses
10% raw             -> all tested current windows feasible
0% raw              -> all tested current windows feasible
```

These are **not candidate final percentages**.
They only show that a tiny generic bonus is unlikely to be enough and that opportunity normalization can solve the right failure mode.

### Assessment
**Recommended.**

---

# 5. Why Option D is preferred over simply giving Stage-clear EXP

A flat Stage-clear bonus would say:

```text
clear Stage -> +X regardless of timing
```

That weakens the central game premise that better timing accelerates growth.
It also did not fully repair the divergence in bounded exploratory tests.

The proposed Stage Quality Budget is different:

```text
Stage progression share
× actual timing quality
```

So progression still comes from the quality of the player's timing performance, while raw attack quantity stops being the dominant variable.

---

# 6. Encounter authoring still matters under Option D

Approval of Option D would **not** mean ignoring attack count.

P4/P6 should still flag:
- a Stage that ends so quickly a class cannot express its mechanics;
- HP sponges that create excessive repetitive timing turns;
- classes with no meaningful opportunity;
- Tier flows that become monotonous;
- role-expression failures.

Natural encounter adjustments remain the first tool for those gameplay defects.

The distinction is:

```text
encounter authoring fixes bad gameplay shape
progression normalization fixes systemic XP-opportunity bias
```

Do not use one system to disguise defects in the other.

---

# 7. If Option D is approved — bounded next test

Do not choose a production blend immediately.

Run a P4-B2 candidate matrix with at least:

```text
raw-turn weight λ = 0.00 / 0.10 / 0.25 / 0.50
```

and compare:
- Lv6/11/16/21/26/31 P25/P50/P75/P90;
- class/Tier spread;
- timing-quality sensitivity;
- post-unlock Stage count;
- degree of remaining natural self-damping;
- Stage-by-Stage budget smoothness;
- whether T1–T4 encounter identity remains distinct;
- robustness to the Mage feedback WATCH.

Only after that evidence should one blend or possibly pure Stage Quality Budget become the provisional P4 candidate.

This approval would still **not** freeze:
- `λ`;
- quality vector;
- StageProgressionBudget values;
- visible EXP numbers;
- skill thresholds;
- Lv26/Lv31 power;
- production implementation.

---

# 8. Recommendation

Approve Option D as the **next bounded calibration direction**, while retaining Option C as the normal encounter-level correction tool.

Recommended combined principle:

> Tier and Stage authoring determine combat identity and healthy pacing. Run EXP uses a class-neutral timing-quality-normalized Stage budget so class efficiency does not unintentionally move the progression spine by many Stages. A limited raw-turn component may remain if evidence supports it.

Do not approve class/Tier-specific hidden XP correction.
Do not nerf class identities merely to manufacture equal attack counts.

---

# 9. User decision requested

Choose one:

- **A** — keep pure per-turn EXP and reopen common skill-reach expectations;
- **B** — allow class-specific XP/threshold correction;
- **C** — attempt encounter-authoring-only correction;
- **D (recommended)** — class-neutral Stage Quality Budget + raw-turn hybrid, then run a bounded blend comparison before selecting exact values.

No option is active until user approval.
