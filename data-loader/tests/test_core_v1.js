// test_core_v1.js -- the page's number encoder (dl_core_v1.js) against hp-prime-kit's, over cases_v1.json
// (made by gen_cases_v1.py with the kit).  Run: node test_core_v1.js
const path = require('path');
const C = require(path.join(__dirname, '..', 'dl_core_v1.js'));
const fs = require('fs');
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'cases_v1.json')));
let bad = [], n = 0, skipped = 0;
for (const [s, want] of cases) {
  if (want === 'ERR') { skipped++; continue; }
  const p = C.parseNumber(s);
  const got = Buffer.from(C.encodeParsed(p)).toString('hex');
  n++;
  if (got !== want) bad.push([s, got, want]);
}
console.log('encoder vs hp-prime-kit:', n, 'compared,', bad.length, 'differ,', skipped, 'outside a double (not comparable)');
console.log(bad.slice(0, 5));
// beyond a double: the Prime's own extremes, from the text
for (const s of ['1E499', '9.99999999999E499', '1E-499', '1E500', '1E-500']) {
  const p = C.parseNumber(s);
  console.log(s, C.inRange(p) ? C.decode(C.encodeParsed(p)) : 'out of range');
}
console.log('blank marker', C.decode(C.encodeParsed(C.BLANK_WORD)), Buffer.from(C.encodeParsed(C.BLANK_WORD)).toString('hex'));
// half-up rounding at the 13th digit, where a double and the text can disagree
for (const s of ['1234567890125', '1234567890124.9', '9999999999995', '0.12345678901250', '-2.5000000000005'])
  console.log('round', s, '->', C.decode(C.encodeParsed(C.parseNumber(s))));
// the whole Rossi file against the kit's (examples/M1.hpmat, written by `hpprime matrix write` from the same
// numbers, the file that ran on the Virtual Calculator)
const csv = fs.readFileSync(path.join(__dirname, '..', 'examples', 'rossi.csv'), 'utf8');
const t = C.readTable(csv);
const infos = t.cols.map(C.describe);
const buf = C.buildHpmat(t.cols, infos);
const kitf = fs.readFileSync(path.join(__dirname, '..', 'examples', 'M1.hpmat'));
console.log('Rossi M1.hpmat: ', buf.length, 'bytes; identical to the kit\'s:', Buffer.compare(Buffer.from(buf), kitf) === 0);
const t2 = t;
console.log('with its header row:', t2.header, t2.names.join(','), t2.cols[0].length, 'rows');
const zipped = C.zip([{name: 'M1.hpmat', data: buf}, {name: 'READ_ME.txt', data: new TextEncoder().encode('test\r\n')}]);
console.log('zip of M1.hpmat and a read-me:', zipped.length, 'bytes');
// ragged, text and blanks
const t3 = C.readTable('score\tgroup\tnote\n12\tmale\tx\n15\tfemale\n\tmale\t\nNA\tfemale\t3\n7\t\t\n');
const i3 = t3.cols.map(C.describe);
console.log(JSON.stringify(i3.map(i => [i.kind, i.values, i.blanks, i.codes ? Array.from(i.codes) : null])));
const b3 = C.buildHpmat(t3.cols.slice(0, 2), i3.slice(0, 2));
const cells = []; for (let k = 16; k < b3.length; k += 8) cells.push(C.decode(b3.slice(k, k + 8)));
console.log('rows', new DataView(b3.buffer).getUint32(8, true), 'cols', new DataView(b3.buffer).getUint32(12, true), cells.join(' | '));
