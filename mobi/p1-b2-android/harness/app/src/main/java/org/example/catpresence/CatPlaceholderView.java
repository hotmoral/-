package org.example.catpresence;

import android.content.Context;
import android.graphics.Canvas;
import android.graphics.Color;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.RectF;
import android.view.MotionEvent;
import android.view.View;
import android.view.WindowInsets;

public final class CatPlaceholderView extends View {
    public interface InteractionListener {
        void onPointerDown(float rawX, float rawY);
        void onPointerMove(float rawX, float rawY);
        void onPointerUp(float rawX, float rawY);
        void onPointerCancel();
        void onInsetsChanged();
    }

    private final Paint fillPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint detailPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final Paint tailPaint = new Paint(Paint.ANTI_ALIAS_FLAG);
    private final RectF visualBounds = new RectF();
    private final RectF bodyBounds = new RectF();
    private final RectF touchBounds = new RectF();
    private InteractionListener listener;

    public CatPlaceholderView(Context context) {
        super(context);
        setBackgroundColor(Color.TRANSPARENT);
        fillPaint.setColor(Color.rgb(86, 115, 139));
        fillPaint.setStyle(Paint.Style.FILL);
        detailPaint.setColor(Color.rgb(245, 245, 245));
        detailPaint.setStyle(Paint.Style.FILL);
        tailPaint.setColor(Color.rgb(86, 115, 139));
        tailPaint.setStyle(Paint.Style.STROKE);
        tailPaint.setStrokeCap(Paint.Cap.ROUND);
    }

    public void setInteractionListener(InteractionListener listener) {
        this.listener = listener;
    }

    public RectF getVisualBoundsLocal() {
        return new RectF(visualBounds);
    }

    public RectF getBodyBoundsLocal() {
        return new RectF(bodyBounds);
    }

    public RectF getTouchBoundsLocal() {
        return new RectF(touchBounds);
    }

    @Override
    protected void onSizeChanged(int w, int h, int oldw, int oldh) {
        super.onSizeChanged(w, h, oldw, oldh);
        visualBounds.set(w * 0.06f, h * 0.03f, w * 0.96f, h * 0.89f);
        bodyBounds.set(w * 0.14f, h * 0.12f, w * 0.84f, h * 0.83f);
        touchBounds.set(0f, 0f, w, h);
        tailPaint.setStrokeWidth(Math.max(4f, w * 0.075f));
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        float w = getWidth();
        float h = getHeight();
        if (w <= 0 || h <= 0) return;

        RectF body = new RectF(w * 0.23f, h * 0.43f, w * 0.82f, h * 0.82f);
        canvas.drawOval(body, fillPaint);

        float headCx = w * 0.36f;
        float headCy = h * 0.34f;
        float headR = w * 0.22f;
        canvas.drawCircle(headCx, headCy, headR, fillPaint);

        Path leftEar = new Path();
        leftEar.moveTo(w * 0.19f, h * 0.22f);
        leftEar.lineTo(w * 0.23f, h * 0.04f);
        leftEar.lineTo(w * 0.36f, h * 0.19f);
        leftEar.close();
        canvas.drawPath(leftEar, fillPaint);

        Path rightEar = new Path();
        rightEar.moveTo(w * 0.38f, h * 0.18f);
        rightEar.lineTo(w * 0.50f, h * 0.05f);
        rightEar.lineTo(w * 0.54f, h * 0.23f);
        rightEar.close();
        canvas.drawPath(rightEar, fillPaint);

        Path tail = new Path();
        tail.moveTo(w * 0.78f, h * 0.61f);
        tail.cubicTo(w * 0.98f, h * 0.55f, w * 0.98f, h * 0.30f, w * 0.86f, h * 0.25f);
        canvas.drawPath(tail, tailPaint);

        float eyeR = Math.max(2f, w * 0.025f);
        canvas.drawCircle(w * 0.30f, h * 0.32f, eyeR, detailPaint);
        canvas.drawCircle(w * 0.42f, h * 0.32f, eyeR, detailPaint);

        Path nose = new Path();
        nose.moveTo(w * 0.36f, h * 0.38f);
        nose.lineTo(w * 0.33f, h * 0.41f);
        nose.lineTo(w * 0.39f, h * 0.41f);
        nose.close();
        canvas.drawPath(nose, detailPaint);
    }

    @Override
    public boolean onTouchEvent(MotionEvent event) {
        if (listener == null) return true;
        switch (event.getActionMasked()) {
            case MotionEvent.ACTION_DOWN:
                listener.onPointerDown(event.getRawX(), event.getRawY());
                return true;
            case MotionEvent.ACTION_MOVE:
                listener.onPointerMove(event.getRawX(), event.getRawY());
                return true;
            case MotionEvent.ACTION_UP:
                listener.onPointerUp(event.getRawX(), event.getRawY());
                performClick();
                return true;
            case MotionEvent.ACTION_CANCEL:
                listener.onPointerCancel();
                return true;
            default:
                return true;
        }
    }

    @Override
    public boolean performClick() {
        super.performClick();
        return true;
    }

    @Override
    public WindowInsets onApplyWindowInsets(WindowInsets insets) {
        if (listener != null) {
            post(listener::onInsetsChanged);
        }
        return super.onApplyWindowInsets(insets);
    }
}
