package com.example.einsteingame;

import android.app.Activity;
import android.app.Instrumentation;
import android.content.Intent;
import android.os.Bundle;
import android.os.SystemClock;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

/** Test-only diagnostic for Back -> Home response latency. */
public final class ClumiBackHomeLatencyRunner extends Instrumentation {
    private final List<Sample> samples = new ArrayList<>();

    @Override public void onCreate(Bundle args) { super.onCreate(args); start(); }

    private void ui(Runnable action) {
        Throwable[] failure = new Throwable[1];
        runOnMainSync(() -> { try { action.run(); } catch (Throwable t) { failure[0] = t; } });
        if (failure[0] != null) throw new AssertionError("UI action failed", failure[0]);
    }

    private ClumiNavigationController navigation(MainActivity activity) throws Exception {
        Field field = MainActivity.class.getDeclaredField("navigation");
        field.setAccessible(true);
        return (ClumiNavigationController) field.get(activity);
    }

    private void invoke(MainActivity activity, String method, Class<?>[] types, Object... args) throws Exception {
        Method target = MainActivity.class.getDeclaredMethod(method, types);
        target.setAccessible(true);
        Throwable[] failure = new Throwable[1];
        runOnMainSync(() -> { try { target.invoke(activity, args); } catch (Throwable t) { failure[0] = t; } });
        if (failure[0] != null) throw new AssertionError("Invocation failed: " + method, failure[0]);
    }

    private void waitNavigationIdle(MainActivity activity, long timeoutMs) throws Exception {
        ClumiNavigationController nav = navigation(activity);
        long deadline = SystemClock.elapsedRealtime() + timeoutMs;
        while (SystemClock.elapsedRealtime() < deadline) {
            boolean[] active = new boolean[1];
            ui(() -> active[0] = nav.active());
            if (!active[0]) return;
            SystemClock.sleep(5);
        }
        throw new AssertionError("Navigation did not become idle");
    }

    private boolean hasHome(MainActivity activity) {
        boolean[] result = new boolean[1];
        ui(() -> result[0] = activity.getWindow().getDecorView().findViewWithTag("home-continue") != null);
        return result[0];
    }

    private Sample backHome(MainActivity activity, String origin) throws Exception {
        ClumiNavigationController nav = navigation(activity);
        waitNavigationIdle(activity, 7000);
        int capturesBefore = nav.readyCaptures;
        int fallbacksBefore = nav.readyFallbacks;
        int retriesBefore = nav.captureRetries;

        final long[] handler = new long[1];
        final boolean[] homeCommittedAtReturn = new boolean[1];
        long t0 = SystemClock.elapsedRealtime();
        ui(() -> {
            long call = SystemClock.elapsedRealtime();
            activity.onBackPressed();
            handler[0] = SystemClock.elapsedRealtime() - call;
            homeCommittedAtReturn[0] = activity.getWindow().getDecorView().findViewWithTag("home-continue") != null;
        });

        long prepareDone = -1;
        long deadline = t0 + 7000;
        while (SystemClock.elapsedRealtime() < deadline) {
            boolean[] preparing = new boolean[1];
            boolean[] active = new boolean[1];
            ui(() -> { preparing[0] = nav.preparing(); active[0] = nav.active(); });
            if (!preparing[0]) { prepareDone = SystemClock.elapsedRealtime() - t0; break; }
            SystemClock.sleep(2);
        }
        waitNavigationIdle(activity, 7000);
        long total = SystemClock.elapsedRealtime() - t0;
        if (!hasHome(activity)) throw new AssertionError(origin + ": Home not committed");

        Sample s = new Sample();
        s.origin = origin;
        s.handlerMs = handler[0];
        s.homeCommittedAtReturn = homeCommittedAtReturn[0];
        s.readyCaptures = nav.readyCaptures - capturesBefore;
        s.readyFallbacks = nav.readyFallbacks - fallbacksBefore;
        s.captureRetries = nav.captureRetries - retriesBefore;
        s.readyLatencyMs = s.readyCaptures > 0 ? nav.lastReadyLatency : -1;
        s.transitionStartMs = prepareDone;
        s.totalMs = total;
        s.readyEvaluations = s.readyCaptures > 0 ? nav.lastReadyEvaluations : -1;
        samples.add(s);
        return s;
    }

    private void open(MainActivity activity, String method, Class<?>[] types, Object... args) throws Exception {
        invoke(activity, method, types, args);
        waitNavigationIdle(activity, 7000);
    }

    @Override public void onStart() {
        Bundle result = new Bundle();
        try {
            getUiAutomation();
            getTargetContext().getSharedPreferences("clumi_progress_v1", 0).edit().clear().commit();
            Intent intent = new Intent(getTargetContext(), MainActivity.class);
            intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            MainActivity activity = (MainActivity) startActivitySync(intent);
            if (activity == null) throw new AssertionError("MainActivity launch failed");
            waitNavigationIdle(activity, 7000);

            open(activity, "showStages", new Class<?>[0]); backHome(activity, "stages");
            open(activity, "showRewards", new Class<?>[0]); backHome(activity, "rewards");
            open(activity, "showSettings", new Class<?>[0]); backHome(activity, "settings");
            open(activity, "showStart", new Class<?>[]{int.class}, 1); backHome(activity, "start");

            long worstHandler = 0, worstReady = 0, worstTotal = 0;
            int fallback = 0, retries = 0, captures = 0;
            boolean committed = true;
            StringBuilder stream = new StringBuilder();
            for (Sample s : samples) {
                stream.append("CLUMI_BACK_HOME_SAMPLE ").append(s.line()).append('\n');
                worstHandler = Math.max(worstHandler, s.handlerMs);
                if (s.readyLatencyMs >= 0) worstReady = Math.max(worstReady, s.readyLatencyMs);
                worstTotal = Math.max(worstTotal, s.totalMs);
                fallback += s.readyFallbacks;
                retries += s.captureRetries;
                captures += s.readyCaptures;
                committed &= s.homeCommittedAtReturn;
            }
            String summary = "CLUMI_BACK_HOME_STATUS=PASS samples=" + samples.size()
                    + " worst_handler_ms=" + worstHandler
                    + " worst_ready_ms=" + worstReady
                    + " worst_total_ms=" + worstTotal
                    + " home_committed_at_handler_return=" + committed
                    + " ready_captures=" + captures
                    + " ready_fallbacks=" + fallback
                    + " capture_retries=" + retries;
            stream.append(summary).append('\n');
            result.putString("stream", stream.toString());
            finish(Activity.RESULT_OK, result);
        } catch (Throwable failure) {
            failure.printStackTrace();
            result.putString("stream", "CLUMI_BACK_HOME_STATUS=FAIL error=" + failure + "\n");
            finish(Activity.RESULT_CANCELED, result);
        }
    }

    private static final class Sample {
        String origin;
        long handlerMs, readyLatencyMs, transitionStartMs, totalMs;
        int readyEvaluations, readyCaptures, readyFallbacks, captureRetries;
        boolean homeCommittedAtReturn;
        String line() {
            return "origin=" + origin
                    + " handler_ms=" + handlerMs
                    + " committed_at_return=" + homeCommittedAtReturn
                    + " ready_ms=" + readyLatencyMs
                    + " transition_start_ms=" + transitionStartMs
                    + " total_ms=" + totalMs
                    + " ready_evaluations=" + readyEvaluations
                    + " captures=" + readyCaptures
                    + " fallbacks=" + readyFallbacks
                    + " retries=" + captureRetries;
        }
    }
}
