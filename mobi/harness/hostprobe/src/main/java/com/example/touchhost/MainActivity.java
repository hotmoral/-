package com.example.touchhost;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Color;
import android.graphics.Insets;
import android.os.Build;
import android.os.Bundle;
import android.os.SystemClock;
import android.view.Display;
import android.view.Gravity;
import android.view.WindowInsets;
import android.view.WindowInsetsController;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;

import java.io.FileOutputStream;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private static final String ACTION_COMMAND = "com.example.touchhost.COMMAND";

    private LinearLayout root;
    private EditText editor;
    private TextView status;
    private BroadcastReceiver commandReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER_HORIZONTAL);
        root.setPadding(48, 96, 48, 48);
        root.setBackgroundColor(Color.rgb(245, 247, 250));
        root.setFocusableInTouchMode(true);

        TextView title = new TextView(this);
        title.setText("Synthetic IME Host");
        title.setTextSize(26f);
        title.setTextColor(Color.rgb(35, 40, 50));
        root.addView(title, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        TextView explanation = new TextView(this);
        explanation.setText("Test-only editor. No real user content is used.");
        explanation.setTextSize(16f);
        explanation.setTextColor(Color.rgb(70, 75, 85));
        root.addView(explanation, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        editor = new EditText(this);
        editor.setHint("Synthetic editor for keyboard visibility testing");
        editor.setText("fixture");
        editor.setSelection(editor.length());
        editor.setTextSize(20f);
        editor.setSingleLine(false);
        editor.setMinLines(4);
        root.addView(editor, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        status = new TextView(this);
        status.setTextSize(16f);
        status.setTextColor(Color.rgb(45, 50, 60));
        root.addView(status, new LinearLayout.LayoutParams(
                LinearLayout.LayoutParams.MATCH_PARENT,
                LinearLayout.LayoutParams.WRAP_CONTENT));

        setContentView(root);
        root.requestFocus();

        getWindow().getDecorView().setOnApplyWindowInsetsListener((v, insets) -> {
            writeInsetsSnapshot("apply", insets);
            return insets;
        });

        commandReceiver = new BroadcastReceiver() {
            @Override
            public void onReceive(Context context, Intent intent) {
                String mode = intent == null ? null : intent.getStringExtra("mode");
                handleCommand(mode);
            }
        };
        IntentFilter filter = new IntentFilter(ACTION_COMMAND);
        if (Build.VERSION.SDK_INT >= 33) {
            registerReceiver(commandReceiver, filter, Context.RECEIVER_EXPORTED);
        } else {
            registerReceiver(commandReceiver, filter);
        }

        root.post(() -> writeCurrentSnapshot("created"));
    }

    @Override
    protected void onDestroy() {
        if (commandReceiver != null) {
            unregisterReceiver(commandReceiver);
            commandReceiver = null;
        }
        super.onDestroy();
    }

    private void handleCommand(String mode) {
        if ("show".equals(mode)) {
            editor.requestFocus();
            editor.postDelayed(() -> {
                WindowInsetsController controller = editor.getWindowInsetsController();
                if (controller != null) {
                    controller.show(WindowInsets.Type.ime());
                }
                writeCurrentSnapshot("show_requested");
            }, 250L);
        } else if ("hide".equals(mode)) {
            WindowInsetsController controller = getWindow().getDecorView().getWindowInsetsController();
            if (controller != null) {
                controller.hide(WindowInsets.Type.ime());
            }
            editor.clearFocus();
            root.requestFocus();
            root.postDelayed(() -> writeCurrentSnapshot("hide_requested"), 250L);
        } else if ("reset".equals(mode)) {
            editor.setText("fixture");
            editor.setSelection(editor.length());
            writeCurrentSnapshot("reset");
        } else {
            writeCurrentSnapshot("capture");
        }
    }

    private void writeCurrentSnapshot(String reason) {
        WindowInsets insets = getWindow().getDecorView().getRootWindowInsets();
        writeInsetsSnapshot(reason, insets);
    }

    private void writeInsetsSnapshot(String reason, WindowInsets insets) {
        boolean imeVisible = false;
        Insets ime = Insets.NONE;
        Insets statusBars = Insets.NONE;
        Insets navigationBars = Insets.NONE;
        Insets gestures = Insets.NONE;
        String insetState = "UNKNOWN";

        if (insets != null) {
            imeVisible = insets.isVisible(WindowInsets.Type.ime());
            ime = insets.getInsets(WindowInsets.Type.ime());
            statusBars = insets.getInsets(WindowInsets.Type.statusBars());
            navigationBars = insets.getInsets(WindowInsets.Type.navigationBars());
            gestures = insets.getInsets(WindowInsets.Type.systemGestures());
            insetState = "OBSERVED";
        }

        Display display = getDisplay();
        int rotation = display == null ? -1 : display.getRotation();
        int displayState = display == null ? Display.STATE_UNKNOWN : display.getState();
        boolean hasWindowFocus = getWindow().getDecorView().hasWindowFocus();
        boolean editorFocus = editor.hasFocus();
        String editorText = editor.getText() == null ? "" : editor.getText().toString();

        String snapshot =
                "reason=" + reason + "\n"
                        + "elapsedRealtimeMs=" + SystemClock.elapsedRealtime() + "\n"
                        + "insetState=" + insetState + "\n"
                        + "imeVisible=" + imeVisible + "\n"
                        + "imeInsets=" + formatInsets(ime) + "\n"
                        + "statusBars=" + formatInsets(statusBars) + "\n"
                        + "navigationBars=" + formatInsets(navigationBars) + "\n"
                        + "systemGestures=" + formatInsets(gestures) + "\n"
                        + "windowFocus=" + hasWindowFocus + "\n"
                        + "editorFocus=" + editorFocus + "\n"
                        + "editorText=" + editorText + "\n"
                        + "editorLength=" + editorText.length() + "\n"
                        + "rotation=" + rotation + "\n"
                        + "displayState=" + displayState + "\n";

        writeText("host_ime_latest.txt", snapshot, false);
        writeText("host_ime_events.txt", "---\n" + snapshot, true);
        status.setText("IME visible=" + imeVisible + "  insets=" + formatInsets(ime));
    }

    private static String formatInsets(Insets insets) {
        return insets.left + "," + insets.top + "," + insets.right + "," + insets.bottom;
    }

    private void writeText(String file, String value, boolean append) {
        try (FileOutputStream out = openFileOutput(file, append ? MODE_APPEND : MODE_PRIVATE)) {
            out.write(value.getBytes(StandardCharsets.UTF_8));
        } catch (Exception ignored) {
        }
    }
}
