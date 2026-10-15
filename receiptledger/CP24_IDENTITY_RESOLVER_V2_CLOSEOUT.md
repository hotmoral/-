# ReceiptLedger V1 — CP24 Identity Resolver V2 Closeout

Updated: 2026-10-16 KST
Status: **PASS / COMPLETE**

## 1. Frozen boundary

CP24 implementation is frozen at:

`4b556afd4dd52b68cf768e937bb456665ad4c231`

Canonical validation:

- Actions `38824134990` — SUCCESS
- job `116727478370` — SUCCESS
- artifact `12014915453`
- artifact digest `sha256:4740590ca2c7d7525842aa3ebe6ec7964911d303322ebad77b5701344ce76867`
- debug APK SHA-256 `0656c60110ba7debcb0801ddee048cd2220b959c2119539a79274eebbc05eb6e`

Any later commit in this branch that only synchronizes status/handoff documents is not additional CP24 implementation.

## 2. What CP24 accomplished

CP24 adds a deterministic resolver from current receipt evidence + confirmed catalog knowledge to an **existing stable catalog ID**.

The resolver can return:

- `AUTO_LINK` — sufficient identity authority;
- `REVIEW` — an existing identity is plausible/known but automatic authority is insufficient or conflicting;
- `UNRESOLVED` — no defensible existing candidate.

It never merges catalog entities and never creates a new entity automatically.

## 3. Frozen authority order

1. exact MERCHANT alias;
2. exact GLOBAL alias;
3. unique strict semantic exact;
4. deterministic semantic suggestion;
5. unresolved.

MERCHANT alias is more specific than GLOBAL alias. A dangling alias or a strong explicit contradiction fails to REVIEW rather than falling through silently.

## 4. Strict semantic auto-link rule

Semantic auto-link is intentionally narrow. It requires one unique existing STANDARD candidate with:

- non-ambiguous CP23 evidence;
- confirmed exact catalog product name;
- confirmed exact catalog specification;
- confirmed/exact brand when either side carries brand;
- confirmed/exact variant when either side carries variant.

Therefore a product-name match, category match, store match, or HIGH parser confidence is insufficient by itself.

Fuzzy/edit-distance/embedding/phonetic similarity remains non-authoritative.

## 5. Automation vs safety result

Canonical local metrics:

`fixtures=24 known_identity=20 auto_links=14 correct_auto_links=14 incorrect_auto_links=0 false_merge=0 false_split=1 review_required=6 unresolved=4 repeat_cases=4 repeat_reused=4`

The result deliberately balances both risks:

- unsafe automatic link / false merge: **0**;
- repeat confirmed reuse: **4/4**;
- known-identity fragmentation risk: **1/20 = 5%**.

The one fragmentation-risk fixture is not hidden or “fixed” by weakening identity safety. It represents weak evidence where the correct existing identity is not surfaced. Future confirmation/review UX and safe knowledge reuse may reduce it.

## 6. Compatibility result

Unchanged:

- CP21 catalog meaning and stable-ID authority;
- CP22 product schema 2 and receipt schema 1;
- legacy product IDs/item links;
- CP23 parser semantics and ambiguity rules;
- receipt-derived price/date/store/validation truth;
- permission/network/privacy model.

No database migration was required.

## 7. Test/build result

- CP24 identity tests 8/8 PASS
- CP23 semantics 7/7 PASS
- CP21 catalog 15/15 PASS
- CP22 persistence 7/7 PASS
- lint 0 errors / 0 warnings
- debug APK build PASS
- forbidden-permission audit PASS

## 8. Deliberate limitations

- semantic commodity grouping is still deferred to CP26;
- resolver quality evidence is synthetic/local, not CP35 E2E accuracy;
- semantic ranking currently enumerates the personal catalog linearly; CP36 owns representative-scale performance proof;
- CP24 provides resolver/learning primitives and evidence, not final Capture/Review UI integration;
- unresolved/review decisions do not authorize automatic new-product creation.

## 9. Next dependency boundary

Next planned checkpoint: **CP25 — Category System**.

CP25 may use stable resolved catalog IDs for browse/classification metadata, but **category must never become product identity authority**. CP24 resolver rules remain frozen unless an explicit canonical amendment is justified.

## 10. Stop condition

CP24 is closed. Synchronize canonical handoff/status documents in a docs-only commit, verify no executable change after the frozen implementation HEAD, and stop before CP25 until explicitly authorized.
