# Timing Defense — P5/P6 Stage46-47 Armored Midwave Replacement Diagnostic V0.1

Date: 2026-10-24 KST  
Status: **DIAGNOSTIC RESULT / NO CONTENT ADOPTION / NO NUMERICAL FREEZE / NO PRODUCTION AUTHORITY**

Depends on:
- `143_P5_SKILLED_V2_LATE_RUN_REINTERPRETATION_AND_P5_P6_FIDELITY_GATE_V0_1.md`
- `144_P5_P6_PERSISTENT_STATE_FIDELITY_BRIDGE_RESULT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`

## 0. User hypothesis

The user clarified that the proposed “new armored monster” was **not a newly designed monster**. It refers to the existing temporary `ARMORED_DURABLE_PROXY` already used in Stage48 diagnostics: a BRUTE/SHIELD-like hardened diagnostic body.

Hypothesis:

> Stage46-47 high-volume pressure structurally favors Mage/Archer. Replacing a few ordinary bodies in the middle of the wave with the existing armored diagnostic body may interrupt mass-clear efficiency while preserving the current overall mastery difficulty.

No new monster identity or new scalar was authorized.

## 1. Probe design

Run:
- GitHub Actions run `39976475153`
- deterministic repeat: **PASS**
- output SHA256: `99f0c0e6a0137c1919b66754d7714d30b69a60e49cf37422296bff33b580d36c`

Temporary branch:
- `timing-defense-workspace-temp-armored-midwave`

Input basis:
- P5→P6 persistent-state fidelity bridge
- `SKILLED_V2_CENTRAL`
- 20 deterministic seeds × five classes = 100 skilled cases per variant
- entry charge boundary = 0 (prior bridge proved 0..3 is not the dominant cause)
- `BALANCED` diagnostic shop profile
- Stage48/49 unchanged
- total monster count unchanged
- only GRUNT bodies are replaced, so RUNNER/FLYER/SPLITTER/etc. role semantics are not removed
- existing `ARMORED_DURABLE_PROXY` anchor reused unchanged

Variants:

```text
BASELINE
  Stage46/47 unchanged

ARMOR1_PER_STAGE
  Stage46: one mid-stage GRUNT -> ARMORED_DURABLE_PROXY
  Stage47: one mid-stage GRUNT -> ARMORED_DURABLE_PROXY

ARMOR2_PER_STAGE
  Stage46: two GRUNTs around early/mid-late pressure -> ARMORED_DURABLE_PROXY
  Stage47: same
```

Actual replacement chronology:

```text
ARMOR1
Stage46 32.74s band +2
Stage47 30.24s band +2

ARMOR2
Stage46 20.68s band -1, 40.60s band -2
Stage47 19.18s band -1, 39.26s band -2
```

## 2. Skilled result

Through Stage49:

| Variant | Archer | Mage | Rogue | Knight | Tank | Total |
|---|---:|---:|---:|---:|---:|---:|
| BASELINE | 18/20 | 18/20 | 6/20 | 5/20 | 1/20 | 48/100 |
| ARMOR1_PER_STAGE | 17/20 | 17/20 | 6/20 | 5/20 | 1/20 | 46/100 |
| ARMOR2_PER_STAGE | 13/20 | 15/20 | 4/20 | 5/20 | 1/20 | 38/100 |

Failure-stage totals:

```text
BASELINE
Stage46 23
Stage47 21
Stage49  8

ARMOR1_PER_STAGE
Stage46 25
Stage47 23
Stage49  6

ARMOR2_PER_STAGE
Stage46 27
Stage47 24
Stage49 11
```

## 3. All-perfect control

All three variants:

```text
Knight 1/1
Rogue  1/1
Tank   1/1
Archer 1/1
Mage   1/1
TOTAL  5/5 through Stage49
```

Therefore the tested armored insertions did not remove the current all-perfect deterministic completion path.

## 4. Interpretation

### A. User hypothesis is directionally supported at low dosage

`ARMOR1_PER_STAGE` changed only the two currently strongest late-run classes in this paired sample:

```text
Archer 18 -> 17
Mage   18 -> 17
Rogue   6 -> 6
Knight  5 -> 5
Tank    1 -> 1
```

This is a **selective pressure signal**. A sparse armored midwave body can interrupt Mage/Archer throughput without immediately worsening the weaker three classes in the observed 20-seed sample.

### B. More armored bodies are not a free solution

At two replacements per Stage:

```text
Archer 18 -> 13
Mage   18 -> 15
Rogue   6 -> 4
```

Overall skilled completion also fell from `48%` to `38%`.

Thus:

```text
MORE_ARMORED_COUNT != BETTER_CLASS_BALANCE
```

The second armored body begins to create broad pressure rather than only trimming high-volume-clearing advantage.

### C. Sparse armored insertion is not a complete class-gap repair

One body per Stage reduced the high-end classes slightly but did not raise Knight/Rogue/Tank survival.

Therefore it should not be described as “solving” the entire class divergence. It is better classified as:

```text
SPARSE_ARMORED_MIDWAVE = PROMISING_SELECTIVE_ENCOUNTER_LEVER
NOT = COMPLETE_CLASS_BALANCE_FIX
```

### D. Geometry/chronology should be explored before changing the proxy scalar

Because `ARMOR1_PER_STAGE` showed the desired selective direction while `ARMOR2_PER_STAGE` over-pressured the field, the next low-cost diagnostic—if authorized by the current work direction—is **placement sensitivity of one armored body**, not higher count or immediate stat inflation.

Candidate axes:
- earlier vs midpoint vs later insertion;
- band alignment vs offset;
- interaction with current density peak / Archer strict-line opportunity / Mage cluster opportunity.

Do not change the armored anchor scalar until placement sensitivity is understood.

## 5. Authority boundary

This document does **not** approve:
- adding the armored body to production Stage46 or Stage47;
- one armored body per Stage as launch authoring;
- the current proxy HP/armor/knock/speed/wall values;
- a new monster identity;
- any class buff/nerf;
- any Stage46/47 exact cadence/count;
- any change to Stage48 or Stage49;
- any production implementation.

The existing armored body remains a diagnostic proxy only.

## 6. Current decision implication

Evidence now supports a narrower authoring hypothesis:

> A sparse, correctly placed hardened body may be useful for trimming Mage/Archer mass-clear advantage while retaining the intended skilled-vs-perfect mastery gap.

The tested center `1 armored replacement per Stage46/47` is **promising evidence, not an adopted packet**.

Any adoption of this as Stage46/47 content direction requires explicit user approval.
