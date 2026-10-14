package com.example.overlayprobe;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

public final class ProbeCommandReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        String mode = intent == null ? null : intent.getStringExtra("mode");
        OverlayService service = OverlayService.getInstance();
        if (service == null) {
            Log.e("OverlayProbe", "COMMAND_REJECTED service_not_running mode=" + mode);
            return;
        }
        Log.i("OverlayProbe", "COMMAND mode=" + mode);
        service.handleCommand(mode);
    }
}
