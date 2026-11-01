// page_check_v3.js -- opens DataLoader_v3.html in Chromium (Playwright), reads the example, downloads M1.hpmat and
// compares it with examples/M1.hpmat (the file that ran on the Virtual Calculator), then pastes a text-coded
// table.  Run: node page_check_v3.js   (needs Playwright)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ acceptDownloads: true, viewport: { width: 1100, height: 1500 } });
  const p = await ctx.newPage();
  const errs = [];
  p.on('pageerror', e => errs.push(String(e)));
  p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + path.join(__dirname, '..', 'DataLoader_v3.html'));
  await p.waitForTimeout(800);
  console.log('readout:', await p.textContent('#readout'));
  console.log('summary:', await p.textContent('#summary'));
  console.log('rows in table:', await p.$$eval('#cols tbody tr', r => r.length));
  console.log('button:', await p.textContent('#save'));
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('#save')]);
  const dlPath = path.join(require('os').tmpdir(), 'page_M1.hpmat'); await dl.saveAs(dlPath);
  const same = Buffer.compare(fs.readFileSync(dlPath), fs.readFileSync(path.join(__dirname, '..', 'examples', 'M1.hpmat'))) === 0;
  console.log('download:', dl.suggestedFilename(), fs.statSync(dlPath).size, 'bytes; identical to the file tested on the calculator:', same);
  console.log('status:', await p.textContent('#savestatus'));
  await p.screenshot({ path: path.join(require('os').tmpdir(), 'dl_page_v3.png'), fullPage: true });
  // a paste with text groups and blanks
  await p.fill('#paste', 'score\tsex\n12\tmale\n15\tfemale\nNA\tmale\n9\tfemale\n');
  await p.waitForTimeout(500);
  console.log('text case:', await p.textContent('#readout'), '|', await p.textContent('#padnote'));
  console.log('codes cell:', await p.$$eval('td.codes', t => t.map(x => x.textContent)));
  console.log('errors:', errs);
  await b.close();
})();
