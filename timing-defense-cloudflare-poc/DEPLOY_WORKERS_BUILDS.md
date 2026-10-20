# Timing Defense Cloudflare DO PoC — Workers Builds deployment

This PoC is intentionally deployed through Cloudflare Workers Builds / GitHub integration rather than GitHub Actions.

## Fixed source
- Repository: `hotmoral/-`
- Branch: `timing-defense-cloudflare-do-poc`
- Root directory: `timing-defense-cloudflare-poc`
- Worker name: `timing-defense-do-poc`
- Wrangler config: `wrangler.jsonc`
- Deploy command: `npx wrangler deploy`

## Why this route
- Does not consume private-repository GitHub Actions minutes.
- Cloudflare Workers Builds can create/manage its own deployment API token after account authorization.
- Keeps credentials out of the repository.
- Every room is a SQLite-backed Durable Object and the client/room transport uses WebSocket Hibernation.

## One-time Cloudflare account connection
1. Cloudflare Dashboard -> Workers & Pages -> Create application.
2. Choose GitHub as the repository source and authorize the Cloudflare Workers & Pages GitHub App for repository `hotmoral/-`.
3. Select repository `hotmoral/-`.
4. Select production branch `timing-defense-cloudflare-do-poc`.
5. Set Root directory to `timing-defense-cloudflare-poc`.
6. The Worker/project name must be exactly `timing-defense-do-poc` to match `wrangler.jsonc`.
7. Leave Build command empty unless the dashboard requires one.
8. Deploy command: `npx wrangler deploy`.
9. Save and Deploy.

Do not paste a Cloudflare API token into GitHub source files or commit one to this repository.

## First public smoke test
After deployment, keep the generated `*.workers.dev` URL and verify in this order:
1. `GET /api/health` -> HTTP 200 and `service=timing-defense-do-poc`.
2. Root `/` loads the dedicated PoC UI.
3. Device A creates a room.
4. Device B opens the invite URL / enters the same six-character code.
5. Both players appear ONLINE.
6. READY on A propagates to B and READY on B propagates to A.
7. START is enabled only for the host after both are READY.
8. START creates one authoritative test monster with HP 300 on both clients.
9. Attack from A changes HP 300 -> 200 on both clients.
10. Attack from B changes HP 200 -> 100 on both clients.
11. Refresh one client and confirm the same session/slot/state resumes and the next attack sequence is accepted.

## PASS boundary
The Cloudflare architecture PoC is PASS only if two independent clients complete the full smoke test above on the same public deployment.

A PASS does not mean v0.35 has been migrated. It only authorizes the next migration slice: existing v0.31 room/READY/START semantics onto the Durable Object transport.

## Frozen guards
- Do not merge this PoC into `timing-defense-live-v011` before the public two-client PASS.
- Do not change combat balance values as part of this migration.
- Do not change the approved combo UI/animation.
- Preserve `timing-defense-live-v011` as the v0.35 source baseline until the migration lane independently reaches parity.
