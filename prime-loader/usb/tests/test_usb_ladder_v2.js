// test_usb_ladder_v2.js -- usb_ladder_v2.js against the mock calculator, with one thing changed at a time: what the
// second test page will conclude on each such calculator.  Roger Metcalf & Claude, 17 Nov 2026.
//
//     node test_usb_ladder_v2.js            (about three minutes)
//
// NOTHING HERE TOUCHES A CALCULATOR.  The mock does by default what the author's G2 and G1 did on 17 Nov 2026, and
// beyond that what the leading reading says; each scenario below is a calculator that turns out otherwise.  A pass
// says the test page reaches a true conclusion on every one of them, in a time that has an end.
const fs = require('fs'), path = require('path');
const P = require('../prime_usb_v2.js'), MockPrime = require('./mock_prime_v2.js'), L = require('../usb_ladder_v2.js');
const PROGRAMS = path.join(__dirname, '..', '..', '..', 'programs');

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
const T = { first: 600, then: 500, probe: 150, listen: 80, gap: 60, tries: 3, settle: 10, quiet: 30, recover: 1500 };
// One run of the test on one mock.  person: what the person at the calculator answers when asked whether a program
// is in its list ('look': what is true of the mock).  stopAt: press Stop once the log has this many lines.
async function scenario(mopts, extra) {
  extra = extra || {};
  const mock = new MockPrime(mopts), lines = [], cells = {}, asked = [];
  let paused = 0;
  const link = new P.Link(mock.port());
  Object.assign(link.pace, { release: 5, stall: 40, patience: 60, ack: 300 });
  const t0 = Date.now();
  const res = await L.run(link, {
    log: s => lines.push(s), cell: (k, c, st, tx) => { cells[k + c] = st + ':' + tx; },
    ask: async q => { asked.push(q.name); return extra.person === undefined ? !!mock.programs[q.name] : extra.person; },
    pause: async () => { paused++; },
    stop: () => !!extra.stopAt && lines.length >= extra.stopAt
  }, { core: P, t: T, budget: extra.budget });
  mock.stop();
  return { mock, res, lines, log: lines.join('\n'), cells, asked, paused, ms: Date.now() - t0, link };
}
const ok5 = (cells, k) => [1, 2, 3, 4, 5].every(c => /^ok:/.test(cells[k + c] || ''));
const none = (cells, k) => [1, 2, 3, 4, 5].every(c => !(k + c in cells));

(async () => {
  // ---------------------------------------------------------------- the test programs
  const sizeOf = n => P.normalizeSource(fs.readFileSync(path.join(PROGRAMS, fs.readdirSync(PROGRAMS).filter(f => f.startsWith(n + '_'))[0]), 'utf8')).length;
  const all = fs.readdirSync(PROGRAMS).filter(f => /\.txt$/.test(f)).map(f => P.normalizeSource(fs.readFileSync(path.join(PROGRAMS, f), 'utf8')).length);
  check('P1 size 3 is DataLoad\'s length and size 5 EpiStats\'s, the smallest and the largest of the ' + all.length + ' programs in programs/',
        L.SIZES[2].chars === sizeOf('DataLoad') && L.SIZES[4].chars === sizeOf('EpiStats') && Math.min(...all) === L.SIZES[2].chars && Math.max(...all) === L.SIZES[4].chars, sizeOf('DataLoad') + ' ' + sizeOf('EpiStats'));
  let exact = true, shape = true;
  for (const r of L.ROUTES) for (const s of L.SIZES) {
    const p = L.makeProgram(r.name, s.step, s.chars);
    if (p.length !== s.chars || p !== L.makeProgram(r.name, s.step, s.chars)) exact = false;
    if (!p.endsWith('\nEXPORT ' + r.name + '()\nBEGIN\n RETURN ' + s.step + ';\nEND;') || p.split('\n').slice(0, -4).some(l => !/^\/\/ /.test(l) && l.trim() !== '')) shape = false;
  }
  check('P2 a test program is exactly the length asked for, every time the same text', exact);
  check('P3 it is comment lines and one function, the function last, so that a program cut short does not compile', shape);
  let fills = true;
  const counts = [];
  for (const cap of [1023, 63]) for (const n of L.LIMITS) {
    const chars = L.charsFor(n, cap, 'ZZUSBC'), got = P.framesLegacy(P.programV1('ZZUSBC', L.makeProgram('ZZUSBC', n, chars)), cap).length;
    counts.push(got + ' reports of ' + (cap + 1) + ': ' + chars.toLocaleString('en-US') + ' characters');
    if (got !== n || P.framesLegacy(P.programV1('ZZUSBC', L.makeProgram('ZZUSBC', n, chars + 1)), cap).length !== n + 1) fills = false;
  }
  check('P4 route C\'s two programs fill exactly 254 and 255 reports, of a G2 and of a G1, and one character more would need one report more (' + counts.join('; ') + ')', fills);
  const zipped = [];
  for (const s of L.SIZES) zipped.push(Math.ceil((await P.programV3('ZZUSBD', L.makeProgram('ZZUSBD', s.step, s.chars))).length / 1023));
  const realZip = Math.ceil((await P.programV3('EpiStats', P.normalizeSource(fs.readFileSync(path.join(PROGRAMS, fs.readdirSync(PROGRAMS).filter(f => f.startsWith('EpiStats_'))[0]), 'utf8')))).length / 1023);
  check('P5 compressed, the five test programs are ' + zipped.join(', ') + ' reports of a G2; the largest compresses a little worse than EpiStats itself (' + realZip + '), so it is the harder case',
        zipped[0] === 1 && zipped[4] > realZip && zipped[4] <= 1.4 * realZip, zipped.join());
  check('P6 the table of the page: three cells for route C and five for each other', L.cellsOf('C').length === 3 && /254/.test(L.cellsOf('C')[1].cap) && ['A', 'E', 'D'].every(k => L.cellsOf(k).length === 5) && /289,813/.test(L.cellsOf('D')[4].cap));

  // ---------------------------------------------------------------- 1. the leading reading, on a G2
  let s = await scenario({});
  check('S1 G2, the leading reading: C comes back at a few lines, at 254 reports and at 255', ['C1', 'C2', 'C3'].every(k => /^ok:/.test(s.cells[k])) && /^ok:255 reports$/.test(s.cells.C3), JSON.stringify(s.cells));
  check('S1 A (old framing, compressed) is not kept at first, though told "FD", and the person is asked to look for ZZUSBA', /ZZUSBA: 300 characters[\s\S]*?no request|Asked for it back with F8 01, the name ending in a NUL: no answer/.test(s.log) && s.asked.join() === 'ZZUSBA' && s.paused === 0 &&
        s.res.routes.A.steps[0].unread === true && s.mock.fds.map(x => x.kind + '/' + x.framing).join() === 'long/old,long/new');
  check('S1 E carries a few lines in the newer framing; D is kept once the mock is told "FD" there, and climbs to 289,813 characters', /^ok:/.test(s.cells.E1) && !('E2' in s.cells) && ok5(s.cells, 'D') && s.mock.fmt === 3);
  check('S1 the result leads with the largest size arriving, names each route that carried it, and says what "FD" did', /^A PROGRAM THE SIZE OF THE BOOK'S LARGEST \(289,813 characters\) WENT TO THIS CALCULATOR AND CAME BACK THE SAME: (old|newer) framing, compressed, \d+ reports; and (old|newer) framing, compressed, \d+ reports\.$/m.test(s.res.text) &&
        /Told "FD" \(long form, new framing\): it answered FD 01 00 00 00 01 03, and then spoke version 03\./.test(s.res.text), s.res.text);
  check('S1 once the newer framing has raised the version, A is tried again in the OLD framing, as on hp-prime-kit\'s G2, and there it is kept, to the largest size; the result says it was the second try',
        /A AGAIN, the old framing, compressed, now that the calculator speaks version 03\./.test(s.log) && ok5(s.cells, 'A') &&
        /A\. Old framing, compressed: came back the same at 300, 8,269, 40,856, 140,000, 289,813 characters \(the last in \d+ reports\), but only at the second try, after the newer framing had raised its version to 03\./.test(s.res.text), s.res.text);
  check('S1 the old framing is asked again at the end and answers; the test\'s programs are off the calculator', s.res.oldAfterNew === true && /Afterwards the old framing was still answered/.test(s.res.text) && Object.keys(s.mock.programs).length === 0 && s.res.left.length === 0 &&
        /The test's programs were taken off the calculator again\.$/.test(s.res.text));
  check('S1 the log shows what the calculator sent: its control report, its acknowledgements with their positions, how each answer began', /\. < a control report: FF EC 00 00 00 00 00 01/.test(s.log) &&
        /\. < acknowledgement: report 01, position 1,015, message \d+/.test(s.log) && /\. < message \d+, 114 bytes, begins FA 01 00 00 00 6C/.test(s.log) && /\. > \d+ more reports of it, numbered 02-/.test(s.log));
  check('S1 ... and never the serial number', !/SECRET/.test(s.log) && !/53 45 43 52/.test(s.log));
  check('S1 nothing but the four test programs was ever sent, and the mock had no error of its own', s.mock.arrived.every(a => a.name === null || /^ZZUSB[CAED]$/.test(a.name)) && !s.mock.error, s.mock.error);
  const S1ms = s.ms;

  // ---------------------------------------------------------------- 2. the same on a G1
  s = await scenario({ product: 0x1541 });
  check('S2 G1 (64-byte reports), the leading reading: C at 254 and 255 reports (7,990 and 8,021 characters); D to 289,813 characters in ' + (s.cells.D5 || '').replace('ok:', ''),
        /^ok:254 reports$/.test(s.cells.C2) && /^ok:255 reports$/.test(s.cells.C3) && ok5(s.cells, 'D') && /7,990, 8,021 characters/.test(s.res.text) && /^ok:2,0\d\d reports$/.test(s.cells.D5), JSON.stringify(s.cells));
  check('S2 the mock stood after 76 reports of its long answers until it was acknowledged, and the log says so once; after that the page acknowledged in time', /the calculator stood until it was acknowledged after 76 reports/.test(s.log) &&
        (s.log.match(/the calculator stood until/g) || []).length === 1 && s.mock.resent === 0 && s.link.learned === 76, (s.log.match(/the calculator stood until/g) || []).length + ' ' + s.mock.resent);

  // ---------------------------------------------------------------- 3. nothing raises the version
  s = await scenario({ fdNew: null });
  check('S3 a calculator no "FD" moves: D is not kept, the person is asked about ZZUSBD too, and the sizes climb NOT compressed in the newer framing, to 289,813 characters in 567 reports',
        /^bad:not read back$/.test(s.cells.D1) && s.asked.join() === 'ZZUSBA,ZZUSBD' && ok5(s.cells, 'E') && /^ok:567 reports$/.test(s.cells.E5) && s.mock.fmt === 1 &&
        /CAME BACK THE SAME: newer framing, not compressed, 567 reports/.test(s.res.text) && /The compressed program was not kept, so the sizes are tried not compressed/.test(s.log), s.res.text);
  check('S3 all four "FD" were sent, the short one of the old framing last of all, and each is in the result', s.mock.fds.map(x => x.kind + '/' + x.framing).join() === 'long/old,long/new,short/new,short/old' && (s.res.text.match(/Told "FD"/g) || []).length === 4 &&
        /A AGAIN, the old framing, compressed: the calculator still speaks version 01, so the short "FD" is tried\./.test(s.log) && /A\. Old framing, compressed: NOT kept/.test(s.res.text) && /The person did not find ZZUSBA/.test(s.res.text));

  s = await scenario({ fdFirst: true });
  check('S3 a calculator that listens to nothing in the newer framing until it is told "FD": who it is and the few lines of E go unanswered first; after "FD" it says who it is, D is kept, E is tried once more and kept, and D climbs to the top',
        s.res.routes.E.steps.length === 2 && s.res.routes.E.steps[0].unread === true && s.res.routes.E.steps[1].ok === true && ok5(s.cells, 'D') && /^ok:/.test(s.cells.E1) &&
        /It did not say who it is in the newer framing/.test(s.log) && /the first time it has said who it is in the newer framing/.test(s.log) && /E once more, now that "FD" has been told:/.test(s.log) && s.asked.join() === 'ZZUSBA', JSON.stringify(s.cells) + s.asked.join());

  // ---------------------------------------------------------------- 4. the old framing takes "FD"
  s = await scenario({ fdOld: 'long' });
  check('S4 a calculator that takes "FD" in the old framing: A is kept and climbs to 289,813 characters there; the person is asked only to press a key', ok5(s.cells, 'A') && s.asked.length === 0 && s.paused === 1 &&
        /A\. Old framing, compressed: came back the same at 300, 8,269, 40,856, 140,000, 289,813 characters/.test(s.res.text) && /The person at the calculator pressed a key and clicked Continue/.test(s.log), JSON.stringify(s.cells));
  s = await scenario({ fdOld: 'long', product: 0x1541 });
  check('S4 the same on a G1: the sizes that would need more than 255 reports are not sent, and the table and the result say how many they would have been',
        /^ok:/.test(s.cells.A1) && /^ok:/.test(s.cells.A2) && [3, 4, 5].every(c => /^skip:[\d,]+ reports: more than the old framing keeps$/.test(s.cells['A' + c])) &&
        /A\. Old framing, compressed: came back the same at 300, 8,269 characters \(the last in \d+ reports\); 40,856, 140,000, 289,813 characters not sent/.test(s.res.text) &&
        s.mock.arrived.filter(a => a.framing === 'old' && a.layout === 'v3').every(a => a.reports <= 255), JSON.stringify(s.cells));
  s = await scenario({ fdOld: 'long', needRelease: 'v3' });
  check('S4 a calculator that keeps a compressed program only when the report "01" follows: found at the few lines, and every later size is sent with one', /^ok:1 report, then a report 01$/.test(s.cells.A1) && ok5(s.cells, 'A') &&
        /with a report "01" after each/.test(s.res.text) && s.mock.releases >= 5, s.cells.A1 + ' ' + s.mock.releases);
  s = await scenario({ fmt: 3 });
  check('S4 a calculator that speaks 03 from the start, as hp-prime-kit\'s did: A is kept with no "FD" sent in the old framing', ok5(s.cells, 'A') && s.mock.fds.filter(x => x.framing === 'old').length === 0 && /It answered with version 03 at the start/.test(s.res.text));

  s = await scenario({ fdOld: 'short', fdNew: null });
  check('S4 a calculator that only the short "FD" of the old framing moves: that is tried last of all, A is then kept there, and the result says which "FD" did it',
        ok5(s.cells, 'A') && /^bad:not read back$/.test(s.cells.D1) && /but only at the second try, after the short "FD" in the old framing\./.test(s.res.text) && s.mock.fds[s.mock.fds.length - 1].kind === 'short' && s.mock.fds[s.mock.fds.length - 1].framing === 'old', s.res.text);

  // ---------------------------------------------------------------- 5. where the old framing stops
  s = await scenario({ maxOld: 254, stallMs: 350, busyMs: 500 });
  check('S5 a calculator that keeps 254 reports and not 255, holding the cable: C2 is OK, C3 fails as "the program sent before", and the log says where the cable stood',
        /^ok:254 reports$/.test(s.cells.C2) && /^bad:came back changed$/.test(s.cells.C3) && /THE CABLE STOOD: 0\.\d s at report 255\./.test(s.log) &&
        /NOT at 130,421 characters \(255 reports\): what came back differs.*it is the program sent before, whole: the new one was not kept/.test(s.res.text), s.res.text.split('\n')[2]);
  check('S5 ... its first request afterwards has no answer, as on the G2; the test asks again, finds the calculator answering, and goes on: D still climbs to the top',
        /try 1 of 3: no answer\./.test(s.log) && !/STOPPED ANSWERING/.test(s.log) && ok5(s.cells, 'D'), JSON.stringify(s.cells));
  s = await scenario({ fdOld: 'long', maxOld: 100, product: 0x1541 });
  check('S5 a calculator whose old framing stops lower still: nothing is sent in it that needs more reports than it has kept (here the first test\'s 10)',
        /^bad:/.test(s.cells.C2) && !('C3' in s.cells) && s.mock.arrived.filter(a => a.framing === 'old' && a.layout === 'v3').every(a => a.reports <= 10) && /^skip:/.test(s.cells.A2), JSON.stringify(s.cells));

  // ---------------------------------------------------------------- 6. no newer framing, and no old one afterwards
  let t0 = Date.now();
  s = await scenario({ v2: false });
  check('S6 a calculator without the newer framing: said after one message, and the rest of that part left out; the old framing still answers', /^bad:not sent$/.test(s.cells.E1) && none(s.cells, 'D') &&
        /The calculator acknowledges nothing in the newer framing, so the rest of this part is left out/.test(s.log) && /D\. Newer framing, compressed: not tried\./.test(s.res.text) && s.res.oldAfterNew === true && s.mock.fds.every(x => x.framing === 'old'), s.res.text);
  s = await scenario({ oldAfterNew: false });
  check('S6 a calculator that no longer answers the old framing once the newer is open: the result says so', s.res.oldAfterNew === false && /Afterwards the old framing was NOT answered/.test(s.res.text) && ok5(s.cells, 'D') && s.res.left.length === 0);

  // ---------------------------------------------------------------- 7. calculators that stop
  s = await scenario({ deadAfter: 9 });
  check('S7 a calculator that stops answering during the old framing: the test ends there, sends nothing more, and names what may still be on it', s.res.alive === false && s.res.gone === false &&
        /THE CALCULATOR HAS STOPPED ANSWERING\. Nothing more will be sent\./.test(s.log) && /THE CALCULATOR STOPPED ANSWERING/.test(s.res.text) && s.res.left.includes('ZZUSBC') && !('E1' in s.cells) && !/deleted \(a request for it now has no answer\)/.test(s.log), s.res.text);
  s = await scenario({ deadAfterNew: 6 });
  check('S7 a calculator that stops answering in the newer framing: that part ends, the old framing is asked, and nothing is called deleted on the strength of silence', s.res.newDead === true && s.res.oldAfterNew === false &&
        !/ZZUSB[ED]: deleted/.test(s.log) && s.res.left.length >= 1 && /STILL ON THE CALCULATOR, or not known to be off it/.test(s.res.text), s.res.text);
  t0 = Date.now();
  s = await scenario({ dieAt: 600 });
  check('S7 a calculator that goes off the cable (it switched itself off on 17 Nov): the test ends at once, in ' + (s.ms / 1000).toFixed(1) + ' s all told, says so, and keeps what it had found',
        s.res.gone === true && /THE CALCULATOR WENT OFF THE CABLE: /.test(s.log) && /THE CALCULATOR WENT OFF THE CABLE before the test ended/.test(s.res.text) && /^ok:/.test(s.cells.C3) && s.res.left.length >= 1 && s.ms < S1ms + 3000, s.ms);
  s = await scenario({ dieAt: 1 });
  check('S7 off the cable before it says who it is: nothing was sent, and the result says that', s.res.gone === true && s.res.info === null && /went off the cable before it said who it is\. Nothing was sent to it\./.test(s.res.text) && s.mock.arrived.length === 0);
  s = await scenario({ deadAfter: 0 });
  check('S7 a calculator that never answers: nothing is sent, and the result asks whether it is on and whether the Kit is closed', s.res.alive === false && s.mock.arrived.length === 0 && /did not answer, so nothing was sent to it/.test(s.res.text) && /Connectivity Kit closed/.test(s.res.text));

  // ---------------------------------------------------------------- 8. what stopped the first page
  s = await scenario({ ackRepeat: 20, fdNew: null });
  check('S8 a calculator that repeats its acknowledgements every 20 ms and keeps no compressed program (17 Nov, where the first page stood still): the test runs to its end, in ' + (s.ms / 1000).toFixed(1) + ' s',
        ok5(s.cells, 'E') && /^bad:not read back$/.test(s.cells.D1) && /RESULT/.test(s.log) && s.ms < 60000 && /\.\.\. and [\d,]+ more of that kind/.test(s.log), s.ms);
  s = await scenario({ ackRepeat: 20, ackEvery: 1, product: 0x1541, fdNew: null }, { budget: 40 });
  const longest = s.log.split('\n').length;
  check('S8 a G1 that acknowledges every single report of 9,201: the log stays a log (' + longest.toLocaleString('en-US') + ' lines), and says what it left out', ok5(s.cells, 'E') && longest < 2500 && /more lines of this kind were left out\)/.test(s.log), longest);

  // ---------------------------------------------------------------- 9. the person, and Stop
  s = await scenario({ silentF8: true, takeV3: true });
  check('S9 a calculator that keeps programs and answers no request (hp-prime-kit\'s G2): nothing is read back, the person finds ZZUSBA in the list, and the result says it WAS kept',
        /^bad:not read back$/.test(s.cells.C1) && /^bad:not read back$/.test(s.cells.A1) && s.asked.includes('ZZUSBA') && /The person saw ZZUSBA in the calculator's list, so it WAS kept, and no request reads it back/.test(s.res.text) &&
        /It was never read back, so the page cannot tell whether it was there \(the person saw it in the list\): please look/.test(s.log) && s.res.left.includes('ZZUSBA'), s.res.text);
  s = await scenario({}, { person: null });
  check('S9 a person who does not answer: the log says "no answer", and the test goes on', /whether ZZUSBA is in its list of programs: no answer\./.test(s.log) && ok5(s.cells, 'D'));
  s = await scenario({}, { stopAt: 30 });
  check('S9 Stop, pressed early: the test ends, says it was stopped, and takes its program off the calculator first', s.res.stopped === true && /STOPPED by the Stop button/.test(s.log) && /The test was stopped before its end/.test(s.res.text) &&
        Object.keys(s.mock.programs).length === 0 && !('D1' in s.cells), s.res.text);
  s = await scenario({ keepOnDelete: true });
  check('S9 a calculator on which the delete does nothing: each program is named as STILL there, once, with how to delete it by hand', s.res.left.slice().sort().join() === 'ZZUSBA,ZZUSBC,ZZUSBD,ZZUSBE' && /ZZUSBC is STILL on the calculator after the delete/.test(s.log) &&
        /STILL ON THE CALCULATOR, or not known to be off it: /.test(s.res.text) && /tap More, then Delete/.test(s.res.text), s.res.left.join());
  s = await scenario({ copies: 3, product: 0x1541 });
  check('S9 a G1 that sends each file three times: every size still reads back the same', ['C1', 'C2', 'C3'].every(k => /^ok:/.test(s.cells[k])) && ok5(s.cells, 'D'), JSON.stringify(s.cells));
  s = await scenario({ crlf: true });
  check('S9 a calculator that hands a program back with other line ends: counted as the same, and the log says once that it differs so', ok5(s.cells, 'D') && (s.log.match(/the same but for its line ends/g) || []).length === 1);
  s = await scenario({ cutAt: 30000 });
  check('S9 a calculator that stores only the first 30,000 characters: the first size past that fails as "differs", with where', /^ok:/.test(s.cells.C1) && /^bad:came back changed$/.test(s.cells.C2) &&
        /what came back differs: 30,000 characters against 129,910 sent, the first difference at character 30,001/.test(s.log), s.cells.C2);

  console.log(`\n${pass} PASS, ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
