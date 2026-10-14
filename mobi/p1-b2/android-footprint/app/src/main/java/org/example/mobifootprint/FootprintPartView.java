package org.example.mobifootprint;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.MotionEvent;
import android.view.View;

public final class FootprintPartView extends View {
    public interface DragDelegate {
        void onDragBy(float dx, float dy);
    }

    private final String part;
    private final Paint fill = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint text = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final DragDelegate dragDelegate;
    private float downRawX;
    private float downRawY;
    private float lastRawX;
    private float lastRawY;
    private boolean moved;

    public FootprintPartView(Context context, String part, int color, DragDelegate dragDelegate) {
        super(context);
        this.part = part;
        this.dragDelegate = dragDelegate;
        fill.setColor(color);
        text.setColor(Color.WHITE);
        text.setTextSize(24f);
        text.setFakeBoldText(true);
        setTag("MobiFootprintPart-" + part);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float r = Math.min(getWidth(), getHeight()) * 0.22f;
        canvas.drawRoundRect(0, 0, getWidth(), getHeight(), r, r, fill);
        canvas.drawText(part, 8f, Math.min(getHeight() - 8f, 30f), text);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        switch (event.getActionMasked()) {
            case MotionEvent.ACTION_DOWN:
                downRawX = lastRawX = event.getRawX();
                downRawY = lastRawY = event.getRawY();
                moved = false;
                QaState.recordHit(getContext(), part);
                return true;
            case MotionEvent.ACTION_MOVE:
                float dx = event.getRawX() - lastRawX;
                float dy = event.getRawY() - lastRawY;
                if (Math.abs(event.getRawX() - downRawX) + Math.abs(event.getRawY() - downRawY) > 8f) {
                    moved = true;
                }
                lastRawX = event.getRawX();
                lastRawY = event.getRawY();
                if ("CORE".equals(part) && dragDelegate != null) {
                    dragDelegate.onDragBy(dx, dy);
                }
                return true;
            case MotionEvent.ACTION_UP:
            case MotionEvent.ACTION_CANCEL:
                return true;
            default:
                return true;
        }
    }

    public String getPart() {
        return part;
    }
}
