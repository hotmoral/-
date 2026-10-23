# Timing Defense — P5 Clear/Kill Income-Mix Sensitivity V0.1

Date: 2026-10-23 KST  
Status: **DIRECTIONAL SENSITIVITY / 70-30 WORKING CENTER SUPPORTED / NO NUMERICAL FREEZE / NO PRODUCTION CHANGE**

Depends on:
- `116_P5_RUN_COIN_SHOP_A2_APPROVED_STRUCTURAL_CONTRACT_V0_1.md`
- `117_P5_SPEND_CAPACITY_ENVELOPE_V0_1.md`
- `118_P5_ECONOMY_ONLY_POLICY_PREFLIGHT_V0_1.md`

---

# 0. Purpose

Test how much of an intended player's personal run income should come from:

```text
predictable all-human Stage-clear income
vs
killer-only ordinary-monster income
```

without yet choosing production coin denominations.

Keep baseline total spend capacity at the current working CENTER = 50% of full-shop reference cost.

---

# 1. Candidate source mixes

```text
CLEAR / KILL
80 / 20
70 / 30
60 / 40
```

Kill-share multiplier is measured relative to the expected/equal-share kill-income component:

```text
1.0 = expected kill share
0.8 / 1.2 = moderate ±20% relative kill-share deviation
0.6 / 1.4 = stress ±40% relative deviation
```

Resulting whole-wallet capacity ratio:

```text
80/20:
moderate 48%..52%
stress   46%..54%

70/30:
moderate 47%..53%
stress   44%..56%

60/40:
moderate 46%..54%
stress   42%..58%
```

---

# 2. Balanced final rank sensitivity

At the same CENTER50 expected wallet, total six-track rank sum at Stage49 is approximately:

```text
80/20
moderate: 44..45 total ranks
stress:   43..46

70/30
moderate: 43..46
stress:   42..47

60/40
moderate: 43..46
stress:   41..48
```

Expected-share center is about 45 total ranks under the current reference shape.

No tested source mix approaches six-track full max (60 total Rank10 ranks).

---

# 3. 70/30 working-center detail

Balanced Stage49 rank shapes:

```text
kill multiplier 0.8
ATK7 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK7
(total 43)

kill multiplier 1.0
ATK8 / CRIT7 / CRITDMG7 / FORT8 / DEF7 / KNOCK8
(total 45)

kill multiplier 1.2
ATK8 / CRIT7 / CRITDMG8 / FORT8 / DEF7 / KNOCK8
(total 46)
```

Stress:

```text
kill multiplier 0.6
all six roughly Rank7
(total 42)

kill multiplier 1.4
ATK8 / CRIT8 / CRITDMG8 / FORT8 / DEF7 / KNOCK8
(total 47)
```

Stage trajectory total-rank counts under 70/30:

```text
             S20  S30  S40  S45  S49
kill x0.8     20   29   37   41   43
kill x1.0     21   30   38   42   45
kill x1.2     22   31   39   43   46
```

Moderate divergence stays roughly one total purchased rank on either side at several checkpoints and three total ranks across the two extremes by Stage49.

---

# 4. Interpretation

## 80/20
Pros:
- strongest protection from class/last-hit wallet divergence.

Risk:
- kill reward may become too economically decorative and reduce satisfaction from personal finishing contribution.

## 60/40
Pros:
- personal kill performance matters more.

Risk:
- stress kill-share variation can create up to ~7 total-rank separation in this simple rank-space model;
- more likely to require multiplayer/class normalization later.

## 70/30
Current best compromise direction:
- kill reward remains economically noticeable;
- common clear floor still dominates enough to damp moderate last-hit variance;
- moderate ±20% kill-share divergence maps to only ~47%..53% total spend capacity;
- Stage49 rank divergence remains bounded in the first preflight.

Classification:

```text
CLEAR_KILL_70_30 = WORKING_CENTER_SUPPORTED
NOT_FROZEN
```

---

# 5. Important limitations

This sensitivity does not yet model:
- actual 50-Stage monster reward distribution;
- exact class-specific kill-share from current nine-monster encounters;
- solo vs 2/3/4P encounter scaling;
- AI kill ownership;
- shop power changing future kill share;
- combat clear/fail feedback;
- EXP feedback.

Therefore `70/30` is an analysis center only.

---

# 6. Next boundary

Use the working `50% total spend capacity + 70/30 clear/kill source mix` as the center lane for the next defensive integration probe, with:

```text
spend capacity sensitivity: 45 / 50 / 55
source mix sensitivity: 80/20 / 70/30 / 60/40
kill-share sensitivity: moderate ±20%, stress ±40%
```

Next test:
- Fortification value/cost envelope;
- generic DEF value/cap envelope;
- persistent wall attrition and Stage49->50 reserve;
- whether DEFENSE_HEAVY becomes a trivial dominant strategy.

No production values are frozen.