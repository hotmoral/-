package com.receiptledger.v1;

import android.app.Activity;
import android.os.Bundle;
import android.view.Gravity;
import android.view.ViewGroup;
import android.widget.LinearLayout;
import android.widget.TextView;

public final class MainActivity extends Activity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        int padding = Math.round(24 * getResources().getDisplayMetrics().density);

        LinearLayout root = new LinearLayout(this);
        root.setOrientation(LinearLayout.VERTICAL);
        root.setGravity(Gravity.CENTER);
        root.setPadding(padding, padding, padding, padding);
        root.setLayoutParams(new ViewGroup.LayoutParams(
                ViewGroup.LayoutParams.MATCH_PARENT,
                ViewGroup.LayoutParams.MATCH_PARENT));

        TextView title = new TextView(this);
        title.setText(R.string.foundation_title);
        title.setTextSize(26);
        title.setGravity(Gravity.CENTER);

        TextView body = new TextView(this);
        body.setText(getString(R.string.foundation_body, FoundationIdentity.FOUNDATION_ID));
        body.setTextSize(16);
        body.setGravity(Gravity.CENTER);
        body.setPadding(0, padding, 0, 0);

        root.addView(title);
        root.addView(body);
        setContentView(root);
    }
}
