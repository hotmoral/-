# Timing Defense — Cloudflare v0.31/v0.32 parity validation progress

Updated: 2026-10-21 KST

Public URL:
- https://timing-defense-do-poc.sktjsek.workers.dev

Deployment pointer branch:
- timing-defense-cloudflare-do-poc

Parity implementation branch:
- timing-defense-cloudflare-v031-parity

## Device evidence observed
Android Samsung Browser + independent PC client:
- actual Timing Defense lobby UI loads from Cloudflare,
- FRIEND waiting room creates authoritative room,
- room code RABEE2 observed,
- P1 host and selected KNIGHT identity visible,
- AI FILL preserved at P2 as MAGE,
- independent remote P3 joined as ROGUE,
- both human READY states propagated,
- host START became enabled only after both humans READY,
- START transitioned shared room through authoritative start gate,
- Android showed `RUN GATE OPEN` and `동기 시작 게이트를 통과했습니다.`,
- Samsung Browser short-landscape waiting-room content remained visible without the prior lower-content clipping.

## Current PASS subset
PASS:
- FRIEND create/join,
- participant nickname/class/slot propagation,
- AI FILL slot preservation,
- host identity,
- READY propagation,
- all-human READY gate,
- host START path,
- authoritative shared start gate,
- v0.32 short-landscape layout regression check.

Still required before closing the parity slice:
1. READY cancel propagation,
2. non-host START prohibition,
3. refresh/reconnect while still in WAITING preserves same room/session/slot,
4. disconnect/reconnect does not corrupt host/online ownership.

Stage 1 combat remains intentionally out of scope until this parity slice closes.
