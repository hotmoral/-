package com.receiptledger.v1.commodity;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** CP26 grouping result. Grouping identifies a commodity only; it never asserts price comparability. */
public final class CommodityGroupingDecisionV2 {
    public enum State { AUTO_GROUP, REVIEW, UNRESOLVED }
    public enum Authority {
        MERCHANT_EXACT_ALIAS,
        GLOBAL_EXACT_ALIAS,
        EXACT_COMMODITY_NAME,
        COMMODITY_SUGGESTION,
        CROSS_KIND_CONFLICT,
        NONE
    }

    public final State state;
    public final String catalogEntryId;
    public final Authority authority;
    public final List<String> candidateIds;
    public final String reason;

    private CommodityGroupingDecisionV2(
            State state,
            String catalogEntryId,
            Authority authority,
            List<String> candidateIds,
            String reason) {
        this.state = state;
        this.catalogEntryId = catalogEntryId;
        this.authority = authority;
        this.candidateIds = Collections.unmodifiableList(new ArrayList<>(candidateIds));
        this.reason = reason == null ? "" : reason;
    }

    public static CommodityGroupingDecisionV2 autoGroup(String id, Authority authority, String reason) {
        List<String> ids = new ArrayList<>();
        ids.add(id);
        return new CommodityGroupingDecisionV2(State.AUTO_GROUP, id, authority, ids, reason);
    }

    public static CommodityGroupingDecisionV2 review(
            String suggestedId, Authority authority, List<String> candidates, String reason) {
        return new CommodityGroupingDecisionV2(State.REVIEW, suggestedId, authority,
                candidates == null ? Collections.<String>emptyList() : candidates, reason);
    }

    public static CommodityGroupingDecisionV2 unresolved(String reason) {
        return new CommodityGroupingDecisionV2(State.UNRESOLVED, null, Authority.NONE,
                Collections.<String>emptyList(), reason);
    }
}
