# Timing Defense — Cloudflare v0.34 Render Parity Candidate

Updated: 2026-10-21 KST

## Status
Implementation and deployment trigger prepared. **Device validation pending.**

## Preserved baseline
- v0.33 Cloudflare authoritative Stage 1 device PASS checkpoint: `timing-defense-cloudflare-v033-pass-20261021`
- validated v0.33 deployment pointer HEAD: `dd35771a198355b0d7ff2a99e88b8e32b1c0df37`

## Candidate
- implementation branch: `timing-defense-cloudflare-v034-render`
- implementation commit: `c78765b2c29b1ab0812e64c6de7a8ca3b379c2cc`
- Cloudflare watched deployment branch trigger HEAD: `adc6709d51e9b076498c7c26e172478d24d9f797`

## Scope
Presentation only. Server/DO combat authority is unchanged.

Added:
- monster object reconciliation by authoritative monster id,
- smooth pursuit of time-derived authoritative target position,
- snap on large discontinuity,
- remote human projectile VFX synthesized from authoritative hit events,
- AI/passive projectile VFX synthesized from authoritative events,
- local projectile-arrival impact flash/particles immediately for responsiveness,
- local predicted presentation does not mutate monster HP or progression,
- server-confirmed local hit suppresses duplicate flash/particle while still applying authoritative damage/progression state.

## Explicit non-goals
No change to:
- damage values,
- monster HP,
- spawn count/gap,
- passive damage/interval,
- AI combat rules,
- EXP / charge / combo / coin authority,
- room / READY / START authority,
- Team Shop,
- Stage 2.

## Device gate
Android + PC must verify:
1. v0.33 shared HP / BASE HP / EXP / charge / clear remain identical,
2. Android monster motion is smooth and has no large jitter/regression,
3. remote human projectiles are visible,
4. AI/passive presentation remains visual-only and does not duplicate damage,
5. local projectile impact visually reacts at arrival without the previous extra perceived delay,
6. no double flash / double damage number from predicted + confirmed local hit,
7. no duplicate damage from any presentation projectile,
8. waiting-room / READY / START behavior does not regress.

PASS authorizes only the v0.35 reconnect / Team Shop / Stage 2 parity migration.
