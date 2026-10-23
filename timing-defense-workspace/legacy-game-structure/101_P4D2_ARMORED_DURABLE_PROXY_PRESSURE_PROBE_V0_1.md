# Timing Defense — P4-D2 Armored Durable Proxy Pressure Probe V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED DIAGNOSTIC / DURABLE PRESSURE AXIS SUPPORTED / NOT A NEW-MONSTER APPROVAL / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Authority / context:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
- `100_P4D2_STAGE48_49_CADENCE_CORRECTED_DIRECTIONAL_FEEDBACK_V0_1.md`
- `../PLAYER_SKILL_AUTHORITY_REVIEW_2026-10-22.md`

Replay assets:
- `../../tools/run_p4d2_armored_durable_proxy_probe_v0_1.py`
- `data/p4d2_armored_durable_proxy_fixture_v0_1.json`

Local diagnostic full-output SHA-256 from the prepared runner/fixture semantics:

```text
4737d374acdda313eb77fe870bf50938313bd53690b3d46227292f01b79a9a92
```

The committed runner should still receive a repository-checkout one-command replay before using this hash as regression/freeze authority.

---

# 0. User hypothesis

User proposed that the late game can pressure Tank/Mage without nerfing their Lv31 skills by introducing high-HP, high-armor durable threats.

The useful question is not:

> Can we create a monster that Tank/Mage simply cannot kill?

It is:

> Can a durable pressure axis survive Tank/Mage's one-cast reset while preserving Tank control, Mage clustering payoff, Rogue multihit execution, Archer armor-ignore identity and Knight frontline damage?

Answer from this bounded proxy:

**YES — the direction is strongly supported.**

---

# 1. Proxy boundary

`ARMORED_DURABLE_PROXY` is **not an approved tenth monster**.

It is a diagnostic combination of already-existing pressure axes:

```text
BRUTE-like high HP
+
SHIELD-like damage mitigation
+
moderate knock resistance
```

Working center for the first probe only:

```text
HP              1600
armor multiplier 0.55
knock resistance 0.65
slow movement anchor 0.04
wall damage proxy 160
```

Sensitivity range:

```text
HP: 1400 / 1600 / 1800
armor multiplier: 0.65 / 0.55 / 0.50
```

None of these values are frozen.

The moderate `0.65` knock resistance is deliberate. The proxy should resist instant deletion by Tank, but Tank's core control must remain meaningful. A high-HP/high-armor/high-KB-resist stat pile would be a hard counter and is not the intended direction.

---

# 2. Single durable target — one Lv31 final package

At the working center:

| Class | Result against one durable proxy |
|---|---|
| Knight | removes **65.4%**, leaves ~553 HP |
| Rogue | **kills it** with the 16-dagger storm |
| Tank | removes **15.5%**, leaves ~1353 HP, but pushes it |
| Archer | removes **94.9%**, leaves ~82 HP because armor is ignored |
| Mage | removes **24.8%** from the primary durable target, leaves ~1204 HP |

This is an unusually useful separation because it follows the existing class identities rather than flattening them.

## Rogue
The 16-projectile final retains a clear durable-normal execution role. No evidence here supports reducing the dagger count.

## Archer
Armor ignore matters dramatically. The final nearly deletes the 1600-HP proxy despite the proxy's mitigation axis.

## Knight
The two-wave frontline finisher heavily wounds the target but does not automatically delete it.

## Tank
Low damage is intentional here. The important retained response is displacement/control.

Diagnostic push against the proxy at the current final center:

```text
0.047 × 2.5 × 0.65 = 0.076375 normalized displacement
```

Therefore the proxy does **not** invalidate Tank's role; Tank buys time rather than erasing it.

## Mage
The primary durable enemy is intentionally difficult because the current Arcane Collapse identity is density collapse rather than single-target execution.

---

# 3. Clustered vs distributed durable pressure

Three identical durable proxies were tested in two layouts.

## Clustered three

Reset fraction of total durable HP after one final:

```text
Knight  43.6%
Rogue   48.8%
Tank    15.5%
Archer  63.3%
Mage    45.4%
```

## Distributed three

```text
Knight  21.8%
Rogue   48.8%
Tank    15.5%
Archer  31.6%
Mage    29.7%
```

This is the important authoring result.

### Mage
Mage remains materially better when durable enemies are clustered:

```text
clustered 45.4%
distributed 29.7%
```

So the durable axis does not erase Mage's crowd identity. It gives encounter authoring a lever:
- cluster durable pressure -> Mage regains payoff;
- separate durable pressure -> Mage cannot solve everything with one collapse.

### Archer
The wider final corridor remains powerful but not screen-wide:

```text
clustered 63.3%
distributed 31.6%
```

This supports the user-approved `huge straight arrow` principle: line/corridor positioning matters.

### Rogue
Rogue is comparatively geometry-insensitive in these snapshots because the storm keeps focusing/retargeting sequentially.
That is class identity, not a defect.

### Tank
Tank's damage reset remains low in both layouts, but this probe intentionally does not convert its displacement/shield into equivalent damage. The next temporal probe must measure the time bought by push + barrier before judging Tank survivability.

---

# 4. Protected backline cases

## Durable front + SUPPORTER

With two durable bodies in front and SUPPORTER/RUNNER behind, a single final no longer reduces the encounter to the same trivial screen-clear problem for every class.

The durable front survives for all classes except Rogue can execute one durable target. Tank/Mage can clear lighter bodies yet still inherit the durable remainder.

This is useful because it creates a real second decision after the flashy final rather than merely inflating HP globally.

## Durable front + SIEGER/SHIELD

In the bounded snapshot:
- Tank's global hit leaves the SIEGER at roughly 70 HP while both durable bodies remain heavily alive;
- Mage leaves the SIEGER at roughly 268 HP while both durable bodies remain;
- Rogue executes one durable but leaves the protected SIEGER untouched in the same package path;
- Archer nearly deletes one aligned durable but cannot automatically erase all off-corridor protection.

This suggests a promising late-game pattern:

```text
durable frontline
+
protected role threat
+
final reset
+
surviving second pulse / reposition / cleanup decision
```

The next temporal probe must determine whether the surviving SIEGER/CHARGER windows are readable and fair rather than just unavoidable wall damage.

---

# 5. Sensitivity interpretation

The 3×3 single-target grid (`HP 1400/1600/1800 × armor .65/.55/.50`) preserved the main ordering:

- Rogue killed the single proxy throughout the tested grid with the current 16-dagger package.
- Archer killed the 1400-HP candidates and left only ~5% at HP1600 or ~15.7% at HP1800 because armor ignore bypasses the mitigation axis.
- Knight moved from very strong partial deletion toward roughly half-HP remainder as durability rises.
- Tank consistently left roughly 79–88% HP because its final is control-oriented.
- Mage primary-target remainder stayed roughly 67–80% because its final is not a single-target execution package.

The `1600 / .55` working center is therefore a useful **diagnostic middle**, not a balance recommendation.
It creates class separation without requiring any Lv31 nerf.

---

# 6. Why this is better than global HP inflation

Document 100 already found that naive global pressure increases can kill Knight/Rogue first while Tank/Mage remain comfortable.

The durable proxy behaves differently because it changes the **type of unresolved pressure**, not merely total body count.

It creates:
- single-target execution value for Rogue;
- armor-ignore value for Archer;
- frontline chunking value for Knight;
- time-buying value for Tank;
- clustering/spacing sensitivity for Mage.

That is the desired kind of asymmetric pressure.

---

# 7. Hard-counter safeguards

If this axis later becomes real content, do **not** simply maximize every defensive stat.

Required safeguards:

1. **Tank control remains valid.**
   - moderate rather than extreme knock resistance;
   - displacement/time-buying must remain a legitimate solution.

2. **Mage has a positional answer.**
   - clustered durable bodies must still reward Arcane Collapse;
   - do not make every durable threat permanently isolated by rule.

3. **No permanent Archer monopoly.**
   - armor ignore can be a strong answer, but encounter geometry should still matter;
   - off-corridor threats remain relevant.

4. **Rogue execution remains finite.**
   - 16 daggers may delete one durable target, but multiple distributed durables consume the storm rather than letting it erase the whole battlefield.

5. **Knight retains meaningful chunk/knock value.**
   - durability should not rise until two-wave damage becomes visually irrelevant.

6. **Do not introduce a stat-only clone as a new monster.**
   - current 9-monster extensibility rules require future monsters to add a distinct decision/telegraph;
   - this proxy may later become a variant, an authored late-stage state, or a new archetype only after a separate monster-identity decision.

---

# 8. Verdict

Classification:

```text
DURABLE_PRESSURE_AXIS = SUPPORTED
TANK_MAGE_LATE_PRESSURE_LEVER = PROMISING
ROGUE_EXECUTION_IDENTITY = PRESERVED
ARCHER_ARMOR_IGNORE_IDENTITY = PRESERVED
TANK_CONTROL_HARD_COUNTER = NO at current proxy center
MAGE_CLUSTERING_PAYOFF = PRESERVED
NEW_MONSTER_APPROVED = NO
NUMERICAL_FREEZE = NO
```

The user's hypothesis is therefore accepted as a **P4-D2 pressure-design direction**, not yet as a monster-roster decision.

---

# 9. Exact next work

Build a temporal durable-pressure probe that preserves the cadence/no-target corrections from documents 99–100 and measures:

```text
1. isolated durable arrival after a successful P×P reset
2. two/three distributed durable arrivals across successive reset windows
3. durable frontline + timed SUPPORTER/SIEGER second pulse
4. durable frontline + CHARGER window
5. Tank time bought by knockback/barrier rather than raw damage
6. Mage recovery when durable threats are clustered vs deliberately separated
7. whether Knight/Rogue become unfairly punished before Tank/Mage are meaningfully pressured
```

Repair order remains:

```text
encounter timing / spacing / role pressure
-> proxy durability sensitivity
-> only then class numbers if still necessary
```

Do not modify production gameplay yet.
