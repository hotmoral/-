package com.receiptledger.v1;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import org.junit.Test;

public final class FoundationContractTest {
    @Test
    public void publicFoundationIdentityIsStable() {
        assertEquals("receiptledger", FoundationIdentity.PUBLIC_NAMESPACE);
        assertEquals("RL_V1_FOUNDATION_01", FoundationIdentity.FOUNDATION_ID);
        assertTrue(FoundationIdentity.PUBLIC_DEBUG_BUILD);
    }
}
