package org.example.catpresence;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.view.MotionEvent;
import android.view.View;

public final class FootprintWindowView extends View {
    private final String partId;
    private final Paint fill = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint text = new Paint(Paint.ANTI_ALIAS_FLAG);

    public FootprintWindowView(Context context, String partId) {
        super(context);
        this.partId = partId;
        setBackgroundColor(Color.TRANSPARENT);
        fill.setColor(colorFor(partId));
        fill.setStyle(Paint.Style.FILL);
        text.setColor(Color.WHITE);
        text.setTextAlign(Paint.Align.CENTER);
        text.setTextSize(dp(11));
        setClickable(true);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float w = getWidth();
        float h = getHeight();
        float r = Math.min(w, h) * 0.18f;
        canvas.drawRoundRect(1f, 1f, Math.max(1f, w - 1f), Math.max(1f, h - 1f), r, r, fill);
        canvas.drawText(partId, w / 2f, h / 2f + text.getTextSize() * 0.35f, text);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (event.getActionMasked() == MotionEvent.ACTION_UP) {
            QaState.increment(getContext(), "overlayTouchCount");
            QaState.increment(getContext(), "touch_" + partId);
            QaState.putString(getContext(), "lastOverlayTouch", partId + "@" + Math.round(event.getRawX()) + "," + Math.round(event.getRawY()));
            QaState.appendEvent(getContext(), "overlay_touch part=" + partId + " x=" + Math.round(event.getRawX()) + " y=" + Math.round(event.getRawY()));
            performClick();
        }
        return true;
    }

    @Override
    public boolean performClick() {
        super.performClick();
        return true;
    }

    private int colorFor(String id) {
        switch (id) {
            case "ALL": return Color.rgb(65, 105, 140);
            case "CORE": return Color.rgb(65, 105, 140);
            case "FORE": return Color.rgb(73, 120, 153);
            case "HIND": return Color.rgb(55, 93, 126);
            case "TAIL": return Color.rgb(85, 132, 164);
            default: return Color.DKGRAY;
        }
    }

    private float dp(float value) {
        return value * getResources().getDisplayMetrics().density;
    }
}
