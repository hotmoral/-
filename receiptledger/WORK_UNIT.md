# ReceiptLedger public execution work unit

## Current stage

**CP21 — Catalog Domain V2 is COMPLETE.**

- branch: `receiptledger/run-v1-catalog-domain-v2-20261016`
- frozen implementation HEAD: `8596106c370e172161ef00e8d460dc78667bf80d`
- canonical implementation Actions: `38808985222` — SUCCESS
- artifact ID: `12008555521`
- artifact digest: `sha256:d4b84972d05d61941f08565fcc5537579bc7126798adb8c3771a442dca2ae8e9`
- APK SHA-256: `1fa055ead0b207f1404e673541f4a76585c014b3fba0bf2362186adb0180ebd6`
- Catalog Domain tests: 15/15 PASS
- lint: 0 errors / 0 warnings
- versionCode 20
- versionName `1.0.19-catalog-domain-v2`

Client alignment amendment commit:
`60f40f1eba0792bbcb5a3c08aa6724b4010297bd`

CI scope/trigger maintenance commit:
`94de4de3bef32e0165fd33810c9460ff6356b243`

Governance verification run:
`38812273375` — SUCCESS.

## Frozen CP21 contract

- STANDARD_PRODUCT vs NON_STANDARD_COMMODITY;
- no V2 entity for UNCLASSIFIED;
- stable ID is identity/equality authority;
- semantic fields/category/store do not silently merge entities;
- legacy IDs/names/types migrate without semantic guessing;
- global and merchant alias scopes are distinct;
- source/confidence/confirmation are independent;
- exact physical equivalence is limited to defensible units;
- package forms have no guessed conversion;
- commodity grouping != price comparability;
- purchase price truth remains receipt-traceable.

## Client-requirement amendment now governing downstream work

1. Measure false split/identity fragmentation as well as false merge; false merge remains higher severity.
2. CP23–CP26 measure relevant automatic-success, review-required and repeat-confirmation reuse locally.
3. CP27 defines canonical comparison-price semantics before statistics or labels.
4. UI execution order is CP29 Search/Browse -> CP30 Design System -> CP31 Product Detail -> CP32 Commodity Detail -> CP33 Capture/Review UX -> CP34 Commercial UI Shell.

## CI note

Runs `38811970256` and `38812118401` failed only because the old CP21 scope guard rejected the newly added canonical docs before test/build. They are not app regressions.

The workflow was minimally corrected and `38812273375` passed full validation. Future markdown-only handoff changes no longer auto-trigger the CP21 Android build.

## Next planned work unit

**CP22 — Persistence V2**

Required preflight before schema writes:

1. inventory current receipt/product DB schemas and lifecycle;
2. preserve every product ID and existing item link;
3. design migration sequencing/fail-closed behavior across separate databases;
4. define storage for merchant alias scope and CP21 structured semantics without duplicating price truth;
5. define indexes needed by future resolver/search/history workloads;
6. decide direct SQLite vs Room from concrete requirements;
7. create migration regression vectors before irreversible operations.

CP22 must not reinterpret CP21 or the client-alignment amendment.

## Group discipline

- recover canonical GitHub state;
- state essential goal/non-goals;
- inspect materially affected consistency risks;
- resolve cheap contradictions before implementation;
- avoid unrelated cleanup and over-broad architecture work;
- implement the smallest coherent proof;
- run scoped CI/evidence for executable changes;
- freeze exact refs;
- synchronize handoff/status materials;
- stop before the next unauthorized checkpoint.

## Public/privacy rules

Modify only `receiptledger/**` and explicitly approved ReceiptLedger-prefixed workflows.

Never include secrets, signing material, real private receipt photos, personal purchase DBs/backups, personal identifiers or uncleared assets.

APK permission firewall remains no CAMERA, broad media/storage, INTERNET or ACCESS_NETWORK_STATE permission unless explicitly reauthorized.

## Stop condition

**CP21 plus client-requirement alignment are complete and synchronized. Await explicit authorization for CP22.**
