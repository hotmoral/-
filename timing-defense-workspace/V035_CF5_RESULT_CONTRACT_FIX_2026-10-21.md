# Cloudflare v0.35 cf.5 Result Contract Fix

Date: 2026-10-21 KST

Corrected multiplayer result contract after two-human/no-AI device evidence:
- final rows come from authoritative `state.participants`, not local `S.ai` / local stats,
- AI rows appear only when authoritative `aiFill` is configured,
- human KILLS/DMG/LV/MAX COMBO come from authoritative `run.players`,
- server now tracks `killCoinEarned` separately from wallet `coin`,
- KILL COIN counts monster-kill rewards only and is not reduced by Team Shop purchases,
- stage-clear reward is not mixed into KILL COIN,
- AI kill/damage/kill-coin contribution is also server-tracked for AI-fill runs,
- both clients should render the same final snapshot.

This is a deployment candidate, not PASS until device-validated.