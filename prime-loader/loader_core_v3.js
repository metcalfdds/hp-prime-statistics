// loader_core_v3.js -- the Prime Loader's file work: find the Virtual Calculator's folder, move what is on it to a
// dated backup, and write the chosen programs and data into it.  Roger Metcalf & Claude.
// v3 (17 Nov 2026, night; Roger: "let the student choose?--1) put all the programs on the Virtual Calculator at once
//   or 2) I'll choose which Chapter to load, one at a time"): planBook, for "one chapter": the book's own programs are
//   moved to the backup, so that the calculator lists that chapter's, and a program of the student's own is never
//   moved.  plan, which moved every program whoever wrote it (v1's way), is gone: nothing on the page uses it.
// v2 (17 Nov 2026, the review "they must be bullet proof and as simple as possible"): planAdd, for a data file loaded
//   on its own (only the files about to be replaced are moved; v1 moved every program off the calculator), and
//   checkHpmat, which looks inside a data file before it is taken.  Everything else is v1's (1 Nov 2026).
//
// No DOM here.  The page hands it a FileSystemDirectoryHandle (the folder the student picked, through the browser's
// File System Access API); the tests hand it a folder in the browser's private file system (OPFS), which has the same
// interface.  Nothing is ever deleted outright: every file is copied into the backup and read back before the original
// is removed.
//
// WHAT WE KNOW ABOUT THE FOLDER (Lessons Learned v7ze, Section 16; hp-prime-kit docs/topics/deploy.md):
//   Documents\HP Prime\Calculators\Prime   the calculator's whole memory, read when it starts.  A program copied in
//                                          while the calculator is closed is in its Program Catalog at the next start.
//   Documents\HP Prime\Temp\HPEmuInstance.lock   present while a calculator window holds "Prime" (gone when it closes).
//   A running calculator writes its memory back when it exits, so anything written while it runs would be undone:
//   the loader refuses to write while the lock is there, unless the student says the calculator is closed.
//   HP's own apps are folders whose names begin with "&" (&Statistics 1Var.hpappdir ...): never touched.
//   A backup must live OUTSIDE Calculators\, where every folder is read as a calculator of its own.

'use strict';

const LoaderCore = (function () {

  async function child(dir, name, kind) {          // a child handle, or null when there is none
    try {
      return kind === 'dir' ? await dir.getDirectoryHandle(name) : await dir.getFileHandle(name);
    } catch (e) {
      return null;
    }
  }

  async function names(dir) {                      // [{name, kind}] in a folder, sorted
    const out = [];
    for await (const [name, h] of dir.entries()) out.push({ name: name, kind: h.kind });
    out.sort((a, b) => a.name.localeCompare(b.name));
    return out;
  }

  // The student may pick HP Prime (asked for), Documents, Calculators or Prime.  Returns
  //   {ok:true, base, calc, how}   base = the HP Prime folder, calc = Calculators\Prime
  //   {ok:false, why}              a sentence for the student
  async function locate(picked) {
    const n = picked.name;
    let base = null;
    if (await child(picked, 'Calculators', 'dir')) base = picked;                       // HP Prime itself
    else {
      const hp = await child(picked, 'HP Prime', 'dir');                                // Documents
      if (hp && await child(hp, 'Calculators', 'dir')) base = hp;
    }
    if (!base) {
      if (n === 'Calculators' || n === 'Prime' || /^Prime_\d+$/.test(n))
        return { ok: false, why: 'That is a folder inside "HP Prime". Please choose the folder named HP Prime itself (in Documents).' };
      return { ok: false, why: 'That folder has no calculator in it. Please choose the folder named HP Prime, in Documents.' };
    }
    const cals = await child(base, 'Calculators', 'dir');
    const calc = await child(cals, 'Prime', 'dir');
    if (!calc)
      return { ok: false, why: 'The Virtual Calculator has not made its folder yet. Start it once, close it (Calculator menu, Exit), then try again.' };
    return { ok: true, base: base, calc: calc, how: picked === base ? 'HP Prime' : 'Documents' };
  }

  async function isRunning(base) {                 // the lock file of the calculator named Prime
    const t = await child(base, 'Temp', 'dir');
    if (!t) return false;
    return !!(await child(t, 'HPEmuInstance.lock', 'file'));
  }

  // planBook (v3), for "one chapter": what to move before that chapter's programs are written.  bookTops is every
  // file and folder name the page can load (AnovaLab.hpprgm ... CentralLimit.hpappdir).  Whatever on the calculator
  // has one of those names is moved, and so is a file about to be replaced (a data matrix); a program of the
  // student's own, whose name the book does not use, stays where it is, and so does everything of HP's.
  async function planBook(calc, bookTops, paths) {
    const book = bookTops.map(s => s.toLowerCase()), tops = paths.map(p => p.split('/')[0].toLowerCase());
    const move = [];
    for (const e of await names(calc)) {
      const n = e.name.toLowerCase();
      if (e.name[0] !== '&' && (book.includes(n) || tops.includes(n))) move.push(e);
    }
    return move;
  }

  // v2: what would move when files are ADDED to what is on the calculator (all the programs, programs picked one by
  // one, a data file with DataLoad): only the entries about to be replaced, matched by name without regard to
  // capitals.  HP's own apps never.
  async function planAdd(calc, paths) {
    const tops = paths.map(p => p.split('/')[0].toLowerCase());
    const move = [];
    for (const e of await names(calc)) if (e.name[0] !== '&' && tops.includes(e.name.toLowerCase())) move.push(e);
    return move;
  }

  // v2: is this a matrix file the calculator can read?  '' when it is, else the reason as the end of a sentence.
  // (hp-prime-kit, docs/topics/formats.md, formats.hpmat: bytes 01 00; the type, whose low byte is 14 for real and
  // 94 for complex numbers; the rank, 2 or 1; rows; columns; then 8 bytes for a real cell, 16 for a complex one.)
  function checkHpmat(b) {
    if (b.length < 16) return 'it is too short to be a calculator matrix file';
    if (b[0] !== 1 || b[1] !== 0 || (b[2] !== 0x14 && b[2] !== 0x94)) return 'it does not begin the way a calculator matrix file does';
    const v = new DataView(b.buffer, b.byteOffset, b.byteLength);
    const rank = v.getUint32(4, true), rows = v.getUint32(8, true), cols = v.getUint32(12, true);
    if (rank !== 1 && rank !== 2) return 'it does not begin the way a calculator matrix file does';
    if (rows * cols === 0) return 'it holds no numbers';
    if (16 + (b[2] === 0x94 ? 16 : 8) * rows * cols !== b.length) return 'its size does not match the rows and columns it names (the file may be cut short)';
    return '';
  }

  async function readAll(fileHandle) {
    const f = await fileHandle.getFile();
    return new Uint8Array(await f.arrayBuffer());
  }

  async function writeFile(dir, name, bytes) {
    const fh = await dir.getFileHandle(name, { create: true });
    const w = await fh.createWritable();
    await w.write(bytes);
    await w.close();
    const back = await readAll(fh);                  // read it back: same length, same bytes
    if (back.length !== bytes.length) throw new Error('read-back length differs: ' + name);
    for (let i = 0; i < back.length; i++) if (back[i] !== bytes[i]) throw new Error('read-back differs: ' + name);
    return back.length;
  }

  async function copyTree(src, dstParent, name) {  // copies a file or a folder; returns bytes copied
    if (src.kind === 'file') return writeFile(dstParent, name, await readAll(src));
    const d = await dstParent.getDirectoryHandle(name, { create: true });
    let total = 0;
    for await (const [n, h] of src.entries()) total += await copyTree(h, d, n);
    return total;
  }

  function stamp(now) {                            // "2026-11-01 0812": Windows-safe, sorts by time
    const p = v => String(v).padStart(2, '0');
    return now.getFullYear() + '-' + p(now.getMonth() + 1) + '-' + p(now.getDate()) + ' ' + p(now.getHours()) + p(now.getMinutes());
  }

  // Moves the planned entries into  HP Prime\Loader backups\<stamp>\  (copy, read back, then remove).
  async function backup(base, calc, move, now) {
    if (move.length === 0) return { folder: null, moved: [] };
    const root = await base.getDirectoryHandle('Loader backups', { create: true });
    let name = stamp(now), k = 1;
    while (await child(root, name, 'dir')) name = stamp(now) + ' (' + (++k) + ')';
    const dest = await root.getDirectoryHandle(name, { create: true });
    const moved = [];
    for (const e of move) {
      const h = e.kind === 'file' ? await calc.getFileHandle(e.name) : await calc.getDirectoryHandle(e.name);
      await copyTree(h, dest, e.name);
      await calc.removeEntry(e.name, { recursive: true });
      moved.push(e.name);
    }
    return { folder: 'Loader backups\\' + name, moved: moved };
  }

  // files: [{path: 'TTestLabG.hpprgm' or 'CentralLimit.hpappdir/CentralLimit.hpapp', data: Uint8Array}]
  async function install(calc, files) {
    const written = [];
    for (const f of files) {
      const parts = f.path.split('/');
      let d = calc;
      for (let i = 0; i < parts.length - 1; i++) d = await d.getDirectoryHandle(parts[i], { create: true });
      await writeFile(d, parts[parts.length - 1], f.data);
      written.push(f.path);
    }
    return written;
  }

  // ---- reading the embedded zip (deflate or stored), with each file's CRC checked ----
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

  async function inflateRaw(bytes) {
    const ds = new DecompressionStream('deflate-raw');
    const out = new Response(new Blob([bytes]).stream().pipeThrough(ds));
    return new Uint8Array(await out.arrayBuffer());
  }

  // zip bytes -> Map(name -> Uint8Array), every CRC checked
  async function unzip(zipBytes) {
    const v = new DataView(zipBytes.buffer, zipBytes.byteOffset, zipBytes.byteLength);
    let e = zipBytes.length - 22;
    while (e >= 0 && v.getUint32(e, true) !== 0x06054b50) e--;
    if (e < 0) throw new Error('not a zip');
    const count = v.getUint16(e + 10, true);
    let p = v.getUint32(e + 16, true);
    const dec = new TextDecoder();
    const out = new Map();
    for (let i = 0; i < count; i++) {
      if (v.getUint32(p, true) !== 0x02014b50) throw new Error('bad central directory');
      const method = v.getUint16(p + 10, true), crc = v.getUint32(p + 16, true);
      const csize = v.getUint32(p + 20, true), usize = v.getUint32(p + 24, true);
      const nlen = v.getUint16(p + 28, true), xlen = v.getUint16(p + 30, true), clen = v.getUint16(p + 32, true);
      const off = v.getUint32(p + 42, true);
      const name = dec.decode(zipBytes.subarray(p + 46, p + 46 + nlen));
      p += 46 + nlen + xlen + clen;
      if (name.endsWith('/')) continue;
      const lnlen = v.getUint16(off + 26, true), lxlen = v.getUint16(off + 28, true);
      const raw = zipBytes.subarray(off + 30 + lnlen + lxlen, off + 30 + lnlen + lxlen + csize);
      const data = method === 0 ? raw.slice() : method === 8 ? await inflateRaw(raw) : null;
      if (!data) throw new Error('unsupported compression in ' + name);
      if (data.length !== usize || crc32(data) !== crc) throw new Error('damaged file in the page: ' + name);
      out.set(name, data);
    }
    return out;
  }

  return { locate, isRunning, planAdd, planBook, checkHpmat, backup, install, unzip, crc32, stamp, names };
})();

if (typeof module !== 'undefined') module.exports = LoaderCore;
