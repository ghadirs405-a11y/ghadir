#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 15b: JS features —
   1) Music playback fix: materialize blobs with explicit MIME (WebView content:// safe),
      audio error handler + retry, smarter play() error message
   2) App-start boot splash (short HUD sequence, skippable, per-session)
   3) Backup export / restore import in profile modal
   4) Online/offline HUD badge for the Android APK bridge"""
import io, sys

P = '/home/z/my-project/public/app.html'
src = io.open(P, encoding='utf-8').read()
orig_len = len(src)
fails = []

def rep(old, new, n=1, tag=''):
    global src
    c = src.count(old)
    if c != n:
        fails.append(f'[{tag}] expected {n}, found {c}: {old[:70]!r}')
        return
    src = src.replace(old, new)

# ============ 1. Music playback fixes ============
print('== 1. music ==')
rep('''    // ---- Upload flow ----''',
'''    // ---- Upload flow ----
    function musicMimeFor(name, fallback) {
      const ext = (String(name || '').split('.').pop() || '').toLowerCase();
      const map = { mp3: 'audio/mpeg', m4a: 'audio/mp4', mp4: 'audio/mp4', ogg: 'audio/ogg', oga: 'audio/ogg', wav: 'audio/wav', aac: 'audio/aac', flac: 'audio/flac', opus: 'audio/opus', weba: 'audio/webm', webm: 'audio/webm', wma: 'audio/x-ms-wma', aif: 'audio/aiff', aiff: 'audio/aiff' };
      return map[ext] || fallback || 'audio/mpeg';
    }
    // WebView files picked via content:// sometimes fail as blob/audio sources.
    // Materializing the bytes into a plain JS-owned Blob with explicit MIME fixes playback.
    function musicMaterialize(file) {
      return new Promise(resolve => {
        const fallbackBlob = () => { try { return new Blob([file], { type: musicMimeFor(file.name, file.type) }); } catch (e) { return file; } };
        let fr = null;
        try { fr = new FileReader(); } catch (e) { resolve(fallbackBlob()); return; }
        const to = setTimeout(() => { try { fr.abort(); } catch (e2) {} resolve(fallbackBlob()); }, 25000);
        fr.onload = () => { clearTimeout(to); try { resolve(new Blob([fr.result], { type: musicMimeFor(file.name, file.type) })); } catch (e) { resolve(fallbackBlob()); } };
        fr.onerror = () => { clearTimeout(to); resolve(fallbackBlob()); };
        try { fr.readAsArrayBuffer(file); } catch (e) { clearTimeout(to); resolve(fallbackBlob()); }
      });
    }''', 1, 'materialize-fn')

rep('''        const id = 'mu' + Date.now() + Math.floor(Math.random() * 1000);
        const ok = await idbMusicPut({ id: id, blob: f, addedAt: new Date().toISOString() });
        if (!ok) { showToast('حافظه مرورگر اجازه ذخیره نداد 😕'); continue; }
        const duration = await musicGetDuration(f);''',
'''        const id = 'mu' + Date.now() + Math.floor(Math.random() * 1000);
        const storeBlob = f.size > 60 * 1024 * 1024 ? f : await musicMaterialize(f);
        const ok = await idbMusicPut({ id: id, blob: storeBlob, addedAt: new Date().toISOString() });
        if (!ok) { showToast('حافظه مرورگر اجازه ذخیره نداد 😕'); continue; }
        const duration = await musicGetDuration(storeBlob);''', 1, 'upload-materialize')

rep('''        showToast('پخش خودکار مرورگر اجازه نداد — دکمه پخش را بزن ▶️');''',
'''        showToast(e && e.name === 'NotAllowedError' ? 'پخش خودکار مرورگر اجازه نداد — دکمه پخش را بزن ▶️' : 'پخش این فایل ممکن نشد — آن را حذف و دوباره آپلود کن 🎵');''', 1, 'play-catch')

rep('''    musicAudio.addEventListener('pause', () => { updateMusicMiniPlayer(); renderMusicList(); });''',
'''    musicAudio.addEventListener('pause', () => { updateMusicMiniPlayer(); renderMusicList(); });
    musicAudio.addEventListener('error', () => {
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
    });''', 1, 'audio-error-handler')

rep('''style="background: ${isPlaying ? '#181445' : 'linear-gradient(135deg,#630ed4,#8b5cf6)'};"''',
    '''style="background: ${isPlaying ? 'linear-gradient(135deg,#0e7490,#7c3aed)' : 'linear-gradient(135deg,#630ed4,#8b5cf6)'};"''', 1, 'playbtn-hud')

# ============ 2. Boot splash markup ============
print('== 2. boot splash ==')
SPLASH = '''<div id="hudGrid" aria-hidden="true"></div>
  <div id="appBootScreen" aria-hidden="true">
    <div class="boot-grid-bg"></div>
    <div class="boot-hud-title">هسته ردیاب عادت‌ها<span class="boot-hud-ver">نسخه ۲.۰</span></div>
    <div class="boot-tag boot-tag-tl">حافظه: محلی</div>
    <div class="boot-tag boot-tag-br">امنیت: فعال</div>
    <div class="boot-corner boot-c-tl"></div><div class="boot-corner boot-c-tr"></div>
    <div class="boot-corner boot-c-bl"></div><div class="boot-corner boot-c-br"></div>
    <div class="boot-center">
      <div class="boot-orbiter" style="width:150px;height:150px;">
        <svg class="boot-ring boot-ring-a" viewBox="0 0 200 200" aria-hidden="true">
          <circle cx="100" cy="100" r="92" fill="none" stroke="rgba(34,211,238,0.35)" stroke-width="1.5" stroke-dasharray="10 14"/>
          <circle cx="100" cy="100" r="78" fill="none" stroke="rgba(139,92,246,0.45)" stroke-width="1" stroke-dasharray="3 9"/>
        </svg>
        <svg class="boot-ring boot-ring-b" viewBox="0 0 200 200" aria-hidden="true">
          <circle cx="100" cy="100" r="86" fill="none" stroke="rgba(34,211,238,0.3)" stroke-width="2.5" stroke-dasharray="46 260" stroke-linecap="round"/>
          <circle cx="100" cy="8" r="3.5" fill="#22d3ee"/>
        </svg>
        <div class="boot-head-wrap" style="width:92px;height:92px;">
          <svg class="boot-head" viewBox="0 0 120 120" aria-hidden="true">
            <defs>
              <linearGradient id="appBootGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#22d3ee"/>
                <stop offset="1" stop-color="#8b5cf6"/>
              </linearGradient>
            </defs>
            <line x1="60" y1="13" x2="60" y2="24" stroke="url(#appBootGrad)" stroke-width="3" stroke-linecap="round"/>
            <circle class="boot-antenna" cx="60" cy="9" r="4" fill="#22d3ee"/>
            <rect x="26" y="24" width="68" height="60" rx="18" fill="rgba(34,211,238,0.07)" stroke="url(#appBootGrad)" stroke-width="2.5"/>
            <rect x="16" y="44" width="8" height="20" rx="4" fill="rgba(34,211,238,0.22)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
            <rect x="96" y="44" width="8" height="20" rx="4" fill="rgba(34,211,238,0.22)" stroke="rgba(34,211,238,0.5)" stroke-width="1.5"/>
            <rect class="boot-eye" x="39" y="46" width="13" height="9" rx="4.5" fill="#22d3ee"/>
            <rect class="boot-eye" x="68" y="46" width="13" height="9" rx="4.5" fill="#22d3ee"/>
            <rect x="46" y="64" width="28" height="7" rx="3.5" fill="none" stroke="rgba(34,211,238,0.55)" stroke-width="1.5"/>
            <line x1="53" y1="65.5" x2="53" y2="69.5" stroke="rgba(34,211,238,0.55)" stroke-width="1.5"/>
            <line x1="60" y1="65.5" x2="60" y2="69.5" stroke="rgba(34,211,238,0.55)" stroke-width="1.5"/>
            <line x1="67" y1="65.5" x2="67" y2="69.5" stroke="rgba(34,211,238,0.55)" stroke-width="1.5"/>
          </svg>
          <div class="boot-scanline"></div>
        </div>
      </div>
      <div class="boot-terminal" id="appBootTerminal" style="min-height:74px;"></div>
      <div class="boot-progress-track"><div class="boot-progress-fill" id="appBootFill"></div></div>
      <div class="boot-percent" id="appBootPct">۰٪</div>
    </div>
    <div class="boot-skip-hint">برای رد کردن، لمس کن</div>
  </div>'''
rep('<div id="hudGrid" aria-hidden="true"></div>', SPLASH, 1, 'splash-markup')

# splash CSS (append after selection rule)
rep('''  ::selection { background: rgba(34,211,238,0.35); color: #ffffff; }''',
'''  ::selection { background: rgba(34,211,238,0.35); color: #ffffff; }
  /* app-start boot splash (short cinematic sequence) */
  #appBootScreen { position: fixed; inset: 0; z-index: 80; background: radial-gradient(ellipse at 50% 42%, #1b1147 0%, #0d0722 52%, #050310 100%); display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.45s ease; cursor: pointer; }
  #appBootScreen.active { opacity: 1; pointer-events: auto; }
  #appBootScreen.leaving { opacity: 0; }
  #appBootScreen .boot-head-wrap { position: absolute; }
  #appBootScreen .boot-orbiter { position: relative; }''', 1, 'splash-css')

# ============ 3. Backup section in profile modal ============
print('== 3. backup ==')
BAK = '''        <div id="notebookHistory" class="space-y-2"></div>
      </div>

      <div class="border-t border-surface-container-highest pt-4">
        <h4 class="font-bold text-on-surface text-sm mb-1 flex items-center gap-2">
          <span class="material-symbols-outlined text-[18px] text-agent-secondary">cloud_sync</span>
          پشتیبان‌گیری اطلاعات
        </h4>
        <p class="text-[11px] text-on-surface-variant leading-relaxed mb-3">از همه‌ی عادت‌ها، استریک‌ها، حال‌ها و یادداشت‌هایت یک فایل پشتیبان بگیر تا در هر گوشی یا بعد از نصب نسخه جدید آن‌ها را بازیابی کنی. (خود فایل‌های موزیک شامل نمی‌شوند و باید دوباره آپلود شوند)</p>
        <div class="flex gap-2">
          <button onclick="exportDataBak()" class="flex-1 py-2.5 rounded-xl bg-primary/15 border border-primary/40 text-primary text-xs font-bold flex items-center justify-center gap-1.5 active:scale-95 transition-transform">
            <span class="material-symbols-outlined text-[16px]">download</span> دانلود پشتیبان
          </button>
          <button onclick="document.getElementById('bakFileInput').click()" class="flex-1 py-2.5 rounded-xl bg-surface-container-low border border-surface-container-highest text-on-surface text-xs font-bold flex items-center justify-center gap-1.5 active:scale-95 transition-transform">
            <span class="material-symbols-outlined text-[16px]">upload</span> بازیابی پشتیبان
          </button>
        </div>
        <input type="file" id="bakFileInput" accept="application/json,.json" class="hidden" onchange="importDataBakFile(this)">
      </div>'''
rep('''        <div id="notebookHistory" class="space-y-2"></div>
      </div>''', BAK, 1, 'backup-section')

# ============ 4. New script block before </body> ============
print('== 4. feature js ==')
FEATURE_JS = '''  <script>
    // ==== TASK 15: app-start boot splash, backup/restore, APK online badge ====
    (function appBootSequence() {
      const scr = document.getElementById('appBootScreen');
      if (!scr) return;
      let done = false;
      let timers = [];
      try { if (sessionStorage.getItem('app_boot_done')) { scr.remove(); return; } } catch (e) {}
      scr.classList.add('active');
      const fin = () => {
        if (done) return; done = true;
        timers.forEach(clearTimeout);
        try { sessionStorage.setItem('app_boot_done', '1'); } catch (e) {}
        scr.classList.add('leaving');
        setTimeout(() => { try { scr.remove(); } catch (e) {} }, 500);
      };
      scr.addEventListener('pointerdown', fin, { once: true });
      const fa = n => String(n).replace(/\\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]);
      const LINES = [
        { t: 'راه‌اندازی هسته ردیاب عادت‌ها…', ok: false },
        { t: 'اتصال به حافظه محلی… ✓', ok: true },
        { t: 'بارگذاری کوه‌های پیشرفت… ✓', ok: true },
        { t: 'همگام‌سازی استریک‌ها… ✓', ok: true },
        { t: 'آماده‌سازی کتابخانه موزیک… ✓', ok: true },
        { t: 'سیستم آماده است — موفق باشی 🚀', ok: true }
      ];
      const term = document.getElementById('appBootTerminal');
      const fill = document.getElementById('appBootFill');
      const pct = document.getElementById('appBootPct');
      LINES.forEach((l, i) => timers.push(setTimeout(() => {
        if (!term) return;
        const d = document.createElement('div');
        d.className = 'boot-line' + (l.ok ? ' ok' : '');
        d.innerHTML = '<span class="cur"></span>' + l.t;
        term.appendChild(d);
      }, 140 + i * 380)));
      const t0 = performance.now();
      const DUR = 2500;
      const step = t => {
        if (done) return;
        const k = Math.min(1, (t - t0) / DUR);
        const v = Math.round((1 - Math.pow(1 - k, 1.25)) * 100);
        if (fill) fill.style.width = v + '%';
        if (pct) pct.textContent = fa(v) + '٪';
        if (k < 1) requestAnimationFrame(step);
        else setTimeout(fin, 320);
      };
      requestAnimationFrame(step);
      timers.push(setTimeout(fin, 6000));
    })();

    function exportDataBak() {
      try {
        const data = { app: 'habits-tracker', version: 2, exportedAt: new Date().toISOString(), state: state };
        const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'habits-backup-' + new Date().toISOString().slice(0, 10) + '.json';
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(() => { try { URL.revokeObjectURL(a.href); } catch (e) {} }, 5000);
        showToast('فایل پشتیبان ذخیره شد 💾');
      } catch (e) { showToast('پشتیبان‌گیری ممکن نشد 😕'); }
    }
    function importDataBakFile(inp) {
      const f = inp && inp.files && inp.files[0];
      if (!f) return;
      inp.value = '';
      const fr = new FileReader();
      fr.onload = () => {
        try {
          const data = JSON.parse(fr.result);
          const st = data && data.state ? data.state : data;
          if (!st || typeof st !== 'object' || !Array.isArray(st.habits)) { showToast('این فایل پشتیبان معتبر نیست 😕'); return; }
          Object.assign(state, st);
          saveState();
          renderAll();
          closeAllModals();
          triggerConfetti();
          showToast('اطلاعات با موفقیت بازیابی شد ✅');
        } catch (e) { showToast('خواندن فایل پشتیبان ممکن نشد 😕'); }
      };
      fr.onerror = () => showToast('خواندن فایل ممکن نشد 😕');
      fr.readAsText(f);
    }

    (function apkNetBadge() {
      if (!(window.AndroidApp && typeof window.AndroidApp.isOnline === 'function')) return;
      const el = document.createElement('div');
      el.id = 'netBadge';
      el.style.cssText = 'position:fixed;top:10px;left:10px;z-index:75;display:flex;align-items:center;gap:5px;font-size:9px;font-weight:800;padding:3px 9px;border-radius:100px;background:rgba(16,10,40,0.85);border:1px solid rgba(34,211,238,0.4);color:#67e8f9;letter-spacing:0.5px;backdrop-filter:blur(8px);pointer-events:none;';
      document.body.appendChild(el);
      const upd = () => {
        let on = false;
        try { on = !!window.AndroidApp.isOnline(); } catch (e) {}
        el.innerHTML = '<span style="width:5px;height:5px;border-radius:50%;background:' + (on ? '#34d399' : '#64748b') + ';box-shadow:0 0 8px ' + (on ? 'rgba(52,211,153,0.9)' : 'none') + ';"></span>' + (on ? 'آنلاین' : 'آفلاین');
        el.style.borderColor = on ? 'rgba(34,211,238,0.4)' : 'rgba(100,116,139,0.4)';
        el.style.color = on ? '#67e8f9' : '#94a3b8';
      };
      upd();
      setInterval(upd, 4000);
    })();
  </script>
</body>'''
rep('</body>', FEATURE_JS, 1, 'feature-js')

io.open(P, 'w', encoding='utf-8').write(src)
print(f'\nDone. {orig_len} -> {len(src)} bytes')
if fails:
    print('FAILED:')
    for f in fails: print('  ' + f)
    sys.exit(1)
print('ALL OK')
