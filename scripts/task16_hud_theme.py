#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 16b: FULL mission-control HUD — push the whole app into the agent
boot-sequence visual language (cyan glow, corner brackets, scan sweeps,
terminal chips, HUD headers). Layered on top of task-15 dark foundation."""
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

# ============ 1. leftover light CSS -> dark HUD ============
print('== 1. leftovers ==')
# streak calendar wrapper was still WHITE
rep('''    .streak-calendar-wrapper {
      background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%);
      border-radius: 1.5rem;
      padding: 16px 14px;
      border: 1px solid rgba(139,92,246,0.32);
      box-shadow: 0 4px 20px rgba(99, 14, 212, 0.08);''',
'''    .streak-calendar-wrapper {
      background: linear-gradient(160deg, rgba(35,26,74,0.88), rgba(17,11,40,0.94));
      border-radius: 1.5rem;
      padding: 16px 14px;
      border: 1px solid rgba(34,211,238,0.22);
      box-shadow: 0 10px 30px rgba(0,0,0,0.45), inset 0 1px 0 rgba(34,211,238,0.1);''',
    1, 'streak-bg')
rep('background: linear-gradient(90deg, #630ed4, #a78bfa, #fbbf24);',
    'background: linear-gradient(90deg, #8b5cf6, #22d3ee, #6ee7b7); box-shadow: 0 0 12px rgba(34,211,238,0.45);',
    1, 'streak-topline')

# quote-card -> cyan transmission panel
rep('''    .quote-card {
      background: linear-gradient(135deg, rgba(124, 58, 237, 0.05) 0%, rgba(255, 219, 202, 0.08) 100%);
      border: 1px solid rgba(124, 58, 237, 0.15);''',
'''    .quote-card {
      background: linear-gradient(135deg, rgba(34, 211, 238, 0.06) 0%, rgba(139, 92, 246, 0.08) 100%);
      border: 1px solid rgba(34, 211, 238, 0.25);
      box-shadow: 0 10px 30px rgba(0,0,0,0.4), inset 0 1px 0 rgba(34,211,238,0.12);''',
    1, 'quote-card')
rep('color: rgba(124, 58, 237, 0.15);', 'color: rgba(34, 211, 238, 0.2);', 1, 'quote-mark')

# ============ 2. HUD signature layer (appended before </style>) ============
print('== 2. hud layer ==')
hud_css = '''
  /* ==== TASK 16: FULL MISSION-CONTROL HUD (agent boot-sequence language) ==== */
  /* fixed screen frame: 4 corner brackets like the boot screen */
  #hudFrame { position: fixed; inset: 9px; z-index: 63; pointer-events: none; opacity: .85; }
  #hudFrame span { position: absolute; width: 24px; height: 24px; border: 2px solid rgba(34,211,238,0.34); }
  #hudFrame .hf-tl { top: 0; left: 0; border-right: none; border-bottom: none; border-radius: 9px 0 0 0; }
  #hudFrame .hf-tr { top: 0; right: 0; border-left: none; border-bottom: none; border-radius: 0 9px 0 0; }
  #hudFrame .hf-bl { bottom: 0; left: 0; border-right: none; border-top: none; border-radius: 0 0 0 9px; }
  #hudFrame .hf-br { bottom: 0; right: 0; border-left: none; border-top: none; border-radius: 0 0 9px 0; }
  /* vignette over the grid for depth */
  #hudGrid::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 38%, transparent 52%, rgba(2,1,8,0.42) 100%); }
  /* diagonal corner ticks on every major card */
  .habit-card, .quote-card, main > .bg-white, .music-collection-card { position: relative; }
  .habit-card::before, .quote-card::before, main > .bg-white::before, .music-collection-card::before {
    content: ''; position: absolute; top: 6px; right: 6px; width: 13px; height: 13px;
    border-top: 2px solid rgba(34,211,238,0.45); border-right: 2px solid rgba(34,211,238,0.45);
    border-top-right-radius: 5px; pointer-events: none; z-index: 2;
  }
  .habit-card::after, .quote-card::after, main > .bg-white::after, .music-collection-card::after {
    content: ''; position: absolute; bottom: 6px; left: 6px; width: 13px; height: 13px;
    border-bottom: 2px solid rgba(139,92,246,0.5); border-left: 2px solid rgba(139,92,246,0.5);
    border-bottom-left-radius: 5px; pointer-events: none; z-index: 2;
  }
  .streak-calendar-wrapper::after {
    content: ''; position: absolute; bottom: 6px; left: 6px; width: 13px; height: 13px;
    border-bottom: 2px solid rgba(34,211,238,0.4); border-left: 2px solid rgba(34,211,238,0.4);
    border-bottom-left-radius: 5px; pointer-events: none; z-index: 2;
  }
  /* HUD section headers: cyan glowing icons + letterspaced titles */
  main h3 { letter-spacing: 0.3px; }
  main h3 .material-symbols-outlined { color: #22d3ee !important; text-shadow: 0 0 10px rgba(34,211,238,0.5); }
  main .text-primary { color: #22d3ee !important; text-shadow: 0 0 8px rgba(34,211,238,0.3); }
  main .bg-primary\\/10 { background: rgba(34,211,238,0.1) !important; }
  #musicPage .text-primary, .modal-sheet .text-primary { color: #22d3ee !important; text-shadow: 0 0 8px rgba(34,211,238,0.3); }
  /* terminal-style data chips */
  #streakTotalLabel, #musicCountLabel { color: #7fe7f4 !important; border-color: rgba(34,211,238,0.3) !important; text-shadow: 0 0 8px rgba(34,211,238,0.35); font-weight: 800; }
  /* header: cyan hairline + scan sweep */
  .glass-strong { border-bottom: 1px solid rgba(34,211,238,0.22) !important; }
  .glass-strong { position: relative; overflow: hidden; }
  .glass-strong::after { content: ''; position: absolute; top: 0; bottom: 0; width: 34%; left: -40%; background: linear-gradient(100deg, transparent, rgba(34,211,238,0.07) 45%, rgba(139,92,246,0.06) 55%, transparent); animation: hudSweep 6.5s linear infinite; pointer-events: none; }
  @keyframes hudSweep { 0% { left: -40%; } 100% { left: 140%; } }
  /* nav: active = cyan glow (sequence style) */
  .nav-btn.active .material-symbols-outlined { color: #22d3ee !important; text-shadow: 0 0 12px rgba(34,211,238,0.55); }
  .nav-btn.active span:last-child { color: #a5f3fc !important; }
  /* primary buttons: cyan glow ring */
  .bg-primary { box-shadow: 0 0 20px rgba(34,211,238,0.16), 0 6px 16px rgba(0,0,0,0.35) !important; }
  /* progress: boot-style cyan-violet glow */
  #musicMiniProgress { background: linear-gradient(90deg, #8b5cf6, #22d3ee) !important; box-shadow: 0 0 10px rgba(34,211,238,0.5); }
  /* modal sheets: top HUD hairline */
  .modal-sheet { border-top: 1px solid rgba(34,211,238,0.38) !important; }
  /* hero HUD status line */
  .hud-sysline { display: inline-flex; align-items: center; gap: 6px; font-size: 9.5px; font-weight: 700; letter-spacing: 2px; color: rgba(125,211,252,0.62); margin-top: 4px; }
  .hud-sysline::before { content: ''; width: 6px; height: 6px; border-radius: 2px; background: #22d3ee; box-shadow: 0 0 8px rgba(34,211,238,0.8); animation: bootCursor 0.9s steps(1) infinite; }
  .hud-sysline::after { content: ''; flex: 1; min-width: 60px; height: 1px; margin-right: 8px; background: linear-gradient(270deg, rgba(34,211,238,0.4), transparent); }
'''
rep('  /* app-start boot splash (short cinematic sequence) */', hud_css + '\n  /* app-start boot splash (short cinematic sequence) */', 1, 'hud-css')

# ============ 3. HTML: hudFrame element + hero sysline + version bump ============
print('== 3. html ==')
rep('<div id="hudGrid" aria-hidden="true"></div>',
    '<div id="hudGrid" aria-hidden="true"></div>\n  <div id="hudFrame" aria-hidden="true"><span class="hf-tl"></span><span class="hf-tr"></span><span class="hf-bl"></span><span class="hf-br"></span></div>',
    1, 'hudFrame')
rep('''      <h2 class="text-2xl font-bold text-on-surface leading-tight mb-3">مسیر صعود به قله موفقیت</h2>
      <p class="text-sm text-on-surface-variant leading-relaxed">هر عادت یک کوه است. با استمرار، قله را فتح کن.</p>''',
'''      <h2 class="text-2xl font-bold text-on-surface leading-tight mb-1.5">مسیر صعود به قله موفقیت</h2>
      <p class="text-sm text-on-surface-variant leading-relaxed">هر عادت یک کوه است. با استمرار، قله را فتح کن.</p>
      <p class="hud-sysline">سامانه فعال — همه ماژول‌ها آماده</p>''',
    1, 'hero-sysline')
# boot version labels 2.0 -> 2.1
c = src.count('نسخه ۲.۰')
rep('نسخه ۲.۰', 'نسخه ۲.۱', 2, 'boot-version') if c == 2 else fails.append(f'[boot-version] expected 2, found {c}')

io.open(P, 'w', encoding='utf-8').write(src)
print(f'done: {orig} -> {len(src)} chars ({len(src)-orig:+d})')
if fails:
    print('FAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('ALL HUD PATCHES OK')
