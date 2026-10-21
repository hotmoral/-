# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**
7. v0.37 Slice B Stage 3 + BRUTE — **PASS**

Exact v0.37 Slice B full-PASS checkpoint:
- branch `timing-defense-cloudflare-v037-slice-b-pass-20261021`
- HEAD `08af6e1e9f399ad13369990dcc452f012ddda1fa`

Read:
- `N3_COMBO_MILESTONE_REVIEW_2026-10-21.md`
- `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`
- `PROJECT_STATUS.md`
- `SESSION_HANDOFF.md`
- `CLOUDFLARE_POST_V035_PREFLIGHT_2026-10-21.md`

## Numerical decisions already closed
- N1 exact legacy EXP — **PASS / frozen for migration parity**.
- N2 exact AI stage multiplier `1 + (stage - 1) * 0.035` — **PASS / frozen for migration parity**.

## Active decision gate — N3 combo milestone attacks
Status: **EXACT LEGACY RULE RECOVERED / USER PRODUCT DECISION REQUIRED**

Do not implement Slice C event delivery or Stage 4 until the N3 product direction is explicitly chosen, because N3 changes the required worst-case event-delivery capacity.

Exact recovered milestone grammar:
- combo 5 -> raw-equivalent budget 60,
- combo 10 -> 90,
- combo 20 -> 150,
- combo 30 -> 210,
- combo 40/50/60/... -> repeat 210,
- combo count itself remains unbounded,
- persistent 5/8/12/15% combo multiplier is a separate already-existing mechanic.

Legacy class burst shapes:
- Rogue: 2 / 3 / 4 / 5 daggers,
- Knight: 67% primary + 33% one secondary,
- Tank: 60% primary + up to two 20% nearby hits,
- Archer: 70% primary + 30% one strict-line secondary,
- Mage: 55% primary + up to three 15% nearby hits.

N3 never grants EXP/charge/combo/crit and does not recursively activate the normal skill chain. Player damage/kills/kill coin remain normal consequences of the milestone attack.

Important ambiguity:
- legacy implementation independently rounds each sub-hit, producing small max-budget overshoot for some classes,
- milestone display tier also indirectly escalates knockback,
- these are implementation consequences and were not clearly balance-frozen by V8.

Current recommendation:
- **Option B / cleaned N3 contract**,
- keep the mastery system, trigger grammar, budgets and class geometry,
- normalize theoretical max damage to exact 60/90/150/210,
- explicitly define N3 knockback instead of inheriting accidental tier-based escalation,
- preserve no-EXP/no-charge/no-combo/no-crit/no-recursive-proc semantics,
- retain armor, kill contribution, coin, and frozen boss scalars.

See `N3_COMBO_MILESTONE_REVIEW_2026-10-21.md` for Option A/B/C details.

## Event-delivery consequence already established
Current server retains 48 recent events internally but public snapshots expose only the last 24.

N3 can exceed 24 events in a legitimate synchronized 4-human burst with the already validated Lv6 skills:
- 4 Lv6 Rogues at a 30+ milestone: up to 28 combat-hit events before passive fire,
- 4 dense-target Lv6 Mages at a milestone: up to 32 combat-hit events before passive fire.

Therefore if N3 is retained, Slice C must replace the fixed 24-event-tail assumption with loss-resistant event delivery before N3 is enabled.

## Next implementation slice after N3 decision — Slice C / larger-party baseline
Do **not** start Stage 4 yet.

Target party combinations:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

Required audit/implementation:
1. Verify fixed P1–P4 slot ownership under all supported mixes.
2. Verify host identity under reconnect and simulated peers.
3. Verify READY/START semantics with 3–4 humans.
4. Verify Team Shop READY/NEXT with larger parties and human+AI mixes.
5. Preserve current fixed AI FILL semantics unless separately decided.
6. Verify result-board participant ordering/count.
7. Generalize event delivery so each client can obtain all events after its event floor without depending on only `events.slice(-24)`.
8. Preserve reconnect historical-event suppression and server damage authority.
9. Expand 3/4-client live automation before manual play.
10. If N3 Option A/B is approved, size and stress-test the delivery kernel against its worst-case event burst even before N3 itself is enabled.

### Automation requirement
Cover at minimum:
- 3H,
- 4H,
- 2H+2AI,
- 3H+1AI,
- READY -> START,
- synchronized Stage 1 combat,
- reconnect,
- Team Shop READY/NEXT,
- Stage 2 entry,
- participant/result consistency,
- event-ID monotonicity and no silent event loss at the designed maximum burst.

### Manual validation policy
After automation passes:
- use simulated peers so one phone remains sufficient where practical,
- run one short Samsung Browser render/input smoke,
- do not ask for repetitive manual party-size or exact-number verification already covered by automation.

## Following slices
### N3 authority slice, if retained
After Slice C event kernel is hardened:
- server-authoritative milestone trigger,
- forced combo 5/10/20/30/40 tests for all five classes,
- synchronized four-player milestone stress,
- final device presentation smoke.

### Stage 4 — SHIELD / armor
Only after Slice C closes and the N3 placement decision is respected.

### Stage 5–6
- checkpoint boss,
- FLYER,
- authoritative Y geometry required before FLYER/geometric skill interactions.

### Stage 7–9
- mixed-roster stress.

### Stage 10
- final boss and final result semantics.

### Lv11/16/21 authority
Use forced-level deterministic tests before natural progression depends on each milestone.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work must continue to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
