# Mobi P1-C — Public 3D Cat Source / License Review

Date: 2026-10-16
Status: STAGE A / SOURCE-LICENSE REVIEW
Authority: public bounded analysis only; private `hotmoral/Mobi` remains canonical

## 1. Question

Identify a redistribution-safe domestic-cat 3D source that is good enough to justify a native 96x96 projection discriminator, without adopting 3D as Mobi's canonical representation.

## 2. Selection criteria

A candidate is eligible only if all are true:

1. exact source/provider is identifiable;
2. license is explicit and permits modification + redistribution + commercial use;
3. raw mesh is downloadable in a machine-readable format;
4. the source is a domestic/feline body rather than an anthropomorphic cat character;
5. morphology is not so stylized that failure would say nothing about realistic feline projection;
6. the first experiment can use the mesh without retopology, repainting, manual silhouette correction, or rig authoring.

## 3. Candidate review

### A. Innerscene — Standing cat — PRIMARY

- page: https://www.innerscene.com/tools/library/3d-parts/standing-cat-cda42538
- raw file named by provider: `cat-original.glb`
- format: GLB
- listed size: 4.7 MB
- listed dimensions: 310.4 x 794.7 x 746.7 mm
- listed nominal shoulder height: 390 mm
- description: smooth domestic shorthair, continuous sculpted body, digitigrade legs, small paws, pointed ears, curved upright tail
- rig: explicitly omitted
- fur strands: explicitly omitted
- provider status: Innerscene original model
- license: CC0 / public domain
- provider explicitly permits use, modification, redistribution, and commercial use without attribution
- library terms: https://www.innerscene.com/tools/library/terms

Disposition: **SELECT AS PRIMARY STATIC MORPHOLOGY SOURCE**.

Why: the absence of a rig is an advantage for the first discriminator because the test asks only whether already-authored feline morphology survives multi-view projection and 96x96 rasterization. It also avoids conflating rig quality with morphology quality.

### B. Innerscene — Domestic cat walking — BACKUP / POSE COMPARATOR

- page: https://www.innerscene.com/tools/library/3d-parts/domestic-cat-walking-4e8ff6c2
- raw file: `domestic-cat-walking.glb`
- format: GLB
- listed size: 870 KB
- listed dimensions: 0.536 x 0.210 x 0.430 m
- provider: Innerscene original model
- license: CC0 / public domain

Disposition: **RETAIN AS BACKUP / STATIC POSE COMPARATOR ONLY**.

Do not infer animation or rigging from the word “walking”; the page only establishes a GLB mesh in a walking pose.

### C. Innerscene — Domestic cat sitting — BACKUP / POSTURE COMPARATOR

- page: https://www.innerscene.com/tools/library/3d-parts/domestic-cat-sitting-c7caf7c2
- raw file: `domestic-cat-sitting.glb`
- format: GLB
- listed size: 828 KB
- listed dimensions: 0.315 x 0.224 x 0.420 m
- provider: Innerscene original model
- license: CC0 / public domain

Disposition: **RETAIN AS BACKUP / POSTURE COMPARATOR ONLY**.

### D. Quaternius / Poly Pizza cat — NEGATIVE/STYLE CONTROL, NOT PRIMARY

- page: https://poly.pizza/m/qKICY6xla2
- author: Quaternius
- format: FBX / glTF
- license: CC0
- classified by provider as low-poly and animated

Disposition: **DO NOT USE AS PRIMARY MORPHOLOGY SOURCE**.

Reason: redistribution is safe, but the strongly low-poly/stylized source would confound the core question. It remains useful later as a deliberately lower-detail control if needed.

### E. BlendKit Domestic Cat, Rigged — EXCLUDED FROM PUBLIC EXECUTION SOURCE

- page: https://www.blendkit.com/asset-gallery-detail/6b3bbcc7-db99-4424-9436-8e6678ee9354/
- listed polygon count: 11,056
- license: Royalty Free, not CC0

Disposition: **EXCLUDE FROM RAW-ASSET PUBLIC REPOSITORY/EXECUTION PATH**.

Reason: commercial use is allowed, but BlendKit's Royalty Free terms restrict reselling/redistributing the asset itself. Mobi's public bounded execution lane should prefer a source whose raw redistribution status is unambiguous.

## 4. Stage A result

> **PASS / REDISTRIBUTION-SAFE PRIMARY SOURCE FOUND**

Primary source for the next inspection stage:

> **Innerscene `Standing cat` / `cat-original.glb` / CC0**

Backups:

- Innerscene `Domestic cat walking`
- Innerscene `Domestic cat sitting`

## 5. Important limitations

Stage A does **not** establish:

- mesh vertex/triangle count;
- manifoldness or watertightness;
- mesh object count / materials / primitive count;
- coordinate axis orientation;
- exact source hash;
- rig/skin/animation details beyond what the page states;
- actual silhouette quality;
- 96x96 readability;
- suitability for mathematical reduction;
- canonical adoption.

Those require raw-file inspection and projection evidence.

## 6. Next boundary

Proceed only to **Stage B — raw GLB acquisition + immutable hash + structural inspection**.

Do not yet:

- render final 96x96 acceptance evidence;
- author a rig;
- animate walking;
- decimate/retopologize;
- manually correct silhouette;
- derive a generative mathematical model;
- modify private canonical state.
