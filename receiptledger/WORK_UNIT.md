# ReceiptLedger public execution work unit

Updated: 2026-10-16 KST

## Current stage

**CP32 — Commodity Detail is COMPLETE.**

- branch: `receiptledger/run-v1-commodity-detail-20261016`
- predecessor handoff: `1025f3d4f319ae6924bcf5012797b879757434fe`
- frozen implementation HEAD: `e42629ccd66a80a4a1a14de0c7798b178d6b0062`
- canonical Actions: `38855942283` — SUCCESS
- job: `116827303606` — SUCCESS
- artifact ID: `12027322130`
- artifact digest: `sha256:ce1ae60e5a9e5295359f433a85417b2efc5a39bca95b29b2480e82e7154f4a9b`
- APK SHA-256: `320379024800e5c0ee441656ea8d28bef20ac2ee0377332190b770645c8606d2`
- CP32 tests: 11/11 PASS
- CP31 9/9, CP30 9/9, CP29 8/8, CP28 8/8, CP27 8/8, CP26 8/8 PASS in packaged XML evidence
- full prior regression suite required by workflow
- lint: 0 errors / 0 warnings
- versionCode 31
- versionName `1.0.30-commodity-detail`

## Frozen CP32 contract

- NON_STANDARD commodities only;
- Commodity Detail is a read-only projection over canonical catalog/CP27/CP28/receipt data;
- no duplicate mutable price truth or conversion table;
- stable catalog ID remains identity authority;
- real latest purchase remains distinct from latest strict-comparable observation;
- WEIGHT_KG / VOLUME_L / EACH are independent strict comparison bases;
- each strict basis owns its own latest/previous/usual/CP28 judgment/chart;
- LIKE_FORM remains one reference-only cohort per preserved package/form key;
- contextual forms always remain unjudged and receive no judgment-colored chart;
- no fake normalization such as bag/box/bundle -> kg/L/each;
- excluded observations remain provenance and never enter judgment/chart values;
- every rendered purchase row preserves receipt navigation;
- product schema 2 / receipt schema 1 unchanged.

## Commercial UI result

Design direction:

**quiet confidence / price-first / evidence-backed**

NON_STANDARD rule:

**clarity before apparent simplicity**

Compact hierarchy:

`commodity identity -> real latest purchase -> strict comparable prices -> contextual reference forms -> purchase history`

CP30 typography/spacing/radius/elevation/semantic/responsive grammar is reused rather than forked.

History rows are >=64dp. Strict charts expose Korean accessibility summaries, reuse Path allocation, use Android nonlinear-font-scaling-safe SP conversion and call the single-basis chart guard.

Expanded two-pane remains gated by CP30: width >=840dp and height >=480dp.

## Local quality evidence

`CP32_METRICS commodity_detail_version=1 strict_basis_kinds=3 contextual_policy=1 grouping_not_comparability=1 responsive_cases=6 traceability=1 chart_single_basis=1 strict_sections=2 contextual_sections=2 purchase_rows=9`

Canonical artifact inspection confirms:

- APK SHA above;
- lint `No issues found.`;
- CP32/31/30/29/28/27/26 packaged test XMLs all have zero failures/errors/skips;
- packaged permissions contain only the internal dynamic-receiver permission.

## Pre-closeout corrections

CP32 was not closed at the first green state.

1. initial CI `38855330418` found an invalid CP30 spacing-token reference;
2. `69b6c3d...` corrected it and run `38855551821` became green;
3. plan/code/lint review found two `SetTextI18n` warnings and rejected that green run for closure;
4. final `e42629cc...` moved text composition into string resources and strengthened CI to require clean lint;
5. canonical run `38855942283` passed all gates.

## Integration boundary

Legacy Price History routes STANDARD to CP31 Product Detail and NON_STANDARD to CP32 Commodity Detail.

`MainActivity` was not changed. The user explicitly chose to keep complete launcher/home/navigation integration in CP34 rather than add temporary navigation now.

## Known limitations

- CP33 Capture/Review UX V2 not built;
- CP34 commercial shell/navigation not built;
- current launcher remains the existing OCR-development entry;
- final icon artwork/library and dark-theme finalization remain open;
- CP32 does not include emulator/device screenshot comparison or real-user usability evidence.

## Next planned work unit

**CP33 — Capture / Review UX V2**

Before implementation:

1. recover CP32 frozen and handoff refs separately;
2. re-read capture/OCR/review/validation/identity/provenance contracts materially relevant to the front-half flow;
3. measure where review burden is actually created before redesigning screens;
4. distinguish auto-confirmed, review-required and unresolved outcomes clearly;
5. preserve raw OCR/receipt evidence and edit provenance;
6. reduce repeated manual work for already confirmed identities where frozen resolver evidence allows it;
7. never auto-confirm ambiguous identity merely for fewer taps;
8. preserve price eligibility/discount attribution rules;
9. consume CP30 design grammar and existing commercial-quality bar;
10. do not build CP34 home/navigation shell in the same checkpoint;
11. finish scoped CI/evidence/handoff and stop before CP34.

## Group discipline

- recover canonical GitHub state;
- restate essential goal/non-goals;
- inspect materially relevant contradictions;
- fix cheap contract gaps before closure even if CI is green;
- avoid unrelated cleanup/speculative scope;
- implement smallest coherent proof;
- run scoped CI/evidence;
- freeze exact refs;
- synchronize handoff materials;
- verify post-boundary changes are documentation-only;
- stop before next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows. Never commit secrets, signing material, private receipt photos, personal purchase DBs/backups, identifiers or uncleared assets.

Forbidden APK permissions remain CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE unless explicitly reauthorized.

## Stop condition

**CP32 is complete. Await explicit authorization for CP33.**
