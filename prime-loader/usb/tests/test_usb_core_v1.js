// test_usb_core_v1.js -- prime_usb_v1.js against hp-prime-kit's own code, against the byte examples its sources
// publish, and against the mock calculator.  Roger Metcalf & Claude, 17 Nov 2026.
//
//     python3 kit_reference_v1.py REF      (writes hp-prime-kit's message for every program in programs/)
//     node test_usb_core_v1.js REF
//
// NOTHING HERE TOUCHES A CALCULATOR.  A pass says three things and no more:
//   A  the messages are, byte for byte, the ones hp-prime-kit builds (whose layout was read from a G2's own message),
//      and the ones hp-prime-web's tests expect (the older layout, the request, the delete);
//   B  the reports are cut the way each description says, at the sizes ours need (129 reports, 567 with the wrap);
//   C  a Link and the mock calculator, which was written apart from it, agree on a whole session: identify, send in
//      each layout and framing, read back, delete; and each way the mock can fail is seen and named, never passed
//      over as a success.
const fs = require('fs'), path = require('path'), crypto = require('crypto'), zlib = require('zlib');
const P = require('../prime_usb_v1.js'), MockPrime = require('./mock_prime_v1.js');

const REF = path.resolve(process.argv[2]);
const ref = JSON.parse(fs.readFileSync(path.join(REF, 'reference.json'), 'utf8'));
const PROGRAMS = path.join(__dirname, '..', '..', '..', 'programs');
const KIT = process.env.HPKIT || '/tmp/kit/hp-prime-kit-HEAD';
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const bytes = s => Uint8Array.from(s.trim().split(/\s+/).map(h => parseInt(h, 16)));
const same = (a, b) => a.length === b.length && Buffer.from(a).equals(Buffer.from(b));
const src = r => P.normalizeSource(fs.readFileSync(r.name === 'SELFTEST' ? path.join(KIT, 'examples', 'selftest', 'SELFTEST.txt') : path.join(PROGRAMS, r.file), 'utf8'));

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
const quick = link => { link.pace.release = 5; return link; };

(async () => {
  // ---------------------------------------------------------------- A. the messages
  check('A1 the checksum is CRC-16/XMODEM: "123456789" gives 31C3', P.crc16(Buffer.from('123456789')) === 0x31C3);
  // hp-prime-web, tests/protocol.test.ts (MIT): its three byte examples of the older layout
  const EB = 'EB 01 00 00 00 14 06 10 66 C9 5A 00 5A 00 54 00 5F 00 54 00 45 00 53 00 54 00';
  const F7 = 'F7 01 00 00 00 34 06 04 BC 43 48 00 49 00 45 00 58 00 50 00 4F 00 52 00 54 00 20 00 48 00 49 00 28 00 29 00 0A 00 42 00 45 00 47 00 49 00 4E 00 0A 00 45 00 4E 00 44 00 3B 00';
  const F8 = 'F8 01 00 00 00 0A 06 06 4A 49 48 00 49 00 00 00';
  check('A2 delete "ZZT_TEST" is hp-prime-web\'s example, byte for byte', same(P.deleteMessage('ZZT_TEST', 1), bytes(EB)), P.hex(P.deleteMessage('ZZT_TEST', 1)));
  check('A3 the older layout of a program is hp-prime-web\'s example, byte for byte', same(P.programV1('HI', 'EXPORT HI()\nBEGIN\nEND;'), bytes(F7)), P.hex(P.programV1('HI', 'EXPORT HI()\nBEGIN\nEND;')));
  check('A4 a request for "HI", its name ending in a NUL, is hp-prime-web\'s example, byte for byte', same(P.requestMessage('HI', 1, true), bytes(F8)), P.hex(P.requestMessage('HI', 1, true)));
  // hp-prime-kit, docs/topics/usb.md, usb.file-request: the bytes it sent a G2 (no NUL), 00 being the report's number
  check('A5 a request for "SELFTEST" in version 03 with no NUL begins as hp-prime-kit\'s did: F8 03 00 00 00 14 06 10 91 6E',
        P.hex(P.requestMessage('SELFTEST', 3, false), 10) === 'F8 03 00 00 00 14 06 10 91 6E ...', P.hex(P.requestMessage('SELFTEST', 3, false), 10));
  // hp-prime-kit, usb.program-message: SELFTEST as a G2 itself sent it held 2,304 bytes uncompressed, beginning 06 10 98 D2
  const st = ref.find(r => r.name === 'SELFTEST'), stInner = P.innerV3('SELFTEST', src(st));
  check('A6 SELFTEST\'s uncompressed part is 2,304 bytes beginning 06 10 98 D2, as a G2 sent it (hp-prime-kit)', stInner.length === 2304 && P.hex(stInner, 4) === '06 10 98 D2 ...', stInner.length + ' ' + P.hex(stInner, 4));
  const stMsg = await P.programV3('SELFTEST', src(st));
  check('A7 its message begins F7 03, the stream\'s length plus 4, then 00 09 00 00 and a zlib stream (78)',
        stMsg[0] === 0xF7 && stMsg[1] === 3 && P.rdU32be(stMsg, 2) === stMsg.length - 6 && P.hex(stMsg.subarray(6, 11)) === '00 09 00 00 78', P.hex(stMsg, 12));

  // every program of the book, against the kit's own message
  let innerOk = 0, lenOk = 0, frameOk = 0, roundOk = 0, v1Ok = 0, minR = 1e9, maxR = 0, minRaw = 1e9, maxRaw = 0, minK = 1e9, maxK = 0, total = 0, past = 0;
  const bad = [];
  const progs = ref.filter(r => r.name !== 'SELFTEST');
  for (const r of progs) {
    const s = src(r), inner = P.innerV3(r.name, s), kit = new Uint8Array(fs.readFileSync(path.join(REF, r.name + '.msg')));
    if (s.length === r.chars && inner.length === r.inner_len && sha(inner) === r.inner_sha) innerOk++; else bad.push(r.name + ' inner');
    const msg = await P.programV3(r.name, s);
    const back = zlib.inflateSync(Buffer.from(msg.subarray(10)));
    if (P.rdU32be(msg, 2) === msg.length - 6 && P.rdU32le(msg, 6) === inner.length && sha(back) === r.inner_sha) lenOk++; else bad.push(r.name + ' message');
    const kf = P.framesLegacy(kit, 1023);
    if (kf.length === r.reports && sha(Buffer.concat(kf.map(f => Buffer.from(f)))) === r.reports_sha) frameOk++; else bad.push(r.name + ' frames');
    const f = await P.parseFile(kit);                       // the kit's message, read as if a calculator had sent it
    if (f.name === r.name && f.text === s && f.compressed && f.crcOk && f.lengthOk && f.type === 6) roundOk++; else bad.push(r.name + ' parse');
    const v1 = P.programV1(r.name, s), g = await P.parseFile(v1);
    if (g.name === r.name && g.text === s && !g.compressed && g.crcOk && g.lengthOk) v1Ok++; else bad.push(r.name + ' v1');
    const mine = P.framesLegacy(msg, 1023).length, raw = P.framesLegacy(v1, 1023).length;
    minR = Math.min(minR, mine); maxR = Math.max(maxR, mine); minRaw = Math.min(minRaw, raw); maxRaw = Math.max(maxRaw, raw);
    minK = Math.min(minK, r.reports); maxK = Math.max(maxK, r.reports); total += msg.length; if (raw > 254) past++;
  }
  check('A8 all ' + progs.length + ' programs: the uncompressed part is hp-prime-kit\'s, byte for byte (SHA-256), checksum included', innerOk === progs.length, bad);
  check('A9 all ' + progs.length + ': the message\'s two lengths are right and its stream unpacks to that part', lenOk === progs.length, bad);
  check('A10 all ' + progs.length + ': hp-prime-kit\'s message is cut into hp-prime-kit\'s reports, byte for byte', frameOk === progs.length, bad);
  check('A11 all ' + progs.length + ': hp-prime-kit\'s message reads back to the program\'s name and source, checksum good', roundOk === progs.length, bad);
  check('A12 all ' + progs.length + ': the older layout reads back to the same name and source', v1Ok === progs.length, bad);
  console.log('     reports a program: compressed by this browser\'s zlib ' + minR + ' to ' + maxR + ' (hp-prime-kit\'s level 1: ' + minK + ' to ' + maxK + '); not compressed ' + minRaw + ' to ' + maxRaw +
              '; all ' + progs.length + ' compressed: ' + total.toLocaleString('en-US') + ' bytes; not compressed, ' + past + ' of the ' + progs.length + ' take more than 254 reports');
  check('A13 no program needs more than 254 reports compressed, so none reaches the sequence number\'s wrap', maxR <= 254 && maxK <= 254, maxR);
  check('A14 every program fits one message of the newer framing (' + P.V2_MAX.toLocaleString('en-US') + ' bytes)', progs.every(r => fs.statSync(path.join(REF, r.name + '.msg')).size <= P.V2_MAX));
  check('A15 normalizeSource: CRLF and CR become LF, and one newline at the end is dropped (hp-prime-kit\'s rule)',
        P.normalizeSource('a\r\nb\rc\n') === 'a\nb\nc' && P.normalizeSource('a\n\n') === 'a\n' && P.normalizeSource('a') === 'a');
  check('A16 names: letters, digits and "_", a letter or "_" first', P.validName('TTestLabG') && P.validName('_x1') && !P.validName('1abc') && !P.validName('a b') && !P.validName('') && !P.validName('a-b'));

  // ---------------------------------------------------------------- B. the framing
  const big = new Uint8Array(1023 * 300 + 7).map((_, i) => (i * 7 + 3) & 255), fr = P.framesLegacy(big, 1023);
  check('B1 old framing: 301 reports, numbered 00 to FE and then 00 again, never FF',
        fr.length === 301 && fr[0][0] === 0 && fr[254][0] === 0xFE && fr[255][0] === 0x00 && fr[300][0] === 45 && fr.every(f => f[0] !== 0xFF), P.runs(fr.map(f => f[0])));
  check('B2 old framing: the pieces put together are the message', same(Buffer.concat(fr.map(f => Buffer.from(f.subarray(1)))), big) && fr[300].length === 8);
  check('B3 old framing: a one-byte message is one report of two bytes', P.framesLegacy(Uint8Array.of(0xFA), 1023).length === 1 && P.hex(P.framesLegacy(Uint8Array.of(0xFA), 1023)[0]) === '00 FA');
  const m2 = big.subarray(0, 5000), f2 = P.framesV2(m2, 7, 1023);
  check('B4 newer framing: 01, the message number and the size low byte first, then 1,015 bytes; then 02, 03 ... with 1,023',
        f2.length === 5 && P.hex(f2[0], 9) === '01 07 00 00 00 88 13 00 00 ...' && f2[0].length === 1024 && f2[1][0] === 2 && f2[1].length === 1024 && f2[4][0] === 5 &&
        same(Buffer.concat([Buffer.from(f2[0].subarray(9))].concat(f2.slice(1).map(f => Buffer.from(f.subarray(1))))), m2), P.hex(f2[0], 9));
  let threw = false;
  try { P.framesV2(new Uint8Array(P.V2_MAX + 1), 1, 1023); } catch (e) { threw = /carries/.test(e.message); }
  check('B5 newer framing: a message over its limit is refused before anything is sent', threw && P.framesV2(new Uint8Array(P.V2_MAX), 1, 1023).length === 240);
  check('B6 an acknowledgement is FE 01, the report, 00, the position, the message number', P.hex(P.ackV2(5, 5000, 7, true)) === 'FE 01 05 00 88 13 00 00 07 00 00 00');
  check('B7 a G1\'s 64-byte reports: 63 bytes a report', P.framesLegacy(big.subarray(0, 200), 63).length === 4 && P.framesLegacy(big.subarray(0, 200), 63)[3].length === 12);

  // ---------------------------------------------------------------- C. a Link and the mock calculator
  const notes = [];
  const session = opts => { const mock = new MockPrime(opts); const link = quick(new P.Link(mock.port(), t => notes.push(t))); return { mock, link }; };
  const tiny = 'EXPORT ZZT()\nBEGIN\n RETURN 1;\nEND;';
  const dl = progs.find(r => r.name === 'DataLoad'), epi = progs.find(r => r.name === 'EpiStats');
  const DL = src(dl), EPI = src(epi);

  let { mock, link } = session();
  const info = await link.info();
  check('C1 identify: build 15515, the version text, 108 bytes, reply version 03', info.build === 15515 && info.version === 'V2.060.650' && info.bytes === 108 && info.ver === 3, JSON.stringify(info));
  check('C2 the serial number is nowhere in what identify returns', !JSON.stringify(info).includes('SECRET'));
  check('C3 ready: the calculator says Y', await link.ready() === true);
  let out = await link.sendProgram('ZZT', tiny, { layout: 'v3', release: true });
  check('C4 a small program, compressed, with the report 01 after it: one report, kept, and one 01 seen', out.reports === 1 && mock.programs.ZZT === tiny && mock.releases === 1 && mock.arrived[0].layout === 'v3', JSON.stringify(mock.arrived));
  let f = await link.readProgram('ZZT', { ver: 1, nul: true });
  check('C5 read back with F8 01 and a NUL: the same text, not compressed, checksum good', !!f && f.text === tiny && !f.compressed && f.crcOk, f && f.text);
  f = await link.readProgram('ZZT', { ver: 3, nul: true });
  check('C6 read back with F8 03 and a NUL: the same text, compressed, checksum good', !!f && f.text === tiny && f.compressed && f.crcOk);
  f = await link.readProgram('ZZT', { ver: 3, nul: false, first: 300 });
  check('C7 with no NUL after the name the mock stays silent, and that is reported as no answer, not as a failure to parse', f === null);
  f = await link.readProgram('NOTTHERE', { ver: 1, nul: true, first: 300 });
  check('C8 a program that is not there: silence, reported as no answer', f === null);
  out = await link.sendProgram('DataLoad', DL, { layout: 'v3' });
  f = await link.readProgram('DataLoad', { ver: 3 });
  check('C9 DataLoad (' + DL.length.toLocaleString('en-US') + ' characters): ' + out.reports + ' reports compressed; read back the same', mock.programs.DataLoad === DL && !!f && f.text === DL && out.reports >= 15 && out.reports <= 25, out.reports);
  out = await link.sendProgram('EpiStats', EPI, { layout: 'v3' });
  f = await link.readProgram('EpiStats', { ver: 3 });
  check('C10 EpiStats (' + EPI.length.toLocaleString('en-US') + ' characters): ' + out.reports + ' reports compressed; read back the same in ' + (f && f.reports) + ' reports', mock.programs.EpiStats === EPI && !!f && f.text === EPI && out.reports > 90 && out.reports < 140, out.reports);
  out = await link.sendProgram('EpiStats', EPI, { layout: 'v1', release: false });
  check('C11 EpiStats not compressed: ' + out.reports + ' reports, past the wrap, and the mock put them together', out.reports === 567 && mock.arrived[mock.arrived.length - 1].kept && mock.arrived[mock.arrived.length - 1].layout === 'v1' && mock.programs.EpiStats === EPI, out.reports);
  f = await link.readProgram('EpiStats', { ver: 1, first: 8000 });
  check('C12 read back not compressed: 567 reports whose numbers ran 00-FE,00-FE,00-38, and the same text', !!f && f.text === EPI && f.reports === 567 && f.firsts === '00-FE,00-FE,00-38', f && f.firsts);
  await link.deleteProgram('ZZT');
  f = await link.readProgram('ZZT', { ver: 1, first: 300 });
  check('C13 delete: the program is gone from the mock, and a request for it is met with silence', !('ZZT' in mock.programs) && f === null);

  // the newer framing
  ({ mock, link } = session());
  await link.info();
  await link.openV2();
  out = await link.sendProgram('ZZC', tiny, { layout: 'v3' });
  check('C14 newer framing: the mock opened it, took the program, and acknowledged it', mock.v2open && mock.programs.ZZC === tiny && mock.arrived[0].framing === 'new' && out.reports === 1);
  f = await link.readProgram('ZZC', { ver: 3 });
  check('C15 newer framing: read back the same, and the answer was acknowledged with its size and number', !!f && f.text === tiny && mock.hostAcks.length === 1 && mock.hostAcks[0].ok === 1 && mock.hostAcks[0].id === 1 && mock.hostAcks[0].pos === f.bytes, JSON.stringify(mock.hostAcks));
  out = await link.sendProgram('EpiStats', EPI, { layout: 'v3' });
  f = await link.readProgram('EpiStats', { ver: 3 });
  check('C16 newer framing: EpiStats in ' + out.reports + ' reports, read back the same', mock.programs.EpiStats === EPI && !!f && f.text === EPI);
  const i2 = await link.info();
  check('C17 newer framing: identify still answers', i2.build === 15515);
  ({ mock, link } = session({ nackOnce: 40 }));
  await link.openV2();
  out = await link.sendProgram('EpiStats', EPI, { layout: 'v3' });
  check('C18 newer framing: asked for report 40 again, the Link sends from there and the program arrives whole', mock.nacked === true && mock.programs.EpiStats === EPI && notes.length >= 0);
  // a message of the newer framing that the calculator sends a second time (our acknowledgement missed), by a port
  // whose reports are queued by hand
  {
    const q = [], sent = [], pad = f => { const r = new Uint8Array(1024); r.set(f); return r; };
    const sp = { reportSize: 1024, send: async f => { sent.push(Uint8Array.from(f)); }, read: async () => (q.length ? q.shift() : null), poll: () => null, drain: () => 0 };
    const lk = new P.Link(sp);
    lk.v2 = true;
    const m1 = await P.programV3('AAA', DL), m2 = await P.programV3('BBB', tiny);
    P.framesV2(m1, 7, 1023).forEach(f => q.push(pad(f)));
    const r1 = await lk.recvV2([0xF7], 300, 300);
    P.framesV2(m1, 7, 1023).forEach(f => q.push(pad(f)));          // message 7 again, all its reports
    P.framesV2(m2, 8, 1023).forEach(f => q.push(pad(f)));
    const r2 = await lk.recvV2([0xF7], 300, 300), g1 = await P.parseFile(r1), g2 = await P.parseFile(r2);
    check('C18b newer framing: a message the calculator sends a second time is acknowledged again and passed over, never taken for the next answer',
          g1.name === 'AAA' && g1.text === DL && g2.name === 'BBB' && g2.text === tiny && sent.length === 3 && sent.every(a => a[0] === 0xFE && a[1] === 1) &&
          sent.map(a => P.rdU32le(a, 8)).join() === '7,7,8' && P.rdU32le(sent[0], 4) === m1.length, sent.map(a => P.hex(a)).join(' | '));
  }
  ({ mock, link } = session({ v2: false }));
  await link.openV2();
  let err = null;
  try { await link.sendV2(Uint8Array.of(0xFA), 400); } catch (e) { err = e; }
  check('C19 a calculator without the newer framing: no acknowledgement, named as such', err instanceof P.Silent && /no acknowledgement/.test(err.message), err && err.message);

  // the ways it can go wrong
  ({ mock, link } = session({ maxMessage: 16000 }));
  out = await link.sendProgram('DataLoad', DL, { layout: 'v3' });
  f = await link.readProgram('DataLoad', { ver: 1, first: 300 });
  check('C20 a calculator that drops long messages without a word (G1 firmware): the send looks the same, and the read-back finds nothing', out.reports > 15 && !('DataLoad' in mock.programs) && f === null);
  ({ mock, link } = session({ cutAt: 30000 }));
  await link.sendProgram('DataLoad', DL, { layout: 'v3' });
  f = await link.readProgram('DataLoad', { ver: 3 });
  check('C21 a program cut short on the calculator: the read-back differs from what was sent', !!f && f.text !== DL && f.text.length === 30000);
  ({ mock, link } = session({ silentF8: true }));
  await link.sendProgram('ZZT', tiny, {});
  f = await link.readProgram('ZZT', { ver: 1, first: 300 });
  check('C22 a calculator that never answers a request (hp-prime-kit\'s G2): no answer, though the program is there', f === null && mock.programs.ZZT === tiny);
  ({ mock, link } = session({ needRelease: true }));
  await link.sendProgram('ZZT', tiny, { release: false });
  const before = 'ZZT' in mock.programs;
  await link.sendProgram('ZZT', tiny, { release: true });
  check('C23 a calculator that keeps a program only when the report 01 follows: not kept without it, kept with it', before === false && mock.programs.ZZT === tiny);
  ({ mock, link } = session({ wrap: 'early' }));
  await link.sendProgram('EpiStats', EPI, { layout: 'v3' });
  f = await link.readProgram('EpiStats', { ver: 1, first: 8000 });
  check('C24 a calculator whose long reply counts FD, 00 (keeping FE for itself): still put together, and its numbers are in the log line', !!f && f.text === EPI && f.firsts === '00-FD,00-FD,00-3A', f && f.firsts);
  ({ mock, link } = session({ deadAfter: 1 }));
  await link.info();
  err = null;
  try { await link.info(400); } catch (e) { err = e; }
  check('C25 a calculator that stops answering: "no answer within 0.4 s"', err instanceof P.Silent && /no answer within 0.4 s/.test(err.message), err && err.message);
  ({ mock, link } = session());
  await link.sendProgram('EpiStats', EPI, { layout: 'v3' });
  const p0 = link.port.read;
  let nth = 0;
  link.port.read = ms => p0(ms).then(r => (r && ++nth === 5) ? p0(ms) : r);          // one report of the reply is lost
  err = null;
  try { await link.readProgram('EpiStats', { ver: 3, first: 2000, then: 300 }); } catch (e) { err = e; }
  check('C26 a reply with a report missing: "out of order", with where it stopped', err instanceof P.Cut && /out of order: report 5 where 4 was next/.test(err.message), err && err.message);
  link.port.read = p0;
  ({ mock, link } = session({ takeV3: false }));
  await link.sendProgram('ZZT', tiny, { layout: 'v3' });
  const no3 = !('ZZT' in mock.programs);
  await link.sendProgram('ZZT', tiny, { layout: 'v1', release: false });
  check('C27 a calculator that takes only the older layout: the compressed one is not kept, the older one is', no3 && mock.programs.ZZT === tiny);
  ({ mock, link } = session({ product: 0x1541 }));
  const ig = await link.info();
  out = await link.sendProgram('ZZT', tiny, { layout: 'v3' });
  f = await link.readProgram('ZZT', { ver: 1 });
  check('C28 a G1\'s 64-byte reports: identify in two reports, the program in ' + out.reports + ', read back the same', ig.build === 15515 && out.reports === Math.ceil(out.bytes / 63) && !!f && f.text === tiny);
  err = null;
  try { await link.sendProgram('1 bad name', tiny, {}); } catch (e) { err = e; }
  check('C29 a name the calculator would not take is refused before anything is sent', !!err && /not a name/.test(err.message) && mock.arrived.length === 1);
  // a stale file ahead of the one asked for
  ({ mock, link } = session());
  await link.sendProgram('AAA', tiny, {}); await link.sendProgram('BBB', tiny + '//b', {});
  await link.port.send(P.framesLegacy(P.requestMessage('AAA', 1, true), 1023)[0]);        // an answer nobody waits for
  await P.sleep(30);
  const savedDrain = link.port.drain; link.port.drain = () => 0;                         // ... and it is still in the queue
  f = await link.readProgram('BBB', { ver: 1 });
  link.port.drain = savedDrain;
  check('C30 an answer for another program that arrives first is passed over, not taken for the one asked for', !!f && f.name === 'BBB' && f.text === tiny + '//b' && notes.some(n => /passed over a file named "AAA"/.test(n)), f && f.name);
  check('C31 the mock ran without an error of its own', !mock.error, mock.error);

  console.log(`\n${pass} PASS, ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
