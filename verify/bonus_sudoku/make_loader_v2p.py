# Makes prime-loader/build_loader_v2p.py and loader_template_v2p.html from v2o by exact replacements (26 Nov 2026):
# the bonus program, Sudoku, offered under "More choices" (Roger's choice of 26 Nov 2026; the 31 stay the Population).
# v2o's files are read from git (BASE, main before the bonus), and v2p's are written into this repository's
# prime-loader/; in a shallow clone, deepen it first (git fetch --deepen=50 origin main).  Run from anywhere.
import io, os, subprocess
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
P = os.path.join(REPO, 'prime-loader', '')
BASE = '8483e62'                     # main before the bonus (PR 34 merged)
def load(n):
    if '_v2p' in n:                  # the second pass reads what the first pass wrote
        return io.open(P + n, encoding='utf-8').read()
    return subprocess.run(['git', 'show', '%s:prime-loader/%s' % (BASE, n)], check=True, capture_output=True,
                          cwd=REPO).stdout.decode('utf-8')
def rep(s, old, new, n=1):
    assert s.count(old) == n, (s.count(old), old[:90]); return s.replace(old, new)

# ------------------------------------------------------------------ the build script
b = load('build_loader_v2o.py')
b = rep(b, '"""build_loader_v2o.py -- assembles PrimeLoader_v2o.html:', '"""build_loader_v2p.py -- assembles PrimeLoader_v2p.html:')
b = rep(b, '    python3 build_loader_v2o.py PACK.zip [OUT.html] [--kit PATH]\n',
        '    python3 build_loader_v2p.py PACK.zip [OUT.html] [--kit PATH]\n'
        'v2p (26 Nov 2026): the bonus.  Starter pack v26 (tools/make_starter_pack_v5.py) carries Sudoku beta 2a, the book\'s\n'
        'just-for-fun program (Appendix G), in a folder of its own, "Bonus (optional)", checked on the Virtual Calculator.\n'
        'The page offers it under "More choices" as a box of its own (BONUS below; Roger, 26 Nov 2026, chose the Loader\'s\n'
        '"More choices" for it, with the 31 Statisticles staying the Population): ticked, it goes onto the calculator with\n'
        'whatever else is chosen, by the cable as a program goes (its source, verified), and on the Virtual Calculator as a\n'
        'file; it is in no Sample and not in the Population, and the page never takes it off a calculator.  Its source in\n'
        'the pack must be extras/sudoku/Sudoku_*.txt character for character, as a program\'s must be programs/\'s.\n')
b = rep(b, "OUT = argv[1] if len(argv) > 1 else os.path.join(HERE, 'PrimeLoader_v2o.html')",
        "OUT = argv[1] if len(argv) > 1 else os.path.join(HERE, 'PrimeLoader_v2p.html')")
b = rep(b, """for num, title, progs, _ in CHAPTERS:
    for p in progs:
        assert p in PROGRAMS, (num, p)""", """# v2p: the bonus (not one of the 31): name: (file in the pack, name on the calculator, what it is, the name to type in Home,
# its folder in the repository).  Its version is read from that folder's file name, as a program's is from programs/.
BONUS = {
  'Sudoku': ('Bonus (optional)/Sudoku.hpprgm', 'Sudoku.hpprgm', 'a Sudoku puzzle game, the book\\'s Appendix G', 'Sudoku',
             'extras/sudoku'),
}
BONUS_VER = {}
for _k, _v in BONUS.items():
    _m = [re.match('^' + re.escape(_k) + r'_(beta|v)([^_]+)\\.txt$', os.path.basename(_p))
          for _p in glob.glob(os.path.join(os.path.dirname(HERE), _v[4], _k + '_*.txt'))]
    _m = [_x for _x in _m if _x]
    if len(_m) != 1: sys.exit('STOP: %s holds %d files for %s' % (_v[4], len(_m), _k))
    BONUS_VER[_k] = ('beta ' + _m[0].group(2)) if _m[0].group(1) == 'beta' else 'v' + _m[0].group(2)
    assert _k not in PROGRAMS, _k

for num, title, progs, _ in CHAPTERS:
    for p in progs:
        assert p in PROGRAMS, (num, p)""")
b = rep(b, """for key, (src, dst, _) in DATA.items():
    packed[dst] = zin.read(src)
""", """for key, (src, dst, _) in DATA.items():
    packed[dst] = zin.read(src)
for key, v in BONUS.items():                     # v2p: the bonus, from its own folder of the pack
    if v[0] not in zin.namelist():
        sys.exit('STOP: the pack has no %s' % v[0])
    assert v[1] not in packed, v[1]
    packed[v[1]] = zin.read(v[0])
""")
b = rep(b, """# The groups (see CHAPTER_GROUPS), sized by the characters each program sends down the cable.""",
        """# v2p: the bonus's source must be the repository's, and it travels down the cable the same way.
bonus_src, bonus_len, bonus_checked = {}, {}, {}
for k, v in BONUS.items():
    text, _, start, end = kitprog.read(packed[v[1]])
    mine = glob.glob(os.path.join(os.path.dirname(HERE), v[4], k + '_*.txt'))
    mine = [p for p in mine if re.match('^' + re.escape(k) + r'_(beta|v)[^_]+\\.txt$', os.path.basename(p))]
    want = kitprog.normalize_source(open(mine[0], encoding='utf-8').read()).rstrip()
    if kitprog.normalize_source(text).rstrip() != want:
        sys.exit('STOP: the source inside %s is not %s/%s' % (v[0], v[4], os.path.basename(mine[0])))
    if packed[v[1]][start:end].decode('utf-16-le').rstrip('\\0') != text:
        sys.exit('STOP: the offsets of %s do not give its source' % v[1])
    bonus_src[k] = [start, end]
    bonus_len[k] = len(text)
    bonus_checked[k] = bool(checked_file(packed[v[1]]))

# The groups (see CHAPTER_GROUPS), sized by the characters each program sends down the cable.""")
b = rep(b, """  'pack': os.path.basename(PACK),
  'loader': 'v2o',""", """  'bonus': {k: {'file': v[1], 'version': BONUS_VER[k], 'what': v[2], 'home': v[3], 'files': [v[1]],
                'bytes': len(packed[v[1]]), 'src': bonus_src[k]} for k, v in BONUS.items()},
  'bonus_checked': bonus_checked,
  'pack': os.path.basename(PACK),
  'loader': 'v2p',""")
b = rep(b, "t = open(os.path.join(HERE, 'loader_template_v2o.html'), encoding='utf-8').read()",
        "t = open(os.path.join(HERE, 'loader_template_v2p.html'), encoding='utf-8').read()")
b = rep(b, "'</head>\\n<body>\\n<!-- Written by build_loader_v2o.py: sends", "'</head>\\n<body>\\n<!-- Written by build_loader_v2p.py: sends")
b = rep(b, """print(f'checked files: {sum(checked.values())} of {len(checked)}' + ('' if all(checked.values()) else""",
        """print('bonus: ' + ', '.join('%s %s (%s, %d characters by the cable)' % (k, BONUS_VER[k], 'checked' if bonus_checked[k] else
      'NOT checked', bonus_len[k]) for k in BONUS))
print(f'checked files: {sum(checked.values())} of {len(checked)}' + ('' if all(checked.values()) else""")
# a comment: the starter pack's builder is v5 now (v4 leaves tools/ with this change), and it compares the same way
b = rep(b, "make_starter_pack_v4.py compares the same way", "make_starter_pack_v5.py compares the same way")
io.open(P + 'build_loader_v2p.py', 'w', encoding='utf-8').write(b)

# ------------------------------------------------------------------ the page
t = load('loader_template_v2o.html')
t = rep(t, "/* PrimeLoader v2o (23 Nov 2026).",
        "/* PrimeLoader v2p (26 Nov 2026).  v2o's page with the bonus: under \"More choices\", a box for Sudoku, the book's\n"
        "   just-for-fun program (Appendix G), from starter pack v26's folder \"Bonus (optional)\".  Ticked, it goes with whatever\n"
        "   else is chosen (by the cable as a program goes, its source verified; on the Virtual Calculator as a file); it is in\n"
        "   no Sample and not in the Population, and the page never takes it off a calculator.  The summary under step 2 names\n"
        "   it, and the log's \"Chosen:\" line too.  Every other word and step is v2o's. */\n"
        "/* PrimeLoader v2o (23 Nov 2026).")
t = rep(t, "      <summary>More choices: single programs, and data</summary>",
        "      <summary>More choices: single programs, data, and the bonus</summary>")
t = rep(t, """          <p class="why" style="margin-top:6px">Use this only if your instructor gave you a data file, or you made one with the <a href="__DATALOADER_URL__">Data Loader</a>. Its name must be M0.hpmat to M9.hpmat.</p>
        </div>
      </div>
    </details>""", """          <p class="why" style="margin-top:6px">Use this only if your instructor gave you a data file, or you made one with the <a href="__DATALOADER_URL__">Data Loader</a>. Its name must be M0.hpmat to M9.hpmat.</p>
        </div>
        <div id="bonuslist"></div>
      </div>
    </details>""")
t = rep(t, """const NAMES = Object.keys(CAT.programs).sort((a, b) => a.localeCompare(b));""",
        """const NAMES = Object.keys(CAT.programs).sort((a, b) => a.localeCompare(b));
// v2p: the bonus (Sudoku): not one of the Statisticles, so not in NAMES (the Population, the Samples, the ticked list, or
// the names the page may take off a calculator); it goes only when its own box is ticked.
const BONUS = CAT.bonus || {};
const PROGS = Object.assign({}, CAT.programs, BONUS);                      // every program the page can send
const CHECKED = Object.assign({}, CAT.checked, CAT.bonus_checked || {});
function bonusChosen() { return Object.keys(BONUS).filter(k => $('b_' + k) && $('b_' + k).checked); }""")
t = rep(t, """  const s = new Set(chosen());
  if (dataNeedsProg()) s.add(DATAPROG);
  return NAMES.filter(p => s.has(p));""", """  const s = new Set(chosen());
  if (dataNeedsProg()) s.add(DATAPROG);
  return NAMES.filter(p => s.has(p)).concat(bonusChosen());""")
# the sending code looks every chosen name up in PROGS (the bonus with the Statisticles)
for old, new in [("const cableProgs = sel.filter(p => CAT.programs[p].src), cableRest = sel.filter(p => !CAT.programs[p].src)",
                  "const cableProgs = sel.filter(p => PROGS[p].src), cableRest = sel.filter(p => !PROGS[p].src)"),
                 ("const names = sel.filter(p => CAT.programs[p].src), rest = sel.filter(p => !CAT.programs[p].src)",
                  "const names = sel.filter(p => PROGS[p].src), rest = sel.filter(p => !PROGS[p].src)"),
                 ("for (const p of sel) for (const f of CAT.programs[p].files) files.push({ path: f, data: pf.get(f) });",
                  "for (const p of sel) for (const f of PROGS[p].files) files.push({ path: f, data: pf.get(f) });"),
                 ("for (const p of selection()) for (const f of CAT.programs[p].files) files.push({ name: f, data: pf.get(f) });",
                  "for (const p of selection()) for (const f of PROGS[p].files) files.push({ name: f, data: pf.get(f) });"),
                 ("const p = CAT.programs[name], b = pf.get(p.files[0]);", "const p = PROGS[name], b = pf.get(p.files[0]);")]:
    t = rep(t, old, new)
t = rep(t, "const progs = sel.filter(p => CAT.programs[p].home);", "const progs = sel.filter(p => PROGS[p].home);", 2)
t = rep(t, "if (!progs.every(p => CAT.checked[p]))", "if (!progs.every(p => CHECKED[p]))")
t = rep(t, "const ready = progs.every(p => CAT.checked[p]);", "const ready = progs.every(p => CHECKED[p]);")
# the summary under step 2
t = rep(t, """  const sel = selection(), base = chosen(), data = dataChosen(), auto = dataNeedsProg(), c = chapter(), real = state.target === 'real';""",
        """  const sel = selection(), base = chosen(), data = dataChosen(), auto = dataNeedsProg(), c = chapter(), real = state.target === 'real';
  const bon = bonusChosen();               // v2p""")
t = rep(t, "  if (!h && !data.length) h = state.what === 'chapter'", "  if (!h && !data.length && !bon.length) h = state.what === 'chapter'")
t = rep(t, """    if (!h) h = 'No program chosen';
    if (data.length) h += ', and the data <b>' + dnames + '</b>';
    h += '.';""", """    if (!h) h = bon.length && !data.length ? '' : 'No program chosen';
    if (data.length) h += ', and the data <b>' + dnames + '</b>';
    if (bon.length) h += (h ? ', and ' : '') + '<b>' + esc(bon.join(', ')) + '</b>, the bonus';
    h += '.';""")
io.open(P + 'loader_template_v2p.html', 'w', encoding='utf-8').write(t)
print('ok', len(b), len(t))

# ------------------------------------------------------------------ the bonus's box, and the log's "Chosen:" line
t = load('loader_template_v2p.html')
t = rep(t, """buildList();
$('rossiwhat').textContent = CAT.data.rossi.what;""", """buildList();
for (const k of Object.keys(BONUS)) {          // v2p: one box for each bonus program, under the data in "More choices"
  const row = document.createElement('div'); row.className = 'datarow'; row.style.marginTop = '12px';
  const l = document.createElement('label'), cb = document.createElement('input'), sp = document.createElement('span');
  cb.type = 'checkbox'; cb.id = 'b_' + k; cb.addEventListener('change', refresh);
  sp.innerHTML = 'Add <b>' + esc(k) + '</b>, just for fun: ' + esc(BONUS[k].what) + '.';
  l.appendChild(cb); l.appendChild(document.createTextNode(' ')); l.appendChild(sp); row.appendChild(l);
  const p = document.createElement('p'); p.className = 'why'; p.style.marginTop = '4px';
  p.innerHTML = esc(k) + ' is a bonus, and not one of the <i>Statisticles</i>, so it goes onto the calculator only when this box is ticked, together with whatever else you choose, and this page never takes it off a calculator.';
  row.appendChild(p); $('bonuslist').appendChild(row);
}
$('rossiwhat').textContent = CAT.data.rossi.what;""")
t = rep(t, """state.what === 'group' ? group().title : 'programs ticked one by one') + '; ' + plural(programs.length, 'program')""",
        """state.what === 'group' ? group().title : 'programs ticked one by one') + (bonusChosen().length ? ', and the bonus ' + bonusChosen().join(', ') : '') + '; ' + plural(programs.length, 'program')""")
io.open(P + 'loader_template_v2p.html', 'w', encoding='utf-8').write(t)
print('ok: the bonus box and the log line')
