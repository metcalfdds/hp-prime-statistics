// dl_core_v2.js -- the Data Loader's arithmetic: read pasted data, and write the HP Prime's matrix file (.hpmat).
// Roger Metcalf & Claude.  No DOM here: the page and the node tests share this file.
//
// v2 (17 Nov 2026, from the review "they must be bullet proof and as simple as possible").  The file it writes for
// well-formed data is v1's, byte for byte (tests/test_core_v2.js: the kit's cases and the Rossi file).  What changed
// is how a student's paste is READ, so that nothing is turned into a wrong number or a wrong column without a word:
//   - NA, N/A, #N/A, NaN, NULL, ".", "-" and "?" are blanks in EVERY column (v1 made NA a label of a text column);
//   - "$45,000" and "45%" are numbers (the sign is dropped and the page says so); v1 coded them 1, 2, 3 as text;
//   - a column whose numbers are written with a decimal comma ("3,14") is read as numbers;
//   - one column of "45,000"-style numbers, or of labels with spaces in them, stays ONE column;
//   - labels that differ only in capitals or spacing ("Male", "male ") are one label;
//   - in a text column every cell is a label, a number-like one too ("1", "2", "control");
//   - a cell of a number column that is not a number ("1O") is listed for the page to show, not dropped in silence;
//   - the first row can be declared names or data by the student (opts.header), as can the separator (opts.delim).
// v1: 31 Oct 2026.
//
// THE FILE (hp-prime-kit, docs/topics/formats.md, "formats.hpmat"; checked on the Virtual Calculator 31 Oct 2026):
//   bytes 0-1   01 00
//   bytes 2-3   14 80      type: real matrix (the low byte 14 says real; the high byte varies, 80 is accepted)
//   bytes 4-7   rank 2, little-endian
//   bytes 8-11  rows      bytes 12-15  columns
//   then every cell, row by row, 8 bytes each: the Prime's own number, read as a little-endian 64-bit word:
//     bits 0-11  the decimal exponent, 12-bit two's complement
//     bits 12-59 twelve BCD digits, the first digit at the top (bits 56-59)
//     bits 60-63 the sign: 0 positive, 9 negative          zero is all zeros
//
// NUMBERS are read from their TEXT, digit by digit, never through a binary double, and rounded to the Prime's
// 12 significant digits half up (away from zero), as the Prime rounds.  So "0.1" is exactly 0.1 on the calculator.
//
// BLANKS: a cell with no number becomes 9.99999999999E499, the Prime's largest real (MAXREAL), which no data set can
// hold; DataLoad leaves such cells out, so every list gets only its own values.

'use strict';

const DLCore = (function () {
  const NUM_RE = /^([+-]?)(\d*)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/;
  const THOUSANDS_RE = /^[+-]?\d{1,3}(,\d{3})+(\.\d*)?$/;
  const BLANK_WORD = { sign: 0, digits: '999999999999', exp: 499 };   // MAXREAL, the blank marker

  // A cell's text -> {sign, digits (12), exp} or null when it is not a number.
  // exp is the power of ten of the first digit: 52 is 5.2 x 10^1, digits "520000000000", exp 1.
  function parseNumber(text) {
    let t = String(text).trim();
    if (t === '') return null;
    // a minus from a word processor or the Prime itself (U+2212)
    t = t.replace(/−/g, '-');
    if (THOUSANDS_RE.test(t)) t = t.replace(/,/g, '');
    const m = NUM_RE.exec(t);
    if (!m) return null;
    const intPart = m[2] || '';
    const fracPart = m[3] || '';
    if (intPart === '' && fracPart === '') return null;          // "." or "-" alone
    let e10 = m[4] ? parseInt(m[4], 10) : 0;
    let all = intPart + fracPart;                                  // all the digits
    // the power of ten of all's first digit, before leading zeros are dropped
    let exp = intPart.length - 1 + e10;
    let k = 0;
    while (k < all.length && all[k] === '0') { k++; exp--; }
    all = all.slice(k);
    if (all === '') return { sign: 0, digits: '000000000000', exp: 0, zero: true };
    // round to 12 significant digits, half up
    let digits = all.slice(0, 12);
    if (all.length > 12 && all.charCodeAt(12) >= 53) {           // 13th digit 5-9
      let carry = 1;
      const d = digits.split('').map(Number);
      for (let i = 11; i >= 0 && carry; i--) {
        d[i] += carry;
        if (d[i] === 10) { d[i] = 0; carry = 1; } else { carry = 0; }
      }
      digits = d.join('');
      if (carry) { digits = '1' + digits.slice(0, 11); exp++; }   // 999... rounded up
    }
    digits = digits.padEnd(12, '0');
    return { sign: m[1] === '-' ? 9 : 0, digits: digits, exp: exp, zero: false };
  }

  // The Prime's range: 1E-499 to 9.99999999999E499 (HP Prime User Guide, MINREAL and MAXREAL).
  function inRange(n) {
    return n.zero || (n.exp >= -499 && n.exp <= 499);
  }

  // {sign, digits, exp} -> 8 bytes (Uint8Array), little-endian.
  function encodeParsed(n) {
    const out = new Uint8Array(8);
    if (n.zero) return out;
    let w = BigInt(n.sign) << 60n;
    for (let i = 0; i < 12; i++) w |= BigInt(n.digits.charCodeAt(i) - 48) << BigInt(56 - 4 * i);
    w |= BigInt(n.exp & 0xFFF);
    for (let i = 0; i < 8; i++) { out[i] = Number(w & 0xFFn); w >>= 8n; }
    return out;
  }

  // 8 bytes -> the number as text (for checks): "-7.6E1" style.
  function decode(bytes) {
    let w = 0n;
    for (let i = 7; i >= 0; i--) w = (w << 8n) | BigInt(bytes[i]);
    if (w === 0n) return '0';
    const sign = Number(w >> 60n) === 9 ? '-' : '';
    let digits = '';
    for (let i = 0; i < 12; i++) digits += String(Number((w >> BigInt(56 - 4 * i)) & 0xFn));
    let exp = Number(w & 0xFFFn);
    if (exp >= 2048) exp -= 4096;
    digits = digits.replace(/0+$/, '');
    return sign + digits[0] + (digits.length > 1 ? '.' + digits.slice(1) : '') + 'E' + exp;
  }

  // ---- v2: what a student's cell may look like ----
  const BLANK_WORDS = new Set(['', 'na', 'n/a', '#n/a', 'nan', 'null', '.', '-', '?']);
  function isBlankWord(text) { return BLANK_WORDS.has(String(text).trim().toLowerCase()); }
  function normLabel(text) { return String(text).trim().replace(/\s+/g, ' ').toLowerCase(); }
  const LOOSE_THOUSANDS_RE = /^[+-]?[$£€]?\d{1,3}(,\d{3})+(\.\d*)?%?$/;
  const DECIMAL_COMMA_RE = /^[+-]?[$£€]?\d+,(\d{1,2}|\d{4,})%?$/;          // 3,14  2,5  0,1234: not a thousands comma
  const EURO_THOUSANDS_RE = /^[+-]?[$£€]?\d{1,3}(\.\d{3})+,\d+%?$/;       // 1.234,56

  // A cell's text with the things a spreadsheet adds taken off: a currency sign, a percent sign, and (when the column
  // is written that way) the decimal comma turned into a point.  Returns {text, money, percent}.
  function clean(text, decimalComma) {
    let t = String(text).trim().replace(/−/g, '-');
    let money = false, percent = false;
    const m = /^([+-]?)\s*[$£€]\s*([+-]?)(.*)$/.exec(t);
    if (m && !(m[1] && m[2])) { t = (m[1] || m[2]) + m[3]; money = true; }
    if (/\d\s*%$/.test(t)) { t = t.replace(/\s*%$/, ''); percent = true; }
    if (decimalComma) {
      if (/^[+-]?\d{1,3}(\.\d{3})+,\d+$/.test(t)) t = t.replace(/\./g, '').replace(',', '.');
      else if (/^[+-]?\d*,\d+$/.test(t)) t = t.replace(',', '.');
    }
    return { text: t, money: money, percent: percent };
  }
  function readNumber(text, decimalComma) {       // a parsed number in the Prime's range, or null
    const p = parseNumber(clean(text, decimalComma).text);
    return (p !== null && inRange(p)) ? p : null;
  }

  // Split pasted text into rows of cells.  Tabs (a paste from Excel or SPSS) win, then semicolons, then commas, then
  // runs of spaces; quotes around a CSV field are honoured.  v2: a paste with no tab and no semicolon is ONE column
  // when its commas are all thousands commas ("45,000"), or when splitting at spaces gives no column of numbers
  // ("financial aid" / "no aid").  forced: '\t', ';', ',', ' ' or 'one' (the student's choice), else the rule decides.
  function splitRows(text, forced) {
    const lines = String(text).replace(/\r\n?/g, '\n').split('\n').filter(l => l.trim() !== '');
    if (lines.length === 0) return { rows: [], delim: '', why: '' };
    let delim, why = '';
    if (forced) delim = forced;
    else if (lines.some(l => l.includes('\t'))) delim = '\t';
    else if (lines.some(l => l.includes(';'))) delim = ';';
    else if (lines.some(l => l.includes(','))) {
      const thousands = l => LOOSE_THOUSANDS_RE.test(l.trim());
      if (lines.some(thousands) && lines.every(l => thousands(l) || !l.includes(','))) { delim = 'one'; why = 'thousands'; }
      else delim = ',';
    } else {
      const toks = lines.map(l => l.trim().split(/\s+/));
      const n = toks[0].length;
      const body = toks.length > 1 ? toks.slice(1) : toks;
      let numeric = false;
      if (n >= 2 && toks.every(t => t.length === n))
        for (let j = 0; j < n && !numeric; j++)
          numeric = body.every(t => isBlankWord(t[j]) || readNumber(t[j], false) !== null) && body.some(t => readNumber(t[j], false) !== null);
      if (numeric) delim = ' ';
      else { delim = 'one'; if (toks.some(t => t.length > 1)) why = 'spaces'; }
    }
    const rows = lines.map(l => delim === 'one' ? [l.trim()] : delim === ' ' ? l.trim().split(/\s+/) : splitQuoted(l, delim));
    return { rows: rows, delim: delim, why: why };
  }
  function splitQuoted(line, delim) {
    const out = [];
    let cur = '', q = false;
    for (let i = 0; i < line.length; i++) {
      const c = line[i];
      if (q) {
        if (c === '"') { if (line[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c;
      } else if (c === '"') q = true;
      else if (c === delim) { out.push(cur); cur = ''; }
      else cur += c;
    }
    out.push(cur);
    return out.map(s => s.trim());
  }

  // Rows -> columns.  opts.header: true or false is the student's word; undefined lets the rule decide: the first
  // row is names when none of its cells is a number and one of its columns holds numbers below it, or (a table of labels
  // only) when none of its cells comes back in its own column while labels below do repeat.  opts.delim: see splitRows.
  function readTable(text, opts) {
    opts = opts || {};
    const sp = splitRows(text, opts.delim);
    const rows = sp.rows;
    if (rows.length === 0) return { names: [], cols: [], header: false, headerAuto: false, delim: sp.delim, why: sp.why };
    const width = Math.max(...rows.map(r => r.length));
    let auto = false;
    if (rows.length >= 2) {
      const first = rows[0];
      const named = first.some(c => String(c).trim() !== '');
      const noNumbers = first.every(c => String(c).trim() === '' || (readNumber(c, true) === null && !isBlankWord(c)));
      let numberBelow = false;                 // some named column holds numbers below its name (at least half of its cells)
      for (let j = 0; j < width && !numberBelow; j++) {
        if (String(first[j] === undefined ? '' : first[j]).trim() === '') continue;
        const below = rows.slice(1).map(r => (r[j] === undefined ? '' : r[j])).filter(c => !isBlankWord(c));
        const nums = below.filter(c => readNumber(c, true) !== null).length;
        numberBelow = nums >= 1 && nums >= below.length - nums;
      }
      auto = named && noNumbers && numberBelow;
      if (!auto && named && noNumbers && rows.length >= 3) {
        let comesBack = false, repeats = false;
        for (let j = 0; j < width; j++) {
          const below = rows.slice(1).map(r => normLabel(r[j] === undefined ? '' : r[j])).filter(x => x !== '');
          if (String(first[j] || '').trim() !== '' && below.includes(normLabel(first[j]))) comesBack = true;
          if (new Set(below).size < below.length) repeats = true;
        }
        auto = !comesBack && repeats;
      }
    }
    const header = (opts.header === true || opts.header === false) ? (opts.header && rows.length >= 1) : auto;
    const body = header ? rows.slice(1) : rows;
    const names = [];
    for (let j = 0; j < width; j++) {
      const nm = header ? String(rows[0][j] === undefined ? '' : rows[0][j]).trim() : '';
      names.push(nm || ('column ' + (j + 1)));
    }
    const cols = [];
    for (let j = 0; j < width; j++) cols.push(body.map(r => (r[j] === undefined ? '' : String(r[j]).trim())));
    return { names: names, cols: cols, header: header, headerAuto: auto, delim: sp.delim, why: sp.why };
  }

  // A column's kind: "numbers" (its other cells become blanks, and are listed in oddCells) or "text" (every cell is
  // a label; labels are coded 1, 2, ... in sorted order, capitals and spacing aside).  A column is text when more of
  // its cells are not numbers than are.  Blank words (NA, ".", ...) are blanks in both kinds.
  function describe(col) {
    const cells = col.filter(c => !isBlankWord(c));
    const empty = col.length - cells.length;
    // the decimal comma: some cell is written 3,14 and none is written with a decimal point
    const decimalComma = cells.some(c => DECIMAL_COMMA_RE.test(c.replace(/−/g, '-')) || EURO_THOUSANDS_RE.test(c.replace(/−/g, '-'))) &&
                         !cells.some(c => /\d\.\d/.test(c) && !EURO_THOUSANDS_RE.test(c.replace(/−/g, '-')));
    let nums = 0, money = 0, percent = 0, lo = Infinity, hi = -Infinity;
    const odd = [];
    for (const c of cells) {
      const cl = clean(c, decimalComma);
      const p = parseNumber(cl.text);
      if (p !== null && inRange(p)) {
        nums++;
        if (cl.money) money++;
        if (cl.percent) percent++;
        const v = Number(cl.text.replace(/,/g, ''));
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      } else odd.push(c);
    }
    const kind = odd.length > nums ? 'text' : 'numbers';
    if (kind === 'numbers')
      return { kind: kind, values: nums, blanks: col.length - nums, empty: empty, odd: odd.length, oddCells: odd,
               lo: lo, hi: hi, codes: null, codeOf: null, merged: [], decimalComma: decimalComma && nums > 0,
               money: money, percent: percent };
    // text: every cell that is not a blank word is a label
    const spell = new Map();                                     // key -> the spellings seen, first one first
    for (const c of cells) {
      const k = normLabel(c);
      if (!spell.has(k)) spell.set(k, []);
      if (!spell.get(k).includes(c)) spell.get(k).push(c);
    }
    const keys = Array.from(spell.keys()).sort((a, b) => a.localeCompare(b));
    const codes = new Map(), codeOf = new Map(), merged = [];
    keys.forEach((k, i) => {
      codes.set(spell.get(k)[0], i + 1); codeOf.set(k, i + 1);
      if (spell.get(k).length > 1) merged.push(spell.get(k));
    });
    return { kind: kind, values: cells.length, blanks: col.length - cells.length, empty: empty, odd: 0, oddCells: [],
             lo: lo, hi: hi, codes: codes, codeOf: codeOf, merged: merged, decimalComma: false, money: 0, percent: 0 };
  }

  // The cell as the Prime will hold it: a parsed number, or the blank marker.
  function cellWord(text, info) {
    if (isBlankWord(text)) return BLANK_WORD;
    if (info.kind === 'text') {
      const code = info.codeOf.get(normLabel(text));
      return code === undefined ? BLANK_WORD : parseNumber(String(code));
    }
    const p = readNumber(text, info.decimalComma);
    return p === null ? BLANK_WORD : p;
  }

  // The .hpmat file for the chosen columns: header, then every cell row by row.
  function buildHpmat(cols, infos) {
    const nc = cols.length;
    const nr = Math.max(...cols.map(c => c.length));
    const buf = new Uint8Array(16 + 8 * nr * nc);
    const dv = new DataView(buf.buffer);
    buf[0] = 0x01; buf[1] = 0x00; buf[2] = 0x14; buf[3] = 0x80;
    dv.setUint32(4, 2, true);
    dv.setUint32(8, nr, true);
    dv.setUint32(12, nc, true);
    let off = 16;
    for (let i = 0; i < nr; i++) {
      for (let j = 0; j < nc; j++) {
        const t = i < cols[j].length ? cols[j][i] : '';
        buf.set(encodeParsed(cellWord(t, infos[j])), off);
        off += 8;
      }
    }
    return buf;
  }

  // ---- a small zip (stored, no compression), for viewers that may only save .zip files ----
  const CRC_TABLE = (function () {
    const t = new Uint32Array(256);
    for (let n = 0; n < 256; n++) {
      let c = n;
      for (let k = 0; k < 8; k++) c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
      t[n] = c >>> 0;
    }
    return t;
  })();

  function crc32(bytes) {
    let c = 0xFFFFFFFF;
    for (let i = 0; i < bytes.length; i++) c = CRC_TABLE[(c ^ bytes[i]) & 0xFF] ^ (c >>> 8);
    return (c ^ 0xFFFFFFFF) >>> 0;
  }

  // files: [{name, data (Uint8Array)}] -> Uint8Array of a zip.  Dates are 31 Oct 2026, 12:00.
  function zip(files) {
    const enc = new TextEncoder();
    const parts = [], central = [];
    let offset = 0;
    const dosTime = (12 << 11), dosDate = ((2026 - 1980) << 9) | (10 << 5) | 31;
    for (const f of files) {
      const name = enc.encode(f.name);
      const crc = crc32(f.data);
      const lh = new Uint8Array(30 + name.length);
      const lv = new DataView(lh.buffer);
      lv.setUint32(0, 0x04034b50, true); lv.setUint16(4, 20, true); lv.setUint16(6, 0, true);
      lv.setUint16(8, 0, true); lv.setUint16(10, dosTime, true); lv.setUint16(12, dosDate, true);
      lv.setUint32(14, crc, true); lv.setUint32(18, f.data.length, true); lv.setUint32(22, f.data.length, true);
      lv.setUint16(26, name.length, true); lv.setUint16(28, 0, true);
      lh.set(name, 30);
      parts.push(lh, f.data);
      const ch = new Uint8Array(46 + name.length);
      const cv = new DataView(ch.buffer);
      cv.setUint32(0, 0x02014b50, true); cv.setUint16(4, 20, true); cv.setUint16(6, 20, true);
      cv.setUint16(8, 0, true); cv.setUint16(10, 0, true); cv.setUint16(12, dosTime, true);
      cv.setUint16(14, dosDate, true); cv.setUint32(16, crc, true); cv.setUint32(20, f.data.length, true);
      cv.setUint32(24, f.data.length, true); cv.setUint16(28, name.length, true);
      cv.setUint32(42, offset, true);
      ch.set(name, 46);
      central.push(ch);
      offset += lh.length + f.data.length;
    }
    const cdSize = central.reduce((s, c) => s + c.length, 0);
    const end = new Uint8Array(22);
    const ev = new DataView(end.buffer);
    ev.setUint32(0, 0x06054b50, true); ev.setUint16(8, files.length, true); ev.setUint16(10, files.length, true);
    ev.setUint32(12, cdSize, true); ev.setUint32(16, offset, true);
    const all = parts.concat(central, [end]);
    const total = all.reduce((s, p) => s + p.length, 0);
    const out = new Uint8Array(total);
    let o = 0;
    for (const p of all) { out.set(p, o); o += p.length; }
    return out;
  }

  return { parseNumber, inRange, encodeParsed, decode, splitRows, readTable, describe, cellWord, buildHpmat,
           crc32, zip, BLANK_WORD, isBlankWord, normLabel, clean, readNumber };
})();

if (typeof module !== 'undefined') module.exports = DLCore;
