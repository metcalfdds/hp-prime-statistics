// page_check_v7.js -- DataLoader_v7.html in Chromium (Playwright).  Run: node tests/page_check_v7.js   (27 Nov 2026)
// v7: v6's checks, and the note on a blank cell above a value (DataLoad beta 1i asks how the columns go together): it is
// there for paired columns with a blank in the middle, names the columns and the two answers, and is not there for blanks only
// at the foot, for one column, or for a blank only past the ninth column; a student's slip (a cell left empty in the middle
// of a column) gets it too, and a wholly empty row is left out as before; the note that goes into the zip has its sixth step.
// v6: v5's checks, and three from the accessibility check of 21 Nov 2026 (WCAG 2.1 AA): the page does not scroll sideways in
// a window 320 px wide (1.4.10), the green and the orange used for text have a contrast of 4.5 to 1 or more on every
// surface they stand on (1.4.3), and the list of warnings is a live region with no role (4.1.2).  The automated rules of
// axe-core are run by tools/pages_a11y_v1.js, which needs axe-core installed; this test needs Playwright only.
// v5: v4's checks; step 4's link now opens the Prime Loader ready for a data file (?data=1) and names its step 2.
// v3's checks (the example downloads as the file that ran on the Virtual Calculator; a text-coded paste), and the
// review's: the box starts empty, a paste replaces nothing it should not, every silent change of v3 now has a
// sentence in step 2, the two "Not right?" controls work, and a workbook opened as a file is refused.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), os = require('os');
let pass = 0, fail = 0;
function check(name, ok, detail) { if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : JSON.stringify(detail)); } }
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1100, height: 1500 } });
  await ctx.grantPermissions(['clipboard-read', 'clipboard-write']).catch(() => {});
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.join(__dirname, '..', 'DataLoader_v7.html'));
  await p.waitForTimeout(500);
  const settle = () => p.waitForTimeout(450);
  const warn = async () => (await p.isVisible('#warnings')) ? await p.$$eval('#warnings li', l => l.map(x => x.textContent)) : [];
  const setText = async t => { await p.fill('#paste', t); await settle(); };

  // ---- the page as it opens ----
  check('the box is empty when the page opens', (await p.inputValue('#paste')) === '');
  check('... the readout says so, and nothing can be downloaded', /Nothing here yet/.test(await p.textContent('#readout')) && await p.isDisabled('#save') &&
        (await p.$$eval('#cols tbody tr', r => r.length)) === 0 && !(await p.isVisible('#warnings')));
  check('... the two controls are off until there is data', await p.isDisabled('#hdr') && await p.isDisabled('#delim'));

  // ---- a real paste into the empty box (the clipboard, Ctrl+V) ----
  await p.evaluate(() => navigator.clipboard.writeText('score\tsex\n12\tmale\n15\tfemale\nNA\tmale\n9\tfemale\n'));
  await p.click('#paste'); await p.keyboard.press('Control+V'); await settle();
  check('a paste into the opened page holds only what was pasted', (await p.inputValue('#paste')) === 'score\tsex\n12\tmale\n15\tfemale\nNA\tmale\n9\tfemale\n' &&
        /^4 rows and 2 columns read, with a row of names/.test(await p.textContent('#readout')), await p.textContent('#readout'));
  check('... text is coded, NA is a blank, and step 3 says so', JSON.stringify(await p.$$eval('td.codes', t => t.map(x => x.textContent))) === '["1 = female, 2 = male"]' &&
        /1 blank cell will be marked/.test(await p.textContent('#padnote')), await p.textContent('#padnote'));
  check('... a clean paste has no warnings', (await warn()).length === 0, await warn());

  // ---- the example: the file that ran on the calculator ----
  await p.click('#example'); await settle();
  check('the example: 432 rows and 5 columns, with a row of names', /^432 rows and 5 columns read, with a row of names\. 5 columns will go/.test(await p.textContent('#readout')), await p.textContent('#readout'));
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#save')]);
  const dlPath = path.join(os.tmpdir(), 'page_v6_M1.hpmat'); await dl.saveAs(dlPath);
  check('the example downloads as M1.hpmat, identical to the file tested on the calculator', dl.suggestedFilename() === 'M1.hpmat' &&
        Buffer.compare(fs.readFileSync(dlPath), fs.readFileSync(path.join(__dirname, '..', 'examples', 'M1.hpmat'))) === 0);
  check('... the status sends the student on to step 4', /Now go on to step 4/.test(await p.textContent('#savestatus')));
  check('step 4 leads to the Prime Loader, and names the file', (await p.getAttribute('#s4 ~ .two a', 'href')) === 'https://metcalfdds.github.io/hp-prime-statistics/prime-loader/?data=1' && /In its step 2, click Add a data file you were given/.test(await p.textContent('#s4 ~ .two')) &&
        (await p.textContent('#fname1')) === 'M1.hpmat' && /Add a data file you were given/.test(await p.textContent('main')));

  // ---- every silent change of v3 has a sentence ----
  await setText('x\ty\n1O\t2\n11\t3\n12\t4');
  let w = await warn();
  check('a typo: "1 cell is not a number and will be a blank: 1O"', w.length === 1 && /x: 1 cell is not a number and will be a blank: 1O\./.test(w[0]), w);
  await setText('salary\tgrp\n$45,000\ta\n$52,500\tb');
  w = await warn();
  check('$45,000: numbers, with the sentence about the currency sign', w.some(x => /salary: the currency signs are dropped/.test(x)) &&
        JSON.stringify(await p.$$eval('#cols tbody tr td:nth-child(4)', t => t.map(x => x.textContent))) === '["numbers","text → codes"]', w);
  await setText('rate\n45%\n52%');
  check('45%: the sentence says it is read as 45, not 0.45', (await warn()).some(x => /45% is read as 45, not 0\.45/.test(x)));
  await setText('sex\tx\nMale\t1\nmale\t2\nFemale\t3');
  check('Male and male: "are counted as one label"', (await warn()).some(x => /sex: Male and male are counted as one label/.test(x)), await warn());
  await setText('x;y\n3,14;2\n2,50;3');
  check('3,14: "read as a decimal comma"', (await warn()).some(x => /x: the comma is read as a decimal comma/.test(x)));
  await setText('salary\n45,000\n52,500');
  w = await warn();
  check('one column of 45,000s: one column, and the sentence says how to make it two', /^2 rows and 1 columns? read/.test(await p.textContent('#readout')) && w.some(x => /one column/.test(x) && /choose commas/.test(x)), [await p.textContent('#readout'), w]);
  await p.selectOption('#delim', 'comma'); await settle();
  check('... choosing commas makes it two columns, and the sentence goes', /2 columns read/.test(await p.textContent('#readout')) && !(await warn()).some(x => /one column/.test(x)), await p.textContent('#readout'));
  await setText('aid\nfinancial aid\nno aid\nfinancial aid');
  check('typing in the box keeps the student\'s choice of separator', (await p.inputValue('#delim')) === 'comma');
  await p.click('#clear'); await settle();
  check('Clear empties the box and puts both controls back', (await p.inputValue('#paste')) === '' && (await p.inputValue('#delim')) === '' && await p.isDisabled('#save'));
  await setText('aid\nfinancial aid\nno aid\nfinancial aid');
  check('one column of labels with spaces: one column, two codes', /^3 rows and 1 columns? read, with a row of names/.test(await p.textContent('#readout')) &&
        JSON.stringify(await p.$$eval('td.codes', t => t.map(x => x.textContent))) === '["1 = financial aid, 2 = no aid"]', await p.textContent('#readout'));
  const ids = ['id\tx']; for (let i = 1; i <= 12; i++) ids.push('S' + i + '\t' + i);
  await setText(ids.join('\n'));
  check('a column of 12 ID codes: the sentence says DataLoad takes at most 9 groups', (await warn()).some(x => /id has 12 different labels/.test(x)), await warn());

  // ---- "Not right?": the row of names ----
  await setText('2019\t2020\n5\t6\n7\t8');
  check('names that are numbers: read as data, the box unticked', /^3 rows and 2 columns read, with no row of names/.test(await p.textContent('#readout')) && !(await p.isChecked('#hdr')), await p.textContent('#readout'));
  await p.check('#hdr'); await settle();
  check('... ticking the box makes them names', /^2 rows and 2 columns read, with a row of names/.test(await p.textContent('#readout')) &&
        JSON.stringify(await p.$$eval('#cols tbody tr td:nth-child(3)', t => t.map(x => x.textContent))) === '["2019","2020"]', await p.textContent('#readout'));
  await p.evaluate(() => navigator.clipboard.writeText('a\tb\n1\t2\n3\t4\n'));
  await p.click('#paste'); await p.keyboard.press('Control+A'); await p.keyboard.press('Control+V'); await settle();
  check('a new paste lets the page decide again', (await p.isChecked('#hdr')) && /^2 rows and 2 columns read, with a row of names/.test(await p.textContent('#readout')), await p.textContent('#readout'));

  // ---- files ----
  const give = async (name, buf) => { await p.setInputFiles('#file', { name: name, mimeType: 'application/octet-stream', buffer: buf }); await settle(); };
  await p.click('#clear'); await settle();
  await give('grades.xlsx', Buffer.from([0x50, 0x4B, 3, 4, 20, 0, 6, 0, 8, 0, 0, 0]));
  check('an .xlsx workbook is refused, with the way round it', await p.isVisible('#filestatus') && /grades\.xlsx is a spreadsheet workbook/.test(await p.textContent('#filestatus')) &&
        /copy them \(Ctrl\+C\)/.test(await p.textContent('#filestatus')) && (await p.inputValue('#paste')) === '', await p.textContent('#filestatus'));
  await give('study.sav', Buffer.from('$FL2@(#) IBM SPSS STATISTICS'));
  check('an SPSS .sav file is refused, with the way round it', /study\.sav is an SPSS data file/.test(await p.textContent('#filestatus')) && (await p.inputValue('#paste')) === '');
  await give('photo.dat', Buffer.from([0x89, 0x50, 0x4E, 0x47, 0, 0, 0, 13, 1, 2, 3]));
  check('any other binary file is refused', /photo\.dat is not a text file/.test(await p.textContent('#filestatus')) && (await p.inputValue('#paste')) === '');
  await give('rossi.csv', fs.readFileSync(path.join(__dirname, '..', 'examples', 'rossi.csv')));
  check('a CSV file is read, and the refusal goes away', !(await p.isVisible('#filestatus')) && /^432 rows and 5 columns read/.test(await p.textContent('#readout')));
  await give('latin1.csv', Buffer.from([0x6E, 0x61, 0x6D, 0x65, 0x2C, 0x78, 0x0A, 0x4A, 0x6F, 0x73, 0xE9, 0x2C, 0x35, 0x0A, 0x52, 0x65, 0x6E, 0xE9, 0x65, 0x2C, 0x36, 0x0A]));
  check('a Windows-1252 file keeps its accents', JSON.stringify(await p.$$eval('td.codes', t => t.map(x => x.textContent))) === '["1 = José, 2 = Renée"]', await p.$$eval('td.codes', t => t.map(x => x.textContent)));
  await give('utf16.txt', Buffer.concat([Buffer.from([0xFF, 0xFE]), Buffer.from('a\tb\r\n1\t2\r\n3\t4\r\n', 'utf16le')]));
  check('a UTF-16 text file (Excel\'s "Unicode Text") is read', /^2 rows and 2 columns read, with a row of names/.test(await p.textContent('#readout')), await p.textContent('#readout'));

  // ---- the matrix name runs through the page ----
  await p.selectOption('#mat', '3'); await settle();
  check('choosing M3 names M3.hpmat on the button and in step 4', /M3\.hpmat/.test(await p.textContent('#save')) && (await p.textContent('#fname1')) === 'M3.hpmat' &&
        (await p.textContent('#fname5')) === 'M3 (1).hpmat');
  // ---- v7: a blank cell above a value (DataLoad beta 1i asks how the columns go together) ----
  const pad = async () => (await p.isVisible('#padnote')) ? await p.textContent('#padnote') : '';
  await p.click('#clear'); await settle();
  await setText('before\tafter\n10\t12\n11\tNA\n13\t15\n');
  let pn = await pad();
  check('v7 paired columns with a blank in the middle: the note names the column and both answers',
        /after has a blank cell above a value, so when DataLoad loads these as Columns, it will ask/.test(pn) &&
        /"Pairs: keep complete rows"/.test(pn) && /"Separate groups: drop blanks"/.test(pn) && /Scores by group always keeps only the rows/.test(pn), pn);
  await setText('a\tb\n1\t2\n3\tNA\n5\tNA\n');
  pn = await pad();
  check('v7 blanks only at the foot of a column: the note of v6, with no question', /DataLoad leaves them out, so each list gets only its own values/.test(pn) && !/Pairs/.test(pn), pn);
  await setText('x\n1\nNA\n3\n');
  pn = await pad();
  check('v7 one column with a blank in the middle: no question (one column has no partner)', /each list gets only its own values/.test(pn) && !/Pairs/.test(pn), pn);
  const head = Array.from({ length: 12 }, (_, j) => 'c' + (j + 1)).join('\t');
  const rowsW = [1, 2, 3].map(r => Array.from({ length: 12 }, (_, j) => (r === 2 && j === 10) ? 'NA' : String(r * 100 + j + 1)).join('\t'));
  await setText(head + '\n' + rowsW.join('\n') + '\n');
  pn = await pad();
  check('v7 a blank in the middle of the 11th column only (DataLoad takes the first 9): no question', /each list gets only its own values/.test(pn) && !/Pairs/.test(pn), pn);
  await setText('x\ty\n1\t2\n3\t\n5\t6\n');
  pn = await pad();
  check('v7 a slip, a cell left empty (nothing typed) in the middle of a column: it is a blank above a value, and y is named',
        /y has a blank cell above a value/.test(pn), [pn, await p.textContent('#readout')]);
  await setText('x\ty\n1\t2\n\t\n3\t4\n');
  pn = await pad();
  check('v7 a wholly empty row in the middle of a paste is left out by the page (as in v6), so nothing is asked',
        /^2 rows and 2 columns read/.test(await p.textContent('#readout')) && !/Pairs/.test(pn), [pn, await p.textContent('#readout')]);
  const rm = await p.evaluate(() => readme('M1'));
  check('v7 the note in the zip has the sixth step, with both answers', /6\. If DataLoad says a column has a blank inside, choose "Pairs: keep complete rows"/.test(rm) &&
        /"Separate groups: drop blanks" when the columns are groups\./.test(rm), rm);
  await p.click('#clear'); await settle();

  // ---- v6: accessibility (WCAG 2.1 AA) ----
  {
    const narrow = await b.newContext({ viewport: { width: 320, height: 800 } }); const q = await narrow.newPage();
    await q.goto('file://' + path.join(__dirname, '..', 'DataLoader_v7.html'));
    const wide = () => q.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
    check('in a window 320 px wide the opened page does not scroll sideways', (await wide()) <= 0, await wide());
    await q.click('#example'); await q.waitForTimeout(300);
    check('... nor with the example loaded (the table of columns scrolls inside its own frame)', (await wide()) <= 0, await wide());
    await q.evaluate(() => document.querySelectorAll('details').forEach(d => d.open = true));
    check('... nor with every fold opened', (await wide()) <= 0, await wide());
    await narrow.close();
    const cr = await p.evaluate(() => {
      const lum = c => { const v = c.match(/\d+/g).slice(0, 3).map(x => x / 255).map(x => x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4)); return 0.2126 * v[0] + 0.7152 * v[1] + 0.0722 * v[2]; };
      const probe = document.createElement('span'); document.body.appendChild(probe); const out = {};
      for (const fg of ['--good', '--frame', '--muted', '--accent', '--code']) for (const bg of ['--surface', '--paper', '--warn-bg', '--accent-soft']) {
        probe.style.color = 'var(' + fg + ')'; probe.style.backgroundColor = 'var(' + bg + ')'; const cs = getComputedStyle(probe);
        const a = lum(cs.color), c = lum(cs.backgroundColor); out[fg + ' on ' + bg] = Math.round(100 * (Math.max(a, c) + 0.05) / (Math.min(a, c) + 0.05)) / 100; }
      probe.remove(); return out; });
    const low = Object.entries(cr).filter(([k, v]) => v < 4.5);
    check('every text color has a contrast of 4.5 to 1 or more on every surface of the page (light)', low.length === 0, low);
    check('the list of warnings is a live region and carries no role', await p.$eval('#warnings', e => e.getAttribute('aria-live') === 'polite' && !e.hasAttribute('role')));
  }
  await p.screenshot({ path: path.join(os.tmpdir(), 'dl_page_v6.png'), fullPage: true });
  check('no errors in the page', errs.length === 0, errs);
  console.log('\n' + pass + ' PASS, ' + fail + ' FAIL');
  await b.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
