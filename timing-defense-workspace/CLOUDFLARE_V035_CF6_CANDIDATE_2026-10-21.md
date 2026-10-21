# Cloudflare v0.35 cf.6 candidate — 2026-10-21

Status: IMPLEMENTED / DEVICE VALIDATION PENDING

Bounded fixes only:
- AI NONE room creation payload is forced to `aiFill=[]` from the selected AI-count control, preventing stale rendered AI rows from becoming real authoritative CPUs.
- Team Shop purchase remains server-authoritative but now shows an immediate `처리중…` pending state and blocks duplicate taps until the confirmed rank update or error/timeout.
- Network combat pins the local visual/input class to the authoritative participant `classId` before state/update/draw/tap paths, preventing non-Knight class palette fallback/flicker.
- cf.5 authoritative result board remains in place; with a new AI NONE room it must show only the two human contributors.

Non-goals / unchanged: attack coefficients, monster HP, passive damage/interval, combo coefficients, EXP, shop costs, knockback, stage counts/gaps, class balance, approved combo animation.

Validation required: Android + PC new AI NONE room; shop pending response; Rogue charge color stability; Stage 2 flow; final board exactly two humans with synchronized authoritative metrics.

Current candidate HEAD: `8759bd375e3ef0c2e14d39f50bd914422ba789c1`.
