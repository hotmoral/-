# Timing Defense — SKILLED_V2 Controlled Harness & Fit Schema V0.1

Date: 2026-10-22 KST  
Status: **CALIBRATION DESIGN / HARNESS-ONLY / NO PLAYER-SKILL NUMERIC FREEZE**

Depends on:
- `24_SKILLED_V2_MEASUREMENT_PROTOCOL_V0_1.md`
- `54_ALL20_ROLE_EXPRESSION_AUDIT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Machine-readable companion:
- `data/skilled_v2_controlled_harness_v0_1.yaml`

Validator:
- `tools/validate_skilled_v2_harness.py`

---

# 0. Purpose

The project now has a representative encounter library in which designated monster roles are structurally expressible across all five classes.

The next blocker is no longer encounter geometry.
It is the player model:

> What should `SKILLED_V2` actually do under low pressure, sustained tempo, durable rhythm, target turnover, stateful reads, and mixed pressure?

The user has explicitly established two qualitative anchors:

1. the old notion of `skilled` was too weak
2. combo 40 is readily achievable when concentrating and must not be modeled as a rare high-mastery-only event

This document turns those anchors into a controlled measurement and fitting contract without inventing production probabilities.

---

# 1. HARNESS_ONLY boundary

Calibration harness runs are not campaign attempts.

They must not:
- award stars
- modify class/Tier records
- award permanent progression
- award achievements/titles
- affect run shop economy
- persist campaign EXP/coin outcomes
- count toward Tier clear/failure statistics

They may record:
- timing judgments
- combo state
- heavy/P×P behavior
- target turnover
- pressure context
- action cadence
- role-reading/counterplay events

The harness must preserve the same input/judgment semantics as the game wherever the variable is being measured.

If a harness neutralizes damage, progression, spawn termination, or another non-measured variable, that neutralization must be explicit in the trace metadata.

---

# 2. Why one `PERFECT/GOOD/NORMAL` vector is insufficient

SKILLED_V2 is not an iid dice roll.

Player performance can change with:
- sustained rhythm length
- target death/reorder
- no-target waiting
- density
- stateful telegraph reading
- heavy pair execution
- long combo concentration
- simultaneous tactical pressure

Therefore fitting uses **context-conditioned transition/survival behavior**, not a single global timing percentage.

At minimum the model must separate:

```text
BASELINE
TEMPO
DURABLE
TURNOVER
STATEFUL
MIXED
```

and preserve sequence order inside each trace.

---

# 3. Controlled harness family

## H0 — TIMING_BASELINE

Question:
> What is the player's clean timing ceiling when combat-state noise is minimized?

Purpose:
- baseline judgment distribution
- baseline action cadence
- baseline combo survival
- clean heavy/P×P execution

Controlled environment:
- GRUNT-like reference target presentation
- low pressure
- no stateful mechanic
- no geometry test
- target turnover minimized or explicitly separated from measured segments

Recommended harness-only control:
- use a stable reference target segment long enough for combo40 opportunity
- if target replacement is necessary, mark replacement windows and exclude them from pure baseline estimation

Primary outputs:
- timing outcomes
- inter-action intervals
- combo10/20/40/60 reach
- longest combo
- heavy/P×P completion

Contamination to avoid:
- frequent target deaths
- CHARGER/SIEGER telegraphs
- dense AoE target changes

---

## H1 — SUSTAINED_TEMPO

Question:
> How much does sustained fast approach/tempo reduce timing quality relative to H0?

Purpose:
- tempo degradation
- sustained combo maintenance
- action-cadence adaptation

Reference pressure:
- RUNNER-led sustained approach
- repeated but readable tempo
- low geometry complexity

Primary outputs:
- H1 vs H0 judgment delta
- combo survival delta
- cadence drift
- miss/late-input change

Do not mix this harness with high target-turnover density; that is H3.

---

## H2 — DURABLE_RHYTHM

Question:
> How does a long-lived durable target change combo/heavy behavior?

Purpose:
- long target exposure
- deliberate heavy use
- P×P behavior
- concentration over repeated actions on one durable frontline

Reference pressure:
- BRUTE-led durable target
- low turnover
- no mandatory stateful read

Primary outputs:
- heavy opportunity/completion
- P×P completion
- combo survival during long exposure
- action interval drift over extended rhythm

---

## H3 — TURNOVER_DENSITY

Question:
> How much performance degrades when valid targets die/reorder frequently?

Purpose:
- target reacquisition delay
- first-input accuracy after target change
- no-target wait recovery
- combo disruption attributable specifically to turnover

Controlled environment:
- multiple low-durability targets
- repeated authoritative frontmost changes
- stateful telegraphs minimized

Primary outputs:
- targetChange -> nextValidAction delay
- first judgment after target change
- combo break cause
- missed/invalid input around turnover

Critical distinction:
A timing miss during ordinary rhythm must not be grouped with a turnover-induced miss.

---

## H4 — STATEFUL_READ

Question:
> How much does reading and reacting to a telegraphed stateful mechanic degrade timing execution?

Reference mechanic:
- CHARGER windup/counterplay

The role-expression work already proved that candidate CHARGER contexts can expose a readable windup across all five classes.
H4 should reuse that semantic truth rather than a geometry in which CHARGER dies before windup.

Purpose:
- timing degradation while reading telegraph
- reaction/counterplay latency
- whether tactical response breaks combo rhythm

Primary outputs:
- telegraph visible -> response action latency
- judgment quality immediately before/during/after telegraph
- interrupt attempt/success
- combo break attributable to tactical response

Important:
CHARGER full charge success is not the player-skill target.
The measured variable is response to a readable state.

---

## H5 — MIXED_PRESSURE

Question:
> How does skilled performance behave when multiple already-learned pressure dimensions overlap?

Purpose:
- campaign-like context sensitivity
- interaction between tempo, turnover, density, durability, and stateful reading

Requirements:
- at least two distinct pressure families
- no brand-new mechanic taught inside the harness
- role-expression opportunity already validated for included stateful monsters

Primary outputs:
- combined degradation vs H0
- whether degradation is additive or nonlinear
- longest-combo tail under mixed pressure
- target-turnover + stateful interaction

H5 is not used to define baseline skill. It is used to test transfer of the fitted model toward campaign-like conditions.

---

# 4. Trace event schema

Every captured action trace must preserve sequence order.

Minimum run metadata:

```yaml
traceSession:
  traceId: string
  anonymousPlayerId: string|null
  harnessVersion: string
  harnessId: H0|H1|H2|H3|H4|H5
  classId: knight|rogue|tank|archer|mage|null
  powerMode: HARNESS_NEUTRAL|CURRENT_AUTHORITY_LV6|other
  attemptIndex: integer
  startedAt: timestamp|null
  deviceContext: {}
  calibrationFlags: []
```

Minimum action event:

```yaml
actionEvent:
  seq: integer
  atMs: integer
  targetId: string|null
  targetType: string|null
  targetGeneration: integer|null
  targetChangedSincePriorAction: boolean
  noTargetWaitMsBeforeAction: integer
  pressureContext: BASELINE|TEMPO|DURABLE|TURNOVER|STATEFUL|MIXED
  judgment: PERFECT|GOOD|NORMAL|MISS|INVALID
  comboBefore: integer
  comboAfter: integer
  comboBreakCause: NONE|TIMING|TARGET_TURNOVER|NO_TARGET|TACTICAL_RESPONSE|INVALID_INPUT|OTHER
  chargeBefore: integer
  chargeAfter: integer
  heavyOpportunity: boolean
  heavyAttempted: boolean
  heavyCompleted: boolean
  ppAttempted: boolean
  ppCompleted: boolean
  interActionMs: integer|null
  reacquireDelayMs: integer|null
```

Stateful event:

```yaml
stateEvent:
  atMs: integer
  monsterId: string
  monsterType: string
  state: WINDUP_START|WINDUP_END|INTERRUPTED|FULL_ACTIVATION|TARGET_REORDER|OTHER
  readableSinceMs: integer|null
  relatedActionSeq: integer|null
```

The raw ordered events are retained for fitting; aggregate percentages alone are insufficient.

---

# 5. Derived per-trace metrics

Timing:
- PERFECT / GOOD / NORMAL / MISS / INVALID share
- inter-action median / spread / tail

Combo:
- reach10 / reach20 / reach40 / reach60+
- longest combo
- combo survival curve by current combo band
- break cause distribution

Heavy:
- opportunity count
- attempt rate given opportunity
- completion rate given attempt
- P×P attempt/completion
- abandonment/error rate

Turnover:
- target-change count
- reacquire delay distribution
- first-post-turnover judgment distribution
- turnover-specific combo break rate

Stateful:
- readable-state -> response latency
- interrupt attempt/success
- timing-quality delta around telegraph window
- tactical-response combo breaks

Pressure:
- each H1–H5 metric expressed as delta from the same player's H0 baseline where paired data exists

---

# 6. Fitting model — bounded sequence-aware approach

Do not fit one global categorical vector.

First fit proposal:

```text
A. baseline cadence distribution
B. judgment distribution conditioned on context
C. combo survival / break hazard conditioned on combo band + context
D. target-turnover reacquisition distribution
E. heavy attempt/completion behavior
F. stateful-response latency and local judgment degradation
```

A practical simulator can initially use a semi-Markov / state-transition approximation rather than reproducing every human motor detail.

The fitted state should include enough history to distinguish:
- ordinary rhythm
- immediately after target turnover
- during/after stateful response
- long-combo concentration band

---

# 7. Profile family construction

The fitted dataset produces four conceptually distinct profiles:

```text
SKILLED_V2_CONSERVATIVE
SKILLED_V2_CENTRAL
SKILLED_V2_STRONG
HIGH_MASTERY_STRESS
```

They are not created by arbitrarily multiplying one profile's accuracy.

Instead use player/session distributions or defensible parameter envelopes:
- CONSERVATIVE = lower skilled envelope
- CENTRAL = representative skilled center
- STRONG = upper skilled envelope
- HIGH_MASTERY_STRESS = separate stress profile above ordinary skilled

The same individual may contribute multiple harness traces, but train/validation splitting must avoid placing nearly identical traces from one session on both sides.

---

# 8. Combo40 hard qualitative anchor

User-confirmed anchor:

> 집중하면 combo 40은 쉽게 달성 가능.

Therefore the fitted model fails if:
- combo40 exists only in HIGH_MASTERY_STRESS
- CENTRAL treats combo40 as an extreme tail event in stable representative conditions
- the only way CENTRAL reaches combo40 is perfect-only/no-pressure synthetic behavior

This document intentionally does **not** assign an exact combo40 probability before observed traces exist.

Required fitting report:
- H0 combo40 reach
- H1/H2 combo40 reach
- H5 combo40 reach or survival sensitivity
- reason for any large drop between contexts

---

# 9. Anti-overfit / holdout contract

Minimum rules:

1. retain raw trace order
2. group traces by player/session when splitting
3. hold out at least one context/session group for transfer validation when sample size permits
4. do not tune profile solely to make a chosen campaign clear rate come out below 60%
5. validate against role-expression regression separately
6. report sample size and uncertainty

The user observation is a strong anchor that the old skilled model was weak; it is not permission to clone a single person's exact trace as the population model.

---

# 10. Role-expression regression gate after fitting

Fitted strong play is allowed to prevent full monster abilities.
It is not allowed to make intended monster roles structurally invisible again without review.

After fitting, rerun the all-20 candidate library and classify:
- role opportunity remains readable
- full activation prevented by mastery
- pre-expression deletion reappears

If a fitted STRONG/CENTRAL profile reopens a role-expression failure:
1. inspect the role's visible-window evidence
2. adjust localized authoring if necessary
3. do not automatically buff global HP

---

# 11. Difficulty gate comes later

Only after SKILLED_V2 is fitted/bounded sufficiently:

```text
P(full clear Stage1→50 | intended-entry SKILLED_V2_CENTRAL) < 0.60
```

for ordinary non-T1 Tiers.

The profile must not be reverse-engineered merely to hit 0.60.

Correct order:

```text
observed skilled behavior
 -> fitted player model
 -> synthetic slice
 -> full Tier
 -> measure clear/failure distribution
 -> tune encounter/economy/power curve
```

not:

```text
desired 60% number
 -> weaken player model until simulation matches
```

---

# 12. Lv31 / EXP interaction

Once fitted traces exist, player performance also affects EXP acquisition and skill reach.

Later full-Tier simulation must still enforce:
- Lv31 target unlock Stage41–45
- Stage46–49 post-Lv31 use/mastery
- Stage50 final application

If HIGH_MASTERY reaches Lv31 materially earlier, check whether late Tier content becomes trivialized.
Do not move Lv31 later solely to punish strong players if the CENTRAL target window remains correct.

---

# 13. Fitting admission outputs

Before a profile can be called `SKILLED_V2_*`, publish:

```text
harnessVersion
traceSchemaVersion
sampleCount / playerCount / sessionCount
context coverage H0..H5
cadence distributions
judgment distributions by context
combo survival / combo40 evidence
heavy / P×P behavior
turnover reacquisition
stateful response latency
degradation by context
holdout method
uncertainty / data gaps
role-expression regression result
```

Until then, profiles must be labeled:
`UNFITTED_CALIBRATION_BRACKET` or equivalent.

---

# 14. Current exact boundary

This document and its YAML/validator are the fitting **specification**, not fitted data.

Next executable research step requires observed controlled harness traces or an explicitly authorized playable harness implementation capable of collecting them.

Do not fabricate fitted probabilities in the absence of observed trace data.
