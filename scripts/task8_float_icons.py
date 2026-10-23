# -*- coding: utf-8 -*-
"""Task 8: floating animation for ALL icons (material symbols + standalone emoji icons)
with organic random stagger via MutationObserver. Fail-safe assertions, backup first."""
import io, sys, shutil

PATH = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task8.bak'
src = io.open(PATH, encoding='utf-8').read()
shutil.copyfile(PATH, BAK)

edits = []

# ---------- 1) CSS: global float keyframes (uses `translate` property so it
# composes with existing transform:scale active states instead of overriding them) ----------
edits.append((
    """  </style>
</head>""",
    """  /* ===== FLOATING ICONS (global) ===== */
    @keyframes iconFloat { 0%, 100% { translate: 0 0; } 50% { translate: 0 -3.5px; } }
    .material-symbols-outlined { animation: iconFloat 3.6s ease-in-out infinite; }
    .float-icon { animation: iconFloat 3.6s ease-in-out infinite; }
    .streak-day-icon { animation: iconFloat 3.6s ease-in-out infinite; }
    .habit-emoji-chip, .music-emoji-pick { animation: iconFloat 4.4s ease-in-out infinite; }
    @media (prefers-reduced-motion: reduce) {
      .material-symbols-outlined, .float-icon, .streak-day-icon, .habit-emoji-chip, .music-emoji-pick { animation: none !important; }
    }
  </style>
</head>"""))

# ---------- 2) JS: stagger engine — random negative animation-delay per icon,
# kept organic across re-renders via MutationObserver ----------
edits.append((
    """    if ('serviceWorker' in navigator) {""",
    """    // ================= FLOATING ICONS: STAGGER ENGINE =================
    (function () {
      const rand = () => (-(Math.random() * 3.6)).toFixed(2) + 's';
      const SEL = '.material-symbols-outlined, .float-icon, .streak-day-icon, .habit-emoji-chip, .music-emoji-pick';
      const mark = (el) => { if (!el.style.animationDelay) el.style.animationDelay = rand(); };
      const scan = (node) => {
        if (!node || node.nodeType !== 1) return;
        if (node.matches && node.matches(SEL)) mark(node);
        if (node.querySelectorAll) node.querySelectorAll(SEL).forEach(mark);
      };
      scan(document.body);
      new MutationObserver((muts) => {
        for (const m of muts) for (const n of m.addedNodes) scan(n);
      }).observe(document.body, { childList: true, subtree: true });
    })();

    if ('serviceWorker' in navigator) {"""))

# ---------- 3) Add float-icon class to standalone emoji icons ----------
edits.append((
    """<div id="newHabitEmojiBadge" class="absolute right-2 w-8 h-8 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-[17px]">🏔️</div>""",
    """<div id="newHabitEmojiBadge" class="float-icon absolute right-2 w-8 h-8 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-[17px]">🏔️</div>"""))

edits.append((
    """<span class="text-4xl block mb-2 opacity-50">🏔️</span>""",
    """<span class="float-icon text-4xl block mb-2 opacity-50">🏔️</span>"""))

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
