# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.31**
- URL: `https://timing-defense-v011.onrender.com/v031.html`
- Live source HEAD: `714e1e3060cbbd2c20a65114d2152b37f861ef22`
- Static Render deploy: `dep-dbbioegae00c73dd8cn0` / LIVE
- Multiplayer backend: `https://timing-defense-mp.onrender.com`
- Backend service ID: `srv-dbbimre1egvs73861d80`
- Backend initial deploy: `dep-dbbims61egvs73861f10` / LIVE

## Balance governance
Do not production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify → report → discuss → explicit decision → numerical patch/freeze`.

**Combo guard:** current combo visual/size/position/animation is approved. Do not change it unless explicitly requested.

---

# Immediate validation — v0.31 real shared waiting room
Use two independent browser sessions/devices.

## FRIEND / LINK
1. Client A opens v0.31 and enters TEAM + FRIEND or LINK.
2. A enters the waiting room and receives a real six-character room code.
3. A uses INVITE / COPY LINK.
4. Client B opens the link containing `?room=<CODE>`.
5. B enters the TEAM waiting room.
6. Both clients must show the same human participants, classes and AI FILL slots.
7. READY changes on A/B must propagate to the other client without reload.
8. Host START must remain disabled until at least two humans are present and every human is READY.
9. Only the host may START.
10. START must put both clients in one server-owned `starting` state with the same future `startAt` timestamp.
11. Leaving must remove that participant from the room.
12. If host leaves, server must reassign host to the earliest remaining human slot.

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

Fix only reproducible networking/UI/runtime defects from the clean v0.31 chain.

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
