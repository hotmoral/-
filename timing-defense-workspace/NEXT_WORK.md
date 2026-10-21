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

Read first:
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`
- `CLOUDFLARE_V038_SLICE_C_CANDIDATE_2026-10-21.md`
- `CLOUDFLARE_V037_SLICE_B_PASS_2026-10-21.md`
- `PROJECT_STATUS.md`
- `SESSION_HANDOFF.md`

## Numerical/product decisions
- N1 exact legacy EXP — **PASS / frozen for migration parity**.
- N2 exact AI stage multiplier `1 + (stage - 1) * 0.035` — **PASS / frozen for migration parity**.
- N3 combo milestone attacks — **OPTION B APPROVED / PRODUCT CONTRACT FROZEN / NOT YET ENABLED**.

N3 frozen contract:
- milestones 5 / 10 / 20 / 30 / every +10 after 30,
- exact maximum budgets 60 / 90 / 150 / 210,
- Rogue 2/3/4/5 daggers,
- Knight 67/33 primary-secondary intent,
- Tank 60/20/20 intent,
- Archer 70/30 strict-line intent,
- Mage 55/15/15/15 intent,
- deterministic remainder-safe allocation so no class exceeds the milestone budget,
- no EXP / charge / combo / proc crit / recursive skill / recursive N3,
- normal armor, kill, kill coin and contribution attribution,
- frozen boss scalars apply,
- N3 generic knockback uses NORMAL-equivalent base; milestone number does not escalate generic knockback,
- class identity multipliers still apply, including Tank's class advantage.

N3 implementation remains gated until Slice C event delivery is PASS.

## Active slice — v0.38 Slice C / larger-party event kernel
Status: **IMPLEMENTED / WATCHED BRANCH TRIGGERED / LIVE AUTOMATION PENDING**

Candidate:
- implementation branch `timing-defense-cloudflare-v038-slice-c-event-kernel`
- watched branch `timing-defense-cloudflare-do-poc`
- candidate HEAD `0c96f038f6fcf7ec5e27e7d7fe0db38343a807c7`
- expected health `0.38-cf.1`
- loader cache `cf0381`

### Event-delivery kernel
The old fixed snapshot-tail assumption is replaced for WebSocket delivery:
- server retains 512 authoritative events per run,
- each accepted WebSocket stores `eventRunId` + `eventCursor` in its hibernation attachment,
- newly created events are delivered as per-socket monotonic `event-batch` messages,
- normal socket state snapshots carry zero event payload and no longer depend on `events.slice(-24)`,
- retention discontinuity produces explicit `event-gap`, not silent continuity,
- sockets that existed before a new run start receive the new run from event 0,
- reconnect sockets in an already-running run floor at latest and preserve the existing v0.35 resume/eventFloor no-historical-replay contract.

N3 remains disabled in v0.38.
Stage 4 remains blocked.

### Deterministic validation
v0.38 server self-test includes:
- 512-event retention and monotonic IDs,
- complete 32-event burst delivery (> legacy 24),
- per-socket cursor advancement,
- explicit gap detection,
- pre-run -> new-run cursor behavior,
- reconnect floor behavior,
- independent socket cursors.

### Live party automation
`v038-party-sim.html` runs actual WebSocket scenarios:
- 3H,
- 4H,
- 2H+2AI,
- 3H+1AI.

Each checks:
- expected fixed human/AI slots,
- all-human READY + host START,
- synchronized run roster,
- Stage 1 -> Team Shop -> Stage 2,
- contiguous per-client event IDs,
- zero `event-gap`.

4H additionally checks:
- host reconnect returns to slot 1 with host identity and same run,
- total delivered events exceed the legacy 24-event window.

## Immediate validation gate
Do not implement N3 or Stage 4 yet.

First run:
- `/v038-validation-suite.html`

It must pass:
1. v0.36/v0.37 deterministic server regression,
2. v0.38 event-kernel deterministic tests,
3. v0.36 client regression,
4. v0.37 client regression,
5. v0.38 event-client self-test,
6. 3H / 4H / 2H+2AI / 3H+1AI live simulation.

If automation passes:
- perform one short Samsung Browser render/input smoke only,
- then freeze Slice C PASS checkpoint.

## Next bounded slice after Slice C PASS — N3 authority
Implement the now-frozen Option B contract server-authoritatively.

Required tests:
- forced combo 5/10/20/30/40 for all five classes,
- exact budget allocation,
- target geometry,
- no EXP/charge/combo/crit/recursive proc,
- kill/coin/contribution attribution,
- boss scalar behavior,
- four-player synchronized milestone burst stress,
- final Samsung Browser presentation smoke.

Only after the N3 authority slice closes should Stage 4 SHIELD begin.

## Later
- Stage 4 SHIELD / armor,
- Stage 5–6 checkpoint boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed-roster stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority with forced-level deterministic tests before natural progression depends on them.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains intentionally deferred. Handle later as a shared responsive-safety layer, not per-device patches.

## Frozen governance
No unapproved numerical change. Numerical work continues to follow:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
