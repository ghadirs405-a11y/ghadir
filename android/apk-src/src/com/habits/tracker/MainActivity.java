package com.habits.tracker;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.net.ConnectivityManager;
import android.net.Network;
import android.net.NetworkCapabilities;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.view.KeyEvent;
import android.webkit.JavascriptInterface;
import android.webkit.RenderProcessGoneDetail;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebViewClient;

public class MainActivity extends Activity {

    private WebView web;
    private ValueCallback<Uri[]> filePathCallback;
    private final java.util.Map<String, java.io.ByteArrayOutputStream> trackBuf = new java.util.HashMap<String, java.io.ByteArrayOutputStream>();
    private static final int FILE_CHOOSER_REQUEST = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        web = new WebView(this);
        web.setBackgroundColor(0xFF0B0722);

        WebSettings s = web.getSettings();
        s.setJavaScriptEnabled(true);
        s.setDomStorageEnabled(true);
        s.setAllowFileAccess(true);
        s.setAllowContentAccess(true);
        try {
            s.setAllowFileAccessFromFileURLs(true);
            s.setAllowUniversalAccessFromFileURLs(true);
        } catch (Throwable t) { }
        s.setMediaPlaybackRequiresUserGesture(false);
        s.setTextZoom(100);
        s.setLoadWithOverviewMode(true);
        s.setUseWideViewPort(true);
        s.setMixedContentMode(WebSettings.MIXED_CONTENT_ALWAYS_ALLOW);
        s.setUserAgentString(s.getUserAgentString() + " HabitTrackerAndroid/2.2");

        web.addJavascriptInterface(new Bridge(), "AndroidApp");

        web.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView v, String url) {
                if (url != null && (url.startsWith("file://") || url.startsWith("data:") || url.startsWith("blob:"))) {
                    return false;
                }
                if (url != null && (url.startsWith("http://") || url.startsWith("https://"))) {
                    return false;
                }
                try {
                    startActivity(new Intent(Intent.ACTION_VIEW, Uri.parse(url)));
                } catch (Throwable t) { }
                return true;
            }

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                try {
                    android.net.Uri u = request.getUrl();
                    if (u != null && "appassets.local".equals(u.getHost()) && u.getPath() != null && u.getPath().startsWith("/music/")) {
                        return serveTrack(u.getPath().substring("/music/".length()), request);
                    }
                } catch (Throwable t) { }
                return null;
            }

            @Override
            public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {
                // Avoid dead black screen on old/crashing WebViews: rebuild the view
                try {
                    finish();
                    startActivity(getIntent());
                } catch (Throwable t) { }
                return true;
            }
        });

        web.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(WebView v, ValueCallback<Uri[]> cb, FileChooserParams params) {
                if (filePathCallback != null) {
                    try { filePathCallback.onReceiveValue(null); } catch (Throwable t) { }
                }
                filePathCallback = cb;

                Intent intent = new Intent(Intent.ACTION_GET_CONTENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("audio/*");
                intent.putExtra(Intent.EXTRA_ALLOW_MULTIPLE, true);
                try {
                    String[] types = params.getAcceptTypes();
                    if (types != null && types.length > 0 && types[0] != null && types[0].trim().length() > 0) {
                        intent.setType(types[0].split(",")[0].trim());
                    }
                } catch (Throwable t) { }

                try {
                    startActivityForResult(Intent.createChooser(intent, "انتخاب موزیک"), FILE_CHOOSER_REQUEST);
                } catch (Throwable t) {
                    filePathCallback = null;
                    return false;
                }
                return true;
            }
        });

        setContentView(web);
        web.loadUrl("file:///android_asset/www/index.html");
    }

    @Override
    protected void onActivityResult(int req, int res, Intent data) {
        if (req == FILE_CHOOSER_REQUEST) {
            Uri[] out = null;
            if (res == RESULT_OK && data != null) {
                if (data.getClipData() != null) {
                    int n = data.getClipData().getItemCount();
                    if (n > 0) {
                        out = new Uri[n];
                        for (int i = 0; i < n; i++) out[i] = data.getClipData().getItemAt(i).getUri();
                    }
                } else if (data.getData() != null) {
                    out = new Uri[] { data.getData() };
                }
            }
            if (filePathCallback != null) {
                try { filePathCallback.onReceiveValue(out); } catch (Throwable t) { }
                filePathCallback = null;
            }
            return;
        }
        super.onActivityResult(req, res, data);
    }

    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK && web != null && web.canGoBack()) {
            web.goBack();
            return true;
        }
        return super.onKeyDown(keyCode, event);
    }

    @Override
    protected void onPause() {
        super.onPause();
        if (web != null) web.onPause();
    }

    @Override
    protected void onResume() {
        super.onResume();
        if (web != null) web.onResume();
    }

    @Override
    protected void onDestroy() {
        if (web != null) web.destroy();
        super.onDestroy();
    }

    private WebResourceResponse serveTrack(String id, WebResourceRequest request) {
        try {
            if (id == null || !id.matches("[A-Za-z0-9]+")) return null;
            java.io.File dir = new java.io.File(getFilesDir(), "music");
            java.io.File f = new java.io.File(dir, id + ".bin");
            if (!f.exists() || !f.canRead()) return null;
            String mime = "application/octet-stream";
            try {
                java.io.File mf = new java.io.File(dir, id + ".mime");
                if (mf.exists()) {
                    java.io.FileInputStream mfi = new java.io.FileInputStream(mf);
                    byte[] mb = new byte[(int) mf.length()];
                    int read = mfi.read(mb);
                    mfi.close();
                    if (read > 0) mime = new String(mb, "UTF-8").trim();
                }
            } catch (Throwable t2) { }
            long len = f.length();
            java.util.Map<String, String> h = new java.util.HashMap<String, String>();
            h.put("Accept-Ranges", "bytes");
            h.put("Cache-Control", "no-store");
            String range = request.getRequestHeaders() == null ? null : request.getRequestHeaders().get("Range");
            if (range != null && range.startsWith("bytes=")) {
                long start = 0, end = len - 1;
                try {
                    String spec = range.substring(6).trim();
                    int dash = spec.indexOf('-');
                    String a = dash > 0 ? spec.substring(0, dash).trim() : spec.replace("-", "").trim();
                    String b = (dash > 0 && dash + 1 < spec.length()) ? spec.substring(dash + 1).trim() : "";
                    if (a.length() > 0) start = Long.parseLong(a);
                    if (b.length() > 0) end = Long.parseLong(b);
                } catch (Throwable t3) { }
                if (end >= len) end = len - 1;
                if (start < 0 || start > end || start >= len) {
                    h.put("Content-Range", "bytes */" + len);
                    return new WebResourceResponse(mime, null, 416, "Requested Range Not Satisfiable", h,
                            new java.io.ByteArrayInputStream(new byte[0]));
                }
                h.put("Content-Range", "bytes " + start + "-" + end + "/" + len);
                java.io.FileInputStream fis = new java.io.FileInputStream(f);
                long skipped = 0;
                while (skipped < start) {
                    long s = fis.skip(start - skipped);
                    if (s <= 0) break;
                    skipped += s;
                }
                java.io.InputStream in = new BoundedInputStream(fis, end - start + 1);
                return new WebResourceResponse(mime, null, 206, "Partial Content", h, in);
            }
            h.put("Content-Length", String.valueOf(len));
            return new WebResourceResponse(mime, null, 200, "OK", h,
                    new java.io.BufferedInputStream(new java.io.FileInputStream(f)));
        } catch (Throwable t) {
            return null;
        }
    }

    static class BoundedInputStream extends java.io.InputStream {
        private final java.io.InputStream in;
        private long remaining;
        BoundedInputStream(java.io.InputStream in, long limit) { this.in = in; this.remaining = limit; }
        @Override public int available() throws java.io.IOException { return (int) Math.min(in.available(), remaining); }
        @Override public int read() throws java.io.IOException {
            if (remaining <= 0) return -1;
            int r = in.read();
            if (r >= 0) remaining--;
            return r;
        }
        @Override public int read(byte[] b, int off, int len) throws java.io.IOException {
            if (remaining <= 0) return -1;
            int r = in.read(b, off, (int) Math.min(len, remaining));
            if (r > 0) remaining -= r;
            return r;
        }
        @Override public void close() throws java.io.IOException { in.close(); }
    }

    private boolean validTrackId(String id) {
        return id != null && id.matches("[A-Za-z0-9]+");
    }

    private class Bridge {
        @JavascriptInterface
        public boolean saveTrackBegin(String id) {
            if (!validTrackId(id)) return false;
            try {
                trackBuf.remove(id);
                trackBuf.put(id, new java.io.ByteArrayOutputStream());
                return true;
            } catch (Throwable t) { return false; }
        }
        @JavascriptInterface
        public void saveTrackChunk(String id, String b64) {
            if (!validTrackId(id) || b64 == null) return;
            java.io.ByteArrayOutputStream buf = trackBuf.get(id);
            if (buf == null) return;
            try { buf.write(android.util.Base64.decode(b64, android.util.Base64.DEFAULT)); } catch (Throwable t) { }
        }
        @JavascriptInterface
        public boolean saveTrackEnd(String id, String mime) {
            if (!validTrackId(id)) return false;
            java.io.ByteArrayOutputStream buf = trackBuf.remove(id);
            if (buf == null) return false;
            try {
                java.io.File dir = new java.io.File(getFilesDir(), "music");
                dir.mkdirs();
                java.io.FileOutputStream fo = new java.io.FileOutputStream(new java.io.File(dir, id + ".bin"));
                buf.writeTo(fo);
                fo.close();
                java.io.FileOutputStream fm = new java.io.FileOutputStream(new java.io.File(dir, id + ".mime"));
                fm.write((mime == null || mime.trim().length() == 0 ? "application/octet-stream" : mime).getBytes("UTF-8"));
                fm.close();
                return true;
            } catch (Throwable t) { return false; }
        }
        @JavascriptInterface
        public void saveTrackAbort(String id) {
            if (validTrackId(id)) trackBuf.remove(id);
        }
        @JavascriptInterface
        public boolean trackExists(String id) {
            if (!validTrackId(id)) return false;
            try { return new java.io.File(new java.io.File(getFilesDir(), "music"), id + ".bin").exists(); } catch (Throwable t) { return false; }
        }
        @JavascriptInterface
        public boolean deleteTrack(String id) {
            if (!validTrackId(id)) return false;
            try {
                java.io.File dir = new java.io.File(getFilesDir(), "music");
                boolean ok = new java.io.File(dir, id + ".bin").delete();
                new java.io.File(dir, id + ".mime").delete();
                return ok;
            } catch (Throwable t) { return false; }
        }
        @JavascriptInterface
        public boolean isOnline() {
            try {
                ConnectivityManager cm = (ConnectivityManager) getSystemService(Context.CONNECTIVITY_SERVICE);
                if (cm == null) return false;
                if (Build.VERSION.SDK_INT >= 23) {
                    Network n = cm.getActiveNetwork();
                    if (n == null) return false;
                    NetworkCapabilities caps = cm.getNetworkCapabilities(n);
                    return caps != null && caps.hasCapability(NetworkCapabilities.NET_CAPABILITY_INTERNET);
                } else {
                    android.net.NetworkInfo info = cm.getActiveNetworkInfo();
                    return info != null && info.isConnected();
                }
            } catch (Throwable t) {
                return false;
            }
        }
    }
}
