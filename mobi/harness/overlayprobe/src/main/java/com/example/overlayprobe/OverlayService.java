package com.example.overlayprobe;

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
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Insets;
import android.graphics.Paint;
import android.graphics.PixelFormat;
import android.graphics.Rect;
import android.hardware.display.DisplayManager;
import android.os.BatteryManager;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.os.PowerManager;
import android.os.SystemClock;
import android.provider.Settings;
import android.util.Log;
import android.view.Display;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowInsets;
import android.view.WindowManager;
import android.view.WindowMetrics;

import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;
import java.util.TimeZone;

public final class OverlayService extends Service {
    public static final String ACTION_SMALL = "com.example.overlayprobe.SMALL";
    public static final String ACTION_REMOVE = "com.example.overlayprobe.REMOVE";

    private static final String TAG = "OverlayProbe";
    private static final String CHANNEL_ID = "overlay_probe_channel";
    private static final int NOTIFICATION_ID = 1001;

    private static volatile OverlayService instance;

    private WindowManager windowManager;
    private Context windowContext;
    private View overlayView;
    private WindowManager.LayoutParams params;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private BroadcastReceiver screenReceiver;
    private String currentMode = "A";
    private int overlayTapCount;

    static OverlayService getInstance() {
        return instance;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        instance = this;
        createChannel();
        Notification notification = buildNotification();
        if (Build.VERSION.SDK_INT >= 34) {
            startForeground(
                    NOTIFICATION_ID,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE);
        } else {
            startForeground(NOTIFICATION_ID, notification);
        }

        DisplayManager displayManager = getSystemService(DisplayManager.class);
        Display display = displayManager.getDisplay(Display.DEFAULT_DISPLAY);
        if (display == null) {
            throw new IllegalStateException("Default display unavailable");
        }
        windowContext = createDisplayContext(display)
                .createWindowContext(WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, null);
        windowManager = windowContext.getSystemService(WindowManager.class);
        writeText("overlay_count.txt", "0\n", false);
        writeText("env_events.txt", "", false);

        screenReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String action = intent == null ? "null" : intent.getAction();
                appendEvent("screenBroadcast=" + action);
                handler.postDelayed(() -> captureEnvironment("broadcast_" + action), 150L);
            }
        };
        IntentFilter screenFilter = new IntentFilter();
        screenFilter.addAction(Intent.ACTION_SCREEN_ON);
        screenFilter.addAction(Intent.ACTION_SCREEN_OFF);
        if (Build.VERSION.SDK_INT >= 33) {
            registerReceiver(screenReceiver, screenFilter, Context.RECEIVER_NOT_EXPORTED);
        } else {
            registerReceiver(screenReceiver, screenFilter);
        }

        Log.i(TAG, "SERVICE_CREATED canDrawOverlays=" + Settings.canDrawOverlays(this));
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        String action = intent == null ? ACTION_SMALL : intent.getAction();
        if (!Settings.canDrawOverlays(this)) {
            Log.e(TAG, "OVERLAY_PERMISSION_MISSING");
            return START_STICKY;
        }
        if (ACTION_REMOVE.equals(action)) {
            removeOverlay();
        } else {
            showSmall(false, false);
        }
        return START_STICKY;
    }

    void handleCommand(String mode) {
        handler.post(() -> {
            if ("remove".equals(mode)) {
                removeOverlay();
            } else if ("modeA".equals(mode)) {
                showSmall(false, false);
            } else if ("modeB".equals(mode)) {
                showSmall(true, false);
            } else if ("modeA_bottom".equals(mode)) {
                showSmall(false, true);
            } else if ("modeB_bottom".equals(mode)) {
                showSmall(true, true);
            } else if ("capture".equals(mode)) {
                captureEnvironment("command_capture");
            } else {
                showSmall(false, false);
            }
        });
    }

    @Override
    public void onDestroy() {
        removeOverlay();
        if (screenReceiver != null) {
            unregisterReceiver(screenReceiver);
            screenReceiver = null;
        }
        instance = null;
        Log.i(TAG, "SERVICE_DESTROYED");
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void showSmall(boolean altFocusableIm, boolean bottom) {
        removeOverlay();
        currentMode = altFocusableIm ? "B_ALT_FOCUSABLE_IM" : "A_NOT_FOCUSABLE_ONLY";

        ProbeShapeView view = new ProbeShapeView(windowContext, altFocusableIm ? "B" : "A");
        int size = dp(92);
        int flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL
                | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS;
        if (altFocusableIm) {
            flags |= WindowManager.LayoutParams.FLAG_ALT_FOCUSABLE_IM;
        }

        params = new WindowManager.LayoutParams(
                size,
                size,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                flags,
                PixelFormat.TRANSLUCENT);
        params.gravity = Gravity.TOP | Gravity.START;

        Rect bounds = windowManager.getCurrentWindowMetrics().getBounds();
        if (bottom) {
            params.x = Math.max(0, (bounds.width() - size) / 2);
            params.y = Math.max(0, bounds.height() - size - dp(110));
        } else {
            params.x = dp(48);
            params.y = dp(160);
        }
        params.alpha = 1.0f;
        params.setTitle("OverlayProbeWindow-" + currentMode);

        view.setOnTouchListener(new DragTouchListener());
        view.setOnApplyWindowInsetsListener((v, insets) -> {
            writeViewInsets("apply", insets);
            handler.post(() -> captureEnvironment("view_insets_apply"));
            return insets;
        });

        overlayView = view;
        windowManager.addView(view, params);
        view.post(() -> {
            writeGeometry();
            view.requestApplyInsets();
            captureEnvironment("overlay_added");
        });
        Log.i(TAG, "SMALL_OVERLAY_ADDED mode=" + currentMode + " bottom=" + bottom);
    }

    private void removeOverlay() {
        if (overlayView != null) {
            try {
                windowManager.removeViewImmediate(overlayView);
            } catch (RuntimeException e) {
                Log.w(TAG, "removeView ignored", e);
            }
            overlayView = null;
            params = null;
            writeText("geometry.txt", "detached\n", false);
            Log.i(TAG, "OVERLAY_REMOVED");
        }
    }

    private void captureEnvironment(String reason) {
        if (windowManager == null || windowContext == null) {
            return;
        }

        WindowMetrics metrics = windowManager.getCurrentWindowMetrics();
        Rect bounds = metrics.getBounds();
        WindowInsets metricsInsets = metrics.getWindowInsets();
        WindowInsets rootInsets = overlayView == null ? null : overlayView.getRootWindowInsets();

        Insets status = metricsInsets.getInsets(WindowInsets.Type.statusBars());
        Insets nav = metricsInsets.getInsets(WindowInsets.Type.navigationBars());
        Insets cutout = metricsInsets.getInsets(WindowInsets.Type.displayCutout());
        Insets gestures = metricsInsets.getInsets(WindowInsets.Type.systemGestures());
        Insets mandatory = metricsInsets.getInsets(WindowInsets.Type.mandatorySystemGestures());
        Insets tappable = metricsInsets.getInsets(WindowInsets.Type.tappableElement());
        Insets systemOverlays = Insets.NONE;
        if (Build.VERSION.SDK_INT >= 34) {
            systemOverlays = metricsInsets.getInsets(WindowInsets.Type.systemOverlays());
        }

        boolean metricsImeVisible = metricsInsets.isVisible(WindowInsets.Type.ime());
        Insets metricsIme = metricsInsets.getInsets(WindowInsets.Type.ime());
        String metricsImeState = classifyIme(metricsImeVisible, metricsIme, true);

        String rootState = "UNKNOWN";
        boolean rootImeVisible = false;
        Insets rootIme = Insets.NONE;
        if (rootInsets != null) {
            rootState = "OBSERVED";
            rootImeVisible = rootInsets.isVisible(WindowInsets.Type.ime());
            rootIme = rootInsets.getInsets(WindowInsets.Type.ime());
        }
        String rootImeState = classifyIme(rootImeVisible, rootIme, rootInsets != null);

        Display display = windowContext.getDisplay();
        int rotation = display == null ? -1 : display.getRotation();
        int displayState = display == null ? Display.STATE_UNKNOWN : display.getState();
        Configuration config = windowContext.getResources().getConfiguration();

        PowerManager powerManager = getSystemService(PowerManager.class);
        boolean interactive = powerManager != null && powerManager.isInteractive();
        BatteryManager batteryManager = getSystemService(BatteryManager.class);
        boolean charging = batteryManager != null && batteryManager.isCharging();
        int batteryLevel = batteryManager == null
                ? Integer.MIN_VALUE
                : batteryManager.getIntProperty(BatteryManager.BATTERY_PROPERTY_CAPACITY);

        String geometry = "detached";
        if (overlayView != null && overlayView.isAttachedToWindow()) {
            int[] location = new int[2];
            overlayView.getLocationOnScreen(location);
            geometry = location[0] + "," + location[1] + ","
                    + overlayView.getWidth() + "," + overlayView.getHeight();
        }

        String snapshot =
                "reason=" + reason + "\n"
                        + "elapsedRealtimeMs=" + SystemClock.elapsedRealtime() + "\n"
                        + "wallClockMs=" + System.currentTimeMillis() + "\n"
                        + "timezone=" + TimeZone.getDefault().getID() + "\n"
                        + "mode=" + currentMode + "\n"
                        + "overlayGeometry=" + geometry + "\n"
                        + "windowBounds=" + formatRect(bounds) + "\n"
                        + "density=" + metrics.getDensity() + "\n"
                        + "rotation=" + rotation + "\n"
                        + "orientation=" + config.orientation + "\n"
                        + "displayState=" + displayState + "\n"
                        + "interactive=" + interactive + "\n"
                        + "charging=" + charging + "\n"
                        + "batteryLevel=" + batteryLevel + "\n"
                        + "statusBars=" + formatInsets(status) + "\n"
                        + "navigationBars=" + formatInsets(nav) + "\n"
                        + "displayCutout=" + formatInsets(cutout) + "\n"
                        + "systemGestures=" + formatInsets(gestures) + "\n"
                        + "mandatoryGestures=" + formatInsets(mandatory) + "\n"
                        + "tappableElement=" + formatInsets(tappable) + "\n"
                        + "systemOverlays=" + formatInsets(systemOverlays) + "\n"
                        + "metricsImeVisible=" + metricsImeVisible + "\n"
                        + "metricsImeInsets=" + formatInsets(metricsIme) + "\n"
                        + "metricsImeState=" + metricsImeState + "\n"
                        + "rootInsetState=" + rootState + "\n"
                        + "rootImeVisible=" + rootImeVisible + "\n"
                        + "rootImeInsets=" + formatInsets(rootIme) + "\n"
                        + "rootImeState=" + rootImeState + "\n";

        writeText("env_latest.txt", snapshot, false);
        writeText("env_events.txt", "---\n" + snapshot, true);
        Log.i(TAG, "ENV_SNAPSHOT reason=" + reason
                + " mode=" + currentMode
                + " metricsImeVisible=" + metricsImeVisible
                + " metricsIme=" + formatInsets(metricsIme)
                + " rootImeVisible=" + rootImeVisible
                + " rootIme=" + formatInsets(rootIme));
    }

    private void writeViewInsets(String reason, WindowInsets insets) {
        boolean visible = insets.isVisible(WindowInsets.Type.ime());
        Insets ime = insets.getInsets(WindowInsets.Type.ime());
        String value =
                "reason=" + reason + "\n"
                        + "elapsedRealtimeMs=" + SystemClock.elapsedRealtime() + "\n"
                        + "mode=" + currentMode + "\n"
                        + "imeVisible=" + visible + "\n"
                        + "imeInsets=" + formatInsets(ime) + "\n"
                        + "imeState=" + classifyIme(visible, ime, true) + "\n";
        writeText("overlay_view_insets_latest.txt", value, false);
        writeText("overlay_view_insets_events.txt", "---\n" + value, true);
    }

    private static String classifyIme(boolean visible, Insets insets, boolean sourceAvailable) {
        if (!sourceAvailable) {
            return "UNKNOWN";
        }
        if (!visible) {
            return "OBSERVED_HIDDEN";
        }
        if (insets.left != 0 || insets.top != 0 || insets.right != 0 || insets.bottom != 0) {
            return "OBSERVED_DOCKED_OR_EDGE_INSETTING";
        }
        return "PARTIAL_VISIBLE_NO_EDGE_INSET";
    }

    private void writeGeometry() {
        if (overlayView == null || !overlayView.isAttachedToWindow()) {
            writeText("geometry.txt", "detached\n", false);
            return;
        }
        int[] location = new int[2];
        overlayView.getLocationOnScreen(location);
        String value = location[0] + " " + location[1] + " "
                + overlayView.getWidth() + " " + overlayView.getHeight() + "\n";
        writeText("geometry.txt", value, false);
        Log.i(TAG, "GEOMETRY " + value.trim());
    }

    private void recordOverlayTap(MotionEvent event) {
        overlayTapCount++;
        writeText("overlay_count.txt", Integer.toString(overlayTapCount) + "\n", false);
        Log.i(TAG, "OVERLAY_TAP count=" + overlayTapCount
                + " localX=" + Math.round(event.getX())
                + " localY=" + Math.round(event.getY()));
    }

    private void appendEvent(String value) {
        writeText("env_events.txt",
                "---\nreason=event\nelapsedRealtimeMs=" + SystemClock.elapsedRealtime() + "\n" + value + "\n",
                true);
    }

    private void writeText(String file, String value, boolean append) {
        try (FileOutputStream out = openFileOutput(file, append ? MODE_APPEND : MODE_PRIVATE)) {
            out.write(value.getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            Log.e(TAG, "write failed file=" + file, e);
        }
    }

    private static String formatInsets(Insets insets) {
        return insets.left + "," + insets.top + "," + insets.right + "," + insets.bottom;
    }

    private static String formatRect(Rect rect) {
        return rect.left + "," + rect.top + "," + rect.right + "," + rect.bottom;
    }

    private int dp(int value) {
        return Math.round(value * windowContext.getResources().getDisplayMetrics().density);
    }

    private void createChannel() {
        NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID,
                "Overlay probe service",
                NotificationManager.IMPORTANCE_LOW);
        getSystemService(NotificationManager.class).createNotificationChannel(channel);
    }

    private Notification buildNotification() {
        Intent open = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(
                this,
                0,
                open,
                PendingIntent.FLAG_IMMUTABLE | PendingIntent.FLAG_UPDATE_CURRENT);
        return new Notification.Builder(this, CHANNEL_ID)
                .setSmallIcon(android.R.drawable.ic_menu_view)
                .setContentTitle("Environment probe active")
                .setContentText("Generic structural-signal runtime test")
                .setContentIntent(pendingIntent)
                .setOngoing(true)
                .build();
    }

    private final class DragTouchListener implements View.OnTouchListener {
        private float downRawX;
        private float downRawY;
        private int startX;
        private int startY;

        @Override
        public boolean onTouch(View v, MotionEvent event) {
            if (params == null) {
                return false;
            }
            switch (event.getActionMasked()) {
                case MotionEvent.ACTION_DOWN:
                    downRawX = event.getRawX();
                    downRawY = event.getRawY();
                    startX = params.x;
                    startY = params.y;
                    recordOverlayTap(event);
                    return true;
                case MotionEvent.ACTION_MOVE:
                    params.x = startX + Math.round(event.getRawX() - downRawX);
                    params.y = startY + Math.round(event.getRawY() - downRawY);
                    windowManager.updateViewLayout(overlayView, params);
                    return true;
                case MotionEvent.ACTION_UP:
                case MotionEvent.ACTION_CANCEL:
                    v.post(() -> {
                        writeGeometry();
                        captureEnvironment("touch_end");
                    });
                    return true;
                default:
                    return true;
            }
        }
    }

    private static final class ProbeShapeView extends View {
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);
        private final String label;

        ProbeShapeView(Context context, String label) {
            super(context);
            this.label = label;
            setBackgroundColor(Color.TRANSPARENT);
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            float w = getWidth();
            float h = getHeight();
            paint.setColor("B".equals(label) ? Color.rgb(65, 165, 105) : Color.rgb(70, 135, 220));
            canvas.drawCircle(w * 0.5f, h * 0.5f, Math.min(w, h) * 0.36f, paint);
            paint.setColor(Color.WHITE);
            paint.setTextAlign(Paint.Align.CENTER);
            paint.setTextSize(Math.min(w, h) * 0.18f);
            canvas.drawText(label, w * 0.5f, h * 0.56f, paint);
        }
    }
}
