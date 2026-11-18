// test_usb_core_v3.js -- prime_usb_v3.js against hp-prime-kit's own code, against the numbers in the logs of two real
// calculators, and against the mock calculator.  Roger Metcalf & Claude, 17 Nov 2026.
//
//     python3 kit_reference_v1.py REF      (writes hp-prime-kit's message for every program in programs/)
//     node test_usb_core_v3.js REF
//
// NOTHING HERE TOUCHES A CALCULATOR.  A pass says this and no more:
//   A  the messages are, byte for byte, the ones hp-prime-kit builds and hp-prime-web's tests expect, and the requests
//      and deletes begin with the bytes the author's two calculators answered on 17 Nov 2026 (../logs/);
//   B  the reports are cut and numbered, and a position counted, the way those logs show;
//   C  a Link and the mock calculator, which was written apart from it and by default does what the two calculators
//      did, agree on the route the Loader takes; a word of the calculator's clock, a lost report and a late answer are
//      each seen, named and survived;
//   D  no wait is without an end;
//   E  a load says what happened to each program, and never calls one loaded that was not read back;
//   F  the book's programs, every one, go onto a pretend G1 and a pretend G2 and come back the same;
//   G  a log shows what passed, twelve bytes of a message at most, and never the serial number.
const fs = require('fs'), path = require('path'), crypto = require('crypto'), zlib = require('zlib');
const P = require('../prime_usb_v3.js'), MockPrime = require('./mock_prime_v3.js');

const REF = path.resolve(process.argv[2]);
const ref = JSON.parse(fs.readFileSync(path.join(REF, 'reference.json'), 'utf8'));
const PROGRAMS = path.join(__dirname, '..', '..', '..', 'programs');
const KIT = process.env.HPKIT || '/tmp/kit/hp-prime-kit-HEAD';
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const bytes = s => Uint8Array.from(s.trim().split(/\s+/).map(h => parseInt(h, 16)));
const same = (a, b) => a.length === b.length && Buffer.from(a).equals(Buffer.from(b));
const src = r => P.normalizeSource(fs.readFileSync(r.name === 'SELFTEST' ? path.join(KIT, 'examples', 'selftest', 'SELFTEST.txt') : path.join(PROGRAMS, r.file), 'utf8'));
const num = n => String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ',');

let pass = 0, fail = 0;
function check(name, ok, detail) {
  if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : detail); }
}
// The waits of a test: the mock's clock every 80 ms, and the Link's patience to match.
const quick = link => { Object.assign(link.pace, { release: 5, stall: 40, ack: 500, back: 25, quiet: 40 }); return link; };
const G1 = 0x1541;

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

  // the bytes the two calculators answered or obeyed on 17 Nov, as their logs show them (ZZUSBE, six letters)
  const heads = [[P.requestMessage('ZZUSBE', 3, true), 'F8 03 00 00 00 12 06 0E C3 21 5A 00'], [P.requestMessage('ZZUSBE', 1, true), 'F8 01 00 00 00 12 06 0E 07 00 5A 00'],
                 [P.requestMessage('ZZUSBE', 3, false), 'F8 03 00 00 00 10 06 0C 39 9A 5A 00'], [P.requestMessage('ZZUSBE', 1, false), 'F8 01 00 00 00 10 06 0C E0 D7 5A 00'],
                 [P.deleteMessage('ZZUSBE', 3), 'EB 03 00 00 00 10 06 0C 7E 51 5A 00'], [P.deleteMessage('ZZUSBE', 1), 'EB 01 00 00 00 10 06 0C A7 1C 5A 00']];
  check('A17 the requests and the deletes for ZZUSBE begin with the bytes in the logs of 17 Nov: the two with a NUL were answered with the program, the deletes took it off',
        heads.every(h => P.hex(h[0].subarray(0, 12)) === h[1]), heads.map(h => P.hex(h[0].subarray(0, 12))).join(' | '));
  // what the whole book is, not compressed in the newer framing: counted here, because the README and the page's words say it
  const chars = rawAll.reduce((n, x) => n + x.chars, 0);
  const reportsOf = (x, cap) => P.framesV2(P.programV1(x.name, 'x'.repeat(x.chars)), 1, cap).length;
  const g1Reports = rawAll.reduce((n, x) => n + reportsOf(x, 63), 0), g2Reports = rawAll.reduce((n, x) => n + reportsOf(x, 1023), 0);
  const biggest = rawAll.reduce((m, x) => x.chars > m.chars ? x : m), smallest = rawAll.reduce((m, x) => x.chars < m.chars ? x : m);
  console.log('     the ' + rawAll.length + ' programs: ' + num(chars) + ' characters; not compressed in the newer framing ' + num(g1Reports) + ' reports of a G1 and ' + num(g2Reports) + ' of a G2; the largest is ' +
              biggest.name + ' (' + num(biggest.chars) + ' characters, ' + num(reportsOf(biggest, 63)) + ' and ' + num(reportsOf(biggest, 1023)) + ' reports), the smallest ' + smallest.name + ' (' + num(smallest.chars) + ')');
  check('A18 the book\'s ' + rawAll.length + ' programs are 4,147,067 characters: 131,683 reports of a G1 and 8,125 of a G2, not compressed in the newer framing; the largest, EpiStats, is 289,813 characters (9,201 and 567 reports)',
        rawAll.length === 31 && chars === 4147067 && g1Reports === 131683 && g2Reports === 8125 && biggest.name === 'EpiStats' && biggest.chars === 289813 && reportsOf(biggest, 63) === 9201 && reportsOf(biggest, 1023) === 567,
        [rawAll.length, chars, g1Reports, g2Reports, biggest.name, biggest.chars].join(' '));

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

  // the numbers the two calculators themselves said on 17 Nov (../logs/, the two logs of the second test)
  check('B10 the window is 77 reports, the calculator\'s own stand is at 240 reports\' worth, and the old framing\'s most is 255', P.WINDOW === 77 && P.STANDS_AT === 240 && P.OLD_MOST === 255);
  check('B11 the positions in the logs are the room of the reports: G2 78,763 (77), 157,534 (154), 132,982 (130), 580,033 (567); G1 4,843 (77), 14,545 (231), 15,112 (240), 15,175 (241), 132,481 (2,103), 579,655 (9,201)',
        P.roomAfter(77, 1023) === 78763 && P.roomAfter(154, 1023) === 157534 && P.roomAfter(130, 1023) === 132982 && P.roomAfter(567, 1023) === 580033 && P.roomAfter(77, 63) === 4843 &&
        P.roomAfter(231, 63) === 14545 && P.roomAfter(240, 63) === 15112 && P.roomAfter(241, 63) === 15175 && P.roomAfter(2103, 63) === 132481 && P.roomAfter(9201, 63) === 579655 &&
        P.reportsAt(78763, 1023) === 77 && P.reportsAt(78762, 1023) === 76 && P.reportsAt(15175, 63) === 241);
  const e63 = P.framesV2(new Uint8Array(579648), 16, 63), e1023 = P.framesV2(new Uint8Array(579648), 16, 1023);
  check('B12 the 579,648 bytes of the largest test program: 9,201 reports of a G1, the 77th numbered 4D and the last 81; 567 of a G2, the last 3F; as the two logs number them',
        e63.length === 9201 && e63[76][0] === 0x4D && e63[9200][0] === 0x81 && e1023.length === 567 && e1023[76][0] === 0x4D && e1023[566][0] === 0x3F, [e63.length, P.hex2(e63[9200][0]), e1023.length, P.hex2(e1023[566][0])].join(' '));
  check('B13 the time allowed for an answer to begin: 3 s for a short program, and for the largest four times the 3.1 s a G1 took', P.patienceFor(0) === 3000 && P.patienceFor(300) < 3100 && P.patienceFor(289813) >= 4 * 3100 && P.patienceFor(289813) < 20000, P.patienceFor(289813));
  const d = (hexs, v2, ex) => P.describe(bytes(hexs + ' 00 00 00 00 00 00 00 00 00 00 00 00'), v2, ex);
  check('B14 a report is named for the log: an acknowledgement, a "send again" (always written), the last acknowledgement again (FF), a message\'s start',
        /^acknowledgement: report 4E, position 78,763, message 16$/.test(d('FE 01 4E 00 AB 33 01 00 10 00 00 00', true).text) && d('FE 00 02 00 F7 03 00 00 10 00 00 00', true).loud === true &&
        /^"SEND AGAIN": report 02, position 1,015, message 16$/.test(d('FE 00 02 00 F7 03 00 00 10 00 00 00', true).text) && /again \(FF\), position 55, message 17$/.test(d('FE 01 FF 00 37 00 00 00 11 00 00 00', true).text) &&
        d('FE 01 FF 00 37 00 00 00 11 00 00 00', true).key !== d('FE 01 01 00 37 00 00 00 11 00 00 00', true).key && /^message 9, 132,431 bytes, begins F7 03 00 02 05 49 3C D8 08 00 78 01$/.test(d('01 09 00 00 00 4F 05 02 00 F7 03 00 02 05 49 3C D8 08 00 78 01', true).text));
  check('B15 in the old framing a report that carries a message on is counted as that whatever its number: FE is not an acknowledgement, 00 after FE not a new message (both were misread in a log of 17 Nov)',
        d('FE 00 65 00 2C 00 36 00', false, 0xFE).kind === 'more' && d('00 00 67 00 65 00 2C 00', false, 0).kind === 'more' && d('00 FA 03 00 00 00 6C', false).kind === 'start' && d('00 FA 03 00 00 00 6C AA BB CC DD EE FF', false).text === 'message begins FA 03 00 00 00 6C');

  // ---------------------------------------------------------------- C. a Link and the mock calculator
  const notes = [];
  const session = opts => {
    const mock = new MockPrime(Object.assign({ tickMs: 80 }, opts || {}));
    const link = quick(new P.Link(mock.port(), { note: t => notes.push(t) }));
    return { mock, link };
  };
  const tiny = 'EXPORT ZZT()\nBEGIN\n RETURN 1;\nEND;';
  const dl = progs.find(r => r.name === 'DataLoad'), epi = progs.find(r => r.name === 'EpiStats');
  const DL = src(dl), EPI = src(epi);
  // a program whose "F7 01" message fills exactly so many reports of the newer framing
  const fill = (name, reports, cap) => 'x'.repeat(Math.floor(((cap - 8) + (reports - 1) * cap - 10 - 2 * name.length) / 2));
  const multiples = (acks, cap, n) => acks.filter(a => a.ok).map(a => P.reportsAt(a.pos, cap)).every(k => k % 77 === 0 || k === n);

  let { mock, link } = session();
  let b = await link.begin(1000);
  check('C1 a session begins as it did on both calculators: version 01; "FD 01 00 00 00 01 03" in the old framing, answered with the same bytes; version 03; then "FF EC", which has no answer; ' +
        'then "who are you" in the newer framing, answered in it and acknowledged with the room of its one report: six reports from the host in all',
        b.told && b.reply === 'FD 01 00 00 00 01 03' && b.ver === 3 && b.open && b.info.build === 15751 && b.info.version === 'V2.060.650' && mock.fds.length === 1 && mock.fds[0].kind === 'long' && mock.fds[0].framing === 'old' &&
        mock.v2open && link.v2 && mock.reportsIn === 6 && mock.hostAcks.length === 1 && mock.hostAcks[0].pos === 1015 && mock.hostAcks[0].id === 3 && mock.handledNew === 1,
        JSON.stringify([b.told, b.reply, b.ver, mock.fds, mock.reportsIn, mock.hostAcks]));
  check('C2 the serial number is nowhere in what it returns', !JSON.stringify(b).includes('SECRET'));
  let out = await link.sendProgram('ZZT', tiny);
  let f = await link.readProgram('ZZT', { ver: 3, nul: true });
  check('C3 a program goes as "F7 01" unless asked otherwise, one report, acknowledged with position 1,015; kept; and comes back compressed in a stream that begins 78 01, the same text, checksum good',
        out.reports === 1 && out.acks.length === 1 && out.acks[0].ok && out.acks[0].pos === 1015 && mock.arrived[0].layout === 'v1' && mock.arrived[0].framing === 'new' && mock.programs.ZZT === tiny &&
        !!f && f.text === tiny && f.compressed && f.crcOk && f.lengthOk && f.ver === 3 && /78 01$/.test(f.head), f && f.head);
  let t0 = Date.now();
  f = await link.readProgram('ZZT', { ver: 3, nul: false, first: 300 });
  check('C4 asked for with no NUL after the name it stays silent, as both calculators did: no answer, said after 0.3 s and not later', f === null && Date.now() - t0 >= 280 && Date.now() - t0 < 700, Date.now() - t0);
  out = await link.sendProgram('ZZD', tiny, { layout: 'v3' });
  f = await link.readProgram('ZZD', { ver: 3, first: 300 });
  check('C5 compressed by the browser ("F7 03", a stream beginning 78 9C), though it speaks 03: acknowledged, NOT kept, nothing comes back, as on both calculators',
        out.acks.length === 1 && out.acks[0].ok && !('ZZD' in mock.programs) && f === null && mock.arrived[mock.arrived.length - 1].why === 'compressed');
  await link.deleteProgram('ZZT', 3);
  f = await link.readProgram('ZZT', { ver: 3, first: 300 });
  check('C6 "EB 03" takes a program off, and a request for it is then met with silence', !('ZZT' in mock.programs) && f === null);
  mock.stop();

  ({ mock, link } = session({ fmt: 3 }));
  b = await link.begin(1000);
  check('C7 a calculator that speaks 03 already (a second load without unplugging) is not told again', !b.told && b.ver === 3 && mock.fds.length === 0 && mock.v2open);
  mock.stop();
  ({ mock, link } = session({ fdOld: null }));
  b = await link.begin(1000);
  check('C8 a calculator that does not take the "FD" still says 01, and the newer framing is then NOT asked for: nothing about it is changed', b.told && b.reply === null && b.ver === 1 && !b.open && !mock.v2open && !link.v2);
  mock.stop();

  // the sizes around the window, on both report sizes
  const edges = [];
  for (const product of [0x2441, G1]) {
    for (const n of [2, 76, 77, 78, 153, 154, 155, 231, 232, 480]) {
      ({ mock, link } = session({ product, tickMs: 0 }));
      await link.begin(1000);
      const cap = link.cap, text = fill('ZZE', n, cap), t = Date.now();
      out = await link.sendProgram('ZZE', text);
      const ms = Date.now() - t, want = Math.floor(n / 77) + (n % 77 ? 1 : 0);
      f = await link.readProgram('ZZE', { ver: 3 });
      const okAcks = out.acks.length === want && out.acks.every(a => a.ok) && multiples(out.acks, cap, n) && out.acks[out.acks.length - 1].pos === P.roomAfter(n, cap);
      if (!(out.reports === n && mock.programs.ZZE === text && okAcks && out.backs === 0 && mock.outOfTurn === 0 && mock.statuses === 0 && ms < 70 && !!f && f.text === text))
        edges.push((product === G1 ? 'G1 ' : 'G2 ') + n + ': ' + JSON.stringify([out.reports, out.acks.length, want, out.backs, mock.outOfTurn, mock.statuses, ms, !!f && f.text === text]));
      mock.stop();
    }
  }
  check('C9 programs of exactly 2, 76, 77, 78, 153, 154, 155, 231, 232 and 480 reports, of a G2 and of a G1: each acknowledged at every 77th report and at its end and nowhere else, no report sent twice, ' +
        'and never a wait for the calculator\'s clock (v2 waited 0.7 s at every 76th)', edges.length === 0, edges.join('; '));

  // the largest program on a G1: its send, and the long answer the calculator stands in
  ({ mock, link } = session({ product: G1, tickMs: 0 }));
  await link.begin(1000);
  const seenG1 = [];
  link.progress = (have, of) => seenG1.push(have + '/' + of);
  out = await link.sendProgram('EpiStats', EPI);
  f = await link.readProgram('EpiStats', { ver: 3 });
  const ha = mock.hostAcks.filter(a => a.id === f.id);
  check('C10 EpiStats to a G1: 9,201 reports, the last numbered 81; 120 acknowledgements (119 at every 77th report, and the whole); no report twice; progress is told at each',
        out.reports === 9201 && out.acks.length === 120 && multiples(out.acks, 63, 9201) && out.acks[119].seq === 0x81 && out.acks[119].pos === 579655 + 0 && out.backs === 0 && mock.outOfTurn === 0 &&
        mock.programs.EpiStats === EPI && seenG1.filter(x => /\/9201$/.test(x)).length === 120 && seenG1[0] === '77/9201' && seenG1[119] === '9201/9201', JSON.stringify([out.reports, out.acks.length, out.acks[119], seenG1.length]));
  const at = ha.map(a => P.reportsAt(a.pos, 63));
  check('C11 ... and it comes back the same in ' + num(f.reports) + ' reports: the Link acknowledges at 241 reports and every 240 after, with the number of the last report that came, and the whole, ' +
        'so the calculator, which stands at 240 reports\' worth unacknowledged, never stood for longer than a moment',
        !!f && f.text === EPI && f.compressed && f.reports > 482 && f.stalls.length === 0 && f.again === 0 && f.gaps === 0 && ha.every(a => a.ok === 1) && at[0] === 241 && at.slice(0, -1).every((k, i) => k === 241 + 240 * i) &&
        at[at.length - 1] === f.reports && mock.waits.every(w => w.ms < 60), JSON.stringify([f.reports, at, mock.waits.map(w => w.ms)]));
  mock.stop();

  // the calculator's clock speaks in the middle of what is coming in
  const clock = [];
  for (const o of [{ tickOnReport: 1 }, { tickOnReport: 1, tickLate: 3 }, { tickOnReport: 40, tickLate: 2 }, { tickOnReport: 76, tickLate: 0 }, { tickOnReport: 100, tickLate: 5 },
                   { product: G1, tickOnReport: 1, tickNack: true }, { product: G1, tickOnReport: 30, tickLate: 4 }, { product: G1, tickOnReport: 77, tickLate: 1 }]) {
    ({ mock, link } = session(Object.assign({ tickMs: 0 }, o)));
    await link.begin(1000);
    out = await link.sendProgram('EpiStats', EPI);
    // a "send again" that is out of date costs one report sent twice; an acknowledgement, or a word that is up to date, costs nothing
    const stale = mock.o.tickNack && mock.o.tickLate > 0 && mock.o.tickOnReport < 77, twice = stale ? 1 : 0;
    if (!(mock.programs.EpiStats === EPI && mock.statuses === 1 && mock.outOfTurn === twice && out.backs === twice && out.again === twice && mock.nacks === twice))
      clock.push(JSON.stringify(o) + ': ' + JSON.stringify([mock.programs.EpiStats === EPI, mock.statuses, mock.outOfTurn, out.backs, out.again, mock.nacks]));
    mock.stop();
  }
  check('C12 the calculator\'s clock says "send again" for a report that is on its way, as the G2\'s did after the first report of its longest message: ONE report is sent a second time, the calculator ' +
        'says what it has, and the sending goes on from there (v2 went back seven times); a word that is an acknowledgement, or is up to date, costs nothing', clock.length === 0, clock.join('; '));

  // a report that is really lost
  const lost = [];
  for (const o of [{ loseAt: 5 }, { loseAt: 77 }, { loseAt: 78 }, { loseAt: 300 }, { product: G1, loseAt: 200 }, { product: G1, loseAt: 1298 }, { loseAt: 5, nack: false }, { product: G1, loseAt: 200, nack: false },
                   { product: G1, loseAt: 1298, nack: false }, { loseAt: 80, nack: false }]) {
    ({ mock, link } = session(Object.assign({ tickMs: 100 }, o)));      // (a report lost at the end of a window is known only by the calculator's clock)
    await link.begin(1000);
    const text = o.product === G1 ? DL : EPI, t = Date.now();
    out = await link.sendProgram('ZZL', text);
    f = await link.readProgram('ZZL', { ver: 3 });
    if (!(mock.lost && mock.programs.ZZL === text && out.backs === 1 && !!f && f.text === text && Date.now() - t < 1500)) lost.push(JSON.stringify(o) + ': ' + JSON.stringify([mock.lost, mock.programs.ZZL === text, out.backs, Date.now() - t]));
    mock.stop();
  }
  check('C13 a report lost on the way (the 5th, the 77th, the 78th, the 300th, a G1\'s 200th, a message\'s last): with the calculator\'s "send again", or without it on the word of its clock, ' +
        'the sending goes back once and the program arrives whole', lost.length === 0, lost.join('; '));

  // a word about some other message that has this message's number (a load before this one, on the same calculator)
  ({ mock, link } = session({ tickMs: 0 }));
  await link.begin(1000);
  {
    const port = link.port, send0 = port.send, stray = new Uint8Array(1024);
    stray.set(P.ackV2(0xFF, 1000000, link.id, true));             // "all of message N is here", said of another message N
    let k = 0;
    port.send = function (fr) { if (++k === 3) mock.onreport(stray); return send0.call(port, fr); };
    out = await link.sendProgram('EpiStats', EPI);
    port.send = send0;
  }
  check('C14 a stray acknowledgement that claims more reports than have been sent is passed over: the message is not taken for finished, and arrives whole', out.reports === 567 && mock.programs.EpiStats === EPI && mock.outOfTurn === 0 && out.acks.length === 8, out.acks.length);
  mock.stop();

  // an answer that takes its time (a G1 took 3.1 s to begin sending 289,813 characters back; v2 waited 3.0)
  ({ mock, link } = session({ product: G1, lagMs: 3300 }));
  await link.begin(1000);
  await link.sendProgram('DataLoad', DL);
  t0 = Date.now();
  f = await link.readProgram('DataLoad', { ver: 3, first: P.patienceFor(289813) });
  check('C15 an answer that begins 3.3 s after the request, where v2 gave up at 3.0: with the wait that the largest program is given, it is read back the same', !!f && f.text === DL && Date.now() - t0 >= 3250 && Date.now() - t0 < 4200, Date.now() - t0);
  mock.stop();

  // an answer that comes after the reader has given up must not be left standing
  ({ mock, link } = session({ product: G1, lagMs: 250 }));
  await link.begin(1000);
  await link.sendProgram('EpiStats', EPI);
  f = await link.readProgram('EpiStats', { ver: 3, first: 100 });
  const gaveUp = f === null;
  await P.sleep(400);                                             // by now the calculator has sent 241 reports and stands
  const stood = !!mock.standing && mock.standing.at === 241;
  const i3 = await link.info(1000);                              // the next request: what is waiting is taken first
  check('C16 the reader gives up, the answer comes late and the calculator stands after 241 reports; before the next request the Link takes the answer to its end and acknowledges it, so the calculator ' +
        'answers again (on 17 Nov the G1\'s answer was thrown away, and it answered nothing more)',
        gaveUp && stood && i3.build === 15751 && !mock.standing && mock.flushed === 0 && mock.hostAcks.filter(a => P.reportsAt(a.pos, 63) >= 241).length >= 2, JSON.stringify([gaveUp, stood, !!mock.standing, mock.hostAcks.length]));
  f = await link.readProgram('EpiStats', { ver: 3 });
  check('C17 ... and the program is then read back the same', !!f && f.text === EPI);
  mock.stop();

  // a calculator left standing by a page that is gone: the next page's first question, in the old framing, frees it
  ({ mock, link } = session({ product: G1 }));
  await link.begin(1000);
  await link.sendProgram('EpiStats', EPI);
  await link.send(P.requestMessage('EpiStats', 3, true));         // asked for, and then the page goes away without reading
  await P.sleep(150);
  const stood2 = !!mock.standing;
  link.port.drain();
  const link2 = quick(new P.Link(link.port));                     // a new page on the same cable
  b = await link2.begin(2000);
  check('C18 the G1 of 17 Nov at 210 s: asked "who are you" in the old framing while an answer stands, the mock sends the rest of that answer numbered in the old way (' + num(mock.flushed) +
        ' reports) and then answers; the new page reads its answer among them and begins as usual', stood2 && mock.flushed > 1000 && b.info.build === 15751 && b.ver === 3 && !b.told && link2.v2, JSON.stringify([stood2, mock.flushed, b.ver]));
  out = await link2.sendProgram('DataLoad', DL);
  f = await link2.readProgram('DataLoad', { ver: 3 });
  check('C19 ... and loads and reads back a program', mock.programs.DataLoad === DL && !!f && f.text === DL);
  mock.stop();

  // a port whose reports are queued by hand
  const scripted = (size, onSend) => {
    const q = [], sent = [];
    let waiter = null;
    const push = fr => { const r = new Uint8Array(size); r.set(fr); if (waiter) { const w = waiter; waiter = null; w(r); } else q.push(r); };
    const port = { reportSize: size, sent: sent,
      send: async fr => { sent.push(Uint8Array.from(fr)); if (onSend) onSend(fr, push, sent.length); },
      read: ms => q.length ? Promise.resolve(q.shift()) : new Promise(res => { const t = setTimeout(() => { waiter = null; res(null); }, ms); waiter = r => { clearTimeout(t); res(r); }; }),
      poll: () => (q.length ? q.shift() : null), drain: () => { const n = q.length; q.length = 0; return n; } };
    return { port, push, sent };
  };
  {
    // among reports numbered in the old way, one numbered 00 whose next byte happens to be FA is not the answer
    const s = scripted(64, (fr, push, n) => {
      if (n !== 1) return;
      push(Uint8Array.of(0xF2, 1, 2, 3)); push(Uint8Array.of(0x00, 0xFA, 0x99, 0x88, 0x77, 0x66, 0x55, 0x44)); push(Uint8Array.of(0x01, 9, 9, 9));
      const body = new Uint8Array(108); body[72] = 0x87; body[73] = 0x3D; 'V0.050.640'.split('').forEach((c, i) => { body[76 + i] = c.charCodeAt(0); });
      const msg = P.cat([0xFA, 3, 0, 0, 0, 108], body);
      push(P.cat([0x00], msg.subarray(0, 63))); push(P.cat([0x01], msg.subarray(63)));
    });
    const lk = quick(new P.Link(s.port)), i4 = await lk.info(500);
    check('C20 among the reports of an older answer, one numbered 00 that goes on "FA 99 88 77 66" is not taken for the answer to "who are you": the real one after it is', i4.build === 15751 && i4.ver === 3 && i4.version === 'V0.050.640', JSON.stringify(i4));
  }
  {
    const s = scripted(1024), lk = quick(new P.Link(s.port));
    lk.v2 = true;
    const m1 = P.programV1('AAA', DL), fs1 = P.framesV2(m1, 7, 1023);
    fs1.slice(0, 6).forEach(s.push); fs1.slice(3, 6).forEach(s.push); fs1.slice(6).forEach(s.push);       // reports 4 to 6 a second time
    const r1 = await lk.recvV2([0xF7], 300, 300), g1 = await P.parseFile(r1);
    check('C21 reports of an answer that come a second time are dropped and counted, and the answer is whole', g1.name === 'AAA' && g1.text === DL && lk.last.again === 3 && lk.last.gaps === 0 && s.sent.length === 1 && s.sent[0][1] === 1);
    s.sent.length = 0;
    const fs2 = P.framesV2(m1, 8, 1023);
    let asked = false;
    s.port.send = async fr => { s.sent.push(Uint8Array.from(fr)); if (fr[0] === 0xFE && fr[1] === 0 && !asked) { asked = true; fs2.slice(4).forEach(s.push); } };
    fs2.forEach((x, k) => { if (k !== 4) s.push(x); });           // its fifth report is lost on the way
    const r2 = await lk.recvV2([0xF7], 300, 300), g2 = await P.parseFile(r2);
    check('C22 a report of an answer missing: the Link asks for it once ("FE 00", its number, the room of what it has), drops what came out of turn, and puts the answer together when it is sent again',
          g2.text === DL && s.sent.length === 2 && s.sent[0][0] === 0xFE && s.sent[0][1] === 0 && s.sent[0][2] === fs2[4][0] && P.rdU32le(s.sent[0], 4) === P.roomAfter(4, 1023) && P.rdU32le(s.sent[0], 8) === 8 && s.sent[1][1] === 1,
          s.sent.map(x => P.hex(x.subarray(0, 12))).join(' | '));
  }

  // ---------------------------------------------------------------- D. no wait without an end
  const timed = async fn => { const t = Date.now(); let e = null, v; try { v = await fn(); } catch (x) { e = x; } return { ms: Date.now() - t, e, v }; };
  ({ mock, link } = session({ deadAfter: 0 }));
  let r = await timed(() => link.begin(400));
  check('D1 a calculator that answers nothing: "no answer within 0.4 s", after 0.4 s', r.e instanceof P.Silent && /no answer within 0\.4 s/.test(r.e.message) && r.ms >= 380 && r.ms < 700, r.ms + ' ' + (r.e && r.e.message));
  ({ mock, link } = session({ deadAfter: 1 }));
  r = await timed(() => link.begin(400));
  check('D2 one that answers once and then nothing: the "FD" has no answer (0.9 s is given), and the second "who are you" ends the same way', r.e instanceof P.Silent && r.ms >= 1250 && r.ms < 1700, r.ms);
  {
    // what stopped the first page on 17 Nov: the calculator repeats its acknowledgement while the page waits for an answer
    const s = scripted(1024, (fr, push) => { if (fr[0] === 0x01) push(P.ackV2(1, 1015, P.rdU32le(fr, 1), true)); });
    const lk = quick(new P.Link(s.port));
    lk.v2 = true;
    const iv = setInterval(() => s.push(P.ackV2(0xFF, 1015, 1, true)), 20);
    r = await timed(() => lk.readProgram('ZZT', { ver: 3, first: 400 }));
    clearInterval(iv);
    check('D3 acknowledgements that keep arriving do not lengthen the wait for an answer: "no answer" after 0.4 s, though one came every 20 ms', r.e === null && r.v === null && r.ms >= 380 && r.ms < 600, r.ms);
    const s2 = scripted(1024), lk2 = quick(new P.Link(s2.port));
    lk2.v2 = true;
    r = await timed(() => lk2.sendProgram('ZZT', tiny));
    check('D4 a calculator that acknowledges nothing: the message is given up after the 0.5 s allowed, and the words say where it stood', r.e instanceof P.Silent && /message 1 stood for 0\.5 s with 0 of its 1 report acknowledged; the calculator said nothing/.test(r.e.message) && r.ms >= 480 && r.ms < 800, r.ms + ' ' + (r.e && r.e.message));
    // one that says "send again" for the same report whatever it is sent
    const s3 = scripted(1024, (fr, push) => { if (fr[0] !== 0xFE) push(P.ackV2(2, 1015, 1, false)); }), lk3 = quick(new P.Link(s3.port));
    lk3.v2 = true;
    const iv3 = setInterval(() => s3.push(P.ackV2(2, 1015, 1, false)), 60);        // ... and on its clock
    r = await timed(() => lk3.sendProgram('ZZL', EPI));
    clearInterval(iv3);
    check('D5 a calculator that asks for the same report again whatever it is sent: given up after 0.5 s without progress, having sent that report again several times',
          r.e instanceof P.Silent && /"send again", report 02, position 1,015/.test(r.e.message) && r.ms >= 480 && r.ms < 900 && s3.sent.filter(x => x[0] === 2).length >= 5 && s3.sent.length < 1500, r.ms + ' ' + s3.sent.length + ' ' + (r.e && r.e.message));
    // an answer that breaks off
    const s4 = scripted(1024), lk4 = quick(new P.Link(s4.port));
    lk4.v2 = true;
    const fr4 = P.framesV2(P.programV1('AAA', DL), 5, 1023);
    fr4.slice(0, 3).forEach(s4.push);
    r = await timed(() => lk4.recvV2([0xF7], 300, 300));
    check('D6 an answer that breaks off after three reports: "the reply stopped after 3,061 of 81,728 bytes", 0.3 s after the last one, and what had come was acknowledged once on the way in case the calculator was waiting',
          r.e instanceof P.Cut && /stopped after 3,061 of 81,728 bytes, 3 reports/.test(r.e.message) && r.ms >= 280 && r.ms < 600 && s4.sent.length === 1 && P.rdU32le(s4.sent[0], 4) === P.roomAfter(3, 1023), r.ms + ' ' + (r.e && r.e.message));
  }
  ({ mock, link } = session({ product: G1, dieAt: 700 }));
  await link.begin(1000);
  r = await timed(() => link.sendProgram('DataLoad', DL));
  check('D7 the calculator goes off the cable in the middle of a program: the send ends at once, with the error named Gone', P.isGone(r.e) && r.ms < 300 && !('DataLoad' in mock.programs), r.ms + ' ' + (r.e && r.e.name));
  ({ mock, link } = session({ deadAfterNew: 2 }));              // (its two: "who are you" in the newer framing, and the program)
  await link.begin(1000);
  await link.sendProgram('ZZT', tiny);
  r = await timed(() => link.readProgram('ZZT', { ver: 3, first: 5000 }));
  check('D8 a calculator that stops answering after it took the program: the request for it back is not acknowledged, which is said as that (and not as "the program is not there"), after 0.5 s',
        r.e instanceof P.Silent && /stood for 0\.5 s with 0 of its 1 report acknowledged/.test(r.e.message) && r.ms < 900, r.ms + ' ' + (r.e && r.e.message));

  // ---------------------------------------------------------------- E. a load
  const run = async (opts, programs, more) => {
    const mock = new MockPrime(Object.assign({ tickMs: 80 }, opts || {})), link = quick(new P.Link(mock.port()));
    const log = [], items = [];
    const ui = Object.assign({ log: t => log.push(t), trace: (t, at) => log.push('    . ' + t), item: (k, st) => items.push(k + st) }, more || {});
    const res = await P.load(link, programs, ui, { settle: 10, first: 600 });
    mock.stop();
    return { mock, res, log, items, text: log.join('\n') };
  };
  const three = [{ name: 'AAA', source: tiny }, { name: 'DataLoad', source: DL + '\r\n' }, { name: 'CCC', source: tiny + '//c' }];
  let L = await run({}, three);
  check('E1 three programs onto a G2: all read back the same; each goes "send", "check", "ok"; a source with CRLF goes with LF, and nothing else of it is changed',
        L.res.ok && L.res.done.join() === 'AAA,DataLoad,CCC' && L.res.failed === null && !L.res.gone && !L.res.stopped && L.items.join() === '0send,0check,0ok,1send,1check,1ok,2send,2check,2ok' &&
        L.mock.programs.DataLoad === DL + '\n' && L.mock.programs.AAA === tiny && L.res.info.build === 15751 && L.res.told, JSON.stringify(L.res));
  check('E2 its log says who answered, what was told, and for each program what was sent and that it was read back the same',
        /It answered: firmware build 15751, "V2\.060\.650", version 01\. Its reports carry 1,023 bytes each\./.test(L.text) && /it answered FD 01 00 00 00 01 03, and it now answers with version 03/.test(L.text) &&
        /DataLoad: 40,857 characters\.\n(.*\n)*?  Sent 81,740 bytes in 80 reports, \d\.\d\d s\. Acknowledged 2 times\.\n(.*\n)*?  Read back the same: \d+ reports?, compressed/.test(L.text), L.text.slice(0, 1500));
  let n = 0;
  L = await run({}, three, { stop: () => n++ >= 1 });
  check('E3 Stop is looked at between two programs and never inside one: after the first, the load ends with one program on the calculator, whole, and says which was not begun',
        !L.res.ok && L.res.stopped && L.res.done.join() === 'AAA' && L.mock.arrived.length === 1 && /STOPPED by the Stop button, before DataLoad\./.test(L.text), JSON.stringify(L.res));
  L = await run({ drop: ['DataLoad'] }, three);
  check('E4 a program the calculator acknowledges and does not keep, as both did with a compressed one: "missing"; the first program is done, the third is never sent, and the load is not called good',
        !L.res.ok && L.res.failed.name === 'DataLoad' && L.res.failed.why === 'missing' && L.res.done.join() === 'AAA' && L.mock.arrived.length === 2 && L.items.join() === '0send,0check,0ok,1send,1check,1bad' &&
        /NOT ON THE CALCULATOR: it acknowledged the request for DataLoad and sent nothing in 4\.6 s\./.test(L.text), JSON.stringify(L.res) + L.items.join());
  {
    const mock = new MockPrime({ tickMs: 80, drop: ['DataLoad'] }), link = quick(new P.Link(mock.port())), log = [];
    mock.programs.DataLoad = 'EXPORT DataLoad()\nBEGIN\n// the version of last term\nEND;';
    const res = await P.load(link, three, { log: t => log.push(t) }, { settle: 10 });
    mock.stop();
    check('E5 ... and when an older DataLoad is on the calculator and the new one is not kept, the old one comes back: "differs", with both lengths and where they part',
          !res.ok && res.failed.name === 'DataLoad' && res.failed.why === 'differs' && /NOT THE SAME: \d\d characters came back against 40,857 sent; the first difference is at character \d+\./.test(log.join('\n')), JSON.stringify(res.failed));
  }
  L = await run({ cutAt: 30000 }, three);
  check('E6 a calculator that keeps only the first 30,000 characters: "differs", the first difference at character 30,001', L.res.failed.why === 'differs' && L.res.failed.name === 'DataLoad' && /first difference is at character 30,001\./.test(L.text), L.text.slice(-300));
  L = await run({ fdOld: null }, three);
  check('E7 a calculator that still says version 01 after the "FD": "version"; no program is sent and the newer framing is not asked for',
        L.res.failed.why === 'version' && L.res.failed.name === null && L.res.done.length === 0 && L.mock.arrived.length === 0 && !L.mock.v2open && L.items.length === 0 && /IT DOES NOT SPEAK VERSION 03/.test(L.text), JSON.stringify(L.res));
  L = await run({ deadAfter: 0 }, three);
  check('E8 a calculator that answers nothing: "silent", after the 0.6 s allowed; nothing was sent but the question', L.res.failed.why === 'silent' && L.res.ms < 1000 && L.mock.reportsIn === 1 && /NO ANSWER: no answer within 0\.6 s\./.test(L.text), JSON.stringify(L.res));
  L = await run({ dieAt: 40 }, three);
  check('E9 the cable pulled in the middle of the second program: the load ends at once, "gone", with the first program done and no failure invented for the second',
        L.res.gone && !L.res.ok && L.res.failed === null && L.res.done.join() === 'AAA' && L.res.ms < 800 && /THE CALCULATOR WENT OFF THE CABLE/.test(L.text) && !('DataLoad' in L.mock.programs), JSON.stringify(L.res));
  L = await run({ deadAfterNew: 4 }, three);
  check('E10 a calculator that takes the second program and then answers nothing: "unread" (the page cannot tell whether it arrived), not "missing"', L.res.failed.why === 'unread' && L.res.failed.name === 'DataLoad' && L.res.done.join() === 'AAA' && /NOT READ BACK: message \d+ stood/.test(L.text), JSON.stringify(L.res));
  L = await run({ crlf: true }, three);
  check('E11 a calculator that hands a program back with CRLF and a last line end: still the same program', L.res.ok && L.res.done.length === 3);
  L = await run({}, [{ name: 'bad name', source: tiny }]);
  check('E12 a name the calculator would not take is refused before anything of it is sent: "unsent", with the name', L.res.failed.why === 'unsent' && /"bad name" is not a name the calculator takes/.test(L.res.failed.text) && L.mock.arrived.length === 0);
  L = await run({ product: G1, loseAt: 9 }, [{ name: 'EpiStats', source: EPI }, { name: 'ZZZ', source: tiny }]);
  check('E13 the log of a load: a "send again" is always in it, however long the message; the ordinary lines beyond the first forty are counted and left out',
        L.res.ok && /"SEND AGAIN": report 09, position 496, message 2/.test(L.text) && /1 time a report was sent again/.test(L.text) && /\(\d+ more lines of this kind left out\)/.test(L.text) && L.log.length < 200, L.log.length);
  L = await run({ product: G1, muteAt: 5000, tickMs: 0 }, [{ name: 'EpiStats', source: EPI }, { name: 'ZZZ', source: tiny }]);
  check('E14 ... and when a load fails, the last reports that the log had left out are written after the failure, since those are the ones wanted',
        L.res.failed.why === 'unsent' && /\(\d+ more lines of this kind left out\)\n  NOT SENT: message 2 stood for 0\.5 s with 4,\d\d\d of its 9,201 reports acknowledged[^\n]*\n  The last reports before that, which the log had left out:\n(    \. [<>] [^\n]*\n){29}    \. [<>] [^\n]*$/.test(L.text), L.text.slice(-900));

  // ---------------------------------------------------------------- F. the book's programs, every one
  const fleet = progs.map(r => ({ name: r.name, source: src(r) }));
  for (const product of [G1, 0x2441]) {
    const mock = new MockPrime({ product, tickMs: 600 }), link = new P.Link(mock.port());
    let have = 0;
    link.progress = () => { have++; };
    const t = Date.now(), res = await P.load(link, fleet, {}, { settle: 0 });
    mock.stop();
    const whole = fleet.every(p => mock.programs[p.name] === p.source), sent = mock.arrived.reduce((s, a) => s + a.reports, 0), want = product === G1 ? 131683 : 8125;
    check('F' + (product === G1 ? 1 : 2) + ' all ' + fleet.length + ' programs onto a pretend ' + (product === G1 ? 'G1' : 'G2') + ': each read back the same; ' + num(sent) + ' reports of programs, none sent twice, no word of the clock needed (' +
          ((Date.now() - t) / 1000).toFixed(1) + ' s against the mock, which takes a report at once)',
          res.ok && res.done.length === 31 && whole && sent === want && mock.outOfTurn === 0 && mock.nacks === 0 && mock.arrived.every(a => a.kept && a.layout === 'v1' && a.framing === 'new') &&
          mock.waits.every(w => w.ms < 80) && have >= Math.floor(want / 77), JSON.stringify([res.ok, res.done.length, whole, sent, mock.outOfTurn, res.failed]));
  }

  // ---------------------------------------------------------------- G. the log
  {
    const lines = [], tr = new P.Tracer((t, at) => lines.push(t), { budget: 8, keep: 3 });
    const pad = fr => { const x = new Uint8Array(64); x.set(fr); return x; };
    tr.report('>', pad(P.framesV2(new Uint8Array(500).fill(0xAB), 4, 63)[0]), true);
    for (let k = 2; k <= 9; k++) tr.report('>', pad([k, 1, 2, 3]), true);
    tr.report('<', pad(P.ackV2(0x0A, 559, 4, true)), true);
    for (let k = 0; k < 6; k++) tr.report('<', pad(P.ackV2(0xFF, 559, 4, true)), true);
    tr.report('<', pad(P.ackV2(0x0B, 622, 4, false)), true);
    for (let k = 0; k < 9; k++) { tr.report('>', pad([0x0B + k, 9]), true); tr.report('<', pad(P.ackV2(0x0C + k, 685 + 63 * k, 4, true)), true); }
    const tail = tr.tail();
    tr.mark();
    check('G1 the log of reports: a message\'s start with its number, size and first twelve bytes; the reports after it only counted, with their numbers; three of a run of one kind and then their count',
          lines[0] === '> message 4, 500 bytes, begins AB AB AB AB AB AB AB AB AB AB AB AB' && lines[1] === '> 8 more reports of it, numbered 02-09' && lines[2] === '< acknowledgement: report 0A, position 559, message 4' &&
          lines.filter(l => /again \(FF\)/.test(l)).length === 3 + 1 && /^< \.\.\. and 3 more of that kind; the last: the last acknowledgement again/.test(lines[6]) && lines[8] === '> 1 more report of it, numbered 0B', lines.slice(0, 9).join(' | '));
    check('G2 after its budget of ordinary lines the rest are counted, and said at the next line of the caller\'s; a "send again" is written all the same; and the last ones left out can be had',
          lines.some(l => /^< "SEND AGAIN": report 0B, position 622, message 4$/.test(l)) && /^\(\d+ more lines? of this kind left out\)$/.test(lines[lines.length - 1]) && tail.length === 3 &&
          /acknowledgement: report 14, position 1,189/.test(tail[2][0]) && typeof tail[2][1] === 'number', lines.slice(-3).join(' | ') + ' // ' + tail.map(x => x[0]).join(' | '));
  }
  {
    // everything a load can write, against the serial number and the twelve-byte rule, on both report sizes
    let leaks = 0, longest = 0, count = 0;
    for (const product of [G1, 0x2441]) {
      const L2 = await run({ product, loseAt: 3 }, three);
      for (const l of L2.log) {
        count++;
        if (/SECRET|SERIAL/.test(l)) leaks++;
        const m = l.match(/(?:begins|report:) ((?:[0-9A-F]{2} ?)+)/);
        if (m) longest = Math.max(longest, m[1].trim().split(' ').length);
      }
      const hexOf = [...'SECRETSERIAL0001'].map(c => c.charCodeAt(0).toString(16).toUpperCase()).join(' ');
      if (L2.text.includes(hexOf.slice(0, 11))) leaks++;
    }
    check('G3 in ' + count + ' lines of two loads\' logs: no line shows more than twelve bytes of a message, and the serial number, which the mock sends in its answer to "who are you", is in none, as text or as bytes', leaks === 0 && longest === 12 && count > 60, leaks + ' ' + longest + ' ' + count);
  }

  console.log('\n' + pass + ' PASS, ' + fail + ' FAIL');
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
