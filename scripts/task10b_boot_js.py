# -*- coding: utf-8 -*-
"""Task 10 (part B): JS — longer multi-phase boot timeline + materialize transition."""
import sys

PATH = '/home/z/my-project/public/app.html'

with open(PATH, encoding='utf-8') as f:
    c = f.read()

def sub_once(content, old, new, name):
    n = content.count(old)
    assert n == 1, f'ABORT [{name}]: expected 1 occurrence, found {n}'
    print(f'OK  {name}')
    return content.replace(old, new, 1)

# ---------- safety ----------
assert 'openAgentWithBoot' in c and 'playBootSound' in c, 'task9 JS missing'
assert 'buildBootLines' not in c, 'task10b already applied'

# ============ 1) BOOT_LINES -> buildBootLines() ============
OLD_A = '''    // ================= AGENT BOOT SCREEN (CINEMATIC ROBOT) =================
    const BOOT_LINES = [
      'در حال برقراری اتصال عصبی...',
      'بارگذاری مغز دیجیتال...',
      'کالیبره‌سازی مدل زبانی...',
      'همگام‌سازی حافظه عادت‌ها...'
    ];
    let bootTimers = [];
    let bootActive = false;'''
NEW_A = '''    // ================= AGENT BOOT SCREEN (CINEMATIC ROBOT — LONG CUT) =================
    function buildBootLines() {
      const habits = state.habits || [];
      const n = habits.length;
      const doneToday = habits.filter(h => h.completions && h.completions[today()]).length;
      return [
        'اتصال به شبکه عصبی مرکزی...',
        `شناسایی ${toPersian(n)} عادت فعال...`,
        'بارگذاری مغز دیجیتال...',
        'کالیبره‌سازی مدل زبانی فارسی...',
        'همگام‌سازی حافظه بلندمدت...',
        'تحلیل الگوهای رفتاری تو...',
        'فعال‌سازی ماژول انگیزش...',
        `بررسی پیشرفت امروز: ${toPersian(doneToday)} از ${toPersian(n)} عادت`,
        'آخرین بررسی امنیتی...'
      ];
    }
    let bootTimers = [];
    let bootActive = false;'''
c = sub_once(c, OLD_A, NEW_A, 'boot lines builder')

# ============ 2) playBootSound: extended 5-layer cinematic sound ============
OLD_B = '''    function playBootSound() {
      try {
        if (state.settings.batterySaver) return;
        initAudio();
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(760, now + 0.9);
        g.gain.setValueAtTime(0.0001, now);
        g.gain.exponentialRampToValueAtTime(0.06, now + 0.25);
        g.gain.exponentialRampToValueAtTime(0.0001, now + 1.1);
        osc.connect(g); g.connect(masterGain);
        osc.start(now); osc.stop(now + 1.15);
        [880, 1174.66].forEach((f, i) => {
          const o2 = audioCtx.createOscillator();
          const g2 = audioCtx.createGain();
          o2.type = 'triangle'; o2.frequency.value = f;
          const t0 = now + 1.9 + i * 0.14;
          g2.gain.setValueAtTime(0.0001, t0);
          g2.gain.exponentialRampToValueAtTime(0.05, t0 + 0.02);
          g2.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.22);
          o2.connect(g2); g2.connect(masterGain);
          o2.start(t0); o2.stop(t0 + 0.25);
        });
      } catch (e) { /* silent */ }
    }'''
NEW_B = '''    function playBootSound() {
      try {
        if (state.settings.batterySaver) return;
        initAudio();
        const now = audioCtx.currentTime;
        // 1) deep reactor swell
        const sub = audioCtx.createOscillator();
        const subG = audioCtx.createGain();
        sub.type = 'sine';
        sub.frequency.setValueAtTime(55, now);
        sub.frequency.exponentialRampToValueAtTime(190, now + 1.6);
        subG.gain.setValueAtTime(0.0001, now);
        subG.gain.exponentialRampToValueAtTime(0.05, now + 0.5);
        subG.gain.exponentialRampToValueAtTime(0.0001, now + 1.9);
        sub.connect(subG); subG.connect(masterGain);
        sub.start(now); sub.stop(now + 2);
        // 2) rising power sweep
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(180, now);
        osc.frequency.exponentialRampToValueAtTime(760, now + 1.1);
        g.gain.setValueAtTime(0.0001, now);
        g.gain.exponentialRampToValueAtTime(0.045, now + 0.35);
        g.gain.exponentialRampToValueAtTime(0.0001, now + 1.35);
        osc.connect(g); g.connect(masterGain);
        osc.start(now); osc.stop(now + 1.4);
        // 3) ready beeps
        [880, 1174.66].forEach((f, i) => {
          const o2 = audioCtx.createOscillator();
          const g2 = audioCtx.createGain();
          o2.type = 'triangle'; o2.frequency.value = f;
          const t0 = now + 2.35 + i * 0.16;
          g2.gain.setValueAtTime(0.0001, t0);
          g2.gain.exponentialRampToValueAtTime(0.05, t0 + 0.02);
          g2.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.24);
          o2.connect(g2); g2.connect(masterGain);
          o2.start(t0); o2.stop(t0 + 0.27);
        });
        // 4) final rising arpeggio
        [659.25, 830.61, 987.77].forEach((f, i) => {
          const o3 = audioCtx.createOscillator();
          const g3 = audioCtx.createGain();
          o3.type = 'triangle'; o3.frequency.value = f;
          const t0 = now + 4.75 + i * 0.12;
          g3.gain.setValueAtTime(0.0001, t0);
          g3.gain.exponentialRampToValueAtTime(0.045, t0 + 0.02);
          g3.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.3);
          o3.connect(g3); g3.connect(masterGain);
          o3.start(t0); o3.stop(t0 + 0.33);
        });
        // 5) ready chord on flash
        [523.25, 659.25].forEach((f) => {
          const o4 = audioCtx.createOscillator();
          const g4 = audioCtx.createGain();
          o4.type = 'sine'; o4.frequency.value = f;
          const t0 = now + 5.32;
          g4.gain.setValueAtTime(0.0001, t0);
          g4.gain.exponentialRampToValueAtTime(0.05, t0 + 0.04);
          g4.gain.exponentialRampToValueAtTime(0.0001, t0 + 0.85);
          o4.connect(g4); g4.connect(masterGain);
          o4.start(t0); o4.stop(t0 + 0.9);
        });
      } catch (e) { /* silent */ }
    }'''
c = sub_once(c, OLD_B, NEW_B, 'extended boot sound')

# ============ 3) hideBootScreen + materialized opener ============
OLD_C = '''    function hideBootScreen(thenOpen) {
      stopBootTimers();
      const scr = document.getElementById('agentBootScreen');
      if (!scr || !scr.classList.contains('active')) {
        if (thenOpen) openModal('agentModal');
        return;
      }
      scr.classList.remove('active');
      bootActive = false;
      if (thenOpen) setTimeout(() => openModal('agentModal'), 140);
    }'''
NEW_C = '''    function openAgentModalMaterialized() {
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

    function hideBootScreen(thenOpen) {
      stopBootTimers();
      const scr = document.getElementById('agentBootScreen');
      if (!scr || !scr.classList.contains('active')) {
        if (thenOpen) openAgentModalMaterialized();
        return;
      }
      scr.classList.remove('active');
      scr.classList.remove('boot-final');
      bootActive = false;
      if (thenOpen) setTimeout(() => openAgentModalMaterialized(), 140);
    }'''
c = sub_once(c, OLD_C, NEW_C, 'materialize transition')

# ============ 4) openAgentWithBoot: 5-phase long timeline ============
OLD_D = '''    function openAgentWithBoot() {
      if (bootActive) return;
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        openModal('agentModal');
        return;
      }
      bootActive = true;
      playBootSound();
      const scr = document.getElementById('agentBootScreen');
      const term = document.getElementById('bootTerminal');
      const fill = document.getElementById('bootProgressFill');
      const pct = document.getElementById('bootPercent');
      const flash = document.getElementById('bootFlash');
      term.innerHTML = '';
      fill.style.width = '0%';
      pct.textContent = '۰٪';
      flash.classList.remove('fire');
      scr.classList.add('active');
      const t0 = performance.now(), DUR = 2150;
      const step = (t) => {
        if (!bootActive) return;
        const k = Math.min(1, (t - t0) / DUR);
        const eased = 1 - Math.pow(1 - k, 2.2);
        const v = Math.round(eased * 100);
        fill.style.width = v + '%';
        pct.textContent = toPersian(v) + '٪';
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      BOOT_LINES.forEach((line, i) => {
        bootTimers.push(setTimeout(() => {
          if (!bootActive) return;
          term.querySelectorAll('.cur').forEach(c => c.remove());
          const div = document.createElement('div');
          div.className = 'boot-line';
          div.innerHTML = line + ' <span class="cur"></span>';
          term.appendChild(div);
        }, 350 + i * 480));
      });
      bootTimers.push(setTimeout(() => {
        if (!bootActive) return;
        term.querySelectorAll('.cur').forEach(c => c.remove());
        const ok = document.createElement('div');
        ok.className = 'boot-line ok';
        ok.textContent = '✅ دستیار هوشمند آنلاین است';
        term.appendChild(ok);
      }, 350 + BOOT_LINES.length * 480 + 140));
      bootTimers.push(setTimeout(() => { if (bootActive) flash.classList.add('fire'); }, 2450));
      bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, 2680));
      bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, 4500));
    }'''
NEW_D = '''    function openAgentWithBoot() {
      if (bootActive) return;
      if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        openModal('agentModal');
        return;
      }
      bootActive = true;
      playBootSound();
      const scr = document.getElementById('agentBootScreen');
      const term = document.getElementById('bootTerminal');
      const fill = document.getElementById('bootProgressFill');
      const pct = document.getElementById('bootPercent');
      const flash = document.getElementById('bootFlash');
      const status = document.getElementById('bootStatus');
      const eq = document.getElementById('bootEq');
      term.innerHTML = '';
      fill.style.width = '0%';
      pct.textContent = '۰٪';
      status.textContent = 'فاز ۱ — انرژی‌رسانی هسته';
      flash.classList.remove('fire');
      scr.classList.remove('boot-final');
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
      const setPhase = (txt) => { if (bootActive) status.textContent = txt; };
      const LINES = buildBootLines();
      const t0 = performance.now(), DUR = 5250;
      const plateau = (v) => {
        if (v > 0.32 && v < 0.4) v = 0.32 + (v - 0.32) * 0.22;
        if (v > 0.68 && v < 0.76) v = 0.68 + (v - 0.68) * 0.22;
        return v;
      };
      const step = (t) => {
        if (!bootActive) return;
        const k = Math.min(1, (t - t0) / DUR);
        const eased = plateau(1 - Math.pow(1 - k, 1.25));
        const v = Math.round(eased * 100);
        fill.style.width = v + '%';
        pct.textContent = toPersian(v) + '٪';
        if (k < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      bootTimers.push(setTimeout(() => setPhase('فاز ۲ — متریالایز پوسته ربات'), 900));
      bootTimers.push(setTimeout(() => { if (bootActive) eq.classList.add('on'); }, 2050));
      bootTimers.push(setTimeout(() => setPhase('فاز ۳ — اتصال شبکه عصبی'), 2150));
      bootTimers.push(setTimeout(() => setPhase('فاز ۴ — همگام‌سازی حافظه'), 3550));
      LINES.forEach((line, i) => {
        bootTimers.push(setTimeout(() => {
          if (!bootActive) return;
          term.querySelectorAll('.cur').forEach(cc => cc.remove());
          const div = document.createElement('div');
          div.className = 'boot-line';
          div.innerHTML = line + ' <span class="cur"></span>';
          term.appendChild(div);
        }, 1150 + i * 430));
      });
      bootTimers.push(setTimeout(() => {
        if (!bootActive) return;
        scr.classList.add('boot-final');
        setPhase('فاز ۵ — آماده‌به‌کار نهایی');
      }, 4700));
      bootTimers.push(setTimeout(() => {
        if (!bootActive) return;
        term.querySelectorAll('.cur').forEach(cc => cc.remove());
        const ok = document.createElement('div');
        ok.className = 'boot-line ok';
        ok.textContent = '✅ دستیار هوشمند آنلاین است — خوش آمدی';
        term.appendChild(ok);
      }, 4820));
      bootTimers.push(setTimeout(() => { if (bootActive) flash.classList.add('fire'); }, 5300));
      bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, 5650));
      bootTimers.push(setTimeout(() => { if (bootActive) hideBootScreen(true); }, 9000));
    }'''
c = sub_once(c, OLD_D, NEW_D, 'long boot timeline')

# ---------- post checks ----------
assert 'BOOT_LINES' not in c, 'old BOOT_LINES leftover'
assert c.count('openAgentModalMaterialized') == 3, 'materialize hook count'
assert 'buildBootLines' in c and 'boot-final' in c

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(c)
print('SAVED', PATH)
