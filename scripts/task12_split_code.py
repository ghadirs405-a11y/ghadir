#!/usr/bin/env python3
# Task 12: split app.html into fully-viewable parts + zip package
import os, zipfile, shutil

SRC = '/home/z/my-project/public/app.html'
OUT = '/home/z/my-project/download/code_parts'
ZIP = '/home/z/my-project/download/habits_app_source.zip'

with open(SRC, 'r', encoding='utf-8') as f:
    text = f.read()
lines = text.split('\n')
total = len(lines)
size_kb = len(text.encode('utf-8')) / 1024

os.makedirs(OUT, exist_ok=True)

# 6 parts (~915 lines each) — every part small enough for any phone viewer
N = 6
per = (total + N - 1) // N
names = []
for i in range(N):
    s, e = i * per, min(total, (i + 1) * per)
    name = f'part_{i+1}_of_{N}_lines_{s+1}-{e}.txt'
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines[s:e]))
    names.append(name)
    print(f'{name}: {e-s} lines, {os.path.getsize(os.path.join(OUT, name))/1024:.0f} KB')

# Persian readme inside the folder
readme = f'''کد کامل اپلیکیشن ردیاب عادت‌ها — نسخه تکه‌تکه‌شده
=====================================================
فایل اصلی: public/app.html  ({total} خط / {size_kb:.0f} کیلوبایت)
دلیل تکه‌شدن: فایل کامل در بعضی نمایشگرها بریده می‌شود؛ هر تکه این‌جا کامل و قابل مشاهده است.

تکه‌ها (به ترتیب):
{chr(10).join('  ' + n for n in names)}

⚠️ نکته: این تکه‌ها دقیقاً پشت‌سرهم قرار می‌گیرند و کل فایل اصلی را می‌سازند
(برای بازیابی: محتوای ۶ فایل را به همان ترتیب به هم بچسبانید).

راه راحت‌تر: صفحه «کدبان» در آدرس /code.html — کل کد را زنده با صفحه‌بندی،
جستجو و دکمه دانلود نشان می‌دهد. فایل کامل هم در download/app.html هست.
'''
with open(os.path.join(OUT, 'README.txt'), 'w', encoding='utf-8') as f:
    f.write(readme)

# zip with everything (original + parts + viewer)
if os.path.exists(ZIP):
    os.remove(ZIP)
with zipfile.ZipFile(ZIP, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(SRC, 'app.html')
    z.write('/home/z/my-project/public/code.html', 'code_viewer.html')
    z.write(os.path.join(OUT, 'README.txt'), 'code_parts/README.txt')
    for n in names:
        z.write(os.path.join(OUT, n), f'code_parts/{n}')

print(f'\nZIP: {ZIP} ({os.path.getsize(ZIP)/1024:.0f} KB)')
# integrity check: concatenation must equal original
joined = []
for n in names:
    with open(os.path.join(OUT, n), 'r', encoding='utf-8') as f:
        joined.append(f.read())
assert '\n'.join(joined) == text, 'MISMATCH!'
print('Integrity: parts concat == original ✓')
