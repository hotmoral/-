# Timing Defense — E11 Escort-Siege Timing Adjustment Report V0.1

Date: 2026-10-22 KST  
Status: **BOUNDED CENTRAL-TRACE DIAGNOSTIC / NOT PRODUCTION AUTHORING FREEZE**

Depends on:
- `48_ROLE_EXPRESSION_FINE_SCAN_REPORT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`

Probe mode:
- `CURRENT_AUTHORITY_LV6`
- `TRACE_BRACKET_CENTRAL`
- five classes
- E11 lower activation band near `shiftTowardWall ~= 0.70`

---

# 0. Problem

At the lowest all-five E11 SIEGER actual-shot sample near `0.70`, role expression existed for all five classes, but Archer allowed one ordinary GRUNT-equivalent contact wall hit in the diagnostic.

That meant:
- SIEGER role expression = good
- encounter wall leak = still WATCH

The goal was to remove the ordinary leak without:
- increasing SIEGER HP
- moving the entire formation farther forward
- deleting the escort/screen identity
- suppressing the first-shot opportunity

---

# 1. Bounded timing search

Search dimensions:
- whole-formation shift: approximately `0.69..0.73`
- delay applied only to the two ordinary GRUNT bodies
- GRUNT delay: `0..500ms` in small diagnostic steps
- SIEGER spawn timing: small `-100..+200ms` diagnostic variation

SHIELD and BRUTE timings were held fixed to preserve the core escort structure.

---

# 2. Best low-change candidate

A minimal clean candidate was found at approximately:

```text
shiftTowardWall = 0.70
GRUNT spawn delay = +250ms for both ordinary GRUNTs
SIEGER spawn delay = 0ms
```

Base E11 candidate:
```text
SHIELD   0ms
BRUTE    250ms
GRUNT    500ms
GRUNT    750ms
SIEGER   1550ms
```

Adjusted diagnostic candidate:
```text
SHIELD   0ms
BRUTE    250ms
GRUNT    750ms
GRUNT    1000ms
SIEGER   1550ms
```

---

# 3. Five-class CENTRAL result

At that diagnostic candidate:

| Class | SIEGER shots | ordinary contact wall leak | first shot |
|---|---:|---:|---:|
| Knight | 2 | 0 | ~4.465s |
| Rogue | 1 | 0 | ~4.465s |
| Tank | 2 | 0 | ~4.465s |
| Archer | 1 | 0 | ~4.755s |
| Mage | 1 | 0 | ~4.465s |

Interpretation:
- all five classes still experience SIEGER objective pressure
- the earlier Archer ordinary contact leak disappears
- class asymmetry remains: Knight/Tank permit two shots in this probe while Rogue/Archer/Mage permit one
- this is acceptable at the structural level because outcomes do not need to be equal

---

# 4. Why this is preferable to a durability buff

The defect came from encounter scheduling, not proof that SIEGER HP was globally too low.

A +250ms delay to two ordinary escort bodies:
- gives the player cleaner target turnover
- avoids an incidental wall leak
- preserves SIEGER activation
- preserves SHIELD/BRUTE escort identity
- does not alter global monster coefficients

This is consistent with the authoring order:

```text
geometry / cadence / screen timing
 -> role expression
 -> only then capability coefficients if still required
```

---

# 5. Current status

`E11_TIMING_CANDIDATE_FOUND`

But NOT admitted yet because:
- only the unfitted CENTRAL trace has been checked for this exact candidate
- first-shot opportunity vs actual-shot success is not yet explicitly separated in the canonical simulator
- CONSERVATIVE/STRONG trace robustness still needs testing
- fitted SKILLED_V2 is still future work

---

# 6. Next

1. store this as a diagnostic recipe override, not replacement production data
2. test CONSERVATIVE/CENTRAL/STRONG brackets
3. add first-shot-opportunity proxy/readability measurement
4. reject if Strong systematically erases the role before a readable window
5. reject if Conservative creates excessive repeated objective damage
6. only then promote E11 from WATCH to candidate PASS

No live gameplay code or production value is changed by this report.
