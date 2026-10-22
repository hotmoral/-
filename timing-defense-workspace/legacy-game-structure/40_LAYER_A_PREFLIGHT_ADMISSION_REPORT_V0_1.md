# Timing Defense — Layer-A Preflight Admission Report V0.1

Date: 2026-10-22 KST  
Status: **ADMISSION REVIEW / CLASS-AWARE COMBAT MICRO-SIM NEXT**

Evidence:
- `35_LAYERA0_ENCOUNTER_ENVELOPE_VALIDATION_REPORT_V0_1.md`
- `36_REPRESENTATIVE_RECIPE_STATIC_PREFLIGHT_REPORT_V0_1.md`
- `37_REPRESENTATIVE_RECIPE_KINEMATIC_PREFLIGHT_REPORT_V0_1.md`
- `38_FORMATION_DEPTH_SCHEMA_AMENDMENT_V0_1.md`
- `39_FRONTMOST_DPS_SENSITIVITY_REPORT_V0_1.md`

---

# 0. Admission question

Model A representative encounter recipes are now ready to enter **class-aware Layer-A combat micro-simulation**?

This review deliberately does not ask whether production balance is finished.

---

# 1. Encounter-envelope validation

Result:
```text
PASS errors=0 warnings=0
```

Confirmed:
- Tier roster unlock constraints
- legal archetype sets
- formation/cadence progression
- pressure labels
- feasible complexity ranges
- Lv31 Ascension consistency

A modeling error was corrected during validation:
- encounter-archetype complexity != Stage dominant complexity.

---

# 2. Representative static recipe validation

Result:
**PASS**

20 deterministic recipes cover representative T1–T4 questions.

Density summary:
- max authored 4s = 7
- max conservative effective 4s = 10
- no WATCH/ERROR in current static density guardrails

One genuine vocabulary leak was caught and corrected:
- T3 E17 used CD06 ESCORT
- changed to CD07 LATE_INSERT
- CD06 preserved as T4 novelty

---

# 3. Kinematic validation

Result:
**PASS WITH WATCHES**

Confirmed:
- T3 representative CHARGER telegraphs do not stack unreadably in current offsets
- E10 focused siege and E11 escorted siege produce distinct actual geometry
- E19 can produce a durable-screened first SIEGER shot
- E09/E16 produce meaningful support-aura windows

Structural defect discovered and fixed at schema level:
- nominal BACK role + delayed spawn was insufficient when backline unit moves faster than front unit
- formation authoring now requires explicit X-depth capability (`spawnXOffset` candidate)

This is a reusable authoring fix, not a one-off recipe hack.

---

# 4. Generic DPS sensitivity

Result:
**DIAGNOSTIC PASS / HIGH SENSITIVITY CONFIRMED**

Main finding:
Special mechanics can disappear or become dominant depending on frontline removal speed.

Examples:
- E11/E19 SIEGER fires under low generic DPS but may fire zero times at medium/high probe throughput
- E12/E19 SUPPORTER protected aura can range from very long to short
- CHARGER can be deleted before windup at high generic throughput
- SPLITTER child wall leakage falls sharply as throughput rises

Therefore:
- no production HP/count patch should be made yet
- capability uptime must be measured against class-aware action traces

---

# 5. Remaining blocker before exact Stage authoring

The blocker is **not** campaign structure anymore.

The blocker is:
> We do not yet have a sufficiently calibrated class-aware player-action model for the desired SKILLED_V2 difficulty target.

Needed next:
1. deterministic action-trace representation
2. class-aware damage/geometry/control paths
3. model modes:
   - CURRENT_AUTHORITY
   - LEGACY_PARITY_CANDIDATE
   - FUTURE_SKILL_PLACEHOLDER where required
4. SKILLED_V2 conservative/central/strong action traces or fitted parameters
5. capability uptime metrics under those traces

Do not bypass this by inventing one arbitrary DPS number.

---

# 6. Class-aware Layer-A required outputs

For each representative recipe × class × action profile:
- time to first kill
- kill order
- frontline block time
- target reorder count
- wall damage
- clear/end time
- peak active
- class opportunity realized

Special:
- CHARGER windups / completed / interrupted / erased-before-windup
- SPLITTER parent deaths / children / child wall occupancy
- SUPPORTER aura and screened aura uptime
- SIEGER first-shot probability / shot count / screened firing uptime
- FLYER geometry opportunity

Power modes must record skill state explicitly.

---

# 7. Admission verdict

## Result
**ADMIT TO CLASS-AWARE LAYER-A COMBAT MICRO-SIMULATION**

Upstream structure does not need another broad redesign before this step.

Model A remains:
- default bounded simulation spine
- NOT production freeze

Model B remains fallback only if T4 lower-layer evidence fails.

---

# 8. Explicit stop boundary

Do NOT yet:
- author exact 200 Stage launch campaign
- freeze monster HP/speed/armor
- freeze final launch Tier count
- freeze EXP formula
- freeze star/achievement values
- change live gameplay code

The next work is **micro**, not broad campaign redesign:
class-aware combat simulation of representative recipes, followed by synthetic slices only after PASS.
