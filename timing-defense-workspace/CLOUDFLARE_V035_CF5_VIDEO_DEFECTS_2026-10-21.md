# Cloudflare v0.35 cf.5 video defects — 2026-10-21

Status: DEFECTS CONFIRMED / NOT PASS

Evidence: Android Samsung Browser recording supplied by user after cf.5.

Confirmed defects:
1. Team Shop purchase has no immediate pending feedback. The client waits for server-confirmed state before rank/coin changes, so a valid tap can look ignored for roughly a network round trip and invites duplicate tapping.
2. Rogue Timing Square CHARGE presentation intermittently switches to the knight/yellow palette and flickers. This is not intended. Treat as a network-run local-class stability issue; non-knight classes can be affected, while Knight can mask the defect because yellow is its normal palette.
3. AI NONE run nevertheless contained a real CPU 2 contributor in the authoritative result board (non-zero kills/damage). This is not merely a result renderer ghost row. The room creation client serializes AI rows without explicitly honoring the selected AI-count=0 state, so stale DOM rows can leak into `aiFill`.
4. cf.5 result board itself now correctly shows STAGE 2 CLEAR, both human participants, and populated authoritative KILLS/DMG/KILL COIN/LV/MAX COMBO. However, because the run incorrectly contained CPU 2, cf.5 result parity is not PASS.

Next bounded fix: cf.6 only — explicit AI-count serialization, pending-state Team Shop UX without optimistic economy mutation, authoritative local-class pinning, and result rows reflecting actual run participants. No balance changes.
