package com.receiptledger.v1.ui;

import android.app.Activity;
import android.graphics.Insets;
import android.os.Build;
import android.view.View;
import android.view.WindowInsets;

public final class SystemBarInsetHelper {
    private SystemBarInsetHelper() {}

    public static void apply(Activity activity, View content) {
        final int baseLeft = content.getPaddingLeft();
        final int baseTop = content.getPaddingTop();
        final int baseRight = content.getPaddingRight();
        final int baseBottom = content.getPaddingBottom();

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.VANILLA_ICE_CREAM) {
            return;
        }

        content.setOnApplyWindowInsetsListener((view, windowInsets) -> {
            Insets safeInsets = windowInsets.getInsets(
                    WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout());
            int[] padding = resolvePadding(
                    baseLeft,
                    baseTop,
                    baseRight,
                    baseBottom,
                    safeInsets.left,
                    safeInsets.top,
                    safeInsets.right,
                    safeInsets.bottom);
            view.setPadding(padding[0], padding[1], padding[2], padding[3]);
            return windowInsets;
        });
        content.requestApplyInsets();
    }

    static int[] resolvePadding(
            int baseLeft,
            int baseTop,
            int baseRight,
            int baseBottom,
            int insetLeft,
            int insetTop,
            int insetRight,
            int insetBottom) {
        return new int[] {
                baseLeft + insetLeft,
                baseTop + insetTop,
                baseRight + insetRight,
                baseBottom + insetBottom
        };
    }
}
