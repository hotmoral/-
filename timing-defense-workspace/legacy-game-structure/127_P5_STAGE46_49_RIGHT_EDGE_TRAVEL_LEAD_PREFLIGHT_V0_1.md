# Timing Defense — P5 Stage46–49 Right-Edge Travel-Lead Preflight V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL KINEMATIC PREFLIGHT / NORMAL RIGHT-EDGE ENTRY REQUIRED / NAKED EARLY SIEGER REJECTED / ESCORTED TRAVEL NEXT / NO PRODUCTION FREEZE**

Depends on:
- `126_P5_POST_SHOP_STAGE49_ENTRY_DEPTH_RECONVERGENCE_V0_1.md`
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`

Assets:
- `data/p5_stage46_49_right_edge_lead_fixture_v0_1.json`
- `data/p5_stage46_49_right_edge_lead_preflight_summary_v0_1.json`
- `../../tools/run_p5_stage46_49_right_edge_lead_preflight_v0_1.py`

---

## 0. User clarification / corrected implementation intent

The user explicitly rejected an ambiguous interpretation of the prior `spawnX` experiment.

Production-facing intent is now explicit:

```text
NO mid-field pop-in.
Enemies still appear from the normal right edge.
Late-role threats may appear earlier so they have naturally traveled farther by the later pressure moment.
```

Therefore doc126's row-level `spawnX` override is retained only as a **spatial-pressure proof**. It is not the preferred implementation/authored-spawn mechanism.

---

## 1. Converting the old spatial proxy into travel lead

Diagnostic right-edge spawn anchor:

```text
normal spawnX = 0.92
```

Current provisional speeds:

```text
SIEGER = 0.045
ARMORED_DURABLE_PROXY = 0.040
```

The prior promising Stage49 spatial proxy used approximately:

```text
SIEGER x = 0.48
durable x = 0.65
```

If untouched, equivalent travel leads from x=0.92 are:

```text
SIEGER: (0.92 - 0.48) / 0.045 ~= 9.78 s
durable: (0.92 - 0.65) / 0.040 = 6.75 s
```

Sensitivity conversion:

```text
SIEGER x 0.45..0.55 -> about 8.22..10.44 s lead
durable x 0.60..0.70 -> about 5.50..8.00 s lead
```

These are kinematic conversions only, not production values.

---

## 2. Candidate Stage46–49 travel-lead ramp

First directional ramp:

```text
Stage46: SIEGER 4.0 s early / durable 3.0 s early
Stage47: SIEGER 6.0 s early / durable 4.5 s early
Stage48: SIEGER 8.0 s early / durable 6.0 s early
Stage49: SIEGER 9.75 s early / durable 6.75 s early
```

Intended gameplay progression:

```text
46 = power revelation / light escort
47 = escorted second pulse
48 = protected role pulse
49 = durable frontline + SIEGER time budget
```

At the later pressure-reference moment, untouched SIEGER positions are approximately:

```text
46 -> x0.74
47 -> x0.65
48 -> x0.56
49 -> x0.481
```

This gives a coherent late-Tier ramp without teleporting an enemy into the field.

---

## 3. Critical finding — naked early SIEGER is the wrong implementation

At the current P5 40%-legacy shop diagnostic center with BALANCED ATK rank8:

```text
ATK multiplier ~= 1.256
```

Approximate ordinary PERFECT root packages against SIEGER HP520 imply roughly:

```text
Knight  -> 2 roots
Rogue   -> 2 roots
Tank    -> 3 roots
Archer  -> 2 roots
Mage    -> 3 roots
```

But the proposed lead windows expose a naked SIEGER for approximately:

```text
4.0 s lead  -> ~3 root opportunities
6.0 s lead  -> ~5
8.0 s lead  -> ~7
9.75 s lead -> ~8
```

Therefore simply spawning an isolated SIEGER earlier can make the encounter **easier**, because the player receives many extra ordinary attacks before the role threat matures.

Classification:

```text
MIDFIELD_POP_IN_REQUIRED = FALSE
NAKED_EARLY_SIEGER_IS_SAFE_REPLACEMENT = FALSE
ESCORT_OR_FRONTMOST_PROTECTION_REQUIRED = TRUE
```

---

## 4. Correct next authoring language

The next combat probe must use:

```text
normal right-edge spawn
+ earlier SIEGER entry
+ frontmost escort/frontline protection
+ increasing protection from Stage46 -> Stage49
```

Not:

```text
mid-field spawning
blanket SIEGER HP inflation
hidden Archer/Mage shop nerf
Lv31 power nerf
```

Protection should be readable and counterable, not hard lockout.

Useful structure:

```text
Stage46:
light front line; strong play may still erase SIEGER early

Stage47:
clear escort relationship / second pulse

Stage48:
durable or role-bearing frontline protects an off-axis SIEGER long enough to create a decision

Stage49:
distributed durable frontline + timed SIEGER pulse; repeated P×P failure must consume wall reserve
```

Because target selection is frontmost, relative placement and band geometry can protect the SIEGER naturally while still allowing class-specific answers.

---

## 5. Admission target for full combat reconvergence

With shop power present:

```text
all-success -> all classes survive and Lv31 remains spectacular
one mistake -> recoverable
Stage46-47 two mistakes -> recoverable
Stage48-49 two mistakes -> may be harsher but must remain readable/fair
repeated mastery failure -> every class eventually dies or enters Stage50 in a clearly poor state
```

Identical mistake budgets are not required.

---

## 6. Exact next step

Build a full-combat Stage46–49 directional fixture where:

1. every authored enemy starts at the normal right-edge `spawnX`;
2. role threats use `spawnLeadSeconds` / earlier schedule times rather than row-level mid-field `spawnX`;
3. a warmup/reference offset prevents negative spawn times;
4. SIEGER lead is accompanied by frontmost protection rather than naked exposure;
5. Stage46→49 progressively strengthens protection/second-pulse timing;
6. ATK/FORT/DEF shop power remains present;
7. KNOCK and CRIT/CRITDMG remain in their separately deferred fidelity lanes.

No production implementation or numerical freeze is authorized by this preflight.
