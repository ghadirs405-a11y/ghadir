#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TASK 18 - Patch D: honors cabinet rebuild + developer credit + full notebook
import io, sys

APP = '/home/z/my-project/public/app.html'
src = io.open(APP, encoding='utf-8').read()

def replace_once(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: found %d' % (tag, n)); sys.exit(1)
    print('OK  [%s]' % tag)
    return s.replace(old, new, 1)

# ---------- D1) trophy shelf HTML: add next-goal + honors grid ----------
old_trophy = '''      <!-- Trophy Case -->
      <div class="trophy-shelf rounded-2xl p-4">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px] text-tertiary">military_tech</span>
            <h4 class="font-bold text-on-surface text-sm">ویترین افتخارات</h4>
          </div>
          <span class="text-[10px] text-tertiary font-bold bg-tertiary-fixed px-2 py-0.5 rounded-full" id="trophyCount">۰ کسب شده</span>
        </div>

        <div class="grid grid-cols-5 gap-1.5 mb-3">
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-diamond" id="medalDiamond">
            <div class="medal-shine"></div>
            <span class="text-2xl">💎</span>
            <span class="text-[7px] font-bold text-cyan-900">الماس</span>
            <span class="text-[7px] text-cyan-800">۱۰</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-platinum" id="medalPlatinum">
            <div class="medal-shine"></div>
            <span class="text-2xl"></span>
            <span class="text-[7px] font-bold text-indigo-900">پلاتین</span>
            <span class="text-[7px] text-indigo-800">۷۰</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-gold" id="medalGold">
            <div class="medal-shine"></div>
            <span class="text-2xl">🥇</span>
            <span class="text-[7px] font-bold text-amber-900">طلا</span>
            <span class="text-[7px] text-amber-800">۴۰</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-silver" id="medalSilver">
            <div class="medal-shine"></div>
            <span class="text-2xl">🥈</span>
            <span class="text-[7px] font-bold text-slate-700">نقره</span>
            <span class="text-[7px] text-slate-600">۲۱</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-bronze" id="medalBronze">
            <div class="medal-shine"></div>
            <span class="text-2xl"></span>
            <span class="text-[7px] font-bold text-amber-900">برنز</span>
            <span class="text-[7px] text-amber-800">۷</span>
          </div>
        </div>

        <div class="border-t border-surface-container-highest pt-3 mt-3">
          <h5 class="text-xs font-bold text-on-surface mb-2 flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px] text-primary">local_fire_department</span>
            چالش‌های فعال
          </h5>
          <div class="space-y-2" id="challengesList"></div>
        </div>
      </div>'''
new_trophy = '''      <!-- Trophy Case (TASK 18 REBUILT) -->
      <div class="trophy-shelf rounded-2xl p-4">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[20px] text-tertiary">military_tech</span>
            <h4 class="font-bold text-on-surface text-sm">ویترین افتخارات</h4>
          </div>
          <span class="text-[10px] text-tertiary font-bold bg-tertiary-fixed px-2 py-0.5 rounded-full" id="trophyCount">۰ کسب شده</span>
        </div>

        <div id="nextGoalCard" class="mb-3"></div>

        <div class="grid grid-cols-5 gap-1.5 mb-3">
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-diamond" id="medalDiamond">
            <div class="medal-shine"></div>
            <span class="text-2xl">💎</span>
            <span class="text-[7px] font-bold text-cyan-900">الماس</span>
            <span class="text-[7px] text-cyan-800">۱۰۰</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-platinum" id="medalPlatinum">
            <div class="medal-shine"></div>
            <span class="text-2xl">🏅</span>
            <span class="text-[7px] font-bold text-indigo-900">پلاتین</span>
            <span class="text-[7px] text-indigo-800">۷۰</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-gold" id="medalGold">
            <div class="medal-shine"></div>
            <span class="text-2xl">🥇</span>
            <span class="text-[7px] font-bold text-amber-900">طلا</span>
            <span class="text-[7px] text-amber-800">۴۰</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-silver" id="medalSilver">
            <div class="medal-shine"></div>
            <span class="text-2xl">🥈</span>
            <span class="text-[7px] font-bold text-slate-700">نقره</span>
            <span class="text-[7px] text-slate-600">۲۱</span>
          </div>
          <div class="relative aspect-square rounded-2xl flex flex-col items-center justify-center gap-0.5 medal-bronze" id="medalBronze">
            <div class="medal-shine"></div>
            <span class="text-2xl">🥉</span>
            <span class="text-[7px] font-bold text-amber-900">برنز</span>
            <span class="text-[7px] text-amber-800">۷</span>
          </div>
        </div>

        <div class="border-t border-surface-container-highest pt-3 mt-1">
          <h5 class="text-xs font-bold text-on-surface mb-2 flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px] text-tertiary">workspace_premium</span>
            نشان‌های افتخار
          </h5>
          <div class="grid grid-cols-4 gap-1.5 mb-1" id="honorsGrid"></div>
        </div>

        <div class="border-t border-surface-container-highest pt-3 mt-3">
          <h5 class="text-xs font-bold text-on-surface mb-2 flex items-center gap-1">
            <span class="material-symbols-outlined text-[14px] text-primary">local_fire_department</span>
            چالش‌های فعال
          </h5>
          <div class="space-y-2" id="challengesList"></div>
        </div>
      </div>'''
src = replace_once(src, old_trophy, new_trophy, 'D1.trophy-html')

# ---------- D2) renderTrophyCase rebuild ----------
old_fn_start = '    function renderTrophyCase() {'
old_fn_end = "      document.getElementById('trophyCount').textContent = toPersian(unlockedCount) + ' کسب شده';\n    }"
i0 = src.index(old_fn_start)
i1 = src.index(old_fn_end) + len(old_fn_end)
new_fn = '''    function renderTrophyCase() {
      const container = document.getElementById('trophyCase');
      const maxStreak = state.habits.length > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
      const totalCompletions = state.habits.reduce((acc, h) => acc + Object.keys(h.completions || {}).length, 0);
      const moodCount = (state.moodLog || []).length;
      const noteCount = (state.notebookEntries || []).length;
      const trackCount = (state.musicTracks || []).length;

      const medals = [
        { id: 'medalDiamond', threshold: 100, emoji: '💎', name: 'الماس' },
        { id: 'medalPlatinum', threshold: 70, emoji: '🏅', name: 'پلاتین' },
        { id: 'medalGold', threshold: 40, emoji: '🥇', name: 'طلا' },
        { id: 'medalSilver', threshold: 21, emoji: '🥈', name: 'نقره' },
        { id: 'medalBronze', threshold: 7, emoji: '🥉', name: 'برنز' }
      ];
      medals.forEach(medal => {
        const el = document.getElementById(medal.id);
        if (!el) return;
        if (maxStreak >= medal.threshold) el.classList.remove('medal-locked');
        else el.classList.add('medal-locked');
      });

      // next-goal hero card (TASK 18)
      const goalCard = document.getElementById('nextGoalCard');
      if (goalCard) {
        const next = medals.slice().reverse().find(m => maxStreak < m.threshold);
        if (next) {
          const pct = Math.min(99, Math.round((maxStreak / next.threshold) * 100));
          const remain = next.threshold - maxStreak;
          const cheers = ['اولین مدال نزدیک‌تر از چیزی است که فکر می‌کنی!', 'زنجیره را قطع نکن — مدال بعدی توست!', 'هر روز یک تیک، یک قدم به قله!', 'تو از روز اول قوی‌تری!'];
          goalCard.innerHTML =
            '<div class="rounded-2xl p-3.5 bg-gradient-to-l from-amber-500/15 via-amber-400/5 to-transparent border border-amber-500/30">' +
              '<div class="flex items-center justify-between mb-1.5">' +
                '<div class="flex items-center gap-2"><span class="text-xl">' + next.emoji + '</span>' +
                '<div><div class="text-[12px] font-extrabold text-on-surface">هدف بعدی: مدال ' + next.name + '</div>' +
                '<div class="text-[9.5px] text-on-surface-variant font-bold">' + toPersian(remain) + ' روز استریک دیگر تا فتح!</div></div></div>' +
                '<span class="text-[11px] font-extrabold text-amber-600">' + toPersian(pct) + '٪</span></div>' +
              '<div class="w-full h-2 bg-amber-500/15 rounded-full overflow-hidden"><div class="h-full rounded-full bg-gradient-to-r from-amber-400 to-amber-600 transition-all" style="width:' + pct + '%"></div></div>' +
              '<div class="text-[9.5px] text-on-surface-variant mt-1.5 font-bold">🔥 ' + cheers[Math.floor(Date.now() / 86400000) % cheers.length] + '</div>' +
            '</div>';
        } else {
          goalCard.innerHTML = '<div class="rounded-2xl p-3.5 bg-gradient-to-l from-amber-500/15 to-transparent border border-amber-500/30 text-[12px] font-extrabold text-on-surface">🏆 باورنکردنی است! همه مدال‌های استریک را فتح کردی — تو افسانه‌ی این کوه‌ها هستی!</div>';
        }
      }

      // honors badge grid (TASK 18)
      const perfectDay = (() => {
        const dates = new Set();
        state.habits.forEach(h => Object.keys(h.completions || {}).forEach(d => dates.add(d)));
        if (!state.habits.length) return false;
        for (const d of dates) {
          if (state.habits.every(h => h.completions && h.completions[d])) return true;
        }
        return false;
      })();
      const gratCount = (state.notebookEntries || []).filter(e => (e.tags || []).indexOf('gratitude') !== -1).length + (state.moodLog || []).filter(m => m.gratitude).length;
      const badges = [
        { id: 'first_step', emoji: '👣', name: 'اولین قدم', desc: 'اولین تیک تاریخ', ok: totalCompletions >= 1 },
        { id: 'trio', emoji: '🧩', name: 'سه‌گانه', desc: '۳ عادت همزمان', ok: state.habits.length >= 3 },
        { id: 'week_one', emoji: '🌱', name: 'هفته اول', desc: '۷ تیک کل', ok: totalCompletions >= 7 },
        { id: 'fifty', emoji: '⭐', name: 'پنجاه‌تایی', desc: '۵۰ تیک کل', ok: totalCompletions >= 50 },
        { id: 'conqueror', emoji: '🏔️', name: 'فاتح قله', desc: 'استریک = مدت چالش', ok: state.habits.some(h => (h.streak || 0) >= (h.duration || 21)) },
        { id: 'seven_up', emoji: '🚀', name: 'هفت‌گانه', desc: '۷ عادت فعال', ok: state.habits.length >= 7 },
        { id: 'perfect_day', emoji: '💯', name: 'روز کامل', desc: 'همه عادت‌ها در یک روز', ok: perfectDay },
        { id: 'reflector', emoji: '🪞', name: 'بازتاب‌گر', desc: '۳ بازتاب حال', ok: moodCount >= 3 },
        { id: 'mindful', emoji: '🧠', name: 'خودآگاه', desc: '۷ بازتاب حال', ok: moodCount >= 7 },
        { id: 'writer', emoji: '✍️', name: 'نویسنده', desc: '۵ یادداشت', ok: noteCount >= 5 },
        { id: 'grateful', emoji: '🙏', name: 'شاکر', desc: '۳ سپاس ثبت‌شده', ok: gratCount >= 3 },
        { id: 'music_lover', emoji: '🎧', name: 'موسیقیدان', desc: 'اولین موزیک کتابخانه', ok: trackCount >= 1 }
      ];
      const honorsGrid = document.getElementById('honorsGrid');
      if (honorsGrid) {
        honorsGrid.innerHTML = badges.map(b =>
          '<div class="relative rounded-xl p-2 flex flex-col items-center justify-center gap-0.5 text-center ' + (b.ok ? 'bg-amber-500/10 border border-amber-500/35' : 'bg-surface-container-low border border-surface-container-highest opacity-55') + '" title="' + b.desc + '">' +
            '<span class="text-lg' + (b.ok ? '' : ' grayscale') + '">' + b.emoji + '</span>' +
            '<span class="text-[8px] font-extrabold ' + (b.ok ? 'text-amber-600' : 'text-on-surface-variant') + '">' + b.name + '</span>' +
            '<span class="text-[7px] text-on-surface-variant leading-tight">' + b.desc + '</span>' +
            (b.ok ? '<span class="absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full bg-amber-500 text-white flex items-center justify-center text-[8px] font-black">✓</span>' : '') +
          '</div>'
        ).join('');
      }

      const challengesList = document.getElementById('challengesList');
      const challenges = [
        { id: 'weekly_streak', title: 'چالش هفتگی', desc: '۷ روز متوالی تمام عادت‌ها', progress: Math.min(100, (maxStreak / 7) * 100), reward: '🥉 مدال برنز', unlocked: maxStreak >= 7 },
        { id: 'monthly_streak', title: 'چالش ماهانه', desc: '۲۱ روز پیوستگی', progress: Math.min(100, (maxStreak / 21) * 100), reward: '🥈 مدال نقره', unlocked: maxStreak >= 21 },
        { id: 'master_challenge', title: 'چالش استاد', desc: '۴۰ روز استریک طلایی', progress: Math.min(100, (maxStreak / 40) * 100), reward: '🥇 مدال طلا', unlocked: maxStreak >= 40 },
        { id: 'platinum_challenge', title: 'چالش پلاتین', desc: '۷۰ روز استقامت', progress: Math.min(100, (maxStreak / 70) * 100), reward: '🏅 مدال پلاتین', unlocked: maxStreak >= 70 },
        { id: 'diamond_challenge', title: 'چالش الماس', desc: '۱۰۰ روز افسانه‌ای', progress: Math.min(100, (maxStreak / 100) * 100), reward: '💎 مدال الماس', unlocked: maxStreak >= 100 },
        { id: 'completion_challenge', title: 'چالش تکمیل', desc: '۵۰ تیک کل', progress: Math.min(100, (totalCompletions / 50) * 100), reward: '🏆 نشان استاد', unlocked: totalCompletions >= 50 },
        { id: 'mood_challenge', title: 'چالش خودآگاهی', desc: '۷ روز ثبت حال', progress: Math.min(100, (moodCount / 7) * 100), reward: '💗 نشان آگاهی', unlocked: moodCount >= 7 },
        { id: 'notebook_challenge', title: 'چالش قلم', desc: '۵ یادداشت', progress: Math.min(100, (noteCount / 5) * 100), reward: '📔 نشان نویسنده', unlocked: noteCount >= 5 }
      ];
      if (challengesList) {
        challengesList.innerHTML = challenges.map(ch => `
          <div class="challenge-card">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <span class="text-lg">${ch.unlocked ? '✅' : '🎯'}</span>
                <div>
                  <div class="text-xs font-bold text-on-surface">${ch.title}</div>
                  <div class="text-[9px] text-on-surface-variant">${ch.desc}</div>
                </div>
              </div>
              <span class="text-[9px] font-bold ${ch.unlocked ? 'text-primary' : 'text-on-surface-variant'} bg-white px-2 py-0.5 rounded-full">${ch.reward}</span>
            </div>
            <div class="w-full h-1.5 bg-surface-container-high rounded-full overflow-hidden">
              <div class="h-full bg-gradient-to-r from-primary to-secondary rounded-full transition-all" style="width: ${ch.progress}%"></div>
            </div>
            <div class="text-[9px] text-on-surface-variant mt-1 text-left">${toPersian(Math.round(ch.progress))}٪</div>
          </div>
        `).join('');
      }

      let unlockedCount = badges.filter(b => b.ok).length + medals.filter(m => maxStreak >= m.threshold).length;
      document.getElementById('trophyCount').textContent = toPersian(unlockedCount) + ' کسب شده';
    }'''
src = src[:i0] + new_fn + src[i1:]
print('OK  [D2.trophy-fn]')

# ---------- D3) developer card + version footer ----------
old_about = '''      <!-- About -->
      <p class="text-center text-[9.5px] text-on-surface-variant font-medium pt-1 pb-1">نسخه ۲.۲ · همه داده‌ها فقط روی همین گوشی ذخیره می‌شود 🔒</p>'''
new_about = '''      <!-- Developer credit (TASK 18) -->
      <div class="bg-gradient-to-l from-violet-500/10 via-fuchsia-500/5 to-transparent rounded-2xl p-4 border border-violet-500/25">
        <div class="flex items-center gap-3">
          <img src="${''}" data-robot-src="1" class="w-12 h-12 rounded-2xl object-cover border border-violet-500/40 shadow-sm hidden" id="devRobotImg" alt="ربات">
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-violet-500 to-fuchsia-600 flex items-center justify-center text-white text-xl shadow-md flex-shrink-0" id="devAvatar">👨‍💻</div>
          <div class="flex-1 min-w-0">
            <div class="text-[13px] font-extrabold text-on-surface">غدیر سروری <span class="text-[10px] font-bold text-on-surface-variant">· Ghadir Sarvari</span></div>
            <div class="text-[10.5px] text-on-surface-variant font-bold leading-relaxed">توسعه‌دهنده این اپ — ساخته‌شده با عشق برای ساختن روزهای بهتر 💜</div>
            <div class="text-[9.5px] text-violet-500 font-extrabold mt-0.5">github.com/ghadirs405-a11y</div>
          </div>
        </div>
      </div>

      <!-- About -->
      <p class="text-center text-[9.5px] text-on-surface-variant font-medium pt-1 pb-1">نسخه ۲.۳ · توسعه‌دهنده: غدیر سروری · همه داده‌ها فقط روی همین گوشی ذخیره می‌شود 🔒</p>'''
src = replace_once(src, old_about, new_about, 'D3.dev-card')

# ---------- D4) notebook: search/filter/export UI ----------
old_hist = '''      <div class="border-t border-surface-container-highest pt-4">
        <h4 class="font-bold text-on-surface text-sm mb-3 flex items-center gap-2">
          <span class="material-symbols-outlined text-[18px] text-primary">history</span>
          یادداشت‌های قبلی
        </h4>
        <div id="notebookHistory" class="space-y-2"></div>
      </div>'''
new_hist = '''      <div class="border-t border-surface-container-highest pt-4">
        <div class="flex items-center justify-between mb-2">
          <h4 class="font-bold text-on-surface text-sm flex items-center gap-2">
            <span class="material-symbols-outlined text-[18px] text-primary">history</span>
            یادداشت‌های قبلی
          </h4>
          <button onclick="exportNotebookTxt()" class="w-8 h-8 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface-variant active:scale-90 transition-transform" title="خروجی متن">
            <span class="material-symbols-outlined text-[15px]">download</span>
          </button>
        </div>
        <div class="flex items-center gap-2 bg-surface-container-low border border-surface-container-highest rounded-xl px-3 py-2 mb-2">
          <span class="material-symbols-outlined text-[16px] text-on-surface-variant">search</span>
          <input id="notebookSearch" type="text" placeholder="جستجو در یادداشت‌ها..." oninput="renderNotebookHistory()" class="flex-1 bg-transparent text-[12px] text-on-surface focus:outline-none placeholder:text-on-surface-variant">
        </div>
        <div class="flex gap-1 flex-wrap mb-3" id="notebookFilterRow">
          <button onclick="setNotebookFilter(this,'all')" class="nb-filter text-[9px] px-2 py-1 rounded-full bg-primary text-on-primary border border-primary font-bold">همه</button>
          <button onclick="setNotebookFilter(this,'pinned')" class="nb-filter text-[9px] px-2 py-1 rounded-full bg-surface-container-low text-on-surface-variant border border-surface-container-highest">📌 سنجاق‌شده</button>
          <button onclick="setNotebookFilter(this,'thought')" class="nb-filter text-[9px] px-2 py-1 rounded-full bg-surface-container-low text-on-surface-variant border border-surface-container-highest">💭 فکر</button>
          <button onclick="setNotebookFilter(this,'challenge')" class="nb-filter text-[9px] px-2 py-1 rounded-full bg-surface-container-low text-on-surface-variant border border-surface-container-highest">🔥 چالش</button>
          <button onclick="setNotebookFilter(this,'achievement')" class="nb-filter text-[9px] px-2 py-1 rounded-full bg-surface-container-low text-on-surface-variant border border-surface-container-highest">🏆 دستاورد</button>
          <button onclick="setNotebookFilter(this,'gratitude')" class="nb-filter text-[9px] px-2 py-1 rounded-full bg-surface-container-low text-on-surface-variant border border-surface-container-highest">🙏 سپاس</button>
        </div>
        <div id="notebookHistory" class="space-y-2"></div>
      </div>'''
src = replace_once(src, old_hist, new_hist, 'D4.notebook-ui')

# word counter on textarea
src = replace_once(src,
  '<textarea id="notebookText" rows="6" placeholder="افکار، چالش‌ها، دستاوردها، یا هر چیزی که می‌خواهی به یاد بسپاری..."',
  '<textarea id="notebookText" rows="6" oninput="updateNoteWordCount()" placeholder="افکار، چالش‌ها، دستاوردها، یا هر چیزی که می‌خواهی به یاد بسپاری..."',
  'D4b.textarea')

# ---------- D5) renderNotebookHistory rebuild + new functions ----------
old_rnh_start = '    function renderNotebookHistory() {'
old_rnh_end = '''    function deleteNotebookEntry(id) {'''
i0 = src.index(old_rnh_start)
i1 = src.index(old_rnh_end)
new_rnh = '''    let notebookFilter = 'all';
    function setNotebookFilter(btn, f) {
      notebookFilter = f;
      document.querySelectorAll('#notebookFilterRow .nb-filter').forEach(b => {
        b.classList.remove('bg-primary', 'text-on-primary', 'border-primary');
        b.classList.add('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      });
      btn.classList.remove('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      btn.classList.add('bg-primary', 'text-on-primary', 'border-primary');
      renderNotebookHistory();
    }
    function updateNoteWordCount() {
      const t = (document.getElementById('notebookText') || {}).value || '';
      const words = t.trim() ? t.trim().split(/\\s+/).length : 0;
      let el = document.getElementById('noteWordCount');
      if (!el) {
        el = document.createElement('div');
        el.id = 'noteWordCount';
        el.className = 'text-[9px] text-on-surface-variant font-bold text-left mt-1';
        const ta = document.getElementById('notebookText');
        if (ta && ta.parentElement) ta.parentElement.appendChild(el);
      }
      el.textContent = toPersian(words) + ' واژه';
    }
    function toggleNotePin(id) {
      const e = (state.notebookEntries || []).find(x => x.id === id);
      if (!e) return;
      e.pinned = !e.pinned;
      saveState();
      renderNotebookHistory();
      renderNotebookPreview();
      showToast(e.pinned ? 'یادداشت سنجاق شد 📌' : 'سنجاق برداشته شد');
    }
    function editNotebookEntry(id) {
      const e = (state.notebookEntries || []).find(x => x.id === id);
      const ta = document.getElementById('notebookText');
      if (!e || !ta) return;
      ta.value = e.text;
      state.notebookEntries = state.notebookEntries.filter(x => x.id !== id);
      saveState();
      ta.focus();
      updateNoteWordCount();
      renderNotebookHistory();
      renderNotebookPreview();
      showToast('متن برای ویرایش آماده شد — بعد از تغییر، ذخیره کن ✏️');
    }
    function exportNotebookTxt() {
      try {
        const es = (state.notebookEntries || []).slice().sort((a, b) => (a.date < b.date ? -1 : 1));
        if (!es.length) { showToast('یادداشتی برای خروجی نیست 📔'); return; }
        const lines = es.map(e => '— ' + e.date + ' —\\n' + e.text + ((e.tags && e.tags.length) ? '\\n[' + e.tags.join(', ') + ']' : '') + '\\n');
        const blob = new Blob([lines.join('\\n')], { type: 'text/plain;charset=utf-8' });
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = 'notebook-' + today() + '.txt';
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(() => { try { URL.revokeObjectURL(a.href); } catch (x) {} }, 4000);
        showToast('خروجی یادداشت‌ها ذخیره شد 💾');
      } catch (e) { showToast('خروجی ممکن نشد 😕'); }
    }
    function renderNotebookHistory() {
      const container = document.getElementById('notebookHistory');
      if (!container) return;

      if ((state.notebookEntries || []).length === 0) {
        container.innerHTML = '<div class="text-center text-on-surface-variant text-xs py-4">هنوز یادداشتی نداری</div>';
        return;
      }

      const tagEmojis = { thought: '💭', challenge: '🔥', achievement: '🏆', gratitude: '🙏' };
      const tagLabels = { thought: 'فکر', challenge: 'چالش', achievement: 'دستاورد', gratitude: 'سپاس' };
      const q = ((document.getElementById('notebookSearch') || {}).value || '').trim();
      let list = state.notebookEntries.slice();
      if (q) list = list.filter(e => (e.text || '').indexOf(q) !== -1);
      if (notebookFilter === 'pinned') list = list.filter(e => e.pinned);
      else if (notebookFilter !== 'all') list = list.filter(e => (e.tags || []).indexOf(notebookFilter) !== -1);
      list.sort((a, b) => (b.pinned ? 1 : 0) - (a.pinned ? 1 : 0));

      if (!list.length) {
        container.innerHTML = '<div class="text-center text-on-surface-variant text-xs py-4">نتیجه‌ای یافت نشد 🔍</div>';
        return;
      }

      container.innerHTML = list.slice(0, 30).map(entry => {
        const d = new Date(entry.timestamp);
        const dateStr = d.toLocaleDateString('fa-IR', { day: 'numeric', month: 'short' });
        const timeStr = d.toLocaleTimeString('fa-IR', { hour: '2-digit', minute: '2-digit' });
        const tags = (entry.tags || []).map(t => `<span class="text-[9px] px-1.5 py-0.5 rounded-full bg-primary/10 text-primary">${tagEmojis[t] || ''} ${tagLabels[t] || t}</span>`).join(' ');
        return `
          <div class="notebook-entry ${entry.pinned ? 'border-primary/50' : ''}">
            <div class="flex items-center justify-between mb-1">
              <span class="text-[9px] text-on-surface-variant font-mono">${dateStr} • ${timeStr}${entry.pinned ? ' 📌' : ''}</span>
              <div class="flex items-center gap-1">
                <button onclick="toggleNotePin('${entry.id}')" class="text-on-surface-variant hover:text-primary" title="سنجاق">
                  <span class="material-symbols-outlined text-[14px]">${entry.pinned ? 'push_pin' : 'keep'}</span>
                </button>
                <button onclick="editNotebookEntry('${entry.id}')" class="text-on-surface-variant hover:text-primary" title="ویرایش">
                  <span class="material-symbols-outlined text-[14px]">edit</span>
                </button>
                <button onclick="deleteNotebookEntry('${entry.id}')" class="text-on-surface-variant hover:text-error">
                  <span class="material-symbols-outlined text-[14px]">delete</span>
                </button>
              </div>
            </div>
            <p class="text-xs text-on-surface leading-relaxed mb-1">${escapeHtml(entry.text)}</p>
            ${tags ? `<div class="flex gap-1 flex-wrap">${tags}</div>` : ''}
          </div>
        `;
      }).join('');
    }

'''
src = src[:i0] + new_rnh + src[i1:]
print('OK  [D5.notebook-fn]')

io.open(APP, 'w', encoding='utf-8').write(src)
print('DONE patch D')
