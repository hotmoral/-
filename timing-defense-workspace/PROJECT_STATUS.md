# Timing Defense — Project Status

Updated: 2026-10-23 KST

## Production checkpoint
- branch `timing-defense-cloudflare-do-poc`
- HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- v0.45 SIEGER FULL PASS
- production gameplay/numerical changes remain unauthorized

## Operating authority
- `legacy-game-structure/86_SESSION_RECOVERY_AND_CROSS_STAGE_REVIEW_PROTOCOL_V0_1.md`
- active dependency plan: `legacy-game-structure/data/system_dependency_calibration_order_v0_27.yaml`
- class identity gate: `legacy-game-structure/129_P5_CLASS_IDENTITY_RADAR_INVARIANT_GATE_V0_1.md`
- finite-packet preflight: `legacy-game-structure/130_P5_CLASS_IDENTITY_FINITE_PACKET_PROBE_PREFLIGHT_V0_1.md`
- first directional identity result: `legacy-game-structure/131_P5_CLASS_IDENTITY_FIRST_DIRECTIONAL_RESULT_V0_1.md`
- live remote always wins

---

# Current phase

**P4 PROVISIONAL STRUCTURAL COMPLETE_WITH_WATCHES / P5 A2 USER_APPROVED — CLASS IDENTITY RECONVERGENCE ACTIVE / TANK CONTROL-VS-CLEAR SEARCH NEXT**

```text
P0..P3 structural foundation complete
-> P4 player-power spine provisional complete with watches
-> P5 A2 USER APPROVED
-> five-class shop combat complete directionally
-> right-edge escorted Stage46-49 direction PROMISING
-> radar-defined class identity promoted to balance invariant
-> finite-packet identity runner/fixture authored
-> first independent directional identity reconstruction complete
-> Tank negative solo-throughput defect found
-> Archer/Mage identity strongly supported
-> Rogue shop-driven wave-cleanup breakpoint found
-> Knight paired fixture needs refinement
```

No user decision is currently pending.
No production change is authorized.

---

# Class identity authority

Approved radar profile:

| Class | 공격 | 치명 | 민첩 | 넉백 | 관통 | 광역 |
|---|---:|---:|---:|---:|---:|---:|
| Knight | 4 | 2 | 3 | 3 | 4 | 2 |
| Rogue | 2 | 5 | 5 | 1 | 1 | 1 |
| Tank | 2 | 1 | 1 | 5 | 1 | 3 |
| Archer | 3 | 2 | 4 | 1 | 5 | 2 |
| Mage | 4 | 2 | 2 | 1 | 1 | 5 |

These are identity/readability levels, not literal combat coefficients.

Governance:

```text
high radar axis -> must remain a real reason for success
low radar axis  -> must remain a real limitation after skills/shop growth
SURVIVAL != CLEAR
```

Tank user direction:

```text
Tank solo parity is not required.
Tank should be excellent at survival/control but poor at enemy removal.
Late solo may be near-impractical or materially slower/frustrating than damage classes.
No absolute hard class lockout is required.
```

---

# First directional identity result

Authority boundary:
- result was reconstructed independently from current committed combat semantics and the authored finite packets;
- committed one-command runner exact execution remains pending;
- no number below is frozen.

## Tank — current defect

Same mixed finite packet at current 40%-legacy ATK/FORT/DEF diagnostic center:

```text
Knight  8.079s
Rogue   7.581s
Tank    8.079s
Archer  6.953s
Mage    8.079s
non-Tank median ~= 7.830s
Tank / median ~= 1.03x
```

This does not preserve the intended poor solo-clear weakness.

Likely root axis:
`Lv31 Absolute Barrier battlefield-wide damage contribution`.

Approved Lv31 contract says Tank may strongly reset pressure through control/wall protection **without becoming generic Mage-style damage**.

Directional damage-only sensitivity while keeping control/barrier structure:

```text
shock .75 -> 8.079s  (1.03x median)
shock .50 -> 10.333s (1.32x)
shock .40 -> 12.575s (1.61x)
shock .35 -> 13.702s (1.75x)
shock .30 -> 14.829s (1.89x)
shock .25 -> 18.209s (2.33x)
shock .20 -> 21.578s (2.76x)
shock .15 -> 23.832s (3.04x)
shock .10 -> 29.454s (3.76x)
```

These values are sensitivity only. Very low damage can overload the current Stage49 stress, so the next task is a **control-vs-clear Pareto search**, not choosing a coefficient now.

## Archer — identity supported

First finite pair:

```text
aligned line ~= 3.58s
scatter      ~= 8.08s
```

The same qualitative split survives ATTACK_HEAVY.
Thus Archer line dependence remains strong; the prior Stage49 attack-heavy problem is localized primarily to packet/frontmost chronology rather than a global Archer identity collapse.

## Mage — identity supported

```text
clustered   ~= 3.78s
distributed ~= 8.08s
```

Density/AoE identity remains strong.

## Rogue — new breakpoint watch

With approximately comparable total durability:
- durable packet = armored durable proxy + BRUTE;
- broad packet = 8 GRUNT + 8 RUNNER.

Rogue direct clear:

```text
shop scale 0%  : durable 3.828s / broad 5.453s
20%            : durable 3.778s / broad 4.406s
30%            : durable 3.727s / broad 3.829s
40%            : durable 3.727s / broad 3.829s
```

Root breakpoint:

```text
Dagger Storm base dagger = 600 * .45 = 270
at ~30% shop diagnostic scale -> ~321.84
GRUNT HP = 320
```

Once one dagger one-shots one GRUNT, approved post-kill retargeting can serially clean many weak bodies.

New HIGH watch:
`P5_ROGUE_DAGGER_GRUNT_ONESHOT_BREAKPOINT_WATCH`.

Do not remove approved retargeting or nerf Rogue yet; first measure distinct targets per storm and realistic shop magnitudes.

## Knight — fixture refinement required

First BALANCED pair suggested aligned advantage (`~3.73s` vs `~5.83s`), but ATK sensitivity exposed a non-monotonic target-death/second-wave chronology breakpoint.

Therefore:

```text
Knight identity defect = NOT established
current Knight paired fixture = insufficiently robust
```

Refine the probe before changing Knight.

---

# Current class classification

```text
Knight = STRUCTURALLY PLAUSIBLE / PAIRED FIXTURE REFINEMENT REQUIRED
Rogue  = CORE IDENTITY PRESENT / SHOP-DRIVEN BROAD-CLEANUP BREAKPOINT HIGH WATCH
Tank   = CONTROL IDENTITY PRESENT / NEGATIVE SOLO-THROUGHPUT DEFECT DIRECTIONALLY CONFIRMED
Archer = LINE DEPENDENCE STRONGLY CONFIRMED / STAGE49 CHRONOLOGY WATCH LOCALIZED
Mage   = DENSITY DEPENDENCE STRONGLY CONFIRMED
```

---

# Stable P5 / encounter boundaries

A2 shop semantics remain approved; exact values remain open.
Current diagnostic centers only:

```text
full-shop reference 16360
spend center 50%
income mix center 70/30
shop effect center 40% legacy-relative
```

Cross-class shop lane remains ATK/FORT/DEF.
KNOCK and CRIT/CRITDMG remain separate policy lanes.

Actual enemy entry remains:

```text
NORMAL RIGHT EDGE ONLY
NO MID-FIELD POP-IN
```

Stage46→49 direction remains power revelation -> transition -> protected role pulse -> escorted second pulse.
Do not resume precise Stage49 tuning until class identity reconverges.

---

# Exact next boundary

1. Tank control-vs-clear Pareto search: preserve knockback/slow/barrier, scan lower final damage contribution, measure both wall survival and actual solo throughput;
2. Rogue distinct-target-per-storm + one-shot breakpoint sensitivity;
3. replace Knight paired packet with a more robust penetration-causality probe;
4. exact/committed-execute the identity runner when byte-equivalent execution is available;
5. integrate identity metrics into the source-patched Stage46–49 right-edge runner;
6. only then resume Stage49 packet chronology refinement;
7. later KNOCK, CRIT/CRITDMG, EXP/Lv feedback, P10/P10R.

P6 remains blocked pending P5 closure.
