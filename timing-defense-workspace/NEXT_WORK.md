# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.28**
- URL: `https://timing-defense-v011.onrender.com/v028.html`
- Live source HEAD: `df6a18a2722e42e4e4046ff4e6c0b4fb44af894d`
- Render deploy: `dep-dbbhkonavr4c73dtoe0g` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless the user explicitly asks.

---

# Immediate device validation — v0.28

## Orientation / viewport contract
Timing Defense is landscape-only.

Verify on the same Samsung Browser / Android device:
- direct landscape load fills the entire browser content width,
- portrait mode never exposes the lobby/combat/result UI,
- portrait shows only the dedicated `가로 화면 전용` gate,
- rotating back to landscape restores the full-width lobby,
- no left-half-only lobby / black-right-half state is visible,
- if Samsung Browser retains a stale portrait-width viewport while physically landscape, the malformed lobby is hidden,
- stale viewport repair is attempted automatically,
- if repair does not settle, the recovery screen shows `가로 상태에서 새로고침`.

## v0.27 regression checks
Character select:
- six cards remain `3 × 2`,
- skill names one line,
- `습득 LV N` one line,
- descriptions use full lower width,
- radar preserves correct hex proportions,
- arrow taps work,
- horizontal swipe works,
- rapid swipe + arrow use does not double-step.

Combat/result:
- combo unchanged,
- combat title absent,
- BASE HP top-center stable,
- top-right STAGE → LV → KILLS stable,
- result names/class badges do not overlap,
- RETRY / LOBBY remain separated.

TEAM waiting UX:
- FRIEND/LINK/RANDOM local waiting screens open correctly,
- nickname/class/AI FILL slots preserved,
- READY/back controls work,
- no fake link, match success, or remote participant,
- START remains disabled before real networking.

Fix implementation/visual defects directly. Do not change numerical combat balance or combo presentation from this validation.

---

# Following implementation boundary — real multiplayer architecture
Once v0.28 orientation + v0.27 UX validation is clean, move from local waiting UX to actual networking.

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
