// test_core_v2.js -- dl_core_v2.js.  Run: node tests/test_core_v2.js      (17 Nov 2026)
// Part 1 is test_core_v1.js's: the number encoder against hp-prime-kit's over cases_v1.json, the Prime's extremes,
// half-up rounding, and the Rossi file byte for byte against the file that ran on the Virtual Calculator.
// Part 2 is new: the pastes a student makes that v1 read wrongly without a word (the review of 17 Nov 2026).
const path = require('path'), fs = require('fs');
const C = require(path.join(__dirname, '..', 'dl_core_v2.js'));
let pass = 0, fail = 0;
function check(name, ok, detail) { if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : JSON.stringify(detail)); } }

// ---------------- part 1: what v1 was tested for ----------------
const cases = JSON.parse(fs.readFileSync(path.join(__dirname, 'cases_v1.json')));
let bad = [], n = 0, skipped = 0;
for (const [s, want] of cases) {
  if (want === 'ERR') { skipped++; continue; }
  const got = Buffer.from(C.encodeParsed(C.parseNumber(s))).toString('hex');
  n++; if (got !== want) bad.push([s, got, want]);
}
check('encoder against hp-prime-kit: ' + n + ' numbers, none differ (' + skipped + ' outside a double, not comparable)', n > 1000 && bad.length === 0, bad.slice(0, 3));
const ext = s => { const p = C.parseNumber(s); return C.inRange(p) ? C.decode(C.encodeParsed(p)) : 'out of range'; };
check('the Prime\'s extremes', ext('1E499') === '1E499' && ext('9.99999999999E499') === '9.99999999999E499' && ext('1E-499') === '1E-499' &&
      ext('1E500') === 'out of range' && ext('1E-500') === 'out of range');
check('the blank marker is 9.99999999999E499', C.decode(C.encodeParsed(C.BLANK_WORD)) === '9.99999999999E499');
const rnd = s => C.decode(C.encodeParsed(C.parseNumber(s)));
check('half-up rounding at the 13th digit', rnd('1234567890125') === '1.23456789013E12' && rnd('1234567890124.9') === '1.23456789012E12' &&
      rnd('9999999999995') === '1E13' && rnd('0.12345678901250') === '1.23456789013E-1' && rnd('-2.5000000000005') === '-2.5E0' && rnd('-2.50000000000051') === '-2.5E0' && rnd('-2.500000000005') === '-2.50000000001E0',
      [rnd('1234567890125'), rnd('9999999999995'), rnd('-2.5000000000005')]);
const csv = fs.readFileSync(path.join(__dirname, '..', 'examples', 'rossi.csv'), 'utf8');
const t = C.readTable(csv), infos = t.cols.map(C.describe);
const buf = C.buildHpmat(t.cols, infos);
check('the Rossi file: 17,296 bytes, identical to the file that ran on the Virtual Calculator',
      buf.length === 17296 && Buffer.compare(Buffer.from(buf), fs.readFileSync(path.join(__dirname, '..', 'examples', 'M1.hpmat'))) === 0, buf.length);
check('the Rossi file: its row of names is found, 432 rows, 5 number columns, nothing odd',
      t.header && t.cols[0].length === 432 && infos.every(i => i.kind === 'numbers' && i.odd === 0 && i.blanks === 0 && !i.decimalComma), t.names);
check('the zip writer', C.zip([{ name: 'M1.hpmat', data: buf }, { name: 'READ_ME.txt', data: new TextEncoder().encode('test\r\n') }]).length === 17514);

// ---------------- part 2: a student's paste ----------------
function rd(text, opts) {
  const tb = C.readTable(text, opts), inf = tb.cols.map(C.describe);
  const b = tb.cols.length ? C.buildHpmat(tb.cols, inf) : new Uint8Array(16), cells = [];
  for (let k = 16; k < b.length; k += 8) cells.push(C.decode(b.slice(k, k + 8)));
  return { tb, inf, cells, rows: tb.cols.length ? tb.cols[0].length : 0 };
}
const BL = '9.99999999999E499';
let r;
r = rd('sex\tscore\nmale\t3\nfemale\t4\nNA\t5\n.\t6\nmale\t7');
check('NA and "." in a text column are blanks, not labels', r.inf[0].kind === 'text' && r.inf[0].codes.size === 2 && r.inf[0].blanks === 2 &&
      JSON.stringify(r.cells) === JSON.stringify(['2E0', '3E0', '1E0', '4E0', BL, '5E0', BL, '6E0', '2E0', '7E0']), r.cells);
r = rd('x\ty\n5\tNA\nn/a\t2\n#N/A\t3\nNaN\t4\nnull\t5\n-\t6\n?\t7');
check('every blank word is a blank in a number column, and none is "odd"', r.inf[0].values === 1 && r.inf[0].odd === 0 && r.inf[1].values === 6 && r.inf[1].odd === 0, [r.inf[0], r.inf[1]]);
r = rd('x\ty\n1O\t2\n11\t3\n12\t4');
check('a typo in a number column is listed, and becomes a blank', r.inf[0].kind === 'numbers' && JSON.stringify(r.inf[0].oddCells) === '["1O"]' && r.cells[0] === BL, r.inf[0]);
r = rd('salary\tgrp\n$45,000\ta\n-$52,500.50\tb\n$1,000,000\ta');
check('"$45,000" is the number 45000 (v1: text, coded 1, 2, 3)', r.tb.header && r.inf[0].kind === 'numbers' && r.inf[0].money === 3 &&
      r.cells[0] === '4.5E4' && r.cells[2] === '-5.25005E4' && r.cells[4] === '1E6', r.cells);
r = rd('rate\tgrp\n45%\ta\n52.5 %\tb');
check('"45%" is the number 45', r.inf[0].kind === 'numbers' && r.inf[0].percent === 2 && r.cells[0] === '4.5E1' && r.cells[2] === '5.25E1', r.cells);
r = rd('salary\n45,000\n52,500\n61,250');
check('one column of 45,000-style numbers stays one column (v1: two)', r.tb.cols.length === 1 && r.tb.why === 'thousands' && r.tb.header &&
      JSON.stringify(r.cells) === '["4.5E4","5.25E4","6.125E4"]', r.cells);
r = rd('a,b\n1,500\n2,450');
check('a real two-column CSV is still two columns', r.tb.cols.length === 2 && r.tb.delim === ',' && JSON.stringify(r.cells) === '["1E0","5E2","2E0","4.5E2"]', r.cells);
r = rd('1,500\n2,450', { delim: ',' });
check('the student can say "comma" where the rule says thousands', r.tb.cols.length === 2 && JSON.stringify(r.cells) === '["1E0","5E2","2E0","4.5E2"]', r.cells);
r = rd('aid\nfinancial aid\nno aid\nfinancial aid');
check('one column of labels with spaces stays one column (v1: two)', r.tb.cols.length === 1 && r.tb.why === 'spaces' && r.tb.header &&
      JSON.stringify(Array.from(r.inf[0].codes)) === '[["financial aid",1],["no aid",2]]' && JSON.stringify(r.cells) === '["1E0","2E0","1E0"]', r.cells);
r = rd('grp score\nctrl 5.1\ntrt 6.2');
check('columns separated by spaces are still read when one of them holds numbers', r.tb.cols.length === 2 && r.tb.delim === ' ' && r.inf[1].kind === 'numbers');
r = rd('5\n6\n7');
check('one column of numbers, no names', r.tb.cols.length === 1 && !r.tb.header && JSON.stringify(r.cells) === '["5E0","6E0","7E0"]');
r = rd('sex\tx\nMale\t1\nmale \t2\nFemale\t3\n  MALE\t4');
check('Male, male and MALE are one label, and the page is told', r.inf[0].codes.size === 2 && r.inf[0].merged.length === 1 && r.inf[0].merged[0].length === 3 &&
      JSON.stringify(r.cells) === '["2E0","1E0","2E0","2E0","1E0","3E0","2E0","4E0"]', r.cells);
r = rd('g\tx\n1\t5\n2\t6\ncontrol\t7\ncontrol\t8\ncontrol\t9');
check('in a text column a number-like cell is a label too (v1: a blank)', r.inf[0].kind === 'text' && r.inf[0].codes.size === 3 && r.inf[0].blanks === 0 && r.cells[0] === '1E0' && r.cells[4] === '3E0', r.cells);
r = rd('x;y\n3,14;2\n2,50;3\n1.234,5;4');
check('a column written with decimal commas is numbers (v1: text, coded)', r.inf[0].kind === 'numbers' && r.inf[0].decimalComma &&
      r.cells[0] === '3.14E0' && r.cells[2] === '2.5E0' && r.cells[4] === '1.2345E3', r.cells);
r = rd('x\ty\n1,234.5\t2\n2,000\t3');
check('1,234.5 beside a decimal point is thousands, not a decimal comma', !r.inf[0].decimalComma && r.cells[0] === '1.2345E3' && r.cells[2] === '2E3', r.cells);
r = rd('group\nyes\nno\nyes');
check('a table of labels only: the first row is found to be a name', r.tb.header && r.tb.names[0] === 'group' && r.rows === 3);
r = rd('yes\nno\nyes');
check('a table of labels only with no name row: none is invented', !r.tb.header && r.rows === 3);
r = rd('2019\t2020\n5\t6\n7\t8');
check('names that are numbers: the rule says data', !r.tb.header && r.rows === 3);
r = rd('2019\t2020\n5\t6\n7\t8', { header: true });
check('... and the student can say they are names', r.tb.header && r.tb.names.join() === '2019,2020' && r.rows === 2 && r.tb.headerAuto === false);
r = rd('score\tsex\n12\tmale\n15\tfemale', { header: false });
check('... or that a first row of words is data', !r.tb.header && r.rows === 3 && r.tb.headerAuto === true);
r = rd('name,score\n"Smith, J",5\n"Lee",6');
check('a quoted CSV field keeps its comma', r.tb.cols.length === 2 && r.inf[0].codes.has('Smith, J'));
r = rd('score\tgroup\tnote\n12\tmale\tx\n15\tfemale\n\tmale\t\nNA\tfemale\t3\n7\t\t\n');
check('ragged rows, blanks and text together (v1\'s own case)', r.rows === 5 && r.inf[0].values === 3 && r.inf[1].values === 4 && r.inf[1].codes.size === 2 && r.tb.cols.length === 3, r.inf.map(i => [i.kind, i.values, i.blanks]));
r = rd('x\n1e600\n5');
check('a number beyond the Prime\'s range is listed, not written', r.tb.header && JSON.stringify(r.inf[0].oddCells) === '["1e600"]' && r.cells[0] === BL, r.inf[0]);
r = rd('score\tsex\nNA\tmale\n15\tfemale\n12\tmale');
check('a blank in the first data row does not hide the row of names', r.tb.header && r.rows === 3 && r.inf[0].values === 2);
r = rd('﻿week,arrest\r\n20,1\r\n17,1\r\n');
check('a byte-order mark and Windows line ends do no harm', r.tb.header && r.tb.names[0] === 'week' && JSON.stringify(r.cells) === '["2E1","1E0","1.7E1","1E0"]', [r.tb.names, r.cells]);
r = rd('   \n\n');
check('nothing pasted: no table, no error', r.tb.cols.length === 0);
r = rd('−5\t−2.5');
check('a typographic minus is a minus', JSON.stringify(r.cells) === '["-5E0","-2.5E0"]', r.cells);
console.log('\n' + pass + ' PASS, ' + fail + ' FAIL');
process.exit(fail ? 1 : 0);
