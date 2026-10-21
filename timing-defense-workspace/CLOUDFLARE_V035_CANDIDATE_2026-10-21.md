# Cloudflare v0.35 Parity Candidate — 2026-10-21

## Status
**SUPERSEDED BY DEVICE PASS / CLOSED**

This document records the initial v0.35 migration candidate and its early partial validation. The candidate subsequently advanced through cf.3-cf.7 defect closure and received full Android + PC device validation.

Canonical closure record:
- `CLOUDFLARE_V035_PASS_2026-10-21.md`

Exact validated deployment:
- public URL: `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- health version: `0.35-cf.7`
- preserved PASS branch: `timing-defense-cloudflare-v035-pass-20261021`

## Original bounded migration scope
The v0.35 lane ported:
- same-session/reload recovery from Durable Object state,
- event-floor recovery to suppress historical projectile replay,
- Stage 1 -> Team Shop,
- Stage 1 reward `55 + stage*12` (67 after Stage 1),
- server-owned per-human coin/ranks/purchases,
- READY purchase lock/unlock,
- all-human shop READY gate,
- host-only NEXT STAGE,
- synchronized future Stage 2 start,
- Stage 2 authoritative GRUNT/RUNNER combat,
- Stage 2 count 10 / gap 1040 ms / 62% GRUNT 38% RUNNER,
- existing Stage 2 HP scaling and +10% ordinary non-boss experiment,
- shared WALL HP +100 and aggregate DEF prototype semantics,
- bounded Stage 2 clear,
- v0.34 render smoothing/projectile behavior retained.

## Important audit fixes made before/through device closure
- exact AI interval contract restored: Rogue 1150 ms, Tank 1650 ms, all other classes 1400 ms,
- Stage 2 `starting` room status / shared `startAt` restored,
- Stage 2 clear event/status grammar restored,
- duplicate reconnect WebSocket competition prevented,
- event-floor guard added for reconnect replay safety,
- public run stage hardcoding removed,
- Stage 2 intro/input path restored through existing stage-start flow,
- authoritative result-board data added,
- cumulative KILL COIN separated from current wallet balance,
- Team Shop pending feedback / duplicate-tap guard added,
- Rogue Timing Square Knight/yellow palette leakage removed,
- remote human timing-projectile rendering aligned with local human timing attacks.

## Final validation outcome
The remaining Stage 2 authority, result-board, reconnect, shop UX and visual-parity gates were subsequently device-confirmed PASS. No numerical balance values were intentionally changed during the closure work.

For current truth and next boundary, read:
- `CLOUDFLARE_V035_PASS_2026-10-21.md`
- `PROJECT_STATUS.md`
- `NEXT_WORK.md`
- `SESSION_HANDOFF.md`
