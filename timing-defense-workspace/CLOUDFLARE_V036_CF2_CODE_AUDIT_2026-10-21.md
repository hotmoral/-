# Timing Defense — Cloudflare v0.36 cf.2 Code/Authority Audit

Date: 2026-10-21 KST
Status: **CODE AUDIT FIXES DEPLOY-TRIGGERED / DEVICE SMOKE ONLY REMAINS**

## Why this audit was run
The Slice A validation plan initially asked the user to visually verify N1/N2 and every Lv6 class effect on a real device. That is unnecessarily manual for deterministic server rules. Numerical/server-authority behavior should be verified primarily by code/contract tests; real-device validation should be reserved for browser/network/presentation integration.

## Server/contract findings retained as code-verifiable
- N1 exact timing EXP table is explicit in `v036-entry.js`.
- N2 AI stage multiplier is explicit: `1 + (stage-1)*0.035` and is applied only to authoritative AI damage.
- Knight Lv6 server damage = legacy additive +12% component.
- Rogue Lv6 second dagger = 55%, scheduled +55 ms, same-target allowed with nearest fallback.
- Tank Lv6 server knockback = base authoritative knockback ×1.30.
- Archer Lv6 = up to two strict-line 52% authoritative secondary hits.
- Mage Lv6 = up to three 50% authoritative nearby splash hits.
- secondary hits carry `actionId`, `hitIndex`, `skillKind` metadata.

## Code audit defects found before device acceptance

### CF2-A — Rogue local secondary could transiently mutate client state
Legacy v0.16 creates Rogue's Lv6 second dagger as a local `owner:'skill'` projectile. Under the Cloudflare network update loop that projectile could still reach legacy `v016ResolveSkillHit()` and `visualImpact()`, transiently modifying local monster HP/kill/coin presentation before the authoritative server snapshot corrected it.

This did not give the client server authority, but it violated the intended prediction contract and could cause visual double/flicker states.

Fix:
- in network mode, remove only the newly-created legacy Rogue secondary projectile after local launch,
- keep the primary local prediction,
- render Rogue secondary from the authoritative server `skill` event for local and remote clients.

### CF2-B — New secondary-VFX layer did not inherit v0.35 reconnect event floor
v0.35 resume correctly restores `mp.lastEvent` from the server `eventFloor` and returns an empty historical event list. The new v0.36 secondary-VFX layer originally maintained an independent floor and could therefore replay old skill VFX on the next normal state snapshot after reconnect.

Fix:
- detect `source === 'v035-resume'`,
- adopt the restored `mp.lastEvent` floor,
- clear pending secondary visuals when run identity changes,
- do not process historical secondary events after resume.

## cf.2 deployment marker
Expected health:
- `version: 0.36-cf.2`
- `fix: rogue-local-secondary-mutation-blocked-secondary-vfx-event-floor`

Watched deployment branch after trigger:
- `timing-defense-cloudflare-do-poc`
- HEAD `e93d93934eceb5e3000a97183505af257b9faa77`

Cache-busted client generation:
- `cf0363`

## Revised validation burden
Do NOT require the user to manually eyeball every N1/N2/Lv6 numerical value.

Code/contract acceptance covers deterministic server values and ownership.

Final real-device smoke should be short and cover only integration that code inspection cannot fully prove:
1. two clients can still join/start,
2. one Lv6 secondary effect is visibly delivered without duplicate/flicker,
3. basic Stage 1 -> shop -> Stage 2 transition still works,
4. if reconnect is exercised, no historical secondary-VFX burst appears.

A full five-class visual matrix is not required unless the code/contract audit or smoke test exposes a class-specific presentation defect.

## N3
N3 combo-milestone extra attacks remain deferred and mandatory for explicit later discussion. This audit does not implement, remove, freeze or rebalance N3.
