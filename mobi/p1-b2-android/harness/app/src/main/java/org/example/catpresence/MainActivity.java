package org.example.catpresence;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.provider.Settings;
import android.view.MotionEvent;
import android.view.View;

public final class MainActivity extends Activity {
    public static final String EXTRA_QA_COMMAND = "p1_qa_command";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(new HostSurfaceView());
        QaState.appendEvent(this, "p1_activity_create");
        handleIntent(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleIntent(intent);
    }

    @Override
    protected void onResume() {
        super.onResume();
        QaState.appendEvent(this, "p1_activity_resume");
    }

    private void handleIntent(Intent intent) {
        if (intent == null) return;
        String command = intent.getStringExtra(EXTRA_QA_COMMAND);
        if (command == null || command.isEmpty()) return;
        QaState.putString(this, "lastQaCommand", command);
        QaState.appendEvent(this, "qa_command " + command);

        String action = null;
        switch (command) {
            case "start_f0": action = PresenceService.ACTION_START_F0; break;
            case "start_f1": action = PresenceService.ACTION_START_F1; break;
            case "start_f2": action = PresenceService.ACTION_START_F2; break;
            case "set_f0": action = PresenceService.ACTION_SET_F0; break;
            case "set_f1": action = PresenceService.ACTION_SET_F1; break;
            case "set_f2": action = PresenceService.ACTION_SET_F2; break;
            case "move_stress": action = PresenceService.ACTION_MOVE_STRESS; break;
            case "stop": action = PresenceService.ACTION_STOP; break;
            case "reset_counts":
                QaState.putInt(this, "hostTouchCount", 0);
                QaState.putInt(this, "overlayTouchCount", 0);
                QaState.putInt(this, "touch_ALL", 0);
                QaState.putInt(this, "touch_CORE", 0);
                QaState.putInt(this, "touch_FORE", 0);
                QaState.putInt(this, "touch_HIND", 0);
                QaState.putInt(this, "touch_TAIL", 0);
                QaState.appendEvent(this, "touch_counts_reset");
                return;
            default:
                QaState.appendEvent(this, "qa_command_unknown " + command);
                return;
        }

        Intent serviceIntent = new Intent(this, PresenceService.class).setAction(action);
        if (PresenceService.ACTION_STOP.equals(action)) {
            startService(serviceIntent);
        } else {
            startForegroundService(serviceIntent);
        }
    }

    private final class HostSurfaceView extends View {
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);

        HostSurfaceView() {
            super(MainActivity.this);
            setBackgroundColor(Color.rgb(245, 245, 245));
            setFocusable(true);
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            paint.setColor(Color.rgb(30, 30, 30));
            paint.setTextSize(36f);
            canvas.drawText("Mobi P1-B2.2 footprint host", 36f, 72f, paint);
            paint.setTextSize(26f);
            canvas.drawText("Overlay permission=" + Settings.canDrawOverlays(MainActivity.this), 36f, 116f, paint);
            canvas.drawText("Tap-through host surface", 36f, 156f, paint);
        }

        @Override
        public boolean onTouchEvent(MotionEvent event) {
            if (event.getActionMasked() == MotionEvent.ACTION_UP) {
                QaState.increment(MainActivity.this, "hostTouchCount");
                QaState.putInt(MainActivity.this, "lastHostX", Math.round(event.getX()));
                QaState.putInt(MainActivity.this, "lastHostY", Math.round(event.getY()));
                QaState.appendEvent(MainActivity.this,
                        "host_touch x=" + Math.round(event.getX()) + " y=" + Math.round(event.getY()));
            }
            return true;
        }
    }
}
