# Timing Defense — Project Status

Updated: 2026-10-22 KST

## Executable checkpoint
- v0.45 SIEGER FULL PASS
- deployment HEAD `ea22cc279603394dc4b439b6fdbb0c83aff4299a`
- no gameplay/numerical implementation authorized after v0.45

---

# Current planning phase

**Class-aware Layer-A Combat Micro-Simulation**

Upstream structure is sufficiently closed.
Current default campaign spine is Model A.

Primary integrated authority:
- `legacy-game-structure/31_MASTER_CAMPAIGN_MATRIX_V0_2.md`

Current admission boundary:
- `legacy-game-structure/40_LAYER_A_PREFLIGHT_ADMISSION_REPORT_V0_1.md`

---

# Core user-confirmed truth

- 5 classes, independent Tier progression.
- Shared Tier/Stage combat content across classes.
- 1 Tier = 50 Stage.
- fail1–19=0★ / fail20–39=1★ / fail40–49=2★ / Stage50 clear=3★.
- stars = broad account permanent growth.
- achievements = targeted cross-class growth.
- recoverable soft walls intentional; hard class lockout forbidden.
- current 9 ordinary monsters are not lifetime final roster.
- T1 does not teach all 9; higher Tiers introduce new monsters.
- future Tier/monster expansion open.
- non-T1 intended-entry `SKILLED_V2_CENTRAL` full-Tier clear should normally be <60%.
- combo40 is skilled-achievable.
- **Lv31 target unlock window = Stage41–45.**
- Stage46–49 = post-Lv31 mastery.
- Stage50 = final, not Lv31 tutorial.

---

# Model A

```text
T1 G/R/B              Foundation / Timing & Frontline
T2 +SH/F              Mitigation / Geometry
T3 +C/SP              Burst / Transformation
T4 +SUP/SI            Formation / Siege
T5+ future            Expansion
```

Status:
**default bounded simulation spine / NOT production freeze**

Fallback Model B:
- T4 +SUPPORTER
- T5 +SIEGER
- only if T4 lower-layer evidence fails.

---

# Player power spine candidate

- Lv6 5–7
- Lv11 11–14
- Lv16 18–21
- Lv21 25–28
- Lv26 32–36
- Lv31 **41–45**

Only Lv31 window is user-confirmed.
Other windows remain calibration candidates.

Late grammar:
```text
31–39 pressure / soft-wall build
40     2★ gate
41–45  Lv31 Ascension
46–49  post-Lv31 mastery
50     Tier Final
```

---

# Current validation chain

## Master Campaign Layer-0
PASS, `errors=0 warnings=0`.

## Encounter Envelope Layer-A0
PASS, `errors=0 warnings=0`.

Tier legal archetypes:
- T1: 3
- T2: 7
- T3: 13
- T4: all current E01–E20

## Representative recipe static preflight
PASS.
- 20 recipes
- max authored 4s = 7
- max conservative effective 4s = 10
- no density WATCH/ERROR

## Kinematic preflight
PASS WITH WATCHES.

Key confirmed geometry:
- E10 focused siege first shot unscreened
- E11 escorted siege first shot screened
- E19 fortress can produce durable-screened siege
- representative CHARGER max simultaneous windup = 1

Important schema finding:
- delayed spawn alone cannot reliably represent `BACK`
- formation authoring needs actual initial X-depth (`spawnXOffset` design direction)
- target authority still uses actual frontmost X; no target override

## Generic DPS sensitivity
Diagnostic complete; high throughput sensitivity confirmed.

- SIEGER capability can disappear entirely when front screen is removed quickly
- CHARGER can die before windup
- SUPPORTER protected-aura duration changes sharply with throughput
- SPLITTER wall leakage changes sharply with throughput

No numeric patch authorized from this diagnostic.

---

# Difficulty / meta principle

Full clear rate alone is insufficient.
Fail location controls stars and therefore cross-class progression.

Preferred ordinary soft wall:
```text
late fail -> 1★/2★
 -> other-class progression
 -> permanent growth
 -> return
 -> old wall becomes attainable
```

Avoid normal difficulty dominated by Stage1–19 0★ failures.

Tier unlock first simulation hypothesis:
`CLEAR_LOCK` = same class Stage50 clear required to unlock next Tier.
Not frozen.

---

# Current exact boundary

Now work on:
**class-aware representative encounter micro-simulation**.

Required next outputs:
- deterministic action traces / SKILLED_V2 parameterization
- class-specific kill order and target reorder
- frontline block time
- wall pressure
- CHARGER telegraph/interrupt viability
- SPLITTER population pressure
- SUPPORTER aura/screened uptime
- SIEGER first-shot/shot-count/screened-firing uptime
- class opportunity/starvation

After PASS:
synthetic Tier slices, then full Tier simulation.

---

# Still not frozen

- final launch Tier count
- exact Tier unlock policy
- production monster coefficients
- exact 200-Stage schedule
- exact EXP formula
- Lv11+ production coefficients
- permanent star reward values
- achievement reward graph/value
- boss cadence/design
- shop cadence/economy
- detailed multiplayer balance

No live gameplay code or production balance number was changed by the current tranche.
