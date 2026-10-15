package com.receiptledger.v1.ui;

import static org.junit.Assert.assertArrayEquals;

import org.junit.Test;

public final class SystemBarInsetHelperTest {
    @Test
    public void resolvePadding_addsInsetsToOriginalBasePadding() {
        assertArrayEquals(
                new int[] {14, 32, 18, 40},
                SystemBarInsetHelper.resolvePadding(10, 12, 14, 16, 4, 20, 4, 24));
    }

    @Test
    public void resolvePadding_isStableAcrossRepeatedInsetDispatches() {
        int[] first = SystemBarInsetHelper.resolvePadding(12, 12, 12, 12, 0, 24, 0, 48);
        int[] second = SystemBarInsetHelper.resolvePadding(12, 12, 12, 12, 0, 24, 0, 48);
        assertArrayEquals(first, second);
        assertArrayEquals(new int[] {12, 36, 12, 60}, second);
    }
}
