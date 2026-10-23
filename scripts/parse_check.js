// Parse check with precise error reporting
const fs = require('fs');
const src = fs.readFileSync('/home/z/my-project/scripts/inline_check.js', 'utf8');
try {
  new Function(src);
  console.log('PARSE OK');
} catch (e) {
  console.log('PARSE FAIL:', e.message);
  // try to locate: binary search over prefixes to find first failing offset region
  let lo = 0, hi = src.length;
  // find minimal prefix that fails
  while (lo < hi) {
    const mid = Math.floor((lo + hi) / 2);
    // advance to next newline to avoid cutting mid-token
    let cut = src.indexOf('\n', mid);
    if (cut === -1) cut = src.length;
    try { new Function(src.slice(0, cut)); lo = cut + 1; }
    catch (e2) { hi = mid; }
  }
  const lineNum = src.slice(0, lo).split('\n').length;
  console.log('first failing region ends around line:', lineNum);
  console.log(src.split('\n').slice(lineNum - 3, lineNum + 2).map((l, i) => (lineNum - 2 + i) + ': ' + l.slice(0, 160)).join('\n'));
}
