package org.example.catpresence;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.pm.ServiceInfo;
import android.content.res.Configuration;
import android.graphics.PixelFormat;
import android.graphics.Rect;
import android.hardware.display.DisplayManager;
import android.os.Build;
import android.os.IBinder;
import android.provider.Settings;
import android.view.Display;
import android.view.Gravity;
import android.view.WindowManager;
import android.view.WindowMetrics;

import java.util.LinkedHashMap;
import java.util.Map;

public final class PresenceService extends Service {
    public static final String ACTION_START_F0 = "org.example.catpresence.action.P1_START_F0";
    public static final String ACTION_START_F1 = "org.example.catpresence.action.P1_START_F1";
    public static final String ACTION_START_F2 = "org.example.catpresence.action.P1_START_F2";
    public static final String ACTION_SET_F0 = "org.example.catpresence.action.P1_SET_F0";
    public static final String ACTION_SET_F1 = "org.example.catpresence.action.P1_SET_F1";
    public static final String ACTION_SET_F2 = "org.example.catpresence.action.P1_SET_F2";
    public static final String ACTION_MOVE_STRESS = "org.example.catpresence.action.P1_MOVE_STRESS";
    public static final String ACTION_STOP = "org.example.catpresence.action.P1_STOP";

    public static final String MODE_F0 = "F0_SINGLE_ALL";
    public static final String MODE_F1 = "F1_CORE_TAIL";
    public static final String MODE_F2 = "F2_CORE_FORE_HIND_TAIL";

    private static final String CHANNEL_ID = "p1_b22_multiwindow";
    private static final int NOTIFICATION_ID = 1202;

    private Context windowContext;
    private WindowManager windowManager;
    private final LinkedHashMap<String, PartWindow> parts = new LinkedHashMap<>();
    private boolean receiverRegistered;
    private String mode = MODE_F0;
    private int rootX;
    private int rootY;
    private int marginPx;

    private final BroadcastReceiver screenReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            if (Intent.ACTION_SCREEN_OFF.equals(intent.getAction())) {
                QaState.appendEvent(PresenceService.this, "screen_off");
            } else if (Intent.ACTION_SCREEN_ON.equals(intent.getAction())) {
                QaState.appendEvent(PresenceService.this, "screen_on");
            }
        }
    };

    private static final class PartWindow {
        final String id;
        final int offsetXDp;
        final int offsetYDp;
        final int widthDp;
        final int heightDp;
        final FootprintWindowView view;
        final WindowManager.LayoutParams params;

        PartWindow(String id, int offsetXDp, int offsetYDp, int widthDp, int heightDp,
                   FootprintWindowView view, WindowManager.LayoutParams params) {
            this.id = id;
            this.offsetXDp = offsetXDp;
            this.offsetYDp = offsetYDp;
            this.widthDp = widthDp;
            this.heightDp = heightDp;
            this.view = view;
            this.params = params;
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        QaState.putBoolean(this, "serviceActive", true);
        QaState.appendEvent(this, "p1_service_create");
        QaState.putString(this, "prototype", "P1_B2_2_MULTIWINDOW_V01");

        DisplayManager dm = getSystemService(DisplayManager.class);
        Display display = dm == null ? null : dm.getDisplay(Display.DEFAULT_DISPLAY);
        if (display == null) throw new IllegalStateException("primary display unavailable");
        windowContext = createDisplayContext(display).createWindowContext(
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, null);
        windowManager = windowContext.getSystemService(WindowManager.class);
        marginPx = dp(12);

        IntentFilter filter = new IntentFilter();
        filter.addAction(Intent.ACTION_SCREEN_ON);
        filter.addAction(Intent.ACTION_SCREEN_OFF);
        if (Build.VERSION.SDK_INT >= 33) {
            registerReceiver(screenReceiver, filter, Context.RECEIVER_NOT_EXPORTED);
        } else {
            registerReceiver(screenReceiver, filter);
        }
        receiverRegistered = true;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String action = intent == null ? null : intent.getAction();
        if (ACTION_STOP.equals(action)) {
            QaState.appendEvent(this, "explicit_stop");
            shutdown();
            return START_NOT_STICKY;
        }
        if (!Settings.canDrawOverlays(this)) {
            QaState.appendEvent(this, "overlay_permission_missing");
            stopSelf();
            return START_NOT_STICKY;
        }

        ensureForeground();
        if (parts.isEmpty()) {
            int[] initial = clampRoot(dp(100), dp(160));
            rootX = initial[0];
            rootY = initial[1];
        }

        if (ACTION_START_F1.equals(action) || ACTION_SET_F1.equals(action)) {
            applyMode(MODE_F1);
        } else if (ACTION_START_F2.equals(action) || ACTION_SET_F2.equals(action)) {
            applyMode(MODE_F2);
        } else if (ACTION_START_F0.equals(action) || ACTION_SET_F0.equals(action) || parts.isEmpty()) {
            applyMode(MODE_F0);
        } else if (ACTION_MOVE_STRESS.equals(action)) {
            runMoveStress();
        }

        QaState.putBoolean(this, "userEnabled", true);
        persistState();
        return START_STICKY;
    }

    private void ensureForeground() {
        NotificationManager nm = getSystemService(NotificationManager.class);
        if (nm.getNotificationChannel(CHANNEL_ID) == null) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID, "P1 footprint feasibility", NotificationManager.IMPORTANCE_LOW);
            channel.setDescription("Technical multi-Window footprint feasibility prototype");
            nm.createNotificationChannel(channel);
        }
        PendingIntent pendingIntent = PendingIntent.getActivity(
                this, 0, new Intent(this, MainActivity.class),
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        Notification n = new Notification.Builder(this, CHANNEL_ID)
                .setSmallIcon(android.R.drawable.ic_menu_info_details)
                .setContentTitle("Mobi P1 footprint test active")
                .setContentText("Technical multi-Window overlay experiment")
                .setContentIntent(pendingIntent)
                .setOngoing(true)
                .setCategory(Notification.CATEGORY_SERVICE)
                .build();
        if (Build.VERSION.SDK_INT >= 34) {
            startForeground(NOTIFICATION_ID, n, ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE);
        } else {
            startForeground(NOTIFICATION_ID, n);
        }
    }

    private int overlayFlags() {
        return WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL
                | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS;
    }

    private void applyMode(String newMode) {
        removeAllWindows();
        mode = newMode;
        int[] clamped = clampRoot(rootX, rootY);
        rootX = clamped[0];
        rootY = clamped[1];

        if (MODE_F0.equals(mode)) {
            addPart("ALL", 0, 0, 154, 122);
        } else if (MODE_F1.equals(mode)) {
            addPart("CORE", 0, 0, 96, 122);
            addPart("TAIL", 94, 10, 60, 22);
        } else if (MODE_F2.equals(mode)) {
            addPart("CORE", 0, 0, 96, 80);
            addPart("FORE", 8, 72, 20, 48);
            addPart("HIND", 68, 72, 24, 50);
            addPart("TAIL", 94, 10, 60, 22);
        } else {
            throw new IllegalArgumentException("unknown mode " + mode);
        }
        QaState.appendEvent(this, "mode_applied " + mode + " windows=" + parts.size());
        persistState();
    }

    private void addPart(String id, int offsetXDp, int offsetYDp, int widthDp, int heightDp) {
        FootprintWindowView view = new FootprintWindowView(windowContext, id);
        WindowManager.LayoutParams lp = new WindowManager.LayoutParams(
                dp(widthDp), dp(heightDp), WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                overlayFlags(), PixelFormat.TRANSLUCENT);
        lp.gravity = Gravity.TOP | Gravity.START;
        lp.x = rootX + dp(offsetXDp);
        lp.y = rootY + dp(offsetYDp);
        lp.setTitle("MobiP1" + mode.substring(0, 2) + "_" + id);
        windowManager.addView(view, lp);
        parts.put(id, new PartWindow(id, offsetXDp, offsetYDp, widthDp, heightDp, view, lp));
    }

    private void removeAllWindows() {
        for (PartWindow part : parts.values()) {
            try {
                windowManager.removeViewImmediate(part.view);
            } catch (RuntimeException ignored) {
            }
        }
        parts.clear();
        QaState.putBoolean(this, "overlayAttached", false);
        QaState.putInt(this, "windowCount", 0);
    }

    private void updatePositions() {
        for (PartWindow part : parts.values()) {
            part.params.x = rootX + dp(part.offsetXDp);
            part.params.y = rootY + dp(part.offsetYDp);
            windowManager.updateViewLayout(part.view, part.params);
        }
        persistState();
    }

    private void runMoveStress() {
        if (parts.isEmpty()) return;
        int startX = rootX;
        int startY = rootY;
        int exceptions = 0;
        int maxRelativeError = 0;
        for (int i = 0; i < 300; i++) {
            double phase = (2.0 * Math.PI * i) / 299.0;
            int requestedX = startX + Math.round((float) (dp(36) * Math.sin(phase)));
            int requestedY = startY + Math.round((float) (dp(18) * Math.sin(phase * 2.0)));
            int[] p = clampRoot(requestedX, requestedY);
            rootX = p[0];
            rootY = p[1];
            for (PartWindow part : parts.values()) {
                int expectedX = rootX + dp(part.offsetXDp);
                int expectedY = rootY + dp(part.offsetYDp);
                part.params.x = expectedX;
                part.params.y = expectedY;
                try {
                    windowManager.updateViewLayout(part.view, part.params);
                } catch (RuntimeException e) {
                    exceptions++;
                }
                maxRelativeError = Math.max(maxRelativeError,
                        Math.max(Math.abs(part.params.x - expectedX), Math.abs(part.params.y - expectedY)));
            }
        }
        rootX = startX;
        rootY = startY;
        try {
            updatePositions();
        } catch (RuntimeException e) {
            exceptions++;
        }
        QaState.putInt(this, "stressUpdateCount", 300);
        QaState.putInt(this, "stressExceptions", exceptions);
        QaState.putInt(this, "maxRelativeErrorPx", maxRelativeError);
        QaState.appendEvent(this, "move_stress_complete mode=" + mode
                + " updates=300 exceptions=" + exceptions + " maxRelativeErrorPx=" + maxRelativeError);
        persistState();
    }

    private int[] clampRoot(int x, int y) {
        Rect bounds = windowManager.getCurrentWindowMetrics().getBounds();
        int maxX = Math.max(marginPx, bounds.width() - dp(154) - marginPx);
        int maxY = Math.max(marginPx, bounds.height() - dp(122) - marginPx);
        return new int[]{
                Math.max(marginPx, Math.min(x, maxX)),
                Math.max(marginPx, Math.min(y, maxY))
        };
    }

    private void persistState() {
        QaState.putString(this, "mode", mode);
        QaState.putInt(this, "windowCount", parts.size());
        QaState.putBoolean(this, "overlayAttached", !parts.isEmpty());
        QaState.putInt(this, "rootX", rootX);
        QaState.putInt(this, "rootY", rootY);
        QaState.putInt(this, "gapTestX", rootX + dp(48));
        QaState.putInt(this, "gapTestY", rootY + dp(100));
        WindowMetrics metrics = windowManager.getCurrentWindowMetrics();
        Rect b = metrics.getBounds();
        QaState.putString(this, "globalBounds", b.left + "," + b.top + "," + b.right + "," + b.bottom);
        for (String id : new String[]{"ALL", "CORE", "FORE", "HIND", "TAIL"}) {
            PartWindow part = parts.get(id);
            if (part == null) {
                QaState.putInt(this, "part_" + id + "_present", 0);
                continue;
            }
            QaState.putInt(this, "part_" + id + "_present", 1);
            QaState.putInt(this, "part_" + id + "_x", part.params.x);
            QaState.putInt(this, "part_" + id + "_y", part.params.y);
            QaState.putInt(this, "part_" + id + "_w", part.params.width);
            QaState.putInt(this, "part_" + id + "_h", part.params.height);
        }
        Display display = getDisplay();
        QaState.putInt(this, "rotation", display == null ? -1 : display.getRotation());
        QaState.putInt(this, "orientation", getResources().getConfiguration().orientation);
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        if (!parts.isEmpty()) {
            int[] p = clampRoot(rootX, rootY);
            rootX = p[0];
            rootY = p[1];
            try {
                updatePositions();
            } catch (RuntimeException e) {
                QaState.appendEvent(this, "configuration_update_error " + e.getClass().getSimpleName());
            }
        }
        QaState.appendEvent(this, "configuration_changed orientation=" + newConfig.orientation);
        persistState();
    }

    private void shutdown() {
        removeAllWindows();
        QaState.putBoolean(this, "userEnabled", false);
        QaState.putBoolean(this, "serviceActive", false);
        QaState.appendEvent(this, "p1_service_stop");
        stopForeground(STOP_FOREGROUND_REMOVE);
        stopSelf();
    }

    @Override
    public void onDestroy() {
        removeAllWindows();
        if (receiverRegistered) {
            try { unregisterReceiver(screenReceiver); } catch (RuntimeException ignored) {}
            receiverRegistered = false;
        }
        QaState.putBoolean(this, "serviceActive", false);
        QaState.appendEvent(this, "p1_service_destroy");
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private int dp(int value) {
        return Math.round(value * getResources().getDisplayMetrics().density);
    }
}
