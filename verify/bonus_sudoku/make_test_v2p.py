# Makes prime-loader/tests/test_loader_v2p.js from v2o by exact replacements, and adds part 14, the bonus (26 Nov 2026).
# v2o's test is read from git (BASE, main before the bonus), and v2p's is written into this repository's
# prime-loader/tests/; in a shallow clone, deepen it first (git fetch --deepen=50 origin main).  Run from anywhere.
import io, os, subprocess
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(REPO, 'prime-loader', 'tests', '')
BASE = '8483e62'                     # main before the bonus (PR 34 merged)
s = subprocess.run(['git', 'show', BASE + ':prime-loader/tests/test_loader_v2o.js'], check=True, capture_output=True,
                   cwd=REPO).stdout.decode('utf-8')
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:90]); s = s.replace(old, new)
rep("// test_loader_v2o.js -- drives PrimeLoader_v2o.html in Chromium", "// test_loader_v2p.js -- drives PrimeLoader_v2p.html in Chromium")
rep("// Roger Metcalf & Claude, 18 Nov 2026.   node tests/test_loader_v2o.js PrimeLoader_v2o.html PACK.zip\n//\n",
    "// Roger Metcalf & Claude, 18 Nov 2026.   node tests/test_loader_v2p.js PrimeLoader_v2p.html PACK.zip\n//\n"
    "// v2p (26 Nov 2026): test_loader_v2o.js with the page's new name and the new name of \"More choices\", and part 14, the\n"
    "// bonus: Sudoku, from starter pack v26's \"Bonus (optional)\", is in the catalog as a bonus and not among the 31, in no\n"
    "// Sample; under More choices it has a box of its own; ticked, it is named in the summary and goes onto the Virtual\n"
    "// Calculator with the Population (34 files) or alone (1 file), byte for byte as the pack holds it, and down the cable\n"
    "// with a Sample, its source as the pack's and as extras/sudoku/'s; the log's \"Chosen:\" line names it; and a later\n"
    "// Sample that does not tick it leaves it on the calculator.\n//\n")
rep("/More choices: single programs, and data/", "/More choices: single programs, data, and the bonus/", 2)
rep("/PrimeLoader_v2o\\.html\\?data=1$/", "/PrimeLoader_v2p\\.html\\?data=1$/")
rep('content="0; url=PrimeLoader_v2o\\.html"><\\/noscript>/', 'content="0; url=PrimeLoader_v2p\\.html"><\\/noscript>/')
rep("/^HP Prime Loader, v2o, straight down the cable\\. /", "/^HP Prime Loader, v2p, straight down the cable\\. /")
PART14 = r"""
  // ---- 14 (v2p). the bonus, Sudoku, under "More choices" ----
  {
    const bonusFile = fs.readFileSync(path.join(tmp, 'Bonus (optional)', 'Sudoku.hpprgm'));
    const B = CATALOG.bonus && CATALOG.bonus.Sudoku;
    const bsrc = B ? bonusFile.subarray(B.src[0], B.src[1]).toString('utf16le').replace(/\0+$/, '') : '';
    const EX = path.join(__dirname, '..', '..', 'extras', 'sudoku');
    const exSrc = canon(fs.readFileSync(path.join(EX, fs.readdirSync(EX).find(x => /^Sudoku_beta[^_]+\.txt$/.test(x))), 'utf8'));
    check('bonus: the catalog has Sudoku as a bonus, checked, its source in the pack the same as extras/sudoku/\'s but for the blank space at its end; it is not one of the 31 and in no Sample',
          !!B && CATALOG.bonus_checked.Sudoku === true && B.files.length === 1 && B.files[0] === 'Sudoku.hpprgm' && canon(bsrc) === exSrc && !('Sudoku' in CATALOG.programs) &&
          Object.keys(CATALOG.programs).length === 31 && !CATALOG.groups.some(g => g.programs.includes('Sudoku')), JSON.stringify(B && [B.version, B.src, B.bytes]));
    const bp = await ctx.newPage(), berrs = [];
    bp.on('pageerror', e => berrs.push(String(e)));
    await bp.goto('http://localhost:8766/');
    await bp.evaluate(async () => {           // the calculator is closed for this part: no lock
      const t = await (await (await navigator.storage.getDirectory()).getDirectoryHandle('HP Prime')).getDirectoryHandle('Temp');
      try { await t.removeEntry('HPEmuInstance.lock'); } catch (e) { }
    });
    await bp.click('#more > summary');
    check('bonus: under "More choices", one box of its own, not ticked, with its words; the list to tick still has 31 programs, and the Population is still the 31',
          await bp.locator('#bonuslist input[type=checkbox]').count() === 1 && !(await bp.isChecked('#b_Sudoku')) &&
          /^Add Sudoku, just for fun: a Sudoku puzzle game, the book's Appendix G\.\s?Sudoku is a bonus, and not one of the Statisticles, so it goes onto the calculator only when this box is ticked, together with whatever else you choose, and this page never takes it off a calculator\.$/.test((await bp.textContent('#bonuslist')).replace(/\s+/g, ' ').trim()) &&
          await bp.locator('#proglist .prog input').count() === 31 && (await bp.textContent('#summary')) === 'The Population: all 31 Statisticles.', (await bp.textContent('#bonuslist')).replace(/\s+/g, ' '));
    await bp.check('#b_Sudoku');
    check('bonus: ticked beside the Population, the summary names it after the 31', (await bp.textContent('#summary')) === 'The Population: all 31 Statisticles, and Sudoku, the bonus.', await bp.textContent('#summary'));
    const had = (await readTree())[C + 'Sudoku.hpprgm'];
    await bp.click('#load');
    await bp.waitForFunction(() => /every file read back and checked/.test(document.getElementById('status').textContent) || !document.getElementById('running').hidden);
    await bp.waitForSelector('#done:not([hidden])', { timeout: 60000 });
    let bt = await readTree(), brep = await bp.textContent('#report');
    check('bonus, Virtual Calculator, the Population and Sudoku: 34 files went on, Sudoku.hpprgm byte for byte as the pack\'s bonus file, and the 30 program files too',
          had === undefined && same(bt[C + 'Sudoku.hpprgm'], bonusFile) && /^34 files went onto the calculator, and each was read back and checked\./.test(brep) &&
          packPrg.every(n => same(bt[C + n], packFile(n))), brep);
    // Sudoku alone: "Only the programs I tick", none ticked, and the bonus's box
    await bp.reload();
    await bp.click('#more > summary');
    await bp.check('#w_pick');
    await bp.check('#b_Sudoku');
    check('bonus alone: the summary says only that, and Load is on', (await bp.textContent('#summary')) === 'Sudoku, the bonus.' && !(await bp.isDisabled('#load')), await bp.textContent('#summary'));
    await bp.click('#load');
    await bp.waitForSelector('#done:not([hidden])', { timeout: 60000 });
    bt = await readTree(); brep = await bp.textContent('#report');
    check('bonus alone: 1 file went on, Sudoku.hpprgm, byte for byte (the box and the label are two blocks, so their words meet without a space in textContent)', /^1 file went onto the calculator, and it was read back and checked\.|^1 file went onto the calculator/.test(brep) &&
          same(bt[C + 'Sudoku.hpprgm'], bonusFile), brep);
    check('bonus: no errors on its page', berrs.length === 0, berrs);
    await bp.close();
    // the cable: Chapters 1-3 and Sudoku, then Chapters 4-6 without it
    const ub = await usbPage({});
    await ub.p.check('#t_real');
    await ub.p.selectOption('#group', 'c1');
    await ub.p.click('#more > summary');
    await ub.p.check('#b_Sudoku');
    const c1 = CATALOG.groups.find(g => g.id === 'c1').programs.slice().sort((a, b) => a.localeCompare(b));
    check('bonus, cable: the summary names Chapters 1–3 and the bonus', (await ub.p.textContent('#summary')) === 'Chapters 1–3: ' + c1.join(', ') + ', and Sudoku, the bonus.', await ub.p.textContent('#summary'));
    await ub.p.click('#usbsend');
    await usbEnd(ub.p);
    let bst = await state(ub.p), bgot = await prime(ub.p);
    check('bonus, cable: every program and Sudoku on the calculator, each download verified; Sudoku\'s source is the pack\'s, character for character, and extras/sudoku/\'s but for the blank space at its end',
          bst.done && !bst.fail && bst.status === (c1.length + 1) + ' programs on the calculator, each download verified.' && bgot.programs.Sudoku === bsrc && canon(bgot.programs.Sudoku) === exSrc &&
          c1.every(n => bgot.programs[n] === packSource(n)) && Object.keys(bgot.programs).length === c1.length + 1, JSON.stringify([bst.status, Object.keys(bgot.programs)]));
    check('bonus, cable: the log\'s "Chosen:" line names the bonus', new RegExp('\\nChosen: Chapters 1–3, and the bonus Sudoku; ' + (c1.length + 1) + ' programs, ').test(bst.log), bst.log.split('\n').find(l => /^Chosen/.test(l)));
    await ub.p.check('#b_Sudoku', { force: true });
    await ub.p.uncheck('#b_Sudoku');
    await ub.p.selectOption('#group', 'c4');
    await ub.p.click('#usbsend');
    await usbEnd(ub.p);
    bst = await state(ub.p); bgot = await prime(ub.p);
    const c4 = CATALOG.groups.find(g => g.id === 'c4').programs;
    check('bonus, cable: a later Sample without it leaves Sudoku on the calculator (the page never takes it off), while the Statisticles not in that Sample are taken off',
          bst.done && bgot.programs.Sudoku === bsrc && c4.every(n => bgot.programs[n] === packSource(n)) &&
          Object.keys(bgot.programs).filter(n => n !== 'Sudoku').every(n => c4.includes(n)), JSON.stringify(Object.keys(bgot.programs)));
    check('bonus, cable: no errors on its page', ub.errs.length === 0, ub.errs);
  }

  check('no errors in the page', errors.length === 0, errors);"""
rep("\n  check('no errors in the page', errors.length === 0, errors);", PART14)
io.open(P + 'test_loader_v2p.js', 'w', encoding='utf-8').write(s)
print('ok', len(s))
