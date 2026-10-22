# Timing Defense — Role Metrics V0.2 Instrumentation

Date: 2026-10-22 KST  
Status: **ANALYSIS TOOLING / EXISTING V0.1 EVIDENCE PRESERVED**

New tools:
- `tools/simulate_class_aware_role_metrics_v0_2.py`
- `tools/evaluate_role_expression_v0_2.py`

The original `simulate_class_aware_layer_a.py` V0.1 is intentionally left unchanged because earlier reports depend on its exact output semantics.

---

# 0. Purpose

The Role Expression Contract cannot be enforced reliably with clear time alone.
V0.2 adds direct telemetry for each current monster identity without changing live gameplay behavior.

---

# 1. New per-monster temporal tracking

For each spawned monster V0.2 tracks:
- spawn X
- minimum reached X
- alive time
- frontline time
- hits received
- raw damage attempted against it
- actual damage absorbed
- prevented damage

These rows are aggregated into `roleMetricsByType`.

---

# 2. RUNNER

New direct output:
- `runnerDistanceAdvancedMax`
- per-type alive/frontline time

Combined later with the structural speed anchor to determine whether RUNNER actually expresses approach pressure before deletion.

---

# 3. BRUTE

New direct outputs:
- `bruteFrontlineMs`
- `bruteHitsReceived`
- `bruteDamageAbsorbed`

This allows BRUTE to be judged by durable screening rather than clear time only.

---

# 4. SHIELD

New direct outputs:
- `shieldMitigatedHits`
- `shieldPreventedDamage`
- per-type frontline time

This distinguishes mathematical armor presence from actual mitigation expression in a combat trace.

---

# 5. FLYER

New geometry opportunity outputs:
- `flyerArcherLineOpportunityMs`
- `flyerMageSplashOpportunityMs`
- existing `flyerSkillHits`

At each simulation tick V0.2 checks whether a current FLYER is a legal secondary opportunity under the current Archer line or Mage splash geometry around the authoritative frontmost target.

This is still a bounded solo-slot geometry probe, not final production coverage.

---

# 6. CHARGER

Added:
- `chargerWindupVisibleMs`

Existing:
- windup entries
- completed charge
- interrupts
- erased-before-windup

Minimum contract can now be represented directly as:

```text
chargerWindups > 0
AND chargerWindupVisibleMs > 0
```

Exact readable minimum milliseconds remain OPEN.

---

# 7. SPLITTER

Added:
- `splitterChildAliveMs`
- `splitterChildFrontlineMs`
- `splitterTargetReorders`
- `splitterPeakActiveDelta`

This closes the earlier ambiguity where children spawned correctly but might have disappeared before changing the combat state.

Minimum structural consequence precheck becomes:

```text
children > 0
AND childAliveMs > 0
AND one of:
  childFrontlineMs > 0
  targetReorders > 0
  peakActiveDelta > 0
```

---

# 8. SUPPORTER

Added:
- `supporterAliveMs`
- `supportAuraTargetCount`
- `supportScreenedAuraRatio`

Existing aura/screened-aura milliseconds remain.

This allows duration to be normalized instead of comparing raw aura seconds across encounters of different length.

---

# 9. SIEGER

Added:
- `siegerOpportunityEntries`
- `siegerWindupVisibleMs`
- `siegerErasedBeforeOpportunity`

This is the most important V0.2 distinction.

Minimum contract is now based on:

```text
standoff/windup opportunity exists
AND visible windup time exists
```

not:

```text
shotCount > 0
```

Actual shot success remains a difficulty/outcome metric.

---

# 10. Wall damage decomposition

V0.2 outputs:
- `wallDamageByType`
- `wallHitsByType`

SIEGER shot damage uses the explicit `SIEGER_SHOT` key.
Ordinary body contact remains keyed by monster type.

This is required to distinguish:
- intended special-objective pressure
- accidental ordinary contact leak

---

# 11. Automatic evaluator

`evaluate_role_expression_v0_2.py` consumes V0.2 JSONL plus:
- `data/monster_role_expression_contract_v0_1.yaml`

It can require all five classes to show structural role expression.

Current gates intentionally use **nonzero structural evidence only**.
Exact quantitative thresholds remain open until player calibration.

---

# 12. Remaining work

V0.2 instrumentation makes the next critical-set rerun technically well-defined.

Still required:
1. run candidate geometry overrides through V0.2
2. evaluate 10 critical recipes × 3 brackets × 5 classes
3. inspect failures for true role erasure vs intentionally absent role monster
4. set only bounded pre-SKILLED structural gates
5. expand to 20 recipes only after critical-set PASS

No live gameplay source or production balance coefficient is changed by this instrumentation.
