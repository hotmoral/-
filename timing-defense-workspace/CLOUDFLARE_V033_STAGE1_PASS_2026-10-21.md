# Timing Defense — Cloudflare v0.33 Stage 1 Parity PASS

Updated: 2026-10-21 KST

## Result
Cloudflare Durable Objects authoritative Stage 1 parity is **public Android + PC device PASS**.

Validated on the real game flow after the already-PASS v0.31/v0.32 room/READY/START gate.

## Device-validated properties
- same Stage 1 run entered on both clients,
- same authoritative monster identities / HP trend,
- cross-device human attacks affect the same monster state,
- BASE HP remains identical on both clients,
- EXP / charge remain identical on both clients,
- Stage 1 clear is shared,
- no duplicate client-authoritative enemy spawning observed,
- no duplicate local wall-damage authority observed,
- v0.31/v0.32 waiting-room behavior remained usable.

## Architecture
The Cloudflare lane does not recreate the old always-on 50 ms server loop. Durable Object authority advances from timestamps / scheduled events / alarms, while clients render the world from authoritative state.

## Presentation defects separated from authority parity
Device video review found two presentation issues that do **not** invalidate authoritative Stage 1 parity:
1. remote human projectile not visible,
2. local projectile reaches the monster before server-confirmed hit presentation appears, creating a small perceived delay.

These belong to the next v0.34 presentation slice.

## Frozen numerical behavior
No combat/balance value was intentionally changed during the migration. Stage 1 keeps the recovered v0.33 contract, including GRUNT count/gap, current ordinary-monster +10% experiment, passive 40/2s candidate, existing judgment damage/EXP/combo/charge rules, AI timing and wall damage.

## Preserved checkpoint
- branch: `timing-defense-cloudflare-v033-pass-20261021`
- validated deployment pointer HEAD: `dd35771a198355b0d7ff2a99e88b8e32b1c0df37`

## Authorized next slice
Only v0.34 presentation parity is authorized next:
- monster object reconciliation by server id,
- render smoothing / time-derived extrapolation,
- remote human / AI / passive projectile VFX from authoritative events,
- immediate local presentation-only impact at projectile arrival,
- server authority remains the only source for HP / EXP / coin / kills / progression.
