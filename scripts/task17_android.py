#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 17d: MainActivity — native audio bridge (chunked save) + pseudo-https
interception (https://appassets.local/music/<id>) with Range support, plus
version bump to versionCode 4 / versionName 2.2."""
import io, sys

JP = '/home/z/my-project/android/apk-src/src/com/habits/tracker/MainActivity.java'
MP = '/home/z/my-project/android/apk-src/AndroidManifest.xml'
fails = []

j = io.open(JP, encoding='utf-8').read()

# ---------- 1. import ----------
old = 'import android.webkit.WebViewClient;'
if j.count(old) != 1:
    fails.append('import anchor')
else:
    j = j.replace(old, 'import android.webkit.WebResourceRequest;\nimport android.webkit.WebResourceResponse;\nimport android.webkit.WebViewClient;')

# ---------- 2. field for chunk buffers ----------
old = '    private ValueCallback<Uri[]> filePathCallback;'
if j.count(old) != 1:
    fails.append('field anchor')
else:
    j = j.replace(old, old + '\n    private final java.util.Map<String, java.io.ByteArrayOutputStream> trackBuf = new java.util.HashMap<String, java.io.ByteArrayOutputStream>();')

# ---------- 3. shouldInterceptRequest inside WebViewClient ----------
old = '''            @Override
            public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {'''
new = '''            @Override
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
            public boolean onRenderProcessGone(WebView view, RenderProcessGoneDetail detail) {'''
if j.count(old) != 1:
    fails.append('intercept anchor')
else:
    j = j.replace(old, new)

# ---------- 4. serveTrack + bounded stream + bridge methods (before last closing brace) ----------
tail = '''    private WebResourceResponse serveTrack(String id, WebResourceRequest request) {
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
        public boolean isOnline() {'''
if j.count(tail) != 1:
    fails.append('bridge anchor')
else:
    j = j.replace(tail, tail.replace('private class Bridge {', 'private class Bridge {')  # keep, replaced below
              .replace('private boolean validTrackId(String id) {\n        return id != null && id.matches("[A-Za-z0-9]+");\n    }\n\n    private class Bridge {',
                       'private boolean validTrackId(String id) {\n        return id != null && id.matches("[A-Za-z0-9]+");\n    }\n\n    private class Bridge {')
              , tail)  # no-op guard
# The above no-op trick is unnecessary; do the real insertion:
old_bridge = '''    private class Bridge {
        @JavascriptInterface
        public boolean isOnline() {'''
new_bridge = '''    private class Bridge {
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
        public boolean isOnline() {'''
if j.count(old_bridge) != 1:
    fails.append('bridge-body anchor')
else:
    j = j.replace(old_bridge, new_bridge)

# drop the placeholder no-op block if it leaked (safety)
j = j.replace('''    private boolean validTrackId(String id) {
        return id != null && id.matches("[A-Za-z0-9]+");
    }

    private class Bridge {
        @JavascriptInterface
        public boolean isOnline() {''', '''    private boolean validTrackId(String id) {
        return id != null && id.matches("[A-Za-z0-9]+");
    }
PLACHOLDER_SPLIT
    private class Bridge {
        @JavascriptInterface
        public boolean isOnline() {''')
# actually simpler: ensure validTrackId exists exactly once
if j.count('private boolean validTrackId') != 1:
    fails.append('validTrackId count = %d' % j.count('private boolean validTrackId'))

io.open(JP, 'w', encoding='utf-8').write(j)

# ---------- 5. manifest bump ----------
m = io.open(MP, encoding='utf-8').read()
old_v = 'android:versionCode="3"\n    android:versionName="2.1"'
if m.count(old_v) != 1:
    fails.append('manifest version anchor')
else:
    m = m.replace(old_v, 'android:versionCode="4"\n    android:versionName="2.2"')
    io.open(MP, 'w', encoding='utf-8').write(m)
    print('manifest -> versionCode 4 / versionName 2.2')

# UA bump
old_ua = 'HabitTrackerAndroid/2.1'
if j.count(old_ua) != 1:
    fails.append('UA anchor')
else:
    j = j.replace(old_ua, 'HabitTrackerAndroid/2.2')
    io.open(JP, 'w', encoding='utf-8').write(j)
    print('UA -> 2.2')

if fails:
    print('FAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('JAVA PATCHES OK')
