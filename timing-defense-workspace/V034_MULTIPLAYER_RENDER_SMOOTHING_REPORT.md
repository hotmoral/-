# Timing Defense — v0.34 Multiplayer Render Smoothing / Remote VFX Report

Updated: 2026-10-20 KST

## Public build
- Version: **v0.34**
- URL: `https://timing-defense-v011.onrender.com/v034.html`
- Live source HEAD: `6bfd51d7d496a0151d4448e71533b4e39de8eaa0`
- Static Render deploy: `dep-dbbklbrbc2fs73bgtq70` / LIVE
- Multiplayer backend remains the v0.33 authoritative Stage 1 server.

## Trigger
Two-client device validation of v0.33 confirmed real shared enemy HP: an attack performed on the PC client reduced the same monster HP on the Android client. The Android recording also exposed two presentation/runtime defects:
1. remote human attacks changed HP but showed no projectile on the receiving client,
2. Android movement looked slightly stepped while the PC client reported little/no visible stutter.

## Root cause
v0.33 intentionally consumed authoritative snapshots roughly every 100 ms and directly replaced monster x/y from each snapshot while local monster velocity was disabled. This made the shared state correct, but visual movement could advance in visible 100 ms steps, especially on Samsung Browser/mobile GPU.

v0.33 also rendered only the result of remote combat events (HP/hit flash/damage float). It did not synthesize a visual-only projectile for remote humans, AI FILL, or server-owned passive attacks.

## v0.34 client changes
File:
- `timing-defense-v011/v034-combat-sync.js`

### 1. In-place authoritative monster reconciliation
- Keeps monster objects by server monster id instead of recreating every monster object on every snapshot.
- Updates authoritative HP/maxHP and new network target x/y in place.
- Removes objects only when no longer present in the authoritative snapshot.
- Reduces short-lived object allocation/GC pressure on mobile.

### 2. 60 fps render smoothing
- Server snapshot cadence stays unchanged.
- Each rendered monster eases toward the latest authoritative target every animation frame.
- Adds a bounded short extrapolation using the monster's known movement speed between snapshots.
- Large discontinuities still snap to the authoritative location to avoid runaway divergence.
- Visual interpolation never becomes gameplay authority; the next server snapshot remains final.

### 3. Remote attack VFX
Visual-only projectiles are synthesized from ordered server combat events for:
- remote human timing attacks,
- AI FILL attacks,
- server-owned passive attacks.

The projectile starts at the visual party member's weapon position and follows the current authoritative target. Class-readable shapes/colors are used:
- Knight: amber/gold blade wave,
- Rogue: charcoal/silver dagger,
- Tank: blue shock arc,
- Archer: green straight arrow,
- Mage: purple orb.

Remote impact particles/damage floats are delayed until the visual projectile reaches the target rather than appearing at launch.

Local timing attacks continue to use the existing local projectile animation; v0.34 does not duplicate those projectiles.

### 4. Party allocation optimization
Remote party visual rows are rebuilt only when participant/AI configuration changes, not on every 100 ms snapshot.

## Authority / balance guard
No gameplay balance values changed.
- server tick remains 50 ms,
- authoritative shared snapshots remain about 100 ms,
- passive remains experimental 40 / 2.0 s,
- ordinary HP compensation unchanged,
- combo coefficients unchanged,
- combo presentation untouched.

Interpolation and projectile synthesis are presentation-only. Server authority for damage, target, HP, BASE HP, EXP/LV, charge, kill, coin and Stage 1 completion remains unchanged.

## Device validation required
Use the same Android + PC pair:
1. Join the same v0.34 room and START.
2. Confirm Android monster movement is visibly smoother than v0.33.
3. PC attacks must visibly launch that PC player's class projectile on Android.
4. Android attacks must visibly launch the Android player's class projectile on PC.
5. AI FILL and passive attacks should also have visible projectiles.
6. Shared HP/kill/BASE HP must remain identical.
7. No duplicated remote damage or duplicated local projectile should appear.
8. Stage 1 clear/game-over must remain synchronized.

## Next boundary after PASS
- reconnect/rejoin snapshot recovery,
- explicit revision/desync diagnostics,
- authoritative Stage 1 -> shop transition,
- Stage 2 server authority,
- synchronized shop/economy and NEXT gate,
- then Stage 3–10 and Lv6+ multiplayer skill authority.
