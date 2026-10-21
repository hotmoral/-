# Timing Defense — N3 Combo Milestone Frozen Contract

Date: 2026-10-21 KST  
Decision: **OPTION B APPROVED / PRODUCT CONTRACT FROZEN / IMPLEMENTATION NOT YET ENABLED**

## 1. Trigger grammar
- PERFECT only increments combo.
- GOOD / NORMAL / MISS reset combo.
- heavy X and Y count independently.
- milestone proc at combo 5 / 10 / 20 / 30.
- after 30, proc again at every +10: 40 / 50 / 60 / ...
- power caps at the 30-tier; combo count itself remains unbounded.

## 2. Persistent combo multiplier remains separate
- 5–9: +5%
- 10–19: +8%
- 20–29: +12%
- 30+: +15% cap

N3 is an additional milestone burst on top of this persistent multiplier.

## 3. Exact milestone damage budgets
- 5 combo: 60 raw-equivalent maximum budget
- 10 combo: 90
- 20 combo: 150
- 30+ combo: 210
- 40/50/60/etc continue to use 210

Unlike the experimental legacy implementation, independent rounding must not make a class exceed the exact milestone budget.

## 4. Frozen class geometry
### Rogue
- 5/10/20/30+ => 2/3/4/5 daggers.
- distribute the exact total milestone budget across the daggers deterministically.
- same-target execution allowed.
- if the original target disappears before a later dagger resolves, nearest-valid-target fallback is allowed, matching the prior multihit identity.

### Knight
- primary 67% intent + one forward/near secondary 33% intent.
- max two targets.
- total realized damage must never exceed the milestone budget.
- if no secondary exists, unused secondary budget is not redirected to primary.

### Tank
- primary 60% intent + up to two nearby secondary portions of 20% each.
- max three targets.
- unused secondary portions are not redirected.

### Archer
- primary 70% intent + one strict straight-line secondary 30% intent.
- no seeking, bending or unrelated retargeting.
- unused line-secondary portion is not redirected.

### Mage
- primary 55% intent + up to three nearby secondary portions of 15% each.
- max four targets.
- unused splash portions are not redirected.

For percentage splits whose independent rounding would exceed the budget, server allocation must use a deterministic remainder-safe allocator so the total maximum is exactly the milestone budget.

## 5. Proc isolation
N3 attacks:
- grant no EXP,
- grant no charge,
- do not increment combo,
- do not roll ordinary proc crit,
- do not recursively trigger class skills,
- do not recursively trigger another N3 milestone.

They remain player-owned authoritative damage for:
- monster HP,
- kill attribution,
- kill coin,
- contribution damage.

Normal monster armor rules apply. Existing frozen boss scalars apply, including Rogue boss dagger scalar 0.70 where relevant.

## 6. Knockback contract
Legacy milestone display tiers accidentally coupled N3 to GOOD/PERFECT/SUPER/CRITICAL knockback escalation. That coupling is explicitly rejected.

Frozen rule:
- N3 uses **NORMAL-equivalent generic knockback base** for milestone hits.
- class identity multipliers that are independently authoritative may still apply.
- Tank retains its class knockback advantage.
- milestone number itself does not increase generic knockback.

No new N3-specific knockback coefficient is introduced by this decision.

## 7. Presentation identity
N3 should remain a rare mastery/spectacle event with class-specific projectile/impact presentation.
The milestone label can scale visually at 5/10/20/30+, but visual tier must not secretly alter damage or knockback beyond this frozen contract.

## 8. Multiplayer/event-delivery prerequisite
N3 must not be enabled on the live multiplayer path until Slice C replaces the current fixed snapshot-tail assumption with a monotonic, loss-detectable event-delivery contract.

Reason: synchronized 4-player milestone bursts can exceed the old public 24-event snapshot window.

## 9. Validation requirement before enabling N3
A dedicated later N3 authority slice must include:
- forced combo 5/10/20/30/40 deterministic tests for all five classes,
- exact-budget assertions,
- geometry/target-selection assertions,
- no EXP/charge/combo/crit/recursive-skill assertions,
- kill/coin/contribution attribution assertions,
- boss-scalar assertions,
- 4-player synchronized milestone event-volume stress,
- one final Samsung Browser presentation smoke.

## 10. Governance
This contract is now product-frozen. Numerical or behavioral changes require the normal workflow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
