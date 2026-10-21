# Timing Defense — Monster Capability Live-Wiring Plan V1

Date: 2026-10-22 KST
Status: ACTIVE IMPLEMENTATION PLAN

## Purpose
Move from pure capability helpers into the authoritative combat kernel without reconstructing legacy Stage 4–10.

The last fully closed live checkpoint remains v0.39 N3 FULL PASS at `911dd67cf4bb4d704e050f8e3a92cb34c48deb3a`.

## Slice order
1. SHIELD / common armor layer
2. FLYER / authoritative Y geometry
3. CHARGER state machine
4. SPLITTER child-spawn kernel
5. SUPPORTER dynamic movement aura
6. SIEGER repeated wall-attack kernel

Each slice is capability-first and stage-number-independent.

## Slice A — SHIELD / common armor layer
Scope:
- retain current v0.39 Stage 1–3 as regression fixtures only,
- do not enable legacy Stage 4,
- add SHIELD metadata to every geometry/knock path that currently falls back to GRUNT,
- route SHIELD damage through one authoritative armor policy,
- preserve normal / AI / passive / Lv6 / N3 attribution and event semantics,
- expose deterministic sandbox hooks/tests rather than a campaign stage.

Required invariants:
- SHIELD armor provisional anchor `.72` is a sandbox test coefficient, not production balance freeze,
- `100 raw -> 72 actual`, minimum 1,
- SHIELD knock resistance `.62` and size `1.08` are used by Lv6/N3 geometry and knock calculations,
- BRUTE remains unarmored and existing Stage 1–3 results remain unchanged,
- kill / coin / killCoinEarned / damage contribution remain correct,
- AI stage multiplier occurs before armor,
- N3 raw budget metadata remains pre-armor while authoritative event damage is post-armor,
- no client-side damage authority is introduced.

Validation:
- pure capability selftest regression,
- new deterministic SHIELD authority selftest,
- v0.39 full server/client/event/4H regression,
- live GitHub Actions + Playwright after deployment candidate is ready,
- Samsung Browser only if presentation cannot be judged automatically.

## Governance
No legacy Stage 4 recipe implementation in this lane.
No production monster coefficient is frozen by passing capability tests.
