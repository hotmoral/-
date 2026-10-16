# Mobi — Authored Pixel Animation Asset Budget and Pruning Analysis

Status: **PUBLIC ANALYSIS / NON-CANONICAL / NO IMPLEMENTATION DECISION**  
Date: **2026-10-16**

## 1. Goal

Quantify how large an authored pixel-animation system could become, then identify where additional directions/frames/behaviors stop buying visible value.

This is a planning model, not a final asset count.

## 2. Counting unit

Use **full-frame equivalent (FFE)** as the neutral counting unit.

One FFE = one complete raster animation frame for one growth stage, one direction and one clip role.

Paired cat-cat interactions count both synchronized roles.

Overlay/micro clips count as FFE here only to keep arithmetic comparable; real storage may be lower if partial layers are used.

## 3. Three portfolio envelopes

These envelopes intentionally span a wide range.

### 3.1 Lean feasibility portfolio

Per growth stage planning model:

| Family | actions | directions | frames | roles | FFE/stage |
|---|---:|---:|---:|---:|---:|
| locomotion | 3 | 16 | 16 | 1 | 768 |
| locomotion transitions | 3 | 8 | 8 | 1 | 192 |
| posture/rest | 6 | 4 | 10 | 1 | 240 |
| grooming | 3 | 4 | 16 | 1 | 192 |
| exploration | 4 | 8 | 10 | 1 | 320 |
| play | 3 | 8 | 12 | 1 | 288 |
| user interaction | 3 | 4 | 10 | 1 | 120 |
| cat-cat paired | 3 | 4 | 12 | 2 | 288 |
| environment | 2 | 8 | 10 | 1 | 160 |
| micro | 5 | 1 | 6 | 1 | 30 |

Total: **2,598 FFE/stage**, **10,392 FFE across four stages**.

This is enough to test the authored-animation architecture but too narrow for the intended long-term Mobi behavior richness.

### 3.2 Balanced portfolio hypothesis

Per growth stage planning model:

| Family | actions | directions | frames | roles | FFE/stage |
|---|---:|---:|---:|---:|---:|
| locomotion | 4 | 24 | 24 | 1 | 2,304 |
| locomotion transitions | 4 | 12 | 10 | 1 | 480 |
| posture/rest | 10 | 8 | 12 | 1 | 960 |
| grooming | 6 | 4 | 24 | 1 | 576 |
| exploration | 6 | 8 | 14 | 1 | 672 |
| play | 6 | 8 | 16 | 1 | 768 |
| user interaction | 6 | 8 | 12 | 1 | 576 |
| cat-cat paired | 6 | 8 | 14 | 2 | 1,344 |
| environment | 4 | 8 | 14 | 1 | 448 |
| micro | 8 | 1 | 6 | 1 | 48 |

Symmetric upper estimate: **8,176 FFE/stage**, **32,704 FFE across four stages**.

This is not a proposal to author exactly 32,704 frames. It is the useful middle reference envelope before stage-specific pruning and mirror reuse.

### 3.3 Premium / stress envelope

Per growth stage planning model:

- locomotion: 6 actions × D36 × F32;
- locomotion transitions: 6 × D24 × F16;
- posture/rest: 14 × D12 × F18;
- grooming: 10 × D8 × F32;
- exploration: 10 × D16 × F20;
- play: 10 × D16 × F24;
- user interaction: 10 × D12 × F18;
- cat-cat paired: 10 × D12 × F24 × 2 roles;
- environment: 8 × D16 × F20;
- micro: 12 × D1 × F8.

Result: **32,416 FFE/stage**, **129,664 FFE across four stages**.

This is a useful stress ceiling, not a sensible starting target. It shows why uniform premium density rapidly becomes expensive.

## 4. Stage-specific sparse balanced model

A more realistic portfolio does not expose every action equally at every growth stage.

Example availability counts using the balanced density assumptions:

| Family | G1 | G2 | G3 | G4 |
|---|---:|---:|---:|---:|
| locomotion | 3 | 4 | 4 | 4 |
| locomotion transition | 3 | 4 | 4 | 4 |
| posture/rest | 8 | 9 | 10 | 10 |
| grooming | 3 | 5 | 6 | 6 |
| exploration | 5 | 6 | 6 | 6 |
| play | 6 | 6 | 6 | 5 |
| user interaction | 5 | 6 | 6 | 6 |
| cat-cat paired | 4 | 5 | 6 | 6 |
| environment | 3 | 4 | 4 | 4 |
| micro | 8 | 8 | 8 | 8 |

Resulting illustrative FFE:

- G1: **6,232**
- G2: **7,760**
- G3: **8,176**
- G4: **8,048**
- total: **30,216 FFE**

This already lowers the balanced symmetric model from 32,704 to 30,216 without reducing quality where it matters.

## 5. Mirror-reuse ceiling

For a perfectly mirrorable full-circle directional bank with even direction count `D`, horizontal/vertical reflection pairing can theoretically reduce the unique authored headings to roughly:

`D / 2 + 1`

Examples:

- D8 → 5 unique headings;
- D12 → 7;
- D16 → 9;
- D24 → 13;
- D36 → 19.

This is a **theoretical body-base authoring ceiling**, not an unconditional rule.

Mirroring is only valid when:

- anatomical L/R metadata is swapped correctly;
- coat/accessory asymmetry is not baked into the body frame or is handled separately;
- the action itself is mirror-symmetric;
- paired interactions do not encode a fixed asymmetric role that breaks reflection.

If every eligible direction in the three planning envelopes were mirror-reused, the FFE counts would fall approximately to:

- Lean: **10,392 → 6,768** (34.9% reduction)
- Balanced: **32,704 → 19,952** (39.0% reduction)
- Premium: **129,664 → 73,504** (43.3% reduction)

For the stage-sparse balanced example, the same theoretical maximum gives about **18,402 unique authored FFE** from 30,216 runtime directional FFE.

Actual savings will be lower because not every clip should be mirrored.

## 6. Candidate growth sizes and raw decoded memory

Working size hypothesis only:

- G1 64×64: 16 KiB/frame in raw RGBA;
- G2 72×72: ~20.25 KiB/frame;
- G3 84×84: ~27.56 KiB/frame;
- G4 96×96: 36 KiB/frame.

If all frames of the stage-sparse balanced example were decoded simultaneously, raw RGBA would be roughly **754 MiB**. Under the theoretical mirror-authoring ceiling it would still be roughly **459 MiB**.

Therefore the runtime architecture must **not** load the entire animation library as decoded textures.

Required runtime principle if this family is selected:

> load only the active growth stage and a small working set of action atlases; evict inactive banks.

## 7. Disk/package size must be measured, not guessed

PNG/palette compression varies heavily with:

- transparency;
- palette size;
- per-frame visual complexity;
- atlas packing;
- duplicate regions;
- compression format chosen for Android distribution/runtime.

For planning sensitivity only, if compressed storage averaged:

| Avg compressed bytes/frame | Lean 10,392 | Balanced 32,704 | Premium 129,664 |
|---:|---:|---:|---:|
| 1 KiB | ~10 MiB | ~32 MiB | ~127 MiB |
| 2 KiB | ~20 MiB | ~64 MiB | ~253 MiB |
| 4 KiB | ~41 MiB | ~128 MiB | ~507 MiB |
| 8 KiB | ~81 MiB | ~256 MiB | ~1,013 MiB |

These are not forecasts. A real prototype atlas must be encoded and measured before package-size decisions.

## 8. Direction-density pruning

Do not select a global direction count.

### Primary locomotion experiment

Compare at native scale:

- D8 — coarse baseline;
- D12 — 30°;
- D16 — 22.5°;
- D24 — 15°;
- D36 — 10°;
- optionally D48 only if D36 still shows visible directional stepping.

Pruning rule:

> choose the lowest direction count whose increase to the next tier does not create a meaningful improvement in perceived heading, silhouette continuity, gait readability or transition quality.

Likely high-value comparison: **D16 vs D24 vs D36**. Do not assume the winner in advance.

### Lower-direction families

Posture, grooming, rest and many social actions should test D4/D8/D12 rather than inherit locomotion density.

## 9. Frame-density pruning

For one representative high-quality walk cycle at each candidate native scale, compare:

- F12;
- F16;
- F24;
- F32.

For long expressive actions such as grooming/stretch, separately test F24/F32/F48 where duration justifies it.

Pruning rule:

> choose the lowest authored frame count whose increase to the next tier produces no meaningful improvement in paw contact, shoulder/haunch motion, body rhythm, tail continuity or loop seam quality.

Playback timing may be continuous even when authored frame count is finite.

## 10. Behavior-breadth pruning

Separate candidate actions into four product tiers.

### Tier A — identity/core

Must exist early if this family is pursued:

- idle stand;
- normal walk;
- walk start;
- walk stop;
- turn/orient;
- stand→sit;
- sit idle;
- sit→stand;
- lie/rest;
- basic jump/landing if Mobi requires vertical environment interaction.

### Tier B — life simulation

High-value richness:

- sleep/wake;
- yawn/stretch;
- grooming family;
- sniff/look/investigate;
- basic play/pounce;
- user approach/avoid/attention response.

### Tier C — relationship expression

Required to make long-term user-cat/cat-cat state meaningful:

- nuzzle/rub;
- trust-based rest;
- cat-cat greeting;
- sit/lie near;
- play invitation/chase;
- mutual grooming;
- retreat/conflict-resolution variants.

### Tier D — luxury/rare

Add only after coverage metrics show value:

- rare tumbles;
- elaborate grooming chains;
- multiple equivalent yawn/stretch variants;
- rare failure/recovery actions;
- specialized environment tricks.

## 11. Four-stage differentiation pruning

Do not duplicate every action four times purely because four growth stages exist.

For each action classify:

- `UNIQUE_MOTION`: stage needs genuinely different choreography;
- `TIMING_VARIANT`: same motion structure but different cadence/amplitude;
- `ART_VARIANT`: same choreography/contact timing, separately drawn proportions;
- `SHARED`: no visible benefit from stage-specific version;
- `UNAVAILABLE`: not part of that stage's repertoire.

Strong candidates for `UNIQUE_MOTION` in G1/G2:

- basic walk/scamper;
- stop/turn balance;
- pounce/tumble;
- jump/landing;
- sit/lie transitions;
- some grooming due body proportions/coordination.

Strong candidates for shared choreography with stage-specific art:

- blink;
- slow blink;
- simple look;
- basic breathing;
- some user orient/attention reactions.

## 12. Cat-cat interaction explosion control

Do not author a unique pair clip for every `(growthA × growthB × relationship × direction)` combination.

Preferred model:

1. paired action defines `ROLE_A` and `ROLE_B`;
2. each role has contact markers and timing events;
3. runtime aligns the two cats using those markers;
4. growth-stage role variants are authored only where size/proportion differences visibly require them;
5. relationship state chooses which paired action is allowed, not a separate animation bank.

This turns pair behavior from combinatorial multiplication into synchronized reusable roles.

## 13. State-to-animation architecture

Behavioral complexity must not become animation-asset complexity.

Recommended separation:

`behavior state` → `intent/action` → `clip family + direction + growth variant` → `transition clip` → `frame/event metadata`.

Examples:

- user trust changes **whether** the cat approaches or avoids; it does not require a unique `walk_trust_0.73` clip.
- cat-cat affinity changes greeting/play/conflict selection; it does not require duplicate locomotion.
- energy changes action selection and playback timing within bounded limits; it should not automatically multiply cycle banks.

## 14. Provisional pruning result

Not a final product decision, but the current efficient search space is:

### Growth

- keep **4 stages** as the working architecture;
- exact visual sizes remain open, with ~64/72/84/96 px as one test ladder.

### Direction

- primary locomotion: test **D16 / D24 / D36** as the main quality-cost frontier, retaining D8/D12 as lower baselines;
- posture/social: primarily D8/D12 with D4 baseline;
- rest/groom: D4/D8 first;
- micro: D1/local overlay where valid.

### Frames

- walk: test **F16 / F24 / F32**, with F12 baseline;
- run/quick transitions: F8–F16;
- posture transitions: F12–F24;
- long grooming/expression: F24–F48+, only when duration requires it.

### Portfolio

- Lean ~10k FFE is a feasibility-sized library;
- Balanced sparse ~30k runtime FFE / potentially ~18k–20k unique base authored FFE with aggressive valid mirroring is a plausible mid-range planning target;
- Premium ~130k FFE is a stress ceiling and should be avoided unless user-visible benefit is demonstrated.

## 15. Next experiment recommended

Do **not** build all four stages or dozens of behaviors yet.

Use one representative adult or near-adult body and create a controlled comparison for **one normal walk cycle**:

- direction: D12 / D16 / D24 / D36;
- frame density: F12 / F16 / F24 / F32;
- same art quality and gait reference;
- native pixel scale;
- inspect direction stepping, gait realism, contact, loop seam and authoring cost.

Then perform the same style of threshold experiment on one posture transition and one low-direction action.

This determines Mobi-specific density thresholds before asset multiplication begins.