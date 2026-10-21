# Timing Defense — Monster Capability Foundation PASS

Date: 2026-10-22 KST
Status: **FOUNDATION PASS / NOT LIVE-WIRED / NOT BALANCE FROZEN**

## Source branch
- `timing-defense-cloudflare-v040-monster-capability-foundation`
- validated HEAD: `68882c2013d1d35aaedbf12e5725fde377795044`

This branch starts exactly from the v0.39 FULL PASS checkpoint and does not replace or mutate the watched live deployment branch.

## Scope
Pure stage-number-independent capability helpers only:
- provisional nine-archetype metadata
- SHIELD armor helper
- FLYER authoritative Y-function candidate
- CHARGER state transition helper
- SPLITTER deterministic two-child helper
- SUPPORTER non-stacking speed-aura helper
- SIEGER standoff/windup/fire/reposition helper

No final stage recipe, no Stage 4 reconstruction and no production balance claim.

## CI
GitHub Actions workflow:
`.github/workflows/timing-defense-monster-capability-v1.yml`

Run:
- id `39693813756`
- result: **SUCCESS**

Validated foundation invariants:
- 9 ordinary archetypes exist
- 9 primary roles are unique
- SHIELD 100 raw -> 72 provisional armor result
- SHIELD minimum damage rule
- BRUTE is not accidentally armored
- FLYER Y helper returns deterministic base/amplitude positions
- CHARGER advance -> windup
- CHARGER windup knockback interrupt
- CHARGER re-arm guard
- CHARGER windup -> charge and provisional charge speed
- SPLITTER exactly two children
- children cannot split recursively
- deterministic child offsets
- SUPPORTER aura off/on behavior
- SUPPORTER same-aura non-stacking
- SUPPORTER does not buff itself
- SIEGER advance -> windup
- windup -> fire
- fire -> cooldown
- knockback-induced reposition

## Numerical boundary
All numbers in `MONSTER_PROVISIONAL_TEST_ENVELOPE_V1.md` remain:
**PROVISIONAL — NOT BALANCE FROZEN**.

They are executable anchors for deterministic tests only.

## Next implementation boundary
Wire capabilities into the authoritative combat kernel in bounded slices while preserving v0.39 regression:
1. SHIELD / common armor layer
2. FLYER / authoritative Y geometry
3. CHARGER
4. SPLITTER
5. SUPPORTER
6. SIEGER

Each live-wiring slice must retain:
- existing v0.39 authoritative combat/N3 behavior
- event-stream/reconnect guarantees
- GitHub Actions automation
- no unapproved production numerical tuning.
