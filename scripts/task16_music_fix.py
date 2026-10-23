#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 16a: fix music PLAYBACK on Android WebView (upload works, play fails).
Root cause: on a file:// page, blob: URLs come from an opaque origin and the
Chromium media stack on some WebView versions refuses to load audio from them.
Fix: robust load chain  blob URL  ->  (on error/timeout)  base64 data URL.
Also: guard the global audio error handler during controlled load attempts,
and give musicGetDuration the same fallback so durations work on the phone."""
import io, sys

P = '/home/z/my-project/public/app.html'
src = io.open(P, encoding='utf-8').read()
orig = len(src)
fails = []

def rep(old, new, n=1, tag=''):
    global src
    c = src.count(old)
    if c != n:
        fails.append(f'[{tag}] expected {n}, found {c}: {old[:80]!r}')
        return
    src = src.replace(old, new)
    print(f'  ok [{tag}] x{c}')

# ---------- 1. helpers: data-url + robust load chain ----------
helpers = r'''
    // ---- TASK 16: WebView-safe audio loading ----
    // On file:// pages some Android WebView versions refuse media from blob:
    // URLs (opaque origin). Falling back to a base64 data URL bypasses that.
    let musicLoadBusy = false;
    function musicBlobToDataUrl(blob) {
      return new Promise(resolve => {
        try {
          const fr = new FileReader();
          const to = setTimeout(() => resolve(null), 40000);
          fr.onload = () => { clearTimeout(to); resolve(fr.result || null); };
          fr.onerror = () => { clearTimeout(to); resolve(null); };
          fr.readAsDataURL(blob);
        } catch (e) { resolve(null); }
      });
    }
    function musicAttachOnce(ev, fn) { musicAudio.addEventListener(ev, fn, { once: true }); return fn; }
    function musicLoadVia(kind, srcVal, timeoutMs, onOk, onFail) {
      const okH = musicAttachOnce('canplay', () => { cleanup(); onOk(); });
      const okH2 = musicAttachOnce('loadeddata', () => { cleanup(); onOk(); });
      const errH = musicAttachOnce('error', () => { cleanup(); onFail(); });
      const to = setTimeout(() => { cleanup(); onFail(); }, timeoutMs);
      function cleanup() {
        clearTimeout(to);
        try { musicAudio.removeEventListener('canplay', okH); musicAudio.removeEventListener('loadeddata', okH2); musicAudio.removeEventListener('error', errH); } catch (e) {}
      }
      try {
        musicAudio.src = srcVal;
        musicAudio.load();
      } catch (e) { cleanup(); onFail(); }
    }
    // Tries blob URL first (fast + streaming); on failure retries as data URL.
    function musicLoadAudio(blob) {
      musicLoadBusy = true;
      return new Promise(resolve => {
        const finish = ok => { musicLoadBusy = false; resolve(ok); };
        let url = null;
        try { url = URL.createObjectURL(blob); } catch (e) { url = null; }
        if (!url) { viaData(); return; }
        musicLoadVia('blob', url, 9000, () => {
          currentMusicUrl = url; finish(true);
        }, () => { viaData(); });
        function viaData() {
          try { if (url) URL.revokeObjectURL(url); } catch (e) {}
          musicBlobToDataUrl(blob).then(du => {
            if (!du) { currentMusicUrl = null; finish(false); return; }
            musicLoadVia('data', du, 30000, () => {
              currentMusicUrl = du; finish(true); // data URLs need no revoke
            }, () => { currentMusicUrl = null; finish(false); });
          });
        }
      });
    }
'''

old_anchor = '''    function musicCleanName(fileName) {'''
rep(old_anchor, helpers + '\n' + old_anchor, 1, 'helpers')

# ---------- 2. playMusicTrack -> use the load chain ----------
old_play = '''    async function playMusicTrack(id) {
      const meta = state.musicTracks.find(t => t.id === id);
      if (!meta) return;
      const rec = await idbMusicGet(id);
      if (!rec || !rec.blob) { showToast('فایل این موزیک پیدا نشد — دوباره آپلودش کن 🎵'); return; }
      try { if (currentMusicUrl) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
      currentMusicUrl = URL.createObjectURL(rec.blob);
      musicAudio.src = currentMusicUrl;
      try {
        await musicAudio.play();
      } catch (e) {
        currentPlayingId = id;
        renderMusicList();
        updateMusicMiniPlayer();
        showToast(e && e.name === 'NotAllowedError' ? 'پخش خودکار مرورگر اجازه نداد — دکمه پخش را بزن ▶️' : 'پخش این فایل ممکن نشد — آن را حذف و دوباره آپلود کن 🎵');
        return;
      }'''
new_play = '''    async function playMusicTrack(id) {
      const meta = state.musicTracks.find(t => t.id === id);
      if (!meta) return;
      const rec = await idbMusicGet(id);
      if (!rec || !rec.blob) { showToast('فایل این موزیک پیدا نشد — دوباره آپلودش کن 🎵'); return; }
      try { if (currentMusicUrl && currentMusicUrl.startsWith('blob:')) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
      currentMusicUrl = null;
      const loaded = await musicLoadAudio(rec.blob);
      if (!loaded) {
        currentPlayingId = id;
        renderMusicList();
        updateMusicMiniPlayer();
        showToast('پخش این فایل ممکن نشد — فرمت را عوض کن یا دوباره آپلودش کن 🎵');
        return;
      }
      try {
        await musicAudio.play();
      } catch (e) {
        currentPlayingId = id;
        renderMusicList();
        updateMusicMiniPlayer();
        showToast(e && e.name === 'NotAllowedError' ? 'پخش خودکار مرورگر اجازه نداد — دکمه پخش را بزن ▶️' : 'پخش این فایل ممکن نشد — آن را حذف و دوباره آپلود کن 🎵');
        return;
      }'''
rep(old_play, new_play, 1, 'playMusicTrack')

# ---------- 3. global error handler: no spam during chain, retry via chain ----------
old_err = '''    musicAudio.addEventListener('error', () => {
      if (!currentPlayingId) return;
      showToast('پخش این فایل ممکن نشد — دوباره تلاش می‌کنم 🎵');
      const rid = currentPlayingId;
      idbMusicGet(rid).then(rec => {
        if (!rec || !rec.blob) return;
        try { if (currentMusicUrl) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
        try {
          currentMusicUrl = URL.createObjectURL(rec.blob);
          musicAudio.src = currentMusicUrl;
          musicAudio.play().catch(() => {});
        } catch (e) {}
      });
    });'''
new_err = '''    musicAudio.addEventListener('error', () => {
      if (!currentPlayingId || musicLoadBusy) return; // task16: ignore mid-chain errors
      showToast('پخش این فایل ممکن نشد — دوباره تلاش می‌کنم 🎵');
      const rid = currentPlayingId;
      idbMusicGet(rid).then(rec => {
        if (!rec || !rec.blob || musicLoadBusy) return;
        try { if (currentMusicUrl && currentMusicUrl.startsWith('blob:')) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
        currentMusicUrl = null;
        musicLoadAudio(rec.blob).then(ok => { if (ok) musicAudio.play().catch(() => {}); });
      });
    });'''
rep(old_err, new_err, 1, 'error-handler')

# ---------- 4. musicGetDuration: same fallback ----------
old_dur = '''    function musicGetDuration(blob) {
      return new Promise(resolve => {
        let url;
        try { url = URL.createObjectURL(blob); } catch (e) { return resolve(0); }
        const a = new Audio();
        a.preload = 'metadata';
        let settled = false;
        const done = d => { if (settled) return; settled = true; try { URL.revokeObjectURL(url); } catch (e) {} resolve(d); };
        a.onloadedmetadata = () => { const d = a.duration; done(isFinite(d) && d > 0 ? Math.round(d) : 0); };
        a.onerror = () => done(0);
        setTimeout(() => done(0), 5000);
        a.src = url;
      });
    }'''
new_dur = '''    function musicGetDuration(blob) {
      return new Promise(resolve => {
        // task16: try blob URL, fall back to data URL (WebView file:// safe)
        const probe = new Audio();
        probe.preload = 'metadata';
        let settled = false;
        const done = d => { if (settled) return; settled = true; resolve(d); };
        const viaData = () => {
          musicBlobToDataUrl(blob).then(du => {
            if (!du) return done(0);
            probe.onloadedmetadata = () => { const d = probe.duration; done(isFinite(d) && d > 0 ? Math.round(d) : 0); };
            probe.onerror = () => done(0);
            setTimeout(() => done(0), 12000);
            probe.src = du;
          });
        };
        let url = null;
        try { url = URL.createObjectURL(blob); } catch (e) { viaData(); return; }
        probe.onloadedmetadata = () => { const d = probe.duration; try { URL.revokeObjectURL(url); } catch (e) {} done(isFinite(d) && d > 0 ? Math.round(d) : 0); };
        probe.onerror = () => { try { URL.revokeObjectURL(url); } catch (e) {} viaData(); };
        setTimeout(() => { try { URL.revokeObjectURL(url); } catch (e) {} viaData(); }, 5000);
        probe.src = url;
      });
    }'''
rep(old_dur, new_dur, 1, 'musicGetDuration')

# ---------- 5. toggleMusicPlay / stopMusic: only revoke blob urls (data urls fine) ----------
old_stop = '''      try { if (currentMusicUrl) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
      currentMusicUrl = null;
      const player = document.getElementById('musicMiniPlayer');'''
new_stop = '''      try { if (currentMusicUrl && currentMusicUrl.startsWith('blob:')) URL.revokeObjectURL(currentMusicUrl); } catch (e) {}
      currentMusicUrl = null;
      const player = document.getElementById('musicMiniPlayer');'''
rep(old_stop, new_stop, 1, 'stopMusic')

io.open(P, 'w', encoding='utf-8').write(src)
print(f'done: {orig} -> {len(src)} bytes ({len(src)-orig:+d})')
if fails:
    print('FAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('ALL PATCHES OK')
