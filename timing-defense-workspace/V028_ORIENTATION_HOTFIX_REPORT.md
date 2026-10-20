# Timing Defense v0.28 — Orientation / Viewport Hotfix

Date: 2026-10-20 KST

## Trigger
Android/Samsung Browser device feedback showed a broken state after orientation/viewport transition: the game lobby rendered only in the left portion of the physical landscape screen while the remaining right side stayed black. The visible lobby behaved like a stale portrait-width viewport even though the device was physically landscape.

This is not an intended alternate layout. Timing Defense remains landscape-only.

## Fix
Files:
- `timing-defense-v011/v028-orientation.js`
- `timing-defense-v011/v028.html`

### Landscape-only gate
- Portrait orientation no longer exposes the game/lobby UI.
- A full-screen orientation gate is shown instead.
- Copy instructs the player to rotate to landscape.
- The gate sits above all lobby/combat/result surfaces and blocks interaction behind it.

### Stale landscape viewport handling
If the device reports physical landscape but the visual viewport still behaves as portrait:
1. reset the viewport meta to the current landscape screen width,
2. force document reflow,
3. re-measure after a short delay,
4. if still invalid, hide the broken game UI and show a safe recovery screen,
5. expose a `가로 상태에서 새로고침` recovery button rather than displaying a half-width broken layout.

### Orientation transition hooks
Revalidation runs on:
- `orientationchange`,
- window resize,
- VisualViewport resize,
- Screen Orientation API change when available.

When a valid landscape viewport is restored, main surfaces are reset to full `100vw` width.

## Explicit non-goals / regression guards
- No combat value changed.
- No combo logic or visual changed.
- No radar/skill/waiting-room behavior changed from v0.27.
- No actual multiplayer transport added.

## Device validation
On the same Samsung Browser/device:
1. open v0.28 in landscape and confirm the lobby occupies the full content width,
2. rotate to portrait and confirm only the orientation gate is visible,
3. rotate back to landscape and confirm the lobby returns full-width,
4. if Samsung Browser retains a stale portrait viewport, confirm the broken half-layout is hidden and the recovery screen is shown,
5. verify v0.27 fixes remain intact: skill title/level one-line, proportional radar, swipe + arrows, result rows, TEAM waiting UX.
