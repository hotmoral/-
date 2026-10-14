package org.example.mobifootprint;

import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.provider.Settings;
import android.view.Gravity;
import android.view.MotionEvent;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;

import java.util.Map;

public final class MainActivity extends Activity {
    public static final String EXTRA_QA_COMMAND = "p1_b22_qa_command";
    private TextView report;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        if (!getSharedPreferences(QaState.PREF, MODE_PRIVATE).contains("prototype")) {
            QaState.reset(this);
        }
        buildUi();
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
        refreshReport();
    }

    private void buildUi() {
        LinearLayout column = new LinearLayout(this);
        column.setOrientation(LinearLayout.VERTICAL);
        column.setPadding(28, 28, 28, 60);
        column.setBackgroundColor(Color.rgb(245, 245, 245));
        column.setOnTouchListener((v, event) -> {
            if (event.getActionMasked() == MotionEvent.ACTION_DOWN) {
                QaState.recordHostHit(this, event.getRawX(), event.getRawY());
                refreshReport();
            }
            return false;
        });

        TextView title = new TextView(this);
        title.setText("Mobi P1-B2.2 Multi-Window Footprint\nLow-fidelity technical comparator");
        title.setTextSize(22f);
        title.setTextColor(Color.BLACK);
        title.setPadding(0, 0, 0, 20);
        column.addView(title);

        addButton(column, "Grant / inspect overlay permission", v -> {
            Intent i = new Intent(Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                    Uri.parse("package:" + getPackageName()));
            startActivity(i);
        });
        addButton(column, "F0 — 1 Window control", v -> send(MultiWindowService.ACTION_F0));
        addButton(column, "F1 — CORE + TAIL", v -> send(MultiWindowService.ACTION_F1));
        addButton(column, "F2 — CORE + FORE + HIND + TAIL", v -> send(MultiWindowService.ACTION_F2));
        addButton(column, "Move group A → B", v -> send(MultiWindowService.ACTION_MOVE_B));
        addButton(column, "Move group B → A", v -> send(MultiWindowService.ACTION_MOVE_A));
        addButton(column, "Reset QA counters", v -> {
            QaState.reset(this);
            refreshReport();
        });
        addButton(column, "Stop / remove all overlay parts", v -> send(MultiWindowService.ACTION_STOP));
        addButton(column, "Refresh QA report", v -> refreshReport());
        addButton(column, "Copy QA report", v -> {
            refreshReport();
            ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            clipboard.setPrimaryClip(ClipData.newPlainText("P1-B2.2 QA", report.getText()));
        });

        TextView probe = new TextView(this);
        probe.setText("HOST PASS-THROUGH PROBE AREA\nTap blank space here. If no overlay child covers the point, HOST must receive it.");
        probe.setTextSize(18f);
        probe.setGravity(Gravity.CENTER);
        probe.setTextColor(Color.DKGRAY);
        probe.setBackgroundColor(Color.rgb(226, 238, 246));
        probe.setMinHeight(520);
        column.addView(probe, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT, 520));

        report = new TextView(this);
        report.setTextSize(13f);
        report.setTextColor(Color.BLACK);
        report.setPadding(0, 22, 0, 20);
        column.addView(report);

        ScrollView scroll = new ScrollView(this);
        scroll.addView(column);
        setContentView(scroll);
    }

    private void addButton(LinearLayout parent, String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setOnClickListener(listener);
        parent.addView(button, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));
    }

    private void send(String action) {
        Intent intent = new Intent(this, MultiWindowService.class).setAction(action);
        startForegroundService(intent);
        refreshReport();
    }

    private void handleIntent(Intent intent) {
        if (intent == null) return;
        String command = intent.getStringExtra(EXTRA_QA_COMMAND);
        if (command == null) return;
        switch (command) {
            case "reset": QaState.reset(this); break;
            case "f0": send(MultiWindowService.ACTION_F0); break;
            case "f1": send(MultiWindowService.ACTION_F1); break;
            case "f2": send(MultiWindowService.ACTION_F2); break;
            case "move_b": send(MultiWindowService.ACTION_MOVE_B); break;
            case "move_a": send(MultiWindowService.ACTION_MOVE_A); break;
            case "stop": send(MultiWindowService.ACTION_STOP); break;
            case "refresh": refreshReport(); break;
            default: throw new IllegalArgumentException("unknown qa command=" + command);
        }
    }

    private void refreshReport() {
        if (report == null) return;
        Map<String, ?> all = getSharedPreferences(QaState.PREF, MODE_PRIVATE).getAll();
        StringBuilder b = new StringBuilder("P1-B2.2 QA Report\n");
        b.append("package=").append(getPackageName()).append('\n');
        b.append("overlayPermission=").append(Settings.canDrawOverlays(this)).append('\n');
        all.keySet().stream().sorted().forEach(key -> b.append(key).append('=').append(all.get(key)).append('\n'));
        report.setText(b.toString());
    }
}
