#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 17c: rebuild the profile section from scratch — professional & friendly.
Identity hero (avatar+level+XP), stats grid, Jalali joined date, keeps every
existing feature (notebook, alarms, battery saver, trophies, backup)."""
import io, re, sys

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

# ---------- 1. CSS ----------
rep('''  /* app-start boot splash (short cinematic sequence) */''',
'''  /* ---- TASK 17: professional profile ---- */
  .profile-hero { background: linear-gradient(160deg, rgba(35,26,74,0.88), rgba(17,11,40,0.94)); border: 1px solid #3d3380; border-radius: 1.5rem; box-shadow: 0 10px 30px rgba(0,0,0,0.45), inset 0 1px 0 rgba(139,92,246,0.16); }
  .prof-stat { background: linear-gradient(160deg, rgba(35,26,74,0.88), rgba(17,11,40,0.94)); border: 1px solid #3d3380; border-radius: 1rem; padding: 10px 4px 8px; display: flex; flex-direction: column; align-items: center; gap: 1px; }
  .prof-stat .material-symbols-outlined { font-size: 17px; }
  .profile-avatar-btn { transition: transform 0.15s; border: 2px solid transparent; border-radius: 14px; width: 38px; height: 38px; display: flex; align-items: center; justify-content: center; font-size: 20px; background: rgba(255,255,255,0.05); }
  .profile-avatar-btn:active { transform: scale(0.88); }
  .profile-avatar-btn.sel { border-color: #8b5cf6; background: rgba(139,92,246,0.18); box-shadow: 0 0 10px rgba(139,92,246,0.3); }
  /* app-start boot splash (short cinematic sequence) */''', 1, 'css')

# ---------- 2. replace the whole profile modal block ----------
new_block = '''  <div id="profileModal" class="modal-sheet hidden fixed bottom-0 left-0 right-0 z-[61] bg-surface rounded-t-[32px] border-t border-surface-container-highest max-w-lg mx-auto max-h-[92vh] overflow-y-auto">
    <div class="sticky top-0 bg-surface/95 backdrop-blur-md p-4 border-b border-surface-container-highest flex items-center justify-between z-10">
      <button onclick="closeAllModals()" class="w-8 h-8 rounded-full bg-surface-container-lowest border border-outline-variant flex items-center justify-center text-on-surface active:scale-90">
        <span class="material-symbols-outlined text-[20px]">arrow_forward</span>
      </button>
      <h3 class="font-bold text-on-surface text-base">پروفایل</h3>
      <div class="w-8"></div>
    </div>
    <div class="p-5 flex flex-col gap-4">

      <!-- TASK 17: identity hero -->
      <div class="profile-hero p-5" id="profileHero">
        <div class="flex items-center gap-4">
          <div class="relative flex-shrink-0">
            <div class="w-[72px] h-[72px] rounded-[24px] bg-gradient-to-br from-primary/30 to-secondary/20 border border-primary/40 flex items-center justify-center text-[38px] select-none" id="profileAvatarEl">🦁</div>
            <span class="absolute -bottom-2 -left-2 px-2 py-0.5 rounded-full bg-gradient-to-l from-primary to-secondary text-white text-[9px] font-extrabold shadow-lg whitespace-nowrap" id="profileLevelChip">سطح ۱</span>
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2">
              <h3 class="font-extrabold text-on-surface text-lg truncate" id="profileNameEl">قهرمان عادت‌ها</h3>
              <button onclick="toggleProfileEdit()" aria-label="ویرایش پروفایل" class="w-7 h-7 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface-variant active:scale-90 transition-transform flex-shrink-0">
                <span class="material-symbols-outlined text-[14px]">edit</span>
              </button>
            </div>
            <p class="text-[11px] text-on-surface-variant mt-0.5 font-medium" id="profileJoinedEl">همسفر مسیر قله</p>
            <div class="mt-2.5">
              <div class="flex items-center justify-between text-[9px] font-bold mb-1">
                <span class="text-on-surface-variant" id="profileXpLabel">۰ امتیاز تجربه</span>
                <span class="text-secondary" id="profileNextLvl">تا سطح ۲: ۲۵</span>
              </div>
              <div class="h-2 rounded-full bg-surface-container-highest overflow-hidden">
                <div class="h-full rounded-full bg-gradient-to-l from-primary to-secondary transition-all duration-700" id="profileXpBar" style="width:0%"></div>
              </div>
            </div>
          </div>
        </div>
        <div id="profileEditBox" class="hidden mt-4 pt-4 border-t border-surface-container-highest">
          <label class="text-[10px] font-bold text-on-surface-variant block mb-1.5">نام نمایشی تو</label>
          <input id="profileNameInput" maxlength="24" placeholder="مثلاً: کوهنورد کوچک" class="w-full bg-surface-container-low border border-surface-container-highest rounded-xl px-3 py-2.5 text-sm font-bold text-on-surface focus:outline-none focus:border-primary transition-colors">
          <label class="text-[10px] font-bold text-on-surface-variant block mt-3 mb-2">شکلک اختصاصی‌ات را انتخاب کن</label>
          <div class="flex flex-wrap gap-1.5" id="profileAvatarPicker"></div>
          <button onclick="saveProfileIdentity()" class="mt-4 w-full py-2.5 rounded-xl bg-primary text-white text-xs font-extrabold active:scale-95 transition-transform flex items-center justify-center gap-1.5 shadow-lg">
            <span class="material-symbols-outlined text-[15px]">check_circle</span> ذخیره پروفایل
          </button>
        </div>
      </div>

      <!-- TASK 17: stats grid -->
      <div class="grid grid-cols-4 gap-2" id="profileStats"></div>

      <!-- Daily Notebook -->
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-surface-container-highest">
        <div class="flex items-center justify-between mb-3">
          <div class="flex items-center gap-2">
            <span class="material-symbols-outlined text-[18px] text-primary">auto_stories</span>
            <h4 class="font-bold text-on-surface text-sm">دفترچه یادداشت روزانه</h4>
          </div>
          <button onclick="openModal('notebookModal')" class="text-[10px] text-primary font-bold bg-on-primary-container px-2 py-1 rounded-full flex items-center gap-1">
            <span class="material-symbols-outlined text-[12px]">edit</span>
            نوشتن
          </button>
        </div>
        <div id="notebookPreview" class="space-y-2">
          <div class="text-center text-on-surface-variant text-xs py-4">
            <span class="material-symbols-outlined text-3xl opacity-30 block mb-2">auto_stories</span>
            هنوز یادداشتی ننوشتی. افکار، چالش‌ها و دستاوردهایت را ثبت کن.
          </div>
        </div>
      </div>

      <!-- Alarm Settings -->
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-surface-container-highest">
        <div class="flex items-start gap-3 mb-4">
          <div class="w-10 h-10 rounded-xl bg-surface-container-low flex items-center justify-center text-secondary flex-shrink-0">
            <span class="material-symbols-outlined text-[20px]">alarm</span>
          </div>
          <div class="flex-1">
            <h4 class="font-bold text-on-surface text-sm mb-1">تنظیمات آلارم</h4>
            <p class="text-xs text-on-surface-variant">یادآوری روزانه برای هر عادت</p>
          </div>
        </div>
        <div class="flex flex-col gap-2" id="alarmSettingsList"></div>
      </div>

      <!-- Battery Saver -->
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-surface-container-highest">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-xl bg-surface-container-low flex items-center justify-center text-tertiary flex-shrink-0">
              <span class="material-symbols-outlined text-[20px]">battery_saver</span>
            </div>
            <div>
              <h4 class="font-bold text-on-surface text-sm">حالت ذخیره باتری</h4>
              <p class="text-[10px] text-on-surface-variant">غیرفعال کردن انیمیشن‌ها برای صرفه‌جویی</p>
            </div>
          </div>
          <div class="w-11 h-6 bg-surface-container-highest rounded-full relative cursor-pointer transition-all" id="batterySaverToggle" onclick="toggleBatterySaver()">
            <div class="absolute top-0.5 right-0.5 w-5 h-5 bg-white rounded-full transition-all shadow-sm"></div>
          </div>
        </div>
      </div>

      <!-- Trophy Case -->
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
      </div>

      <!-- Data & backup -->
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-surface-container-highest">
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
      </div>

      <!-- About -->
      <p class="text-center text-[9.5px] text-on-surface-variant font-medium pt-1 pb-1">نسخه ۲.۲ · همه داده‌ها فقط روی همین گوشی ذخیره می‌شود 🔒</p>
    </div>
  </div>

  <!-- Notebook Modal -->'''

m = re.search(r'  <div id="profileModal".*?<!-- Notebook Modal -->', src, re.S)
if not m:
    fails.append('[profile-block] markers not found')
else:
    src = src[:m.start()] + new_block + src[m.end():]
    print(f'  ok [profile-block] replaced {m.end()-m.start()} chars')

# ---------- 3. state migration ----------
rep('''        if (!Array.isArray(state.musicCollections)) state.musicCollections = [];''',
'''        if (!Array.isArray(state.musicCollections)) state.musicCollections = [];
        if (!state.profile || typeof state.profile !== 'object') state.profile = { name: '', avatar: '', joined: state.chellehStartDate || today() };''', 1, 'migration')

# ---------- 4. profile JS ----------
profile_js = r'''
    // ================= TASK 17: PROFILE HERO =================
    const PROFILE_AVATARS = ['🦁', '🐯', '🐺', '🦊', '🐼', '🦅', '🐢', '🦋', '🌸', '🌟', '🚀', '👑'];
    window.__profileDraftAvatar = null;
    function profileXP() {
      let xp = 0;
      state.habits.forEach(h => { Object.values(h.completions || {}).forEach(v => { if (v) xp++; }); });
      return xp;
    }
    function profileJoinedText() {
      const p = state.profile || {};
      let iso = p.joined || null;
      if (!iso && state.habits.length) {
        const dates = state.habits.map(h => h.addedAt).filter(Boolean).sort();
        if (dates.length) iso = dates[0];
      }
      if (!iso) iso = state.chellehStartDate || today();
      try {
        const j = jalaliFromIso(iso);
        return `همسفر از ${toPersian(j.jd)} ${JALALI_MONTHS[j.jm - 1]} ${toPersian(j.jy)}`;
      } catch (e) { return 'همسفر مسیر قله'; }
    }
    function renderProfileHero() {
      if (!state.profile || typeof state.profile !== 'object') state.profile = { name: '', avatar: '', joined: state.chellehStartDate || today() };
      const p = state.profile;
      const av = document.getElementById('profileAvatarEl');
      if (!av) return;
      const avatar = p.avatar || '🦁';
      av.textContent = avatar;
      const xp = profileXP();
      const level = Math.floor(Math.sqrt(xp / 25)) + 1;
      const curBase = 25 * (level - 1) * (level - 1);
      const nextAt = 25 * level * level;
      const pct = Math.min(100, Math.max(0, Math.round(((xp - curBase) / (nextAt - curBase)) * 100)));
      const chip = document.getElementById('profileLevelChip');
      if (chip) chip.textContent = `سطح ${toPersian(level)}`;
      const nameEl = document.getElementById('profileNameEl');
      if (nameEl) nameEl.textContent = p.name || 'قهرمان عادت‌ها';
      const joinedEl = document.getElementById('profileJoinedEl');
      if (joinedEl) joinedEl.textContent = profileJoinedText();
      const xpLbl = document.getElementById('profileXpLabel');
      if (xpLbl) xpLbl.textContent = `${toPersian(xp)} امتیاز تجربه`;
      const nextEl = document.getElementById('profileNextLvl');
      if (nextEl) nextEl.textContent = `تا سطح ${toPersian(level + 1)}: ${toPersian(nextAt - xp)} تیک`;
      const bar = document.getElementById('profileXpBar');
      if (bar) bar.style.width = pct + '%';
      const stats = document.getElementById('profileStats');
      if (stats) {
        const active = state.habits.length;
        const best = active > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;
        const nowIso = today();
        let fullDays = 0;
        for (let i = 0; i < 30; i++) {
          const ds = isoShiftDays(nowIso, -i);
          if (active > 0 && state.habits.every(h => h.completions[ds])) fullDays++;
        }
        const cells = [
          { icon: 'checklist', color: 'text-primary', v: toPersian(active), l: 'عادت فعال' },
          { icon: 'task_alt', color: 'text-emerald-400', v: toPersian(xp), l: 'کل تیک‌ها' },
          { icon: 'local_fire_department', color: 'text-amber-400', v: toPersian(best), l: 'بهترین استریک' },
          { icon: 'calendar_month', color: 'text-sky-400', v: toPersian(fullDays), l: 'روز کامل (۳۰)' }
        ];
        stats.innerHTML = cells.map(c => `<div class="prof-stat"><span class="material-symbols-outlined ${c.color}">${c.icon}</span><span class="text-base font-extrabold text-on-surface leading-none">${c.v}</span><span class="text-[8.5px] font-bold text-on-surface-variant">${c.l}</span></div>`).join('');
      }
      const picker = document.getElementById('profileAvatarPicker');
      if (picker && !picker.dataset.built) {
        picker.dataset.built = '1';
        picker.innerHTML = PROFILE_AVATARS.map(e => `<button type="button" class="profile-avatar-btn ${e === avatar ? 'sel' : ''}" data-e="${e}" onclick="setProfileAvatar('${e}')">${e}</button>`).join('');
      }
    }
    function toggleProfileEdit() {
      const box = document.getElementById('profileEditBox');
      if (!box) return;
      const willShow = box.classList.contains('hidden');
      box.classList.toggle('hidden');
      if (willShow) {
        const p = state.profile || {};
        const inp = document.getElementById('profileNameInput');
        if (inp) inp.value = p.name || '';
        window.__profileDraftAvatar = null;
        renderProfileHero();
        refreshAvatarPickerSel();
        try { box.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } catch (e) {}
      }
    }
    function refreshAvatarPickerSel() {
      const picker = document.getElementById('profileAvatarPicker');
      if (!picker) return;
      const cur = window.__profileDraftAvatar || (state.profile && state.profile.avatar) || '🦁';
      picker.querySelectorAll('.profile-avatar-btn').forEach(b => {
        b.classList.toggle('sel', b.dataset.e === cur);
      });
    }
    function setProfileAvatar(e) {
      window.__profileDraftAvatar = e;
      refreshAvatarPickerSel();
    }
    function saveProfileIdentity() {
      const inp = document.getElementById('profileNameInput');
      const name = (inp && inp.value || '').trim().slice(0, 24);
      state.profile = state.profile || { joined: today() };
      state.profile.name = name;
      if (window.__profileDraftAvatar) state.profile.avatar = window.__profileDraftAvatar;
      if (!state.profile.joined) state.profile.joined = today();
      saveState();
      window.__profileDraftAvatar = null;
      const box = document.getElementById('profileEditBox');
      if (box) box.classList.add('hidden');
      renderProfileHero();
      showToast('پروفایل ذخیره شد ✨');
    }
'''

rep('''    // ================= STREAK CALENDAR =================''', profile_js + '''
    // ================= STREAK CALENDAR =================''', 1, 'profile-js')

# ---------- 5. hook into renderAll ----------
rep('''      renderNotifications();
    }''', '''      renderNotifications();
      renderProfileHero();
    }''', 1, 'renderAll-hook')

io.open(P, 'w', encoding='utf-8').write(src)
print(f'done: {orig} -> {len(src)} chars ({len(src)-orig:+d})')
if fails:
    print('FAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('PROFILE PATCHES OK')
