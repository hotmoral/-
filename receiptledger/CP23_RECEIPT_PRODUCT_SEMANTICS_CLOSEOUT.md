# ReceiptLedger V1 — CP23 Receipt Product Semantics Closeout

Updated: 2026-10-16 KST
Status: **PASS / COMPLETE**

## 1. Boundary

- branch: `receiptledger/run-v1-receipt-product-semantics-20261016`
- frozen implementation HEAD: `5bffb66bd43814f8d638791b5697f79ff089028b`
- canonical Actions: `38822100885` — SUCCESS
- artifact: `12013477721`
- APK SHA-256: `e4e64f85f9700089b32f9f0b8121eef0a2f565d09b5428599d3717296c1b8324`
- version: `1.0.21-receipt-product-semantics` / versionCode 22

## 2. What CP23 accomplished

CP23 adds a deterministic, storage-independent semantic candidate layer over the existing receipt item name.

It can conservatively expose:

- explicit/known brand evidence;
- lexical product/family text;
- explicit parenthetical variant;
- package count / exact package measure candidates;
- raw purchase-form candidates;
- confidence, evidence and reason;
- ambiguity/review requirements.

It does not create or merge catalog identities.

## 3. Central product decision

A standalone physical unit is not sufficient to decide packaged-product specification versus commodity purchase form.

Therefore strings such as:

- `감자 1KG`
- `왕교자 1.05KG`
- `생수 2L`

preserve both defensible semantic readings and require review. CP23 does not manufacture certainty merely to raise automation metrics.

## 4. Quality result

Golden/parser evidence:

- 26 fixtures
- 68 expected fields
- 66 predicted fields
- 64 correct fields
- precision 96.9696%
- recall 94.1176%
- 10 ambiguous cases, 10/10 review-gated
- 2/2 no-invention negatives clean

The deliberate misses are part of the safety boundary: an unknown first-time brand is not inferred from position alone, and a free-form flavor/model suffix is not promoted to variant without explicit evidence.

## 5. Preserved contracts

No changes to:

- CP21 stable-ID identity authority;
- CP21 catalog domain source;
- CP22 product schema v2;
- receipt DB/schema v1;
- product persistence / identity runtime;
- receipt persistence runtime;
- Android manifest;
- permissions;
- receipt-derived price truth.

## 6. Superseded run

`38821795314` failed only because initial sorting code used API24+ Java collection convenience APIs under minSdk23. The compatibility issue was fixed without increasing minSdk or suppressing lint. Final lint is 0/0.

## 7. Downstream boundary

Next planned checkpoint: **CP24 — Identity Resolver V2**.

CP24 may consume CP23 evidence, but must independently define and prove identity-link authority. It must measure at least:

- false merge;
- false split / identity fragmentation;
- automatic link success;
- review-required rate;
- incorrect automatic decision rate;
- repeat-purchase reuse after prior confirmation.

CP23 confidence alone is never sufficient to merge/link a catalog entity.

## 8. Stop condition

CP23 is closed after canonical status/handoff synchronization. Do not start CP24 without explicit user authorization.
