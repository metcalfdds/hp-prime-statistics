// idb_handle_probe_v1.js (15 Nov 2026) -- does this browser survive reading a folder handle back from IndexedDB?
//
// The Prime Loader remembers the calculator's folder by keeping its FileSystemDirectoryHandle in IndexedDB.  On the
// cloud workspace of 15 Nov 2026 (Chrome for Testing 153.0.8010.12 under Playwright 1.63, both the headless shell and
// the full build) the browser process ended with SIGTRAP the moment such a handle was read back, with a page that
// holds nothing of ours: this one.  A string put and read is fine; putting the handle is fine; reading it is not.
// test_loader_v1t.js therefore keeps the handle's name there.  Whether a student's Chrome or Edge does the same with
// a folder picked from the disk cannot be tried here (the picker has no window in a headless browser): try the page
// itself on a real browser, twice, so that the second visit reads the handle.
//
//   node tests/idb_handle_probe_v1.js
const { chromium } = require('playwright');
const http = require('http');
const IDB = `const idb = () => new Promise((res, rej) => { const r = indexedDB.open('t', 1); r.onupgradeneeded = () => r.result.createObjectStore('kv'); r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); });
const put = async (k, v) => { const db = await idb(); await new Promise(res => { const t = db.transaction('kv', 'readwrite'); t.objectStore('kv').put(v, k); t.oncomplete = res; t.onerror = res; }); };
const get = async (k) => { const db = await idb(); return await new Promise(res => { const q = db.transaction('kv').objectStore('kv').get(k); q.onsuccess = () => res(q.result); q.onerror = () => res(undefined); }); };`;
const DIR = ` const r = await navigator.storage.getDirectory(); const d = await r.getDirectoryHandle('HP Prime', { create: true });`;
const OPS = {
  'a string put and read': IDB + ` await put('a', 'hello'); return await get('a');`,
  'a folder handle put': IDB + DIR + ` await put('h', d); return 'put';`,
  'a folder handle put and read back': IDB + DIR + ` await put('h', d); const h = await get('h'); return 'read ' + (h && h.name);`,
};
(async () => {
  const srv = http.createServer((q, r) => { r.writeHead(200, { 'Content-Type': 'text/html' }); r.end('<html><body>x</body></html>'); }).listen(8795);
  let bad = 0;
  for (const name of Object.keys(OPS)) {
    let b;
    try {
      b = await chromium.launch();
      const p = await (await b.newContext()).newPage();
      await p.goto('http://localhost:8795/');
      console.log('OK  ', name, ':', await p.evaluate('(async () => {' + OPS[name] + '})()'), ' (' + b.version() + ')');
    } catch (e) { bad++; console.log('STOP', name, ':', String(e).split('\n')[0].slice(0, 110)); }
    try { await b.close(); } catch (e) { /* already gone */ }
  }
  srv.close();
  process.exit(bad ? 1 : 0);
})();
