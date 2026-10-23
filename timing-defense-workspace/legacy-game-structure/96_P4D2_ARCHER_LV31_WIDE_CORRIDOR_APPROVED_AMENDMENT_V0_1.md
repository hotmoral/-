# Timing Defense — P4-D2 Archer Lv31 Wide-Corridor Approved Amendment V0.1

Date: 2026-10-23 KST  
Status: **USER APPROVED STRUCTURAL AMENDMENT / EXACT WIDTH AND DAMAGE UNFROZEN / P4-D2 CONTINUES / NO PRODUCTION CHANGE**

Depends on:
- `91_P4D1_LV31_POWER_FANTASY_AND_STAGE46_MASTERY_GATE_APPROVED_CONTRACT_V0_1.md`
- `92_P4D2_LV31_MASTERY_POWER_AND_STAGE46_PRESSURE_PREFLIGHT_V0_1.md`
- `94_P4D2_LV31_CURRENT_ROSTER_PRESSURE_RESPONSE_PROBE_V0_1.md`
- `95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `88_P4C1_LV26_STRUCTURAL_SKILL_APPROVED_CONTRACT_V0_1.md`

---

# 0. User decision

The user explicitly approved option **A** on 2026-10-23 KST.

Approved principle:

> Lv31 `Sky-Piercing Arrow` is not only visually huge. Its authoritative gameplay collision corridor is also wider than ordinary/Lv26 Archer arrows.

This approval resolves the material geometry gate exposed by document 95.

It does **not** freeze the exact collision width, exact sprite-to-collider ratio, or exact per-target damage coefficient.

---

# 1. Approved Lv31 Archer geometry semantics

For P×P CRITICAL `Sky-Piercing Arrow`:

1. Exactly one authoritative final arrow/ray package is created from the root action.
2. The projectile remains a **locked straight shot**.
3. No homing is introduced.
4. No bending/curving is introduced.
5. No off-line retarget is introduced.
6. All live attackable enemies whose authoritative geometry intersects the final arrow corridor may be hit once by that arrow.
7. Penetration depth has no target-count cap inside the actual final-arrow corridor.
8. The final-arrow gameplay corridor is **materially wider than ordinary/Lv26 Archer arrow collision width**.
9. The wider corridor is still a line/corridor mechanic, not a circular AoE or screen-wide target selection.
10. Armor-ignore and no penetration-decay continuity remain part of the Lv31 final-arrow identity.
11. Generated final-arrow hits remain root-owned, deterministic, attributable, and do not independently generate EXP/charge/combo/N3 or recursive skill trees.

---

# 2. Why this is the approved interpretation

Document 95 showed two separate facts.

First, a narrow Lv31 arrow at `1.00` per target regressed durable-target burst relative to the Lv26 Triple Shot continuity package (`1.00 + .65 + .65 = 2.30`).

Second, after the arrow already killed every target it intersected, increasing damage from `1.00 -> 1.50 -> 2.00 -> 2.30` did not improve survival against distributed late-run pressure. The remaining failure was geometric: enemies immediately outside the narrow ordinary-arrow line were untouched.

A modestly wider but still straight corridor solved that failure mode without adding homing, bending, arbitrary target selection, or a circular AoE.

Therefore the approved change is a class-identity refinement, not a generic power scalar patch.

---

# 3. Class-role separation preserved

The approved geometry keeps the five Lv31 identities distinct:

```text
Knight = bounded broad two-pass frontline break
Rogue  = many real tracking projectiles / target-persistent multihit
Tank   = battlefield control + wall protection reset
Archer = huge wide straight corridor with unlimited depth
Mage   = fixed-area staged density collapse + bounded chain
```

Important distinction:
- Archer width expands a **straight corridor**.
- Mage still owns broad area/density collapse.
- Knight still owns bounded frontal multi-pass disruption rather than unlimited-depth line deletion.

No class identity is reopened by this amendment.

---

# 4. Numeric status — still provisional

Still **NOT FROZEN**:

```text
exact Lv31 Archer collision width
exact width multiplier vs ordinary/Lv26 arrow
exact sprite size
exact sprite-to-collider ratio
exact per-target damage coefficient
```

Current P4-D2 continuity center for damage remains:

```text
per-target coefficient = 2.30 root basis candidate
```

This is a test center only.

The next geometry calibration should vary width independently from damage. Do not compensate insufficient width only by increasing damage.

---

# 5. Required next P4-D2 checks

With the structural question resolved, P4-D2 must now test:

1. **width sensitivity** — enough to feel huge and reset pressure without becoming screen-wide AoE;
2. **protected backline geometry** — SUPPORTER/SIEGER can be erased when genuinely aligned, but off-corridor positioning must still matter;
3. **role expression** — final-arrow power may preempt threats at mastery level, but encounter authoring must not make specialist decisions disappear universally;
4. **Stage48–49 miss pressure** — successful P×P should reset line pressure, while missed P×P permits dangerous backlog/rebound;
5. **class divergence repair through encounter grammar first**, not hidden class buffs/XP corrections;
6. deterministic replay/attribution and future multiplayer event-volume behavior.

---

# 6. Supersession note

Any older P4-D1/P4-D2 clause stating that the final arrow's large visual size should **not** widen gameplay collision is superseded by this user-approved amendment.

The following remain unchanged:
- one straight final projectile/ray;
- no homing;
- no bending;
- no off-line retarget;
- unlimited penetration depth inside the corridor;
- exact width is not yet numerically frozen.

---

# 7. Boundary

`ARCHER_LV31_WIDE_CORRIDOR_PRINCIPLE = USER_APPROVED`

P4-D2 remains active.
No user decision is required merely to iterate the exact width candidate or to continue role-alignment / Stage48–49 pressure probes.

Do not start P4-E until the remaining P4-D2 feedback package is closed.
Do not modify production gameplay.
