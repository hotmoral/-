# Timing Defense — N3 Combo Milestone Review

Date: 2026-10-21 KST  
Status: **EXACT LEGACY RULE RECOVERED / PRODUCT DECISION REQUIRED BEFORE SLICE C IMPLEMENTATION**

## 0. Why this review is now

N3 is the experimental PERFECT-combo milestone extra-attack system.
It was intentionally deferred during v0.36/v0.37 because it can multiply combat-event volume in 3–4 player multiplayer.

Slice C is specifically the larger-party/event-delivery slice, so the product contract must be decided now before the delivery kernel is finalized.

No N3 numerical or gameplay change is implemented by this document.

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

Milestone raw-equivalent candidate budget:
- 5 combo: 60
- 10 combo: 90
- 20 combo: 150
- 30+ combo: 210

The counter continues upward, but 40/50/60/etc continue to use 210.

---

## 4. Exact playable legacy class behavior

### Rogue
Milestone projectile count:
- 5: 2 daggers
- 10: 3 daggers
- 20: 4 daggers
- 30+: 5 daggers

Each dagger receives approximately `budget / count`, rounded individually.
Actual maximum raw totals from the legacy rounding:
- 5: 30×2 = 60
- 10: 30×3 = 90
- 20: 38×4 = 152
- 30+: 42×5 = 210

All daggers initially target the same selected monster. If that target disappears before a later dagger resolves, legacy skill resolution can fall back to the nearest living monster.

### Knight
- primary target: 67% of budget
- one forward/near secondary target: 33% of budget, if available
- max 2 hit events

Legacy rounded max totals:
- 5: 40 + 20 = 60
- 10: 60 + 30 = 90
- 20: 101 + 50 = 151
- 30+: 141 + 69 = 210

If no valid secondary target exists, only the 67% primary portion is realized.

### Tank
- primary target: 60% of budget
- up to two nearby secondary targets: 20% each
- max 3 hit events

Max total with two nearby targets:
- 5: 36 + 12 + 12 = 60
- 10: 54 + 18 + 18 = 90
- 20: 90 + 30 + 30 = 150
- 30+: 126 + 42 + 42 = 210

With fewer nearby targets, some of the theoretical budget is intentionally unrealized.

### Archer
- primary target: 70% of budget
- one strict straight-line target behind it: 30%, if available
- no seeking/bending
- max 2 hit events

Max total when a line target exists:
- 5: 42 + 18 = 60
- 10: 63 + 27 = 90
- 20: 105 + 45 = 150
- 30+: 147 + 63 = 210

If no valid line target exists, only 70% is realized.

### Mage
- primary target: 55% of budget
- up to three nearby targets: 15% each
- max 4 hit events

Legacy independent rounding produces small overshoot at higher tiers:
- 5: 33 + 9×3 = 60
- 10: 50 + 14×3 = 92
- 20: 83 + 23×3 = 152
- 30+: 116 + 32×3 = 212

If fewer nearby targets exist, the unused splash portions are not redirected to the primary target.

---

## 5. What N3 does NOT do in the experimental implementation

Combo reward projectiles are explicitly created with:
- no proc crit,
- no PERFECT flag for skill chaining,
- no normal skill-power rank,
- no EXP grant,
- no charge gain,
- no new combo increment.

Therefore N3 is a terminal bonus attack, not a recursive proc engine.

However, legacy `visualImpact` still treats it as local player damage for ordinary combat consequences:
- monster HP damage,
- kill attribution,
- kill coin reward,
- normal armor interaction,
- normal local hit visual feedback.

Frozen boss Rogue scalar 0.70 also applies through the normal Rogue impact path.

---

## 6. Ambiguous legacy coupling that requires an explicit product decision

The implementation assigns milestone tiers for the projectile:
- 5 -> GOOD
- 10 -> PERFECT
- 20 -> SUPER
- 30+ -> CRITICAL

`visualImpact` uses tier to determine knockback, and class-level knock multipliers can also participate.

Therefore the old playable code can make higher N3 milestones cause stronger knockback even though the V8 balance report describes the milestone primarily as a raw-damage-equivalent budget.

This knockback behavior is an **implementation consequence, not clearly frozen by the V8 design report**.
Do not silently preserve or remove it; decide explicitly.

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

Interpretation from V8:
- N3 is not intended as ordinary DPS inflation,
- its main purpose is mastery reward / pressure / spectacle,
- 20+ and repeated 30+ procs are rare prestige bursts.

---

## 8. Slice C event-volume consequence

Current Durable Object event storage keeps at most 48 recent events, while public snapshots expose only the last 24 events.

N3 can exceed that 24-event snapshot tail during synchronized 4-player bursts, even with the currently validated Lv6-only skill set.

Illustrative worst-case simultaneous milestone bursts:

### Four Lv6 Rogues at 30+
Per player:
- normal authoritative primary = 1 event
- Lv6 second dagger = 1 event
- N3 = 5 dagger events
- total = 7 combat-hit events per player

Four players = **28 hit events**, before passive events.

### Four Lv6 Mages with dense valid targets
Per player:
- normal primary + up to 3 Lv6 splash = 4 events
- N3 primary + up to 3 N3 splash = 4 events
- total = 8 events per player

Four players = **32 hit events**, before passive events.

Therefore fixed `events.slice(-24)` is not sufficient as the long-term N3 delivery contract.
Rare probability does not make silent visual-event loss acceptable.

Slice C should generalize event delivery before N3 is enabled in multiplayer.

---

## 9. Product decision options

### Option A — literal legacy port
Preserve the old playable behavior exactly:
- trigger grammar 5/10/20/30/every +10,
- budgets 60/90/150/210,
- existing class geometry,
- existing independent rounding (including Rogue/Mage small overshoot),
- existing milestone-tier knockback behavior.

Pros:
- closest migration parity.

Cons:
- preserves incidental rounding and knockback coupling that were never clearly balance-frozen.

### Option B — cleaned N3 contract (recommended)
Preserve the intended design while removing implementation accidents:
- same trigger grammar,
- same 60/90/150/210 capped budgets,
- same class identities/target geometry,
- no EXP / charge / combo / crit / recursive skill proc,
- player gets normal damage/kills/kill-coin attribution,
- armor and frozen boss scalars apply normally,
- normalize each milestone so its class's theoretical maximum damage budget is exactly 60/90/150/210 rather than 151/152/212 rounding artifacts,
- explicitly define knockback rather than inheriting it accidentally from milestone display tier.

Recommended knockback sub-rule for Option B:
- preserve class identity but prevent milestone damage tier from automatically escalating generic knockback,
- use a fixed N3 knockback semantic per class or NORMAL-equivalent base, with Tank retaining its class knockback advantage.

Pros:
- keeps the mastery reward and class flavor,
- easier to reason about and server-test,
- avoids freezing accidental code artifacts.

Cons:
- not byte-for-byte legacy parity, so requires explicit approval.

### Option C — no N3
Keep persistent 5/8/12/15% combo bonus only and discard milestone attacks.

This is a real product decision, not the current default. N3 must not disappear merely because implementation is inconvenient.

---

## 10. Recommended execution order after decision

If A or B is approved:
1. Slice C first upgrades event delivery to a loss-resistant monotonic event stream/history contract.
2. Validate 3H / 4H / 2H+2AI / 3H+1AI without N3 enabled.
3. Add N3 as its own bounded server-authority slice on top of the hardened event kernel.
4. Deterministic forced-combo tests for 5/10/20/30/40 on all five classes.
5. 4-player synchronized milestone stress simulation.
6. One final Samsung Browser presentation smoke.
7. Only then continue to Stage 4 SHIELD.

If C is approved, record N3 as explicitly rejected rather than merely deferred.

---

## 11. Current recommendation

**Recommend Option B: retain N3 as a mastery system, but formalize it before server implementation rather than copying v0.18's incidental rounding/knockback behavior.**

The V8 evidence supports the underlying concept: ordinary players are barely affected, while high PERFECT streaks gain memorable class-specific burst moments.

The event-delivery kernel must be fixed in Slice C before N3 is enabled.