#!/usr/bin/env python3
"""build_loader_v1m.py -- assembles PrimeLoader_v1m.html: the page template, the loader's core, the Data Loader's core
(for its zip writer), the chapter list, and every program file from a starter pack, embedded so the page works offline.

    python3 build_loader_v1m.py PACK.zip [OUT.html] [--kit PATH]

v1m (7 Nov 2026, night): starter pack v15, with a 31st program, TDist3D beta 1 (Student's t as a surface turned
with a finger: every t curve at once, a red slice with its critical value and tail chance, a Curves view; offered
with Chapters 9 and 11), and BurrLab beta 1p (the Family map's border drawn as four lines, not a one-colour RECT_P
that filled it dark gray on the G1; deeper tints; the tail shades opaque).  The catalog names those versions and the
EVERYTHING card counts 31.  The page template is v1c's, unchanged.

v1l (5 Nov 2026): starter pack v14, whose 30 programs carry round 9: one header on every help page, "<Name> help
n/N: <Topic>", American spelling on screen, and "Roger D. Metcalf"; and round 10 of the same day: 19 of them
refuse a typed value that no real problem needs (a mean or x from -10,000 to 10,000; an SD, a df or a rate at most 1,000;
a typed sample size at most 10,000), with a sentence that gives the range.  The catalog names those versions.  The page
template is v1c's, unchanged.

v1k (4 Nov 2026, night): starter pack v13, whose 18 changed programs carry round 8: the monkey test's 1,000
runs on every program that had not had them (every form field a real number only; a D list holding a number of
more than 50 digits left out or refused with a sentence; AnovaLab's s and sigma0 from 1E-50 to 1E50; DataLoad's
SD that cannot overflow), and "t test" written "t-test" on every screen (AnovaLab, FitCheck, StudRange, PowerViz
v2.5o, TTestLab beta 1f, TTestLabG beta 1d, TestChooser beta 2e); and SeizureLab is now ExhibitLab.  The catalog
names those versions, says
"t-tests", Chapter 11 is "t-Tests: Two Samples" and Chapter 1 "Data, Sampling, and Study Design"
(the Oxford comma), as in the book.  The page template is v1c's, unchanged.

v1j (4 Nov 2026): starter pack v12, whose 5 changed programs carry round 7: TTestLab beta 1e and TTestLabG beta 1c
name the flowchart's go-ahead key Run, not OK (on the Prime's own screens OK closes the screen); EpiStats v1.7h
passes its first monkey test (every form field a real number only, sample sizes and incidence rates that cannot
underflow or overflow, layouts that fit) and names its own version; ChiTable beta 3i's party table is GSS 2000;
ErrorRate beta 1g's help says it has run on the Virtual Calculator.  The catalog names those versions.  The page
template is v1c's, unchanged.

v1i (2 Nov 2026, night): starter pack v11, whose 11 changed programs carry round 6: what a student types is
kept to sensible ranges, and refused with a sentence outside them (alpha from 0.001 to 0.2 everywhere; StudRange's
k, df and m; DNAMixLR's yes/no answers and allele names; EpiStats' and TrendTest's counts), and every menu item
fits its box; BurrLab beta 1l draws a y-axis on every plot page.  The catalog names those versions.  The page
template is v1c's, unchanged.

v1h (2 Nov 2026, night): starter pack v10, whose 30 programs carry round 5: every number of 1,000 or more on
the screen shows its commas (12,345.678; never after the decimal point, never in a year, never in text the CAS
reads), and AgreeLab and ResampLab draw d-bar.  The catalog names those versions.  The page template is v1c's,
unchanged.

v1g (2 Nov 2026): starter pack v9, whose PowerViz v2.5l, ScatterLab beta 2f, ChiTable beta 3f and GaltonBoard beta
3f carry the monkey test's fourth round (every form field takes a real number only; numbers the program cannot draw
are refused with a sentence; labels that never cut a number; GaltonBoard's board holds 5,000 balls).  The catalog
names those versions.  The page template is v1c's, unchanged.

v1f (1 Nov 2026, night): starter pack v8, whose CICatcher beta 2e, Norm3 v2.4d, NormExplorer beta 42e and StatDist
v2.7h carry the monkey test's third round (every form field takes a real number only; numbers the program cannot
draw are refused with a sentence; StatDist's limits family by family) and what testing them on the Virtual Calculator
found.  The catalog names those versions.  The page template is v1c's, unchanged.

v1e (1 Nov 2026, evening): starter pack v7, whose SampDist v2.3e and BayesTree beta 8f carry the monkey test's fixes
(every form field takes a real number only; numbers the program cannot draw or use are refused with a sentence) and
what testing them on the Virtual Calculator found.  The catalog names those versions.  The page template is v1c's,
unchanged.

v1d (1 Nov 2026): starter pack v6, whose TTestLab beta 1c and TTestLabG beta 1a carry the monkey test's fixes
(every form field takes a real number only; a number with more than 50 digits, or a typed N over 1,000,000, is
refused with a sentence).  The catalog names those versions.  The page template is v1c's, unchanged.

v1c (1 Nov 2026): the repository is published on GitHub Pages (SITE below), so the book can link to the page.  The
build also writes index.html beside the page, which sends a browser on to the current version: the fixed address
SITE + 'prime-loader/' always opens the newest page, and only this file changes when the version does.  The Data
Loader link is the web address of the newest data-loader/DataLoader_v*.html.

v1b (1 Nov 2026): the template's v1b (plain-language explanations at every step; Firefox and Safari get their own
route: one zip, named for the chapter, unpacked with Windows' Extract All into the calculator's folder; a "Something
not working?" section).  The build itself is v1a's.

v1a (1 Nov 2026): knows whether the pack's files are CHECKED (carry the Virtual Calculator's compiled block, so they
run with no Check: measured that morning, see starter-pack v5).  It finds each program's source record with
hp-prime-kit (--kit, else $HPKIT, else /tmp/kit/hp-prime-kit-HEAD) and calls a file checked when anything sits
between the 152-byte header and the source (the kit's has_compiled_block).  The page then tells students to tap a
program and Run, with the Check step only as a fallback.  A pack with any unchecked program keeps the Check step.

Roger Metcalf & Claude, 1 Nov 2026.  The chapters follow the Universal Companion Guide's Chapter Plan (its survey
table, 31 Oct 2026): for each chapter, the programs that exist now.  Chapters whose program is still to be written say
so.  The program files are taken byte for byte from the pack's "Copy these into Prime" folder and its sample matrix;
the build stops if any program the catalog names is missing from the pack, or if the pack holds one it does not name.
"""
import base64, io, json, os, sys, zipfile, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[1:]
KIT = os.environ.get('HPKIT', '/tmp/kit/hp-prime-kit-HEAD')
if '--kit' in argv:
    i = argv.index('--kit'); KIT = argv[i + 1]; del argv[i:i + 2]
PACK = argv[0]
OUT = argv[1] if len(argv) > 1 else os.path.join(HERE, 'PrimeLoader_v1m.html')
SITE = 'https://metcalfdds.github.io/hp-prime-statistics/'
sys.path.insert(0, KIT)
from hpkit import program as kitprog            # hp-prime-kit (MIT, JordiRigau/hp-prime-kit)

# name: (file or app folder, version, what it does in a student's words, the name to type in Home)
PROGRAMS = {
  'AgreeLab':     ('AgreeLab.hpprgm', 'beta 1f', 'Examiner agreement: kappa and its cousins', 'AgreeLab'),
  'AnovaLab':     ('AnovaLab.hpprgm', 'beta 1e', 'ANOVA: one-way and two-way, and tests for variances', 'AnovaLab'),
  'BayesTree':    ('BayesTree.hpprgm', 'beta 8i', 'Bayes as a tree of 1,000 people: slide the prevalence', 'BayesTree'),
  'BiNorm3D':     ('BiNorm3D.hpprgm', 'beta 1e', 'Correlation in 3-D: turn the bivariate normal with a finger', 'BiNorm3D'),
  'BurrLab':      ('BurrLab.hpprgm', 'beta 1p', 'A model for long right tails (Burr XII)', 'BurrLab'),
  'CICatcher':    ('CICatcher.hpprgm', 'beta 2h', 'Fifty confidence intervals: how many catch the truth?', 'CICatcher'),
  'CentralLimit': ('CentralLimit.hpappdir', 'beta 3f', 'The central limit theorem, one sample at a time (an app)', None),
  'ChiTable':     ('ChiTable.hpprgm', 'beta 3k', 'Chi-square for a two-way table: drag the bars', 'ChiTable'),
  'DNAMixLR':     ('DNAMixLR.hpprgm', 'beta 3i', 'Likelihood ratios for DNA mixtures', 'DNAMixLR'),
  'DataLoad':     ('DataLoad.hpprgm', 'beta 1e', 'Puts a data file into the Statistics lists, with box plots', 'DATALOAD'),
  'EpiStats':     ('EpiStats.hpprgm', 'v1.7j', 'Epidemiology: 2 x 2 tables, risk and odds', 'EpiStats'),
  'ErrorRate':    ('ErrorRate.hpprgm', 'beta 1i', 'Error rates from proficiency tests', 'ErrorRate'),
  'FitCheck':     ('FitCheck.hpprgm', 'beta 1e', 'Goodness of fit: does the data match the model?', 'FitCheck'),
  'GaltonBoard':  ('GaltonBoard.hpprgm', 'beta 3h', 'Pour balls through pegs: the binomial becomes normal', 'GaltonBoard'),
  'Norm3':        ('Norm3.hpprgm', 'v2.4f', 'Drag x and watch the normal area', 'Norm3'),
  'NormExplorer': ('NormExplorer.hpprgm', 'beta 42i', 'The normal curve: areas, z scores, your own data', 'NormExp'),
  'PowerViz':     ('PowerViz.hpprgm', 'v2.5q', 'Power: drag the curves and watch alpha, beta and power', 'POWERVIZ'),
  'RankLab':      ('RankLab.hpprgm', 'beta 1f', 'Rank tests: sign, Wilcoxon, Mann-Whitney, Kruskal-Wallis', 'RankLab'),
  'ResampLab':    ('ResampLab.hpprgm', 'beta 1g', 'Permutation tests and the bootstrap, drawn as they run', 'ResampLab'),
  'RiskLab':      ('RiskLab.hpprgm', 'beta 1e', 'Risk scores and ROC curves', 'RiskLab'),
  'SampDist':     ('SampDist.hpprgm', 'v2.3i', 'The sampling distribution of the mean', 'SampDist'),
  'ScatterLab':   ('ScatterLab.hpprgm', 'beta 2i', 'Build a scatterplot with your finger; fit the line', 'ScatterLab'),
  'ExhibitLab':   ('ExhibitLab.hpprgm', 'beta 1f', 'How many units of a drug seizure to test?', 'ExhibitLab'),
  'StatDist':     ('StatDist.hpprgm', 'v2.7k', '27 distributions, each a plot you can touch', 'StatDist'),
  'StudRange':    ('StudRange.hpprgm', 'beta 15l', "Tukey's q, the studentized range", 'StudRange'),
  'SurvLab':      ('SurvLab.hpprgm', 'beta 1e', 'Time to an event: survival curves', 'SurvLab'),
  'TDist3D':      ('TDist3D.hpprgm', 'beta 1', "Student's t as a surface: every t curve at once, turned with a finger", 'TDist3D'),
  'TTestLab':     ('TTestLab.hpprgm', 'beta 1h', 't-tests in five steps (the advanced version)', 'TTESTLAB'),
  'TTestLabG':    ('TTestLabG.hpprgm', 'beta 1f', 't-tests in five steps', 'TTESTLABG'),
  'TestChooser':  ('TestChooser.hpprgm', 'beta 2f', 'Which test? A flowchart you tap', 'TestChooser'),
  'TrendTest':    ('TrendTest.hpprgm', 'beta 3l', 'Chi-square for a trend', 'TrendTest'),
}

# The book's chapters (Chapter Plan, 31 Oct 2026): (number, title, programs now, still to come)
CHAPTERS = [
  (1,  'Data, Sampling, and Study Design', [], 'SampleLab'),
  (2,  'Graphs of Data', ['ScatterLab', 'DataLoad'], 'DescribeLab'),
  (3,  'Describing Data with Numbers', ['DataLoad', 'NormExplorer'], 'DescribeLab'),
  (4,  'Probability', ['BayesTree'], 'ProbLab'),
  (5,  'Binomial and Poisson', ['StatDist', 'GaltonBoard'], None),
  (6,  'The Normal Distribution', ['NormExplorer', 'Norm3', 'StatDist', 'GaltonBoard'], None),
  (7,  'Sampling Distributions and the CLT', ['CentralLimit', 'SampDist', 'GaltonBoard'], None),
  (8,  'Confidence Intervals', ['CICatcher', 'ResampLab'], None),
  (9,  'Hypothesis Testing: One Sample', ['TDist3D', 'PowerViz', 'FitCheck', 'AnovaLab'], 'one-sample t in TTestLabG'),
  (10, 'Power and Sample Size', ['PowerViz'], None),
  (11, 't-Tests: Two Samples', ['TTestLabG', 'TDist3D', 'DataLoad', 'ResampLab'], None),
  (12, 'Chi-Square', ['ChiTable', 'FitCheck'], None),
  (13, 'Correlation and Regression', ['ScatterLab', 'BiNorm3D'], None),
  (14, 'ANOVA', ['AnovaLab', 'DataLoad'], None),
  (15, 'Nonparametric Tests', ['RankLab', 'ResampLab', 'DataLoad'], None),
]
ALWAYS_OFFERED = 'TestChooser'      # the flowchart fits every chapter: offered beside them

DATA = {
  'rossi': ('Sample data (optional)/M1.hpmat', 'M1.hpmat',
            'The Rossi re-arrest study: 432 men released from prison, 5 columns (week of re-arrest, arrested, '
            'financial aid, age, prior convictions)'),
}

for num, title, progs, _ in CHAPTERS:
    for p in progs:
        assert p in PROGRAMS, (num, p)
assert ALWAYS_OFFERED in PROGRAMS

# ---- take the files from the pack ----
zin = zipfile.ZipFile(PACK)
prefix = 'Copy these into Prime/'
packed = {}
for info in zin.infolist():
    if info.filename.startswith(prefix) and not info.is_dir():
        packed[info.filename[len(prefix):]] = zin.read(info)
top = {p.split('/')[0] for p in packed}
named = {v[0] for v in PROGRAMS.values()}
missing, extra = named - top, top - named
if missing or extra:
    sys.exit(f'STOP: catalog and pack differ. Missing from pack: {sorted(missing)}; not in catalog: {sorted(extra)}')
for key, (src, dst, _) in DATA.items():
    packed[dst] = zin.read(src)

def checked_file(data):
    _, _, start, _ = kitprog.read(data)
    return kitprog.has_compiled_block(data, start)

checked = {}
for k, v in PROGRAMS.items():
    prg = [p for p in packed if p.split('/')[0] == v[0] and (p.endswith('.hpprgm') or p.endswith('.hpappprgm'))]
    assert len(prg) == 1, (k, prg)
    checked[k] = checked_file(packed[prg[0]])

buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for name in sorted(packed):
        zi = zipfile.ZipInfo(name, date_time=(2026, 11, 1, 12, 0, 0))
        zi.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(zi, packed[name])
emb = buf.getvalue()

catalog = {
  'programs': {k: {'file': v[0], 'version': v[1], 'what': v[2], 'home': v[3],
                   'files': sorted(p for p in packed if p.split('/')[0] == v[0]),
                   'bytes': sum(len(packed[p]) for p in packed if p.split('/')[0] == v[0])}
               for k, v in PROGRAMS.items()},
  'checked': {k: bool(c) for k, c in checked.items()},
  'all_checked': all(checked.values()),
  'chapters': [{'num': n, 'title': t, 'programs': p, 'coming': c} for n, t, p, c in CHAPTERS],
  'always': ALWAYS_OFFERED,
  'data': {k: {'file': v[1], 'what': v[2], 'bytes': len(packed[v[1]])} for k, v in DATA.items()},
  'pack': os.path.basename(PACK),
  'pack_sha256': hashlib.sha256(open(PACK, 'rb').read()).hexdigest()[:12],
}

t = open(os.path.join(HERE, 'loader_template_v1c.html'), encoding='utf-8').read()
import glob as _glob
_dl = sorted(_glob.glob(os.path.join(HERE, '..', 'data-loader', 'DataLoader_v*.html')),
             key=lambda p: [int(x) if x.isdigit() else x for x in __import__('re').split(r'(\d+)', os.path.basename(p))])
if not _dl:
    sys.exit('STOP: no data-loader/DataLoader_v*.html beside this folder')
DL_URL = SITE + 'data-loader/' + os.path.basename(_dl[-1])
assert t.count('__DATALOADER_URL__') == 1
t = t.replace('__DATALOADER_URL__', DL_URL)
# the Data Loader's core (its zip writer): in the repository it is ../data-loader/dl_core_v1.js
dl = next(p for p in (os.path.join(HERE, '..', 'data-loader', 'dl_core_v1.js'), os.path.join(HERE, 'dl_core_v1.js'))
          if os.path.exists(p))
parts = {
  '/*LOADERCORE*/': open(os.path.join(HERE, 'loader_core_v1.js'), encoding='utf-8').read(),
  '/*DLCORE*/': open(dl, encoding='utf-8').read(),
  '/*CATALOG*/': json.dumps(catalog, ensure_ascii=False),
  '/*PACK*/': json.dumps(base64.b64encode(emb).decode('ascii')),
}
for k, v in parts.items():
    assert t.count(k) == 1, k
    t = t.replace(k, v)
open(OUT, 'w', encoding='utf-8').write(t)
page = os.path.basename(OUT)
redirect = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>HP Prime Loader</title>\n'
            '<meta http-equiv="refresh" content="0; url=' + page + '">\n'
            '<link rel="canonical" href="' + SITE + 'prime-loader/' + page + '">\n'
            '<style>body{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#172033;background:#f6f8fb}'
            '@media (prefers-color-scheme:dark){body{color:#e8edf6;background:#0f1420}a{color:#7d9cff}}</style>\n'
            '</head>\n<body>\n<!-- Written by build_loader_v1m.py: sends the browser on to the current Prime Loader, so the '
            'address .../prime-loader/ never changes. -->\n'
            '<p>Opening the HP Prime Loader&hellip; If nothing happens, <a href="' + page + '">click here</a>.</p>\n'
            '</body>\n</html>\n')
open(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'index.html'), 'w', encoding='utf-8').write(redirect)
print('index.html -> ' + page + '; Data Loader link: ' + DL_URL)
print(f'checked files: {sum(checked.values())} of {len(checked)}' + ('' if all(checked.values()) else
      '  (unchecked: ' + ', '.join(k for k, c in checked.items() if not c) + ')'))
print(f'{os.path.basename(OUT)}: {len(t):,} bytes; {len(packed)} files embedded '
      f'({sum(len(b) for b in packed.values()):,} bytes, {len(emb):,} zipped); pack {catalog["pack"]} {catalog["pack_sha256"]}')
