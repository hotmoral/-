# ReceiptLedger Post-V1 — CP37 Physical Device OCR Validation Consistency Review

Updated: 2026-10-17 KST
Checkpoint: CP37

## 1. Predecessor consistency

CP37 starts from current docs-only handoff `d0a3a9ec7658808c82247715d58ac106a3778186` while preserving frozen CP36 executable `78cdd99c7df8fcdff2765a4e7e66b428397e7cf4` as the behavior baseline.

CP37 does not reopen CP20–36 domain decisions. It exists solely because CP35/36 explicitly left physical-device / real-image OCR evidence unresolved.

## 2. Evidence-boundary consistency

CP35 proved downstream purchase-registration behavior only from synthetic token/geometry input. CP36 measured emulator OCR latency but explicitly refused to trade accuracy for emulator speed without real-image evidence.

CP37 therefore must measure the same existing production path rather than substitute a new OCR path before baseline evidence exists.

## 3. Privacy consistency

Receipt images and recognized text can contain private purchase information. Public-repo evidence must therefore be sanitized by construction.

Allowed report data is structural/aggregate only: timings, dimensions, pass counts, enum/state labels, correction counts and booleans.

Forbidden report data includes OCR text, store/product/date/price values, receipt IDs, product IDs, file paths/URIs and image data.

No automatic upload, INTERNET permission or analytics SDK is allowed.

## 4. Permission consistency

The existing app intentionally avoids CAMERA and broad media/storage permissions by delegating camera capture to an external camera app and image selection to the system document picker.

CP37 must preserve this posture. A physical-device campaign is not justification to add direct camera or storage permissions.

## 5. Review/provenance consistency

CP33 defines when a receipt requires review. CP37 may observe that decision but must not weaken or reimplement it.

For validation, the user must visually inspect even AUTO_CONFIRMED samples. Corrections continue through the existing review/edit flow so user provenance remains the same as normal app behavior.

A correction after an initial AUTO_CONFIRMED decision is evidence of a safety gap; instrumentation must not suppress that fact.

## 6. OCR/recovery consistency

Frozen baseline:

- `MlKitOcrEngine` owns one Korean `TextRecognizer` instance and reuses it;
- `OcrRecoveryEngine` may run ORIGINAL, CONTRAST and BINARY passes, bounded by `MAX_PASSES=3`;
- `ReceiptRecognitionPipeline` chooses/merges candidates;
- MainActivity consumes the final `RecoveryResult`.

Phase A instrumentation may time and count these operations but must not change recognition options, pass ordering, preprocessing or candidate selection.

## 7. Correction-delta semantics

The initial baseline for a sample is the `ReceiptRecord` created immediately from OCR/recovery before any review/edit interaction.

The final record is the record immediately before durable save after all user corrections/confirmations.

Sanitized deltas compare only equality/change state:

- store name changed? yes/no;
- purchase date changed? yes/no;
- printed total changed? yes/no;
- discount sum changed? yes/no;
- item count changed? count delta/boolean;
- per-ordinal name/quantity/unit-price/line-amount changed counts.

The report must never serialize either before or after values.

## 8. Identity/price consistency

CP37 instrumentation must not inspect or export stable product IDs, exact aliases or price-history values. Post-save exact-alias reuse remains existing CP33 behavior and is outside CP37's report payload.

The product schema remains 2; receipt schema remains 1.

## 9. UX isolation

Any validation affordance should be limited to debug builds. Preferred behavior is a post-save `검증 결과 복사` control available only when the installed application is debuggable.

No validation instrumentation should alter the normal save enablement, review requirements or Home/search/detail navigation.

## 10. Failure handling

Instrumentation must not turn successful save into failure. Report construction/copy must occur after durable save and must be non-authoritative.

If report generation fails, the receipt save remains successful.

OCR failures may expose only sanitized error class/category if reporting them is needed; exception messages that may contain provider/path details must not be serialized.

## 11. Performance measurement integrity

The elapsed timer must start immediately before the existing `OcrRecoveryEngine.recognize(...)` call and stop at its final callback. It therefore measures the full current OCR/recovery operation, including additional passes when triggered.

UI selection/image decode/document detection are intentionally outside this OCR/recovery latency metric unless separately labeled.

## 12. Scope-creep guard

Phase A does not justify:

- OCR optimization;
- new analytics storage;
- release pipeline work;
- new permissions;
- UI redesign;
- schema migration;
- new identity/search/price behavior.

If instrumentation exposes a separate material defect, document it first and decide whether it belongs in CP37 before implementing.

## 13. Conclusion

A small, debug-only, sanitized instrumentation layer around the frozen capture/review path is consistent with CP20–36 contracts and is the lowest-cost way to resolve the remaining OCR evidence gap.
