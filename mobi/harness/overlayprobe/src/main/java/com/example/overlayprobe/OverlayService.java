package com.example.overlayprobe;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ServiceInfo;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.PixelFormat;
import android.hardware.display.DisplayManager;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import android.provider.Settings;
import android.util.Log;
import android.view.Display;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowManager;

import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

public final class OverlayService extends Service {
    public static final String ACTION_SMALL = "com.example.overlayprobe.SMALL";
    public static final String ACTION_REMOVE = "com.example.overlayprobe.REMOVE";
    public static final String ACTION_MOVE_TEST = "com.example.overlayprobe.MOVE_TEST";

    private static final String TAG = "OverlayProbe";
    private static final String CHANNEL_ID = "overlay_probe_channel";
    private static final int NOTIFICATION_ID = 1001;
    private static final int MOVEMENT_FRAMES = 300;
    private static final long MOVEMENT_INTERVAL_MS = 33L;

    private static volatile OverlayService instance;

    private WindowManager windowManager;
    private Context windowContext;
    private View overlayView;
    private WindowManager.LayoutParams params;
    private final Handler handler = new Handler(Looper.getMainLooper());
    private int overlayTapCount;
    private int movementFrame;
    private Runnable movementRunnable;

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
        writeText("overlay_count.txt", "0\n");
        writeText("movement_result.txt", "not_started\n");
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
        } else if (ACTION_MOVE_TEST.equals(action)) {
            startMovementTest();
        } else {
            showSmall();
        }
        return START_STICKY;
    }

    void handleCommand(String mode) {
        handler.post(() -> {
            if ("remove".equals(mode)) {
                removeOverlay();
            } else if ("move".equals(mode)) {
                startMovementTest();
            } else {
                showSmall();
            }
        });
    }

    @Override
    public void onDestroy() {
        stopMovement();
        removeOverlay();
        instance = null;
        Log.i(TAG, "SERVICE_DESTROYED");
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    private void showSmall() {
        stopMovement();
        removeOverlay();

        ProbeShapeView view = new ProbeShapeView(windowContext);
        int size = dp(92);
        params = new WindowManager.LayoutParams(
                size,
                size,
                WindowManager.LayoutParams.TYPE_APPLICATION_OVERLAY,
                WindowManager.LayoutParams.FLAG_NOT_FOCUSABLE
                        | WindowManager.LayoutParams.FLAG_NOT_TOUCH_MODAL
                        | WindowManager.LayoutParams.FLAG_LAYOUT_NO_LIMITS,
                PixelFormat.TRANSLUCENT);
        params.gravity = Gravity.TOP | Gravity.START;
        params.x = dp(48);
        params.y = dp(160);
        params.alpha = 1.0f;
        params.setTitle("OverlayProbeWindow");

        view.setOnTouchListener(new DragTouchListener());
        overlayView = view;
        windowManager.addView(view, params);
        view.post(this::writeGeometry);
        Log.i(TAG, "SMALL_OVERLAY_ADDED sizeDp=92");
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
            writeText("geometry.txt", "detached\n");
            Log.i(TAG, "OVERLAY_REMOVED");
        }
    }

    private void startMovementTest() {
        showSmall();
        movementFrame = 0;
        writeText("movement_result.txt", "running\n");

        movementRunnable = new Runnable() {
            @Override
            public void run() {
                if (overlayView == null || params == null) {
                    writeText("movement_result.txt", "aborted_detached frame=" + movementFrame + "\n");
                    Log.e(TAG, "MOVEMENT_ABORTED frame=" + movementFrame);
                    return;
                }

                int cycle = movementFrame % 120;
                int wave = cycle <= 60 ? cycle : 120 - cycle;
                params.x = dp(32) + dp(4) * wave;
                params.y = dp(150) + dp(2) * ((movementFrame * 3) % 120);
                try {
                    windowManager.updateViewLayout(overlayView, params);
                } catch (RuntimeException e) {
                    writeText("movement_result.txt", "update_failed frame=" + movementFrame + " error=" + e.getClass().getSimpleName() + "\n");
                    Log.e(TAG, "MOVEMENT_UPDATE_FAILED frame=" + movementFrame, e);
                    return;
                }

                if (movementFrame % 30 == 0) {
                    Log.i(TAG, "MOVEMENT_FRAME frame=" + movementFrame + " x=" + params.x + " y=" + params.y);
                }
                movementFrame++;

                if (movementFrame >= MOVEMENT_FRAMES) {
                    boolean attached = overlayView.isAttachedToWindow();
                    writeGeometry();
                    writeText(
                            "movement_result.txt",
                            "completed frames=" + MOVEMENT_FRAMES + " attached=" + attached + "\n");
                    Log.i(TAG, "MOVEMENT_DONE frames=" + MOVEMENT_FRAMES + " attached=" + attached);
                    movementRunnable = null;
                } else {
                    handler.postDelayed(this, MOVEMENT_INTERVAL_MS);
                }
            }
        };
        handler.post(movementRunnable);
    }

    private void stopMovement() {
        if (movementRunnable != null) {
            handler.removeCallbacks(movementRunnable);
            movementRunnable = null;
        }
    }

    private void writeGeometry() {
        if (overlayView == null || !overlayView.isAttachedToWindow()) {
            writeText("geometry.txt", "detached\n");
            return;
        }
        int[] location = new int[2];
        overlayView.getLocationOnScreen(location);
        String value = location[0] + " " + location[1] + " "
                + overlayView.getWidth() + " " + overlayView.getHeight() + "\n";
        writeText("geometry.txt", value);
        Log.i(TAG, "GEOMETRY " + value.trim());
    }

    private void recordOverlayTap(MotionEvent event) {
        overlayTapCount++;
        writeText("overlay_count.txt", Integer.toString(overlayTapCount) + "\n");
        Log.i(TAG, "OVERLAY_TAP count=" + overlayTapCount
                + " localX=" + Math.round(event.getX())
                + " localY=" + Math.round(event.getY()));
    }

    private void writeText(String file, String value) {
        try (FileOutputStream out = openFileOutput(file, MODE_PRIVATE)) {
            out.write(value.getBytes(StandardCharsets.UTF_8));
        } catch (Exception e) {
            Log.e(TAG, "write failed file=" + file, e);
        }
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
                .setContentTitle("Overlay probe active")
                .setContentText("Generic foreground-service runtime test")
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
                    v.post(OverlayService.this::writeGeometry);
                    return true;
                default:
                    return true;
            }
        }
    }

    private static final class ProbeShapeView extends View {
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);

        ProbeShapeView(Context context) {
            super(context);
            setBackgroundColor(Color.TRANSPARENT);
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            float w = getWidth();
            float h = getHeight();
            paint.setColor(Color.rgb(70, 135, 220));
            canvas.drawCircle(w * 0.5f, h * 0.5f, Math.min(w, h) * 0.36f, paint);
            paint.setColor(Color.WHITE);
            paint.setTextAlign(Paint.Align.CENTER);
            paint.setTextSize(Math.min(w, h) * 0.18f);
            canvas.drawText("P", w * 0.5f, h * 0.56f, paint);
        }
    }
}
