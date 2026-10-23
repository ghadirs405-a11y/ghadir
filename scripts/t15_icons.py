#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 15: generate HUD-style launcher icons (dark violet + cyan robot head)."""
from PIL import Image, ImageDraw
import math, os

OUT = '/home/z/my-project/android/apk-src/res'
SIZES = {'mdpi': 48, 'hdpi': 72, 'xhdpi': 96, 'xxhdpi': 144, 'xxxhdpi': 192}

def draw_icon(size):
    S = 4  # supersample
    W = size * S
    img = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # deep-space radial background (rounded square)
    r = W * 0.22
    bg = Image.new('RGBA', (W, W), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bg)
    for y in range(W):
        t = y / W
        # vertical gradient #1B1147 -> #050310
        c = (int(27 + (5 - 27) * t), int(17 + (3 - 17) * t), int(71 + (16 - 71) * t), 255)
        bd.line([(0, y), (W, y)], fill=c)
    mask = Image.new('L', (W, W), 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(r), fill=255)
    img.paste(bg, (0, 0), mask)
    d = ImageDraw.Draw(img)

    cx, cy = W / 2, W / 2

    # dashed orbit ring
    ring_r = W * 0.40
    for a in range(0, 360, 14):
        a0 = math.radians(a)
        a1 = math.radians(a + 7)
        d.arc([cx - ring_r, cy - ring_r, cx + ring_r, cy + ring_r], math.degrees(a0), math.degrees(a1),
              fill=(34, 211, 238, 110), width=max(1, int(W * 0.008)))

    # gradient stroke helper: draw head with layered rounded rects
    head_w, head_h = W * 0.46, W * 0.40
    hx0, hy0 = cx - head_w / 2, cy - head_h / 2 - W * 0.02
    hx1, hy1 = cx + head_w / 2, cy + head_h / 2 - W * 0.02

    # antenna
    d.line([(cx, cy - W * 0.30), (cx, hy0)], fill=(34, 211, 238, 230), width=max(2, int(W * 0.022)))
    d.ellipse([cx - W * 0.028, cy - W * 0.335, cx + W * 0.028, cy - W * 0.275], fill=(34, 211, 238, 255))

    # head body fill (glassy) + border gradient approximated by two strokes
    d.rounded_rectangle([hx0, hy0, hx1, hy1], radius=int(head_w * 0.26),
                        fill=(34, 211, 238, 20))
    # border: draw gradient by segments (top cyan -> bottom violet)
    seg = 64
    bw = max(2, int(W * 0.016))
    rr = int(head_w * 0.26)
    for i in range(seg):
        t = i / (seg - 1)
        col = (int(34 + (139 - 34) * t), int(211 + (92 - 211) * t), int(238 + (246 - 238) * t), 255)
        y = hy0 + (hy1 - hy0) * i / seg
        d.line([(hx0, y), (hx1, y)], fill=col, width=1)
    # redraw border properly: outline with gradient via per-row lines at edges
    for i in range(seg):
        t = i / (seg - 1)
        col = (int(34 + (139 - 34) * t), int(211 + (92 - 211) * t), int(238 + (246 - 238) * t), 255)
        y = hy0 + (hy1 - hy0) * (i + 0.5) / seg
        d.line([(hx0, y), (hx0 + bw, y)], fill=col, width=bw)
        d.line([(hx1 - bw, y), (hx1, y)], fill=col, width=bw)
    for i in range(int(head_w)):
        t = i / head_w
        col = (34, 211, 238, 255) if t < 0.5 else (139, 92, 246, 255)
        x = hx0 + i
        d.line([(x, hy0), (x, hy0 + bw)], fill=col, width=bw)
        d.line([(x, hy1 - bw), (x, hy1)], fill=col, width=bw)

    # ears
    ew, eh = W * 0.055, W * 0.14
    for ex in (hx0 - ew * 1.6, hx1 + ew * 0.6):
        d.rounded_rectangle([ex, cy - eh / 2 - W * 0.02, ex + ew, cy + eh / 2 - W * 0.02],
                            radius=int(ew / 2), fill=(34, 211, 238, 70),
                            outline=(34, 211, 238, 160), width=max(1, int(W * 0.008)))

    # eyes (glowing cyan)
    eye_w, eye_h = W * 0.095, W * 0.062
    ey = cy - W * 0.035
    for exx in (cx - W * 0.115, cx + W * 0.02):
        d.rounded_rectangle([exx, ey, exx + eye_w, ey + eye_h], radius=int(eye_h / 2), fill=(34, 211, 238, 255))

    # mouth (speaker lines)
    my = cy + W * 0.085
    mw = W * 0.20
    d.rounded_rectangle([cx - mw / 2, my, cx + mw / 2, my + W * 0.05], radius=int(W * 0.025),
                        outline=(34, 211, 238, 170), width=max(1, int(W * 0.009)))
    for k in (-1, 0, 1):
        x = cx + k * W * 0.045
        d.line([(x, my + W * 0.012), (x, my + W * 0.038)], fill=(34, 211, 238, 170),
               width=max(1, int(W * 0.007)))

    return img.resize((size, size), Image.LANCZOS)

for dpi, px in SIZES.items():
    pdir = os.path.join(OUT, f'mipmap-{dpi}')
    os.makedirs(pdir, exist_ok=True)
    draw_icon(px).save(os.path.join(pdir, 'ic_launcher.png'))
    draw_icon(px).save(os.path.join(pdir, 'ic_launcher_round.png'))
    print('icon', dpi, px)
print('ICONS OK')
