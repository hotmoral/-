# ReceiptLedger V1 — CP36 Performance / Reliability Vectors

Updated: 2026-10-16 KST
Version: 1.0.0

## 1. Measurement profile

CP36 records both deterministic structural evidence and Android runtime evidence.

Runtime metrics are taken on the canonical GitHub Actions emulator profile declared in the CP36 workflow. The profile, API level, ABI and memory allocation are part of the evidence and must be frozen with the run.

Timing samples use monotonic clocks. Setup/population time is not included in the user-path measurement unless the setup itself is the behavior under test.

## 2. JVM vectors

### JV-01 — CP29 structural amplification 1k

Fixture:

- 1,000 classified products;
- one linked receipt/item per product;
- one exact canonical-name query.

Verify:

- correct single exact result;
- one catalog enumeration;
- per-product metadata/link/receipt reads are counted;
- result ordering/ranking matches frozen CP29 semantics.

### JV-02 — CP29 structural amplification 10k

Same shape at 10,000 products.

Verify exact result and deterministic call ratios. Record 10k/1k amplification.

### JV-03 — recent/frequent scale

10,000 products with deterministic recency/frequency distribution.

Verify top results exactly and record read amplification.

### JV-04 — long price history

One STANDARD product with 1,000 linked valid receipts.

Verify:

- all 1,000 observations remain receipt-traceable;
- newest/previous/cohort count are correct;
- CP28 baseline still uses only the frozen previous max-five rule;
- Product Detail returns complete history.

### JV-05 — deterministic recovery

Run the same synthetic `OcrDocument`/recognition candidate through the frozen recovery/selection path repeatedly and require identical selected status, score and structured output every time.

No random or timing-dependent semantic result is permitted.

## 3. Android runtime vectors

### AR-01 — Home cold start

- clean installed app;
- force-stop between samples;
- launch `.HomeActivity` with `am start -W`;
- at least five measured samples after one non-recorded priming launch when needed for package/runtime initialization.

Record median and maximum `TotalTime` plus process PSS after idle.

Decision budget: median <=2,500 ms, max <=5,000 ms, PSS <=220 MiB.

### AR-02 — Bundled Korean OCR

Generate a public-safe synthetic receipt bitmap in memory and run production `MlKitOcrEngine`.

Record:

- first completed recognition latency;
- at least three warm recognition samples;
- warm median;
- PSS before/after OCR;
- non-empty recognized document requirement.

Decision budget: cold <=5,000 ms, warm median <=1,500 ms.

Accuracy beyond non-empty successful processing is not claimed by this vector.

### AR-03 — SQLite search 1k

Populate production receipt/product SQLite schemas with 1,000 deterministic products, links and receipts in a setup transaction. Then instantiate the frozen production stores/services and time an exact CP29 search.

Decision budget <=750 ms.

### AR-04 — SQLite search 10k

Same shape at 10,000 products.

Decision budget <=3,000 ms. Record 10k/1k ratio.

### AR-05 — SQLite recent 10k

Run frozen `recent(3)` over the same 10k data shape.

Decision budget <=3,000 ms and exact newest IDs required.

### AR-06 — Long price/detail history

One STANDARD product with 1,000 linked valid receipt observations.

Measure:

- `PriceIntelligenceServiceV2.analyze()`;
- `ProductDetailServiceV1.load()`.

Each path must preserve 1,000 exact source receipt rows. User-facing detail load budget <=2,000 ms.

### AR-07 — 1,000-point chart draw

Feed the AR-06 Product Detail into `ProductPriceChartViewV1`, measure/layout at a fixed size and draw to an in-memory bitmap/canvas.

Decision budget <=500 ms. No point/basis mutation allowed.

### AR-08 — product catalog migration 1 -> 2

Create a schema-1 fixture with 1,000 products, aliases and representative item links; set DB user version to 1; open through production `SqliteProductCatalogStore`.

Verify:

- schema version becomes 2;
- all product IDs/names/types remain;
- every old alias resolves as GLOBAL to the same product ID;
- item links remain intact;
- V2 tables/indexes exist;
- migration <=5,000 ms.

### AR-09 — unsupported migration fail-fast

Invoke the migration contract with unsupported version endpoints and require `IllegalStateException`; no destructive fallback.

### AR-10 — archive reconcile scale

Create approximately 2,000 archive entries/files containing a deterministic mixture of:

- live canonical image names;
- orphan canonical image names;
- temp names.

Run `ReceiptImageArchive.reconcile(liveIds)`.

Verify all live files remain, all orphan/temp files are removed, count is exact, and runtime <=2,000 ms.

### AR-11 — repository close/reopen/delete

Save one synthetic receipt + bitmap through `ReceiptRepository`, close, reopen, load record and sampled image, then delete.

Verify:

- durable record and image agree after reopen;
- delete removes both;
- second image deletion/reconcile is safe/idempotent;
- no fabricated record appears when image is missing.

### AR-12 — repeated runtime stability

Repeat bounded open/search/detail/close cycles and require no exception or persistent-state drift. This is a bounded reliability check, not a leak-proof formal proof.

## 4. Result classification

For every vector report one of:

- `PASS_WITHIN_BUDGET`
- `PASS_SEMANTIC_BUT_SLOW`
- `FAIL_RELIABILITY`
- `INFRA_NOT_MEASURED`

`PASS_SEMANTIC_BUT_SLOW` requires post-measurement root-cause analysis before CP36 closeout.

## 5. Optimization decision record

If CP36 introduces any production hardening, evidence must include before/after values for the exact failing vector and prove unchanged CP29/27/28/31/32/33 semantics through regression tests.
