# Timing Defense — Role Expression Admission Audit V0.1

Date: 2026-10-22 KST  
Status: **CRITICAL-SET AUDIT / NOT PRODUCTION BALANCE FREEZE**

Authority:
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `42_CLASS_AWARE_LAYER_A_MICROSIM_REPORT_V0_1.md`
- `44_ENTRY_DEPTH_ACTIVATION_WINDOW_REPORT_V0_1.md`

Machine-readable contract:
- `data/monster_role_expression_contract_v0_1.yaml`

Tools:
- `validate_monster_role_expression_contract.py`
- `evaluate_stateful_role_expression.py`

---

# 0. Admission question

Can the current Model-A representative encounter set proceed to synthetic Tier slices under the new rule:

> intended monster roles must not disappear before the player has a readable role-expression/counterplay opportunity?

Answer:

**NO — CRITICAL-SET ROLE-EXPRESSION ADMISSION IS STILL BLOCKED.**

The blocker is no longer broad campaign structure.
It is localized to encounter-level role expression and missing instrumentation.

---

# 1. Current nine-monster status

| Monster | Current status | Evidence |
|---|---|---|
| GRUNT | BASELINE_EXEMPT | neutral reference; no special gate |
| RUNNER | MEASUREMENT_REQUIRED | speed identity exists mechanically, but role-expression metric not yet instrumented |
| BRUTE | PRELIMINARY_ROLE_PRESENT / METRIC_REQUIRED | durable-frontline behavior appears, but block/screen metrics are incomplete |
| SHIELD | MEASUREMENT_REQUIRED | mitigation exists mechanically; prevented-damage / effective-hit role expression not yet audited |
| FLYER | MEASUREMENT_REQUIRED | geometry exists; actual geometry-opportunity metric incomplete |
| CHARGER | FAIL_DEFAULT_GEOMETRY | 60 pre-windup erasures and 0 windups in the prior critical class/trace sweep |
| SPLITTER | PARTIAL_PASS / WATCH | parent -> children transform works; meaningful child survival/frontline effect needs direct metrics |
| SUPPORTER | PASS_WITH_WATCH | aura expression exists; screened aura varies sharply by class/throughput |
| SIEGER | FAIL_DEFAULT_GEOMETRY | prior E11/E19 default class-aware sweep produced 0 shots; first-shot-opportunity instrumentation still needs refinement |

---

# 2. Spawn-delete rule applied

The following are now explicit structural failures in a designated role encounter:

- CHARGER repeatedly dies before visible windup
- SIEGER repeatedly dies before a real first-shot opportunity
- SUPPORTER dies without ever buffing another monster
- SPLITTER parent dies and its children produce no meaningful post-split state
- FLYER is removed before its vertical geometry can matter
- SHIELD is removed without mitigation changing any effective decision
- BRUTE is removed without functioning as a durable frontline
- RUNNER is removed before its speed changes arrival/front-order pressure

This does not protect monsters from skilled counterplay after their role becomes readable.

---

# 3. CHARGER current evidence

Default representative geometry:
- `T3_E07_M`
- `T3_E13_H`
- `T3_E17_M`

Prior critical sweep:
- three trace brackets
- five classes
- `CURRENT_AUTHORITY_LV6`
- 60 CHARGER parent observations
- 0 windups

Contract result:
`FAIL_DEFAULT_GEOMETRY`.

Geometry diagnostic then showed:
- E07 begins to expose windup for some classes around a ~0.25 X shift toward wall
- first observed interrupt behavior around ~0.30 in the diagnostic
- E17 with a protected CHARGER reaches all-five windup visibility around ~0.45

These are diagnostic search anchors only.
They are not production coordinates.

---

# 4. SIEGER current evidence

Default representative geometry:
- `T4_E11_M`
- `T4_E19_M`

Prior critical sweep:
- 0 SIEGER shots across all current class/trace probes

Contract result:
`FAIL_DEFAULT_GEOMETRY`.

Entry-depth diagnostic showed bounded activation windows:

E11:
- ~0.70: 5/5 classes saw >=1 shot
- ~0.75: 5/5
- ~0.80: 5/5
- ~0.85: 0/5

E19:
- ~0.70: 4/5
- ~0.75: 5/5
- ~0.80: 5/5
- ~0.85: 0/5

This proves a role-expression window exists, but does not yet prove it is readable/safe enough for production authoring.

---

# 5. SUPPORTER current evidence

Screened-aura ranges in the prior class-aware critical sweep:

- E12: ~0.155s to ~11.855s
- E16: ~0.005s to ~4.720s
- E19: ~1.205s to ~5.405s

Contract result:
`PASS_WITH_WATCH`.

Reason:
- minimum aura expression exists
- duration is highly class/throughput sensitive
- zero/near-zero values in some probes may still collapse the intended support identity

Required normalized metric:
`screenedAuraUptime / supporterAliveTime`.

---

# 6. SPLITTER current evidence

Current class-aware probes confirm:
- parent death
- two-child creation

But current optimistic trace probes produced no child wall leakage in sampled recipes.

Wall leakage is not required for minimum expression.
The required question is instead:

> did the split materially change active population, target order, or frontline occupancy for a meaningful interval?

Current instrumentation is insufficient to answer this robustly.

Contract result:
`PARTIAL_PASS / WATCH`.

---

# 7. Passive-role instrumentation gap

Before all-20-recipe admission, add direct metrics for:

## RUNNER
- distanceAdvanced
- timeToWallDeltaVsGrunt
- speed-driven front-order changes

## BRUTE
- frontlineBlockTime
- hitsReceived
- screenTimeProvided

## SHIELD
- mitigatedHits
- preventedDamage
- effectiveHitCount delta

## FLYER
- flyerGeometryOpportunityTime
- line/splash opportunity changes

These are not reasons to redesign the monsters.
They are missing observability needed to enforce the contract.

---

# 8. Admission state

Current critical-set result:

```text
ROLE_EXPRESSION_ADMISSION = BLOCKED
```

Reasons:
1. CHARGER default role-expression failure
2. SIEGER default role-expression failure
3. missing passive-role metrics
4. SPLITTER meaningful-child-lifetime metric incomplete
5. SIEGER first-shot-opportunity vs actual-shot distinction not yet instrumented

No upstream campaign redesign is required.

---

# 9. Exact next work

1. add role-expression fields/metrics to class-aware simulation output
2. fine-sweep CHARGER E07/E17 around known activation search regions
3. fine-sweep SIEGER E11/E19 around known activation search regions
4. reject ranges with unavoidable early wall damage or zero reaction window
5. preserve five-class structural opportunity without equalizing outcomes
6. add RUNNER/BRUTE/SHIELD/FLYER metrics
7. rerun critical subset
8. require critical-set role-expression PASS before expanding to all 20 recipes
9. only then return to fitted `SKILLED_V2` and synthetic Tier slices

---

# 10. Non-goals

Do not use this audit to:
- freeze monster HP
- freeze entry coordinates
- make every special ability always complete
- remove class asymmetry
- override frontmost targeting
- author exact 200 Stage campaign

The contract protects **meaningful role opportunity**, not guaranteed enemy success.
