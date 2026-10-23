# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized

## Operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_28.yaml`
- class identity gate: `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- class identity closure: `legacy-game-structure/135_P5_CLASS_IDENTITY_GROUP_DIRECTIONAL_CLOSURE_V0_1.md`
- integrated runner preflight: `legacy-game-structure/136_P5_IDENTITY_AWARE_STAGE46_49_INTEGRATED_RUNNER_PREFLIGHT_V0_1.md`
- live remote always wins

---

# Current phase

**P4 PROVISIONAL STRUCTURAL COMPLETE_WITH_WATCHES / P5 A2 USER_APPROVED — CLASS IDENTITY GROUP DIRECTIONALLY CLOSED / IDENTITY-AWARE STAGE46–49 RUNNER AUTHORED / CHECKOUT-EXACT EXECUTION NEXT**

```text
P0..P3 structural foundation complete
-> P4 player-power spine provisional complete with watches
-> P5 A2 USER APPROVED
-> five-class shop combat complete directionally
-> normal-right-edge Stage46–49 direction promising
-> radar identity promoted to balance invariant
-> class-identity diagnostic group DIRECTIONALLY CLOSED
-> identity-aware Stage46–49 integration runner + fixture authored
-> static/source-patch preflight complete
-> checkout-equivalent execution/result review NEXT
```

No user decision is currently pending.
No production change is authorized.
No numerical value is frozen.

---

# Stable P5 shop boundary

A2 approved semantics remain:

```text
EVERY_STAGE_AVAILABLE_BUT_NONBLOCKING
PERSONAL WALLETS
KILLER_ONLY PERSONAL ordinary-monster coin baseline
ALL-HUMAN Stage-clear income-floor candidate
FORTIFICATION = max HP + matched current increase
ATK/CRIT/CRITDMG/KNOCK personal
FORTIFICATION/DEF purchases contribute to shared wall
six categories retained
NO_ROUTINE_FULL_SHOP_MAXOUT_BY_STAGE49
```

Working diagnostics only:

```text
full-shop reference = 16360
spend capacity center = 50%
income mix center = 70/30
common shop-effect diagnostic center = 40% legacy-relative
```

The first integrated runner intentionally uses a fixed late-segment shop snapshot across Stage46–49 so it can isolate identity/chronology/wall-deficit behavior without inventing an unapproved per-stage purchase history.
Actual ATK/DEF acquisition-time feedback remains pending fidelity work.

---

# Class identity radar gate

Approved identity reference:

| Class | 공격 | 치명 | 민첩 | 넉백 | 관통 | 광역 |
|---|---:|---:|---:|---:|---:|---:|
| Knight | 4 | 2 | 3 | 3 | 4 | 2 |
| Rogue | 2 | 5 | 5 | 1 | 1 | 1 |
| Tank | 2 | 1 | 1 | 5 | 1 | 3 |
| Archer | 3 | 2 | 4 | 1 | 5 | 2 |
| Mage | 4 | 2 | 2 | 1 | 1 | 5 |

Interpretation:

```text
high radar axis -> must remain a real reason the class succeeds
low radar axis  -> must remain a real limitation after growth
SURVIVAL != CLEAR
```

---

# Class identity group closure — preserved

## Knight

Refined durable pair:

```text
BALANCED 40%: aligned 9.20s / dispersed 12.575s
DEFENSE_HEAVY 40%: aligned 11.45s / dispersed 12.575s
no shop: aligned 12.575s / dispersed 15.95s
```

Classification:
`DIRECTIONALLY_ALIGNED / NO STRUCTURAL IDENTITY DEFECT ESTABLISHED`.

## Rogue

Core multihit/durable execution identity remains valid.
Current shop ATK can push one Dagger Storm projectile over a fresh GRUNT one-shot breakpoint.

At the 40% diagnostic center the newly encoded analytic check gives approximately:

```text
BALANCED atk8          -> 339.12 vs GRUNT HP320
ATTACK_HEAVY atk9      -> 347.76
DEFENSE_HEAVY atk6     -> 321.84
ROLE_AWARE Rogue atk10 -> 356.40
```

Therefore even DEFENSE_HEAVY narrowly crosses the fresh-GRUNT breakpoint.
The important integrated metric is now distinct targets hit/killed per storm, not merely breakpoint existence.

Active guard:
`ROGUE_STORM_SINGLE_DAGGER_ORDINARY_ONESHOT_NOT_ROUTINE`.
Approved deterministic retargeting remains unchanged.

## Tank

Current provisional Lv31 shockwave damage center `0.75` remains directionally inconsistent with poor-solo-throughput identity.
Preserve knockback/slow/barrier/control; first repair axis is battlefield-wide enemy damage contribution.

Integrated sensitivity only:

```text
0.20 / 0.25 / 0.30
working center = 0.25
```

No production coefficient is selected.

## Archer

Strict-line identity remains strongly preserved.
The prior Stage49 issue remains localized to frontmost/HP-breakpoint/SIEGER chronology.
No global Archer nerf is justified.

## Mage

Cluster-vs-distributed density identity remains strongly preserved.
No structural Mage redesign is justified.

---

# New integrated runner state

Assets:

```text
tools/run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py
legacy-game-structure/data/p5_identity_aware_stage46_49_integration_fixture_v0_1.json
legacy-game-structure/136_P5_IDENTITY_AWARE_STAGE46_49_INTEGRATED_RUNNER_PREFLIGHT_V0_1.md
```

Encoded requirements:

```text
all physical spawnX = 0.92
mid-field pop-in forbidden
spawnLeadSeconds changes schedule only
wall current/max/absolute deficit carried Stage46->47->48->49
Tank 0.20/0.25/0.30, control package unchanged
Rogue per-storm distinct-target hit/kill telemetry
GRUNT/RUNNER/SHIELD fresh one-dagger breakpoint report
Knight refined aligned/dispersed regression
Archer line/scatter regression
Mage cluster/distributed regression
```

The new runner avoids the existing P5 v0.1/v0.2 source-patch weakness where a module-level `hit()` line was targeted inside `inspect.getsource(stage46.simulate)`.
ATK is now applied through a guarded `hit` wrapper; only `simulate()`-owned lines are source-patched.

This is a runner-fidelity correction, not a reopening of the closed class-identity conclusions.

---

# Stage-boundary model / active watch

The inherited recipes are bounded 60-second stress windows, not exact launch-stage scripts.
The integrated runner carries wall state but does not transplant living diagnostic mobs across the synthetic stage boundary.

Active watch:

```text
P5_STAGE_BOUNDARY_BACKLOG_DISCARD_BIAS
```

`endActive` is retained in output.
If material backlog exists at a boundary, Stage49 wall reserve remains directional only and must not be interpreted as exact stage-clear reserve before the boundary model is refined.

---

# Encounter boundary

Actual game direction remains:

```text
ALL ENEMIES ENTER FROM NORMAL RIGHT EDGE
NO MID-FIELD POP-IN
```

Late-stage direction remains:

```text
Stage46 = power revelation
Stage47 = transition / recovery room
Stage48 = first protected role pulse
Stage49 = stronger escorted second pulse
```

Do not tune Stage49 in isolation.

---

# Exact replay boundary

Completed now:
- new integrated runner authored;
- integration fixture authored;
- local syntax compile of the authored runner content passed;
- source-patch fidelity reviewed statically.

Still pending:

```text
checkout-equivalent import/run of the new integrated runner
repeat determinism/output admission
numerical interpretation of Stage46-49 chain
other pending P4/P5 exact fidelity replays
```

The current local execution environment cannot clone `github.com` because DNS resolution is unavailable; no exact output was fabricated from directional evidence.

---

# Exact next boundary

1. checkout-equivalent import/run of `run_p5_identity_aware_stage46_49_integrated_probe_v0_1.py`;
2. admit/fix only simulator fidelity if a guarded source patch fails;
3. review Tank `0.20 / 0.25 / 0.30` survival-vs-clear behavior;
4. review Rogue distinct-target cleanup and ordinary one-dagger runtime events;
5. confirm Knight/Archer/Mage targeted regressions;
6. inspect `endActive` and decide whether stage-boundary backlog fidelity must be raised before interpretation;
7. only then refine Stage49 frontmost/escort chronology;
8. later KNOCK parity, CRIT/CRITDMG policy, real shop acquisition timing/EXP feedback, P10/P10R.

P6 remains blocked pending P5 closure.
