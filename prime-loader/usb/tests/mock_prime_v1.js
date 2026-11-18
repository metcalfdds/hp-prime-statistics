// mock_prime_v1.js -- a pretend HP Prime on a pretend cable, for the tests of prime_usb_v1.js and of the pages that use
// it.  Roger Metcalf & Claude, 17 Nov 2026.
//
// IT IS NOT A CALCULATOR.  It answers the way three public descriptions say a G2 answers (the same three the code under
// test was written from: hp-prime-kit's docs/topics/usb.md, hp-prime-web's docs/PROTOCOL.md, PrimeDev's PrimeWeb/Frames),
// so a test that passes here says the page and the mock read those descriptions the same way, and no more.  Its byte
// work is written apart from prime_usb_v1.js (its own checksum, its own framing) so that a slip in one is not hidden
// by the same slip in the other.
//
// It runs in Node and, injected with addInitScript, in a page, where MockPrime.install() puts a fake navigator.hid
// in the browser's place.
//
// What can be switched (opts), each one a way a real calculator might differ or fail:
//   readVers      [1, 3]   the versions of a request for a file that it answers (F8 01 not compressed, F8 03 compressed)
//   keepOnDelete  false    a delete does nothing
//   crlf          false    hands a program back with CR LF line ends and a last newline (the text is the same program)
//   replyVer      3 | 1    the version byte of its replies ([kit] saw 03 on firmware 2.4.15515; [web]'s code expects 01)
//   needNul       true     a request for a file is answered only when the name ends in a NUL ([web]); 'never': only when it does not
//   silentF8      false    never answers a request for a file ([kit]: "answered once, and why not since is not known")
//   maxMessage    Infinity a program whose message is longer is dropped without a word ([web], of G1 firmware: 15,928)
//   maxReports    Infinity ... or one that came in more reports than this (15,928 bytes is about 253 reports of a G1)
//   takeV1/takeV3 true     whether each layout of a program is accepted
//   needRelease   false    a program in the old framing is kept only when a report "01" follows it ([kit] sent one)
//   cutAt         null     stores only the first cutAt characters of a program (a damaged transfer)
//   wrap          'hplp'   its long replies count FD FE 00 01 ('hplp') or FD 00 01 ('early')
//   v2            true     whether it takes the newer framing
//   nackOnce      0        in the newer framing, asks once for this report again
//   deadAfter     null     stops answering after this many messages (a calculator that hangs)
//   busy          false    open() fails, as it does while HP's Connectivity Kit holds the calculator
//   none          false    no calculator on the cable: the browser's chooser comes back empty
//   product       0x2441   a G2; 0x1541 is a G1, whose reports are 64 bytes (reportSize)

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
  function text(b) { let s = ''; for (let i = 0; i + 1 < b.length; i += 2) s += String.fromCharCode(b[i] | (b[i + 1] << 8)); return s; }
  function bytes(s) { const b = new Uint8Array(2 * s.length); for (let i = 0; i < s.length; i++) { b[2 * i] = s.charCodeAt(i) & 255; b[2 * i + 1] = s.charCodeAt(i) >> 8; } return b; }
  function join(parts) { let n = 0; parts.forEach(function (p) { n += p.length; }); const o = new Uint8Array(n); let k = 0; parts.forEach(function (p) { o.set(p, k); k += p.length; }); return o; }
  async function through(b, ts) { const w = ts.writable.getWriter(); w.write(b).catch(function () {}); w.close().catch(function () {}); return new Uint8Array(await new Response(ts.readable).arrayBuffer()); }

  function MockPrime(opts) {
    this.o = Object.assign({ replyVer: 3, needNul: true, silentF8: false, maxMessage: Infinity, takeV1: true, takeV3: true,
      needRelease: false, cutAt: null, readVers: [1, 3], keepOnDelete: false, maxReports: Infinity, crlf: false, wrap: 'hplp', v2: true, nackOnce: 0, deadAfter: null, busy: false, none: false,
      product: 0x2441, build: 15515, version: 'V2.060.650', serial: 'SECRETSERIAL0001' }, opts || {});
    this.size = this.o.reportSize || (this.o.product === 0x2441 ? 1024 : 64);
    this.programs = {};            // name -> source text, as stored
    this.arrived = [];             // {name, layout, framing, reports, bytes, kept}
    this.handled = 0; this.releases = 0; this.hostAcks = []; this.reportsIn = 0; this.reportsOut = 0;
    this.v2open = false; this.outId = 1;
    this.rx = null;                // the old framing's message being put together
    this.rx2 = null;               // the newer framing's
    this.pending = null;           // a program waiting for its report "01" (needRelease)
    this.chain = Promise.resolve();
    this.onreport = null;          // set by whoever listens
    this.dead = false;
  }

  MockPrime.prototype.emit = function (frame) {
    const r = new Uint8Array(this.size);
    r.set(frame);
    this.reportsOut++;
    const self = this;
    setTimeout(function () { if (self.onreport && !self.dead) self.onreport(r); }, 0);
  };

  // One report from the host.  Reports are padded to their full size, as Windows and WebHID deliver them.
  MockPrime.prototype.receive = function (report) {
    const self = this, r = Uint8Array.from(report);
    this.reportsIn++;
    this.chain = this.chain.then(function () { return self.step(r); }).catch(function (e) { self.error = String(e && e.stack || e); });
    return this.chain;
  };

  MockPrime.prototype.step = async function (r) {
    if (this.dead) return;
    const s = r[0], cap = this.size - 1;
    if (s === 0xFF) {                                             // out of band
      if (r[1] === 0xEC && this.o.v2) this.v2open = true;
      return;
    }
    // A report that continues the old-framing message in hand is taken before anything else: its number can be FE,
    // which is also how an acknowledgement begins, or 01, which is also how a message of the newer framing begins,
    // or 00 after FE, which is also how a new message begins.  Only the message's own length tells them apart.
    if (this.rx && s === this.rx.seq) {
      const x = this.rx, take = Math.min(x.total - x.got, cap);
      x.buf.set(r.subarray(1, 1 + take), x.got); x.got += take; x.n++;
      x.seq = s === 0xFE ? 0 : s + 1;                             // FE is followed by 00; FF is never a number
      if (x.got >= x.total) { this.rx = null; return this.message(x.buf, 'old', x.n); }
      return;
    }
    if (s === 0xFE) { this.hostAcks.push({ ok: r[1], seq: r[2], pos: le(r, 4), id: le(r, 8) }); return; }
    // the newer framing
    if (this.v2open && s === 0x01 && le(r, 1) !== 0) {
      const id = le(r, 1), total = le(r, 5);
      this.rx2 = { id: id, total: total, buf: new Uint8Array(total), got: 0, seq: 2, n: 1 };
      const take = Math.min(total, cap - 8);
      this.rx2.buf.set(r.subarray(9, 9 + take)); this.rx2.got = take;
      return this.v2done(1);
    }
    if (this.v2open && this.rx2 && s >= 2 && s <= 0xFD && s === this.rx2.seq) {
      const x = this.rx2, take = Math.min(x.total - x.got, cap);
      if (this.o.nackOnce && s === this.o.nackOnce && !this.nacked) {      // "send that one again"
        this.nacked = true;
        this.emit(join([[0xFE, 0x00, s, 0], [x.got & 255, (x.got >> 8) & 255, (x.got >> 16) & 255, 0], [x.id & 255, (x.id >> 8) & 255, 0, 0]]));
        return;
      }
      x.buf.set(r.subarray(1, 1 + take), x.got); x.got += take; x.seq++; x.n++;
      return this.v2done(s);
    }
    // the old framing, a message's first report
    if (s === 0x01 && !this.rx) {                                 // the report "01" that [kit] sent after a program
      this.releases++;
      if (this.pending) { const p = this.pending; this.pending = null; this.keep(p); }
      return;
    }
    if (s !== 0x00) { this.rx = null; return; }                   // out of order: the message in hand is dropped
    const cmd = r[1];
    if (cmd === 0xFA || cmd === 0xFF || cmd === 0xF9) { this.rx = null; return this.message(r.slice(1, 2), 'old', 1); }
    const total = 6 + be(r, 3), take = Math.min(total, cap);
    this.rx = { total: total, buf: new Uint8Array(total), got: take, seq: 1, n: 1 };
    this.rx.buf.set(r.subarray(1, 1 + take));
    if (this.rx.got >= this.rx.total) { const x = this.rx; this.rx = null; return this.message(x.buf, 'old', x.n); }
  };

  MockPrime.prototype.v2done = function (seq) {
    const x = this.rx2;
    if (!x || x.got < x.total) return;
    this.rx2 = null;
    this.emit(join([[0xFE, 0x01, seq, 0], [x.total & 255, (x.total >> 8) & 255, (x.total >> 16) & 255, 0], [x.id & 255, (x.id >> 8) & 255, (x.id >> 16) & 255, 0]]));
    return this.message(x.buf, 'new', x.n);
  };

  // A reply, in the framing the request came in.
  MockPrime.prototype.reply = function (msg, framing) {
    const cap = this.size - 1;
    if (framing === 'new') {
      if (msg.length > 240 * 1023 - 8) return;                    // more than a message of the newer framing carries ([pd])
      const id = this.outId++;
      this.emit(join([[0x01, id & 255, (id >> 8) & 255, 0, 0, msg.length & 255, (msg.length >> 8) & 255, (msg.length >> 16) & 255, 0], msg.subarray(0, cap - 8)]));
      let seq = 2;
      for (let o = cap - 8; o < msg.length; o += cap) this.emit(join([[seq++], msg.subarray(o, o + cap)]));
      return;
    }
    let seq = 0, o = 0;
    do {
      this.emit(join([[seq], msg.subarray(o, o + cap)]));
      o += cap;
      seq = this.o.wrap === 'early' ? (seq === 0xFD ? 0 : seq + 1) : (seq === 0xFE ? 0 : seq + 1);
    } while (o < msg.length);
  };

  MockPrime.prototype.keep = function (p) {
    let src = p.source;
    if (this.o.cutAt !== null) src = src.slice(0, this.o.cutAt);
    this.programs[p.name] = src;
    p.kept = true;
  };

  MockPrime.prototype.message = async function (m, framing, n) {
    this.handled++;
    if (this.o.deadAfter !== null && this.handled > this.o.deadAfter) { this.dead = true; return; }
    const cmd = m[0], head = function (c, v, body) { return join([[c, v, (body.length >>> 24) & 255, (body.length >>> 16) & 255, (body.length >>> 8) & 255, body.length & 255], body]); };
    if (cmd === 0xFF) return this.reply(Uint8Array.of(0x59), framing);
    if (cmd === 0xFA) {
      const body = new Uint8Array(108), put = function (s, at) { for (let i = 0; i < s.length; i++) body[at + i] = s.charCodeAt(i); };
      body[108 - 36] = this.o.build & 255; body[108 - 35] = this.o.build >> 8;
      put(this.o.version, 108 - 32); put(this.o.serial, 108 - 16);
      return this.reply(head(0xFA, this.o.replyVer, body), framing);
    }
    if (cmd === 0xF7) {
      const rec = { name: null, layout: m[1] === 3 ? 'v3' : 'v1', framing: framing, reports: n, bytes: m.length, kept: false };
      this.arrived.push(rec);
      if (m.length > this.o.maxMessage || n > this.o.maxReports) { rec.why = 'too long'; return; }   // dropped without a word
      if (m[1] === 3) {
        if (!this.o.takeV3) { rec.why = 'layout'; return; }
        if (be(m, 2) !== m.length - 6) { rec.why = 'length'; return; }
        let inner;
        try { inner = await through(m.subarray(10), new DecompressionStream('deflate')); } catch (e) { rec.why = 'zlib'; return; }
        if (inner.length !== le(m, 6)) { rec.why = 'uncompressed length'; return; }
        const nl = inner[1], want = inner[2] | (inner[3] << 8), z = inner.slice();
        z[2] = 0; z[3] = 0;
        const all = join([[0xF7, 0x03, (z.length >>> 24) & 255, (z.length >>> 16) & 255, (z.length >>> 8) & 255, z.length & 255], z]);
        if (crc(all, 0, all.length) !== want) { rec.why = 'checksum'; return; }
        if (inner[0] !== 0x06 || inner[inner.length - 1] !== 0 || inner[inner.length - 2] !== 0) { rec.why = 'shape'; return; }
        rec.name = text(inner.subarray(4, 4 + nl)); rec.source = text(inner.subarray(4 + nl, inner.length - 2));
      } else if (m[1] === 1) {
        if (!this.o.takeV1) { rec.why = 'layout'; return; }
        if (be(m, 2) !== m.length - 6) { rec.why = 'length'; return; }
        const nl = m[7], want = m[8] | (m[9] << 8), z = m.slice();
        z[8] = 0; z[9] = 0;
        if (crc(z, 0, z.length - 6) !== want) { rec.why = 'checksum'; return; }
        if (m[6] !== 0x06) { rec.why = 'shape'; return; }
        rec.name = text(m.subarray(10, 10 + nl)); rec.source = text(m.subarray(10 + nl));
      } else { rec.why = 'version'; return; }
      if (this.o.needRelease && framing === 'old') { this.pending = rec; return; }
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
      if (this.o.silentF8 || (this.o.needNul === true && !nul) || (this.o.needNul === 'never' && nul) || !(name in this.programs) || this.o.readVers.indexOf(m[1]) < 0) return;
      const src = bytes(this.o.crlf ? this.programs[name].replace(/\n/g, '\r\n') + '\r\n' : this.programs[name]), nm = bytes(name);
      if (m[1] === 3) {
        const inner = join([[0x06, nm.length, 0, 0], nm, src, [0, 0]]);
        const all = join([[0xF7, 0x03, (inner.length >>> 24) & 255, (inner.length >>> 16) & 255, (inner.length >>> 8) & 255, inner.length & 255], inner]);
        const c = crc(all, 0, all.length);
        inner[2] = c & 255; inner[3] = c >> 8;
        const stream = await through(inner, new CompressionStream('deflate')), n4 = stream.length + 4;
        return this.reply(join([[0xF7, 0x03, (n4 >>> 24) & 255, (n4 >>> 16) & 255, (n4 >>> 8) & 255, n4 & 255],
                                [inner.length & 255, (inner.length >> 8) & 255, (inner.length >> 16) & 255, (inner.length >>> 24) & 255], stream]), framing);
      }
      const out = head(0xF7, 0x01, join([[0x06, nm.length, 0, 0], nm, src]));
      const c = crc(out, 0, out.length - 6);
      out[8] = c & 255; out[9] = c >> 8;
      return this.reply(out, framing);
    }
  };

  // A port for Link, straight onto the mock (the Node tests).
  MockPrime.prototype.port = function () {
    const self = this, q = [];
    let waiter = null;
    this.onreport = function (r) { if (waiter) { const w = waiter; waiter = null; w(r); } else q.push(r); };
    return {
      reportSize: this.size,
      send: function (frame) { const r = new Uint8Array(self.size); r.set(frame); return self.receive(r).then(function () {}); },
      read: function (ms) {
        if (q.length) return Promise.resolve(q.shift());
        return new Promise(function (res) { const t = setTimeout(function () { waiter = null; res(null); }, ms); waiter = function (r) { clearTimeout(t); res(r); }; });
      },
      poll: function () { return q.length ? q.shift() : null; },
      drain: function () { const n = q.length; q.length = 0; return n; }
    };
  };

  // A fake navigator.hid, for a page.  -> the mock, kept at window.__prime for the test to look at.
  MockPrime.install = function (opts) {
    const mock = new MockPrime(opts), listeners = [];
    const bits = mock.size * 8;
    const device = {
      vendorId: 0x03F0, productId: mock.o.product, productName: 'HP Prime Calculator', opened: false,
      collections: [{ usagePage: 0xFF81, usage: 0x82,
        inputReports: [{ reportId: 0, items: [{ reportSize: 8, reportCount: bits / 8 }] }],
        outputReports: [{ reportId: 0, items: [{ reportSize: 8, reportCount: bits / 8 }] }], featureReports: [] }],
      open: async function () {
        if (mock.o.busy) throw new DOMException('Failed to open the device.', 'NotAllowedError');
        device.opened = true;
      },
      close: async function () { device.opened = false; },
      sendReport: async function (id, data) {
        if (!device.opened) throw new DOMException('The device must be opened first.', 'InvalidStateError');
        if (mock.unplugged) throw new DOMException('Failed to write the report.', 'NotAllowedError');
        const b = data instanceof Uint8Array ? data : new Uint8Array(data.buffer || data);
        mock.lastLength = b.length;
        await mock.receive(b);
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
    // The cable pulled out: writes fail from here, and the browser tells the page.
    mock.unplug = function () {
      mock.unplugged = true; mock.dead = true; device.opened = false;
      gone.slice().forEach(function (fn) { fn({ device: device }); });
    };
    Object.defineProperty(navigator, 'hid', { value: hid, configurable: true });
    window.__prime = mock;
    return mock;
  };

  return MockPrime;
})();

if (typeof module !== 'undefined') module.exports = MockPrime;
