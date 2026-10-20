# Timing Defense — v0.21 Implementation Report

Date: 2026-10-20 KST
Status: **LIVE / UX-POLISH ONLY — no numerical balance retune**

## Public build
- URL: `https://timing-defense-v011.onrender.com/v021.html`
- Live source HEAD: `5a1c7fbfb575e805ce65eb238157abd2136ba3fa`
- Render deploy: `dep-dbbec549v7es73euenkg` / LIVE

Files:
- `timing-defense-v011/v021-polish.js`
- `timing-defense-v011/v021.html`

## Changes

### EXP feedback cleanup
- Removed the old lower-left `EXP +N` floating text.
- EXP gain is consolidated beside the vertical level/EXP gauge as `+EXP N`.

### Timing judgment pop
GOOD / PERFECT / CRITICAL and heavy-result labels are rendered inside the Timing Square as short impact-style pops instead of persistent/outer HUD text.

Current presentation language:
- NORMAL = small neutral gray,
- GOOD = green,
- PERFECT = larger gold,
- HEAVY / HEAVY+ / GREAT / SUPER / CRITICAL = progressively distinct size/color/glow,
- MISS = red.

The pop lasts roughly 330 ms and is intended to read as tactile feedback rather than a blocking information panel.

### Natural battlefield
The black/grid prototype backdrop was replaced by a muted geometric natural landscape:
- sky gradient,
- sun haze,
- distant mountain silhouettes,
- field/ground layers,
- simple tree silhouettes,
- stone defensive wall/platforms.

The background remains deliberately subdued so monsters, Timing Square and projectiles retain priority.

### Stage start completion cue
v0.20 `STAGE N / READY` is retained.
When the intro finishes and combat becomes active, a centered `START!` pop appears briefly while combat begins.

### Results centering
The end-run contribution panel is redrawn around the viewport center rather than visually leaning toward the lower-right.

### Debug clutter
- right-side N/G/P/C + AVG stats are hidden in this build,
- old lower-left hint is hidden.

## Unchanged combat values
v0.21 does not change:
- passive `40 / 2.0 s`,
- non-boss HP `+10%`,
- combo persistent `+5/+8/+12/+15%`,
- milestone budgets `60/90/150/210`,
- class coefficients, monster coefficients, EXP, shop or pressure recipes.

## Validation boundary
- JS syntax was checked before push.
- Render LIVE confirms published source/build availability.
- No claim is made that the visual composition was independently browser-rendered by this AI; Android/device feedback remains the visual acceptance source.
