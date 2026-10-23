# -*- coding: utf-8 -*-
"""
Remove the following sections from public/app.html (per user request):
  1. "۲ روز استریک" badge (in progress ring card)
  2. "مسیر پیشرفت تو" (timeline progress)
  3. "خلاصه هفتگی" (weekly bar chart)
  4. "نکته مراقبه لحظه‌ای" (mindfulness tip)
  5. "مسیر احساسی ۳۰ روزه" (30-day mood chart in profile)
  6. "آمار کلی" (profile stats)
  7. "سپر آرامش" (emergency modal + header button + breathing JS)
  8. "کوه نمادین اراده و پیشرفت" (mountain symbol card in add-habit modal)
  9. "سپر اراده و یادداشت قلبی" (shield card in add-habit modal)
  10. Stat cards "رهایی و پاکی" + "طراوت ذهن" (keep "عادت‌های امروز")
Plus all related JS functions/calls so nothing breaks.
"""
import io, re, sys

PATH = '/home/z/my-project/public/app.html'
with io.open(PATH, encoding='utf-8') as f:
    lines = f.read().split('\n')

LOG = []

def find_one(pred, desc, start=0):
    idxs = [i for i, l in enumerate(lines) if i >= start and pred(l)]
    assert len(idxs) == 1, "%s: expected exactly 1 match, got %d" % (desc, len(idxs))
    return idxs[0]

def find_from(pred, desc, start):
    idxs = [i for i, l in enumerate(lines) if i >= start and pred(l)]
    assert idxs, "%s: no match from index %d" % (desc, start)
    return idxs[0]

def remove(start, end, desc):
    assert 0 <= start < end <= len(lines), "%s: bad range %d:%d" % (desc, start, end)
    del lines[start:end]
    LOG.append("removed lines %d..%d -> %s" % (start + 1, end, desc))

def remove_block(s_pred, e_pred, desc, s_assert=None, e_assert=None):
    s = find_one(s_pred, desc + ' [start]')
    e = find_from(e_pred, desc + ' [end]', s + 1)
    if s_assert:
        for off, chk in s_assert:
            assert chk(lines[s + off]), "%s: start assert failed at +%d" % (desc, off)
    if e_assert:
        for off, chk in e_assert:
            assert chk(lines[e + off]), "%s: end assert failed at %+d" % (desc, off)
    remove(s, e, desc)

def remove_single(pred, desc):
    i = find_one(pred, desc)
    remove(i, i + 1, desc)

# ---------- 1. Header "سپر آرامش" (emergency) button ----------
i = find_one(lambda l: "openModal('emergencyModal')" in l, 'header emergency button')
assert 'shield' in lines[i + 1] and lines[i + 2].strip() == '</button>'
remove(i, i + 3, 'header emergency button (سپر آرامش trigger)')

# ---------- 2. Stats cards: keep "عادت‌های امروز", remove "رهایی و پاکی" + "طراوت ذهن" ----------
i = find_one(lambda l: l == '    <div class="grid grid-cols-3 gap-2.5 mb-6">', 'stats grid container')
lines[i] = '    <div class="mb-6">'
LOG.append('stats grid container -> single card wrapper')

i = find_one(lambda l: 'id="statPurityDays"' in l, 'statPurityDays card')
assert 'rounded-2xl p-3 flex flex-col' in lines[i - 4]
assert lines[i - 1].strip() == '</div>'
assert 'رهایی و پاکی' in lines[i + 1]
assert 'id="statMindFresh"' in lines[i + 7]
assert 'طراوت ذهن' in lines[i + 8]
assert lines[i + 9].strip() == '</div>'   # closes "طراوت ذهن" card
assert lines[i + 10].strip() == '</div>'  # container close, must survive
remove(i - 4, i + 10, 'stat cards "رهایی و پاکی" + "طراوت ذهن"')

# ---------- 3. "۲ روز استریک" badge in progress ring ----------
i = find_one(lambda l: 'bg-tertiary-fixed/50 border border-tertiary-fixed' in l, 'streak badge box')
assert '\U0001F525' in lines[i + 1]                       # 🔥
assert 'id="streakCount"' in lines[i + 2]
assert lines[i + 3].strip() == '</div>'
remove(i, i + 4, '"۲ روز استریک" badge')

# ---------- 4. "مسیر پیشرفت تو" + "خلاصه هفتگی" sections ----------
remove_block(
    lambda l: '<!-- Timeline Progress -->' in l,
    lambda l: '<!-- Category Filter -->' in l,
    'sections "مسیر پیشرفت تو" + "خلاصه هفتگی"')

# ---------- 5. "نکته مراقبه لحظه‌ای" card ----------
remove_block(
    lambda l: '<!-- Mindfulness Tips -->' in l,
    lambda l: '<!-- Quick Mood Entry -->' in l,
    'section "نکته مراقبه لحظه‌ای"')

# ---------- 6. Profile modal: "مسیر احساسی ۳۰ روزه" ----------
remove_block(
    lambda l: '<!-- 30-Day Mood Chart -->' in l,
    lambda l: '<!-- Alarm Settings -->' in l,
    'profile card "مسیر احساسی ۳۰ روزه"')

# ---------- 7. Profile modal: "آمار کلی" ----------
s = find_one(lambda l: l == '      <!-- Stats -->', 'profile "آمار کلی" [start]')
e = find_one(lambda l: '  <!-- Notebook Modal -->' in l, 'profile "آمار کلی" [end]')
assert lines[e - 3].rstrip() == '    </div>'   # closes p-5 container (KEEP)
assert lines[e - 2].rstrip() == '  </div>'     # closes profileModal (KEEP)
assert lines[e - 1] == ''                      # blank line (KEEP)
remove(s, e - 3, 'profile card "آمار کلی"')

# ---------- 8. Add-habit modal: "کوه نمادین اراده و پیشرفت" ----------
remove_block(
    lambda l: '<!-- Mountain Symbol Card -->' in l,
    lambda l: '<!-- Timeline Card -->' in l,
    'card "کوه نمادین اراده و پیشرفت"')

# ---------- 9. Add-habit modal: "سپر اراده و یادداشت قلبی" ----------
remove_block(
    lambda l: '<!-- Shield Card -->' in l,
    lambda l: '<!-- Action Buttons -->' in l,
    'card "سپر اراده و یادداشت قلبی"')

# ---------- 10. Emergency modal "سپر آرامش" (whole modal) ----------
remove_block(
    lambda l: '  <!-- Emergency Modal -->' in l,
    lambda l: '  <!-- Edit Goals Modal -->' in l,
    'emergency modal "سپر آرامش"')

# ---------- 11. JS: mindfulness tips block ----------
remove_block(
    lambda l: 'MINDFULNESS TIPS' in l,
    lambda l: 'AUDIO ENGINE' in l,
    'JS mindfulnessTips + setMindfulnessTip + refreshMindfulnessTip')

# ---------- 12. JS: init call ----------
remove_single(lambda l: l.strip() == 'setMindfulnessTip();', 'JS init setMindfulnessTip() call')

# ---------- 13. JS: renderAll calls ----------
remove_single(lambda l: l.strip() == 'renderTimelineProgress();', 'renderAll: renderTimelineProgress')
remove_single(lambda l: l.strip() == 'renderWeeklyBarChart();', 'renderAll: renderWeeklyBarChart')
remove_single(lambda l: l == '      renderProfileStats();', 'renderAll: renderProfileStats (6-space)')

# ---------- 14. JS: renderProgress streak lines ----------
i = find_one(lambda l: "getElementById('streakCount')" in l, 'renderProgress streakCount')
assert 'Math.max' in lines[i - 1]
remove(i - 1, i + 1, 'renderProgress maxStreak + streakCount lines')

# ---------- 15. JS: renderStats purity/mind lines ----------
i = find_one(lambda l: "getElementById('statPurityDays')" in l, 'renderStats statPurityDays')
j = find_from(lambda l: 'statMindFresh' in l, 'renderStats statMindFresh', i + 1)
assert j == i + 5
assert lines[i - 1].strip().startswith('const maxStreak')
remove(i - 1, j + 1, 'renderStats purity/mind lines')

# ---------- 16. JS: renderTimelineProgress function ----------
remove_block(
    lambda l: 'TIMELINE PROGRESS' in l,
    lambda l: 'function renderWeeklyBarChart' in l,
    'JS renderTimelineProgress()')

# ---------- 17. JS: renderWeeklyBarChart function ----------
remove_block(
    lambda l: 'function renderWeeklyBarChart' in l,
    lambda l: "let currentFilter = 'all';" in l,
    'JS renderWeeklyBarChart()')

# ---------- 18. JS: guided breathing block ----------
remove_block(
    lambda l: 'GUIDED BREATHING' in l,
    lambda l: '30-DAY MOOD CHART' in l,
    'JS guided breathing engine')

# ---------- 19. JS: renderProfileMoodChart function ----------
remove_block(
    lambda l: '30-DAY MOOD CHART' in l,
    lambda l: 'NOTEBOOK =================' in l,
    'JS renderProfileMoodChart()')

# ---------- 20. JS: renderProfileStats function ----------
remove_block(
    lambda l: 'function renderProfileStats() {' in l,
    lambda l: 'function renderAlarmSettings() {' in l,
    'JS renderProfileStats()')

# ---------- 21. JS: openModal cleanups ----------
remove_single(lambda l: l == '        renderProfileStats();', 'openModal: renderProfileStats call (8-space)')
remove_single(lambda l: l.strip() == 'renderProfileMoodChart();', 'openModal: renderProfileMoodChart call')

i = find_one(lambda l: "id === 'emergencyModal'" in l, 'openModal emergency handler')
assert 'breathType' in lines[i + 1] and lines[i + 4].strip() == '}'
assert 'notificationsModal' in lines[i + 5]
remove(i, i + 5, 'openModal emergencyModal handler')

# ---------- leftover check ----------
leftover_patterns = [
    'emergencyModal', 'setBreathType', 'startBreathing', 'stopBreathing', 'resetBreathing',
    'breathingInterval', 'breathTypes', 'streakCount', 'timelineContainer', 'weeklyBarChart',
    'weeklyBarLabels', 'mindfulnessTip', 'refreshMindfulnessTip', 'setMindfulnessTip',
    'renderTimelineProgress', 'renderWeeklyBarChart', 'renderProfileMoodChart',
    'renderProfileStats', 'statPurityDays', 'statMindFresh', 'moodTrendLabel',
    'profileMoodChart', 'profileTotalCompletions', 'profileBestStreak',
]
problems = []
for p in leftover_patterns:
    hits = [n + 1 for n, l in enumerate(lines) if p in l]
    if hits:
        problems.append('%s -> lines %s' % (p, hits))

with io.open(PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print('OK - %d removals applied, new line count: %d' % (len(LOG), len(lines)))
for entry in LOG:
    print('  *', entry)
if problems:
    print('\nLEFTOVER REFERENCES (must fix):')
    for p in problems:
        print('  !', p)
    sys.exit(1)
else:
    print('\nNo leftover references. Clean.')
