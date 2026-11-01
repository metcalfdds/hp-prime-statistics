// dl_core_v1.js -- the Data Loader's arithmetic: read pasted data, and write the HP Prime's matrix file (.hpmat).
// Roger Metcalf & Claude, 31 Oct 2026.  No DOM here: the page and the node tests share this file.
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

  // Split pasted text into rows of cells.  Tabs (a paste from Excel or SPSS) win, then semicolons, then commas, then
  // runs of spaces.  Quotes around a CSV field are honoured.
  function splitRows(text) {
    const lines = String(text).replace(/\r\n?/g, '\n').split('\n').filter(l => l.trim() !== '');
    if (lines.length === 0) return { rows: [], delim: '' };
    const sample = lines.slice(0, 20).join('\n');
    let delim = ' ';
    if (sample.includes('\t')) delim = '\t';
    else if (sample.includes(';')) delim = ';';
    else if (sample.includes(',')) delim = ',';
    const rows = lines.map(l => (delim === ' ') ? l.trim().split(/\s+/) : splitQuoted(l, delim));
    return { rows: rows, delim: delim };
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

  // Rows -> columns, with a header when the first row is names over numbers.
  function readTable(text) {
    const sp = splitRows(text);
    const rows = sp.rows;
    if (rows.length === 0) return { names: [], cols: [], header: false, delim: sp.delim };
    const width = Math.max(...rows.map(r => r.length));
    let header = false;
    if (rows.length >= 2) {
      const first = rows[0], second = rows[1];
      let named = 0, numberBelow = 0;
      for (let j = 0; j < width; j++) {
        const a = (first[j] || '').trim();
        if (a !== '' && parseNumber(a) === null) named++;
        if (parseNumber(second[j] || '') !== null) numberBelow++;
      }
      header = named > 0 && numberBelow > 0 && first.every(c => parseNumber(c) === null || c.trim() === '');
    }
    const body = header ? rows.slice(1) : rows;
    const names = [];
    for (let j = 0; j < width; j++) {
      const nm = header ? (rows[0][j] || '').trim() : '';
      names.push(nm || ('column ' + (j + 1)));
    }
    const cols = [];
    for (let j = 0; j < width; j++) cols.push(body.map(r => (r[j] === undefined ? '' : String(r[j]).trim())));
    return { names: names, cols: cols, header: header, delim: sp.delim };
  }

  // A column's kind: "numbers" (blanks and a few odd cells allowed, they become blanks) or "text" (coded 1, 2, ...
  // by its labels in sorted order).  A column is text when most of its non-empty cells are not numbers.
  function describe(col) {
    let nums = 0, texts = 0, empty = 0;
    const labels = new Set();
    let lo = Infinity, hi = -Infinity;
    for (const c of col) {
      if (c === '') { empty++; continue; }
      const p = parseNumber(c);
      if (p !== null && inRange(p)) {
        nums++;
        const v = Number(c.replace(/−/g, '-').replace(/,/g, ''));
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      } else { texts++; labels.add(c); }
    }
    const kind = texts > nums ? 'text' : 'numbers';
    let codes = null;
    if (kind === 'text') {
      const sorted = Array.from(labels).sort((a, b) => a.localeCompare(b));
      codes = new Map(sorted.map((s, i) => [s, i + 1]));
    }
    const values = kind === 'text' ? texts : nums;
    return { kind: kind, values: values, blanks: col.length - values, empty: empty, odd: kind === 'text' ? nums : texts,
             lo: lo, hi: hi, codes: codes };
  }

  // The cell as the Prime will hold it: a parsed number, or the blank marker.
  function cellWord(text, info) {
    if (info.kind === 'text') {
      if (text === '' || !info.codes.has(text)) return BLANK_WORD;
      return parseNumber(String(info.codes.get(text)));
    }
    const p = parseNumber(text);
    if (p === null || !inRange(p)) return BLANK_WORD;
    return p;
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
           crc32, zip, BLANK_WORD };
})();

if (typeof module !== 'undefined') module.exports = DLCore;
