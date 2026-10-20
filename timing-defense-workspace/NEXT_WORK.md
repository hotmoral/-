# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.32**
- URL: `https://timing-defense-v011.onrender.com/v032.html`
- Live source HEAD: `16b602221caf1d19c062e17363ac786d2bd20d18`
- Static Render deploy: `dep-dbbivgjrjlhs73ee5bm0` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend deploy: `dep-dbbims61egvs73861f10` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# Immediate validation — v0.32 real shared waiting room
Use the same Samsung Browser landscape device plus a second independent browser/device when checking actual shared state.

## FRIEND / LINK layout hotfix
1. Open TEAM + FRIEND and enter the waiting room.
2. Confirm the left panel shows READY + INVITE and lower status/link content without clipping.
3. Open TEAM + LINK and confirm READY + COPY LINK and lower status/link content without clipping.
4. The long invite URL must remain one line with ellipsis and must not push actions off-screen.
5. No internal vertical scrolling should be required for normal waiting-room use.

## FRIEND / LINK shared-state validation
1. Client A enters TEAM + FRIEND or LINK and receives a six-character room code.
2. A uses INVITE / COPY LINK.
3. Client B opens the room link and enters the TEAM waiting room.
4. Both clients must show the same human participants, classes and AI FILL slots.
5. READY changes on A/B must propagate to the other client without reload.
6. Host START must remain disabled until at least two humans are present and every human is READY.
7. Only the host may START.
8. START must put both clients in one server-owned `starting` state with the same future `startAt` timestamp.
9. Leaving must remove that participant from the room.
10. If host leaves, server must reassign host to the earliest remaining human slot.

## RANDOM
With two independent sessions:
- both enter TEAM + RANDOM,
- both search,
- backend must pair them into one room,
- both must then receive the same shared participant state.

## Runtime regression
Recheck:
- portrait orientation gate,
- full-width landscape rendering,
- skill one-line headers,
- radar proportions,
- swipe/arrows,
- combo untouched,
- BASE HP and STAGE → LV → KILLS HUD.

Fix only reproducible networking/UI/runtime defects from the clean v0.32 chain.

---

# Following implementation boundary — synchronized combat
After two-client waiting-room validation passes:
1. Define authoritative run snapshot and seed/version contract.
2. Convert server `startAt` into an actual synchronized local run start.
3. Define player action event envelope:
   - room/run id,
   - player slot,
   - attack round id,
   - X/Y phase,
   - timing judgment,
   - client monotonic sequence,
   - server receive/order metadata.
4. Decide authority split for timing judgments vs damage resolution.
5. Synchronize enemy spawn/death/HP, wall HP, coin, EXP/level, charge and stage transitions.
6. Add periodic authoritative snapshots.
7. Add disconnect/reconnect grace handling.
8. Add snapshot recovery and desync detection/reconciliation.
9. Add multiplayer shop/economy authority.
10. Validate DUO / TRIPLE / FULL independently.

Do not claim end-to-end multiplayer gameplay until two independent clients can start one run and observe the same authoritative combat state throughout.

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
- durable multiplayer state store,
- horizontal scaling strategy,
- reconnect/session recovery policy,
- invite-link security/token contract,
- exact combat authority split,
- shop/economy authority,
- duplicate-class rule,
- DUO/TRIPLE/FULL reconciliation details,
- Lv26/Lv31 coefficients,
- final passive damage/interval,
- final HP compensation,
- combo/milestone coefficients,
- final E/X/tier values,
- final result metrics.
