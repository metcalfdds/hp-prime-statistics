// test_usb_ladder_v1.js -- the ladder of usb_ladder_v1.js, run against ten pretend calculators, each one a way a real
// one may turn out to be.  Roger Metcalf & Claude, 17 Nov 2026.      node test_usb_ladder_v1.js
//
// NOTHING HERE TOUCHES A CALCULATOR.  What is checked is what the test page will CONCLUDE: that it calls a way good
// only when the program came back the same, stops a way at its first failure, stops altogether when the calculator
// stops answering, asks the person when nothing can be read back, takes its programs off again, and says in plain
// words what happened.  Each pretend calculator is mock_prime_v1.js with one switch thrown.
const fs = require('fs'), path = require('path');
const P = require('../prime_usb_v1.js'), L = require('../usb_ladder_v1.js'), MockPrime = require('./mock_prime_v1.js');

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
const FAST = { probe: 150, first: 1500, then: 1500, gap: 20, tries: 3, settle: 5 };
async function go(mopts, ropts, answers) {
  const mock = new MockPrime(mopts), link = new P.Link(mock.port());
  link.pace.release = 5;
  const lines = [], cells = {}, asked = [];
  const ui = { log: s => lines.push(s), cell: (w, s, st, tx) => { cells[w + s] = st + ':' + tx; },
               ask: async (way, st) => { asked.push(way.key + st.step); return answers ? !!answers[way.key + st.step] : false; },
               stop: () => !!(ropts && ropts.stopAfter && lines.length > ropts.stopAfter) };
  const res = await L.run(link, ui, Object.assign({ core: P, t: FAST }, ropts || {}));
  return { mock, res, lines, cells, asked, text: lines.join('\n') };
}
const bests = r => Object.keys(r.res.ways).map(k => k + ':' + r.res.ways[k].best).join(' ');
const okLine = l => l.startsWith('//') || /^(EXPORT ZZUSB[A-D]\(\)|BEGIN| RETURN \d;|END;)$/.test(l);

(async () => {
  // ---- the test programs themselves
  const sizes = fs.readdirSync(path.join(__dirname, '..', '..', '..', 'programs')).filter(f => /\.txt$/.test(f))
    .map(f => ({ f, n: P.normalizeSource(fs.readFileSync(path.join(__dirname, '..', '..', '..', 'programs', f), 'utf8')).length })).sort((a, b) => a.n - b.n);
  check('P1 step 3 is the size of the book\'s smallest program and step 5 of its largest, counted in programs/ now',
        L.STEPS[2].chars === sizes[0].n && /^DataLoad_/.test(sizes[0].f) && L.STEPS[4].chars === sizes[sizes.length - 1].n && /^EpiStats_/.test(sizes[sizes.length - 1].f),
        sizes[0].f + ' ' + sizes[0].n + '; ' + sizes[sizes.length - 1].f + ' ' + sizes[sizes.length - 1].n);
  let shape = true, lens = true;
  for (const w of L.WAYS) for (const st of L.STEPS) { const s = L.makeProgram(w.name, st.step, st.chars); lens = lens && s.length === st.chars; shape = shape && s.split('\n').every(okLine) && s.endsWith('\nEXPORT ' + w.name + '()\nBEGIN\n RETURN ' + st.step + ';\nEND;'); }
  check('P2 every test program has exactly the characters its step names', lens);
  check('P3 every line of every test program is a comment or one of the function\'s four lines, and the function comes last', shape);
  let odd = 0;
  for (let c = 140; c < 4000; c++) { const s = L.makeProgram('ZZUSBB', 2, c); if (s.length !== c || !s.split('\n').every(okLine)) odd++; }
  check('P4 ... and so at every length from 140 to 3,999 characters (a cut never leaves half a comment mark)', odd === 0, odd);
  check('P5 the same program every time, and a different one for each way and step', L.makeProgram('ZZUSBA', 3, 40856) === L.makeProgram('ZZUSBA', 3, 40856) &&
        L.makeProgram('ZZUSBA', 3, 40856) !== L.makeProgram('ZZUSBB', 3, 40856) && L.makeProgram('ZZUSBA', 2, 8269).slice(100, 400) !== L.makeProgram('ZZUSBA', 3, 40856).slice(100, 400));
  check('P6 the test programs are plain ASCII, and their names are ones the calculator takes', L.WAYS.every(w => P.validName(w.name)) && /^[\x0a\x20-\x7e]+$/.test(L.makeProgram('ZZUSBD', 4, 140000)));
  const n5 = P.framesLegacy(await P.programV3('ZZUSBA', L.makeProgram('ZZUSBA', 5, 289813)), 1023).length;
  check('P7 the largest test program takes ' + n5 + ' reports compressed: more than any program of the book (101), under the 254 where the numbers wrap', n5 > 101 && n5 < 254, n5);

  // ---- 1. a calculator that does everything the descriptions say
  let r = await go();
  check('S1 everything works: all four ways reach 289,813 characters', bests(r) === 'A:289813 B:289813 C:289813 D:289813', bests(r));
  check('S1 the two requests with a NUL are tried on way A step 1, the one kept is the one that brings the program back compressed (F8 03), and no request without a NUL is sent to a calculator that has answered', r.res.reader.key === 2 && r.res.readerNew.key === 2 &&
        /F8 01, the name ending in a NUL: the same program came back \(1 report, not compressed, reply version 01; it began F7 01 00 00 02 68 06 0C/.test(r.text) && !/no NUL:/.test(r.text) && /This calculator answers F8 03, the name ending in a NUL/.test(r.text), r.text.split('\n').filter(l => /Asked for it back/.test(l)).slice(0, 2).join(' | '));
  check('S1 every cell ends green with its report count', ['A', 'B', 'C', 'D'].every(k => [1, 2, 3, 4, 5].every(s => /^ok:\d+ reports?$/.test(r.cells[k + s]))), JSON.stringify(r.cells));
  check('S1 way C\'s largest went in 567 reports and came back, compressed, in fewer than 140', /Sent 579,6\d\d bytes in 567 reports, \d+\.\d\d s on the cable/.test(r.text) && /Read back the same: 1[0-3]\d reports, compressed, reply version 03/.test(r.text));
  check('S1 the four test programs are gone from the mock, and the result says so', Object.keys(r.mock.programs).length === 0 && r.res.left.length === 0 && /The test programs were deleted from the calculator again/.test(r.res.text));
  check('S1 the result names the four ways and says "read back the same"', /arrived whole when it was sent compressed, with the report 01 after it \(way A, read back the same\); and when sent compressed, nothing after it \(way B, read back the same\); and when sent not compressed \(way C/.test(r.res.text) && /way D, read back the same/.test(r.res.text), r.res.text);
  check('S1 nobody was asked anything, and the serial number is nowhere in the log', r.asked.length === 0 && !/SECRET/.test(r.text));
  check('S1 the old framing\'s three test programs are taken off in the old framing, before the newer one is asked for; way D\'s after it', r.text.indexOf('TAKING ZZUSBA, ZZUSBB, ZZUSBC OFF AGAIN') > 0 &&
        r.text.indexOf('TAKING ZZUSBA, ZZUSBB, ZZUSBC OFF AGAIN') < r.text.indexOf('THE NEWER FRAMING') && r.text.indexOf('THE NEWER FRAMING') < r.text.indexOf('TAKING ZZUSBD OFF AGAIN'));
  check('S1 the mock saw nothing but the four test names', r.mock.arrived.every(a => /^ZZUSB[A-D]$/.test(a.name)) && r.mock.arrived.length === 20, r.mock.arrived.length);

  // ---- 2. hp-prime-kit's G2: programs arrive, and no request for one is ever answered
  r = await go({ silentF8: true }, null, { A1: true, B1: true, C1: true, A3: true, A5: true, D1: false });
  check('S2 nothing can be read back: the page says so and asks the person, about step 1 of A, B and C, then A at steps 3 and 5 only, then D once',
        r.res.blind === true && JSON.stringify(r.asked) === '["A1","B1","C1","A3","A5","D1"]', JSON.stringify(r.asked));
  check('S2 way A is good by eye to the largest size; B and C stand at step 1; D, which the person did not see, is not good', bests(r) === 'A:289813 B:300 C:300 D:0', bests(r));
  check('S2 the result says "checked by eye", that nothing could be read back, and which programs to delete by hand',
        /way A, checked by eye/.test(r.res.text) && /answered none of the four requests/.test(r.res.text) && /To delete by hand, if they are there .*ZZUSBA, ZZUSBB, ZZUSBC, ZZUSBD/.test(r.res.text), r.res.text);
  r = await go({ silentF8: true }, null, {});
  check('S2b the same calculator and a person who sees nothing: no way is called good', bests(r) === 'A:0 B:0 C:0 D:0' && !/arrived whole/.test(r.res.text));

  // ---- 3. a calculator that drops a long message without a word (G1 firmware, as hp-prime-web reports it)
  r = await go({ maxMessage: 16000 });
  check('S3 messages over 16,000 bytes dropped: compressed ways stop after 8,269 characters, the uncompressed way after 300', bests(r) === 'A:8269 B:8269 C:300 D:8269', bests(r));
  check('S3 the failure is named: what came back was the step before, whole', /Way A \(compressed, with the report 01 after it\) worked up to 8,269 characters and failed at 40,856: what came back differs: 8,269 characters against 40,856 sent, the first difference at character 42 \(it is the program of the step before, whole: the new one was not kept\)/.test(r.res.text), r.res.text);
  check('S3 no way was pushed past its first failure', r.mock.arrived.length === 3 + 3 + 2 + 3, r.mock.arrived.length);
  check('S3 the cells: green, green, red, and nothing after', /^ok/.test(r.cells.A2) && /^bad:came back changed/.test(r.cells.A3) && r.cells.A4 === undefined);

  // ---- 4. a calculator that keeps a program only when the report 01 follows
  r = await go({ needRelease: true });
  check('S4 only the way that sends the report 01 works in the old framing', bests(r) === 'A:289813 B:0 C:0 D:289813', bests(r));
  check('S4 ... and B and C are named as failing at the smallest program', /Way B \(compressed, nothing after it\) did not work for the smallest program: no answer/.test(r.res.text) && /Way C \(not compressed\) did not work/.test(r.res.text), r.res.text);

  // ---- 5. a calculator that takes only the older layout
  r = await go({ takeV3: false });
  check('S5 only the uncompressed way works, and the reader is found on it, not given up for lost after way A', bests(r) === 'A:0 B:0 C:289813 D:0' && r.res.blind === false && r.res.reader.key === 2, bests(r));
  check('S5 ways A and B were asked for again once the reader was known, and still did not come back', (r.text.match(/asked for again with F8 03, the name ending in a NUL: no answer/g) || []).length === 2);

  // ---- 6. a calculator that hangs
  r = await go({ deadAfter: 9 });
  check('S6 the calculator stops answering: the test stops, nothing more is sent, and the result says what to do', r.res.alive === false && /THE CALCULATOR HAS STOPPED ANSWERING/.test(r.text) &&
        /stopped answering during the test\. Unplug the cable/.test(r.res.text) && /paperclip/.test(r.res.text) && r.res.ways.D.tried === false, r.res.text);
  const sentAfter = r.mock.reportsIn;
  check('S6 ... and the programs it may hold are listed for deleting by hand', /To delete by hand/.test(r.res.text) && r.res.left.length >= 1);
  r = await go({ deadAfter: 0 });
  check('S6b a calculator that never answers: nothing is sent, and the result asks about the power and the Connectivity Kit', r.res.alive === false && r.mock.arrived.length === 0 &&
        /did not answer, so nothing was sent/.test(r.res.text) && /Connectivity Kit closed/.test(r.res.text));

  // ---- 7. no newer framing
  r = await go({ v2: false });
  check('S7 a calculator without the newer framing: A, B, C good, D not sent, named', bests(r) === 'A:289813 B:289813 C:289813 D:0' && /Way D .* did not work for the smallest program: not sent: no acknowledgement/.test(r.res.text), r.res.text);
  check('S7 ... and silence in the newer framing is not taken for a dead calculator: the old framing is asked, it answers, and the test ends as usual', r.res.alive === true && r.res.v2gone === true &&
        /No answer in the newer framing; the calculator still answers in the old one/.test(r.text) && !/STOPPED ANSWERING/.test(r.text) && Object.keys(r.mock.programs).length === 0);

  // ---- 8. a damaged transfer
  r = await go({ cutAt: 100000 });
  check('S8 a program cut to 100,000 characters on the calculator: good to 40,856, and the difference is placed', bests(r) === 'A:40856 B:40856 C:40856 D:40856' &&
        /100,000 characters against 140,000 sent, the first difference at character 100,001/.test(r.res.text), r.res.text);

  // ---- 8b. a calculator that answers only the older request, not compressed
  r = await go({ readVers: [1] });
  check('S8b only F8 01 is answered: old-framing ways are good, their long programs read back in 567 reports whose numbers are logged', r.res.reader.key === 1 && bests(r).startsWith('A:289813 B:289813 C:289813') &&
        /Read back the same: 567 reports, not compressed, reply version 01, numbered 00-FE,00-FE,00-38/.test(r.text), bests(r));
  check('S8b ... and in the newer framing, where a reply that long does not fit one message, way D stops at 40,856 with the reason', r.res.ways.D.best === 40856 && /Way D .* worked up to 40,856 characters and failed at 140,000: no answer/.test(r.res.text), r.res.text);
  r = await go({ keepOnDelete: true }, { ways: ['A'], maxStep: 2 });
  check('S8c a delete that does nothing: the program is found still there, and the result lists it', r.res.left.join() === 'ZZUSBA' && /ZZUSBA is STILL on the calculator after the delete/.test(r.text) && /To delete by hand, if they are there .*: ZZUSBA\./.test(r.res.text), r.res.text);

  // ---- 8d. a calculator that takes at most 253 reports a message (what the G1's 15,928 bytes comes to)
  r = await go({ maxReports: 253 });
  check('S8d at most 253 reports a message: every compressed way reaches the largest size, and the uncompressed way stops at 40,856 (its next step is 274 reports)',
        bests(r) === 'A:289813 B:289813 C:40856 D:289813' && /Way C \(not compressed\) worked up to 40,856 characters and failed at 140,000/.test(r.res.text), bests(r));

  // ---- 8e. a calculator that hands the text back with other line ends
  r = await go({ crlf: true }, { ways: ['A', 'D'], maxStep: 3 });
  check('S8e CR LF line ends and a last newline on what comes back: still the same program, said once in the log', bests(r) === 'A:40856 D:40856' &&
        (r.text.match(/the same but for its line ends or a last newline/g) || []).length === 1, bests(r));

  // ---- 8f. a calculator that answers a request only when its name has NO NUL after it
  r = await go({ needNul: 'never' }, { ways: ['A'], maxStep: 2 });
  check('S8f neither request with a NUL is answered: only then are the two without one tried, the first that answers is kept, and the other is not sent',
        r.res.reader.key === 3 && bests(r) === 'A:8269' && /F8 03, the name ending in a NUL: no answer/.test(r.text) && /F8 01, no NUL: the same program came back/.test(r.text) && !/F8 03, no NUL/.test(r.text), r.text.split('\n').filter(l => /Asked for it back/.test(l)).join(' | '));

  // ---- 9. the Stop button
  r = await go({}, { stopAfter: 14 });
  check('S9 Stop: the test ends early, says so, and still takes its programs off', r.res.stopped === true && /STOPPED by the Stop button/.test(r.text) && /stopped before its end/.test(r.res.text) &&
        Object.keys(r.mock.programs).length === 0, Object.keys(r.mock.programs));

  // ---- 10. a G1's small reports, and chosen ways
  r = await go({ product: 0x1541 }, { ways: ['A'], maxStep: 3 });
  check('S10 64-byte reports, way A only, three steps: good to 40,856, in ' + (r.res.ways.A.steps[2] || {}).reports + ' reports', bests(r) === 'A:40856' && r.res.ways.A.steps[2].reports > 250, bests(r));
  check('S10 ... and the result does not call 40,856 "the size of our largest program"', /A test program of 40,856 characters arrived whole/.test(r.res.text) && !/largest/.test(r.res.text), r.res.text);

  console.log(`\n${pass} PASS, ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
