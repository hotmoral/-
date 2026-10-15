# ReceiptLedger V1 — Session Handoff

Updated: 2026-10-16 KST

## 0. Read this before doing any implementation

This file is the restart contract for a new GPT session.

Do **not** reconstruct project state from old chat memory. Do **not** guess what was completed. Use GitHub as the execution source of truth for this public ReceiptLedger workspace.

Read in this order:

1. `receiptledger/PROJECT_STATUS_LATEST.md`
2. `receiptledger/SESSION_HANDOFF.md`
3. `receiptledger/TARGET_API36_CORE_PLAN.md`
4. `receiptledger/README.md`
5. `receiptledger/WORK_UNIT.md`
6. relevant prior `*_CORE_PLAN.md` files only when needed for a dependency contract
7. current Android source under `receiptledger/harness/android-v1/`
8. current ReceiptLedger workflows under `.github/workflows/receiptledger-*.yml`

After reading, verify exact GitHub refs and the completed Build Hygiene Actions evidence before editing anything.

## 1. Exact handoff state

Repository: `hotmoral/-`

Last fully completed implementation checkpoint:
**ReceiptLedger V1 Build Hygiene Core**

Frozen implementation baseline:
`53d03fc219d4b15bf09cebbc368ae6af6a55053a`

Completed branch:
`receiptledger/run-v1-build-hygiene-core-20261015`

Verified Actions run:
`38755847381` — SUCCESS

Verified Build Hygiene artifact digest:
`sha256:903e259ff0f2156cf14b8d5e39a2b3424f54ec97318df4290d31c63046f2ebd2`

Final lint result at that implementation boundary:
`0 errors, 1 warning`

The remaining warning is `OldTargetApi` because compileSdk/targetSdk are still 35.

## 2. Current working branch for the next GPT

Reserved next branch:
`receiptledger/run-v1-target-api36-core-20261015`

This branch was created directly from the completed Build Hygiene implementation baseline.

At the time of handoff, **Target API 36 production implementation has not started**.

Only handoff/status documentation is allowed to differ from the Build Hygiene source baseline before the next GPT begins implementation. The next GPT must compare the branch against `53d03fc219d4b15bf09cebbc368ae6af6a55053a` and confirm that pre-handoff differences are documentation-only.

## 3. What is already working

The public V1 app already has a complete first vertical slice:

- Android app foundation and GitHub Actions APK generation
- external-camera capture without app CAMERA permission
- system document/image picker without broad storage permission
- EXIF normalization and bounded bitmap decoding
- conservative document-region detection
- perspective correction and coordinate mapping
- bundled Korean ML Kit OCR
- OCR source-coordinate contract
- layout reconstruction from OCR elements
- receipt structure classification
- item tuple extraction with provenance
- receipt arithmetic validation
- OCR recovery passes with bounded pass budget
- conservative cross-pass merge
- user review/edit before save
- app-private SQLite persistence
- app-private receipt image archive
- receipt list/detail/delete UI
- conservative merchant/store extraction
- STANDARD / NON_STANDARD / UNCLASSIFIED product identity model
- exact confirmed alias reuse only
- price-history derivation from receipt data
- integrated unit/regression tests
- Android lint gate
- debug APK and public evidence packaging

## 4. Security / privacy boundary

This repository is public. Assume every pushed byte, workflow log, and artifact is permanently public.

Never commit or upload:

- release signing keystore
- signing passwords
- API keys, OAuth secrets, access tokens
- real receipt photos unless the user explicitly approves a sanitized public fixture
- actual personal purchase database
- personal identifiers
- private backups
- proprietary/private assets not cleared for public release

Do not add network permission casually. The current app intentionally removes `INTERNET` and `ACCESS_NETWORK_STATE` even though ML Kit dependencies may try to merge them.

Public APKs are debug/unsigned-style development artifacts only. Release signing must remain a separate private path.

## 5. Namespace isolation

ReceiptLedger may modify only:

- `receiptledger/**`
- explicitly ReceiptLedger-prefixed workflows: `.github/workflows/receiptledger-*.yml`

Do not modify, consume, reuse, cache from, or depend on:

- `mobi/**`
- `einstein/**`
- `linkline/**`
- other project branches/artifacts/caches/output

Do not change repository-wide permissions/rulesets/secrets/settings without explicit user approval.

## 6. Next task — exact boundary

The next task is **V1 Target API 36 Core**, and only that task.

Primary goals:

1. move `compileSdk` from 35 to 36
2. move `targetSdk` from 35 to 36
3. update AGP to an API-36-compatible version (minimum verified direction: AGP 8.9.1 or newer compatible choice)
4. update Gradle to the compatible version for the selected AGP (AGP 8.9 family requires Gradle 8.11.1+)
5. preserve Java 17 and minSdk 23
6. handle Android 16 forced edge-to-edge correctly in programmatic View UIs
7. audit predictive-back behavior; do not invent custom interception if the app does not need it
8. preserve all existing functionality and data contracts
9. retain Android lint at 0 errors
10. remove the existing `OldTargetApi` warning by legitimately targeting API 36, not by suppression/baseline
11. preserve permission firewall: no CAMERA, broad storage/media, INTERNET, ACCESS_NETWORK_STATE, MANAGE_EXTERNAL_STORAGE
12. build a debug APK and publish evidence artifact through a ReceiptLedger-prefixed workflow

## 7. Non-goals for Target API 36 Core

Do not mix these into the checkpoint:

- OCR accuracy redesign
- new parser heuristics
- new product matching logic
- DB schema redesign unless API 36 forces it
- UI redesign/polish beyond system-bar/inset compatibility required by API 36
- release signing
- Play Store publishing
- importing private receipt samples
- adding network services

## 8. Required verification before closing Target API 36 Core

At minimum:

- exact branch HEAD recorded
- public-tree namespace audit PASS
- unit tests PASS
- `lintDebug` PASS with **0 errors**
- verify `OldTargetApi` warning is gone
- `assembleDebug` PASS
- APK ZIP integrity PASS
- packaged permissions inspected and forbidden permissions absent
- launcher + all internal activities remain correctly exported/non-exported
- API 23 compatibility not regressed
- edge-to-edge/inset handling code compiled and covered by static/unit contract where feasible
- evidence artifact uploaded
- artifact SHA-256/digest recorded
- update `PROJECT_STATUS_LATEST.md` and this handoff file before moving to the next checkpoint

## 9. Stop condition

Once Target API 36 Core is green and its status/handoff documents are synchronized, stop and report. Do not automatically begin the next feature group unless the user explicitly instructs continuation.
