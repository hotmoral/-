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
8. v0.38 Slice C automated server/client/larger-party validation — **PASS**

Exact v0.38 automation checkpoint:
- branch `timing-defense-cloudflare-v038-automation-pass-20261022`
- HEAD `1afb125c86fc5c085c6b1246dec77b36a1d30159`

## N3 product decision — APPROVED / FROZEN CONTRACT
Option B is approved.

Frozen N3 contract:
- triggers at 5 / 10 / 20 / 30 and every +10 after 30,
- exact theoretical max raw-equivalent budgets 60 / 90 / 150 / 210,
- preserve class-specific burst geometry,
- deterministic remainder-safe allocation,
- no EXP / charge / combo increment / crit / recursive skill proc / recursive N3,
- normal damage/kills/kill-coin/contribution attribution,
- armor and frozen boss scalars remain applicable,
- N3 generic knockback uses NORMAL-equivalent semantics rather than accidental milestone-tier escalation,
- Tank retains its normal class knockback identity.

N3 is approved but **not yet enabled in combat**. Slice C full closure comes first.

## v0.38 Slice C automation — PASS
The corrected cf.3 validation suite passed:
- SERVER 28/28,
- v0.36 client regression,
- v0.37 client regression,
- v0.38 event client,
- larger-party simulation,
- FINAL PASS.

Automated larger-party coverage:
- 3H,
- 4H,
- 2H+2AI,
- 3H+1AI,
- fixed slots,
- host identity and reconnect,
- READY/START,
- synchronized Stage 1,
- Team Shop,
- Stage 2 entry,
- monotonic event IDs,
- no unexpected gap,
- >24 events delivered without silent loss.

Current event kernel:
- 512 retained authoritative events,
- per-WebSocket event cursor/run ID,
- monotonic event batches,
- explicit event-gap rather than silent loss,
- reconnect historical-event suppression preserved.

## Immediate next step — one 4H Samsung Browser smoke
Do not repeat numerical or network correctness tests manually.

Current watched smoke-candidate HEAD:
`cbcddf35443ff901b4a30dd6621da5a984335fb5`

Single-device harness:
- query `partybot=3`,
- local phone remains the real player/host,
- three simulated HUMAN peers join through native WebSockets,
- peer classes: ARCHER / MAGE / TANK,
- peers auto READY,
- peers issue normal timing action packets during combat,
- peers auto READY in Team Shop,
- smoke badge appears only during combat.

Manual smoke acceptance:
1. waiting room visibly contains local host + `SIM-A` + `SIM-M` + `SIM-T`,
2. local READY/START controls are usable and not obscured,
3. combat starts and remote-human attacks render without obvious flicker/event burst/canvas corruption,
4. local timing input remains usable,
5. Stage 1 clear enters Team Shop with all four humans visible,
6. simulated peers become READY while local controls remain usable,
7. host NEXT enters Stage 2.

If this passes:
- preserve a v0.38 Slice C full-PASS branch at the exact smoke HEAD,
- write Slice C PASS report,
- synchronize PROJECT_STATUS / NEXT_WORK / SESSION_HANDOFF,
- begin dedicated N3 authority slice.

## Following slice — N3 authority
After Slice C full PASS:
- forced combo 5 / 10 / 20 / 30 / 40 tests for all five classes,
- exact total budget assertions,
- class target-geometry assertions,
- no EXP/charge/combo/crit/recursive-proc assertions,
- normal kill/coin/contribution assertions,
- boss scalar assertions,
- four-player synchronized milestone stress,
- one final Samsung Browser presentation smoke.

Then:
- Stage 4 SHIELD / armor,
- Stage 5–6 boss + FLYER + authoritative Y geometry,
- Stage 7–9 mixed-roster stress,
- Stage 10 final boss/result,
- Lv11/16/21 authority.

## Deferred UX
Responsive safety across heterogeneous phone sizes/aspect ratios remains deferred. Handle later as a shared responsive-safety layer, not device-specific patches.

## Frozen governance
No unapproved numerical change. Continue:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> patch/freeze`.
