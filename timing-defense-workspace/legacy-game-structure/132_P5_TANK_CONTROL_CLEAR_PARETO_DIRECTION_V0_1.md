# Timing Defense — P5 Tank Control-vs-Clear Pareto Direction V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL IDENTITY REPAIR BRACKET / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`

## 1. Confirmed problem

The current provisional Tank Lv31 shockwave damage center `0.75` lets Tank clear the mixed finite packet at roughly damage-class speed:

```text
Knight  8.079 s
Rogue   7.581 s
Tank    8.079 s
Archer  6.953 s
Mage    8.079 s
```

Tank / non-Tank median ~= `1.03x`.

This violates the intended negative Tank identity:
- excellent control / wall preservation;
- poor enemy-removal throughput;
- solo parity not required;
- no absolute code-level lockout required.

## 2. Repair axis

Do **not** reduce Tank knockback, slow, battlefield reset, or wall barrier first.

Repair the part that is erasing the weakness:

```text
battlefield-wide damage contribution
```

while preserving:

```text
battlefield-wide control + displacement + barrier fantasy
```

## 3. Directional sensitivity already recovered

| shockwave coefficient | mixed-packet direct clear | vs non-Tank median |
|---:|---:|---:|
| 0.75 | 8.079 s | 1.03x |
| 0.50 | 10.333 s | 1.32x |
| 0.40 | 12.575 s | 1.61x |
| 0.35 | 13.702 s | 1.75x |
| 0.30 | 14.829 s | 1.89x |
| 0.25 | 18.209 s | 2.33x |
| 0.20 | 21.578 s | 2.76x |
| 0.15 | 23.832 s | 3.04x |
| 0.10 | 29.454 s | 3.76x |

Separate late-pressure sensitivity showed `0.10` can allow backlog to overwhelm the wall in the current Stage49-like stress, while `0.25` still preserves meaningful Tank survival/control with materially larger backlog.

## 4. First integrated diagnostic bracket

For the next Stage46–49 identity-aware simulation only:

```text
0.20 / 0.25 / 0.30
working center = 0.25
```

This is **not a production value recommendation or freeze**.

Why this bracket:
- `0.30` is already materially slower than damage classes;
- `0.25` is over 2x slower on the finite packet while preserving control in prior late-pressure direction;
- `0.20` tests the lower edge before control-induced backlog becomes too dangerous;
- `0.10` is already known to be too low in the current pressure recipe.

## 5. Required next acceptance

The integrated Stage46–49 lane must measure both sides together:

```text
Tank wall survival/control
AND
Tank actual enemy-removal throughput
```

A candidate is invalid if it makes Tank clear at damage-class speed.
A candidate is also invalid if reduced damage makes normal skilled Tank control collapse before its defensive identity can function.

No exact clear-time ratio is frozen from one packet.

## 6. Current classification

```text
TANK_CONTROL_IDENTITY = PRESERVE
TANK_WALL_PROTECTION_IDENTITY = PRESERVE
TANK_CURRENT_LV31_DAMAGE_0P75 = IDENTITY_DEFECT_DIRECTIONALLY
NEXT_DIAGNOSTIC_RANGE = 0.20 / 0.25 / 0.30
NEXT_DIAGNOSTIC_CENTER = 0.25
PRODUCTION_FREEZE = NO
```
