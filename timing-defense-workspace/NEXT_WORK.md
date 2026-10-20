# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.23**
- URL: `https://timing-defense-v011.onrender.com/v023.html`
- Live source HEAD: `6a7a4acafda9fe7dc405455c73adc3d7065f1285`
- Render deploy: `dep-dbbfierrjlhs73e3mfeg` / LIVE

## Balance governance remains unchanged
Do **not** production-freeze passive/combo/enemy-HP values from UX feedback.
Required order:
`implement/test → measure → classify intent/artifact/defect → report → discuss → explicit decision → numerical freeze/patch`.

---

# Immediate device validation — v0.23

## Character selection
Verify:
- only the centered hero visibly slides when class changes,
- left class info and right skill info update cleanly,
- arrows and swipe both work,
- nickname input remains usable,
- character silhouette/weapon remains readable.

## Skill roadmap
Verify:
- all six icons are visible together,
- tapping any icon shows full skill name + full description,
- descriptions do not truncate,
- mechanic-specific icon shapes remain legible,
- short Android landscape does not overflow.

## Combat readability
Verify:
- Rogue Timing Square edge is now clearly visible on natural scenery,
- Rogue 1–3 charge pips are visible in active/inactive states,
- every valid local timing EXP event shows a fresh `+EXP N`, including gains between level-ups,
- lower-left EXP float stays absent,
- attack debug line stays hidden.

## Play settings
Verify:
- SOLO still allows 0–3 AI,
- TEAM hides/disables +3 AI,
- TEAM automatically leaves at least one human slot,
- AI class buttons show readable glyph + KNI/ROG/TNK/ARC/MAG,
- +3 SOLO AI no longer clips summary badly,
- TEAM page no longer requires awkward internal scrolling for normal landscape height.

## End-run board
Verify:
- local nickname shown,
- PLAYER/CLASS lines do not collide between rows,
- rank medals align with values,
- RETRY/LOBBY remain accessible.

Fix implementation/visual defects only from this validation.

---

# Next implementation slice — v0.24 waiting-room UX
The previously planned v0.23 waiting flow moved to v0.24 because v0.23 was used for device-feedback polish.

Goal: implement user-visible TEAM waiting states without pretending real network connectivity exists.

## FRIEND
- waiting-room surface,
- local nickname/class/slot,
- reserved human slots,
- invite control placeholder,
- ready/start separate from connection state.

## LINK
- room/link presentation,
- copy/share affordance only with truthful limitation,
- joining/waiting/participant-slot state,
- no fake join confirmation.

## RANDOM
- searching state,
- cancel action,
- participant placeholders,
- match-found transition design,
- no fake match success.

## Shared rules
- chosen nickname/class/tier preserved,
- AI filler configuration preserved where valid,
- TEAM AI max remains +2 so at least one human slot is reserved,
- leaving waiting returns safely to play settings,
- combat never runs behind waiting UI.

---

# Following boundary — real multiplayer architecture
After v0.24 UX stabilizes:
- room creation/authority,
- invite/link contract,
- join/leave lifecycle,
- random matchmaking queue,
- slot/class ownership,
- synchronized start,
- Attack Round/combat events,
- disconnect/reconnect,
- state reconciliation/desync policy.

Do not claim real multiplayer until two independent clients share authoritative game state.

---

# Experimental combat values retained unchanged
Passive:
- 40 raw / 2.0 s
- no EXP / charge / crit / skill / combo
- ordinary non-boss HP +10%

Combo:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap
- milestone budgets 60 / 90 / 150 / 210 cap.

No retuning from lobby/readability observations.

---

# Later balance execution
After lobby/network architecture reaches a stable combat model:
1. full-run wall HP carry,
2. local + AI/human-equivalent EXP/level progression,
3. shop progression,
4. passive-only / Average / Skilled / Expert,
5. solo / 2P / 3P / 4P,
6. pressure recipe rerun,
7. report before numerical production freeze.

## Still unresolved
- final passive/HP/combo coefficients,
- final result-board metrics,
- E/X values and tier structure,
- multiplayer economy/shop ownership,
- duplicate-class policy,
- DUO/TRIPLE/FULL sync,
- Lv26/Lv31 coefficients,
- room authority/network protocol,
- invite/link security contract,
- matchmaking/rejoin/reconciliation policy.
