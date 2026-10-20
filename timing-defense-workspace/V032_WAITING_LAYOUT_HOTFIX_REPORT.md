# Timing Defense v0.32 — Waiting Room Layout Hotfix

Updated: 2026-10-20 KST

## Scope
Device validation of v0.31 on Samsung Browser showed that FRIEND and LINK waiting rooms were functionally connected to the real multiplayer backend, but the left information panel clipped its lower content on short landscape viewports.

Observed symptom:
- room creation/connection worked,
- participant slots were visible,
- the lower READY / INVITE or COPY LINK / link-status area was partially or fully hidden,
- RANDOM did not show the same clipping because its left-side content is shorter.

## Root cause
The generated invite URL was rendered as normal wrapping text inside a fixed-height panel. On the target Android landscape viewport the long URL consumed several extra lines. The inherited waiting-panel rule used `overflow:hidden`, so the lower actions/status/link content was clipped.

## v0.32 fix
Files:
- `timing-defense-v011/v032-waiting-layout.js`
- `timing-defense-v011/v032.html`

Changes:
- FRIEND/LINK invite URL is constrained to one line with ellipsis,
- READY / INVITE / COPY LINK action row receives guaranteed vertical space,
- local-player card and informational spacing are compacted,
- short-height landscape media rules apply an additional compact layout,
- footer height is explicitly reserved,
- RANDOM networking flow is unchanged.

## Non-goals / guards
No changes to:
- room authority,
- room code generation,
- SSE transport,
- READY semantics,
- host START gate,
- RANDOM matching logic,
- combat,
- combo display/logic,
- numerical balance.

## Deployment
- Public version: `v0.32`
- URL: `https://timing-defense-v011.onrender.com/v032.html`
- Live source HEAD: `16b602221caf1d19c062e17363ac786d2bd20d18`
- Static Render deploy: `dep-dbbivgjrjlhs73ee5bm0` / LIVE
- Multiplayer backend remains: `https://timing-defense-mp.onrender.com`
- Backend deploy remains: `dep-dbbims61egvs73861f10` / LIVE

## Next validation
On the same Samsung Browser landscape device:
1. FRIEND waiting room: confirm READY + INVITE + lower link/status content are visible without scrolling or clipping.
2. LINK waiting room: confirm READY + COPY LINK + lower link/status content are visible without clipping.
3. Recheck participant slots and READY propagation with two independent clients.
4. Recheck RANDOM pairing.
5. If clean, proceed to synchronized combat/run-state implementation.