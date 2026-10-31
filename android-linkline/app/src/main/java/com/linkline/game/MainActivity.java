package com.linkline.game;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.graphics.Color;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.webkit.WebChromeClient;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.util.Collections;

public final class MainActivity extends Activity {
    private static final String LOCAL_SCHEME = "https";
    private static final String LOCAL_HOST = "linkline.local";
    private static final String START_URL = "https://linkline.local/";

    private WebView webView;
    private boolean pageReady = false;
    private int lastNativeViewportHeightPx = -1;

    @SuppressLint("SetJavaScriptEnabled")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        getWindow().setStatusBarColor(Color.rgb(247, 244, 236));
        getWindow().setNavigationBarColor(Color.rgb(247, 244, 236));
        getWindow().getDecorView().setSystemUiVisibility(
            View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR
        );

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(247, 244, 236));
        WebView.setWebContentsDebuggingEnabled(true);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(false);
        settings.setAllowContentAccess(false);
        settings.setUseWideViewPort(true);
        settings.setLoadWithOverviewMode(false);
        settings.setTextZoom(100);
        settings.setBuiltInZoomControls(false);
        settings.setDisplayZoomControls(false);
        settings.setSupportZoom(false);
        settings.setMixedContentMode(WebSettings.MIXED_CONTENT_NEVER_ALLOW);
        settings.setCacheMode(WebSettings.LOAD_DEFAULT);

        webView.setWebChromeClient(new WebChromeClient());
        webView.setWebViewClient(new LocalAssetClient());
        webView.addOnLayoutChangeListener((v, left, top, right, bottom, oldLeft, oldTop, oldRight, oldBottom) -> {
            if (pageReady && (bottom - top) != (oldBottom - oldTop)) {
                syncNativeViewport();
            }
        });
        setContentView(webView);

        webView.loadUrl(START_URL);
    }

    private void syncNativeViewport() {
        if (webView == null || !pageReady) return;
        webView.post(() -> {
            if (webView == null || !pageReady) return;
            int heightPx = webView.getHeight();
            if (heightPx <= 0 || heightPx == lastNativeViewportHeightPx) return;
            lastNativeViewportHeightPx = heightPx;

            float density = getResources().getDisplayMetrics().density;
            int cssHeight = Math.max(1, Math.round(heightPx / density));
            String js = "(function(){"
                + "var h=" + cssHeight + ";"
                + "var root=document.documentElement;"
                + "root.style.setProperty('--linkline-native-height',h+'px');"
                + "root.classList.toggle('linkline-native-h760',h<=760);"
                + "root.classList.toggle('linkline-native-h680',h<=680);"
                + "root.classList.toggle('linkline-native-h620',h<=620);"
                + "var s=document.getElementById('linkline-native-viewport-style');"
                + "if(!s){s=document.createElement('style');s.id='linkline-native-viewport-style';document.head.appendChild(s);}"
                + "s.textContent='"
                + ".app-shell[data-view=\"home\"]{height:var(--linkline-native-height)!important;min-height:var(--linkline-native-height)!important;max-height:var(--linkline-native-height)!important;}"
                + "html.linkline-native-h760 .view-home{gap:12px!important;}"
                + "html.linkline-native-h760 .home-actions{transform:translateY(-14px)!important;gap:14px!important;}"
                + "html.linkline-native-h680 .app-shell{padding-top:max(12px,env(safe-area-inset-top))!important;padding-bottom:max(12px,env(safe-area-inset-bottom))!important;}"
                + "html.linkline-native-h680 .topbar{min-height:64px!important;padding-bottom:12px!important;}"
                + "html.linkline-native-h680 .stage{margin-top:7px!important;}"
                + "html.linkline-native-h680 .screen{padding-top:12px!important;}"
                + "html.linkline-native-h680 .signal-preview{width:min(calc(var(--linkline-native-height)*.54),320px)!important;}"
                + "html.linkline-native-h680 .home-stage{font-size:30px!important;}"
                + "html.linkline-native-h680 .home-actions{gap:12px!important;transform:translateY(-12px)!important;}"
                + "html.linkline-native-h680 .home-secondary{gap:10px!important;}"
                + "html.linkline-native-h680 .icon-action{min-height:88px!important;padding-top:61px!important;}"
                + "html.linkline-native-h680 .icon-action::before{width:54px!important;height:54px!important;}"
                + "html.linkline-native-h680 .icon-action::after{width:29px!important;height:29px!important;top:12.5px!important;}"
                + "';"
                + "requestAnimationFrame(function(){window.dispatchEvent(new Event('resize'));});"
                + "})();";
            webView.evaluateJavascript(js, null);
        });
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
        } else {
            super.onBackPressed();
        }
    }

    @Override
    protected void onDestroy() {
        if (webView != null) {
            webView.stopLoading();
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }

    private final class LocalAssetClient extends WebViewClient {
        @Override
        public void onPageFinished(WebView view, String url) {
            super.onPageFinished(view, url);
            pageReady = true;
            lastNativeViewportHeightPx = -1;
            syncNativeViewport();
        }

        @Override
        public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            return !isLocal(uri);
        }

        @Override
        public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
            Uri uri = request.getUrl();
            if (!isLocal(uri)) return null;

            String path = uri.getPath();
            if (path == null || path.isEmpty() || "/".equals(path)) path = "/index.html";
            if (path.contains("..")) return notFound();

            String assetPath = "www" + path;
            try {
                InputStream input = getAssets().open(assetPath);
                String mime = mimeType(path);
                String encoding = isTextMime(mime) ? "UTF-8" : null;
                return new WebResourceResponse(mime, encoding, input);
            } catch (IOException ignored) {
                return notFound();
            }
        }

        private boolean isLocal(Uri uri) {
            return LOCAL_SCHEME.equals(uri.getScheme()) && LOCAL_HOST.equals(uri.getHost());
        }

        private WebResourceResponse notFound() {
            byte[] body = "Not Found".getBytes(StandardCharsets.UTF_8);
            return new WebResourceResponse(
                "text/plain",
                "UTF-8",
                404,
                "Not Found",
                Collections.emptyMap(),
                new ByteArrayInputStream(body)
            );
        }
    }

    private static boolean isTextMime(String mime) {
        return mime.startsWith("text/")
            || mime.contains("javascript")
            || mime.contains("json")
            || mime.contains("svg")
            || mime.contains("manifest");
    }

    private static String mimeType(String path) {
        String lower = path.toLowerCase();
        if (lower.endsWith(".html")) return "text/html";
        if (lower.endsWith(".css")) return "text/css";
        if (lower.endsWith(".mjs") || lower.endsWith(".js")) return "text/javascript";
        if (lower.endsWith(".json")) return "application/json";
        if (lower.endsWith(".webmanifest")) return "application/manifest+json";
        if (lower.endsWith(".svg")) return "image/svg+xml";
        if (lower.endsWith(".png")) return "image/png";
        if (lower.endsWith(".jpg") || lower.endsWith(".jpeg")) return "image/jpeg";
        if (lower.endsWith(".webp")) return "image/webp";
        if (lower.endsWith(".woff2")) return "font/woff2";
        if (lower.endsWith(".woff")) return "font/woff";
        return "application/octet-stream";
    }
}
