#!/usr/bin/env python3
"""docs_d106_v1.py -- the repository's pages after the book's Draft 106 (the refocus, 26 Nov 2026), by exact replacements:
no page names the book's Appendix G (it went to the book's website archive), the current pack is v27 and the current
Loader v2q (make_v2q_v1.py), and Draft 105's Appendix F, "For HP programmers", has a home in docs/book/ (Roger, 26 Nov
2026, 18:31: "The programming part can go to GitHub and a future website").  Run after make_v2q_v1.py, the Loader's
build and its test, from the repository's top folder:  python3 verify/refocus_d106/docs_d106_v1.py"""
import io, os, re

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(REPO)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, old, new, n=1, where=''):
    assert s.count(old) == n, (where, s.count(old), old[:100])
    return s.replace(old, new)


out = rd('prime-loader/tests/test_loader_v2q_output.txt')
m = re.search(r'\n(\d+) PASS, (\d+) FAIL\n', out)
assert m and m.group(2) == '0' and out.rstrip().endswith('exit 0'), 'the Loader test has not passed'
NPASS = int(m.group(1))
a = rd('tools/pages_a11y_v1_output.txt')                 # node tools/pages_a11y_v1.js > tools/pages_a11y_v1_output.txt
ma = re.search(r'\n(\d+) PASS, (\d+) FAIL', a)
assert 'PrimeLoader_v2q.html' in a and ma and ma.group(2) == '0', 'the accessibility check has not passed on v2q'
NA11Y = int(ma.group(1))

# ---- README.md ------------------------------------------------------------------------------------------------
s = rd('README.md')
s = rep(s, 'starter-pack/HP_Prime_Statistics_Starter_Pack_v26.zip)', 'starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip)', where='README pack')
s = rep(s, "the book's bonus, just for fun (its Appendix G), a Sudoku puzzle game", "the book's bonus, just for fun, a Sudoku puzzle game", where='README bonus')
s = rep(s, "built properly, by `tools/make_starter_pack_v5.py`, and read back", "built properly, by `tools/make_starter_pack_v6.py`, and read back", where='README tool')
wr('README.md', s)

# ---- CLAUDE.md --------------------------------------------------------------------------------------------------
s = rd('CLAUDE.md')
s = rep(s, "Sudoku (`extras/sudoku/`, the book's Appendix G) is not one of the 31 *Statisticles*.",
        "Sudoku (`extras/sudoku/`) is not one of the 31 *Statisticles*. Since the book's Draft 106 (26 Nov 2026, the refocus) no "
        "appendix tells about it (Draft 105's Appendix G went to the book's website archive), so no page here may send a reader "
        "to one.", where='CLAUDE bonus')
s = rep(s, "(`BONUS` in `tools/make_starter_pack_v5.py`)", "(`BONUS` in `tools/make_starter_pack_v6.py`)", where='CLAUDE tool')
s = rep(s, "(`BONUS` in `prime-loader/build_loader_v2p.py`)", "(`BONUS` in `prime-loader/build_loader_v2q.py`)", where='CLAUDE build')
s = rep(s, '(`python3 tools/make_starter_pack_v5.py v27 --kit $HPKIT`)', '(`python3 tools/make_starter_pack_v6.py v28 --kit $HPKIT`)', where='CLAUDE pack')
s = rep(s, 'The build makes the groups (`build_loader_v2p.py`, `CHAPTER_GROUPS`', 'The build makes the groups (`build_loader_v2q.py`, `CHAPTER_GROUPS`', where='CLAUDE groups')
s = rep(s, 'Its test (`tests/test_loader_v2p.js`, about twelve minutes)', 'Its test (`tests/test_loader_v2q.js`, about twelve minutes)', where='CLAUDE test')
s = rep(s, 'is counted in `test_usb_core_v3d.js` (A18) or `test_loader_v2p.js`.', 'is counted in `test_usb_core_v3d.js` (A18) or `test_loader_v2q.js`.', where='CLAUDE count')
s = rep(s, "(`prime-loader/`, v2p since 26 Nov 2026, which is v2o's page",
        "(`prime-loader/`, v2q since 26 Nov 2026, evening, which is v2p's page with the bonus's box in new words, no Appendix G, "
        "built from starter pack v27; v2p, of 26 Nov, was v2o's page", where='CLAUDE loader')
wr('CLAUDE.md', s)

# ---- extras -------------------------------------------------------------------------------------------------------
s = rd('extras/README.md')
s = rep(s, "for a class experiment on whether fewer clues take longer (the book's Appendix G).",
        "for a class experiment on whether fewer clues take longer.", where='extras')
wr('extras/README.md', s)
s = rd('extras/sudoku/README.md')
s = rep(s, "It is a bonus, just for fun, and not one of the 31 *Statisticles*: the book tells about it, and about the statistics "
           "hiding in a Sudoku, in Appendix G, \"Just for fun: Sudoku, and the statistics hiding in it\", and Appendix F tells how "
           "the program works inside.",
        "It is a bonus, just for fun, and not one of the 31 *Statisticles*. The book's Draft 105 told about it, and about the "
        "statistics hiding in a Sudoku, in its Appendix G, and how the program works inside in its Appendix F; since Draft 106 "
        "(26 November 2026, the refocus) the book has neither, and Draft 105's Appendix F is in this repository: "
        "[docs/book/](../../docs/book/), section \"How our Sudoku works inside\".", where='sudoku readme')
wr('extras/sudoku/README.md', s)

# ---- the Loader's README ----------------------------------------------------------------------------------------------
s = rd('prime-loader/README.md')
s = rep(s, '### What v2p adds (26 November 2026): the bonus\n',
        '### What v2q changes (26 November 2026, evening): no Appendix G\n\n'
        'The book\'s Draft 106 (the refocus, 26 November 2026) has no Appendix G: Draft 105\'s "Just for fun: Sudoku, and the '
        'statistics hiding in it" went to the book\'s website archive. So the bonus\'s box says what Sudoku is, "Add **Sudoku**, '
        'just for fun: a Sudoku puzzle game that keeps a record of the games you finish", where v2p said "a Sudoku puzzle game, '
        'the book\'s Appendix G", and the page is built from starter pack v27, whose READ_ME_FIRST.txt drops the same words '
        '(`docs/changes/StarterPack_v27_NOTES.md`). Every other word and step is v2p\'s, and every program file is v26\'s, byte '
        'for byte. Made from v2p by `verify/refocus_d106/make_v2q_v1.py`; `tests/test_loader_v2q.js` gave **%d PASS, 0 FAIL** in '
        'Chromium (`tests/test_loader_v2q_output.txt`), and `tools/pages_a11y_v1.js` %d PASS, 0 FAIL. Not sent to a calculator.\n\n'
        '### What v2p adds (26 November 2026): the bonus\n' % (NPASS, NA11Y), where='loader v2q section')
s = rep(s, 'The page is one file, `PrimeLoader_v2p.html`, and also works offline', 'The page is one file, `PrimeLoader_v2q.html`, and also works offline', where='loader top')
s = rep(s, '| `PrimeLoader_v2p.html` | The page, built: open this one.', '| `PrimeLoader_v2q.html` | The page, built: open this one.', where='loader files 1')
s = rep(s, '| `loader_template_v2p.html` | The page\'s source,', '| `loader_template_v2q.html` | The page\'s source,', where='loader files 2')
s = rep(s, '| `build_loader_v2p.py` | `python3 build_loader_v2p.py ../starter-pack/HP_Prime_Statistics_Starter_Pack_v26.zip',
        '| `build_loader_v2q.py` | `python3 build_loader_v2q.py ../starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip', where='loader files 3')
s = rep(s, '| `tests/test_loader_v2p.js` | The Chromium test: `node tests/test_loader_v2p.js PrimeLoader_v2p.html ../starter-pack/HP_Prime_Statistics_Starter_Pack_v26.zip`',
        '| `tests/test_loader_v2q.js` | The Chromium test: `node tests/test_loader_v2q.js PrimeLoader_v2q.html ../starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip`',
        where='loader files 4')
wr('prime-loader/README.md', s)
s = rd('prime-loader/usb/README.md')
s = rep(s, 'node ../tests/test_loader_v2p.js ../PrimeLoader_v2p.html ../../starter-pack/HP_Prime_Statistics_Starter_Pack_v26.zip',
        'node ../tests/test_loader_v2q.js ../PrimeLoader_v2q.html ../../starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip', where='usb')
wr('prime-loader/usb/README.md', s)

# ---- tools/README.md ----------------------------------------------------------------------------------------------
s = rd('tools/README.md')
s = rep(s, '| `make_starter_pack_v5.py` + `CentralLimit_app_base_v1.hpapp` | **The starter pack** (v5 of the tool, 26 November 2026: v4\'s, with the bonus;',
        '| `make_starter_pack_v6.py` + `CentralLimit_app_base_v1.hpapp` | **The starter pack** (v6 of the tool, 26 November 2026, evening: v5\'s, '
        'without the instructions\' pointer to the book\'s Appendix G, which the book\'s Draft 106 does not have, so pack v27 was made from v26 by '
        'that change alone, `verify/refocus_d106/make_v2q_v1.py`; v5, of 26 November 2026: v4\'s, with the bonus;', where='tools 1')
s = rep(s, '`python3 make_starter_pack_v5.py v27 --kit PATH --checked FOLDER` builds every program in `programs/` into `starter-pack/HP_Prime_Statistics_Starter_Pack_v27.zip`',
        '`python3 make_starter_pack_v6.py v28 --kit PATH --checked FOLDER` builds every program in `programs/` into `starter-pack/HP_Prime_Statistics_Starter_Pack_v28.zip`',
        where='tools 2')
wr('tools/README.md', s)

# ---- docs ------------------------------------------------------------------------------------------------------------
s = rd('docs/test-status.md')
s = rep(s, '**Test status, 26 November 2026.**\n',
        '**Test status, 26 November 2026 (evening).**\n\n'
        '- **26 November 2026, evening: no Appendix G; starter pack v27 and the Prime Loader v2q.** The book\'s Draft 106 (the '
        'refocus) has no Appendix G, so the pack\'s READ_ME_FIRST.txt and the Loader\'s bonus box no longer name one. Starter pack '
        'v27 is v26 byte for byte but for READ_ME_FIRST.txt (its first line and that sentence), so every program in it is the one '
        'v26 tested (`docs/changes/StarterPack_v27_NOTES.md`); the Prime Loader v2q, built from it, gave %d PASS, 0 FAIL in '
        'Chromium (`prime-loader/tests/test_loader_v2q_output.txt`), and the accessibility check of the pages %d PASS, 0 FAIL '
        '(`tools/pages_a11y_v1_output.txt`). Not sent to a calculator.\n\n'
        '**Test status, 26 November 2026.**\n' % (NPASS, NA11Y), where='test status')
wr('docs/test-status.md', s)
s = rd('docs/README.md')
s = rep(s, '| `test-status.md` |',
        '| `book/` | **From the book.** Draft 105\'s Appendix F, "For HP programmers", as Draft 105 printed it, with its references: '
        'in Draft 106 (26 Nov 2026, the refocus) it left the book for this repository and the book\'s future website. |\n'
        '| `test-status.md` |', where='docs readme')
wr('docs/README.md', s)
print('pages updated; the Loader test: %d PASS, 0 FAIL; the pages\' accessibility: %d PASS, 0 FAIL' % (NPASS, NA11Y))
