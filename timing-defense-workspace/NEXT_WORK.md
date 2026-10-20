# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.22**
- URL: `https://timing-defense-v011.onrender.com/v022.html`
- Live source HEAD: `7a321d021cafbfc32749b4e8b9421b2bf908826a`
- Render deploy: `dep-dbbef5s9v7es73eupvlg` / LIVE

## Balance governance remains unchanged
Do **not** production-freeze passive, combo-reward or enemy-HP values from first impressions.

Required order:
`implement/test → measure → identify intent/artifact/defect → report → discuss → explicit decision → numerical freeze/patch`

---

# Immediate device validation — v0.22

## 1. v0.21 combat presentation inheritance
Verify under the v0.22 loader:
- natural battlefield renders cleanly,
- lower-left EXP float is gone,
- gauge feedback reads `+EXP N`,
- NORMAL/GOOD/PERFECT/heavy/CRITICAL pop **inside Timing Square** and disappear quickly,
- judgment popup does not hide the active sweep,
- `STAGE N / READY → START!` timing feels clean,
- result panel is visually centered,
- debug N/G/P/C/AVG remains hidden.

## 2. Nickname / carousel
Check on Android landscape:
- nickname input is easy to focus/type,
- nickname persists after revisiting the page,
- arrow navigation transitions cleanly,
- swipe threshold is comfortable and does not accidentally navigate on minor taps,
- all five class hero silhouettes/weapon identities are distinct,
- carousel does not vertically overflow on short landscape screens.

## 3. Skill roadmap
Inspect all 30 roadmap icons.
Acceptance intent:
- icon shape communicates skill mechanic without relying only on text,
- different skills inside one class are visually distinct,
- class palette remains recognizable,
- examples such as Double Dagger / Triple Shot / shield / ground impact / chain explosion are immediately inferable.

## 4. Play settings
Current interaction is button/segmented rather than dropdown-first.
Verify:
- SOLO/TEAM choice obvious,
- AI count easy to change,
- AI position P2/P3/P4 understandable,
- AI class initials/buttons readable,
- duplicate AI positions swap correctly,
- Tier1 presentation does not look like an empty dropdown,
- default is SOLO / AI NONE / highest available tier.

## 5. Actual combat configuration
Test:
- no AI → solo starts immediately,
- +1/+2/+3 AI starts immediately in SOLO mode,
- selected AI classes appear in selected positions,
- local chosen class appears correctly,
- old in-combat class bar and bottom TEAM/SPEED setup panel do not appear.

---

# Next implementation slice — v0.23 team waiting-flow UX

Goal: implement the user-visible state machine for TEAM without pretending networking already works.

## FRIEND flow
- TEAM → FRIEND
- waiting-room screen
- local nickname/class/slot shown
- invited-player slots shown as waiting
- invite action placeholder/control prepared for real network wiring
- ready/start state clearly separated from connection state

## LINK flow
- TEAM → LINK
- room/link presentation surface
- copy/share affordance may exist only if its current limitation is explicit
- joining state / waiting state / participant-slot state designed
- do not claim another client has joined without backend confirmation.

## RANDOM flow
- TEAM → RANDOM
- searching state
- cancel matching
- player-slot placeholders
- match-found transition designed
- no fake successful match.

## Common waiting-room rules
- chosen local class/nickname/tier preserved,
- AI filler configuration remains visible/adjustable where allowed,
- leaving returns safely to play settings,
- combat must not run behind waiting UI,
- actual server/room state will replace mock/local state later without changing the overall UX hierarchy.

---

# Following boundary — real multiplayer architecture
After v0.23 UX is stable, design/implement actual network behavior:
- room creation/authority,
- shareable invite/link contract,
- join/leave lifecycle,
- random matchmaking queue,
- slot/class ownership,
- start synchronization,
- Attack Round / combat event synchronization,
- disconnect/reconnect,
- state reconciliation,
- server/client anti-desync rules.

Do not claim real multiplayer until two independent clients can actually share authoritative game state.

---

# Experimental combat values retained unchanged
Passive:
- 40 raw / 2.0 s
- no EXP / charge / crit / skill / combo
- non-boss HP +10%

Combo persistent bonus:
- 5–9 +5%
- 10–19 +8%
- 20–29 +12%
- 30+ +15% cap

Milestones:
- 5 / 10 / 20 / 30 / every +10 thereafter
- budgets 60 / 90 / 150 / 210 cap

Do not retune these from lobby/UX feedback.

---

# Later balance execution
After lobby/network architecture reaches a stable combat model:
1. run full-run progression simulation with wall HP carried stage-to-stage,
2. local + AI/human-equivalent EXP/level progression,
3. shop progression where valid,
4. passive-only / Average / Skilled / Expert,
5. solo / 2P / 3P / 4P,
6. then rerun pressure recipes.

Report before any numerical production freeze.

## Still unresolved / not production-frozen
- final passive damage/interval,
- final ordinary/elite/boss HP compensation,
- combo/milestone coefficients,
- final result-board metrics,
- final E/X pressure coefficients,
- exact tier progression/count/names,
- multiplayer economy/shop ownership,
- duplicate-class policy,
- sync DUO/TRIPLE/FULL rules,
- Lv26/Lv31 coefficients,
- room authority/network protocol,
- invite/link security contract,
- matchmaking policy,
- disconnect/rejoin behavior.
