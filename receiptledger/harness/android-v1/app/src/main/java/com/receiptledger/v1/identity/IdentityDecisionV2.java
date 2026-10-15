package com.receiptledger.v1.identity;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Immutable CP24 resolver outcome. It never creates or merges catalog entities. */
public final class IdentityDecisionV2 {
    public enum Status { AUTO_LINK, REVIEW, UNRESOLVED }

    public enum Authority {
        MERCHANT_EXACT_ALIAS,
        GLOBAL_EXACT_ALIAS,
        STRICT_SEMANTIC_EXACT,
        SEMANTIC_SUGGESTION,
        ALIAS_CONFLICT,
        SEMANTIC_AMBIGUOUS,
        NONE
    }

    public final Status status;
    public final Authority authority;
    public final String catalogEntryId;
    public final List<String> rankedCandidateIds;
    public final String reason;

    private IdentityDecisionV2(
            Status status,
            Authority authority,
            String catalogEntryId,
            List<String> rankedCandidateIds,
            String reason) {
        this.status = status;
        this.authority = authority;
        this.catalogEntryId = catalogEntryId;
        this.rankedCandidateIds = Collections.unmodifiableList(new ArrayList<>(rankedCandidateIds));
        this.reason = reason == null ? "" : reason;
    }

    public static IdentityDecisionV2 autoLink(String id, Authority authority, String reason) {
        List<String> ids = new ArrayList<>();
        ids.add(id);
        return new IdentityDecisionV2(Status.AUTO_LINK, authority, id, ids, reason);
    }

    public static IdentityDecisionV2 review(
            String suggestedId, Authority authority, List<String> rankedIds, String reason) {
        return new IdentityDecisionV2(Status.REVIEW, authority, suggestedId,
                rankedIds == null ? Collections.<String>emptyList() : rankedIds, reason);
    }

    public static IdentityDecisionV2 unresolved(String reason) {
        return new IdentityDecisionV2(Status.UNRESOLVED, Authority.NONE, null,
                Collections.<String>emptyList(), reason);
    }

    public boolean autoLinked() {
        return status == Status.AUTO_LINK && catalogEntryId != null;
    }

    public boolean includesCandidate(String id) {
        return id != null && rankedCandidateIds.contains(id);
    }
}
