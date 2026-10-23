# -*- coding: utf-8 -*-
"""Generate PWA icons for Habits Tracker: purple gradient + white mountain + gold flag."""
from PIL import Image, ImageDraw
import os

OUT = '/home/z/my-project/public/icons'
os.makedirs(OUT, exist_ok=True)

C_TOP = (139, 92, 246)    # violet-500
C_BOT = (99, 14, 212)     # primary
GOLD = (251, 191, 36)
WHITE = (255, 255, 255)


def rounded_gradient(size, radius_ratio=0.2237):
    """App-icon style rounded square with vertical gradient. Returns RGBA image."""
    s = size
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    grad = Image.new('RGBA', (s, s))
    gd = ImageDraw.Draw(grad)
    for y in range(s):
        t = y / max(s - 1, 1)
        r = int(C_TOP[0] + (C_BOT[0] - C_TOP[0]) * t)
        g = int(C_TOP[1] + (C_BOT[1] - C_TOP[1]) * t)
        b = int(C_TOP[2] + (C_BOT[2] - C_TOP[2]) * t)
        gd.line([(0, y), (s, y)], fill=(r, g, b, 255))
    mask = Image.new('L', (s, s), 0)
    md = ImageDraw.Draw(mask)
    rad = int(s * radius_ratio)
    md.rounded_rectangle([0, 0, s - 1, s - 1], radius=rad, fill=255)
    img.paste(grad, (0, 0), mask)
    return img


def draw_mountain(img, content_scale=1.0, flag=True):
    """Draw white twin-peak mountain + gold flag centered in image."""
    s = img.size[0]
    d = ImageDraw.Draw(img)
    cx = s / 2
    base_y = s * (0.78 * content_scale + (1 - content_scale) * 0.5)
    h = s * 0.42 * content_scale
    w = s * 0.62 * content_scale
    # left peak (taller)
    apex1 = (cx - w * 0.18, base_y - h)
    # right peak (shorter)
    apex2 = (cx + w * 0.30, base_y - h * 0.72)
    left = (cx - w / 2, base_y)
    right = (cx + w / 2, base_y)
    valley = (cx + w * 0.04, base_y - h * 0.34)
    d.polygon([left, apex1, valley, apex2, right], fill=WHITE)
    # snow caps
    def snow(apex, frac):
        aw = w * frac
        mid = (apex[0], apex[1] + h * 0.20)
        d.polygon([
            (apex[0], apex[1]),
            (apex[0] - aw, apex[1] + h * 0.22),
            (apex[0] - aw * 0.45, apex[1] + h * 0.16),
            (apex[0], apex[1] + h * 0.24),
            (apex[0] + aw * 0.5, apex[1] + h * 0.19),
        ], fill=(237, 224, 255))
    snow(apex1, 0.26)
    snow(apex2, 0.20)
    # flag on main peak
    if flag:
        pole_h = h * 0.22
        top = (apex1[0], apex1[1] - pole_h)
        d.line([apex1, top], fill=WHITE, width=max(3, int(s * 0.016)))
        fw, fh = s * 0.115 * content_scale, s * 0.075 * content_scale
        d.polygon([top, (top[0] + fw, top[1] + fh * 0.42), (top[0], top[1] + fh)], fill=GOLD)
    return img


# 1) Standard icons (rounded, transparent corners) — purpose "any"
for size, name in [(512, 'icon-512.png'), (192, 'icon-192.png')]:
    img = rounded_gradient(size)
    draw_mountain(img, content_scale=1.0)
    img.save(f'{OUT}/{name}')
    print('saved', name)

# 2) Apple touch icon (full-bleed square, iOS rounds it)
img = Image.new('RGBA', (180, 180))
grad = Image.new('RGBA', (180, 180))
gd = ImageDraw.Draw(grad)
for y in range(180):
    t = y / 179
    r = int(C_TOP[0] + (C_BOT[0] - C_TOP[0]) * t)
    g = int(C_TOP[1] + (C_BOT[1] - C_TOP[1]) * t)
    b = int(C_TOP[2] + (C_BOT[2] - C_TOP[2]) * t)
    gd.line([(0, y), (180, y)], fill=(r, g, b, 255))
img = grad
draw_mountain(img, content_scale=1.0)
img.convert('RGB').save(f'{OUT}/icon-180.png')
print('saved icon-180.png')

# 3) Maskable (full bleed, artwork inside 80% safe zone)
img = Image.new('RGBA', (512, 512))
grad = Image.new('RGBA', (512, 512))
gd = ImageDraw.Draw(grad)
for y in range(512):
    t = y / 511
    r = int(C_TOP[0] + (C_BOT[0] - C_TOP[0]) * t)
    g = int(C_TOP[1] + (C_BOT[1] - C_TOP[1]) * t)
    b = int(C_TOP[2] + (C_BOT[2] - C_TOP[2]) * t)
    gd.line([(0, y), (512, y)], fill=(r, g, b, 255))
img = grad
draw_mountain(img, content_scale=0.78)
img.convert('RGB').save(f'{OUT}/icon-512-maskable.png')
print('saved icon-512-maskable.png')

# 4) Favicon 32
img = rounded_gradient(32, radius_ratio=0.25)
draw_mountain(img, content_scale=1.0, flag=False)
img.save(f'{OUT}/icon-32.png')
print('saved icon-32.png')

print('DONE')
