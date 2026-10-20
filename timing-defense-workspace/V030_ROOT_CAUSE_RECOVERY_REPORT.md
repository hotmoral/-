# Timing Defense v0.30 — Root Cause Recovery Report

Updated: 2026-10-20 KST

## Summary
v0.27 introduced a DOM observer regression in the skill-level normalization path. The observer rewrote each `.v024SkillLv` text node on every callback even when the final text was already identical. Because the observer watched `childList` changes across the lobby subtree, its own `textContent` rewrite could retrigger the observer indefinitely.

Problematic v0.27 logic:

```js
function normalizeSkillLevels(){
  root?.querySelectorAll('.v024SkillLv').forEach(el=>{
    const n=(el.textContent||'').match(/\d+/)?.[0]||'';
    if(n) el.textContent=`습득 LV ${n}`;
  })
}
new MutationObserver(normalizeSkillLevels).observe(root,{childList:true,subtree:true});
```

By contrast, the earlier v0.26 normalizer had an equality guard and only changed text when the value was actually different.

## Why v0.28 / v0.29 were the wrong recovery direction
The half-render / black-right-side symptom was initially treated as a viewport/orientation failure. v0.28 and v0.29 therefore added increasingly aggressive viewport repair logic. After code audit, the first new severe regression boundary is v0.27 and the infinite observer loop is a concrete implementation defect capable of starving normal rendering/event progress. The viewport patches therefore addressed a symptom before the underlying loop was removed.

## v0.30 recovery strategy
v0.30 intentionally returns to the last known-good layout/viewport foundation and keeps the desired v0.27 UX features.

Loader order:
1. existing v0.26 stack,
2. `v030-safety.js`,
3. existing `v027-polish.js`.

`v030-safety.js` intercepts only the specific redundant `normalizeSkillLevels` MutationObserver before v0.27 creates it. The safe v0.26 skill-level normalizer remains active and already produces the required `습득 LV N` output with an equality guard.

v0.28 and v0.29 viewport-repair scripts are **not loaded** by v0.30.

## Orientation contract
Timing Defense remains landscape-only.

v0.30 uses a simple portrait-only full-screen gate with maximum z-index. It does **not**:
- rewrite viewport meta width,
- force numeric screen widths,
- compare physical/CSS pixel widths,
- resize the lobby/canvas based on screen metrics.

This prevents orientation handling from modifying an otherwise correct landscape layout.

## Preserved v0.27 features
- one-line skill names,
- one-line `습득 LV N`,
- corrected radar aspect ratio,
- Android horizontal swipe navigation,
- fixed arrow navigation,
- result-board PLAYER / CLASS collision fix,
- truthful local TEAM waiting-room UI for FRIEND / LINK / RANDOM.

## Regression guards
- Combo visual/logic remains untouched.
- Combat coefficients remain untouched.
- Projectile travel timing remains untouched.
- Actual multiplayer remains unimplemented; local waiting UX must not be presented as network connectivity.

## Device validation required
On the same Samsung Browser device:
1. open v0.30 directly in landscape,
2. confirm full-width lobby rendering,
3. confirm no progressive freeze/partial paint,
4. verify arrow + swipe class navigation,
5. verify radar and skill cards,
6. rotate to portrait and confirm only the orientation gate is shown,
7. rotate back to landscape and confirm full-width lobby returns,
8. verify result board and TEAM waiting UI.

If v0.30 still renders half-width, collect the new screenshot before adding any further viewport manipulation. The next diagnosis must start from the clean v0.30 chain rather than v0.28/v0.29 heuristics.
