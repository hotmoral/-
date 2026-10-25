# Timing Defense — T1 Wave A Exact Spawn Authoring Baseline User Approved V0.1

Date: 2026-10-26 KST  
Status: **USER APPROVED AUTHORING BASELINE WITH WATCHES / NO PRODUCTION CHANGE / NO NUMERICAL FREEZE / NO FULL-T1 FREEZE**

## 1. User decision

The user explicitly approved promotion of the full Wave A exact-spawn candidates after full static closure.

Approved authoring target stages:
```text
A1 = [1,4,8]
A2 = [15,19]
A3 = [24,25,29,30,31]
A4 = [33,37,38]
```

The following exact candidate properties are now canonical **T1 authoring baseline WITH WATCHES** for those 13 stages:
- monster counts/types;
- exact spawn timestamps;
- exact Y positions;
- authored formation/cadence realization already admitted by the skeleton.

## 2. Exact identities adopted

```text
A1 SHA256 = 44616732b4cbba8bc52df294d98e0ab485b400d7ec7e9b9bfdd9f3fe32d2910d
A2 SHA256 = 2d3bf477e80617c0d26d2c349588caa446195b39c2581df0f11dd29eb1f37f8d
A3 SHA256 = 30860f1ff0911ff121491e62a5fa2ede84b43c6e4ce9bd7ec5f0f8a68d9592e6
A4 SHA256 = 93b9c785ca800ad97ad0149e9931e1d43b58328744dbb5867fdc5b9261dfef36
full accumulated Wave A SHA256 = 28b23f1f6332785009028ae9e531912c7dc2fb54da3a3a2db1536569b743774b
```

Static authority before adoption:
```text
A1 run 40193818274 = PASS
A2 run 40200875375 = PASS
A3 run 40205404257 = PASS
A4 run 40210214458 = PASS
full accumulated materialization = PASS
errors=[] / warnings=[] on final slice admissions
```

Source closure: `179_T1_WIDER_EXACT_AUTHORING_WAVE_A4_AND_FULL_STATIC_CLOSURE_V0_1.md`.

## 3. Adoption boundary

This approval means the exact Wave A spawn recipes are no longer merely diagnostic/candidate evidence. They are canonical authoring baseline for the 13 listed stages.

It does **not** authorize or freeze:
```text
production deployment
monster scalar changes
class scalar changes
shop / EXP / P×P changes
Archer exact Lv31 corridor width
Mage Lv31 numerical centers
full Stage1-50 exact recipe set
```

No production gameplay change occurred.

## 4. Lifecycle guard remains

Wave A targets are noncontiguous. Do not chain only Wave A stages as a persistent runtime sequence.

Persistent dynamic evidence requires real contiguous authored coverage, or a separately specified non-persistent diagnostic contract.

## 5. Cheapest next contiguous coverage

The smallest high-value contiguous completion is Stage15-25.

Already exact-authored in that interval:
```text
15 = Wave A approved
18 = representative authority
19 = Wave A approved
20-23 = representative v0.2 authority
24-25 = Wave A approved
```

Only missing exact recipes:
```text
16
17
```

Therefore the next bounded authoring package should materialize only Stage16 and Stage17, statically admit them, and then Stage15-25 becomes eligible for lifecycle-faithful persistent dynamic validation.

Skeleton authority:
```text
Stage16 = E03 / B / F02 / CD02 / C1 / BULWARK
Stage17 = E01 / G / F01 / CD03 / C1 / BASELINE
```

Stage16 should verify BRUTE durable-front readability after Stage15 pure teach and before Stage18 first mix.
Stage17 should deliberately decompress/recover before Stage18 without introducing any new mechanic.

## 6. Watches

Existing watches remain in force. No new watch is added by this adoption alone.

## 7. Conclusion

```text
FULL WAVE A EXACT SPAWN AUTHORING BASELINE = USER APPROVED WITH WATCHES
DYNAMIC EXECUTION = NOT YET AUTHORIZED BY CONTIGUITY
PRODUCTION = UNCHANGED / UNAUTHORIZED
NUMERICAL FREEZE = NO
FULL T1 RECIPE FREEZE = NO
NEXT = STAGE16_17 CONTIGUOUS-COVERAGE MATERIALIZATION + STATIC GATE
```
