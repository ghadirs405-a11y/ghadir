#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TASK 18 - Patch A: robot avatar + 45s per-page sequence engine + offline AI (phone fix)
import io, sys, base64, shutil

APP = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task18.bak'
ROBOT_WEBP = '/home/z/my-project/upload/robot_avatar_256.webp'

src = io.open(APP, encoding='utf-8').read()
orig_len = len(src)

def replace_once(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: found %d occurrences' % (tag, n)); sys.exit(1)
    print('OK  [%s]' % tag)
    return s.replace(old, new, 1)

shutil.copyfile(APP, BAK)

b64 = base64.b64encode(open(ROBOT_WEBP, 'rb').read()).decode()

# ---------- A1) CSS ----------
css_anchor = "#agentBootScreen.boot-final .boot-status { color: #6ee7b7; text-shadow: 0 0 10px rgba(52,211,153,0.55); }"
css_add = css_anchor + """
  /* ==== TASK 18: per-page AI sequence engine (45s) ==== */
  #agentBootScreen .boot-robot-wrap { position: relative; width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; }
  #agentBootScreen .boot-robot-img { width: 126px; height: 126px; border-radius: 50%; object-fit: cover; border: 2.5px solid var(--seq-a, #22d3ee); box-shadow: 0 0 30px color-mix(in srgb, var(--seq-a, #22d3ee) 55%, transparent), 0 0 80px rgba(139,92,246,0.35); animation: bootRobotPulse 2.8s ease-in-out infinite; background: #14092e; }
  #agentBootScreen .boot-robot-ring { position: absolute; inset: 2px; border-radius: 50%; border: 1.5px dashed var(--seq-a, #22d3ee); opacity: .5; animation: bootSpin 16s linear infinite; }
  #agentBootScreen .boot-robot-ring.r2 { inset: -9px; border-color: var(--seq-b, #8b5cf6); opacity: .4; animation-direction: reverse; animation-duration: 22s; }
  @keyframes bootRobotPulse { 0%,100% { transform: scale(1); filter: brightness(1); } 50% { transform: scale(1.045); filter: brightness(1.14); } }
  @keyframes bootSpin { to { transform: rotate(360deg); } }
  #agentBootScreen.boot-fast .boot-robot-ring { animation-duration: 5s; opacity: .8; }
  #agentBootScreen.boot-fast .boot-robot-ring.r2 { animation-duration: 7s; }
  #agentBootScreen .boot-status { color: var(--seq-a, #6ee7b7); text-shadow: 0 0 10px color-mix(in srgb, var(--seq-a, #6ee7b7) 50%, transparent); }
  #agentBootScreen .boot-ring-a circle, #agentBootScreen .boot-ring-b circle { stroke: var(--seq-a, #22d3ee); }
  #agentBootScreen .boot-percent { color: var(--seq-a, #e2e8f0); }
  #agentBootScreen .boot-skip-btn { position: absolute; bottom: 26px; left: 50%; transform: translateX(-50%); padding: 7px 18px; border-radius: 100px; background: rgba(255,255,255,0.08); border: 1px solid var(--seq-a, #22d3ee); color: #e2e8f0; font-size: 11px; font-weight: 800; letter-spacing: .3px; backdrop-filter: blur(6px); z-index: 5; }
  #agentBootScreen .boot-terminal { max-height: 118px; overflow: hidden; }"""
src = replace_once(src, css_anchor, css_add, 'A1.css')

# ---------- A2) boot title dynamic + version ----------
src = replace_once(src,
  '<div class="boot-hud-title">هسته دستیار هوشمند<span class="boot-hud-ver">نسخه ۲.۲</span></div>',
  '<div class="boot-hud-title"><span id="bootHudTitle">هسته دستیار هوشمند</span><span class="boot-hud-ver" id="bootHudVer">نسخه ۲.۳</span></div>',
  'A2.title')

# ---------- A3) replace robot svg with photo-robot ----------
svg_start = src.index('<svg class="boot-head"')
svg_end = src.index('</svg>', svg_start) + len('</svg>')
svg_block = src[svg_start:svg_end]
robot_html = ('<div class="boot-robot-wrap">'
              '<div class="boot-robot-ring r2" aria-hidden="true"></div>'
              '<img id="bootRobotImg" class="boot-robot-img" alt="ربات دستیار هوشمند — چهره رو به بیننده" />'
              '<div class="boot-robot-ring" aria-hidden="true"></div>'
              '</div>')
print('OK  [A3.svg] removed %d chars of svg robot' % len(svg_block))
src = src[:svg_start] + robot_html + src[svg_end:]

# ---------- A4) skip hint (unique via bootFlash anchor) ----------
src = replace_once(src, '''<div class="boot-skip-hint">برای رد کردن، لمس کن</div>
    <div class="boot-flash" id="bootFlash"></div>''',
                        '''<button type="button" class="boot-skip-btn">رد کردن سکانس ⏭</button>
    <div class="boot-skip-hint">لمس صفحه = رد کردن</div>
    <div class="boot-flash" id="bootFlash"></div>''', 'A4.skip')

# ---------- A5) sequence engine: replace openAgentModalMaterialized..listener ----------
blk_start = src.index('    function openAgentModalMaterialized() {')
blk_end = src.index("    document.getElementById('agentBootScreen').addEventListener('pointerdown', () => hideBootScreen(true));")
blk_end = src.index('\n', blk_end)

ENGINE = r'''    function openAgentModalMaterialized() {
      const m = document.getElementById('agentModal');
      const reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      if (m && !reduce) {
        m.classList.remove('agent-materialize');
        void m.offsetWidth;
        m.classList.add('agent-materialize');
        setTimeout(() => m.classList.remove('agent-materialize'), 1300);
      }
      openModal('agentModal');
    }

    // ================= TASK 18: PER-PAGE 45s AI SEQUENCE ENGINE =================
    const ROBOT_AVATAR = 'data:image/webp;base64,__B64__';
    const SEQ_DUR = 45000;
    let seqTargetOpen = null;

    const SEQ_THEMES = {
      agent: {
        title: 'هسته دستیار هوشمند', tagTL: 'اتصال: پایدار', accent: '#22d3ee', accent2: '#8b5cf6',
        motto: 'دستیار آنلاین است — بپرس تا بسازیم ✨',
        open: () => { try { openAgentModalMaterialized(); } catch (e) { openModal('agentModal'); } },
        phases: ['انرژی‌رسانی هسته', 'متریالایز پوسته ربات', 'اتصال شبکه عصبی', 'همگام‌سازی حافظه بلندمدت', 'بارگذاری شخصیت فارسی‌زبان', 'تحلیل الگوهای رفتاری تو', 'کالیبره ماژول انگیزش', 'تست امنیت و حریم خصوصی', 'آماده‌به‌کار نهایی'],
        lines: () => {
          const habits = state.habits || [];
          const doneToday = habits.filter(h => h.completions && h.completions[today()]).length;
          return [
            'بوت کردن مغز دیجیتال...',
            'اتصال به شبکه عصبی مرکزی... ✓',
            'شناسایی ' + toPersian(habits.length) + ' عادت فعال... ✓',
            'بارگذاری مدل زبانی فارسی... ✓',
            'پیشرفت امروز: ' + toPersian(doneToday) + ' از ' + toPersian(habits.length),
            'همگام‌سازی حافظه کوتاه و بلندمدت... ✓',
            'روشن‌کردن ماژول انگیزه و شوخ‌طبعی... ✓',
            'رمزگذاری حریم خصوصی... ✓',
            'قفل گشوده شد — دستیار آماده است ✓'
          ];
        }
      },
      home: {
        title: 'هسته خانه و روز جدید', tagTL: 'روز: امیدبخش', accent: '#a78bfa', accent2: '#22d3ee',
        motto: 'خانه آماده است — امروز را فتح کن ☀️',
        open: () => { try { renderAll(); showToast('روز جدید روشن شد ☀️'); } catch (e) {} },
        phases: ['بیدارکردن خانه هوشمند', 'خواندن حافظه روزهای قبل', 'چیدن عادت‌های امروز', 'روشن‌کردن زنجیره استریک', 'محاسبه ارتفاع کوه پیشرفت', 'هماهنگی انگیزه‌سنج', 'تنظیم نور امید', 'مرور بازتاب دیروز', 'آماده‌سازی روز جدید'],
        lines: () => {
          const habits = state.habits || [];
          const done = habits.filter(h => h.completions && h.completions[today()]).length;
          const streak = state.habits ? Math.max(0, ...habits.map(h => h.streak || 0)) : 0;
          const moods = (state.moodLog || []).length;
          return [
            'بیدارکردن هسته خانه...',
            'بارگذاری روزهای گذشته از حافظه... ✓',
            'چیدن ' + toPersian(habits.length) + ' عادت برای امروز... ✓',
            'بررسی زنجیره: بهترین ' + toPersian(streak) + ' روز پیوسته 🔥',
            'انرژی ثبت‌شده تا امروز: ' + toPersian(moods) + ' بازتاب',
            done > 0 ? 'کارهای امروز شروع شده: ' + toPersian(done) + ' ✓' : 'صبحت بخیر — امروز صفحه سفیدی برای شروع داری ✨',
            'کالیبره‌کردن انگیزه‌سنج...',
            'نور امید روی بیشینه...',
            'خانه آماده است ✓'
          ];
        }
      },
      mountain: {
        title: 'سامانه کوه و قله', tagTL: 'ارتفاع‌سنج: فعال', accent: '#34d399', accent2: '#8b5cf6',
        motto: 'کوه‌ها آماده‌اند — قدم بعدی رو بزن 🏔️',
        open: () => { try { openModal('mountainModal'); } catch (e) {} },
        phases: ['فعال‌سازی ارتفاع‌سنج', 'بررسی هوا و مسیر صعود', 'شمردن کمپ‌های هر کوه', 'بارگذاری نقشه قله‌ها', 'محاسبه شیب پیشرفت', 'بازبینی روزهای اردو', 'چک‌لیست تجهیزات صعود', 'قفل‌گشایی مسیرهای فتح‌شده', 'اعلام وضعیت صعود'],
        lines: () => {
          const habits = state.habits || [];
          const conquered = habits.filter(h => (h.streak || 0) >= (h.duration || 21)).length;
          const climbing = habits.length - conquered;
          return [
            'روشن‌کردن ارتفاع‌سنج کوانتومی...',
            'اسکن ' + toPersian(habits.length) + ' کوه پیشرفت... ✓',
            conquered ? 'کوه‌های فتح‌شده: ' + toPersian(conquered) + ' 🏔️ ✓' : 'هنوز قله‌ای فتح نشده — اولین قدم منتظر است',
            climbing ? toPersian(climbing) + ' صعود فعال در جریان است...' : 'همه قله‌ها فتح شده‌اند!',
            'بررسی هوا: مناسب برای عادت‌های جدید ✓',
            'کمپ‌ها و پرچم‌ها نصب شد...',
            'نقشه مسیر قله ترسیم شد ✓',
            'تجهیزات صعود آماده...',
            'وضعیت: آماده صعود ✓'
          ];
        }
      },
      plus: {
        title: 'کارخانه ساخت عادت', tagTL: 'کارگاه: باز', accent: '#8b5cf6', accent2: '#34d399',
        motto: 'کارخانه روشن شد — عادت بعدی‌ات را بساز 🛠️',
        open: () => { try { openModal('addHabitModal'); } catch (e) {} },
        phases: ['روشن‌کردن کارخانه', 'بارگذاری قالب‌های عادت', 'کالیبره مدت‌های چالش', 'ترسیم مسیرهای قله', 'همگام‌سازی با صفحه کوه', 'فعال‌سازی یادآور هوشمند', 'تنظیم سخت‌گیر و مهربان', 'بازبینی پیشنهادهای شخصی', 'بازکردن درب کارگاه'],
        lines: () => [
          'روشن‌کردن کارخانه ساخت عادت...',
          'بارگذاری ۲۰+ قالب آماده... ✓',
          'کالیبره مدت‌ها: ۷ / ۲۱ / ۴۰ / ۷۰ / ۱۰۰ ✓',
          'ترسیم مسیر قله برای هر مدت... ✓',
          'اتصال به سامانه کوه... ✓',
          'یادآور هوشمند تنظیم شد ⏰ ✓',
          'پیشنهادهای شخصی بر اساس عادت‌های تو آماده شد',
          'تست کیفیت مسیر... ✓',
          'درب کارگاه باز شد ✓'
        ]
      },
      music: {
        title: 'استودیو موزیک', tagTL: 'استودیو: آماده', accent: '#34d399', accent2: '#f59e0b',
        motto: 'استودیو آماده است — آرامش را پخش کن 🎧',
        open: () => { try { openMusicPage(); } catch (e) {} },
        phases: ['روشن‌کردن استودیو', 'بارگذاری قفسه موزیک', 'کوک سازهای کلکسیون‌ها', 'آماده‌سازی آهنگساز هوشمند', 'تنظیم اکولایزر آرامش', 'فعال‌سازی پخش‌خودکار زمانی', 'کالیبره صدای محیطی', 'اتصال بلندگوهای مجازی', 'شمارش معکوس پخش'],
        lines: () => {
          const n = (state.musicTracks || []).length;
          const gens = [['آرامش', 24], ['تمرکز', 24], ['انرژی', 24], ['خواب', 18], ['طبیعت', 24], ['انگیزه', 18]];
          const gtotal = gens.reduce((a, g) => a + g[1], 0);
          return [
            'روشن‌کردن استودیو موزیک...',
            'بارگذاری قفسه: ' + toPersian(n) + ' موزیک شخصی ✓',
            'آهنگساز هوشمند آنلاین شد 🎼 ✓',
            toPersian(gtotal) + ' قطعه تولیدی در ۶ کلکسیون آماده است',
            'کلکسیون آرامش: ' + toPersian(24) + ' قطعه ✓',
            'کلکسیون تمرکز: ' + toPersian(24) + ' قطعه ✓',
            'اکولایزر روی حالت «آرامش ذهنی»...',
            'پخش‌خودکار زمانی فعال ⏰ ✓',
            'استودیو آماده پخش ✓'
          ];
        }
      },
      profile: {
        title: 'اتاق افتخارات', tagTL: 'افتخارات: در حال شمارش', accent: '#f59e0b', accent2: '#8b5cf6',
        motto: 'اتاق افتخارات باز شد — به خودت افتخار کن 🏆',
        open: () => { try { openModal('profileModal'); } catch (e) {} },
        phases: ['بازکردن درب اتاق افتخارات', 'تمیزکردن قاب مدال‌ها', 'شمردن روزهای پیوسته', 'بازخوانی داستان صعود تو', 'برق‌انداختن تندیس‌ها', 'محاسبه سطح و تجربه', 'بازبینی رکوردهای شخصی', 'چیدن افتخارات جدید', 'اعلام افتخار امروز'],
        lines: () => {
          const habits = state.habits || [];
          const ticks = habits.reduce((a, h) => a + Object.keys(h.completions || {}).length, 0);
          const best = habits.length ? Math.max(0, ...habits.map(h => h.streak || 0)) : 0;
          return [
            'بازکردن درب اتاق افتخارات...',
            'پرداخت تندیس‌های برنز تا الماس ✓',
            'شمارش تیک‌های تاریخ تو: ' + toPersian(ticks) + ' ✓',
            'بهترین استریک: ' + toPersian(best) + ' روز 🔥',
            'بازخوانی داستان صعود تو...',
            'محاسبه XP و سطح...',
            'برق‌انداختن ویترین ✓',
            'هدف بعدی در حال محاسبه...',
            'اتاق آماده بازدید است ✓'
          ];
        }
      }
    };

    function stopBootTimers() { bootTimers.forEach(clearTimeout); bootTimers = []; }

    function hideBootScreen(thenOpen) {
      stopBootTimers();
      const scr = document.getElementById('agentBootScreen');
      if (!scr || !scr.classList.contains('active')) {
        if (thenOpen) { const f = seqTargetOpen || (() => openAgentModalMaterialized()); seqTargetOpen = null; f(); }
        return;
      }
      scr.classList.remove('active');
      scr.classList.remove('boot-final');
      scr.classList.remove('boot-fast');
      bootActive = false;
      if (thenOpen) {
        const f = seqTargetOpen || (() => openAgentModalMaterialized());
        seqTargetOpen = null;
        setTimeout(() => { try { f(); } catch (e) {} }, 140);
      }
    }

    function openPageWithSequence(themeId) {
      const theme = SEQ_THEMES[themeId] || SEQ_THEMES.agent;
      if (bootActive) return;
      try {
        if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) { theme.open(); return; }
        bootActive = true;
        seqTargetOpen = theme.open;
        try { playBootSound(); } catch (e) {}
        const scr = document.getElementById('agentBootScreen');
        const term = document.getElementById('bootTerminal');
        const fill = document.getElementById('bootProgressFill');
        const pct = document.getElementById('bootPercent');
        const flash = document.getElementById('bootFlash');
        const status = document.getElementById('bootStatus');
        const eq = document.getElementById('bootEq');
        const rImg = document.getElementById('bootRobotImg');
        const tEl = document.getElementById('bootHudTitle');
        if (tEl) tEl.textContent = theme.title;
        scr.style.setProperty('--seq-a', theme.accent);
        scr.style.setProperty('--seq-b', theme.accent2);
        if (rImg) { try { rImg.src = ROBOT_AVATAR; } catch (e) {} }
        term.innerHTML = '';
        fill.style.width = '0%';
        pct.textContent = '۰٪';
        status.textContent = 'فاز ۱ از ۹ — ' + theme.phases[0];
        flash.classList.remove('fire');
        scr.classList.remove('boot-final', 'boot-fast');
        eq.classList.remove('on');
        if (!eq.childElementCount) {
          for (let i = 0; i < 13; i++) {
            const bar = document.createElement('span');
            bar.style.animationDelay = (-(Math.random() * 0.9)).toFixed(2) + 's';
            bar.style.animationDuration = (0.6 + Math.random() * 0.7).toFixed(2) + 's';
            eq.appendChild(bar);
          }
        }
        scr.classList.add('active');
        const LINES = theme.lines();
        const t0 = performance.now(), DUR = SEQ_DUR;
        const plateau = (v) => {
          if (v > 0.32 && v < 0.42) v = 0.32 + (v - 0.32) * 0.25;
          if (v > 0.70 && v < 0.80) v = 0.70 + (v - 0.70) * 0.25;
          return v;
        };
        const step = (t) => {
          if (!bootActive) return;
          const k = Math.min(1, (t - t0) / DUR);
          const eased = plateau(1 - Math.pow(1 - k, 1.2));
          const v = Math.round(eased * 100);
          fill.style.width = v + '%';
          pct.textContent = toPersian(v) + '٪';
          if (k < 1) requestAnimationFrame(step);
        };
        requestAnimationFrame(step);
        const NP = theme.phases.length;
        for (let i = 0; i < NP; i++) {
          bootTimers.push(setTimeout(() => {
            if (!bootActive) return;
            status.textContent = 'فاز ' + toPersian(i + 1) + ' از ' + toPersian(NP) + ' — ' + theme.phases[i];
          }, Math.round(i * DUR / NP)));
        }
        const lineStart = 3500, lineEnd = DUR - 4200, n = LINES.length;
        LINES.forEach((line, i) => {
          const at = lineStart + Math.round((lineEnd - lineStart) * (i / Math.max(1, n - 1)));
          bootTimers.push(setTimeout(() => {
            if (!bootActive) return;
            term.querySelectorAll('.cur').forEach(cc => cc.remove());
            const div = document.createElement('div');
            div.className = 'boot-line';
            div.innerHTML = line + ' <span class="cur"></span>';
            term.appendChild(div);
            while (term.childElementCount > 7) { try { term.removeChild(term.firstChild); } catch (e) { break; } }
          }, at));
        });
        bootTimers.push(setTimeout(() => { if (bootActive) eq.classList.add('on'); }, Math.round(DUR * 0.16)));
        bootTimers.push(setTimeout(() => { if (bootActive) scr.classList.add('boot-fast'); }, Math.round(DUR * 0.62)));
        bootTimers.push(setTimeout(() => { if (bootActive) scr.classList.add('boot-final'); }, Math.round(DUR * 0.87)));
        bootTimers.push(setTimeout(() => {
          if (!bootActive) return;
          term.querySelectorAll('.cur').forEach(cc => cc.remove());
          const ok = document.createElement('div');
          ok.className = 'boot-line ok';
          ok.textContent = '✅ ' + theme.motto;
          term.appendChild(ok);
        }, Math.round(DUR * 0.94)));
        bootTimers.push(setTimeout(() => { if (bootActive) flash.classList.add('fire'); }, Math.round(DUR * 0.975)));
        bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, DUR - 150));
        bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, DUR + 8000));
      } catch (e) {
        bootActive = false;
        stopBootTimers();
        try { theme.open(); } catch (e2) {}
      }
    }

    function openAgentWithBoot() { openPageWithSequence('agent'); }

    document.getElementById('agentBootScreen').addEventListener('pointerdown', () => hideBootScreen(true));'''

ENGINE = ENGINE.replace('__B64__', b64)
src = src[:blk_start] + ENGINE + src[blk_end:]
print('OK  [A5.engine] sequence engine replaced')

# ---------- A6) offline AI engine + hybrid sendAgentMessage ----------
anchor = '    async function sendAgentMessage(text) {'
OFFLINE = r'''    // ================= TASK 18: OFFLINE AI ENGINE (works on phone / file://) =================
    function offlineAgentIntent(msg) {
      const m = (msg || '').toLowerCase();
      const has = (...ws) => ws.some(w => m.indexOf(w) !== -1);
      if (has('سلام', 'درود', 'هی', 'hello', 'hi')) return 'greet';
      if (has('انگیزه', 'دلسرد', 'خسته', 'نمی‌توانم', 'نمیتوانم', 'نمی تونم', 'بی‌حال', 'بیحال', 'ماندم')) return 'motivate';
      if (has('برنامه', 'عادت جدید', 'روتین', 'بساز', 'طراحی کن', 'پیشنهاد عادت')) return 'plan';
      if (has('استریک', 'آمار', 'پیشرفت', 'گزارش', 'چند روز', 'وضعیت')) return 'stats';
      if (has('اینستاگرام', 'سوشال', 'شبکه اجتماعی', 'لینکدین', 'پست')) return 'social';
      if (has('موزیک', 'آهنگ', 'موسیقی', 'آرامش صوتی')) return 'music';
      if (has('حالم', 'احساس', 'غم', 'افسرده', 'اضطراب', 'استرس')) return 'mood';
      if (has('تشکر', 'ممنون', 'مرسی')) return 'thanks';
      if (has('تو کی', 'کی هستی', 'توسعه‌دهنده', 'سازنده', 'درباره تو')) return 'about';
      return 'fallback';
    }

    function offlineAgentStatsText() {
      const habits = state.habits || [];
      const doneToday = habits.filter(h => h.completions && h.completions[today()]).length;
      const best = habits.length ? Math.max(0, ...habits.map(h => h.streak || 0)) : 0;
      const ticks = habits.reduce((a, h) => a + Object.keys(h.completions || {}).length, 0);
      return '📊 گزارش لحظه‌ای تو:\n• عادت‌های فعال: ' + toPersian(habits.length) + '\n• امروز: ' + toPersian(doneToday) + ' از ' + toPersian(habits.length) + ' تکمیل شده\n• بهترین استریک: ' + toPersian(best) + ' روز 🔥\n• کل تیک‌های تاریخ: ' + toPersian(ticks) + '\n\nهر عدد از این‌ها یک قله فتح‌شده است!';
    }

    function offlineAgentPlanFor(msg) {
      const m = (msg || '').toLowerCase();
      const has = (...ws) => ws.some(w => m.indexOf(w) !== -1);
      const P = (name, icon, cat, time) => ({ name, icon, category: cat, alarmTime: time });
      const bank = [];
      if (has('ورزش', 'باشگاه', 'بدنسازی', 'دویدن', 'حرکت')) bank.push(P('۱۰ دقیقه حرکت و نرمش', '🏃', 'productivity', '07:00'), P('پیاده‌روی روزانه', '🚶', 'productivity', '18:00'));
      if (has('مطالعه', 'کتاب', 'درس', 'یادگیری')) bank.push(P('۱۵ دقیقه مطالعه کتاب', '📚', 'productivity', '21:00'), P('مرور جزوه یا یادداشت', '📝', 'productivity', '20:00'));
      if (has('آب', 'نوشیدن', 'هیدرات')) bank.push(P('۸ لیوان آب', '💧', 'self-care', '09:00'));
      if (has('خواب', 'بیدار', 'صبح', 'سحرخیز')) bank.push(P('خواب سر ساعت ۲۳', '😴', 'self-care', '22:30'), P('بیدارباش بدون چرت‌زدن', '🌅', 'self-care', '06:30'));
      if (has('مدیتیشن', 'آرامش', 'تنفس', 'ذهن')) bank.push(P('۵ دقیقه تنفس آرام', '🧘', 'self-care', '08:00'));
      if (has('اینستاگرام', 'سوشال', 'شبکه اجتماعی', 'پست', 'لینکدین')) bank.push(P('۳۰ دقیقه ساخت محتوا', '🎬', 'productivity', '17:00'), P('ساعت طلایی بدون موبایل', '📵', 'self-care', '21:00'));
      if (has('زبان', 'انگلیسی', 'لغت')) bank.push(P('۱۰ لغت جدید انگلیسی', '🗣️', 'productivity', '19:00'));
      if (has('کار', 'پروژه', 'تمرکز')) bank.push(P('۹۰ دقیقه تمرکز عمیق', '🎯', 'productivity', '10:00'));
      if (!bank.length) bank.push(P('۵ دقیقه تنفس آرام', '🧘', 'self-care', '08:00'), P('۱۵ دقیقه مطالعه کتاب', '📚', 'productivity', '21:00'), P('۸ لیوان آب', '💧', 'self-care', '09:00'), P('پیاده‌روی روزانه', '🚶', 'productivity', '18:00'));
      const uniq = []; const seen = {};
      bank.forEach(h => { if (!seen[h.name]) { seen[h.name] = 1; uniq.push(h); } });
      const planHabits = uniq.slice(0, 4);
      const names = ['پرواز اول', 'پلکان صعود', 'نسیم تازه', 'مسیر قله', 'ستاره راهنما', 'قدم‌های محکم'];
      return {
        name: names[Math.floor(Math.random() * names.length)],
        duration: 21,
        habits: planHabits
      };
    }

    function offlineAgentReply(msg) {
      const intent = offlineAgentIntent(msg);
      const habits = state.habits || [];
      const doneToday = habits.filter(h => h.completions && h.completions[today()]).length;
      const best = habits.length ? Math.max(0, ...habits.map(h => h.streak || 0)) : 0;
      if (intent === 'greet') {
        return { reply: 'سلام رفیق! 👋 من اینجا هستم تا هر روز کنارت باشم.\nالان ' + toPersian(doneToday) + ' از ' + toPersian(habits.length) + ' عادت امروزت انجام شده.\n\nمی‌خواهی برنامه جدید بسازیم، گزارش بگیری یا فقط انگیزه بگیری؟' };
      }
      if (intent === 'motivate') {
        const quotes = ['قله‌ها را قدم‌به‌قدم فتح می‌کنند 🏔️', 'روزهای سخت، استریک‌های طلایی می‌سازند ✨', 'تو فقط به قدم بعدی نیاز داری، نه به یک جهش 🚀'];
        return { reply: 'شنیدم حالت خوب نیست... طبیعیه، مسیر صعود همیشه سربالایی نیست 🌤️\n\nبهترین استریک تو تا حالا ' + toPersian(best) + ' روز بوده — این یعنی تو توانش را داری.\n\n' + quotes[Math.floor(Math.random() * quotes.length)] + '\n\nپیشنهاد: فقط یکی از عادت‌های سبک را امروز تیک بزن، بقیه‌اش خودش می‌آید 💪' };
      }
      if (intent === 'plan') {
        const plan = offlineAgentPlanFor(msg);
        return { reply: 'برنامه «' + plan.name + '» را بر اساس حرف‌هایت طراحی کردم 🛠️\nشامل ' + toPersian(plan.habits.length) + ' عادت برای یک چالش ' + toPersian(plan.duration) + ' روزه با مسیر قله مشخص.\n\nاگر دکمه اعمال را بزنی، مستقیم به روزهایت اضافه می‌شود — مسیر قله‌اش هم در صفحه کوه رسم می‌شود! 🏔️', plan: plan };
      }
      if (intent === 'stats') return { reply: offlineAgentStatsText() };
      if (intent === 'social') {
        return { reply: 'برای شبکه اجتماعی‌کردن، بخش «برنامه‌ساز شبکه اجتماعی» در همین صفحه را ببین — می‌توانی حوزه‌ات (هوش مصنوعی، برنامه‌نویسی، آموزش...) را انتخاب کنی تا یک برنامه انتشار محتوا برایت بچینم 🎬', plan: offlineAgentPlanFor('اینستاگرام پست محتوا') };
      }
      if (intent === 'music') {
        return { reply: '🎧 کلکسیون‌های تولیدی من آماده‌اند: آرامش (۲۴ قطعه)، تمرکز (۲۴)، انرژی (۲۴)، خواب (۱۸)، طبیعت (۲۴) و انگیزه (۱۸).\n\nبه کتابخانه موزیک برو و «آرامش» را باز کن — قطعه‌ها همین‌جا ساخته می‌شوند، بدون اینترنت!' };
      }
      if (intent === 'mood') {
        return { reply: 'حالت تو برایم مهم است 💜\nهمین حالا «حال و بازتاب امروز» را ثبت کن — حتی دو خط کوتاه.\nبعداً نمودار ۷ روزه نشان می‌دهد کدام عادت‌ها حالت را بهتر کرده‌اند.\n\nیادت باشد: احساسات هم مثل آب‌وهواست، می‌گذرد 🌈' };
      }
      if (intent === 'thanks') return { reply: 'خواهش می‌کنم رفیق! 🙏 من همیشه همین‌جاام. حالا برو و آن تیک امروزم را بزن 😉' };
      if (intent === 'about') return { reply: 'من دستیار هوشمند این اپ هستم 🤖\nاین برنامه را غدیر سروری (Ghadir Sarvari) ساخته — با عشق برای ساختن روزهای بهتر.\n\nمن کاملاً آفلاین کار می‌کنم؛ همه حرف‌هایت فقط روی همین گوشی می‌ماند 🔒' };
      return { reply: 'می‌توانم این کارها را برایت بکنم:\n\n• 📊 «گزارش بده» — آمار و استریک‌هایت\n• 🛠️ «برنامه بساز برای ورزش/مطالعه/خواب...» — برنامه عادت آماده\n• 🔥 «انگیزه بده» — کمی سوخت برای ادامه\n• 🎧 «موزیک آرامش» — پیشنهاد قطعه\n• 💜 «حالم خوب نیست» — همدلی و راه‌حل\n\nکدام را می‌خواهی؟' };
    }

'''
src = replace_once(src, anchor, OFFLINE + anchor, 'A6a.offline-fn')

# hybrid fetch: server if http(s), else offline engine
old_fetch = """        const res = await fetch('/api/agent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: msg,
            history: history,
            context: getAgentContext()
          })
        });
        if (!res.ok) throw new Error('HTTP ' + res.status);
        const data = await res.json();"""
new_fetch = """        const canHTTP = location.protocol === 'http:' || location.protocol === 'https:';
        let data = null;
        if (canHTTP) {
          try {
            const res = await fetch('/api/agent', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                message: msg,
                history: history,
                context: getAgentContext()
              })
            });
            if (res.ok) data = await res.json();
          } catch (netErr) { data = null; }
        }
        if (!data) {
          await new Promise(r => setTimeout(r, 700 + Math.random() * 900));
          data = offlineAgentReply(msg);
        }"""
src = replace_once(src, old_fetch, new_fetch, 'A6b.hybrid')

# friendlier offline error text
src = replace_once(src,
  "pushAgentMessage('agent', 'اوپس! ارتباط با مغز هوشمندم برقرار نشد 📡 لطفاً چند لحظه بعد دوباره امتحان کن.');",
  "pushAgentMessage('agent', 'اوپس! یک لحظه مغزم قفل کرد 📡 دوباره امتحان کن — اگر اینترنت هم نباشد، مغز محلی‌ام جواب می‌دهد.');",
  'A6c.errtxt')

# ---------- A7) nav rewiring ----------
src = replace_once(src,
  '<button onclick="openModal(\'profileModal\')" aria-label="پروفایل" class="w-10 h-10 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface-variant active:scale-90 transition-transform">',
  '<button onclick="openPageWithSequence(\'profile\')" aria-label="پروفایل" class="w-10 h-10 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface-variant active:scale-90 transition-transform">',
  'A7a.header-profile')
src = replace_once(src,
  '<button class="flex-1 flex flex-col items-center gap-1 active:scale-90 transition-transform nav-btn" onclick="openModal(\'mountainModal\')">',
  '<button class="flex-1 flex flex-col items-center gap-1 active:scale-90 transition-transform nav-btn" onclick="openPageWithSequence(\'mountain\')">',
  'A7b.nav-mountain')
src = replace_once(src,
  '<button onclick="openModal(\'addHabitModal\')" class="relative w-14 h-14 rounded-full',
  '<button onclick="openPageWithSequence(\'plus\')" class="relative w-14 h-14 rounded-full',
  'A7c.nav-plus')
src = replace_once(src,
  '<button class="flex-1 flex flex-col items-center gap-1 active:scale-90 transition-transform nav-btn" onclick="openMusicPage()">',
  '<button class="flex-1 flex flex-col items-center gap-1 active:scale-90 transition-transform nav-btn" onclick="openPageWithSequence(\'music\')">',
  'A7d.nav-music')
src = replace_once(src,
  '<button class="flex-1 flex flex-col items-center gap-1 active:scale-90 transition-transform nav-btn" onclick="openModal(\'profileModal\')">',
  '<button class="flex-1 flex flex-col items-center gap-1 active:scale-90 transition-transform nav-btn" onclick="openPageWithSequence(\'profile\')">',
  'A7e.nav-profile')
src = replace_once(src,
  '''<div class="w-9 h-9 rounded-xl bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-primary font-bold text-lg">
          <span class="material-symbols-outlined text-[20px]">mountain_flag</span>
        </div>''',
  '''<div onclick="openPageWithSequence('home')" role="button" title="سکانس خانه" class="w-9 h-9 rounded-xl bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-primary font-bold text-lg cursor-pointer active:scale-90 transition-transform">
          <span class="material-symbols-outlined text-[20px]">mountain_flag</span>
        </div>''',
  'A7f.header-logo-home')

io.open(APP, 'w', encoding='utf-8').write(src)
print('DONE patch A: %d -> %d chars (+%d)' % (orig_len, len(src), len(src) - orig_len))
