// usb_ladder_v2.js -- the second test of a real HP Prime on its cable, with prime_usb_v2.js.  Roger Metcalf & Claude,
// 17 Nov 2026.
//
// WHAT THE FIRST TEST FOUND (logs/, the author's G2 and G1, both on firmware build 15751)
//   * Both answer with version 01.  A program sent NOT compressed ("F7 01") in the old framing is kept and comes back
//     the same: 80 reports of the G2, 10 of the G1.  At 274 reports (G2) and 263 (G1) it is not kept.
//   * A program sent COMPRESSED ("F7 03") is not kept, in either framing.
//   * The newer framing is taken, and a message in it is acknowledged.
// WHAT THIS ONE ASKS, in the order it asks
//   C  Where does the old framing stop?  A program of exactly 254 reports, then one of exactly 255, the most there
//      are before their numbers start again.  (11 of the book's 31 programs take more than 255 reports of a G2 as
//      they are; all 31 take more than 255 of a G1.)
//   A  Does the calculator keep a compressed program once it has been told that this page speaks version 03?
//      PrimeDev holds the bytes of such a message ("FD"); nobody has written down what a calculator does with them.
//   E  Does the newer framing carry a program that is not compressed, past 255 reports?
//   D  The same, compressed: what HP's own Connectivity Kit appears to do.
// Each route begins with a program of a few lines, and a route that works climbs toward the size of the book's largest
// program.  Every report the calculator sends is in the log, the long runs counted and the rest shown, because what it
// does at each of these points is the thing to find out.
//
// WHAT GOES ON THE CALCULATOR.  Four programs at most, ZZUSBC, ZZUSBA, ZZUSBE and ZZUSBD, each replaced at every step
// and deleted at the end.  Each is comment lines and one function that returns a number, the function LAST, so that a
// program cut short on the way does not compile.  Nothing else on the calculator is written, read or deleted.
//
// No DOM here.  run() takes a Link and an object of callbacks; the page supplies one that draws, the Node test one that
// records.

'use strict';

const PrimeLadder = (function () {

  const VERSION = 'v2';
  // The characters of the test program at each size.  3 is DataLoad's size and 5 is EpiStats's, the smallest and the
  // largest program of the book at the time of writing (tests/test_usb_ladder_v2.js counts them again).
  const SIZES = [
    { step: 1, chars: 300, like: 'a few lines' },
    { step: 2, chars: 8269, like: 'the largest program hp-prime-kit sent' },
    { step: 3, chars: 40856, like: 'DataLoad, our smallest program' },
    { step: 4, chars: 140000, like: 'a program of middle size' },
    { step: 5, chars: 289813, like: 'EpiStats, our largest program' }
  ];
  const LIMITS = [254, 255];                      // route C's second and third steps, in reports
  const ROUTES = [
    { key: 'C', name: 'ZZUSBC', framing: 'old', layout: 'v1', title: 'Old framing, not compressed', from: 'hp-prime-web; kept on 17 Nov up to 80 reports of the G2 and 10 of the G1' },
    { key: 'A', name: 'ZZUSBA', framing: 'old', layout: 'v3', title: 'Old framing, compressed', from: 'hp-prime-kit; not kept on 17 Nov' },
    { key: 'E', name: 'ZZUSBE', framing: 'new', layout: 'v1', title: 'Newer framing, not compressed', from: 'PrimeDev\'s framing; not tried before' },
    { key: 'D', name: 'ZZUSBD', framing: 'new', layout: 'v3', title: 'Newer framing, compressed', from: 'PrimeDev; what the Connectivity Kit appears to do; not kept on 17 Nov' }
  ];
  function cellsOf(key) {
    if (key === 'C') return [{ col: 1, cap: '300 characters' }].concat(LIMITS.map(function (n, i) { return { col: i + 2, cap: 'exactly ' + n + ' reports' }; }));
    return SIZES.map(function (s) { return { col: s.step, cap: num(s.chars) + ' characters' }; });
  }

  const WORDS = ('LOCAL BEGIN END IF THEN ELSE FOR FROM TO DO WHILE REPEAT UNTIL RETURN EXPORT CASE DEFAULT BREAK CONTINUE STEP DOWNTO ' +
    'TEXTOUT_P RECT_P LINE_P FILLPOLY_P ARC_P PIXON_P BLIT_P DIMGROB_P GETKEY WAIT MOUSE CHOOSE INPUT MSGBOX PRINT STRING SIZE MAX MIN ABS SQRT EXP LN ' +
    'ROUND FLOOR CEILING IP FP SIGN RANDOM RANDINT SUM MAKELIST CONCAT SORT REVERSE POS LEFT RIGHT MID UPPER LOWER EXPR IFTE NOT AND OR XOR ' +
    'mean sd alpha beta power sample count total index value result table list matrix row col width height left top color label title help page ' +
    'x y z n k m p q r s t i j a b c d e f g h u v w lo hi mid sum sq df se ci lower upper tail area curve shade axis tick grid plot draw key touch').split(' ');

  function rng(seed) {                               // xorshift32: the same text on every computer
    let x = (seed >>> 0) || 1;
    return function () { x ^= x << 13; x >>>= 0; x ^= x >>> 17; x ^= x << 5; x >>>= 0; return x; };
  }
  // A test program of exactly `chars` characters, which returns `tag`.  Its comment lines are made of the words a PPL
  // program is made of, so that it compresses about as our programs do (a little worse: the test counts both).
  function makeProgram(name, tag, chars) {
    const head = '// ' + name + ': a test of the USB cable, number ' + tag + '. Safe to delete.\n';
    const tail = '\nEXPORT ' + name + '()\nBEGIN\n RETURN ' + tag + ';\nEND;';
    const room = chars - head.length - tail.length;
    if (room < 0) throw new Error('a test program needs at least ' + (head.length + tail.length) + ' characters');
    const r = rng(1000 * tag + name.charCodeAt(name.length - 1)), lines = [];
    let n = 0;
    while (n < room + 1) {                                       // n counts a newline after every line, the last too
      const k = 3 + r() % 9, parts = [];
      for (let i = 0; i < k; i++) {
        const t = r() % 10;
        if (t < 6) parts.push(WORDS[r() % WORDS.length]);
        else if (t < 8) parts.push(String(r() % 1000));
        else parts.push(WORDS[r() % WORDS.length] + '(' + WORDS[r() % WORDS.length] + ',' + (r() % 100) + ')');
      }
      const line = '// ' + ' '.repeat(r() % 4) + parts.join(r() % 3 ? ' ' : ':=') + ';';
      lines.push(line); n += line.length + 1;
    }
    let body = lines.join('\n').slice(0, room);
    // The cut can leave a last line of one character, "/", which is not a comment, or of none: either joins the line
    // before it as blanks, and the length stays what was asked for.
    const li = body.lastIndexOf('\n');
    if (li >= 0 && body.length - li - 1 <= 1) body = body.slice(0, li) + ' '.repeat(body.length - li);
    return head + body + tail;
  }
  // The characters of a program whose "F7 01" message fills exactly `reports` reports of the old framing: the message
  // is ten bytes, the name and the source, two bytes a character.
  function charsFor(reports, cap, name) { return Math.floor((reports * cap - 10 - 2 * name.length) / 2); }
  function firstDifference(a, b) {
    const n = Math.min(a.length, b.length);
    for (let i = 0; i < n; i++) if (a.charCodeAt(i) !== b.charCodeAt(i)) return i;
    return a.length === b.length ? -1 : n;
  }
  function num(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function said(e) { return String(e && e.message ? e.message : e).replace(/[.\s]+$/, ''); }      // an error's own words, less its full stop
  function secs(ms) { return (ms / 1000).toFixed(ms < 9950 ? 1 : 0) + ' s'; }
  function reportsText(n) { return num(n) + ' report' + (n === 1 ? '' : 's'); }
  function Halt() { this.name = 'Halt'; }           // the test ends here
  function Leave() { this.name = 'Leave'; }         // the part in hand ends here

  // The reports that pass, for the log: a line for each one that starts a message, acknowledges or controls, the first
  // three of any run of one kind and then their count; the reports that carry on a message are only counted, with
  // their numbers.  `budget` lines between two lines of the test's own, and then a count of what was left out.
  function Tracer(emit, P, budget) {
    let run = null, serial = 0, left = budget || 60, dropped = 0;
    const out = function (s) { if (left > 0) { left--; emit(s); } else dropped++; };
    const over = function (r) { return r.t1 - r.t0 >= 100 ? ', over ' + secs(r.t1 - r.t0) : ''; };
    const flush = function () {
      if (!run) return;
      const r = run;
      run = null;
      if (r.kind === 'more') out(r.dir + ' ' + num(r.count) + ' more report' + (r.count === 1 ? '' : 's') + ' of it, numbered ' + P.runs(r.seqs) + over(r));
      else if (r.count > r.shown) out(r.dir + ' ... and ' + num(r.count - r.shown) + ' more of that kind' + over(r) + '; the last: ' + r.last);
    };
    this.flush = function () {
      flush();
      if (dropped) { emit('(' + num(dropped) + ' more lines of this kind were left out)'); dropped = 0; }
      left = budget || 60;
    };
    this.report = function (dir, rep, v2) {
      const d = P.describe(rep, v2), key = dir + d.kind + (d.kind === 'start' ? ++serial : (d.key || '')), now = Date.now();
      if (run && run.key === key) {
        run.count++; run.t1 = now; run.last = d.text;
        if (d.kind === 'more') { if (run.seqs.length < 20000) run.seqs.push(d.seq); }
        else if (run.count <= 3) { run.shown = run.count; out(dir + ' ' + d.text); }
        return;
      }
      flush();
      run = { key: key, dir: dir, kind: d.kind, count: 1, shown: d.kind === 'more' ? 0 : 1, t0: now, t1: now, last: d.text, seqs: d.kind === 'more' ? [d.seq] : null };
      if (d.kind !== 'more') out(dir + ' ' + d.text);
    };
  }

  // ui: {log(text), cell(routeKey, col, state, text), ask({name}) -> Promise<bool>, pause() -> Promise, stop() -> bool}
  // opts.core: PrimeUSB.  opts.t: the waits in ms, for a test that cannot wait as long as a calculator may need.
  // -> {info, routes: {C: {steps, best, ...}}, told, opened, oldAfterNew, alive, gone, stopped, left, top, text}
  async function run(link, ui, opts) {
    opts = opts || {};
    const P = opts.core;
    const t = Object.assign({ first: 3000, then: 2500, probe: 1200, listen: 900, gap: 1500, tries: 4, settle: 400, quiet: 250, recover: 24000 }, opts.t || {});
    const T0 = Date.now();
    const res = { info: null, routes: {}, told: [], opened: null, newInfo: null, oldAfterNew: null, alive: true, gone: false, stopped: false, newDead: false, left: [], top: null, text: '' };
    ROUTES.forEach(function (r) { res.routes[r.key] = { key: r.key, title: r.title, name: r.name, steps: [], best: null, tried: false, reader: null, release: false, lastSrc: null, seen: null }; });
    const stamp = function () { return ('      ' + ((Date.now() - T0) / 1000).toFixed(1)).slice(-7); };
    const tracer = new Tracer(function (s) { ui.log(stamp() + '        . ' + s); }, P, opts.budget);
    const log = function (s) { tracer.flush(); ui.log(s === '' ? '' : stamp() + '  ' + s); };
    const route = function (k) { return ROUTES.filter(function (r) { return r.key === k; })[0]; };
    let fmt = 1, cleaning = false;
    link.trace = function (dir, r, v2) { tracer.report(dir, r, v2); };
    link.note = function (s) { log('  ' + s); };
    const check = function () {
      if (cleaning || !ui.stop || !ui.stop()) return;
      if (!res.stopped) { res.stopped = true; log('STOPPED by the Stop button.'); }
      throw new Halt();
    };

    const askInfo = async function () {
      try { return await link.info(t.first); }
      catch (e) { if (P.isGone(e)) throw e; log('    Asked who it is: ' + said(e) + '.'); return null; }
    };
    // The ways of asking for a program back, the one in the version the calculator speaks first.  [log]: the name
    // must end in a NUL; the two without one are asked only when neither of the others is answered.
    const readers = function () {
      const a = fmt === 3 ? 3 : 1, b = a === 3 ? 1 : 3;
      return [{ ver: a, nul: true }, { ver: b, nul: true }, { ver: a, nul: false }, { ver: b, nul: false }];
    };
    const titleOf = function (rd) { return 'F8 0' + rd.ver + (rd.nul ? ', the name ending in a NUL' : ', no NUL'); };
    const describe = function (b) {
      return reportsText(b.reports) + (b.compressed ? ', compressed' : ', not compressed') + ', version 0' + b.ver + (b.crcOk ? '' : ', ITS CHECKSUM NOT AS EXPECTED') +
             (/,/.test(b.numbered || '') ? ', numbered ' + b.numbered : '') +
             (b.stalls && b.stalls.length ? '; the calculator stood until it was acknowledged after ' + b.stalls.slice(0, 6).map(num).join(', ') + (b.stalls.length > 6 ? ', ...' : '') + ' reports' : '') +
             (b.again ? '; ' + num(b.again) + ' reports came a second time' : '') + (b.gaps ? '; ' + num(b.gaps) + ' came out of turn' : '');
    };
    const slowText = function (out) {
      if (!out.slow || !out.slow.length) return '';
      return ' THE CABLE STOOD: ' + out.slow.map(function (x) { return secs(x.ms) + ' at report ' + num(x.report); }).join(', ') + '.';
    };
    const ackText = function (out) {
      if (!out.acks) return '';
      if (!out.acks.length) return out.implied ? ' No acknowledgement; the calculator began an answer instead.' : ' No acknowledgement.';
      const a = out.acks, one = function (x) { return (x.ok ? '' : '"send again" ') + 'report ' + P.hex2(x.seq) + ' position ' + num(x.pos) + ' (' + num(x.sent) + ' sent, ' + secs(x.ms) + ')'; };
      let s = ' Acknowledged ' + num(a.length) + ' time' + (a.length === 1 ? '' : 's') + ': ' + a.slice(0, 4).map(one).join('; ') + (a.length > 5 ? '; ...' : '') + (a.length > 4 ? '; ' + one(a[a.length - 1]) : '') + '.';
      if (out.waits) s += ' The page stood at its window of ' + link.window + ' reports ' + num(out.waits) + ' time' + (out.waits === 1 ? '' : 's') + ' until an acknowledgement came.';
      if (out.unacked) s += ' ' + num(out.unacked) + ' time' + (out.unacked === 1 ? '' : 's') + ' none came while the page waited at its window (' + secs(link.pace.patience) + ' the first three times, 0.05 s after that), and it went on.';
      return s;
    };

    // Ask for the program back until it is the one sent, or the tries run out.  A calculator may need a moment to
    // store a long program, and until then it answers with the copy before, or not at all.
    const readBack = async function (r, src, how, tries, first, before) {
      const start = Date.now();
      let why = 'no answer';
      for (let k = 1; k <= tries; k++) {
        check();
        let back = null;
        why = 'no answer';
        try { back = await link.readProgram(r.name, { ver: how.ver, nul: how.nul, first: first, then: t.then }); }
        catch (e) { if (P.isGone(e)) throw e; why = said(e); back = null; }
        if (back && back.text === src) return { ok: true, back: back, tries: k, ms: Date.now() - start };
        if (back && P.normalizeSource(back.text) === src) {        // the same program with other line ends, or a newline added
          if (!res.lineEnds) { res.lineEnds = true; log('      (what came back is the same but for its line ends or a last newline: ' + num(back.text.length) + ' characters against ' + num(src.length) + ')'); }
          return { ok: true, back: back, tries: k, ms: Date.now() - start };
        }
        if (back) {
          why = 'what came back differs: ' + num(back.text.length) + ' characters against ' + num(src.length) + ' sent, the first difference at character ' + num(firstDifference(back.text, src) + 1);
          if (before && back.text === before) why += ' (it is the program sent before, whole: the new one was not kept)';
        }
        if (tries > 1) log('      try ' + k + ' of ' + tries + ': ' + why + '.');
        if (k < tries) await link.swallow(t.gap);                 // (listening: a late copy of an earlier answer is passed over here)
      }
      return { ok: false, why: why, tries: tries, ms: Date.now() - start };
    };
    // bare: whether the two requests without a NUL are asked at all (once for each route is enough).
    const find = async function (r, src, bare) {
      let best = null;
      let asked = 0;
      for (const rd of readers()) {
        check();
        if (!rd.nul && (best || !bare)) break;
        if (asked++) await link.swallow(t.quiet);                  // so that a second copy of the last answer is not taken for this one
        const g = await readBack(r, src, rd, 1, t.probe, null);
        log('    Asked for it back with ' + titleOf(rd) + ': ' + (g.ok ? 'the same program came back (' + describe(g.back) + '; it began ' + g.back.head + ').' : g.why + '.'));
        if (g.ok && (!best || (g.back.compressed && !best.back.compressed))) { best = g; best.reader = rd; }
      }
      return best;
    };
    // One program by one route: send, and read back.  mode 'find': try the ways of asking, and keep the one that
    // answers; 'read': ask the way that answered before.  -> the step's record
    const attempt = async function (r, st, mode) {
      check();
      const w = res.routes[r.key], src = makeProgram(r.name, st.tag, st.chars), rec = { col: st.col, tag: st.tag, chars: st.chars, ok: false, src: src, why: 'the test ended before this was done' };
      w.steps.push(rec); w.tried = true;
      ui.cell(r.key, st.col, 'busy', 'sending');
      log('  ' + r.name + ': ' + num(st.chars) + ' characters (' + st.like + ').');
      let out;
      try { out = await link.sendProgram(r.name, src, { layout: r.layout, release: w.release }); }
      catch (e) {
        if (P.isGone(e)) throw e;
        rec.why = 'not sent: ' + said(e);
        log('    NOT SENT: ' + said(e) + '.');
        ui.cell(r.key, st.col, 'bad', 'not sent');
        return rec;
      }
      rec.reports = out.reports; rec.bytes = out.bytes; rec.sendMs = out.ms; rec.acks = out.acks ? out.acks.length : null; rec.waits = out.waits; rec.unacked = out.unacked;
      log('    Sent ' + num(out.bytes) + ' bytes in ' + reportsText(out.reports) + ', ' + (out.ms / 1000).toFixed(2) + ' s on the cable.' + slowText(out) + ackText(out) + (out.said ? ' Then it sent: ' + out.said + '.' : ''));
      if (out.refused) { rec.why = 'the calculator refused it (F9)'; log('    REFUSED (F9).'); ui.cell(r.key, st.col, 'bad', 'refused'); return rec; }
      await link.swallow(t.settle);
      ui.cell(r.key, st.col, 'busy', 'reading back');
      let got = null;
      if (mode === 'find') {
        got = await find(r, src, !w.bared);
        w.bared = true;
        if (!got) { rec.unread = true; rec.why = 'sent, and no request brought it back'; ui.cell(r.key, st.col, 'bad', 'not read back'); return rec; }
        w.reader = got.reader;
      } else {
        got = await readBack(r, src, w.reader, t.tries, t.first, w.lastSrc);
        if (got.ok) log('    Read back the same: ' + describe(got.back) + ', ' + secs(got.ms) + (got.tries > 1 ? ', on try ' + got.tries : '') + '.');
      }
      if (got.ok) {
        rec.ok = true; rec.readMs = got.ms; rec.backReports = got.back.reports; rec.backCompressed = got.back.compressed;
        w.best = { chars: st.chars, reports: out.reports, bytes: out.bytes }; w.lastSrc = src;
        ui.cell(r.key, st.col, 'ok', reportsText(out.reports));
        return rec;
      }
      rec.why = got.why;
      log('    NOT THE SAME: ' + rec.why + '.');
      ui.cell(r.key, st.col, 'bad', /differs/.test(rec.why) ? 'came back changed' : 'did not come back');
      return rec;
    };
    const size1 = function () { return { col: 1, tag: 1, chars: SIZES[0].chars, like: SIZES[0].like }; };
    // The small program of a route.  In the old framing, if nothing brings it back, hp-prime-kit's report "01" is sent
    // and it is asked for once more: its G2 got one after every program, and whether a program needs it "was not separated".
    const small = async function (r) {
      const rec = await attempt(r, size1(), 'find');
      if (rec.ok || !rec.unread || r.framing !== 'old' || r.layout !== 'v3') return rec;
      log('    hp-prime-kit sent a report "01" after each program. One is sent now, and the program asked for again.');
      await link.release();
      await link.swallow(t.settle);
      const g = await find(r, rec.src, false);
      if (g) {
        const w = res.routes[r.key];
        rec.ok = true; rec.unread = false; rec.why = null; w.reader = g.reader; w.release = true;
        w.best = { chars: rec.chars, reports: rec.reports, bytes: rec.bytes }; w.lastSrc = rec.src;
        ui.cell(r.key, 1, 'ok', reportsText(rec.reports) + ', then a report 01');
      }
      return rec;
    };
    // "FD": tell the calculator the newest version of the messages this page speaks, and ask who it is again.
    const tell = async function (kind) {
      check();
      log('  Telling the calculator that this page speaks version 03: "' + P.hex(P.maxVersionMessage(kind)) + '" (PrimeDev\'s bytes' + (kind === 'short' ? ', the short form' : '') + ').');
      let r = null;
      try { r = await link.maxVersion(kind, t.listen); }
      catch (e) { if (P.isGone(e)) throw e; log('    ' + said(e) + '.'); }
      if (r) log(r.reply ? '    It answered: ' + r.reply + '.' : '    It sent no answer of its own within ' + secs(t.listen) + (r.acks && r.acks.length ? ' (it acknowledged the message)' : '') + '.');
      const i = await askInfo();
      if (i) {
        log('    Asked who it is: it answers with version 0' + i.ver + (i.ver !== fmt ? ', CHANGED from 0' + fmt : ', as before') + (link.v2 && !res.newInfo ? ' (the first time it has said who it is in the newer framing)' : '') + '.');
        fmt = i.ver;
        if (link.v2) res.newInfo = i;
      }
      res.told.push({ framing: link.v2 ? 'new' : 'old', kind: kind, reply: r ? r.reply : null, ver: i ? i.ver : null });
      if (!i && (!link.v2 || res.newInfo)) await stillThere();        // it said who it was before this message, and now it does not
    };
    // A compressed program of a few lines, after telling the calculator "FD" in each of the forms given until one
    // is kept (none is told to a calculator that speaks 03 already).
    const compressed = async function (r, kinds) {
      let rec = null;
      for (const kind of (fmt === 3 ? [null] : kinds)) {
        if (kind) await tell(kind);
        rec = await small(r);
        if (rec.ok) break;
      }
      return rec;
    };
    // Up the sizes.  most: in the old framing, the most reports a message has been kept at; a size that needs more is
    // not sent, because the calculator's answer to one too many is to hold the cable ([log]: for 49 s).
    const climb = async function (r, most) {
      for (const sz of SIZES.slice(1)) {
        check();
        if (most) {
          const src = makeProgram(r.name, sz.step, sz.chars), msg = r.layout === 'v1' ? P.programV1(r.name, src) : await P.programV3(r.name, src);
          const n = Math.ceil(msg.length / link.cap);
          if (n > most) {
            res.routes[r.key].steps.push({ col: sz.step, tag: sz.step, chars: sz.chars, ok: false, skipped: true, reports: n });
            log('  ' + r.name + ': ' + num(sz.chars) + ' characters would be ' + reportsText(n) + ' here, more than the ' + most + ' the old framing has kept. Not sent.');
            ui.cell(r.key, sz.step, 'skip', reportsText(n) + ': more than the old framing keeps');
            continue;
          }
        }
        const rec = await attempt(r, { col: sz.step, tag: sz.step, chars: sz.chars, like: sz.like }, 'read');
        if (!rec.ok) return false;
      }
      return true;
    };
    // After a failure: does the calculator still answer?  It may need a while ([log]: the G2's first request after the
    // message it did not keep had no answer).
    const recover = async function () {
      const t0 = Date.now();
      for (let k = 0; ; k++) {
        check();
        let i = null;
        try { i = await link.info(k ? Math.min(2000, t.first) : t.first); } catch (e) { if (P.isGone(e)) throw e; }
        if (i) { if (k) log('  The calculator answers again, ' + secs(Date.now() - t0) + ' later.'); return true; }
        if (Date.now() - t0 >= t.recover) return false;
        await P.sleep(Math.min(1000, t.gap));
      }
    };
    // ... and if it does not: in the old framing the test ends; in the newer one that part of it ends, and the old
    // framing is asked afterwards.
    const stillThere = async function () {
      if (await recover()) return;
      if (link.v2) { res.newDead = true; log('  THE CALCULATOR HAS STOPPED ANSWERING in the newer framing. The rest of this part is left out.'); throw new Leave(); }
      res.alive = false;
      log('THE CALCULATOR HAS STOPPED ANSWERING. Nothing more will be sent.');
      throw new Halt();
    };
    const answers = async function () {
      try { await link.info(t.first); return true; } catch (e) { if (P.isGone(e)) throw e; return false; }
    };
    // Take test programs off again ("EB"), and ask for each to see that it is gone.
    const takeOff = async function (keys) {
      const mine = ROUTES.filter(function (r) { return keys.indexOf(r.key) >= 0 && res.routes[r.key].tried && !res.routes[r.key].off; });
      if (!mine.length) return;
      log('');
      log('TAKING ' + mine.map(function (r) { return r.name; }).join(', ') + ' OFF THE CALCULATOR AGAIN ("EB", in the ' + (link.v2 ? 'newer' : 'old') + ' framing).');
      // A delete has no answer, and the proof of it is that a request for the program then has none either: which
      // proves nothing on a calculator that has stopped answering.  So it is asked who it is before, and after.
      const can = !link.v2 || !!res.newInfo, bySilence = [];
      if (can && !(await answers())) {
        log('  The calculator does not answer, so its programs cannot be taken off, or checked.');
        mine.forEach(function (r) { if (res.left.indexOf(r.name) < 0) res.left.push(r.name); });
        return;
      }
      for (const r of mine) {
        const w = res.routes[r.key], vers = fmt === 3 ? [3, 1] : [1, 3];
        try {
          if (!w.reader) {                                          // never read back: both versions of the delete, and the page cannot check
            for (const v of vers) await link.deleteProgram(r.name, v);
            log('  ' + r.name + ': a delete was sent. It was never read back, so the page cannot tell whether it was there' + (w.seen ? ' (the person saw it in the list): please look' : '') + '.');
            if (w.seen && res.left.indexOf(r.name) < 0) res.left.push(r.name);
            if (!link.v2) w.off = true;                             // (sent in the newer framing, it is sent once more in the old one, where a delete is known to work)
            continue;
          }
          let still = null;
          for (const v of vers) {
            await link.deleteProgram(r.name, v);
            try { still = await link.readProgram(r.name, { ver: w.reader.ver, nul: w.reader.nul, first: Math.min(t.probe, 1200), then: t.then }); }
            catch (e) { if (P.isGone(e)) throw e; still = null; }
            if (!still) break;
          }
          const at = res.left.indexOf(r.name);
          if (still) { if (at < 0) res.left.push(r.name); log('  ' + r.name + ' is STILL on the calculator after the delete.'); }
          else { w.off = true; bySilence.push(r); if (at >= 0) res.left.splice(at, 1); log('  ' + r.name + ': deleted (a request for it now has no answer).'); }
        } catch (e) {
          if (P.isGone(e)) throw e;
          if (res.left.indexOf(r.name) < 0) res.left.push(r.name);
          log('  Could not delete ' + r.name + ': ' + said(e) + '.');
        }
      }
      if (bySilence.length && can && !(await answers())) {
        log('  The calculator has stopped answering, so the silence after ' + (bySilence.length === 1 ? 'that delete' : 'those deletes') + ' proves nothing.');
        bySilence.forEach(function (r) { res.routes[r.key].off = false; if (res.left.indexOf(r.name) < 0) res.left.push(r.name); });
      }
    };

    const body = async function () {
      // ---- who is there
      log('Asking the calculator who it is (old framing, "00 FA") ...');
      res.info = await askInfo();
      if (!res.info) { res.alive = false; return; }
      fmt = res.info.ver;
      log('It answered: firmware build ' + res.info.build + ', "' + res.info.version + '"; ' + res.info.bytes + ' bytes of information, version 0' + fmt + '. Its reports carry ' + num(link.cap) + ' bytes each.');

      // ---- C: the old framing, not compressed, and where it stops
      const C = route('C'), wC = res.routes.C;
      log('');
      log('C. THE OLD FRAMING, NOT COMPRESSED ("F7 01"). A few lines first; then a program of exactly ' + LIMITS[0] + ' reports and one of exactly ' + LIMITS[1] + ', the most there are before their numbers start again.');
      const c1 = await small(C);
      if (c1.ok) {
        for (let k = 0; k < LIMITS.length; k++) {
          const rec = await attempt(C, { col: k + 2, tag: LIMITS[k], chars: charsFor(LIMITS[k], link.cap, C.name), like: 'exactly ' + LIMITS[k] + ' reports' }, 'read');
          if (!rec.ok) break;
        }
      }
      if (wC.steps.some(function (s) { return !s.ok; })) await stillThere();
      // What the old framing has kept, in reports: this run's best, or the first test's ([log]).
      const most = Math.max(wC.best ? wC.best.reports : 0, link.cap >= 1023 ? 80 : 10);

      // ---- A: the old framing, compressed
      const A = route('A');
      log('');
      log('A. THE OLD FRAMING, COMPRESSED ("F7 03"). On 17 Nov neither calculator kept this, and both answered with version 01 where hp-prime-kit\'s G2, which did keep it, answered 03.');
      res.most = most;
      const a1 = await compressed(A, ['long']);
      if (a1.ok) { if (!(await climb(A, most))) await stillThere(); }

      // ---- between the two framings: a key on the calculator, and a look at it if a program went unread
      check();
      log('');
      if (a1.unread && ui.ask) {
        const yes = await ui.ask({ name: A.name });
        check();
        res.routes.A.seen = yes === true;
        log('The person at the calculator was asked whether ' + A.name + ' is in its list of programs: ' + (yes === true ? 'YES, it is there.' : yes === false ? 'no, it is not there.' : 'no answer.'));
      } else if (ui.pause) {
        await ui.pause();
        check();
        log('The person at the calculator pressed a key and clicked Continue.');
      }
      check();
      await takeOff(['C', 'A']);

      try { await newer(); }
      catch (e) { if (!(e instanceof Leave)) throw e; }
    };
    const newer = async function () {
      // ---- E and D: the newer framing
      const E = route('E'), D = route('D');
      log('');
      log('E and D. THE NEWER FRAMING ("FF EC 00 00 00 00 00 00"; PrimeDev; by hp-prime-emulator\'s reading, what the Connectivity Kit itself asks for).');
      res.opened = await link.openV2(t.listen);
      log('  Asked for it. ' + (res.opened.replies.length ? 'The calculator answered: ' + res.opened.replies.join(' | ') + '.' : 'The calculator sent no answer of its own within ' + secs(t.listen) + '.') +
          (res.opened.others ? ' (' + res.opened.others + ' other report' + (res.opened.others === 1 ? '' : 's') + ' came: the lines above.)' : ''));
      res.newInfo = await askInfo();
      if (res.newInfo) { log('  Asked who it is, in the newer framing: it answers with version 0' + res.newInfo.ver + '.'); fmt = res.newInfo.ver; }
      else log('  It did not say who it is in the newer framing. The test goes on: on 17 Nov it acknowledged a message there.');
      log('  E, not compressed:');
      const e1 = await small(E);
      if (!res.newInfo && !e1.ok && /^not sent/.test(e1.why || '')) {
        res.newDead = true;
        log('  The calculator acknowledges nothing in the newer framing, so the rest of this part is left out.');
        throw new Leave();
      }
      log('  D, compressed:');
      const d1 = await compressed(D, ['long', 'short']);
      // If the few lines of E were not kept before "FD" was told, they are tried once more now: the first message of
      // a session that PrimeDev holds is the "FD", and a calculator may want it before anything else.
      let e2 = e1;
      if (!e1.ok && res.told.some(function (x) { return x.framing === 'new'; })) { log('  E once more, now that "FD" has been told:'); e2 = await small(E); }
      let whole = true;
      if (d1.ok) whole = await climb(D, 0);
      else if (e2.ok) { log('  The compressed program was not kept, so the sizes are tried not compressed.'); whole = await climb(E, 0); }
      if ((!whole || (!e2.ok && !d1.ok)) && res.newInfo && !(await recover())) { res.newDead = true; log('  The calculator does not answer in the newer framing any more.'); }
      // A look at the calculator for whatever was sent and not read back: whether it is in the list says whether the
      // newer framing delivered it at all.
      for (const r of [E, D]) {
        const w = res.routes[r.key], last = w.steps[w.steps.length - 1];
        if (!last || !last.unread || !ui.ask) continue;
        check();
        const yes = await ui.ask({ name: r.name });
        check();
        w.seen = yes === true;
        log('The person at the calculator was asked whether ' + r.name + ' is in its list of programs: ' + (yes === true ? 'YES, it is there.' : yes === false ? 'no, it is not there.' : 'no answer.'));
      }
    };
    // What is left to do whether or not the body ran to its end: the test programs off, and the old framing asked
    // once more, which says whether a page can go back to it.
    const ending = async function () {
      cleaning = true;
      if (!res.info || !res.alive) return;
      if (!link.v2) { await takeOff(['C', 'A']); return; }
      if (!res.newDead) await takeOff(['E', 'D']);
      log('');
      link.v2 = false;
      let i = null;
      try { i = await link.info(t.first); } catch (e) { if (P.isGone(e)) throw e; }
      res.oldAfterNew = !!i;
      log('AFTER THE NEWER FRAMING, the old one was asked "00 FA" again: ' + (i ? 'answered, with version 0' + i.ver + '.' : 'NO ANSWER.'));
      if (!i) { ['E', 'D'].forEach(function (k) { const w = res.routes[k]; if (w.tried && !w.off && res.left.indexOf(w.name) < 0) res.left.push(w.name); }); return; }
      fmt = i.ver;
      // A once more.  If the newer framing raised the version, this is hp-prime-kit's own case: its G2 had been with
      // the Connectivity Kit, answered 03, and kept a compressed program in the OLD framing.  If nothing has raised
      // it, the short "FD" is tried here, last of all, where nothing that follows depends on what it does.
      const A = route('A'), wA = res.routes.A;
      if (!res.stopped && wA.tried && !wA.best) {
        log('');
        log('A AGAIN, the old framing, compressed' + (fmt === 3 ? ', now that the calculator speaks version 03.' : ': the calculator still speaks version 01, so the short "FD" is tried.'));
        wA.off = false; wA.again = true;
        const raised = fmt === 3;
        try {
          const a2 = await compressed(A, ['short']);
          if (a2.ok) { wA.late = raised ? 'after the newer framing had raised its version to 03' : 'after the short "FD" in the old framing'; await climb(A, res.most); }
        } catch (e) { if (P.isGone(e)) throw e; if (!(e instanceof Halt) && !(e instanceof Leave)) throw e; }
      }
      await takeOff(['C', 'A', 'E', 'D']);
    };

    for (const part of [body, ending]) {
      try { await part(); }
      catch (e) {
        if (P.isGone(e)) { res.gone = true; res.alive = false; log('THE CALCULATOR WENT OFF THE CABLE: ' + said(e) + '. Nothing more can be sent.'); break; }
        if (!(e instanceof Halt)) throw e;
      }
    }
    if (res.gone || !res.alive) ROUTES.forEach(function (r) { const w = res.routes[r.key]; if (w.tried && !w.off && res.left.indexOf(r.name) < 0) res.left.push(r.name); });
    tracer.flush();
    res.text = summary(res, link);
    ROUTES.forEach(function (r) { res.routes[r.key].steps.forEach(function (s) { delete s.src; }); res.routes[r.key].lastSrc = null; });
    log('');
    log('RESULT');
    res.text.split('\n').forEach(function (l) { log('  ' + l); });
    return res;
  }

  // What the test found, in sentences.
  function summary(res, link) {
    const L = [], R = res.routes, big = SIZES[SIZES.length - 1].chars;
    if (!res.info) return res.gone ? 'The calculator went off the cable before it said who it is. Nothing was sent to it.'
                                   : 'The calculator did not answer, so nothing was sent to it. Is it switched on and at its Home screen? Is HP\'s Connectivity Kit closed?';
    let top = null;
    ROUTES.forEach(function (r) { const w = R[r.key]; if (w.best && (!top || w.best.chars > top.chars)) top = { key: r.key, title: r.title, chars: w.best.chars, reports: w.best.reports }; });
    res.top = top;
    // every route that carried the largest size, the fewest reports first
    const tops = ROUTES.filter(function (r) { return R[r.key].best && R[r.key].best.chars >= big; }).map(function (r) { return { title: r.title, reports: R[r.key].best.reports }; })
                       .sort(function (a, b) { return a.reports - b.reports; });
    if (tops.length) L.push('A PROGRAM THE SIZE OF THE BOOK\'S LARGEST (' + num(big) + ' characters) WENT TO THIS CALCULATOR AND CAME BACK THE SAME: ' +
                            tops.map(function (x) { return x.title.toLowerCase() + ', ' + reportsText(x.reports); }).join('; and ') + '.');
    else if (top && top.chars < big) L.push('The largest program that went to this calculator and came back the same: ' + num(top.chars) + ' characters (' + top.title.toLowerCase() + ', ' + reportsText(top.reports) + '). The book\'s largest is ' + num(big) + '.');
    else if (!top) L.push('No program came back from this calculator.');
    L.push('');
    ROUTES.forEach(function (r) {
      const w = R[r.key];
      if (!w.tried) { L.push(r.key + '. ' + w.title + ': not tried.'); return; }
      const ok = w.steps.filter(function (s) { return s.ok; }), bad = w.steps.filter(function (s) { return !s.ok && !s.skipped; }), skipped = w.steps.filter(function (s) { return s.skipped; });
      let s = r.key + '. ' + w.title + ': ';
      if (ok.length) {
        const last = ok[ok.length - 1];
        s += 'came back the same at ' + ok.map(function (x) { return num(x.chars); }).join(', ') + ' characters (the last in ' + reportsText(last.reports) + ')';
        if (w.release) s += ', with a report "01" after each';
        if (w.late) s += ', but only at the second try, ' + w.late;
      } else s += 'NOT kept';
      const b = bad.length ? bad[bad.length - 1] : null;
      if (b && (!ok.length || b.chars > ok[ok.length - 1].chars)) s += (ok.length ? '; NOT at ' + num(b.chars) + ' characters' + (b.reports ? ' (' + reportsText(b.reports) + ')' : '') : '') + ': ' + b.why;
      if (skipped.length) s += '; ' + skipped.map(function (x) { return num(x.chars); }).join(', ') + ' characters not sent (' + skipped.map(function (x) { return num(x.reports); }).join(', ') + ' reports)';
      if (w.seen === true) s += '. The person saw ' + w.name + ' in the calculator\'s list, so it WAS kept, and no request reads it back';
      if (w.seen === false && !ok.length) s += '. The person did not find ' + w.name + ' in the calculator\'s list';
      L.push(s + '.');
    });
    L.push('');
    L.push('It answered with version 0' + res.info.ver + ' at the start.' + res.told.map(function (x) {
      return ' Told "FD" (' + (x.kind === 'short' ? 'short' : 'long') + ' form, ' + x.framing + ' framing): ' + (x.reply ? 'it answered ' + x.reply : 'no answer of its own') + (x.ver ? ', and then spoke version 0' + x.ver : '') + '.';
    }).join(''));
    if (res.opened) L.push('The newer framing: ' + (res.opened.replies.length ? 'on being asked, it answered ' + res.opened.replies.join(' | ') : 'on being asked, it sent nothing of its own') + '.' +
                           (res.oldAfterNew === null ? '' : ' Afterwards the old framing was ' + (res.oldAfterNew ? 'still answered.' : 'NOT answered.')));
    if (res.gone) L.push('THE CALCULATOR WENT OFF THE CABLE before the test ended. What is above this line in the log stands.');
    else if (!res.alive) L.push('THE CALCULATOR STOPPED ANSWERING. If it does not come back by itself, press its On key; failing that, press a straightened paperclip into the reset hole on its back.');
    if (res.stopped) L.push('The test was stopped before its end.');
    if (res.left.length) L.push('STILL ON THE CALCULATOR, or not known to be off it: ' + res.left.join(', ') + '. Each is comment lines and one small function; to delete one, press Shift, then Program, tap its name, tap More, then Delete.');
    else L.push('The test\'s programs were taken off the calculator again.');
    return L.join('\n');
  }

  return { VERSION: VERSION, SIZES: SIZES, LIMITS: LIMITS, ROUTES: ROUTES, cellsOf: cellsOf, makeProgram: makeProgram, charsFor: charsFor,
           firstDifference: firstDifference, num: num, Tracer: Tracer, run: run, summary: summary };
})();

if (typeof module !== 'undefined') module.exports = PrimeLadder;
