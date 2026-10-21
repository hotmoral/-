# Cloudflare v0.35 cf.4 Result Contract — INCOMPLETE

Date: 2026-10-21 KST

User clarification from two-human/no-AI device run:
- both devices showed only the local human plus a CPU row instead of both human participants,
- KILLS / DMG / COIN were zero even for the active local human,
- therefore the inherited local result board was not a valid multiplayer result source.

Audit of cf.4:
- participant rows were corrected to authoritative `state.participants`,
- human KILLS/DMG/LV/MAX COMBO were switched to authoritative `run.players`,
- but COIN incorrectly used current wallet `player.coin`, which can be reduced by shop purchases and includes non-kill rewards.

cf.4 is not a PASS checkpoint.

Required corrected contract:
- rows = authoritative human participants + only actually configured AI FILL,
- KILLS = authoritative cumulative player/AI kills,
- DMG = authoritative cumulative player/AI damage,
- KILL COIN = cumulative monster-kill rewards only, independent of wallet spending and stage-clear rewards,
- LV/MAX COMBO = authoritative run values,
- both clients render the same final snapshot.
