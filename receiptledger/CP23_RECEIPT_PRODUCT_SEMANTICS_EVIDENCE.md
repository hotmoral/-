# ReceiptLedger V1 — CP23 Receipt Product Semantics Evidence

Updated: 2026-10-16 KST

## Canonical executable boundary

- branch: `receiptledger/run-v1-receipt-product-semantics-20261016`
- predecessor handoff: `913150c7acb06cb80a18833a10680657213239ec`
- frozen implementation HEAD: `5bffb66bd43814f8d638791b5697f79ff089028b`
- canonical Actions run: `38822100885` — SUCCESS
- job: `116720855010` — SUCCESS
- artifact ID: `12013477721`
- artifact name: `receiptledger-v1-receipt-product-semantics-38822100885`
- artifact digest: `sha256:fa22d082545adae7c414b0f1c089604174341f7e879c1acd5e4677e1dc2b7195`
- artifact expires: `2026-10-29T23:13:56Z`
- debug APK SHA-256: `e4e64f85f9700089b32f9f0b8121eef0a2f565d09b5428599d3717296c1b8324`

## Test / lint evidence

- `ReceiptProductSemanticParserTest`: 7/7 PASS, 0 skipped/failures/errors
- frozen `CatalogDomainV2Test`: 15/15 PASS
- frozen `CatalogPersistenceContractV2Test`: 7/7 PASS
- Android lint: 0 errors / 0 warnings (`No issues found.`)
- assembleDebug: PASS
- APK ZIP integrity: PASS
- forbidden-permission audit: PASS

Packaged permission output contains only the generated app-local dynamic-receiver-not-exported permission; CAMERA, broad media/storage, INTERNET and ACCESS_NETWORK_STATE remain absent.

## Semantic quality evidence

Exact canonical metric line:

`CP23_METRICS fixtures=26 expected_fields=68 predicted_fields=66 correct_fields=64 precision_ppm=969696 recall_ppm=941176 review_required=13 semantic_ready=13 ambiguous=10 ambiguous_reviewed=10 no_invention_negatives=2`

Interpretation:

- public-safe synthetic fixtures: 26
- field precision: 96.9696%
- field recall: 94.1176%
- review-required: 13
- semantic-ready: 13
- ambiguous cases detected: 10
- ambiguous cases review-gated: 10/10
- designated no-invention negatives: 2/2 clean

These are local deterministic parser-fixture metrics, not a claim of real-receipt field accuracy. CP35 remains the end-to-end real/sanitized receipt evaluation stage.

## Frozen behavior evidenced

- parsed semantic values are `PARSED_FROM_RECEIPT / UNCONFIRMED`;
- CP23 has no catalog-ID/merge authority;
- known-brand prefix or explicit bracketed brand evidence only; generic first-token brand guessing is forbidden;
- free-form variant suffixes are not guessed;
- explicit `입/개입` and multiplicative package expressions are parsed conservatively;
- standalone physical measures such as `1KG`/`1L` preserve both package-specification and purchase-form readings and require review;
- strong raw forms such as 봉/상자/단 are preserved without guessed conversion;
- context-sensitive 팩/개 remain review-gated;
- product schema remains 2;
- receipt schema remains 1;
- receipt-derived price truth remains unchanged.

## Superseded failed run

Run `38821795314` — FAILURE.

This run passed public-tree and scope/frozen-contract guards, but Android lint found four `NewApi` errors because the initial parser used `List.sort` / Java comparator convenience APIs treated as API 24+ while ReceiptLedger supports minSdk 23.

No semantic metric/evidence packaging ran in that attempt. The fix replaced only sorting implementation with API23-safe `Collections.sort` plus an explicit comparator. minSdk was not raised and lint was not suppressed.

Canonical successful evidence is run `38822100885` at `5bffb66...`.
