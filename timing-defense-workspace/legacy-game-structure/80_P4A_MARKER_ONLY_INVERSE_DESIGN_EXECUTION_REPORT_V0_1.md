# Timing Defense — P4-A Marker-Only Inverse Design Execution Report V0.1

Date: 2026-10-23 KST  
Status: **P4-A PASS / CENTRAL UNIVERSAL CURVE FEASIBLE / NUMERIC CANDIDATES NOT FROZEN**

Depends on:
- `78_P4_FULL_PLAYER_POWER_SPINE_EXP_MODEL_PROPOSAL_V0_1.md`
- `79_P4_EXP_AND_PLAYER_POWER_SPINE_APPROVED_CONTRACT_V0_1.md`
- `28_MODEL_A_TIER_AUTHORING_WINDOWS_V0_1.md`
- `29_MODEL_A_TIER_PRESSURE_COMPLEXITY_ENVELOPE_V0_1.md`
- `32_MODEL_A_TIER_ENCOUNTER_AVAILABILITY_V0_1.md`
- `33_MODEL_A_FORMATION_CADENCE_VOCABULARY_V0_1.md`
- `34_MODEL_A_FREQUENCY_RANGE_ENVELOPE_V0_1.md`

Machine evidence:
- `data/p4a_marker_opportunity_corpus_v0_1.json`
- `data/p4a_marker_inverse_design_summary_v0_1.json`
- `../tools/run_p4a_marker_inverse_design_v0_1.py`
- `../tools/validate_p4a_marker_inverse_design_v0_1.py`

---

# 0. Question

Can one universal run-local EXP curve plausibly place the six skill milestones in the intended Stage windows across T1–T4 **without**:
- class-specific XP multipliers;
- Tier-specific hidden XP multipliers;
- flattening every Tier into the same Stage-flow shape;
- inventing Lv26/Lv31 power proxies;
- or authoring the final 200 launch Stages early?

P4-A marker-only answer:

**YES for the CENTRAL synthetic opportunity envelopes.**

This is not yet a P4 full-power answer because skill power is disabled in P4-A.

---

# 1. Executed corpus

```text
T1 × LOW/CENTRAL/HIGH
T2 × LOW/CENTRAL/HIGH
T3 × LOW/CENTRAL/HIGH
T4 × LOW/CENTRAL/HIGH
= 12 synthetic 50-Stage fixtures

100 deterministic SKILLED_V2_CENTRAL streams per fixture
= 1,200 marker-only synthetic Tier runs
```

The fixtures are calibration envelopes, not production Stage authoring.

The player-model stream remains deterministic/streak-aware and persistent through each 50-Stage synthetic Tier.

---

# 2. Static corpus gates

All final fixtures pass the bounded authoring checks used by P4-A:

```text
fixtureCount                 PASS
Tier encounter availability  PASS
teaching / earliest-use      PASS
pressure presence ranges     PASS
complexity count ranges      PASS
10-Stage class opportunity   PASS
formation/cadence vocabulary PASS
C4 boundedness               PASS
exact-signature triple guard PASS
```

T4 specifically satisfies both SUPPORT/SIEGE Tier identity and bounded C4 use without forcing every late Stage into fortress-like maximal complexity.

---

# 3. Workload semantics

P4-A uses `workloadEhp` only as a relative timing-opportunity proxy.

It is derived from existing provisional monster HP/armor anchors and representative encounter packages.

It is **not**:
- production monster HP authority;
- a new Stage HP growth formula;
- production difficulty;
- clear-rate evidence;
- exact Stage authoring.

No automatic per-Stage HP escalation formula was introduced.

LOW/CENTRAL/HIGH differ by legal encounter-package composition and placement, not by a hidden universal HP multiplier.

---

# 4. First diagnostic and bounded refinement

The first CENTRAL pass did not immediately support one universal threshold at every milestone.

Result before refinement:
- Lv6 feasible;
- Lv11 feasible;
- Lv16 universal CENTRAL P50 interval **empty**;
- Lv21 universal CENTRAL P50 interval **empty**;
- Lv26 feasible;
- Lv31 feasible.

Cause classification:

**OPPORTUNITY_SHAPE_MISMATCH, not immediate EXP-formula failure.**

T2 had too much relative timing workload concentrated in the mid band while T4 had too little in the corresponding band.

Under the user-approved P4 rule, the response was not to add hidden Tier EXP multipliers.
Instead the synthetic corpus was boundedly redistributed while preserving each Tier identity:
- T2 CENTRAL: some mid-band workload shifted later inside existing mitigation/geometry vocabulary and static ranges;
- T4 CENTRAL: some support/siege-compatible workload shifted earlier inside existing formation/siege vocabulary and static ranges.

No new production Stage recipe was frozen.

After this bounded redistribution, all six CENTRAL T1–T4 universal threshold intersections became non-empty.

---

# 5. CENTRAL opportunity scale

Final CENTRAL marker workload/turn evidence:

| Tier | Relative workloadEhp | P50 completed turns | P50 Stage50 XP_CREDIT |
|---|---:|---:|---:|
| T1 | 118860 | 507 | 1128.5625 |
| T2 | 120050 | 509 | 1139.8750 |
| T3 | 118490 | 506 | 1123.6250 |
| T4 | 134290 | 567 | 1258.3750 |

These totals do not imply that Tier flows are identical.
T4 remains formation/siege-heavy and carries higher marker workload in this corpus.

---

# 6. Universal CENTRAL P50 threshold feasibility

Using the approved target windows, the marker-only CENTRAL corpus produced these common feasible cumulative XP_CREDIT intervals:

| Milestone | Target Stage window | Common feasible threshold interval |
|---|---:|---:|
| Lv6 | 5–7 | `(119.7500, 141.4375]` |
| Lv11 | 11–14 | `(227.5000, 276.1875]` |
| Lv16 | 18–21 | `(382.0625, 396.7500]` |
| Lv21 | 25–28 | `(532.8125, 591.5625]` |
| Lv26 | 32–36 | `(702.6250, 793.1250]` |
| Lv31 | **41–45** | `(973.0000, 1002.6875]` |

Every interval is non-empty.

Therefore P4-A provides evidence that a universal class/Tier EXP curve is structurally feasible at the marker-only CENTRAL layer.

---

# 7. First-pass midpoint anchor candidates — NOT FROZEN

For the sole purpose of giving P4-B a neutral starting point, P4-A records the midpoint of each feasible interval:

```text
A6   = 130.59375
A11  = 251.84375
A16  = 389.40625
A21  = 562.18750
A26  = 747.87500
A31  = 987.84375
```

These are **simulation candidates only**.

They are not:
- final EXP requirements;
- player-visible EXP integers;
- production values;
- P17 numerical freeze.

P4-B is expected to move these if actual Lv6–21 combat power changes later timing opportunities.

---

# 8. CENTRAL reach at midpoint candidates

P50 unlock Stage by Tier:

| Milestone | T1 | T2 | T3 | T4 | Target |
|---|---:|---:|---:|---:|---:|
| Lv6 | 7 | 6 | 5 | 7 | 5–7 |
| Lv11 | 13 | 11 | 12 | 13 | 11–14 |
| Lv16 | 19 | 18 | 19 | 21 | 18–21 |
| Lv21 | 26 | 27 | 26 | 27 | 25–28 |
| Lv26 | 34 | 34 | 34 | 34 | 32–36 |
| Lv31 | 43 | 43 | 45 | 41 | **41–45** |

Lv31 P75/P90 marker-only evidence:

```text
T1  43 / 43
T2  44 / 44
T3  45 / 45
T4  42 / 42
```

Tail acceptance criteria remain intentionally unfrozen until full P4 evidence exists.

---

# 9. LOW/HIGH stress-envelope result

LOW/HIGH opportunity envelopes are sensitivity probes, not additional milestone targets.

They deliberately show that progression timing is sensitive to encounter workload.

Example Lv31 P50 at the midpoint candidate:

```text
T1 LOW 49 / CENTRAL 43 / HIGH 40
T2 LOW 51 / CENTRAL 43 / HIGH 37
T3 LOW 51 / CENTRAL 45 / HIGH 41
T4 LOW 48 / CENTRAL 41 / HIGH 40
```

Interpretation:
- the EXP curve cannot compensate for arbitrarily sparse/dense combat opportunity without changing progression timing;
- this sensitivity should remain visible rather than being hidden behind automatic Tier XP multipliers;
- later encounter authoring and player-power coupling must converge around a viable opportunity envelope.

This is consistent with the approved rule that EXP must not homogenize Tier identity.

---

# 10. Validation result

Final bounded local re-execution against the compact corpus and validator produced:

```json
{"recordType":"P4A_VALIDATION","result":"PASS","errors":[],"fixtures":12,"seedsPerFixture":100,"allCentralIntersectionsNonEmpty":true,"warning":"P4-A marker-only diagnostic; candidate anchors are not numerically frozen."}
```

Canonical repository blobs at this report boundary:

```text
runner    0892f332cd177e78b8fa4e31522563a9809b049e
validator ebd5e932189e70891a8e4d4edf65f997e70f367b
corpus    c3f1dff341e65bf81204ad360bafa3cdce7c4c7d
summary   3f21f1a3ee46b8bc0b297e035ffca5b8a97d0652
```

The compact corpus and validator were also hash-matched to the locally re-executed copies. Runner representation was reviewed for the same P4-A algorithm/data semantics; this report does not claim a four-file byte-identical local mirror.

---

# 11. What P4-A proves

P4-A supports:
- one universal EXP-curve direction remains viable;
- Tier-specific hidden XP multipliers are not required at marker-only CENTRAL;
- exact Stage-flow identity need not be homogenized;
- encounter opportunity placement materially affects milestone timing;
- bounded encounter redistribution can repair progression-shape mismatch before adding hidden progression correction;
- Lv31 Stage41–45 is achievable simultaneously across T1–T4 CENTRAL marker-only fixtures.

---

# 12. What P4-A does NOT prove

P4-A does not establish:
- final XP_CREDIT quality weights;
- final A6/A11/A16/A21/A26/A31;
- exact intermediate level thresholds;
- player-visible EXP scale;
- actual class-specific skill-power feedback;
- final Lv26/Lv31 mechanics;
- production Stage recipes;
- Base HP / fail rate / clear rate;
- shop or permanent-power coupling;
- final P75/P90 gates;
- production numerical balance.

---

# 13. Next boundary

P4-A is complete for its approved scope.

Next internal gate:

```text
P4-B — LV6_TO_LV21_COMBAT_FEEDBACK_INTEGRATION
```

P4-B may use:
- current authoritative Lv6 behavior;
- exact v0.16 Lv11/Lv16/Lv21 mechanics as simulation-only parity candidates;
- the P4-A midpoint anchors only as starting candidates.

P4-B must measure actual class-specific changes in kill speed / timing-turn opportunity and then re-evaluate the universal milestone curve.

Lv26 and Lv31 power remain OFF until their separate user-decision gates.