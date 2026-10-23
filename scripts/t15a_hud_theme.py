#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 15a: Global HUD theme — convert light Material theme to dark deep-space HUD
   matching the agent boot-sequence design language (violet space + cyan glow)."""
import io, sys, re

P = '/home/z/my-project/public/app.html'
src = io.open(P, encoding='utf-8').read()
orig_len = len(src)
fails = []

def rep(s, old, new, n=1, tag=''):
    global src
    c = src.count(old)
    if c != n:
        fails.append(f'[{tag}] expected {n}, found {c}: {old[:70]!r}')
        return s
    src = src.replace(old, new)
    return s

def rep_all(s, old, new, tag='', expect_min=1):
    global src
    c = src.count(old)
    if c < expect_min:
        fails.append(f'[{tag}] expected >= {expect_min}, found {c}: {old[:70]!r}')
        return s
    src = src.replace(old, new)
    print(f'  ok [{tag}] x{c}')
    return s

# ============ A. Tailwind config tokens -> HUD dark palette ============
print('== A. tokens ==')
rep(src, "surface: '#fcf8ff',", "surface: '#0b0722',", 1, 'surface')
rep(src, "'surface-container': '#efebff',", "'surface-container': '#1a1345',", 1, 's-cont')
rep(src, "'surface-container-low': '#f6f2ff',", "'surface-container-low': '#120c2f',", 1, 's-low')
rep(src, "'surface-container-high': '#e9e5ff',", "'surface-container-high': '#201856',", 1, 's-high')
rep(src, "'surface-container-highest': '#e3dfff',",
    "'surface-container-highest': '#3d3380',\n            'surface-container-lowest': '#0e0929',", 1, 's-highest+lowest')
rep(src, "'on-surface': '#181445',", "'on-surface': '#eef1ff',", 1, 'on-surface')
rep(src, "'on-surface-variant': '#4a4455',", "'on-surface-variant': '#9aa3c0',", 1, 'on-surface-var')
rep(src, "primary: '#630ed4',", "primary: '#8b5cf6',", 1, 'primary')
rep(src, "'on-primary-container': '#ede0ff',", "'on-primary-container': '#251954',", 1, 'on-prim-cont')
rep(src, "secondary: '#6b38d4',", "secondary: '#a78bfa',", 1, 'secondary')
rep(src, "tertiary: '#843700',", "tertiary: '#fbbf24',", 1, 'tertiary')
rep(src, "'tertiary-container': '#aa4900',", "'tertiary-container': '#d97706',", 1, 'tert-cont')
rep(src, "'tertiary-fixed': '#ffdbca',", "'tertiary-fixed': '#382511',", 1, 'tert-fixed')
rep(src, "'on-tertiary-fixed': '#341100',", "'on-tertiary-fixed': '#fcd34d',", 1, 'on-tert-fixed')
rep(src, "outline: '#7b7487',", "outline: '#8b93a7',", 1, 'outline')
rep(src, "'outline-variant': '#ccc3d8',", "'outline-variant': '#3d3380',", 1, 'outline-var')

# ============ B. body + meta theme-color ============
print('== B. body/meta ==')
rep(src, 'background-color: #fcf8ff;',
    'background: radial-gradient(ellipse at 50% -8%, #1b1147 0%, #0d0722 55%, #070417 100%) fixed;',
    1, 'body-bg')
# meta theme-color (any remaining #fcf8ff in meta)
src, nmeta = re.subn(r'(<meta name="theme-color" content=")#fcf8ff(")', r'\g<1>#0b0722\g<2>', src)
print(f'  theme-color meta patched: {nmeta}')

# ============ C. component CSS patches ============
print('== C. components ==')
# global light-color swaps (safe, verified)
rep_all(src, 'rgba(227, 223, 255, 0.8)', 'rgba(139,92,246,0.32)', 'border-soft')
rep_all(src, 'rgba(227,223,255,0.9)', 'rgba(139,92,246,0.35)', 'border-mtn1')
rep_all(src, 'rgba(227,223,255,0.95)', 'rgba(139,92,246,0.4)', 'border-mtn2')
rep_all(src, 'color: #4a4455;', 'color: #9aa3c0;', 'text-muted')
rep_all(src, 'color: #6b647f;', 'color: #9aa3c0;', 'text-musiccat')
rep_all(src, 'background: white; border: 2px solid #e3dfff;',
        'background: rgba(255,255,255,0.045); border: 2px solid #3d3380;', 'emoji-chips', 2)
rep_all(src, 'border-color: #630ed4; background: #f3eefe;',
        'border-color: #8b5cf6; background: rgba(139,92,246,0.16);', 'emoji-active', 2)
rep_all(src, '#e3dfff', '#3d3380', 'e3dfff-rest')
rep_all(src, 'background: #630ed4;\n      color: white;\n      border-color: #630ed4;',
        'background: linear-gradient(135deg, #0e7490, #7c3aed);\n      color: white;\n      border-color: rgba(34,211,238,0.55);', 'chip-active', 2)
rep_all(src, 'background: #630ed4 !important;', 'background: linear-gradient(135deg, #0e7490, #7c3aed) !important;', 'dur-sel')
rep_all(src, 'border-color: #630ed4 !important;', 'border-color: rgba(34,211,238,0.55) !important;', 'dur-sel-b')
rep_all(src, 'border-right: 3px solid #630ed4;', 'border-right: 3px solid #8b5cf6;', 'notif-accent')
rep_all(src, 'box-shadow: 0 4px 12px rgba(99, 14, 212, 0.15);', 'box-shadow: 0 10px 26px rgba(0,0,0,0.45);', 'notif-hover')
rep_all(src, 'box-shadow: 0 2px 8px rgba(99, 14, 212, 0.3);', 'box-shadow: 0 0 16px rgba(34,211,238,0.28);', 'streak-tab-glow')
rep_all(src, 'box-shadow: 0 4px 12px rgba(99, 14, 212, 0.08);', 'box-shadow: 0 8px 22px rgba(0,0,0,0.45);', 'tl-card-sh')
rep_all(src, 'box-shadow: 0 2px 10px rgba(99,14,212,0.05);', 'box-shadow: 0 8px 22px rgba(0,0,0,0.4), inset 0 1px 0 rgba(139,92,246,0.15);', 'mtnstat-sh')
rep_all(src, 'box-shadow: 0 2px 12px rgba(99,14,212,0.06);', 'box-shadow: 0 8px 22px rgba(0,0,0,0.4), inset 0 1px 0 rgba(139,92,246,0.15);', 'mtncard-sh')
rep_all(src, '.mtn-card:hover { box-shadow: 0 6px 18px rgba(99,14,212,0.12); }',
        '.mtn-card:hover { box-shadow: 0 12px 30px rgba(0,0,0,0.55), 0 0 20px rgba(34,211,238,0.12); }', 'mtncard-hov')
rep_all(src, 'background: rgba(239, 235, 255, 0.8);', 'background: rgba(139,92,246,0.12);', 'habit-expanded')
rep_all(src, 'background: linear-gradient(135deg, rgba(99, 14, 212, 0.05) 0%, rgba(167, 139, 250, 0.05) 100%);',
        'background: linear-gradient(135deg, rgba(99, 14, 212, 0.16) 0%, rgba(167, 139, 250, 0.12) 100%);', 'notif-unread')
rep(src, 'background: white;\n      border: 2.5px solid #fbbf24;\n      color: #181445;',
    'background: #1b1345;\n      border: 2.5px solid #fbbf24;\n      color: #eef1ff;', 1, 'today-cell')
rep(src, '.music-tab.active { background: #181445; color: white; border-color: #181445; box-shadow: 0 4px 12px rgba(24,20,69,0.25); }',
    '.music-tab.active { background: linear-gradient(135deg, #0e7490, #7c3aed); color: white; border-color: rgba(34,211,238,0.55); box-shadow: 0 0 16px rgba(34,211,238,0.28); }', 1, 'music-tab-active')
rep(src, '.music-tab-new { border: 1.5px dashed #b7a4f5; background: rgba(99,14,212,0.05); color: #630ed4; }',
    '.music-tab-new { border: 1.5px dashed rgba(139,92,246,0.5); background: rgba(139,92,246,0.08); color: #a78bfa; }', 1, 'music-tab-new')
rep(src, '.music-collection-card { box-shadow: 0 10px 26px rgba(24,20,69,0.16); }',
    '.music-collection-card { box-shadow: 0 14px 34px rgba(0,0,0,0.5); }', 1, 'music-coll-sh')
rep(src, '.music-empty-card { border: 2px dashed #d6cffa; background: rgba(237,233,254,0.4); border-radius: 24px; }',
    '.music-empty-card { border: 2px dashed rgba(139,92,246,0.45); background: rgba(139,92,246,0.06); border-radius: 24px; }', 1, 'music-empty')
rep(src, 'box-shadow: 0 8px 20px rgba(24,20,69,0.22);', 'box-shadow: 0 10px 26px rgba(0,0,0,0.5);', 1, 'music-fab-sh')
rep(src, 'box-shadow: 0 4px 12px rgba(99,14,212,0.3);', 'box-shadow: 0 4px 14px rgba(0,0,0,0.4), 0 0 12px rgba(139,92,246,0.3);', 1, 'music-play-sh')
rep(src, '.music-grad-pick { width: 46px; height: 32px; border-radius: 11px; border: 3px solid white;',
    '.music-grad-pick { width: 46px; height: 32px; border-radius: 11px; border: 3px solid #0b0722;', 1, 'grad-pick')
# nav SVG white -> dark glass
rep(src, 'C 172 0 162 12 145 12 Z" fill="#ffffff" />', 'C 172 0 162 12 145 12 Z" fill="#120c2ff" />'.replace('120c2ff', '120c2f'), 1, 'nav-fill')
rep(src, 'stroke="rgba(227,223,255,0.7)"', 'stroke="rgba(139,92,246,0.55)"', 1, 'nav-stroke')
# backdrop -> black
rep(src, 'bg-on-surface/40 backdrop-blur-sm', 'bg-black/65 backdrop-blur-md', 1, 'backdrop')
# tertiary badge white border on colored card
rep(src, 'shadow-sm border border-white">+</div>', 'shadow-sm border border-white/25">+</div>', 1, 'badge-border')

# any remaining background: white in CSS -> glass (catch-all)
src, nrest = re.subn(r'background: white;', 'background: linear-gradient(160deg, rgba(35,26,74,0.85), rgba(17,11,40,0.92));', src)
print(f'  catch-all background:white -> glass: {nrest}')
# remaining #4a4455 text colors
src, nrest2 = re.subn(r'color: #4a4455', 'color: #9aa3c0', src)
print(f'  remaining #4a4455: {nrest2}')

# ============ D. HTML: hudGrid layer + body tag ============
print('== D. html ==')
rep(src, '<body class="min-h-screen flex flex-col relative overflow-x-hidden">',
    '<body class="min-h-screen flex flex-col relative overflow-x-hidden">\n  <div id="hudGrid" aria-hidden="true"></div>', 1, 'hudGrid')

# ============ E. decoration CSS block (before </style>) ============
print('== E. decor css ==')
HUD_CSS = '''
  /* ==== TASK 15: GLOBAL HUD THEME (deep-space mission control) ==== */
  html { background: #050310; }
  #hudGrid { position: fixed; inset: 0; z-index: 0; pointer-events: none; background-image: linear-gradient(rgba(139,92,246,0.055) 1px, transparent 1px), linear-gradient(90deg, rgba(139,92,246,0.055) 1px, transparent 1px); background-size: 44px 44px; -webkit-mask-image: radial-gradient(ellipse at 50% 28%, black 22%, transparent 76%); mask-image: radial-gradient(ellipse at 50% 28%, black 22%, transparent 76%); animation: bootGridMove 16s linear infinite; }
  #hudGrid::after { content: ''; position: absolute; inset: 0; background: repeating-linear-gradient(0deg, rgba(255,255,255,0.013) 0 1px, transparent 1px 4px); }
  body > *:not(#hudGrid):not(script):not(style) { position: relative; z-index: 1; }
  /* glass cards (bg-white was light) */
  .bg-white { background: linear-gradient(160deg, rgba(35,26,74,0.88), rgba(17,11,40,0.94)) !important; box-shadow: 0 10px 30px rgba(0,0,0,0.45), inset 0 1px 0 rgba(139,92,246,0.16) !important; }
  .w-5.bg-white, .w-10.bg-white { background: #f8fafc !important; box-shadow: 0 1px 4px rgba(0,0,0,0.5) !important; }
  /* modal sheets: agentModal mission-control treatment */
  .modal-sheet { background: radial-gradient(ellipse at 50% -10%, #241458 0%, #130b34 46%, #0c0722 100%) !important; box-shadow: 0 -12px 70px rgba(34,211,238,0.15), 0 -1px 0 rgba(139,92,246,0.55) !important; }
  .modal-sheet > .sticky { background: rgba(15,9,38,0.96) !important; }
  .modal-backdrop { background: rgba(2,1,8,0.72) !important; backdrop-filter: blur(6px); }
  /* toast: HUD transmission pill */
  #toast { background: rgba(16,10,40,0.96) !important; border: 1px solid rgba(34,211,238,0.45) !important; color: #eef1ff !important; box-shadow: 0 10px 34px rgba(0,0,0,0.55), 0 0 26px rgba(34,211,238,0.14) !important; backdrop-filter: blur(14px); }
  /* nav: cyan hairline glow above the glass bar */
  nav svg.drop-shadow-lg { filter: drop-shadow(0 -8px 26px rgba(34,211,238,0.14)) drop-shadow(0 4px 10px rgba(0,0,0,0.5)); }
  /* native controls on dark */
  input, textarea, select { color-scheme: dark; }
  input::placeholder, textarea::placeholder { color: #6b7392; }
  /* scrollbars */
  ::-webkit-scrollbar { width: 4px; height: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.42); border-radius: 999px; }
  ::-webkit-scrollbar-thumb:hover { background: rgba(34,211,238,0.5); }
  /* small contrast fixes */
  .text-emerald-600 { color: #34d399; }
  .bg-amber-50 { background-color: rgba(251,191,36,0.08) !important; }
  .text-amber-900 { color: #fcd34d; }
  .text-amber-800 { color: #fcd34d; }
  .text-amber-600 { color: #fbbf24; }
  /* selection */
  ::selection { background: rgba(34,211,238,0.35); color: #ffffff; }
'''
idx = src.find('</style>')
assert idx > 0
src = src[:idx] + HUD_CSS + src[idx:]

io.open(P, 'w', encoding='utf-8').write(src)
print(f'\nDone. {orig_len} -> {len(src)} bytes')
if fails:
    print('FAILED REPLACEMENTS:')
    for f in fails: print('  ' + f)
    sys.exit(1)
print('ALL OK')
