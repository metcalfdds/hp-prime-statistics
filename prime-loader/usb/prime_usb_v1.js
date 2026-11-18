// prime_usb_v1.js -- a real HP Prime on its USB cable, from a web page (WebHID).  Roger Metcalf & Claude, 17 Nov 2026.
//
// NOTHING HERE HAS RUN ON A CALCULATOR.  It is written from three public descriptions of what travels on the cable,
// and it is tested against hp-prime-kit's own code byte for byte and against a mock calculator made from the same
// descriptions (tests/mock_prime_v1.js).  PrimeUSBTest_v1.html is the first run on a real HP Prime, and until that run
// says otherwise every line below is a reading of somebody else's measurements.
//
// WHERE EACH FACT COMES FROM (all three MIT; no code of theirs is here, only what they measured)
//   [kit]  JordiRigau/hp-prime-kit, docs/topics/usb.md and hpkit/usb.py.  Measured on one G2 on firmware 2.4.15515,
//          from Windows, 3 to 5 Nov 2026: the device, the old framing, the information request, a program sent as
//          "F7 03" with its source compressed (310 bytes in one report up to 16,558 bytes in six), the report "01"
//          after it, and the newer framing's opening.  A request for a file ("F8 03", the name with no NUL after it)
//          was answered once and never again.
//   [web]  APie357/hp-prime-web, docs/PROTOCOL.md.  Tested on one G2 (it reports "V2.060.650"), 9 and 10 Nov 2026,
//          old framing: a program sent as "F7 01" with its source as it is ("over 16 KB" accepted), read back with
//          "F8 01" and the name ENDING IN A NUL (without it the calculator stays silent), deleted with "EB 01".
//          From others' G1 tests it reports that G1 firmware dropped, without a word, uploads over about 15,928 bytes.
//   [pd]   BeatSkip/PrimeDev (Oscar Spierings), PrimeWeb/Frames.  The newer framing, which HP's Connectivity Kit
//          uses on firmware build 10591 and later: message numbers, acknowledgements, at most 240 frames a message.
//
// WHAT IS NOT KNOWN, and what the test page is for: whether either way of sending holds for a program the size of
// ours (ours are 41,000 to 290,000 characters: 21 to 129 reports compressed, 80 to 567 as they are); which request
// reads a program back on Roger's firmware; anything at all about a G1.
//
// No DOM here.  The page hands Link a port ({reportSize, send, read, drain}); HidPort wraps a WebHID device, and the
// tests hand it the mock.

'use strict';

const PrimeUSB = (function () {

  const VENDOR = 0x03F0;                                                   // [kit] usb.device; [web]
  const MODELS = { 0x2441: 'HP Prime G2', 0x1541: 'HP Prime G1', 0x0441: 'HP Prime G1 (early firmware)' };   // [web], [pd]
  const FILTERS = Object.keys(MODELS).map(function (p) { return { vendorId: VENDOR, productId: Number(p) }; });
  const F7 = 0xF7, F8 = 0xF8, F9 = 0xF9, FA = 0xFA, EB = 0xEB, READY = 0xFF, YES = 0x59, PROGRAM = 0x06;
  const V2_MAX = 240 * 1023 - 8;                                           // [pd] a message of the newer framing

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
  // big-endian, and the part itself with its checksum bytes at 0.
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
  // The checksum is taken over all but the last six bytes, its own two at 0, and no NUL follows the source.  [web]
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

  // ---------------------------------------------------------------- framing
  // The old framing: a report is a sequence number and up to cap bytes; the number starts at 00 and counts up, FE is
  // followed by 00, and FF is never a sequence number.  [web], from hplp; [kit] sent at most six reports.
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
  // first), then up to cap - 8 bytes; the reports after it are a sequence number from 02 and up to cap bytes.  [pd], [kit]
  function framesV2(msg, id, cap) {
    if (msg.length > V2_MAX) throw new Error('this message is ' + msg.length + ' bytes, and the newer framing carries ' + V2_MAX + ' at most');
    const out = [], first = cap - 8;
    out.push(cat([0x01], u32le(id), u32le(msg.length), msg.subarray(0, first)));
    let seq = 2;
    for (let o = first; o < msg.length; o += cap) out.push(cat([seq++], msg.subarray(o, o + cap)));
    return out;
  }
  // An acknowledgement: FE, 01 (or 00 for "send again"), a sequence number, 00, a position and the message number.  [pd], [kit]
  function ackV2(seq, pos, id, ok) { return cat([0xFE, ok === false ? 0 : 1, seq, 0], u32le(pos), u32le(id)); }
  const V2_OPEN = Uint8Array.of(0xFF, 0xEC, 0, 0, 0, 0, 0, 0);          // [pd], [kit] usb.newer-framing
  const RELEASE = Uint8Array.of(0x01);                                     // [kit] the report that followed every send

  // ---------------------------------------------------------------- what the calculator sends
  // The information reply: the build number two bytes low byte first, 36 bytes from the end; ten characters of
  // version 32 from the end.  The serial number is 16 from the end, and it is not read.  [kit] identify; [web]
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

  // ---------------------------------------------------------------- the link
  function Silent(what) { this.name = 'Silent'; this.message = what; }
  Silent.prototype = Object.create(Error.prototype);
  function Cut(what) { this.name = 'Cut'; this.message = what; }
  Cut.prototype = Object.create(Error.prototype);
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  // port: {reportSize, send(Uint8Array) -> Promise, read(ms) -> Promise<Uint8Array|null>, drain() -> count}
  // note(text): one line for the log, for whoever reads it afterwards.
  function Link(port, note) {
    this.port = port;
    this.cap = port.reportSize - 1;
    this.note = note || function () {};
    this.v2 = false;
    this.id = 1;                    // the newer framing's message number
    this.pace = { release: 250 };   // [kit] GAP before the report "01"
  }

  Link.prototype.sendFrames = async function (frames) {
    for (let i = 0; i < frames.length; i++) await this.port.send(frames[i]);
  };

  // One reply in the old framing.  cmds: the first bytes that count as this reply.  A report that is not the start
  // of it is passed over ([kit] read_reply), so neither a stray report nor a repeated acknowledgement can be taken
  // for the answer.  -> the message, from its command byte on.
  Link.prototype.recvLegacy = async function (cmds, first, then) {
    let buf = null, total = 0, got = 0, seq = 0, n = 0, limit = first, skipped = 0;
    const firsts = [];
    for (;;) {
      const r = await this.port.read(limit);
      if (!r) {
        if (buf === null) throw new Silent('no answer within ' + (first / 1000) + ' s' + (skipped ? ' (' + skipped + ' other report(s) came)' : ''));
        throw new Cut('the reply stopped after ' + got + ' of ' + total + ' bytes, ' + n + ' report(s); they began ' + runs(firsts));
      }
      const s = r[0];
      if (buf === null) {
        if (s !== 0x00 || cmds.indexOf(r[1]) < 0) { skipped++; if (skipped <= 3) this.note('  passed over a report that begins ' + hex(r, 12)); continue; }
        if (r[1] === YES || r[1] === READY) return r.slice(1, 2);
        total = 6 + rdU32be(r, 3);
        if (total > 64 * 1024 * 1024) throw new Error('the reply claims ' + total + ' bytes: ' + hex(r, 12));
        buf = new Uint8Array(total);
      } else {
        if (s === 0xFF) continue;                                  // never a sequence number: [web], [kit]
        if (s !== seq) {
          if (s === 0xFE) continue;                                // an acknowledgement of the newer framing: [kit]
          if (!(seq === 0xFE && s === 0x00))                       // (a sender that keeps FE for itself wraps one early)
            throw new Cut('the reply came out of order: report ' + s + ' where ' + seq + ' was next, after ' + got + ' of ' + total + ' bytes; reports began ' + runs(firsts));
        }
      }
      const take = Math.min(total - got, r.length - 1);
      buf.set(r.subarray(1, 1 + take), got);
      got += take; n++; firsts.push(s);
      seq = s === 0xFE ? 0 : s + 1;
      if (got >= total) { this.last = { reports: n, firsts: runs(firsts) }; return buf; }
      limit = then;
    }
  };
  // 00 01 02 ... as "00-FE,00-3A": what a long reply's sequence numbers did, which nobody has written down for a G2.
  function runs(a) {
    const out = [];
    for (let i = 0; i < a.length;) {
      let j = i;
      while (j + 1 < a.length && a[j + 1] === a[j] + 1) j++;
      out.push(hex([a[i]]) + (j > i ? '-' + hex([a[j]]) : ''));
      i = j + 1;
    }
    return out.join(',');
  }

  // The newer framing.  Opening it is one report with no answer of its own.  [pd], [kit]
  Link.prototype.openV2 = async function () {
    await this.port.send(V2_OPEN);
    this.v2 = true;
    await sleep(100);
  };
  // Send one message and wait for its acknowledgement.  A "send again" goes back to the report it names.  [pd]
  // -> {id, reports, acks}: acks is what the calculator said on the way, kept for the log, because what its
  // "position" counts is not written down anywhere.
  Link.prototype.sendV2 = async function (msg, wait) {
    const id = this.id++, frames = framesV2(msg, id, this.cap), acks = [], last = frames.length - 1;
    let again = 0;
    const mine = function (r) { return !!r && r[0] === 0xFE && r.length >= 12 && rdU32le(r, 8) === id; };
    const seen = function (r) { if (acks.length < 12) acks.push((r[1] ? 'ok' : 'again') + ' report ' + r[2] + ' position ' + rdU32le(r, 4)); };
    for (let i = 0; i < frames.length; i++) {
      await this.port.send(frames[i]);
      for (let r = this.port.poll(); r; r = this.port.poll()) {
        if (!mine(r)) continue;
        seen(r);
        if (r[1] === 0x01) { if (i === last) return { id: id, reports: frames.length, acks: acks }; continue; }
        if (again < 3) { again++; i = Math.max(0, r[2] - 1) - 1; }          // "send again from report r[2]"
      }
    }
    const end = Date.now() + (wait || 8000);
    for (;;) {
      const left = end - Date.now(), r = left > 0 ? await this.port.read(left) : null;
      if (!r) throw new Silent('no acknowledgement of message ' + id + ' within ' + ((wait || 8000) / 1000) + ' s' + (acks.length ? ' (it said: ' + acks.join('; ') + ')' : ''));
      if (!mine(r)) continue;
      seen(r);
      if (r[1] === 0x01) return { id: id, reports: frames.length, acks: acks };
      if (again >= 3) throw new Cut('the calculator kept asking for report ' + r[2] + ' of message ' + id + ' again');
      again++;
      for (let i = Math.max(0, r[2] - 1); i < frames.length; i++) await this.port.send(frames[i]);
    }
  };
  // One message from the calculator in the newer framing, acknowledged when it is whole.  [pd]
  Link.prototype.recvV2 = async function (cmds, first, then) {
    let buf = null, total = 0, got = 0, id = 0, seq = 0, limit = first, n = 0;
    for (;;) {
      const r = await this.port.read(limit);
      if (!r) {
        if (buf === null) throw new Silent('no answer within ' + (first / 1000) + ' s');
        throw new Cut('the reply stopped after ' + got + ' of ' + total + ' bytes');
      }
      const s = r[0];
      if (s === 0xFE || s === 0xFF || s === 0x00) continue;        // acknowledgements (they repeat), and old-framing strays
      if (s === 0x01) {
        if (rdU32le(r, 1) === this.lastIn && buf === null) {       // the message before, sent again: our acknowledgement was missed
          await this.port.send(ackV2(this.lastSeq || 1, this.lastTotal || 0, this.lastIn, true));
          this.skipping = true;
          continue;
        }
        this.skipping = false;
        id = rdU32le(r, 1); total = rdU32le(r, 5);
        if (total > V2_MAX + 8) throw new Error('the reply claims ' + total + ' bytes: ' + hex(r, 12));
        buf = new Uint8Array(total); got = 0; n = 0;
        const take = Math.min(total, r.length - 9);
        buf.set(r.subarray(9, 9 + take), 0); got = take; seq = 2; n = 1;
      } else {
        if (buf === null) continue;                                 // the tail of something that began before we listened, or of a repeat
        if (s !== seq) throw new Cut('the reply came out of order: report ' + s + ' where ' + seq + ' was next');
        const take = Math.min(total - got, r.length - 1);
        buf.set(r.subarray(1, 1 + take), got); got += take; seq++; n++;
      }
      if (got >= total) {
        await this.port.send(ackV2(s, total, id, true));
        this.lastIn = id; this.lastSeq = s; this.lastTotal = total;
        if (cmds.indexOf(buf[0]) >= 0) { this.last = { reports: n, firsts: 'message ' + id }; return buf; }
        this.note('  passed over a message that begins ' + hex(buf, 8));
        buf = null; limit = first;
        continue;
      }
      limit = then;
    }
  };

  Link.prototype.send = async function (msg) {
    this.port.drain();
    if (this.v2) return this.sendV2(msg);
    const frames = framesLegacy(msg, this.cap);
    await this.sendFrames(frames);
    return { reports: frames.length };
  };
  Link.prototype.recv = function (cmds, first, then) {
    return this.v2 ? this.recvV2(cmds, first, then || 2500) : this.recvLegacy(cmds, first, then || 2500);
  };

  // -> {build, version, bytes, ver}.  [kit]: "00 FA" was answered within 1 ms by "00 FA 03 00 00 00 6C".
  Link.prototype.info = async function (first) {
    await this.send(Uint8Array.of(FA));
    const r = await this.recv([FA], first || 3000);
    const i = parseInfo(r.subarray(6));
    i.bytes = r.length - 6; i.ver = r[1];
    return i;
  };
  // [web]: FF is answered by the one byte 59, "Y".  Not measured by [kit].
  Link.prototype.ready = async function (first) {
    await this.send(Uint8Array.of(READY));
    try { const r = await this.recv([YES, READY], first || 2000); return r[0] === YES || r[0] === READY; }
    catch (e) { if (e instanceof Silent) return false; throw e; }
  };

  // how: {layout: 'v3' | 'v1', release: true | false}; the framing is the link's.
  // Nothing acknowledges a program in the old framing ([kit], [web]), so "sent" is all this can say:
  // -> {bytes, reports, said}.  said: what the calculator answered in the next moment, if anything ([web]: an F9 then
  // was a refusal on older firmware).
  Link.prototype.sendProgram = async function (name, source, how) {
    how = how || {};
    if (!validName(name)) throw new Error('"' + name + '" is not a name the calculator takes');
    const msg = how.layout === 'v1' ? programV1(name, source) : await programV3(name, source);
    const t0 = Date.now(), out = await this.send(msg), ms = Date.now() - t0;     // the time on the cable, before any pause
    if (!this.v2 && how.release !== false) { await sleep(this.pace.release); await this.port.send(RELEASE); }
    let said = null;
    const r = await this.port.read(how.listen === undefined ? 400 : how.listen);
    if (r && r[0] === 0x00 && r[1] !== 0x00) said = hex(r, 12);
    return { bytes: msg.length, reports: out.reports, ms: ms, acks: out.acks || null, said: said, refused: !!(r && r[0] === 0x00 && r[1] === F9) };
  };

  // how: {ver: 1 | 3, nul: true | false, first: ms}.  -> the file (parseFile), or null when the calculator stays
  // silent, which is also what it does for a program it does not have ([web]).
  Link.prototype.readProgram = async function (name, how) {
    how = how || {};
    const end = Date.now() + (how.first || 3000);
    try { await this.send(requestMessage(name, how.ver || 1, how.nul !== false)); }
    catch (e) { if (e instanceof Silent) { this.note('  ' + e.message); return null; } throw e; }
    for (;;) {
      let msg;
      try { msg = await this.recv([F7], Math.max(1, end - Date.now()), how.then || 2500); }
      catch (e) { if (e instanceof Silent) return null; throw e; }
      const f = await parseFile(msg);
      f.reports = this.last ? this.last.reports : 0; f.firsts = this.last ? this.last.firsts : ''; f.bytes = msg.length; f.head = hex(msg, 12);
      if (f.name === name) return f;
      this.note('  passed over a file named "' + f.name + '"');      // the Send key of the calculator, or a late answer
      if (Date.now() >= end) return null;
    }
  };

  // [web]: EB has no answer; ask for the file afterwards, and silence means it is gone.
  Link.prototype.deleteProgram = async function (name, ver) {
    await this.send(deleteMessage(name, ver || 1));
    await sleep(300);
  };

  // ---------------------------------------------------------------- WebHID
  // The size of report 0 in a direction, from the device's own description; 1,024 on a G2 ([kit]) and 64 on a G1 ([web]).
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
    this.queue = []; this.waiter = null; this.sent = 0; this.received = 0;
    this.onReport = function (e) {
      const r = new Uint8Array(e.data.buffer, e.data.byteOffset, e.data.byteLength).slice();
      self.received++;
      if (self.waiter) { const w = self.waiter; self.waiter = null; w(r); } else self.queue.push(r);
    };
    device.addEventListener('inputreport', this.onReport);
  }
  HidPort.prototype.send = async function (frame) {
    const data = new Uint8Array(this.outSize);
    data.set(frame.subarray(0, this.outSize));
    await this.device.sendReport(0, data);
    this.sent++;
  };
  HidPort.prototype.read = function (ms) {
    const self = this;
    if (this.queue.length) return Promise.resolve(this.queue.shift());
    return new Promise(function (res) {
      const t = setTimeout(function () { self.waiter = null; res(null); }, ms);
      self.waiter = function (r) { clearTimeout(t); res(r); };
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

  return { VENDOR: VENDOR, MODELS: MODELS, FILTERS: FILTERS, V2_MAX: V2_MAX, V2_OPEN: V2_OPEN, RELEASE: RELEASE,
           cat: cat, u32be: u32be, u32le: u32le, rdU32be: rdU32be, rdU32le: rdU32le, utf16le: utf16le, fromUtf16le: fromUtf16le,
           hex: hex, crc16: crc16, normalizeSource: normalizeSource, validName: validName, deflate: deflate, inflate: inflate,
           innerV3: innerV3, programV3: programV3, programV1: programV1, requestMessage: requestMessage, deleteMessage: deleteMessage,
           framesLegacy: framesLegacy, framesV2: framesV2, ackV2: ackV2, parseInfo: parseInfo, parseFile: parseFile,
           Link: Link, Silent: Silent, Cut: Cut, HidPort: HidPort, supported: supported, choose: choose, open: open, sleep: sleep, runs: runs };
})();

if (typeof module !== 'undefined') module.exports = PrimeUSB;
