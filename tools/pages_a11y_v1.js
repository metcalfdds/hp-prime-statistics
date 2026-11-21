// pages_a11y_v1.js -- the accessibility check of the two loader pages (21 Nov 2026), against WCAG 2.1 A and AA.
//   node tools/pages_a11y_v1.js            (needs Playwright, as the pages' own tests do, and axe-core: npm install axe-core)
// For each page, in each state a student can put it in (below), in the light and the dark colors:
//   1. axe-core's automated rules for WCAG 2.0 and 2.1, levels A and AA: no violation.  What axe cannot decide by itself
//      (it calls these "incomplete") is printed for a person to read; the step numerals are the usual ones.
//   2. Reflow (1.4.10): in a window 320 px wide the page does not scroll sideways.
//   3. Keyboard (2.1.1, 2.4.7): every stop of the Tab key is on the screen and shows a focus mark.
//   4. Headings: no level is skipped (a best practice, not a rule of WCAG).
// The current page of each folder is read from that folder's index.html, so a new version needs no change here.
// WHAT THIS DOES NOT SHOW: that a screen reader reads the page well.  No screen reader was run.  A program finds roughly a
// third to a half of the things WCAG asks for; the rest takes a person (docs/dev/pages-accessibility-2026-11-21.md).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
let axePath; try { axePath = require.resolve('axe-core/axe.min.js'); } catch (e) { console.error('axe-core is not installed: npm install axe-core'); process.exit(2); }
const ROOT = path.join(__dirname, '..');
const current = dir => path.join(ROOT, dir, fs.readFileSync(path.join(ROOT, dir, 'index.html'), 'utf8').match(/([A-Za-z]+Loader_v[0-9a-z]+\.html)/)[1]);
const open_all = 'document.querySelectorAll("details").forEach(d => d.open = true)';
const PAGES = [
  ['prime-loader', [['as opened', ''], ['a real HP Prime chosen', 'document.getElementById("t_real").click()'], ['... and every fold opened', open_all],
                    ['... and "tick the programs yourself"', 'document.getElementById("w_pick").click()'], ['the Virtual Calculator again, folds open', 'document.getElementById("t_vc").click()']]],
  ['data-loader', [['as opened', ''], ['the example loaded', 'document.getElementById("example").click()'], ['... and every fold opened', open_all]]]];
let pass = 0, fail = 0;
const check = (name, ok, detail) => { if (ok) { pass++; console.log('PASS', name); } else { fail++; console.log('FAIL', name, detail === undefined ? '' : JSON.stringify(detail).slice(0, 600)); } };
(async () => {
  const b = await chromium.launch();
  for (const [dir, states] of PAGES) {
    const file = current(dir); console.log('\n== ' + path.relative(ROOT, file));
    for (const scheme of ['light', 'dark']) {
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 }, colorScheme: scheme }); const p = await ctx.newPage();
      await p.goto('file://' + file); await p.addScriptTag({ path: axePath });
      for (const [label, js] of states) {
        if (js) { await p.evaluate(js); await p.waitForTimeout(350); }
        const r = await p.evaluate(async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'] }, resultTypes: ['violations', 'incomplete'] }));
        check(scheme + ', ' + label + ': no violation of axe\'s WCAG A and AA rules (' + r.passes.length + ' rules passed)', r.violations.length === 0,
              r.violations.map(v => v.id + ' x' + v.nodes.length + ': ' + v.nodes[0].target.join(' ') + ' ' + (v.nodes[0].any[0] ? v.nodes[0].any[0].message : '')));
        if (r.incomplete.length) console.log('     for a person to read: ' + r.incomplete.map(v => v.id + ' x' + v.nodes.length + ' (' + v.nodes.map(n => n.target.join(' ')).slice(0, 4).join(', ') + ')').join('; '));
        if (scheme === 'light') {
          const hs = await p.evaluate(() => [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(h => h.getBoundingClientRect().height > 0).map(h => +h.tagName[1]));
          check('... ' + label + ': no heading level is skipped (' + hs.length + ' headings)', hs.every((l, i) => i === 0 ? l === 1 : l <= hs[i - 1] + 1), hs.join(''));
        }
      }
      await ctx.close();
    }
    for (const [label, js] of states.filter((s, i) => i === 0 || i === states.length - 1)) {            // reflow: the first state and the fullest one
      const ctx = await b.newContext({ viewport: { width: 320, height: 800 } }); const p = await ctx.newPage(); await p.goto('file://' + file);
      for (const [l2, j2] of states) { if (j2) { await p.evaluate(j2); await p.waitForTimeout(200); } if (l2 === label) break; }
      const over = await p.evaluate(() => document.documentElement.scrollWidth - document.documentElement.clientWidth);
      check('320 px wide, ' + label + ': the page does not scroll sideways', over <= 0, over + ' px too wide'); await ctx.close();
    }
    for (const [label, js] of [states[0], states[1]]) {                                                 // the Tab key
      const ctx = await b.newContext({ viewport: { width: 1280, height: 900 } }); const p = await ctx.newPage(); await p.goto('file://' + file);
      if (js) { await p.evaluate(js); await p.waitForTimeout(300); }
      const seen = new Set(); const bad = []; let n = 0;
      for (let i = 0; i < 120; i++) {
        await p.keyboard.press('Tab');
        const s = await p.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return null; if (!e.dataset.a11yStop) e.dataset.a11yStop = String(Math.random());
          const c = getComputedStyle(e), r = e.getBoundingClientRect(), lab = e.closest('label, .filebtn'); const lc = lab ? getComputedStyle(lab) : null;
          const mark = (c.outlineStyle !== 'none' && parseFloat(c.outlineWidth) > 0) || c.boxShadow !== 'none' || (lc && lc.outlineStyle !== 'none' && parseFloat(lc.outlineWidth) > 0);
          return { key: e.dataset.a11yStop, id: e.tagName + (e.id ? '#' + e.id : ''), mark, vis: (r.width > 1 && r.height > 1) || !!lab }; });
        if (!s || seen.has(s.key)) break; seen.add(s.key); n++;
        if (!s.mark) bad.push('no focus mark: ' + s.id); if (!s.vis) bad.push('not on the screen: ' + s.id);
      }
      check('Tab key, ' + label + ': ' + n + ' stops, each on the screen with a focus mark', n > 3 && bad.length === 0, bad);
      await ctx.close();
    }
  }
  console.log('\n' + pass + ' PASS, ' + fail + ' FAIL'); await b.close(); process.exit(fail ? 1 : 0);
})().catch(e => { console.error(e); process.exit(2); });
