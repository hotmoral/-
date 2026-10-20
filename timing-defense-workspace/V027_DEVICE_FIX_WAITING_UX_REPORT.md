# Timing Defense v0.27 — Device Fix + TEAM Waiting UX

Updated: 2026-10-20 KST

## Public state
- URL: `https://timing-defense-v011.onrender.com/v027.html`
- Live source HEAD: `6208e5d4665ca6acb6ebbd1105c50c0551c03630`
- Render deploy: `dep-dbbhfp3rjlhs73e9nvp0` / LIVE

## Scope
v0.27 responds to Android screenshots after v0.26 and closes the remaining safe UI defects before real multiplayer transport work.

No combat coefficients, projectile timing, or combo presentation were changed.

## Character-select fixes
### Skill cards
- Six cards remain `3 × 2`.
- Skill name is forced to one line.
- Acquisition level is forced to one line as `습득 LV N`.
- Font sizes are reduced slightly to prevent Korean line wrapping.
- Description still uses the full lower width of each card.

### Radar
- The radar canvas now preserves its intrinsic `330:280` aspect ratio.
- CSS no longer independently stretches width and height.
- Five rings and six axes remain unchanged.
- Approved profile values and animation remain unchanged.

### Swipe
The v0.22 pointerup-only gesture was unreliable after later overlay/hit-target changes.
v0.27 replaces it with:
- pointer capture,
- explicit horizontal-vs-vertical intent detection,
- ~38 px horizontal threshold,
- arrow click dispatch after a valid swipe,
- arrow/button/input exclusion.

Arrow taps remain separate and fixed.

## Result board
The PLAYER / CLASS collision is removed structurally:
- nickname/CPU label is one line,
- class is a compact colored badge on the same row,
- no second class line can collide with the row below,
- four-player spacing is recalculated,
- board height is reduced so RETRY/LOBBY have clearer separation.

Metrics remain:
`KILLS / DMG / COIN / LV / MAX COMBO`.

## TEAM waiting-room UX
TEAM start now opens a truthful local waiting-room surface instead of flashing a temporary placeholder.

### Shared
- Selected nickname/class retained.
- AI FILL positions/classes retained.
- P1 is the local player.
- P2/P3/P4 show AI FILL or HUMAN SLOT / WAITING.
- Local READY state is available.
- START stays disabled until real room authority/participant synchronization exists.
- Back returns to PLAY SETTING.

### FRIEND
- INVITE affordance exists.
- Pressing it explicitly states that invite transport is not connected yet.
- No fake remote join is created.

### LINK
- ROOM LINK affordance exists.
- No fake URL is generated.
- UI explicitly states that a real room link requires backend room creation.

### RANDOM
- SEARCH / CANCEL SEARCH UI state exists.
- Search state explicitly says `NETWORK NOT CONNECTED`.
- No fake match-found transition or remote participant is generated.

## Network truth boundary
v0.27 is **not real multiplayer**.
Do not claim multiplayer is implemented until two independent clients join the same authoritative room and share synchronized state.

## Device validation target
1. skill names and `습득 LV` never wrap,
2. radar is no longer vertically squashed,
3. horizontal swipe works anywhere in the non-interactive carousel area,
4. result-board rows no longer overlap,
5. TEAM waiting screen opens and returns safely,
6. FRIEND/LINK/RANDOM copy remains truthful,
7. SOLO behavior remains unchanged,
8. combo presentation remains unchanged.
