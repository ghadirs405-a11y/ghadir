#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TASK 18 - Patch C: mood & reflection upgrade (home + modal) + plus page (challenge duration & summit route)
import io, sys

APP = '/home/z/my-project/public/app.html'
src = io.open(APP, encoding='utf-8').read()

def replace_once(s, old, new, tag):
    n = s.count(old)
    if n != 1:
        print('FAIL[%s]: found %d' % (tag, n)); sys.exit(1)
    print('OK  [%s]' % tag)
    return s.replace(old, new, 1)

# ---------- C1) mood modal rebuild ----------
old_modal = '''    <div class="p-5 flex flex-col gap-5">
      <div>
        <label class="text-xs font-bold text-on-surface mb-3 block">سطح انرژی عاطفی (۱ تا ۵)</label>
        <div class="flex justify-between gap-2" id="moodScorePicker"></div>
      </div>
      <div>
        <label class="text-xs font-bold text-on-surface mb-2 block">بازتاب روز</label>
        <textarea id="reflectionText" rows="4" placeholder="امروز چه حسی داشتی؟" class="w-full bg-surface-container-low border border-surface-container-highest rounded-xl px-4 py-3 text-sm text-on-surface focus:border-primary focus:outline-none placeholder:text-on-surface-variant resize-none"></textarea>
      </div>
      <div class="bg-surface-container-low rounded-2xl p-3 flex items-start gap-2 border border-surface-container-highest">
        <span class="material-symbols-outlined text-[16px] text-tertiary flex-shrink-0 mt-0.5">info</span>
        <p class="text-[11px] text-on-surface-variant leading-relaxed">با ثبت منظم حال و بازتاب، می‌توانی رابطه‌ی بین عادت‌ها و سلامت روانت را بهتر درک کنی.</p>
      </div>
      <button onclick="saveMoodAndReflection()" class="w-full py-3.5 rounded-xl bg-primary text-on-primary font-bold text-sm active:scale-95 transition-transform shadow-md">ذخیره حال و بازتاب</button>
    </div>
  </div>

  <!-- Mood Chart Modal -->'''
new_modal = '''    <div class="p-5 flex flex-col gap-5">
      <div>
        <label class="text-xs font-bold text-on-surface mb-3 block">سطح انرژی عاطفی (۱ تا ۵)</label>
        <div class="flex justify-between gap-2" id="moodScorePicker"></div>
      </div>
      <div>
        <label class="text-xs font-bold text-on-surface mb-2 block">حال تو با کدام جمله نزدیک‌تر است؟</label>
        <div class="grid grid-cols-3 gap-1.5" id="moodFeelingChips">
          <button type="button" onclick="pickMoodFeeling(this,'آرام')" class="mood-feel py-2 rounded-xl text-[11px] font-bold bg-surface-container-low border border-surface-container-highest text-on-surface-variant active:scale-95 transition-all">😌 آرام</button>
          <button type="button" onclick="pickMoodFeeling(this,'خوشحال')" class="mood-feel py-2 rounded-xl text-[11px] font-bold bg-surface-container-low border border-surface-container-highest text-on-surface-variant active:scale-95 transition-all">😄 خوشحال</button>
          <button type="button" onclick="pickMoodFeeling(this,'پرانرژی')" class="mood-feel py-2 rounded-xl text-[11px] font-bold bg-surface-container-low border border-surface-container-highest text-on-surface-variant active:scale-95 transition-all">⚡ پرانرژی</button>
          <button type="button" onclick="pickMoodFeeling(this,'خسته')" class="mood-feel py-2 rounded-xl text-[11px] font-bold bg-surface-container-low border border-surface-container-highest text-on-surface-variant active:scale-95 transition-all">😮‍💨 خسته</button>
          <button type="button" onclick="pickMoodFeeling(this,'مضطرب')" class="mood-feel py-2 rounded-xl text-[11px] font-bold bg-surface-container-low border border-surface-container-highest text-on-surface-variant active:scale-95 transition-all">😰 مضطرب</button>
          <button type="button" onclick="pickMoodFeeling(this,'غمگین')" class="mood-feel py-2 rounded-xl text-[11px] font-bold bg-surface-container-low border border-surface-container-highest text-on-surface-variant active:scale-95 transition-all">😔 غمگین</button>
        </div>
      </div>
      <div>
        <label class="text-xs font-bold text-on-surface mb-2 block">بازتاب روز</label>
        <textarea id="reflectionText" rows="3" placeholder="امروز چه گذشت؟ چه چیزی خوب/بد بود؟ (حتی دو خط کوتاه کافی است)" class="w-full bg-surface-container-low border border-surface-container-highest rounded-xl px-4 py-3 text-sm text-on-surface focus:border-primary focus:outline-none placeholder:text-on-surface-variant resize-none"></textarea>
      </div>
      <div class="grid grid-cols-1 gap-2">
        <div class="flex items-center gap-2 bg-surface-container-low border border-surface-container-highest rounded-xl px-3 py-2">
          <span class="text-[16px]">🙏</span>
          <input id="moodGratitude" type="text" placeholder="یک چیزی که امروز بابتش شکرگزار بودی..." class="flex-1 bg-transparent text-[12px] text-on-surface focus:outline-none placeholder:text-on-surface-variant">
        </div>
        <div class="flex items-center gap-2 bg-surface-container-low border border-surface-container-highest rounded-xl px-3 py-2">
          <span class="text-[16px]">🏅</span>
          <input id="moodWin" type="text" placeholder="کوچک‌ترین برد امروزت چه بود؟" class="flex-1 bg-transparent text-[12px] text-on-surface focus:outline-none placeholder:text-on-surface-variant">
        </div>
      </div>
      <div id="moodInsightCard" class="rounded-2xl p-3.5 border border-primary/25 bg-primary/5"></div>
      <div id="moodYesterdayRow" class="text-[11px] text-on-surface-variant"></div>
      <div class="bg-surface-container-low rounded-2xl p-3 flex items-start gap-2 border border-surface-container-highest">
        <span class="material-symbols-outlined text-[16px] text-tertiary flex-shrink-0 mt-0.5">tips_and_updates</span>
        <p class="text-[11px] text-on-surface-variant leading-relaxed">با ثبت منظم، اپ رابطه‌ی عادت‌ها و انرژی‌ات را کشف می‌کند: مثلاً می‌فهمد بعد از ورزش یا مطالعه، حالت چند درجه بهتر می‌شود.</p>
      </div>
      <button onclick="saveMoodAndReflection()" class="w-full py-3.5 rounded-xl bg-primary text-on-primary font-bold text-sm active:scale-95 transition-transform shadow-md flex items-center justify-center gap-2">
        <span class="material-symbols-outlined text-[18px]">favorite</span>
        ذخیره حال و بازتاب
      </button>
    </div>
  </div>

  <!-- Mood Chart Modal -->'''
src = replace_once(src, old_modal, new_modal, 'C1.mood-modal')

# ---------- C2) saveMoodAndReflection ----------
old_save = '''    function saveMoodAndReflection() {
      const text = document.getElementById('reflectionText').value.trim();
      const todayStr = today();
      
      state.moodLog = state.moodLog.filter(m => m.date !== todayStr);
      state.moodLog.push({ date: todayStr, score: selectedMoodScore, reflection: text });

      saveState();
      closeAllModals();
      document.getElementById('reflectionText').value = '';
      showToast('حال و بازتاب امروز ذخیره شد ✍️');
      renderAll();
    }'''
new_save = '''    function saveMoodAndReflection() {
      const text = document.getElementById('reflectionText').value.trim();
      const grat = (document.getElementById('moodGratitude') || {}).value ? document.getElementById('moodGratitude').value.trim() : '';
      const win = (document.getElementById('moodWin') || {}).value ? document.getElementById('moodWin').value.trim() : '';
      const todayStr = today();

      state.moodLog = state.moodLog.filter(m => m.date !== todayStr);
      state.moodLog.push({
        date: todayStr,
        score: selectedMoodScore,
        reflection: text,
        feeling: window.selectedMoodFeeling || '',
        gratitude: grat,
        win: win
      });

      saveState();
      closeAllModals();
      document.getElementById('reflectionText').value = '';
      window.selectedMoodFeeling = '';
      document.querySelectorAll('#moodFeelingChips .mood-feel').forEach(b => b.classList.remove('mood-feel-on'));
      const doneBefore = (state.moodLog || []).length;
      const dayStreak = moodStreakDays();
      showToast('حال و بازتاب امروز ذخیره شد ✍️ (استریک بازتاب: ' + toPersian(dayStreak) + ' روز)');
      try { triggerConfetti(); } catch (e) {}
      if (dayStreak > 0 && dayStreak % 7 === 0) {
        try { addNotification('achievement', 'استریک بازتاب!', toPersian(dayStreak) + ' روز پیوسته حالت را ثبت کردی — خودشناسی حرفه‌ای!', 'psychology'); } catch (e) {}
      }
      renderAll();
    }
    function moodStreakDays() {
      const logs = (state.moodLog || []).map(m => m.date);
      let n = 0;
      const d = new Date();
      for (;;) {
        const iso = d.toISOString().slice(0, 10);
        if (logs.indexOf(iso) !== -1) { n++; d.setDate(d.getDate() - 1); } else break;
      }
      return n;
    }
    function pickMoodFeeling(btn, label) {
      window.selectedMoodFeeling = label;
      document.querySelectorAll('#moodFeelingChips .mood-feel').forEach(b => {
        b.classList.remove('bg-primary', 'text-on-primary', 'border-primary', 'mood-feel-on');
        b.classList.add('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      });
      btn.classList.remove('bg-surface-container-low', 'text-on-surface-variant', 'border-surface-container-highest');
      btn.classList.add('bg-primary', 'text-on-primary', 'border-primary', 'mood-feel-on');
    }
    function renderMoodInsights() {
      const card = document.getElementById('moodInsightCard');
      if (!card) return;
      const logs = (state.moodLog || []).slice().sort((a, b) => (a.date < b.date ? 1 : -1)).slice(0, 7);
      if (!logs.length) {
        card.innerHTML = '<div class="flex items-start gap-2"><span class="text-[18px]">🌱</span><p class="text-[11.5px] text-on-surface-variant leading-relaxed font-medium">هنوز داده‌ای برای تحلیل نداریم. بعد از چند روز ثبت، اینجا می‌گویم مثلاً «روزهایی که مطالعه کردی، حالت ۲۰٪ بهتر بوده».</p></div>';
        const yRow = document.getElementById('moodYesterdayRow');
        if (yRow) yRow.textContent = '';
        return;
      }
      const avg = logs.reduce((a, m) => a + (m.score || 3), 0) / logs.length;
      const recent3 = logs.slice(0, 3).reduce((a, m) => a + (m.score || 3), 0) / 3;
      const prev3 = logs.slice(3, 6);
      const prevAvg = prev3.length ? prev3.reduce((a, m) => a + (m.score || 3), 0) / prev3.length : null;
      const trend = prevAvg === null ? '' : (recent3 >= prevAvg + 0.4 ? ' 📈 روند صعودی — داریم بهتر می‌شویم!' : (recent3 <= prevAvg - 0.4 ? ' 📉 کمی افت کرده‌ایم — خودت را نلا نکن، یک قدم کوچک کافی است.' : ' ➖ روند پایدار.'));
      // correlate: on higher-mood days, which habits were done more?
      const habits = state.habits || [];
      const highDays = logs.filter(m => (m.score || 3) >= 4).map(m => m.date);
      const lowDays = logs.filter(m => (m.score || 3) <= 2).map(m => m.date);
      let corr = '';
      if (highDays.length && lowDays.length) {
        const rates = habits.map(h => {
          const hi = highDays.filter(d => h.completions && h.completions[d]).length / highDays.length;
          const lo = lowDays.filter(d => h.completions && h.completions[d]).length / lowDays.length;
          return { name: h.name || 'عادت', diff: hi - lo };
        }).sort((a, b) => b.diff - a.diff)[0];
        if (rates && rates.diff >= 0.25) corr = '<div class="mt-2 pt-2 border-t border-primary/15 text-[11px] font-bold text-primary">💡 کشف من: روزهایی که «' + rates.name + '» را انجام دادی، حالت معنادار بهتر بوده!</div>';
      }
      const yRow = document.getElementById('moodYesterdayRow');
      if (yRow) {
        const yIso = new Date(Date.now() - 86400000).toISOString().slice(0, 10);
        const yLog = (state.moodLog || []).find(m => m.date === yIso);
        yRow.innerHTML = yLog ? ('دیروز: ' + ['😫', '😕', '😐', '🙂', '🤩'][(yLog.score || 3) - 1] + ' ' + (yLog.feeling ? '· ' + yLog.feeling + ' ' : '') + '· ' + (yLog.reflection ? escapeHtml(yLog.reflection).slice(0, 60) : 'بدون متن')) : 'دیروز ثبت نکردی — امروز شروع کن 🌟';
      }
      const emojis = ['😫', '😕', '😐', '🙂', '🤩'];
      card.innerHTML = '<div class="flex items-center justify-between mb-1.5"><span class="text-[11.5px] font-extrabold text-on-surface">بینش ۷ روز اخیر</span><span class="text-[10px] font-bold text-primary bg-primary/10 px-2 py-0.5 rounded-full">میانگین: ' + avg.toFixed(1).replace(/\\d/g, d => '۰۱۲۳۴۵۶۷۸۹'[d]) + ' از ۵ ' + emojis[Math.min(4, Math.round(avg) - 1)] + '</span></div>' +
        '<p class="text-[11px] text-on-surface-variant leading-relaxed">بر اساس ' + toPersian(logs.length) + ' بازتاب اخیر تو' + (trend ? ' — ' + trend : '') + '</p>' + corr;
    }'''
src = replace_once(src, old_save, new_save, 'C2.save')

# ---------- C3) renderTodayMoodPreview upgrade ----------
old_prev = '''    function renderTodayMoodPreview() {
      const preview = document.getElementById('todayMoodPreview');
      const todayLog = state.moodLog.find(m => m.date === today());
      if (todayLog) {
        const emojis = ['😫', '😕', '😐', '🙂', '🤩'];
        preview.innerHTML = `
          <span class="text-[10px] text-on-surface-variant">امروز:</span>
          <div class="flex items-center gap-2">
            <span class="text-lg">${emojis[todayLog.score - 1]}</span>
            <span class="text-[10px] text-tertiary font-bold">انرژی: ${toPersian(todayLog.score)}/۵</span>
          </div>
        `;
      } else {
        preview.innerHTML = `<span class="text-[10px] text-on-surface-variant">وضعیت امروز:</span><span class="text-[10px] text-on-surface-variant">هنوز ثبت نشده</span>`;
      }
    }'''
new_prev = '''    function renderTodayMoodPreview() {
      const preview = document.getElementById('todayMoodPreview');
      if (!preview) return;
      const emojis = ['😫', '😕', '😐', '🙂', '🤩'];
      const todayLog = (state.moodLog || []).find(m => m.date === today());
      const last7 = [];
      for (let i = 6; i >= 0; i--) {
        const iso = new Date(Date.now() - i * 86400000).toISOString().slice(0, 10);
        const m = (state.moodLog || []).find(x => x.date === iso);
        last7.push(m ? (m.score || 3) : 0);
      }
      const bars = last7.map(s => {
        const h = s ? Math.round(6 + (s / 5) * 16) : 4;
        const c = s >= 4 ? '#34d399' : (s >= 3 ? '#a78bfa' : (s > 0 ? '#f59e0b' : '#e2e0ea'));
        return '<div style="width:7px;height:' + h + 'px;border-radius:3px;background:' + c + ';"></div>';
      }).join('');
      const streak = moodStreakDays();
      if (todayLog) {
        preview.innerHTML = `
          <div class="flex items-center gap-2">
            <span class="text-lg">${emojis[(todayLog.score || 3) - 1]}</span>
            <div class="flex flex-col">
              <span class="text-[10px] text-tertiary font-extrabold">ثبت شد · انرژی ${toPersian(todayLog.score || 3)}/۵${todayLog.feeling ? ' · ' + todayLog.feeling : ''}</span>
              <span class="text-[9px] text-on-surface-variant font-bold">🔥 استریک بازتاب: ${toPersian(streak)} روز</span>
            </div>
          </div>
          <div class="flex items-end gap-1">${bars}</div>
        `;
      } else {
        preview.innerHTML = `
          <div class="flex items-center gap-2">
            <span class="text-[10px] text-on-surface-variant font-bold">وضعیت امروز: هنوز ثبت نشده</span>
            ${streak > 0 ? '<span class="text-[9px] text-tertiary font-extrabold">🔥 ' + toPersian(streak) + ' روز پیوسته — قطع نکن!</span>' : ''}
          </div>
          <div class="flex items-end gap-1">${bars}</div>
        `;
      }
    }'''
src = replace_once(src, old_prev, new_prev, 'C3.preview')

# ---------- C4) openModal hook for insights ----------
anchor_open = '    function openModal(id) {'
idx = src.index(anchor_open)
line_end = src.index('\n', idx)
src = src[:line_end + 1] + "      try { if (id === 'moodModal') renderMoodInsights(); } catch (e) {}\n" + src[line_end + 1:]
print('OK  [C4.openmodal-hook]')

# ---------- C5) plus page: preview box + camps + smart tip ----------
old_box = '''          <!-- Mountain Preview (always visible) -->
          <div class="bg-surface rounded-2xl p-3 border border-surface-container-highest flex flex-col gap-2.5 shadow-inner">
            <div class="flex items-center justify-between text-right px-0.5">
              <span class="text-[11px] font-bold text-primary" id="progressLabel">۰ از ۲۱ روز</span>
              <div class="flex items-center gap-1.5 text-[12px] font-bold text-on-surface">
                <span class="material-symbols-outlined text-[17px] text-primary">linear_scale</span>
                <span class="">پیش‌نمایش مسیر صعود:</span>
              </div>
            </div>
            <div class="relative w-full h-24 bg-gradient-to-b from-sky-100/50 to-surface-container-low rounded-xl overflow-hidden border border-surface-container-highest">
              <svg id="mountainPreviewSvg" viewBox="0 0 300 100" class="w-full h-full" preserveAspectRatio="none"></svg>
            </div>
            <div class="flex items-center justify-between text-[9px] font-bold text-on-surface-variant px-0.5" id="mountainPreviewLabels"></div>
          </div>'''
new_box = '''          <!-- Smart duration advisor (TASK 18) -->
          <div class="flex items-center justify-between gap-2 bg-gradient-to-l from-violet-500/10 via-fuchsia-500/5 to-transparent border border-violet-500/25 rounded-2xl px-3 py-2.5">
            <div class="flex items-center gap-2 min-w-0">
              <span class="material-symbols-outlined text-[17px] text-violet-500">auto_awesome</span>
              <span class="text-[11px] font-bold text-on-surface leading-snug truncate" id="smartTipLine">توصیه هوشمند: برای شروع، ۲۱ روز بهترین تعادل بین «تثبیت» و «طاقت‌فرسا نبودن» است.</span>
            </div>
          </div>
          <div class="flex items-center justify-between gap-2 -mt-1">
            <span class="text-[11px] font-bold text-on-surface-variant">روز سفارشی:</span>
            <div class="flex items-center gap-2">
              <button type="button" onclick="setCustomDuration(-7)" class="w-8 h-8 rounded-xl bg-surface-container-low border border-surface-container-highest text-on-surface font-extrabold active:scale-90 transition-transform">−۷</button>
              <span class="min-w-[64px] text-center text-[13px] font-extrabold text-primary" id="customDurLabel">۲۱ روز</span>
              <button type="button" onclick="setCustomDuration(7)" class="w-8 h-8 rounded-xl bg-surface-container-low border border-surface-container-highest text-on-surface font-extrabold active:scale-90 transition-transform">+۷</button>
              <button type="button" onclick="applyCustomDuration()" class="px-3 h-8 rounded-xl bg-primary text-on-primary text-[10.5px] font-extrabold active:scale-95 transition-transform">اعمال</button>
            </div>
          </div>

          <!-- Mountain Preview (always visible) -->
          <div class="bg-surface rounded-2xl p-3 border border-surface-container-highest flex flex-col gap-2.5 shadow-inner">
            <div class="flex items-center justify-between text-right px-0.5">
              <span class="text-[11px] font-bold text-primary" id="progressLabel">۰ از ۲۱ روز</span>
              <div class="flex items-center gap-1.5 text-[12px] font-bold text-on-surface">
                <span class="material-symbols-outlined text-[17px] text-primary">linear_scale</span>
                <span class="">پیش‌نمایش مسیر صعود:</span>
              </div>
            </div>
            <div class="relative w-full h-24 bg-gradient-to-b from-sky-100/50 to-surface-container-low rounded-xl overflow-hidden border border-surface-container-highest">
              <svg id="mountainPreviewSvg" viewBox="0 0 300 100" class="w-full h-full" preserveAspectRatio="none"></svg>
            </div>
            <div class="flex items-center justify-between text-[9px] font-bold text-on-surface-variant px-0.5" id="mountainPreviewLabels"></div>
          </div>

          <!-- Summit route camps (TASK 18) -->
          <div class="bg-surface rounded-2xl p-3 border border-surface-container-highest flex flex-col gap-2.5">
            <div class="flex items-center gap-1.5 text-[12px] font-bold text-on-surface">
              <span class="material-symbols-outlined text-[17px] text-tertiary">flag_circle</span>
              <span>مسیر قله — کمپ‌های صعود:</span>
            </div>
            <div class="relative flex items-start justify-between gap-1 px-0.5 pt-1" id="campsRow"></div>
            <div class="text-[10px] text-on-surface-variant font-medium leading-relaxed" id="routeEndDate"></div>
          </div>'''
src = replace_once(src, old_box, new_box, 'C5.plus-box')

# ---------- C6) selectDuration tail + new functions ----------
old_tail = '''      renderMountainPreview(duration);
    }'''
new_tail = '''      renderMountainPreview(duration);
      renderChallengeCamps(duration);
      renderSmartTip(duration);
      const cl = document.getElementById('customDurLabel');
      if (cl) cl.textContent = toPersian(duration) + ' روز';
      window.customDuration = duration;
    }

    // ===== TASK 18: summit camps + smart advisor =====
    const JM_NAMES = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند'];
    function jalaliDateAfterOffset(days) {
      try {
        const d = new Date(Date.now() + days * 86400000);
        const iso = d.toISOString().slice(0, 10);
        const j = jalaliFromIso(iso);
        return toPersian(j.jd) + ' ' + JM_NAMES[(j.jm || 1) - 1];
      } catch (e) { return ''; }
    }
    function renderChallengeCamps(duration) {
      const row = document.getElementById('campsRow');
      if (!row) return;
      const camps = [
        { at: 0, label: 'پایگاه', icon: 'camping', desc: 'شروع سفر' },
        { at: 0.25, label: 'کمپ ۱', icon: 'flag', desc: 'گره خوردن' },
        { at: 0.55, label: 'کمپ ۲', icon: 'landscape', desc: 'نیمه راه' },
        { at: 0.85, label: 'کمپ ۳', icon: 'filter_hdr', desc: 'هوای رقیق' },
        { at: 1, label: 'قله', icon: 'emoji_events', desc: 'فتح!' }
      ];
      row.innerHTML = camps.map((c, i) => {
        const day = Math.max(1, Math.round(duration * c.at));
        const date = jalaliDateAfterOffset(day - 1);
        const isPeak = i === camps.length - 1;
        return '<div class="flex flex-col items-center gap-1 flex-1 min-w-0">' +
          '<div class="' + (isPeak ? 'w-9 h-9 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 text-white shadow-md' : 'w-8 h-8 rounded-full bg-primary/10 border border-primary/30 text-primary') + ' flex items-center justify-center">' +
            '<span class="material-symbols-outlined text-[16px]">' + c.icon + '</span></div>' +
          '<span class="text-[9.5px] font-extrabold ' + (isPeak ? 'text-amber-600' : 'text-on-surface') + '">' + c.label + '</span>' +
          '<span class="text-[8.5px] text-on-surface-variant font-bold leading-tight text-center">روز ' + toPersian(day) + '</span>' +
          (date ? '<span class="text-[8px] text-on-surface-variant/80 text-center leading-tight">' + date + '</span>' : '') +
        '</div>';
      }).join('');
      const endEl = document.getElementById('routeEndDate');
      if (endEl) endEl.innerHTML = '🏁 رسیدن به قله: روز ' + toPersian(duration) + ' — حدود <b>' + jalaliDateAfterOffset(duration - 1) + '</b>' + (duration >= 40 ? ' · این مسیر نشان «استاد» دارد 🥇' : '');
    }
    function renderSmartTip(duration) {
      const el = document.getElementById('smartTipLine');
      if (!el) return;
      const durs = (state.habits || []).map(h => h.duration || 21);
      let tip;
      if (duration >= 100) tip = 'ریشه‌داری! مخصوص عادت‌هایی که می‌خواهی هویتت شوند — مسیر طولانی ولی دگرگون‌کننده.';
      else if (duration >= 70) tip = 'چالش استاد 🥇 — فقط برای عادت‌هایی که واقعاً به آن‌ها تعهد داری.';
      else if (duration >= 40) tip = '۴۰ روز، مرز طلایی تثبیت — نصف راه را که بروی، بدن خودش دنبال می‌کند.';
      else if (duration >= 21) tip = '۲۱ روز، تعادل علمی بین ساخت عادت و فرسایش انگیزه — انتخاب هوشمندانه!';
      else if (duration >= 7) tip = '۷ روز، برای آزمودن عادت عالی است — اگر نشست، بعداً به ۲۱ ارتقا بده.';
      else tip = 'چالش کوتاه و سبک — برای شروع‌های بی‌استرس مناسب است.';
      if (durs.length) {
        const avg = Math.round(durs.reduce((a, b) => a + b, 0) / durs.length);
        tip += ' (میانگین چالش‌های قبلی تو: ' + toPersian(avg) + ' روز)';
      }
      el.textContent = 'توصیه هوشمند: ' + tip;
    }
    function setCustomDuration(delta) {
      window.customDuration = Math.max(3, Math.min(365, (window.customDuration || 21) + delta));
      const cl = document.getElementById('customDurLabel');
      if (cl) cl.textContent = toPersian(window.customDuration) + ' روز';
    }
    function applyCustomDuration() {
      const d = window.customDuration || 21;
      document.querySelectorAll('.duration-btn').forEach(el => {
        el.className = 'duration-btn bg-surface-container-low hover:bg-surface-container text-on-surface rounded-xl p-2 flex flex-col items-center justify-center text-center border border-surface-container-highest active:scale-95 transition-all';
      });
      window.selectedDuration = d;
      document.getElementById('progressLabel').textContent = '۰ از ' + toPersian(d) + ' روز';
      document.getElementById('timelineSubtitle').textContent = toPersian(d) + ' روزه (سفارشی) • مسیر صعود به قله';
      renderMountainPreview(d);
      renderChallengeCamps(d);
      renderSmartTip(d);
      showToast('چالش ' + toPersian(d) + ' روزه سفارشی اعمال شد 🎯');
    }'''
src = replace_once(src, old_tail, new_tail, 'C6.duration-fns')

io.open(APP, 'w', encoding='utf-8').write(src)
print('DONE patch C')
