// mock_prime_v2.js -- a pretend HP Prime on a pretend cable, for the tests of prime_usb_v2.js and of the pages that use
// it.  Roger Metcalf & Claude, 17 Nov 2026.
//
// IT IS NOT A CALCULATOR.  By default it does what the author's G2 and G1 did on 17 Nov 2026 (../logs/), as far as
// those three logs go, and beyond them what the leading reading of four public descriptions says ([kit] hp-prime-kit,
// [web] hp-prime-web, [pd] PrimeDev, [emu] hp-prime-emulator; prime_usb_v2.js says what each one holds).  Every
// "beyond" has a switch, so that a test can ask what the page does on a calculator that turns out otherwise.  Its
// byte work is written apart from prime_usb_v2.js (its own checksum, its own framing), so that a slip in one is not
// hidden by the same slip in the other.
//
// FROM THE LOGS (both calculators on firmware build 15751)
//   fmt 1          it answers with version 01, keeps a program sent as "F7 01", does not keep one sent as "F7 03", and
//                  answers "F8 01" and "F8 03" alike, the name ending in a NUL, with "F7 01"; "EB 01" deletes
//   maxOld 255     an old-framing message of more reports than this is not kept (80 was, 274 was not; a G1: 10 and
//                  263; [emu]'s G1: 254 and 259)
//   stallMs 0      ... and the cable stands this long at the first report too many (49 s on the G2, nothing on the G1)
//   busyMs 0       ... and for this long afterwards it answers nothing (the G2's first request after it had no answer)
//   v2 true        it takes "FF EC", and acknowledges a message of the newer framing with the room of its reports
//                  (1,015 after one report of a G2, 370 after six of a G1)
//   copies 1       how many times it sends a file for one request (the G1 sent one several times)
// GUESSES, EACH WITH ITS SWITCH
//   fdOld null, fdNew 'long'   which form of the message "FD" raises its version to 03, in which framing: 'long'
//                  (FD 01 00 00 00 01 03), 'short' (FD 03), 'both', or null for neither.  [pd] has the bytes; nobody
//                  has written down what a calculator does with them
//   fdReply true   it answers such a message with the same form
//   ecReply [...]  what it sends back on "FF EC" ([emu]: a control report; its bytes are not known); null for nothing
//   ackEvery 0     it acknowledges every so many reports of a message, besides at its end
//   ackRepeat 0    it repeats its last acknowledgement every so many ms ([kit]: about 500)
//   window 76, needAck true, retryMs 150   when IT sends in the newer framing: after `window` reports it waits for the
//                  host's acknowledgement, and sends them again after retryMs without one ([emu]: 76 and 500 ms)
//   ackPos 'room'  the position it wants in the host's acknowledgement at a message's end: the room of the reports,
//                  or with 'size' the message's length is enough ([pd] sends the length)
//   oldAfterNew true   it still answers the old framing after "FF EC" ([kit])
//   fdFirst false  in the newer framing it listens to nothing until it has been told "FD", though it acknowledges
//                  everything ([pd] holds an "FD" as the first message of a session)
//   takeV1 true    it keeps "F7 01" whatever version it speaks; 'fmt1': only while it speaks 01
//   takeV3 'fmt3'  it keeps "F7 03" only once it speaks 03; true: always; false: never
// AS IN v1
//   needNul, silentF8, keepOnDelete, crlf, cutAt, nackOnce, deadAfter, busy, none, product (0x1541 is a G1, whose
//   reports are 64 bytes), wrap ('hplp': its long old-framing replies count FD FE 00; 'early': FD 00)
//   deadAfterNew null   it stops answering after this many messages of the newer framing
//   needRelease false   in the old framing it keeps a program only when a report "01" follows it ([kit] sent one after
//                  each): true for every program, 'v3' for a compressed one only
//   dieAt 0        it goes off the cable when this many reports have come from the host (a calculator that switches itself off)
//   hang false     ... and a write to it afterwards never comes back, as Chrome's did on 17 Nov

'use strict';

const MockPrime = (function () {

  function crc(b, from, to) {                       // CRC-16, polynomial 1021, from 0, by table
    let c = 0;
    for (let i = from; i < to; i++) c = ((c << 8) & 0xFFFF) ^ TABLE[((c >> 8) ^ b[i]) & 255];
    return c;
  }
  const TABLE = (function () {
    const t = new Uint16Array(256);
    for (let i = 0; i < 256; i++) { let c = i << 8; for (let k = 0; k < 8; k++) c = (c & 0x8000) ? ((c << 1) ^ 0x1021) : (c << 1); t[i] = c & 0xFFFF; }
    return t;
  })();
  function be(b, o) { return b[o] * 16777216 + b[o + 1] * 65536 + b[o + 2] * 256 + b[o + 3]; }
  function le(b, o) { return b[o] + b[o + 1] * 256 + b[o + 2] * 65536 + b[o + 3] * 16777216; }
  function b32(n) { return [(n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255]; }
  function l32(n) { return [n & 255, (n >>> 8) & 255, (n >>> 16) & 255, (n >>> 24) & 255]; }
  function text(b) { let s = ''; for (let i = 0; i + 1 < b.length; i += 2) s += String.fromCharCode(b[i] | (b[i + 1] << 8)); return s; }
  function bytes(s) { const b = new Uint8Array(2 * s.length); for (let i = 0; i < s.length; i++) { b[2 * i] = s.charCodeAt(i) & 255; b[2 * i + 1] = s.charCodeAt(i) >> 8; } return b; }
  function join(parts) { let n = 0; parts.forEach(function (p) { n += p.length; }); const o = new Uint8Array(n); let k = 0; parts.forEach(function (p) { o.set(p, k); k += p.length; }); return o; }
  async function through(b, ts) { const w = ts.writable.getWriter(); w.write(b).catch(function () {}); w.close().catch(function () {}); return new Uint8Array(await new Response(ts.readable).arrayBuffer()); }
  function pause(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }
  function ackOf(ok, seq, pos, id) { return join([[0xFE, ok ? 1 : 0, seq, 0], l32(pos), l32(id)]); }

  function MockPrime(opts) {
    this.o = Object.assign({ product: 0x2441, build: 15751, version: null, serial: 'SECRETSERIAL0001',
      fmt: 1, fdOld: null, fdNew: 'long', fdReply: true, maxOld: 255, stallMs: 0, busyMs: 0,
      v2: true, ecReply: [0xFF, 0xEC, 0, 0, 0, 0, 0, 1], ackEvery: 0, ackRepeat: 0, window: 76, needAck: true, retryMs: 150, ackPos: 'room',
      oldAfterNew: true, fdFirst: false, takeV1: true, takeV3: 'fmt3', copies: 1,
      needNul: true, silentF8: false, keepOnDelete: false, crlf: false, cutAt: null, needRelease: false, nackOnce: 0, deadAfter: null, deadAfterNew: null,
      busy: false, none: false, wrap: 'hplp', dieAt: 0, hang: false }, opts || {});
    if (!this.o.version) this.o.version = this.o.product === 0x2441 ? 'V2.060.650' : 'V0.050.640';
    this.size = this.o.reportSize || (this.o.product === 0x2441 ? 1024 : 64);
    this.fmt = this.o.fmt;         // the version it speaks now
    this.programs = {};            // name -> source text, as stored
    this.arrived = [];             // {name, layout, framing, reports, bytes, kept, why}
    this.fds = [];                 // {kind, framing}: each "FD" that came
    this.handled = 0; this.handledNew = 0; this.releases = 0; this.hostAcks = []; this.reportsIn = 0; this.reportsOut = 0; this.resent = 0; this.goBacks = 0; this.gaveUp = 0;
    this.v2open = false; this.outId = 1;
    this.rx = null;                // the old framing's message being put together
    this.rx2 = null;               // the newer framing's
    this.pending = null;           // a program waiting for its report "01" (needRelease)
    this.chain = Promise.resolve(); this.tail = Promise.resolve();
    this.onreport = null;          // set by whoever listens
    this.dead = false; this.quietUntil = 0;
    this.ackQ = []; this.ackWaiter = null; this.repeat = null; this.lastAck = null; this.sendingNew = 0;
  }

  MockPrime.prototype.emit = function (frame) {
    const r = new Uint8Array(this.size);
    r.set(frame);
    this.reportsOut++;
    const self = this;
    setTimeout(function () { if (self.onreport && !self.dead) self.onreport(r); }, 0);
  };
  MockPrime.prototype.stop = function () { if (this.repeat) { clearInterval(this.repeat); this.repeat = null; } };

  // One report from the host.  Reports are padded to their full size, as Windows and WebHID deliver them.
  MockPrime.prototype.receive = function (report) {
    const self = this, r = Uint8Array.from(report);
    this.reportsIn++;
    if (this.o.dieAt && this.reportsIn === this.o.dieAt && this.unplug) { this.unplug(); return Promise.resolve(); }
    if (this.dead) return Promise.resolve();
    // A host's acknowledgement is taken at once and not in its turn: the mock may be in the middle of sending,
    // waiting for exactly this.  (FE is also the number of an old-framing message's 255th report.)
    if (this.v2open && r[0] === 0xFE && !(this.rx && this.rx.seq === 0xFE)) {
      const a = { ok: r[1], seq: r[2], pos: le(r, 4), id: le(r, 8) };
      this.hostAcks.push(a); this.ackQ.push(a);
      if (this.ackWaiter) { const w = this.ackWaiter; this.ackWaiter = null; w(); }
      return Promise.resolve();
    }
    this.chain = this.chain.then(function () { return self.step(r); }).catch(function (e) { self.error = String(e && e.stack || e); });
    return this.chain;
  };

  MockPrime.prototype.step = async function (r) {
    if (this.dead) return;
    const s = r[0], cap = this.size - 1;
    const room = function (k) { return k < 1 ? 0 : (cap - 8) + (k - 1) * cap; };
    if (s === 0xFF) {                                             // out of band
      if (r[1] === 0xEC && this.o.v2) {
        this.v2open = true;
        if (this.o.ecReply) this.emit(Uint8Array.from(this.o.ecReply));
        if (this.o.ackRepeat && !this.repeat) { const self = this; this.repeat = setInterval(function () { self.tick(); }, this.o.ackRepeat); if (this.repeat.unref) this.repeat.unref(); }
      }
      return;
    }
    // A report that continues the old-framing message in hand is taken before anything else: its number can be FE,
    // which is also how an acknowledgement begins, or 01, which is also how a message of the newer framing begins,
    // or 00 after FE, which is also how a new message begins.  Only the message's own length tells them apart.
    if (this.rx && s === this.rx.seq) {
      const x = this.rx, take = Math.min(x.total - x.got, cap);
      x.n++;
      if (x.n > this.o.maxOld && !x.dropped) { x.dropped = true; if (this.o.stallMs) await pause(this.o.stallMs); }   // one report too many
      if (!x.dropped) x.buf.set(r.subarray(1, 1 + take), x.got);
      x.got += take;
      x.seq = s === 0xFE ? 0 : s + 1;                             // FE is followed by 00; FF is never a number
      if (x.got >= x.total) {
        this.rx = null;
        if (x.dropped) {                                          // dropped without a word
          this.arrived.push({ name: null, layout: x.buf[1] === 3 ? 'v3' : 'v1', framing: 'old', reports: x.n, bytes: x.total, kept: false, why: 'too many reports' });
          this.quietUntil = Date.now() + this.o.busyMs;
          return;
        }
        return this.message(x.buf, 'old', x.n);
      }
      return;
    }
    if (s === 0xFE) return;                                       // an acknowledgement before the newer framing was opened
    // the newer framing
    if (this.v2open && s === 0x01 && le(r, 1) !== 0) {
      const id = le(r, 1), total = le(r, 5);
      this.rx2 = { id: id, total: total, buf: new Uint8Array(total), got: 0, seq: 2, n: 1, asked: -1 };
      const take = Math.min(total, cap - 8);
      this.rx2.buf.set(r.subarray(9, 9 + take)); this.rx2.got = take;
      return this.v2took(1, room);
    }
    if (this.v2open && this.rx2 && s >= 2 && s <= 0xFD) {
      const x = this.rx2;
      if (s !== x.seq) {                                          // one is missing (or these follow a "send again"): ask once
        if (x.asked !== x.n) { x.asked = x.n; this.emit(ackOf(false, x.seq, room(x.n), x.id)); }
        return;
      }
      if (this.o.nackOnce && x.n + 1 === this.o.nackOnce && !this.nacked) {      // "send that one again"
        this.nacked = true; x.asked = x.n;
        this.emit(ackOf(false, s, room(x.n), x.id));
        return;
      }
      const take = Math.min(x.total - x.got, cap);
      x.buf.set(r.subarray(1, 1 + take), x.got); x.got += take; x.n++; x.last = s;
      x.seq = s === 0xFD ? 2 : s + 1;                             // 02 to FD and round again: [emu]
      return this.v2took(s, room);
    }
    if (this.v2open && !this.o.oldAfterNew) return;
    // the old framing, a message's first report
    if (s === 0x01 && !this.rx) {                                 // the report "01" that [kit] sent after a program
      this.releases++;
      if (this.pending) { const p = this.pending; this.pending = null; this.keep(p); }
      return;
    }
    if (s !== 0x00) { this.rx = null; return; }                   // out of order: the message in hand is dropped
    if (Date.now() < this.quietUntil) return;                     // still busy with what it dropped
    const cmd = r[1];
    if (cmd === 0xFA || cmd === 0xFF || cmd === 0xF9) { this.rx = null; return this.message(r.slice(1, 2), 'old', 1); }
    const total = 6 + be(r, 3), take = Math.min(total, cap);
    this.rx = { total: total, buf: new Uint8Array(total), got: take, seq: 1, n: 1, dropped: false };
    this.rx.buf.set(r.subarray(1, 1 + take));
    if (this.rx.got >= this.rx.total) { const x = this.rx; this.rx = null; return this.message(x.buf, 'old', x.n); }
  };

  // A report of a newer-framing message was taken: acknowledge at the end, and on the way if it is that kind.
  MockPrime.prototype.v2took = function (seq, room) {
    const x = this.rx2;
    if (!x) return;
    if (x.got >= x.total) {
      this.rx2 = null;
      this.sendAck(ackOf(true, seq, room(x.n), x.id));
      return this.message(x.buf, 'new', x.n);
    }
    if (this.o.ackEvery && x.n % this.o.ackEvery === 0) this.sendAck(ackOf(true, seq, room(x.n), x.id));
  };
  MockPrime.prototype.sendAck = function (a) { this.emit(a); this.lastAck = a; };
  // Its clock ([kit]: "repeats that about every 0.5 s"): while a message is coming in, an acknowledgement of what has
  // come so far; otherwise the last one again.
  MockPrime.prototype.tick = function () {
    if (this.dead) return this.stop();
    const cap = this.size - 1, x = this.rx2;
    if (x) { const a = ackOf(true, x.last || 1, (cap - 8) + (x.n - 1) * cap, x.id); this.emit(a); this.lastAck = a; }
    else if (this.lastAck && !this.sendingNew) this.emit(this.lastAck);
  };

  // A reply, in the framing the request came in.
  MockPrime.prototype.reply = function (msg, framing) {
    const cap = this.size - 1, self = this;
    if (framing === 'new') {                                      // in its turn, and without holding up what the host sends meanwhile
      this.sendingNew++;
      this.tail = this.tail.then(function () { return self.sendNew(msg); }).catch(function (e) { self.error = String(e && e.stack || e); }).then(function () { self.sendingNew--; });
      return;
    }
    let seq = 0, o = 0;
    do {
      this.emit(join([[seq], msg.subarray(o, o + cap)]));
      o += cap;
      seq = this.o.wrap === 'early' ? (seq === 0xFD ? 0 : seq + 1) : (seq === 0xFE ? 0 : seq + 1);
    } while (o < msg.length);
  };
  // The next acknowledgement the host sent about message id, or null after ms.
  MockPrime.prototype.nextAck = async function (id, ms) {
    const end = Date.now() + ms, self = this;
    for (;;) {
      for (let k = 0; k < this.ackQ.length; k++) if (this.ackQ[k].id === id) return this.ackQ.splice(k, 1)[0];
      const left = end - Date.now();
      if (left <= 0 || this.dead) return null;
      await new Promise(function (res) {
        const t = setTimeout(function () { self.ackWaiter = null; res(); }, left);
        self.ackWaiter = function () { clearTimeout(t); res(); };
      });
    }
  };
  // A message of the newer framing, sent the way [emu] reads the Connectivity Kit's own sending: `window` reports,
  // then a wait for the other side's acknowledgement, and the same reports again after retryMs without one.
  MockPrime.prototype.sendNew = async function (msg) {
    const cap = this.size - 1, id = this.outId++, frames = [];
    frames.push(join([[0x01], l32(id), l32(msg.length), msg.subarray(0, cap - 8)]));
    let seq = 2;
    for (let o = cap - 8; o < msg.length; o += cap) { frames.push(join([[seq], msg.subarray(o, o + cap)])); seq = seq === 0xFD ? 2 : seq + 1; }
    const n = frames.length, at = function (p) { return p < cap - 8 ? 0 : 1 + Math.floor((p - (cap - 8)) / cap); };
    let i = 0, acked = 0, tries = 0;
    while (!this.dead) {
      while (i < n && (!this.o.needAck || !this.o.window || i - acked < this.o.window)) { this.emit(frames[i]); i++; }
      if (!this.o.needAck) return;
      const a = await this.nextAck(id, this.o.retryMs);
      if (!a) {                                                   // nothing came: the same reports again
        if (++tries > 4) { this.gaveUp++; return; }
        this.resent += i - acked; i = acked;
        continue;
      }
      if (a.ok) {
        let k = Math.min(i, at(a.pos));
        if (this.o.ackPos === 'size' && i >= n && a.pos >= msg.length) k = n;
        if (k > acked) { acked = k; tries = 0; }
        if (acked >= n) return;
      } else if (a.seq) {                                         // "send again from this one"
        let j = -1;
        for (let k = i - 1; k >= 0; k--) if (frames[k][0] === a.seq) { j = k; break; }
        if (j >= 0) { i = j; if (acked > j) acked = j; this.goBacks++; }
      }
    }
  };

  MockPrime.prototype.keep = function (p) {
    let src = p.source;
    if (this.o.cutAt !== null) src = src.slice(0, this.o.cutAt);
    this.programs[p.name] = src;
    p.kept = true;
  };

  MockPrime.prototype.message = async function (m, framing, n) {
    this.handled++;
    if (framing === 'new') this.handledNew++;
    if ((this.o.deadAfter !== null && this.handled > this.o.deadAfter) || (framing === 'new' && this.o.deadAfterNew !== null && this.handledNew > this.o.deadAfterNew)) { this.dead = true; this.stop(); return; }
    const cmd = m[0], head = function (c, v, body) { return join([[c, v], b32(body.length), body]); };
    if (framing === 'new' && this.o.fdFirst && cmd !== 0xFD && !this.fds.some(function (x) { return x.framing === 'new'; })) return;   // acknowledged, and not listened to
    if (cmd === 0xFF) return this.reply(Uint8Array.of(0x59), framing);
    if (cmd === 0xFA) {
      const body = new Uint8Array(108), put = function (s, at) { for (let i = 0; i < s.length; i++) body[at + i] = s.charCodeAt(i); };
      body[108 - 36] = this.o.build & 255; body[108 - 35] = this.o.build >> 8;
      put(this.o.version, 108 - 32); put(this.o.serial, 108 - 16);
      return this.reply(head(0xFA, this.fmt, body), framing);
    }
    if (cmd === 0xFD) {                                           // "the newest version I speak"
      const kind = (m.length >= 7 && m[1] === 1 && be(m, 2) === 1 && m[6] === 3) ? 'long' : (m[1] === 3 ? 'short' : null);
      const want = framing === 'new' ? this.o.fdNew : this.o.fdOld;
      this.fds.push({ kind: kind, framing: framing });
      if (kind && (want === kind || want === 'both')) {
        this.fmt = 3;
        if (this.o.fdReply) return this.reply(kind === 'long' ? Uint8Array.of(0xFD, 1, 0, 0, 0, 1, 3) : Uint8Array.of(0xFD, 3, 0, 0, 0, 0), framing);
      }
      return;
    }
    if (cmd === 0xF7) {
      const rec = { name: null, layout: m[1] === 3 ? 'v3' : 'v1', framing: framing, reports: n, bytes: m.length, kept: false };
      this.arrived.push(rec);
      if (m[1] === 3) {
        if (!(this.o.takeV3 === true || (this.o.takeV3 === 'fmt3' && this.fmt === 3))) { rec.why = 'version 03 while it speaks 0' + this.fmt; return; }
        if (be(m, 2) !== m.length - 6) { rec.why = 'length'; return; }
        let inner;
        try { inner = await through(m.subarray(10), new DecompressionStream('deflate')); } catch (e) { rec.why = 'zlib'; return; }
        if (inner.length !== le(m, 6)) { rec.why = 'uncompressed length'; return; }
        const nl = inner[1], want = inner[2] | (inner[3] << 8), z = inner.slice();
        z[2] = 0; z[3] = 0;
        const all = join([[0xF7, 0x03], b32(z.length), z]);
        if (crc(all, 0, all.length) !== want) { rec.why = 'checksum'; return; }
        if (inner[0] !== 0x06 || inner[inner.length - 1] !== 0 || inner[inner.length - 2] !== 0) { rec.why = 'shape'; return; }
        rec.name = text(inner.subarray(4, 4 + nl)); rec.source = text(inner.subarray(4 + nl, inner.length - 2));
      } else if (m[1] === 1) {
        if (!(this.o.takeV1 === true || (this.o.takeV1 === 'fmt1' && this.fmt === 1))) { rec.why = 'version 01 while it speaks 0' + this.fmt; return; }
        if (be(m, 2) !== m.length - 6) { rec.why = 'length'; return; }
        const nl = m[7], want = m[8] | (m[9] << 8), z = m.slice();
        z[8] = 0; z[9] = 0;
        if (crc(z, 0, z.length - 6) !== want) { rec.why = 'checksum'; return; }
        if (m[6] !== 0x06) { rec.why = 'shape'; return; }
        rec.name = text(m.subarray(10, 10 + nl)); rec.source = text(m.subarray(10 + nl));
      } else { rec.why = 'version'; return; }
      if (framing === 'old' && (this.o.needRelease === true || this.o.needRelease === rec.layout)) { this.pending = rec; return; }
      this.keep(rec);
      return;
    }
    if (cmd === 0xF8 || cmd === 0xEB) {
      const nl = m[7], want = m[8] | (m[9] << 8), z = m.slice();
      z[8] = 0; z[9] = 0;
      if (be(m, 2) !== m.length - 6 || crc(z, 0, z.length - 6) !== want || m[6] !== 0x06) return;
      let name = text(m.subarray(10, 10 + nl));
      const nul = name.charAt(name.length - 1) === '\u0000';
      if (nul) name = name.slice(0, -1);
      if (cmd === 0xEB) { if (!nul && !this.o.keepOnDelete) delete this.programs[name]; return; }   // a delete's name has no NUL
      if (this.o.silentF8 || (this.o.needNul === true && !nul) || (this.o.needNul === 'never' && nul) || !(name in this.programs)) return;
      const src = bytes(this.o.crlf ? this.programs[name].replace(/\n/g, '\r\n') + '\r\n' : this.programs[name]), nm = bytes(name);
      let out;
      if (this.fmt === 3) {                                       // it answers in the version it speaks, whichever was asked: [log]
        const inner = join([[0x06, nm.length, 0, 0], nm, src, [0, 0]]);
        const all = join([[0xF7, 0x03], b32(inner.length), inner]);
        const c = crc(all, 0, all.length);
        inner[2] = c & 255; inner[3] = c >> 8;
        const stream = await through(inner, new CompressionStream('deflate'));
        out = join([[0xF7, 0x03], b32(stream.length + 4), l32(inner.length), stream]);
      } else {
        out = head(0xF7, 0x01, join([[0x06, nm.length, 0, 0], nm, src]));
        const c = crc(out, 0, out.length - 6);
        out[8] = c & 255; out[9] = c >> 8;
      }
      for (let k = 0; k < this.o.copies; k++) this.reply(out, framing);
      return;
    }
  };

  function goneError(why) { const e = new Error(why); e.name = 'Gone'; return e; }

  // A port for Link, straight onto the mock (the Node tests).
  MockPrime.prototype.port = function () {
    const self = this, q = [];
    let waiter = null, gone = null;
    this.onreport = function (r) { port.received++; if (waiter) { const w = waiter; waiter = null; w(r); } else q.push(r); };
    const port = {
      reportSize: this.size, sent: 0, received: 0,
      send: function (frame) {
        if (gone) return Promise.reject(goneError(gone));
        const r = new Uint8Array(self.size);
        r.set(frame); port.sent++;
        return self.receive(r).then(function () { if (gone) throw goneError(gone); });
      },
      read: function (ms) {
        if (q.length) return Promise.resolve(q.shift());
        if (gone) return Promise.reject(goneError(gone));
        return new Promise(function (res, rej) {
          const t = setTimeout(function () { waiter = null; res(null); }, ms);
          waiter = function (r) { clearTimeout(t); if (r === null) rej(goneError(gone)); else res(r); };
        });
      },
      poll: function () { return q.length ? q.shift() : null; },
      drain: function () { const n = q.length; q.length = 0; return n; },
      lose: function (why) {
        if (gone) return;
        gone = why || 'the calculator went off the cable'; self.dead = true; self.stop();
        if (waiter) { const w = waiter; waiter = null; w(null); }
      }
    };
    this.unplug = function () { port.lose(); };
    return port;
  };

  // A fake navigator.hid, for a page.  -> the mock, kept at window.__prime for the test to look at.
  MockPrime.install = function (opts) {
    const mock = new MockPrime(opts), listeners = [];
    const bits = mock.size * 8;
    const device = {
      vendorId: 0x03F0, productId: mock.o.product, productName: mock.o.product === 0x2441 ? 'HP Prime' : 'Prime Graphing Calculator', opened: false,
      collections: [{ usagePage: 0xFF81, usage: 0x82,
        inputReports: [{ reportId: 0, items: [{ reportSize: 8, reportCount: bits / 8 }] }],
        outputReports: [{ reportId: 0, items: [{ reportSize: 8, reportCount: bits / 8 }] }], featureReports: [] }],
      open: async function () {
        if (mock.o.busy) throw new DOMException('Failed to open the device.', 'NotAllowedError');
        device.opened = true;
      },
      close: async function () { device.opened = false; },
      sendReport: function (id, data) {
        if (mock.unplugged) return mock.o.hang ? new Promise(function () {}) : Promise.reject(new DOMException('Failed to write the report.', 'NotAllowedError'));
        if (!device.opened) return Promise.reject(new DOMException('The device must be opened first.', 'InvalidStateError'));
        const b = data instanceof Uint8Array ? data : new Uint8Array(data.buffer || data);
        mock.lastLength = b.length;
        return mock.receive(b).then(function () { if (mock.unplugged && mock.o.hang) return new Promise(function () {}); });
      },
      addEventListener: function (t, fn) { if (t === 'inputreport') listeners.push(fn); },
      removeEventListener: function (t, fn) { const i = listeners.indexOf(fn); if (i >= 0) listeners.splice(i, 1); }
    };
    mock.onreport = function (r) { listeners.slice().forEach(function (fn) { fn({ data: new DataView(r.buffer, r.byteOffset, r.byteLength), device: device, reportId: 0 }); }); };
    mock.device = device;
    const gone = [];
    const hid = {
      requestDevice: async function () { mock.asked = (mock.asked || 0) + 1; return mock.o.none ? [] : [device]; },
      getDevices: async function () { return []; },
      addEventListener: function (t, fn) { if (t === 'disconnect') gone.push(fn); }, removeEventListener: function () {}
    };
    // The cable pulled out, or the calculator switched off: the browser tells the page, and writes fail from here
    // (or, with `hang`, never come back).
    mock.unplug = function () {
      if (mock.unplugged) return;
      mock.unplugged = true; mock.dead = true; mock.stop();
      setTimeout(function () { device.opened = false; gone.slice().forEach(function (fn) { fn({ device: device }); }); }, mock.o.tellAfter || 0);
    };
    Object.defineProperty(navigator, 'hid', { value: hid, configurable: true });
    window.__prime = mock;
    return mock;
  };

  return MockPrime;
})();

if (typeof module !== 'undefined') module.exports = MockPrime;
