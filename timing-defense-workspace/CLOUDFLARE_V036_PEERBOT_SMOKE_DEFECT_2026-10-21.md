# v0.36 single-device peerbot smoke defect — 2026-10-21

Observed on Samsung Browser single-device smoke:
- real local participant remained HOST / ROGUE in authoritative room state,
- SIM-PC joined as human slot 2 / ARCHER,
- client debug/local presentation switched to GUEST / ARCHER,
- fixed bottom overlays covered READY / START / NEXT controls.

Root cause:
- v033 Cloudflare bridge wraps every `/ws/` WebSocket and treats each welcome as the primary local socket/session/slot.
- the first peerbot implementation used `window.WebSocket`, so the synthetic second-human socket was also intercepted and overwrote the primary bridge identity.
- debug controls dynamically read `bridge.slot || mp.slot`, so after the overwrite they targeted SIM-PC instead of the real local human.
- peerbot/debug test overlays were fixed to bottom corners regardless of lobby/shop CTA placement.

Classification:
- test-harness defect only; not evidence of a Durable Object multiplayer authority regression.
- previous cf.3 SERVER 10/10 / CLIENT 4/4 / MULTICLIENT 9/9 / FINAL PASS remains valid for its automated scope.

Correction:
1. peerbot now constructs the synthetic peer with the native WebSocket constructor recovered from the already-open primary native socket, bypassing the v033 wrapper.
2. peerbot can no longer mutate `bridge.socket`, `bridge.session`, or `bridge.slot`.
3. debug controls capture and pin the primary local session/slot and explicitly send that slot to the debug-level endpoint.
4. debug controls are hidden outside starting/intro/combat and moved to the right-center edge.
5. peerbot status badge is hidden outside combat and reduced to a small top-center indicator.
6. corrected smoke loader cache generation: `cf0365`.

Revalidation target:
- one Samsung Browser only,
- local remains HOST / chosen local class,
- SIM-PC remains a separate second human,
- lobby/shop CTA controls unobstructed,
- during combat set local LV6 and perform several timing attacks,
- no obvious duplicate projectile, flicker, or visual corruption.
