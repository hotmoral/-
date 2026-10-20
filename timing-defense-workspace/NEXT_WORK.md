# Timing Defense — Next Work Boundary

## Current public state
- Public LIVE version: **v0.26**
- URL: `https://timing-defense-v011.onrender.com/v026.html`
- Live source HEAD: `8aee137de2f775cda3537b6cc0b9404f6692a55b`
- Render deploy: `dep-dbbgvjjbc2fs73b657s0` / LIVE

## Balance governance remains unchanged
Do **not** production-freeze passive/combo/enemy-HP/projectile-speed values from UX feedback alone.
Required order:
`implement/test → measure → classify intent/artifact/defect → report → discuss → explicit decision → numerical freeze/patch`.

**Specific v0.26 guard:** do not change combo display/size/position/animation from the latest overlap feedback. User explicitly clarified that the combat title was the defect.

---

# Immediate device validation — v0.26

## Character-select skill cards
Verify on the same Android landscape setup:
- all six cards remain `3 × 2`,
- icon stays beside skill name,
- `습득 LV N` is directly below every skill name,
- description uses the full card width below the icon/name row,
- formerly blank lower-left space is now used,
- larger text still fits without clipping.

## Left combat profile
Verify:
- radar is visibly higher,
- all six labels and five rings remain readable,
- role summary is fully visible,
- one-sentence description is fully visible and not clipped,
- approved radar animation/data remain unchanged.

Approved profiles remain frozen presentation data:
- Knight `4/2/3/3/4/2`
- Rogue `2/5/5/1/1/1`
- Tank `2/1/1/5/1/3`
- Archer `3/2/4/1/5/2`
- Mage `4/2/2/1/1/5`

## Hero + navigation
Verify:
- class name is above the hero head,
- no duplicate class name remains under the hero,
- arrows stay at fixed screen coordinates when pressed,
- rapid repeated taps register reliably,
- carousel swipe remains functional away from arrow buttons.

## Combat HUD
Verify:
- legacy `TIMING DEFENSE` battle title is absent,
- combo visual is unchanged,
- BASE HP appears top-center as a long gauge with current/max value,
- BASE HP is immediately noticeable during play,
- top-right order is exactly: STAGE → LV → KILLS,
- each status has its icon before the text,
- old bottom status strings are no longer duplicated.

## Home base
Verify the base now reads as a fortified structure rather than a plain vertical slab:
- armored cap,
- crenellations,
- reinforced columns,
- four character bays/platforms,
- characters remain correctly layered on top.

## Combat skill strip
Verify the six slots below Timing Square:
- use the same skill artwork as character select,
- learned skills are full-color/readable,
- locked skills use the same icon dimmed/grayscaled,
- slot order stays Lv6 / 11 / 16 / 21 / 26 / 31,
- strip does not collide with Timing Square/EXP UI.

## Existing regression checks
- Rogue Timing Square/charge/EXP remains charcoal/black + silver,
- all valid timing EXP gains still show `+EXP N`,
- projectile contrast/trails remain visible over natural scenery,
- projectile travel timing remains unchanged,
- READY → START and inside-square judgment remain intact,
- result/retry/lobby flow remains reachable.

Fix visual/implementation defects directly. Do not change numerical combat balance or combo presentation from this validation.

---

# Next implementation slice — waiting-room UX
After v0.26 visual validation, implement the deferred TEAM waiting states without pretending networking already works.

## FRIEND
- waiting-room surface,
- local nickname/class/slot,
- reserved human slots,
- invite control placeholder,
- ready/start separate from connection state.

## LINK
- room/link presentation,
- truthful copy/share limitation before backend wiring,
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
- TEAM AI max remains +2,
- leaving waiting returns safely to play settings,
- combat never runs behind waiting UI.

---

# Following boundary — real multiplayer architecture
After waiting UX stabilizes:
- room creation/authority,
- shareable invite/link contract,
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

No retuning from lobby/HUD/readability observations.

## Still unresolved
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