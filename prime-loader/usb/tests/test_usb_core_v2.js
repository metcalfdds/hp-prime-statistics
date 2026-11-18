// test_usb_core_v2.js -- prime_usb_v2.js against hp-prime-kit's own code, against the byte examples its sources
// publish, and against the mock calculator.  Roger Metcalf & Claude, 17 Nov 2026.
//
//     python3 kit_reference_v1.py REF      (writes hp-prime-kit's message for every program in programs/)
//     node test_usb_core_v2.js REF
//
// NOTHING HERE TOUCHES A CALCULATOR.  A pass says four things and no more:
//   A  the messages are, byte for byte, the ones hp-prime-kit builds (whose layout was read from a G2's own message),
//      and the ones hp-prime-web's tests expect (the older layout, the request, the delete);
//   B  the reports are cut the way each description says, and an acknowledgement's position counts what the two
//      calculators' own acknowledgements counted on 17 Nov 2026;
//   C  a Link and the mock calculator, which was written apart from it and by default does what those two calculators
//      did, agree on a whole session in each framing; each way the mock can differ or fail is seen and named;
//   D  no wait is without an end: not when acknowledgements keep arriving (what stopped the first page on 17 Nov),
//      not when stray reports do, not when the calculator goes off the cable in the middle of a write.
const fs = require('fs'), path = require('path'), crypto = require('crypto'), zlib = require('zlib');
const P = require('../prime_usb_v2.js'), MockPrime = require('./mock_prime_v2.js');

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
const quick = link => { Object.assign(link.pace, { release: 5, stall: 40, patience: 60, ack: 400 }); return link; };

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
  const rawAll = [];
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
    minK = Math.min(minK, r.reports); maxK = Math.max(maxK, r.reports); total += msg.length; if (raw > P.OLD_MOST) past++;
    rawAll.push({ name: r.name, raw: raw, zip: mine, chars: s.length });
  }
  check('A8 all ' + progs.length + ' programs: the uncompressed part is hp-prime-kit\'s, byte for byte (SHA-256), checksum included', innerOk === progs.length, bad);
  check('A9 all ' + progs.length + ': the message\'s two lengths are right and its stream unpacks to that part', lenOk === progs.length, bad);
  check('A10 all ' + progs.length + ': hp-prime-kit\'s message is cut into hp-prime-kit\'s reports, byte for byte', frameOk === progs.length, bad);
  check('A11 all ' + progs.length + ': hp-prime-kit\'s message reads back to the program\'s name and source, checksum good', roundOk === progs.length, bad);
  check('A12 all ' + progs.length + ': the older layout reads back to the same name and source', v1Ok === progs.length, bad);
  const fit = rawAll.filter(x => x.raw <= P.OLD_MOST), topFit = fit.reduce((m, x) => Math.max(m, x.raw), 0), over = rawAll.filter(x => x.raw > P.OLD_MOST).map(x => x.name).sort();
  console.log('     reports a program of a G2: compressed by this browser\'s zlib ' + minR + ' to ' + maxR + ' (hp-prime-kit\'s level 1: ' + minK + ' to ' + maxK + '); not compressed ' + minRaw + ' to ' + maxRaw +
              '; not compressed, ' + past + ' of the ' + progs.length + ' take more than ' + P.OLD_MOST + ' reports (' + over.join(', ') + '), and the largest of the other ' + fit.length + ' takes ' + topFit);
  check('A13 no program needs more than ' + P.OLD_MOST + ' reports of a G2 compressed, so compressed every one fits the old framing', maxR <= P.OLD_MOST && maxK <= P.OLD_MOST, maxR);
  check('A14 not compressed, ' + fit.length + ' of the ' + progs.length + ' fit ' + P.OLD_MOST + ' reports of a G2 and ' + past + ' do not; none fits ' + P.OLD_MOST + ' reports of a G1 (63 bytes each)',
        fit.length + past === progs.length && past === 11 && rawAll.every(x => Math.ceil((10 + 2 * x.name.length + 2 * x.chars) / 63) > P.OLD_MOST), past);
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
  const f3 = P.framesV2(big, 9, 1023), seq3 = f3.map(f => f[0]);
  check('B5 newer framing: a long message\'s reports are numbered 01, then 02 to FD, then 02 again (hp-prime-emulator\'s reading of the Kit), never 00, FE or FF',
        f3.length === 301 && seq3[0] === 1 && seq3[1] === 2 && seq3[252] === 0xFD && seq3[253] === 2 && seq3[300] === 49 && seq3.slice(1).every(s => s >= 2 && s <= 0xFD) &&
        same(Buffer.concat([Buffer.from(f3[0].subarray(9))].concat(f3.slice(1).map(f => Buffer.from(f.subarray(1))))), big), P.runs(seq3));
  check('B6 an acknowledgement is FE 01, the report, 00, the position, the message number', P.hex(P.ackV2(5, 5000, 7, true)) === 'FE 01 05 00 88 13 00 00 07 00 00 00' && P.hex(P.ackV2(5, 5000, 7, false), 3) === 'FE 00 05 ...');
  check('B7 a G1\'s 64-byte reports: 63 bytes a report', P.framesLegacy(big.subarray(0, 200), 63).length === 4 && P.framesLegacy(big.subarray(0, 200), 63)[3].length === 12);
  // logs/: the G2 acknowledged one report with position 1,015; the G1 acknowledged six with position 370
  check('B8 a position is the room of the reports taken: 1,015 after one report of a G2 and 370 after six of a G1, as the two calculators said on 17 Nov',
        P.roomAfter(1, 1023) === 1015 && P.roomAfter(6, 63) === 370 && P.roomAfter(0, 63) === 0 && P.reportsAt(370, 63) === 6 && P.reportsAt(369, 63) === 5 && P.reportsAt(1015, 1023) === 1 && P.reportsAt(1014, 1023) === 0);
  check('B9 "the newest version I speak": PrimeDev\'s seven bytes, and the two of its table', P.hex(P.maxVersionMessage('long')) === 'FD 01 00 00 00 01 03' && P.hex(P.maxVersionMessage('short')) === 'FD 03');
  check('B10 the old framing\'s most is 255 reports and the window 76', P.OLD_MOST === 255 && P.WINDOW === 76);

  // ---------------------------------------------------------------- C. a Link and the mock calculator
  const notes = [], seen = [];
  const session = opts => {
    const mock = new MockPrime(opts);
    const link = quick(new P.Link(mock.port(), { note: t => notes.push(t), trace: (d, r, v2) => seen.push(d + ' ' + P.describe(r, v2).text) }));
    return { mock, link };
  };
  const tiny = 'EXPORT ZZT()\nBEGIN\n RETURN 1;\nEND;';
  const dl = progs.find(r => r.name === 'DataLoad'), epi = progs.find(r => r.name === 'EpiStats');
  const DL = src(dl), EPI = src(epi);
  const fill = (name, reports, cap) => 'x'.repeat(Math.floor((reports * cap - 10 - 2 * name.length) / 2));

  let { mock, link } = session();
  const info = await link.info();
  check('C1 identify: build 15751, the text, 108 bytes, version 01, as the G2 answered on 17 Nov', info.build === 15751 && info.version === 'V2.060.650' && info.bytes === 108 && info.ver === 1, JSON.stringify(info));
  check('C2 the serial number is nowhere in what identify returns', !JSON.stringify(info).includes('SECRET'));
  check('C3 ready: the calculator says Y', await link.ready() === true);
  let out = await link.sendProgram('ZZT', tiny, { layout: 'v1' });
  let f = await link.readProgram('ZZT', { ver: 1, nul: true });
  check('C4 old framing, not compressed: one report, kept; read back with F8 01 and a NUL, the same text, not compressed, checksum good',
        out.reports === 1 && mock.programs.ZZT === tiny && !!f && f.text === tiny && !f.compressed && f.crcOk && f.ver === 1, f && f.text);
  f = await link.readProgram('ZZT', { ver: 3, nul: true });
  check('C5 asked with F8 03, the mock answers with F7 01 all the same, as both calculators did', !!f && f.text === tiny && !f.compressed && f.ver === 1);
  let t0 = Date.now();
  f = await link.readProgram('ZZT', { ver: 1, nul: false, first: 300 });
  check('C6 with no NUL after the name the mock stays silent: no answer, reported after 0.3 s and not later', f === null && Date.now() - t0 >= 280 && Date.now() - t0 < 600, Date.now() - t0);
  out = await link.sendProgram('ZZA', tiny, { layout: 'v3', release: true });
  f = await link.readProgram('ZZA', { ver: 1, first: 300 });
  check('C7 compressed, old framing, to a calculator that speaks version 01: sent, not kept, nothing comes back (17 Nov, both calculators)',
        out.reports === 1 && !('ZZA' in mock.programs) && f === null && mock.releases === 1 && /version 03 while it speaks 01/.test(mock.arrived[mock.arrived.length - 1].why));
  const s255 = fill('ZZC', 255, 1023), s256 = fill('ZZC', 256, 1023);
  out = await link.sendProgram('ZZC', s255, { layout: 'v1' });
  f = await link.readProgram('ZZC', { ver: 1 });
  check('C8 exactly 255 reports, numbered 00 to FE: kept, and read back the same in 255', out.reports === 255 && out.bytes === 260864 && mock.programs.ZZC === s255 && !!f && f.text === s255 && f.reports === 255 && f.numbered === '00-FE', out.reports + ' ' + (f && f.numbered));
  out = await link.sendProgram('ZZC', s256, { layout: 'v1' });
  f = await link.readProgram('ZZC', { ver: 1 });
  check('C9 one report more, 256: not kept, and the program before is what comes back (17 Nov: 274 of the G2, 263 of the G1)', out.reports === 256 && mock.programs.ZZC === s255 && !!f && f.text === s255 && mock.arrived[mock.arrived.length - 1].why === 'too many reports');
  ({ mock, link } = session({ stallMs: 320, busyMs: 250 }));
  await link.sendProgram('ZZC', tiny, { layout: 'v1' });
  out = await link.sendProgram('ZZC', s256, { layout: 'v1', listen: 10 });
  f = await link.readProgram('ZZC', { ver: 1, first: 150 });
  const f9 = await (async () => { await P.sleep(260); return link.readProgram('ZZC', { ver: 1 }); })();
  check('C10 a calculator that holds the cable at the report too many: the send says where it stood (report 256) and for how long; the next request has no answer, the one after has the old program',
        out.slow.length === 1 && out.slow[0].report === 256 && out.slow[0].ms >= 300 && f === null && !!f9 && f9.text === tiny, JSON.stringify(out.slow));
  await link.deleteProgram('ZZC');
  f = await link.readProgram('ZZC', { ver: 1, first: 300 });
  check('C11 delete: the program is gone from the mock, and a request for it is met with silence', !('ZZC' in mock.programs) && f === null);

  // "FD", the old framing
  ({ mock, link } = session());
  let mv = await link.maxVersion('long', 150);
  check('C12 "FD" to the default mock in the old framing: nothing of its own comes back, and it still speaks 01', mv.reply === null && mock.fmt === 1 && (await link.info()).ver === 1 && mock.fds.length === 1 && mock.fds[0].kind === 'long' && mock.fds[0].framing === 'old');
  ({ mock, link } = session({ fdOld: 'short' }));
  mv = await link.maxVersion('long', 150);
  const still1 = mock.fmt === 1;
  mv = await link.maxVersion('short', 150);
  out = await link.sendProgram('DataLoad', DL, { layout: 'v3' });
  f = await link.readProgram('DataLoad', { ver: 3 });
  check('C13 a calculator that takes the short "FD" in the old framing: the long one changes nothing, the short one is answered and it speaks 03; DataLoad compressed is then kept, and comes back compressed in ' + (f && f.reports) + ' reports',
        still1 && mv.reply === 'FD 03 00 00 00 00' && mock.fmt === 3 && (await link.info()).ver === 3 && mock.programs.DataLoad === DL && !!f && f.text === DL && f.compressed && f.ver === 3 && f.reports === out.reports, JSON.stringify(mv));

  // the newer framing
  ({ mock, link } = session());
  await link.info();
  let op = await link.openV2(120);
  check('C14 newer framing: asked for with FF EC 00 00 00 00 00 00, and the mock\'s control report is handed back for the log', mock.v2open && op.replies.length === 1 && /^FF EC 00 00 00 00 00 01/.test(op.replies[0]) && op.others === 0, JSON.stringify(op));
  const i2 = await link.info();
  check('C15 newer framing: identify answers, and the answer was acknowledged with the room of its one report, 1,015', i2.build === 15751 && i2.ver === 1 && mock.hostAcks.length === 1 && mock.hostAcks[0].ok === 1 && mock.hostAcks[0].pos === 1015 && mock.hostAcks[0].id === 1, JSON.stringify(mock.hostAcks));
  out = await link.sendProgram('ZZE', tiny, { layout: 'v1' });
  f = await link.readProgram('ZZE', { ver: 1 });
  check('C16 newer framing, not compressed: acknowledged once with position 1,015, kept, read back the same', out.reports === 1 && out.acks.length === 1 && out.acks[0].ok && out.acks[0].pos === 1015 && mock.programs.ZZE === tiny && !!f && f.text === tiny && !f.compressed);
  out = await link.sendProgram('ZZD', tiny, { layout: 'v3' });
  f = await link.readProgram('ZZD', { ver: 3, first: 300 });
  check('C17 newer framing, compressed, while it speaks 01: acknowledged and NOT kept, as on 17 Nov', out.acks.length === 1 && !('ZZD' in mock.programs) && f === null);
  mv = await link.maxVersion('long', 200);
  out = await link.sendProgram('EpiStats', EPI, { layout: 'v3' });
  f = await link.readProgram('EpiStats', { ver: 3 });
  check('C18 after "FD" in the newer framing the mock answers it and speaks 03; EpiStats compressed (' + out.reports + ' reports) is kept and comes back the same, compressed',
        mv.reply === 'FD 01 00 00 00 01 03' && mock.fmt === 3 && mock.programs.EpiStats === EPI && !!f && f.text === EPI && f.compressed && out.reports > 76 && out.reports < 255, JSON.stringify(mv));
  check('C19 ... and at its window of 76 reports, where this mock says nothing, the Link waited and then went on: the count is handed back', out.unacked === 1 && out.waits === 0 && out.acks.length === 1, out.unacked + ' ' + out.waits);
  check('C20 ... and the mock, which stops after 76 reports until it is acknowledged, was acknowledged at 76 and at the end, and sent nothing twice',
        f.stalls.join() === '76' && link.learned === 76 && mock.resent === 0 && f.again === 0 && f.gaps === 0, f.stalls.join() + ' ' + link.learned + ' ' + mock.resent);
  f = await link.readProgram('EpiStats', { ver: 3 });
  check('C21 the second time the Link acknowledges at 76 without being waited for', !!f && f.text === EPI && f.stalls.length === 0 && mock.resent === 0);

  // a G1, and the long way round
  ({ mock, link } = session({ product: 0x1541 }));
  const ig = await link.info();
  await link.openV2(60);
  out = await link.sendProgram('EpiStats', EPI, { layout: 'v1' });
  f = await link.readProgram('EpiStats', { ver: 1, first: 4000 });
  check('C22 a G1\'s 64-byte reports, newer framing: EpiStats not compressed is ' + out.reports.toLocaleString('en-US') + ' reports, past the numbers\' turn many times; kept, and read back the same',
        ig.version === 'V0.050.640' && out.reports === 9201 && mock.programs.EpiStats === EPI && !!f && f.text === EPI && f.reports === 9201 && mock.resent === 0, out.reports + ' ' + mock.resent);
  // the three things a calculator may do at our window
  ({ mock, link } = session({ product: 0x1541, ackEvery: 76 }));
  await link.openV2(60);
  out = await link.sendProgram('DataLoad', DL, { layout: 'v1' });
  check('C23 a calculator that acknowledges every 76 reports: the Link never goes on unacknowledged', mock.programs.DataLoad === DL && out.unacked === 0 && out.acks.length >= Math.floor(out.reports / 76), out.unacked + ' ' + out.acks.length);
  ({ mock, link } = session({ product: 0x1541, ackRepeat: 25 }));
  await link.openV2(60);
  out = await link.sendProgram('DataLoad', DL, { layout: 'v1' });
  check('C24 a calculator that acknowledges on a clock: the Link waits at its window for the clock, and the program arrives', mock.programs.DataLoad === DL && out.unacked === 0 && out.waits >= 1, out.unacked + ' ' + out.waits);
  mock.stop();
  ({ mock, link } = session({ product: 0x1541, nackOnce: 40 }));
  await link.openV2(60);
  out = await link.sendProgram('DataLoad', DL, { layout: 'v1' });
  check('C25 asked for report 40 again, the Link sends from there and the program arrives whole', mock.nacked === true && mock.programs.DataLoad === DL && out.acks.some(a => !a.ok));
  ({ mock, link } = session({ needAck: false }));
  await link.openV2(60);
  await link.sendProgram('DataLoad', DL, { layout: 'v1' });
  f = await link.readProgram('DataLoad', { ver: 1 });
  check('C26 a calculator that sends without waiting to be acknowledged: read back the same, with no pause', !!f && f.text === DL && f.stalls.length === 0);
  ({ mock, link } = session({ ackPos: 'size', copies: 3 }));
  await link.openV2(60);
  await link.sendProgram('AAA', tiny, { layout: 'v1' }); await link.sendProgram('BBB', tiny + '//b', { layout: 'v1' });
  f = await link.readProgram('AAA', { ver: 1 });
  await link.swallow(150);
  const g = await link.readProgram('BBB', { ver: 1 });
  check('C27 a calculator that sends each file three times (the G1 sent one several times): after a listen the next answer is the right one, and every copy was acknowledged',
        !!f && f.text === tiny && !!g && g.text === tiny + '//b' && mock.hostAcks.filter(a => a.ok).length >= 4 && mock.gaveUp === 0, JSON.stringify(mock.hostAcks.length));
  ({ mock, link } = session({ v2: false }));
  await link.openV2(60);
  let err = null;
  try { await link.sendV2(Uint8Array.of(0xFA)); } catch (e) { err = e; }
  check('C28 a calculator without the newer framing: no acknowledgement, named as such, after 0.4 s', err instanceof P.Silent && /no acknowledgement of the whole of message 1 \(1 report\) within 0\.4 s; none came at all/.test(err.message), err && err.message);
  ({ mock, link } = session({ oldAfterNew: false }));
  await link.openV2(60);
  link.v2 = false;
  err = null;
  try { await link.info(300); } catch (e) { err = e; }
  check('C29 a calculator that no longer answers the old framing once the newer is open: "no answer within 0.3 s"', err instanceof P.Silent && /no answer within 0\.3 s/.test(err.message), err && err.message);

  // a message the calculator sends in pieces a second time, and one with a report missing, by a port whose reports
  // are queued by hand
  {
    const q = [], sent = [], pad = f => { const r = new Uint8Array(1024); r.set(f); return r; };
    const sp = { reportSize: 1024, send: async f => { sent.push(Uint8Array.from(f)); if (f[0] === 0xFE && f[1] === 0) again(); }, read: async () => (q.length ? q.shift() : null), poll: () => null, drain: () => 0 };
    const lk = quick(new P.Link(sp));
    lk.v2 = true;
    const m1 = await P.programV3('AAA', DL), fs1 = P.framesV2(m1, 7, 1023);
    let again = () => {};
    fs1.slice(0, 6).forEach(x => q.push(pad(x)));
    fs1.slice(3, 6).forEach(x => q.push(pad(x)));                  // reports 4 to 6 again: a retry of the calculator's
    fs1.slice(6).forEach(x => q.push(pad(x)));
    const r1 = await lk.recvV2([0xF7], 300, 300), g1 = await P.parseFile(r1);
    check('C30 reports that come a second time are dropped, counted, and the message is whole', g1.name === 'AAA' && g1.text === DL && lk.last.again === 3 && lk.last.gaps === 0 && sent.length === 1 && sent[0][1] === 1 && P.rdU32le(sent[0], 4) === P.roomAfter(fs1.length, 1023));
    sent.length = 0;
    const fs2 = P.framesV2(m1, 8, 1023);
    fs2.forEach((x, k) => { if (k !== 4) q.push(pad(x)); });        // its fifth report is lost on the way
    again = () => { again = () => {}; fs2.slice(4).forEach(x => q.push(pad(x))); };
    const r2 = await lk.recvV2([0xF7], 300, 300), g2 = await P.parseFile(r2);
    check('C31 a report missing: the Link asks for it once ("FE 00" and its number), drops what came out of turn, and puts the message together when it is sent again',
          g2.text === DL && sent.length === 2 && sent[0][0] === 0xFE && sent[0][1] === 0 && sent[0][2] === fs2[4][0] && P.rdU32le(sent[0], 8) === 8 && sent[1][1] === 1 && lk.last.gaps === fs2.length - 5, sent.map(a => P.hex(a, 12)).join(' | '));
  }

  // ---------------------------------------------------------------- D. no wait without an end
  // What stopped the first page: a calculator that repeats its acknowledgement while the page waits for an answer.
  ({ mock, link } = session({ ackRepeat: 20 }));
  await link.openV2(60);
  await link.sendProgram('ZZD', tiny, { layout: 'v3' });               // acknowledged, not kept
  t0 = Date.now();
  f = await link.readProgram('ZZD', { ver: 1, first: 400 });
  let took = Date.now() - t0;
  check('D1 newer framing: acknowledgements arriving every 20 ms do not lengthen the wait for an answer: none in 0.4 s, said after ' + took + ' ms', f === null && took >= 380 && took < 800 && mock.reportsOut > 15, took + ' ms, ' + mock.reportsOut + ' reports');
  mock.stop();
  {
    // the old framing: a stream of reports that are not the answer
    let n = 0;
    const sp = { reportSize: 1024, send: async () => {}, read: ms => new Promise(res => setTimeout(() => { n++; const r = new Uint8Array(1024); r[0] = 0xFE; r[1] = 1; r[2] = 1; res(r); }, 15)), poll: () => null, drain: () => 0 };
    const lk = quick(new P.Link(sp));
    t0 = Date.now(); err = null;
    try { await lk.recvLegacy([0xF7], 400, 400); } catch (e) { err = e; }
    took = Date.now() - t0;
    check('D2 old framing: the same, with ' + n + ' reports that were not the answer: "no answer within 0.4 s", after ' + took + ' ms, and it says how many others came', err instanceof P.Silent && took >= 380 && took < 800 && /other reports came/.test(err.message), err && err.message);
    // a reply that starts and never ends
    let k = 0;
    sp.read = ms => new Promise(res => setTimeout(() => { const r = new Uint8Array(1024); if (k++ === 0) { r[1] = 0xF7; r[2] = 1; r[5] = 0x40; } else { r[0] = 0xFF; } res(r); }, 15));
    t0 = Date.now(); err = null;
    try { await lk.recvLegacy([0xF7], 400, 300); } catch (e) { err = e; }
    took = Date.now() - t0;
    check('D3 old framing: a reply that begins and then only control reports come: "the reply stopped", 0.3 s after its last report (' + took + ' ms)', err instanceof P.Cut && /the reply stopped after 1,023 of 16,390 bytes, 1 report/.test(err.message) && took < 700, err && err.message);
  }
  ({ mock, link } = session({ dieAt: 100 }));
  err = null; t0 = Date.now();
  try { await link.sendProgram('ZZC', s255, { layout: 'v1' }); } catch (e) { err = e; }
  check('D4 a calculator that goes off the cable in the middle of a program: the send ends at once with "Gone", and so does whatever is tried next', P.isGone(err) && Date.now() - t0 < 500 &&
        P.isGone(await link.info().catch(e => e)) && P.isGone(await link.port.read(50).catch(e => e)), err && err.message);
  {
    // HidPort itself, on a pretend WebHID device
    const dev = { productId: 0x2441, opened: true, collections: [], listeners: [], sent: [], mode: 'ok',
      addEventListener(t, fn) { this.listeners.push(fn); }, removeEventListener() {}, close: async () => {},
      sendReport(id, data) { this.sent.push(data.length); return this.mode === 'ok' ? Promise.resolve() : this.mode === 'fail' ? Promise.reject(new Error('Failed to write the report.')) : new Promise(() => {}); } };
    let hp = new P.HidPort(dev);
    await hp.send(Uint8Array.of(0, 0xFA));
    check('D5 HidPort: a report goes out at its full size, 1,024 bytes, padded', dev.sent.join() === '1024' && hp.sent === 1 && hp.reportSize === 1024);
    dev.mode = 'never';                                              // what Chrome did on 17 Nov: the write never came back
    t0 = Date.now();
    const w = hp.send(Uint8Array.of(0, 0xFA)).catch(e => e), rd = hp.read(5000).catch(e => e);
    setTimeout(() => hp.lose('the browser says it went off the cable'), 60);
    const [we, re] = [await w, await rd];
    check('D6 HidPort: when the browser says the calculator has gone, a write that never comes back and a read that is waiting both end at once with "Gone"',
          P.isGone(we) && P.isGone(re) && Date.now() - t0 < 400 && /went off the cable/.test(we.message) && P.isGone(await hp.send(Uint8Array.of(0)).catch(e => e)) && P.isGone(await hp.read(10).catch(e => e)), we && we.message);
    hp = new P.HidPort(dev); hp.limit = 120;
    t0 = Date.now();
    const e2 = await hp.send(Uint8Array.of(0, 0xFA)).catch(e => e);
    check('D7 HidPort: with no word from the browser, a write that never comes back ends at its own limit: "did not take a report within 0.1 s"', P.isGone(e2) && /did not take a report within 0\.1 s/.test(e2.message) && Date.now() - t0 < 500, e2 && e2.message);
    dev.mode = 'fail'; hp = new P.HidPort(dev);
    const e3 = await hp.send(Uint8Array.of(0, 0xFA)).catch(e => e);
    check('D8 HidPort: a write the browser refuses is a calculator that has gone, in the browser\'s own words', P.isGone(e3) && /could not write to the calculator \(Failed to write the report\)/.test(e3.message), e3 && e3.message);
  }

  // ---------------------------------------------------------------- what a log line may hold
  const lines = seen.join('\n');
  check('E1 the trace of all the sessions above (' + seen.length.toLocaleString('en-US') + ' reports) never holds the serial number, as text or as bytes', seen.length > 20000 && !/SECRET/.test(lines) && !/53 45 43 52/.test(lines));
  // (the bytes of a line are what follows "begins" or "control report:"; the rest of it is words and counts)
  const shown = s => { const k = Math.max(s.lastIndexOf('begins '), s.lastIndexOf('report: ')); return k < 0 ? 0 : (s.slice(k).match(/\b[0-9A-F]{2}\b/g) || []).length; };
  const worst = seen.reduce((m, s) => Math.max(m, shown(s)), 0);
  check('E2 no line of it shows more than twelve bytes of a report', worst === 12, worst);
  check('E3 an information reply is shown by its six-byte head alone, in either framing', seen.includes('< message begins FA 01 00 00 00 6C') && seen.some(s => /^< message \d+, 114 bytes, begins FA 0[13] 00 00 00 6C$/.test(s)));
  check('E4 the mock ran without an error of its own', !mock.error, mock.error);

  console.log(`\n${pass} PASS, ${fail} FAIL`);
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
