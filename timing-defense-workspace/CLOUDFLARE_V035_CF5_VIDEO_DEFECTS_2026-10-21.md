# Cloudflare v0.35 cf.5 video defects — 2026-10-21

Status: TWO DEFECTS CONFIRMED / RESULT BOARD BEHAVIOR CLARIFIED

Evidence: Android Samsung Browser recording supplied by user after cf.5, plus user clarification that the tested run intentionally included an AI participant.

Confirmed defects:
1. Team Shop purchase has no immediate pending feedback. The client waits for server-confirmed state before rank/coin changes, so a valid tap can look ignored for roughly a network round trip and invites duplicate tapping.
2. Rogue Timing Square CHARGE presentation intermittently switches to the knight/yellow palette and flickers. This is not intended. Treat as a network-run local-class stability issue; non-knight classes can be affected, while Knight can mask the defect because yellow is its normal palette.

Clarified non-defect:
- CPU 2 appearing in the result board was expected for the recorded run because the user intentionally added AI. Its KILLS/DMG/KILL COIN contribution is therefore valid evidence that the authoritative result board includes actual AI participants.
- cf.5 result board correctly shows STAGE 2 CLEAR, both human participants, the intentional AI participant, and populated authoritative KILLS/DMG/KILL COIN/LV/MAX COMBO.

Next bounded fix: cf.6 only — pending-state Team Shop UX without optimistic economy mutation, plus authoritative local-class pinning to remove palette/CHARGE flicker. No AI roster changes. No balance changes.
