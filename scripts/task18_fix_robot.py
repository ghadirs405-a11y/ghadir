#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TASK 18 - Fix: robot img must go into agentBootScreen, app splash keeps its svg robot
import io, sys

APP = '/home/z/my-project/public/app.html'
BAK = '/home/z/my-project/scripts/app_before_task18.bak'
src = io.open(APP, encoding='utf-8').read()
bak = io.open(BAK, encoding='utf-8').read()

ROBOT_DIV = ('<div class="boot-robot-wrap"><div class="boot-robot-ring r2" aria-hidden="true"></div>'
             '<img id="bootRobotImg" class="boot-robot-img" alt="ربات دستیار هوشمند — چهره رو به بیننده" />'
             '<div class="boot-robot-ring" aria-hidden="true"></div></div>')

# 1) extract ORIGINAL app-splash svg from backup
w_anchor = '<div class="boot-head-wrap" style="width:92px;height:92px;">'
wi = bak.index(w_anchor)
s0 = bak.index('<svg', wi)
s1 = bak.index('</svg>', s0) + len('</svg>')
app_svg = bak[s0:s1]
assert 'boot-head' in app_svg and 'boot-eye' in app_svg, 'wrong svg extracted'
print('OK  [1] original app-splash svg recovered (%d chars)' % len(app_svg))

# 2) restore it in current file (replace the misplaced robot div in appBootScreen)
if src.count(ROBOT_DIV) != 1:
    print('FAIL: robot div count =', src.count(ROBOT_DIV)); sys.exit(1)
src = src.replace(ROBOT_DIV, app_svg, 1)
print('OK  [2] app splash svg restored')

# 3) replace AGENT boot svg (first boot-head svg AFTER agentBootScreen marker)
m = src.index('<div id="agentBootScreen"')
s0 = src.index('<svg class="boot-head"', m)
s1 = src.index('</svg>', s0) + len('</svg>')
src = src[:s0] + ROBOT_DIV + src[s1:]
print('OK  [3] agent boot svg -> photo robot')

io.open(APP, 'w', encoding='utf-8').write(src)
print('DONE fix — robot occurrences:', src.count('bootRobotImg'))
