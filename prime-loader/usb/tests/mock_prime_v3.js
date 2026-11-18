// mock_prime_v3.js -- a pretend HP Prime on a pretend cable, for the tests of prime_usb_v3.js and of the Loader that
// uses it.  Roger Metcalf & Claude, 17 Nov 2026.
//
// IT IS NOT A CALCULATOR.  By default it does what the author's G2 and G1 did on 17 Nov 2026, as far as the five logs
// of ../logs/ go (both on firmware build 15751); each line below marked [log] is something one of those logs shows.
// What the logs do not show has a switch and a default that says so.  Its byte work is written apart from
// prime_usb_v3.js (its own checksum, its own framing), so that a slip in one is not hidden by the same slip in the other.
//
// THE OLD FRAMING [log]
//   fmt 1           "who are you" (FA) is answered with version 01
//   fdOld 'long'    told "FD 01 00 00 00 01 03" it answers the same seven bytes and speaks version 03 from then on
//                   ('short': FD 03; 'both'; null: it takes neither and stays at 01, which no calculator here did)
//   maxOld 255      a message of more reports than this is not kept (254 and 255 were; 274 and 263 were not)
//   nulTail true    what it gives back ends in two zero bytes more than it was sent
//   needNul true    it answers a request (F8 01 or F8 03) whose name ends in a NUL, and no other
//   wrap 'hplp'     its long replies are numbered 00 ... FE and then 00
// THE NEWER FRAMING [log]
//   v2 true, ecReply null   it takes "FF EC" and sends no report of its own in answer
//   ackEvery 77     it acknowledges every 77th report of a message as it comes, with the number of the report it wants
//                   next and the room of those it has; and the whole, with the number of its last report
//   nack true       a report out of turn is answered at once with "send again", the report it wants and the room of
//                   what it has; once for each place it stands at (the G2 said it for the first of two such reports)
//   tickMs 600      its clock: so long after its last word, and again and again, it says where it stands.  In the
//                   middle of a message: the report it wants next and the room of what it has.  Otherwise: its last
//                   acknowledgement again, with FF for the report.  (A G1's clock was slower and less even.)
//   tickNack        ... and in the middle of a message that word is a "send again" until the message's first
//                   acknowledgement has gone (true for a G2; a G1's was an acknowledgement every time)
//   tickOnReport 0  the clock speaks just after this report of a message has come, once in each message long enough
//                   (the G2 did after the first report of its longest message, 0.6 s after its last acknowledgement)
//   tickLate 1      ... and that word reaches the host only when so many more reports have come and been taken: it is
//                   out of date by then, as the G2's was (it named report 02, which the G2 then took)
//   window 240, needAck true   when IT sends: it stops once so many reports' worth is unacknowledged, and stands
//                   there until the host acknowledges.  While it stands it acknowledges what comes and answers nothing.
//   oldFlush true   ... until a request comes in the old framing: then the rest of the answer that stood goes out
//                   unacknowledged, numbered on in the old way (FE, 00, 01 ...), and the answers that waited behind
//                   it follow in the old framing (the G1, at 210 s)
//   takeV3 false    a program sent compressed ("F7 03") is acknowledged and not kept, whatever version it speaks
//                   (true: kept, which no calculator here did)
//   fmt 3 answers   once it speaks 03 it gives a program back compressed, as "F7 03" with a zlib stream that begins 78 01
//   lagMs 0, lagPerChar 0   how long before an answer to a request begins; a G1 took 3.1 s over 289,813 characters
//                   and a G2 0.9 s, since they compress it first
//   firstId 3       the number of its own first message
// NOT FROM A LOG, EACH WITH ITS SWITCH
//   fdNew 'long'    what it does with "FD" in the newer framing (never sent to a calculator)
//   drop []         names of programs it acknowledges and does not keep
//   loseAt 0        it loses this report of a message (counted from 1), once
//   cutAt null      it keeps only so many characters of a program
//   copies 1        how many times it sends a file for one request
//   crlf            it gives a program back with CRLF line ends and one more at the end
//   silentF8        it answers no request for a program;  keepOnDelete: a delete takes nothing off
//   deadAfter k     it answers nothing after its k-th message;  deadAfterNew k: after its k-th of the newer framing
//   busy            the browser cannot open it (another program has it);  none: the browser's list is empty
//   dieAt 0         it goes off the cable when this many reports have come from the host
//   muteAt 0        it stays on the cable and says nothing more when this many reports have come
//   hang false      ... and a write to it afterwards never comes back, as Chrome's did on 17 Nov [log]
//   stallMs, busyMs what the old framing does at a report too many: the cable stands, then it answers nothing for a while [log]

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
  // The next turn of the event loop, without a timer's millisecond: what the mock sends arrives while the host is
  // still sending, as a calculator's does, and not only when the host stops to wait.
  const soon = typeof setImmediate === 'function' ? function (f) { setImmediate(f); } : (function () {
    const q = [], ch = new MessageChannel();
    ch.port1.onmessage = function () { const f = q.shift(); if (f) f(); };
    return function (f) { q.push(f); ch.port2.postMessage(0); };
  })();

  function MockPrime(opts) {
    const g2 = !opts || opts.product === undefined || opts.product === 0x2441;
    this.o = Object.assign({ product: 0x2441, build: 15751, version: null, serial: 'SECRETSERIAL0001',
      fmt: 1, fdOld: 'long', fdNew: 'long', fdReply: true, maxOld: 255, stallMs: 0, busyMs: 0, nulTail: true, needNul: true, wrap: 'hplp',
      v2: true, ecReply: null, ackEvery: 77, nack: true, tickMs: 600, tickNack: g2, tickOnReport: 0, tickLate: 1, window: 240, needAck: true, oldFlush: true,
      takeV3: false, lagMs: 0, lagPerChar: 0, firstId: 3,
      drop: [], loseAt: 0, cutAt: null, copies: 1, crlf: false, silentF8: false, keepOnDelete: false, deadAfter: null, deadAfterNew: null,
      busy: false, none: false, dieAt: 0, muteAt: 0, hang: false }, opts || {});
    if (!this.o.version) this.o.version = this.o.product === 0x2441 ? 'V2.060.650' : 'V0.050.640';
    this.size = this.o.reportSize || (this.o.product === 0x2441 ? 1024 : 64);
    this.fmt = this.o.fmt;         // the version it speaks now
    this.programs = {};            // name -> source text, as stored
    this.arrived = [];             // {name, layout, framing, reports, bytes, kept, why}
    this.fds = [];                 // {kind, framing}: each "FD" that came
    this.handled = 0; this.handledNew = 0; this.releases = 0; this.reportsIn = 0; this.reportsOut = 0;
    this.hostAcks = [];            // every acknowledgement the host sent: {ok, seq, pos, id}
    this.outOfTurn = 0;            // reports of a newer-framing message that came when another was wanted (sent twice, or after a gap)
    this.nacks = 0; this.statuses = 0;      // "send again" for a report out of turn; words of its clock in the middle of a message
    this.waits = [];               // {id, at, ms}: each time it stood, sending, until the host acknowledged
    this.flushed = 0;              // reports of a newer-framing answer that went out numbered in the old way
    this.v2open = false; this.outId = this.o.firstId;
    this.rx = null;                // the old framing's message being put together
    this.rx2 = null;               // the newer framing's
    this.chain = Promise.resolve(); this.tail = Promise.resolve();
    this.onreport = null;          // set by whoever listens
    this.dead = false; this.quietUntil = 0; this.lost = false;
    this.ackQ = []; this.ackWaiter = null; this.clock = null; this.lastAck = null; this.sendingNew = 0; this.standing = null; this.outOld = false;
  }

  MockPrime.prototype.emit = function (frame) {
    const r = new Uint8Array(this.size), self = this;
    r.set(frame);
    this.reportsOut++;
    soon(function () { if (self.onreport && !self.dead) self.onreport(r); });
  };
  MockPrime.prototype.stop = function () { if (this.clock) { clearTimeout(this.clock); this.clock = null; } };
  // Its clock starts again at every word it says.
  MockPrime.prototype.arm = function () {
    const self = this;
    this.stop();
    if (!this.o.tickMs || this.dead || !this.v2open) return;
    this.clock = setTimeout(function () { self.clock = null; self.tick(); }, this.o.tickMs);
    if (this.clock.unref) this.clock.unref();
  };
  MockPrime.prototype.say = function (a, last) { this.emit(a); if (last) this.lastAck = a; this.arm(); };
  // Where it stands in the message that is coming in.
  MockPrime.prototype.status = function () {
    const x = this.rx2, cap = this.size - 1;
    this.statuses++;
    this.say(ackOf(!(this.o.tickNack && x.acks === 0), x.seq, (cap - 8) + (x.n - 1) * cap, x.id), false);
  };
  MockPrime.prototype.tick = function () {
    if (this.dead) return;
    if (this.rx2) return this.status();
    if (this.lastAck) { const a = this.lastAck.slice(); a[2] = 0xFF; this.emit(a); }
    this.arm();
  };

  // One report from the host.  Reports are padded to their full size, as Windows and WebHID deliver them.
  MockPrime.prototype.receive = function (report) {
    const self = this, r = Uint8Array.from(report);
    this.reportsIn++;
    if (this.o.dieAt && this.reportsIn === this.o.dieAt && this.unplug) { this.unplug(); return Promise.resolve(); }
    if (this.o.muteAt && this.reportsIn >= this.o.muteAt) { this.dead = true; this.stop(); }
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
        this.v2open = true; this.outOld = false;
        if (this.o.ecReply) this.emit(Uint8Array.from(this.o.ecReply));
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
      this.outOld = false;
      this.rx2 = { id: id, total: total, buf: new Uint8Array(total), got: 0, seq: 2, n: 1, asked: -1, acks: 0, ticked: false };
      if (!this.clock) this.arm();                                // its clock runs while a message is coming in, whether or not it has said anything yet
      const take = Math.min(total, cap - 8);
      this.rx2.buf.set(r.subarray(9, 9 + take)); this.rx2.got = take;
      return this.v2took(1, room);
    }
    if (this.v2open && this.rx2 && s >= 2 && s <= 0xFD) {
      const x = this.rx2;
      if (this.o.loseAt && x.n + 1 === this.o.loseAt && s === x.seq && !this.lost) { this.lost = true; return; }     // this one never arrives
      if (s !== x.seq) {                                          // not the one it wants: "send again", once for this place
        this.outOfTurn++;
        if (this.o.nack && x.asked !== x.n) { x.asked = x.n; this.nacks++; this.say(ackOf(false, x.seq, room(x.n), x.id), false); }
        return;
      }
      const take = Math.min(x.total - x.got, cap);
      x.buf.set(r.subarray(1, 1 + take), x.got); x.got += take; x.n++;
      x.seq = s === 0xFD ? 2 : s + 1;                             // 02 to FD and round again
      return this.v2took(s, room);
    }
    // the old framing, a message's first report
    if (s === 0x01 && !this.rx) { this.releases++; return; }      // the report "01" that hp-prime-kit sent after a program
    if (s !== 0x00) { this.rx = null; return; }                   // out of order: the message in hand is dropped
    if (Date.now() < this.quietUntil) return;                     // still busy with what it dropped
    if (this.standing && this.o.oldFlush) this.flush();           // [log]: the answer that stood goes out now, unacknowledged
    const cmd = r[1];
    if (cmd === 0xFA || cmd === 0xFF || cmd === 0xF9) { this.rx = null; return this.message(r.slice(1, 2), 'old', 1); }
    const total = 6 + be(r, 3), take = Math.min(total, cap);
    this.rx = { total: total, buf: new Uint8Array(total), got: take, seq: 1, n: 1, dropped: false };
    this.rx.buf.set(r.subarray(1, 1 + take));
    if (this.rx.got >= this.rx.total) { const x = this.rx; this.rx = null; return this.message(x.buf, 'old', x.n); }
  };

  // A report of a newer-framing message was taken: acknowledge every 77th and the whole; and the clock, if it is
  // set to speak here.
  MockPrime.prototype.v2took = function (seq, room) {
    const x = this.rx2;
    if (!x) return;
    if (x.got >= x.total) {
      this.rx2 = null;
      this.say(ackOf(true, seq, room(x.n), x.id), true);
      return this.message(x.buf, 'new', x.n);
    }
    if (this.o.ackEvery && x.n % this.o.ackEvery === 0) { x.acks++; this.say(ackOf(true, x.seq, room(x.n), x.id), true); }
    if (x.held && x.n >= x.held.at) { const a = x.held.a; x.held = null; this.statuses++; this.say(a, false); }
    if (this.o.tickOnReport && x.n === this.o.tickOnReport && !x.ticked) {
      x.ticked = true;
      const a = ackOf(!(this.o.tickNack && x.acks === 0), x.seq, room(x.n), x.id);       // what the clock says now ...
      if (this.o.tickLate) x.held = { a: a, at: x.n + this.o.tickLate };                   // ... heard only later
      else { this.statuses++; this.say(a, false); }
    }
  };

  // A reply, in the framing the request came in; after `lag` ms, in its turn behind the replies before it.
  MockPrime.prototype.reply = function (msg, framing, lag) {
    const cap = this.size - 1, self = this;
    if (framing === 'new' || this.sendingNew) {                   // in its turn, and without holding up what the host sends meanwhile
      this.sendingNew++;
      this.tail = this.tail.then(function () { return lag ? pause(lag) : null; })
        .then(function () { return (framing === 'new' && !self.outOld) ? self.sendNew(msg) : self.sendOld(msg); })
        .catch(function (e) { self.error = String(e && e.stack || e); }).then(function () { self.sendingNew--; });
      return;
    }
    if (lag) { this.sendingNew++; this.tail = this.tail.then(function () { return pause(lag); }).then(function () { self.sendOld(msg); self.sendingNew--; }); return; }
    this.sendOld(msg);
  };
  MockPrime.prototype.sendOld = function (msg) {
    const cap = this.size - 1;
    let seq = 0, o = 0;
    do {
      this.emit(join([[seq], msg.subarray(o, o + cap)]));
      o += cap;
      seq = this.o.wrap === 'early' ? (seq === 0xFD ? 0 : seq + 1) : (seq === 0xFE ? 0 : seq + 1);
    } while (o < msg.length);
  };
  // The next acknowledgement the host sends about message id; null if the answer is to be flushed instead, or the
  // mock has gone.
  MockPrime.prototype.nextAck = async function (id) {
    const self = this;
    for (;;) {
      for (let k = 0; k < this.ackQ.length; k++) if (this.ackQ[k].id === id) return this.ackQ.splice(k, 1)[0];
      if (this.dead || this.outOld) return null;
      await new Promise(function (res) { self.ackWaiter = res; });
    }
  };
  // [log]: when it sends, it stops once `window` reports' worth is unacknowledged and stands there until the host
  // acknowledges; the logs show no report sent a second time and no end to the standing.
  MockPrime.prototype.sendNew = async function (msg) {
    const cap = this.size - 1, id = this.outId++, frames = [];
    frames.push(join([[0x01], l32(id), l32(msg.length), msg.subarray(0, cap - 8)]));
    let seq = 2;
    for (let o = cap - 8; o < msg.length; o += cap) { frames.push(join([[seq], msg.subarray(o, o + cap)])); seq = seq === 0xFD ? 2 : seq + 1; }
    const n = frames.length, room = function (k) { return k < 1 ? 0 : (cap - 8) + (k - 1) * cap; };
    const at = function (p) { return p < cap - 8 ? 0 : 1 + Math.floor((p - (cap - 8)) / cap); };
    let i = 0, acked = 0;
    while (!this.dead) {
      while (i < n && (!this.o.needAck || room(i) - room(acked) < this.o.window * cap)) { this.emit(frames[i]); i++; }
      if (!this.o.needAck || acked >= n) return;
      const t = Date.now();
      this.standing = { id: id, at: i };
      const a = await this.nextAck(id);
      this.standing = null;
      this.waits.push({ id: id, at: i, ms: Date.now() - t });
      if (!a) {
        if (this.outOld && !this.dead) {                          // the rest, numbered on in the old way and not waited for
          let s = frames[i - 1][0];
          for (; i < n; i++) { s = s === 0xFE ? 0 : s + 1; this.emit(join([[s], frames[i].subarray(1)])); this.flushed++; }
        }
        return;
      }
      if (a.ok) { const k = Math.min(i, at(a.pos)); if (k > acked) acked = k; if (acked >= n) return; }
      else { const k = Math.min(i, at(a.pos)); i = k; if (acked > k) acked = k; }                 // the host asks for one again
    }
  };
  MockPrime.prototype.flush = function () {
    this.outOld = true;
    if (this.ackWaiter) { const w = this.ackWaiter; this.ackWaiter = null; w(); }
  };

  MockPrime.prototype.keep = function (p) {
    let src = p.source;
    if (this.o.cutAt !== null) src = src.slice(0, this.o.cutAt);
    if (this.o.drop.indexOf(p.name) >= 0) { p.why = 'dropped'; return; }
    this.programs[p.name] = src;
    p.kept = true;
  };

  MockPrime.prototype.message = async function (m, framing, n) {
    this.handled++;
    if (framing === 'new') this.handledNew++;
    if ((this.o.deadAfter !== null && this.handled > this.o.deadAfter) || (framing === 'new' && this.o.deadAfterNew !== null && this.handledNew > this.o.deadAfterNew)) { this.dead = true; this.stop(); return; }
    const cmd = m[0], head = function (c, v, body) { return join([[c, v], b32(body.length), body]); };
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
        if (this.o.takeV3 !== true) { rec.why = 'compressed'; return; }
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
        if (be(m, 2) !== m.length - 6) { rec.why = 'length'; return; }
        const nl = m[7], want = m[8] | (m[9] << 8), z = m.slice();
        z[8] = 0; z[9] = 0;
        if (crc(z, 0, z.length - 6) !== want) { rec.why = 'checksum'; return; }
        if (m[6] !== 0x06) { rec.why = 'shape'; return; }
        rec.name = text(m.subarray(10, 10 + nl)); rec.source = text(m.subarray(10 + nl));
      } else { rec.why = 'version'; return; }
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
      const stored = this.programs[name];
      const src = bytes(this.o.crlf ? stored.replace(/\n/g, '\r\n') + '\r\n' : stored), nm = bytes(name), end = this.o.nulTail ? [0, 0] : [];
      let out;
      if (this.fmt === 3) {                                       // it answers in the version it speaks, whichever was asked: [log]
        const inner = join([[0x06, nm.length, 0, 0], nm, src, [0, 0]]);
        const all = join([[0xF7, 0x03], b32(inner.length), inner]);
        const c = crc(all, 0, all.length);
        inner[2] = c & 255; inner[3] = c >> 8;
        const stream = await through(inner, new CompressionStream('deflate'));
        stream[1] = 0x01;                                         // [log]: the calculators' streams begin 78 01 (the level it claims; the stream reads the same)
        out = join([[0xF7, 0x03], b32(stream.length + 4), l32(inner.length), stream]);
      } else {
        out = head(0xF7, 0x01, join([[0x06, nm.length, 0, 0], nm, src, end]));
        const c = crc(out, 0, out.length - 6);
        out[8] = c & 255; out[9] = c >> 8;
      }
      const lag = this.o.lagMs + Math.round(this.o.lagPerChar * stored.length);
      for (let k = 0; k < this.o.copies; k++) this.reply(out, framing, lag);
      return;
    }
  };

  function goneError(why) { const e = new Error(why); e.name = 'Gone'; return e; }

  // A port for Link, straight onto the mock (the Node tests).  A write comes back a turn of the event loop after
  // the mock has taken the report, so that what the mock says can arrive between two writes, as on a cable.
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
        return self.receive(r).then(function () { return new Promise(soon); }).then(function () { if (gone) throw goneError(gone); });
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
        device.opened = true; mock.opens = (mock.opens || 0) + 1;
      },
      close: async function () { device.opened = false; mock.closes = (mock.closes || 0) + 1; },
      sendReport: function (id, data) {
        if (mock.unplugged) return mock.o.hang ? new Promise(function () {}) : Promise.reject(new DOMException('Failed to write the report.', 'NotAllowedError'));
        if (!device.opened) return Promise.reject(new DOMException('The device must be opened first.', 'InvalidStateError'));
        const b = data instanceof Uint8Array ? data : new Uint8Array(data.buffer || data);
        mock.lastLength = b.length;
        return mock.receive(b).then(function () { return new Promise(soon); }).then(function () { if (mock.unplugged && mock.o.hang) return new Promise(function () {}); });
      },
      addEventListener: function (t, fn) { if (t === 'inputreport') listeners.push(fn); },
      removeEventListener: function (t, fn) { const i = listeners.indexOf(fn); if (i >= 0) listeners.splice(i, 1); }
    };
    mock.onreport = function (r) { listeners.slice().forEach(function (fn) { fn({ data: new DataView(r.buffer, r.byteOffset, r.byteLength), device: device, reportId: 0 }); }); };
    mock.device = device;
    const gone = [];
    const hid = {
      requestDevice: async function () { mock.asked = (mock.asked || 0) + 1; if (mock.o.none) return []; mock.granted = true; return [device]; },
      // (the browser lists the calculators the page was let talk to before that are on a cable now)
      getDevices: async function () { return mock.granted && !mock.unplugged ? [device] : []; },
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
