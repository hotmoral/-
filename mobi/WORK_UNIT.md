# Public execution work unit

Status: **T0-3 E6 MOBILE PACKAGE BUILT / OEM RUNTIME PENDING / WORKFLOWS PARKED**

This public branch is a generic Android execution harness only. It is not the canonical Mobi repository.

## Accepted T0-2 runtime identity

- commit: `cd0b2568d4d01753b6131bbcfcebe68fbff0eded`
- workflow run: `38521870448`
- conclusion: `SUCCESS`
- artifact ID: `11874282241`
- artifact digest: `sha256:cb4954bb21fe76cf848bf05de37cb145883d86805276063ce01815fdda87a032`

## Accepted T0-3 generic E5 runtime identity

- commit: `9d4e1b4310398af4970a9b04ed374ab5eec3bf78`
- workflow run: `38525620788`
- job: `115725153619`
- conclusion: `SUCCESS`
- artifact ID: `11875528144`
- artifact digest: `sha256:cd9c88c1ad058cabdaa5e35e2a99ae8da4af9e4b5d4a40c47b7f5da30e9421f5`

The private canonical Mobi repository reviewed and recorded the generic result. It does not constitute Samsung/One UI evidence.

## Samsung / One UI E6 desktop/RTL package

A public-safe package for one real Samsung Galaxy + Samsung Keyboard run was built successfully.

- package source/build commit: `1705adc3c4c74fbbaf59b0900f9b5fb346dc2c34`
- workflow run: `38527148222`
- job: `115730078195`
- conclusion: `SUCCESS`
- artifact ID: `11876298146`
- artifact digest: `sha256:83cfd0c09a0223c5a698d05a2374227c595d2e57167b046228a042205f3e608b`

## Samsung / One UI E6 mobile-only package

A second public-safe package was built for PC-free execution on the same Galaxy through Termux + Android Wireless debugging + adb.

- package source/build commit: `cd7c6ecb3ee3ca6d38a8a5eb7b0de813010016f5`
- workflow run: `38531492273`
- job: `115744188730`
- conclusion: `SUCCESS`
- artifact ID: `11877439165`
- artifact digest: `sha256:8494e059719e58ead1465817bcef1c24898631a5aa205588cca5725d25bf83dd`
- package mode: `termux_wireless_adb_same_device`
- package verification: shell syntax PASS, internal SHA-256 manifest PASS, both APK ZIP containers PASS

The mobile package includes:

- two synthetic debug APKs
- `setup_termux.sh`
- `pair_connect.sh`
- `run.sh`
- the unchanged Samsung E6 evidence runner
- Korean step-by-step instructions

Neither package build is E6 runtime evidence. E6 remains pending until one package is actually executed on a real Samsung/One UI device with Samsung Keyboard active and the resulting evidence is reviewed in private `hotmoral/Mobi`.

All Mobi workflows on this branch are manual-only after package construction. Do not trigger another run merely for redundancy.

## Rules

- Do not include private Mobi canonical source, product design, private assets, credentials, signing material, or private repository identifiers.
- Do not use source, fixtures, caches, artifacts, or workflow output from other project namespaces.
- Do not modify repository-wide settings for this work unit.
- Public results are provisional until reviewed and recorded in the private canonical Mobi repository.
- Cleanup of public branches/runs/artifacts is hygiene, not secrecy; anything published must be safe to remain public permanently.
- Do not run again merely for redundancy. Revalidation requires a concrete new evidence need.
