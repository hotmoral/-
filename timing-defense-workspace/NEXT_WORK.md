# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes unauthorized

## Mandatory authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active plan `legacy-game-structure/data/system_dependency_calibration_order_v0_27.yaml`
- `CHARACTER_PROFILE_RADAR_V1.md`
- `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- `legacy-game-structure/130_P5_CLASS_IDENTITY_FINITE_PACKET_PROBE_PREFLIGHT_V0_1.md`
- `legacy-game-structure/131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`

Live remote wins.

---

# ACTIVE PACKAGE — P5

**A2 APPROVED / CLASS IDENTITY RECONVERGENCE ACTIVE / TANK CONTROL-VS-CLEAR SEARCH NEXT**

No user decision is pending.
No numerical value is frozen.

---

# What the first identity scan changed

## Tank
Current all-success finite-packet enemy-removal speed is too close to damage classes:

```text
Tank 8.079s
non-Tank median ~7.830s
ratio ~1.03x
```

This violates the user-directed negative Tank identity.

Likely root cause is current provisional Lv31 battlefield-wide damage contribution, not the knockback/barrier/control package.

Do **not** delete Tank control.
Do **not** choose an exact damage coefficient yet.

Next Tank question:

```text
How low can final damage contribution go
while Tank still survives late pressure through control,
and while solo enemy-removal becomes materially slower?
```

## Archer
Aligned vs scatter separation is strong (`~3.58s` vs `~8.08s`).
Keep line-specialist identity. Treat the old attack-heavy Stage49 problem as a localized packet chronology issue, not a global Archer nerf trigger.

## Mage
Cluster vs distributed separation is strong (`~3.78s` vs `~8.08s`).
Keep density/AoE identity.

## Rogue
New HIGH watch:
`P5_ROGUE_DAGGER_GRUNT_ONESHOT_BREAKPOINT_WATCH`.

At sufficient shop ATK, one provisional Lv31 dagger crosses GRUNT one-shot damage and approved retargeting lets remaining daggers serially clean many weak enemies.
Do not remove retargeting yet; measure distinct targets per storm and realistic shop effect magnitudes first.

## Knight
Current paired fixture has a target-death/second-wave chronology breakpoint.
Refine the fixture before changing Knight.

---

# Immediate next work

## 1. Tank control-vs-clear Pareto search

Keep fixed:
- battlefield-wide pressure-reset spectacle;
- knockback/control;
- Aftershock slow identity;
- wall barrier/protection;
- Tank Iron Wall semantics.

Vary only provisional Lv31 enemy-damage contribution directionally.
Measure together:

```text
finite-packet direct clear time
unfinished / backlog
late-pressure wall reserve
wall contacts / SIEGER exposure
control contribution
one/two-miss recovery
```

The first sensitivity already shows a broad range from damage-class-like speed to much slower solo clearing; no value is selected yet.

## 2. Rogue breakpoint probe

Add:
- distinct targets hit/killed by one Dagger Storm;
- GRUNT/RUNNER/SHIELD threshold crossings;
- shop ATK sensitivity around the one-dagger-one-GRUNT breakpoint;
- durable-target execution comparison.

## 3. Knight probe refinement

Design a penetration-causality packet where aligned vs off-axis comparison is not dominated by final second-wave target-death retarget chronology.

## 4. Exact execution boundary

The authored committed identity runner still needs exact committed-byte execution when a suitable lane is available.
Current first result is directional reconstruction only.

## 5. Then

- integrate identity outputs into source-patched Stage46–49 normal-right-edge runner;
- carry wall deficit Stage46→49;
- resume Stage49 packet chronology only after identity reconvergence;
- later KNOCK parity, CRIT/CRITDMG policy, EXP/Lv feedback, P10/P10R.

---

# Fixed rules

```text
SURVIVAL != CLEAR
TANK SOLO PARITY NOT REQUIRED
NO ABSOLUTE CLASS LOCKOUT
ALL ENEMIES ENTER FROM NORMAL RIGHT EDGE
NO MID-FIELD POP-IN
DO NOT FORCE IDENTICAL CLASS DPS OR CLEAR TIME
```

Do not modify/deploy production gameplay.
P6 remains blocked pending P5 closure.
