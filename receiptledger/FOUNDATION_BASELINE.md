# ReceiptLedger V1 Foundation Baseline

Branch: `receiptledger/run-v1-foundation-20261015`

Purpose: prove a clean public Android build/test/APK pipeline before adding OCR, camera, parser, persistence, or real application features.

## Public material in this work unit

- minimal Android application source
- one deterministic JVM contract test
- public-tree safety audit script
- ReceiptLedger-only GitHub Actions workflow
- generated debug APK and build metadata

## Explicit non-goals

- OCR
- camera/gallery import
- receipt parsing
- database/persistence
- real receipt fixtures
- production UI
- release signing
- existing v0.11.x source import

## Android identity

- namespace: `com.receiptledger.v1`
- applicationId: `com.receiptledger.v1`
- minSdk: 23
- targetSdk: 35
- compileSdk: 35
- Java: 17
- build artifact: debug APK only

The new package ID intentionally avoids replacing the existing ReceiptLedger installation while the v1 architecture is still experimental.

## Acceptance

1. public-material audit passes
2. JVM contract test passes
3. Android debug APK compiles
4. APK ZIP integrity passes
5. APK SHA-256 and build identity are emitted
6. artifact is uploaded under a ReceiptLedger-prefixed name
7. no other project namespace is modified
