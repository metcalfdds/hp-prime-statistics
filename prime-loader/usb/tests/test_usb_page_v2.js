// test_usb_page_v2.js -- PrimeUSBTest_v2.html in Chromium, with a pretend calculator in navigator.hid's place.
// Roger Metcalf & Claude, 17 Nov 2026.      node test_usb_page_v2.js ../PrimeUSBTest_v2.html
//
// NOTHING HERE TOUCHES A CALCULATOR.  The page is driven the way its reader will drive it, and the ways it goes wrong
// for a reader: no calculator on the cable, the Connectivity Kit still open, a browser that has no USB, Stop, and
// above all a calculator that goes off the cable in the middle, with a write that never comes back: what happened on
// 17 Nov 2026, when the first page stood still ("the program seems stuck").
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');

const PAGE = path.resolve(process.argv[2]);
const MOCK = fs.readFileSync(path.join(__dirname, 'mock_prime_v2.js'), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
const FAST = { first: 600, then: 500, probe: 150, listen: 80, gap: 60, tries: 3, settle: 10, quiet: 30, recover: 1500 };
const PACE = { release: 5, stall: 40, patience: 60, ack: 300 };

(async () => {
  const srv = http.createServer((q, r) => { r.setHeader('content-type', 'text/html; charset=utf-8'); r.end(fs.readFileSync(PAGE)); }).listen(8767);
  const browser = await chromium.launch();
  const open = async (mopts, extra) => {
    const ctx = await browser.newContext(Object.assign({ acceptDownloads: true }, extra || {}));
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    if (mopts !== null) await page.addInitScript({ content: 'window.__ladderT = ' + JSON.stringify(FAST) + '; window.__pace = ' + JSON.stringify(PACE) + ';\n' + MOCK + '\n;MockPrime.install(' + JSON.stringify(mopts || {}) + ');' });
    await page.goto('http://localhost:8767/');
    return { page, errors, ctx };
  };
  const connect = async page => { await page.click('#connect'); await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent)); };
  const ended = page => page.waitForFunction(() => /The test has ended|broke off/.test(document.getElementById('rstatus').textContent), null, { timeout: 120000 });
  const cells = page => page.$$eval('#gridbody td[id]', e => e.map(x => x.id.slice(2) + '=' + x.className + ':' + (x.querySelector('.mark') ? x.querySelector('.mark').textContent : '')));
  const visible = (page, sel) => page.waitForSelector(sel, { state: 'visible', timeout: 60000 });
  const mockState = page => page.evaluate(() => ({ programs: Object.keys(window.__prime.programs), arrived: window.__prime.arrived.map(a => a.name), last: window.__prime.lastLength, error: window.__prime.error || null, fmt: window.__prime.fmt }));

  // ---- 1. the page as it opens
  let { page, errors } = await open({});
  check('U1 the table has a row for each of the four routes: three cells for C and five for each other, each with what it will send and no mark yet',
        await page.locator('#gridbody tr').count() === 4 && await page.locator('#gridbody td[id]').count() === 18 && (await cells(page)).every(c => /=:$/.test(c)) &&
        /exactly 255 reports/.test(await page.textContent('#c_C3')) && /289,813 characters/.test(await page.textContent('#c_D5')), JSON.stringify(await cells(page)));
  check('U1 before connecting: Run, Stop, Save and Copy are off, and there is no notice about the browser',
        await page.isDisabled('#run') && await page.isDisabled('#stop') && await page.isDisabled('#save') && await page.isDisabled('#copy') && !(await page.isVisible('#nohid')) && !(await page.isVisible('#ask')) && !(await page.isVisible('#pause')));
  const head = await page.textContent('header');
  check('U1 the page says it is the second test, what the first found, and that it is not for students', /This is the second test/.test(head) && /17 November 2026/.test(head) && /not compressed/.test(head) && /not for students/.test(head));
  check('U1 the four things to do first: a backup, close the Connectivity Kit, plug the calculator in, and press Home just before Run', await page.locator('#s0 ~ ol.steps > li').count() === 4 &&
        /Close HP's Connectivity Kit/.test(await page.textContent('ol.steps')) && /Just before you click Run, press the Home key/.test(await page.textContent('ol.steps')));

  // ---- 2. connect, and the whole test on the leading reading of a G2
  await connect(page);
  const cs = await page.textContent('#cstatus');
  check('U2 connected: the model, the firmware build and the report size', /^Connected: HP Prime G2, firmware build 15751 \(V2\.060\.650\)\. Its reports are 1,024 bytes\.$/.test(cs), cs);
  let log = await page.inputValue('#log');
  check('U2 the log begins with the page\'s version, the browser, the device and the version it answers with', /^PrimeUSBTest v2 \(ladder v2\), /.test(log) && /Browser: Mozilla/.test(log) && /Device: HP Prime G2 \(USB 03F0:2441\), "HP Prime"; reports of 1024 bytes in and 1024 out, by the calculator\./.test(log) &&
        /Identify: firmware build 15751, "V2\.060\.650", version 01\./.test(log), log);
  check('U2 Run is on now, and Connect has become Disconnect', !(await page.isDisabled('#run')) && await page.isVisible('#disconnect') && !(await page.isVisible('#connect')));
  await page.click('#run');
  check('U2 while it runs: Run is off, Stop is on', await page.isDisabled('#run') && !(await page.isDisabled('#stop')));
  await visible(page, '#ask');
  check('U2 half way, the page asks the person to look for ZZUSBA in the calculator\'s list, with the keys to press, and waits', /press Shift, then Program \(the 1 key\)\. Is ZZUSBA in the list\?/.test(await page.textContent('#askp')) &&
        /^Yes, ZZUSBA is in the list$/.test(await page.textContent('#askyes')) && /^No, it is not$/.test(await page.textContent('#askno')) && !(await page.isVisible('#pause')));
  const before = (await page.inputValue('#log')).length;
  await page.waitForTimeout(400);
  check('U2 ... nothing is sent while it waits for the answer', (await page.inputValue('#log')).length === before);
  await page.click('#askno');
  await ended(page);
  let cs2 = await cells(page);
  check('U2 the table: C three times OK, E once OK, D five times OK, and A, tried again at the end, five times OK', cs2.join() === 'C1=ok:OK,C2=ok:OK,C3=ok:OK,A1=ok:OK,A2=ok:OK,A3=ok:OK,A4=ok:OK,A5=ok:OK,E1=ok:OK,E2=:,E3=:,E4=:,E5=:,D1=ok:OK,D2=ok:OK,D3=ok:OK,D4=ok:OK,D5=ok:OK', cs2.join());
  const res = await page.textContent('#resulttext');
  check('U2 the result is shown in plain words, in the green panel', await page.isVisible('#result') && /A PROGRAM THE SIZE OF THE BOOK'S LARGEST \(289,813 characters\) WENT TO THIS CALCULATOR AND CAME BACK THE SAME/.test(res) &&
        /The test's programs were taken off the calculator again/.test(res) && /panel done/.test(await page.getAttribute('#result', 'class')), res);
  const m = await mockState(page);
  check('U2 the calculator holds nothing of the test afterwards, only the four test programs were ever sent, and every report went out at 1,024 bytes',
        m.programs.length === 0 && m.arrived.every(n => n === null || /^ZZUSB[CAED]$/.test(n)) && m.last === 1024 && !m.error, JSON.stringify(m));
  log = await page.inputValue('#log');
  check('U2 the log holds the answer of the person, the calculator\'s own reports, the result, and where the test started and ended', /whether ZZUSBA is in its list of programs: no, it is not there\./.test(log) &&
        /\. < acknowledgement: report 01, position 1,015, message/.test(log) && /RESULT/.test(log) && /---- test started \d\d:\d\d:\d\d ----/.test(log) && /---- test ended \d\d:\d\d:\d\d; reports sent [\d]+, received [\d]+ ----/.test(log));
  check('U2 the log does not hold the serial number, as text or as bytes', !/SECRET/.test(log) && !/53 45 43 52/.test(log));
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#save')]);
  const saved = fs.readFileSync(await dl.path(), 'utf8');
  check('U2 Save the log: a text file named for the second test and the time, with Windows line ends, holding the whole log', /^PrimeUSBTest2_log_\d{4}-\d\d-\d\d_\d{4}\.txt$/.test(dl.suggestedFilename()) && saved.replace(/\r\n/g, '\n').trim() === log.trim() && /\r\n/.test(saved), dl.suggestedFilename());
  // ---- a second run with no reconnecting: the calculator has been in the newer framing meanwhile
  await page.click('#run');
  await visible(page, '#pause');
  check('U2 Run once more, with nothing unplugged: this time the mock speaks 03, A is kept, and the page asks only for a key on the calculator', /Press the Home key on the calculator, then click Continue/.test(await page.textContent('#pause')) && !(await page.isVisible('#ask')));
  await page.click('#pausego');
  await ended(page);
  cs2 = await cells(page);
  check('U2 ... and the second run ends like the first, with A now OK at all five sizes', cs2.filter(c => /=ok:OK$/.test(c)).length === 14 && /^A5=ok:OK$/.test(cs2[7]) && (await mockState(page)).programs.length === 0, cs2.join());
  check('U2 no error of the page\'s own', errors.length === 0, errors.join(' | '));
  await page.context().close();

  // ---- 3. what stopped the first page: the calculator goes off the cable, and the write in hand never comes back
  ({ page, errors } = await open({ dieAt: 560, hang: true }));
  await connect(page);
  let t0 = Date.now();
  await page.click('#run');
  await visible(page, '#ask');
  await page.click('#askno');
  await ended(page);
  const took = Date.now() - t0;
  const r3 = await page.textContent('#resulttext'), l3 = await page.inputValue('#log');
  check('U3 a calculator that goes off the cable while a write to it never comes back: the test ENDS (in ' + (took / 1000).toFixed(1) + ' s), where the first page stood still for good', took < 60000 && /The test has ended/.test(await page.textContent('#rstatus')));
  check('U3 the log has the browser\'s word for it and the test\'s, and the result says what stands and what may be left on the calculator', /THE BROWSER SAYS THE CALCULATOR WENT OFF THE CABLE \(\d\d:\d\d:\d\d\)\./.test(l3) &&
        /THE CALCULATOR WENT OFF THE CABLE: the browser says it went off the cable \(unplugged, or switched off\)\. Nothing more can be sent\./.test(l3) && /THE CALCULATOR WENT OFF THE CABLE before the test ended/.test(r3) &&
        /STILL ON THE CALCULATOR, or not known to be off it: /.test(r3) && /panel warn/.test(await page.getAttribute('#result', 'class')), r3);
  check('U3 afterwards the page is back at Connect, says to turn the calculator on and plug it in, and Run is off', await page.isVisible('#connect') && await page.isDisabled('#run') &&
        /went off the cable during the test: unplugged, or it switched itself off\. Turn it on, plug it in again and click Connect/.test(await page.textContent('#cstatus')) && !(await page.isDisabled('#save')));
  check('U3 no error of the page\'s own', errors.length === 0, errors.join(' | '));
  await page.context().close();

  // ---- 4. off the cable while the page is waiting for the person
  ({ page, errors } = await open({}));
  await connect(page);
  await page.click('#run');
  await visible(page, '#ask');
  await page.evaluate(() => window.__prime.unplug());
  await ended(page);
  check('U4 off the cable while the page waits for an answer from the person: the question is taken away and the test ends', !(await page.isVisible('#ask')) && /WENT OFF THE CABLE/.test(await page.textContent('#resulttext')) && await page.isVisible('#connect') && errors.length === 0, errors.join(' | '));
  await page.context().close();
  ({ page, errors } = await open({}));
  await connect(page);
  await page.evaluate(() => window.__prime.unplug());
  await page.waitForFunction(() => /went off the cable/.test(document.getElementById('cstatus').textContent));
  check('U4 off the cable before Run: the page says so and goes back to Connect', await page.isVisible('#connect') && await page.isDisabled('#run') && /THE BROWSER SAYS THE CALCULATOR WENT OFF THE CABLE/.test(await page.inputValue('#log')));
  await page.context().close();

  // ---- 5. Stop
  ({ page, errors } = await open({}));
  await connect(page);
  await page.click('#run');
  await visible(page, '#ask');
  await page.click('#stop');
  await ended(page);
  const r5 = await page.textContent('#resulttext');
  check('U5 Stop while the page waits for the person: the question goes, the test ends, says it was stopped, and its programs are off the calculator', !(await page.isVisible('#ask')) && /The test was stopped before its end/.test(r5) &&
        /The test's programs were taken off the calculator again/.test(r5) && (await mockState(page)).programs.length === 0 && await page.isDisabled('#stop') && !(await page.isDisabled('#run')) && errors.length === 0, r5);
  await page.context().close();
  ({ page, errors } = await open({ product: 0x1541, fdNew: null }));
  await connect(page);
  check('U5 a G1: the device line gives its name and its 64-byte reports', /Device: HP Prime G1 \(USB 03F0:1541\), "Prime Graphing Calculator"; reports of 64 bytes in and 64 out/.test(await page.inputValue('#log')) && /Its reports are 64 bytes/.test(await page.textContent('#cstatus')));
  await page.click('#run');
  await visible(page, '#ask');
  await page.click('#askno');
  await page.waitForFunction(() => /busy/.test((document.getElementById('c_E4') || {}).className || ''), null, { timeout: 120000 });
  await page.click('#stop');
  await ended(page);
  const r5b = await page.textContent('#resulttext');
  check('U5 Stop in the middle of a long send on a G1: the test ends at the step in hand and takes its programs off', /The test was stopped before its end/.test(r5b) && (await mockState(page)).programs.length === 0 && errors.length === 0, r5b + errors.join(' | '));
  await page.context().close();

  // ---- 6. the ways of not getting started
  ({ page, errors } = await open({ none: true }));
  await page.click('#connect');
  await page.waitForFunction(() => /No calculator was chosen/.test(document.getElementById('cstatus').textContent));
  check('U6 no calculator on the cable: the page says what to look at (switched on, the cable, a cable that only charges), and Run stays off', /is it switched on/.test(await page.textContent('#cstatus')) && /only charge/.test(await page.textContent('#cstatus')) && await page.isDisabled('#run'));
  await page.context().close();
  ({ page, errors } = await open({ busy: true }));
  await page.click('#connect');
  await page.waitForFunction(() => /could not open it/.test(document.getElementById('cstatus').textContent));
  check('U6 the Connectivity Kit still open: the page says to close the Kit, in those words', /Close the Kit, then click Connect again/.test(await page.textContent('#cstatus')) && await page.isDisabled('#run'));
  await page.context().close();
  ({ page, errors } = await open({ deadAfter: 0 }));
  await page.click('#connect');
  await page.waitForFunction(() => /did not answer when asked who it is/.test(document.getElementById('cstatus').textContent), null, { timeout: 20000 });
  check('U6 a calculator that does not answer: the page says so, and what to do if a test has just run', /unplug the calculator, plug it in again/.test(await page.textContent('#cstatus')) && /Identify: no answer\./.test(await page.inputValue('#log')));
  await page.click('#run');
  await ended(page);
  check('U6 ... Run then sends nothing and says why', /did not answer, so nothing was sent to it/.test(await page.textContent('#resulttext')) && (await mockState(page)).arrived.length === 0);
  await page.context().close();
  ({ page, errors } = await open(null));
  await page.addInitScript(() => { Object.defineProperty(navigator, 'hid', { value: undefined, configurable: true }); });
  await page.reload();
  check('U6 a browser with no USB for pages: the notice shows, names Edge and Chrome, and Connect is off', await page.isVisible('#nohid') && /Microsoft Edge/.test(await page.textContent('#nohid')) && await page.isDisabled('#connect') && errors.length === 0, errors.join(' | '));
  await page.context().close();

  // ---- 7. a narrow window
  ({ page, errors } = await open({}, { viewport: { width: 390, height: 800 } }));
  const wide = await page.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
  check('U7 at a phone\'s width the page itself does not scroll sideways (the table scrolls in its own box)', wide <= 1, wide);
  await page.context().close();

  await browser.close(); srv.close();
  console.log(`\n${pass} PASS, ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
