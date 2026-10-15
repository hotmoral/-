# ReceiptLedger V1 — CP24 Identity Resolver V2 Golden Vectors

Updated: 2026-10-16 KST

The vectors below are synthetic and contain no real personal purchase data.

## A. Alias precedence / reuse

1. MERCHANT exact alias only -> AUTO_LINK merchant target.
2. GLOBAL exact alias only -> AUTO_LINK global target.
3. Same raw alias maps differently in MERCHANT and GLOBAL -> merchant target wins deterministically.
4. MERCHANT alias points to missing catalog row -> REVIEW, no GLOBAL fallback.
5. GLOBAL alias points to missing catalog row -> REVIEW.
6. Exact alias + explicit confirmed specification conflict -> REVIEW.
7. Exact alias + explicit confirmed brand conflict -> REVIEW.
8. Exact alias + harmless lexical abbreviation difference -> AUTO_LINK.
9. Confirmed merchant alias learned after review -> next identical merchant purchase AUTO_LINK.
10. Explicit global alias learned -> next purchase in another merchant can AUTO_LINK globally when no merchant-specific override exists.

## B. Strict semantic exact

11. Confirmed brand + productName + 5입 specification exactly match one STANDARD entry -> AUTO_LINK.
12. Same productName but 10입 candidate vs 5입 catalog -> not that product.
13. Confirmed productName + exact specification with no brand on either side -> unique AUTO_LINK.
14. Catalog has confirmed brand but receipt brand absent -> suggestion/review, not semantic AUTO_LINK.
15. Receipt brand present but catalog brand absent/unconfirmed -> suggestion/review.
16. Catalog confirmed variant present but receipt variant absent -> suggestion/review.
17. Exact productName + specification but two different stable IDs have identical confirmed semantics -> REVIEW ambiguity, no merge.
18. Standalone 1KG/1L CP23 ambiguity -> REVIEW even if one STANDARD candidate appears plausible.

## C. Suggestion / fragmentation

19. Exact confirmed productName but specification missing -> REVIEW with existing candidate, no auto-create.
20. Exact productName + compatible confirmed fields but strict completeness missing -> deterministic suggestion.
21. Multiple same-score suggestions -> REVIEW with stable-ID ordered candidates.
22. Known existing product with receipt text too weak to identify any candidate -> UNRESOLVED and counted as fragmentation risk.
23. Entirely unknown product -> UNRESOLVED but not false split because no expected existing identity exists.
24. NON_STANDARD commodity without confirmed alias -> CP24 semantic resolver does not guess grouping.

## D. Determinism

25. Reverse/shuffle catalog enumeration order -> identical status, authority, selected ID and ranked candidate order.
26. Equivalent exact package units (1kg vs 1000g, 1L vs 1000mL) use CP21 deterministic specification token semantics.

## E. Synthetic acceptance metrics

The executable test fixture must emit one `CP24_METRICS` line containing at minimum:

- fixtures;
- known_identity;
- auto_links;
- correct_auto_links;
- incorrect_auto_links;
- false_merge;
- false_split;
- review_required;
- unresolved;
- repeat_cases;
- repeat_reused;

Required local thresholds:

- `false_merge=0`;
- `incorrect_auto_links=0`;
- `repeat_reused == repeat_cases`;
- `false_split / known_identity <= 0.05`;
- every conflict vector is REVIEW-gated.
