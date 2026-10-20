# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.27**
- URL: `https://timing-defense-v011.onrender.com/v027.html`
- Live source HEAD: `6208e5d4665ca6acb6ebbd1105c50c0551c03630`
- Render deploy: `dep-dbbhfp3rjlhs73e9nvp0` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless the user explicitly asks.

---

# Immediate device validation — v0.27

## Character select
Verify on the same Android landscape setup:
- all six skill cards remain `3 × 2`,
- skill names remain one line,
- `습득 LV N` remains one line,
- descriptions still use the full lower width,
- radar hex is no longer vertically squashed,
- six labels/five rings remain readable,
- arrow taps remain reliable,
- horizontal swipe now works across non-interactive carousel areas,
- rapid swipe + arrow use does not double-step unexpectedly.

## Combat / result regression
Verify:
- combo unchanged,
- combat title absent,
- BASE HP top-center stable,
- top-right STAGE → LV → KILLS stable,
- home-base art and combat skill icons unchanged from v0.26,
- result PLAYER / CLASS rows no longer overlap,
- class appears as a same-row badge,
- RETRY / LOBBY do not visually collide with the board.

## TEAM waiting-room UX
Test all three modes:

### FRIEND
- TEAM start opens waiting room,
- local nickname/class preserved,
- AI FILL slots preserved,
- open human slots visible,
- READY toggles locally,
- INVITE clearly says network transport is not connected,
- back returns to PLAY SETTING.

### LINK
- ROOM LINK affordance visible,
- no fake link generated,
- copy states clearly explain backend room creation is still absent.

### RANDOM
- SEARCH / CANCEL SEARCH local UI works,
- status explicitly says NETWORK NOT CONNECTED,
- no fake match-found state,
- no fake remote participant.

### Shared
- START remains disabled until real authority/participant synchronization exists,
- combat never runs behind the waiting overlay.

Fix implementation/visual defects directly. Do not change numerical combat balance or combo presentation from this validation.

---

# Following implementation boundary — real multiplayer architecture
Once v0.27 UI validation is clean, move from local waiting UX to actual networking.

Required architecture:
1. room authority / backend state owner,
2. FRIEND room create/invite/join lifecycle,
3. LINK room URL/code contract and validation,
4. RANDOM queue and match assignment,
5. participant slot + class ownership,
6. authoritative ready/start transition,
7. synchronized stage/run start,
8. Attack Round / combat-event synchronization,
9. disconnect/reconnect grace handling,
10. authoritative snapshot/reconciliation/desync policy,
11. multiplayer shop/economy ownership.

Do not claim real multiplayer until two independent clients share one authoritative room/game state.

---

# Later gameplay/system work
After network foundation is stable:
- implement Lv26 / Lv31 skills,
- finalize duplicate-class policy,
- rerun full-run progression and pressure simulation,
- validate solo / 2P / 3P / 4P,
- finalize passive/ordinary HP/combo coefficients only after report/discussion,
- finalize E/X pressure values and tier progression,
- finalize result-board metric policy.

## Still unresolved
- room/backend technology choice,
- invite/link security contract,
- matchmaking policy,
- reconnect/reconciliation behavior,
- multiplayer economy/shop authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL synchronization details,
- Lv26/Lv31 coefficients,
- final passive damage/interval,
- final HP compensation,
- combo/milestone coefficients,
- final E/X/tier values,
- final result metrics.
