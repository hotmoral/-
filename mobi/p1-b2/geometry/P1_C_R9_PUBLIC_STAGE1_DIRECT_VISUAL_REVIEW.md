# Mobi P1-C-R9 — Public Stage 1 Direct Visual Review

Status: **FAIL / HARD FALSIFIER FIRED / NO R9 EXPANSION**  
Date: **2026-10-16**  
Public execution repo: `hotmoral/-`  
Public branch: `mobi/run-p1-c-r9-intrinsic-curve-pixel-raster-20261016`  
Accepted execution HEAD: `e3d3020b99a8aa92280bc42ad9cae48d92fc9346`

## 1. Scope reviewed

This review evaluates the frozen Stage 1 neutral/orientation evidence only.

The tested representation is:

`RF_K_BOUNDED_INTRINSIC_DEFORMABLE_CURVE_CARRIER_WITH_PIXEL_RASTERIZATION`

The test uses one body-local curve carrier for every tested yaw and deterministic 80x80 rasterization. It does not use authored PROFILE / 3Q / FRONT shape banks, angle-specific sprite assets, frame-specific corrections, motion-shape laws, morphology expansion, shading, texture or final-art rescue.

## 2. Accepted public execution

- workflow: `Mobi P1-C-R9 Curve Pixel Stage 1`
- run: `38872708322` — **SUCCESS**
- job: `116880341665` — **SUCCESS**
- artifact: `12034101138`
- artifact name: `mobi-p1-c-r9-curve-pixel-stage1-38872708322`
- artifact digest: `sha256:2dc9a02091232acb8136d2cd63d80900571d290586e940cc30c47a0a4e4b7d87`

All workflow stages passed: frozen input verification, unit tests, deterministic evidence generation, evidence validation, hashing and artifact upload.

## 3. Frozen carrier identity

- prototype version: `P1_C_R9_INTRINSIC_CURVE_PIXEL_V1`
- carrier signature: `1159a34a650543374666a161bd2890bcfaa31a96ee53b2a59e69e31f2bf2bf6e`
- curve groups: `15`
- body-local control nodes: `60`
- cubic curve segments: `15`
- native raster: `80 x 80`
- samples per cubic: `33`
- external domains: exactly `CORE / FORE_L / FORE_R / HIND_L / HIND_R / TAIL`

This is inside the frozen R9 capacity ceiling.

## 4. Mechanical result

Mechanical Stage 1 is **PASS**.

- bounded tests: **9/9 PASS**
- carrier signature remains one identity across tested yaw values
- profile / 3Q / front paw endpoint errors: exactly `0.0 dp` for all four paws
- deterministic rerender: `true`
- orientation steps: `13`
- max area jump ratio: `0.17028670721112077`
- max centroid step: `2.720578114348863 px`
- max adjacent XOR/union ratio: `0.35077881619937695`
- max connected component count: `3`
- minimum occupied pixels: `955`
- seed `1` / `777` evidence: byte-identical
- `mechanicalPass=true`

This establishes an important positive result:

> One bounded body-local curve carrier can drive deterministic 80x80 raster output through continuous 0°→90° orientation while preserving canonical neutral paw binding and without authored view assets.

Mechanical success does not establish CAT_ID or HEAD_BODY.

## 5. Profile review

Evidence: `P1CR9_M0_80_PROFILE.png`

Observed:

- the silhouette is coherent and compact at native scale;
- tail, body, head and four legs remain readable as separate gross regions;
- pixelization itself is stable and does not introduce severe noise;
- however the torso reads as a long near-rectangular plank;
- shoulder/chest, abdominal tuck and pelvis/haunch hierarchy are weak;
- limb origins read as near-vertical supports rather than feline anatomical emergence;
- head/neck integration is crude;
- ears carry a disproportionate amount of feline identity.

Disposition:

> **PROFILE CAT_ID is insufficient.**

The failure is primarily source-carrier form, not pixel quantization.

## 6. Three-quarter review

Evidence: `P1CR9_M0_80_THREE_QUARTER.png`

Observed:

- orientation is visibly different from profile and is generated continuously from the same carrier;
- the body narrows coherently with yaw;
- nevertheless the figure reads as a generic stylized quadruped;
- four limbs become parallel narrow columns;
- shoulder/chest and pelvis/haunch do not establish a feline-specific mass hierarchy;
- head/body relation remains weak;
- the binary image contains three connected components in this view, consistent with the mechanical metric;
- proximal limb emergence is not convincingly anatomical.

Disposition:

> **3Q CAT_ID / proximal emergence are insufficient.**

## 7. Exact-front review

Evidence: `P1CR9_M0_80_FRONT.png`

Observed:

- the intrinsic carrier does not geometrically collapse to zero width;
- rasterization is deterministic and stable;
- however the visible result becomes a narrow central vertical mass with two long leg columns;
- the head→neck→shoulder/chest→trunk hierarchy is not convincingly expressed;
- fore/hind origins do not separate into a natural feline frontal organization;
- the ears become the dominant cat cue.

Disposition:

> **EXACT-FRONT HEAD_BODY HARD FAIL.**

This directly fires a predeclared Stage 1 hard falsifier.

## 8. Ear-neutralized review

Evidence:

- `P1CR9_M0_80_EAR_NEUTRAL_3Q.png`
- `P1CR9_M0_80_EAR_NEUTRAL_FRONT.png`

Three-quarter without ears:

- silhouette remains mechanically coherent;
- the body reads as a generic small quadruped rather than specifically feline;
- head identity becomes especially weak.

Exact front without ears:

- feline identity effectively disappears;
- the figure reduces to a generic narrow body/head column with two visible leg columns;
- remaining mass organization is not sufficient to recover CAT_ID.

Disposition:

> **EAR-NEUTRALIZED CAT_ID HARD FAIL.**

This fires the second predeclared Stage 1 hard falsifier.

## 9. Orientation-strip review

Evidence: `P1CR9_M0_80_ORIENTATION_0_TO_90_STRIP.png`

Positive:

- the same carrier produces a visibly continuous profile→3Q→front transition;
- no catastrophic frame-to-frame raster popping is visible;
- the quantitative pixel-stability bounds also pass;
- this demonstrates that deterministic pixel quantization is compatible with continuous semantic orientation in a bounded prototype.

Negative:

- continuous transformation preserves a generic source form rather than creating feline specificity;
- the exact-front failure emerges gradually rather than as an abrupt sprite/view switch;
- orientation continuity therefore does not solve CAT_ID by itself.

## 10. Domain / proximal diagnostic

Evidence:

- `P1CR9_M0_80_DOMAIN_3Q.png`
- `P1CR9_M0_80_DOMAIN_FRONT.png`

The six declared domains remain mechanically separable and deterministic. However the visible limb carriers narrow into column-like structures and do not read as natural forelimb emergence from shoulder/chest or hindlimb emergence from pelvis/haunch.

Therefore:

> Domain correctness and paw pinning succeed, but proximal anatomical organization remains perceptually insufficient.

## 11. Causal interpretation

The evidence separates two questions cleanly.

### Demonstrated

1. deterministic 80x80 pixel rasterization is feasible;
2. one body-local curve carrier can support continuous profile→front orientation;
3. pixel quantization need not cause severe orientation popping;
4. canonical neutral paw endpoints can remain exact;
5. exactly six external domains can remain intact;
6. no authored runtime view bank is required for basic orientation continuity.

### Not demonstrated

1. the tested 15-curve / 60-node carrier carries enough feline-specific form;
2. exact-front HEAD_BODY is structurally convincing;
3. ear-neutralized CAT_ID is retained;
4. proximal limb emergence is naturally feline.

The decisive learning is:

> **Pixel rasterization successfully reduces display bandwidth, but it cannot rescue a structurally generic source carrier.**

The remaining causal problem is still how feline-specific visible form is authored/carried, not merely output resolution.

## 12. Hard-stop decision

The frozen Stage 1 scope declared hard stops for exact-front HEAD_BODY failure and material ear-neutralized CAT_ID collapse.

Both occurred.

Therefore do **not** run within R9:

- motion-shape law authoring;
- walking/running deformation evidence;
- 64/96px expansion;
- morphology expansion;
- Android/device integration;
- shading/fur/final-art rescue;
- coefficient/view-specific tuning of this carrier.

No R9 V2/V3 tuning loop is authorized after this accepted evidence.

## 13. Narrow Stage 1 disposition

> **FAIL / `TESTED_RF_K_NEUTRAL_CURVE_PIXEL_CARRIER_NOT_DEMONSTRATED`**

This is intentionally narrow.

It does **not** prove that:

- pixel art is unsuitable for Mobi;
- every intrinsic curve carrier fails;
- native pixel-part puppets fail;
- authored component-based pixel systems fail;
- a reference-authored richer curve grammar fails;
- motion-driven shape deformation fails;
- a reference-retopologized/subdivided source rendered to pixels fails.

Those are separate families or separate change-control questions.
