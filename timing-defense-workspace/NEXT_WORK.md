# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Superseding architecture decision
The replacement always-on Node-host deployment lane is no longer the primary next action.

User-approved direction:
**Cloudflare Workers + Durable Objects PoC first.**

Read `CLOUDFLARE_DO_MIGRATION_DECISION_2026-10-21.md` before execution.

The existing portable Node host remains a fallback artifact only. Do not deploy it as the primary recovery path unless the Durable Objects PoC is rejected by evidence.

## Current state
- Latest implemented game prototype: **v0.35**.
- Last Android + PC device-PASS multiplayer baseline: **v0.34**.
- Render static/backend services remain suspended for **Monthly Quota Exceeded**.
- Live branch remains `timing-defense-live-v011` at `7ab0da2434d727ca5bcad35dd9ce75a436c3c78a` unless later verified otherwise.
- Experimental architecture branch: `timing-defense-cloudflare-do-poc`.
- Current PoC code is isolated under `timing-defense-cloudflare-poc/`.
- The PoC does not modify v0.35 gameplay or balance values.

## Balance / UI guard
Do not numerically patch or production-freeze attack damage, monster HP, passive interval, combo coefficients, EXP, shop costs, knockback, stage count/gaps or class balance during this architecture migration.

Required numerical workflow remains:
`implement/test -> measure -> classify -> report -> discuss -> explicit decision -> numerical patch/freeze`.

Current combo display/size/position/animation remains approved and frozen unless explicitly requested.

---

# Immediate execution group — Durable Objects viability PoC

Do not migrate the full v0.35 game yet.

## A. Isolated PoC contract
The first public build must prove only:
1. create one six-character authoritative room,
2. connect two independent browser clients,
3. synchronize participant/host state,
4. synchronize READY,
5. enforce host-only START,
6. create one authoritative test monster,
7. accept an attack from either client,
8. broadcast identical monster HP to both clients,
9. reconnect the same stored session without corrupting active connection ownership.

Diagnostic PoC constants are intentionally isolated and are not game-balance changes.

## B. Target platform contract
- Frontend/static assets: Cloudflare Workers Static Assets.
- Room authority: one SQLite-backed Durable Object per room code.
- Transport: WebSocket Hibernation API.
- Current Korea-centered placement hint: `apac-ne`.
- Execution model: event-driven.
- Do **not** reproduce the legacy 50 ms always-on Node simulation loop in the new architecture.

## C. Public PoC smoke test
After Cloudflare deployment verify:
- `/api/health` returns PoC architecture metadata,
- root diagnostic page loads,
- room create works,
- second client joins the same room,
- READY propagates both ways,
- non-host cannot START,
- host START works only after both humans READY,
- both clients see the same 300 HP diagnostic monster,
- an accepted attack changes 300 -> 200 on both clients,
- the other client can change 200 -> 100 on both clients,
- the next accepted attack changes 100 -> 0 and both clients enter `clear`.

## D. Device gate
Use Android + PC as two independent clients.

PASS requires the full public sequence:
`same room -> READY -> host START -> same monster -> A attack visible on B -> B attack visible on A -> clear`.

Also refresh/reconnect one client and confirm the same session/slot can recover without the replaced old WebSocket marking the new connection offline.

## E. Failure rule
If the PoC fails because of a Cloudflare platform constraint, stop and classify the constraint before porting production gameplay.

Do not work around a platform limitation by changing gameplay/balance behavior.

---

# Migration group — only after PoC PASS

1. Port the v0.31 authoritative room/session/READY/START contract to the Durable Object.
2. Preserve the client-side waiting-room UX and v0.32 short-landscape fixes.
3. Port v0.33 Stage 1 authoritative consequences: spawn identity, HP, BASE HP, actions, passive/AI consequences, EXP/LV/coin.
4. Replace continuous 50 ms server position integration with event/time-derived authoritative movement where safe.
5. Preserve v0.34 interpolation/extrapolation and remote projectile VFX as presentation-only behavior.
6. Port v0.35 session recovery, Team Shop, purchase validation, READY/NEXT and Stage 2.
7. Android + PC device-test through Stage 2 and reconnect.
8. Fix only reproducible parity defects.
9. Synchronize canonical docs when v0.35-equivalent Cloudflare parity is device-PASS.

---

# Following game implementation — only after Cloudflare v0.35 parity PASS

1. Generalize the authoritative stage/shop state machine through Stage 10.
2. Add GRUNT / RUNNER / BRUTE / SHIELD / FLYER plus Stage 5/10 bosses.
3. Validate DUO / TRIPLE / FULL room/shop/READY/NEXT behavior.
4. Move Lv6/Lv11/Lv16/Lv21 multiplayer skill consequences under server authority.
5. Strengthen revision/desync diagnostics and reconciliation.
6. Decide durable room lifetime, cleanup and invite-token policy.
7. Implement Lv26/Lv31 only after networking stabilizes.
8. Rerun Solo/2P/3P/4P simulations before numerical freeze.

## Current truth boundary
Safe claims:
- v0.34 Android + PC authoritative Stage 1 is device-PASS.
- v0.34 smoothing and remote projectile VFX are device-PASS.
- v0.35 reconnect/shop/Stage-2 code exists and passed local API/integration checks.
- Render outage is a hosting quota suspension, not proven gameplay regression.
- a separate Durable Objects PoC implementation now exists for architecture validation.

Do not claim:
- public Cloudflare PoC PASS before deployment/device evidence,
- v0.35 Cloudflare parity,
- Stage 3–10 multiplayer,
- complete Lv6+ multiplayer skill authority,
- final production persistence/security/balance semantics.
