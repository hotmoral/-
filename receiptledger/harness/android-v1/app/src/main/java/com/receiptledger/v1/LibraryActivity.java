package com.receiptledger.v1;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.Gravity;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.ScrollView;
import android.widget.TextView;
import com.receiptledger.v1.archive.ReceiptRepository;
import com.receiptledger.v1.design.DesignTokensV1;
import com.receiptledger.v1.design.ResponsiveLayoutPolicyV1;
import com.receiptledger.v1.design.UiKitV1;
import com.receiptledger.v1.persistence.ReceiptRecord;
import com.receiptledger.v1.ui.ReceiptDisplayFormatter;
import com.receiptledger.v1.ui.SystemBarInsetHelper;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/** CP34 receipt-history destination. Product discovery lives in SearchBrowseActivity. */
public final class LibraryActivity extends Activity {
    private final ExecutorService worker = Executors.newSingleThreadExecutor();
    private ReceiptRepository repository;
    private LinearLayout list;
    private TextView status;
    private long generation;

    @Override protected void onCreate(Bundle state) {
        super.onCreate(state);
        repository = new ReceiptRepository(getApplicationContext());

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.TOP | Gravity.CENTER_HORIZONTAL);
        UiKitV1.applyPage(this, root);

        ScrollView scroll = new ScrollView(this);
        scroll.setFillViewport(true);
        root.addView(scroll, new LinearLayout.LayoutParams(-1, 0, 1f));

        LinearLayout content = new LinearLayout(this);
        content.setOrientation(LinearLayout.VERTICAL);
        scroll.addView(content, new ScrollView.LayoutParams(
                contentWidthPx(), ScrollView.LayoutParams.WRAP_CONTENT,
                Gravity.TOP | Gravity.CENTER_HORIZONTAL));

        content.addView(UiKitV1.title(this, R.string.library_title));
        content.addView(UiKitV1.body(this, getString(R.string.library_intro)));

        Button add = UiKitV1.button(this, R.string.library_add_receipt,
                v -> startActivity(new Intent(this, MainActivity.class)), UiKitV1.ButtonTone.PRIMARY);
        content.addView(add, blockParams(DesignTokensV1.SPACE_3_DP));
        Button find = UiKitV1.button(this, R.string.library_find,
                v -> startActivity(new Intent(this, SearchBrowseActivity.class)), UiKitV1.ButtonTone.SECONDARY);
        content.addView(find, blockParams(DesignTokensV1.SPACE_2_DP));
        Button close = UiKitV1.button(this, R.string.close_library, v -> finish(), UiKitV1.ButtonTone.SECONDARY);
        content.addView(close, blockParams(DesignTokensV1.SPACE_2_DP));

        status = UiKitV1.status(this);
        content.addView(status, blockParams(DesignTokensV1.SPACE_2_DP));

        list = new LinearLayout(this);
        list.setOrientation(LinearLayout.VERTICAL);
        content.addView(list, blockParams(DesignTokensV1.SPACE_1_DP));

        setContentView(root);
        SystemBarInsetHelper.apply(this, root);
    }

    @Override protected void onResume() {
        super.onResume();
        reload();
    }

    private void reload() {
        long ticket = ++generation;
        status.setText(R.string.library_loading);
        worker.execute(() -> {
            List<ReceiptRecord> records;
            boolean failed = false;
            try {
                records = repository.listNewestFirst(200);
            } catch (RuntimeException error) {
                records = Collections.emptyList();
                failed = true;
            }
            final List<ReceiptRecord> result = records;
            final boolean loadFailed = failed;
            runOnUiThread(() -> {
                if (ticket != generation) return;
                list.removeAllViews();
                if (loadFailed) {
                    status.setText(R.string.search_browse_failed);
                    return;
                }
                status.setText(getString(R.string.library_count, result.size()));
                if (result.isEmpty()) {
                    list.addView(UiKitV1.body(this, getString(R.string.library_empty)));
                    return;
                }
                for (ReceiptRecord record : result) {
                    Button row = UiKitV1.listRow(this, ReceiptDisplayFormatter.summary(record), v -> {
                        Intent intent = new Intent(this, ReceiptDetailActivity.class);
                        intent.putExtra(ReceiptDetailActivity.EXTRA_ID, record.id);
                        startActivity(intent);
                    });
                    list.addView(row, blockParams(DesignTokensV1.SPACE_1_DP));
                }
            });
        });
    }

    private LinearLayout.LayoutParams blockParams(int topDp) {
        LinearLayout.LayoutParams params = new LinearLayout.LayoutParams(-1, -2);
        if (topDp > 0) params.topMargin = UiKitV1.dp(this, topDp);
        return params;
    }

    private int contentWidthPx() {
        int widthDp = getResources().getConfiguration().screenWidthDp;
        if (widthDp < 1) {
            widthDp = Math.max(1, Math.round(
                    getResources().getDisplayMetrics().widthPixels
                            / getResources().getDisplayMetrics().density));
        }
        int gutter = ResponsiveLayoutPolicyV1.pageGutterDp(widthDp);
        int available = Math.max(UiKitV1.dp(this, 240),
                getResources().getDisplayMetrics().widthPixels - UiKitV1.dp(this, gutter * 2));
        return Math.min(available, UiKitV1.dp(this, ResponsiveLayoutPolicyV1.contentMaxWidthDp()));
    }

    @Override protected void onDestroy() {
        generation++;
        worker.shutdownNow();
        repository.close();
        super.onDestroy();
    }
}
