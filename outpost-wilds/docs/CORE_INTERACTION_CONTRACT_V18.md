# Outpost Wilds — Core Interaction Contract V18

These behaviors are mandatory gameplay contracts, not optional presentation details. Any later client renderer must preserve them and the QA lane must fail when one is removed.

1. **Local action ranges are always rendered.** The local survivor has a gather radius and current-weapon auto-attack radius on the ground.
2. **Every active build/upgrade/repair project has a visible square contribution pad.** The pad boundary is rendered below world art; its label and remaining resource cost are rendered in the foreground so buildings cannot cover them.
3. **The growth mission drawer can never be blank while active projects exist.** It uses `snapshot.story.objectives` first and falls back to `snapshot.pads`.
4. **The local survivor is a ghost with respect to world objects.** Trees, rocks, facilities, walls, enemies, pads and props never modify player position or movement vector. Only world bounds constrain movement.
5. **Player movement speed is deterministic and constant.** Carry amount, gather state, construction state and nearby objects do not change speed.
6. **Players render in the foreground.** World objects and enemies render first; remote players render after them; the local player renders last.
7. **Nickname entry is required on session entry.** The chosen nickname is sent to the server and rendered above the survivor.
8. **Chat is modal with respect to action buttons.** When chat is open, the meat/ration action cannot overlap or block the chat composer/send control.
9. **Weapon progression is by weapon identity, not per-weapon numeric levels.** Shared upgrades replace the current weapon with the next named weapon in the lineage.
10. **Image-backed art is the canonical world presentation.** Character, monsters, resources, weapons, walls and facilities use independent transparent raster assets; facility levels use distinct files.

The canonical renderer exposes `window.__OW_CORE_RENDER_CONTRACT__` and calls `v18DrawInteractionGround()` and `v18DrawInteractionForeground()` every frame. Later patches must preserve or explicitly replace this contract with equivalent behavior plus updated regression coverage.
