# Timing Defense — Render Monthly Quota Outage

Date: 2026-10-20 KST

## Incident
The v0.35 source and both Render deploys completed successfully around 12:21 UTC.

At 12:39:35–12:39:37 UTC Render suspended the multiplayer backend, Timing Defense static site, and the workspace's other Render services.

Observed Render event on the affected services:
- `service_suspended`
- `suspender_added`
- actor/reason: `Monthly Quota Exceeded`
- service state: `suspended`
- suspenders: `billing`

Therefore the reported `v035.html` link failure is an infrastructure quota outage, not evidence of a v0.35 loader or gameplay-code regression.

## Important inference
The suspension affected both web services and static sites across the workspace at essentially the same time. The Render event API does not identify the exact monthly bucket. This is consistent with a workspace-level included-usage/billing limit. Render documentation states that exhausted free usage can suspend services for the remainder of the current monthly period when no billable overage is allowed.

Do not attempt repeated redeploys as a fix. A successful build artifact cannot serve while the workspace is suspended by billing/quota enforcement.

## Stable code boundary
- v0.34 remains the latest device-validated gameplay/network baseline.
- v0.35 source exists and had successful Render deploys before the quota suspension, but device validation of its reconnect/shop/Stage 2 flow was interrupted by the outage.
- Treat v0.35 as implemented but infrastructure-blocked, not PASS.

## Portable-host recovery prep
Added to `timing-defense-live-v011`:
- `timing-defense-server/portable.js`
- `timing-defense-v011/v035-host-adapter.js`
- `timing-defense-v011/v035-portable.html`

`portable.js` runs the existing authoritative server unchanged on an internal localhost port, proxies `/api/*` and `/health` including SSE streaming, and serves the Timing Defense static client from the same public origin.

The host adapter rewrites the hard-coded legacy Render multiplayer origin to the current origin on non-Render full-stack hosts. On the original Render static hostname it preserves the existing separate-backend behavior.

Local smoke validation completed:
- Node syntax PASS
- `/health` 200 PASS
- `/` static loader 200 PASS
- host adapter 200 PASS
- room creation API PASS

No gameplay coefficients, combo behavior, timing judgments, monster HP, passive values, or class balance values were changed by this recovery preparation.

## Next boundary
1. Connect an alternative persistent Node hosting provider.
2. Deploy branch `timing-defense-live-v011` with start command `node timing-defense-server/portable.js`.
3. Verify public root page and `/health`.
4. Re-run Android + PC room/READY/START smoke test.
5. Re-run v0.35 Stage 1 -> TEAM SHOP -> READY -> Stage 2 validation.
6. Test reconnect recovery.
7. Only after those pass, continue Stage 3–10 authority expansion.

## Render follow-up
When Render usage resets or the workspace billing policy changes, the original services can be reconsidered. Before relying on Render again, review `Billing -> Monthly Included Usage` and reduce unused simultaneous free web services / bandwidth consumption where appropriate.
