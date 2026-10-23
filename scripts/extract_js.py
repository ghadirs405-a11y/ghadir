# -*- coding: utf-8 -*-
"""Extract inline <script> blocks from app.html into one JS file for node --check."""
import io, re

src = io.open('/home/z/my-project/public/app.html', encoding='utf-8').read()
blocks = re.findall(r'<script(?![^>]*src=)[^>]*>(.*?)</script>', src, flags=re.S)
assert blocks, 'no inline script found'
js = '\n;\n'.join(blocks)
io.open('/home/z/my-project/scripts/inline_check.js', 'w', encoding='utf-8').write(js)
print('extracted %d inline script block(s), %d chars' % (len(blocks), len(js)))
