// usb_ladder_v1.js -- the first test of prime_usb_v1.js on a real HP Prime: test programs of growing size, sent four
// ways and read back.  Roger Metcalf & Claude, 17 Nov 2026.
//
// WHY A LADDER.  Each public description of the cable stops at a small program: hp-prime-kit sent 16,558 bytes in six
// reports, hp-prime-web "over 16 KB".  The book's programs are 41,000 to 290,000 characters: 17 to 101 reports
// compressed, 80 to 567 as they are.  So the test climbs: 300 characters, then hp-prime-kit's own largest, then the
// size of our smallest program (DataLoad), then a size between, then the size of our largest (EpiStats).  A way of
// sending stops at its first failure and is not pushed further.
//
// WHAT GOES ON THE CALCULATOR.  Four programs at most, named ZZUSBA, ZZUSBB, ZZUSBC and ZZUSBD, each replaced at
// every step and deleted at the end.  Each is comment lines and one function that returns its step number, the
// function LAST, so that a program cut short on the way does not compile and cannot answer.  Nothing else on the
// calculator is written, read or deleted.
//
// No DOM here.  run() takes a Link and an object of callbacks; the page supplies one that draws, the Node test one that
// records.

'use strict';

const PrimeLadder = (function () {

  const VERSION = 'v1';
  // The steps: the characters of the test program.  3 is DataLoad's size and 5 is EpiStats's, the smallest and the
  // largest program of the book at the time of writing (tests/test_usb_ladder_v1.js counts them again).
  const STEPS = [
    { step: 1, chars: 300, like: 'a few lines' },
    { step: 2, chars: 8269, like: 'the largest program hp-prime-kit sent' },
    { step: 3, chars: 40856, like: 'DataLoad, our smallest program' },
    { step: 4, chars: 140000, like: 'a program of middle size' },
    { step: 5, chars: 289813, like: 'EpiStats, our largest program' }
  ];
  // The ways of sending.  A is hp-prime-kit's, measured on firmware 2.4.15515 from Windows; C is hp-prime-web's;
  // D is the framing HP's own Connectivity Kit uses.  D comes last because nothing says how to leave it.
  const WAYS = [
    { key: 'A', name: 'ZZUSBA', framing: 'old', how: { layout: 'v3', release: true }, title: 'compressed, with the report 01 after it', from: 'hp-prime-kit' },
    { key: 'B', name: 'ZZUSBB', framing: 'old', how: { layout: 'v3', release: false }, title: 'compressed, nothing after it', from: 'hp-prime-kit, less its last report' },
    { key: 'C', name: 'ZZUSBC', framing: 'old', how: { layout: 'v1', release: false }, title: 'not compressed', from: 'hp-prime-web' },
    { key: 'D', name: 'ZZUSBD', framing: 'new', how: { layout: 'v3' }, title: 'compressed, in the newer framing', from: 'PrimeDev; the Connectivity Kit\'s framing' }
  ];
  // The ways of asking for a program back.  1 is hp-prime-web's, which its G2 answered; 4 is hp-prime-kit's, which
  // its G2 answered once.
  const READS = [
    { key: 1, ver: 1, nul: true, title: 'F8 01, the name ending in a NUL' },
    { key: 2, ver: 3, nul: true, title: 'F8 03, the name ending in a NUL' },
    { key: 3, ver: 1, nul: false, title: 'F8 01, no NUL' },
    { key: 4, ver: 3, nul: false, title: 'F8 03, no NUL' }
  ];
  const WORDS = ('LOCAL BEGIN END IF THEN ELSE FOR FROM TO DO WHILE REPEAT UNTIL RETURN EXPORT CASE DEFAULT BREAK CONTINUE STEP DOWNTO ' +
    'TEXTOUT_P RECT_P LINE_P FILLPOLY_P ARC_P PIXON_P BLIT_P DIMGROB_P GETKEY WAIT MOUSE CHOOSE INPUT MSGBOX PRINT STRING SIZE MAX MIN ABS SQRT EXP LN ' +
    'ROUND FLOOR CEILING IP FP SIGN RANDOM RANDINT SUM MAKELIST CONCAT SORT REVERSE POS LEFT RIGHT MID UPPER LOWER EXPR IFTE NOT AND OR XOR ' +
    'mean sd alpha beta power sample count total index value result table list matrix row col width height left top color label title help page ' +
    'x y z n k m p q r s t i j a b c d e f g h u v w lo hi mid sum sq df se ci lower upper tail area curve shade axis tick grid plot draw key touch').split(' ');

  function rng(seed) {                               // xorshift32: the same text on every computer
    let x = (seed >>> 0) || 1;
    return function () { x ^= x << 13; x >>>= 0; x ^= x >>> 17; x ^= x << 5; x >>>= 0; return x; };
  }
  // A test program of exactly `chars` characters.  Its comment lines are made of the words a PPL program is made of,
  // so that it compresses about as our programs do (a little worse: 128 reports at EpiStats's size against 101).
  function makeProgram(name, step, chars) {
    const head = '// ' + name + ': a test of the USB cable, step ' + step + ' of ' + STEPS.length + '. Safe to delete.\n';
    const tail = '\nEXPORT ' + name + '()\nBEGIN\n RETURN ' + step + ';\nEND;';
    const room = chars - head.length - tail.length;
    if (room < 0) throw new Error('a test program needs at least ' + (head.length + tail.length) + ' characters');
    const r = rng(1000 * step + name.charCodeAt(name.length - 1)), lines = [];
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
  function firstDifference(a, b) {
    const n = Math.min(a.length, b.length);
    for (let i = 0; i < n; i++) if (a.charCodeAt(i) !== b.charCodeAt(i)) return i;
    return a.length === b.length ? -1 : n;
  }
  function num(n) { return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ','); }
  function said(e) { return String(e && e.message ? e.message : e).replace(/[.\s]+$/, ''); }      // an error's own words, less its full stop
  function secs(ms) { return (ms / 1000).toFixed(ms < 9950 ? 1 : 0) + ' s'; }

  // ui: {log(text), cell(wayKey, step, state, text), ask(way, step) -> Promise<bool>, stop() -> bool}
  // opts.core: PrimeUSB.  opts.t: {probe, first, then, gap, tries, settle} in ms, for a test that cannot wait as long
  // as a calculator may need.  opts.ways: the keys to try (all four when left out).
  // -> {info, reader, readerNew, blind, ways: {A: {steps: [...], best}}, alive, left, text}
  async function run(link, ui, opts) {
    opts = opts || {};
    const P = opts.core, t = Object.assign({ probe: 2500, first: 4000, then: 3000, gap: 2000, tries: 6, settle: 400 }, opts.t || {});
    const T0 = Date.now(), res = { info: null, reader: null, readerNew: null, blind: false, ways: {}, alive: true, left: [], stopped: false };
    const log = function (s) { ui.log(s === '' ? '' : ('      ' + ((Date.now() - T0) / 1000).toFixed(1)).slice(-7) + '  ' + s); };
    const stopped = function () { if (!res.stopped && ui.stop && ui.stop()) { res.stopped = true; log('STOPPED by the Stop button.'); } return res.stopped; };
    const wanted = WAYS.filter(function (y) { return !opts.ways || opts.ways.indexOf(y.key) >= 0; });
    wanted.forEach(function (y) { res.ways[y.key] = { steps: [], best: 0, title: y.title, tried: false }; });
    link.note = function (s) { log(s); };

    // ---- 1. who is there
    log('Asking the calculator who it is ...');
    try { res.info = await link.info(3000); }
    catch (e) {
      res.alive = false;
      log('NO ANSWER: ' + said(e) + '.');
      res.text = 'The calculator did not answer, so nothing was sent to it. Is it switched on and at its Home screen? Is HP\'s Connectivity Kit closed?';
      log(res.text);
      return res;
    }
    log('It answered: firmware build ' + res.info.build + ', "' + res.info.version + '"; ' + res.info.bytes + ' bytes of information, reply version 0' + res.info.ver + '.');

    // Ask for the program back until it is the one sent, or the tries run out.  A calculator may need a moment to
    // store a long program, and until then it answers with the copy before, or not at all.
    const readBack = async function (way, src, how, tries, first, before) {
      const start = Date.now();
      let why = 'no answer';
      for (let k = 1; k <= tries; k++) {
        if (stopped()) return { ok: false, why: 'stopped', tries: k - 1, ms: Date.now() - start };
        let back = null;
        why = 'no answer';
        try { back = await link.readProgram(way.name, { ver: how.ver, nul: how.nul, first: first, then: t.then }); }
        catch (e) { why = said(e); back = null; }
        if (back && back.text === src) return { ok: true, back: back, tries: k, ms: Date.now() - start };
        if (back && P.normalizeSource(back.text) === src) {        // the same program with other line ends, or a newline added
          if (!res.lineEnds) { res.lineEnds = true; log('      (what came back is the same but for its line ends or a last newline: ' + num(back.text.length) + ' characters against ' + num(src.length) + ')'); }
          return { ok: true, back: back, tries: k, ms: Date.now() - start };
        }
        if (back) {
          why = 'what came back differs: ' + num(back.text.length) + ' characters against ' + num(src.length) + ' sent, the first difference at character ' + num(firstDifference(back.text, src) + 1);
          if (before && back.text === before) why += ' (it is the program of the step before, whole: the new one was not kept)';
        }
        if (tries > 1) log('      try ' + k + ' of ' + tries + ': ' + why + '.');
        if (k < tries) await P.sleep(t.gap);
      }
      return { ok: false, why: why, tries: tries, ms: Date.now() - start };
    };
    const describe = function (b) {
      return b.reports + ' report' + (b.reports === 1 ? '' : 's') + (b.compressed ? ', compressed' : ', not compressed') + ', reply version 0' + b.ver +
             (b.crcOk ? '' : ', ITS CHECKSUM NOT AS EXPECTED') + (b.reports > 250 ? ', numbered ' + b.firsts : '');
    };
    // One step of one way: send, and check.  how to check: a reader (a way of asking that this calculator answers),
    // 'find' (try the four ways of asking), or 'eye' (ask the person).  -> the step's record
    const attempt = async function (way, st, check) {
      const w = res.ways[way.key], src = makeProgram(way.name, st.step, st.chars), rec = { step: st.step, chars: st.chars, ok: false };
      w.steps.push(rec); w.tried = true;
      ui.cell(way.key, st.step, 'busy', 'sending');
      log('  Way ' + way.key + ', step ' + st.step + ': ' + num(st.chars) + ' characters (' + st.like + ').');
      let out;
      try { out = await link.sendProgram(way.name, src, way.how); }
      catch (e) { rec.why = 'not sent: ' + said(e); log('    NOT SENT: ' + said(e) + '.'); ui.cell(way.key, st.step, 'bad', 'not sent'); return rec; }
      rec.reports = out.reports; rec.bytes = out.bytes; rec.sendMs = out.ms;
      log('    Sent ' + num(out.bytes) + ' bytes in ' + out.reports + ' report' + (out.reports === 1 ? '' : 's') + ', ' + (out.ms / 1000).toFixed(2) + ' s on the cable.' +
          (out.acks && out.acks.length ? ' The calculator said: ' + out.acks.join('; ') + '.' : '') + (out.said ? ' Then it sent: ' + out.said + '.' : ''));
      if (out.refused) { rec.why = 'the calculator refused it (F9)'; log('    REFUSED (F9).'); ui.cell(way.key, st.step, 'bad', 'refused'); return rec; }
      await P.sleep(t.settle);
      if (check === 'eye') {
        ui.cell(way.key, st.step, 'busy', 'look at the calculator');
        const yes = ui.ask ? await ui.ask(way, st) : false;
        rec.ok = !!yes; rec.byEye = true;
        log('    The person at the calculator says ' + way.name + (yes ? ' ANSWERS ' + st.step + '.' : ' does NOT answer ' + st.step + '.'));
        ui.cell(way.key, st.step, yes ? 'ok' : 'bad', yes ? 'seen on the calculator' : 'not on the calculator');
        if (yes) w.best = st.chars; else rec.why = 'not seen on the calculator';
        return rec;
      }
      ui.cell(way.key, st.step, 'busy', 'reading back');
      let got = null, reader = check === 'find' ? null : check;
      if (!reader) {
        // The two requests whose name ends in a NUL are both asked.  One that brings the program back compressed is
        // the one to keep: a long program then comes back in far fewer reports, short of where their numbers wrap
        // (and inside what the newer framing carries in one message).  The two without a NUL are asked only when
        // neither of those was answered: hp-prime-kit's G2 stopped answering after such a request, and why is not
        // known, so one is not sent to a calculator that has just answered.
        for (const rd of READS) {
          if (stopped() || (reader && !rd.nul)) break;
          const r = await readBack(way, src, rd, 1, t.probe);
          log('    Asked for it back with ' + rd.title + ': ' + (r.ok ? 'the same program came back (' + describe(r.back) + '; it began ' + r.back.head + ').' : r.why + '.'));
          if (r.ok && (!reader || (r.back.compressed && !got.back.compressed))) { reader = rd; got = r; rec.reader = rd; }
          if (reader && !rd.nul) break;
        }
        if (!reader) { rec.unread = true; rec.why = 'sent, and none of the four requests brought it back'; ui.cell(way.key, st.step, 'bad', 'not read back'); return rec; }
      } else {
        const prev = STEPS.filter(function (x) { return x.step === st.step - 1; })[0];
        got = await readBack(way, src, reader, st.step === 1 ? 2 : t.tries, t.first, prev ? makeProgram(way.name, prev.step, prev.chars) : null);
        if (got.ok) log('    Read back the same: ' + describe(got.back) + ', ' + secs(got.ms) + (got.tries > 1 ? ', on try ' + got.tries : '') + '.');
      }
      if (got && got.ok) {
        rec.ok = true; rec.readMs = got.ms; rec.tries = got.tries; w.best = st.chars;
        ui.cell(way.key, st.step, 'ok', out.reports + (out.reports === 1 ? ' report' : ' reports'));
        return rec;
      }
      rec.why = got ? got.why : 'no answer';
      log('    NOT THE SAME: ' + rec.why + '.');
      ui.cell(way.key, st.step, 'bad', /differs/.test(rec.why) ? 'came back changed' : 'did not come back');
      return rec;
    };
    // After a step fails: is the calculator still there?  If it is not, nothing more is sent.
    const stillThere = async function () {
      try { await link.info(3000); return true; }
      catch (e) {
        if (link.v2) {
          // No answer in the newer framing is not no calculator: hp-prime-kit found the old framing still answered.
          link.v2 = false;
          try { await link.info(3000); log('  No answer in the newer framing; the calculator still answers in the old one, so the old one is used from here.'); res.v2gone = true; return true; }
          catch (e2) { /* neither framing */ }
        }
        res.alive = false; log('THE CALCULATOR HAS STOPPED ANSWERING (' + said(e) + '). Nothing more will be sent.'); return false;
      }
    };
    const climb = async function (way, check, steps) {
      for (const st of steps) {
        if (stopped() || !res.alive) return;
        const rec = await attempt(way, st, check);
        if (!rec.ok) { await stillThere(); return; }
      }
    };
    const upper = STEPS.filter(function (x) { return x.step > 1 && (!opts.maxStep || x.step <= opts.maxStep); });
    const byEye = upper.filter(function (x) { return x.step === 3 || x.step === 5; });       // fewer questions for a person

    // Take test programs off again (EB 01), and ask for each to see that it is gone.
    const takeOff = async function (ways) {
      const mine = ways.filter(function (y) { return res.ways[y.key].tried; });
      if (!mine.length) return;
      if (!res.alive) { mine.forEach(function (y) { res.left.push(y.name); }); return; }
      log('');
      log('TAKING ' + mine.map(function (y) { return y.name; }).join(', ') + ' OFF AGAIN (EB 01).');
      for (const way of mine) {
        const rd = way.framing === 'new' && !res.v2gone ? res.readerNew : res.reader;
        try {
          await link.deleteProgram(way.name, 1);
          if (!rd) { res.left.push(way.name); log('  A delete was sent for ' + way.name + '; the page cannot tell whether it worked.'); continue; }
          let still = null;
          try { still = await link.readProgram(way.name, { ver: rd.ver, nul: rd.nul, first: Math.min(t.probe, 1500), then: t.then }); } catch (e) { still = null; }
          if (still) { res.left.push(way.name); log('  ' + way.name + ' is STILL on the calculator after the delete.'); }
          else log('  ' + way.name + ': deleted (a request for it now has no answer).');
        } catch (e) { res.left.push(way.name); log('  Could not delete ' + way.name + ': ' + said(e) + '.'); }
      }
    };

    // ---- 2. the old framing: the smallest program each way, which also finds a way of reading back
    const old = wanted.filter(function (y) { return y.framing === 'old'; }), first = STEPS[0];
    if (old.length) { log(''); log('THE OLD FRAMING. First the smallest program, each way: ' + old.map(function (y) { return y.key + ' = ' + y.title; }).join('; ') + '.'); }
    for (const way of old) {
      if (stopped() || !res.alive) break;
      const rec = await attempt(way, first, res.reader || 'find');
      if (rec.reader) { res.reader = rec.reader; log('  This calculator answers ' + rec.reader.title + ': that is how the rest is read back.'); }
      if (!rec.ok && !rec.unread) await stillThere();
    }
    if (old.length && res.alive && !stopped()) {
      if (res.reader) {
        // A way that went out before the reader was found is asked for again now.
        for (const way of old) {
          const rec = res.ways[way.key].steps[0];
          if (!rec || !rec.unread || stopped()) continue;
          const r = await readBack(way, makeProgram(way.name, first.step, first.chars), res.reader, 1, t.probe);
          log('  Way ' + way.key + ', step 1, asked for again with ' + res.reader.title + ': ' + (r.ok ? 'the same program came back.' : r.why + '.'));
          if (r.ok) { rec.ok = true; rec.unread = false; delete rec.why; res.ways[way.key].best = first.chars; ui.cell(way.key, 1, 'ok', rec.reports + (rec.reports === 1 ? ' report' : ' reports')); }
          else { rec.unread = false; rec.why = r.why; ui.cell(way.key, 1, 'bad', 'did not come back'); }
        }
        log('');
        log('UP THE LADDER, each way that passed step 1.');
        for (const way of old) if (res.ways[way.key].best > 0) await climb(way, res.reader, upper);
      } else {
        // Nothing was read back, whichever way it was sent: this calculator does not answer the request (as
        // hp-prime-kit found of its G2).  The person holding it is asked instead, and asked as little as possible.
        res.blind = true;
        log('');
        log('NO PROGRAM COULD BE READ BACK, whichever way it was sent. The page now asks the person at the calculator.');
        let chosen = null;
        for (const way of old) {
          if (stopped()) break;
          const rec = res.ways[way.key].steps[0];
          if (!rec || !rec.unread) continue;
          ui.cell(way.key, 1, 'busy', 'look at the calculator');
          const yes = ui.ask ? await ui.ask(way, first) : false;
          rec.byEye = true; rec.unread = false; rec.ok = !!yes;
          log('  The person at the calculator says ' + way.name + (yes ? ' ANSWERS 1.' : ' does NOT answer 1.'));
          ui.cell(way.key, 1, yes ? 'ok' : 'bad', yes ? 'seen on the calculator' : 'not on the calculator');
          if (yes) { res.ways[way.key].best = first.chars; delete rec.why; if (!chosen) chosen = way; } else rec.why = 'not seen on the calculator';
        }
        if (chosen) { log(''); log('UP THE LADDER by eye, way ' + chosen.key + ' only, at the sizes of our smallest and largest programs.'); await climb(chosen, 'eye', byEye); }
      }
    }

    await takeOff(old);              // in the old framing, before the newer one is asked for

    // ---- 3. the newer framing, last: nothing says how to leave it
    const neu = wanted.filter(function (y) { return y.framing === 'new'; });
    for (const way of neu) {
      if (stopped() || !res.alive) break;
      log('');
      log('THE NEWER FRAMING (way ' + way.key + ': ' + way.title + '; ' + way.from + ').');
      try { await link.openV2(); log('  Asked for the newer framing (FF EC).'); }
      catch (e) { log('  Could not ask for it: ' + said(e) + '.'); continue; }
      const rec = await attempt(way, first, 'find');
      if (rec.reader) { res.readerNew = rec.reader; await climb(way, rec.reader, upper); }
      else if (rec.unread && res.alive && !stopped()) {
        ui.cell(way.key, 1, 'busy', 'look at the calculator');
        const yes = ui.ask ? await ui.ask(way, first) : false;
        rec.byEye = true; rec.unread = false; rec.ok = !!yes;
        log('  The person at the calculator says ' + way.name + (yes ? ' ANSWERS 1.' : ' does NOT answer 1.'));
        ui.cell(way.key, 1, yes ? 'ok' : 'bad', yes ? 'seen on the calculator' : 'not on the calculator');
        if (yes) { res.ways[way.key].best = first.chars; delete rec.why; await climb(way, 'eye', byEye); } else rec.why = 'not seen on the calculator';
      } else if (!rec.ok) await stillThere();
    }

    await takeOff(neu);

    // ---- 4. what it comes to
    const lines = [], biggest = upper.length ? upper[upper.length - 1].chars : first.chars, tried = wanted.filter(function (y) { return res.ways[y.key].tried; });
    const good = tried.filter(function (y) { return res.ways[y.key].best >= biggest; });
    const some = tried.filter(function (y) { return res.ways[y.key].best > 0 && res.ways[y.key].best < biggest; });
    const none = tried.filter(function (y) { return res.ways[y.key].best === 0; });
    if (!res.alive) lines.push('The calculator stopped answering during the test. Unplug the cable. If the calculator does not respond to its keys, a paperclip in the reset hole on its back restarts it.');
    if (res.stopped) lines.push('The test was stopped before its end, so what follows is what was done up to then.');
    if (good.length) lines.push('A test program of ' + num(biggest) + ' characters' + (biggest === STEPS[STEPS.length - 1].chars ? ', the size of our largest program,' : '') + ' arrived whole when it was sent ' +
                                good.map(function (y) { return y.title + ' (way ' + y.key + (res.ways[y.key].steps.some(function (r) { return r.byEye; }) ? ', checked by eye' : ', read back the same') + ')'; }).join('; and when sent ') + '.');
    some.forEach(function (y) {
      const w = res.ways[y.key], bad = w.steps[w.steps.length - 1];
      lines.push('Way ' + y.key + ' (' + y.title + ') worked up to ' + num(w.best) + ' characters' + (bad && !bad.ok ? ' and failed at ' + num(bad.chars) + ': ' + bad.why : '') + '.');
    });
    none.forEach(function (y) { const w = res.ways[y.key], bad = w.steps[0]; lines.push('Way ' + y.key + ' (' + y.title + ') did not work for the smallest program' + (bad && bad.why ? ': ' + bad.why : '') + '.'); });
    if (res.blind) lines.push('This calculator answered none of the four requests for a program in the old framing, so the page could not read anything back there by itself.');
    if (res.left.length) lines.push('To delete by hand, if they are there (Shift, then Program; tap the name to highlight it; tap More, then Delete): ' + res.left.join(', ') + '.');
    else if (res.alive && tried.length) lines.push('The test programs were deleted from the calculator again.');
    res.text = lines.join('\n');
    log('');
    log('RESULT');
    lines.forEach(function (l) { log(l); });
    return res;
  }

  return { VERSION: VERSION, STEPS: STEPS, WAYS: WAYS, READS: READS, makeProgram: makeProgram, firstDifference: firstDifference, run: run, num: num };
})();

if (typeof module !== 'undefined') module.exports = PrimeLadder;
