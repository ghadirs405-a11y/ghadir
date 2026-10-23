# -*- coding: utf-8 -*-
"""
Task 5: حذف بخش‌های درخواستی کاربر + بازسازی کامل «کوه‌های من»
حذف‌ها:
  1. بخش ۰ از ۰ عادت‌های امروز (Stats Cards)
  2. بخش ٪ تکمیل / ۰ از ۰ عادت (Progress Ring)
  3. تب‌های ایجنت: بیدارباش، برنامه، گزارش، آنالیز، بینش (+ دکمه صدای هدر)
  4. تمام JS/CSS یتیم مربوطه
بازسازی:
  - مودال کوه‌های من از اول: هیرو قله + آمار + کارت‌های کوه شیک و کاربرپسند
هر عملیات با assert روی محتوای خطوط بررسی می‌شود؛ در صورت عدم تطابق، قبل از نوشتن فایل متوقف می‌شود.
"""
import shutil, sys, io

SRC = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task5.bak'

with io.open(SRC, 'r', encoding='utf-8') as f:
    lines = f.read().split('\n')  # 0-indexed

orig_count = len(lines)
print('Original line count:', orig_count)

# ---------------------------------------------------------------- helpers
def L(n):  # 1-indexed line -> 0-indexed
    return lines[n - 1]

def assert_contains(n, needle, ctx=''):
    if needle not in L(n):
        sys.exit('ASSERT FAIL at line %d (expect %r): %r | %s' % (n, needle, L(n)[:120], ctx))

def assert_eq(n, expected):
    if L(n) != expected:
        sys.exit('ASSERT EQ FAIL at line %d (expect %r): %r' % (n, expected, L(n)))

def assert_blank(n):
    if L(n).strip() != '':
        sys.exit('ASSERT BLANK FAIL at line %d: %r' % (n, L(n)[:120]))

def delete(start, end):
    """delete lines[start..end] inclusive (1-indexed)"""
    global lines
    lines = lines[:start - 1] + lines[end:]

def replace(start, end, new_text):
    """replace lines[start..end] inclusive with new_text (string)"""
    global lines
    lines = lines[:start - 1] + new_text.split('\n') + lines[end:]

# ---------------------------------------------------------------- assertions (on ORIGINAL file)
# --- R19: openModal mountainModal case (5674-5679)
assert_contains(5674, "if (id === 'mountainModal')")
assert_eq(5679, '      }')
assert_contains(5680, "notificationsModal")

# --- R18: mountain JS section (4266-4482)
assert_contains(4266, 'MOUNTAIN SCENE')
assert_contains(4267, 'function renderMountainScene')
assert_eq(4481, '    }')
assert_blank(4482)
assert_contains(4483, 'NOTEBOOK')

# --- R17: renderProgress + renderStats defs (3941-3963)
assert_contains(3941, 'function renderProgress')
assert_eq(3962, '    }')
assert_blank(3963)
assert_contains(3964, 'STREAK CALENDAR')

# --- R16: renderAll calls (3928-3929)
assert_contains(3928, 'renderProgress();')
assert_contains(3929, 'renderStats();')
assert_contains(3930, 'renderStreakCalendar();')

# --- R15b: agent settings load in DOMContentLoaded (3877-3883)
assert_contains(3877, '// Load agent settings')
assert_eq(3882, '      }')
assert_blank(3883)
assert_contains(3884, '// Check for unread agent notifications')

# --- R15a: startAgentWakeChecker() call (3868)
assert_contains(3867, 'startAlarmChecker();')
assert_contains(3868, 'startAgentWakeChecker();')

# --- R14: agent plan/checkin/analysis/insights/wake JS (3477-3858)
assert_blank(3477)
assert_contains(3478, 'function renderAgentDailyPlan')
assert_contains(3531, 'function toggleAgentTask')
assert_contains(3536, 'function speakDailyPlan')
assert_contains(3549, 'function renderAgentCheckin')
assert_contains(3583, 'let selectedAgentMood')
assert_contains(3592, 'function submitAgentCheckin')
assert_contains(3642, 'function generateCheckinAnalysis')
assert_contains(3663, 'function calculateAgentScore')
assert_contains(3679, 'function getScoreMessage')
assert_contains(3687, 'function generateAgentAnalysis')
assert_contains(3758, 'function generateAgentInsights')
assert_contains(3815, 'function saveAgentSettings')
assert_contains(3828, 'function startAgentWakeChecker')
assert_eq(3858, '    }')
assert_blank(3859)
assert_contains(3860, 'INIT')

# --- R13: switchAgentTab else-ifs (3438-3447)
assert_contains(3438, "else if (tabName === 'wake')")
assert_contains(3447, 'generateAgentInsights();')
assert_contains(3448, "else if (tabName === 'report')")

# --- R12: morning messages (2836-2850)
assert_blank(2835)
assert_contains(2836, 'AGENT FUNCTIONS')
assert_contains(2837, 'const morningMessages')
assert_contains(2845, 'function generateNewMorningMessage')
assert_blank(2850)
assert_contains(2851, 'CHAT & AUTOMATION')

# --- R11: speakAgentMessage + weather (2695-2743)
assert_blank(2695)
assert_contains(2696, 'function speakAgentMessage')
assert_contains(2721, 'WEATHER')
assert_contains(2728, 'function renderWeatherWidget')
assert_eq(2742, '    }')
assert_blank(2743)
assert_contains(2744, 'NOTIFICATIONS')

# --- R10: Progress Ring HTML (1281-1301)
assert_contains(1281, '<!-- Progress Ring -->')
assert_eq(1300, '    </div>')
assert_blank(1301)
assert_contains(1302, 'Streak Calendar')

# --- R9: Stats Cards HTML (1270-1279)
assert_contains(1270, '<!-- Stats Cards -->')
assert_contains(1276, 'statHabitsToday')
assert_eq(1279, '    </div>')
assert_blank(1280)
assert_contains(1281, '<!-- Progress Ring -->')

# --- R8: header speak button (1538-1540)
assert_contains(1538, 'speakAgentMessage')
assert_eq(1540, '      </button>')
assert_eq(1541, '    </div>')

# --- R7: 5 agent tab buttons (1561-1565)
assert_contains(1561, "switchAgentTab('wake')")
assert_contains(1562, "switchAgentTab('plan')")
assert_contains(1563, "switchAgentTab('checkin')")
assert_contains(1564, "switchAgentTab('analysis')")
assert_contains(1565, "switchAgentTab('insights')")
assert_contains(1566, "switchAgentTab('report')")

# --- R2..R6: five tab content blocks (1631-1897)
assert_contains(1631, 'Tab Content: Wake Up')
assert_contains(1632, 'agentTabWake')
assert_contains(1695, 'agentTabPlan')
assert_contains(1733, 'agentTabCheckin')
assert_contains(1793, 'agentTabAnalysis')
assert_contains(1844, 'agentTabInsights')
assert_eq(1896, '      </div>')
assert_blank(1897)
assert_contains(1898, 'Weekly Auto Report')

# --- R1: Mountain Modal HTML (2119-2197)
assert_contains(2119, '<!-- Mountain Modal -->')
assert_contains(2120, 'id="mountainModal"')
assert_contains(2138, 'statTotalMountains')
assert_contains(2156, 'weatherIcon')
assert_contains(2194, 'mountainScroll')
assert_eq(2197, '  </div>')
assert_blank(2198)
assert_contains(2199, '<!-- Add Habit Modal -->')

# --- CSS ops
# C6: .agent-progress-ring (883-886)
assert_contains(883, '.agent-progress-ring')
assert_blank(886)
assert_contains(887, '.agent-chat-bubble')

# C5: .agent-score-circle + .agent-mood (790-851)
assert_contains(790, '.agent-score-circle {')
assert_eq(850, '    }')
assert_blank(851)
assert_contains(852, '.agent-notification-badge')

# C4: .agent-task-item family + stat-bar + strength/weakness (623-707)
assert_contains(623, '.agent-task-item {')
assert_eq(706, '    }')
assert_blank(707)
assert_contains(708, '.agent-btn {')

# C0: .stat-card (233-237)
assert_contains(233, '.stat-card {')
assert_blank(237)
assert_contains(238, '.medal-gold')

# C2+C3: weather CSS + .mountain-scroll (193-205)
assert_contains(193, '.weather-widget')
assert_contains(197, '.mountain-scroll')
assert_blank(205)
assert_contains(206, '.category-filter-chip')

# C1: .mountain-card (131-136)
assert_contains(131, '.mountain-card {')
assert_eq(136, '    }')
assert_blank(137)
assert_contains(138, '.notebook-page')

print('All assertions passed. Applying operations bottom-up...')

# ---------------------------------------------------------------- NEW CONTENT BLOCKS

NEW_MOUNTAIN_CSS = '''    /* ===== My Mountains (REBUILT) ===== */
    .mtn-hero {
      background: linear-gradient(140deg, #4c0da0 0%, #630ed4 45%, #8b5cf6 100%);
      border-radius: 24px;
      padding: 22px 20px 24px;
      position: relative;
      overflow: hidden;
      color: white;
      box-shadow: 0 12px 28px rgba(99, 14, 212, 0.30);
    }
    .mtn-hero-svg {
      position: absolute; left: 0; right: 0; bottom: -2px; width: 100%; height: auto;
      pointer-events: none;
    }
    .mtn-stage-chip {
      display: inline-flex; align-items: center; gap: 5px;
      background: rgba(255,255,255,0.16); border: 1px solid rgba(255,255,255,0.32);
      backdrop-filter: blur(4px); -webkit-backdrop-filter: blur(4px);
      padding: 5px 12px; border-radius: 100px; font-size: 10.5px; font-weight: 800;
    }
    .mtn-hero-bar { height: 10px; background: rgba(255,255,255,0.22); border-radius: 6px; overflow: hidden; }
    .mtn-hero-fill {
      height: 100%; border-radius: 6px;
      background: linear-gradient(90deg, #fbbf24, #fde047);
      box-shadow: 0 0 12px rgba(251,191,36,0.65);
      position: relative; overflow: hidden;
      transition: width 1.1s cubic-bezier(0.34,1.3,0.64,1);
    }
    .mtn-hero-fill::after {
      content: ''; position: absolute; inset: 0;
      background: linear-gradient(100deg, transparent 20%, rgba(255,255,255,0.5) 50%, transparent 80%);
      animation: mtnShimmer 2.4s ease-in-out infinite;
    }
    @keyframes mtnShimmer { 0% { transform: translateX(-120%); } 55%, 100% { transform: translateX(240%); } }
    .mtn-stat {
      background: white; border: 1px solid rgba(227,223,255,0.9); border-radius: 16px;
      padding: 10px 12px; box-shadow: 0 2px 10px rgba(99,14,212,0.05);
    }
    .mtn-card {
      background: white; border: 1px solid rgba(227,223,255,0.95); border-radius: 18px;
      padding: 12px; display: flex; align-items: center; gap: 12px;
      box-shadow: 0 2px 12px rgba(99,14,212,0.06);
      cursor: pointer; transition: transform .18s ease, box-shadow .18s ease;
      animation: mtnRise .5s cubic-bezier(0.22,1,0.36,1) both;
    }
    .mtn-card:hover { box-shadow: 0 6px 18px rgba(99,14,212,0.12); }
    .mtn-card:active { transform: scale(0.977); }
    @keyframes mtnRise { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
    .mtn-icon-wrap {
      width: 52px; height: 52px; border-radius: 16px; flex-shrink: 0;
      display: flex; align-items: center; justify-content: center; font-size: 24px;
      position: relative;
    }
    .mtn-bar { height: 8px; background: rgba(237,233,254,0.9); border-radius: 5px; overflow: hidden; }
    .mtn-bar-fill { height: 100%; border-radius: 5px; transition: width 1s cubic-bezier(0.4,0,0.2,1); }
    .mtn-conquered {
      background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
      border-color: rgba(245,158,11,0.45);
    }'''

NEW_MOUNTAIN_HTML = '''  <!-- Mountain Modal (REBUILT) -->
  <div id="mountainModal" class="modal-sheet hidden fixed bottom-0 left-0 right-0 z-[61] bg-surface rounded-t-[32px] border-t border-surface-container-highest max-w-lg mx-auto max-h-[92vh] overflow-y-auto">
    <div class="sticky top-0 bg-surface/95 backdrop-blur-md p-4 border-b border-surface-container-highest flex items-center justify-between z-10">
      <button onclick="closeAllModals()" class="w-8 h-8 rounded-full bg-surface-container-lowest border border-outline-variant flex items-center justify-center text-on-surface active:scale-90">
        <span class="material-symbols-outlined text-[20px]">arrow_forward</span>
      </button>
      <div class="flex items-center gap-2">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-primary to-agent-secondary flex items-center justify-center shadow-md">
          <span class="material-symbols-outlined text-[17px] text-white">mountain_flag</span>
        </div>
        <h3 class="font-bold text-on-surface text-base">کوه‌های من</h3>
      </div>
      <div class="w-8"></div>
    </div>
    <div class="p-5 flex flex-col gap-4" id="mountainModalBody"></div>
  </div>'''

NEW_MOUNTAIN_JS = '''    // ================= MY MOUNTAINS (REBUILT) =================
    function mountainStats() {
      const totalMountains = state.habits.length;
      const totalStreakDays = state.habits.reduce((s, h) => s + (h.streak || 0), 0);
      const conquered = state.habits.filter(h => Math.min(1, (h.streak || 0) / (h.duration || 21)) >= 0.95).length;
      const avgGrowth = totalMountains > 0
        ? state.habits.reduce((s, h) => s + Math.min(1, (h.streak || 0) / (h.duration || 21)), 0) / totalMountains
        : 0;
      return { totalMountains, totalStreakDays, conquered, avgGrowth, overallPercent: Math.round(avgGrowth * 100) };
    }

    function mountainStage(percent) {
      if (percent >= 95) return { emoji: '🏆', name: 'فتح قله', message: 'قله را فتح کردی! تو یک قهرمانی 🏆' };
      if (percent >= 75) return { emoji: '🏔️', name: 'نزدیک قله', message: 'به قله نزدیک شدی؛ آخرین تلاش را بکن' };
      if (percent >= 50) return { emoji: '🧗', name: 'نیمه‌راه', message: 'نیمه راه را طی کردی؛ قله نزدیک است' };
      if (percent >= 25) return { emoji: '⛺', name: 'پایگاه اول', message: 'پایگاه اول را فتح کردی؛ ادامه بده' };
      if (percent > 0) return { emoji: '🥾', name: 'شروع مسیر', message: 'قدم‌های اول را برداشتی؛ مسیر آغاز شده' };
      return { emoji: '🥾', name: 'آماده صعود', message: 'اولین قدم را بردار و مسیر صعود را آغاز کن' };
    }

    function mountainHeroSvg() {
      return `<svg class="mtn-hero-svg" viewBox="0 0 400 100" preserveAspectRatio="none" aria-hidden="true">
        <path d="M0 100 L60 46 L105 72 L175 20 L245 76 L310 38 L400 100 Z" fill="rgba(255,255,255,0.13)"/>
        <path d="M140 100 L228 24 L316 100 Z" fill="rgba(255,255,255,0.20)"/>
        <path d="M210 40 L228 24 L246 40 L237 47 L228 40 L219 47 Z" fill="rgba(255,255,255,0.75)"/>
        <line x1="228" y1="24" x2="228" y2="10" stroke="rgba(255,255,255,0.85)" stroke-width="2"/>
        <path d="M228 10 L242 14 L228 19 Z" fill="#fbbf24"/>
        <circle cx="356" cy="20" r="11" fill="rgba(255,255,255,0.45)"/>
        <ellipse cx="70" cy="26" rx="26" ry="7" fill="rgba(255,255,255,0.30)"/>
        <ellipse cx="320" cy="52" rx="22" ry="6" fill="rgba(255,255,255,0.22)"/>
      </svg>`;
    }

    function renderMountains() {
      const container = document.getElementById('mountainModalBody');
      if (!container) return;
      const stats = mountainStats();
      const stage = mountainStage(stats.overallPercent);

      if (stats.totalMountains === 0) {
        container.innerHTML = `
          <div class="text-center py-10 px-4">
            <div class="text-6xl mb-4 opacity-60">🏔️</div>
            <h4 class="font-bold text-on-surface text-base mb-1.5">هنوز کوهی برای صعود نساخته‌ای</h4>
            <p class="text-xs text-on-surface-variant leading-relaxed mb-5">هر عادت یک کوه است؛ با هر روز استمرار، یک قدم به قله نزدیک‌تر می‌شوی.</p>
            <button onclick="closeAllModals(); setTimeout(() => openModal('addHabitModal'), 120);" class="agent-btn agent-btn-primary mx-auto px-8">
              <span class="material-symbols-outlined text-[18px]">add</span>
              ساخت اولین کوه
            </button>
          </div>
        `;
        return;
      }

      const cards = state.habits.map((habit, i) => {
        const duration = habit.duration || 21;
        const streak = habit.streak || 0;
        const growth = Math.min(1, streak / duration);
        const percent = Math.round(growth * 100);
        const isConquered = growth >= 0.95;
        const remaining = Math.max(0, duration - streak);
        const cat = categories[habit.category] || categories.productivity;
        const accent = isConquered ? '#f59e0b' : cat.color;
        return `
        <div class="mtn-card ${isConquered ? 'mtn-conquered' : ''}" style="animation-delay: ${i * 0.06}s" onclick="openMountainDetail('${habit.id}')">
          <div class="mtn-icon-wrap" style="background: ${cat.color}1c; border: 1.5px solid ${cat.color}59;">
            ${habit.icon || '🏔️'}
            ${isConquered ? '<span class="absolute -top-1.5 -left-1.5 text-[13px]">🏆</span>' : ''}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between gap-2 mb-1.5">
              <div class="flex items-center gap-1.5 min-w-0">
                <span class="text-[13px] font-bold text-on-surface truncate">${habit.name}</span>
                <span class="text-[8.5px] font-bold px-1.5 py-0.5 rounded-md flex-shrink-0 whitespace-nowrap" style="color: ${cat.color}; background: ${cat.color}1a;">${cat.emoji} ${cat.label}</span>
              </div>
              <span class="text-[13px] font-black flex-shrink-0" style="color: ${accent};">${toPersian(percent)}٪</span>
            </div>
            <div class="mtn-bar mb-1.5"><div class="mtn-bar-fill" style="width: ${percent}%; background: linear-gradient(90deg, ${cat.color}, ${isConquered ? '#fbbf24' : cat.color + 'b3'});"></div></div>
            <div class="flex items-center justify-between text-[9.5px] text-on-surface-variant">
              <span>🔥 ${toPersian(streak)} روز پیوستگی</span>
              <span class="font-bold" style="color: ${accent};">${isConquered ? '🏆 قله فتح شد' : toPersian(remaining) + ' روز تا قله'}</span>
            </div>
          </div>
        </div>`;
      }).join('');

      container.innerHTML = `
        <div class="mtn-hero">
          ${mountainHeroSvg()}
          <div class="relative z-10">
            <div class="flex items-center justify-between mb-3">
              <span class="mtn-stage-chip">${stage.emoji} مرحله: ${stage.name}</span>
              <span class="text-[10px] font-bold opacity-80">کوهستان اراده</span>
            </div>
            <div class="flex items-end gap-1.5 mb-3">
              <span class="text-[44px] leading-none font-black">${toPersian(stats.overallPercent)}</span>
              <span class="text-base font-bold opacity-90 mb-1.5">٪ صعود کلی</span>
            </div>
            <div class="mtn-hero-bar mb-3"><div class="mtn-hero-fill" style="width: ${stats.overallPercent}%"></div></div>
            <p class="text-[11.5px] font-semibold opacity-95 leading-relaxed relative z-10">${stage.message} ✨</p>
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2">
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center text-lg flex-shrink-0">🏔️</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.totalMountains)}</div>
              <div class="text-[9px] text-on-surface-variant mt-1">کوه فعال</div>
            </div>
          </div>
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-secondary/10 flex items-center justify-center text-lg flex-shrink-0">🔥</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.totalStreakDays)}</div>
              <div class="text-[9px] text-on-surface-variant mt-1">روزهای پیوستگی</div>
            </div>
          </div>
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-tertiary-fixed flex items-center justify-center text-lg flex-shrink-0">📈</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.overallPercent)}٪</div>
              <div class="text-[9px] text-on-surface-variant mt-1">میانگین رشد</div>
            </div>
          </div>
          <div class="mtn-stat flex items-center gap-2.5">
            <div class="w-9 h-9 rounded-xl bg-primary/10 flex items-center justify-center text-lg flex-shrink-0">🏆</div>
            <div>
              <div class="text-[15px] font-black text-on-surface leading-none">${toPersian(stats.conquered)}</div>
              <div class="text-[9px] text-on-surface-variant mt-1">قله‌های فتح‌شده</div>
            </div>
          </div>
        </div>

        <div class="flex items-center justify-between mt-1">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[18px] text-primary">hiking</span>
            <h4 class="font-bold text-on-surface text-sm">کوه‌های در حال صعود</h4>
          </div>
          <span class="text-[10px] text-on-surface-variant bg-surface-container-low px-2 py-1 rounded-lg border border-surface-container-highest">برای جزئیات بزن</span>
        </div>

        <div class="flex flex-col gap-2.5">
          ${cards}
        </div>
      `;
    }

    function openMountainDetail(habitId) {
      const habit = state.habits.find(h => h.id === habitId);
      if (!habit) return;
      const duration = habit.duration || 21;
      const streak = habit.streak || 0;
      const percent = Math.round(Math.min(1, streak / duration) * 100);
      if (percent >= 95) {
        showToast('🏆 ' + habit.name + ': قله فتح شد! ' + toPersian(streak) + ' روز استمرار');
      } else {
        showToast((habit.icon || '🏔️') + ' ' + habit.name + ': ' + toPersian(percent) + '٪ صعود — ' + toPersian(duration - streak) + ' روز تا قله');
      }
    }'''

# ---------------------------------------------------------------- operations (bottom-up)

# R19: openModal mountainModal case
replace(5674, 5679, "      if (id === 'mountainModal') {\n        renderMountains();\n      }")

# R18: mountain JS section
replace(4266, 4482, NEW_MOUNTAIN_JS)

# R17: renderProgress + renderStats defs
delete(3941, 3963)

# R16: renderAll calls
delete(3928, 3929)

# R15b: agent settings load
delete(3877, 3883)

# R15a: startAgentWakeChecker() call
delete(3868, 3868)

# R14: plan/checkin/analysis/insights/wake JS
delete(3477, 3858)

# R13: switchAgentTab else-ifs
delete(3438, 3447)

# R12: morning messages
delete(2836, 2850)

# R11: speakAgentMessage + weather
delete(2695, 2743)

# R1: Mountain Modal HTML
replace(2119, 2197, NEW_MOUNTAIN_HTML)

# R2..R6: five tab contents
delete(1631, 1897)

# R7: tab buttons
delete(1561, 1565)

# R8: header speak button
delete(1538, 1540)

# R10: Progress Ring
delete(1281, 1301)

# R9: Stats Cards
delete(1270, 1279)

# CSS C6
delete(883, 886)
# CSS C5
delete(790, 851)
# CSS C4
delete(623, 707)
# CSS C0
delete(233, 237)
# CSS C2+C3
delete(193, 205)
# CSS C1
replace(131, 136, NEW_MOUNTAIN_CSS)

# ---------------------------------------------------------------- write
shutil.copyfile(SRC, BAK)
print('Backup saved:', BAK)

with io.open(SRC, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('New line count:', len(lines), '(removed %d lines)' % (orig_count - len(lines)))
print('DONE')
