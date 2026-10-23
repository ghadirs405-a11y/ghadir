#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 17a: streak calendar -> Hijri Shamsi (Jalali) month view.
Embeds the standard jalaali conversion (pure JS), renders a navigable
Persian month grid with weekday header, completion states and stats."""
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

# ---------- 1. CSS ----------
rep('''    .streak-day-cell {''',
'''    /* ---- TASK 17: Jalali (Hijri Shamsi) streak month grid ---- */
    .streak-jgrid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px; }
    .streak-jwd { text-align: center; font-size: 9px; font-weight: 800; color: #9aa3c0; padding: 2px 0 6px; }
    .streak-jday { aspect-ratio: 1; border-radius: 11px; display: flex; align-items: center; justify-content: center; font-size: 12.5px; font-weight: 800; color: #eef1ff; background: rgba(255,255,255,0.04); border: 1px solid #2a2354; position: relative; cursor: pointer; transition: all 0.2s; min-height: 38px; }
    .streak-jday:hover { transform: scale(1.1); z-index: 5; }
    .streak-jday.completed { background: linear-gradient(135deg, #0e7490, #7c3aed); border-color: rgba(34,211,238,0.55); box-shadow: 0 0 10px rgba(34,211,238,0.25); }
    .streak-jday.partial { background: rgba(139,92,246,0.18); border-color: #a78bfa; color: #c4b5fd; }
    .streak-jday.today { background: #1b1345; border: 2px solid #fbbf24; color: #fde68a; box-shadow: 0 0 0 3px rgba(251,191,36,0.18); transform: scale(1.07); }
    .streak-jday.future { opacity: 0.32; }
    .streak-jcheck { position: absolute; top: 2px; left: 4px; font-size: 8px; color: #a5f3fc; font-weight: 900; }
    .streak-jnav { display: flex; align-items: center; gap: 4px; }
    .streak-jnav button { width: 27px; height: 27px; border-radius: 9px; background: rgba(139,92,246,0.12); border: 1px solid #3d3380; color: #eef1ff; display: flex; align-items: center; justify-content: center; transition: transform 0.15s; }
    .streak-jnav button:active { transform: scale(0.9); }
    .streak-day-cell {''', 1, 'css')

# ---------- 2. jalaali engine + month view ----------
jalali_js = r'''
    // ================= TASK 17: JALALI (HIJRI SHAMSI) ENGINE =================
    function jDiv(a, b) { return ~~(a / b); }
    function jMod(a, b) { return a - ~~(a / b) * b; }
    const JALALI_BREAKS = [-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210, 1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178];
    function jalCal(jy) {
      const bl = JALALI_BREAKS.length, gy = jy + 621;
      let leapJ = -14, jp = JALALI_BREAKS[0], jm, jump = 0, n, i;
      for (i = 1; i < bl; i += 1) {
        jm = JALALI_BREAKS[i];
        jump = jm - jp;
        if (jy < jm) break;
        leapJ = leapJ + jDiv(jump, 33) * 8 + jDiv(jMod(jump, 33), 4);
        jp = jm;
      }
      n = jy - jp;
      leapJ = leapJ + jDiv(n, 33) * 8 + jDiv(jMod(n, 33) + 3, 4);
      if (jMod(jump, 33) === 4 && jump - n === 4) leapJ += 1;
      const leapG = jDiv(gy, 4) - jDiv((jDiv(gy, 100) + 1) * 3, 4) - 150;
      const march = 20 + leapJ - leapG;
      if (jump - n < 6) n = n - jump + jDiv(jump + 4, 33) * 33;
      let leap = jMod(jMod(n + 1, 33) - 1, 4);
      if (leap === -1) leap = 4;
      return { leap: leap, gy: gy, march: march };
    }
    function g2dJ(gy, gm, gd) {
      let d = jDiv((gy + jDiv(gm - 8, 6) + 100100) * 1461, 4) + jDiv(153 * jMod(gm + 9, 12) + 2, 5) + gd - 34840408;
      d = d - jDiv(jDiv(gy + 100100 + jDiv(gm - 8, 6), 100) * 3, 4) + 752;
      return d;
    }
    function d2gJ(jdn) {
      let j = 4 * jdn + 139361631;
      j = j + jDiv(jDiv(4 * jdn + 183187720, 146097) * 3, 4) * 4 - 3908;
      const i = jDiv(jMod(j, 1461), 4) * 5 + 308;
      const gd = jDiv(jMod(i, 153), 5) + 1;
      const gm = jMod(jDiv(i, 153), 12) + 1;
      const gy = jDiv(j, 1461) - 100100 + jDiv(8 - gm, 6);
      return { gy: gy, gm: gm, gd: gd };
    }
    function jalaliFromIso(iso) {
      const p = String(iso).split('-');
      const jdn = g2dJ(+p[0], +p[1], +p[2]);
      let jy = d2gJ(jdn).gy - 621, r = jalCal(jy), jdn1f = g2dJ(r.gy, 3, r.march), k = jdn - jdn1f, jm, jd;
      if (k >= 0) {
        if (k <= 185) { jm = 1 + jDiv(k, 31); jd = jMod(k, 31) + 1; return { jy: jy, jm: jm, jd: jd }; }
        else k -= 186;
      } else { jy -= 1; k += 179; if (r.leap === 1) k += 1; }
      jm = 7 + jDiv(k, 30);
      jd = jMod(k, 30) + 1;
      return { jy: jy, jm: jm, jd: jd };
    }
    function jdnFromJalali(jy, jm, jd) {
      const r = jalCal(jy);
      return g2dJ(r.gy, 3, r.march) + (jm - 1) * 31 - jDiv(jm, 7) * (jm - 7) + jd - 1;
    }
    function gregorianFromJalali(jy, jm, jd) { return d2gJ(jdnFromJalali(jy, jm, jd)); }
    function jalaliMonthLen(jy, jm) {
      if (jm <= 6) return 31;
      if (jm <= 11) return 30;
      return jalCal(jy).leap === 0 ? 30 : 29;
    }
    function isoFromGregorian(gy, gm, gd) { return gy + '-' + String(gm).padStart(2, '0') + '-' + String(gd).padStart(2, '0'); }
    function isoShiftDays(baseIso, shift) {
      const d = new Date(baseIso + 'T00:00:00Z');
      d.setUTCDate(d.getUTCDate() + shift);
      return d.toISOString().split('T')[0];
    }
    function isoToDateObj(iso) { return new Date(iso + 'T00:00:00Z'); }
    const JALALI_MONTHS = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
    const JALALI_WD = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنجشنبه', 'جمعه'];
    let streakJ = { jy: 0, jm: 0 };

    function streakRelevantHabits() {
      if (streakFilterCategory === 'all') return state.habits;
      return state.habits.filter(h => h.category === streakFilterCategory);
    }

    function renderStreakJalali() {
      const wrapper = document.getElementById('streakCalendarWrapper');
      if (!wrapper) return;
      const nowIso = today();
      if (!streakJ.jy) { const j = jalaliFromIso(nowIso); streakJ.jy = j.jy; streakJ.jm = j.jm; }
      const todayJ = jalaliFromIso(nowIso);
      const isCurrentMonth = streakJ.jy === todayJ.jy && streakJ.jm === todayJ.jm;
      const mlen = jalaliMonthLen(streakJ.jy, streakJ.jm);
      const firstG = gregorianFromJalali(streakJ.jy, streakJ.jm, 1);
      const firstDate = isoToDateObj(isoFromGregorian(firstG.gy, firstG.gm, firstG.gd));
      const offset = (firstDate.getUTCDay() + 1) % 7; // Saturday-first grid
      const relevant = streakRelevantHabits();
      const totalStreak = state.habits.length > 0 ? Math.max(...state.habits.map(h => h.streak || 0)) : 0;

      let html = '<div class="streak-category-header">';
      html += '<div class="flex items-center gap-2">';
      html += '<div class="w-8 h-8 rounded-lg bg-gradient-to-br from-primary/20 to-secondary/20 flex items-center justify-center">';
      html += '<span class="material-symbols-outlined text-[18px] text-primary">calendar_month</span>';
      html += '</div>';
      html += '<div>';
      html += `<div class="text-xs font-bold text-on-surface">${JALALI_MONTHS[streakJ.jm - 1]} ${toPersian(streakJ.jy)}</div>`;
      html += '<div class="text-[10px] text-on-surface-variant font-medium">تقویم هجری شمسی</div>';
      html += '</div>';
      html += '</div>';
      html += '<div class="streak-jnav">';
      html += '<button onclick="streakMonthShift(-1)" aria-label="ماه قبل"><span class="material-symbols-outlined text-[16px]">chevron_right</span></button>';
      if (!isCurrentMonth) html += '<button onclick="streakJumpToday()" aria-label="امروز" style="width:auto;padding:0 8px;font-size:9px;font-weight:800;">امروز</button>';
      html += '<button onclick="streakMonthShift(1)" aria-label="ماه بعد"><span class="material-symbols-outlined text-[16px]">chevron_left</span></button>';
      html += `<span class="text-[10px] text-primary font-bold bg-on-primary-container px-2 py-1 rounded-full">${toPersian(totalStreak)} روز</span>`;
      html += '</div>';
      html += '</div>';

      html += '<div class="streak-category-tabs">';
      const cats = [
        { id: 'all', label: 'همه', emoji: '📊' },
        { id: 'spiritual', label: 'معنوی', emoji: '🕊️' },
        { id: 'productivity', label: 'بهره‌وری', emoji: '⚡' },
        { id: 'self-care', label: 'مراقبت', emoji: '💖' },
        { id: 'family', label: 'خانواده', emoji: '👨‍👩👧' }
      ];
      cats.forEach(cat => {
        html += `<button class="streak-cat-tab ${streakFilterCategory === cat.id ? 'active' : ''}" onclick="setStreakFilter('${cat.id}')">${cat.emoji} ${cat.label}</button>`;
      });
      html += '</div>';

      html += '<div class="streak-jgrid" style="margin-bottom:4px;">';
      ['ش', 'ی', 'د', 'س', 'چ', 'پ', 'ج'].forEach(w => { html += `<div class="streak-jwd">${w}</div>`; });
      html += '</div>';

      html += '<div class="streak-jgrid">';
      for (let g = 0; g < offset; g++) html += '<div></div>';
      for (let day = 1; day <= mlen; day++) {
        const g = gregorianFromJalali(streakJ.jy, streakJ.jm, day);
        const dateStr = isoFromGregorian(g.gy, g.gm, g.gd);
        const dObj = isoToDateObj(dateStr);
        const isToday = dateStr === nowIso;
        const isFuture = dObj.getTime() > isoToDateObj(nowIso).getTime() && !isToday;
        let cls = 'streak-jday';
        if (isToday) cls += ' today';
        else if (isFuture) cls += ' future';
        else if (relevant.length > 0 && relevant.every(h => h.completions[dateStr])) cls += ' completed';
        else if (relevant.some(h => h.completions[dateStr])) cls += ' partial';
        const wdName = JALALI_WD[(dObj.getUTCDay() + 1) % 7];
        const doneCount = state.habits.filter(h => h.completions[dateStr]).length;
        const check = (cls.indexOf('completed') > -1) ? '<span class="streak-jcheck">✓</span>' : '';
        html += `<div class="${cls}" title="${wdName} ${toPersian(day)} ${JALALI_MONTHS[streakJ.jm - 1]}" onclick="streakDayTap('${dateStr}')">${toPersian(day)}${check}</div>`;
      }
      html += '</div>';

      const currentStreak = calculateCurrentStreak();
      const longestStreak = calculateLongestStreak(90);
      let rateDays = 0, rateDone = 0;
      for (let day = 1; day <= mlen; day++) {
        const g = gregorianFromJalali(streakJ.jy, streakJ.jm, day);
        const dateStr = isoFromGregorian(g.gy, g.gm, g.gd);
        if (isoToDateObj(dateStr).getTime() > isoToDateObj(nowIso).getTime()) break;
        if (!relevant.length) break;
        rateDays++;
        if (relevant.every(h => h.completions[dateStr])) rateDone++;
      }
      const completionRate = rateDays > 0 ? Math.round((rateDone / rateDays) * 100) : 0;

      html += '<div class="streak-stats-row">';
      html += `<div class="streak-stat-card"><div class="streak-stat-value">${toPersian(currentStreak)}</div><div class="streak-stat-label">استریک فعلی 🔥</div></div>`;
      html += `<div class="streak-stat-card"><div class="streak-stat-value" style="color: #fbbf24;">${toPersian(longestStreak)}</div><div class="streak-stat-label">طولانی‌ترین ⭐</div></div>`;
      html += `<div class="streak-stat-card"><div class="streak-stat-value" style="color: #34d399;">${toPersian(completionRate)}٪</div><div class="streak-stat-label">نرخ تکمیل ${JALALI_MONTHS[streakJ.jm - 1]} 📊</div></div>`;
      html += '</div>';

      wrapper.innerHTML = html;
      document.getElementById('streakTotalLabel').textContent = toPersian(totalStreak) + ' روز';
    }

    function streakMonthShift(delta) {
      let jm = streakJ.jm + delta, jy = streakJ.jy;
      if (jm < 1) { jm = 12; jy -= 1; }
      if (jm > 12) { jm = 1; jy += 1; }
      streakJ = { jy: jy, jm: jm };
      renderStreakJalali();
    }
    function streakJumpToday() {
      const j = jalaliFromIso(today());
      streakJ = { jy: j.jy, jm: j.jm };
      renderStreakJalali();
    }
    function streakDayTap(dateStr) {
      const j = jalaliFromIso(dateStr);
      const done = state.habits.filter(h => h.completions[dateStr]).length;
      const wdName = JALALI_WD[(isoToDateObj(dateStr).getUTCDay() + 1) % 7];
      if (state.habits.length === 0) { showToast(`${wdName} ${toPersian(j.jd)} ${JALALI_MONTHS[j.jm - 1]} ${toPersian(j.jy)}`); return; }
      showToast(`${wdName} ${toPersian(j.jd)} ${JALALI_MONTHS[j.jm - 1]} — ${toPersian(done)} از ${toPersian(state.habits.length)} عادت انجام شد ${done === state.habits.length && done > 0 ? '✅' : done > 0 ? '💪' : '🌱'}`);
    }
'''

rep('''    function renderStreakCalendar() {
      const wrapper = document.getElementById('streakCalendarWrapper');''',
    jalali_js + '''
    function renderStreakCalendar() {
      const wrapper = document.getElementById('streakCalendarWrapper');''', 1, 'jalali-engine')

# route all call sites to the Jalali renderer
c = src.count('      renderStreakCalendar();')
if c != 2:
    fails.append(f'[call-sites] expected 2, found {c}')
else:
    src = src.replace('      renderStreakCalendar();', '      renderStreakJalali();')
    print(f'  ok [call-sites] x{c}')

# ---------- 3. version labels ----------
c = src.count('نسخه ۲.۰')
if c != 2:
    fails.append(f'[boot-version] expected 2, found {c}')
else:
    src = src.replace('نسخه ۲.۰', 'نسخه ۲.۲')
    print('  ok [boot-version] x2')

io.open(P, 'w', encoding='utf-8').write(src)
print(f'done: {orig} -> {len(src)} chars ({len(src)-orig:+d})')
if fails:
    print('FAILURES:')
    for f in fails: print(' ', f)
    sys.exit(1)
print('JALALI PATCHES OK')
