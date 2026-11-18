// test_usb_page_v1.js -- PrimeUSBTest_v1.html in Chromium, with a pretend calculator in navigator.hid's place.
// Roger Metcalf & Claude, 17 Nov 2026.      node test_usb_page_v1.js ../PrimeUSBTest_v1.html
//
// NOTHING HERE TOUCHES A CALCULATOR.  The page is driven the way its reader will drive it, and the way a reader gets
// it wrong: no calculator on the cable, the Connectivity Kit still open, a browser that has no USB, the cable pulled
// out half way, Stop, and a calculator that will not let anything be read back, so that the person is asked.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path'), http = require('http');

const PAGE = path.resolve(process.argv[2]);
const MOCK = fs.readFileSync(path.join(__dirname, 'mock_prime_v1.js'), 'utf8');
let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
const FAST = { probe: 250, first: 2500, then: 2500, gap: 30, tries: 3, settle: 10 };

(async () => {
  const srv = http.createServer((q, r) => { r.setHeader('content-type', 'text/html; charset=utf-8'); r.end(fs.readFileSync(PAGE)); }).listen(8767);
  const browser = await chromium.launch();
  const open = async (mopts, extra) => {
    const ctx = await browser.newContext(Object.assign({ acceptDownloads: true }, extra || {}));
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    if (mopts !== null) await page.addInitScript({ content: 'window.__ladderT = ' + JSON.stringify(FAST) + ';\n' + MOCK + '\n;MockPrime.install(' + JSON.stringify(mopts || {}) + ');' });
    await page.goto('http://localhost:8767/');
    return { page, errors, ctx };
  };
  const done = page => page.waitForFunction(() => /The test has ended|broke off/.test(document.getElementById('rstatus').textContent), null, { timeout: 240000 });
  const cells = page => page.$$eval('#gridbody td', e => e.map(x => x.className + ':' + x.textContent));

  // ---- 1. the page as it opens
  let { page, errors } = await open({});
  check('U1 the table has a row for each of the four ways and a column for each of the five steps, all empty',
        await page.locator('#gridbody tr').count() === 4 && await page.locator('#gridhead th').count() === 6 && (await cells(page)).every(c => c === ':'));
  check('U1 the column heads give each step\'s size and what it stands for', /289,813 characters/.test(await page.textContent('#gridhead')) && /DataLoad, our smallest program/.test(await page.textContent('#gridhead')));
  check('U1 before connecting: Run, Stop, Save and Copy are off, and there is no notice about the browser',
        await page.isDisabled('#run') && await page.isDisabled('#stop') && await page.isDisabled('#save') && await page.isDisabled('#copy') && !(await page.isVisible('#nohid')));
  check('U1 the page says it has never been run on a calculator, and that it is not for students', /never been run on a calculator/.test(await page.textContent('header')) && /not for students/.test(await page.textContent('header')));
  check('U1 the three things to do first: a backup, close the Connectivity Kit, plug the calculator in', await page.locator('#s0 ~ ol.steps > li').count() === 3 && /Close HP's Connectivity Kit/.test(await page.textContent('ol.steps')));

  // ---- 2. connect, and the whole test on a calculator that does everything
  await page.click('#connect');
  await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent));
  const cs = await page.textContent('#cstatus');
  check('U2 connected: the model, the firmware build and the report size', /^Connected: HP Prime G2, firmware build 15515 \(V2\.060\.650\)\. Its reports are 1,024 bytes\.$/.test(cs), cs);
  let log = await page.inputValue('#log');
  check('U2 the log begins with the page\'s version, the browser and the device', /^PrimeUSBTest v1 \(ladder v1\), /.test(log) && /Browser: Mozilla/.test(log) && /Device: HP Prime G2 \(USB 03F0:2441\)/.test(log) && /reports of 1024 bytes in and 1024 out, by the calculator/.test(log), log);
  check('U2 Run is on now, and Connect has become Disconnect', !(await page.isDisabled('#run')) && await page.isVisible('#disconnect') && !(await page.isVisible('#connect')));
  await page.click('#run');
  check('U2 while it runs: Run is off, Stop is on', await page.isDisabled('#run') && !(await page.isDisabled('#stop')));
  await done(page);
  let cs2 = await cells(page);
  check('U2 all twenty cells say OK and their reports', cs2.length === 20 && cs2.every(c => /^ok:OK\d+ reports?$/.test(c)), JSON.stringify(cs2));
  const res = await page.textContent('#resulttext');
  check('U2 the result is shown in plain words', await page.isVisible('#result') && /A test program of 289,813 characters, the size of our largest program, arrived whole/.test(res) && /deleted from the calculator again/.test(res), res);
  const m = await page.evaluate(() => ({ programs: Object.keys(window.__prime.programs), arrived: window.__prime.arrived.length, last: window.__prime.lastLength, asked: window.__prime.asked, error: window.__prime.error || null,
                                         names: window.__prime.arrived.map(a => a.name).filter((v, i, a) => a.indexOf(v) === i).sort() }));
  check('U2 on the calculator: twenty programs arrived under the four test names only, none is left, and every report was 1,024 bytes', m.programs.length === 0 && m.arrived === 20 &&
        m.names.join() === 'ZZUSBA,ZZUSBB,ZZUSBC,ZZUSBD' && m.last === 1024 && m.asked === 1 && m.error === null, JSON.stringify(m));
  log = await page.inputValue('#log');
  check('U2 the log has the test\'s start, its result and its end, with the count of reports', /---- test started/.test(log) && /\n +\d+\.\d  RESULT\n/.test(log) && /---- test ended .*reports sent \d+, received \d+ ----/.test(log));
  check('U2 the serial number is nowhere on the page or in the log', !/SECRET/.test(log) && !/SECRET/.test(await page.content()));
  const [dl] = await Promise.all([page.waitForEvent('download'), page.click('#save')]);
  const saved = fs.readFileSync(await dl.path(), 'utf8');
  check('U2 Save the log: a text file named by date and time, holding the log', /^PrimeUSBTest_log_\d{4}-\d\d-\d\d_\d{4}\.txt$/.test(dl.suggestedFilename()) && saved.replace(/\r\n/g, '\n').trim() === log.trim() && /Saved PrimeUSBTest_log_/.test(await page.textContent('#lstatus')), dl.suggestedFilename());
  check('U2 no errors in the page', errors.length === 0, errors);

  // ---- 3. nothing on the cable
  ({ page, errors } = await open({ none: true }));
  await page.click('#connect');
  await page.waitForFunction(() => /No calculator was chosen/.test(document.getElementById('cstatus').textContent));
  check('U3 no calculator in the browser\'s list: the page says what to check, and Run stays off', /is it switched on, and is the cable pushed in at both ends/.test(await page.textContent('#cstatus')) && await page.isDisabled('#run') && !(await page.isDisabled('#connect')));

  // ---- 4. the Connectivity Kit still open
  ({ page, errors } = await open({ busy: true }));
  await page.click('#connect');
  await page.waitForFunction(() => /could not open it/.test(document.getElementById('cstatus').textContent));
  check('U4 the calculator is held by another program: the page names the Connectivity Kit and says to close it, and Run stays off', /Close the Kit, then click Connect again/.test(await page.textContent('#cstatus')) && await page.isDisabled('#run') && errors.length === 0, errors);

  // ---- 5. a browser with no USB for pages
  ({ page, errors } = await open(null));
  await page.addInitScript(() => { Object.defineProperty(Navigator.prototype, 'hid', { get: () => undefined, configurable: true }); });
  await page.reload();
  check('U5 no WebHID: a notice names Edge and Chrome, and Connect is off', await page.isVisible('#nohid') && /Microsoft Edge/.test(await page.textContent('#nohid')) && await page.isDisabled('#connect') && errors.length === 0, errors);

  // ---- 6. a calculator that answers no request for a program: the person is asked
  ({ page, errors } = await open({ silentF8: true }));
  await page.click('#connect');
  await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent));
  await page.click('#run');
  const answers = [];
  for (let i = 0; i < 6; i++) {
    await page.waitForSelector('#ask:not([hidden])', { timeout: 120000 });
    const q = await page.textContent('#askp'), yes = await page.textContent('#askyes');
    answers.push(q.match(/Is (ZZUSB[A-D]) in the list/)[1] + ':' + yes.match(/says ZZUSB[A-D] (\d)/)[1] + (q.includes('\u201c' + yes.replace('Yes, it says ', '') + '\u201d') ? '' : '?'));
    await page.click(i === 5 ? '#askno' : '#askyes');                 // the last one, way D, was not seen
    // the next question can follow at once, so wait for the panel to close OR to ask something else
    await page.waitForFunction(prev => document.getElementById('ask').hidden || document.getElementById('askp').textContent !== prev, q, { timeout: 120000 });
  }
  await done(page);
  check('U6 nothing can be read back: six questions, each naming a program and what its box should say ("ZZUSBA 1", as the Virtual Calculator showed it)', answers.join(' ') === 'ZZUSBA:1 ZZUSBB:1 ZZUSBC:1 ZZUSBA:3 ZZUSBA:5 ZZUSBD:1', answers.join(' '));
  const r6 = await page.textContent('#resulttext');
  check('U6 the result says way A was checked by eye, that nothing could be read back, and what to delete by hand', /way A, checked by eye/.test(r6) && /answered none of the four requests/.test(r6) && /To delete by hand/.test(r6) && /tap More, then Delete/.test(r6), r6);
  cs2 = await cells(page);
  check('U6 the cells say "seen on the calculator", and way D\'s says it was not', cs2.filter(c => /^ok:OKseen on the calculator$/.test(c)).length === 5 && cs2.some(c => /^bad:FAILEDnot on the calculator$/.test(c)), JSON.stringify(cs2));
  check('U6 no errors in the page', errors.length === 0, errors);

  // ---- 7. the cable pulled out half way
  ({ page, errors } = await open({}));
  await page.click('#connect');
  await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent));
  await page.evaluate(() => { const m = window.__prime, r0 = m.receive.bind(m); m.receive = function (r) { if (m.reportsIn > 60 && !m.unplugged) m.unplug(); return r0(r); }; });
  await page.click('#run');
  await done(page);
  const r7 = await page.textContent('#resulttext'), l7 = await page.inputValue('#log');
  check('U7 unplugged during the test: the test stops, says the calculator stopped answering, and nothing more is sent', /stopped answering during the test/.test(r7) && /NOT SENT/.test(l7) && /THE CALCULATOR HAS STOPPED ANSWERING/.test(l7) &&
        /THE CALCULATOR WAS UNPLUGGED/.test(l7) && (await page.getAttribute('#result', 'class')) === 'panel warn' && errors.length === 0, r7 + errors);
  await page.waitForFunction(() => /Plug it in again and click Connect/.test(document.getElementById('cstatus').textContent), null, { timeout: 5000 }).catch(() => {});
  check('U7 ... and afterwards the page is disconnected: it says to plug the calculator in again, Run is off and Connect is back', /unplugged or switched off during the test\. Plug it in again and click Connect/.test(await page.textContent('#cstatus')) &&
        await page.isDisabled('#run') && await page.isVisible('#connect'), await page.textContent('#cstatus'));

  // ---- 7b. the cable pulled out while nothing is running
  ({ page, errors } = await open({}));
  await page.click('#connect');
  await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent));
  await page.evaluate(() => window.__prime.unplug());
  await page.waitForFunction(() => /unplugged/.test(document.getElementById('cstatus').textContent), null, { timeout: 5000 }).catch(() => {});
  check('U7b unplugged while idle: the page says so at once, Run goes off, Connect comes back, and the log notes it', /The calculator was unplugged or switched off\. Plug it in again and click Connect/.test(await page.textContent('#cstatus')) &&
        await page.isDisabled('#run') && await page.isVisible('#connect') && /THE CALCULATOR WAS UNPLUGGED/.test(await page.inputValue('#log')) && errors.length === 0, await page.textContent('#cstatus'));

  // ---- 8. Stop
  ({ page, errors } = await open({}));
  await page.click('#connect');
  await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent));
  await page.click('#run');
  await page.waitForFunction(() => /UP THE LADDER/.test(document.getElementById('log').value));
  await page.click('#stop');
  await done(page);
  const l8 = await page.inputValue('#log');
  check('U8 Stop: the test ends at the step in hand, takes its programs off, and Run comes back on', /STOPPED by the Stop button/.test(l8) && /stopped before its end/.test(await page.textContent('#resulttext')) &&
        (await page.evaluate(() => Object.keys(window.__prime.programs).length)) === 0 && !(await page.isDisabled('#run')) && await page.isDisabled('#stop'));

  // ---- 9. disconnect and connect again; a narrow window; the page as a file
  await page.click('#disconnect');
  check('U9 Disconnect: Run goes off and Connect comes back', await page.isDisabled('#run') && await page.isVisible('#connect') && /Disconnected/.test(await page.textContent('#cstatus')));
  await page.click('#connect');
  await page.waitForFunction(() => /Connected/.test(document.getElementById('cstatus').textContent));
  check('U9 ... and connecting again starts a fresh log', /^PrimeUSBTest v1/.test(await page.inputValue('#log')) && !/STOPPED/.test(await page.inputValue('#log')));
  await page.setViewportSize({ width: 380, height: 800 });
  check('U9 at a phone\'s width the page does not scroll sideways (the table scrolls inside its own box)', await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth));
  const f = await open({});
  await f.page.goto('file://' + PAGE);
  check('U9 opened as a file from a folder: no errors, and the browser offers USB there', f.errors.length === 0 && await f.page.evaluate(() => PrimeUSB.supported()) && !(await f.page.isVisible('#nohid')), f.errors);

  console.log(`\n${pass} PASS, ${fail} FAIL`);
  await browser.close(); srv.close();
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
