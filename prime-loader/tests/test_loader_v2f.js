// test_loader_v2f.js -- drives PrimeLoader_v2f.html in Chromium against a mock Virtual Calculator folder, and its
// cable route (shown only at ?usb=1) against a pretend calculator that does what two real ones did on 17 Nov 2026.
// Roger Metcalf & Claude, 18 Nov 2026.   node tests/test_loader_v2f.js PrimeLoader_v2f.html PACK.zip
//
// v2f shows the cable to every student (after the G2 and G1 logs of 18 Nov): without ?usb=1, in Chrome or Edge, a
// real HP Prime gets the two ways; in a browser without WebHID, the Kit and the sentence naming Chrome and Edge.
// Part 9 (the Kit's way) therefore runs in a page without WebHID, as Firefox and Safari show it; part 13 has the
// cable.  The sentence under the title is Roger's book wording, "and we have tested it" included.
//
// v2e is v2d with one sentence more, for a student's slip: a real HP Prime in a browser that cannot reach it on its
// cable (Firefox, Safari) is told that Chrome or Edge can send the programs down the cable.  Five checks for it,
// at the end: shown there, by the browser's own name; not shown where the cable works, nor where the cable is not
// offered, nor for the Virtual Calculator.
//
// v2d is v2c with the two ways named as Roger named them next, "1) The Statisticles way" and "2) The official HP
// way: the Connectivity Kit", and his sentence under the step's title ("We believe our method should work. ... But just
// in case ..."), WITHOUT its "and we have tested it", which he took back ten minutes later ("the testing claim is not
// valid yet"): the same checks with those words, and one more, that nothing the page shows says "we have tested it"
// while its own note says that this way is still being tested.
// v2c is v2b with the step that offers both ways named as Roger named it, "Two ways to load Statisticles onto a
// physical Prime G1 or G2 calculator" (Statisticles, in italics, being the book's name for its programs), and the
// two called the first way and the second way: the same checks, with those words, and three more for the title, the
// sentence under it and the two names.
// v2b is v2a with the cable route written again (usb/prime_usb_v3a.js, usb/tests/mock_prime_v3a.js): parts 1 to 12
// are v2a's test, with the page's new names; part 13 is new.  NOTHING HERE TOUCHES A CALCULATOR.
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
//   - the cable does not show without ?usb=1, nor in a browser that cannot reach a USB device; with it, it is way
//     1) for a real HP Prime and the Connectivity Kit's steps, whole, are way 2); each program is sent,
//     read back and compared with the pack's own source, character for character; the first one that does not come
//     back the same stops the load; and each slip a student can make (no calculator picked, the Kit left open, the
//     cable pulled out, Stop, a second click) gets its sentence and leaves the page ready to try again.
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
  check('the cable route is in the page, on in a browser with WebHID (Chromium here), and not shown while the Virtual Calculator is chosen', await page.evaluate(() => typeof PrimeUSB === 'object' && typeof PrimeUSB.load === 'function' && usbOn) && !(await page.isVisible('#cable')));
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
  // From here this page is a browser without WebHID (Firefox, Safari), where the Kit's way is the main line; Chrome and
  // Edge get the cable (part 13).
  await page.addInitScript(() => { Object.defineProperty(navigator, 'hid', { value: undefined, configurable: true }); });
  await page.reload();
  await page.check('#t_real');
  check('a real HP Prime: step 3 is the Connectivity Kit\'s steps, and there is no Load button to click',
        JSON.stringify(await steps(page)) === JSON.stringify(['1Which calculator?', '2Which programs?', '3Put them on your HP Prime with HP\'s Connectivity Kit', 'Something not working?']) &&
        !(await page.isVisible('#load')) && await page.isVisible('#download3') && await page.locator('#kitroute ol.steps > li').count() === 6, JSON.stringify(await steps(page)));
  check('... it says programs on the calculator stay, and that a real calculator has less room', (await page.textContent('#effect')) ===
        'Programs already on your calculator stay there. A real calculator has much less room than a computer; if yours runs short, load one chapter at a time.', await page.textContent('#effect'));
  check('... the steps: download, unpack, start the Kit and plug in, drag onto the calculator\'s name, close the Kit, run', /Extract All/.test(await page.textContent('#step3real')) &&
        /drop it on the calculator's name/.test(await page.textContent('#step3real')) && /not into the Content box/.test(await page.textContent('#step3real')) && /Close the Connectivity Kit/.test(await page.textContent('#step3real')));
  check('... the app\'s note shows for all the programs, and says it has not been tried on a real calculator; the last step says how to start an app', await page.isVisible('#realapp') && /has not been tried on a real calculator yet/.test(await page.textContent('#realapp')) && !(await page.isVisible('#realdata')) &&
        await page.isVisible('#realapp2') && /press Apps/.test(await page.textContent('#realapp2')));
  check('... Bonjour is one click away, folded', !(await page.isVisible('#kitroute .panel.warn')) && /The Kit does not show my calculator/.test(await page.textContent('#kitroute details > summary')));
  await page.locator('#kitroute details > summary').click();
  check('... and opens to how to check it', await page.isVisible('#kitroute details .panel.warn') && /Bonjour Service/.test(await page.textContent('#kitroute details')) && /Running/.test(await page.textContent('#kitroute details')));
  check('in a browser without WebHID the cable does not show for a real HP Prime: the Kit\'s steps are the page\'s main line, open, with no fold to click, under the Kit\'s own title',
        !(await page.isVisible('#cable')) && !(await page.isVisible('#kitsum')) && await page.evaluate(() => document.getElementById('kitfold').open) && (await page.textContent('#s3rtitle')) === 'Put them on your HP Prime with HP\'s Connectivity Kit');
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
        /PrimeLoader_v2f\.html\?data=1$/.test(ipg.url()) && await ipg.isVisible('#fromdl'), ipg.url());
  check('... and a browser with scripts off is still sent on, by the line in noscript', /<noscript><meta http-equiv="refresh" content="0; url=PrimeLoader_v2f\.html"><\/noscript>/.test(idx));

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

  // ---- 13. the cable, at the page's test address, against a pretend calculator ----
  // (usb/tests/mock_prime_v3a.js: by default it does what the author's G2 and G1 did on 17 Nov 2026.  Not a calculator.)
  const MOCK = fs.readFileSync(path.join(__dirname, '..', 'usb', 'tests', 'mock_prime_v3a.js'), 'utf8');
  const PROGRAMS = path.join(__dirname, '..', '..', 'programs');
  const canon = s => s.replace(/\r\n?/g, '\n').replace(/\s+$/, '');
  const repoSource = n => { const f = fs.readdirSync(PROGRAMS).find(x => x.startsWith(n + '_')); return canon(fs.readFileSync(path.join(PROGRAMS, f), 'utf8')); };
  const CATALOG = await page.evaluate(() => CAT);
  // a program's source exactly as its file in the pack holds it
  const packSource = n => { const p = CATALOG.programs[n], f = packFile(p.files[0]); return f.subarray(p.src[0], p.src[1]).toString('utf16le').replace(/\0+$/, ''); };
  const usbPage = async (mopts, query, hid) => {
    const c = await browser.newContext({ userAgent: WIN, acceptDownloads: true });
    const p = await c.newPage(), errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    if (hid !== false) await p.addInitScript({ content: MOCK + '\n;MockPrime.install(' + JSON.stringify(mopts || {}) + ');\n' });
    else await p.addInitScript(() => { Object.defineProperty(navigator, 'hid', { value: undefined, configurable: true }); });
    await p.goto('http://localhost:8766/' + (query === undefined ? '?usb=1' : query));
    return { p, errs };
  };
  // the load is over when Send can be clicked again and one of the two panels shows, or the status is a final word
  const usbEnd = (p, ms) => p.waitForFunction(() => !usbBusy && (!document.getElementById('usbdone').hidden || !document.getElementById('usbfail').hidden), null, { timeout: ms || 120000 });
  const state = p => p.evaluate(() => ({ status: document.getElementById('usbstatus').textContent, cls: document.getElementById('usbstatus').className,
    list: [...document.querySelectorAll('#usblist li')].map(x => x.className + ':' + x.children[1].textContent), done: !document.getElementById('usbdone').hidden, fail: !document.getElementById('usbfail').hidden,
    failh: document.getElementById('usbfailh').textContent, failp: document.getElementById('usbfailp').textContent, todo: [...document.querySelectorAll('#usbfaildo li')].map(x => x.textContent),
    report: [...document.querySelectorAll('#usbreport li')].map(x => x.textContent), next: [...document.querySelectorAll('#usbnext li')].map(x => x.textContent),
    bar: document.getElementById('usbbar').getAttribute('aria-valuenow'), barHidden: document.getElementById('usbbar').hidden, log: document.getElementById('usblog').textContent,
    sendOff: document.getElementById('usbsend').disabled, stopHidden: document.getElementById('usbstop').hidden, kitOpen: document.getElementById('kitfold').open, unload: window.onbeforeunload === null }));
  const prime = p => p.evaluate(() => { const m = window.__prime; return { programs: m.programs, arrived: m.arrived.map(a => ({ name: a.name, layout: a.layout, framing: a.framing, reports: a.reports, kept: a.kept })),
    fds: m.fds, outOfTurn: m.outOfTurn, nacks: m.nacks, statuses: m.statuses, asked: m.asked || 0, opens: m.opens || 0, closes: m.closes || 0, reportsIn: m.reportsIn, waits: m.waits.map(w => w.ms), last: m.lastLength, err: m.error || null, standing: !!m.standing, v2open: m.v2open }; });

  let u = await usbPage({});
  check('cable: the test address opens on "A real HP Prime", since that is what it is for', await u.p.isChecked('#t_real') && await u.p.isVisible('#cable'));
  await u.p.check('#t_vc');
  check('cable: nothing of it shows while the Virtual Calculator is chosen', !(await u.p.isVisible('#cable')) && !(await u.p.isVisible('#step3real')) && await u.p.isVisible('#load'));
  await u.p.check('#t_real');
  check('two ways: where both show, step 3 is called what Roger called it, "Two ways to load Statisticles onto a physical Prime G1 or G2 calculator", with Statisticles in italics as the book writes it',
        (await u.p.textContent('#s3rtitle')) === 'Two ways to load Statisticles onto a physical Prime G1 or G2 calculator' && await u.p.isVisible('#s3rtitle') &&
        (await u.p.textContent('#s3rtitle i')) === 'Statisticles' && await u.p.evaluate(() => getComputedStyle(document.querySelector('#s3rtitle i')).fontStyle === 'italic'));
  check('two ways: under the title, Roger\'s sentence as the book has it: we believe our method should work, and we have tested it, and are continually testing it; easier than the Kit, no mDNS (Bonjour) issue; 2) just in case; tell us on GitHub, with the Issues address as a link',
        await u.p.isVisible('#twoways') && (await u.p.textContent('#twoways')) === 'We believe our method should work, and we have tested it, and are continually testing it. It is easier to use than the Connectivity Kit, and it avoids the Kit\'s mDNS (Bonjour) issue. ' +
        'But just in case you have trouble with the Statisticles way, we also present 2), the official HP way. (And if something does go wrong, please be sure to let us know on our GitHub page, github.com/metcalfdds/hp-prime-statistics/issues.) CentralLimit and data files go only by 2).' &&
        (await u.p.textContent('#twoways i')) === 'Statisticles' && (await u.p.getAttribute('#twoways a', 'href')) === 'https://github.com/metcalfdds/hp-prime-statistics/issues');
  check('two ways: each has the name he gave it, "1) The Statisticles way: straight down the USB cable" and "2) The official HP way: the Connectivity Kit", in that order down the page under the sentence',
        await u.p.isVisible('#way1') && (await u.p.textContent('#way1')) === '1) The Statisticles way: straight down the USB cable' && (await u.p.textContent('#way1 i')) === 'Statisticles' &&
        (await u.p.textContent('#kitsum')) === '2) The official HP way: the Connectivity Kit' &&
        await u.p.evaluate(() => { const a = document.getElementById('twoways'), b = document.getElementById('way1'), c = document.getElementById('kitsum'); return a.getBoundingClientRect().top < b.getBoundingClientRect().top && b.getBoundingClientRect().top < c.getBoundingClientRect().top; }));
  check('two ways: right under 1) a line says what was tried (a G2 in Chrome, a G1 in Edge, 18 November 2026; Chapter 12 read back the same; ChiTable ran with no Check), and nothing the page shows still says it is being tested',
        await u.p.isVisible('#cabletested') && (await u.p.textContent('#cabletested')) === 'Tried on the author\'s HP Prime G2 (in Chrome) and G1 (in Edge) on 18 November 2026: each program of Chapter 12 came back from the calculator the same, and ChiTable ran at once, with no Check.' &&
        !/being tested|this is that test|test address/i.test(await u.p.evaluate(() => document.documentElement.outerHTML.replace(/<(script|style)[^>]*>[^]*?<\/\1>/g, m => m.replace(/\/\*[^]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '')))));
  check('two ways: nowhere in what the page shows or can come to show (its comments aside, which keep the history) is either still called "the other way", "the first way" or "the second way"', !/other way|first way|second way/i.test(await u.p.evaluate(() => document.documentElement.outerHTML.replace(/<(script|style)[^>]*>[^]*?<\/\1>/g, m => m.replace(/\/\*[^]*?\*\//g, '').replace(/^\s*\/\/.*$/gm, '')))) &&
        /The first way: straight down the USB cable/.test(await u.p.evaluate(() => document.documentElement.outerHTML)));   // the second half shows the first is not empty: the words are still in the page's history comment, and only there
  check('cable: for a real HP Prime it is way 1): three steps and one button',
        await u.p.isVisible('#cable') && await u.p.locator('#cable ol.steps > li').count() === 3 &&
        await u.p.isVisible('#usbsend') && !(await u.p.isDisabled('#usbsend')) && !(await u.p.isVisible('#usbstop')) && !(await u.p.isVisible('#load')));
  check('cable: its steps say to plug in and switch on at the Home screen, to close the Kit, and what the browser\'s small window is',
        /switch it on/.test(await u.p.textContent('#cable ol.steps')) && /Home screen/.test(await u.p.textContent('#cable ol.steps')) && /Connectivity Kit is open, close it/.test(await u.p.textContent('#cable ol.steps')) &&
        /^The first time, the browser opens a small window/.test(await u.p.textContent('#usbfirst')) && /Click its name, then click Connect/.test(await u.p.textContent('#usbfirst')));
  check('cable: the Connectivity Kit\'s steps are kept whole as way 2), folded under "2) The official HP way: the Connectivity Kit"',
        await u.p.isVisible('#kitsum') && (await u.p.textContent('#kitsum')) === '2) The official HP way: the Connectivity Kit' && !(await u.p.evaluate(() => document.getElementById('kitfold').open)) && !(await u.p.isVisible('#download3')) &&
        await u.p.locator('#kitroute ol.steps > li').count() === 6 && /Bonjour/.test(await u.p.textContent('#kitroute')) && /Drag each program file/.test(await u.p.textContent('#kitroute')));
  await u.p.click('#kitsum');
  check('... one click opens them: the download button and the six steps', await u.p.isVisible('#download3') && await u.p.isVisible('#kitroute ol.steps'));
  await u.p.click('#kitsum');
  check('cable: all the programs: CentralLimit, an app, is named as not travelling this way before anything is sent; the Kit\'s steps stay folded until they are wanted',
        /^Ready to send 30 programs\. CentralLimit \(an app or data\) does not travel the Statisticles way: it goes by the official HP way, 2\) below\.$/.test(await u.p.textContent('#usbstatus')) && !(await u.p.evaluate(() => document.getElementById('kitfold').open)),
        await u.p.textContent('#usbstatus'));
  await u.p.selectOption('#chapter', '12');
  const ch12 = CATALOG.chapters.find(c => c.num === 12).programs.concat([CATALOG.always]).filter((x, i, a) => a.indexOf(x) === i).sort((a, b) => a.localeCompare(b));
  check('cable: Chapter 12 (' + ch12.join(', ') + ') has no app in it: nothing to say before sending', (await u.p.textContent('#usbstatus')) === '' && ch12.every(n => CATALOG.programs[n].src), await u.p.textContent('#usbstatus'));
  await u.p.click('#usbsend');
  await usbEnd(u.p);
  let st = await state(u.p), got = await prime(u.p);
  check('cable, Chapter 12 to a G2: "Done. Your programs are on the calculator.", the bar full, each program ticked, Send ready again and Stop gone',
        st.done && !st.fail && st.cls === 'status ok' && st.status === ch12.length + ' programs on the calculator, each one read back and found the same.' && st.bar === '100' &&
        st.list.join() === ch12.map(n => 'ok:' + n).join() && !st.sendOff && st.stopHidden && st.unload, JSON.stringify([st.status, st.list, st.bar, st.sendOff]));
  check('... what the calculator holds is each program\'s source exactly as the pack\'s file holds it, character for character; and that is programs/ but for the blank space at its end',
        ch12.every(n => got.programs[n] === packSource(n)) && ch12.every(n => canon(got.programs[n]) === repoSource(n)) && Object.keys(got.programs).length === ch12.length,
        ch12.map(n => [n, (got.programs[n] || '').length, packSource(n).length]).join(' '));
  check('... sent the way both calculators kept: "FD 01 00 00 00 01 03" once in the old framing, then every program not compressed in the newer framing, 1,024-byte reports, none sent twice',
        got.fds.length === 1 && got.fds[0].kind === 'long' && got.fds[0].framing === 'old' && got.arrived.length === ch12.length && got.arrived.every(a => a.layout === 'v1' && a.framing === 'new' && a.kept) &&
        got.last === 1024 && got.outOfTurn === 0 && got.nacks === 0 && !got.err && got.opens === 1 && got.closes === 1, JSON.stringify([got.fds, got.arrived.length, got.last, got.outOfTurn, got.err, got.opens, got.closes]));
  check('... the page says what to do next (Shift, Program; tap, Run; Check if it says Syntax Error; unplug) and what happened (read back, character for character; nothing taken off)',
        /Shift, then Program/.test(st.next[0]) && ch12.every(n => st.next[0].includes(n)) && /tap Run/.test(st.next[1]) && /Syntax Error/.test(st.next[2]) && /tap Check/.test(st.next[2]) && /unplug/.test(st.next[3]) &&
        /went down the cable/.test(st.report[0]) && /read back from the calculator and found the same, character for character/.test(st.report[0]) && /left where they are/.test(st.report[1]) && /^It took \d+(\.\d)? seconds\.$/.test(st.report[2]),
        JSON.stringify([st.next, st.report]));
  check('... the details name the page, the browser, the calculator and the choice; say who answered and what each program did; end in a RESULT line; and hold neither the serial number nor more than twelve bytes of any message',
        /^HP Prime Loader, v2f, straight down the cable\. /.test(st.log) && /\nBrowser: Mozilla/.test(st.log) && /\nDevice: HP Prime G2 \(USB 03F0:2441\), "HP Prime"; reports of 1024 bytes in and 1024 out, by the calculator\.\n/.test(st.log) &&
        new RegExp('\\nChosen: Chapter 12; ' + ch12.length + ' programs, [\\d,]+ characters: ' + ch12.join(', ') + '\\.\\n').test(st.log) && /It answered: firmware build 15751, "V2\.060\.650", version 01\./.test(st.log) &&
        ch12.every(n => new RegExp('\\n +\\d+\\.\\d\\d  ' + n + ': [\\d,]+ characters\\.\\n').test(st.log)) && (st.log.match(/Read back the same: /g) || []).length === ch12.length &&
        new RegExp('RESULT: all ' + ch12.length + ' programs on the calculator, each read back the same\\. [\\d,]+ reports carried the programs there and back; \\d+\\.\\d s in all\\.').test(st.log) && !/SECRET|SERIAL/.test(st.log) &&
        Math.max(...(st.log.match(/begins ((?:[0-9A-F]{2} ?)+)/g) || []).map(x => x.trim().split(' ').length - 1)) === 12, st.log.slice(0, 900));
  await u.p.click('#usbdetails > summary');
  const [dlLog] = await Promise.all([u.p.waitForEvent('download'), u.p.click('#usbsave')]);
  const saved = fs.readFileSync(await dlLog.path(), 'utf8');
  check('... Save the details gives a text file named with the date, holding those lines and no serial number', /^PrimeLoader_cable_\d{4}-\d\d-\d\d_\d{4}\.txt$/.test(dlLog.suggestedFilename()) &&
        saved.replace(/\r\n/g, '\n') === st.log && !/SECRET|SERIAL/.test(saved) && /^Saved PrimeLoader_cable_.*\.txt in your Downloads folder\.$/.test(await u.p.textContent('#usbsaved')), dlLog.suggestedFilename());
  // a second load on the same page, without unplugging: the calculator speaks 03 already
  await u.p.selectOption('#chapter', '5');
  const ch5 = CATALOG.chapters.find(c => c.num === 5).programs.concat([CATALOG.always]).filter((x, i, a) => a.indexOf(x) === i).filter(n => CATALOG.programs[n].src).sort((a, b) => a.localeCompare(b));
  const after = await state(u.p);
  check('cable: choosing another chapter afterwards takes away what the page said of the finished load ("Done", the ticks, the bar), which was about other programs; the details stay',
        !after.done && !after.fail && after.list.length === 0 && after.barHidden && after.status === '' && /RESULT: all/.test(after.log), JSON.stringify([after.done, after.list, after.status]));
  await u.p.click('#usbsend');
  await usbEnd(u.p);
  st = await state(u.p); got = await prime(u.p);
  check('cable: a second load without unplugging (Chapter 5: ' + ch5.join(', ') + '): the browser\'s small window is not shown again, the calculator is not told "FD" again, the list starts afresh, the programs are ADDED to the first load\'s',
        st.done && st.list.join() === ch5.map(n => 'ok:' + n).join() && got.fds.length === 1 && ch5.concat(ch12).every(n => got.programs[n] === packSource(n)) && got.opens === 2 && got.closes === 2 && got.asked === 1 &&
        !/Told that this page speaks/.test(st.log) && /version 03\. Its reports/.test(st.log), JSON.stringify([st.list, got.fds.length, Object.keys(got.programs).length]));
  check('cable: no errors in the page', u.errs.length === 0, u.errs);

  // all the programs, onto a G1: 64-byte reports, 131,683 of them
  u = await usbPage({ product: 0x1541 });
  await u.p.check('#t_real');
  const names30 = Object.keys(CATALOG.programs).filter(n => CATALOG.programs[n].src).sort((a, b) => a.localeCompare(b));
  let tAll = Date.now();
  await u.p.click('#usbsend');
  await usbEnd(u.p, 300000);
  tAll = Date.now() - tAll;
  st = await state(u.p); got = await prime(u.p);
  const sentAll = got.arrived.reduce((s, a) => s + a.reports, 0), g1Want = names30.reduce((s, n) => s + 1 + Math.ceil((10 + 2 * n.length + 2 * packSource(n).length - 55) / 63), 0);
  check('cable, all the programs to a G1 (' + (tAll / 1000).toFixed(0) + ' s against the mock): the ' + names30.length + ' that are programs arrive, each the pack\'s source character for character, in ' + sentAll.toLocaleString('en-US') +
        ' reports of 64 bytes, none sent twice; the mock, which stands at 240 reports\' worth of an answer, never stood long',
        st.done && names30.length === 30 && st.list.join() === names30.map(n => 'ok:' + n).join() && names30.every(n => got.programs[n] === packSource(n)) && sentAll === g1Want && sentAll > 120000 && got.last === 64 &&
        got.outOfTurn === 0 && got.waits.every(w => w < 250) && !got.err, JSON.stringify([st.status, st.failh, sentAll, g1Want, got.outOfTurn, Math.max(0, ...got.waits), got.err]));
  const chars30 = names30.reduce((s, n) => s + packSource(n).length, 0), g2Want = names30.reduce((s, n) => s + 1 + Math.ceil((10 + 2 * n.length + 2 * packSource(n).length - 1015) / 1023), 0);
  check('... counted, because the page\'s notes say it: the 30 programs that travel by cable are 4,028,362 characters, 127,913 reports of a G1 and 7,892 of a G2; none has a CR in it',
        chars30 === 4028362 && sentAll === 127913 && g2Want === 7892 && names30.every(n => !/\r/.test(packSource(n))), [chars30, sentAll, g2Want].join(' '));
  check('... CentralLimit is said not to have been sent this way, and the Kit\'s steps are opened for it', st.report.some(l => /^Not sent this way: CentralLimit \(an app or data\)\. For it, use the official HP way \(2, just below\)\.$/.test(l)) && st.kitOpen && /Device: HP Prime G1 \(USB 03F0:1541\)/.test(st.log) &&
        /reports of 64 bytes in and 64 out/.test(st.log), JSON.stringify(st.report));
  check('... and the details stay readable: the page shows at most 1,500 lines of them', st.log.split('\n').length <= 1510, st.log.split('\n').length);
  check('cable: no errors in the page', u.errs.length === 0, u.errs);

  // ---- the slips ----
  u = await usbPage({ none: true });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p);
  check('slip: the browser\'s window closed with no calculator picked (or its list empty): "No calculator was chosen", what to look at (switched on, the cable, a cable that only charges), and Send ready again',
        st.fail && !st.done && st.failh === 'No calculator was chosen' && /Nothing was sent/.test(st.failp) && /switched on/.test(st.todo[0]) && /only charge/.test(st.todo[1]) && /then click Connect/.test(st.todo[2]) && !st.sendOff && st.barHidden && st.list.length === 0,
        JSON.stringify([st.failh, st.todo]));
  u = await usbPage({ busy: true });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p);
  check('slip: the Connectivity Kit left open, so the calculator cannot be opened: the page says to close the Kit and click again', st.fail && /could not open it/.test(st.failh) && /Close HP's Connectivity Kit/.test(st.todo[0]) && !st.sendOff, JSON.stringify([st.failh, st.todo]));
  u = await usbPage({ deadAfter: 0 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  let tS = Date.now();
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p); got = await prime(u.p);
  check('slip: a calculator that does not answer (switched off at the wrong moment, or not at Home): said after 3 s, "Nothing was sent", press Home, pull the cable and push it in again; the Kit\'s steps open; one report went, the question',
        st.fail && st.failh === 'The calculator did not answer' && st.failp === 'Nothing was sent.' && /Home/.test(st.todo[0]) && /Pull its cable out/.test(st.todo[1]) && st.kitOpen && got.reportsIn === 1 && got.arrived.length === 0 &&
        Date.now() - tS < 6000 && !st.sendOff && /NO ANSWER: no answer within 3\.0 s\./.test(st.log), JSON.stringify([st.failh, st.todo, got.reportsIn, Date.now() - tS]));
  u = await usbPage({ fdOld: null });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p); got = await prime(u.p);
  check('slip, not the student\'s: a calculator that still says version 01 after the "FD" (other software than the two it was proved on): nothing is sent, nothing about the calculator is changed, and the page points to the Kit and asks for the details',
        st.fail && /answers differently from the two this way was proved on/.test(st.failh) && /nothing was sent to it/.test(st.failp) && /Connectivity Kit/.test(st.todo[0]) && /Save the details/.test(st.todo[1]) && st.kitOpen &&
        got.arrived.length === 0 && !got.v2open && st.list.every(l => /^wait:/.test(l)), JSON.stringify([st.failh, got.arrived.length, got.v2open, st.list]));
  u = await usbPage({ drop: [ch12[1]] });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p); got = await prime(u.p);
  check('a program the calculator acknowledges and does not keep (' + ch12[1] + '): the load stops there; the one before it is ticked, this one crossed, the ones after never sent; the page does not say Done; ' +
        'it says to delete it if it is in the list and to use the Kit for it and the rest',
        st.fail && !st.done && st.failh === ch12[1] + ' did not come back the same' && /The calculator did not have it\./.test(st.failp) && /does not count it as loaded/.test(st.failp) && /marked ✓ is on the calculator, whole/.test(st.failp) &&
        st.list[0] === 'ok:' + ch12[0] && st.list[1] === 'bad:' + ch12[1] && st.list.slice(2).every(l => /^wait:/.test(l)) && got.arrived.length === 2 && /tap More, then Delete/.test(st.todo[0]) &&
        new RegExp('^Then use the official HP way \\(2, just below\\), for ' + ch12[1] + ' and the programs after it\\.$').test(st.todo[1]) && st.kitOpen && !st.sendOff, JSON.stringify([st.failh, st.failp, st.list, st.todo]));
  u = await usbPage({ cutAt: 5000 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p);
  check('a program damaged on the way: "What came back is not what was sent", nothing ticked, and the details say where the two part', st.fail && /What came back is not what was sent\./.test(st.failp) && st.list[0] === 'bad:' + ch12[0] &&
        /NOT THE SAME: 5,000 characters came back against [\d,]+ sent; the first difference is at character 5,001\./.test(st.log) && !/marked ✓/.test(st.failp), JSON.stringify([st.failp, st.list]));
  // the cable pulled out in the middle of a program; the browser's write never comes back (17 Nov, on the G2)
  // (the reports that have come from the host by the middle of the second program: the six of the opening, the first
  // program's, the request for it back and the acknowledgement of the answer, and thirty of the second)
  const first12 = 1 + Math.ceil((10 + 2 * ch12[0].length + 2 * packSource(ch12[0]).length - 1015) / 1023);
  u = await usbPage({ dieAt: 6 + first12 + 2 + 30, hang: true, tellAfter: 300 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  tS = Date.now();
  await u.p.click('#usbsend'); await usbEnd(u.p, 30000);
  st = await state(u.p); got = await prime(u.p);
  check('slip: the cable pulled out in the middle of the second program, and the browser\'s write to it never comes back: the page says so within seconds (' + ((Date.now() - tS) / 1000).toFixed(1) +
        ' s here), counts the first program and no other, and is ready to send again',
        st.fail && st.failh === 'The calculator went off the cable' && /The program marked ✓ is on the calculator, whole\./.test(st.failp) && new RegExp(ch12[1] + ' and the programs after it are not\\.').test(st.failp) &&
        st.list[0] === 'ok:' + ch12[0] && st.list[1] === 'bad:' + ch12[1] && st.list.slice(2).every(l => /^wait:/.test(l)) && got.arrived.length === 1 && Date.now() - tS < 12000 && !st.sendOff && st.stopHidden && st.unload && /Plug it in again/.test(st.todo[0]) &&
        /THE CALCULATOR WENT OFF THE CABLE/.test(st.log), JSON.stringify([st.failh, st.failp, st.list, Date.now() - tS]));
  check('... no errors in the page', u.errs.length === 0, u.errs);
  u = await usbPage({ dieAt: 60 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p, 30000);
  st = await state(u.p);
  check('slip: the cable pulled out and the browser says so at once: the same words', st.fail && st.failh === 'The calculator went off the cable' && !st.sendOff && u.errs.length === 0, JSON.stringify([st.failh, u.errs]));
  // Stop, clicked while the first program is being checked: the load ends after that program, not in it
  u = await usbPage({ lagMs: 900 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend');
  await u.p.waitForFunction(() => /^Checking /.test(document.getElementById('usbstatus').textContent));
  const mid = await state(u.p);
  await u.p.click('#usbsend', { force: true, timeout: 2000 }).catch(() => {});     // a second click on Send while it runs
  await u.p.click('#usbstop');
  const stopping = await u.p.textContent('#usbstop');
  await usbEnd(u.p);
  st = await state(u.p); got = await prime(u.p);
  check('while a load runs: Send is off and Stop is there; leaving the page would be asked about, because the calculator is in the middle of a program',
        mid.sendOff && !mid.stopHidden && !mid.unload && !mid.done && !mid.fail && /^check:/.test(mid.list[0]), JSON.stringify([mid.sendOff, mid.stopHidden, mid.unload, mid.list]));
  check('slip: Stop, and a second click on Send, while the first program is being checked: the button says it stops after this program; that program is finished and ticked, the next is never begun; ' +
        'the browser was asked for the calculator once only',
        stopping === 'Stopping after this program ...' && st.fail && st.failh === 'Stopped' && st.list[0] === 'ok:' + ch12[0] && st.list.slice(1).every(l => /^wait:/.test(l)) && got.arrived.length === 1 &&
        got.programs[ch12[0]] === packSource(ch12[0]) && got.asked === 1 && /were not sent/.test(st.failp) && /click Send to the calculator again/.test(st.todo[0]) && !st.sendOff && st.unload,
        JSON.stringify([stopping, st.failh, st.list, got.arrived.length, got.asked]));
  // the calculator's clock speaks while the first program is on its way (the G2 on 17 Nov)
  u = await usbPage({ tickOnReport: 1 });
  await u.p.check('#t_real'); await u.p.selectOption('#chapter', '12');
  await u.p.click('#usbsend'); await usbEnd(u.p);
  st = await state(u.p); got = await prime(u.p);
  check('the calculator\'s clock says "send again" just as each program\'s second report goes: every program still arrives the same, at the cost of one report sent twice each; the details show the "SEND AGAIN" lines',
        st.done && got.outOfTurn === ch12.length && got.nacks === ch12.length && ch12.every(n => got.programs[n] === packSource(n)) && (st.log.match(/"SEND AGAIN": report 02/g) || []).length === ch12.length &&
        /1 time a report was sent again/.test(st.log), JSON.stringify([st.done, got.outOfTurn, got.nacks]));
  // nothing chosen yet
  u = await usbPage({});
  await u.p.check('#w_chapter');
  check('slip: "One chapter" with no chapter picked: Send is off, and the page says to choose the chapter', await u.p.isDisabled('#usbsend') && (await u.p.textContent('#summary')) === 'Choose your chapter in the list above.' && (await u.p.textContent('#usbstatus')) === '');
  // nothing in the choice that the cable carries
  u = await usbPage({});
  await u.p.check('#t_real');
  await u.p.click('#more > summary'); await u.p.check('#w_pick'); await u.p.check('#p_CentralLimit');
  check('slip: only CentralLimit ticked, which is an app: Send is off, and the page says it goes by the Kit, whose steps are open',
        await u.p.isDisabled('#usbsend') && /^Nothing in your choice goes the Statisticles way: CentralLimit \(an app or data\) goes by the official HP way, 2\) below\.$/.test(await u.p.textContent('#usbstatus')) &&
        await u.p.evaluate(() => document.getElementById('kitfold').open) && await u.p.isVisible('#download3'), await u.p.textContent('#usbstatus'));
  await u.p.check('#p_DataLoad'); await u.p.check('#rossi');
  check('... with DataLoad ticked too and the sample data: Send is on for the one program, and the data is named with the app as going by the Kit',
        !(await u.p.isDisabled('#usbsend')) && /^Ready to send 1 program\. CentralLimit, M1 \(an app or data\) does not travel the Statisticles way: it goes by the official HP way, 2\) below\.$/.test(await u.p.textContent('#usbstatus')), await u.p.textContent('#usbstatus'));
  await u.p.setViewportSize({ width: 380, height: 800 });
  check('cable: at a phone\'s width nothing runs off the side', await u.p.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  // a G1 that fills up, as the author's did on 18 Nov at 15:41 (all 30 sent; full after 15; NormExplorer kept empty)
  u = await usbPage({ product: 0x1541, room: 2200000 });
  check('a G1: the cable\'s first step tells it to load one chapter at a time', await u.p.isVisible('#g1room') && /On an HP Prime G1, load one chapter at a time/.test(await u.p.textContent('#g1room')));
  await u.p.check('#w_all');
  await u.p.click('#usbsend');
  await usbEnd(u.p, 300000);
  { const st = await state(u.p), got = await u.p.evaluate(() => ({ h: document.getElementById('usbfailh').textContent, p: document.getElementById('usbfailp').textContent, d: document.getElementById('usbfaildo').textContent, kit: document.getElementById('kitfold').open }));
    check('... and when it fills up (here after 15 programs, at NormExplorer, as the author\'s did): "The calculator is full", the 15 marked done, NormExplorer marked bad, and what to do: delete its empty entry, load one chapter at a time',
          st.fail && got.h === 'The calculator is full' && st.list.filter(x => /^ok:/.test(x)).length === 15 && st.list.indexOf('bad:NormExplorer') === 15 &&
          /It took NormExplorer in and kept only its name/.test(got.p) && /The 15 programs marked ✓ are on the calculator, whole\./.test(got.p) &&
          /Tap NormExplorer \(it shows 0 KB\), tap More, then Delete\./.test(got.d) && /in step 2 choose One chapter/.test(got.d) && /NOT KEPT: the calculator took all of NormExplorer/.test(st.log), JSON.stringify([got, st.list.slice(13, 17)])); }

  // the plain address, as every student opens it (v2f: the cable for every student)
  u = await usbPage({}, '');
  check('the plain address opens on the Virtual Calculator, as always', await u.p.isChecked('#t_vc') && await u.p.isVisible('#load') && !(await u.p.isVisible('#cable')));
  await u.p.check('#t_real');
  check('the plain address in Chrome or Edge, for a real HP Prime: the two ways, under their title, with the cable\'s button and the Kit folded below as 2)', await u.p.isVisible('#cable') && await u.p.evaluate(() => PrimeUSB.supported() && usbOn && !usbAsked) &&
        await u.p.isVisible('#usbsend') && await u.p.isVisible('#kitsum') && await u.p.isVisible('#twoways') && !(await u.p.isVisible('#nocable')) && !(await u.p.evaluate(() => document.getElementById('kitfold').open)) &&
        (await u.p.textContent('#s3rtitle')) === 'Two ways to load Statisticles onto a physical Prime G1 or G2 calculator');
  await u.p.click('#usbsend');
  await usbEnd(u.p);
  { const st = await state(u.p);
    check('... and Send puts the 30 programs on a pretend G2 from the plain address, each read back the same', st.done && !st.fail && st.list.length === 30 && st.list.every(x => /^ok:/.test(x)), JSON.stringify(st).slice(0, 400)); }
  u = await usbPage({}, '?usb=1', false);
  await u.p.check('#t_real');
  check('at the test address in a browser that cannot reach a USB device (Firefox, Safari): no cable, no dead button, no "two ways"; the Kit\'s steps are the main line as before, and no error',
        !(await u.p.isVisible('#cable')) && await u.p.evaluate(() => !PrimeUSB.supported() && usbAsked && !usbOn) && await u.p.isVisible('#download3') && !(await u.p.isVisible('#kitsum')) && !(await u.p.isVisible('#twoways')) &&
        (await u.p.textContent('#s3rtitle')) === 'Put them on your HP Prime with HP\'s Connectivity Kit' && u.errs.length === 0, u.errs);

  const NOCABLE = ' cannot reach a calculator on its USB cable, so this page shows the official HP way, the Connectivity Kit, below. In Google Chrome or Microsoft Edge it can also send the programs straight down the cable, the Statisticles way.';
  check('a student\'s slip, a real HP Prime in a browser that cannot reach it on its cable: one sentence says so and names Chrome and Edge, above the Kit\'s steps, which are whole and work',
        await u.p.isVisible('#nocable') && (await u.p.textContent('#nocable')) === 'This browser' + NOCABLE && (await u.p.textContent('#nocable i')) === 'Statisticles' &&
        await u.p.evaluate(() => { const a = document.getElementById('nocable').getBoundingClientRect().top, b = document.getElementById('download3').getBoundingClientRect().top; return a < b; }) &&
        await u.p.isVisible('#download3') && u.errs.length === 0, u.errs);
  await u.p.check('#t_vc');
  check('... and it is not shown for the Virtual Calculator, which needs no cable', !(await u.p.isVisible('#nocable')));
  {
    const c = await browser.newContext({ userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0', acceptDownloads: true });
    const fp = await c.newPage(), ferrs = [];
    fp.on('pageerror', e => ferrs.push(String(e)));
    await fp.addInitScript(() => { delete window.showDirectoryPicker; Object.defineProperty(navigator, 'hid', { value: undefined, configurable: true }); });
    await fp.goto('http://localhost:8766/?usb=1');
    await fp.check('#t_real');
    check('... in Firefox the sentence names Firefox', await fp.isVisible('#nocable') && (await fp.textContent('#nocable')) === 'Firefox' + NOCABLE && ferrs.length === 0, ferrs);
    await c.close();
  }
  u = await usbPage({}, '?usb=1');
  await u.p.check('#t_real');
  check('... and it is not shown where the cable works (Chrome or Edge): there the two ways show', !(await u.p.isVisible('#nocable')) && await u.p.isVisible('#cable') && await u.p.isVisible('#twoways'));
  u = await usbPage({}, '', false);
  await u.p.check('#t_real');
  check('... and at the plain address, in a browser that cannot reach a USB device, the sentence shows too, above the Kit\'s steps',
        await u.p.isVisible('#nocable') && !(await u.p.isVisible('#cable')) && await u.p.isVisible('#download3') && u.errs.length === 0, u.errs);

  check('no errors in the page', errors.length === 0, errors);
  console.log(`\n${pass} PASS, ${fail} FAIL`);
  await browser.close(); srv.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
