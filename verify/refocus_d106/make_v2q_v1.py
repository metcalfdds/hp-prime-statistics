#!/usr/bin/env python3
"""make_v2q_v1.py -- the book's Draft 106 (the refocus, 26 Nov 2026) has no Appendix G, so nothing here may send a
reader there.  Roger, 26 Nov 2026, 18:27, of the book: "I think we need to delete a lot of content"; Draft 105's
Appendix G ("Just for fun: Sudoku, and the statistics hiding in it") went to the book's website archive, and Sudoku
stays a bonus on the Loader (his plan, step 7).

Makes, from the files of PR 35 by exact replacements (each one asserted, so a file that has changed stops the run):
  tools/make_starter_pack_v6.py              v5 without "The book tells about it in Appendix G, ..." in the
                                             instructions (and its own name, and the next pack's number, v28)
  starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip
                                             v26 with READ_ME_FIRST.txt changed in those words and in its first
                                             line (v27); every other file is v26's, byte for byte, with v26's
                                             names, dates and order, so every program is the one v26 tested
  starter-pack/README.md                     v26's page with the same changes (the page v6 would write for v27)
  prime-loader/build_loader_v2q.py           v2p with the bonus's words "a Sudoku puzzle game that keeps a record
                                             of the games you finish" (v2p: "a Sudoku puzzle game, the book's
                                             Appendix G"), and the new names
  prime-loader/loader_template_v2q.html      v2p's, with a first comment for v2q; no other change
  prime-loader/tests/test_loader_v2q.js      v2p's, with the new names and the box's new words
and deletes the v2p, v26 and v5 files that these replace (git keeps them).  Then, by hand (the README beside this):
  python3 prime-loader/build_loader_v2q.py starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip --kit KIT
  node prime-loader/tests/test_loader_v2q.js prime-loader/PrimeLoader_v2q.html starter-pack/..._v27.zip
Run from the repository's top folder:  python3 verify/refocus_d106/make_v2q_v1.py"""
import io, os, sys, zipfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(REPO)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new, n=1, where=''):
    assert s.count(old) == n, (where, s.count(old), old[:100])
    return s.replace(old, new)


SENT = ' The book tells about it in Appendix G, "Just for fun: Sudoku, and the statistics hiding in it".'
WHAT_OLD = "a Sudoku puzzle game, the book's Appendix G"
WHAT_NEW = 'a Sudoku puzzle game that keeps a record of the games you finish'

# ---- 1. the pack tool, v6 --------------------------------------------------------------------------------------
s = rd('tools/make_starter_pack_v5.py')
s = rep(s, '"""make_starter_pack_v5.py -- builds', '"""make_starter_pack_v6.py -- builds', where='tool name')
s = rep(s, '\nv5 (26 Nov 2026): THE BONUS.',
        '\nv6 (26 Nov 2026, evening): NO APPENDIX G.  The book\'s Draft 106 (the refocus) has no Appendix G: Draft 105\'s "Just for\n'
        'fun: Sudoku, and the statistics hiding in it" went to the book\'s website archive.  So the instructions no longer send\n'
        'the reader there; nothing else is different.  Pack v27 was made from v26 by that one change\n'
        '(verify/refocus_d106/make_v2q_v1.py), not built again, because every program file in it is v26\'s, byte for byte.\n'
        '\nv5 (26 Nov 2026): THE BONUS.', where='tool v6 note')
s = rep(s, "' folder too if you want it, in the same way (calculator closed). The book tells about it in Appendix G,'\n"
           "            ' \"Just for fun: Sudoku, and the statistics hiding in it\".' % (",
        "' folder too if you want it, in the same way (calculator closed).' % (", where='tool sentence')
s = rep(s, 'python3 tools/make_starter_pack_v5.py VER', 'python3 tools/make_starter_pack_v6.py VER', where='tool usage')
s = rep(s, 'Built by `tools/make_starter_pack_v5.py`', 'Built by `tools/make_starter_pack_v6.py`', where='tool page line')
s = rep(s, '`python3 tools/make_starter_pack_v5.py v27 --kit', '`python3 tools/make_starter_pack_v6.py v28 --kit', where='tool next')
wr('tools/make_starter_pack_v6.py', s)
os.remove('tools/make_starter_pack_v5.py')

# ---- 2. the pack, v27 from v26 --------------------------------------------------------------------------------------
OLDZ = 'starter-pack/HP_Prime_Statistics_Starter_Pack_v26.zip'
NEWZ = 'starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip'
zin = zipfile.ZipFile(OLDZ)
with zipfile.ZipFile(NEWZ, 'w') as zout:
    changed = 0
    for info in zin.infolist():
        data = zin.read(info.filename)
        if info.filename == 'READ_ME_FIRST.txt':
            t = data.decode('utf-8')
            t = rep(t, 'HP PRIME STATISTICS STARTER PACK v26 (2026-11-26)', 'HP PRIME STATISTICS STARTER PACK v27 (2026-11-26)',
                    where='pack first line')
            t = rep(t, SENT, '', where='pack sentence')
            assert 'Appendix' not in t and 'v26' not in t
            data = t.encode('utf-8'); changed += 1
        zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
        zi.compress_type = info.compress_type; zi.external_attr = info.external_attr; zi.create_system = info.create_system
        zout.writestr(zi, data)
    assert changed == 1
os.remove(OLDZ)
# read back: every file but the read-me is v26's, byte for byte (the deleted v26 is still in git; compare with it there)
import subprocess
old = zipfile.ZipFile(io.BytesIO(subprocess.run(['git', 'show', 'HEAD:' + OLDZ], check=True, capture_output=True).stdout))
new = zipfile.ZipFile(NEWZ)
assert [i.filename for i in old.infolist()] == [i.filename for i in new.infolist()]
for i in old.infolist():
    if i.filename != 'READ_ME_FIRST.txt':
        assert old.read(i.filename) == new.read(i.filename), i.filename
print('pack v27: %d files, %d bytes; READ_ME_FIRST.txt changed, the other %d the same as v26\'s'
      % (len(new.infolist()), os.path.getsize(NEWZ), len(new.infolist()) - 1))

# ---- 3. the pack's page ---------------------------------------------------------------------------------------------
s = rd('starter-pack/README.md')
s = rep(s, '*v26, 2026-11-26. Built by `tools/make_starter_pack_v5.py`', '*v27, 2026-11-26. Built by `tools/make_starter_pack_v6.py`',
        where='page head')
n = s.count('HP_Prime_Statistics_Starter_Pack_v26.zip'); assert n >= 1
s = s.replace('HP_Prime_Statistics_Starter_Pack_v26.zip', 'HP_Prime_Statistics_Starter_Pack_v27.zip')
s = rep(s, SENT, '', where='page sentence')
s = rep(s, '`python3 tools/make_starter_pack_v5.py v27 --kit', '`python3 tools/make_starter_pack_v6.py v28 --kit', where='page next')
s = rep(s, '[docs/changes/StarterPack_v26_NOTES.md](../docs/changes/StarterPack_v26_NOTES.md)',
        '[docs/changes/StarterPack_v27_NOTES.md](../docs/changes/StarterPack_v27_NOTES.md)', where='page notes')
assert 'Appendix G' not in s
wr('starter-pack/README.md', s)

# ---- 4. the Loader's build, v2q ---------------------------------------------------------------------------------------
s = rd('prime-loader/build_loader_v2p.py')
s = rep(s, '"""build_loader_v2p.py -- assembles PrimeLoader_v2p.html:', '"""build_loader_v2q.py -- assembles PrimeLoader_v2q.html:', where='build name')
s = rep(s, '    python3 build_loader_v2p.py PACK.zip [OUT.html] [--kit PATH]\n',
        '    python3 build_loader_v2q.py PACK.zip [OUT.html] [--kit PATH]\n'
        'v2q (26 Nov 2026, evening): no Appendix G.  The book\'s Draft 106 (the refocus) has no Appendix G, so the bonus\'s box\n'
        'says what Sudoku is, "a Sudoku puzzle game that keeps a record of the games you finish" (v2p: "a Sudoku puzzle game,\n'
        'the book\'s Appendix G"), and the page is built from starter pack v27, whose read-me drops the same words.  Every\n'
        'other word and step is v2p\'s (verify/refocus_d106/make_v2q_v1.py).\n', where='build usage')
s = rep(s, "os.path.join(HERE, 'PrimeLoader_v2p.html')", "os.path.join(HERE, 'PrimeLoader_v2q.html')", where='build out')
s = rep(s, "'Sudoku.hpprgm', '" + WHAT_OLD.replace("'", "\\'") + "', 'Sudoku',", "'Sudoku.hpprgm', '" + WHAT_NEW + "', 'Sudoku',", where='build what')
s = rep(s, "'loader': 'v2p',", "'loader': 'v2q',", where='build loader')
s = rep(s, "'loader_template_v2p.html'", "'loader_template_v2q.html'", where='build template')
s = rep(s, '<!-- Written by build_loader_v2p.py:', '<!-- Written by build_loader_v2q.py:', where='build index')
s = rep(s, 'make_starter_pack_v5.py compares the same way', 'make_starter_pack_v6.py compares the same way', where='build comment')
wr('prime-loader/build_loader_v2q.py', s)
os.remove('prime-loader/build_loader_v2p.py')

# ---- 5. the page's template, v2q ---------------------------------------------------------------------------------
s = rd('prime-loader/loader_template_v2p.html')
s = rep(s, '/* PrimeLoader v2p (26 Nov 2026).',
        '/* PrimeLoader v2q (26 Nov 2026, evening).  v2p\'s page with one change: the bonus\'s box no longer says that Sudoku\n'
        '   is the book\'s Appendix G (the book\'s Draft 106 has none); it says what Sudoku is.  Built from starter pack v27,\n'
        '   whose read-me drops the same words.  Every other word and step is v2p\'s. */\n'
        '/* PrimeLoader v2p (26 Nov 2026).', where='template note')
wr('prime-loader/loader_template_v2q.html', s)
os.remove('prime-loader/loader_template_v2p.html')

# ---- 6. the test, v2q -------------------------------------------------------------------------------------------
s = rd('prime-loader/tests/test_loader_v2p.js')
s = rep(s, '// test_loader_v2p.js -- drives PrimeLoader_v2p.html in Chromium', '// test_loader_v2q.js -- drives PrimeLoader_v2q.html in Chromium', where='test name')
s = rep(s, 'node tests/test_loader_v2p.js PrimeLoader_v2p.html PACK.zip\n//\n',
        'node tests/test_loader_v2q.js PrimeLoader_v2q.html PACK.zip\n//\n'
        '// v2q (26 Nov 2026, evening): test_loader_v2p.js with the page\'s new name, starter pack v27, and the bonus\'s box in\n'
        '// its new words (the book\'s Draft 106 has no Appendix G).  Every check is v2p\'s.\n//\n', where='test usage')
s = rep(s, '/PrimeLoader_v2p\\.html\\?data=1$/', '/PrimeLoader_v2q\\.html\\?data=1$/', where='test data link')
s = rep(s, 'content="0; url=PrimeLoader_v2p\\.html"><\\/noscript>/', 'content="0; url=PrimeLoader_v2q\\.html"><\\/noscript>/', where='test noscript')
s = rep(s, '/^HP Prime Loader, v2p, straight down the cable\\. /', '/^HP Prime Loader, v2q, straight down the cable\\. /', where='test log')
s = rep(s, "a Sudoku puzzle game, the book's Appendix G\\.", 'a Sudoku puzzle game that keeps a record of the games you finish\\.', where='test box')
wr('prime-loader/tests/test_loader_v2q.js', s)
os.remove('prime-loader/tests/test_loader_v2p.js')
os.remove('prime-loader/tests/test_loader_v2p_output.txt')
os.remove('prime-loader/PrimeLoader_v2p.html')
print('made: tools/make_starter_pack_v6.py, %s, starter-pack/README.md, prime-loader/build_loader_v2q.py, '
      'loader_template_v2q.html, tests/test_loader_v2q.js; removed their v5, v26 and v2p files' % NEWZ)
