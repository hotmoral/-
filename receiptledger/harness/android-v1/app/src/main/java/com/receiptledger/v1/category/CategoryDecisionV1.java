package com.receiptledger.v1.category;

import com.receiptledger.v1.catalog.CategoryRef;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** CP25 category result. Category state never changes catalog identity. */
public final class CategoryDecisionV1 {
    public enum State { REUSE_PERSISTED, AUTO_ASSIGNABLE, REVIEW, UNRESOLVED }

    public final State state;
    public final CategoryRef category;
    public final List<CategoryCandidateV1> candidates;
    public final String reason;

    private CategoryDecisionV1(State state, CategoryRef category, List<CategoryCandidateV1> candidates, String reason) {
        this.state = state;
        this.category = category;
        this.candidates = Collections.unmodifiableList(new ArrayList<>(candidates));
        this.reason = reason;
    }

    public static CategoryDecisionV1 reuse(CategoryRef category) {
        return new CategoryDecisionV1(State.REUSE_PERSISTED, category, Collections.<CategoryCandidateV1>emptyList(), "persisted-category");
    }

    public static CategoryDecisionV1 auto(CategoryCandidateV1 candidate, List<CategoryCandidateV1> ranked) {
        return new CategoryDecisionV1(State.AUTO_ASSIGNABLE, candidate.category, ranked, "unique-high-confidence-rule");
    }

    public static CategoryDecisionV1 review(List<CategoryCandidateV1> ranked, String reason) {
        CategoryRef primary = ranked.isEmpty() ? null : ranked.get(0).category;
        return new CategoryDecisionV1(State.REVIEW, primary, ranked, reason);
    }

    public static CategoryDecisionV1 unresolved() {
        return new CategoryDecisionV1(State.UNRESOLVED, null, Collections.<CategoryCandidateV1>emptyList(), "no-defensible-category-evidence");
    }

    public boolean requiresReview() { return state == State.REVIEW || state == State.UNRESOLVED; }
    public boolean canAutoAssign() { return state == State.AUTO_ASSIGNABLE; }
}
