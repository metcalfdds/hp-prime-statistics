// test_loader_v2a.js -- drives PrimeLoader_v2a.html in Chromium against a mock Virtual Calculator folder, and its
// switched-off USB route against a pretend calculator.
// Roger Metcalf & Claude, 17 Nov 2026, night.   node tests/test_loader_v2a.js PrimeLoader_v2a.html PACK.zip
//
// v2a is a new page (two questions and one button), so this is a new test, on the scaffolding of test_loader_v1v.js:
// the browser's folder picker is replaced by one that returns a folder in the browser's private file system (OPFS),
// seeded to look like Documents\HP Prime on a PC that has run the Virtual Calculator (Calculators\Prime with HP's
// apps, settings, an old book program, an old copy of the app, a program of the student's own and a matrix; Temp with
// the lock file), and every file the page writes is compared byte for byte with the starter pack it was built from.
//
// What v2a must do, and each is checked here:
//   - the page asks which calculator and which programs, and has one button;
//   - ALL THE PROGRAMS are added: what was on the calculator stays, a file of the same name is replaced, and the old
//     one is in a dated backup byte for byte;
//   - ONE CHAPTER leaves the calculator with that chapter's programs and TestChooser: the book's other programs are in
//     the backup, and a program of the student's own is NOT moved (v1 moved it);
//   - programs ticked one by one, and a data file on its own, are added, with DataLoad for the data;
//   - choosing "One chapter" without choosing a chapter moves nothing;
//   - A REAL HP PRIME gets the same choice as one zip and the Connectivity Kit's steps, and no Load button;
//   - a calculator that is open is not written to; the wrong folder, a cancelled picker, a bad data file, a phone,
//     a Mac and an old browser each get their sentence (v1v's checks, kept);
//   - Firefox's route: one zip of the choice, to unpack;
//   - the USB route does not show without ?usb=1; with it, each program is sent, read back and compared with
//     programs/, and the first one that cannot be read back stops the run.
// (The Chromium on this machine stops with SIGTRAP when a folder handle is read back from IndexedDB, so the handle's
// NAME goes into IndexedDB in its place: v1t's note, in the code below.)
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
  // (v2a: both scripts go on the context, not the page, so that the second and third pages the test opens have them.)
  // v1t: the Chromium on this machine (Chrome for Testing 153.0.8010.12, Playwright 1.63) stops with SIGTRAP when a
  // folder handle is READ BACK from IndexedDB; tests/idb_handle_probe_v1.js shows it with a page that holds nothing of
  // ours.  The page remembers its folder that way, so here the handle's NAME goes into IndexedDB in its place and the
  // folder is opened again by that name when it is read: the page's remembering still goes through IndexedDB and still
  // has to outlast a reload.  (The mock's HP Prime folder lies at the top of the browser's private file system.)
  await ctx.addInitScript(() => {
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
  await ctx.addInitScript(() => {
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

  // v2a: every file of the mock folder as its length and SHA-256 (and its bytes when it is a few bytes long).  The
  // tree holds the whole pack several times over once the backups fill, and v1v's way, every byte of every file sent
  // back to Node after each load, took most of the test's twelve minutes.
  const readTree = async () => page.evaluate(async () => {
    const out = {};
    async function walk(d, pre) {
      for await (const [n, h] of d.entries()) {
        if (h.kind === 'directory') { await walk(h, pre + n + '/'); continue; }
        const b = new Uint8Array(await (await h.getFile()).arrayBuffer());
        const dg = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', b))).map(x => x.toString(16).padStart(2, '0')).join('');
        out[pre + n] = b.length <= 64 ? { n: b.length, h: dg, a: Array.from(b) } : { n: b.length, h: dg };
      }
    }
    await walk(await navigator.storage.getDirectory(), '');
    return out;
  });
  const sha = buf => require('crypto').createHash('sha256').update(buf).digest('hex');
  const same = (e, buf) => !!e && e.n === buf.length && e.h === sha(buf);
  const small = e => (e && e.a ? JSON.stringify(e.a) : null);
  const C = 'HP Prime/Calculators/Prime/';

  // ---- the page itself ----
  const names = await page.evaluate(() => Object.keys(CAT.programs).sort((a, b) => a.localeCompare(b)));
  const steps = async p => p.$$eval('.step:not([hidden]) > h2', e => e.map(x => x.textContent.trim()));
  check('the page is two questions and one button: which calculator, which programs, Load',
        JSON.stringify(await steps(page)) === JSON.stringify(['1Which calculator?', '2Which programs?', '3Load', 'Something not working?']), JSON.stringify(await steps(page)));
  check('it opens on the Virtual Calculator and all ' + names.length + ' programs, with Load ready', names.length === 31 && await page.isChecked('#t_vc') && await page.isChecked('#w_all') &&
        !(await page.isDisabled('#load')) && (await page.textContent('#summary')) === 'All 31 programs.' && /All 31 programs/.test(await page.textContent('.choice:has(#w_all)')));
  check('it says what Load will do to what is there: added, and what is there stays', (await page.textContent('#effect')) === 'They are added: programs already on the calculator stay.');
  check('the chapter list has 15 chapters; chapter 1, which has no program yet, cannot be chosen',
        await page.locator('#chapter option').count() === 16 && await page.locator('#chapter option[value="1"]').isDisabled());
  check('single programs and data are folded away: the 31 tick boxes exist and are not shown', !(await page.isVisible('#proglist')) && !(await page.isVisible('#rossi')) &&
        await page.locator('#proglist .prog input').count() === 31 && /More choices: single programs, and data/.test(await page.textContent('#more > summary')));
  check('on Windows there is no notice at the top', !(await page.isVisible('#platform')));
  const dlHref = await page.locator('a', { hasText: 'Data Loader' }).first().getAttribute('href');
  check('the Data Loader link is the Data Loader page on GitHub Pages',
        /^https:\/\/metcalfdds\.github\.io\/hp-prime-statistics\/data-loader\/DataLoader_v\d+[a-z]?\.html$/.test(dlHref), dlHref);
  const idx = fs.readFileSync(path.join(path.dirname(PAGE), 'index.html'), 'utf8');
  check('index.html beside the page sends the browser on to it',
        idx.includes('url=' + path.basename(PAGE) + '"') && idx.includes('href="' + path.basename(PAGE) + '"'));
  check('Edge/Chrome route shown; the Firefox route, the real-calculator route, and the running and done panels hidden',
        await page.isVisible('#step3auto') && !(await page.isVisible('#mode-manual')) && !(await page.isVisible('#step3manual')) &&
        !(await page.isVisible('#step3real')) && !(await page.isVisible('#running')) && !(await page.isVisible('#done')));
  check('seven help topics, the first for a student without the Virtual Calculator, which step 1 links to', await page.locator('.help details').count() === 7 &&
        /don't have the Virtual Calculator yet/.test(await page.textContent('.help details:first-of-type summary')) &&
        (await page.getAttribute('.choice:has(#t_vc) a', 'href')) === '#need');
  check('the USB route is in the page and not shown', await page.evaluate(() => typeof PrimeUSB === 'object' && !usbOn) && !(await page.isVisible('#usbpanel')));
  const onCalc = t => Object.keys(t).filter(k => k.startsWith(C) && k.endsWith('.hpprgm')).map(k => k.slice(C.length)).sort();
  const folders = t => Array.from(new Set(Object.keys(t).filter(k => k.startsWith('HP Prime/Loader backups/')).map(k => k.split('/')[2]))).sort();
  const inBackup = (t, f) => Object.keys(t).filter(k => k.startsWith('HP Prime/Loader backups/' + f + '/')).map(k => k.slice(('HP Prime/Loader backups/' + f + '/').length)).sort();
  const hpOwn = t => small(t[C + '&Statistics 1Var.hpappdir/Statistics 1Var.hpapp']) === '[1,2,3]' && small(t[C + '&Function.hpappdir/Function.hpapp']) === '[4,5]' &&
                     small(t[C + 'calc.hpsettings']) === '[9,9,9]' && small(t[C + 'L1.hplist']) === '[7]';
  const packed = fs.readdirSync(path.join(tmp, 'Copy these into Prime'));
  const packPrg = packed.filter(n => n.endsWith('.hpprgm')).sort();
  const APP = ['CentralLimit.hpappdir/CentralLimit.hpapp', 'CentralLimit.hpappdir/CentralLimit.hpappnote', 'CentralLimit.hpappdir/CentralLimit.hpappprgm'];
  const loaded = async () => { await page.waitForFunction(() => /every file read back and checked/.test(document.getElementById('status').textContent)); await page.waitForSelector('#done:not([hidden])'); return readTree(); };

  // ---- 1. all the programs, with the calculator running: refused, nothing changed ----
  const before = await readTree();
  await page.click('#load');
  await page.waitForSelector('#running:not([hidden])');
  check('running calculator: the warning shows, the done panel does not', await page.isVisible('#running') && !(await page.isVisible('#done')));
  check('running calculator: nothing written', JSON.stringify(await readTree()) === JSON.stringify(before));

  // ---- 2. lock gone, Try again: all 31 are ADDED, and what was there stays ----
  await page.evaluate(async () => { const r = await navigator.storage.getDirectory(); const t = await (await r.getDirectoryHandle('HP Prime')).getDirectoryHandle('Temp'); await t.removeEntry('HPEmuInstance.lock'); });
  await page.click('#again');
  let t = await loaded();
  check('after loading, the running warning is gone', !(await page.isVisible('#running')) && await page.isVisible('#done'));
  check('all the programs: the pack\'s 30 program files and the app\'s three, byte for byte', packPrg.length === 30 && packPrg.every(n => same(t[C + n], packFile(n))) && APP.every(n => same(t[C + n], packFile(n))) &&
        Object.keys(t).filter(k => k.startsWith(C + 'CentralLimit.hpappdir/')).length === 3);
  check('all the programs: the student\'s own program is still there, untouched, and so is the matrix', small(t[C + 'OldHomework.hpprgm']) === '[11,12,13]' && small(t[C + 'M1.hpmat']) === '[42,42,42,42]' &&
        JSON.stringify(onCalc(t)) === JSON.stringify(packPrg.concat(['OldHomework.hpprgm']).sort()));
  const f1 = folders(t);
  check('one backup folder, named by date and time', f1.length === 1 && /^\d{4}-\d\d-\d\d \d{4}$/.test(f1[0]), f1);
  check('the backup holds exactly what was replaced, byte for byte: the old ChiTable and the old app',
        JSON.stringify(inBackup(t, f1[0])) === JSON.stringify(['CentralLimit.hpappdir/CentralLimit.hpapp', 'CentralLimit.hpappdir/CentralLimit.hpappprgm', 'ChiTable.hpprgm']) &&
        small(t['HP Prime/Loader backups/' + f1[0] + '/ChiTable.hpprgm']) === '[21,22]' && small(t['HP Prime/Loader backups/' + f1[0] + '/CentralLimit.hpappdir/CentralLimit.hpappprgm']) === '[32,33]', inBackup(t, f1[0]));
  check('HP\'s apps, settings and lists left alone', hpOwn(t));
  check('nothing written outside Prime and the backup', Object.keys(t).every(k => k in before || k.startsWith(C) || k.startsWith('HP Prime/Loader backups/')));
  let nx = await page.textContent('#nextsteps'), rep = await page.textContent('#report');
  const allChecked = await page.evaluate(() => CAT.all_checked);
  check('next steps: the Program Catalog, and CentralLimit as an app', /Your programs are all listed there/.test(nx) && /CentralLimit is an app/.test(nx), nx);
  check(allChecked ? 'checked pack: tap and Run, Check only as a fallback' : 'unchecked pack: the Check step',
        allChecked ? (/Tap one, then tap Run at the bottom right\. That is all\./.test(nx) && /If one ever says Syntax Error/.test(nx) && !/The first time you run each one/.test(nx))
                   : /The first time you run each one/.test(nx), nx);
  check('the report: 33 files, the programs already there left, the replaced files in the backup and not deleted', /^33 files went onto the calculator, and each was read back and checked\./.test(rep) &&
        /already on the calculator were left where they are/.test(rep) && /The files that were replaced are in Documents\\HP Prime\\Loader backups\\/.test(rep) && /not deleted/.test(rep), rep);
  check('the picker was used once', await page.evaluate(() => window.__picks) === 1);

  // ---- 3. reload; one chapter: the calculator lists that chapter, the book's others are in the backup, the student's own stays ----
  await page.reload();
  await page.selectOption('#chapter', '11');
  check('choosing a chapter in the list chooses "One chapter"', await page.isChecked('#w_chapter') && !(await page.isChecked('#w_all')));
  let sum = await page.textContent('#summary');
  check('the summary names chapter 11\'s programs, and TestChooser with its reason', sum === 'Chapter 11, t-Tests: Two Samples: DataLoad, ResampLab, TDist3D, TestChooser, TTestLabG. TestChooser, the which-test flowchart, goes with every chapter.', sum);
  check('... and says the book\'s other programs are moved off and the student\'s own stay', /The book's other programs are moved off into a backup folder; programs of your own stay\./.test(await page.textContent('#effect')));
  await page.click('#load');
  t = await loaded();
  check('after a reload the folder is remembered (no second pick)', await page.evaluate(() => window.__picks) === 0);
  const ch11 = ['DataLoad.hpprgm', 'ResampLab.hpprgm', 'TDist3D.hpprgm', 'TTestLabG.hpprgm', 'TestChooser.hpprgm'];
  check('one chapter: its five programs are on the calculator byte for byte, and the student\'s own program with them, untouched',
        JSON.stringify(onCalc(t)) === JSON.stringify(ch11.concat(['OldHomework.hpprgm']).sort()) && ch11.every(n => same(t[C + n], packFile(n))) && small(t[C + 'OldHomework.hpprgm']) === '[11,12,13]', onCalc(t));
  const f2 = folders(t).filter(f => !f1.includes(f));
  check('one chapter: a second backup folder holds every book program that was there, 30 and the app, byte for byte', f2.length === 1 &&
        JSON.stringify(inBackup(t, f2[0])) === JSON.stringify(packPrg.concat(APP).sort()) && packPrg.concat(APP).every(n => same(t['HP Prime/Loader backups/' + f2[0] + '/' + n], packFile(n))), f2);
  check('one chapter: the app is off the calculator; HP\'s apps, settings, lists and the matrix stay', !Object.keys(t).some(k => k.startsWith(C + 'CentralLimit.hpappdir/')) && hpOwn(t) && small(t[C + 'M1.hpmat']) === '[42,42,42,42]');
  rep = await page.textContent('#report'); nx = await page.textContent('#nextsteps');
  check('the report says the book\'s other programs were moved off, the student\'s own left, and where they are', /The book's other programs were moved off/.test(rep) && /Programs of your own were left where they are/.test(rep) &&
        /What was moved off, and any file that was replaced, is in Documents\\HP Prime\\Loader backups\\/.test(rep), rep);
  check('next steps name the five programs', /DataLoad, ResampLab, TDist3D, TestChooser, TTestLabG/.test(nx), nx);

  // ---- 4. the next chapter, with the sample data ----
  await page.reload();
  await page.selectOption('#chapter', '7');
  await page.locator('#more > summary').click();
  await page.check('#rossi');
  sum = await page.textContent('#summary');
  check('chapter 7 with the sample data: DataLoad is added, with the reason', sum === 'Chapter 7, Sampling Distributions and the CLT: CentralLimit, GaltonBoard, SampDist, TestChooser, and the data M1. TestChooser, the which-test flowchart, goes with every chapter. DataLoad is added because the data need it.', sum);
  await page.click('#load');
  t = await loaded();
  check('chapter 7: its programs, DataLoad and the app on the calculator byte for byte; chapter 11\'s others gone to the backup; the student\'s own stays',
        JSON.stringify(onCalc(t)) === JSON.stringify(['DataLoad.hpprgm', 'GaltonBoard.hpprgm', 'OldHomework.hpprgm', 'SampDist.hpprgm', 'TestChooser.hpprgm']) &&
        ['DataLoad.hpprgm', 'GaltonBoard.hpprgm', 'SampDist.hpprgm', 'TestChooser.hpprgm'].concat(APP).every(n => same(t[C + n], packFile(n))), onCalc(t));
  const f3 = folders(t).filter(f => !f1.includes(f) && !f2.includes(f));
  check('the sample data is M1 byte for byte, and the old M1 is in the third backup with chapter 11\'s five programs', same(t[C + 'M1.hpmat'], sample) && f3.length === 1 &&
        JSON.stringify(inBackup(t, f3[0])) === JSON.stringify(ch11.concat(['M1.hpmat']).sort()) && small(t['HP Prime/Loader backups/' + f3[0] + '/M1.hpmat']) === '[42,42,42,42]', f3.length && inBackup(t, f3[0]));
  nx = await page.textContent('#nextsteps');
  check('next steps: CentralLimit is an app; the data and DataLoad', /CentralLimit is an app/.test(nx) && /Statistics 1Var/.test(nx), nx);

  // ---- 4b. a click on another choice while a load is under way does not switch Load back on ----
  await page.reload();
  await page.selectOption('#chapter', '7');
  await page.evaluate(() => { window.__slow = LoaderCore.install; LoaderCore.install = async (c, f) => { await new Promise(r => setTimeout(r, 700)); return window.__slow(c, f); }; });
  await page.click('#load');
  await page.waitForFunction(() => /Loading \d+ files/.test(document.getElementById('status').textContent));
  await page.check('#w_all');
  const midway = await page.isDisabled('#load');
  await page.evaluate(() => document.getElementById('load').click());
  t = await loaded();
  check('while a load is under way, choosing something else leaves Load off, and a second click starts nothing: what was chosen at the click is what is loaded',
        midway === true && JSON.stringify(onCalc(t)) === JSON.stringify(['DataLoad.hpprgm', 'GaltonBoard.hpprgm', 'OldHomework.hpprgm', 'SampDist.hpprgm', 'TestChooser.hpprgm'].filter(n => n !== 'DataLoad.hpprgm')) &&
        !(await page.isDisabled('#load')), JSON.stringify(onCalc(t)));

  // ---- 5. programs ticked one by one are added ----
  await page.reload();
  await page.locator('#more > summary').click();
  await page.check('#w_pick');
  check('"Only the programs I tick": the list of 31 shows, each with what it does and its chapters; nothing ticked, so Load is off',
        await page.isVisible('#proglist') && await page.locator('#proglist .prog .what').count() === 31 && /Ch\. 9, 11/.test(await page.textContent('label.prog:has(#p_TTestLabG)')) &&
        /any chapter/.test(await page.textContent('label.prog:has(#p_TestChooser)')) && await page.isDisabled('#load') && /Nothing ticked yet/.test(await page.textContent('#summary')));
  await page.check('#p_Norm3'); await page.check('#p_ChiTable');
  check('two ticks: the summary names them', (await page.textContent('#summary')) === '2 programs ticked: ChiTable, Norm3.', await page.textContent('#summary'));
  const nb = folders(t).length;
  await page.click('#load');
  t = await loaded();
  check('ticked programs are added: chapter 7\'s programs, the app and the student\'s own all stay; nothing was replaced, so no backup was made',
        JSON.stringify(onCalc(t)) === JSON.stringify(['ChiTable.hpprgm', 'GaltonBoard.hpprgm', 'Norm3.hpprgm', 'OldHomework.hpprgm', 'SampDist.hpprgm', 'TestChooser.hpprgm']) &&
        same(t[C + 'Norm3.hpprgm'], packFile('Norm3.hpprgm')) && APP.every(n => same(t[C + n], packFile(n))) && folders(t).length === nb && /Nothing needed moving/.test(await page.textContent('#report')), onCalc(t));

  // ---- 6. a data file on its own: it is added, with DataLoad ----
  await page.reload();
  await page.locator('#more > summary').click();
  await page.check('#w_pick');
  const own3 = hpmat(4, 2, 7);
  await page.setInputFiles('#ownfile', { name: 'M3 (2).hpmat', mimeType: 'application/octet-stream', buffer: own3 });
  await page.waitForFunction(() => /M3\.hpmat/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('"M3 (2).hpmat", a browser\'s name for a second download, is taken as M3', /Your data: M3\.hpmat\./.test(await page.textContent('#ownlist')));
  check('a data file alone: DataLoad is ticked and held for it, Load is on, and the summary says why', await page.isChecked('#p_DataLoad') && await page.isDisabled('#p_DataLoad') && !(await page.isDisabled('#load')) &&
        (await page.textContent('#summary')) === 'No program chosen, and the data M3. DataLoad is added because the data need it.', await page.textContent('#summary'));
  await page.click('#load');
  t = await loaded();
  check('own data written as M3, with DataLoad, byte for byte; every program that was there stays', same(t[C + 'M3.hpmat'], own3) && same(t[C + 'DataLoad.hpprgm'], packFile('DataLoad.hpprgm')) &&
        JSON.stringify(onCalc(t)) === JSON.stringify(['ChiTable.hpprgm', 'DataLoad.hpprgm', 'GaltonBoard.hpprgm', 'Norm3.hpprgm', 'OldHomework.hpprgm', 'SampDist.hpprgm', 'TestChooser.hpprgm']), onCalc(t));

  // ---- 6b. "One chapter" with no chapter chosen moves nothing ----
  await page.reload();
  await page.check('#w_chapter');
  check('"One chapter" and no chapter: the page asks for the chapter, and Load is off', (await page.textContent('#summary')) === 'Choose your chapter in the list above.' && await page.isDisabled('#load') && (await page.textContent('#effect')) === '');
  await page.locator('#more > summary').click();
  await page.check('#rossi');
  check('... with the sample data added: Load is on, and the page says the programs there stay', !(await page.isDisabled('#load')) && (await page.textContent('#effect')) === 'They are added: programs already on the calculator stay.' &&
        /^No program chosen, and the data M1\. DataLoad is added/.test(await page.textContent('#summary')), await page.textContent('#summary'));
  await page.click('#load');
  t = await loaded();
  check('... and no book program was moved off: all seven are still there', JSON.stringify(onCalc(t)) === JSON.stringify(['ChiTable.hpprgm', 'DataLoad.hpprgm', 'GaltonBoard.hpprgm', 'Norm3.hpprgm', 'OldHomework.hpprgm', 'SampDist.hpprgm', 'TestChooser.hpprgm']) &&
        same(t[C + 'M1.hpmat'], sample), onCalc(t));

  // ---- 7. a data file is opened before it is taken ----
  await page.reload();
  await page.locator('#more > summary').click();
  await page.check('#w_pick');
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
  check('... and after three refusals nothing is chosen and Load is off', /Nothing ticked yet/.test(await page.textContent('#summary')) && await page.isDisabled('#load'));
  await page.check('#rossi');
  const own1 = hpmat(3, 1, 5);
  await page.setInputFiles('#ownfile', { name: 'M1.hpmat', mimeType: 'application/octet-stream', buffer: own1 });
  await page.waitForFunction(() => /Your data: M1\.hpmat/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('own M1 beside the sample data: the page says which one is used', /Your own M1\.hpmat is used; the sample data set would go into the same matrix, so it is left out/.test(await page.textContent('#summary')), await page.textContent('#summary'));
  await page.click('#load');
  t = await loaded();
  check('... and M1 on the calculator is the student\'s own file, not the sample', same(t[C + 'M1.hpmat'], own1));

  // ---- 8. the wrong folder, and a cancelled picker ----
  await page.reload();
  await page.selectOption('#chapter', '14');
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
  t = await loaded();
  check('picking Documents finds HP Prime inside it: chapter 14 is loaded', same(t[C + 'AnovaLab.hpprgm'], packFile('AnovaLab.hpprgm')) &&
        JSON.stringify(onCalc(t)) === JSON.stringify(['AnovaLab.hpprgm', 'DataLoad.hpprgm', 'OldHomework.hpprgm', 'TestChooser.hpprgm']), onCalc(t));
  await page.evaluate(() => { window.showDirectoryPicker = async () => { throw new DOMException('cancelled', 'AbortError'); }; });
  await page.click('#repick');
  await page.waitForFunction(() => /No folder was chosen/.test(document.getElementById('status').textContent));
  check('cancelling the picker says nothing was loaded', true);

  // ---- 9. a real HP Prime: the same choice, as a zip for the Connectivity Kit ----
  await page.reload();
  await page.check('#t_real');
  check('a real HP Prime: step 3 is the Connectivity Kit\'s steps, and there is no Load button to click',
        JSON.stringify(await steps(page)) === JSON.stringify(['1Which calculator?', '2Which programs?', '3Put them on your HP Prime with HP\'s Connectivity Kit', 'Something not working?']) &&
        !(await page.isVisible('#load')) && await page.isVisible('#download3') && await page.locator('#step3real ol.steps > li').count() === 6, JSON.stringify(await steps(page)));
  check('... it says programs on the calculator stay, and that a real calculator has less room', (await page.textContent('#effect')) ===
        'Programs already on your calculator stay there. A real calculator has much less room than a computer; if yours runs short, load one chapter at a time.', await page.textContent('#effect'));
  check('... the steps: download, unpack, start the Kit and plug in, drag onto the calculator\'s name, close the Kit, run', /Extract All/.test(await page.textContent('#step3real')) &&
        /drop it on the calculator's name/.test(await page.textContent('#step3real')) && /not into the Content box/.test(await page.textContent('#step3real')) && /Close the Connectivity Kit/.test(await page.textContent('#step3real')));
  check('... the app\'s note shows for all the programs, and says it has not been tried on a real calculator; the last step says how to start an app', await page.isVisible('#realapp') && /has not been tried on a real calculator yet/.test(await page.textContent('#realapp')) && !(await page.isVisible('#realdata')) &&
        await page.isVisible('#realapp2') && /press Apps/.test(await page.textContent('#realapp2')));
  check('... Bonjour is one click away, folded', !(await page.isVisible('#step3real .panel.warn')) && /The Kit does not show my calculator/.test(await page.textContent('#step3real details > summary')));
  await page.locator('#step3real details > summary').click();
  check('... and opens to how to check it', await page.isVisible('#step3real details .panel.warn') && /Bonjour Service/.test(await page.textContent('#step3real details')) && /Running/.test(await page.textContent('#step3real details')));
  check('the USB route does not show for a real HP Prime either, without the test address', !(await page.isVisible('#usbpanel')));
  let [dl] = await Promise.all([page.waitForEvent('download'), page.click('#download3')]);
  check('all the programs download as HP_Prime_all_programs.zip, the name the step shows', dl.suggestedFilename() === 'HP_Prime_all_programs.zip' && (await page.textContent('#zipname3')) === 'HP_Prime_all_programs.zip', dl.suggestedFilename());
  const zp = path.join(tmp, 'dl.zip'); await dl.saveAs(zp);
  const out = path.join(tmp, 'dl'); execFileSync('unzip', ['-q', zp, '-d', out]);
  let allSame = true;
  for (const n of packed) {
    if (n.endsWith('.hpappdir')) { for (const f of fs.readdirSync(path.join(tmp, 'Copy these into Prime', n))) allSame = allSame && fs.readFileSync(path.join(out, n, f)).equals(packFile(n + '/' + f)); }
    else allSame = allSame && fs.readFileSync(path.join(out, n)).equals(packFile(n));
  }
  check('zip of everything: all 30 programs and the app, byte for byte', allSame && fs.readdirSync(out).length === packed.length, fs.readdirSync(out).length);
  check('the status says what to do next', /Downloaded HP_Prime_all_programs\.zip \(33 files\)\. Now go on to the next step/.test(await page.textContent('#dlstatus3')), await page.textContent('#dlstatus3'));
  await page.selectOption('#chapter', '12');
  check('a real HP Prime, one chapter: the page says the programs there stay (nothing is moved off a real calculator)', (await page.textContent('#effect')) === 'Programs already on your calculator stay there.' &&
        (await page.textContent('#realprogs')) === 'ChiTable, FitCheck, TestChooser' && !(await page.isVisible('#realapp')) && !(await page.isVisible('#realapp2')));
  [dl] = await Promise.all([page.waitForEvent('download'), page.click('#download3')]);
  const zc = path.join(tmp, 'c12.zip'); await dl.saveAs(zc);
  const oc = path.join(tmp, 'c12'); execFileSync('unzip', ['-q', zc, '-d', oc]);
  check('chapter 12 downloads as HP_Prime_Chapter_12.zip, holding its two programs and TestChooser byte for byte', dl.suggestedFilename() === 'HP_Prime_Chapter_12.zip' &&
        JSON.stringify(fs.readdirSync(oc).sort()) === JSON.stringify(['ChiTable.hpprgm', 'FitCheck.hpprgm', 'TestChooser.hpprgm']) &&
        ['ChiTable.hpprgm', 'FitCheck.hpprgm', 'TestChooser.hpprgm'].every(n => fs.readFileSync(path.join(oc, n)).equals(packFile(n))), fs.readdirSync(oc));
  await page.locator('#more > summary').click();
  await page.check('#rossi');
  check('... with data: the data note shows, names the file, and says it has not been tried on a real calculator', await page.isVisible('#realdata') && (await page.textContent('#realdatanames')) === 'M1.hpmat' && /not yet tried on a real calculator/.test(await page.textContent('#realdata')) &&
        /DataLoad/.test(await page.textContent('#realprogs')));
  await page.check('#t_vc');
  check('back to the Virtual Calculator: Load returns, the Kit steps go, and the chapter is still chosen', await page.isVisible('#load') && !(await page.isVisible('#step3real')) && await page.isChecked('#w_chapter') &&
        /The book's other programs are moved off/.test(await page.textContent('#effect')));
  check('the help has the Kit for the Virtual Calculator too, pointing at step 1', /Choose A real HP Prime in step 1/.test(await page.textContent('.help details:last-of-type')));

  // ---- 9b. from the Data Loader (?data=1): the page opens ready for a data file ----
  const dpg = await ctx.newPage();
  await dpg.goto('http://localhost:8766/?data=1');
  check('from the Data Loader: a notice says what to click, no program is chosen, the data button is in sight, the list of 31 is not, and Load is off',
        await dpg.isVisible('#fromdl') && /Add a data file you were given/.test(await dpg.textContent('#fromdl')) && await dpg.isChecked('#w_pick') && await dpg.isVisible('label[for="ownfile"]') &&
        !(await dpg.isVisible('#proglist')) && (await dpg.textContent('#summary')) === 'No data file added yet.' && await dpg.isDisabled('#load'), await dpg.textContent('#summary'));
  const own2 = hpmat(2, 2, 3);
  await dpg.setInputFiles('#ownfile', { name: 'M2.hpmat', mimeType: 'application/octet-stream', buffer: own2 });
  await dpg.waitForFunction(() => /Your data: M2\.hpmat/.test(document.querySelector('#ownlist').textContent), null, { timeout: 5000 }).catch(() => {});
  check('... a file added: Load comes on, and the page says the data and DataLoad are all that go', !(await dpg.isDisabled('#load')) &&
        (await dpg.textContent('#summary')) === 'No program chosen, and the data M2. DataLoad is added because the data need it.' && (await dpg.textContent('#effect')) === 'They are added: programs already on the calculator stay.', await dpg.textContent('#summary'));
  const tb = await readTree();
  await dpg.click('#load');
  await dpg.waitForSelector('#done:not([hidden])');
  t = await readTree();
  check('... loaded: M2 and DataLoad byte for byte, and every program that was there is still there', same(t[C + 'M2.hpmat'], own2) && same(t[C + 'DataLoad.hpprgm'], packFile('DataLoad.hpprgm')) &&
        JSON.stringify(onCalc(t)) === JSON.stringify(onCalc(tb)), onCalc(t));
  await dpg.click('#w_pick');
  check('... and a click on "Only the programs I tick" brings out the list', await dpg.isVisible('#proglist'));
  check('without ?data=1 the notice is not shown', !(await page.isVisible('#fromdl')));
  const ipg = await ctx.newPage();
  await ipg.goto('file://' + path.join(path.dirname(PAGE), 'index.html') + '?data=1');
  await ipg.waitForFunction(() => !!document.getElementById('fromdl'), null, { timeout: 15000 }).catch(() => {});
  check('index.html carries ?data=1 on to the page, so the Data Loader\'s link to the folder\'s address opens it ready for the file',
        /PrimeLoader_v2a\.html\?data=1$/.test(ipg.url()) && await ipg.isVisible('#fromdl'), ipg.url());
  check('... and a browser with scripts off is still sent on, by the line in noscript', /<noscript><meta http-equiv="refresh" content="0; url=PrimeLoader_v2a\.html"><\/noscript>/.test(idx));

  // ---- 10. Firefox: no folder API, Firefox's user-agent ----
  const fctx = await browser.newContext({ acceptDownloads: true,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0' });
  const p2 = await fctx.newPage();
  const errs2 = []; p2.on('pageerror', e => errs2.push(String(e)));
  await p2.addInitScript(() => { delete window.showDirectoryPicker; });
  await p2.goto('http://localhost:8766/');
  check('Firefox: its own route shows, the Edge route is hidden',
        await p2.isVisible('#mode-manual') && await p2.isVisible('#step3manual') && !(await p2.isVisible('#step3auto')));
  check('Firefox: named, with the reason in plain words', (await p2.textContent('#brname')) === 'Firefox' &&
        /never lets a web page put files into a folder/.test(await p2.textContent('#mode-manual')));
  check('Firefox: three numbered steps, and the third begins with closing the calculator', JSON.stringify(await p2.$$eval('.step:not([hidden]) .stepnum', e => e.map(x => x.textContent))) === '["1","2","3"]' &&
        /Close the Virtual Calculator/.test(await p2.textContent('#step3manual ol.steps > li:first-child')));
  check('Firefox: all the programs are ready to download, and the page says what is on the calculator stays', !(await p2.isDisabled('#download2')) && (await p2.textContent('#zipname')) === 'HP_Prime_all_programs.zip' &&
        (await p2.textContent('#effect')) === 'Programs already on your calculator stay there.');
  await p2.selectOption('#chapter', '12');
  check('Firefox: one chapter names the zip and the programs, and does not promise to move anything off', (await p2.textContent('#zipname')) === 'HP_Prime_Chapter_12.zip' &&
        (await p2.textContent('#manualprogs')) === 'ChiTable, FitCheck, TestChooser' && (await p2.textContent('#effect')) === 'Programs already on your calculator stay there.');
  const [fdl] = await Promise.all([p2.waitForEvent('download'), p2.click('#download2')]);
  check('Firefox: the download is HP_Prime_Chapter_12.zip', fdl.suggestedFilename() === 'HP_Prime_Chapter_12.zip', fdl.suggestedFilename());
  const fz = path.join(tmp, 'ff.zip'); await fdl.saveAs(fz);
  const fo = path.join(tmp, 'ff'); execFileSync('unzip', ['-q', fz, '-d', fo]);
  const fl = fs.readdirSync(fo).sort();
  check('Firefox: the zip holds the chapter\'s programs at its top level, byte for byte',
        JSON.stringify(fl) === JSON.stringify(['ChiTable.hpprgm', 'FitCheck.hpprgm', 'TestChooser.hpprgm']) &&
        fl.every(n => fs.readFileSync(path.join(fo, n)).equals(packFile(n))), fl);
  check('Firefox: the status says what to do next', /Now go on to the next step/.test(await p2.textContent('#dlstatus2')));
  await p2.selectOption('#chapter', '7');
  check('Firefox: the app note shows for chapter 7', await p2.isVisible('#manualapp'));
  await p2.locator('#more > summary').click();
  await p2.check('#rossi');
  check('Firefox: the data note shows when data is picked, and DataLoad joins the list', await p2.isVisible('#manualdata') && /DataLoad/.test(await p2.textContent('#manualprogs')), await p2.textContent('#manualprogs'));
  await p2.check('#w_pick');
  check('Firefox: with nothing but data chosen the zip is HP_Prime_data.zip', (await p2.textContent('#zipname')) === 'HP_Prime_data.zip');
  await p2.check('#t_real');
  check('Firefox, a real HP Prime: the Kit\'s steps show, and the note about Firefox and folders goes', await p2.isVisible('#step3real') && !(await p2.isVisible('#mode-manual')) && !(await p2.isVisible('#step3manual')));
  check('Firefox on Windows: no notice at the top', !(await p2.isVisible('#platform')));
  check('Firefox: no errors in the page', errs2.length === 0, errs2);

  // ---- 11. a phone, a Mac, an old browser ----
  const phone = await (await browser.newContext({ userAgent: 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Mobile Safari/537.36' })).newPage();
  await phone.addInitScript(() => { delete window.showDirectoryPicker; });
  await phone.goto('http://localhost:8766/');
  check('a phone: the notice says the page needs the computer, and gives the address', await phone.isVisible('#platform') &&
        /needs your computer/.test(await phone.textContent('#platformh')) && /phone or a tablet/.test(await phone.textContent('#platformp')) &&
        /http:\/\/localhost:8766\//.test(await phone.textContent('#platformp')), await phone.textContent('#platformp'));
  check('a phone: "that\'s fine, a few more clicks" is not shown', !(await phone.isVisible('#mode-manual')));
  const mac = await (await browser.newContext({ userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15' })).newPage();
  await mac.addInitScript(() => { delete window.showDirectoryPicker; });
  await mac.goto('http://localhost:8766/');
  check('a Mac: the notice says the steps were written for Windows, and points at "A real HP Prime" for the Kit', await mac.isVisible('#platform') && /written for Windows/.test(await mac.textContent('#platformh')) &&
        /Connectivity Kit/.test(await mac.textContent('#platformp')) && /A real HP Prime/.test(await mac.textContent('#platformp')), await mac.textContent('#platformp'));
  const old = await (await browser.newContext({ userAgent: WIN })).newPage();
  await old.addInitScript(() => { delete window.DecompressionStream; });
  await old.goto('http://localhost:8766/');
  await old.check('#t_real');
  check('a browser that cannot unpack: the notice says so, and Load and Download stay off', await old.isVisible('#platform') && /too old for this page/.test(await old.textContent('#platformh')) &&
        await old.isDisabled('#download3') && await old.evaluate(() => document.getElementById('load').disabled));

  // ---- 12. a narrow window, and the page as a file ----
  await page.setViewportSize({ width: 380, height: 800 });
  check('at a phone\'s width nothing runs off the side', await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  await page.setViewportSize({ width: 1280, height: 720 });
  const p3 = await ctx.newPage();
  const errs3 = []; p3.on('pageerror', e => errs3.push(String(e)));
  await p3.goto('file://' + PAGE);
  check('opens as a local file without errors', errs3.length === 0 && (await p3.textContent('#summary')) === 'All 31 programs.', errs3);

  // ---- 13. the USB route, at the page's test address, against a pretend calculator ----
  // (tests/../usb/tests/mock_prime_v1.js: it answers as three public descriptions say a G2 does.  Not a calculator.)
  const MOCK = fs.readFileSync(path.join(__dirname, '..', 'usb', 'tests', 'mock_prime_v1.js'), 'utf8');
  const PROGRAMS = path.join(__dirname, '..', '..', 'programs');
  const repoSource = n => { const f = fs.readdirSync(PROGRAMS).find(x => x.startsWith(n + '_')); return fs.readFileSync(path.join(PROGRAMS, f), 'utf8').replace(/\r\n?/g, '\n').replace(/\s+$/, ''); };
  const usbPage = async (mopts, query) => {
    const c = await browser.newContext({ userAgent: WIN });
    const p = await c.newPage(), errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.addInitScript({ content: MOCK + '\n;MockPrime.install(' + JSON.stringify(mopts || {}) + ');\n' +
      'window.addEventListener("DOMContentLoaded", () => { const s = PrimeUSB.sleep; PrimeUSB.sleep = ms => s(Math.min(ms, 20)); });' });
    await p.goto('http://localhost:8766/' + (query === undefined ? '?usb=1' : query));
    return { p, errs };
  };
  const usbEnd = p => p.waitForFunction(() => /found the same|Stopped|broke off|No calculator|could not open|did not answer|no program/.test(document.getElementById('usbstatus').textContent), null, { timeout: 120000 });
  let u = await usbPage({});
  check('USB: at the test address the panel still does not show for the Virtual Calculator', !(await u.p.isVisible('#usbpanel')));
  await u.p.check('#t_real');
  check('USB: for a real HP Prime it shows, under the Kit\'s steps, and says it has not been proved on a real calculator', await u.p.isVisible('#usbpanel') &&
        /has not been proved on a real calculator yet/.test(await u.p.textContent('#usbpanel')) && /Close the Connectivity Kit first/.test(await u.p.textContent('#usbpanel')) && await u.p.isVisible('#download3'));
  await u.p.selectOption('#chapter', '7');
  await u.p.click('#usbsend');
  await usbEnd(u.p);
  let us = await u.p.textContent('#usbstatus'), ul = await u.p.$$eval('#usblist li', e => e.map(x => x.textContent));
  let got = await u.p.evaluate(() => ({ programs: window.__prime.programs, arrived: window.__prime.arrived.map(a => a.name + ':' + a.layout), last: window.__prime.lastLength, releases: window.__prime.releases }));
  check('USB, chapter 7: its three programs arrive, each read back the same; the app is named as not sent this way',
        /^3 programs on the calculator, each read back and found the same\. Not sent this way: CentralLimit \(an app or a data file; use the Connectivity Kit steps above for those\)\./.test(us) &&
        JSON.stringify(got.arrived) === JSON.stringify(['GaltonBoard:v3', 'SampDist:v3', 'TestChooser:v3']) && got.releases === 3 && got.last === 1024, us + ' ' + JSON.stringify(got.arrived));
  check('USB: what the calculator holds is each program\'s source in programs/, character for character', ['GaltonBoard', 'SampDist', 'TestChooser'].every(n => got.programs[n] === repoSource(n)));
  check('USB: the list says so program by program, and gives the firmware build', /^Connected: HP Prime G2, firmware build 15515\.$/.test(ul[0]) && ul.slice(1).every(l => /: arrived whole \(\d+ reports?, read back the same\)\.$/.test(l)) && ul.length === 4, JSON.stringify(ul));
  check('USB: no errors in the page', u.errs.length === 0, u.errs);
  u = await usbPage({ silentF8: true });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  us = await u.p.textContent('#usbstatus');
  check('USB, a calculator that gives nothing back: the run stops at the first program and sends no more, and the page does not say it arrived',
        /^Stopped at ChiTable\. The page could not read it back, so it will not send the rest\./.test(us) && /Connectivity Kit steps above/.test(us) && (await u.p.evaluate(() => window.__prime.arrived.length)) === 1 &&
        /cannot tell whether it arrived/.test(await u.p.textContent('#usblist')), us);
  u = await usbPage({ maxMessage: 16000 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  us = await u.p.textContent('#usbstatus');
  check('USB, a calculator that drops long messages without a word: stopped at the first program, nothing claimed', /^Stopped at ChiTable\./.test(us) && (await u.p.evaluate(() => Object.keys(window.__prime.programs).length)) === 0, us);
  u = await usbPage({ cutAt: 5000 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  us = await u.p.textContent('#usbstatus');
  check('USB, a program damaged on the way: "it did not arrive whole", with what to do', /^Stopped at ChiTable: it did not arrive whole\. Delete ChiTable on the calculator/.test(us) &&
        /what came back is not what was sent \(5000 characters against \d+\)/.test(await u.p.textContent('#usblist')), us);
  u = await usbPage({});
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.evaluate(() => { const m = window.__prime, r0 = m.receive.bind(m); m.receive = function (r) { if (m.reportsIn > 40 && !m.unplugged) m.unplug(); return r0(r); }; });
  await u.p.click('#usbsend'); await usbEnd(u.p);
  us = await u.p.textContent('#usbstatus');
  check('USB, the cable pulled out half way: "the sending broke off", and which programs are on the calculator is not overstated', /^The sending broke off: /.test(us) && /The programs marked "arrived whole" are on the calculator; the rest are not/.test(us) &&
        !(await u.p.isDisabled('#usbsend')) && u.errs.length === 0, us + u.errs);
  u = await usbPage({ busy: true });
  await u.p.check('#t_real');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  check('USB, the Connectivity Kit still open: the page says to close it', /close the Kit, then click Send again/.test(await u.p.textContent('#usbstatus')) && !(await u.p.isDisabled('#usbsend')));
  u = await usbPage({ none: true });
  await u.p.check('#t_real');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  check('USB, nothing on the cable: the page says what to check', /No calculator was chosen/.test(await u.p.textContent('#usbstatus')) && /cable pushed in at both ends/.test(await u.p.textContent('#usbstatus')));
  u = await usbPage({}, '');
  await u.p.check('#t_real');
  check('USB: without the test address the panel is hidden, whatever the browser can do', !(await u.p.isVisible('#usbpanel')) && await u.p.evaluate(() => PrimeUSB.supported()));

  check('no errors in the page', errors.length === 0, errors);
  console.log(`\n${pass} PASS, ${fail} FAIL`);
  await browser.close(); srv.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
