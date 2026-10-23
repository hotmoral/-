# P5 Stage48 Fodder-Chain + Global Standoff Boundary Result v0.1

Status: `DIAGNOSTIC_RESULT_USER_DECISION_REQUIRED_NO_ADOPTION_NO_FREEZE`

Date: 2026-10-23 KST

## 1. Authority boundary

This document records bounded diagnostic evidence only.

The user has approved **limited armored/hardened frontline as the primary exploration axis**.
That approval does **not** approve:
- `ARMORED_DURABLE_PROXY` as a production monster;
- HP1600 / armor0.55;
- exact body count, spawn timing or packet;
- a tenth ordinary monster;
- an elite/hardened production system;
- any SIEGER standoff value;
- any production gameplay change.

The user also proposed a new diagnostic hypothesis:

> If Mage's follow-up chain is consuming SIEGER, add small ordinary bodies with carefully chosen speed/order so those bodies occupy chain-target opportunities before SIEGER.

That hypothesis was tested as a diagnostic design axis and is supported in a bounded form below.

## 2. Fixed guards

All tests retained:
- physical right-edge spawn `x=0.92`;
- STAGE_SETTLED stage advancement;
- carried wall current/max/absolute deficit;
- no production modification;
- no class-stat modification;
- no Mage skill-rule modification;
- no SIEGER windup modification.

The old `ARMORED_DURABLE_PROXY` remains a diagnostic isolation body only.

## 3. Mage fodder chronology result

First screen run: `39963808641`.

Reference Stage48 diagnostic center used three spatially separated armored proxy bodies followed by SIEGER around `t=8.0`.

### No fodder
- SIEGER first damage about `0.075 s` after spawn;
- death about `3.45 s` after spawn;
- death position about `x=0.765`.

### Late GRUNT pair
- first damage delayed to about `1.575 s` after spawn;
- death delayed to about `4.575 s`;
- death position improved to about `x=0.714`.

### Late BRUTE pair control
- first damage similarly delayed;
- death about `6.075 s`;
- death position about `x=0.647`.

### Other ordinary bodies
- RUNNER/FLYER were often consumed too quickly to provide comparable protection;
- SHIELD/SPLITTER could interact badly with Mage area/phase chronology and were not clean chain sinks in the tested timings;
- sending bodies too early could shift Mage root/heavy phase so that SIEGER spawned into a stronger attack window, making the result worse.

Conclusion:

```text
FODDER_COUNT_ALONE != SOLUTION
FODDER_TYPE + ORDER + ARRIVAL_PHASE = CAUSAL
```

## 4. Phase robustness result

Run: `39964004587`.

SIEGER timing was shifted across approximately `7.70 / 8.00 / 8.30 s`.

Bounded findings:
- `GRUNT2` consistently delayed first SIEGER damage and extended lifetime versus no-fodder control;
- `GRUNT3` gave no material advantage over `GRUNT2` in the tested band;
- when GRUNT was the first cheap body, `GRUNT+RUNNER` / `GRUNT+FLYER` behaved similarly to GRUNT2;
- reversing the order so a fast fragile body arrived first removed much of the benefit;
- `BRUTE+GRUNT` gave protection close to `BRUTE2`, suggesting a useful role split: one durable first body + one cheap trailing body.

Therefore the user's fodder concept is **structurally valid as a chronology/target-order design axis**, not as indiscriminate extra mob count.

## 5. Reduced armored-count cross-class screen

Run: `39964154140`, BALANCED profile, global SIEGER standoff kept at provisional `0.38`.

### Three proxy + two GRUNT (`P3_GRUNT2`)
Approximate SIEGER death results:
- Knight `5.7 s`, `x≈0.673`
- Rogue `5.1 s`, `x≈0.691`
- Tank `6.825 s`, `x≈0.742`
- Archer `7.95 s`, `x≈0.562`
- Mage `4.575 s`, `x≈0.714`

All remained zero-shot/zero-windup at the old global standoff, but the packet was the cleanest balanced protection center found in this slice.

### Two proxy + two GRUNT (`P2_GRUNT2`)
Knight/Mage/Tank protection largely remained, but Rogue/Archer protection degraded materially.

### One proxy + BRUTE/GRUNT
The packet became highly class-skewed; Mage protection collapsed in a tested case.

### Real BRUTE/GRUNT only
Real BRUTE/GRUNT combinations helped some Tank/Archer cases but did not reproduce the cross-class protection envelope for Mage/Rogue.

Conclusion:

```text
REAL_BRUTE_GRUNT_ONLY = INSUFFICIENT_CURRENT_REPLACEMENT
P3_GRUNT2 = CLEANEST_CURRENT_DIAGNOSTIC_CENTER
```

This is not an adoption of three proxy bodies or two GRUNTs.

## 6. SUPPORTER speed-aura screen

Run: `39964353573`.

Adding an existing SUPPORTER to the armored+GRUNT screen modestly improved SIEGER death position in several classes, for example approximately:
- Mage `x≈0.714 -> x≈0.701`
- Tank `x≈0.742 -> x≈0.709`
- Archer also improved slightly.

However:
- lifetime improvement was small;
- SIEGER still did not reach meaningful firing state at global `0.38`;
- some BRUTE+SUPPORTER chronology aligned Mage's heavy window badly and caused severe regression.

Conclusion:

```text
SUPPORTER_SPEED_AURA = SECONDARY_TRAVEL_AID
SUPPORTER_PHASE_INTERACTION = ACTIVE_WATCH
```

## 7. Moderate global standoff scan

Run: `39964650488`.

Stage48 used the clean diagnostic center `P3_GRUNT2`; global SIEGER standoff was scanned across Stage46→49 with STAGE_SETTLED and carried wall deficit.

BALANCED, all five classes:

```text
x=0.38 : 5/5 survive; Stage48 all 0 shots
x=0.50 : 5/5 survive; Stage48 all 0 shots
x=0.55 : 5/5 survive; Stage48 all 0 shots
x=0.60 : 5/5 survive; Stage48 Archer 1 shot only
x=0.65 : 5/5 survive; Stage48 Archer 1 shot only
x=0.70 : 5/5 survive; Stage48 Knight 1 + Archer 1; Rogue/Tank/Mage 0
```

At `x=0.70`, cross-stage reserve was already heavily degraded in some classes:
- Archer final wall about `74` from `2320`;
- Tank final wall about `763` from `2320`.

Thus moderate global advancement still did not create all-class Stage48 role expression before cross-stage pressure became severe.

## 8. Exact boundary scan near first Mage firing region

Run: `39964922669`.

Thresholds `0.72 / 0.74 / 0.76` were tested globally, same Stage48 `P3_GRUNT2` diagnostic center, BALANCED profile, Stage46→49 STAGE_SETTLED.

### x=0.72
- 4/5 survive through Stage49;
- Archer buried at Stage49;
- Stage48 Knight/Archer fire, Rogue/Tank/Mage still zero;
- Tank final wall about `690`.

### x=0.74
- 4/5 survive;
- Archer buried at Stage49;
- Stage48 Knight/Rogue/Archer fire, Tank/Mage zero;
- Tank final wall about `625`.

### x=0.76
- first tested threshold where **all five classes get at least one Stage48 SIEGER shot**;
- Archer is already buried in Stage49;
- Tank final wall about `476`;
- cross-stage pressure is already structurally excessive.

Combined with the earlier corrected cross-stage results:
- `0.78` buried 7/20 representative cases;
- `0.82` buried 12/20.

## 9. Structural conclusion

Observed evidence supports this invariant:

```text
NO_OBSERVED_GLOBAL_STANDOFF_THRESHOLD
SIMULTANEOUSLY:
  (A) GIVES ALL-CLASS STAGE48 SIEGER FIRING
  AND
  (B) PRESERVES CURRENT STAGE46->49 SURVIVAL/RESERVE SHAPE
```

Therefore:

```text
GLOBAL_SIEGER_STANDOFF_AS_PRIMARY_STAGE48_REPAIR = STRONGLY_DISFAVORED_BY_CURRENT_EVIDENCE
```

This does **not** freeze `0.38` as a final production value.
It only says the current evidence gives no useful global-standoff repair window.

The user's fodder idea is retained as a valid axis:

```text
LIMITED_ARMORED_FRONTLINE
+ CHEAP_TARGET_LAYER (GRUNT-LIKE)
+ ORDER / TIMING / SPATIAL DENSITY
= CURRENT MOST PROMISING CHRONOLOGY FAMILY
```

## 10. User decision gate

No new design direction is adopted by this document.

Decision options:

### A — recommended
Keep global SIEGER standoff unchanged for now and continue Stage48 through:
- limited armored/hardened frontline;
- GRUNT-like cheap target layer;
- exact order/timing/spatial separation/travel budget;
- right-edge entry and STAGE_SETTLED unchanged.

### B
Introduce a Stage48-specific SIEGER setup/mechanic instead of changing the monster globally.
This is a semantic exception and requires a separate design decision.

### C
Relax Stage48 intent: Stage48 becomes protected-travel/threat introduction and guaranteed meaningful SIEGER firing is deferred to Stage49.
This changes the late-stage content-intent contract and requires explicit approval.

### D
Escalate to a more explicit hardened/elite/protective mechanic (resistance, aura, protection state, etc.).
This is more coupled and higher scope than A.

Current recommendation: **A**.

Reason:
- it preserves the user's approved armored exploration axis;
- the user's GRUNT/fodder hypothesis has real causal support;
- it does not require changing Mage skill semantics;
- it avoids the demonstrated cross-stage damage of global standoff movement;
- it keeps exact monster stats/content identity open until chronology is exhausted.

Stop here for user approval before adopting one of A/B/C/D.
