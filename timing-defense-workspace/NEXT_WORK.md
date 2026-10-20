# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.30**
- URL: `https://timing-defense-v011.onrender.com/v030.html`
- Live source HEAD: `a235bf2dc0bd5bb5138b4bd89d81512345ec6713`
- Render deploy: `dep-dbbhud8n74is73cp0rug` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# Immediate validation — v0.30 clean recovery

## Why this build exists
v0.27 introduced a self-retriggering MutationObserver in skill-level normalization. That concrete regression is now treated as the primary cause of the severe partial-render/freeze state.

v0.28/v0.29 viewport repair scripts are superseded and **not loaded** by v0.30.

v0.30 keeps:
- known v0.26 layout/combat HUD foundation,
- desired v0.27 one-line skills/radar/swipe/result/waiting UX,
- a targeted guard that prevents only the defective v0.27 observer from running,
- a simple portrait-only orientation gate with no viewport width manipulation.

## Samsung Browser validation
Test on the same Android landscape setup:
- direct v0.30 load fills the full browser content width,
- page remains responsive rather than progressively freezing/partially painting,
- no black-right-half state,
- skill names remain one line,
- `습득 LV N` remains one line,
- radar keeps correct proportions,
- arrow navigation works,
- horizontal swipe works,
- swipe + arrow use does not double-step,
- portrait shows only the `가로 화면 전용` gate,
- returning to landscape restores the full-width lobby.

## Combat/result regression
Verify:
- combo unchanged,
- combat title absent,
- BASE HP top-center stable,
- STAGE → LV → KILLS top-right stable,
- result names/class badges do not overlap,
- RETRY / LOBBY remain separated.

## TEAM waiting UX
Verify FRIEND / LINK / RANDOM:
- local waiting screen opens,
- nickname/class/AI FILL preserved,
- READY/back controls work,
- no fake remote user/link/match success,
- START remains disabled before actual networking.

Fix only defects reproducible from the clean v0.30 chain. Do **not** reintroduce v0.28/v0.29 width heuristics unless separate evidence proves a viewport defect after the observer-loop removal.

---

# Following implementation boundary — actual multiplayer architecture
Once v0.30 runtime/UI stability is confirmed:
1. room authority / backend owner,
2. FRIEND room create/invite/join lifecycle,
3. LINK room URL/code contract,
4. RANDOM queue/match assignment,
5. participant slot + class ownership,
6. authoritative ready/start,
7. synchronized stage/run start,
8. Attack Round/combat-event synchronization,
9. disconnect/reconnect grace handling,
10. snapshot/reconciliation/desync policy,
11. multiplayer shop/economy ownership.

Do not claim real multiplayer until two independent clients share one authoritative room/game state.

---

# Later gameplay/system work
After network foundation stabilizes:
- implement Lv26 / Lv31 skills,
- finalize duplicate-class policy,
- rerun full-run progression/pressure simulation,
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
