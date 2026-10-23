# Timing Defense — P4-D2 Stage49 Tank Time-Budget Role-Pulse Preflight V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED DIRECTIONAL AUTHORING PREFLIGHT / PROMISING ROLE MODULE / NOT A FULL STAGE RECIPE / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `102_P4D2_DURABLE_TEMPORAL_PRESSURE_DIRECTIONAL_PROBE_V0_1.md`
- `103_P4D2_TANK_BARRIER_FIDELITY_CORRECTION_V0_1.md`

Purpose:
Find a late-role-pressure module that:
- uses Tank's true barrier non-downgrade semantics;
- does not require nerfing Absolute Barrier;
- preserves a healthy all-success Mage margin compared with the previously too-harsh durable pulse;
- can consume Tank's time budget after sustained missed P×P windows;
- is used as one rotating grammar, not as the whole Stage49 recipe.

---

# 0. Important framing

One pressure grammar does **not** need to punish all five classes equally.

A healthy Stage48–49 rotation may intentionally distribute responsibility:
- durable/SIEGER role pulse challenges Tank time budget, Mage spacing and Archer geometry;
- frontline/breach grammar challenges Knight reset timing;
- target-persistent durable pressure challenges Rogue storm allocation;
- cluster/scatter/line patterns rotate which class has the easiest reset.

Therefore the acceptance question is:

> Can this module add a meaningful Tank/Mage late-game decision without becoming a universal hard counter?

not:

> Does every class lose the same HP after the same number of mistakes?

---

# 1. Light role-module candidate

Directional candidate only:

```text
pressure cycle ~4.6s diagnostic anchor
one ARMORED_DURABLE_PROXY every second cycle
+
three readable SIEGER threats every second cycle
+
SIEGER group arrives as a role pulse after the initial reset window
```

The durable proxy still uses the diagnostic center only:

```text
HP1600 / armor.55 / knock resistance.65
```

The SIEGER group is a diagnostic role pulse, not exact spawn geometry/cadence.

This module is intentionally lighter than the previously tested every-cycle durable+role patterns.

---

# 2. All-success directional margin

With all P×P opportunities successful in the bounded 60s stress:

```text
Knight  wall2000
Rogue   wall2000
Tank    wall2000
Archer  wall1325
Mage    wall1850
```

This is materially healthier than the strongest earlier durable-role pulse where Mage could fall near `560` or even be buried on all-success play.

Interpretation:
- Mage gets meaningful but recoverable pressure;
- Tank's intended all-success protection fantasy remains intact;
- Knight/Rogue are not killed first by a pressure pattern designed primarily to test Tank/Mage;
- Archer remains the main secondary watch because off-corridor SIEGER exposure can still create substantial wall pressure.

---

# 3. Tank time-budget exhaustion

Using Tank barrier non-downgrade fidelity, consecutive missed-final sensitivity in this light role module was directionally:

```text
2 consecutive misses -> wall1855
3 ->1785
4 ->1370
5 -> 831
6 -> 121
```

This is a much better shape for Tank than forcing one or two missed finals to be universally terminal.

Interpretation:

```text
Tank succeeds by buying time
+
one/two mistakes may remain recoverable
+
sustained P×P failure eventually exhausts the bought time
```

This matches class identity.

Therefore:

`TANK_LARGER_MISTAKE_BUDGET = ALLOWED`

provided sustained failure eventually creates real danger/burial in the full rotating Stage49 grammar.

---

# 4. Mage margin result

The light role module leaves Mage at approximately `1850` wall in the all-success stress.

That is preferable to using distributed durable pressure continuously for the whole stage.

Mage should instead receive alternating windows:

```text
distributed durable window
 -> pressure accumulates

clusterable durable / SIEGER window
 -> Arcane Collapse can recover value
```

This preserves Mage identity while still making spacing a late mastery axis.

---

# 5. Archer watch

Archer finished the light module around `1325` wall despite successful finals.

This does **not** imply Sky-Piercing Arrow should be nerfed or widened again.
The likely issue is that the diagnostic SIEGER group is deliberately off the current primary corridor too often.

Authoring repair order:
1. rotate aligned vs off-axis SIEGER pulses;
2. ensure SIEGER telegraph is readable before firing;
3. allow some role pulses to be solvable by Sky-Piercing line placement;
4. preserve other pulses where off-corridor threats remain relevant;
5. only then revisit exact width/damage if still necessary.

Thus:

`ARCHER_ROLE_PULSE_GEOMETRY_WATCH = ACTIVE`

---

# 6. Why this module is promising

The module demonstrates a useful late-game concept:

```text
initial final reset
-> durable remainder / role pulse appears
-> Tank barrier + push buys time
-> successful next finals keep control
-> sustained misses let synchronized role pressure consume the time budget
```

It also avoids the rejected approach:

```text
just add more HP / more bodies / faster universal spawn
```

which previously killed Knight/Rogue first without solving the intended Tank/Mage authoring problem.

---

# 7. Not a Stage49 freeze

Do not infer:
- exact 3-SIEGER count is final;
- exact every-second-cycle frequency is final;
- exact spawn x/bands are final;
- 60s is a stage duration;
- Tank should tolerate exactly 5 misses;
- Archer should lose exactly 675 wall;
- Mage should end exactly1850.

These are bounded directional authoring signals only.

---

# 8. Verdict

```text
STAGE49_TANK_TIME_BUDGET_ROLE_MODULE = PROMISING
TANK_CONTROL_AND_BARRIER_IDENTITY = PRESERVED
SUSTAINED_TANK_PXP_FAILURE_EVENTUALLY_DANGEROUS = YES
MAGE_ALL_SUCCESS_MARGIN = HEALTHIER_THAN_PREVIOUS_STRONG_PULSE
KNIGHT_ROGUE_EARLY_COLLAPSE = NO IN THIS MODULE
ARCHER_OFF_CORRIDOR_SIEGER_PRESSURE = WATCH
FULL_STAGE49_RECIPE = NOT APPROVED
NUMERICAL_FREEZE = NO
```

---

# 9. Next boundary

1. exact v0.3 checkout replay remains mandatory for class-fairness authority;
2. integrate this light role module as **one** rotating grammar candidate, not the entire stage;
3. alternate Archer-aligned and off-axis SIEGER geometry;
4. combine with existing frontline/cluster/scatter grammars so Knight/Rogue also face late mastery pressure through their own vulnerabilities;
5. keep Mage cluster-recovery windows;
6. reassess P4-D2 closure only after the full rotation is checked.
