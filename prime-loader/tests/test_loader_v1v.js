// test_loader_v1v.js (17 Nov 2026, evening: the review "they must be bullet proof and as simple as possible").  v1u's
//   checks on PrimeLoader_v1v.html, with these changes and additions:
//   - a data file loaded on its own is ADDED with DataLoad, and the programs on the calculator stay (v1u's check
//     "loading only data clears the programs too (a clean slate)" is gone: it described the fault);
//   - a chapter without DataLoad, loaded with data, gets DataLoad;
//   - a data file is opened and checked: a short file, a text file and a cut-off file are each refused with a reason;
//   - "M1 (2).hpmat", a browser's name for a second download, is taken as M1;
//   - the student's own M1 wins over the sample data set, and the page says so;
//   - a phone, a Mac and Windows: the notice at the top shows, shows, and does not;
//   - the main browser context carries a Windows user-agent, as a student's Edge does.
// was: test_loader_v1u.js (17 Nov 2026: v1t's checks, unchanged, on the page built from starter pack v23, round 17: sixteen
//   programs whose screen text follows the book's house form for a statistic's letter)
// was: test_loader_v1t.js (15 Nov 2026, night: v1s's checks, unchanged, on the page built from starter pack v22, round 16:
// nine programs with new versions)
// was: test_loader_v1s.js (15 Nov 2026: v1r's checks, unchanged, on the page built from starter pack v21, round 15:
// seven programs with new versions)
// was: test_loader_v1r.js (14 Nov 2026, night: v1q's checks on the page built from starter pack v20, round 14 part 2:
// TTestLab beta 1k and TTestLabG beta 1h; Chapter 9 lists TTestLabG)
// was: test_loader_v1q.js (14 Nov 2026: v1p's checks, unchanged, on the page built from starter pack v19, round 14;
// before that, 13 Nov 2026: v1o's checks, unchanged, on the page built from starter pack v18, round 13:
// ChiTable beta 3m's exact test for the 2 x 3 and 3 x 2 tables)
// was: test_loader_v1o.js (13 Nov 2026: v1n's checks, unchanged, on the page built from starter pack v17, round 12: help-page
// fixes in twelve programs)
// was: test_loader_v1n.js (9 Nov 2026: v1m's checks, unchanged, on the page built from starter pack v16, round 11: the help
// pages in plain words)
// was: test_loader_v1m.js (7 Nov 2026, night: v1l's checks, on the page built from starter pack v15, 31 programs: the
// EVERYTHING card and the zip of everything count 31)
// was: test_loader_v1l.js (5 Nov 2026: v1k's checks, on the page built from starter pack v14, round 9)
// was: test_loader_v1k.js -- drives PrimeLoader_v1l.html in Chromium against a mock Virtual Calculator folder.
// Roger Metcalf & Claude, 1 Nov 2026.
//
// The browser's folder picker cannot be driven by a test, so it is replaced by one that returns a folder in the
// browser's private file system (OPFS), seeded to look like Documents\HP Prime on a PC that has run the Virtual
// Calculator: Calculators\Prime with HP's apps, settings, old programs and a matrix; Temp with the lock file.  Every file
// the page writes is compared byte for byte with the starter pack it was built from.
//
//   node tests/test_loader_v1v.js PrimeLoader_v1v.html PACK.zip
// v1k (4 Nov 2026, night): v1j's checks, run on the page built from starter pack v13 (round 8); Chapter 11's card
//   is found by its new title, "t-Tests: Two Samples".
// v1j (4 Nov 2026): v1i's checks, unchanged, run on the page built from starter pack v12 (round 7).
// v1i (2 Nov 2026, night): v1h's checks, unchanged, run on the page built from starter pack v11 (round 6:
//   sensible ranges for what a student types, menu items that fit).
// v1h (2 Nov 2026, night): v1g's checks, unchanged, run on the page built from starter pack v10 (all 30
//   programs: commas in big numbers).
// v1g (2 Nov 2026): v1f's checks, unchanged, run on the page built from starter pack v9 (PowerViz v2.5l, ScatterLab
//   beta 2e, ChiTable beta 3f, GaltonBoard beta 3f).
// v1f (1 Nov 2026, night): v1e's checks, unchanged, run on the page built from starter pack v8 (CICatcher beta 2e,
//   Norm3 v2.4c, NormExplorer beta 42d, StatDist v2.7g).
// v1e (1 Nov 2026, evening): v1d's checks, unchanged, run on the page built from starter pack v7 (SampDist v2.3e,
//   BayesTree beta 8f).
// v1d (1 Nov 2026): v1c's checks, run on the page built from starter pack v6 (TTestLab beta 1c, TTestLabG beta 1a).
//   One change: before 'own data listed' it waits up to 5 s for the page to list the file; in one run of four the
//   check read the list before the page had read the file.
// v1c: the Data Loader link is the Data Loader page's web address on GitHub Pages; index.html beside the page sends
// the browser on to it.
// v1b: the Firefox route (a browser without the folder API, with Firefox's user-agent): its own steps, the zip named
// for the chapter with the files at its top level (Extract All into ...\Calculators\Prime puts them straight there,
// as seen on Roger's computer on 1 Nov 2026), and the plain-language sections.
// v1a: the next steps depend on whether the pack's files are checked (the page's catalog says), and are checked
// against that.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http'), os = require('os');
const { execFileSync } = require('child_process');

const PAGE = path.resolve(process.argv[2]), PACK = path.resolve(process.argv[3]);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'pl-'));
execFileSync('unzip', ['-q', PACK, '-d', tmp]);
const packFile = rel => fs.readFileSync(path.join(tmp, 'Copy these into Prime', rel));
const sample = fs.readFileSync(path.join(tmp, 'Sample data (optional)', 'M1.hpmat'));

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail || ''); }
}

(async () => {
  const srv = http.createServer((q, r) => { r.setHeader('content-type', 'text/html; charset=utf-8'); r.end(fs.readFileSync(PAGE)); }).listen(8766);
  const browser = await chromium.launch();
  const WIN = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36 Edg/141.0.0.0';
  const ctx = await browser.newContext({ acceptDownloads: true, userAgent: WIN });
  // a real matrix file: the 16-byte header, then 8 bytes a cell
  const hpmat = (rows, cols, fill) => { const b = Buffer.alloc(16 + 8 * rows * cols, fill || 0); b[0] = 1; b[1] = 0; b[2] = 0x14; b[3] = 0x80; b.writeUInt32LE(2, 4); b.writeUInt32LE(rows, 8); b.writeUInt32LE(cols, 12); return b; };
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(String(e)));
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  // v1t: the Chromium on this machine (Chrome for Testing 153.0.8010.12, Playwright 1.63) stops with SIGTRAP when a
  // folder handle is READ BACK from IndexedDB; tests/idb_handle_probe_v1.js shows it with a page that holds nothing of
  // ours.  The page remembers its folder that way, so here the handle's NAME goes into IndexedDB in its place and the
  // folder is opened again by that name when it is read: the page's remembering still goes through IndexedDB and still
  // has to outlast a reload.  (The mock's HP Prime folder lies at the top of the browser's private file system.)
  await page.addInitScript(() => {
    const oput = IDBObjectStore.prototype.put, oget = IDBObjectStore.prototype.get;
    IDBObjectStore.prototype.put = function (v, k) {
      if (typeof FileSystemHandle !== 'undefined' && v instanceof FileSystemHandle) return oput.call(this, { __handleName: v.name }, k);
      return oput.call(this, v, k);
    };
    IDBObjectStore.prototype.get = function (k) {
      const real = oget.call(this, k), fake = { onsuccess: null, onerror: null, result: undefined };
      real.onsuccess = async () => {
        let r = real.result;
        if (r && r.__handleName) {
          try { r = await (await navigator.storage.getDirectory()).getDirectoryHandle(r.__handleName); } catch (e) { r = undefined; }
        }
        fake.result = r;
        if (fake.onsuccess) fake.onsuccess();
      };
      real.onerror = () => { if (fake.onerror) fake.onerror(); };
      return fake;
    };
  });
  await page.addInitScript(() => {
    window.__picks = 0;
    window.__pickPath = ['HP Prime'];
    window.showDirectoryPicker = async () => {
      window.__picks++;
      let d = await navigator.storage.getDirectory();
      for (const p of window.__pickPath) d = await d.getDirectoryHandle(p);
      return d;
    };
  });
  await page.goto('http://localhost:8766/');

  // ---- the mock folder ----
  await page.evaluate(async () => {
    const root = await navigator.storage.getDirectory();
    for await (const [n] of root.entries()) await root.removeEntry(n, { recursive: true });
    const put = async (p, bytes) => {
      const parts = p.split('/'); let d = root;
      for (let i = 0; i < parts.length - 1; i++) d = await d.getDirectoryHandle(parts[i], { create: true });
      const w = await (await d.getFileHandle(parts[parts.length - 1], { create: true })).createWritable();
      await w.write(new Uint8Array(bytes)); await w.close();
    };
    const C = 'HP Prime/Calculators/Prime/';
    await put(C + '&Statistics 1Var.hpappdir/Statistics 1Var.hpapp', [1, 2, 3]);
    await put(C + '&Function.hpappdir/Function.hpapp', [4, 5]);
    await put(C + 'calc.hpsettings', [9, 9, 9]);
    await put(C + 'L1.hplist', [7]);
    await put(C + 'M1.hpmat', [42, 42, 42, 42]);
    await put(C + 'OldHomework.hpprgm', [11, 12, 13]);
    await put(C + 'ChiTable.hpprgm', [21, 22]);
    await put(C + 'CentralLimit.hpappdir/CentralLimit.hpapp', [31]);
    await put(C + 'CentralLimit.hpappdir/CentralLimit.hpappprgm', [32, 33]);
    await put('HP Prime/Skins/skin.txt', [1]);
    await put('HP Prime/Temp/HPEmuInstance.lock', [49, 50]);
  });

  const readTree = async () => page.evaluate(async () => {
    const out = {};
    async function walk(d, pre) {
      for await (const [n, h] of d.entries()) {
        if (h.kind === 'directory') await walk(h, pre + n + '/');
        else out[pre + n] = Array.from(new Uint8Array(await (await h.getFile()).arrayBuffer()));
      }
    }
    await walk(await navigator.storage.getDirectory(), '');
    return out;
  });
  const same = (arr, buf) => arr && arr.length === buf.length && Buffer.from(arr).equals(buf);
  const C = 'HP Prime/Calculators/Prime/';

  // ---- the page itself ----
  check('15 chapter cards and 2 more', await page.locator('#chapters .card').count() === 17);
  check('chapter 1 is disabled (its program is still to come)', await page.locator('#chapters .card').first().isDisabled());
  check('Load is disabled before anything is picked', await page.locator('#load').isDisabled());
  check('on Windows there is no notice at the top', !(await page.isVisible('#platform')));
  const dlHref = await page.locator('a', { hasText: 'Data Loader' }).first().getAttribute('href');
  check('the Data Loader link is the Data Loader page on GitHub Pages',
        /^https:\/\/metcalfdds\.github\.io\/hp-prime-statistics\/data-loader\/DataLoader_v\d+[a-z]?\.html$/.test(dlHref), dlHref);
  const idx = fs.readFileSync(path.join(path.dirname(PAGE), 'index.html'), 'utf8');
  check('index.html beside the page sends the browser on to it',
        idx.includes('url=' + path.basename(PAGE) + '"') && idx.includes('href="' + path.basename(PAGE) + '"'));
  check('Edge/Chrome route shown, Firefox route hidden; running and done panels hidden',
        await page.isVisible('#mode-auto') && await page.isVisible('#step3auto') && !(await page.isVisible('#mode-manual')) &&
        !(await page.isVisible('#step3manual')) && !(await page.isVisible('#running')) && !(await page.isVisible('#done')));
  check('plain-language sections present: before you start, why for step 2, six help topics',
        /started it at least once/.test(await page.textContent('#s0').then(() => page.textContent('main'))) &&
        /saves its old memory right over the new programs/.test(await page.textContent('main')) &&
        await page.locator('.help details').count() === 6);

  // ---- 1. chapter 11 with the calculator running: refused, nothing changed ----
  const before = await readTree();
  await page.locator('#chapters .card', { hasText: 't-Tests: Two Samples' }).click();
  const sum = await page.textContent('#summary');
  check('chapter 11 picks TTestLabG, TDist3D, DataLoad, ResampLab', /DataLoad, ResampLab, TDist3D, TTestLabG/.test(sum), sum);
  await page.click('#load');
  await page.waitForSelector('#running:not([hidden])');
  check('running calculator: the warning shows, the done panel does not', await page.isVisible('#running') && !(await page.isVisible('#done')));
  check('running calculator: nothing written', JSON.stringify(await readTree()) === JSON.stringify(before));

  // ---- 2. lock gone, Try again: loads ----
  await page.evaluate(async () => { const r = await navigator.storage.getDirectory(); const t = await (await r.getDirectoryHandle('HP Prime')).getDirectoryHandle('Temp'); await t.removeEntry('HPEmuInstance.lock'); });
  await page.click('#again');
  await page.waitForSelector('#done:not([hidden])');
  check('after loading, the running warning is gone', !(await page.isVisible('#running')) && await page.isVisible('#done'));
  let t = await readTree();
  for (const p of ['TTestLabG.hpprgm', 'TDist3D.hpprgm', 'DataLoad.hpprgm', 'ResampLab.hpprgm'])
    check('loaded byte for byte: ' + p, same(t[C + p], packFile(p)));
  const progs = Object.keys(t).filter(k => k.startsWith(C) && k.endsWith('.hpprgm')).map(k => k.slice(C.length)).sort();
  check('only the chapter\'s programs are on the calculator', JSON.stringify(progs) === JSON.stringify(['DataLoad.hpprgm', 'ResampLab.hpprgm', 'TDist3D.hpprgm', 'TTestLabG.hpprgm']), progs);
  check('the old app is gone from the calculator', !Object.keys(t).some(k => k.startsWith(C + 'CentralLimit.hpappdir/')));
  const bk = Object.keys(t).filter(k => k.startsWith('HP Prime/Loader backups/'));
  const stamp1 = bk.length ? bk[0].split('/')[2] : '';
  check('backup folder named by date and time', /^\d{4}-\d\d-\d\d \d{4}$/.test(stamp1), stamp1);
  const B1 = 'HP Prime/Loader backups/' + stamp1 + '/';
  check('backup holds the old programs byte for byte', JSON.stringify(t[B1 + 'OldHomework.hpprgm']) === '[11,12,13]' && JSON.stringify(t[B1 + 'ChiTable.hpprgm']) === '[21,22]');
  check('backup holds the old app, both files', JSON.stringify(t[B1 + 'CentralLimit.hpappdir/CentralLimit.hpappprgm']) === '[32,33]' && JSON.stringify(t[B1 + 'CentralLimit.hpappdir/CentralLimit.hpapp']) === '[31]');
  check('HP\'s apps, settings, lists and M1 left alone', JSON.stringify(t[C + '&Statistics 1Var.hpappdir/Statistics 1Var.hpapp']) === '[1,2,3]' &&
        JSON.stringify(t[C + '&Function.hpappdir/Function.hpapp']) === '[4,5]' && JSON.stringify(t[C + 'calc.hpsettings']) === '[9,9,9]' &&
        JSON.stringify(t[C + 'L1.hplist']) === '[7]' && JSON.stringify(t[C + 'M1.hpmat']) === '[42,42,42,42]');
  check('nothing written outside Prime and the backup', Object.keys(t).every(k => k.startsWith(C) || k.startsWith('HP Prime/Loader backups/') || k.startsWith('HP Prime/Skins/')));
  const steps = await page.textContent('#nextsteps');
  const allChecked = await page.evaluate(() => CAT.all_checked);
  check('next steps name the programs', /DataLoad, ResampLab, TDist3D, TTestLabG/.test(steps), steps);
  check(allChecked ? 'checked pack: tap and Run, Check only as a fallback' : 'unchecked pack: the Check step',
        allChecked ? (/Tap one, then tap Run at the bottom right\. That is all\./.test(steps) && /If one ever says Syntax Error/.test(steps) && !/The first time you run each one/.test(steps))
                   : /The first time you run each one/.test(steps), steps);
  check('the picker was used once', await page.evaluate(() => window.__picks) === 1);

  // ---- 3. reload: the folder is remembered; chapter 7 + the sample data ----
  await page.reload();
  await page.locator('#chapters .card', { hasText: 'Sampling Distributions' }).click();
  await page.check('#rossi');
  await page.click('#load');
  await page.waitForSelector('#done:not([hidden])');
  check('after a reload the folder is remembered (no second pick)', await page.evaluate(() => window.__picks) === 0);
  t = await readTree();
  for (const p of ['SampDist.hpprgm', 'GaltonBoard.hpprgm', 'CentralLimit.hpappdir/CentralLimit.hpapp', 'CentralLimit.hpappdir/CentralLimit.hpappnote', 'CentralLimit.hpappdir/CentralLimit.hpappprgm'])
    check('loaded byte for byte: ' + p, same(t[C + p], packFile(p)));
  check('the sample data is M1, byte for byte', same(t[C + 'M1.hpmat'], sample));
  check('chapter 7 has no DataLoad of its own: with data, DataLoad comes too', same(t[C + 'DataLoad.hpprgm'], packFile('DataLoad.hpprgm')));
  check('chapter 11\'s programs went to a second backup', Object.keys(t).some(k => /Loader backups\/[^/]+ \(2\)\/TTestLabG\.hpprgm$/.test(k)) ||
        Object.keys(t).filter(k => k.endsWith('/TTestLabG.hpprgm') && k.includes('Loader backups')).length === 1);
  check('the old M1 is in a backup, byte for byte', Object.entries(t).some(([k, v]) => k.includes('Loader backups') && k.endsWith('/M1.hpmat') && JSON.stringify(v) === '[42,42,42,42]'));
  const steps2 = await page.textContent('#nextsteps');
  check('next steps: CentralLimit is an app; the data and DataLoad', /CentralLimit/.test(steps2) && /Statistics 1Var/.test(steps2), steps2);

  // ---- 4. your own data file, on its own: it is ADDED, with DataLoad, and the programs stay ----
  await page.reload();
  const own3 = hpmat(4, 2, 7);
  await page.setInputFiles('#ownfile', { name: 'M3.hpmat', mimeType: 'application/octet-stream', buffer: own3 });
  // v1d: wait for the page to list the file (it reads the file first); one run in four read the list too early
  await page.waitForFunction(() => /M3\.hpmat/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('own data listed', /Your data: M3\.hpmat\./.test(await page.textContent('#ownlist')));
  const sumA = await page.textContent('#summary');
  check('data on its own: the summary says DataLoad is added and the programs stay', /Will add the data M3 and the program DataLoad/.test(sumA) && /The programs already on your calculator stay/.test(sumA), sumA);
  const before4 = await readTree();
  await page.click('#load');
  await page.waitForSelector('#done:not([hidden])');
  t = await readTree();
  check('own data written as M3, byte for byte', same(t[C + 'M3.hpmat'], own3));
  check('data on its own: DataLoad is put on the calculator, byte for byte', same(t[C + 'DataLoad.hpprgm'], packFile('DataLoad.hpprgm')));
  check('data on its own: every program and app that was on the calculator is still there, unchanged',
        Object.keys(before4).filter(k => k.startsWith(C)).every(k => JSON.stringify(t[k]) === JSON.stringify(before4[k])) &&
        Object.keys(before4).filter(k => k.startsWith(C) && k.endsWith('.hpprgm')).length === 3 &&
        same(t[C + 'SampDist.hpprgm'], packFile('SampDist.hpprgm')) && same(t[C + 'CentralLimit.hpappdir/CentralLimit.hpapp'], packFile('CentralLimit.hpappdir/CentralLimit.hpapp')));
  const newBk = Object.keys(t).filter(k => k.includes('Loader backups') && !(k in before4));
  check('data on its own: the one thing put aside is the DataLoad it replaced (chapter 7 with data had brought one)',
        newBk.length === 1 && /\/DataLoad\.hpprgm$/.test(newBk[0]) && same(t[newBk[0]], packFile('DataLoad.hpprgm')), newBk);
  const rep4 = await page.textContent('#report'), steps4 = await page.textContent('#nextsteps');
  check('data on its own: the report says the other programs were left, and the steps name DataLoad', /other programs on the calculator were left where they are/.test(rep4) && /files that were replaced were moved, not deleted/.test(rep4) && /DataLoad/.test(steps4) && /Statistics 1Var/.test(steps4), rep4);
  // a second file for the same matrix: the old M3 and the old DataLoad go to a backup, nothing else moves
  const own3b = hpmat(2, 3, 9);
  await page.setInputFiles('#ownfile', { name: 'M3 (2).hpmat', mimeType: 'application/octet-stream', buffer: own3b });
  await page.waitForFunction(() => /M3\.hpmat/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('"M3 (2).hpmat", a second download, is taken as M3', /Your data: M3\.hpmat\./.test(await page.textContent('#ownlist')));
  await page.click('#load');
  await page.waitForFunction(() => /every file read back and checked/.test(document.getElementById('status').textContent));
  await page.waitForSelector('#done:not([hidden])');
  t = await readTree();
  check('the new M3 replaced the old one, which is in a backup byte for byte', same(t[C + 'M3.hpmat'], own3b) &&
        Object.entries(t).some(([k, v]) => k.includes('Loader backups') && k.endsWith('/M3.hpmat') && same(v, own3)));
  check('... and the programs are still all there', same(t[C + 'SampDist.hpprgm'], packFile('SampDist.hpprgm')) && same(t[C + 'GaltonBoard.hpprgm'], packFile('GaltonBoard.hpprgm')) &&
        same(t[C + 'DataLoad.hpprgm'], packFile('DataLoad.hpprgm')));

  // ---- 4b. a data file is opened before it is taken ----
  await page.reload();
  await page.setInputFiles('#ownfile', { name: 'mydata.hpmat', mimeType: 'application/octet-stream', buffer: hpmat(1, 1) });
  await page.waitForFunction(() => /Not added/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('a badly named data file is refused with a reason', /M0\.hpmat to M9\.hpmat/.test(await page.textContent('#ownlist')));
  const refusedFor = async (name, buf, re) => {
    await page.setInputFiles('#ownfile', { name: name, mimeType: 'application/octet-stream', buffer: buf });
    await page.waitForFunction(n => document.querySelector('#ownlist').textContent.includes(n), name, { timeout: 5000 }).catch(() => {});
    const txt = await page.textContent('#ownlist');
    return re.test(txt) && !/Your data/.test(txt) ? true : txt;
  };
  let rf = await refusedFor('M4.hpmat', Buffer.from([1, 0, 20, 128]), /M4\.hpmat: it is too short to be a calculator matrix file/);
  check('a 4-byte file named M4.hpmat is refused: too short', rf === true, rf);
  rf = await refusedFor('M1.hpmat', Buffer.from('week,arrest,fin,age,prio\n20,1,0,27,3\n17,1,0,18,8\n'), /does not begin the way a calculator matrix file does/);
  check('a CSV file renamed M1.hpmat is refused: not a matrix file', rf === true, rf);
  rf = await refusedFor('M2.hpmat', hpmat(5, 2).subarray(0, 60), /its size does not match the rows and columns it names/);
  check('a matrix file cut short is refused', rf === true, rf);
  check('... and after three refusals nothing is picked and Load is off', /Nothing picked yet/.test(await page.textContent('#summary')) && await page.isDisabled('#load'));

  // ---- 4c. a chapter without DataLoad, with data: DataLoad comes too; the student's own M1 wins over the sample ----
  await page.locator('#chapters .card', { hasText: 'Correlation and Regression' }).click();
  await page.check('#rossi');
  const sumC = await page.textContent('#summary');
  check('chapter 13 with the sample data: DataLoad is in the list, with the reason', /BiNorm3D, DataLoad, ScatterLab/.test(sumC) && /DataLoad is added because the data need it/.test(sumC), sumC);
  const own1 = hpmat(3, 1, 5);
  await page.setInputFiles('#ownfile', { name: 'M1.hpmat', mimeType: 'application/octet-stream', buffer: own1 });
  await page.waitForFunction(() => /Your data: M1\.hpmat/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('own M1 beside the sample data: the page says which one is used', /Your own M1\.hpmat is used; the sample data set would go into the same matrix, so it is left out/.test(await page.textContent('#summary')), await page.textContent('#summary'));
  await page.click('#load');
  await page.waitForSelector('#done:not([hidden])');
  t = await readTree();
  check('chapter 13 with data: ScatterLab, BiNorm3D and DataLoad are on the calculator, and nothing else', JSON.stringify(Object.keys(t).filter(k => k.startsWith(C) && k.endsWith('.hpprgm')).map(k => k.slice(C.length)).sort()) ===
        JSON.stringify(['BiNorm3D.hpprgm', 'DataLoad.hpprgm', 'ScatterLab.hpprgm']) && same(t[C + 'DataLoad.hpprgm'], packFile('DataLoad.hpprgm')));
  check('... and M1 is the student\'s own file, not the sample', same(t[C + 'M1.hpmat'], own1));

  // ---- 5. the wrong folder ----
  await page.reload();
  await page.locator('#chapters .card', { hasText: 'CHAPTER 14' }).click();
  await page.evaluate(() => { window.__pickPath = ['HP Prime', 'Calculators']; });
  await page.click('#repick');
  await page.waitForFunction(() => /HP Prime itself/.test(document.getElementById('status').textContent));
  check('picking Calculators explains which folder to pick', true);
  await page.evaluate(() => { window.__pickPath = ['HP Prime', 'Skins']; });
  await page.click('#repick');
  await page.waitForFunction(() => /no calculator in it/.test(document.getElementById('status').textContent));
  check('picking an unrelated folder explains which folder to pick', true);
  await page.evaluate(() => { window.__pickPath = []; });       // the root above HP Prime, as if Documents
  await page.click('#repick');
  await page.waitForSelector('#done:not([hidden])');
  t = await readTree();
  check('picking Documents finds HP Prime inside it', same(t[C + 'AnovaLab.hpprgm'], packFile('AnovaLab.hpprgm')));

  // ---- 6. cancelling the picker ----
  await page.evaluate(() => { window.showDirectoryPicker = async () => { throw new DOMException('cancelled', 'AbortError'); }; });
  await page.click('#repick');
  await page.waitForFunction(() => /No folder was chosen/.test(document.getElementById('status').textContent));
  check('cancelling the picker says nothing was loaded', true);

  // ---- 7. everything, and the zip ----
  await page.reload();
  await page.locator('#chapters .card', { hasText: 'All 31 programs' }).click();
  await page.locator('.help summary', { hasText: 'Connectivity Kit' }).click();
  check('Kit help: the Bonjour reminder shows first, with how to check it',
        await page.locator('.help details[open] .panel.warn', { hasText: 'make sure Bonjour is running' }).isVisible() &&
        /Bonjour Service/.test(await page.textContent('.help details[open]')) && /Running/.test(await page.textContent('.help details[open]')));
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#download')]);
  check('everything downloads as HP_Prime_programs.zip', dl.suggestedFilename() === 'HP_Prime_programs.zip', dl.suggestedFilename());
  const zp = path.join(tmp, 'dl.zip'); await dl.saveAs(zp);
  const out = path.join(tmp, 'dl'); execFileSync('unzip', ['-q', zp, '-d', out]);
  const packed = fs.readdirSync(path.join(tmp, 'Copy these into Prime'));
  let allSame = true;
  for (const n of packed) {
    if (n.endsWith('.hpappdir')) { for (const f of fs.readdirSync(path.join(tmp, 'Copy these into Prime', n))) allSame = allSame && fs.readFileSync(path.join(out, n, f)).equals(packFile(n + '/' + f)); }
    else allSame = allSame && fs.readFileSync(path.join(out, n)).equals(packFile(n));
  }
  check('zip of everything: all 31 programs and the app, byte for byte', allSame && fs.readdirSync(out).length === packed.length, fs.readdirSync(out).length);
  await page.click('#load');
  await page.waitForSelector('#done:not([hidden])');
  t = await readTree();
  check('everything: 30 programs and the app on the calculator', Object.keys(t).filter(k => k.startsWith(C) && k.endsWith('.hpprgm')).length === 30 &&
        Object.keys(t).filter(k => k.startsWith(C + 'CentralLimit.hpappdir/')).length === 3);

  // ---- 8. Firefox: no folder API, Firefox's user-agent ----
  const fctx = await browser.newContext({ acceptDownloads: true,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0' });
  const p2 = await fctx.newPage();
  const errs2 = []; p2.on('pageerror', e => errs2.push(String(e)));
  await p2.addInitScript(() => { delete window.showDirectoryPicker; });
  await p2.goto('http://localhost:8766/');
  check('Firefox: its own route shows, the Edge route is hidden',
        await p2.isVisible('#mode-manual') && await p2.isVisible('#step3manual') && !(await p2.isVisible('#mode-auto')) && !(await p2.isVisible('#step3auto')));
  check('Firefox: named, with the reason in plain words', (await p2.textContent('#brname')) === 'Firefox' &&
        /never lets a web page put files into a folder/.test(await p2.textContent('#mode-manual')));
  check('Firefox: Download is off until a chapter is picked', await p2.locator('#download2').isDisabled());
  await p2.locator('#chapters .card', { hasText: 'Chi-Square' }).click();
  check('Firefox: the steps name the zip and the programs', (await p2.textContent('#zipname')) === 'HP_Prime_Chapter_12.zip' &&
        (await p2.textContent('#manualprogs')) === 'ChiTable, FitCheck');
  const [fdl] = await Promise.all([p2.waitForEvent('download'), p2.click('#download2')]);
  check('Firefox: the download is HP_Prime_Chapter_12.zip', fdl.suggestedFilename() === 'HP_Prime_Chapter_12.zip', fdl.suggestedFilename());
  const fz = path.join(tmp, 'ff.zip'); await fdl.saveAs(fz);
  const fo = path.join(tmp, 'ff'); execFileSync('unzip', ['-q', fz, '-d', fo]);
  const fl = fs.readdirSync(fo).sort();
  check('Firefox: the zip holds the chapter\'s programs at its top level, byte for byte',
        JSON.stringify(fl) === JSON.stringify(['ChiTable.hpprgm', 'FitCheck.hpprgm']) &&
        fs.readFileSync(path.join(fo, 'ChiTable.hpprgm')).equals(packFile('ChiTable.hpprgm')) &&
        fs.readFileSync(path.join(fo, 'FitCheck.hpprgm')).equals(packFile('FitCheck.hpprgm')), fl);
  check('Firefox: the status says what to do next', /Now go on to the next step/.test(await p2.textContent('#dlstatus2')));
  await p2.locator('#chapters .card', { hasText: 'CHAPTER 7' }).click();
  check('Firefox: two chapters make HP_Prime_Chapters_7_12.zip; the app note shows for CentralLimit',
        (await p2.textContent('#zipname')) === 'HP_Prime_Chapters_7_12.zip' && await p2.isVisible('#manualapp'));
  await p2.check('#rossi');
  check('Firefox: the data note shows when data is picked, and DataLoad joins the list', await p2.isVisible('#manualdata') && /DataLoad/.test(await p2.textContent('#manualprogs')), await p2.textContent('#manualprogs'));
  check('Firefox on Windows: no notice at the top', !(await p2.isVisible('#platform')));
  check('Firefox: no errors in the page', errs2.length === 0, errs2);

  // ---- 8b. a phone and a Mac ----
  const phone = await (await browser.newContext({ userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36' })).newPage();
  await phone.addInitScript(() => { delete window.showDirectoryPicker; });
  await phone.goto('http://localhost:8766/');
  check('a phone: the notice says the page needs the Windows computer, and gives the address', await phone.isVisible('#platform') &&
        /needs your Windows computer/.test(await phone.textContent('#platformh')) && /phone or a tablet/.test(await phone.textContent('#platformp')) &&
        /http:\/\/localhost:8766\//.test(await phone.textContent('#platformp')), await phone.textContent('#platformp'));
  check('a phone: neither "this page can do the copying" nor "that\'s fine, a few more clicks" is shown', !(await phone.isVisible('#mode-auto')) && !(await phone.isVisible('#mode-manual')));
  const mac = await (await browser.newContext({ userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15' })).newPage();
  await mac.addInitScript(() => { delete window.showDirectoryPicker; });
  await mac.goto('http://localhost:8766/');
  check('a Mac: the notice says the steps were written for Windows', await mac.isVisible('#platform') && /written for Windows/.test(await mac.textContent('#platformh')) &&
        /Connectivity Kit/.test(await mac.textContent('#platformp')), await mac.textContent('#platformp'));
  const old = await (await browser.newContext({ userAgent: WIN })).newPage();
  await old.addInitScript(() => { delete window.DecompressionStream; });
  await old.goto('http://localhost:8766/');
  await old.locator('#chapters .card', { hasText: 'Chi-Square' }).click();
  check('a browser that cannot unpack: the notice says so, and Load and Download stay off', await old.isVisible('#platform') && /too old for this page/.test(await old.textContent('#platformh')) &&
        await old.isDisabled('#load') && await old.isDisabled('#download'));

  // ---- 9. opened as a local file ----
  const p3 = await ctx.newPage();
  const errs3 = []; p3.on('pageerror', e => errs3.push(String(e)));
  await p3.goto('file://' + PAGE);
  check('opens as a local file without errors', errs3.length === 0 && await p3.locator('#chapters .card').count() === 17, errs3);

  check('no errors in the page', errors.length === 0, errors);
  console.log(`\n${pass} PASS, ${fail} FAIL`);
  await browser.close(); srv.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
