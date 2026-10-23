# Timing Defense — P4-D2 Stage48–49 Grammar Reset Proxy V0.1

Date: 2026-10-23 KST  
Status: **BOUNDED STATIC RESET PROXY / ROTATING-GRAMMAR DIRECTION SUPPORTED / NO NUMERICAL FREEZE / P4-D2 CONTINUES**

Authority:
- `95_P4D2_STAGE46_STATEFUL_TEMPORAL_PRESSURE_PROBE_V0_1.md`
- `96_P4D2_ARCHER_LV31_WIDE_CORRIDOR_APPROVED_AMENDMENT_V0_1.md`
- `97_P4D2_ROLE_ALIGNMENT_AND_ARCHER_WIDTH_PROBE_V0_1.md`

Machine-readable evidence:
- `data/p4d2_stage48_49_grammar_reset_proxy_v0_1.json`

---

# 0. Purpose

Document 95 showed a class-divergent miss problem in one generic mixed pressure recipe:
- Rogue/Knight became near-terminal quickly after missed P×P resets;
- Tank/Archer/Mage retained much more recovery margin.

The approved repair order is **encounter grammar first**, not hidden class buffs, EXP correction, or automatic nerfs.

This cheap proxy asks whether four late-band pressure grammars can naturally expose different class strengths/weaknesses when one successful Lv31 final is applied.

It is intentionally static and bounded. It is not a full Stage48/49 simulation.

---

# 1. Grammar families

```text
LINE_ESCORT
CLUSTER_CASCADE
FRONTLINE_BREACH
DURABLE_SCATTER
```

Working Lv31 centers are the current unfrozen P4-D2 centers:

```text
Knight  second wave 1.00
Rogue   16 daggers × .45
Tank    shockwave .75 / KB ×2.5
Archer  2.30 per target / MID_ADJACENT-style wide straight corridor
Mage    three stages .75 / radius1.25
```

---

# 2. Immediate reset result

| Grammar | Knight | Rogue | Tank | Archer | Mage |
|---|---:|---:|---:|---:|---:|
| LINE_ESCORT | **8/8** | 7/8 | 5/8* | **8/8** | 4/8 |
| CLUSTER_CASCADE | 8/9 | **9/9** | **9/9*** | 6/9 | **9/9** |
| FRONTLINE_BREACH | 7/8 | 5/8 | 4/8* | 5/8 | 7/8 |
| DURABLE_SCATTER | 7/8 | 6/8 | 3/8* | 3/8 | 2/8 |

Cells are immediate kills / snapshot bodies.

`*` Tank kill count materially understates its real final value because the static proxy does not price future time gained by global knockback, Aftershock, and wall barrier.

---

# 3. Interpretation

## LINE / ESCORT
- Archer receives the expected premium payoff from earned alignment.
- Knight also clears bounded frontline depth strongly.
- Mage does not receive a free screen-wide clear because fixed-circle geometry still matters.

## CLUSTER / CASCADE
- Mage receives the expected premium density payoff.
- Rogue's 16-projectile storm also handles clustered bodies efficiently through deterministic retarget.
- Tank's global shockwave performs strongly against the low/mid-durability cluster, while its future control value is additional.
- Archer leaves off-line bodies even with the approved wider corridor.

## FRONTLINE / BREACH
- Knight remains a strong frontline breaker.
- Tank's value is undercounted by kills because surviving durable bodies are also displaced/controlled.
- Rogue/Archer do not automatically erase every durable frontline body.

## DURABLE / SCATTER
This is the important counterweight.
- Archer cannot convert wide spatial scatter into free line deletion.
- Mage cannot turn widely separated durable bodies into one cluster collapse.
- Rogue/Knight remove more bodies but still do not imply universal trivialization.
- Tank gains time/control rather than raw full clear.

Thus no single grammar is a universal late-game test.

---

# 4. Structural conclusion

Result:

`ROTATING_GRAMMAR_CAN_DISTRIBUTE_CLASS_VULNERABILITY`

The evidence supports a Stage48–49 authoring direction like:

```text
LINE / ESCORT
-> CLUSTER / CASCADE
-> FRONTLINE / BREACH
-> DURABLE / SCATTER
-> recombine at higher pressure
```

The purpose is not equal damage or identical clear curves.
The purpose is to ensure every class eventually encounters a recurring pressure family that punishes a missed P×P reset through that class's natural weakness.

This is consistent with the user's desired late-game loop:

```text
Lv31 power is enormous
+
P×P/combo must still be maintained
+
missing resets lets the wrong kind of pressure accumulate
```

---

# 5. What this does NOT prove

This proxy does not prove:
- exact Stage48/49 clear rate;
- exact spawn cadence or composition;
- exact one-miss/two-miss recovery probability;
- final Tank balance;
- final Archer width;
- final Mage/SPLITTER chronology;
- final EXP convergence.

The next useful evidence is a **dynamic repeated-miss rotation probe** using these four grammar families over time.

---

# 6. Cross-system consistency

No reason was found to:
- nerf Rogue projectile count below the current 16 center;
- narrow Archer back to ordinary width;
- inflate SUPPORTER/SIEGER/SPLITTER HP merely to survive ultimates;
- add hidden class-specific late-game corrections.

Role-expression remains an authoring constraint:
- CHARGER telegraph should appear before interrupt counterplay in designated windows;
- SIEGER positioning/windup must create a readable decision opportunity;
- SPLITTER rebound should remain available when Mage misses or fails to catch the package.

---

# 7. Exact next boundary

Continue P4-D2 with dynamic Stage48–49 grammar rotation:

1. rotate the four grammar families over time;
2. compare all-P×P vs one miss vs two consecutive misses;
3. record class-specific burial/recovery direction;
4. check CHARGER/SIEGER/SPLITTER role opportunity counts;
5. tune grammar/ordering before class coefficients;
6. keep all exact content/numbers provisional.

No user decision is required at this boundary.
