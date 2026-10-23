# -*- coding: utf-8 -*-
"""Task 7: mobile UX + PWA professionalism fixes for public/app.html.
Bottom-up string edits with hard assertions (fail-safe before write)."""
import io, sys, shutil

PATH = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task7.bak'
src = io.open(PATH, encoding='utf-8').read()
shutil.copyfile(PATH, BAK)

edits = []

# ---------- 1) STREAK CALENDAR GRID: fix clipped 7th column ----------
edits.append((
    """    .streak-days-grid {
      display: grid;
      grid-template-columns: repeat(7, 1fr);
      gap: 8px;
      margin-top: 12px;
    }""",
    """    .streak-days-grid {
      display: grid;
      grid-template-columns: repeat(7, minmax(0, 1fr));
      gap: 6px;
      margin-top: 12px;
    }"""))

edits.append((
    """      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      cursor: pointer;
      position: relative;
      min-height: 52px;
    }""",
    """      transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
      cursor: pointer;
      position: relative;
      min-height: 46px;
    }"""))

edits.append((
    "    .streak-day-label { font-size: 8px; font-weight: 600; opacity: 0.8; }\n    .streak-day-number { font-size: 14px; font-weight: 800; line-height: 1; }",
    "    .streak-day-label { font-size: 9px; font-weight: 600; opacity: 0.8; }\n    .streak-day-number { font-size: 13px; font-weight: 800; line-height: 1; }"))

edits.append((
    """    .streak-calendar-wrapper {
      background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%);
      border-radius: 1.5rem;
      padding: 20px;""",
    """    .streak-calendar-wrapper {
      background: linear-gradient(135deg, #ffffff 0%, #faf5ff 100%);
      border-radius: 1.5rem;
      padding: 16px 14px;"""))

edits.append((
    "    .streak-stat-label { font-size: 9px; color: #4a4455; margin-top: 4px; font-weight: 500; }",
    "    .streak-stat-label { font-size: 10px; color: #4a4455; margin-top: 4px; font-weight: 500; }"))

# ---------- 2) TOUCH TARGETS: chips ----------
edits.append((
    """    .category-filter-chip {
      padding: 6px 14px;
      border-radius: 100px;
      font-size: 11px;""",
    """    .category-filter-chip {
      padding: 9px 16px;
      border-radius: 100px;
      font-size: 11.5px;"""))

edits.append((
    """    .streak-cat-tab {
      padding: 6px 12px;
      border-radius: 100px;
      font-size: 10px;""",
    """    .streak-cat-tab {
      padding: 8px 14px;
      border-radius: 100px;
      font-size: 10.5px;"""))

# ---------- 3) HEADER BUTTONS: 36px -> 40px (main header 3 buttons) ----------
edits.append((
    """        <button onclick="openModal('agentModal')" class="relative w-9 h-9 rounded-full bg-gradient-to-br from-agent-primary/20 to-agent-secondary/20 border border-agent-primary/30 flex items-center justify-center text-agent-primary active:scale-90 transition-transform">
          <span class="material-symbols-outlined text-[20px]">smart_toy</span>""",
    """        <button onclick="openModal('agentModal')" aria-label="دستیار هوشمند" class="relative w-10 h-10 rounded-full bg-gradient-to-br from-agent-primary/20 to-agent-secondary/20 border border-agent-primary/30 flex items-center justify-center text-agent-primary active:scale-90 transition-transform">
          <span class="material-symbols-outlined text-[21px]">smart_toy</span>"""))

edits.append((
    """        <button onclick="openModal('notificationsModal')" class="relative w-9 h-9 rounded-full bg-gradient-to-br from-amber-400/25 to-orange-500/25 border border-amber-500/30 flex items-center justify-center text-amber-600 active:scale-90 transition-transform" title="اعلان‌ها و یادآورها">""",
    """        <button onclick="openModal('notificationsModal')" aria-label="اعلان‌ها و یادآورها" class="relative w-10 h-10 rounded-full bg-gradient-to-br from-amber-400/25 to-orange-500/25 border border-amber-500/30 flex items-center justify-center text-amber-600 active:scale-90 transition-transform" title="اعلان‌ها و یادآورها">"""))

edits.append((
    """        <button onclick="openModal('profileModal')" class="w-9 h-9 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface-variant active:scale-90 transition-transform">
          <span class="material-symbols-outlined text-[20px]">person</span>""",
    """        <button onclick="openModal('profileModal')" aria-label="پروفایل" class="w-10 h-10 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface-variant active:scale-90 transition-transform">
          <span class="material-symbols-outlined text-[21px]">person</span>"""))

# ---------- 4) MUSIC PAGE HEADER BUTTONS: 36px -> 40px ----------
edits.append((
    """            <button onclick="closeMusicPage()" class="w-9 h-9 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface active:scale-90 transition-transform">""",
    """            <button onclick="closeMusicPage()" aria-label="بازگشت" class="w-10 h-10 rounded-full bg-surface-container-low border border-surface-container-highest flex items-center justify-center text-on-surface active:scale-90 transition-transform">"""))

edits.append((
    """        <button id="musicVoiceBtnHeader" onclick="startMusicVoice()" class="w-9 h-9 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center text-primary active:scale-90 transition-transform" title="پخش با صدا">""",
    """        <button id="musicVoiceBtnHeader" onclick="startMusicVoice()" aria-label="پخش با صدا" class="w-10 h-10 rounded-full bg-primary/10 border border-primary/30 flex items-center justify-center text-primary active:scale-90 transition-transform" title="پخش با صدا">"""))

# ---------- 5) "مدیریت همه" tiny link -> proper chip ----------
edits.append((
    """        <button onclick="openModal('addHabitModal')" class="text-[11px] font-bold text-primary flex items-center gap-0.5 hover:underline">
          <span>مدیریت همه</span>""",
    """        <button onclick="openModal('addHabitModal')" class="text-[11px] font-bold text-primary bg-primary/10 px-3 py-2 rounded-full flex items-center gap-0.5 active:scale-95 transition-transform">
          <span>مدیریت همه</span>"""))

# ---------- 6) EMPTY HABITS STATE: add CTA button ----------
old_empty = """        list.innerHTML = `<div class="text-center py-8 text-on-surface-variant"><span class="text-4xl block mb-2 opacity-50">🏔️</span><p class="text-sm font-medium">${state.habits.length === 0 ? 'هنوز عادتی نساختی' : 'عادتی در این دسته نیست'}</p></div>`;"""
new_empty = """        const emptyMsg = state.habits.length === 0 ? 'هنوز عادتی نساختی' : 'عادتی در این دسته نیست';
        const emptyCta = state.habits.length === 0 ? 'ساخت اولین عادت' : 'افزودن عادت جدید';
        list.innerHTML = `<div class="text-center py-8 text-on-surface-variant"><span class="text-4xl block mb-2 opacity-50">🏔️</span><p class="text-sm font-medium mb-3">${emptyMsg}</p><button onclick="openModal('addHabitModal')" class="px-5 py-3 rounded-2xl bg-gradient-to-br from-primary-container to-primary text-on-primary text-xs font-bold shadow-lg active:scale-95 transition-transform inline-flex items-center gap-1.5"><span class="material-symbols-outlined text-[17px]">add</span>${emptyCta}</button></div>`;"""
edits.append((old_empty, new_empty))

# ---------- 7) "مسیر پیوستگی تو" 9px -> 10px ----------
edits.append((
    """      html += '<div class="text-[9px] text-on-surface-variant">مسیر پیوستگی تو</div>';""",
    """      html += '<div class="text-[10px] text-on-surface-variant font-medium">مسیر پیوستگی تو</div>';"""))

# ---------- 8) HEAD: PWA + professional meta ----------
old_meta = """  <meta content="#fcf8ff" name="theme-color">
  <title>Habits Tracker | دستیار هوشمند روزانه</title>"""
new_meta = """  <meta content="#fcf8ff" name="theme-color">
  <meta name="description" content="دستیار هوشمند عادت‌سازی فارسی — برنامه‌ی شخصی با هوش مصنوعی، کوه‌های پیشرفت، تقویم استریک، کتابخانه موزیک و یادآور روزانه.">
  <meta name="mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="Habits Tracker">
  <meta name="application-name" content="Habits Tracker">
  <link rel="manifest" href="/manifest.webmanifest">
  <link rel="icon" type="image/png" sizes="32x32" href="/icons/icon-32.png">
  <link rel="icon" type="image/png" sizes="192x192" href="/icons/icon-192.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/icons/icon-180.png">
  <title>Habits Tracker | دستیار هوشمند روزانه</title>"""
edits.append((old_meta, new_meta))

# ---------- APPLY (all must match) ----------
fail = [i for i, (o, n) in enumerate(edits) if o not in src]
if fail:
    for i in fail:
        print('MISSING PATTERN #%d:' % i)
        print(edits[i][0][:180])
        print('---')
    sys.exit('ABORT: %d pattern(s) not found; file untouched.' % len(fail))

for o, n in edits:
    assert src.count(o) == 1, 'pattern not unique: %s' % o[:80]
    src = src.replace(o, n)

io.open(PATH, 'w', encoding='utf-8').write(src)
print('OK: %d edits applied. Backup at %s' % (len(edits), BAK))
