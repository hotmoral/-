package com.example.einsteingame;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.Rect;
import android.graphics.drawable.ColorDrawable;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.InputDevice;
import android.view.MotionEvent;
import android.view.View;
import android.view.ViewGroup;
import java.io.File;
import java.io.FileOutputStream;
import java.io.PrintWriter;

/** Test-only runtime proof for the fixed 360x800 Clumi viewport contract. */
public final class ClumiFixedViewportRuntimeRunner extends Instrumentation {
    private int assertions;
    private String profile;

    @Override public void onCreate(Bundle args) {
        super.onCreate(args);
        profile = args.getString("profile", "unknown");
        start();
    }

    private void check(boolean value, String message) {
        assertions++;
        if (!value) throw new AssertionError(message);
    }

    private void ui(Runnable action) {
        Throwable[] failure = new Throwable[1];
        runOnMainSync(() -> {
            try { action.run(); } catch (Throwable t) { failure[0] = t; }
        });
        if (failure[0] != null) throw new AssertionError("UI action failed", failure[0]);
    }

    private View tagged(MainActivity activity, String tag) {
        View[] found = new View[1];
        ui(() -> found[0] = activity.getWindow().getDecorView().findViewWithTag(tag));
        return found[0];
    }

    private View waitTagged(MainActivity activity, String tag, long timeoutMs) {
        long deadline = SystemClock.uptimeMillis() + timeoutMs;
        View result;
        do {
            result = tagged(activity, tag);
            if (result != null && result.isAttachedToWindow()) return result;
            SystemClock.sleep(50);
        } while (SystemClock.uptimeMillis() < deadline);
        return result;
    }

    private void waitInputReady(MainActivity activity) {
        long deadline = SystemClock.uptimeMillis() + 5000;
        boolean[] ready = {false};
        do {
            ui(() -> ready[0] = !activity.navigationInProgress());
            if (ready[0]) return;
            SystemClock.sleep(50);
        } while (SystemClock.uptimeMillis() < deadline);
        check(false, "Navigation becomes ready for input");
    }

    private File folder() {
        File dir = new File(getTargetContext().getExternalFilesDir(null), "fixed-viewport/" + profile);
        if (!dir.exists() && !dir.mkdirs()) throw new AssertionError("Cannot create evidence folder");
        return dir;
    }

    private Bitmap screenshot(String name) throws Exception {
        Bitmap bitmap = getUiAutomation().takeScreenshot();
        check(bitmap != null, "Native screenshot captured: " + name);
        try (FileOutputStream out = new FileOutputStream(new File(folder(), name + ".png"))) {
            check(bitmap.compress(Bitmap.CompressFormat.PNG, 100, out), "Screenshot written: " + name);
        }
        return bitmap;
    }

    private Geometry verifyViewport(MainActivity activity, String phase, Bitmap screenshot) {
        Geometry g = new Geometry();
        ui(() -> {
            ViewGroup content = activity.findViewById(android.R.id.content);
            check(content != null && content.getChildCount() == 1, phase + ": one content root");
            View candidate = content.getChildAt(0);
            check(candidate instanceof ClumiFixedViewport, phase + ": content root is ClumiFixedViewport");
            ClumiFixedViewport viewport = (ClumiFixedViewport) candidate;
            check(viewport.getChildCount() == 1, phase + ": viewport has one logical scene");
            check(viewport.getClipChildren() && viewport.getClipToPadding(),
                    phase + ": viewport clips the logical scene to its real bounds");
            View scene = viewport.getChildAt(0);
            int logicalWidth = ClumiUi.dp(activity, ClumiUi.DESIGN_WIDTH_DP);
            int logicalHeight = ClumiUi.dp(activity, ClumiUi.DESIGN_HEIGHT_DP);
            check(ClumiUi.DESIGN_WIDTH_DP == 360 && ClumiUi.DESIGN_HEIGHT_DP == 800,
                    phase + ": logical design contract is 360x800dp");
            check(scene.getWidth() == logicalWidth && scene.getHeight() == logicalHeight,
                    phase + ": scene remains exact logical size");
            check(Math.abs(scene.getPivotX()) < 0.001f && Math.abs(scene.getPivotY()) < 0.001f,
                    phase + ": transform pivot is top-left");
            float expected = Math.min(viewport.getWidth() / (float) logicalWidth,
                    viewport.getHeight() / (float) logicalHeight);
            check(Math.abs(scene.getScaleX() - scene.getScaleY()) < 0.0001f,
                    phase + ": X/Y scale is uniform");
            check(Math.abs(scene.getScaleX() - expected) < 0.001f,
                    phase + ": scale equals min(real/logical)");
            float expectedX = (viewport.getWidth() - logicalWidth * expected) * 0.5f;
            float expectedY = (viewport.getHeight() - logicalHeight * expected) * 0.5f;
            check(Math.abs(scene.getTranslationX() - expectedX) <= 1.0f,
                    phase + ": scene horizontally centered");
            check(Math.abs(scene.getTranslationY() - expectedY) <= 1.0f,
                    phase + ": scene vertically centered");
            check(viewport.getBackground() instanceof ColorDrawable
                            && ((ColorDrawable) viewport.getBackground()).getColor() == Color.BLACK,
                    phase + ": exposed letterbox/pillarbox background is black");
            int[] screen = new int[2];
            viewport.getLocationOnScreen(screen);
            g.viewportX = screen[0];
            g.viewportY = screen[1];
            g.viewportWidth = viewport.getWidth();
            g.viewportHeight = viewport.getHeight();
            g.logicalWidth = logicalWidth;
            g.logicalHeight = logicalHeight;
            g.scale = scene.getScaleX();
            g.translationX = scene.getTranslationX();
            g.translationY = scene.getTranslationY();
        });

        if ("home".equals(phase)) {
            if ("360x640".equals(profile)) {
                check(g.translationX > 1f, "short profile exposes black horizontal pillarbox area");
            } else if ("360x800".equals(profile)) {
                check(g.scale > 0.90f && g.scale <= 1.001f,
                        "native profile stays near 1x inside the actual Android content viewport");
            } else if ("360x900".equals(profile)) {
                check(g.translationY > 1f, "tall profile exposes black vertical letterbox area");
            } else {
                check(false, "Known runtime profile");
            }
        }
        return g;
    }

    private void physicalTap(View target) {
        Rect rect = new Rect();
        ui(() -> check(target.getGlobalVisibleRect(rect) && rect.width() > 0 && rect.height() > 0,
                "Home CTA has transformed physical bounds"));
        float x = rect.exactCenterX();
        float y = rect.exactCenterY();
        System.out.println("CLUMI_PHYSICAL_TAP x=" + x + " y=" + y + " profile=" + profile);
        long downTime = SystemClock.uptimeMillis();
        MotionEvent down = MotionEvent.obtain(downTime, downTime, MotionEvent.ACTION_DOWN, x, y, 0);
        down.setSource(InputDevice.SOURCE_TOUCHSCREEN);
        check(getUiAutomation().injectInputEvent(down, true), "Physical ACTION_DOWN injected");
        down.recycle();
        long upTime = SystemClock.uptimeMillis();
        MotionEvent up = MotionEvent.obtain(downTime, upTime, MotionEvent.ACTION_UP, x, y, 0);
        up.setSource(InputDevice.SOURCE_TOUCHSCREEN);
        check(getUiAutomation().injectInputEvent(up, true), "Physical ACTION_UP injected");
        up.recycle();
    }

    private void writeSummary(Geometry home, Geometry start) throws Exception {
        try (PrintWriter out = new PrintWriter(new File(folder(), "summary.txt"))) {
            out.println("status=PASS");
            out.println("profile=" + profile);
            out.println("assertions=" + assertions);
            out.println("logical_dp=360x800");
            out.println("home_viewport_px=" + home.viewportWidth + "x" + home.viewportHeight);
            out.println("home_logical_px=" + home.logicalWidth + "x" + home.logicalHeight);
            out.println("home_scale=" + home.scale);
            out.println("home_translation_px=" + home.translationX + "," + home.translationY);
            out.println("start_scale=" + start.scale);
            out.println("start_translation_px=" + start.translationX + "," + start.translationY);
            out.println("touch=PASS");
            out.println("black_bars=PASS_BY_VIEW_CONTRACT_AND_SCREENSHOT_EVIDENCE");
        }
    }

    @Override public void onStart() {
        Bundle result = new Bundle();
        try {
            getUiAutomation();
            getTargetContext().getSharedPreferences("clumi_progress_v1", 0).edit().clear().commit();
            Intent intent = new Intent(getTargetContext(), MainActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            MainActivity activity = (MainActivity) startActivitySync(intent);
            check(activity != null, "MainActivity launched");
            waitInputReady(activity);
            View cta = waitTagged(activity, "home-continue", 5000);
            check(cta != null && cta.isShown() && cta.isEnabled(), "Home CTA ready");
            Bitmap homeShot = screenshot("01_home");
            Geometry home = verifyViewport(activity, "home", homeShot);
            homeShot.recycle();

            physicalTap(cta);
            View panel = waitTagged(activity, "start-panel", 5000);
            check(panel != null && panel.isShown(), "Transformed physical touch opens Stage Start");
            waitInputReady(activity);
            Bitmap startShot = screenshot("02_stage_start");
            Geometry start = verifyViewport(activity, "start", startShot);
            startShot.recycle();
            check(Math.abs(home.scale - start.scale) < 0.001f,
                    "Screen transition preserves viewport scale");
            check(Math.abs(home.translationX - start.translationX) <= 1f
                            && Math.abs(home.translationY - start.translationY) <= 1f,
                    "Screen transition preserves viewport centering");
            writeSummary(home, start);
            result.putString("stream", "CLUMI_FIXED_VIEWPORT_STATUS=PASS profile=" + profile
                    + " assertions=" + assertions + "\n");
            finish(Activity.RESULT_OK, result);
        } catch (Throwable failure) {
            failure.printStackTrace();
            result.putString("stream", "CLUMI_FIXED_VIEWPORT_STATUS=FAIL profile=" + profile
                    + " error=" + failure + "\n");
            finish(Activity.RESULT_CANCELED, result);
        }
    }

    private static final class Geometry {
        int viewportX, viewportY, viewportWidth, viewportHeight, logicalWidth, logicalHeight;
        float scale, translationX, translationY;
    }
}
