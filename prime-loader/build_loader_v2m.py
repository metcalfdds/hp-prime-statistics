#!/usr/bin/env python3
"""build_loader_v2m.py -- assembles PrimeLoader_v2m.html: the page template, the loader's core, the Data Loader's core
(for its zip writer), the USB core, the chapter list, and every program file from a starter pack, embedded so the
page works offline.

    python3 build_loader_v2m.py PACK.zip [OUT.html] [--kit PATH]
v2m (21 Nov 2026): the template's v2m, accessibility only (the template's first comment says what): deeper orange and
green for text, a role and the page's own name for the log's box, and one heading's level.  The same pack, the same
groups, the same cable code (prime_usb_v3d.js), and not a word that a student reads is different.
v2h (18 Nov 2026, 17:45): the template's v2h, and EpiStats in a group of its own (ALONE, below): sent to the author's
G1 with two programs behind it, it would not run and the calculator reset; sent alone, it ran (Roger, 17:01 and 17:30).
prime_usb_v3d.js rests the calculator after each program.
v2g (18 Nov 2026, 16:50): the template's v2g: groups of chapters for a real HP Prime (CHAPTER_GROUPS below, and the
advanced programs dealt into three), which the cable sends after taking the book's other programs off; the Virtual
Calculator takes all the programs with nothing to choose.  prime_usb_v3d.js.
v2f (18 Nov 2026, 15:40): the template's v2f, the cable for every student (the G2 and G1 logs of 18 Nov).  It went to the author's PC
at 15:59 and wrote the logs of 16:04 and 16:11, and was never published.
v2e (18 Nov 2026, 12:30): the template's v2e, which tells a student in Firefox or Safari with a real HP Prime
that Chrome or Edge can send the programs down the cable.  The same pack and cable code.
v2d (18 Nov 2026, 04:20 to 04:35): the page template's v2d, in which the two ways are "1) The Statisticles way" and
"2) The official HP way: the Connectivity Kit" and the sentence under the step's title is Roger's, without its "and we
have tested it" until that is so (Roger: "the testing claim is not valid yet").  The same pack and cable code.
v2c (18 Nov 2026): the page template's v2c, which names the step that offers the cable and the Connectivity Kit as Roger
named it ("Two ways to load Statisticles onto a physical Prime G1 or G2 calculator") and the two ways as the first and
the second.  The same pack (v23) and the same usb/prime_usb_v3d.js.
v2b (17 Nov 2026, late): the page template's v2b and usb/prime_usb_v3d.js, on starter pack v23 as before (no program
changed).  That evening the author's G2 and his G1 took test programs of every size down their cables by one route
(usb/logs/); v2b's cable panel sends the chosen programs by that route and reads each back.  It shows only at the
test address (?usb=1) until a real chapter has loaded on a calculator, and there it stands above the Connectivity
Kit's steps, which are kept whole (Roger: "maybe we shoould keep the instructions for the COnnectivity Kit as a
backup").  The catalog now names the page's version, for the cable's log.
v2a (17 Nov 2026, night): the page template's v2a and the loader core's v3, on starter pack v23 as before.  Roger,
after the review: "i'm thinking we need to make this process as simple as is possible", then "How about let the
student choose?--1) put all the programs on the Virtual Calculator at once or 2) I'll choose which Chapter to load, one
at a time", then "we do need to make some sort of very simple loader ... to get the programs on a physical
calcuator".  The page asks two things and has one button: which calculator (the Virtual Calculator, or a real HP
Prime), and which programs (all of them, or one chapter).  All the programs are ADDED to what is on the calculator;
one chapter leaves the calculator with that chapter's programs and TestChooser, the book's other programs moved to
the backup, and a program of the student's own is never moved (loader_core_v3.js, planBook).  For a real HP Prime the
same choice downloads as one zip, with HP's Connectivity Kit steps in the page's main line.
  The build now also (a) finds where each program's source lies inside its .hpprgm (hp-prime-kit's reader), checks
that source against programs/ character for character, and writes the two offsets into the catalog, and (b) embeds
usb/prime_usb_v1.js.  Both serve sending a program straight down the USB cable, which the page shows only at its
test address (?usb=1) until it has been proved on a calculator: usb/README.md.
v1v (17 Nov 2026, the review "they must be bullet proof and as simple as possible"): the page template's v1d and the
loader core's v2, on starter pack v23 as before (no program changed).  A data file loaded on its own is ADDED, with
DataLoad, and the programs on the calculator stay (v1u moved every program to the backup and left the student with
data and no DataLoad); DataLoad goes on with any data, whatever chapter is picked; a data file is opened and checked
before it is taken; the student's own M1 wins over the sample data set; a phone, a computer that is not Windows and
a browser too old to unpack the programs each get a plain notice at the top.  The Data Loader's core is its v2 (the
zip writer is unchanged).
v1u (17 Nov 2026): starter pack v23, whose sixteen programs changed by round 17 carry their new versions.  Round 17
changed words on their screens only, to the book's house form for a statistic's letter ("F-test", "df = (n - 1)",
"p-value"): AgreeLab beta 1i, AnovaLab beta 1j, CICatcher beta 2m, EpiStats v1.7m, ExhibitLab beta 1i, FitCheck beta 1j,
PowerViz v2.5t, RankLab beta 1k, ResampLab beta 1j, ScatterLab beta 2m, StudRange beta 15n, TDist3D beta 1b, TTestLab
beta 1l, TTestLabG beta 1i, TestChooser beta 2h and TrendTest beta 3n.  The script is v1t's but for these lines and its
own name; the page template is v1c's, unchanged.
v1t (15 Nov 2026, night): starter pack v22, whose nine programs changed by round 16 carry their new versions: AnovaLab
beta 1i (Dunnett's test of every group against a control), RankLab beta 1j (Page's L for an ordered trend, and the runs
test), FitCheck beta 1i (Dixon's outlier test), CICatcher beta 2l (tolerance intervals), BiNorm3D beta 1g (a target view
with the circular error probable), and StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h and BurrLab beta 1r, whose
headers say what was done with the programs they stand beside.  The script is v1s's but for these lines and its own
name; the page template is v1c's, unchanged.
v1s (15 Nov 2026): starter pack v21, whose seven programs changed by round 15 carry their new versions: ScatterLab
beta 2l (a 95% interval for the population's correlation on the Inference page), FitCheck beta 1h (a standard error
beside the skewness and the kurtosis), and RankLab beta 1i, AnovaLab beta 1h, ResampLab beta 1i, ExhibitLab beta 1h and
SurvLab beta 1g, whose credits say what was done with the TI-83/84 programs they follow.  The script is v1r's but for
these lines and its own name; the page template is v1c's, unchanged.
v1r (14 Nov 2026, night): starter pack v20, whose TTestLab beta 1k and TTestLabG beta 1h (round 14, part 2) add the
one-sample t-test and the one- and two-proportion z-tests.  Chapter 9 now lists TTestLabG, and its "Coming: one-sample
t in TTestLabG" is gone.  Each program's version is now read from the repository's programs/ folder when the page is
built: v1q's table still named an older version for 14 of the 31 programs (in the page's data, not on the page).
v1q (14 Nov 2026): starter pack v19, whose CICatcher beta 2k and ScatterLab beta 2k (round 14) carry the help-page
wording fix and the slope's test, the two bands and Anscombe's quartet; nothing else differs from v1p.
v1p (13 Nov 2026): starter pack v18, whose ChiTable beta 3m (round 13) gives the exact test for its 2 x 3 and 3 x 2
tables.  The catalog names that version.  The page template is v1c's, unchanged.

v1o (13 Nov 2026): starter pack v17, whose twelve programs changed by round 12 (help-page fixes from the book's
pre-submission read: AnovaLab, BayesTree, CICatcher, DataLoad, EpiStats, FitCheck, PowerViz, RankLab, RiskLab, SampDist,
StatDist, TTestLab) carry their new versions.  The catalog names those versions.  The page template is v1c's, unchanged.

v1n (9 Nov 2026): starter pack v16, whose 31 programs carry round 11: the help pages in plain words, each changed
page laid out again at the calculator's own glyph widths (GlyphProbe_v1 on the Virtual Calculator), so nothing is cut; a page that no
longer fitted became two (AnovaLab, ChiTable, PowerViz, ErrorRate, StudRange, BayesTree and BurrLab have more help
pages).  The catalog names those versions.  The page template is v1c's, unchanged.

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
OUT = argv[1] if len(argv) > 1 else os.path.join(HERE, 'PrimeLoader_v2m.html')
SITE = 'https://metcalfdds.github.io/hp-prime-statistics/'
sys.path.insert(0, KIT)
from hpkit import program as kitprog            # hp-prime-kit (MIT, JordiRigau/hp-prime-kit)

# name: (file or app folder, version, what it does in a student's words, the name to type in Home)
PROGRAMS = {
  'AgreeLab':     ('AgreeLab.hpprgm', 'beta 1g', 'Examiner agreement: kappa and its cousins', 'AgreeLab'),
  'AnovaLab':     ('AnovaLab.hpprgm', 'beta 1f', 'ANOVA: one-way and two-way, and tests for variances', 'AnovaLab'),
  'BayesTree':    ('BayesTree.hpprgm', 'beta 8j', 'Bayes as a tree of 1,000 people: slide the prevalence', 'BayesTree'),
  'BiNorm3D':     ('BiNorm3D.hpprgm', 'beta 1f', 'Correlation in 3-D: turn the bivariate normal with a finger', 'BiNorm3D'),
  'BurrLab':      ('BurrLab.hpprgm', 'beta 1q', 'A model for long right tails (Burr XII)', 'BurrLab'),
  'CICatcher':    ('CICatcher.hpprgm', 'beta 2i', 'Fifty confidence intervals: how many catch the truth?', 'CICatcher'),
  'CentralLimit': ('CentralLimit.hpappdir', 'beta 3g', 'The central limit theorem, one sample at a time (an app)', None),
  'ChiTable':     ('ChiTable.hpprgm', 'beta 3m', 'Chi-square for a two-way table: drag the bars', 'ChiTable'),
  'DNAMixLR':     ('DNAMixLR.hpprgm', 'beta 3j', 'Likelihood ratios for DNA mixtures', 'DNAMixLR'),
  'DataLoad':     ('DataLoad.hpprgm', 'beta 1f', 'Puts a data file into the Statistics lists, with box plots', 'DATALOAD'),
  'EpiStats':     ('EpiStats.hpprgm', 'v1.7k', 'Epidemiology: 2 x 2 tables, risk and odds', 'EpiStats'),
  'ErrorRate':    ('ErrorRate.hpprgm', 'beta 1j', 'Error rates from proficiency tests', 'ErrorRate'),
  'FitCheck':     ('FitCheck.hpprgm', 'beta 1f', 'Goodness of fit: does the data match the model?', 'FitCheck'),
  'GaltonBoard':  ('GaltonBoard.hpprgm', 'beta 3i', 'Pour balls through pegs: the binomial becomes normal', 'GaltonBoard'),
  'Norm3':        ('Norm3.hpprgm', 'v2.4g', 'Drag x and watch the normal area', 'Norm3'),
  'NormExplorer': ('NormExplorer.hpprgm', 'beta 42j', 'The normal curve: areas, z scores, your own data', 'NormExp'),
  'PowerViz':     ('PowerViz.hpprgm', 'v2.5r', 'Power: drag the curves and watch alpha, beta and power', 'POWERVIZ'),
  'RankLab':      ('RankLab.hpprgm', 'beta 1g', 'Rank tests: sign, Wilcoxon, Mann-Whitney, Kruskal-Wallis', 'RankLab'),
  'ResampLab':    ('ResampLab.hpprgm', 'beta 1h', 'Permutation tests and the bootstrap, drawn as they run', 'ResampLab'),
  'RiskLab':      ('RiskLab.hpprgm', 'beta 1f', 'Risk scores and ROC curves', 'RiskLab'),
  'SampDist':     ('SampDist.hpprgm', 'v2.3j', 'The sampling distribution of the mean', 'SampDist'),
  'ScatterLab':   ('ScatterLab.hpprgm', 'beta 2j', 'Build a scatterplot with your finger; fit the line', 'ScatterLab'),
  'ExhibitLab':   ('ExhibitLab.hpprgm', 'beta 1g', 'How many units of a drug seizure to test?', 'ExhibitLab'),
  'StatDist':     ('StatDist.hpprgm', 'v2.7l', '27 distributions, each a plot you can touch', 'StatDist'),
  'StudRange':    ('StudRange.hpprgm', 'beta 15m', "Tukey's q, the studentized range", 'StudRange'),
  'SurvLab':      ('SurvLab.hpprgm', 'beta 1f', 'Time to an event: survival curves', 'SurvLab'),
  'TDist3D':      ('TDist3D.hpprgm', 'beta 1a', "Student's t as a surface: every t curve at once, turned with a finger", 'TDist3D'),
  'TTestLab':     ('TTestLab.hpprgm', 'beta 1i', 't-tests and z-tests in five steps (the advanced version)', 'TTESTLAB'),
  'TTestLabG':    ('TTestLabG.hpprgm', 'beta 1g', 't-tests and z-tests in five steps', 'TTESTLABG'),
  'TestChooser':  ('TestChooser.hpprgm', 'beta 2g', 'Which test? A flowchart you tap', 'TestChooser'),
  'TrendTest':    ('TrendTest.hpprgm', 'beta 3m', 'Chi-square for a trend', 'TrendTest'),
}

# v1r: each program's version is read from the repository's programs/ folder (the file name after _beta or _v), so
# the catalog cannot fall behind a program again.  A program with no file there, or with two, stops the build.
import glob, re
for _k in sorted(PROGRAMS):
    _m = [re.match('^' + re.escape(_k) + r'_(beta|v)(.+)\.txt$', os.path.basename(_p))
          for _p in glob.glob(os.path.join(os.path.dirname(HERE), 'programs', _k + '_*.txt'))]
    _m = [_x for _x in _m if _x]
    if len(_m) != 1: sys.exit('STOP: programs/ holds %d files for %s' % (len(_m), _k))
    PROGRAMS[_k] = (PROGRAMS[_k][0], ('beta ' + _m[0].group(2)) if _m[0].group(1) == 'beta' else 'v' + _m[0].group(2)) + PROGRAMS[_k][2:]

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
  (9,  'Hypothesis Testing: One Sample', ['TTestLabG', 'TDist3D', 'PowerViz', 'FitCheck', 'AnovaLab'], None),
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

# Groups for a real HP Prime (Roger, 18 Nov 2026, 16:16 and 16:18: "for a physical G1 or G2 choose 1) Ch 1-3, 2) Ch 4-6,
# 3) Ch 7--9. 4) Ch 10-12, 5) Ch 13-15, 6) Advanced 1, 7) Advanced 2, 8) Advanced 3"), because neither calculator
# held all 30 programs (the G1 full after 15, the G2 stopped after 13: usb/logs/, 18 Nov).  A chapter group is its
# chapters' programs and the flowchart.  The advanced programs (those of no chapter): EpiStats, the longest program
# of all, is Advanced 1 by itself (Roger, 18 Nov, 17:25: "I wounder if we maybe should handle EpiStats separately from
# the others?"; with ErrorRate and TrendTest sent behind it, his G1 would not run it and reset, and sent alone it ran),
# and the others are dealt into Advanced 2 and Advanced 3, of about the same size, in alphabetical order within each,
# by this script.
CHAPTER_GROUPS = [(1, 3), (4, 6), (7, 9), (10, 12), (13, 15)]
ALONE = 'EpiStats'

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

# v2a: where each program's source lies in its file, for the USB route (a program travels down the cable as its source,
# not as its .hpprgm: hp-prime-kit, docs/topics/usb.md).  The source found there must be the repository's own,
# character for character, or the build stops.  An app is three files and does not travel this way.
src_at = {}
src_len = {}        # the characters each program sends down the cable
for k, v in PROGRAMS.items():
    if not v[0].endswith('.hpprgm'):
        continue
    text, _, start, end = kitprog.read(packed[v[0]])
    mine = glob.glob(os.path.join(os.path.dirname(HERE), 'programs', k + '_*.txt'))
    # (blank space after a program's last line does not count: make_starter_pack_v4.py compares the same way, and
    # programs/ResampLab_beta1j.txt ends in one blank line more than its checked file)
    want = kitprog.normalize_source(open(mine[0], encoding='utf-8').read()).rstrip()
    if kitprog.normalize_source(text).rstrip() != want:
        sys.exit('STOP: the source inside %s is not programs/%s' % (v[0], os.path.basename(mine[0])))
    if packed[v[0]][start:end].decode('utf-16-le').rstrip('\0') != text:
        sys.exit('STOP: the offsets of %s do not give its source' % v[0])
    src_at[k] = [start, end]
    src_len[k] = len(text)

# The groups (see CHAPTER_GROUPS), sized by the characters each program sends down the cable.
def _chars(k):
    return src_len.get(k, 0)
GROUPS = []
_in_chapters = set()
for a, b in CHAPTER_GROUPS:
    progs = set(ALWAYS_OFFERED for _ in [0])
    for num, title, p, _ in CHAPTERS:
        if a <= num <= b:
            progs |= set(p)
    _in_chapters |= progs
    GROUPS.append({'id': 'c%d' % a, 'title': 'Chapters %d\u2013%d' % (a, b), 'file': 'Chapters_%d-%d' % (a, b),
                   'programs': sorted(progs, key=str.lower)})
assert ALONE in PROGRAMS and ALONE not in _in_chapters, ALONE
assert all(_chars(ALONE) >= _chars(k) for k in PROGRAMS), 'the program that goes alone is the longest'
_adv = sorted((k for k in PROGRAMS if k not in _in_chapters and k != ALONE), key=lambda k: (-_chars(k), k))
_bins = [[ALONE], [], []]
for k in _adv:                                   # largest first, each into the lightest group
    min(_bins[1:], key=lambda g: (sum(_chars(x) for x in g), len(g))).append(k)
for i, g in enumerate(_bins):
    GROUPS.append({'id': 'a%d' % (i + 1), 'title': 'Advanced %d' % (i + 1), 'file': 'Advanced_%d' % (i + 1),
                   'programs': sorted(g, key=str.lower)})
for g in GROUPS:
    g['chars'] = sum(_chars(k) for k in g['programs'])
    assert g['chars'] < 1300000, (g['title'], g['chars'])      # both calculators gave out near 2,000,000 (18 Nov)
assert sorted(set(k for g in GROUPS for k in g['programs'])) == sorted(PROGRAMS), 'every program is in a group'

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
                   'bytes': sum(len(packed[p]) for p in packed if p.split('/')[0] == v[0]),
                   'src': src_at.get(k)}
               for k, v in PROGRAMS.items()},
  'checked': {k: bool(c) for k, c in checked.items()},
  'all_checked': all(checked.values()),
  'chapters': [{'num': n, 'title': t, 'programs': p, 'coming': c} for n, t, p, c in CHAPTERS],
  'always': ALWAYS_OFFERED,
  'groups': GROUPS,
  'data': {k: {'file': v[1], 'what': v[2], 'bytes': len(packed[v[1]])} for k, v in DATA.items()},
  'pack': os.path.basename(PACK),
  'loader': 'v2m',
  'pack_sha256': hashlib.sha256(open(PACK, 'rb').read()).hexdigest()[:12],
}

t = open(os.path.join(HERE, 'loader_template_v2m.html'), encoding='utf-8').read()
import glob as _glob
_dl = sorted(_glob.glob(os.path.join(HERE, '..', 'data-loader', 'DataLoader_v*.html')),
             key=lambda p: [int(x) if x.isdigit() else x for x in __import__('re').split(r'(\d+)', os.path.basename(p))])
if not _dl:
    sys.exit('STOP: no data-loader/DataLoader_v*.html beside this folder')
DL_URL = SITE + 'data-loader/' + os.path.basename(_dl[-1])
assert t.count('__DATALOADER_URL__') == 1
t = t.replace('__DATALOADER_URL__', DL_URL)
# the Data Loader's core (its zip writer): in the repository it is ../data-loader/dl_core_v2.js
dl = next(p for p in (os.path.join(HERE, '..', 'data-loader', 'dl_core_v2.js'), os.path.join(HERE, 'dl_core_v2.js'))
          if os.path.exists(p))
parts = {
  '/*LOADERCORE*/': open(os.path.join(HERE, 'loader_core_v3.js'), encoding='utf-8').read(),
  '/*DLCORE*/': open(dl, encoding='utf-8').read(),
  '/*PRIMEUSB*/': open(os.path.join(HERE, 'usb', 'prime_usb_v3d.js'), encoding='utf-8').read(),
  '/*CATALOG*/': json.dumps(catalog, ensure_ascii=False),
  '/*PACK*/': json.dumps(base64.b64encode(emb).decode('ascii')),
}
for k, v in parts.items():
    assert t.count(k) == 1, k
    t = t.replace(k, v)
open(OUT, 'w', encoding='utf-8').write(t)
page = os.path.basename(OUT)
# v2a: the redirect carries on whatever follows the address (the Data Loader links to .../prime-loader/?data=1, and
# the author's test address ends ?usb=1); a browser with scripts off still gets there, without it.
redirect = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '<title>HP Prime Loader</title>\n'
            '<script>location.replace("' + page + '" + location.search + location.hash);</script>\n'
            '<noscript><meta http-equiv="refresh" content="0; url=' + page + '"></noscript>\n'
            '<link rel="canonical" href="' + SITE + 'prime-loader/' + page + '">\n'
            '<style>body{font:16px/1.5 system-ui,sans-serif;margin:2rem;color:#172033;background:#f6f8fb}'
            '@media (prefers-color-scheme:dark){body{color:#e8edf6;background:#0f1420}a{color:#7d9cff}}</style>\n'
            '</head>\n<body>\n<!-- Written by build_loader_v2m.py: sends the browser on to the current Prime Loader, so the '
            'address .../prime-loader/ never changes. -->\n'
            '<p>Opening the HP Prime Loader&hellip; If nothing happens, <a href="' + page + '">click here</a>.</p>\n'
            '</body>\n</html>\n')
open(os.path.join(os.path.dirname(os.path.abspath(OUT)), 'index.html'), 'w', encoding='utf-8').write(redirect)
print('index.html -> ' + page + '; Data Loader link: ' + DL_URL)
print(f'checked files: {sum(checked.values())} of {len(checked)}' + ('' if all(checked.values()) else
      '  (unchecked: ' + ', '.join(k for k, c in checked.items() if not c) + ')'))
print(f'{os.path.basename(OUT)}: {len(t.encode("utf-8")):,} bytes; {len(packed)} files embedded '
      f'({sum(len(b) for b in packed.values()):,} bytes, {len(emb):,} zipped); pack {catalog["pack"]} {catalog["pack_sha256"]}')
