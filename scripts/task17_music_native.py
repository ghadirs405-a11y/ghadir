#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 17b: music playback native path for the Android APK.
On the user's phone even the blob->dataUrl chain fails, so now (when the
Android bridge is present) the bytes are ALSO streamed to Java at upload
time (chunked base64) and playback uses a pseudo-https URL served by
shouldInterceptRequest from real files — bulletproof on every WebView."""
import io, sys

P = '/home/z/my-project/public/app.html'
src = io.open(P, encoding='utf-8').read()
orig = len(src)
fails = []

def rep(old, new, n=1, tag=''):
    global src
    c = src.count(old)
    if c != n:
        fails.append(f'[{tag}] expected {n}, found {c}: {old[:90]!r}')
        return
    src = src.replace(old, new)
    print(f'  ok [{tag}] x{c}')

# ---------- 1. native bridge helpers ----------
native_js = r'''
    // ---- TASK 17: native (Android) audio path — real files via interception ----
    function musicNativeOn() {
      try { return !!(window.AndroidApp && typeof window.AndroidApp.saveTrackBegin === 'function' && typeof window.AndroidApp.trackExists === 'function'); } catch (e) { return false; }
    }
    function musicNativeUrl(id) { return 'https://appassets.local/music/' + id; }
    async function musicNativeSave(id, blob) {
      try {
        const A = window.AndroidApp;
        if (!A || typeof A.saveTrackBegin !== 'function') return false;
        if (typeof A.trackExists === 'function' && A.trackExists(id)) { try { A.deleteTrack(id); } catch (e0) {} }
        A.saveTrackBegin(id);
        const du = await musicBlobToDataUrl(blob);
        if (!du) { try { A.saveTrackAbort(id); } catch (e1) {} return false; }
        const b64 = du.slice(du.indexOf(',') + 1);
        const CH = 1048576; // 1MB of base64 = multiple of 4, decodes independently
        for (let i = 0; i < b64.length; i += CH) {
          A.saveTrackChunk(id, b64.slice(i, i + CH));
        }
        const mime = musicMimeFor('', (blob && blob.type) || 'audio/mpeg');
        const ok = A.saveTrackEnd(id, mime);
        return !!ok;
      } catch (e) {
        try { window.AndroidApp.saveTrackAbort(id); } catch (e2) {}
        return false;
      }
    }
'''
rep('''    function musicCleanName(fileName) {''', native_js + '''
    function musicCleanName(fileName) {''', 1, 'native-helpers')

# ---------- 2. load chain: native URL first when available ----------
old_chain = '''    // Tries blob URL first (fast + streaming); on failure retries as data URL.
    function musicLoadAudio(blob) {
      musicLoadBusy = true;
      return new Promise(resolve => {
        const finish = ok => { musicLoadBusy = false; resolve(ok); };
        let url = null;
        try { url = URL.createObjectURL(blob); } catch (e) { url = null; }
        if (!url) { viaData(); return; }'''
new_chain = '''    // Order: native file (APK) -> blob URL (fast) -> data URL (base64).
    function musicLoadAudio(blob, id) {
      musicLoadBusy = true;
      return new Promise(resolve => {
        const finish = ok => { musicLoadBusy = false; resolve(ok); };
        if (id && musicNativeOn()) {
          let has = false;
          try { has = !!window.AndroidApp.trackExists(id); } catch (e) { has = false; }
          if (has) {
            musicLoadVia('native', musicNativeUrl(id), 8000, () => finish(true), () => viaBlob());
            return;
          }
        }
        viaBlob();
        function viaBlob() {
        let url = null;
        try { url = URL.createObjectURL(blob); } catch (e) { url = null; }
        if (!url) { viaData(); return; }'''
rep(old_chain, new_chain, 1, 'load-chain')

# close the extra function wrapper introduced above
old_tail = '''        function viaData() {
          try { if (url) URL.revokeObjectURL(url); } catch (e) {}
          musicBlobToDataUrl(blob).then(du => {
            if (!du) { currentMusicUrl = null; finish(false); return; }
            musicLoadVia('data', du, 30000, () => {
              currentMusicUrl = du; finish(true); // data URLs need no revoke
            }, () => { currentMusicUrl = null; finish(false); });
          });
        }
      });
    }'''
new_tail = '''          function viaData() {
            try { if (url) URL.revokeObjectURL(url); } catch (e) {}
            musicBlobToDataUrl(blob).then(du => {
              if (!du) { currentMusicUrl = null; finish(false); return; }
              musicLoadVia('data', du, 30000, () => {
                currentMusicUrl = du; finish(true); // data URLs need no revoke
              }, () => { currentMusicUrl = null; finish(false); });
            });
          }
        }
      });
    }'''
rep(old_tail, new_tail, 1, 'load-chain-tail')

# blob phase references currentMusicUrl = url inside viaBlob scope — keep; verify string present
if "currentMusicUrl = url; finish(true);" not in src:
    fails.append('[blob-ok-line] missing')

# ---------- 3. call sites ----------
rep('''      currentMusicUrl = null;
      const loaded = await musicLoadAudio(rec.blob);''',
'''      currentMusicUrl = null;
      const loaded = await musicLoadAudio(rec.blob, id);''', 1, 'play-call')

rep('''        musicLoadAudio(rec.blob).then(ok => { if (ok) musicAudio.play().catch(() => {}); });''',
'''        musicLoadAudio(rec.blob, rid).then(ok => { if (ok) musicAudio.play().catch(() => {}); });''', 1, 'retry-call')

# ---------- 4. upload: stream bytes to native too ----------
old_up = '''        const storeBlob = f.size > 60 * 1024 * 1024 ? f : await musicMaterialize(f);
        const ok = await idbMusicPut({ id: id, blob: storeBlob, addedAt: new Date().toISOString() });
        if (!ok) { showToast('حافظه مرورگر اجازه ذخیره نداد 😕'); continue; }'''
new_up = '''        const storeBlob = f.size > 60 * 1024 * 1024 ? f : await musicMaterialize(f);
        const ok = await idbMusicPut({ id: id, blob: storeBlob, addedAt: new Date().toISOString() });
        if (!ok) { showToast('حافظه مرورگر اجازه ذخیره نداد 😕'); continue; }
        if (musicNativeOn()) await musicNativeSave(id, storeBlob); // task17: native copy for guaranteed playback'''
rep(old_up, new_up, 1, 'upload-native')

# ---------- 5. delete: remove native copy ----------
rep('''      if (currentPlayingId === id) stopMusic();
      idbMusicDelete(id);''',
'''      if (currentPlayingId === id) stopMusic();
      idbMusicDelete(id);
      try { if (musicNativeOn() && window.AndroidApp.deleteTrack) window.AndroidApp.deleteTrack(id); } catch (e) {}''', 1, 'delete-native')

io.open(P, 'w', encoding='utf-8').write(src)
print(f'done: {orig} -> {len(src)} chars ({len(src)-orig:+d})')
if fails:
    print('FAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('NATIVE MUSIC PATCHES OK')
