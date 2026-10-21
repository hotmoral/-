# Timing Defense — Next Work Boundary

Updated: 2026-10-21 KST

## Closed migration gates
1. Cloudflare Durable Objects viability PoC — **PASS**
2. v0.31/v0.32 real-game waiting-room parity — **PASS**
3. v0.33 authoritative Stage 1 parity — **PASS**
4. v0.34 render smoothing / remote projectile parity — **PASS**

## Current v0.35 status
Cloudflare v0.35 is **DEVICE VALIDATION PARTIAL PASS**. Core flow is confirmed; only cf.7 visual parity remains.

Confirmed on device:
- Stage 1 -> shared Team Shop,
- authoritative shop purchase / coin / rank flow,
- immediate `처리중…` purchase feedback and duplicate-tap blocking,
- both-human shop READY,
- host NEXT STAGE,
- synchronized Stage 2 transition,
- `STAGE 2 / READY / START`,
- Timing Square and local tap input,
- remote projectile visibility,
- Stage 2 bounded clear,
- authoritative result board with actual human/AI participants and populated KILLS / DMG / KILL COIN / LV / MAX COMBO,
- reconnect validation — PASS.

## cf.7 deployed candidate
Cloudflare watched branch:
- `timing-defense-cloudflare-do-poc`
- HEAD `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- expected health version `0.35-cf.7`

Bounded cf.7 fixes only:
1. Remove Rogue Timing Square Knight/yellow palette leakage caused by inherited v0.24 drawing wrapper.
2. Render remote **human timing attacks** with the same class/tier projectile family as local human timing attacks. Passive/automatic shots remain visually distinct.

No combat balance, economy values, Stage plan, damage authority, EXP, shop cost, knockback or reconnect semantics changed.

## Immediate device gate
A short two-human Stage 1 network test is sufficient.

Confirm only:
1. Rogue CHARGE dots/text/square no longer flash Knight/yellow or exhibit the reported color flicker.
2. A remote human timing attack has the same projectile visual family as the corresponding local human timing attack; it must no longer look like the passive/automatic shot.

Already closed — do not repeat unless regression is observed:
- shop pending UX,
- reconnect,
- Stage 2 transition/input,
- Stage 2 clear/result board.

## Closure rule
If both cf.7 checks pass:
1. mark Cloudflare v0.35 full device PASS,
2. preserve exact validated deployment HEAD as a v0.35 PASS checkpoint branch,
3. write the v0.35 PASS report,
4. sync `PROJECT_STATUS.md`, `NEXT_WORK.md`, `SESSION_HANDOFF.md`,
5. only then open the next migration slice (Stage 3–10 / larger-party / Lv6+ multiplayer authority as separately scoped work).

## Deferred item
Responsive safety across heterogeneous phone screen sizes/aspect ratios is intentionally deferred until the current v0.35 closure is complete. It should be reviewed later as a shared responsive-safety layer rather than per-device patches.

## Frozen governance
No numerical change to attack damage, monster HP, passive interval, combo coefficients, EXP, shop cost, knockback, stage count/gap or class balance without the established measure/report/discuss/explicit-decision workflow.
