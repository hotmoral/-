# Timing Defense — T1 2P Authoring Envelope V0.1

Date: 2026-10-22 KST  
Status: **SIMULATION CANDIDATE / NOT PRODUCTION BALANCE FROZEN**

Depends on:
- `13_T1_STAGE_SKELETON_CANDIDATE_V0_2.md`
- `10_ENCOUNTER_COMPLEXITY_MATRIX_V0_1.md`
- `04_MONSTER_ENCOUNTER_MODEL.md`
- `07_AUTHORING_DATA_SCHEMA.md`

Historical readability reference only:
- old 5-monster `PRESSURE_RECIPES_V1.md` 2P P95 4-second spawn density ≈ 11
- old 2P P95 6-second density ≈ 13.5

Those values are not copied as production limits.

---

# 0. 목적

T1 2-player baseline에서 각 encounter archetype이 **몇 개의 authored monster를 직접 생성할 수 있는지**를 먼저 bounded candidate로 정의한다.

아직 결정하지 않는 것:
- production HP
- production armor/speed
- reward
- final wall damage
- exact Stage duration
- final spawn millisecond values

이번 문서의 숫자는 simulator input candidate다.

---

# 1. Count vocabulary

## Authored count
Stage/encounter data가 직접 spawn하도록 적는 monster 수.

## Effective entity count
전투 중 생성된 entity까지 포함.

SPLITTER 1개가 죽어 child 2개를 만들면:

```text
1 authored SPLITTER -> 3 total effective entities over encounter lifetime
```

따라서 SPLITTER `n`개의 최대 추가 child volume:

```text
+2n
```

## Intensity buckets

- `L` — teaching / low
- `M` — standard T1 mixed
- `H` — high-pressure T1
- `X` — bounded extreme/stress candidate

`X`는 production default가 아니다.
T1 Stage49/50의 C4라고 해서 자동으로 X count를 쓰지 않는다.

---

# 2. 2P composition candidates

Abbreviations:
- G GRUNT
- R RUNNER
- B BRUTE
- SH SHIELD
- F FLYER
- C CHARGER
- SP SPLITTER
- SUP SUPPORTER
- SI SIEGER

## E01 BASELINE_MARCH

| Intensity | Candidate | Authored | Effective max |
|---|---|---:|---:|
| L | 4G | 4 | 4 |
| M | 6G | 6 | 6 |
| H | 8G | 8 | 8 |
| X | 10G | 10 | 10 |

T1 normal use: L/M. X is density stress only.

## E02 RUSH_WAVE

| L | 2G + 3R | 5 | 5 |
| M | 3G + 4R | 7 | 7 |
| H | 2G + 6R | 8 | 8 |
| X | 1G + 8R | 9 | 9 |

## E03 HEAVY_LINE

| L | 1B + 3G | 4 | 4 |
| M | 2B + 3G | 5 | 5 |
| H | 2B + 4G | 6 | 6 |
| X | 3B + 4G | 7 | 7 |

Count보다 BRUTE dwell/durability가 실제 압력일 가능성이 높다.

## E04 SHIELD_SCREEN

| L | 1SH + 3G | 4 | 4 |
| M | 1SH + 4G | 5 | 5 |
| H | 2SH + 4G | 6 | 6 |
| X | 2SH + 5G | 7 | 7 |

## E05 MIXED_WALL

| L | 1B + 1SH + 2G | 4 | 4 |
| M | 1B + 1SH + 3G | 5 | 5 |
| H | 1B + 2SH + 3G | 6 | 6 |
| X | 2B + 2SH + 3G | 7 | 7 |

## E06 AIR_PRESSURE

| L | 2F + 3G | 5 | 5 |
| M | 2F + 4G | 6 | 6 |
| H | 3F + 4G | 7 | 7 |
| X | 3F + 5G | 8 | 8 |

## E07 CHARGE_BREAK

| L | 1C + 3G | 4 | 4 |
| M | 1C + 4G | 5 | 5 |
| H | 2C + 4G | 6 | 6 |
| X | 2C + 5G | 7 | 7 |

## E08 SPLIT_FLOOD

| L | 1SP + 3G | 4 | 6 |
| M | 2SP + 3G | 5 | 9 |
| H | 2SP + 4G | 6 | 10 |
| X | 3SP + 4G | 7 | 13 |

Important:
- Effective max assumes every parent splits.
- child creation timing depends on kill timing, so static authored density is insufficient.
- T1 X should not be used before micro-sim proves child burst readable.

## E09 SUPPORT_COLUMN

| L | 1SUP + 4G | 5 | 5 |
| M | 1SUP + 2R + 3G | 6 | 6 |
| H | 1SUP + 2R + 4G | 7 | 7 |
| X | 1SUP + 3R + 4G | 8 | 8 |

T1 candidate keeps one SUPPORTER per authored encounter package by default.
Same-type aura stacking is forbidden by capability contract anyway.

## E10 SIEGE_LINE

| L | 1SI + 3G | 4 | 4 |
| M | 1SI + 4G | 5 | 5 |
| H | 1SI + 2R + 3G | 6 | 6 |
| X | 1SI + 3R + 3G | 7 | 7 |

T1 candidate keeps **one SIEGER** in an E10 package.
T4 may later explore multiple SIEGER compositions.

## E11 ESCORT_SIEGE

| L | 1SI + 1SH + 2G | 4 | 4 |
| M | 1SI + 1SH + 1B + 2G | 5 | 5 |
| H | 1SI + 2SH + 1B + 2G | 6 | 6 |
| X | 1SI + 2SH + 2B + 2G | 7 | 7 |

Actual pressure is screened firing uptime, not raw count.

## E12 BUFFED_BULWARK

| L | 1SUP + 1B + 1SH + 2G | 5 | 5 |
| M | 1SUP + 1B + 2SH + 2G | 6 | 6 |
| H | 1SUP + 2B + 2SH + 2G | 7 | 7 |
| X | 1SUP + 2B + 2SH + 3G | 8 | 8 |

## E13 RUSH_BREACH

| L | 1C + 3R | 4 | 4 |
| M | 1C + 4R + 1G | 6 | 6 |
| H | 2C + 4R | 6 | 6 |
| X | 2C + 5R | 7 | 7 |

M/H may have equal count but different CHARGER share.
This is intentional: intensity is not count-only.

## E14 AIR_RUSH

| L | 2F + 3R | 5 | 5 |
| M | 2F + 4R | 6 | 6 |
| H | 3F + 4R | 7 | 7 |
| X | 3F + 5R | 8 | 8 |

## E15 REPLICATE_RUSH

| L | 1SP + 3R | 4 | 6 |
| M | 2SP + 3R | 5 | 9 |
| H | 2SP + 4R | 6 | 10 |
| X | 3SP + 4R | 7 | 13 |

## E16 CASCADE

| L | 1SUP + 1SP + 3G | 5 | 7 |
| M | 1SUP + 2SP + 3G | 6 | 10 |
| H | 1SUP + 2SP + 2R + 2G | 7 | 11 |
| X | 1SUP + 3SP + 2R + 2G | 8 | 14 |

T1 Stage47/50 should begin simulation at L/M, not H/X.

## E17 BREACH_SCREEN

| L | 1C + 1SH + 2G | 4 | 4 |
| M | 1C + 1B + 1SH + 2G | 5 | 5 |
| H | 1C + 1B + 2SH + 2G | 6 | 6 |
| X | 2C + 1B + 2SH + 2G | 7 | 7 |

## E18 DUAL_AXIS

| L | 1SI + 2F + 2G | 5 | 5 |
| M | 1SI + 2F + 1SH + 2G | 6 | 6 |
| H | 1SI + 3F + 1SH + 2G | 7 | 7 |
| X | 1SI + 3F + 1SH + 1B + 2G | 8 | 8 |

BULWARK contribution is variant-dependent; E18 core identity remains AERIAL+SIEGE.

## E19 FORTRESS

| L | 1SI + 1SUP + 1SH + 1B | 4 | 4 |
| M | 1SI + 1SUP + 1SH + 1B + 1G | 5 | 5 |
| H | 1SI + 1SUP + 2SH + 1B + 1G | 6 | 6 |
| X | 1SI + 1SUP + 2SH + 2B + 1G | 7 | 7 |

T1 Stage49/50 default candidate = **L/M only**.
C4 complexity를 count까지 H/X로 올리는 것을 금지한다.

## E20 COLLAPSE_CHAIN
T1 V0.2에서 사용하지 않는다.
No T1 numeric envelope required yet.

---

# 3. Cadence bucket candidates

이 값은 simulator candidate이며 production ms freeze가 아니다.

## CD01 DRIP_SLOW
- unit gap: 900–1200 ms
- purpose: teaching / recovery / heavy readability

## CD02 DRIP
- unit gap: 650–900 ms
- purpose: ordinary sustained flow

## CD03 WAVE
- group size: 2–3
- within-group gap: 180–320 ms
- group gap: 1100–1600 ms
- purpose: visible packets without full burst saturation

## CD04 BURST_LIGHT
- unit gap: 140–220 ms
- one burst target size: normally 3–5
- purpose: T1 short pressure burst

## CD05 STAGGER
- type/group gap: 400–800 ms
- purpose: cause readable target-order changes

## CD06 ESCORT
- screen group spawns first
- protected/backline group delay: 500–900 ms
- purpose: intentional arrival/screening order

## CD07 LATE_INSERT
- baseline/screen establishes first
- special insert delay: 900–1600 ms
- purpose: SUPPORTER/SIEGER/CHARGER threat insertion

## CD08 OVERLAP_BOUNDED
- stage-level policy, not a raw unit gap
- next encounter begins while prior encounter may remain alive
- T1 use only after static/micro-sim confirms active-count envelope

---

# 4. Formation IDs V0.1

No final coordinates yet. These are authoring intent IDs.
Runtime target order remains position/validity authoritative.

## F01 LINE_LIGHT
- mostly one ground line
- low screening complexity
- penetration-readable

## F02 LINE_DURABLE_FRONT
- BRUTE/SHIELD intended to arrive before followers
- used for E03/E04/E05

## F03 CLUSTER_LIGHT
- close Y spacing
- Mage/AoE opportunity

## F04 SCATTER_LIGHT
- wider Y offsets
- lowers easy line/cluster exploitation

## F05 AIR_OFFSET
- FLYER offset from ground formation
- Y geometry is the purpose

## F06 SCREEN_BACKLINE
- ground screen FRONT/MID
- SIEGER or SUPPORTER intended BACK
- used E10/E11/E12/E19 variants

## F07 ESCORT_COLUMN
- durable screen first
- protected threat later via CD06

## F08 SPLIT_AXIS
- separated ground/air or two temporal groups
- used E18/selected variants

## F09 REPLICATION_CLUSTER
- SPLITTER parents placed so child spawn can create meaningful but bounded density
- child offsets remain capability-authoritative

---

# 5. T1 2P static readability guardrails — candidate only

Historical 5-monster 2P reference:
- P95 4s spawn ≈ 11
- P95 6s ≈ 13.5

New T1 V0.1 candidate deliberately starts below/around that envelope before SPLITTER child effects.

## Authored spawn creation
- normal target: max 4s authored spawns `<= 8`
- watch: `9–10`
- structural warning before simulation: `>10`

## Effective entity creation including SPLITTER children
- normal target: max 4s effective entity creation `<= 10`
- watch: `11–13`
- structural warning: `>13`

These are not runtime hard caps.
They are first-pass authoring/simulation alerts.

## Peak active count
Before exact combat simulation:
- target envelope: 6–8 active in most T1 situations
- watch: 9–10
- stress-only: 11+

This is not a production hard cap; actual kill speed, movement, stagger and SPLITTER timing determine true active count.

---

# 6. Count-specific structural guardrails

## SPLITTER
- authored count cannot be evaluated without effective count.
- 3-SP X packages generate up to +6 children.
- E16 X effective max 14 is **stress-only**, not T1 normal candidate.

## SUPPORTER
- T1 package default one SUPPORTER.
- difficulty comes from aura uptime and screened duration, not adding many SUPPORTERs.

## SIEGER
- T1 package default one SIEGER.
- difficulty comes from first-shot time, shot count, screening and reposition opportunity.
- multiple SIEGER packages are deferred to later Tier exploration.

## BRUTE/SHIELD
- do not use count plus durability multiplier plus support aura all at maximum in T1.

## CHARGER
- multiple CHARGERs may exist in H/X candidate, but telegraph readability is a mandatory micro-sim/device concern.

---

# 7. Initial intensity mapping by Stage band

Not exact per-Stage assignment yet.

- Stage1–9: L, occasional M checkpoint prep
- Stage10: M
- Stage11–19: L/M; Stage19 M
- Stage20–29: L/M; teaching starts L
- Stage30: M separated phases
- Stage31–39: M/H
- Stage40–48: H focused or M/H selected synergy
- Stage49: E19 L/M despite C4
- Stage50: E13 M/H -> E16 L/M -> E19 L/M

This prevents “late Stage = every axis X” behavior.

---

# 8. Cross-category consistency audit

## T1 structure
PASS candidate.
All used E01–E19 except E20 have a bounded 2P count envelope.

## Complexity
PASS candidate.
C4 E19 explicitly capped to L/M in T1.

## SIEGE/SUPPORT identity
PASS candidate.
Count scaling is intentionally conservative; uptime is the primary metric.

## SPLITTER
WATCH.
Effective creation can reach 13–14 in X packages; T1 should not use those without micro-sim.

## Historical readability
PASS as starting comparison.
Normal authored burst target <=8 is below old 2P P95 11 reference, leaving room for new stateful mechanics.

## Production authority
PASS.
No live coefficient or campaign patch is authorized by this document.

---

# 9. Exact next step

Before writing the full 50-stage numeric dataset:

1. map E01–E19 to allowed formation/cadence combinations,
2. choose representative L/M/H recipes for micro-sim,
3. statically compute authored 4s/6s burst for those recipes,
4. separately stress SPLITTER effective entity creation,
5. test SIEGER screened shot uptime,
6. test SUPPORTER screened aura uptime,
7. test CHARGER telegraph concurrency,
8. revise count/cadence envelope if needed,
9. only then assign exact candidate recipe to every T1 Stage.
