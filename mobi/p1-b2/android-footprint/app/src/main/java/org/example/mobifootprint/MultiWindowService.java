package org.example.mobifootprint;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.res.Configuration;
import android.graphics.Color;
import android.graphics.PixelFormat;
import android.graphics.Rect;
import android.os.Build;
import android.os.IBinder;
import android.provider.Settings;
import android.view.Gravity;
import android.view.WindowManager;

import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.Map;

public final class MultiWindowService extends Service implements FootprintPartView.DragDelegate {
    public static final String ACTION_F0 = "org.example.mobifootprint.F0";
    public static final String ACTION_F1 = "org.example.mobifootprint.F1";
    public static final String ACTION_F2 = "org.example.mobifootprint.F2";
    public static final String ACTION_MOVE_A = "org.example.mobifootprint.MOVE_A";
    public static final String ACTION_MOVE_B = "org.example.mobifootprint.MOVE_B";
    public static final String ACTION_STOP = "org.example.mobifootprint.STOP";

    private static final String CHANNEL = "p1_b22_footprint";
    private static final int NOTIFICATION_ID = 2202;

    private final LinkedHashMap<String, Child> children = new LinkedHashMap<>();
    private WindowManager windowManager;
    private float density;
    private int groupX;
    private int groupY;
    private String variant = "NONE";
    private BroadcastReceiver screenReceiver;

    private static final class Spec {
        final String part;
        final float xDp, yDp, wDp, hDp;
        final int color;

        Spec(String part, float xDp, float yDp, float wDp, float hDp, int color) {
            this.part = part;
            this.xDp = xDp;
            this.yDp = yDp;
            this.wDp = wDp;
            this.hDp = hDp;
            this.color = color;
        }
    }

    private static final class Child {
        final Spec spec;
        final FootprintPartView view;
        final WindowManager.LayoutParams lp;

        Child(Spec spec, FootprintPartView view, WindowManager.LayoutParams lp) {
            this.spec = spec;
            this.view = view;
            this.lp = lp;
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        density = getResources().getDisplayMetrics().density;
        windowManager = (WindowManager) getSystemService(WINDOW_SERVICE);
        createNotificationChannel();
        startForeground(NOTIFICATION_ID, buildNotification());
        QaState.recordService(this, true);
        registerScreenReceiver();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (intent == null || intent.getAction() == null) return START_STICKY;
        String action = intent.getAction();
        if (ACTION_STOP.equals(action)) {
            stopCleanly();
            return START_NOT_STICKY;
        }
        if (!Settings.canDrawOverlays(this)) {
            QaState.recordVariant(this, "PERMISSION_DENIED", 0);
            return START_STICKY;
        }
        switch (action) {
            case ACTION_F0: attachVariant("F0"); break;
            case ACTION_F1: attachVariant("F1"); break;
            case ACTION_F2: attachVariant("F2"); break;
            case ACTION_MOVE_A: moveToDp(80f, 220f); break;
            case ACTION_MOVE_B: moveToDp(140f, 340f); break;
            default: break;
        }
        return START_STICKY;
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        clampAndUpdate(0);
        QaState.recordRotation(this, getDisplayRotation());
    }

    @Override
    public void onDragBy(float dx, float dy) {
        groupX += Math.round(dx);
        groupY += Math.round(dy);
        clampAndUpdate(0);
    }

    private void attachVariant(String next) {
        removeAllChildren();
        variant = next;
        groupX = dp(80f);
        groupY = dp(220f);
        for (Spec spec : specs(next)) addChild(spec);
        clampAndUpdate(0);
        QaState.recordVariant(this, variant, children.size());
        QaState.recordRotation(this, getDisplayRotation());
    }

    private Spec[] specs(String v) {
        if ("F0".equals(v)) {
            return new Spec[] {
                    new Spec("ALL", 0, 0, 190, 115, Color.rgb(76, 103, 128))
            };
        }
        if ("F1".equals(v)) {
            return new Spec[] {
                    new Spec("CORE", 0, 0, 135, 90, Color.rgb(65, 100, 130)),
                    new Spec("TAIL", 115, 12, 75, 64, Color.rgb(130, 88, 126))
            };
        }
        if ("F2".equals(v)) {
            return new Spec[] {
                    new Spec("CORE", 22, 0, 112, 78, Color.rgb(65, 100, 130)),
                    new Spec("HIND", 0, 58, 58, 57, Color.rgb(93, 124, 88)),
                    new Spec("FORE", 84, 57, 54, 58, Color.rgb(151, 105, 62)),
                    new Spec("TAIL", 115, 12, 75, 64, Color.rgb(130, 88, 126))
            };
        }
        throw new IllegalArgumentException("unknown variant=" + v);
    }

    private void addChild(Spec spec) {
        FootprintPartView view = new FootprintPartView(this, spec.part, spec.color, this);
        WindowManager.LayoutParams lp = new WindowManager.LayoutParams(
                dp(spec.wDp),
                dp(spec.hDp),
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                        | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL
                        | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                PixelFormat.TRANSLUCENT);
        lp.gravity = Gravity.TOP | Gravity.START;
        lp.x = groupX + dp(spec.xDp);
        lp.y = groupY + dp(spec.yDp);
        lp.setTitle("MobiP1B22-" + spec.part);
        windowManager.addView(view, lp);
        children.put(spec.part, new Child(spec, view, lp));
    }

    private void moveToDp(float xDp, float yDp) {
        int targetX = dp(xDp);
        int targetY = dp(yDp);
        groupX = targetX;
        groupY = targetY;
        clampAndUpdate(0);
        int error = Math.abs(groupX - clampX(targetX)) + Math.abs(groupY - clampY(targetY));
        QaState.recordGroup(this, groupX, groupY, error);
    }

    private void clampAndUpdate(int ignored) {
        groupX = clampX(groupX);
        groupY = clampY(groupY);
        for (Child child : children.values()) {
            child.lp.x = groupX + dp(child.spec.xDp);
            child.lp.y = groupY + dp(child.spec.yDp);
            try {
                windowManager.updateViewLayout(child.view, child.lp);
            } catch (IllegalArgumentException ignoredException) {
                // A child removed during teardown is not re-added implicitly.
            }
        }
        QaState.recordGroup(this, groupX, groupY, 0);
        QaState.recordGeometry(this, geometryString());
    }

    private int clampX(int value) {
        Rect bounds = windowManager.getCurrentWindowMetrics().getBounds();
        int width = dp(maxRightDp());
        return Math.max(0, Math.min(value, Math.max(0, bounds.width() - width)));
    }

    private int clampY(int value) {
        Rect bounds = windowManager.getCurrentWindowMetrics().getBounds();
        int height = dp(maxBottomDp());
        return Math.max(0, Math.min(value, Math.max(0, bounds.height() - height)));
    }

    private float maxRightDp() {
        float max = 0f;
        for (Child child : children.values()) max = Math.max(max, child.spec.xDp + child.spec.wDp);
        return max;
    }

    private float maxBottomDp() {
        float max = 0f;
        for (Child child : children.values()) max = Math.max(max, child.spec.yDp + child.spec.hDp);
        return max;
    }

    private String geometryString() {
        StringBuilder b = new StringBuilder();
        for (Map.Entry<String, Child> entry : children.entrySet()) {
            Child c = entry.getValue();
            if (b.length() > 0) b.append(';');
            b.append(entry.getKey()).append('=')
                    .append(c.lp.x).append(',').append(c.lp.y).append(',')
                    .append(c.lp.width).append(',').append(c.lp.height);
        }
        return b.toString();
    }

    private void removeAllChildren() {
        for (Child child : children.values()) {
            try {
                windowManager.removeViewImmediate(child.view);
            } catch (IllegalArgumentException ignored) {}
        }
        children.clear();
        QaState.recordVariant(this, variant, 0);
        QaState.recordGeometry(this, "");
    }

    private void stopCleanly() {
        removeAllChildren();
        variant = "NONE";
        QaState.recordVariant(this, variant, 0);
        QaState.recordService(this, false);
        stopForeground(STOP_FOREGROUND_REMOVE);
        stopSelf();
    }

    private int dp(float value) {
        return Math.round(value * density);
    }

    private int getDisplayRotation() {
        return getDisplay() == null ? -1 : getDisplay().getRotation();
    }

    private void createNotificationChannel() {
        NotificationManager manager = (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
        manager.createNotificationChannel(new NotificationChannel(
                CHANNEL, "Mobi P1 footprint prototype", NotificationManager.IMPORTANCE_LOW));
    }

    private Notification buildNotification() {
        return new Notification.Builder(this, CHANNEL)
                .setContentTitle("Mobi P1 footprint prototype")
                .setContentText("Low-fidelity overlay footprint feasibility is active")
                .setSmallIcon(android.R.drawable.ic_menu_view)
                .setOngoing(true)
                .build();
    }

    private void registerScreenReceiver() {
        screenReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                if (Intent.ACTION_SCREEN_OFF.equals(intent.getAction())) {
                    QaState.recordScreen(MultiWindowService.this, false);
                } else if (Intent.ACTION_SCREEN_ON.equals(intent.getAction())) {
                    QaState.recordScreen(MultiWindowService.this, true);
                    clampAndUpdate(0);
                }
            }
        };
        IntentFilter filter = new IntentFilter();
        filter.addAction(Intent.ACTION_SCREEN_OFF);
        filter.addAction(Intent.ACTION_SCREEN_ON);
        if (Build.VERSION.SDK_INT >= 33) registerReceiver(screenReceiver, filter, Context.RECEIVER_NOT_EXPORTED);
        else registerReceiver(screenReceiver, filter);
    }

    @Override
    public void onDestroy() {
        removeAllChildren();
        if (screenReceiver != null) {
            try { unregisterReceiver(screenReceiver); } catch (IllegalArgumentException ignored) {}
        }
        QaState.recordService(this, false);
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
