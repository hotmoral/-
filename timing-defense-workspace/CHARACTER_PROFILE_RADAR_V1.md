# Timing Defense — Character Profile Radar V1

Status: **APPROVED / V1**
Updated: 2026-10-20 KST

## Purpose
The pre-game class radar is a **readability / identity graphic**, not a literal exposure of hidden numerical combat coefficients.
It should let a player understand a class at a glance without reading a stat sheet.

## Axes
Six fixed axes:
- 공격력
- 치명타
- 민첩성
- 넉백
- 관통
- 광역

`민첩성` means the class's overall quickness / chained attack feel / rapid combat development. It does **not** mean the current passive auto-attack interval. The passive auto-attack interval is currently common at 2.0 s across classes.

## Scale
Use **5 visual levels**.
The UI should not print numeric 1–5 values by default; the five concentric hexagon rings communicate the level visually.

Interpretation:
- 1 = very low
- 2 = low
- 3 = medium
- 4 = high
- 5 = specialty / defining strength

Equal values between classes are explicitly allowed. This is a class-profile graphic, not a forced 1st–5th ranking table.

## Approved profile values
| Class | 공격력 | 치명타 | 민첩성 | 넉백 | 관통 | 광역 |
|---|---:|---:|---:|---:|---:|---:|
| Knight | 4 | 2 | 3 | 3 | 4 | 2 |
| Rogue | 2 | 5 | 5 | 1 | 1 | 1 |
| Tank | 2 | 1 | 1 | 5 | 1 | 3 |
| Archer | 3 | 2 | 4 | 1 | 5 | 2 |
| Mage | 4 | 2 | 2 | 1 | 1 | 5 |

## Visual identity
- Knight: gold.
- Rogue: charcoal/black profile fill with silver luminous outline for dark-theme readability.
- Tank: blue.
- Archer: green.
- Mage: purple.

## Animation contract
On class change:
1. five-ring hexagonal web appears immediately,
2. a class-color scan expands from center,
3. six vertices grow outward with a short sequential delay (`띠리리릭` feel),
4. the class polygon fills behind the outline,
5. each vertex lands with a small glow/pulse,
6. a short settling pulse finishes the transition.

Animation should feel fast and premium, not like a long data visualization. Target total duration is roughly one second.

## Governance
Changing the radar shape does **not** itself change combat balance. If combat coefficients change enough to alter a class's identity, report/discuss first, then update this profile intentionally.
