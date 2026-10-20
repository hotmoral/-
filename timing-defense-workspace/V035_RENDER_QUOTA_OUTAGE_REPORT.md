# Timing Defense v0.35 — Render quota outage / hosting recovery report

Updated: 2026-10-20 KST

## Incident
v0.35 code and both Render deployments completed successfully around 12:21 UTC, but the public link later became unreachable.

Render service events identify the cause exactly:
- multiplayer backend `srv-dbbimre1egvs73861d80`: `service_suspended` at 2026-10-20T12:39:35Z
- static game site `srv-dbb1c9mi0phs73b5bao0`: `service_suspended` at 2026-10-20T12:39:36Z
- suspension actor/reason for both: `Monthly Quota Exceeded`

This was not a v0.35 JavaScript/server crash. Both v0.35 builds/deploys had succeeded before the quota suspension.

## Consequence
The Render URLs are currently not a valid test surface. v0.35 must remain **device-unvalidated** until it is hosted again.

Stable gameplay evidence remains:
- v0.34 Android + PC shared combat: PASS
- v0.34 movement smoothing: PASS
- v0.34 remote projectile VFX: PASS

## Recovery preparation
The live branch now includes portable-host preparation so the same game can be moved to a single full-stack Node host without hard dependency on the Render static-site + Render backend split:
- `timing-defense-v011/v035-host-adapter.js`
- `timing-defense-v011/v035-portable.html`
- `timing-defense-server/portable-host.js`

`portable-host.js` serves the game files and proxies `/health` and `/api/*` to the existing authoritative Node server running as a child process. The host adapter reroutes the legacy hard-coded Render backend URLs to the current origin when deployed outside the old Render static hostname.

Local checks completed:
- Node syntax checks pass for the portable wrapper/adapter.
- local `/health` proxy returns the v0.35 backend health response.
- portable root/static asset routing returns HTTP 200.

## Truth boundary
Do not describe the Render outage as a v0.35 gameplay regression.
Do not claim v0.35 device PASS until a replacement host is live and Android + PC tests complete Stage 1 -> shop -> Stage 2 and reconnect checks.

## Next action
Connect/deploy to a replacement full-stack host, then run the existing v0.35 device validation plan. No numerical balance changes are required for this incident.
