// prime_usb_v3b.js -- a real HP Prime on its USB cable, from a web page (WebHID).  Roger Metcalf & Claude, 17 Nov 2026.
//
// v3b (18 Nov 2026, 17:45): a rest for the calculator after each program, before the next one is sent (lullFor).
// What the author's calculators did with what Loader v2g sent them, every download verified (the logs of 16:54 and
// 16:59, and Roger's word on what then ran from the Program Catalog):
//     G2  DataLoad      40,856 characters   the next program began 0.54 s after it arrived   Run opened the editor
//     G2  NormExplorer 185,782                                    0.99 s                      ran
//     G2  ScatterLab   115,148                                    0.77 s                      Run opened the editor
//     G2  TestChooser   80,946               the last one                                    ran
//     G1  EpiStats     289,813                                    4.84 s                      the calculator RESET on Run
//     G1  ErrorRate    115,298                                    1.94 s                      ran
//     G1  TrendTest    105,568               the last one                                    ran
// and at 17:28 EpiStats, sent to the G1 ALONE, ran without Check.  A program that needed its Check ran after it.
// So: the last program of a send has always run, and a program with another close behind it sometimes has not.  WHY
// IS NOT KNOWN.  hp-prime-kit measured that a G2 compiles a program that arrives this way, on programs of up to
// 16,558 bytes sent one at a time (usb.send-program); the guess here is that a program sent close behind stops that
// work, and that the G1 had most of EpiStats's 4.84 s taken by the page's own request to have it back (3.95 s of
// compressing).  A fixed 2 s from arrival, v3b's first form (17:05, never on a calculator), would not have helped
// EpiStats.  So the rest is counted from the moment the download is verified, when the calculator has nothing of
// ours left to do, and it grows with the program and is longer on a G1: 2 s, and 0.5 s more for each 100,000
// characters on a G2 (reports of 1,024 bytes) or 2 s more on a G1 (reports of 64).  THESE NUMBERS ARE CHOSEN, NOT
// MEASURED: they are several times the longest time that was seen to fail on a G2, and nothing bounds them on a G1
// but ErrorRate's 1.94 s.  The log says how long each program was given.  The Loader also sends EpiStats in a group
// of its own (build_loader_v2h.py), the one arrangement seen to work for it on a G1.
//
// v3a (18 Nov 2026, 15:50): one outcome more, 'full'.  On 18 Nov at 15:41 the author's G1, sent all 30 programs by
// Loader v2d, took 15 (2,104,376 characters), then acknowledged every report of NormExplorer and, asked for it back,
// sent it EMPTY: 36 bytes, its head and its name, not compressed.  Its Program Catalog showed NormExplorer at 0 KB
// and 4.35 MB of programs (Roger: "I think we're out of memory").  [log] usb/logs/PrimeLoader_v2d_G1_Chrome_2026-11-18_1541.txt
// A send that stands for a minute is "stuck", not "gone" (res.stuck): the G2 of 16:11 the same day, still on its cable,
// took one report of the 14th program and then nothing for 60 s.  And one wait longer: the time given the calculator to begin giving a program back (patienceFor, below), after the
// G2's log of 15:49 the same day, in which that time grew as the load went on and EpiStats outlasted it.  Nothing
// else changed: the route and the pacing are v3's.
//
// WHAT HAS RUN ON A CALCULATOR (logs/, 17 Nov 2026: the author's G2 and his G1, both on firmware build 15751, from
// Chrome and Edge 157 on Windows; the first three logs with prime_usb_v1.js, the two of 21:43 and 21:47 with v2).
// These lines are marked [log] below.
//   * "Who are you" (00 FA) is answered with version 01 by both.  Told "FD 01 00 00 00 01 03" in the OLD framing, each
//     answers the same seven bytes and speaks version 03 from then on, in both framings: its "who are you" says 03 and
//     it sends a file compressed ("F7 03", a zlib stream that begins 78 01).
//   * THE ROUTE THAT WORKS: after that "FD", the newer framing ("FF EC", which neither answers with a report of its
//     own), and in it a program NOT compressed ("F7 01").  300, 8,269, 40,856, 140,000 and 289,813 characters were
//     kept and came back the same from the G2 (the last in 567 reports); the first four came back the same from the
//     G1 (the fourth in 4,445 reports), and the fifth, 9,201 reports, was acknowledged and sent back four times as a
//     message of the G2's own length, to a page that had stopped waiting a tenth of a second before each began.
//   * NOT kept: a program this code compresses ("F7 03", the browser's zlib, which begins 78 9C), in either framing,
//     whether the calculator speaks 01 or 03.
//   * The old framing keeps a program of 254 reports and one of 255 (both calculators), and not one of 274 (G2) or
//     263 (G1); the calculator's own answer of 256 reports is numbered 00 to FE and then 00.
//   * In the newer framing the calculator acknowledges every 77th report of a message as it arrives, with the number
//     of the report it wants next and the room of the reports it has (1,015 for a G2's first and 1,023 for each after;
//     55 and 63 for a G1); when the sender stops in the middle it says where it stands, within 0.7 s, as an
//     acknowledgement or as a "send again"; a report out of turn is answered at once with "send again"; and a whole
//     message with the number of its last report.  While nothing happens it repeats that with FF for the number.
//   * When the calculator sends, it stops once 240 reports' worth is unacknowledged, and goes on when acknowledged.
//   * It takes the calculator a while to begin a long answer, since it compresses it first: 0.9 s (G2) and 3.1 s (G1)
//     for 289,813 characters.
//   * A delete ("EB 01" while it speaks 01, "EB 03" while it speaks 03); the old framing is still answered once the
//     newer has been asked for.
//   * A word that is not an answer to anything: the G2 said "send again" for report 02 just as the second report of
//     its longest message went out, 0.6 s after its last acknowledgement, and then took that report.  So a "send
//     again" may be the calculator's clock and not a lost report, and the page cannot tell which from the word alone.
//   * A G1 whose answer was left unacknowledged after 241 reports answered nothing more in the newer framing; asked
//     "who are you" in the old one, it sent the rest of that answer numbered in the old way (... FE, 00, 01 ...) and
//     then answered.
// WHAT STOPPED EARLIER VERSIONS, each on a real calculator: v1 waited without end, because every repeated
// acknowledgement started its wait again; v2 stopped after 76 reports where the calculator wanted the 77th, so each
// 77 reports cost 0.7 s; it gave a G1 3.0 s to begin an answer that took 3.1; it went back at every "send again" and
// so sent the G2 seven reports twice, each of which brought the next "send again"; and it threw away what was waiting
// before a request, which is how the G1's answer came to stand unacknowledged.
// WHAT OF THIS VERSION HAS NOT RUN ON A CALCULATOR: its pacing (77 reports, the acknowledgement, 77 more, with
// nothing between: the calculators were sent 77 at a time only with 0.7 s between), what it does at a "send again",
// and load() with one of the book's programs.  The tests run it against tests/mock_prime_v3b.js, which is the two
// calculators as far as five logs go.
//
// WHERE EACH FACT NOT FROM THE LOGS COMES FROM (all four MIT; no code of theirs is here, only what they measured or read)
//   [kit]  JordiRigau/hp-prime-kit, docs/topics/usb.md and hpkit/usb.py.  One G2 on firmware 2.4.15515, from Windows,
//          3 to 5 Nov 2026: it kept a program sent as "F7 03", compressed by zlib at level 1 (78 01), in the old framing.
//   [web]  APie357/hp-prime-web, docs/PROTOCOL.md.  One G2, 9 and 10 Nov 2026, old framing: "F7 01", "F8 01" with the
//          name ENDING IN A NUL, "EB 01".
//   [pd]   BeatSkip/PrimeDev (Oscar Spierings), PrimeWeb/Frames and Utility/MessageUtils.cs.  The newer framing, and
//          the bytes of the message "FD 01 00 00 00 01 03".
//   [emu]  golba98/hp-prime-emulator, docs/reverse-engineering.  A reading of HP's Connectivity Kit 2.4.2 r15751 as
//          data: a message's reports are numbered 01, then 02 to FD and 02 again; a window of 76; a retry after 500 ms.
//
// No DOM here.  The page hands Link a port ({reportSize, send, read, poll, drain}); HidPort wraps a WebHID device, and
// the tests hand it the mock.

'use strict';

const PrimeUSB = (function () {

  const VENDOR = 0x03F0;                                                   // [kit] usb.device; [web]
  const MODELS = { 0x2441: 'HP Prime G2', 0x1541: 'HP Prime G1', 0x0441: 'HP Prime G1 (early firmware)' };   // [web], [pd]
  const FILTERS = Object.keys(MODELS).map(function (p) { return { vendorId: VENDOR, productId: Number(p) }; });
  const F7 = 0xF7, F8 = 0xF8, F9 = 0xF9, FA = 0xFA, FD = 0xFD, EB = 0xEB, READY = 0xFF, YES = 0x59, PROGRAM = 0x06;
  const MAX_MESSAGE = 16 * 1024 * 1024;                                    // more than this in one reply is a misread length
  const OLD_MOST = 255;                                                    // [log], [emu]: see framesLegacy
  const STANDS_AT = 240;                                                   // [log]: reports' worth of its own message the calculator leaves unacknowledged
  const WINDOW = 77;                                                       // [log]: the calculator acknowledges every 77th report ([emu] reads 76 in the Kit)

  // ---------------------------------------------------------------- bytes
  function cat() {
    let n = 0;
    for (let i = 0; i < arguments.length; i++) n += arguments[i].length;
    const out = new Uint8Array(n);
    let o = 0;
    for (let i = 0; i < arguments.length; i++) { out.set(arguments[i], o); o += arguments[i].length; }
    return out;
  }
  function u32be(n) { return [(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255]; }
  function u32le(n) { return [n & 255, (n >>> 8) & 255, (n >>> 16) & 255, (n >>> 24) & 255]; }
  function rdU32be(b, o) { return ((b[o] << 24) | (b[o + 1] << 16) | (b[o + 2] << 8) | b[o + 3]) >>> 0; }
  function rdU32le(b, o) { return (b[o] | (b[o + 1] << 8) | (b[o + 2] << 16) | (b[o + 3] << 24)) >>> 0; }
  function utf16le(s) {
    const b = new Uint8Array(s.length * 2);
    for (let i = 0; i < s.length; i++) { const c = s.charCodeAt(i); b[2 * i] = c & 255; b[2 * i + 1] = c >> 8; }
    return b;
  }
  function fromUtf16le(b) {
    const n = b.length >> 1, parts = [];
    for (let i = 0; i < n; i += 8192) {
      const m = Math.min(n, i + 8192), codes = new Array(m - i);
      for (let j = i; j < m; j++) codes[j - i] = b[2 * j] | (b[2 * j + 1] << 8);
      parts.push(String.fromCharCode.apply(null, codes));
    }
    return parts.join('');
  }
  function hex(b, n) {
    const m = Math.min(b.length, n || b.length), out = [];
    for (let i = 0; i < m; i++) out.push((b[i] < 16 ? '0' : '') + b[i].toString(16).toUpperCase());
    return out.join(' ') + (m < b.length ? ' ...' : '');
  }
  function hex2(n) { return (n < 16 ? '0' : '') + n.toString(16).toUpperCase(); }
  function num(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function secs(ms) { return (ms / 1000).toFixed(ms < 9950 ? 1 : 0) + ' s'; }
  function secs2(ms) { return (ms / 1000).toFixed(2) + ' s'; }
  // CRC-16, polynomial 1021, starting from 0 ("XMODEM"): [kit] usb.program-message; [web].
  function crc16(b, from, to) {
    let c = 0;
    for (let i = from || 0, e = to === undefined ? b.length : to; i < e; i++) {
      c ^= b[i] << 8;
      for (let k = 0; k < 8; k++) c = (c & 0x8000) ? ((c << 1) ^ 0x1021) & 0xFFFF : (c << 1) & 0xFFFF;
    }
    return c;
  }
  // The text as the Connectivity Kit stores it: LF line ends, and no newline after the last line.  [kit] program.py
  function normalizeSource(t) {
    const s = String(t).replace(/\r\n/g, '\n').replace(/\r/g, '\n');
    return s.charAt(s.length - 1) === '\n' ? s.slice(0, -1) : s;
  }
  // [kit] takes letters, digits and "_", up to 127 characters; [web] wants a letter or "_" first.  Both rules here.
  function validName(n) { return /^[A-Za-z_][A-Za-z0-9_]{0,62}$/.test(n); }

  // ---------------------------------------------------------------- zlib, by the browser's own streams
  async function pipe(bytes, ts) {
    const w = ts.writable.getWriter();
    w.write(bytes).catch(function () {});
    w.close().catch(function () {});
    return new Uint8Array(await new Response(ts.readable).arrayBuffer());
  }
  function deflate(b) { return pipe(b, new CompressionStream('deflate')); }       // 'deflate' is the zlib format
  function inflate(b) { return pipe(b, new DecompressionStream('deflate')); }

  // ---------------------------------------------------------------- messages
  // [kit] usb.program-message, read from a G2's own message: the part that is compressed is
  //   type 06, the name's length in bytes, a checksum low byte first, the name, the source, 00 00
  // (name and source UTF-16, low byte first), and the checksum is taken over F7 03, that part's length as four bytes
  // big-endian, and the part itself with its checksum bytes at 0.  [pd] HpAppDir.cs builds an app's the same way.
  function innerV3(name, source) {
    const nm = utf16le(name);
    if (nm.length > 255) throw new Error('the name is too long');
    const inner = cat([PROGRAM, nm.length, 0, 0], nm, utf16le(source), [0, 0]);
    const crc = crc16(cat([F7, 0x03], u32be(inner.length), inner));
    inner[2] = crc & 255; inner[3] = crc >> 8;
    return inner;
  }
  // The message: F7 03, the compressed part's length plus 4 (big-endian), the uncompressed length (low byte first),
  // and the zlib stream.  [kit]; [log]: the calculators' own are laid out so, and their checksums come out by the
  // rule above.  [log]: NEITHER CALCULATOR KEPT ONE BUILT HERE, speaking 01 or 03.  The browser's stream begins 78 9C
  // and theirs, like [kit]'s, 78 01; whether that is why is not known.  Nothing that loads a calculator uses this.
  async function programV3(name, source) {
    const inner = innerV3(name, source), stream = await deflate(inner);
    return cat([F7, 0x03], u32be(stream.length + 4), u32le(inner.length), stream);
  }
  // The older layout, nothing compressed: F7 01, a length (big-endian), type, name length, checksum, name, source.
  // The checksum is taken over all but the last six bytes, its own two at 0, and no NUL follows the source.
  // [web]; [log]: both calculators kept it.
  function programV1(name, source) {
    const nm = utf16le(name);
    if (nm.length > 255) throw new Error('the name is too long');
    const body = cat([PROGRAM, nm.length, 0, 0], nm, utf16le(source));
    const msg = cat([F7, 0x01], u32be(body.length), body);
    const crc = crc16(msg, 0, msg.length - 6);
    msg[8] = crc & 255; msg[9] = crc >> 8;
    return msg;
  }
  // F8 asks for a file and EB deletes one: cmd, version, length, type, name length, checksum (over all but the last
  // six bytes), name.  [web]: the name of a request must end in a NUL, counted in its length; a delete's must not.
  // [log]: both hold on build 15751.
  function named(cmd, ver, name, nul) {
    const nm = nul ? cat(utf16le(name), [0, 0]) : utf16le(name);
    if (nm.length > 255) throw new Error('the name is too long');
    const msg = cat([cmd, ver], u32be(4 + nm.length), [PROGRAM, nm.length, 0, 0], nm);
    const crc = crc16(msg, 0, msg.length - 6);
    msg[8] = crc & 255; msg[9] = crc >> 8;
    return msg;
  }
  function requestMessage(name, ver, nul) { return named(F8, ver || 1, name, nul !== false); }
  function deleteMessage(name, ver) { return named(EB, ver || 1, name, false); }
  // "The newest version of the messages that I speak is 03."  [pd] names the command (MAX_PROT_VER, FD) and holds, as
  // the first message of a session, the seven bytes of the 'long' form.  [log]: both calculators answer the long form
  // with the same seven bytes, in the old framing, and speak version 03 from then on.  The 'short' form is the two
  // bytes [pd]'s table of commands would give; it has not been sent to a calculator.
  function maxVersionMessage(kind) { return kind === 'short' ? Uint8Array.of(FD, 0x03) : Uint8Array.of(FD, 0x01, 0, 0, 0, 0x01, 0x03); }

  // ---------------------------------------------------------------- framing
  // The old framing: a report is a sequence number and up to cap bytes; the number starts at 00 and counts up, FE is
  // followed by 00, and FF is never a sequence number.  [web], from hplp; [log]: a calculator's own answer of 256
  // reports is numbered so.  [log]: both calculators kept a program of 255 reports and neither one of more (274 on
  // the G2, 263 on the G1; [emu]'s G1: 259), so OLD_MOST is 255.
  function framesLegacy(msg, cap) {
    const out = [];
    let seq = 0, o = 0;
    do {
      const piece = msg.subarray(o, o + cap), r = new Uint8Array(1 + piece.length);
      r[0] = seq; r.set(piece, 1); out.push(r);
      o += piece.length;
      seq = seq === 0xFE ? 0 : seq + 1;
    } while (o < msg.length);
    return out;
  }
  // The newer framing: the first report is 01, a message number and the message's size (each four bytes, low byte
  // first), then up to cap - 8 bytes; the reports after it are a sequence number and up to cap bytes.  [pd], [kit].
  // The numbers run 02 to FD and then 02 again.  [emu]; [log]: 9,201 reports of a G1 went so, and the calculators'
  // own long answers are numbered so.
  function framesV2(msg, id, cap) {
    if (msg.length > MAX_MESSAGE) throw new Error('this message is ' + num(msg.length) + ' bytes, more than this page sends as one');
    const out = [], first = cap - 8;
    out.push(cat([0x01], u32le(id), u32le(msg.length), msg.subarray(0, first)));
    let seq = 2;
    for (let o = first; o < msg.length; o += cap) { out.push(cat([seq], msg.subarray(o, o + cap))); seq = seq === 0xFD ? 2 : seq + 1; }
    return out;
  }
  // What an acknowledgement's position counts: the room of the reports taken, 1,015 for a G2's first and 1,023 for
  // each after it (55 and 63 for a G1).  [log]: 1,015 after one report of a G2, 370 after six of a G1.
  function roomAfter(k, cap) { return k < 1 ? 0 : (cap - 8) + (k - 1) * cap; }
  function reportsAt(pos, cap) { return pos < cap - 8 ? 0 : 1 + Math.floor((pos - (cap - 8)) / cap); }
  // An acknowledgement: FE, 01 (or 00 for "send again"), a sequence number, 00, a position and the message number.
  // [pd], [kit]; [log]: the calculators' own are laid out so.
  function ackV2(seq, pos, id, ok) { return cat([0xFE, ok === false ? 0 : 1, seq, 0], u32le(pos), u32le(id)); }
  const V2_OPEN = Uint8Array.of(0xFF, 0xEC, 0, 0, 0, 0, 0, 0);          // [pd], [kit] usb.newer-framing, [emu]
  const RELEASE = Uint8Array.of(0x01);                                     // [kit] the report that followed every send

  // ---------------------------------------------------------------- what the calculator sends
  // The information reply: the build number two bytes low byte first, 36 bytes from the end; ten characters 32 from
  // the end ("V2.060.650" on a G2 and "V0.050.640" on a G1, whatever the firmware: [log], [emu]).  The serial number
  // is 16 from the end, and it is not read.  [kit] identify; [web]
  function parseInfo(body) {
    const n = body.length;
    if (n < 36) throw new Error('the calculator answered with ' + n + ' bytes of information, and at least 36 were expected');
    let v = '';
    for (let i = n - 32; i < n - 22 && body[i] !== 0; i++) v += String.fromCharCode(body[i]);
    return { build: body[n - 36] | (body[n - 35] << 8), version: v.replace(/[^\x20-\x7e]/g, '?') };
  }
  // A file from the calculator, in either layout.  -> {ver, type, name, data, text, compressed, crcOk}
  async function parseFile(msg) {
    if (msg.length < 10 || msg[0] !== F7) throw new Error('not a file: it begins ' + hex(msg, 8));
    const strip = function (s) { return s.replace(/\u0000+$/, ''); };
    // [kit]: after the six-byte head, the uncompressed length (low byte first) and a zlib stream, which starts 78.
    if (msg.length > 12 && msg[10] === 0x78 && ((msg[10] << 8) | msg[11]) % 31 === 0) {
      let inner = null;
      try { inner = await inflate(msg.subarray(10)); } catch (e) { inner = null; }
      if (inner && inner.length >= 4) {
        if (inner[0] === F7) {                       // [web]'s other reading: a whole old-layout message inside
          const f = await parseFile(inner); f.compressed = true; return f;
        }
        const nl = inner[1], crc = inner[2] | (inner[3] << 8), z = inner.slice();
        z[2] = 0; z[3] = 0;
        const data = inner.subarray(4 + nl);
        return { ver: msg[1], type: inner[0], name: strip(fromUtf16le(inner.subarray(4, 4 + nl))), data: data,
                 text: strip(fromUtf16le(data)), compressed: true, lengthOk: inner.length === rdU32le(msg, 6),
                 crcOk: crc16(cat([F7, msg[1]], u32be(z.length), z)) === crc };
      }
    }
    const nl = msg[7], crc = msg[8] | (msg[9] << 8), z = msg.slice();
    z[8] = 0; z[9] = 0;
    const data = msg.subarray(10 + nl);
    return { ver: msg[1], type: msg[6], name: strip(fromUtf16le(msg.subarray(10, 10 + nl))), data: data,
             text: strip(fromUtf16le(data)), compressed: false, lengthOk: rdU32be(msg, 2) + 6 === msg.length,
             crcOk: crc16(z, 0, z.length - 6) === crc };
  }

  // One report, for a log: what kind it is and a line about it.  Only a report that starts a message has any of its
  // content shown, twelve bytes of it at most; the serial number is in the last sixteen of 108.
  // -> {kind: 'start' | 'more' | 'ack' | 'control', seq, key, text, loud: a line a log should never leave out}
  // expect: in the old framing, the number the next report of the message in hand will carry.  Such a report is
  // counted as carrying the message on whatever its bytes look like ([log]: one numbered FE read as an acknowledgement).
  function describe(r, v2, expect) {
    const s = r[0];
    if (!v2 && expect !== undefined && s === expect) return { kind: 'more', seq: s, key: 'm', text: 'report ' + hex2(s) };
    if (s === 0xFF) return { kind: 'control', key: 'c', loud: true, text: 'a control report: ' + hex(r.subarray(0, 12)) };
    if (s === 0xFE && r.length >= 12 && r[1] <= 1 && r[3] === 0) {
      const id = rdU32le(r, 8), again = r[1] === 1 && r[2] === 0xFF;
      return { kind: 'ack', key: (again ? 'r' : 'a') + id + (r[1] ? '' : 'n'), seq: r[2], ok: r[1] === 1, pos: rdU32le(r, 4), id: id, loud: r[1] !== 1,
               text: (again ? 'the last acknowledgement again (FF)' : (r[1] ? 'acknowledgement' : '"SEND AGAIN"') + ': report ' + hex2(r[2])) + ', position ' + num(rdU32le(r, 4)) + ', message ' + id };
    }
    if (v2 && s === 0x01) {
      const body = r.subarray(9);
      return { kind: 'start', seq: 1, text: 'message ' + rdU32le(r, 1) + ', ' + num(rdU32le(r, 5)) + ' bytes, begins ' + hex(body.subarray(0, body[0] === FA ? 6 : 12)) };
    }
    if (v2 && s === 0x00) return { kind: 'start', seq: 0, text: 'a report of the OLD framing, begins ' + hex(r.subarray(1, r[1] === FA ? 7 : 13)) };
    if (!v2 && s === 0x00) return { kind: 'start', seq: 0, text: 'message begins ' + hex(r.subarray(1, r[1] === FA ? 7 : 13)) };
    return { kind: 'more', seq: s, key: 'm', text: 'report ' + hex2(s) };
  }
  // 00 01 02 ... as "00-FE,00-3A": what a long message's sequence numbers did.
  function runs(a) {
    const out = [];
    for (let i = 0; i < a.length;) {
      let j = i;
      while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++;
      out.push(hex2(a[i]) + (j > i ? '-' + hex2(a[j]) : ''));
      i = j + 1;
    }
    return out.length > 6 ? out.slice(0, 3).join(',') + ', ... ,' + out.slice(-2).join(',') + ' (' + out.length + ' runs)' : out.join(',');
  }

  // ---------------------------------------------------------------- a log of the reports that pass
  // emit(text, at): a line, and the time (Date.now()) of the first report it tells of.
  // A line for each report that starts a message, acknowledges or controls, the first three of any run of one kind
  // and then their count; the reports that carry a message on are only counted, with their numbers.  After `budget`
  // lines since mark() the ordinary ones are counted and not written (a "send again" and a control report always
  // are); the last `keep` of those left out can be had with tail(), for when something has gone wrong.
  function Tracer(emit, opts) {
    opts = opts || {};
    const budget = opts.budget || 40, keep = opts.keep === undefined ? 30 : opts.keep;
    let run = null, serial = 0, left = budget, dropped = 0, ring = [];
    const out = function (text, at, loud) {
      if (loud) emit(text, at);
      else if (left > 0) { left--; emit(text, at); }
      else { dropped++; if (keep) { ring.push([text, at]); if (ring.length > keep) ring.shift(); } }
    };
    const over = function (r) { return r.t1 - r.t0 >= 100 ? ', over ' + secs(r.t1 - r.t0) : ''; };
    const flush = function () {
      if (!run) return;
      const r = run;
      run = null;
      if (r.kind === 'more') out(r.dir + ' ' + num(r.count) + ' more report' + (r.count === 1 ? '' : 's') + ' of it, numbered ' + runs(r.seqs) + over(r), r.t0);
      else if (r.count > r.shown) out(r.dir + ' ... and ' + num(r.count - r.shown) + ' more of that kind' + over(r) + '; the last: ' + r.last, r.t0);
    };
    this.report = function (dir, rep, v2, expect) {
      const d = describe(rep, v2, expect), key = dir + d.kind + (d.kind === 'start' ? ++serial : (d.key || '')), now = Date.now();
      if (run && run.key === key) {
        run.count++; run.t1 = now; run.last = d.text;
        if (d.kind === 'more') { if (run.seqs.length < 20000) run.seqs.push(d.seq); }
        else if (run.count <= 3) { run.shown = run.count; out(dir + ' ' + d.text, now, d.loud); }
        return;
      }
      flush();
      run = { key: key, dir: dir, kind: d.kind, count: 1, shown: d.kind === 'more' ? 0 : 1, t0: now, t1: now, last: d.text, seqs: d.kind === 'more' ? [d.seq] : null };
      if (d.kind !== 'more') out(dir + ' ' + d.text, now, d.loud);
    };
    // A line of the caller's own follows: what was counted is said, and the count starts again.
    this.mark = function () {
      flush();
      if (dropped) emit('(' + num(dropped) + ' more line' + (dropped === 1 ? '' : 's') + ' of this kind left out)', Date.now());
      dropped = 0; left = budget; ring = [];
    };
    // The last lines left out since mark(): [[text, at]].
    this.tail = function () { flush(); const t = ring; ring = []; dropped -= t.length; return t; };
  }

  // ---------------------------------------------------------------- the link
  function Silent(what) { this.name = 'Silent'; this.message = what; }       // nothing came in the time allowed
  Silent.prototype = Object.create(Error.prototype);
  function Cut(what) { this.name = 'Cut'; this.message = what; }             // something came, and it broke off or made no sense
  Cut.prototype = Object.create(Error.prototype);
  function Gone(what) { this.name = 'Gone'; this.message = what; }           // the calculator is no longer on the cable
  Gone.prototype = Object.create(Error.prototype);
  function isGone(e) { return !!e && e.name === 'Gone'; }
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function said(e) { return String(e && e.message ? e.message : e).replace(/[.\s]+$/, ''); }

  // port: {reportSize, send(Uint8Array) -> Promise, read(ms) -> Promise<Uint8Array|null>, poll() -> Uint8Array|null,
  //        drain() -> count}.  A port whose calculator has gone rejects with an error named 'Gone'.
  // hooks: {note(text), trace(dir, report, v2, expect), progress(have, of)}.  Every report that goes out or comes in
  // passes trace, so that a log can show what the calculator did and not only what this code made of it.
  function Link(port, hooks) {
    hooks = typeof hooks === 'function' ? { note: hooks } : (hooks || {});
    this.port = port;
    this.cap = port.reportSize - 1;
    this.note = hooks.note || function () {};
    this.trace = hooks.trace || function () {};
    this.v2 = false;
    this.id = 1;                    // the newer framing's message number
    this.stash = [];                // reports that came while a message was going out, and are not acknowledgements of it
    this.window = WINDOW;
    this.progress = hooks.progress || null;      // (reports the calculator has, reports in the message), as it acknowledges
    // release: [kit]'s gap before the report "01".  stall: how long a pause in a reply counts as the calculator waiting
    // for us.  ack: how long the calculator may leave a message where it stands before the message is given up.
    // back: after one report is sent again, how long to listen for what the calculator says to it.  quiet: a word
    // that comes this long after our last report was sent knows of every report we sent.
    this.pace = { release: 250, stall: 300, ack: 5000, back: 40, quiet: 100, erase: 300 };
    this.last = null;
  }

  Link.prototype.tx = async function (frame, expect) { this.trace('>', frame, this.v2, expect); await this.port.send(frame); };
  // What comes next, within ms.  The stash first.
  Link.prototype.rx = async function (ms, expect) {
    if (this.stash.length) return this.stash.shift();
    const r = await this.port.read(ms);
    if (r) this.trace('<', r, this.v2, expect);
    return r;
  };
  Link.prototype.rawNow = function () { const r = this.port.poll(); if (r) this.trace('<', r, this.v2); return r; };
  // Before a request: what is waiting belongs to something earlier.  It goes through the trace, not into the dark.
  Link.prototype.clear = function () {
    let n = this.stash.length;
    this.stash = [];
    for (let r = this.rawNow(); r; r = this.rawNow()) n++;
    return n;
  };

  // ---- the old framing
  // -> {reports, ms, slow: [{report, ms}]}: slow is where the cable stood ([log]: 49 s somewhere in 274 reports).
  Link.prototype.sendLegacy = async function (msg) {
    const frames = framesLegacy(msg, this.cap), slow = [], t0 = Date.now();
    for (let i = 0; i < frames.length; i++) {
      const t = Date.now();
      await this.tx(frames[i], i ? frames[i][0] : undefined);
      const ms = Date.now() - t;
      if (ms >= 250 && slow.length < 8) slow.push({ report: i + 1, ms: ms });
    }
    return { reports: frames.length, ms: Date.now() - t0, slow: slow };
  };
  // One reply in the old framing.  cmds: the first bytes that count as this reply.  A report that is not the start
  // of it is passed over, and does not lengthen the wait: `first` ms for the reply to begin, counted once, and `then`
  // ms between two reports of it.  -> the message, from its command byte on.
  // fits(report): a further test of a report that looks like the start ([log]: a G1 sent 1,862 reports of an earlier
  // answer, numbered in the old way, before the answer asked for, and one in 256 of those numbered 00 would pass for
  // the start of any reply).
  Link.prototype.recvLegacy = async function (cmds, first, then, fits) {
    const end = Date.now() + first;
    let buf = null, total = 0, got = 0, seq = 0, n = 0, last = 0, skipped = 0;
    const firsts = [];
    for (;;) {
      const left = (buf === null ? end : last + then) - Date.now(), r = left > 0 ? await this.rx(left, buf === null ? undefined : seq) : null;
      if (!r) {
        if (buf === null) throw new Silent('no answer within ' + secs(first) + (skipped ? ' (' + skipped + ' other report' + (skipped === 1 ? '' : 's') + ' came)' : ''));
        throw new Cut('the reply stopped after ' + num(got) + ' of ' + num(total) + ' bytes, ' + n + ' report' + (n === 1 ? '' : 's') + ', numbered ' + runs(firsts));
      }
      const s = r[0];
      if (buf === null) {
        if (s !== 0x00 || cmds.indexOf(r[1]) < 0 || (fits && !fits(r))) { skipped++; continue; }
        if (r[1] === YES || r[1] === READY) return r.slice(1, 2);
        total = 6 + rdU32be(r, 3);
        if (total > MAX_MESSAGE) throw new Cut('the reply claims ' + num(total) + ' bytes: ' + hex(r, 8));
        buf = new Uint8Array(total);
      } else {
        if (s === 0xFF) continue;                                  // never a sequence number: [web], [kit]
        if (s !== seq) {
          if (s === 0xFE) continue;                                // an acknowledgement of the newer framing: [kit]
          if (!(seq === 0xFE && s === 0x00))                       // (a sender that keeps FE for itself wraps one early)
            throw new Cut('the reply came out of order: report ' + hex2(s) + ' where ' + hex2(seq) + ' was next, after ' + num(got) + ' of ' + num(total) + ' bytes; numbered ' + runs(firsts));
        }
      }
      const take = Math.min(total - got, r.length - 1);
      buf.set(r.subarray(1, 1 + take), got);
      got += take; n++; firsts.push(s); last = Date.now();
      seq = s === 0xFE ? 0 : s + 1;
      if (got >= total) { this.last = { reports: n, numbered: runs(firsts) }; return buf; }
    }
  };

  // ---- the newer framing
  // Opening it is one report.  [emu] reads in the Kit an answer to it, a control report that chooses a mode; [log]:
  // neither calculator sent one within 0.9 s, and both took the newer framing all the same.  Whatever does come in
  // the next `listen` ms is handed back for a log.
  // -> {replies: [hex], others: count}
  Link.prototype.openV2 = async function (listen) {
    this.clear();
    await this.tx(V2_OPEN);
    this.v2 = true;
    const end = Date.now() + (listen || 600), replies = [];
    let others = 0;
    for (;;) {
      const left = end - Date.now(), r = left > 0 ? await this.rx(left) : null;
      if (!r) break;
      if (r[0] === 0xFF) { if (replies.length < 4) replies.push(hex(r.subarray(0, 12))); } else others++;
    }
    return { replies: replies, others: others };
  };
  // Send one message.  [log]: the calculator acknowledges every 77th report as it arrives, so 77 go out and then the
  // sending waits for that acknowledgement (in the logs, whose clock shows tenths of a second, it follows the 77th
  // report at once).
  // Every word of the calculator's about this message, an acknowledgement or a "send again", carries the room of the
  // reports it has, and that is what is believed.  When it has FEWER than were sent:
  //   * a "send again" is acted on at once, and so is any word that comes while the sending stands and `pace.quiet`
  //     after the last report went (by then the calculator knows of every report): ONE report is sent again, the first
  //     it says it has not got, and then the page listens for `pace.back`.  If the calculator had that report already
  //     ([log]: its clock spoke while reports were on their way) it says so at once, with what it has, and the sending
  //     goes on from there; if it had not, it takes the report in silence and the sending goes on after it.
  //   * an acknowledgement that comes while reports are still going out is only a count: more are on their way.
  // A word that claims more reports than have been sent is about some other message of this number, and is passed
  // over.  The message is through when a position covers it, or when the calculator starts an answer of its own.
  // It is given up when neither side has moved it for `wait` ms.
  // -> {id, reports, ms, acks: [{ms, ok, seq, pos, sent}], backs: times it went back, again: reports that went a second
  //     time, slow, implied}
  Link.prototype.sendV2 = async function (msg, wait) {
    wait = wait || this.pace.ack;
    const id = this.id++, cap = this.cap, frames = framesV2(msg, id, cap), n = frames.length, acks = [], slow = [], t0 = Date.now(), self = this;
    let acked = 0, i = 0, top = 0, best = -1, backs = 0, again = 0, probe = false, backPos = -1, backAt = 0, lastTx = 0, moved = Date.now(), implied = false, own = 0;
    const take = function (r, quiet) {
      if (r[0] === 0xFF) return;
      if (r[0] !== 0xFE) {                                         // not an acknowledgement: it is kept for whoever reads next
        self.stash.push(r);
        if (top >= n && r[0] === 0x01) implied = true;             // the calculator is answering, so it has the message
        return;
      }
      if (r.length < 12 || rdU32le(r, 8) !== id) return;           // about an earlier message (they repeat: [log])
      const ok = r[1] === 0x01, pos = rdU32le(r, 4), k = pos >= msg.length ? n : Math.min(n, reportsAt(pos, cap));
      if (k > top) return;                                         // more than has been sent
      if (acks.length < 600) acks.push({ ms: Date.now() - t0, ok: ok, seq: r[2], pos: pos, sent: i });
      // a word that is neither at a 77th report nor at the end is the calculator's own (its clock, or a report out of turn): the first few are told
      if (k < n && k % self.window !== 0 && ++own <= 4)
        self.note('  (' + secs2(Date.now() - t0) + ' into message ' + id + ' the calculator said ' + (ok ? 'where it stands' : '"send again"') + ': it has ' + num(k) + ' of the ' + num(n) + ' reports; ' + num(i) + ' had been sent)');
      if (pos > best) { best = pos; moved = Date.now(); }
      if (k > acked) { acked = k; if (self.progress) self.progress(acked, n); }
      if (k > i) i = k;                                            // it has more than this pass has sent: go on from there
      if (k >= i) return;
      if (pos === backPos && Date.now() - backAt < self.pace.quiet) return;     // the same word again, from before the report sent again arrived
      if (!ok || quiet) { i = k; backs++; probe = true; backPos = pos; backAt = Date.now(); }
    };
    while (acked < n && !implied) {
      if (Date.now() - moved > wait) {
        const a = acks.length ? acks[acks.length - 1] : null;
        throw new Silent('message ' + id + ' stood for ' + secs(wait) + ' with ' + num(acked) + ' of its ' + num(n) + ' report' + (n === 1 ? '' : 's') + ' acknowledged' +
                         (a ? '; the calculator last said ' + (a.ok ? '' : '"send again", ') + 'report ' + hex2(a.seq) + ', position ' + num(a.pos) : '; the calculator said nothing'));
      }
      if (i < n && i - acked < this.window) {
        const t = Date.now();
        await this.tx(frames[i]);
        lastTx = Date.now();
        if (lastTx - t >= 250 && slow.length < 8) slow.push({ report: i + 1, ms: lastTx - t });
        if (i < top) again++;                                      // this one has gone before
        i++;
        if (i > top) { top = i; moved = lastTx; }
        if (probe) {                                               // one report sent again: what does the calculator say to it?
          probe = false;
          const r = await this.port.read(this.pace.back);
          if (r) { this.trace('<', r, this.v2); take(r, false); }
        }
        for (let r = this.rawNow(); r; r = this.rawNow()) take(r, false);
        continue;
      }
      // 77 are out, or all of it is: the calculator owes a word
      const left = moved + wait - Date.now(), r = left > 0 ? await this.port.read(Math.min(left, 1000)) : null;
      if (!r) continue;
      this.trace('<', r, this.v2);
      take(r, Date.now() - lastTx >= this.pace.quiet);
    }
    return { id: id, reports: n, ms: Date.now() - t0, acks: acks, backs: backs, again: again, slow: slow, implied: implied };
  };
  // One message from the calculator in the newer framing.  `first` ms for it to begin, counted once whatever else
  // arrives; `then` ms between two of its reports.
  // [log]: the calculator stops once 240 reports' worth is unacknowledged, and goes on when it is acknowledged with
  // the number of the last report that came and the room of all that have come; a G1 took that after 240 reports
  // and after 241, again and again through 2,103.  So that is what is sent, each time 240 reports' worth has come
  // since the last, and at the end.  If the calculator stops in the middle all the same, what has come is
  // acknowledged once more after `pace.stall` ms.
  // A report again (a retry of the calculator's) is dropped; a gap asks, once, for the missing one.
  Link.prototype.recvV2 = async function (cmds, first, then) {
    const end = Date.now() + first, cap = this.cap;
    let m = null;
    for (;;) {
      const now = Date.now();
      let wait;
      if (m === null) wait = end - now;
      else {
        const idle = now - m.at;
        if (idle >= then) throw new Cut('the reply stopped after ' + num(m.got) + ' of ' + num(m.total) + ' bytes, ' + num(m.n) + ' report' + (m.n === 1 ? '' : 's') + ' of message ' + m.id);
        wait = m.nudged === m.n ? then - idle : Math.min(then - idle, Math.max(1, this.pace.stall - idle));
      }
      const r = wait > 0 ? await this.rx(wait) : null;
      if (!r) {
        if (m === null) throw new Silent('no answer within ' + secs(first));
        if (m.nudged !== m.n && Date.now() - m.at >= this.pace.stall) {            // it may be waiting for us
          await this.tx(ackV2(m.seq, roomAfter(m.n, cap), m.id, true));
          m.nudged = m.n; m.ackedAt = m.n; m.stalls.push(m.n);
        }
        continue;
      }
      const s = r[0];
      if (s === 0xFE || s === 0xFF) continue;                      // acknowledgements of our own messages (they repeat), and control reports
      if (s === 0x00) {                                            // a report of the old framing
        if (m === null && cmds.indexOf(r[1]) >= 0) {               // ... which begins what we wait for: [log] the old framing is still answered
          if (!this.mixed) this.note('  (the answer came in the OLD framing, though the newer one is open)');
          this.mixed = (this.mixed || 0) + 1;
          this.stash.unshift(r);
          return this.recvLegacy(cmds, Math.max(1, end - Date.now()), then);
        }
        continue;                                                   // otherwise the trace has it
      }
      if (s === 0x01) {
        const id = rdU32le(r, 1), total = rdU32le(r, 5);
        if (m !== null && id === m.id) { m.again++; continue; }    // its first report again
        if (total > MAX_MESSAGE) throw new Cut('the reply claims ' + num(total) + ' bytes: ' + hex(r, 9));
        m = { id: id, total: total, buf: new Uint8Array(total), got: 0, n: 1, seq: 1, next: 2, at: Date.now(), nudged: 0, ackedAt: 0, asked: 0, stalls: [], acks: 0, again: 0, gaps: 0 };
        const take = Math.min(total, r.length - 9);
        m.buf.set(r.subarray(9, 9 + take), 0); m.got = take;
      } else {
        if (m === null) continue;                                   // the tail of something that began before we listened
        if (s !== m.next) {
          const behind = ((m.next - s) + 252) % 252;                // the numbers 02 to FD go round: [emu], [log]
          if (behind >= 1 && behind <= 126) { m.again++; continue; }                // one we have: a retry of the calculator's
          m.gaps++;
          if (m.asked !== m.n) { m.asked = m.n; await this.tx(ackV2(m.next, roomAfter(m.n, cap), m.id, false)); }   // one is missing: ask for it
          continue;
        }
        const take = Math.min(m.total - m.got, r.length - 1);
        m.buf.set(r.subarray(1, 1 + take), m.got);
        m.got += take; m.n++; m.seq = s; m.next = s === 0xFD ? 2 : s + 1; m.at = Date.now();
      }
      if (m.got >= m.total) {
        await this.tx(ackV2(m.seq, roomAfter(m.n, cap), m.id, true));
        const done = m;
        m = null;
        this.last = { reports: done.n, numbered: 'message ' + done.id, id: done.id, stalls: done.stalls, acks: done.acks + 1, again: done.again, gaps: done.gaps };
        if (cmds.indexOf(done.buf[0]) >= 0) return done.buf;
        continue;                                                   // some other message: acknowledged, and the trace has it
      }
      if (roomAfter(m.n, cap) - roomAfter(m.ackedAt, cap) >= STANDS_AT * cap) {       // before the calculator has to stand
        await this.tx(ackV2(m.seq, roomAfter(m.n, cap), m.id, true));
        m.ackedAt = m.n; m.acks++;
      }
    }
  };

  // Before a request in the newer framing: what is waiting belongs to something earlier.  A message of the
  // calculator's among it, whole or begun, is taken to its end and acknowledged, because [log] a G1 whose answer was
  // left unacknowledged after 241 reports answered nothing more.  -> how many reports were waiting
  Link.prototype.settle = async function () {
    const keep = [];
    let n = 0;
    for (let r = this.stash.shift() || this.rawNow(); r; r = this.stash.shift() || this.rawNow()) { n++; if (r[0] !== 0xFE && r[0] !== 0xFF) keep.push(r); }
    if (keep.length) { this.stash = keep; await this.swallow(80, 1500); }
    return n;
  };
  // Send a message in the link's framing, after dealing with whatever was waiting.
  Link.prototype.send = async function (msg) {
    if (this.v2) { await this.settle(); return this.sendV2(msg); }
    this.clear();
    return this.sendLegacy(msg);
  };
  Link.prototype.recv = function (cmds, first, then, fits) {
    return this.v2 ? this.recvV2(cmds, first, then || 2500) : this.recvLegacy(cmds, first, then || 2500, fits);
  };

  // Listen for ms and take nothing: whatever comes is passed over, and in the newer framing a whole message is
  // acknowledged all the same, so that the calculator does not go on sending it.  [log]: the G1 sent one file
  // several times for one request, and a late copy must not be taken for the answer to the next.
  Link.prototype.swallow = async function (ms, then) {
    try { await this.recv([], ms, then || Math.min(ms, 2500)); }
    catch (e) { if (!(e instanceof Silent) && !(e instanceof Cut)) throw e; }
  };

  // -> {build, version, bytes, ver}.  [kit]: "00 FA" was answered by "00 FA 03 00 00 00 6C"; [log]: by version 01.
  Link.prototype.info = async function (first) {
    await this.send(Uint8Array.of(FA));
    const r = await this.recv([FA], first || 3000, 0, function (x) { return x[2] <= 9 && rdU32be(x, 3) >= 36 && rdU32be(x, 3) <= 4096; });
    const i = parseInfo(r.subarray(6));
    i.bytes = r.length - 6; i.ver = r[1];
    return i;
  };
  // [web]: FF is answered by the one byte 59, "Y".
  Link.prototype.ready = async function (first) {
    await this.send(Uint8Array.of(READY));
    try { const r = await this.recv([YES, READY], first || 2000); return r[0] === YES || r[0] === READY; }
    catch (e) { if (e instanceof Silent) return false; throw e; }
  };
  // "FD": see maxVersionMessage.  -> {reports, acks, reply}: reply is how an answer of its own began, or null.
  Link.prototype.maxVersion = async function (kind, listen) {
    const out = await this.send(maxVersionMessage(kind));
    let reply = null;
    try { reply = hex((await this.recv([FD], listen || 900, 900)).subarray(0, 12)); }
    catch (e) { if (!(e instanceof Silent)) throw e; }
    return { reports: out.reports, acks: out.acks || null, reply: reply };
  };
  // How long to give a calculator to BEGIN sending a program of so many characters back.  [log] 17 Nov: it compresses
  // the program first, and a G1 took 3.1 s over 289,813 characters, a G2 0.9 s; v3 allowed 3 s and 0.04 ms a
  // character (14.6 s for EpiStats).  [log] 18 Nov, 15:49, the G2 sent all 30 by Loader v2d: the time before each
  // answer GREW as the load went on, though the programs did not (ChiTable 4.4 s where it had taken 0.6 s by itself
  // at 15:31; DataLoad, 40,856 characters, 2.2 s; DNAMixLR 8.0 s), and EpiStats did not begin within its 14.6 s.
  // Why it grew is not known.  So v3a allows 30 s and 0.1 ms a character (59 s for EpiStats).  The calculator's
  // "where it stands" words keep coming every 0.6 s whether it is busy or not, so they say nothing here.  The cost:
  // a program the calculator did not keep is called missing that much later.
  function patienceFor(chars) { return 30000 + Math.ceil(0.1 * (chars || 0)); }
  // The rest a program is given once its download is verified, before the next program is sent: see v3b, at the
  // top.  Chosen, not measured.  reportSize: 64 on a G1, 1,024 on a G2.
  function lullFor(chars, reportSize) { return 2000 + Math.ceil((reportSize && reportSize <= 64 ? 2000 : 500) * (chars || 0) / 100000); }
  // Open a session the way both calculators took it on 17 Nov [log]: who are you; "FD" if it speaks 01, and who are
  // you again; then the newer framing, and who are you in it, so that the framing is known to work before any program
  // goes.  The newer framing is asked for only of a calculator that now speaks 03 (what one that still speaks 01
  // does with the rest of the route has not been seen).  say(text): what happened, for a log.
  // -> {info, ver, told: whether "FD" was sent, reply: how its answer began or null, open: the newer framing was asked for}
  Link.prototype.begin = async function (first, say) {
    say = say || function () {};
    let info = await this.info(first), told = false, reply = null;
    say('It answered: firmware build ' + info.build + ', "' + info.version + '", version ' + hex2(info.ver) + '. Its reports carry ' + num(this.cap) + ' bytes each.');
    if (info.ver !== 3) {
      told = true;
      reply = (await this.maxVersion('long')).reply;
      info = await this.info(first);
      say('Told that this page speaks version 03 ("FD 01 00 00 00 01 03"), ' + (reply ? 'it answered ' + reply : 'it sent no answer') + ', and it now answers with version ' + hex2(info.ver) + '.');
    }
    if (info.ver === 3) {
      await this.openV2(150);
      const again = await this.info(first);
      say('Asked for the newer framing ("FF EC"), and who it is in that framing: it answers, with version ' + hex2(again.ver) + '.');
    }
    return { info: info, ver: info.ver, told: told, reply: reply, open: info.ver === 3 };
  };
  // [kit]: a report "01" followed every program it sent in the old framing.
  Link.prototype.release = async function () { await this.tx(RELEASE); };

  // how: {layout: 'v1' (not compressed: what both calculators kept) | 'v3', release: true | false, listen: ms}; the
  // framing is the link's.
  // Nothing acknowledges a program in the old framing ([kit], [web], [log]), so "sent" is all this can say there;
  // in the newer one the acknowledgement says the reports arrived, and only reading the program back says it was kept
  // ([log]: a compressed one was acknowledged and not kept).
  // -> {bytes, reports, ms, slow, acks, backs, again, implied, said, refused}.  backs: how many times the sending
  // went back, again: how many reports that sent a second time.  said: what the calculator answered in the
  // next moment, if anything ([web]: an F9 then was a refusal on older firmware).
  Link.prototype.sendProgram = async function (name, source, how) {
    how = how || {};
    if (!validName(name)) throw new Error('"' + name + '" is not a name the calculator takes');
    const msg = how.layout === 'v3' ? await programV3(name, source) : programV1(name, source);
    const out = await this.send(msg);
    let said = null, refused = false;
    if (!this.v2) {
      if (how.release) { await sleep(this.pace.release); await this.release(); }
      const r = await this.rx(how.listen === undefined ? 300 : how.listen);
      if (r && r[0] === 0x00 && r[1] !== 0x00) { said = hex(r.subarray(0, 12)); refused = r[1] === F9; }
    }
    return { bytes: msg.length, reports: out.reports, ms: out.ms, slow: out.slow || [], acks: out.acks || null, backs: out.backs || 0, again: out.again || 0,
             implied: !!out.implied, said: said, refused: refused };
  };

  // how: {ver: 1 | 3, nul: true | false, first: ms, then: ms}.  -> the file (parseFile), or null when the calculator
  // takes the request and then stays silent, which is what it does for a program it does not have ([web], [log]).
  // It ends within `first` ms of the request's going unless the answer has begun by then.  A request that the
  // calculator does not even acknowledge (the newer framing) is not that: it throws Silent.
  Link.prototype.readProgram = async function (name, how) {
    how = how || {};
    await this.send(requestMessage(name, how.ver || 1, how.nul !== false));
    const end = Date.now() + (how.first || 3000);                  // counted from when the request has gone
    for (;;) {
      const left = end - Date.now();
      if (left <= 0) return null;
      let msg;
      try { msg = await this.recv([F7], left, how.then || 2500); }
      catch (e) { if (e instanceof Silent) return null; throw e; }
      const f = await parseFile(msg);
      const l = this.last || {};
      f.reports = l.reports || 0; f.numbered = l.numbered || ''; f.id = l.id; f.acks = l.acks || 0; f.stalls = l.stalls || []; f.again = l.again || 0; f.gaps = l.gaps || 0;
      f.bytes = msg.length; f.head = hex(msg.subarray(0, 12));
      if (f.name === name) return f;
      this.note('  passed over a file named "' + f.name + '"');      // a late answer, or the calculator's own Send key
    }
  };

  // [web], [log]: EB has no answer; ask for the file afterwards, and silence means it is gone.
  Link.prototype.deleteProgram = async function (name, ver) {
    await this.send(deleteMessage(name, ver || 1));
    await sleep(this.pace.erase);          // [log] 17 Nov: deletes 0.3 s apart were taken by both calculators; nothing shorter was tried
  };

  // ---------------------------------------------------------------- a load: programs onto a calculator, each read back
  function firstDifference(a, b) {
    const n = Math.min(a.length, b.length);
    for (let i = 0; i < n; i++) if (a.charCodeAt(i) !== b.charCodeAt(i)) return i;
    return a.length === b.length ? -1 : n;
  }
  function reportsText(n) { return num(n) + ' report' + (n === 1 ? '' : 's'); }
  function sameBut(t) { return String(t).replace(/\r\n?/g, '\n').replace(/\n+$/, ''); }      // a program, but for its line ends and the empty lines at its end
  // The route both calculators took on 17 Nov [log]: begin(); then each program as "F7 01" in the newer framing and,
  // `settle` ms after its last acknowledgement (0.4 s on that day; no shorter gap has been tried), a request for it
  // back, which must bring the same text.  The first program that does not come back the same ends the load, so that
  // nothing is called loaded that was not read back; and the load stops between two programs, never inside one.
  // programs: [{name, source}].  The source goes as it is given, but for its line ends, which are made LF; hp-prime-kit
  // also drops one newline at the end of a text file, and that is for the caller to do or not.  What comes back
  // counts as the same if it differs in nothing but its line ends and the empty lines at its end.
  // ui: {log(text), trace(text, at), item(k, state), stop() -> bool}; state is 'send', 'check', 'ok' or 'bad'.
  // opts: {first, settle, then, budget, keep, patience(chars) -> ms (patienceFor unless a test gives its own),
  //        lull: ms, or (chars, reportSize) -> ms, a program is left alone once its download is verified, before the
  //        next one begins (lullFor unless a test gives its own)}.
  // ui.resting(k, ms), if given, is called when that rest begins for program k.
  // -> {ok, done: [name], failed: null | {name, why, text}, stopped, gone, info, told, reports, ms}
  //    why: 'silent'  no answer to "who are you" (nothing was sent)
  //         'version' it does not speak version 03 after being told (nothing was sent)
  //         'unsent'  the program did not go through (a program in pieces is not kept by the calculator)
  //         'unread'  it went, and the request for it back failed, so the page cannot tell
  //         'missing' it went, was acknowledged, and the calculator does not have it
  //         'full'    it went, was acknowledged, and came back EMPTY: the calculator had no room left and kept the
  //                   name only (a G1, 18 Nov 2026, after 15 of the book's 30 programs: its log in usb/logs/)
  //         'differs' what came back is not what was sent
  async function load(link, programs, ui, opts) {
    ui = ui || {}; opts = opts || {};
    const t0 = Date.now(), res = { ok: false, done: [], failed: null, stopped: false, gone: false, stuck: false, removed: [], info: null, told: false, reports: 0, ms: 0 };
    const tracer = ui.trace ? new Tracer(ui.trace, { budget: opts.budget, keep: opts.keep }) : null;
    const log = function (text) { if (tracer) tracer.mark(); if (ui.log) ui.log(text); };
    const item = function (k, state) { if (ui.item) ui.item(k, state); };
    // line: what the log says of it; then the last reports that the log had left out, since those are the ones wanted now
    const fail = function (name, why, text, line, k) {
      const t = tracer ? tracer.tail() : [];
      log(line);
      if (t.length) { if (ui.log) ui.log('  The last reports before that, which the log had left out:'); t.forEach(function (x) { ui.trace(x[0], x[1]); }); }
      res.failed = { name: name, why: why, text: text };
      if (k !== undefined) item(k, 'bad');
      return res;
    };
    if (tracer) link.trace = function (dir, r, v2, expect) { tracer.report(dir, r, v2, expect); };
    link.note = function (text) { log(text); };
    try {
      let b;
      log('Asking the calculator who it is ("00 FA") ...');
      try { b = await link.begin(opts.first || 3000, log); }
      catch (e) { if (isGone(e)) throw e; return fail(null, 'silent', said(e), 'NO ANSWER: ' + said(e) + '.'); }
      res.info = b.info; res.told = b.told;
      if (b.ver !== 3) return fail(null, 'version', 'version ' + hex2(b.ver), 'IT DOES NOT SPEAK VERSION 03, which the two calculators this route was proved on did once they were told. Nothing was sent.');
      // Room first (ui.remove: names to take off, the book's programs not in this choice).  A delete has no answer
      // [web].  [log] 17 Nov: the G2 deleted a program so in the newer framing, the G1 in the OLD framing only; a
      // delete in the newer framing has NOT yet been seen to work on a G1 (the next log shows it: a G1 that keeps
      // what should have gone fills up, and the page then says so).  A name that is not there costs nothing.
      const off = ui.remove || [];
      if (off.length) {
        log('Making room: taking off the book\'s programs that are not in this choice, if they are there (' + num(off.length) + '): ' + off.join(', ') + '.');
        for (let k = 0; k < off.length; k++) {
          if (ui.stop && ui.stop()) { res.stopped = true; log('STOPPED by the Stop button, while making room.'); return res; }
          if (ui.removing) ui.removing(k, off.length);
          await link.deleteProgram(off[k], 3);
        }
        res.removed = off.slice();
        log('  Done: ' + num(off.length) + ' delete' + (off.length === 1 ? '' : 's') + ' sent.');
      }
      const lull = opts.lull === undefined ? lullFor : opts.lull;      // see v3b, at the top
      let arrivedAt = 0, verifiedAt = 0, lastChars = 0;
      for (let k = 0; k < programs.length; k++) {
        if (ui.stop && ui.stop()) { res.stopped = true; log('STOPPED by the Stop button, before ' + programs[k].name + '.'); break; }
        const p = programs[k], src = String(p.source).replace(/\r\n?/g, '\n');
        item(k, 'send');
        if (arrivedAt) {
          const want = typeof lull === 'function' ? lull(lastChars, link.port.reportSize) : lull, had = Date.now() - verifiedAt;
          if (had < want) {
            if (ui.resting) ui.resting(k - 1, want - had);
            // in short steps, so that Stop and a calculator that goes off the cable are noticed
            for (let left = want - had; left > 0; left -= 100) {
              if (ui.stop && ui.stop()) break;
              await sleep(Math.min(100, left));
            }
          }
          if (ui.stop && ui.stop()) { res.stopped = true; log('STOPPED by the Stop button, before ' + p.name + '.'); break; }
          log('  (' + programs[k - 1].name + ' was left alone for ' + secs2(Date.now() - verifiedAt) + ' after it was verified, ' + secs2(Date.now() - arrivedAt) + ' after it arrived, before the next program began)');
        }
        log(p.name + ': ' + num(src.length) + ' characters.');
        let out, back;
        try { out = await link.sendProgram(p.name, src, { layout: 'v1' }); }
        catch (e) { if (isGone(e)) throw e; return fail(p.name, 'unsent', said(e), '  NOT SENT: ' + said(e) + '.', k); }
        res.reports += out.reports;
        arrivedAt = Date.now(); lastChars = src.length;
        log('  Sent ' + num(out.bytes) + ' bytes in ' + reportsText(out.reports) + ', ' + (out.ms / 1000).toFixed(2) + ' s. Acknowledged ' + num(out.acks.length) + ' time' + (out.acks.length === 1 ? '' : 's') +
            (out.backs ? '; ' + num(out.backs) + ' time' + (out.backs === 1 ? '' : 's') + ' a report was sent again' : '') +
            (out.slow.length ? '; the cable stood at ' + out.slow.map(function (x) { return 'report ' + num(x.report) + ' (' + secs(x.ms) + ')'; }).join(', ') : '') +
            (out.implied ? '; the calculator went on to answer without acknowledging the whole' : '') + '.');
        item(k, 'check');
        await sleep(opts.settle === undefined ? 400 : opts.settle);
        const tb = Date.now();
        try { back = await link.readProgram(p.name, { ver: 3, nul: true, first: (opts.patience || patienceFor)(src.length), then: opts.then || 2500 }); }
        catch (e) { if (isGone(e)) throw e; return fail(p.name, 'unread', said(e), '  NOT READ BACK: ' + said(e) + '.', k); }
        if (!back) return fail(p.name, 'missing', 'no answer in ' + secs(Date.now() - tb), '  NOT ON THE CALCULATOR: it acknowledged the request for ' + p.name + ' and sent nothing in ' + secs(Date.now() - tb) + '.', k);
        res.reports += back.reports;
        if (back.text.length === 0 && src.length > 0)
          return fail(p.name, 'full', 'it came back empty', '  NOT KEPT: the calculator took all of ' + p.name + ' and gave it back empty, as a calculator with no room left does.', k);
        if (back.text !== src && sameBut(back.text) !== sameBut(src)) {
          const what = num(back.text.length) + ' characters came back against ' + num(src.length) + ' sent';
          return fail(p.name, 'differs', what, '  NOT THE SAME: ' + what + '; the first difference is at character ' + num(firstDifference(back.text, src) + 1) + '.', k);
        }
        res.done.push(p.name);
        verifiedAt = Date.now();
        item(k, 'ok');
        log('  Read back the same: ' + reportsText(back.reports) + (back.compressed ? ', compressed' : ', not compressed') + ', ' + secs(Date.now() - tb) +
            (back.stalls && back.stalls.length ? '; the calculator stood until it was acknowledged after ' + back.stalls.map(num).join(', ') + ' reports' : '') +
            (back.again ? '; ' + num(back.again) + ' of its reports came twice' : '') + (back.gaps ? '; ' + num(back.gaps) + ' came out of turn' : '') +
            (back.crcOk === false ? '; ITS CHECKSUM DOES NOT FIT' : '') + '.');
      }
      res.ok = !res.stopped && res.done.length === programs.length;
      return res;
    } catch (e) {
      if (!isGone(e)) throw e;
      res.gone = true;
      res.stuck = /did not take a report within/.test(said(e));      // [log] G2, 18 Nov, 16:11: it was still on the cable
      log((res.stuck ? 'THE CALCULATOR STOPPED RESPONDING: ' : 'THE CALCULATOR WENT OFF THE CABLE: ') + said(e) + '.');
      return res;
    } finally {
      res.ms = Date.now() - t0;
      if (tracer) tracer.mark();
    }
  }

  // ---------------------------------------------------------------- WebHID
  // The size of report 0 in a direction, from the device's own description; 1,024 on a G2 and 64 on a G1 ([log]).
  function reportSize(device, dir) {
    const cs = device.collections || [];
    for (let i = 0; i < cs.length; i++) {
      const rs = (dir === 'in' ? cs[i].inputReports : cs[i].outputReports) || [];
      for (let j = 0; j < rs.length; j++) {
        if ((rs[j].reportId || 0) !== 0) continue;
        let bits = 0;
        const it = rs[j].items || [];
        for (let k = 0; k < it.length; k++) bits += (it[k].reportSize || 0) * (it[k].reportCount || 0);
        if (bits > 0) return Math.ceil(bits / 8);
      }
    }
    return null;
  }
  // Every report goes out at its full size, padded with zeros: that is what Windows did for [kit]'s measurements.
  function HidPort(device) {
    const fallback = device.productId === 0x2441 ? 1024 : 64, self = this;
    this.device = device;
    this.inSize = reportSize(device, 'in') || reportSize(device, 'out') || fallback;
    this.outSize = reportSize(device, 'out') || this.inSize;
    this.reportSize = Math.min(this.inSize, this.outSize);
    this.sizeFrom = reportSize(device, 'out') ? 'the calculator' : 'the usual size for this model';
    this.queue = []; this.waiter = null; this.fail = null; this.sent = 0; this.received = 0;
    this.gone = null;               // why the calculator is no longer there, once it is not
    this.limit = 60000;             // one report: [log] a G2 let the cable stand for 49 s (the old framing, a message it did not keep) and then went on
    this.onReport = function (e) {
      const r = new Uint8Array(e.data.buffer, e.data.byteOffset, e.data.byteLength).slice();
      self.received++;
      if (self.waiter) { const w = self.waiter; self.waiter = null; w(r); } else self.queue.push(r);
    };
    device.addEventListener('inputreport', this.onReport);
  }
  // The calculator went off the cable (the browser's "disconnect").  Whatever is waiting ends now, with Gone.
  // [log]: on 17 Nov a write to a calculator that had gone never came back, and the page stood still.
  HidPort.prototype.lose = function (why) {
    if (this.gone) return;
    this.gone = why || 'the calculator went off the cable';
    if (this.waiter) { const w = this.waiter; this.waiter = null; w(null); }
    if (this.fail) { const f = this.fail; this.fail = null; f(new Gone(this.gone)); }
  };
  HidPort.prototype.send = async function (frame) {
    if (this.gone) throw new Gone(this.gone);
    const data = new Uint8Array(this.outSize), self = this;
    data.set(frame.subarray(0, this.outSize));
    let timer = null;
    const guard = new Promise(function (res, rej) {
      self.fail = rej;
      timer = setTimeout(function () { rej(new Gone('the calculator did not take a report within ' + secs(self.limit))); }, self.limit);
    });
    try {
      const w = Promise.resolve(this.device.sendReport(0, data));
      w.catch(function () {});                                    // (if the guard wins, a late failure of the write has nowhere else to go)
      await Promise.race([w, guard]);
    }
    catch (e) {
      const g = isGone(e) ? e : new Gone('the browser could not write to the calculator (' + said(e) + ')');
      this.gone = this.gone || g.message;
      throw g;
    }
    finally { clearTimeout(timer); this.fail = null; }
    this.sent++;
  };
  HidPort.prototype.read = function (ms) {
    const self = this;
    if (this.queue.length) return Promise.resolve(this.queue.shift());
    if (this.gone) return Promise.reject(new Gone(this.gone));
    return new Promise(function (res, rej) {
      const t = setTimeout(function () { self.waiter = null; res(null); }, ms);
      self.waiter = function (r) { clearTimeout(t); if (r === null && self.gone) rej(new Gone(self.gone)); else res(r); };
    });
  };
  HidPort.prototype.poll = function () { return this.queue.length ? this.queue.shift() : null; };
  HidPort.prototype.drain = function () { const n = this.queue.length; this.queue = []; return n; };
  HidPort.prototype.close = async function () {
    this.device.removeEventListener('inputreport', this.onReport);
    if (this.waiter) { const w = this.waiter; this.waiter = null; w(null); }
    try { if (this.device.opened) await this.device.close(); } catch (e) { /* unplugged already */ }
  };

  function supported() { return typeof navigator !== 'undefined' && !!navigator.hid && (typeof window === 'undefined' || window.isSecureContext !== false); }
  // The calculator to talk to: the one this page was let talk to before, if exactly one such is on a cable now;
  // otherwise the browser's own small window listing the calculators.  -> a device, or null when that window was
  // closed with nothing picked.
  async function choose() {
    let known = [];
    try { known = (await navigator.hid.getDevices()).filter(function (d) { return d.vendorId === VENDOR && !!MODELS[d.productId]; }); } catch (e) { known = []; }
    if (known.length === 1) return known[0];
    const d = await navigator.hid.requestDevice({ filters: FILTERS });
    return d && d.length ? d[0] : null;
  }
  async function open(device) {
    if (!device.opened) await device.open();
    return new HidPort(device);
  }

  return { VENDOR: VENDOR, MODELS: MODELS, FILTERS: FILTERS, MAX_MESSAGE: MAX_MESSAGE, OLD_MOST: OLD_MOST, WINDOW: WINDOW, V2_OPEN: V2_OPEN, RELEASE: RELEASE,
           cat: cat, u32be: u32be, u32le: u32le, rdU32be: rdU32be, rdU32le: rdU32le, utf16le: utf16le, fromUtf16le: fromUtf16le,
           hex: hex, hex2: hex2, num: num, secs: secs, crc16: crc16, normalizeSource: normalizeSource, validName: validName, deflate: deflate, inflate: inflate, lullFor: lullFor,
           innerV3: innerV3, programV3: programV3, programV1: programV1, requestMessage: requestMessage, deleteMessage: deleteMessage,
           maxVersionMessage: maxVersionMessage, framesLegacy: framesLegacy, framesV2: framesV2, roomAfter: roomAfter, reportsAt: reportsAt, ackV2: ackV2,
           parseInfo: parseInfo, parseFile: parseFile, describe: describe, runs: runs, patienceFor: patienceFor, firstDifference: firstDifference,
           Tracer: Tracer, load: load, STANDS_AT: STANDS_AT,
           Link: Link, Silent: Silent, Cut: Cut, Gone: Gone, isGone: isGone, HidPort: HidPort, supported: supported, choose: choose, open: open,
           sleep: sleep, said: said };
})();

if (typeof module !== 'undefined') module.exports = PrimeUSB;
