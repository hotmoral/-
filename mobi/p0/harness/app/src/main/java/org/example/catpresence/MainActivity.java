package org.example.catpresence;

import android.Manifest;
import android.app.Activity;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Typeface;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.view.Gravity;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import android.widget.Toast;

public final class MainActivity extends Activity {
    private TextView statusView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        QaState.appendEvent(this, "activity_create");
        buildUi();
    }

    private void buildUi() {
        int pad = dp(16);
        ScrollView scroll = new ScrollView(this);
        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setPadding(pad, pad, pad, pad);
        scroll.addView(root, new ScrollView.LayoutParams(
                ScrollView.LayoutParams.MATCH_PARENT,
                ScrollView.LayoutParams.WRAP_CONTENT
        ));

        TextView title = new TextView(this);
        title.setText("Cat Presence P0 — technical prototype");
        title.setTextSize(22f);
        title.setTypeface(Typeface.DEFAULT, Typeface.BOLD);
        root.addView(title);

        TextView note = new TextView(this);
        note.setText("This build validates bounded overlay presence, touch footprint, A↔B movement, keyboard coexistence, owner control, and lifecycle evidence. It is not final art or behavior AI.");
        note.setTextSize(15f);
        note.setPadding(0, dp(8), 0, dp(12));
        root.addView(note);

        addButton(root, "1. Grant / inspect overlay permission", v -> openOverlaySettings());
        addButton(root, "2. Start Presence", v -> startPresence());
        addButton(root, "Stop Presence", v -> sendCommand(PresenceService.ACTION_STOP));
        addButton(root, "Move A → B", v -> sendIfActive(PresenceService.ACTION_MOVE_A_TO_B));
        addButton(root, "Move B → A", v -> sendIfActive(PresenceService.ACTION_MOVE_B_TO_A));
        addButton(root, "Reset Position", v -> sendIfActive(PresenceService.ACTION_RESET));
        addButton(root, "Refresh QA State", v -> refreshStatus());
        addButton(root, "Copy QA Report", v -> copyReport());

        TextView guide = new TextView(this);
        guide.setText("Real-device check: Start Presence → leave this app → use another app normally → tap/drag the cat → open Samsung Keyboard and type → rotate once → screen off/on → return here → Copy QA Report → Stop Presence.");
        guide.setTextSize(14f);
        guide.setPadding(0, dp(12), 0, dp(12));
        root.addView(guide);

        statusView = new TextView(this);
        statusView.setTypeface(Typeface.MONOSPACE);
        statusView.setTextSize(12f);
        statusView.setTextIsSelectable(true);
        statusView.setGravity(Gravity.START);
        root.addView(statusView);

        setContentView(scroll);
        refreshStatus();
    }

    private void addButton(LinearLayout root, String label, View.OnClickListener listener) {
        Button button = new Button(this);
        button.setText(label);
        button.setAllCaps(false);
        button.setOnClickListener(listener);
        LinearLayout.LayoutParams lp = new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT
        );
        lp.bottomMargin = dp(6);
        root.addView(button, lp);
    }

    private void openOverlaySettings() {
        Intent intent = new Intent(
                Settings.ACTION_MANAGE_OVERLAY_PERMISSION,
                Uri.parse("package:" + getPackageName())
        );
        startActivity(intent);
    }

    private void startPresence() {
        if (!Settings.canDrawOverlays(this)) {
            Toast.makeText(this, "Grant 'Display over other apps' first.", Toast.LENGTH_LONG).show();
            openOverlaySettings();
            return;
        }
        requestNotificationPermissionIfNeeded();
        Intent intent = new Intent(this, PresenceService.class).setAction(PresenceService.ACTION_START);
        startForegroundService(intent);
        Toast.makeText(this, "Presence start requested.", Toast.LENGTH_SHORT).show();
        statusView.postDelayed(this::refreshStatus, 500L);
    }

    private void sendIfActive(String action) {
        if (!QaState.getBoolean(this, "serviceActive", false)) {
            Toast.makeText(this, "Start Presence first.", Toast.LENGTH_SHORT).show();
            return;
        }
        sendCommand(action);
    }

    private void sendCommand(String action) {
        Intent intent = new Intent(this, PresenceService.class).setAction(action);
        startService(intent);
        statusView.postDelayed(this::refreshStatus, 300L);
    }

    private void requestNotificationPermissionIfNeeded() {
        if (Build.VERSION.SDK_INT >= 33
                && checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) != PackageManager.PERMISSION_GRANTED) {
            requestPermissions(new String[]{Manifest.permission.POST_NOTIFICATIONS}, 200);
        }
    }

    private void copyReport() {
        String report = QaState.buildReport(this);
        ClipboardManager clipboard = getSystemService(ClipboardManager.class);
        clipboard.setPrimaryClip(ClipData.newPlainText("P0 QA Report", report));
        Toast.makeText(this, "QA report copied.", Toast.LENGTH_SHORT).show();
        refreshStatus();
    }

    private void refreshStatus() {
        if (statusView != null) {
            statusView.setText(QaState.buildReport(this));
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        QaState.appendEvent(this, "activity_resume");
        refreshStatus();
    }

    @Override
    protected void onPause() {
        QaState.appendEvent(this, "activity_pause");
        super.onPause();
    }

    private int dp(int dp) {
        return Math.round(dp * getResources().getDisplayMetrics().density);
    }
}
