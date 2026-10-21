# Timing Defense — Next Work Boundary

Updated: 2026-10-22 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**
5. v0.35 reconnect / Team Shop / Stage 2 parity — **PASS**
6. v0.36 Slice A N1/N2 + Lv6 authority — **PASS**
7. v0.37 Slice B Stage 3 + BRUTE — **PASS**
8. v0.38 Slice C larger-party/event kernel — **FULL PASS**

Exact v0.38 full-PASS checkpoint:
- branch `timing-defense-cloudflare-v038-slice-c-pass-20261022`
- HEAD `cbcddf35443ff901b4a30dd6621da5a984335fb5`

## N3 product decision — APPROVED / FROZEN
Option B remains frozen:
- combo 5 / 10 / 20 / 30 / every +10 after 30
- exact raw-equivalent maximum budgets 60 / 90 / 150 / 210
- class geometry retained
- deterministic remainder-safe allocation
- no EXP / charge / combo increment / ordinary crit / recursive skill / recursive N3
- normal armor / kill / kill coin / contribution
- frozen boss scalars
- NORMAL-equivalent generic N3 knockback
- Tank retains class knockback identity

## Active slice — v0.39 N3 authority
Implementation branch:
`timing-defense-cloudflare-v039-n3-authority`

Current watched candidate HEAD:
`cee455520fbee04002d2fb12f33dc24ffe129264`

Expected health:
`0.39-cf.1`

### Implemented candidate behavior
- server detects N3 milestones from authoritative combo-before/action judges
- N3 uses `type: n3` server events
- exact-budget allocator prevents legacy overshoot
- Rogue delayed milestone daggers use dedicated `n3Queue`
- N3 queue is separate from Lv6 Rogue skill queue
- combat-end hardening clears delayed N3 queue
- legacy local combo-reward damage path is suppressed in multiplayer
- N3 client layer renders server-confirmed N3 events only
- Stage 4 remains blocked

### Deterministic validation requirements
All five classes at combo milestones:
- 5
- 10
- 20
- 30
- 40

Must assert:
- exact maximum budget
- exact intended hit count / geometry
- N3 event tier is NORMAL-equivalent for generic knockback
- no extra EXP
- no extra charge
- no extra combo
- no ordinary proc crit
- no recursive class skill
- no recursive N3
- unused secondary budget is not redirected
- kill / coin / kill-coin / contribution attribution
- Rogue boss 0.70 scalar
- Tank Lv6 N3 knockback identity
- Lv6 Rogue normal second dagger + N3 daggers coexist without duplicate authority
- heavy X/Y combo counting and reset semantics

### Live four-human stress
Create 4 human Rogues, arm all at:
- Lv6
- combo 29

Then send synchronized PERFECT.

Expected combat events visible to every connected client:
- 4 ordinary `hit`
- 4 Lv6 Rogue `skill`
- 20 N3 Rogue `n3`
- total **28 combat events**

Must also verify:
- all N3 events milestone 30
- all N3 budget metadata 210
- no `event-gap`
- post-floor event IDs contiguous
- all four server combos become 30

### One-click validation gate
`/v039-validation-suite.html`

It runs:
1. complete v0.38 regression suite
2. N3 deterministic server tests
3. N3 client-authority tests
4. synchronized 4H N3 stress

After automated PASS:
- run one short Samsung Browser presentation smoke only
- preserve exact v0.39 PASS checkpoint
- then move to Stage 4 SHIELD / armor

## Following slices
- Stage 4 SHIELD / armor
- Stage 5–6 checkpoint boss + FLYER + authoritative Y geometry
- Stage 7–9 mixed-roster stress
- Stage 10 final boss/result
- Lv11/16/21 authority

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred. Implement later as one shared responsive layer, not per-device patches.

## Governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
