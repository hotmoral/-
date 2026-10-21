# Cloudflare v0.35 parity — DEVICE PASS

Date: 2026-10-21 KST
Status: **PASS / CLOSED**

## Validated deployment
- public service: `https://timing-defense-do-poc.sktjsek.workers.dev`
- watched branch: `timing-defense-cloudflare-do-poc`
- exact device-validated deployment HEAD: `b8cb477b47bb8a38f6ab06452c5a9cf0bf26d69d`
- health version: `0.35-cf.7`
- preserved PASS checkpoint: `timing-defense-cloudflare-v035-pass-20261021`

## Device validation evidence
Android + PC multiplayer validation closed the v0.35 migration slice.

Confirmed:
- Stage 1 authoritative multiplayer remains synchronized.
- Stage 1 -> shared Team Shop transition works.
- authoritative coin / upgrade rank / purchase flow works.
- purchase buttons immediately show `처리중…` while retaining server-confirmed economy authority and blocking duplicate taps.
- both-human shop READY gate works.
- host-only NEXT STAGE works.
- synchronized Stage 2 transition works.
- `STAGE 2 / READY / START` presentation works.
- Timing Square and direct timing input are active in Stage 2.
- authoritative Stage 2 GRUNT/RUNNER combat reaches bounded clear.
- remote human projectiles are visible.
- local hit presentation remains immediate without duplicating gameplay authority.
- Stage 2 result board shows the actual run participants and populated authoritative KILLS / DMG / KILL COIN / LV / MAX COMBO values.
- required reconnect gate was user-confirmed PASS.
- cf.7 Rogue CHARGE visual no longer leaks the inherited Knight/yellow palette or the reported flicker.
- cf.7 remote human timing attack now uses the normal class timing-projectile visual family instead of the passive/automatic-shot visual family.

## Important defects found and closed during v0.35 validation
1. Public run snapshot inherited `stage: 1` hardcoding, preventing the Stage 2 client transition path.
   - fixed by exposing authoritative `run.stage`.
2. Stage 2 client flow bypassed the existing `startStage(2)` intro path.
   - restored `STAGE / READY / START` and Timing Square/input initialization.
3. Legacy result board used local/single-player state and hardcoded `STAGE 10 CLEAR`.
   - replaced by authoritative current-stage and room/run contribution data.
4. KILL COIN initially used current wallet balance rather than cumulative monster-kill reward.
   - separated cumulative kill-coin contribution from spendable wallet state.
5. Team Shop purchase had no in-flight feedback.
   - added immediate pending UI + duplicate-tap guard while keeping server-confirmed mutation.
6. Rogue Timing Square inherited v0.24 code temporarily rendered the base square as Knight.
   - removed the yellow/knight visual leakage path.
7. Remote human timing hits shared the simplified passive/automatic projectile renderer.
   - remote human timing projectiles now use the same class/tier visual language as local human timing attacks.

## Authority / regression boundary
No numerical balance values were intentionally changed during the cf.3-cf.7 closure work.

Unchanged governance includes:
- attack damage coefficients,
- monster HP,
- passive interval/damage,
- combo coefficients,
- EXP rules,
- shop costs,
- knockback coefficients,
- Stage 1/2 planned counts/gaps,
- class balance identities.

## What this PASS does not establish
This closure does **not** yet prove:
- Stage 3–10 Cloudflare multiplayer generalization,
- larger-party multiplayer behavior beyond the validated slice,
- full Lv6+ multiplayer skill consequence authority,
- final production persistence/security/anti-cheat architecture,
- final shop/shared-wall semantics,
- final numerical balance.

## Next boundary
Open a separate scoped migration slice for Stage 3–10 generalization, larger-party validation, and Lv6+ multiplayer authority. Perform recovery/preflight first; do not silently change balance values.

Deferred UX item: heterogeneous phone-size/aspect-ratio responsive safety should be reviewed later as a shared responsive-safety layer, not as per-device one-off patches.
