# Round 16: working notes (15 Nov 2026)

A working file, kept on the branch so that a restarted cloud session loses nothing (the session's scratch folder was wiped
once, at 17:05 on 15 Nov 2026, with the prototypes and the notes in it; everything pushed survived).  Before the pull
request its lasting parts go into `verify/round16/README.md`, the change notes and the Lessons Learned, and this file goes.

Roger's orders (15 Nov 2026, 14:36): "1) yes cite it 2) Add all please 3) yes tell them why 4) it's just filler, use if needed,
doesn't need a page on its own--same for probability wizard 5) reword as the others---look, be consistent throughout the book";
14:39 "Just do a really good job"; 15:04 (to the course-survey proposals) "beautiful, keep going!"; 15:10 "You are referring to
our Lessons Learned and all the HP Prime reference material and programs in D:\HP-Prime aren't you?"; 15:11 "You were supposed to
make a catalog for that too right?"; 15:13 "interesting to refer back to the HP-67 programs if possible".

The six additions: Dunnett's test (AnovaLab), Page's L and a runs test (RankLab), Dixon's outlier test (FitCheck), exact
tolerance intervals (CICatcher), circular error probability (BiNorm3D).  Credits reworded "as the others" (StatDist, BurrLab,
RiskLab, AgreeLab) and consistently in the book.

## State

| piece | state |
|---|---|
| BiNorm3D beta 1g (target view, CEP) | committed a0842d0; verify 42/42; gate PASS; monkey 1,000/1,000 |
| StatDist v2.7n, AgreeLab 1h, RiskLab 1h, BurrLab 1r (credits) | committed a0842d0; wording verify 25/25 |
| CICatcher beta 2l (tolerance interval, exact factor) | committed 7fc39d8, 05be49c; verify 34/34; gate PASS; monkey 1,000/1,000 |
| FitCheck beta 1i (Dixon's outlier test; the loader's refused sample; axis numbers) | committed 8194529; verify 65/65; gate PASS; monkey 1,000/1,000 |
| RankLab beta 1j (Page's L, runs test) | design settled (points 2 and 3 below); build script next |
| AnovaLab beta 1i (Dunnett) | to do |
| paperwork (change notes, READMEs, Lessons Learned v7zw), Virtual Calculator, starter pack, Prime Loader, pull request | to do |
| Draft 37 of the book | after the round; its working folder must be restored from the source package on the PC |

## How a program is built here

`verify/round16/make_<name>.py` makes the new version from the old by exact replacements (BASE = main 4e8ff66; a miss stops
the build) into a scratch folder.  Gate: a copy of `tools/` outside the repository with the kit zipped beside it as
`Community_Library/github/JordiRigau__hp-prime-kit.zip` (top folder `hp-prime-kit-HEAD`), then
`python3 tools/ppl_gate_v1e.py NEW.txt OLD.txt`: "RESULT: PASS", kit lint 0 errors, `ppl_check_v5 tally: clean` (W3 = a
TEXTOUT_P literal too wide by its estimate: keep a literal to about 52 characters from x = 4, 20 from x = 198).  Smoke and
pictures: `python3 tools/page_render_v1.py PROG --call "X()" --key .. --tap x,y --choose n --out DIR`.  Text is measured at
`verify/round11/glyph_widths_vc.json` (code -> [font 1, font 2, font 3] pixels); a help line is at most 296 px.  Then
`git rm` the old file, copy the new one into `programs/`, write `verify/verify_<Name>_<ver>.py` (T build, A arithmetic against
references, V every way out and the returned line, R regression against the old version, H help, G static, D layout), save
its output beside it, monkey 1,000 (`tools/monkey_chunks_v1.py PROG "X()" 16 0 1000 verify/round16/mk/X.jsonl --lists
[--writes D]`), commit, push.

Harness facts: set globals as FLOATS (a whole-number df given as a Python int is "not a whole number" to it); `INPUT` answers
are dicts by variable name, or `CANCEL` (imported from `ppl_run_v3e`), never 'ok'/'cancel' strings; a screen that carries soft
keys has `func` = the main routine (the wait), a blitted screen has the drawing routine's name and `menu` None;
`h.chooses[i].items / .title`, `h.msgboxes[i].lines`, `h.screens[i].lines() / .texts (.text .x .y .font .width .color)`.

## Design decisions

1. DUNNETT (AnovaLab 1h -> 1i).  F(c) = P(max|T_j| <= c) = INT f_nu(s) G(c s) ds, G(y) = 2 INT_0^7 phi(z) PROD_j [Phi(b_j z +
   y a_j) - Phi(b_j z - y a_j)] dz, b_j = sqrt(n_j/n_0), a_j = sqrt(1 + b_j^2).  A table of G at y = 0, 0.1, ..., 12 (Simpson
   on [0, 7]; nz intervals by b max: 24 / 32 / 48 / 64 / 80 for b max <= 1.25 / 2 / 3 / 4 / 5; b max > 5 refused with a
   sentence), then AnovaLab's own outer scheme (u^2 substitution for df <= 100; 1 +- 12/sqrt(2 df) above) with 4-point
   cubic interpolation.  Found in the prototype: |F error| <= 6E-5, relative error of p <= 0.3 % (p >= 1E-4), d crit relative
   error <= 4E-5 for df >= 3 but up to 1E-2 at df 1-2, so Dunnett needs df >= 3 (as Tukey).  Two-sided only; d crit searched
   up to 60.  Reference: m = 1 equals the t test to 12 digits; two-sided 5 % d for m = 2, 3 at df 20: 2.379, 2.540.
   UI: One-way Menu item "Dunnett: all vs a control" -> pick the control (CHOOSE) -> estimate + "Compute it now / Not now" ->
   page 6 (difference, family CI, adjusted p).  Own routines av_Dn*; old pages untouched; arrows on page 6 guarded.
2. PAGE'S L (RankLab 1i -> 1j, rkTest 7), settled 15 Nov evening.  On the Friedman data (rkFM, b blocks x k treatments,
   within-block midranks rkFR): L = sum_j j R_j over treatments in the order listed; mean b k (k+1)^2/4; variance = sum over
   blocks of k (k+1) (k (k^2-1) - T_i)/144 (T_i = sum (t^3 - t) of the block's ties; no ties: b k^2 (k+1)^2 (k-1)/144);
   z WITHOUT a continuity correction (Page 1963, SciPy, R).  Slot 5 toggles "Rising" / "Falling" (rkTail 2 <-> 1; falling =
   the lower tail of L); slot 4 Exact / Normal.  Exact null by convolving the blocks' own distributions as probabilities
   (rkNDen = 1): an untied block from the stored one-block counts for k = 3..9 (written by the build from Python; support
   sizes 5, 11, 21, 36, 57, 85, 121), a tied block (k <= 5) by walking all k! orders of its midranks on a doubled scale
   (step 0.5); a step budget of about 60,000 decides exact or normal, with the progress bar and "Esc = stop (the normal
   approximation stays)".  RankLab's exact p is CONDITIONAL ON THE TIES; R's PageTest and SciPy's method='exact' use the
   untied null whatever the data (SciPy's notes say its exact p is not adjusted for ties).  The halo preset (rkFNoP = 1) is
   refused with a sentence.  Page 2 = a trend picture (mean rank of each treatment in order, the H0 level (k+1)/2 dotted,
   tap a treatment).  Checks: k = 3: n = 4 critical 54/55/56, n = 5: 66/68/70; equals `scipy.stats.page_trend_test(
   method='exact')` when nothing is tied.
   PRESETS' REFERENCE NUMBERS (Python, exact arithmetic):
   - Ozone (4 subjects x 3 levels; rows -.08 .01 .06 / .21 .17 .19 / .50 -.11 .34 / .14 .07 .14): L = 48, mean 48,
     variance 15/2 with the tie (8 untied), z = 0; exact conditional on the tie P(L >= 48) = 14/27 = 0.5185; the untied
     null gives 83/144 = 0.5764 (R, SciPy exact); SciPy asymptotic 0.5.
   - Draft 1970, days 1-28 as blocks, the 12 months in calendar order: L = 13,440, mean 14,196, SD 228.149, z = -3.3136,
     lower-tail ("falling") p = 0.00046; mean ranks by month 6.86 7.04 8.0 7.07 7.21 6.64 6.07 6.29 5.57 6.86 5.36 5.04.
3. RUNS TEST (RankLab, rkTest 8), settled 15 Nov evening.  The statistic is called "runs" on the screen (R is red in the
   example).  n1, n2 symbols; exact pmf from E_k = 2 C(n1-1, k-1) C(n2-1, k-1) (runs = 2k) and O_k = E_k (n - 2k)/(2k)
   (runs = 2k + 1), E_(k+1)/E_k = (n1-k)(n2-k)/k^2, denominator C(n, n1), in logs; mean 2 n1 n2/n + 1, variance
   2 n1 n2 (2 n1 n2 - n)/(n^2 (n-1)); z WITHOUT a continuity correction, as the HP-65 program and the texts print it;
   two-sided exact = min(1, 2 x the smaller tail) (RankLab's rule, rk_Pick); the null is not symmetric, so on the bars a
   two-sided test colors the smaller tail only.  Page 2 = the sequence as rows of colored squares (tap one: its place,
   kind, run number and length).  D1 with two distinct values = the two symbols; otherwise above / below the median, values
   equal to it dropped.
   PRESETS' REFERENCE NUMBERS:
   - Roulette (HP-65 Stat Pac 2, 1975): n = 25, 14 R, 11 B, 9 runs, mean 13.32, SD 2.4106, z = -1.7921; exact lower
     409/7429 = 0.055055, upper 0.977669, two-sided 0.110109; normal lower 0.0366, two-sided 0.0731 (0.113 with the
     continuity correction).
   - Draft 1970, runs by day (median 183.5, n1 = n2 = 183): 172 runs, mean 184.00, SD 9.552, z = -1.2562; exact lower
     0.1143, two-sided 0.2286; normal two-sided 0.2090.
   A TEACHING FINDING for the book: on the 1970 lottery the runs test by day sees nothing (p = 0.23) while Page's L by
   month (p = 0.0005) and the rank correlation do.
   MENUS.  THE BOOK NAMES MENU ITEMS BY NUMBER ("7 Load a preset", "3 Draft 1970: day vs number", "4 Darwin: Zea mays
   pairs"), so every old item keeps its number.  Main menu: 1-8 as they are, 9 "Page's L (ordered trend)", 10 (shown as A)
   "Runs test (randomness)", 11 Help, 12 Quit.  Presets: old 1-7 keep their places; 8 "Ozone: airway resistance" (Page,
   rising), 9 "Draft 1970: months in order" (Page, falling), 10 "Roulette: red and black" (runs), 11 "Draft 1970: runs by
   day" (runs).  Use my data: "Page's L: rows = blocks" (loads as Friedman does) and "Runs: D1 in order".
4. DIXON (FitCheck 1h -> 1i): the normality view's empty fifth soft key -> the Outlier page.  P(r > R) = n!/((j-1)! m!)
   INT INT_{a<b} F(a)^(j-1) f(a) f(b) [G^m + (i-1) m G^(m-1) (H - G)] da db, m = n-j-1, G = F(b - R (b-a)) - F(a),
   H = F(b) - F(a); (i, j) = (1,1) r10 n 3-7; (1,2) r11 n 8-10; (2,2) r21 n 11-13; (2,3) r22 n 14-30.  Calculator rule:
   Gauss-Legendre N x N over a in Ea +- W sda and b in [max(a, Eb - W sdb), Eb + W sdb], Blom centres pa = (j - .375)/
   (n + .25), sda = sqrt(pa (1-pa)/(n+2))/phi(Ea), b the mirror of x(1); W = 7, N = 20: relative error 2.2E-4 for p > 1E-3,
   1.2E-3 for p > 1E-4 (prototype; the verify script measures it again through the harness).  Shown: the ratio at each end,
   the one-end p of the bigger, "either end" p = min(1, 2 p), a sentence at alpha = 0.05 on the p as shown (4 decimals).
   3 <= n <= 30, raw values only.  Preset: Darwin's 15 differences (RankLab's rkXA - rkXB): n = 15 -> r22; low end
   (x3 - x1)/(x13 - x1) = 9.125/15.375 = 0.5935, one-end p 0.01606, either end 0.0321; high end 0.2754 (p 0.491).  The plain
   r10 at the low end is 0.134 (p 0.42): the second low value (-6) masks the first.  r22, n = 15, one-sided .025 point: 0.5686.
   FOUND WHILE READING FitCheck: a sample refused because every value is the same had already replaced fcX, fcNX and fcXb;
   "The last sample again" then stopped with an index error in the Q-Q page (beta 1h and before).  Mended in beta 1i
   (the spread is checked on a local sorted copy first).  The other refusal paths (Benford, Poisson, binomial, counts) were
   tried and are clean.
5. TOLERANCE (CICatcher 2k -> 2l): done.  Exact two-sided k: 1 - g = 2 INT_0^6 phi(t) ChiCDF(nu, nu rho(t/sqrt n)^2/k^2) dt,
   12-point Gauss-Legendre; reference k (g = .95): n = 10: 2.8563 / 3.3934 / 4.4369 for p = .90 / .95 / .99; Howe 2.8382 /
   3.3819 / 4.4446; the AFIT STAT COE report 09-2020 "Tolerance Intervals Demystified" prints 2.838, 3.381 (Howe's).
6. CEP (BiNorm3D 1f -> 1g): done.  R50: rho = 0: 1.17741; 0.3: 1.15969; 0.6: 1.10100; 0.9: 0.98792.

## What the library in D:\HP-Prime holds (searched 15 Nov 2026 with libsearch_v1.py over Library_Index.db)

- NO HP Prime program in the library does any of the six.  "Dunnett" and "Jonckheere" appear only as names in our TestChooser.
- RUNS TEST on HP calculators: HP-65 Stat Pac 2 (c Hewlett-Packard Company 1975, part 00065-90275), program 22 "The Run Test
  for Randomness", p. 84 (`Museum of HP Calculators flash drive/data/cd08/sw/65stat2.pdf`; OCR `MoHPC_OCR_contents/65STAT2.txt`);
  HP-67/HP-97 Users' Library Solutions: Test Statistics (reorder 00097-14008, part 00097-90163; no date in the text),
  pp. 27-31, "a translation of the HP-65 Stat Pac 2 program", reference there: Freund and Williams, Dictionary/Outline of
  Basic Statistics, McGraw-Hill, 1966 (`.../cd09/sw/67tststa.pdf`); HP-41C RUNTEST, "originally printed in the Test Stats
  Solution Book" (`.../cd17/web/software/41td/runtest.htm`).  They take n1, n2 and the run count u keyed in by the user and
  return mu, sigma, z; "For small samples, the test is based on special tables"; large = both n > 10.  THE HP EXAMPLE: a
  statistician at a roulette table in Las Vegas, RRRR B RRR BBBBB RR BBB RR BB RRR (0 and 00 ignored): 14 R, 11 B, 9 runs ->
  mu 13.32, sigma 2.41, z -1.79 (checked by hand).  Its closing remark, 7 words: "(His suspicion is not entirely unjustified.)"
  The same HP-67 book also has the mean-square successive difference test, Kruskal-Wallis, Fisher's exact test,
  Behrens-Fisher, the intraclass correlation.
- THE HP-65 EXAMPLE'S PAGE: Stat Pac 2, program Stat 2-22A "The Run Test for Randomness", its example on p. 86; the
  HP-67/HP-97 book's example on p. 29 ("This program is a translation of the HP-65 Stat Pac 2 program"; its printing shows
  the z as "1.79").  No TI program in the library does a runs test or Page's L (searched by name and by text).
- PAGE'S L, sources (verified on the web 15 Nov 2026): Page, E. B. (1963) Ordered hypotheses for multiple treatments: a
  significance test for linear ranks. J. Am. Stat. Assoc. 58(301):216-230.  Odeh, R. E. (1977) The exact distribution of
  Page's L-statistic in the two-way layout. Commun. Stat. Simul. Comput. 6(1):49-61.  SciPy `page_trend_test` notes:
  E0 = m n (n+1)^2/4, V0 = m n^2 (n+1)(n^2-1)/144; its "exact" p is not adjusted for ties.
- ROGER'S 2021 OZONE HOMEWORK, its source found on his PC (`D:\Books and Papers\Nonparametric Statistical Methods.pdf`
  = Hollander, Wolfe & Chicken, 3rd ed., 2014): Chapter 7 Problem 1, Table 7.2 "Effect of Experimental Ozone Exposures on
  Airway Resistance (cm H2O/l/s)", p. 301, a subset of Goldsmith, J. R., and J. A. Nadel (1969), "Experimental exposure of
  human subjects to ozone", Journal of the Air Pollution Control Association 19, 329-330.  Columns: after .1, .6, 1.0 ppm.
  Subject 1: -.08, .01, .06; 2: .21, .17, .19; 3: .50, -.11, .34; 4: .14, .07, .14.  Problem 31 applies Page's procedure
  (7.25) to it.
- DUNNETT: HP-41C Users' Library Solutions "Applied Statistics I", program STAT.08 (`.../cd27/sw/41asul1.pdf`): after an
  ANOVA it computes LSD and, for the comparison of all the means to one control, t = |Y0 - Yi| / sqrt(s2 (1/n0 + 1/ni)), which
  the user compares with Dunnett's table (cites C. W. Dunnett, Biometrics 1964; 20; p. 488).  No probability is computed.
- DIXON: every "Dixon" hit in the HP stat pacs is the textbook Dixon and Massey (1969), not the outlier test.  TI STATLITE /
  STATCALC (statcalc.zip, decoded STATLITE__325.txt lines 204-218): its "Outlier test" asks for Q1 and Q3 and prints the IQR
  and the fences Q3 + 1.5 IQR and Q1 - 1.5 IQR: not Dixon's test.  Searches by name (qtest, dixon, grubb) and by text
  ("Dixon's Q / ratio / test / outlier"): nothing.
- TOLERANCE: nothing.  CEP: nothing.  Noncentral t: TI program NCT (noncentraltdist.zip), a 10-term series.
- BIVARIATE NORMAL: HP-65 Stat Pac 1 program 15 (p. 36) and the HP-55 statistics book p. 58 have "Bivariate Normal
  Distribution" programs (not read); Schrausser's HP_Prime_MATH has NVXY.pas.

## Dixon: sources read on the web, 15 Nov 2026

- Which ratio for which n, from two sources: NIST Dataplot "DIXON TEST"
  (itl.nist.gov/div898/software/dataplot/refman1/auxillar/dixon.htm): 3 <= N <= 7, 8 <= N <= 10, 11 <= N <= 13, 14 <= N <= 30,
  minimum and maximum formulas = r10, r11, r21, r22 (its 14-30 "maximum" formula repeats the minimum's: a slip on that page);
  "Dataplot limits the sample to be between 3 and 30"; the test assumes roughly normal data; masking and swamping named.  Its
  references: Dixon (1953) "Processing Data for Outliers", Biometrics 9(1):74-89; Dixon & Massey (1957) Introduction to
  Statistical Analysis, 2nd ed., pp. 275-278; ASTM E 178-08; Iglewicz & Hoaglin (1993).  R package dixonTest (CRAN manual):
  refined = TRUE: r10 3-7, r11 8-10, r21 11-13, r22 14-30; p by pdixon after McBane (2006).
- Dixon, W. J. (1950) Analysis of extreme values. Ann. Math. Stat. 21:488-506, doi:10.1214/aoms/1177729747.
- Dixon, W. J. (1951) Ratios involving extreme values. Ann. Math. Stat. 22(1):68-78, doi:10.1214/aoms/1177729693.
- Dean, R. B. & Dixon, W. J. (1951) Simplified statistics for small numbers of observations. Anal. Chem. 23:636-638,
  doi:10.1021/ac60052a025.
- McBane, G. C. (2006) Programs to compute distribution functions and critical values for extreme value ratios for outlier
  detection. J. Stat. Softw. 16(3):1-9, doi:10.18637/jss.v016.i03.  Read: r(j, i-1) = (x_n - x_(n-j))/(x_n - x_i), first
  subscript = values suspected at the upper end, second = at the lower end; the density as a double integral (its Eq. 4), by
  Gaussian quadrature; values are ONE-tailed, "90% confidence" two-tailed = the alpha .05 columns; Dixon's r10 table has two
  entries off (n = 4 and 6 at alpha .005, by .005 and .003), exactly what our integral found (0.9207 against 0.926; 0.7427
  against 0.740); other tables have more; Rorabacher (1991) interpolated in Dixon's tables.  Its printed r11 values at
  alpha .1 (n = 4, 6, 8, 22, 24, 26, 28, 30: .910 .610 .480 .269 .259 .251 .243 .237) all equal ours to 3 decimals.
- Rorabacher, D. B. (1991) Statistical treatment for rejection of deviant values: critical values of Dixon's "Q" parameter and
  related subrange ratios at the 95% confidence level. Anal. Chem. 63(2):139-146 (title seen in search results; volume and
  pages still to confirm before the book cites it).
- The printed Q table (Rorabacher 1991 by way of Harvey's Analytical Chemistry 2.1 appendix; two-sided alpha .10 / .05 / .01,
  n = 3..10: .941 .765 .642 .560 .507 .468 .437 .412 / .970 .829 .710 .625 .568 .526 .493 .466 / .994 .926 .821 .740 .680
  .634 .598 .568) is r10 at every n and equals the one-sided points at alpha/2 to about 0.005.  Exact one-sided 5 % points
  of r10, n = 3..10: 0.9413, 0.7655, 0.6424, 0.5624, 0.5073, 0.4671, 0.4363, 0.4119; the printed 0.560 (n = 6) cuts off
  5.12 % (40,000,000 simulated samples: 0.05118); the printed 0.926 (n = 4, 99 %) cuts off 0.43 % (exact point 0.9207).

## For the book (Draft 37)

Appendix E cites Student (1919) (confirm from the journal first); Chapter 3: a sentence on the packages' adjusted G1 and G2
(source to verify, e.g. Joanes & Gill 1998); the five lone decorative drawings out (PDF pages 51, 141, 158, 245, 304 of
Draft 36), a filler never gets a page of its own; credits wording consistent (the two "StatDist's framework follows"
sentences, Chapter 5 and Appendix C); the six additions in their chapters with captured screens and the changed help pages
word for word; the program table's versions; new references, each verified; the survey's additions (a sentence on Fisher's
LSD in Chapter 14, a paragraph on the unit of analysis in Chapter 1, three business examples: a filling line's tolerance
interval, a runs test on a production line or daily sales, a two-stock portfolio from the Markowitz unit); the HP-65/67 run
test and its roulette example; McBane's finding on the printed Dixon tables and the exact tolerance factors against Howe's
(show Roger the wording).  Then the Word pass (faults only), the comparison with Draft 36, the changes document, the status
file, the UTA check, the inventory, the source package, Draft 36's files to a _superseded folder.

## PPL rules, a digest for this round (read in full on 15 Nov 2026: START_HERE.md, docs/ppl-rules-for-any-assistant.md v2, docs/lessons-learned_v7zv.md)

SYNTAX / LIMITS
- <= 16 args per call; LOCAL only at the top of a routine, <= 6 names a line; no LOCAL inside IF/FOR/CASE; parameters by
  value; never INPUT into a parameter.
- No // comment inside an open bracket (CHOOSE list, {..}); exponent with capital E; code ASCII (pi = 3.14159265359); <> never !=.
- Names: never a built-in ignoring case (tools/HP_Prime_Builtin_Names.txt; csC = CSC, inV = INV, lsq = LSQ, ans, ci, fp, ip,
  ln, re, im, sign, e, i, x, K, G1-G9); parameters stricter than LOCALs; every helper carries the program's tag, every local a
  routine tag; no names equal apart from case (tools/case_scan_v1.py); a MAKELIST counter is a LOCAL; one name pool for the
  whole fleet (tools/fleet_names_v2.py).
- CHOOSE: list form, idx := 0 before, test idx after (Cancel leaves 0); items <= 30 characters; the box shows 8 items (a 9th
  is cut; a menu that must be seen whole has <= 8); it numbers items itself (1-9, A, B, C); opens with item 1 highlighted.
- INPUT: every number field {name,[0]}; label about 14 characters, help line about 47 with the field's RANGE; INPUT returns 0
  on cancel; refuse a value outside its range with a sentence that gives the range and change NOTHING (never clamp).  Fleet
  limits: mean/x/bound -10,000..10,000; SD/scale/df/rate > 0 and <= 1,000; typed n <= 10,000; table count <= 100,000; alpha
  0.001..0.2 (help "From 0.001 to 0.2; 0.05 is usual"); seed 0..9,999.  Data in lists: no limit, but a D list holding a number
  of > 50 digits is left out or refused with a sentence.
- MSGBOX shows 5 lines.  Commit a dialog sequence all at once or not at all (hold answers in locals until the last dialog
  returned).  A refused read changes nothing (read into locals, check, then assign).  A guard goes BEFORE the quantity it protects.

NUMBERS
- 12 significant digits; overflow -> infinity silently (IFERR does not see it); division by zero IS an error; x := x + step
  can stall (count steps).
- Never 1 - CDF: normal upper tail NORMALD_CDF(m, s, 2m - t); chi-square upper tails as finite positive sums; right-tail
  quantile -NORMALD_ICDF(0,1,alpha); clamp p inside (0,1) before any ICDF.
- Positive terms only (no alternating sums); work in logs where a product can pass 1E499; exact tests: log binomials from the
  neighbor, relative to the biggest term, ties within 1E-7 in the log, cap the count and say so.
- SD from deviations in a second pass; MAX(0, variance) before the root; scale before squaring.
- CHISQUARE(df,x) is the DENSITY.  CHISQUARE_CDF/ICDF and FISHER_CDF/ICDF take whole df only; STUDENT_* any df; STUDENT_CDF
  loses digits at huge df (cap n).  BINOMIAL(n, p, k) order.  POISSON_CDF(l, k<0) is an error.  No GEOMETRIC*, no LNGAMMA
  outside the CAS.
- STRING(x, 2, d): d <= 12; below 10^-d it goes scientific (use STRING(ROUND(x,d),2,d) or "< 0.001"); minus is CHAR(8722),
  E is CHAR(7431); never build CAS/Python text with STRING; a trailing-zero stripper checks for "." first and never strips an
  exponent; a probability prints "p < 0.001", never 0.000.
- INSTRING(s, ..) with s = "" is an error (guard DIM(s) > 0); LEFT(s,0)/RIGHT(s,0) give the whole string; MID(s,0,n) is an error.
- A fixed quadrature grid must be checked at EVERY df/parameter the form accepts.
- Verify every formula against SciPy/statsmodels/exact arithmetic BEFORE the calculator; call the reference twice (one that
  changes is a simulation); derive the reference independently; check a formula by calling its routine through the harness.
- Commas: every number >= 1,000 on screen goes through <prefix>Cm where it becomes text; never in CAS/EXPR text, a year, a
  key, or a name with digits.  A number with no bound on its size needs a bound on what is printed.

SCREEN
- 320 x 240; compose on G1, BLIT_P(G0,0,0,G1) once, DRAWMENU after the blit; a one-colour RECT_P FILLS (outline = two
  colours or four LINE_P); ARC_P rings are not a disc; dotted lines by PIXON_P STEP loops; cache every curve once per frame.
- Text: measure by glyph widths; font-2 lines 14 px apart; never clip a number with TEXTOUT_P's width argument; numbers
  compared on one line carry the same decimals; a comparison has three cases (equal at the decimals shown).
- Help pages: header "<Name> help n/N: <Topic>"; plain words, every soft key named; no figure numbers; no backslash; American
  spelling; "t-test"; a page that does not fit becomes two, split at a block's edge; a label line, a "key = meaning" item, a
  formula and the sentence after it each begin a line of their own; the book prints help pages word for word (program wording
  and book change together).
- Soft keys: no key labeled OK unless it closes; "More" in slot 6 when > 6 actions.  A footer says only what the keys do.
  End with RETURN <summary string>.
- Waiting: drain, wait, drain; a GETKEY drain does not drain touch (capped finger-lift drain after every INPUT/CHOOSE/MSGBOX
  opened from a MOUSE loop); WAIT(-1) lists: check SIZE before x, y; strip taps arrive as {3,x,y} with y >= 218.
- Symbols on screen: chi-square CHAR(967)+CHAR(178), sqrt 8730, >= 8805, <= 8804, <> 8800, +- 177, x 215, -> 8594, inf 8734,
  mu 956, sigma 963, theta 952, rho 961, lambda 955, alpha, beta, subscripts 8320-8322, xbar 57344, phat 57345, yhat 375,
  ybar 563, pi 960, e-acute 233.  Sigma (931) NOT verified.  A division sign (247) is not in the measured glyph table.  A
  double quote in a string is CHAR(34).

HOW A FEATURE IS ADDED
- Search the library and the routine pool first; add a new test BESIDE the old ones (routines of its own; old arithmetic
  wrapped, not edited) so the verify script can show the old screens unchanged.  A feature another program has is written
  from its FORMULA; the change note says what was read.
- Credits say what was done.  Version by letter; header, "What changed" block and the version the student sees; the change
  note; the verify script with its output; a line in verify/README.md; README test-status and program row.
- Verify script: arithmetic against references; EVERY cancel and refusal path; one session of each kind ended and the returned
  line read; old screens equal; D part: text_overlap_v1 + label_fit_v1; comma_check_v1; menus <= 30 characters; a static check
  for !=; runs from the repository alone.
- After any change in programs/: starter pack (next number) in two passes with Check on the Virtual Calculator and NO run
  before collecting the checked files; then the Prime Loader; index.html's link if the Data Loader's number changed.
- Nothing is "device-tested" unless it ran on the Virtual Calculator, a G1 or a G2.  A device fact the harness lacks goes into
  tools/prime_facts_v1.py.
- Virtual Calculator driving: never "open" it while it runs; run by EXPORT name from Home without brackets; the Check box
  closes at the next press; keys can be lost while a page draws (wait 3-6 s); collect checked files before any run.
