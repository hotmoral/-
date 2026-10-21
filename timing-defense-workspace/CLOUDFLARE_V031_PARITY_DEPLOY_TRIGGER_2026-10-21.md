# Cloudflare v0.31/v0.32 parity deployment trigger

Updated: 2026-10-21 KST

## Purpose
Deploy the audited v0.31/v0.32 waiting-room parity migration without requiring another manual Cloudflare dashboard branch change.

## Deployment routing decision
Cloudflare was already configured to watch GitHub branch:
- `timing-defense-cloudflare-do-poc`

Instead of asking the user to change the Cloudflare production-branch setting again, the GitHub deployment branch was converted into a deployment pointer and fast-forwarded to the parity implementation.

The successful PoC baseline was preserved before advancing the pointer:
- archive branch: `timing-defense-cloudflare-do-poc-pass-20261021`
- archived PoC PASS HEAD: `04ee9c2237089a5105fa4f829565f6f50ff248a8`

Parity implementation branch:
- `timing-defense-cloudflare-v031-parity`

Deployment trigger HEAD:
- `e6db85f22f04b2566960c98867c19cebf8fc1a4b`
- message: `Trigger Cloudflare v0.31 parity deployment`

Cloudflare-watched branch was fast-forwarded to the same HEAD:
- `timing-defense-cloudflare-do-poc` -> `e6db85f22f04b2566960c98867c19cebf8fc1a4b`

## Scope of deployed candidate
Included:
- real v0.32 game/lobby asset stack,
- Cloudflare Durable Object/WebSocket replacement for v0.31 FRIEND/LINK waiting-room networking,
- room/session/slot/host authority,
- nickname/class state,
- AI FILL occupancy,
- READY and READY cancel propagation,
- host-only START,
- shared authoritative `startAt = now + 2500 ms`,
- Durable Object alarm transition to `running`,
- waiting-state refresh/reconnect session recovery,
- v0.32 Samsung Browser short-landscape waiting-room CSS,
- static-asset `html_handling: none` to preserve legacy HTML-loader fetch behavior.

Explicitly excluded:
- Stage 1 combat migration,
- v0.33 combat authority,
- v0.34 smoothing/projectiles,
- v0.35 shop/Stage 2,
- RANDOM parity,
- numerical balance changes.

## Verification boundary
Source/deployment trigger is complete.
Public Cloudflare build and device parity remain verification gates until observed.
Do not claim Cloudflare v0.31/v0.32 parity PASS until Android + PC validation completes.
