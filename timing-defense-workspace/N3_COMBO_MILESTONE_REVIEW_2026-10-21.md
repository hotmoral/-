# Timing Defense — N3 Combo Milestone Review

Date: 2026-10-21 KST  
Status: **REVIEW COMPLETE / OPTION B APPROVED / FROZEN CONTRACT CREATED**

The exact legacy rule was recovered and reviewed before Slice C. The user approved **Option B — cleaned N3 contract**.

Canonical frozen contract:
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

N3 is **not enabled in multiplayer yet**. Slice C must harden event delivery first; N3 will then be implemented as its own bounded authority slice.

---

## 1. Source truth audited

Primary legacy implementation:
- `timing-defense-v011/v019-combo-pop.js`
- `timing-defense-v011/v018-auto-combo.js`
- `timing-defense-v011/v016-core.js`
- `timing-defense-v011/v014-combat.js`

Design / calibration truth:
- `DESIGN_DECISIONS.md`
- `BALANCE_SIM_REPORT_V8_AUTO_COMBO.md`

Important distinction:
- V8 was calibration/candidate work, not final frozen balance.
- the later v0.18 source implements the candidate behavior experimentally.
- therefore the source tells us what was playable, but does not automatically freeze it as production balance.

---

## 2. Exact combo trigger grammar

PERFECT streak:
- only PERFECT increments,
- GOOD / NORMAL / MISS reset to 0,
- attacks 1–3 can add +1 each,
- heavy attack X and Y are counted separately,
- fully PERFECT 1→4 cycle contributes +5 total,
- counter is unbounded.

Milestone trigger function in legacy implementation:
- combo 5,
- combo 10,
- combo 20,
- combo 30,
- every multiple of 10 above 30: 40 / 50 / 60 / ...

30+ does not increase power further. Every 40/50/60/etc proc reuses the 30-tier power.

Because heavy X/Y are separate PERFECT judgments, a milestone can be crossed during either half of the heavy input. The pending milestone is resolved after the attack's normal hit resolution.

---

## 3. Persistent combo bonus is separate from N3

Already-existing persistent timing-attack multiplier candidate:
- combo 5–9: +5%
- combo 10–19: +8%
- combo 20–29: +12%
- combo 30+: +15% cap

N3 is an **additional milestone burst on top of that persistent multiplier**.

Milestone raw-equivalent candidate budget recovered from legacy/V8:
- 5 combo: 60
- 10 combo: 90
- 20 combo: 150
- 30+ combo: 210

The approved Option B contract keeps these exact budgets but removes accidental over-budget rounding.

---

## 4. Legacy class behavior recovered

### Rogue
Milestone projectile count:
- 5: 2 daggers
- 10: 3 daggers
- 20: 4 daggers
- 30+: 5 daggers

### Knight
- primary 67% intent
- one forward/near secondary 33% intent
- max 2 hit events

### Tank
- primary 60% intent
- up to two nearby secondary targets at 20% intent each
- max 3 hit events

### Archer
- primary 70% intent
- one strict straight-line secondary 30% intent
- no seeking/bending
- max 2 hit events

### Mage
- primary 55% intent
- up to three nearby targets at 15% intent each
- max 4 hit events

Approved Option B preserves this class geometry but uses deterministic remainder-safe allocation so a milestone never exceeds its exact 60/90/150/210 maximum budget.

---

## 5. Approved proc isolation

N3 attacks:
- no EXP,
- no charge,
- no combo increment,
- no ordinary proc crit,
- no recursive class-skill proc,
- no recursive N3 proc.

They remain authoritative player-owned damage for monster HP, kill attribution, kill coin and contribution damage.
Normal armor rules and frozen boss scalars continue to apply.

---

## 6. Knockback decision — APPROVED

The legacy implementation accidentally coupled milestone display tier to generic GOOD/PERFECT/SUPER/CRITICAL knockback escalation.

Option B explicitly rejects that coupling.

Frozen rule:
- N3 uses NORMAL-equivalent generic knockback base,
- independently authoritative class multipliers may still apply,
- Tank retains its class knockback advantage,
- milestone number itself does not increase generic knockback.

---

## 7. Balance evidence from V8

V8 Monte Carlo treated high streaks as rare mastery events.
Approximate probability of reaching the streak at least once in ~150 judgment opportunities:

- Skilled P40: 5 combo ~61%, 10 combo ~0.87%, 20+ effectively near zero.
- Expert P65: 10 combo ~50.6%, 20 combo ~0.83%, 30 combo ~0.014%.
- Master-test P80: 20 combo ~27.8%, 30 combo ~3.23%, 40 combo ~0.30%.

Estimated mean damage uplift from the combined combo-power candidate remained modest:
- Average ~0.01%
- Skilled ~0.26%
- Expert ~1.99%
- Master-test ~4.74%

The approved product intent remains mastery reward / pressure / spectacle rather than ordinary DPS inflation.

---

## 8. Slice C event-volume consequence

Legacy server storage kept at most 48 recent events and public snapshots exposed only the last 24 events.

Illustrative N3 synchronized burst sizes:
- four Lv6 Rogues at 30+: up to ~28 combat-hit events before passive events,
- four Lv6 Mages in dense geometry: up to ~32 combat-hit events before passive events.

Therefore Slice C must remove dependence on fixed `events.slice(-24)` delivery before N3 is enabled.

---

## 9. Approved execution order

1. Slice C upgrades event delivery to a per-socket monotonic, loss-detectable contract.
2. Validate 3H / 4H / 2H+2AI / 3H+1AI with N3 still disabled.
3. Add N3 as its own bounded server-authority slice.
4. Forced combo tests for 5/10/20/30/40 on all five classes.
5. Four-player synchronized milestone stress simulation.
6. One final Samsung Browser presentation smoke.
7. Then continue to Stage 4 SHIELD.

---

## 10. Decision summary

**Option B is approved and no longer deferred.**

The system is retained, cleaned, and product-frozen by `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`. Implementation remains gated on Slice C event-delivery PASS.
