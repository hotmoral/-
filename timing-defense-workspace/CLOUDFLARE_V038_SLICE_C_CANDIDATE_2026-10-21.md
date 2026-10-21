# Timing Defense — Cloudflare v0.38 Slice C Candidate

Date: 2026-10-21 KST  
Status: **IMPLEMENTED / WATCHED BRANCH TRIGGERED / LIVE AUTOMATION PENDING**

## Exact candidate
- implementation branch: `timing-defense-cloudflare-v038-slice-c-event-kernel`
- watched branch: `timing-defense-cloudflare-do-poc`
- candidate HEAD: `0c96f038f6fcf7ec5e27e7d7fe0db38343a807c7`
- expected health: `0.38-cf.1`
- loader cache generation: `cf0381`

## N3 decision prerequisite
N3 Option B is approved and frozen in:
- `N3_COMBO_MILESTONE_FROZEN_CONTRACT_2026-10-21.md`

N3 is still disabled in this candidate. Slice C hardens multiplayer delivery first.

## Event-kernel changes
- authoritative event history: 512 events,
- per-WebSocket `eventRunId` + `eventCursor` stored in hibernation attachment,
- event delivery uses monotonic `event-batch` messages,
- normal socket state snapshots no longer depend on the legacy public 24-event tail,
- retention discontinuity produces explicit `event-gap` rather than silent loss,
- reconnect/new socket in an already-running run floors at latest and retains the existing v0.35 resume/eventFloor semantics,
- socket that existed before a new run starts begins that run at event 0.

## Deterministic event tests
The v0.38 self-test checks:
- 512-history retention with monotonic IDs,
- a 32-event burst is delivered whole despite exceeding legacy 24,
- cursor advancement,
- explicit retention-gap detection,
- pre-run socket starts new run at event 0,
- reconnect socket floors at latest,
- independent cursors for multiple sockets.

## Larger-party live simulator
Scenarios:
- 3 humans,
- 4 humans,
- 2 humans + 2 AI,
- 3 humans + 1 AI.

Each scenario checks fixed slots, READY/START, synchronized run roster, Stage 1 -> Team Shop -> Stage 2, per-client monotonic event delivery, and no `event-gap`.

4H additionally checks:
- host reconnect keeps slot 1 / host identity / same run,
- delivered event count exceeds the old 24-event snapshot window.

## One-click validation
`/v038-validation-suite.html`

Runs:
1. v0.36/v0.37 server regression + v0.38 event-kernel deterministic tests,
2. v0.36 client regression,
3. v0.37 client regression,
4. v0.38 event-client self-test,
5. 3H / 4H / 2H+2AI / 3H+1AI real WebSocket simulation.

## Gate
Do not declare Slice C PASS until deployed suite reports `FINAL PASS` and one short Samsung Browser render/input smoke is completed.

Do not enable N3 or Stage 4 yet.