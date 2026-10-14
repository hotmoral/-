package org.example.mobifootprint;

import android.content.Context;
import android.content.SharedPreferences;

import java.util.Locale;

public final class QaState {
    public static final String PREF = "p1_b22_qa_state";

    private QaState() {}

    private static SharedPreferences prefs(Context context) {
        return context.getSharedPreferences(PREF, Context.MODE_PRIVATE);
    }

    public static void reset(Context context) {
        prefs(context).edit().clear()
                .putString("prototype", "P1_B2_2_MULTI_WINDOW_V01")
                .putString("variant", "NONE")
                .putInt("childCount", 0)
                .putInt("hostTapCount", 0)
                .putInt("coreTapCount", 0)
                .putInt("foreTapCount", 0)
                .putInt("hindTapCount", 0)
                .putInt("tailTapCount", 0)
                .putString("lastHit", "NONE")
                .putString("lastEvent", "reset")
                .putBoolean("serviceActive", false)
                .putBoolean("screenOffSeen", false)
                .putBoolean("screenOnSeen", false)
                .putInt("rotation", -1)
                .apply();
    }

    public static void recordService(Context context, boolean active) {
        prefs(context).edit().putBoolean("serviceActive", active).apply();
    }

    public static void recordVariant(Context context, String variant, int childCount) {
        prefs(context).edit()
                .putString("variant", variant)
                .putInt("childCount", childCount)
                .putString("lastEvent", "variant=" + variant + " count=" + childCount)
                .apply();
    }

    public static void recordRotation(Context context, int rotation) {
        prefs(context).edit().putInt("rotation", rotation).putString("lastEvent", "rotation=" + rotation).apply();
    }

    public static void recordScreen(Context context, boolean on) {
        SharedPreferences.Editor e = prefs(context).edit();
        if (on) e.putBoolean("screenOnSeen", true).putString("lastEvent", "screen_on");
        else e.putBoolean("screenOffSeen", true).putString("lastEvent", "screen_off");
        e.apply();
    }

    public static void recordGroup(Context context, int x, int y, int moveErrorPx) {
        prefs(context).edit()
                .putInt("groupX", x)
                .putInt("groupY", y)
                .putInt("moveErrorPx", moveErrorPx)
                .putString("lastEvent", "group=" + x + "," + y + " error=" + moveErrorPx)
                .apply();
    }

    public static void recordGeometry(Context context, String geometry) {
        prefs(context).edit().putString("geometry", geometry).apply();
    }

    public static void recordHit(Context context, String part) {
        SharedPreferences p = prefs(context);
        String key = part.toLowerCase(Locale.US) + "TapCount";
        int next = p.getInt(key, 0) + 1;
        p.edit().putInt(key, next).putString("lastHit", part).putString("lastEvent", "hit=" + part).apply();
    }

    public static void recordHostHit(Context context, float x, float y) {
        SharedPreferences p = prefs(context);
        p.edit()
                .putInt("hostTapCount", p.getInt("hostTapCount", 0) + 1)
                .putString("lastHit", "HOST")
                .putString("lastEvent", "host=" + Math.round(x) + "," + Math.round(y))
                .apply();
    }
}
