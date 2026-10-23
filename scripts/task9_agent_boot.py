# -*- coding: utf-8 -*-
"""Task 9: cinematic robot boot screen when tapping the AI assistant header icon.
Sequence: dark HUD scene -> robot head materializes -> eyes ignite -> rotating rings ->
terminal lines type out -> progress 0-100% -> flash -> agent modal opens. Tap = skip."""
import io, sys, shutil

PATH = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task9.bak'
src = io.open(PATH, encoding='utf-8').read()
shutil.copyfile(PATH, BAK)

edits = []

# ---------- 1) CSS ----------
css_block = """  /* ===== AGENT BOOT SCREEN (cinematic robot) ===== */
  #agentBootScreen { position: fixed; inset: 0; z-index: 65; background: radial-gradient(ellipse at 50% 42%, #1b1147 0%, #0d0722 52%, #050310 100%); display: flex; align-items: center; justify-content: center; opacity: 0; pointer-events: none; transition: opacity 0.35s ease; cursor: pointer; }
  #agentBootScreen.active { opacity: 1; pointer-events: auto; }
  .boot-grid-bg { position: absolute; inset: 0; background-image: linear-gradient(rgba(139,92,246,0.08) 1px, transparent 1px), linear-gradient(90deg, rgba(139,92,246,0.08) 1px, transparent 1px); background-size: 44px 44px; -webkit-mask-image: radial-gradient(ellipse at center, black 28%, transparent 74%); mask-image: radial-gradient(ellipse at center, black 28%, transparent 74%); animation: bootGridMove 8s linear infinite; }
  @keyframes bootGridMove { from { background-position: 0 0; } to { background-position: 0 44px; } }
  .boot-corner { position: absolute; width: 44px; height: 44px; border: 2px solid rgba(34,211,238,0.45); }
  .boot-c-tl { top: 22px; left: 22px; border-right: none; border-bottom: none; border-radius: 14px 0 0 0; }
  .boot-c-tr { top: 22px; right: 22px; border-left: none; border-bottom: none; border-radius: 0 14px 0 0; }
  .boot-c-bl { bottom: 22px; left: 22px; border-right: none; border-top: none; border-radius: 0 0 0 14px; }
  .boot-c-br { bottom: 22px; right: 22px; border-left: none; border-top: none; border-radius: 0 0 14px 0; }
  .boot-center { position: relative; display: flex; flex-direction: column; align-items: center; gap: 16px; width: min(320px, 84vw); }
  .boot-orbiter { position: relative; width: 186px; height: 186px; display: flex; align-items: center; justify-content: center; }
  .boot-ring { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible; }
  .boot-ring-a { animation: bootSpin 7s linear infinite; }
  .boot-ring-b { animation: bootSpinRev 4.2s linear infinite; }
  @keyframes bootSpin { to { transform: rotate(360deg); } }
  @keyframes bootSpinRev { to { transform: rotate(-360deg); } }
  .boot-head-wrap { position: relative; width: 116px; height: 116px; }
  .boot-head { width: 100%; height: 100%; animation: bootHeadIn 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) both; }
  @keyframes bootHeadIn { from { opacity: 0; transform: scale(0.55); filter: blur(6px); } to { opacity: 1; transform: scale(1); filter: blur(0) drop-shadow(0 0 16px rgba(34,211,238,0.35)); } }
  .boot-eye { opacity: 0; animation: bootEyeOn 0.5s steps(2, jump-none) 0.85s forwards, bootEyeGlow 2.2s ease-in-out 1.45s infinite; }
  @keyframes bootEyeOn { 0% { opacity: 0; } 40% { opacity: 1; } 55% { opacity: 0.15; } 100% { opacity: 1; } }
  @keyframes bootEyeGlow { 0%, 100% { filter: drop-shadow(0 0 3px rgba(34,211,238,0.75)); } 50% { filter: drop-shadow(0 0 9px rgba(34,211,238,1)); } }
  .boot-antenna { animation: bootAntBlink 1s ease-in-out 1s infinite; }
  @keyframes bootAntBlink { 0%, 100% { opacity: 1; } 50% { opacity: 0.25; } }
  .boot-scanline { position: absolute; left: 6px; right: 6px; top: 8%; height: 3px; border-radius: 3px; background: linear-gradient(90deg, transparent, rgba(34,211,238,0.85), transparent); opacity: 0; animation: bootScan 1.6s ease-in-out 1s infinite; }
  @keyframes bootScan { 0% { top: 8%; opacity: 0; } 12% { opacity: 1; } 88% { opacity: 1; } 100% { top: 88%; opacity: 0; } }
  .boot-terminal { direction: rtl; text-align: right; width: 100%; min-height: 88px; font-size: 12px; font-weight: 600; color: #7fe7f4; display: flex; flex-direction: column; gap: 5px; }
  .boot-line { opacity: 0; animation: bootLineIn 0.25s ease forwards; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .boot-line.ok { color: #6ee7b7; font-weight: 800; }
  .boot-line .cur { display: inline-block; width: 7px; height: 12px; background: #22d3ee; margin-right: 4px; vertical-align: -1px; animation: bootCursor 0.7s steps(1) infinite; }
  @keyframes bootCursor { 50% { opacity: 0; } }
  @keyframes bootLineIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: none; } }
  .boot-progress-track { width: 100%; height: 6px; border-radius: 999px; background: rgba(139,92,246,0.18); overflow: hidden; border: 1px solid rgba(139,92,246,0.35); }
  .boot-progress-fill { height: 100%; width: 0%; border-radius: 999px; background: linear-gradient(90deg, #8b5cf6, #22d3ee); box-shadow: 0 0 12px rgba(34,211,238,0.6); }
  .boot-percent { font-size: 13px; font-weight: 800; color: #a5f3fc; letter-spacing: 1px; }
  .boot-skip-hint { position: absolute; bottom: 32px; left: 0; right: 0; text-align: center; font-size: 11px; color: rgba(226,232,240,0.45); font-weight: 600; }
  .boot-flash { position: absolute; inset: 0; background: radial-gradient(circle at center, rgba(34,211,238,0.5), rgba(139,92,246,0.22) 45%, transparent 70%); opacity: 0; pointer-events: none; }
  .boot-flash.fire { animation: bootFlashFire 0.5s ease forwards; }
  @keyframes bootFlashFire { 0% { opacity: 0; } 30% { opacity: 1; } 100% { opacity: 0; } }

  </style>
</head>"""

edits.append(("""  </style>
</head>""", css_block))

# ---------- 2) HTML (before MODALS comment) ----------
html_block = """  <!-- ================= AGENT BOOT SCREEN (CINEMATIC ROBOT) ================= -->
  <div id="agentBootScreen" aria-hidden="true">
    <div class="boot-grid-bg"></div>
    <div class="boot-corner boot-c-tl"></div><div class="boot-corner boot-c-tr"></div>
    <div class="boot-corner boot-c-bl"></div><div class="boot-corner boot-c-br"></div>
    <div class="boot-center">
      <div class="boot-orbiter">
        <svg class="boot-ring boot-ring-a" viewBox="0 0 200 200" aria-hidden="true">
          <circle cx="100" cy="100" r="92" fill="none" stroke="rgba(34,211,238,0.35)" stroke-width="1.5" stroke-dasharray="10 14"/>
          <circle cx="100" cy="100" r="78" fill="none" stroke="rgba(139,92,246,0.45)" stroke-width="1" stroke-dasharray="3 9"/>
        </svg>
        <svg class="boot-ring boot-ring-b" viewBox="0 0 200 200" aria-hidden="true">
          <circle cx="100" cy="100" r="86" fill="none" stroke="rgba(34,211,238,0.3)" stroke-width="2.5" stroke-dasharray="46 260" stroke-linecap="round"/>
          <circle cx="100" cy="8" r="3.5" fill="#22d3ee"/>
        </svg>
        <div class="boot-head-wrap">
          <svg class="boot-head" viewBox="0 0 120 120" aria-hidden="true">
            <defs>
              <linearGradient id="bootGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#22d3ee"/>
                <stop offset="1" stop-color="#8b5cf6"/>
              </linearGradient>
            </defs>
            <line x1="60" y1="13" x2="60" y2="24" stroke="url(#bootGrad)" stroke-width="3" stroke-linecap="round"/>
            <circle class="boot-antenna" cx="60" cy="9" r="4" fill="#22d3ee"/>
            <rect x="26" y="24" width="68" height="60" rx="18" fill="rgba(34,211,238,0.07)" stroke="url(#bootGrad)" stroke-width="2.5"/>
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
      <div class="boot-terminal" id="bootTerminal"></div>
      <div class="boot-progress-track"><div class="boot-progress-fill" id="bootProgressFill"></div></div>
      <div class="boot-percent" id="bootPercent">۰٪</div>
    </div>
    <div class="boot-skip-hint">برای رد کردن، لمس کن</div>
    <div class="boot-flash" id="bootFlash"></div>
  </div>

  <!-- ================= MODALS ================= -->"""

edits.append(("""  <!-- ================= MODALS ================= -->""", html_block))

# ---------- 3) Header button -> boot flow ----------
edits.append((
    """<button onclick="openModal('agentModal')" aria-label="دستیار هوشمند" class="relative w-10 h-10 rounded-full bg-gradient-to-br from-agent-primary/20 to-agent-secondary/20 border border-agent-primary/30 flex items-center justify-center text-agent-primary active:scale-90 transition-transform">""",
    """<button onclick="openAgentWithBoot()" aria-label="دستیار هوشمند" class="relative w-10 h-10 rounded-full bg-gradient-to-br from-agent-primary/20 to-agent-secondary/20 border border-agent-primary/30 flex items-center justify-center text-agent-primary active:scale-90 transition-transform">"""))

# ---------- 4) JS engine (before serviceWorker block) ----------
js_block = """    // ================= AGENT BOOT SCREEN (CINEMATIC ROBOT) =================
    const BOOT_LINES = [
      'در حال برقراری اتصال عصبی...',
      'بارگذاری مغز دیجیتال...',
      'کالیبره‌سازی مدل زبانی...',
      'همگام‌سازی حافظه عادت‌ها...'
    ];
    let bootTimers = [];
    let bootActive = false;

    function playBootSound() {
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
    }

    function stopBootTimers() { bootTimers.forEach(clearTimeout); bootTimers = []; }

    function hideBootScreen(thenOpen) {
      stopBootTimers();
      const scr = document.getElementById('agentBootScreen');
      if (!scr || !scr.classList.contains('active')) {
        if (thenOpen) openModal('agentModal');
        return;
      }
      scr.classList.remove('active');
      bootActive = false;
      if (thenOpen) setTimeout(() => openModal('agentModal'), 140);
    }

    function openAgentWithBoot() {
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
    }

    document.getElementById('agentBootScreen').addEventListener('pointerdown', () => hideBootScreen(true));

    if ('serviceWorker' in navigator) {"""

edits.append(("""    if ('serviceWorker' in navigator) {""", js_block))

# ---------- APPLY ----------
fail = [i for i, (o, n) in enumerate(edits) if o not in src]
if fail:
    for i in fail:
        print('MISSING PATTERN #%d:' % i)
        print(edits[i][0][:160])
        print('---')
    sys.exit('ABORT: %d pattern(s) not found; file untouched.' % len(fail))

for o, n in edits:
    assert src.count(o) == 1, 'pattern not unique: %s' % o[:80]
    src = src.replace(o, n)

io.open(PATH, 'w', encoding='utf-8').write(src)
print('OK: %d edits applied. Backup at %s' % (len(edits), BAK))
