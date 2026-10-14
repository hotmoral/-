package org.example.catpresence;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.animation.ValueAnimator;
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
import android.graphics.Insets;
import android.graphics.PixelFormat;
import android.graphics.Rect;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.provider.Settings;
import android.view.Display;
import android.view.Gravity;
import android.view.WindowInsets;
import android.view.WindowManager;
import android.view.WindowMetrics;
import android.view.animation.DecelerateInterpolator;

public final class PresenceService extends Service {
    public static final String ACTION_START = "org.example.catpresence.action.START";
    public static final String ACTION_STOP = "org.example.catpresence.action.STOP";
    public static final String ACTION_MOVE_A_TO_B = "org.example.catpresence.action.MOVE_A_TO_B";
    public static final String ACTION_MOVE_B_TO_A = "org.example.catpresence.action.MOVE_B_TO_A";
    public static final String ACTION_RESET = "org.example.catpresence.action.RESET";

    private static final String CHANNEL_ID = "p0_presence";
    private static final int NOTIFICATION_ID = 1001;

    private final Handler mainHandler = new Handler(Looper.getMainLooper());
    private Context windowContext;
    private WindowManager windowManager;
    private WindowManager.LayoutParams layoutParams;
    private CatPlaceholderView catView;
    private boolean overlayAttached;
    private boolean receiverRegistered;
    private ValueAnimator moveAnimator;

    private float pointerDownRawX;
    private float pointerDownRawY;
    private int pointerDownWindowX;
    private int pointerDownWindowY;
    private boolean pointerMoved;

    private int windowSizePx;
    private int marginPx;
    private int dragThresholdPx;

    private final BroadcastReceiver screenReceiver = new BroadcastReceiver() {
        @Override
        public void onReceive(Context context, Intent intent) {
            String action = intent.getAction();
            if (Intent.ACTION_SCREEN_OFF.equals(action)) {
                QaState.appendEvent(PresenceService.this, "screen_off");
                sampleEnvironment("screen_off");
            } else if (Intent.ACTION_SCREEN_ON.equals(action)) {
                QaState.appendEvent(PresenceService.this, "screen_on");
                mainHandler.postDelayed(() -> sampleEnvironment("screen_on"), 250);
            }
        }
    };

    @Override
    public void onCreate() {
        super.onCreate();
        QaState.putBoolean(this, "serviceActive", true);
        QaState.appendEvent(this, "service_create");

        windowContext = createWindowContext(WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY, null);
        windowManager = windowContext.getSystemService(WindowManager.class);
        windowSizePx = dp(112);
        marginPx = dp(12);
        dragThresholdPx = dp(5);

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
            shutdown(true);
            return START_NOT_STICKY;
        }

        if (!Settings.canDrawOverlays(this)) {
            QaState.appendEvent(this, "overlay_permission_missing");
            QaState.putBoolean(this, "userEnabled", false);
            stopSelf();
            return START_NOT_STICKY;
        }

        if (ACTION_START.equals(action)) {
            QaState.putBoolean(this, "userEnabled", true);
            QaState.appendEvent(this, "explicit_start");
        } else if (action == null && !QaState.getBoolean(this, "userEnabled", false)) {
            QaState.appendEvent(this, "sticky_restart_ignored_user_disabled");
            stopSelf();
            return START_NOT_STICKY;
        }

        ensureForeground();
        ensureOverlay();

        if (ACTION_MOVE_A_TO_B.equals(action)) {
            animateTo(targetB(), "A_TO_B");
        } else if (ACTION_MOVE_B_TO_A.equals(action)) {
            animateTo(targetA(), "B_TO_A");
        } else if (ACTION_RESET.equals(action)) {
            cancelMoveAnimator();
            int[] a = targetA();
            setPosition(a[0], a[1], true);
            QaState.putString(this, "lastMove", "RESET final=(" + layoutParams.x + "," + layoutParams.y + ")");
            QaState.appendEvent(this, "position_reset");
        }

        sampleEnvironment(action == null ? "sticky_start" : action);
        return START_STICKY;
    }

    private void ensureForeground() {
        NotificationManager nm = getSystemService(NotificationManager.class);
        if (nm.getNotificationChannel(CHANNEL_ID) == null) {
            NotificationChannel channel = new NotificationChannel(
                    CHANNEL_ID,
                    "P0 Cat Presence",
                    NotificationManager.IMPORTANCE_LOW
            );
            channel.setDescription("Technical foreground presence for the P0 prototype");
            nm.createNotificationChannel(channel);
        }

        Intent activityIntent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent = PendingIntent.getActivity(
                this,
                0,
                activityIntent,
                PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );

        Notification notification = new Notification.Builder(this, CHANNEL_ID)
                .setSmallIcon(android.R.drawable.ic_menu_info_details)
                .setContentTitle("Cat Presence P0 active")
                .setContentText("Tap to open prototype controls")
                .setContentIntent(pendingIntent)
                .setOngoing(true)
                .setCategory(Notification.CATEGORY_SERVICE)
                .build();

        if (Build.VERSION.SDK_INT >= 34) {
            startForeground(
                    NOTIFICATION_ID,
                    notification,
                    ServiceInfo.FOREGROUND_SERVICE_TYPE_SPECIAL_USE
            );
        } else {
            startForeground(NOTIFICATION_ID, notification);
        }
    }

    private void ensureOverlay() {
        if (overlayAttached) return;

        int flags = WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL
                | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS
                | WindowManager.LayoutParams.FLAG_ALT_FOCUSABLE_IM;

        layoutParams = new WindowManager.LayoutParams(
                windowSizePx,
                windowSizePx,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                flags,
                PixelFormat.TRANSLUCENT
        );
        layoutParams.gravity = Gravity.TOP | Gravity.START;
        layoutParams.alpha = 1.0f;
        layoutParams.setTitle("CatPresenceP0Window");

        int savedX = QaState.getInt(this, "windowX", Integer.MIN_VALUE);
        int savedY = QaState.getInt(this, "windowY", Integer.MIN_VALUE);
        int[] a = targetA();
        int initialX = savedX == Integer.MIN_VALUE ? a[0] : savedX;
        int initialY = savedY == Integer.MIN_VALUE ? a[1] : savedY;
        int[] clamped = clamp(initialX, initialY);
        layoutParams.x = clamped[0];
        layoutParams.y = clamped[1];

        catView = new CatPlaceholderView(windowContext);
        catView.setInteractionListener(new CatPlaceholderView.InteractionListener() {
            @Override
            public void onPointerDown(float rawX, float rawY) {
                cancelMoveAnimator();
                pointerDownRawX = rawX;
                pointerDownRawY = rawY;
                pointerDownWindowX = layoutParams.x;
                pointerDownWindowY = layoutParams.y;
                pointerMoved = false;
            }

            @Override
            public void onPointerMove(float rawX, float rawY) {
                float dx = rawX - pointerDownRawX;
                float dy = rawY - pointerDownRawY;
                if (!pointerMoved && (Math.abs(dx) >= dragThresholdPx || Math.abs(dy) >= dragThresholdPx)) {
                    pointerMoved = true;
                }
                if (pointerMoved) {
                    setPosition(pointerDownWindowX + Math.round(dx), pointerDownWindowY + Math.round(dy), false);
                }
            }

            @Override
            public void onPointerUp(float rawX, float rawY) {
                if (pointerMoved) {
                    QaState.increment(PresenceService.this, "dragCount");
                    persistWindowState();
                    QaState.appendEvent(PresenceService.this, "drag_end x=" + layoutParams.x + " y=" + layoutParams.y);
                } else {
                    QaState.increment(PresenceService.this, "tapCount");
                    QaState.appendEvent(PresenceService.this, "cat_tap");
                }
                sampleEnvironment("pointer_up");
            }

            @Override
            public void onPointerCancel() {
                pointerMoved = false;
                QaState.appendEvent(PresenceService.this, "pointer_cancel");
            }

            @Override
            public void onInsetsChanged() {
                sampleEnvironment("root_insets_changed");
            }
        });

        windowManager.addView(catView, layoutParams);
        overlayAttached = true;
        QaState.putBoolean(this, "overlayAttached", true);
        QaState.appendEvent(this, "overlay_added x=" + layoutParams.x + " y=" + layoutParams.y);
        persistWindowState();
        catView.post(this::persistWindowState);
    }

    private void animateTo(int[] requestedTarget, String label) {
        if (!overlayAttached || layoutParams == null) return;
        cancelMoveAnimator();

        int startX = layoutParams.x;
        int startY = layoutParams.y;
        int[] target = clamp(requestedTarget[0], requestedTarget[1]);
        int targetX = target[0];
        int targetY = target[1];
        int[] updates = {0};
        boolean[] cancelled = {false};
        long started = System.currentTimeMillis();

        moveAnimator = ValueAnimator.ofFloat(0f, 1f);
        moveAnimator.setDuration(800L);
        moveAnimator.setInterpolator(new DecelerateInterpolator());
        moveAnimator.addUpdateListener(animation -> {
            float t = (float) animation.getAnimatedValue();
            int x = Math.round(startX + (targetX - startX) * t);
            int y = Math.round(startY + (targetY - startY) * t);
            setPosition(x, y, false);
            updates[0]++;
        });
        moveAnimator.addListener(new AnimatorListenerAdapter() {
            @Override
            public void onAnimationCancel(Animator animation) {
                cancelled[0] = true;
            }

            @Override
            public void onAnimationEnd(Animator animation) {
                if (cancelled[0] || layoutParams == null) return;
                setPosition(targetX, targetY, true);
                int error = Math.max(Math.abs(layoutParams.x - targetX), Math.abs(layoutParams.y - targetY));
                long duration = System.currentTimeMillis() - started;
                String result = label
                        + " start=(" + startX + "," + startY + ")"
                        + " target=(" + targetX + "," + targetY + ")"
                        + " final=(" + layoutParams.x + "," + layoutParams.y + ")"
                        + " errorPx=" + error
                        + " updates=" + updates[0]
                        + " durationMs=" + duration;
                QaState.putString(PresenceService.this, "lastMove", result);
                QaState.appendEvent(PresenceService.this, "move_complete " + result);
                sampleEnvironment("move_complete");
            }
        });
        QaState.appendEvent(this, "move_start " + label + " from=" + startX + "," + startY + " to=" + targetX + "," + targetY);
        moveAnimator.start();
    }

    private void cancelMoveAnimator() {
        if (moveAnimator != null) {
            moveAnimator.cancel();
            moveAnimator = null;
        }
    }

    private void setPosition(int x, int y, boolean persist) {
        if (!overlayAttached || layoutParams == null || catView == null) return;
        int[] clamped = clamp(x, y);
        layoutParams.x = clamped[0];
        layoutParams.y = clamped[1];
        try {
            windowManager.updateViewLayout(catView, layoutParams);
        } catch (IllegalArgumentException ignored) {
            return;
        }
        if (persist) {
            persistWindowState();
        }
    }

    private int[] targetA() {
        int[] safe = safeRegion();
        return new int[]{safe[0], safe[1]};
    }

    private int[] targetB() {
        int[] safe = safeRegion();
        return new int[]{safe[2], safe[3]};
    }

    private int[] clamp(int x, int y) {
        int[] safe = safeRegion();
        int cx = Math.max(safe[0], Math.min(x, safe[2]));
        int cy = Math.max(safe[1], Math.min(y, safe[3]));
        return new int[]{cx, cy};
    }

    private int[] safeRegion() {
        WindowMetrics metrics = windowManager.getCurrentWindowMetrics();
        Rect bounds = metrics.getBounds();
        WindowInsets wi = metrics.getWindowInsets();
        Insets system = wi.getInsetsIgnoringVisibility(
                WindowInsets.Type.systemBars() | WindowInsets.Type.displayCutout()
        );
        int minX = bounds.left + system.left + marginPx;
        int minY = bounds.top + system.top + marginPx;
        int maxX = bounds.right - system.right - marginPx - windowSizePx;
        int maxY = bounds.bottom - system.bottom - marginPx - windowSizePx;
        if (maxX < minX) maxX = minX;
        if (maxY < minY) maxY = minY;
        return new int[]{minX, minY, maxX, maxY};
    }

    private void persistWindowState() {
        if (layoutParams == null) return;
        QaState.putInt(this, "windowX", layoutParams.x);
        QaState.putInt(this, "windowY", layoutParams.y);
        QaState.putInt(this, "windowW", windowSizePx);
        QaState.putInt(this, "windowH", windowSizePx);
        if (catView != null && catView.getWidth() > 0) {
            QaState.putString(this, "visualBoundsLocal", QaState.rectToString(catView.getVisualBoundsLocal()));
            QaState.putString(this, "bodyBoundsLocal", QaState.rectToString(catView.getBodyBoundsLocal()));
            QaState.putString(this, "touchBoundsLocal", QaState.rectToString(catView.getTouchBoundsLocal()));
        }
    }

    private void sampleEnvironment(String reason) {
        if (windowManager == null) return;
        try {
            WindowMetrics metrics = windowManager.getCurrentWindowMetrics();
            Rect bounds = metrics.getBounds();
            WindowInsets wi = metrics.getWindowInsets();
            boolean imeVisible = wi.isVisible(WindowInsets.Type.ime());
            Insets ime = wi.getInsets(WindowInsets.Type.ime());

            QaState.putString(this, "globalBounds", bounds.left + "," + bounds.top + "," + bounds.right + "," + bounds.bottom);
            QaState.putBoolean(this, "imeVisible", imeVisible);
            QaState.putInt(this, "imeBottom", ime.bottom);
            if (imeVisible) {
                QaState.putBoolean(this, "imeEverVisible", true);
                int priorMax = QaState.getInt(this, "maxImeBottom", 0);
                if (ime.bottom > priorMax) {
                    QaState.putInt(this, "maxImeBottom", ime.bottom);
                }
            }
            Display display = windowContext.getDisplay();
            QaState.putInt(this, "rotation", display == null ? -1 : display.getRotation());
            QaState.putInt(this, "orientation", windowContext.getResources().getConfiguration().orientation);
            QaState.putString(this, "sampleReason", reason);
        } catch (RuntimeException e) {
            QaState.appendEvent(this, "sample_error " + e.getClass().getSimpleName());
        }
    }

    @Override
    public void onConfigurationChanged(Configuration newConfig) {
        super.onConfigurationChanged(newConfig);
        QaState.appendEvent(this, "configuration_changed orientation=" + newConfig.orientation);
        mainHandler.postDelayed(() -> {
            if (overlayAttached && layoutParams != null) {
                setPosition(layoutParams.x, layoutParams.y, true);
                sampleEnvironment("configuration_changed");
            }
        }, 250L);
    }

    private void shutdown(boolean explicitUserStop) {
        if (explicitUserStop) {
            QaState.putBoolean(this, "userEnabled", false);
        }
        cancelMoveAnimator();
        removeOverlay();
        stopForeground(STOP_FOREGROUND_REMOVE);
        stopSelf();
    }

    private void removeOverlay() {
        if (!overlayAttached || catView == null) return;
        try {
            windowManager.removeView(catView);
        } catch (IllegalArgumentException ignored) {
            // Already detached.
        }
        overlayAttached = false;
        QaState.putBoolean(this, "overlayAttached", false);
        QaState.appendEvent(this, "overlay_removed");
        catView = null;
        layoutParams = null;
    }

    @Override
    public void onDestroy() {
        cancelMoveAnimator();
        removeOverlay();
        if (receiverRegistered) {
            try {
                unregisterReceiver(screenReceiver);
            } catch (IllegalArgumentException ignored) {
                // Already unregistered.
            }
            receiverRegistered = false;
        }
        QaState.putBoolean(this, "serviceActive", false);
        QaState.appendEvent(this, "service_destroy");
        super.onDestroy();
    }

    private int dp(int dp) {
        return Math.round(dp * getResources().getDisplayMetrics().density);
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }
}
