# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.34**
- URL: `https://timing-defense-v011.onrender.com/v034.html`
- Live source HEAD: `6bfd51d7d496a0151d4448e71533b4e39de8eaa0`
- Static Render deploy: `dep-dbbklbrbc2fs73bgtq70` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbkbno473hc73cldb30` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# Immediate validation — v0.34 multiplayer presentation
Use the same Android + PC pair that passed v0.33 shared-HP validation.

## Render smoothing
1. Both clients join one v0.34 room and START.
2. Android monster movement should no longer visibly step every server snapshot.
3. PC and Android must still converge to the same authoritative enemy positions/HP.
4. Knockback should animate smoothly but must reconcile to server position.

## Remote projectile VFX
- PC human attack must show that PC player's class projectile on Android.
- Android human attack must show that Android player's class projectile on PC.
- AI FILL attack must show the AI class projectile.
- Server passive attack must show a projectile from the relevant human slot.
- Remote visual projectile must not apply damage locally; server snapshot remains the only authority.
- No duplicated local projectile for the player performing the attack.

## Shared-state regression
Continue verifying:
- enemy HP/death,
- KILLS,
- BASE HP,
- local EXP/LV/charge,
- Stage 1 clear/game-over,
- AI/passive damage occurs once only.

## Runtime regression
Also recheck:
- portrait orientation gate,
- full-width landscape rendering,
- character swipe/arrows,
- combo visual unchanged,
- BASE HP top-center HUD,
- STAGE → LV → KILLS HUD,
- FRIEND/LINK waiting-room layout remains unclipped.

Fix only reproducible v0.34 rendering/runtime defects before expanding network scope.

---

# Following network slice after v0.34 PASS
1. Add reconnect/rejoin session recovery using the current authoritative run snapshot.
2. Add explicit run revision / desync diagnostics.
3. Implement authoritative Stage 1 -> shop transition.
4. Decide and implement multiplayer shop ownership/purchase semantics.
5. Add synchronized NEXT gate.
6. Extend server run state to Stage 2.
7. Validate Stage 2 after a shared shop.
8. Extend the same authority contract through Stage 10.
9. Move Lv6/Lv11/Lv16/Lv21 skill consequences under server authority.
10. Validate DUO / TRIPLE / FULL independently.

Do not claim full end-to-end Stage 1–10 multiplayer until two independent clients complete a whole run from the same authoritative state.

---

# Current authority contract
Client owns:
- local Timing Square movement/input,
- captured X/Y judgment,
- purely visual interpolation/projectile rendering.

Server owns:
- run id/seed/start time,
- enemy spawn/id/authoritative position/HP,
- BASE HP,
- target selection,
- normal/heavy state from server charge,
- final attack tier,
- damage/knockback/kill,
- coin,
- EXP/LV,
- charge,
- current combo multiplier candidate,
- passive/AI damage,
- Stage 1 clear/game-over.

Current bounded scope:
- Stage 1 only,
- GRUNT Stage 1 grammar,
- no synchronized shop yet,
- no Lv6+ server skill resolution yet.

---

# Later gameplay/system work
After network foundation stabilizes:
- implement Lv26 / Lv31 skills,
- finalize duplicate-class policy,
- rerun full-run progression/pressure simulation,
- validate Solo / 2P / 3P / 4P,
- finalize passive/ordinary HP/combo coefficients only after report/discussion,
- finalize E/X pressure values and tier progression,
- finalize result-board metric policy.

## Still unresolved
- reconnect/session recovery policy,
- durable multiplayer state store,
- horizontal scaling strategy,
- invite-link security/token contract,
- Stage 2–10 authority,
- multiplayer shop/economy authority,
- complete Lv6+ skill authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation details,
- Lv26/Lv31 coefficients,
- final passive damage/interval,
- final HP compensation,
- combo/milestone coefficients,
- final E/X/tier values,
- final result metrics.
