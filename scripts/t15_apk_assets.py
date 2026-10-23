#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task 15: prepare offline assets for the APK (local tailwind + fonts, strip SW)."""
import io, os, re, shutil, sys, urllib.request

PUB = '/home/z/my-project/public'
WWW = '/home/z/my-project/android/apk-src/assets/www'
UA = 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'

def fetch(url, binary=False, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            return data if binary else data.decode('utf-8')
        except Exception as e:
            last = e
            print(f'  retry {i+1} for {url[:60]}: {e}')
    raise SystemExit(f'FAILED to fetch {url}: {last}')

os.makedirs(WWW, exist_ok=True)
fonts_dir = os.path.join(WWW, 'fonts')
os.makedirs(fonts_dir, exist_ok=True)

html = io.open(os.path.join(PUB, 'app.html'), encoding='utf-8').read()

# ---- 1. Tailwind ----
print('1. tailwind...')
tw = fetch('https://cdn.tailwindcss.com')
io.open(os.path.join(WWW, 'tailwind.js'), 'w', encoding='utf-8').write(tw)
print(f'  tailwind.js {len(tw)//1024}KB')

# ---- 2. Fonts (Vazirmatn + Material Symbols) ----
print('2. fonts...')
specs = [
    ('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap', 'fonts.css'),
    ('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0', 'msymbols.css'),
]
for url, fname in specs:
    css = fetch(url)
    # find woff2 urls and localize
    urls = sorted(set(re.findall(r'url\((https://fonts\.gstatic\.com/[^)]+\.woff2)\)', css)))
    print(f'  {fname}: {len(urls)} woff2')
    for u in urls:
        local = 'fonts/' + u.rsplit('/', 1)[-1]
        data = fetch(u, binary=True)
        io.open(os.path.join(WWW, local.replace('/', os.sep)), 'wb').write(data)
        css = css.replace(u, local)
        print(f'    {u.rsplit("/", 1)[-1]} {len(data)//1024}KB')
    io.open(os.path.join(WWW, fname), 'w', encoding='utf-8').write(css)

# ---- 3. index.html offline transform ----
print('3. index.html...')
idx = html
def rep(s, old, new, tag):
    assert s.count(old) >= 1, f'missing: {tag}'
    return s.replace(old, new)

idx = rep(idx, '<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">',
          '<link href="fonts.css" rel="stylesheet">', 'vazir link')
idx = rep(idx, '<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0" rel="stylesheet">',
          '<link href="msymbols.css" rel="stylesheet">', 'msym link')
idx = idx.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '')
idx = idx.replace('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', '')
idx = rep(idx, '<script src="https://cdn.tailwindcss.com"></script>', '<script src="tailwind.js"></script>', 'tw script')

# strip service worker block (useless on file://)
sw_re = re.compile(r"\n\s*if \('serviceWorker' in navigator\) \{\n.*?\n\s*\}\n", re.S)
idx, n = sw_re.subn('\n', idx)
print(f'  SW blocks stripped: {n}')
assert "serviceWorker" not in idx, 'SW still present'

# absolute internal URLs -> relative (safe on file://)
idx = idx.replace('href="/manifest.webmanifest"', 'href="manifest.webmanifest"')
idx = idx.replace("href='/manifest.webmanifest'", "href='manifest.webmanifest'")
idx = idx.replace('href="/logo.svg"', 'href="logo.svg"')
idx = idx.replace('href="/icons/', 'href="icons/')
idx = idx.replace("href='/icons/", "href='icons/")
assert 'https://fonts.googleapis' not in idx and 'cdn.tailwindcss.com' not in idx, 'external refs remain'

io.open(os.path.join(WWW, 'index.html'), 'w', encoding='utf-8').write(idx)
print(f'  index.html {len(idx)//1024}KB')

# ---- 4. manifest + icons ----
print('4. manifest/icons...')
man = io.open(os.path.join(PUB, 'manifest.webmanifest'), encoding='utf-8').read()
man = man.replace('/icons/icon-192.png', 'icons/icon-192.png').replace('/icons/icon-512.png', 'icons/icon-512.png').replace('/icons/icon-512-maskable.png', 'icons/icon-512-maskable.png')
io.open(os.path.join(WWW, 'manifest.webmanifest'), 'w', encoding='utf-8').write(man)
ic = os.path.join(WWW, 'icons')
os.makedirs(ic, exist_ok=True)
for name in ('icon-192.png', 'icon-512.png', 'icon-512-maskable.png'):
    shutil.copy(os.path.join(PUB, 'icons', name), os.path.join(ic, name))

total = 0
for root, _, files in os.walk(WWW):
    for f in files:
        total += os.path.getsize(os.path.join(root, f))
print(f'ASSETS OK — {total//1024}KB total in www/')
