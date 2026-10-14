package com.example.touchhost;

import android.app.Activity;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.os.Bundle;
import android.view.MotionEvent;
import android.view.View;

import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private int touchCount;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        touchCount = 0;
        writeCount();
        setContentView(new TouchSurface(this));
    }

    private void recordTouch() {
        touchCount++;
        writeCount();
    }

    private void writeCount() {
        try (FileOutputStream out = openFileOutput("host_count.txt", MODE_PRIVATE)) {
            out.write((Integer.toString(touchCount) + "\n").getBytes(StandardCharsets.UTF_8));
        } catch (Exception ignored) {
        }
    }

    private final class TouchSurface extends View {
        private final Paint paint = new Paint(Paint.ANTI_ALIAS_FLAG);

        TouchSurface(Activity context) {
            super(context);
            setBackgroundColor(Color.rgb(245, 247, 250));
            paint.setTextAlign(Paint.Align.CENTER);
        }

        @Override
        public boolean onTouchEvent(MotionEvent event) {
            if (event.getActionMasked() == MotionEvent.ACTION_DOWN) {
                recordTouch();
                invalidate();
            }
            return true;
        }

        @Override
        protected void onDraw(Canvas canvas) {
            super.onDraw(canvas);
            paint.setColor(Color.rgb(40, 45, 55));
            paint.setTextSize(52f);
            canvas.drawText("Touch Host", getWidth() * 0.5f, getHeight() * 0.45f, paint);
            paint.setTextSize(38f);
            canvas.drawText("touches=" + touchCount, getWidth() * 0.5f, getHeight() * 0.52f, paint);

            paint.setStyle(Paint.Style.STROKE);
            paint.setStrokeWidth(4f);
            paint.setColor(Color.rgb(120, 130, 150));
            canvas.drawRect(24f, 24f, getWidth() - 24f, getHeight() - 24f, paint);
            paint.setStyle(Paint.Style.FILL);
        }
    }
}
