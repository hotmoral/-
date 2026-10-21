# Cloudflare v0.35 cf.6 candidate — 2026-10-21

Status: IMPLEMENTED / DEVICE VALIDATION PENDING

Bounded fixes only:
- Team Shop purchase remains server-authoritative but now shows an immediate `처리중…` pending state and blocks duplicate taps until the confirmed rank update or error/timeout.
- Network combat pins the local visual/input class to the authoritative participant `classId` before state/update/draw/tap paths, preventing non-Knight class palette fallback/flicker.
- cf.5 authoritative result board remains unchanged. AI participants remain valid contributors when intentionally configured by the user.

Non-goals / unchanged: AI roster semantics, attack coefficients, monster HP, passive damage/interval, combo coefficients, EXP, shop costs, knockback, stage counts/gaps, class balance, approved combo animation.

Validation required: Android + PC; shop pending response; Rogue charge color stability; Stage 1 -> shop -> Stage 2 flow; final result board retains all actual human/AI participants with synchronized authoritative metrics.
