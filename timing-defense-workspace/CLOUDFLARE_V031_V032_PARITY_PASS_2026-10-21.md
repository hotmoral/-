# Timing Defense — Cloudflare v0.31/v0.32 Parity PASS

Updated: 2026-10-21 KST

## Status
**PASS — public Android + PC device validation complete.**

This closes the first production-parity migration slice on Cloudflare Workers + Durable Objects.

## Deployment / branches
- Public URL: `https://timing-defense-do-poc.sktjsek.workers.dev`
- Cloudflare-tracked deployment branch: `timing-defense-cloudflare-do-poc`
- Deployment pointer HEAD used for the parity build: `e6db85f22f04b2566960c98867c19cebf8fc1a4b`
- Dedicated implementation branch: `timing-defense-cloudflare-v031-parity`
- Preserved PoC PASS checkpoint branch: `timing-defense-cloudflare-do-poc-pass-20261021`

## Scope migrated
Only the v0.31/v0.32 waiting-room/session contract was migrated.

Durable Object / WebSocket authority now owns:
- room identity,
- session identity,
- slot allocation,
- host identity,
- participant nickname/class,
- AI FILL reservation,
- READY state,
- all-human READY gate,
- host-only START,
- shared future `startAt`,
- synchronized starting/running boundary.

Client keeps the existing production waiting-room presentation and v0.32 Samsung Browser layout fixes.

Stage 1 combat is deliberately not part of this slice.

## Public device validation evidence
Validated with Android Samsung Browser + independent PC client:
1. actual Timing Defense lobby loads from the Cloudflare public URL,
2. FRIEND room creation succeeds with a six-character room code,
3. invite URL joins the same room from the second device,
4. nickname/class/slot state is identical across both clients,
5. AI FILL reservation remains authoritative and human joins take the next valid slot,
6. READY propagates both directions,
7. READY cancel propagates,
8. host START remains disabled until all human participants are READY,
9. non-host START remains unavailable,
10. when all humans are READY, host START becomes enabled,
11. START produces one shared authoritative future start gate,
12. both clients reach the same `RUN GATE OPEN` / running boundary,
13. WAITING-state refresh reconnects to the same room/session/slot,
14. host refresh preserves host ownership,
15. the other client stays in the same room and remains online,
16. room code and participant slots remain unchanged after reconnect,
17. Samsung Browser short-landscape waiting-room UI remains usable with READY / INVITE / link / slots / START visible without the v0.31 clipping regression.

## Architecture result
The Cloudflare Durable Object + WebSocket implementation now has device-validated parity for the existing v0.31/v0.32 multiplayer waiting-room contract.

This is stronger than the isolated PoC result because the real game lobby/waiting-room UI and production semantics are now running on the Cloudflare architecture.

## Truth boundary
Safe claims after this PASS:
- Cloudflare v0.31/v0.32 waiting-room parity is device-PASS.
- Existing FRIEND/LINK, slot, class, nickname, READY, host START and future start-gate semantics are preserved.
- v0.32 Samsung Browser layout fix is preserved.
- Waiting-room refresh/reconnect preserves the same session/slot/room/host ownership in the tested path.

Do not claim yet:
- Cloudflare v0.33 Stage 1 combat parity,
- Cloudflare v0.34 smoothing/projectile parity,
- Cloudflare v0.35 reconnect/shop/Stage 2 parity,
- Stage 3–10 multiplayer,
- final persistence/security/balance semantics.

## Authorized next slice
Proceed only to **v0.33 authoritative Stage 1 migration**.

Required next server-owned consequences:
- shared run id / seed / start state,
- Stage 1 spawn identity and schedule,
- authoritative monster HP/death,
- BASE HP,
- human timing-result actions,
- passive / AI consequences,
- EXP / LV / coin / charge / combo candidate state.

Architecture constraint:
- do not recreate the legacy always-on 50 ms position integration unless measurements prove it necessary,
- prefer event/time-derived authoritative movement state where safe,
- preserve v0.34 interpolation/extrapolation and remote projectile behavior later as presentation-only layers,
- no numerical balance changes during this migration slice.
