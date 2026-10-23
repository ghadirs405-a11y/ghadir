#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 17d-fix: insert serveTrack + BoundedInputStream + validTrackId into
MainActivity (the first pass only applied import/field/intercept/bridge)."""
import io, sys

JP = '/home/z/my-project/android/apk-src/src/com/habits/tracker/MainActivity.java'
j = io.open(JP, encoding='utf-8').read()

if j.count('serveTrack') < 1 or j.count('BoundedInputStream') > 0:
    print('unexpected state: serveTrack refs=%d, BoundedInputStream=%d' % (j.count('serveTrack'), j.count('BoundedInputStream')))
    sys.exit(1)

block = '''    private WebResourceResponse serveTrack(String id, WebResourceRequest request) {
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

'''

anchor = '    private class Bridge {'
c = j.count(anchor)
if c != 1:
    print('bridge class anchor count = %d' % c)
    sys.exit(1)
j = j.replace(anchor, block + anchor)
io.open(JP, 'w', encoding='utf-8').write(j)
print('serveTrack+BoundedInputStream+validTrackId inserted OK')
