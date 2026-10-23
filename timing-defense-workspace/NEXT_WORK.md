# Timing Defense — Next Work Boundary

Updated: 2026-10-23 KST

## Production checkpoint
- v0.45 SIEGER FULL PASS
- production branch `timing-defense-cloudflare-do-poc`
- last verified production/source HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- production gameplay/numerical changes remain unauthorized

## Mandatory operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_10.yaml`

Live remote wins.

---

# ACTIVE PHASE — P4-D2 / ARCHER LV31 GAMEPLAY-WIDTH USER DECISION

Completed inside P4-D2:

```text
P4-D1 power-fantasy + Stage46 mastery-gate direction = USER APPROVED_WITH_MODIFICATION
P4-D2 preflight = COMPLETE
P4-D2 first power envelope = COMPLETE
P4-D2 current-nine-roster static response = COMPLETE / PASS_WITH_CORRECTION
P4-D2 stateful temporal Stage46 stress = COMPLETE / CANDIDATE PRESSURE ENVELOPE FOUND
```

Current evidence:
- `legacy-game-structure/94_P4D2_LV31_CURRENT_ROSTER_PRESSURE_RESPONSE_PROBE_V0_1.md`
- `legacy-game-structure/95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `legacy-game-structure/data/p4d2_stage46_temporal_pressure_summary_v0_1.json`

Replay:

```text
python tools/run_p4d2_stage46_temporal_pressure_probe_v0_1.py \
  --base-fixture legacy-game-structure/data/p4d2_lv31_pressure_probe_fixture_v0_1.json \
  --temporal-fixture legacy-game-structure/data/p4d2_stage46_temporal_pressure_fixture_v0_1.json \
  --json-out /tmp/p4d2_stage46_temporal.json > /dev/null
```

Expected full JSON SHA-256:
`110ea2beb87dabb41b4d8dd48af61bbe97e21666413481a9f19df95507c75e75`

---

# What the temporal probe established

A candidate combat-pressure gate exists with the current nine-monster grammar.

Same 60-second deterministic stress envelope:

## Lv26 + every timing input PERFECT

```text
Rogue   buried 28.65s
Tank    buried 33.25s
Knight  buried 35.80s
Archer  buried 52.65s
Mage    buried 56.25s
```

## Lv31 + every P×P final successful

```text
Knight survives / wall 1175
Rogue  survives / wall 1330
Tank   survives / wall 2000
Archer survives / wall 2000
Mage   survives / wall 2000
```

This supports the approved direction:

```text
no code-level Lv31 gate
+
Lv26 cannot indefinitely stabilize late pressure
+
Lv31 P×P provides the necessary explosive pressure reset
```

The 60s duration, 4.6s pressure cycle, 1.125s root cadence and five geometry bands remain diagnostic stress inputs only.

---

# Current provisional centers — not frozen

```text
Knight: second wave 1.00
Rogue: 16 daggers × .45
Tank: shockwave .75 / KB ×2.5 / barrier 250-for-6s candidate
Archer: per-target 2.30 + gameplay-width principle PENDING
Mage: stage .75 / radius1.25 candidate
```

Rogue sensitivity is especially useful:

```text
12 daggers -> buried 41.90s
16 daggers -> pressured but survives, wall 1330
20 daggers -> largely trivializes this fixture, wall 2000 / only 5 active
```

16 remains the working center.

---

# CURRENT USER DECISION — Archer Sky-Piercing Arrow gameplay width

Static continuity already showed that Lv31 per-target 1.00 was too low relative to Lv26 Triple Shot, so P4-D2 uses `2.30` as a provisional per-target continuity center.

Temporal evidence now shows:

## Narrow ordinary-width straight ray

```text
coeff 1.00 -> buried 52.65s
coeff 1.50 -> buried 52.65s
coeff 2.00 -> buried 52.65s
coeff 2.30 -> buried 52.65s
```

Increasing damage does not solve enemies distributed just outside the narrow ray.

## Modestly wider but still straight final-arrow corridor

```text
coeff 1.00 -> survives / wall 1930
coeff 1.50 -> survives / wall 2000
coeff 2.00 -> survives / wall 2000
coeff 2.30 -> survives / wall 2000
```

The missing variable is therefore geometry, not raw damage.

### Option A — RECOMMENDED
Approve this Lv31-only principle:
- `Sky-Piercing Arrow` has a gameplay collision corridor wider than ordinary/Lv26 arrows;
- remains one locked straight projectile/ray;
- no homing;
- no bending;
- no off-line retarget;
- unlimited target depth only inside that straight corridor;
- exact width remains a later P4-D2 calibration variable.

Why recommended:
- `huge arrow` becomes mechanically meaningful;
- preserves Archer line-deletion identity;
- avoids solving geometry failure through arbitrary damage inflation;
- test evidence shows width is the dominant axis.

### Option B
Keep gameplay collision width identical to ordinary/Lv26 arrows and make `huge` visual-only.
Then late dispersed pressure must be solved through another encounter or skill mechanism.

### Option C
Request another geometry analysis before choosing.

Until the user decision:

```text
Archer wider gameplay corridor = CANDIDATE_ONLY
P4-D2 = ACTIVE / USER_DECISION_PENDING
P4-E = BLOCKED
production changes = UNAUTHORIZED
```

---

# Important carried watches after the decision

Even if Option A is approved, P4-D2 still must test:
1. targeted CHARGER WINDUP interrupt/re-arm under Knight/Tank finals;
2. SIEGER standoff/windup/reposition opportunity;
3. Stage48–49 miss-severity class divergence through encounter grammar;
4. Mage/SPLITTER chronological transformation behavior;
5. Stage46 Lv31 acquisition fairness;
6. Rogue 2P/3P/4P 48/64/80 projectile performance stress later;
7. final EXP remains deferred to P10R.

Current miss-severity evidence:
- one missed P×P nearly kills Rogue but barely affects Tank/Archer/Mage;
- two consecutive misses bury Rogue and leave Knight near-terminal while stronger control/AoE classes recover much more easily.

Do not repair this with hidden class-specific balance patches first. Repair the late-band encounter grammar/geometry first.

---

# Required user action

Choose:

```text
A — approve wider straight Lv31 Archer gameplay corridor principle; exact width remains provisional
B — reject gameplay-width increase
C — request more geometry analysis
```

No production implementation or exact number is authorized by A.
