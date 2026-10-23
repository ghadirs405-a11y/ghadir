# -*- coding: utf-8 -*-
"""Task 10 (part A): longer cinematic boot UI + dark HUD theme for agent modal."""
import sys, shutil

PATH = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task10.bak'

with open(PATH, encoding='utf-8') as f:
    c = f.read()

def sub_once(content, old, new, name):
    n = content.count(old)
    assert n == 1, f'ABORT [{name}]: expected 1 occurrence, found {n}'
    print(f'OK  {name}')
    return content.replace(old, new, 1)

# ---------- safety ----------
assert 'BOOT_LINES' in c and 'agentBootScreen' in c, 'task9 code missing'
assert 'agentMaterialize' not in c, 'task10 already applied'

NEW_CSS = '''  /* ==== TASK 10: LONGER CINEMATIC BOOT (phases / equalizer / HUD) ==== */
  .boot-hud-title { position: absolute; top: 28px; left: 0; right: 0; text-align: center; font-size: 11px; font-weight: 800; letter-spacing: 3px; color: rgba(165,243,252,0.85); animation: bootTitleIn 0.9s ease both; }
  .boot-hud-title .boot-hud-ver { font-size: 9px; color: rgba(196,181,253,0.75); letter-spacing: 0.5px; margin-right: 6px; }
  .boot-hud-title::after { content: ''; display: block; width: 130px; height: 1px; margin: 6px auto 0; background: linear-gradient(90deg, transparent, rgba(34,211,238,0.6), transparent); }
  @keyframes bootTitleIn { 0% { opacity: 0; letter-spacing: 9px; filter: blur(5px); } 100% { opacity: 1; letter-spacing: 3px; filter: blur(0); } }
  .boot-tag { position: absolute; font-size: 9px; font-weight: 700; color: rgba(125,211,252,0.55); letter-spacing: 1px; animation: bootTitleIn 1.2s ease both; }
  .boot-tag-tl { top: 78px; left: 24px; }
  .boot-tag-br { bottom: 78px; right: 24px; }
  .boot-eq { display: flex; align-items: flex-end; justify-content: center; gap: 3px; height: 22px; opacity: 0; transition: opacity 0.5s ease; }
  .boot-eq.on { opacity: 1; }
  .boot-eq span { width: 3px; height: 30%; border-radius: 2px; background: linear-gradient(180deg, #22d3ee, #8b5cf6); box-shadow: 0 0 6px rgba(34,211,238,0.5); animation: bootEqBar 0.9s ease-in-out infinite; }
  @keyframes bootEqBar { 0%, 100% { height: 22%; } 50% { height: 100%; } }
  .boot-status { font-size: 10px; font-weight: 700; color: #7fe7f4; letter-spacing: 1px; opacity: 0.92; text-shadow: 0 0 10px rgba(34,211,238,0.4); transition: color 0.4s ease; }
  #agentBootScreen.boot-final .boot-ring-a { animation-duration: 1.7s; }
  #agentBootScreen.boot-final .boot-ring-b { animation-duration: 0.9s; }
  #agentBootScreen.boot-final .boot-eye { animation: bootEyeOn 0.5s steps(2, jump-none) 0.85s forwards, bootEyeGlowFast 0.55s ease-in-out infinite; }
  #agentBootScreen.boot-final .boot-head { animation: bootHeadIn 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) both, bootHeadGlow 0.9s ease-in-out infinite; }
  #agentBootScreen.boot-final .boot-scanline { animation-duration: 0.65s; }
  #agentBootScreen.boot-final .boot-eq span { animation-duration: 0.45s; }
  #agentBootScreen.boot-final .boot-status { color: #6ee7b7; text-shadow: 0 0 10px rgba(52,211,153,0.55); }
  @keyframes bootEyeGlowFast { 0%, 100% { filter: drop-shadow(0 0 5px rgba(34,211,238,0.9)); } 50% { filter: drop-shadow(0 0 14px rgba(34,211,238,1)); } }
  @keyframes bootHeadGlow { 0%, 100% { filter: drop-shadow(0 0 14px rgba(34,211,238,0.4)); } 50% { filter: drop-shadow(0 0 26px rgba(34,211,238,0.75)); } }

  /* ==== TASK 10: CINEMATIC AGENT MODAL (mission-control dark HUD) ==== */
  #agentModal { background: radial-gradient(ellipse at 50% -10%, #2b1663 0%, #170d3d 42%, #0c0722 100%); box-shadow: 0 -12px 70px rgba(34,211,238,0.16), 0 -1px 0 rgba(139,92,246,0.55); }
  #agentModal > .sticky { background: rgba(15,9,38,0.94); border-bottom: 1px solid rgba(139,92,246,0.3); overflow: hidden; }
  #agentModal > .sticky::after { content: ''; position: absolute; bottom: 0; right: -30%; width: 30%; height: 2px; background: linear-gradient(90deg, transparent, rgba(34,211,238,0.9), transparent); animation: agentHeaderScan 3.4s linear infinite; }
  @keyframes agentHeaderScan { 0% { right: -30%; } 100% { right: 100%; } }
  #agentModal > .sticky > div:first-child button, #agentModal > .sticky > button { background: rgba(139,92,246,0.15); border-color: rgba(139,92,246,0.4); color: #cbd5e1; }
  .agent-online-pill { display: inline-flex; align-items: center; gap: 5px; font-size: 9px; font-weight: 800; color: #6ee7b7; background: rgba(16,185,129,0.1); border: 1px solid rgba(52,211,153,0.3); border-radius: 100px; padding: 2px 8px; margin-top: 3px; }
  .agent-online-dot { width: 5px; height: 5px; border-radius: 50%; background: #34d399; box-shadow: 0 0 8px rgba(52,211,153,0.9); animation: agentOnlinePulse 1.6s ease-in-out infinite; }
  @keyframes agentOnlinePulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.35; } }
  #agentModal .agent-header-greeting { background: linear-gradient(150deg, rgba(34,211,238,0.07), rgba(139,92,246,0.12)); border: 1px solid rgba(34,211,238,0.22); box-shadow: inset 0 0 34px rgba(34,211,238,0.05); position: relative; }
  #agentModal .agent-header-greeting::before, #agentModal .agent-header-greeting::after { content: ''; position: absolute; width: 16px; height: 16px; border-color: rgba(34,211,238,0.65); border-style: solid; }
  #agentModal .agent-header-greeting::before { top: 7px; right: 7px; border-width: 2px 2px 0 0; border-radius: 0 6px 0 0; }
  #agentModal .agent-header-greeting::after { bottom: 7px; left: 7px; border-width: 0 0 2px 2px; border-radius: 0 0 0 6px; }
  #agentGreeting { color: #f1f5f9; }
  #agentSubGreeting { color: #7dd3fc; }
  #agentModal .agent-header-greeting span { background: rgba(34,211,238,0.09); color: #67e8f9; border: 1px solid rgba(34,211,238,0.3); }
  #agentModal .agent-avatar { background: linear-gradient(135deg, #0891b2 0%, #7c3aed 100%); box-shadow: 0 0 30px rgba(34,211,238,0.35); }
  #agentModal .agent-avatar svg { animation: agentPulse 2s ease-in-out infinite; }
  #agentModal .text-on-surface { color: #f1f5f9; }
  #agentModal .text-on-surface-variant { color: #8b93a7; }
  #agentModal .agent-tab { background: rgba(139,92,246,0.09); border-color: rgba(139,92,246,0.32); color: #c4b5fd; }
  #agentModal .agent-tab.active { background: linear-gradient(135deg, #0e7490, #7c3aed); border-color: rgba(34,211,238,0.55); box-shadow: 0 0 18px rgba(34,211,238,0.28); color: #ffffff; }
  #agentModal .agent-section { background: rgba(139,92,246,0.06); border-color: rgba(139,92,246,0.3); box-shadow: inset 0 0 26px rgba(139,92,246,0.05); }
  #agentModal .agent-section-title { color: #e2e8f0; }
  #agentModal .agent-section-subtitle { color: #94a3b8; }
  #agentModal .agent-cap-card { background: rgba(255,255,255,0.045); border-color: rgba(34,211,238,0.2); }
  #agentModal .agent-cap-title { color: #e2e8f0; }
  #agentModal .agent-cap-sub { color: #8b93a7; }
  #agentModal .agent-quick-chip { background: rgba(139,92,246,0.1); border-color: rgba(139,92,246,0.38); color: #c4b5fd; }
  #agentModal .agent-quick-chip:active { background: rgba(139,92,246,0.22); }
  #agentModal .agent-chat-wrap { background: rgba(9,5,24,0.6); border-color: rgba(34,211,238,0.22); box-shadow: inset 0 0 44px rgba(0,0,0,0.4); }
  #agentModal .agent-chat-msgs::-webkit-scrollbar-thumb { background: rgba(34,211,238,0.35); }
  #agentModal .agent-msg.bot { background: rgba(139,92,246,0.13); color: #e2e8f0; border-right-color: #22d3ee; box-shadow: 0 2px 10px rgba(0,0,0,0.35); }
  #agentModal .agent-msg.me { background: linear-gradient(135deg, #7c3aed 0%, #4c1d95 100%); box-shadow: 0 3px 12px rgba(124,58,237,0.35); }
  #agentModal .agent-msg-avatar { background: linear-gradient(135deg, #0891b2, #7c3aed); }
  #agentModal .agent-typing-bubble { background: rgba(139,92,246,0.13); border-right-color: #22d3ee; }
  #agentModal .agent-typing-dot { background: #22d3ee; }
  #agentModal .agent-chat-input-row { background: rgba(9,5,24,0.85); border-top: 1px solid rgba(34,211,238,0.14); }
  #agentModal .agent-input { background: rgba(255,255,255,0.06); border-color: rgba(139,92,246,0.35); color: #e2e8f0; }
  #agentModal .agent-input::placeholder { color: #64748b; }
  #agentModal .agent-input:focus { border-color: #22d3ee; box-shadow: 0 0 0 3px rgba(34,211,238,0.12); }
  #agentModal .agent-send-btn { background: linear-gradient(135deg, #0891b2, #7c3aed); box-shadow: 0 0 16px rgba(34,211,238,0.3); }
  #agentModal .agent-chat-clear { background: rgba(255,255,255,0.05); border-color: rgba(139,92,246,0.3); color: #94a3b8; }
  #agentModal .agent-plan-card { background: linear-gradient(150deg, rgba(34,211,238,0.09) 0%, rgba(13,7,34,0.7) 45%, rgba(139,92,246,0.14) 100%); border-color: rgba(34,211,238,0.35); }
  #agentModal .agent-plan-head { background: linear-gradient(135deg, #0e7490 0%, #6d28d9 100%); }
  #agentModal .agent-plan-habit { background: rgba(255,255,255,0.05); border-color: rgba(139,92,246,0.3); }
  #agentModal .agent-plan-habit-name { color: #e2e8f0; }
  #agentModal .agent-plan-habit-meta { color: #94a3b8; }
  #agentModal .agent-plan-habit-tip { color: #67e8f9; background: rgba(34,211,238,0.08); }
  #agentModal .agent-plan-applied { background: rgba(16,185,129,0.12); border-color: rgba(52,211,153,0.45); color: #6ee7b7; }
  #agentModal .agent-btn-primary { background: linear-gradient(135deg, #0891b2, #7c3aed); box-shadow: 0 0 20px rgba(34,211,238,0.25); }
  #agentModal .agent-week-stat { background: rgba(255,255,255,0.05); border-color: rgba(34,211,238,0.2); }
  #agentModal .agent-week-stat-val { color: #a5f3fc; }
  #agentModal .agent-week-stat-label { color: #94a3b8; }
  #agentModal .agent-report-card { background: linear-gradient(135deg, rgba(139,92,246,0.13), rgba(34,211,238,0.07)); border-color: rgba(139,92,246,0.35); }
  #agentModal .agent-report-headline { color: #c4b5fd; }
  #agentModal .agent-report-summary { color: #cbd5e1; }
  #agentModal .agent-report-item { color: #cbd5e1; background: rgba(255,255,255,0.05); }
  #agentModal .agent-report-focus { color: #67e8f9; background: rgba(34,211,238,0.07); border-color: rgba(34,211,238,0.4); }
  #agentModal .agent-report-motivation { color: #fbbf24; background: rgba(251,191,36,0.08); }
  #agentModal .agent-report-date { color: #64748b; }
  #agentModal .agent-toggle-row { color: #cbd5e1; }
  #agentModal .agent-platform-chip { background: rgba(255,255,255,0.05); border-color: rgba(139,92,246,0.3); color: #94a3b8; }
  #agentModal .agent-platform-chip.active { background: linear-gradient(135deg, #0e7490, #7c3aed); box-shadow: 0 0 14px rgba(34,211,238,0.25); }
  #agentModal .agent-social-card { background: rgba(255,255,255,0.04); border-color: rgba(139,92,246,0.28); box-shadow: 0 4px 18px rgba(0,0,0,0.3); }
  #agentModal .agent-social-week { color: #67e8f9; background: rgba(34,211,238,0.08); }
  #agentModal .agent-social-platform { border-color: rgba(139,92,246,0.28); background: rgba(255,255,255,0.03); }
  #agentModal .agent-social-platform-title { color: #e2e8f0; }
  #agentModal .agent-social-meta { color: #cbd5e1; }
  #agentModal .agent-prompt-box { border: 1px solid rgba(34,211,238,0.28); }
  #agentModal.agent-materialize { animation: agentMaterialize 0.9s cubic-bezier(0.23, 1, 0.32, 1); }
  @keyframes agentMaterialize { 0% { opacity: 0; transform: translateY(34px) scale(0.96); filter: blur(16px) brightness(2.4); } 55% { filter: blur(0) brightness(1.2); } 100% { opacity: 1; transform: none; filter: none; } }
  @media (prefers-reduced-motion: reduce) {
    #agentModal.agent-materialize { animation: none; }
    #agentModal > .sticky::after { animation: none; }
    .boot-eq span { animation: none; }
  }

'''

# 1) inject all new CSS right before closing </style>
c = sub_once(c, '\n  </style>', '\n' + NEW_CSS + '  </style>', 'inject CSS block')

# 2) terminal rule: slightly smaller text, taller min-height for 9 lines
c = sub_once(c,
    '  .boot-terminal { direction: rtl; text-align: right; width: 100%; min-height: 88px; font-size: 12px; font-weight: 600; color: #7fe7f4; display: flex; flex-direction: column; gap: 5px; }',
    '  .boot-terminal { direction: rtl; text-align: right; width: 100%; min-height: 100px; font-size: 11.5px; font-weight: 600; color: #7fe7f4; display: flex; flex-direction: column; gap: 4px; }',
    'terminal css tweak')

# 3) boot HTML: HUD title + side tags after grid bg
c = sub_once(c,
    '    <div class="boot-grid-bg"></div>',
    '''    <div class="boot-grid-bg"></div>
    <div class="boot-hud-title">هسته دستیار هوشمند<span class="boot-hud-ver">نسخه ۲.۰</span></div>
    <div class="boot-tag boot-tag-tl">اتصال: پایدار</div>
    <div class="boot-tag boot-tag-br">رمزگذاری: فعال</div>''',
    'boot HUD title/tags')

# 4) boot HTML: equalizer before terminal
c = sub_once(c,
    '      <div class="boot-terminal" id="bootTerminal"></div>',
    '''      <div class="boot-eq" id="bootEq"></div>
      <div class="boot-terminal" id="bootTerminal"></div>''',
    'boot equalizer')

# 5) boot HTML: phase status after percent
c = sub_once(c,
    '      <div class="boot-percent" id="bootPercent">۰٪</div>',
    '''      <div class="boot-percent" id="bootPercent">۰٪</div>
      <div class="boot-status" id="bootStatus">فاز ۱ — انرژی‌رسانی هسته</div>''',
    'boot phase status')

# 6) agent modal header: robot head SVG + online pill
OLD_HEAD = '''      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-agent-primary to-agent-secondary flex items-center justify-center">
          <span class="material-symbols-outlined text-[18px] text-white">smart_toy</span>
        </div>
        <h3 class="font-bold text-on-surface text-base">دستیار هوشمند</h3>
      </div>'''
NEW_HEAD = '''      <div class="flex items-center gap-2">
        <div class="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-400 to-violet-600 flex items-center justify-center shadow-[0_0_16px_rgba(34,211,238,0.45)]">
          <svg viewBox="0 0 120 120" class="w-6 h-6" aria-hidden="true">
            <rect x="26" y="26" width="68" height="58" rx="17" fill="rgba(255,255,255,0.16)" stroke="#f8fafc" stroke-width="6"/>
            <rect x="39" y="47" width="13" height="9" rx="4.5" fill="#a5f3fc"/>
            <rect x="68" y="47" width="13" height="9" rx="4.5" fill="#a5f3fc"/>
            <line x1="60" y1="12" x2="60" y2="26" stroke="#f8fafc" stroke-width="7" stroke-linecap="round"/>
            <circle cx="60" cy="9" r="5" fill="#a5f3fc"/>
          </svg>
        </div>
        <div class="flex flex-col">
          <h3 class="font-bold text-on-surface text-base leading-tight">دستیار هوشمند</h3>
          <div class="agent-online-pill"><span class="agent-online-dot"></span> آنلاین و آماده</div>
        </div>
      </div>'''
c = sub_once(c, OLD_HEAD, NEW_HEAD, 'agent modal header')

# 7) greeting avatar: robot head SVG instead of smart_toy icon
OLD_AV = '''        <div class="agent-avatar mx-auto mb-3">
          <span class="material-symbols-outlined">smart_toy</span>
        </div>'''
NEW_AV = '''        <div class="agent-avatar mx-auto mb-3">
          <svg viewBox="0 0 120 120" class="w-11 h-11" aria-hidden="true">
            <defs>
              <linearGradient id="agentHeadGrad" x1="0" y1="0" x2="1" y2="1">
                <stop offset="0" stop-color="#67e8f9"/>
                <stop offset="1" stop-color="#c4b5fd"/>
              </linearGradient>
            </defs>
            <line x1="60" y1="13" x2="60" y2="24" stroke="url(#agentHeadGrad)" stroke-width="4" stroke-linecap="round"/>
            <circle cx="60" cy="9" r="4" fill="#67e8f9"/>
            <rect x="26" y="24" width="68" height="60" rx="18" fill="rgba(255,255,255,0.1)" stroke="url(#agentHeadGrad)" stroke-width="3.5"/>
            <rect x="39" y="46" width="13" height="9" rx="4.5" fill="#e0f2fe"/>
            <rect x="68" y="46" width="13" height="9" rx="4.5" fill="#e0f2fe"/>
            <rect x="46" y="64" width="28" height="7" rx="3.5" fill="none" stroke="rgba(224,242,254,0.6)" stroke-width="2"/>
          </svg>
        </div>'''
c = sub_once(c, OLD_AV, NEW_AV, 'greeting robot avatar')

with open(PATH, 'w', encoding='utf-8') as f:
    f.write(c)
print('SAVED', PATH)
