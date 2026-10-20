# Timing Defense — Next Work Boundary

Updated: 2026-10-20 KST

## Final handoff synchronization
- Final freeze checkpoint: `HANDOFF_FREEZE_2026-10-20_2334KST.md`
- This session is closed for implementation after synchronization.
- The next GPT must recover canonical GitHub state before executing anything.

## Current state
- Latest implemented prototype: **v0.35**
- Previous device-validated prototype: **v0.34**
- Old Render game URL: `https://timing-defense-v011.onrender.com/v035.html` — **SUSPENDED**
- Old Render backend: `https://timing-defense-mp.onrender.com` — **SUSPENDED**
- Suspension reason on both services: **Monthly Quota Exceeded**
- Last successful v0.35 static deploy: `dep-dbblp8s9v7es73flhq40`
- Last successful v0.35 backend deploy: `dep-dbblpauq1p3s73d1v2mg`
- Live portable-host preparation HEAD: `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a`

The old public URL being unreachable is a hosting outage, not evidence that v0.35 code failed.
Read `V035_RENDER_QUOTA_OUTAGE_REPORT.md` before execution.

## Balance governance
Do not production-freeze or numerically patch passive/combo/enemy HP/projectile speed from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# Immediate execution group — replacement hosting recovery

Do not begin Stage 3 or new gameplay work before this group closes.

## A. Verify canonical state
1. Read `HANDOFF_FREEZE_2026-10-20_2334KST.md`, `SESSION_HANDOFF.md`, `PROJECT_STATUS.md`, `V035_RENDER_QUOTA_OUTAGE_REPORT.md`.
2. Verify live branch HEAD and the portable-host files:
   - `timing-defense-v011/v035-host-adapter.js`
   - `timing-defense-v011/v035-portable.html`
   - `timing-defense-server/portable-host.js`
3. Do not recreate these files unless repository verification proves them incomplete.

## B. Replacement host deployment
Deploy the current v0.35 portable stack to a full-stack Node host.
Required runtime entry point:
- `node timing-defense-server/portable-host.js`

Expected public behavior:
- `/` serves `v035-portable.html`,
- frontend static assets resolve from the same origin,
- `/health` proxies to the authoritative backend,
- `/api/*` proxies to the authoritative backend,
- SSE room stream works through the same public origin.

Avoid introducing gameplay or balance changes while moving hosts.

## C. Host smoke test
Before device testing verify:
- root returns 200,
- required JS files return 200,
- `/health` returns backend v0.35 health,
- room create/join works,
- READY state propagates,
- SSE stream remains connected,
- START returns one shared run state.

## D. Android + PC v0.35 device validation
Use the pair that passed v0.34.

Validate in order:
1. join same room / READY / START,
2. shared Stage 1 combat,
3. Stage 1 -> Team Shop on both clients,
4. independent coin/rank purchases,
5. READY propagation,
6. host-only NEXT STAGE,
7. synchronized Stage 2 GRUNT/RUNNER combat,
8. same enemy HP/deaths/BASE HP,
9. v0.34 smoothing remains smooth,
10. remote projectiles remain visible without duplicate damage.

## E. Reconnect validation
Refresh one client in each state:
- Stage 1 combat,
- Team Shop,
- Stage 2 combat.

Expected:
- same room/session/slot/run restored within the current 180 s same-server grace,
- current authoritative snapshot restored,
- no historic projectile-event burst,
- other client remains in the same shared state.

Current limit:
- room/run data is in-memory,
- backend process restart is not recoverable yet.

## F. Closure rule
This recovery group closes only when:
- replacement public URL is reachable,
- API/SSE smoke tests pass,
- Android + PC v0.35 flow passes through Stage 2 and reconnect checks,
- any reproducible defects are fixed,
- canonical status/handoff docs are synchronized.

---

# Following implementation group — only after v0.35 device PASS
1. Generalize authoritative Stage 2 -> shop -> Stage 3 and common stage state machine through Stage 10.
2. Add remaining monster grammar: GRUNT / RUNNER / BRUTE / SHIELD / FLYER plus Stage 5/10 bosses.
3. Validate full-run shop/READY/NEXT with DUO / TRIPLE / FULL.
4. Move Lv6/Lv11/Lv16/Lv21 skill consequences under server authority.
5. Add stronger revision/desync diagnostics and reconciliation.
6. Decide durable room/run persistence and horizontal-scaling architecture.
7. After networking stabilizes, implement Lv26/Lv31.
8. Rerun Solo/2P/3P/4P simulations before numerical balance freeze.

Do not claim full Stage 1–10 multiplayer until independent clients complete the whole authoritative run.

---

# Current authority contract
Client owns:
- local Timing Square movement/input,
- captured X/Y judgment,
- visual interpolation/projectile rendering,
- shop UI intent only.

Server owns:
- room/session/slot/host,
- run id/seed/start times,
- Stage 1 and Stage 2 enemy spawn/id/position/HP,
- BASE HP,
- target/final tier/damage/knockback/kill,
- coin / EXP / LV / charge / combo candidate,
- passive/AI damage,
- shop coin/ranks/purchase validation,
- shop READY/NEXT gate,
- Stage 1 -> shop -> Stage 2 transition.

Current bounded multiplayer scope:
- Stage 1 + Team Shop + Stage 2,
- Stage 3–10 not yet networked,
- multiplayer Lv6+ skill authority incomplete,
- reconnect is same-server in-memory recovery only.

## Still unresolved / not production-frozen
- replacement long-term host,
- durable persistence / server-restart recovery,
- horizontal scaling,
- invite-link security/token policy,
- Stage 3–10 authority,
- final Team Shop/shared-wall ownership semantics,
- complete Lv6+ skill authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation,
- Lv26/Lv31 coefficients,
- final passive/HP/combo coefficients,
- final E/X pressure/tier values,
- final result metrics.
