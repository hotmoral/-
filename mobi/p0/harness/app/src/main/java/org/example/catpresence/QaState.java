package org.example.catpresence;

import android.content.Context;
import android.content.SharedPreferences;
import android.graphics.RectF;
import android.os.Build;
import android.provider.Settings;

import java.util.ArrayList;
import java.util.List;

public final class QaState {
    private static final String PREFS = "p0_qa_state";
    private static final int MAX_EVENTS = 28;

    private QaState() {}

    private static SharedPreferences prefs(Context context) {
        return context.getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    public static void putBoolean(Context context, String key, boolean value) {
        prefs(context).edit().putBoolean(key, value).apply();
    }

    public static boolean getBoolean(Context context, String key, boolean fallback) {
        return prefs(context).getBoolean(key, fallback);
    }

    public static void putInt(Context context, String key, int value) {
        prefs(context).edit().putInt(key, value).apply();
    }

    public static int getInt(Context context, String key, int fallback) {
        return prefs(context).getInt(key, fallback);
    }

    public static void putLong(Context context, String key, long value) {
        prefs(context).edit().putLong(key, value).apply();
    }

    public static long getLong(Context context, String key, long fallback) {
        return prefs(context).getLong(key, fallback);
    }

    public static void putString(Context context, String key, String value) {
        prefs(context).edit().putString(key, value).apply();
    }

    public static String getString(Context context, String key, String fallback) {
        return prefs(context).getString(key, fallback);
    }

    public static void increment(Context context, String key) {
        putInt(context, key, getInt(context, key, 0) + 1);
    }

    public static synchronized void appendEvent(Context context, String event) {
        String old = getString(context, "events", "");
        String[] split = old.isEmpty() ? new String[0] : old.split("\\n");
        List<String> lines = new ArrayList<>();
        int start = Math.max(0, split.length - (MAX_EVENTS - 1));
        for (int i = start; i < split.length; i++) {
            if (!split[i].isBlank()) {
                lines.add(split[i]);
            }
        }
        lines.add(System.currentTimeMillis() + " " + event);
        putString(context, "events", String.join("\n", lines));
    }

    public static String rectToString(RectF rect) {
        if (rect == null) return "unknown";
        return Math.round(rect.left) + "," + Math.round(rect.top) + "," +
                Math.round(rect.right) + "," + Math.round(rect.bottom);
    }

    public static String buildReport(Context context) {
        StringBuilder sb = new StringBuilder();
        sb.append("P0 Cat Presence QA Report\n");
        sb.append("prototype=P0_PROTO_V1\n");
        sb.append("package=").append(context.getPackageName()).append('\n');
        sb.append("device=").append(Build.MANUFACTURER).append(' ').append(Build.MODEL).append('\n');
        sb.append("android=").append(Build.VERSION.RELEASE).append(" sdk=").append(Build.VERSION.SDK_INT).append('\n');
        sb.append("overlayPermission=").append(Settings.canDrawOverlays(context)).append('\n');
        sb.append("userEnabled=").append(getBoolean(context, "userEnabled", false)).append('\n');
        sb.append("serviceActive=").append(getBoolean(context, "serviceActive", false)).append('\n');
        sb.append("overlayAttached=").append(getBoolean(context, "overlayAttached", false)).append('\n');
        sb.append("globalBounds=").append(getString(context, "globalBounds", "unknown")).append('\n');
        sb.append("windowScreen=")
                .append(getInt(context, "windowX", -1)).append(',')
                .append(getInt(context, "windowY", -1)).append(',')
                .append(getInt(context, "windowW", -1)).append(',')
                .append(getInt(context, "windowH", -1)).append('\n');
        sb.append("visualBoundsLocal=").append(getString(context, "visualBoundsLocal", "unknown")).append('\n');
        sb.append("bodyBoundsLocal=").append(getString(context, "bodyBoundsLocal", "unknown")).append('\n');
        sb.append("touchBoundsLocal=").append(getString(context, "touchBoundsLocal", "unknown")).append('\n');
        sb.append("touchFootprintRule=actual_window_rectangle\n");
        sb.append("tapCount=").append(getInt(context, "tapCount", 0)).append('\n');
        sb.append("dragCount=").append(getInt(context, "dragCount", 0)).append('\n');
        sb.append("lastMove=").append(getString(context, "lastMove", "none")).append('\n');
        sb.append("rotation=").append(getInt(context, "rotation", -1)).append('\n');
        sb.append("orientation=").append(getInt(context, "orientation", -1)).append('\n');
        sb.append("imeVisibleNow=").append(getBoolean(context, "imeVisible", false)).append('\n');
        sb.append("imeBottomNow=").append(getInt(context, "imeBottom", 0)).append('\n');
        sb.append("imeEverVisible=").append(getBoolean(context, "imeEverVisible", false)).append('\n');
        sb.append("maxImeBottomObserved=").append(getInt(context, "maxImeBottom", 0)).append('\n');
        sb.append("lastSampleReason=").append(getString(context, "sampleReason", "none")).append('\n');
        sb.append("recentEvents:\n").append(getString(context, "events", "none")).append('\n');
        return sb.toString();
    }
}
