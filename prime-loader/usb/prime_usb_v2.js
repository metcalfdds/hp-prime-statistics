// prime_usb_v2.js -- a real HP Prime on its USB cable, from a web page (WebHID).  Roger Metcalf & Claude, 17 Nov 2026.
//
// WHAT HAS RUN ON A CALCULATOR (logs/, 17 Nov 2026: the author's G2 and his G1, both on firmware build 15751, from
// Chrome and Edge 157 on Windows, with prime_usb_v1.js).  These lines are marked [log] below.
//   * The old framing, and the information request, answered with version 01 by both calculators.
//   * A program sent as "F7 01", not compressed, and read back with "F8 01" or "F8 03", the name ending in a NUL: the
//     same came back at 1, 17 and 80 reports of a G2 and at 10 reports of a G1.  The answer was "F7 01" both times.
//   * NOT kept: the same layout in 274 reports of a G2 (the cable stood for 49 s on the way) and in 263 of a G1.
//   * NOT kept: a program sent compressed, "F7 03", in the old framing, with or without the report "01" after it.
//   * A delete, "EB 01".
//   * The newer framing: "FF EC" was taken, and a message in it was acknowledged with a position of 1,015 after one
//     report of a G2 and 370 after six of a G1, which is the room of those reports and not the message's length.
//     The compressed program in it was not kept.  v1 then waited without end for an answer, because every repeated
//     acknowledgement started its wait again; v2's waits each have one end, whatever arrives meanwhile.
// EVERYTHING ELSE is still a reading of somebody else's measurements, marked with its source, and the second test
// page (PrimeUSBTest_v2.html) is there to try it.
//
// WHERE EACH FACT COMES FROM (all four MIT; no code of theirs is here, only what they measured or read)
//   [kit]  JordiRigau/hp-prime-kit, docs/topics/usb.md and hpkit/usb.py.  One G2 on firmware 2.4.15515, from Windows,
//          3 to 5 Nov 2026.  Its G2 answered the information request with version 03 and kept a program sent as
//          "F7 03", compressed, in the old framing; it had been used with HP's Connectivity Kit just before.
//   [web]  APie357/hp-prime-web, docs/PROTOCOL.md.  One G2, 9 and 10 Nov 2026, old framing: "F7 01", "F8 01" with the
//          name ENDING IN A NUL, "EB 01".
//   [pd]   BeatSkip/PrimeDev (Oscar Spierings), PrimeWeb/Frames and Utility/MessageUtils.cs.  The newer framing, and
//          the bytes of a message "FD 01 00 00 00 01 03" that it calls the newest protocol version.
//   [emu]  golba98/hp-prime-emulator, docs/reverse-engineering and docs/device.  A reading of HP's Connectivity Kit
//          2.4.2 r15751 as data: the Kit asks "00 FA", then sends "FF EC", and the calculator's answer chooses a
//          mode; in the first mode a message's reports are numbered 01, then 02 to FD and 02 again, at most 76 are
//          sent ahead of an acknowledgement, and there is a retry after 500 ms.  Its own G1 kept a program of 15,926
//          bytes in the old framing (254 reports) and not one of 16,284 (259).
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
  const WINDOW = 76;                                                       // [emu]

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
  // and the zlib stream.  [kit]
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
  // the first message of a session, the seven bytes of the 'long' form; its table of commands gives the two bytes of
  // the 'short' one.  Nobody has written down what a calculator does with either.  NOT MEASURED.
  function maxVersionMessage(kind) { return kind === 'short' ? Uint8Array.of(FD, 0x03) : Uint8Array.of(FD, 0x01, 0, 0, 0, 0x01, 0x03); }

  // ---------------------------------------------------------------- framing
  // The old framing: a report is a sequence number and up to cap bytes; the number starts at 00 and counts up, FE is
  // followed by 00, and FF is never a sequence number.  [web], from hplp; [emu]: the Connectivity Kit's own old-framing
  // code counts the same way.  [log], [emu]: a message of more than 255 reports was nevertheless not kept by a G2
  // (274), a G1 (263) or [emu]'s G1 (259), and one of 254 was; so OLD_MOST is 255 until a calculator says otherwise.
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
  // The numbers run 02 to FD and then 02 again.  [emu]
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
  // -> {kind: 'start' | 'more' | 'ack' | 'control', seq, key, text}
  function describe(r, v2) {
    const s = r[0];
    if (s === 0xFF) return { kind: 'control', key: 'c', text: 'a control report: ' + hex(r.subarray(0, 12)) };
    if (s === 0xFE && r.length >= 12 && r[1] <= 1 && r[3] === 0) {
      const id = rdU32le(r, 8);
      return { kind: 'ack', key: 'a' + id + (r[1] ? '' : 'n'), seq: r[2], ok: r[1] === 1, pos: rdU32le(r, 4), id: id,
               text: (r[1] ? 'acknowledgement' : '"SEND AGAIN"') + ': report ' + hex2(r[2]) + ', position ' + num(rdU32le(r, 4)) + ', message ' + id };
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
  // hooks: {note(text), trace(dir, report, v2)}.  Every report that goes out or comes in passes trace, so that a log
  // can show what the calculator did and not only what this code made of it.
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
    this.learned = 0;               // newer framing: after how many reports the calculator stood and waited for us
    // release: [kit]'s gap before the report "01".  stall: how long a pause in a reply counts as the calculator waiting
    // for us.  patience: how long we wait for it at our window.  ack: how long for its acknowledgement of a whole message.
    this.pace = { release: 250, stall: 300, patience: 650, ack: 3000 };
    this.last = null;
  }

  Link.prototype.tx = async function (frame) { this.trace('>', frame, this.v2); await this.port.send(frame); };
  // What comes next, within ms.  The stash first.
  Link.prototype.rx = async function (ms) {
    if (this.stash.length) return this.stash.shift();
    const r = await this.port.read(ms);
    if (r) this.trace('<', r, this.v2);
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
      await this.tx(frames[i]);
      const ms = Date.now() - t;
      if (ms >= 250 && slow.length < 8) slow.push({ report: i + 1, ms: ms });
    }
    return { reports: frames.length, ms: Date.now() - t0, slow: slow };
  };
  // One reply in the old framing.  cmds: the first bytes that count as this reply.  A report that is not the start
  // of it is passed over, and does not lengthen the wait: `first` ms for the reply to begin, counted once, and `then`
  // ms between two reports of it.  -> the message, from its command byte on.
  Link.prototype.recvLegacy = async function (cmds, first, then) {
    const end = Date.now() + first;
    let buf = null, total = 0, got = 0, seq = 0, n = 0, last = 0, skipped = 0;
    const firsts = [];
    for (;;) {
      const left = (buf === null ? end : last + then) - Date.now(), r = left > 0 ? await this.rx(left) : null;
      if (!r) {
        if (buf === null) throw new Silent('no answer within ' + secs(first) + (skipped ? ' (' + skipped + ' other report' + (skipped === 1 ? '' : 's') + ' came)' : ''));
        throw new Cut('the reply stopped after ' + num(got) + ' of ' + num(total) + ' bytes, ' + n + ' report' + (n === 1 ? '' : 's') + ', numbered ' + runs(firsts));
      }
      const s = r[0];
      if (buf === null) {
        if (s !== 0x00 || cmds.indexOf(r[1]) < 0) { skipped++; continue; }
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
  // Opening it is one report.  [emu]: the calculator answers with a control report, which chooses the mode; what that
  // report holds is not written down, so whatever comes in the next `listen` ms is handed back for the log.
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
  // Send one message.  At most `window` reports go ahead of what the calculator has acknowledged ([emu]: the
  // Connectivity Kit's window is 76).  What a calculator does at that point is not written down: if no
  // acknowledgement comes within `pace.patience` ms the sending goes on, and the count of such times is handed back.
  // A "send again" goes back to the report it names ([pd]).  The message is through when an acknowledgement's
  // position covers it ([log]: both calculators acknowledge a whole message), or when the calculator starts an
  // answer of its own.
  // -> {id, reports, ms, acks: [{ms, ok, seq, pos, sent}], waits, unacked, slow, implied}
  Link.prototype.sendV2 = async function (msg, wait) {
    wait = wait || this.pace.ack;
    const id = this.id++, cap = this.cap, frames = framesV2(msg, id, cap), n = frames.length, acks = [], slow = [], t0 = Date.now(), self = this;
    let acked = 0, floor = 0, i = 0, again = 0, waits = 0, unacked = 0, dumb = 0, stood = 0, progress = Date.now(), implied = false;
    const take = function (r) {
      if (r[0] === 0xFF) return;
      if (r[0] !== 0xFE) {                                         // not an acknowledgement: it is kept for whoever reads next
        self.stash.push(r);
        if (i >= n && r[0] === 0x01) implied = true;               // the calculator is answering, so it has the message
        return;
      }
      if (r.length < 12 || rdU32le(r, 8) !== id) return;           // about an earlier message (they repeat: [kit])
      const ok = r[1] === 0x01, pos = rdU32le(r, 4);
      if (acks.length < 400) acks.push({ ms: Date.now() - t0, ok: ok, seq: r[2], pos: pos, sent: i });
      if (ok) {
        const k = (pos >= msg.length && i >= n) ? n : Math.min(n, reportsAt(pos, cap));
        if (k > acked) { acked = k; progress = Date.now(); if (acked > floor) floor = acked; }
        return;
      }
      if (r[2] === 0) return;                                      // [emu]: a "send again" that names no report
      let j = -1;
      for (let k = Math.min(i, n) - 1; k >= 0; k--) if (frames[k][0] === r[2]) { j = k; break; }
      if (j < 0) return;
      if (++again > 8) throw new Cut('the calculator asked nine times for a report of message ' + id + ' again, the last time for report ' + hex2(r[2]));
      i = j; if (acked > j) acked = j; if (floor > j) floor = j;
      progress = Date.now();
    };
    while (acked < n && !implied) {
      if (i < n && i - floor < this.window) {
        const t = Date.now();
        await this.tx(frames[i]);
        const ms = Date.now() - t;
        if (ms >= 250 && slow.length < 8) slow.push({ report: i + 1, ms: ms });
        i++; progress = Date.now(); stood = 0;
        for (let r = this.rawNow(); r; r = this.rawNow()) take(r);
        continue;
      }
      if (i < n) {                                                 // at the window: an acknowledgement is due
        if (!stood) stood = Date.now();
        // (three windows running with no word, and the pause there is a short one from then on: this calculator
        // acknowledges a message at its end, and waiting 0.65 s at each of 120 windows would only be waiting)
        const left = stood + (dumb >= 3 ? Math.min(50, this.pace.patience) : this.pace.patience) - Date.now(), r = left > 0 ? await this.port.read(left) : null;
        if (!r) { floor = i; unacked++; dumb++; stood = 0; continue; }     // none came: go on
        this.trace('<', r, this.v2);
        const before = floor;
        take(r);
        if (floor > before) { waits++; dumb = 0; stood = 0; }
        continue;
      }
      const left = progress + wait - Date.now(), r = left > 0 ? await this.port.read(left) : null;
      if (!r) {
        const a = acks.length ? acks[acks.length - 1] : null;
        throw new Silent('no acknowledgement of the whole of message ' + id + ' (' + n + ' report' + (n === 1 ? '' : 's') + ') within ' + secs(wait) +
                         (a ? '; the last one said report ' + hex2(a.seq) + ', position ' + num(a.pos) : '; none came at all'));
      }
      this.trace('<', r, this.v2);
      take(r);
    }
    return { id: id, reports: n, ms: Date.now() - t0, acks: acks, waits: waits, unacked: unacked, slow: slow, implied: implied };
  };
  // One message from the calculator in the newer framing.  `first` ms for it to begin, counted once whatever else
  // arrives; `then` ms between two of its reports.  It is acknowledged when it is whole, with the position the
  // calculator's own acknowledgements use ([log]).  If the calculator stops in the middle, it may be waiting for an
  // acknowledgement of what it has sent ([emu]: a window of 76): one is sent after `pace.stall` ms, and the number of
  // reports it had sent is remembered, so that the next time the acknowledgement goes out without the wait.
  // A report again, after a "send again" or a retry of the calculator's, is dropped; a gap asks for the missing one.
  Link.prototype.recvV2 = async function (cmds, first, then) {
    const end = Date.now() + first, cap = this.cap;
    let m = null;
    for (;;) {
      const now = Date.now();
      let wait;
      if (m === null) wait = end - now;
      else {
        const idle = now - m.at;
        if (idle >= then) throw new Cut('the reply stopped after ' + num(m.got) + ' of ' + num(m.total) + ' bytes, ' + m.n + ' report' + (m.n === 1 ? '' : 's') + ' of message ' + m.id);
        wait = m.nudged === m.n ? then - idle : Math.min(then - idle, Math.max(1, this.pace.stall - idle));
      }
      const r = wait > 0 ? await this.rx(wait) : null;
      if (!r) {
        if (m === null) throw new Silent('no answer within ' + secs(first));
        if (m.nudged !== m.n && Date.now() - m.at >= this.pace.stall) {            // it may be waiting for us
          await this.tx(ackV2(m.seq, roomAfter(m.n, cap), m.id, true));
          const since = m.n - m.ackedAt;
          m.nudged = m.n; m.ackedAt = m.n; m.stalls.push(m.n);
          if (since > 1 && (!this.learned || since < this.learned)) this.learned = since;
        }
        continue;
      }
      const s = r[0];
      if (s === 0xFE || s === 0xFF) continue;                      // acknowledgements of our own messages (they repeat), and control reports
      if (s === 0x00) {                                            // a report of the old framing
        if (m === null && cmds.indexOf(r[1]) >= 0) {               // ... which begins what we wait for: [kit] found the old framing still answered
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
        m = { id: id, total: total, buf: new Uint8Array(total), got: 0, n: 1, seq: 1, next: 2, at: Date.now(), nudged: 0, ackedAt: 0, asked: 0, stalls: [], again: 0, gaps: 0 };
        const take = Math.min(total, r.length - 9);
        m.buf.set(r.subarray(9, 9 + take), 0); m.got = take;
      } else {
        if (m === null) continue;                                   // the tail of something that began before we listened
        if (s !== m.next) {
          const behind = ((m.next - s) + 252) % 252;                // the numbers 02 to FD go round: [emu]
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
        this.last = { reports: done.n, numbered: 'message ' + done.id, id: done.id, stalls: done.stalls, again: done.again, gaps: done.gaps };
        if (cmds.indexOf(done.buf[0]) >= 0) return done.buf;
        continue;                                                   // some other message: acknowledged, and the trace has it
      }
      if (this.learned && m.n - m.ackedAt >= this.learned) {        // where it stood the last time: acknowledge before it has to wait
        await this.tx(ackV2(m.seq, roomAfter(m.n, cap), m.id, true));
        m.ackedAt = m.n;
      }
    }
  };

  // Send a message in the link's framing, after putting aside whatever was waiting.
  Link.prototype.send = async function (msg) {
    this.clear();
    return this.v2 ? this.sendV2(msg) : this.sendLegacy(msg);
  };
  Link.prototype.recv = function (cmds, first, then) {
    return this.v2 ? this.recvV2(cmds, first, then || 2500) : this.recvLegacy(cmds, first, then || 2500);
  };

  // Listen for ms and take nothing: whatever comes is passed over, and in the newer framing a whole message is
  // acknowledged all the same, so that the calculator does not go on sending it.  [log]: the G1 sent one file
  // several times for one request, and a late copy must not be taken for the answer to the next.
  Link.prototype.swallow = async function (ms) {
    try { await this.recv([], ms, Math.min(ms, 2500)); }
    catch (e) { if (!(e instanceof Silent) && !(e instanceof Cut)) throw e; }
  };

  // -> {build, version, bytes, ver}.  [kit]: "00 FA" was answered by "00 FA 03 00 00 00 6C"; [log]: by version 01.
  Link.prototype.info = async function (first) {
    await this.send(Uint8Array.of(FA));
    const r = await this.recv([FA], first || 3000);
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
  // [kit]: a report "01" followed every program it sent in the old framing.
  Link.prototype.release = async function () { await this.tx(RELEASE); };

  // how: {layout: 'v3' | 'v1', release: true | false, listen: ms}; the framing is the link's.
  // Nothing acknowledges a program in the old framing ([kit], [web], [log]), so "sent" is all this can say there:
  // -> {bytes, reports, ms, slow, acks, waits, unacked, implied, said, refused}.  said: what the calculator answered in the
  // next moment, if anything ([web]: an F9 then was a refusal on older firmware).
  Link.prototype.sendProgram = async function (name, source, how) {
    how = how || {};
    if (!validName(name)) throw new Error('"' + name + '" is not a name the calculator takes');
    const msg = how.layout === 'v1' ? programV1(name, source) : await programV3(name, source);
    const out = await this.send(msg);
    let said = null, refused = false;
    if (!this.v2) {
      if (how.release) { await sleep(this.pace.release); await this.release(); }
      const r = await this.rx(how.listen === undefined ? 300 : how.listen);
      if (r && r[0] === 0x00 && r[1] !== 0x00) { said = hex(r.subarray(0, 12)); refused = r[1] === F9; }
    }
    return { bytes: msg.length, reports: out.reports, ms: out.ms, slow: out.slow || [], acks: out.acks || null, waits: out.waits || 0,
             unacked: out.unacked || 0, implied: !!out.implied, said: said, refused: refused };
  };

  // how: {ver: 1 | 3, nul: true | false, first: ms, then: ms}.  -> the file (parseFile), or null when the calculator
  // stays silent, which is also what it does for a program it does not have ([web], [log]).  It ends within
  // `first` ms of the request's going unless the answer has begun by then.
  Link.prototype.readProgram = async function (name, how) {
    how = how || {};
    try { await this.send(requestMessage(name, how.ver || 1, how.nul !== false)); }
    catch (e) { if (e instanceof Silent) { this.note('  ' + e.message); return null; } throw e; }
    const end = Date.now() + (how.first || 3000);                  // counted from when the request has gone
    for (;;) {
      const left = end - Date.now();
      if (left <= 0) return null;
      let msg;
      try { msg = await this.recv([F7], left, how.then || 2500); }
      catch (e) { if (e instanceof Silent) return null; throw e; }
      const f = await parseFile(msg);
      const l = this.last || {};
      f.reports = l.reports || 0; f.numbered = l.numbered || ''; f.stalls = l.stalls || []; f.again = l.again || 0; f.gaps = l.gaps || 0;
      f.bytes = msg.length; f.head = hex(msg.subarray(0, 12));
      if (f.name === name) return f;
      this.note('  passed over a file named "' + f.name + '"');      // a late answer, or the calculator's own Send key
    }
  };

  // [web], [log]: EB has no answer; ask for the file afterwards, and silence means it is gone.
  Link.prototype.deleteProgram = async function (name, ver) {
    await this.send(deleteMessage(name, ver || 1));
    await sleep(300);
  };

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
    this.limit = 90000;             // one report: [log] a G2 let the cable stand for 49 s and then went on
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
  // The browser's own window listing the calculators on the cable.  -> a device, or null when the window was closed.
  async function choose() {
    const d = await navigator.hid.requestDevice({ filters: FILTERS });
    return d && d.length ? d[0] : null;
  }
  async function open(device) {
    if (!device.opened) await device.open();
    return new HidPort(device);
  }

  return { VENDOR: VENDOR, MODELS: MODELS, FILTERS: FILTERS, MAX_MESSAGE: MAX_MESSAGE, OLD_MOST: OLD_MOST, WINDOW: WINDOW, V2_OPEN: V2_OPEN, RELEASE: RELEASE,
           cat: cat, u32be: u32be, u32le: u32le, rdU32be: rdU32be, rdU32le: rdU32le, utf16le: utf16le, fromUtf16le: fromUtf16le,
           hex: hex, hex2: hex2, num: num, secs: secs, crc16: crc16, normalizeSource: normalizeSource, validName: validName, deflate: deflate, inflate: inflate,
           innerV3: innerV3, programV3: programV3, programV1: programV1, requestMessage: requestMessage, deleteMessage: deleteMessage,
           maxVersionMessage: maxVersionMessage, framesLegacy: framesLegacy, framesV2: framesV2, roomAfter: roomAfter, reportsAt: reportsAt, ackV2: ackV2,
           parseInfo: parseInfo, parseFile: parseFile, describe: describe, runs: runs,
           Link: Link, Silent: Silent, Cut: Cut, Gone: Gone, isGone: isGone, HidPort: HidPort, supported: supported, choose: choose, open: open,
           sleep: sleep, said: said };
})();

if (typeof module !== 'undefined') module.exports = PrimeUSB;
