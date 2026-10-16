package com.receiptledger.v1.search;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/** Deterministic CP29 search result with diagnostics for later CP36 scale measurement. */
public final class SearchBrowseResultV1 {
    public final String normalizedQuery;
    public final int catalogEntriesScanned;
    public final int matchedEntriesBeforeLimit;
    public final int returnedEntries;
    public final List<SearchBrowseEntryV1> entries;

    SearchBrowseResultV1(
            String normalizedQuery,
            int catalogEntriesScanned,
            int matchedEntriesBeforeLimit,
            List<SearchBrowseEntryV1> entries) {
        this.normalizedQuery = normalizedQuery;
        this.catalogEntriesScanned = catalogEntriesScanned;
        this.matchedEntriesBeforeLimit = matchedEntriesBeforeLimit;
        this.returnedEntries = entries == null ? 0 : entries.size();
        this.entries = Collections.unmodifiableList(new ArrayList<>(entries == null
                ? Collections.<SearchBrowseEntryV1>emptyList() : entries));
    }
}
