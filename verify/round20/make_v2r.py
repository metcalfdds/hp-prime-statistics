#!/usr/bin/env python3
"""make_v2r.py -- round 20 (27 Nov 2026): the Prime Loader v2r, v2q's page built from starter pack v28, whose DataLoad
is beta 1i (blank cells inside paired columns: it asks whether the columns are pairs or separate groups).  The Data
Loader's link in the page is the newest data-loader/DataLoader_v*.html, which the build finds by itself (now v7).

Makes, by exact replacements (each one asserted, so a file that has changed stops the run):
  prime-loader/build_loader_v2r.py           v2q's, with a v2r paragraph in its description and the new names
  prime-loader/loader_template_v2r.html      v2q's, with a first comment for v2r; no other change
  prime-loader/tests/test_loader_v2r.js      v2q's, with the new names; every check is v2q's
and deletes the v2q files that these replace (git keeps them).  Then:
  python3 prime-loader/build_loader_v2r.py starter-pack/HP_Prime_Statistics_Starter_Pack_v28.zip --kit KIT
  node prime-loader/tests/test_loader_v2r.js prime-loader/PrimeLoader_v2r.html starter-pack/..._v28.zip
Run from the repository's top folder:  python3 verify/round20/make_v2r.py"""
import io, os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(REPO)


def rd(p):
    return io.open(p, encoding='utf-8', newline='').read()


def wr(p, s):
    io.open(p, 'w', encoding='utf-8', newline='').write(s)


def rep(s, a, b, where, n=1):
    c = s.count(a)
    if c != n:
        raise SystemExit('make_v2r: %s: the old text stands %d times, not %d' % (where, c, n))
    return s.replace(a, b)


# ---- the build ----
s = rd('prime-loader/build_loader_v2q.py')
s = rep(s, '"""build_loader_v2q.py -- assembles PrimeLoader_v2q.html:', '"""build_loader_v2r.py -- assembles PrimeLoader_v2r.html:', 'build name')
s = rep(s, '    python3 build_loader_v2q.py PACK.zip [OUT.html] [--kit PATH]\n',
        '    python3 build_loader_v2r.py PACK.zip [OUT.html] [--kit PATH]\n'
        'v2r (27 Nov 2026, round 20): v2q\'s page, word for word, built from starter pack v28, whose DataLoad beta 1i asks\n'
        'whether the columns are pairs or separate groups when it loads two or more columns and a blank cell stands above a\n'
        'value in any of them (beta 1h left each blank out of its own column, and paired columns slid out of step).  The\n'
        'Data Loader\'s link is its v7 page, found by the build as before (verify/round20/make_v2r.py).\n', 'build usage and v2r')
s = rep(s, "os.path.join(HERE, 'PrimeLoader_v2q.html')", "os.path.join(HERE, 'PrimeLoader_v2r.html')", 'build out')
s = rep(s, "  'loader': 'v2q',", "  'loader': 'v2r',", 'build version')
s = rep(s, "'loader_template_v2q.html'", "'loader_template_v2r.html'", 'build template')
s = rep(s, '<!-- Written by build_loader_v2q.py:', '<!-- Written by build_loader_v2r.py:', 'build index note')
assert 'v2q' not in s.split('v2q (26 Nov 2026, evening)')[0].replace('v2q\'s', ''), 'a v2q name is left in the build'
wr('prime-loader/build_loader_v2r.py', s)
os.remove('prime-loader/build_loader_v2q.py')

# ---- the template ----
s = rd('prime-loader/loader_template_v2q.html')
s = rep(s, '/* PrimeLoader v2q (26 Nov 2026, evening).',
        '/* PrimeLoader v2r (27 Nov 2026, round 20).  v2q\'s page, word for word, built from starter pack v28 (DataLoad beta 1i);\n'
        '   the Data Loader\'s link is its v7 page. */\n'
        '/* PrimeLoader v2q (26 Nov 2026, evening).', 'template note')
wr('prime-loader/loader_template_v2r.html', s)
os.remove('prime-loader/loader_template_v2q.html')

# ---- the test ----
s = rd('prime-loader/tests/test_loader_v2q.js')
s = rep(s, '// test_loader_v2q.js -- drives PrimeLoader_v2q.html in Chromium', '// test_loader_v2r.js -- drives PrimeLoader_v2r.html in Chromium', 'test name')
s = rep(s, 'node tests/test_loader_v2q.js PrimeLoader_v2q.html PACK.zip\n//\n',
        'node tests/test_loader_v2r.js PrimeLoader_v2r.html PACK.zip\n//\n'
        '// v2r (27 Nov 2026, round 20): test_loader_v2q.js with the page\'s new name and starter pack v28.  Every check is v2q\'s.\n',
        'test usage and v2r')
s = rep(s, 'PrimeLoader_v2q\\.html\\?data=1$', 'PrimeLoader_v2r\\.html\\?data=1$', 'test data link')
s = rep(s, 'url=PrimeLoader_v2q\\.html"', 'url=PrimeLoader_v2r\\.html"', 'test noscript')
s = rep(s, '/^HP Prime Loader, v2q, straight down the cable\\. /', '/^HP Prime Loader, v2r, straight down the cable\\. /', 'test log')
wr('prime-loader/tests/test_loader_v2r.js', s)
os.remove('prime-loader/tests/test_loader_v2q.js')
if os.path.exists('prime-loader/tests/test_loader_v2q_output.txt'):
    os.remove('prime-loader/tests/test_loader_v2q_output.txt')
print('make_v2r: wrote build_loader_v2r.py, loader_template_v2r.html, tests/test_loader_v2r.js; removed their v2q files')
