#!/usr/bin/env python3
"""make_v2s.py -- round 21 (28 Nov 2026): the Prime Loader v2s, v2r's page built from starter pack v29, whose TTestLab
beta 1n and TTestLabG beta 1k work every number of steps 2 and 4 out from the numbers shown before it, so that each step
checks on a calculator (the book's read-through of its Draft 127, item A10).

Makes, by exact replacements (each one asserted, so a file that has changed stops the run):
  prime-loader/build_loader_v2s.py           v2r's, with a v2s paragraph in its description and the new names
  prime-loader/loader_template_v2s.html      v2r's, with a first comment for v2s; no other change
  prime-loader/tests/test_loader_v2s.js      v2r's, with the new names and the cable's counted numbers for pack v29
and deletes the v2r files that these replace (git keeps them).  Then:
  python3 prime-loader/build_loader_v2s.py starter-pack/HP_Prime_Statistics_Starter_Pack_v29.zip --kit KIT
  node prime-loader/tests/test_loader_v2s.js prime-loader/PrimeLoader_v2s.html starter-pack/..._v29.zip
Run from the repository's top folder:  python3 verify/round21/make_v2s.py"""
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
        raise SystemExit('make_v2s: %s: the old text stands %d times, not %d' % (where, c, n))
    return s.replace(a, b)


# ---- the build ----
s = rd('prime-loader/build_loader_v2r.py')
s = rep(s, '"""build_loader_v2r.py -- assembles PrimeLoader_v2r.html:', '"""build_loader_v2s.py -- assembles PrimeLoader_v2s.html:', 'build name')
s = rep(s, '    python3 build_loader_v2r.py PACK.zip [OUT.html] [--kit PATH]\n',
        '    python3 build_loader_v2s.py PACK.zip [OUT.html] [--kit PATH]\n'
        'v2s (28 Nov 2026, round 21): v2r\'s page, word for word, built from starter pack v29, whose TTestLab beta 1n and\n'
        'TTestLabG beta 1k work every number of steps 2 and 4 out from the numbers shown before it, so that each step checks\n'
        'on a calculator (the book\'s read-through of its Draft 127, item A10; verify/round21/make_v2s.py).\n', 'build usage and v2s')
s = rep(s, "os.path.join(HERE, 'PrimeLoader_v2r.html')", "os.path.join(HERE, 'PrimeLoader_v2s.html')", 'build out')
s = rep(s, "  'loader': 'v2r',", "  'loader': 'v2s',", 'build version')
s = rep(s, "'loader_template_v2r.html'", "'loader_template_v2s.html'", 'build template')
s = rep(s, '<!-- Written by build_loader_v2r.py:', '<!-- Written by build_loader_v2s.py:', 'build index note')
assert 'v2r' not in s.split('v2r (27 Nov 2026, round 20)')[0].replace('v2r\'s', ''), 'a v2r name is left in the build'
wr('prime-loader/build_loader_v2s.py', s)
os.remove('prime-loader/build_loader_v2r.py')

# ---- the template ----
s = rd('prime-loader/loader_template_v2r.html')
s = rep(s, '/* PrimeLoader v2r (27 Nov 2026, round 20).',
        '/* PrimeLoader v2s (28 Nov 2026, round 21).  v2r\'s page, word for word, built from starter pack v29 (TTestLab beta 1n\n'
        '   and TTestLabG beta 1k). */\n'
        '/* PrimeLoader v2r (27 Nov 2026, round 20).', 'template note')
wr('prime-loader/loader_template_v2s.html', s)
os.remove('prime-loader/loader_template_v2r.html')

# ---- the test ----
s = rd('prime-loader/tests/test_loader_v2r.js')
s = rep(s, '// test_loader_v2r.js -- drives PrimeLoader_v2r.html in Chromium', '// test_loader_v2s.js -- drives PrimeLoader_v2s.html in Chromium', 'test name')
s = rep(s, 'node tests/test_loader_v2r.js PrimeLoader_v2r.html PACK.zip\n//\n',
        'node tests/test_loader_v2s.js PrimeLoader_v2s.html PACK.zip\n//\n'
        '// v2s (28 Nov 2026, round 21): test_loader_v2r.js with the page\'s new name and starter pack v29.  Every check is v2r\'s;\n'
        '// the counted numbers of the cable are new, because TTestLab beta 1n is 13,016 characters longer than beta 1m and\n'
        '// TTestLabG beta 1k 12,688 longer than beta 1j: the 30 programs that travel by cable are CHARS30 characters,\n'
        '// G1R30 reports of a G1 and G2R30 of a G2 (README, v2s).\n',
        'test usage and v2s')
s = rep(s, 'PrimeLoader_v2r\\.html\\?data=1$', 'PrimeLoader_v2s\\.html\\?data=1$', 'test data link')
s = rep(s, 'url=PrimeLoader_v2r\\.html"', 'url=PrimeLoader_v2s\\.html"', 'test noscript')
s = rep(s, '/^HP Prime Loader, v2r, straight down the cable\\. /', '/^HP Prime Loader, v2s, straight down the cable\\. /', 'test log')
s = rep(s, "the 30 programs that travel by cable are 4,065,308 characters, which would be 129,089 reports of a G1 and 7,962 of a G2;",
        "the 30 programs that travel by cable are CHARS30 characters, which would be G1R30 reports of a G1 and G2R30 of a G2;", 'test counted words')
s = rep(s, "chars30 === 4065308 && reportsOf(names30, 55, 63) === 129089 && reportsOf(names30, 1015, 1023) === 7962",
        "chars30 === C30 && reportsOf(names30, 55, 63) === R1 && reportsOf(names30, 1015, 1023) === R2", 'test counted numbers')
# the numbers, counted from pack v29 (TTestLab +13,016, TTestLabG +12,688 characters)
C30, R1, R2 = 4091012, 129905, 8012
s = (s.replace('CHARS30', '{:,}'.format(C30)).replace('G1R30', '{:,}'.format(R1)).replace('G2R30', '{:,}'.format(R2))
      .replace('=== C30 ', '=== %d ' % C30).replace('=== R1 ', '=== %d ' % R1).replace('=== R2 ', '=== %d ' % R2))
wr('prime-loader/tests/test_loader_v2s.js', s)
os.remove('prime-loader/tests/test_loader_v2r.js')
if os.path.exists('prime-loader/tests/test_loader_v2r_output.txt'):
    os.remove('prime-loader/tests/test_loader_v2r_output.txt')
print('make_v2s: wrote build_loader_v2s.py, loader_template_v2s.html, tests/test_loader_v2s.js; removed their v2r files')
