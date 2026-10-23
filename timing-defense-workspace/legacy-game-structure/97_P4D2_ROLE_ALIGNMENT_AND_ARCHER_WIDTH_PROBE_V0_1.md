# Timing Defense — P4-D2 Role Alignment & Archer Width Probe V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED STRUCTURAL/GEOMETRY FEEDBACK / ARCHER MID-WIDTH CANDIDATE PREFERRED / NO NUMERICAL FREEZE / P4-D2 CONTINUES**

Authority:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
- `45_MONSTER_ROLE_EXPRESSION_CONTRACT_V0_1.md`
- `../MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md`

Machine-readable geometry fixture:
- `data/p4d2_archer_width_role_alignment_v0_1.json`

---

# 0. Questions

After user approval of the wider Lv31 Archer corridor:

1. Can the final arrow become materially wider without turning into a screen-wide AoE?
2. Can SUPPORTER/SIEGER off-corridor protection still matter?
3. Can current Lv31 final-skill identities preserve meaningful CHARGER/SIEGER/SPLITTER decisions in Stage46+ mastery encounters?
4. What encounter-grammar direction should be used next to repair the miss-severity divergence seen in document 95?

Answer:

**YES — a middle-width Archer candidate preserves the desired distinction, and the next repair layer should be encounter grammar rather than class nerfs or monster-HP inflation.**

---

# 1. Archer width: deterministic five-band abstraction

This is a geometry abstraction only. Diagnostic bands are **not production lanes** and do not freeze normalized collision width.

Test candidates:

```text
NARROW       = aim band only
MID_ADJACENT = aim band + immediately adjacent bands
FULL5        = all five diagnostic bands, overbroad comparison endpoint
```

Formation results:

| Formation | NARROW | MID_ADJACENT | FULL5 |
|---|---:|---:|---:|
| aligned depth: 5 enemies on aim line | 5/5 | 5/5 | 5/5 |
| near-line: 3 center + 2 adjacent | 3/5 | **5/5** | 5/5 |
| scatter: one enemy per band | 1/5 | **3/5** | 5/5 |
| protected backline: 3 center + SUPPORTER/SIEGER far offset | 3/5 | **3/5** | 5/5 |

Interpretation:

- `NARROW` fails to make the final arrow's huge scale mechanically meaningful against near-line pressure.
- `FULL5` removes too much positioning language and starts behaving like a screen-wide selection/AoE tool.
- `MID_ADJACENT` is the best current structural center:
  - it still deletes true aligned depth;
  - it catches nearby bodies that a huge arrow should plausibly clip;
  - it does not automatically erase deliberately off-corridor SUPPORTER/SIEGER placement;
  - it preserves Archer as a **wide straight-line** class rather than an area caster.

Therefore:

`ARCHER_WIDTH_DIAGNOSTIC_CENTER = MID_ADJACENT`

This is **not** a production width freeze.

---

# 2. Protected SUPPORTER/SIEGER geometry

The approved Archer principle does not mean every specialist behind a frontline should die automatically.

Authoring rule to carry forward:

```text
if specialist is genuinely aligned / near-aligned with the authoritative shot corridor
-> Sky-Piercing Arrow may erase it through the frontline

if specialist is deliberately displaced outside the final-arrow corridor
-> protection/positioning remains meaningful
```

This makes Archer's mastery decision readable:
- a good line is a major payoff;
- a bad line does not become free homing or screen-wide deletion.

Do not repair off-line specialist survival by adding arbitrary HP to SUPPORTER/SIEGER.

---

# 3. CHARGER role alignment — Knight/Tank finals

Current CHARGER capability:

```text
ADVANCE -> WINDUP(650ms) -> CHARGE
any authoritative positive knockback during WINDUP cancels the current windup
```

Therefore the desired Stage46+ authored interaction is straightforward:

```text
CHARGER WINDUP becomes visible
-> player successfully reaches/uses P×P final
-> Knight/Tank final knockback interrupts or removes the threat
```

This is **valid role expression**, because the CHARGER decision was exposed before the counterplay.

Invalid authoring would be routine removal before the WINDUP is ever readable.

No new CHARGER HP scalar is justified at this stage.

---

# 4. SIEGER role alignment — Knight/Tank/Archer

Current SIEGER capability:

```text
advance -> standoff -> WINDUP(800ms) -> wall shot -> repeat
knockback beyond valid siege range cancels active windup/repeat and forces reposition
```

Desired Stage46+ interactions:

### Knight / Tank
- allow SIEGER to reach or visibly enter standoff/windup in designated mastery windows;
- a correctly timed final knockback may cancel the shot and force reposition;
- exact displacement margin remains a numeric P4-D2/P8 calibration issue.

### Archer
- if the player earns an actual line through frontline -> SIEGER, the final arrow may delete the SIEGER;
- if the SIEGER is intentionally placed outside the final corridor, the player does not get free off-line deletion.

The role-expression requirement is therefore not `SIEGER must always fire once`.
It is that the SIEGER pressure/telegraph creates a readable decision opportunity before mastered counterplay resolves it.

---

# 5. Mage / SPLITTER chronology

The Mage Lv31 final is intentionally capable of suppressing a SPLITTER rebound when the player catches the package correctly.

Current relevant chronology:

```text
root/direct impact or staged blast kills SPLITTER parent
-> children spawn immediately
-> later collapse stages / bounded final chain resolve chronologically
```

With the current provisional Lv31 damage centers, newly spawned 120-HP children inside the active collapse area can be removed by later stages or by the bounded final chain.

At Stage46+ this is **not automatically a failure**.
It can be the correct mastery payoff:

```text
successful well-timed Arcane Collapse
-> suppresses the rebound

missed P×P / off-circle SPLITTER / late-arriving SPLITTER
-> children survive
-> rebound pressure appears
```

Therefore exact Stage48–49 authoring should use SPLITTER timing/position as a recovery/miss-pressure axis instead of inflating child HP merely to force survival through the ultimate.

The older `LV26_MAGE_SPLITTER_ORDERING_WATCH` remains relevant for pre-Lv31 TEACH/STANDARD encounters, where transformation readability still matters more strongly.

---

# 6. Stage48–49 miss-severity divergence: grammar-first repair

Document 95 showed that the generic mixed stress recipe punished Rogue/Knight much more harshly for one or two missed P×P events than Tank/Archer/Mage.

Do **not** immediately solve this by:
- hidden class damage buffs;
- hidden EXP correction;
- blanket monster HP inflation;
- weakening Tank/Archer/Mage finals.

Instead rotate pressure grammars so each class has both favorable and unfavorable reset windows.

Recommended late-band grammar families:

## A. LINE / ESCORT
- deep aligned bodies;
- protected SUPPORTER/SIEGER when off-corridor;
- Archer has premium payoff when alignment is earned;
- poor line acquisition preserves pressure.

## B. CLUSTER / CASCADE
- dense groups;
- SPLITTER population rebound;
- Mage has premium payoff when collapse timing is correct;
- missed P×P creates a rapid density rebound.

## C. FRONTLINE / BREACH
- BRUTE/SHIELD/CHARGER layered advance;
- Knight/Tank gain premium disruption/control value;
- missed reset allows frontline depth to become dangerous.

## D. DURABLE EXECUTION / SCATTER
- one or more durable normal anchors plus distributed fast bodies;
- Rogue gains premium focus/retarget value on anchors;
- swarm/scatter prevents the class from solving the entire wave with single-target multihit alone.

Stage48–49 should rotate these families rather than repeat one generic mixed recipe.
The goal is not equal damage or identical fail curves.
The goal is that **every class must maintain P×P because some recurring pressure family will exploit that class's natural weakness if a reset is missed.**

---

# 7. Cross-stage consistency

## Class identity
No identity collision found after Archer width approval:

```text
Knight = bounded frontline two-pass break
Rogue  = projectile-count/multihit storm
Tank   = battlefield control + wall time
Archer = wide straight unlimited-depth deletion
Mage   = staged fixed-area density collapse
```

## Monster identity
- CHARGER remains a readable windup/interrupt decision.
- SIEGER remains a positioning/windup/reposition decision.
- SPLITTER can become a mastery timing/rebound decision rather than requiring children to survive every ultimate.
- SUPPORTER/SIEGER off-corridor protection remains authorable against Archer.

## EXP
No final EXP conclusion changes. Stage46 possession fairness is still unresolved until later reconvergence authority.

## Production
No production gameplay/source changed.

---

# 8. Current P4-D2 conclusions

Working, still-unfrozen centers:

```text
Knight  second wave 1.00
Rogue   16 daggers × .45
Tank    shockwave .75 / KB ×2.5 / barrier 250-for-6s candidate
Archer  damage center 2.30 / MID_ADJACENT-style wide straight corridor candidate
Mage    stage .75 / radius1.25 candidate
```

Structural status:

```text
Archer wider-than-ordinary Lv31 corridor = USER APPROVED
exact Archer width = NOT FROZEN
Stage46 gate-separation feasibility = FOUND
Stage48–49 grammar convergence = NEXT ACTIVE WORK
```

---

# 9. Exact next work boundary

Continue P4-D2 without a new user decision:

1. construct bounded Stage48–49 grammar sensitivity using LINE / CLUSTER / FRONTLINE / DURABLE-SCATTER cycles;
2. inject isolated and consecutive P×P misses;
3. compare burial/recovery direction by class;
4. ensure CHARGER/SIEGER/SPLITTER role opportunities are present before class-specific counterplay;
5. preserve deterministic attribution;
6. do not freeze exact campaign recipes or final EXP.

Stop for user decision only if this work requires changing a class identity, adding a code-level Lv31 lock, or freezing a material numerical rule.
