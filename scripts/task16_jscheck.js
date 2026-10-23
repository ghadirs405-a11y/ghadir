#!/usr/bin/env node
// Task 16: extract inline <script> blocks from app.html and syntax-check each
const fs = require('fs');
const { execSync } = require('child_process');
const html = fs.readFileSync('/home/z/my-project/public/app.html', 'utf8');
const re = /<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/gi;
let m, i = 0, bad = 0;
while ((m = re.exec(html)) !== null) {
  const code = m[1];
  if (!code.trim()) continue;
  i++;
  const f = `/tmp/t16_block_${i}.js`;
  fs.writeFileSync(f, code);
  try {
    execSync(`node --check ${f}`, { stdio: 'pipe' });
    console.log(`block ${i}: OK (${code.length} chars)`);
  } catch (e) {
    bad++;
    console.log(`block ${i}: SYNTAX ERROR\n${e.stderr.toString().slice(0, 800)}`);
  }
}
console.log(bad ? `${bad} BAD BLOCKS` : 'ALL SCRIPT BLOCKS OK');
process.exit(bad ? 1 : 0);
