# HP Prime Lessons Learned
*Roger Metcalf & Claude · v7q · 23 October 2026 (v7p 23 October 2026; v7o 22 October 2026; v7n 20 October 2026, night; v7m 20 October 2026, evening; v7l 19 October 2026, night; v7k 19 October 2026, evening; v7j 19 October 2026, afternoon; v7i 17 October 2026, evening; v7h 17 October 2026, morning; v7g 16 October 2026, evening; v7f 16 October 2026; v7e 12 October 2026; v7d 11 October 2026; v7c, v7b, v7a and v7 on 10 October 2026; v6 6 October 2026; v5 3 October 2026; v4 1 October 2026; v3 rewritten 28 September 2026)*

**What changed in v7q** (a wrong direction, 23 Oct 2026): the v7o bullet on the harness formula checks said R's `prop.trend.test` prints a trend statistic *smaller* than TrendTest's by (N - 1)/N. It is the other way: Mantel's variance carries the N - 1 and is the larger, so Mantel's statistic is the smaller, and R's Armitage form is larger by N/(N - 1) (snoring-style table [2, 5, 9, 14] of 20 each: Mantel 16.853, R 17.067). The program's own comments had it right; the review's prose did not, and `python/hpstats.py` (new, v7q: the fleet's arithmetic in one tested module) caught it when its test derived Armitage's form by weighted regression, R's way. §14 rule 1, again: derive the reference independently; do not restate the thing under test.

**What changed in v7p** (one stale line, 23 Oct 2026): §3's bullet on `CHISQUARE` still told the reader that "P-values need `1 - CHISQUARE_CDF(n,x)`", the form v7o's own lessons retire. It now points at the forms that keep their digits (§3, §11). Nothing else changed.

**What changed in v7o** (an independent re-check of the whole fleet in a fresh cloud environment, Claude Code, 22 Oct 2026; StudRange beta 15e and TrendTest beta 3f; `docs/dev/independent-review-2026-10-22.md` has the full record):

- **A quadrature grid validated at one df is not validated at every df** (§11). StudRange's outer Simpson grid over s used 32 nodes for df 8 and above, and the beta 15 note said "df 100 and below: unchanged". But the density of s narrows as df grows, to a width of about 1/√(2 df), and from df about 50 to 100 the 32-node grid steps over it: `sr_SRCDF` at SciPy's 95th percentile gave 0.968 at df 90 (true 0.950) and 0.943 at df 70, so the PPL engine's plot cache was up to 2 percentage points off. The Critical value and P-value pages, which pass 64 nodes, were exact all along. Beta 15e uses 64 nodes at every df. The rule: before trusting a fixed grid, compare the integrand's width with the step at every df the form accepts, not only where the first bug was found.
- **Every chi-square upper tail is a finite sum of positive terms** (§11). `1 - CHISQUARE_CDF(df, x)` is exactly 0 on the Prime's 12 digits once the tail is below about 5E-13 (x above about 55 at 2 df). Beta 3d's trick for 1 df (2 P(Z < -√x)) does not extend to k - 1 df, but the closed forms do: even df, e^(-x/2) times the Poisson partial sum; odd df, 2 Φ(-√x) + √(2x/π) e^(-x/2) (1 + x/3 + x²/15 + …). TrendTest beta 3f's `trUpper` does this and matches SciPy to 5E-14 at df 1 to 12, x to 400. Nothing cancels, so nothing is lost.
- **An independent re-check needs only the repository, if the repository is complete** (§14, rule 18). The check ran with nothing of the author's environment: hp-prime-kit from GitHub, Giac from Ubuntu's `xcas` package, SciPy and statsmodels from pip. The gate passed on all 19 programs and every formula agreed. What did not run was the author's own 19 Oct verify suite: its scripts hard-code `/home/claude/work/...`, and 7 of the files they read (harness v3d, `ppl_harness_v1.py`, five intermediate program versions) were in neither git nor the working folder. So: a verify script finds `tools/` and `programs/` by relative path and reads an older version from git history; every version a script compares against is committed before the script is.
- **Check a formula by calling its routine, not by driving its pages** (§14, rule 19). `h.execute('es_WilsonCI(5,20)')` through the harness, or `h.globals_.update({...})` then `h.execute('csCompute()')`, gave 281 comparisons against SciPy, statsmodels and brute-force enumeration in an afternoon, DNAMixLR's θ-corrected mixture probability among them (every allele sequence enumerated). Two conventions recorded, not errors: `es_McNemar` returns 0 and p = 1 when b = c, as R's `mcnemar.test` does (statsmodels corrects anyway); `trCompute` uses Mantel's N - 1 variance, the larger variance, so its statistic is the smaller; R's `prop.trend.test` prints Armitage's form, larger by N/(N - 1) (corrected in v7q).
- **Keep executable code ASCII** (§5, §13). `ppl_check_v4.py` flags a π in code (E5); write 3.14159265359, the Prime's 12 digits, with a comment. Strings and comments may carry any glyph GfxProbe has shown renders.
- **The fleet** (§15): StudRange beta 15e, TrendTest beta 3f, neither yet on a calculator; the 20 Oct versions have had a cursory try on a G1 and a G2, not their checklists.

**What changed in v7n** (symbols on screen in every program; the first G1 timings; 20 Oct 2026, night):

- **Write the symbol, not its name, in text a student sees** (§5, §13). Roger: "use the symbols we developed", then "9 apps? check 20 please". All 20 programs were checked; 17 changed (ChiTable 3e, GaltonBoard 3e, StatDist 2.7f, TrendTest 3e, PowerViz 2.5e, EpiStats 1.7e, CICatcher 2d, CentralLimit 3d, DNAMixLR 3d, ScatterLab 2d, ErrorRate 1e, NormExplorer 42c, Burr3 2.4c, SampDist 2.3c, TestChooser 2b, BiNorm3D 1b, FDAES 3.9c); BayesTree, Norm3 and StudRange already wrote symbols. The glyphs: χ², x̄, p̂, ², √, ≥, ≤, ≠, ±, ×, →, ∞, α β θ λ μ ρ σ φ, and the subscripts ₀ ₁ ₂. Words stay for anything the CAS receives (ASCII only), Home variable names, the "+/-" that names the + and − keys (the house footer), code quoted on screen (R's `wilcox.test(x, mu)`), distribution names (Gamma, Beta) and powers other than ² (no other superscript has been checked). **π, η and τ are new on screen**: the G1 checklists ask for them.
- **A text sweep changes string literals and nothing else, and says so** (§14). `check_glyph_sweep2.py` folds every `CHAR()` build back into its string, blanks every string and comment, and compares the code line by line with the 19 Oct version (identical, apart from five listed display lines), checks that no literal used in a comparison or a replace changed, and that no CAS-bound line changed. The programs' own verify scripts then fail by design wherever they look for the old wording, the old version string, or "exactly these lines changed"; read each failure (the 20 Oct reading: all were of those kinds) rather than re-baselining blindly. The harness drives menus by their text, so a renamed item (StatDist's "Chi-square" → "χ²") stops a script until the label in it is changed.
- **First G1 timings** (§16; Roger, 20 Oct 2026, on the 19 Oct versions): GaltonBoard's pour, 100 balls in about 35 s, and its ×100 soft key in about half a second; StudRange q(0.05, 3, 12) = 3.7729 in about 7 s; BayesTree's drag fast; a light finger tap on a soft key registers, and a tap followed by a key works; NormExplorer's standardize animation smooth but too slow, because each frame's drawing time came on top of a fixed 0.3 s wait (beta 42b waits only for what is left of the 0.3 s, timed with `TICKS`, and its Diagnostics page shows the slowest frame).
- **DNAMixLR writes θ** (beta 3d): `dmTHG` was `"th"` until GfxProbe T14 showed `CHAR(952)` renders; it now is θ.

**What changed in v7m** (the first hardware checks of the 19 Oct fix versions, typed in Home on the G1, 20 Oct 2026, evening; Roger loaded all 20 current programs on the Virtual Calculator, the G2 and the G1 the same day):

- **Five Home lines settled on the G1** (§3). `NORMALD_CDF(0,1,−8)` keeps its digits (6.22096057427E−16), so the built-in lower tail is sound and the "compute upper tails as lower tails" rule rests on it. `NORMALD_ICDF(0,1,1)` returns **∞, not an error**, and `(1.17E6)^101` returns **+∞, not an error**: `IFERR` catches neither, so a probability that can reach 0 or 1, or a power that can overflow, needs its own guard before the call. `FOR I FROM 2 TO 1 DO PRINT(I); END;` runs zero times (Home shows 0; nothing printed). `STRING(x, 2, 1)` gives `"1400000000.0"` at 1.4E9 and `"14000000000.0"` at 1.4E10, `"140000000000"` (no point) at 1.4E11 and `"1.4E12"` above 12 digits: the PC harness's rule is right.
- **The fleet's 64 inverse-CDF calls, audited against the ∞ finding** (20 Oct 2026, read only). Every slider, drag and ladder already clamps its probability inside (0, 1), and NormExplorer beta 42a uses the `−NORMALD_ICDF(0, 1, α)` form throughout. Four programs still form a critical value as `ICDF(1 − α)` from a *typed* α that is checked only for 0 < α < 1: **ChiTable** beta 3d (`csSetAlpha`, line 3291), **EpiStats** v1.7d (sample size, lines 5451, 5526, 5588, 5647), **PowerViz** v2.5d (lines 667, 1000, 1260, 1262, 2007) and **SampDist** v2.3b (lines 584, 589, 1342, 1347). A typed α of about 1E−12 or less makes 1 − α exactly 1 in 12 digits, so the critical value is ∞ with no error message; what each screen then shows is untested. Fix at the next version of each: the mirrored form, or clamp the typed α to the range the program's own drag uses. Overflow: StatDist's window fit can reach +∞ for an extreme shape (Pareto α below about 0.004, Weibull k below about 0.001, log-normal μ above about 1150); floor the shapes or cap the fitted window. Nothing else in the fleet can overflow from user input.
- **Type large numbers with EEX, not a row of zeros** (§14). Two of the first readings were a zero short or a zero over; `1.4ᴇ11` settles a test that `140000000000` cannot.
- **Loading the fleet** (§16). The Connectivity Kit's backup folder (`Documents\HP Connectivity Kit\Calculators\<name>`) is the way to verify a load without reading the screen: each `.hpprgm` holds the pasted source as UTF-16, and a program with a `#PYTHON` block keeps a compiled header in front of it, so search for the master's first 100 characters rather than comparing from byte 0. All 20 matched their masters on the Virtual Calculator, the G2 and the G1. The G2 reset in the middle of a 2.4 MB drag and came back with its lists, matrices and settings at their defaults; the programs arrived on a second pass. The Kit's backup lags the calculator by a few minutes after a transfer and shows the calculator empty until it re-reads it. Send the fleet in batches of about five, and keep FDAES and EpiStats in different batches.
- **Old programs left on a calculator share the name pool** (§2, §15). The G1 still carried eight retired programs (BurrXII_5, ChiSq_beta1i, Fishers_Exact, Normexplorer_beta32b and four StudentizedRange variants). Delete them: they cost memory and their routines can answer for a current program's.
- **The error genealogy is now titled "How the Errors Propagated"** (v1m), and its argument for dentists is *Running Backwards*; both are in the author's working folder, not in this repository.

**What changed in v7l** (the error genealogy, "How the Errors Travelled", 19 Oct 2026, night; FDAES v3.9b; the document and the four researchers' notes are in the author's working folder, not in this repository):

- **Check the correction too** (§14, rule 16). Four researchers traced every error they could find in the dental age estimation literature from its origin to its correction to where it is still repeated. Twice on 19 October a correction of ours carried a fresh error: the fleet review credited Gustafson's 14.2-yr error to Lamendin's method, and the v3.9a history rewrite called Gustafson's ±3.63 "a mean deviation", which is Maples & Rice's 1979 guess. Lucy & Pollard (1995) could not reproduce it, and Aykroyd (1995, *J Forensic Sci* 40(6):925) derived it: the prediction error of a *mean*, computed with the wrong SD. FDAES v3.9b and the Student Guide say so. A paper that corrects an error is still a paper: read it against the original before copying its reasoning.
- **A reference sample's age range shapes the result, and that is bias, not sampling error** (§12). Studies that find "method A overestimates age in population B" are mostly comparing samples of different age structure (age mimicry); the difference does not shrink with sample size, and switching to a "matching" population sample does not cure it. Liversidge (2010, *FSI* 201:95–101) found the reported group differences for Demirjian's method "do not reflect any biological difference". Say which it is on any page that compares groups.
- **Numbers retyped from a handout drift** (§14, rule 16). Mincer's corrected 29.4 appears in no secondary source in Roger's library; the handouts carry the misprint 69.4 and a second wrong value, 19.0, which passes the eye test because the row still rises. Take every number from the original page, and print the page under every reprinted table.
- **FDAES v3.9b** (§15): one page reworded, nothing else; every v3.9a check re-run on it plus a Part V2 for the diff.

**What changed in v7k** (FDAES v3.9a, the same evening; `FDAES_v3.9a_CHANGES.md` and fact sheet v1a section 9 have the details):

- **Historical claims are facts too, and they get the same check as numbers** (§14, rule 16). FDAES's "Historical warnings ignored" page had two of its three entries backwards. Saunders (1837) argued *for* teeth as the test of a factory child's age ("subject to less variation, than that of any other organ", p 45). Saunders et al. (1993) found tooth-formation ages accurate. Every history line in v3.9a now names its paper and page: Gustafson 1950, Maples & Rice 1979, Lucy 1996, Cattell 1928, Harris et al. 2010 (Table 13.12, p 289, still prints Mincer's uncorrected 69.4), the 2011 ABFO workshop and the 2017 ABFO manual. Roger's library catalogue (`D:\Library_Catalog\catalog_v1.sqlite`) found every one of these papers in seconds.
- **An error measured on the fitting sample needs an outside test** (§12). Johanson's one-tooth SD is now 6.0, from his Table 8 (Roger, D5). An independent test on 17 new people (Lucy, Pollard & Roberts 1995) found single-root misses averaging 4.5 yr, an SD of about 5.6. The same test found that shrinking the error for several roots made it too small, so FDAES keeps 5.16 for two or more teeth. v3.9's 8.00 had no source. Roger also confirmed the Willems near-ceiling rule.

**What changed in v7j** (the 18 Oct "= <" cleanup, the FDAES v3.8 emulator run, a six-reviewer critical sweep of the whole fleet on 19 Oct and the fix pass it produced; Fleet_Review_2026-10-19_v1.md and each version's `_CHANGES.md` have the details):

- **The Prime's reals hold 12 significant digits, so `1 − CDF` is exactly 0 once a tail is below about 5E−13** (§3). FDAES v3.8 printed "P(age >= 16): < 0.1%" above "P(age >= 18): 0.0%" on the emulator. Compute every upper tail as a lower tail (the identities are in §3), every difference of two CDFs near 1 by its mirror image, and every right-tail quantile as `−NORMALD_ICDF(0, 1, α)`, never `NORMALD_ICDF(0, 1, 1 − α)`. StatDist v2.7e carries a per-family right tail, `st_sf`, for all 27 families.
- **Alternating sums lose every digit in 12-digit arithmetic** (§3, §11). DNAMixLR's inclusion–exclusion sum for P(E|H) cancelled to 0 with custom hypotheses: a true LR of 357,500 was reported as "Hd cannot produce this mixture". Beta 3c builds the same probability from positive terms only. Overflow is the same family: Burr3's pdf passed 1E500 at large shapes; v2.4b works in logs.
- **A fixed-decimal string of a number with no decimal point has no trailing zeros to strip** (§3). ScatterLab's `slNum` turned 140000000000 into "14".
- **A mean error is not an SD** (§12). Several papers report a mean (absolute) error. For normal errors SD = mean error × √(π/2) = 1.25 × mean error. Lamendin's 10 yr is FDAES's 12.5 yr (Roger, 19 Oct), and Prince & Ubelaker's own groups give 1.28–1.32. Label every spread with what it is and where it comes from.
- **Numbers that may be read in court get two independent transcriptions** (§14, rule 16). Prince & Ubelaker's and Bang & Ramm's tables were typed twice, blind, from 300-dpi page images, then compared with each other and with the OCR. Internal checks followed: nested-model SDs, CI midpoints, profile means reproducing the printed mean age. The same check found FDAES citing Prince & Ubelaker as 47(3):519–523 (the paper prints 47(1):107–116), and found the review itself repeating Gustafson's 14.2-yr error as Lamendin's.
- **Review the fix version too, and a table's ceiling is a floor, not an age** (§12; §14, rule 17). A second reviewer read FDAES v3.9 against the papers and found 25 more items in the new version. Among them: Bang & Ramm's molar rows pool all six molars of a jaw; the girls' Willems maximum is 15.93, not the all-H 15.79 (two G scores beat H); a Prince & Ubelaker estimate outside its sample's 25–99 was banded and pooled; and history pages made claims that nobody had checked against a source. Those claims are now marked "not checked against the sources" on screen. At a table's ceiling (Willems teeth 33–37 all at H) FDAES now says "at least about 15.8–16", draws no band and pools nothing.
- **Every header carries a DISCLAIMER line** (§13; Roger, 19 Oct): "a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes." FDAES, DNAMixLR and ErrorRate also show it on screen.
- **The emulator, two more driving notes** (§16): a quick mouse click on a `CHOOSE` item can end the program (the menu returns Cancel); two of about twenty brief PC-keyboard Enter presses were missed by `GETKEY` + `MOUSE` loops.
- **`FOR i FROM 2 TO 1` is assumed to run zero times, untested on the device** (§3). ErrorRate beta 1d guards its one such loop explicitly.
- **Tools:** `ppl_gate_v1c.py` runs the kit linter on a copy with the `#PYTHON … #END` blocks blanked (StudRange, GaltonBoard and ErrorRate no longer show a false "unbalanced blocks"). `lint_ppl.py` (edited in place, docstring v2) no longer reads the comment lines of `HP_Prime_Builtin_Names.txt` as names, and counts `STRING(MAX(a,b),2,1)` as three arguments. Over the fleet its reports fall from 649 to 320, none new.
- **The review that found these** (§14, rule 17): six reviewers, about 82,000 independent checks against SciPy, statsmodels and exact arithmetic, and **no wrong formula** in any program. What they found was at the edges: 4 crashes on silly or edited inputs, 6 wrong numbers on extreme inputs or in Home exports, and about 25 wrong-text items. Their check scripts became the fix versions' regression tests.

**What changed in v7i** (emulator round 2 on the HP Prime Virtual Calculator 2.4.2, build 2026-09-09, 17 Oct 2026, and the retest of its fix versions that afternoon; Emulator_Round2_Results_2026-10-17_v2.md has every observation, and this repository's copy is [dev/emulator-round2-2026-10-17.md](dev/emulator-round2-2026-10-17.md); each fact below was typed in Home or read from a probe's log to confirm it):

- **`INSTRING` on an empty string is a run-time error** (§3): `INSTRING("", "a")` is "Invalid input". It stopped TrendTest's and ScatterLab's CAS pages (a replace loop searched what was left of a string after the pattern had been its last character), and it sits in every program's CAS fallback: `xxCas` tests `INSTRING(cR, "undef")` after a failed call has set `cR := ""` (§9b). Guard every INSTRING whose first argument can be empty; the kit and the replace loop have new shapes.
- **Fixed decimals turn scientific below 10⁻ᵈ** (§3): `STRING(0.096, 2, 1)` is `"9.6ᴇ−2"`, `STRING(0.0004, 2, 3)` is `"4.000ᴇ−4"`. The exponent's minus is CHAR(8722), the Unicode minus, like the leading minus of a negative number (CASProbe beta 1c's log; v1 of the round-2 results transcribed it as a hyphen). Use `STRING(ROUND(x, d), 2, d)`, or the program's own "< 0.001" for a probability. TrendTest printed `(+9.6ᴇ−2 SE)`.
- **`LEFT(s, 0)` and `RIGHT(s, 0)` are the whole string; `MID(s, 0, n)` is an error** (§3). hp-prime-kit had measured the first; now confirmed on the fleet's build.
- **A `//` comment inside an open bracket is a syntax error** (§5): ChiTable beta 3b put two comment lines inside a CHOOSE list and did not compile. `ppl_check_v4.py` E12, hard in `ppl_gate_v1b.py`.
- **Under `WAIT(-1)`, a tap on the bottom strip is only a click, even on a screen with no soft keys drawn**, and **a tap read through `MOUSE` leaves no click behind** (§7). BayesTree's views ignored footer taps; BayesTree and StudRange skipped a real tap at the spot of a page's closing tap. A queued click comes back from `WAIT(-1)` at once: count a click as stale only if it did (< 100 ms).
- **`AND` and `OR` skip their right side** once the left decides (in Home); **`ROUND` rounds halves away from zero** and a negative value rounded to zero prints as `0.00` (§3). **`TEXTOUT_P` returns the x after its text** (§6; BayesTree beta 8c's breadcrumb uses it).
- **The fix versions were retested on the emulator** (§15): ChiTable 3c compiles, the TrendTest and ScatterLab CAS pages that crashed are exact, BayesTree and StudRange take the first tap after a page closes, no `ᴇ` shows where round 2 found one, and every cut menu line is whole except DNAMixLR's "Hypotheses" line (a wording choice). CASProbe 1c's T43b failed only because it compared text with a hyphen (§3), fixed in 1d.
- **CentralLimit runs as an app** (§16): the Kit's app editor does reach the calculator (round 1's note was wrong); the calculator's **View** key opens the app's Views menu.
- **Tools:** harness **ppl_run_v3d** models the first two facts, and **v3e** the Unicode minus (§14 rule 15); **ppl_gate_v1b** with **ppl_check_v4** catches the comment (rule 14). Every CAS program's `cas='fail'` run stopped at the empty INSTRING under v3d until its fix version.

**What changed in v7h** (the first run on the Prime's firmware: the HP Prime Virtual Calculator 2.4.2, build 2026-09-09, 17 Oct 2026; Emulator_Round1_Results_2026-10-17_v1.md has every observation):

- **The CAS call form was wrong, and the right one is known** (§9b). `CAS(s)` with `s` a string *variable* hands the text back **unevaluated**. The fleet's `xxCas` therefore returned its own input, and ErrorRate beta 1's "Why 3" page showed its question as the answer, badged "exact (CAS)". The form that works is `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))`, then drop the quotes (CASProbe beta 1b: 42 pass, 8 fail, 19 values). All twelve CAS programs carry it now (BRIEF_CAS_v2), and ErrorRate beta 1a shows a real `ln(20)` on the emulator.
- **The Prime prints CAS answers its own way** (§9b, new table): `e^(…)` for exp, `√` for sqrt, braces from `solve`, `∞` and `±∞`. Never parse for `exp(`, `sqrt(` or `list[`; check by value. **CAS variables persist** into the student's CAS until `purge`.
- **Soft keys under `WAIT(-1)`** (§7). A tap on the DRAWMENU strip reaches `WAIT(-1)` **only** as `{3, x, y}`, a click with no press and no lift (MenuTapProbe beta 1; WaitLab's 2014 note holds on 2026-09-09). BayesTree and StudRange looked for a type-0 press there and their soft keys did nothing. Read a strip tap from type 3 with y ≥ 218, and ignore type 3 above the strip, because a screen tap sends 0, 2 and then 3. `GETKEY` + `MOUSE` polling (ChiTable's pattern) sees strip taps as before.
- **Chi-square and F reject a fractional df** (§3). `CHISQUARE_CDF`, `CHISQUARE_ICDF`, `FISHER_CDF` and `FISHER_ICDF` raise "Invalid input" for df = 2.5. The densities `CHISQUARE` and `STUDENT`, and `STUDENT_CDF` / `STUDENT_ICDF`, take any df (Welch is safe). `POISSON_CDF(λ, k < 0)` raises too. StatDist v2.6 stopped on a chi-square df of 2.5.
- **ARC_P discs have holes** (§6). Concentric `ARC_P` rings at r = 3, 2, 1 plus the centre pixel leave the diagonals white (GfxProbe T09), so GaltonBoard's pegs and balls looked like ⊕. Use `FILLPOLY_P`.
- **GfxProbe's answers** (§6 table, §3): `FILLPOLY_P` (both list forms, with alpha), `TRIANGLE_P` (one colour, a three-colour blend, alpha), the ten-argument scaled `BLIT_P`, `MAX`/`SORT` on a list and a LOCAL `MAKELIST` counter (Home's K untouched) all work. MSGBOX shows 5 lines. All nine glyph lines render. `WAIT(−1)` types 0, 1, 2, 3 and 7 arrive as the manual says; their numbers are integers, which `STRING()` prints in hex. `BINOMIAL` takes (n, p, k) only. The 3-D `TRIANGLE_P` mesh drew nothing with our arguments.
- **`LOCAL name(args)` is a legal routine head** (§5; LocalHeadProbe).
- **Testing on the Virtual Calculator** (new §16): what it can and can't settle, and how to drive it.

**What changed in v7g** (the touch and graphics versions, the "More" key, and the CAS let in behind a fence; 16 Oct 2026, evening):

- **The CAS is allowed in fleet programs, behind a fence** (§1, new §9b). Roger, 21:15: "yes, change the rule". The old rule ("CAS only for genuinely symbolic work … keep each program on one side of the fence") stands for the *engine* of a program; the CAS may now add exact and symbolic *answers* — fractions, huge integers, closed forms, derivations, limits — through one call routine per program, on events only, with a decimal fallback and a badge. **Nothing about the CAS has run on our calculators**; CASProbe beta 1 settles the call form, the text it hands back, its error behaviour and its G1 speed.
- **The "More" soft key** (§13). When a screen needs more than six soft-key actions, slot 6 reads "More" on every page and steps to the next page of labels, wrapping to page 1 — the HP 48's NXT key (NEXT on the HP-28) in software (Roger, 16 Oct 2026). A screen whose actions fit in six gets no "More". Used by StatDist v2.6 (plot), BayesTree beta 7 (three pages) and NormExplorer beta 42 (page 2 chooses what the arrows move); the TouchKit template v2 carries the shape.
- **The PC run harness** (§14 rule 15): `ppl_run_v2.py` copies a list or matrix on assignment, as the calculator does (v1 shared the Python list, which could hide or invent aliasing bugs), and accepts a bare `RANDOM`; `ppl_run_v3.py` answers `CAS("...")` with desktop **Giac** — the engine inside the Prime's CAS — so a program's CAS text is tested end to end, and `cas='fail'` tests the fallback.
- **The touch and graphics versions** (§15) — nineteen programs and three new ones (ScatterLab, BiNorm3D, CICatcher), each gated and run in the harness against SciPy/statsmodels; none on hardware yet. ConTable2 and FEP are retired: EpiStats v1.6 module 1 and `EpiStats2x2(a,b,c,d)` replace them.
- **`CHOOSE`'s simple form takes 14 items** (§2, unchanged) — EpiStats v1.6's help menu sits exactly at it; BayesTree, ChiTable, StatDist, GaltonBoard and NormExplorer use the list form for their longer menus.

**What changed in v7f** (the fleet review of 16 October 2026 and the fix versions it produced; two new rules, one checker fix, one probe):

- **A fleet review** (`Fleet_Review_2026-10-16_v1.md`) read all nineteen programs against this file. The fix versions listed in §15 clear its section 2 (runtime errors, wrong numbers, output cut off by MSGBOX, missing drains) and section 3 (the sweeps). None of them has run on hardware yet; every one carries a device-test checklist in its `_CHANGES.md`.
- **`fleet_names_v2.py` requires each helper to carry ITS OWN FILE's tag** (§5). v1 accepted any two-to-four-character prefix as a tag, so StatDist's ten `calc_*` stubs passed as tagged and v7d's "0 untagged" was a false pass. v2 also reports a file that mixes two tags.
- **The MOUSE and WAIT(-1) type tables are different tables** (§7). In a `MOUSE` list the type is 0 New · 1 Completed · 2 Drag · 3 Stretch · 4 Rotate · 5 LongClick; in a `WAIT(-1)` list it is 0 Down · 1 Move · 2 Up · 3 Click · 5 Stretch · 6 Rotate · 7 Long click. Drag is 2 in one and 1 in the other. A handler must say which call it is reading.
- **A GETKEY drain does not drain touch** (§7). BayesTree's node page bracketed `WAIT(-1)` with key drains; the finger lift that opened the page could close it. The capped `MOUSE(1) == -1` drain goes before any wait that touch can satisfy.
- **`WAIT(-1)` gives up after about a minute** and returns −1 (Commands reference). It is the wrong hold for a page that must stay up through a lecture; `xxWaitAny()` is the right one.
- **`ans` is `Ans`** (§5): the lint found it in GfxProbe before the paste did. `K` used as the `MAKELIST` counter writes Home's K on every call. A LOCAL counter appears in 51 corpus programs, almost always with a constant expression; whether the expression can USE a LOCAL counter is untested, so **keep `K` until GfxProbe T19 passes**, then sweep. `G1`…`G6` are the graphics variables — do not use them as LOCAL names even in lowercase.
- **Self-numbered menus were in seven programs, not six** (TrendTest had been missed); all seven are fixed in the versions below. Version strings, companion-file names and file maps inside a program are references too and go stale with every rename — seven were stale.
- **What the Prime can draw that the fleet never used** (§6, new table): translucent `FILLPOLY_P`, blended and translucent `TRIANGLE_P`, the 3-D `TRIANGLE_P` mesh, the ten-argument scaled `BLIT_P`, a second finger in `MOUSE`, the `WAIT(-1)` gesture events. Documented and corpus-used, none verified by us. **GfxProbe beta 1** tests each one and writes the answers to `GP_LOG`; §6's table says what to fill in from it. Until then no fleet program uses them.
- **Open questions that GfxProbe also settles**: how many lines a MSGBOX shows (T13), whether `CHISQUARE_CDF` and `FISHER_CDF` take non-integer df (T11, the door to Gamma and Beta in StatDist), what `POISSON_CDF(λ, −1)` returns (T12), nine unverified glyphs (T14), and whether keys survive `WAIT(0.02)` (T15). A ten-line **LocalHeadProbe** settles whether PowerViz's `LOCAL pv_Name()` routine heads are legal.
- **The canonical footer** is CentralLimit's form (§13): comma-separated, spaces round `=`, dodger blue. Four other forms were in use.
- §8: a `from random import …` guard is a guaranteed fallback on this firmware, not a precaution — `random` is absent, `urandom` present. The `hpprime` drawing argument orders StudRangePy uses ran on the G2 and are recorded as observed.
- §14: rules 13 and 14 (version strings are references; the gate before any paste, `ppl_gate_v1.py`, with `ppl_check_v3.py`).

**What changed in v7e** (a search index for the library; no PPL rule changed):

- **The whole of `D:\HP-Prime` is now searchable in about a second** (box below, §14.11). `Library_Index.db` holds the text of every program and text file in all ~1,650 zips and the loose folders, every `.hpprgm`/`.hpappprgm` decoded (1,658 sources; 100 are compiled objects with no source, indexed by their strings), the text layer of every PDF (628 of 1,051 have one; the rest are scans), and the names of all ~67,000 files. `libsearch_v1.py` searches it; `library_index_build_v1.py` refreshes it incrementally. Build and search instructions are in `CLAUDE.md`.
- Three `.hpprgm` variants turned up while building it: the usual binary header + UTF-16LE source; plain UTF-8 text that merely has the extension (our own September device pulls); and objects with the `7C 61 8A B2` header but no UTF-16 source at all. `Decode-HPPrime.ps1` handles only the first.

**What changed in v7d** (fleet table completed; the exit review extended to the five programs that arrived on 9 October):

- §15 now lists GaltonBoard, TrendTest, TestChooser and DNAMixLR, which were committed to the repository on 9 October 2026 but had never been entered here, and marks CentralLimit as the app it is. All five are still untested on hardware.
- GaltonBoard beta 1a, TrendTest beta 1a and TestChooser beta 1a: every finger-lift drain goes through a capped `xxDrain()` (§7), and GaltonBoard and TrendTest return their summary line instead of printing it. DNAMixLR needed nothing (key-only waits, no trailing `PRINT`). All four already carried tagged helpers (`gb`, `tr`, `tc`, `dm`); `fleet_names_v1.py` over the whole fleet of 20 files: 0 collisions, 0 untagged.
- The masters of these four now live in `D:\HP-Prime` alongside the rest (until 11 October they existed only in the Project and the repository).

**What changed in v7c** (one new rule, device-found, and three loop rules from the fleet exit review, 10 Oct 2026):

- **All programs share ONE pool of routine names** (§5). Roger ran StudRange, hit a runtime error that opened the Program Editor, could not leave it, and ended up looking at a Burr3 screen; only a reset got him out. Five fleet programs defined `NiceNum`, nine defined `fmtp`/`FMTP`/`FmtP`, three `lngamma`, two `Drain`, `FMT` and `ShowHelp`. A call to a helper can land in another program's copy of the same name, whichever was compiled last. The User Guide's "a function without EXPORT is visible only inside its program" does not hold on the device; the library says the same (hummingbird1986: "the global namespace is flat and shared across every program on the device — name collisions between .hpprgm files are the main failure mode"; hp-prime-kit `ppl.global-namespace`, `ppl.compilation-order`). **Rule: every non-EXPORT routine carries the program's tag** (`sr_NiceNum`, `b3_fmtp`, or the `csName` / `cltName` style). `fleet_names_v1.py` checks every program against every other, ignoring case; it found 6 collisions in the fleet and 0 after the rename.
- **Read x and y from a touch list only after checking `SIZE`** (§7). `WAIT(-1)` hands back a list for a touch, and a finger lift can be a one-element list; `kk(2)` on it is a runtime error, which opens the Program Editor at the failing line — the "screen that listed the program". StudRange and BayesTree both did this.
- **A finger-lift drain gets a time limit** (§7). `REPEAT UNTIL MOUSE(1) == -1;` with no limit holds the program for ever if the touch reading sticks; `csDrain()` / `cltDrain()` give up after one second via `TICKS`.
- **Finish with `RETURN`, not `PRINT`** (§7), unless the program really has Terminal output to scroll. ChiTable now returns its summary line; Home shows it and no Terminal screen is left open.
- §14 rule 12 (run the fleet check before every paste); §15 lists the renamed versions, none of which has been re-run on hardware yet.

**What changed in v7b** (device confirmations from ChiTable's first runs, G2 and G1, 10 Oct 2026):

- **Soft keys work this way** (§6): draw the frame to G1, `BLIT_P`, then `DRAWMENU({...})` on the screen; read a tap with y >= 218 as key `MIN(6, IP(x / 53.4) + 1)`. The labels never produce a key code. Verified on both calculators.
- **Now in the confirmed-working list** (§3): file-level `LOCAL` state in a standalone program; `INPUT` with its label list taken from a string variable; `MAKEMAT` followed by element assignment into an `EXPORT`ed matrix; `CHISQUARE` (density), `CHISQUARE_CDF` and `CHISQUARE_ICDF` together; `CHAR(967)+CHAR(178)` for the chi-square glyph, `CHAR(8320)`/`CHAR(8321)` for subscript 0 and 1, `CHAR(215)` for the multiplication sign.
- §15: ChiTable beta 1j is tested on the G2 and the G1.

**What changed in v7a** (one observation added to §2):

- **CHOOSE numbers its items itself, and past 9 it uses letters:** items 10, 11 and 12 are labelled A, B and C on the Prime (Roger, 10 Oct 2026, ChiTable's menu). So menu strings should not carry their own numbers, and any on-screen reference to a late item should say "(A)", not "(10)".

**What changed in v7** (one new rule, device-found):

- **Built-in names are matched case-INsensitively** (§5). `LOCAL csR, csC, ...` at the top of ChiSquare beta 1a was rejected at paste time on the G2 with the cursor after `csC` — the parser read it as `CSC`, the cosecant. The program's own name, `ChiSquare`, was `CHISQUARE` (the density) and would have failed next. A routine prefix does not make a name safe: `csC`, `csR`-style names must be scanned against the command list ignoring case, and so must function names and EXPORT variables. `lint_ppl.py` and `ppl_check_v2.py` now do this for file-level LOCALs, EXPORT variables and function names (10 Oct 2026).
- §5's earlier note that `LOCAL fp` parses fine stands as observed, but it is now the odd one out; do not rely on it.
- §15: ChiTable beta 1b (the renamed ChiSquare) joins the fleet.

**What changed in v6** (paths only; no rule changed):

- The master folder is now **`D:\HP-Prime` on Rogers-HP**. The EliteOne died in early October 2026; its files were copied to D: on Rogers-HP, Roger's new main computer, and kept there for space (Roger, 6 Oct 2026). Every `C:\HP-Prime` below is now `D:\HP-Prime` (box above §1, §9a, §14.11).
- The count of zips at the top of the folder is corrected from "about 400" to **about 940** (938 on 3 Oct 2026, mostly from hpcalc.org).

**What changed in v5** (corrections only; no rule changed):

- The University of Delaware Python pages are **Mike Markowski's**. v4 wrongly credited them to "Mark Mitchell" (§9a).
- The box above §1 no longer calls `HPPrimeProgrammingUDelaware.pdf` the only Python document in the library. Streeter's book and a saved copy of Markowski's pages are both in `Community_Library\docs`.
- That PDF is not a ZIP of page images, as v4 said. The copy on Roger's computer is an ordinary 7-page PDF, printed from Markowski's page in January 2024, whose text layer is garbled.
- §9a now says where each Python source is saved in the library.

**What changed in v4:**

- The `LOCAL` rule is now 6 per line (§2).
- Every update gets a new version number, and stale copies are archived (§14.7).
- Search the whole library, not just the Project's 83 programs (box above §1, §14.11).
- Today's PyProbe findings are folded in: argv, matplotl, the module contents, MSGBOX, Terminal scrolling (§3, §7, §8, §9).
- Python's arrival date is corrected from HP's release notes (§8).

Working notes for writing PPL and MicroPython on the HP Prime. Everything here was found on hardware, not read in a manual — where a claim is inferred rather than observed, it says so.

**Verified on:** HP Prime G2 and G1, both running the **2026-09-09** firmware, plus the desktop Virtual Calculator (2.4.2, the same build; the whole fleet ran there on 16–17 Oct 2026, §16). Firmware matters more than it looks: glyph rendering and app-variable reachability have both proved version-dependent, so a "device-verified" claim is only verified on a stated build.

---

> ## Read this before writing code
>
> Not after. In one September session, four bugs were rediscovered the expensive way — the `STRING` mode, the FREEZE pause, the x-bar glyph, and the LOCAL limit — and all four were already written down here.
>
> Then: **search the whole library** for anything this file does not cover — with the index, not by unzipping: `python3 libsearch_v1.py WORDS` (or `-s "exact text"`, `-r REGEX`, `-n filename`) in `D:\HP-Prime` answers in about a second across every zip, program, decoded `.hpprgm` and PDF there. That means the `.txt` programs uploaded to the Project, plus everything in `D:\HP-Prime` on Roger's computer (Rogers-HP): the fleet, about 940 zips (mostly hpcalc.org), and `Community_Library` (see its `INDEX.md`). `<>` was avoided for a whole session as "unverified" when five corpus programs use it.
>
> Then: **read the uploaded reference PDFs.** Note that `HPPrimeProgrammingUDelaware.pdf` (Mike Markowski's University of Delaware page, printed to PDF in January 2024) has a garbled text layer — it will not turn up in a text search and has to be read as page images. It is not the only Python document in the library: Markowski's pages are also saved as HTML in `Community_Library\docs\markowski_udel\`, and Neil Streeter's *HP Prime Python Activities Book* is `Community_Library\docs\hpprime-python-activities.pdf`. §9a lists every Python source and where it is.

---

## 1 · Which language, and why

**PPL by default.** It is good at calculating, and the native `_P` graphics have no Python equivalent worth reimplementing. Anything that redraws on a keypress stays pure PPL.

**Python (MicroPython) when it makes a program faster, or supplies a needed feature PPL lacks** (Roger's rule, 1 Oct 2026). Compute-heavy engines get a real speed-up, because the math primitives are compiled C while PPL loops are interpreted. Examples are quadrature, root-finding and simulation. A measured case: StudRange's critical value takes about a minute in PPL (60-step bisection) and about 1.5 seconds in Python (secant, ~9 evaluations).

The counter-example matters as much. A live power visualiser with held-key stepping and four reshaded regions per frame gains nothing — its arithmetic is a handful of CDFs per redraw, and the bridge crossing would cost more than the computation. **Of nine programs in this fleet, one was worth converting.**

**The CAS for exact and symbolic answers, behind a fence** (v7g; Roger, 16 Oct 2026). A program's *engine* stays PPL (or Python) numerics, derived and verified off-device against SciPy. The CAS may add what only it can: exact fractions, integers of any size, closed forms, a derivation done live on the student's numbers, a limit. It is reached through ONE call routine per program, only on events, with the decimal answer as the fallback (§9b). Home capitals A–Z are built-in global reals; CAS lowercase names are symbolic; case matters.

State *why* in one line before splitting any project across languages.

## 2 · Hard limits

- **16 arguments** maximum on user function definitions *and* built-in calls. Pack into lists, unpack inside.
- **`CHOOSE` simple syntax caps at 14 options**; the list form `CHOOSE(var,"title",{...})` is unlimited.
- **`CHOOSE` numbers the items itself**, 1-9 and then A, B, C ... for items 10 and up (device, 10 Oct 2026). Do not number them in the strings, and refer to item 10 as (A) in messages and help text.
- **Never test `CHOOSE`'s return value for a specific number.** Initialise the index variable to 0, call `CHOOSE`, then test the index variable itself. Cancel leaves it 0.
- **`INPUT`'s first argument must be a list of variable NAMES**, written back in place. Value lists give "Invalid Input".
- **Never `INPUT` into a function parameter.** Copy to a `LOCAL`, `INPUT` that, assign back. Parameters as targets fail silently.
- **`LOCAL` statement size: 6 per line. That is the rule** (Roger, 1 Oct 2026). For the record:
  - 7 has been seen to work: BayesTree ships three 7-variable lines.
  - The documented figure was 8.
  - The true ceiling has never been established.
  - New code uses at most 6. Split longer lists across several `LOCAL` lines.
- **`LOCAL` inside `IF`/`CASE` is genuinely rejected.** Hoist it to the top of the function, splitting across several lines.
- **A PPL function cannot modify its caller's variables.** Parameters pass by value. Shared state therefore lives in exported globals, which means every write path to that state must be audited together.
- **Parameter names must not collide with built-in FUNCTION names** (`FP`, `IP`, `LN`, `RE`, `IM`, `SIGN`…). `fp` as a parameter is a syntax error even though `LOCAL fp` parses fine — the parameter parser is stricter.
- **Programs with parameters get an auto-generated argument form** from the catalog. Menu-driven tools take zero arguments and hold defaults internally; plot explorers launched from Home with values keep theirs.
- **`.hpprgm` is binary** (UTF-16LE plus header). Distribute as `.txt` and paste into the Connectivity Kit editor. UTF-8 import can append stray CJK characters at the end — harmless, delete them.

## 3 · Command truths

- **`STRING(value, mode, digits)`: mode 1 is Standard and IGNORES the digits argument.** `0.6826894921` stays full length no matter what you ask for. **Fixed decimals need mode 2.** Easy to miss because most values still look right; only long decimals expose it, and it silently disables computed decimal counts on axis labels. Sweep every `STRING` call before delivery.
- **Fixed decimals turn scientific below 10⁻ᵈ** (emulator, round 2, 17 Oct 2026). `STRING(x, 2, d)` prints the scientific form whenever 0 < |x| < 10⁻ᵈ, with U+1D07 (ᴇ) for the E: `STRING(0.096,2,1)` = `"9.6ᴇ−2"`, `STRING(0.0999,2,1)` = `"1.0ᴇ−1"` (it does not round to 0.1 first), `STRING(0.05,2,1)` = `"5.0ᴇ−2"`, `STRING(0.0004,2,3)` = `"4.000ᴇ−4"`. **Both minus signs are CHAR(8722)** (U+2212), never ASCII 45: the exponent's (CASProbe beta 1c T43b read the codes 57 46 54 7431 8722 50) and a negative number's leading one (T01: `STRING(-2.5)` = 8722 50 46 53). So test for the scientific form with `INSTRING(s, CHAR(7431)) > 0`, never by matching the text; beta 1c's T43b matched `"9.6" + CHAR(7431) + "-2"` and reported a false FAIL (fixed in beta 1d). At or above 10⁻ᵈ it is fixed (`STRING(0.1,2,1)` = `"0.1"`, `STRING(0.001,2,3)` = `"0.001"`), and `STRING(0,2,3)` = `"0.000"`. Fixed output also holds at most 12 significant digits (`STRING(123456789012,2,2)` = `"123456789012"`, no decimals) and is scientific from 1E12 (`STRING(1E15,2,0)` = `"1ᴇ15"`). **The safe form is `STRING(ROUND(x, d), 2, d)`**: the rounded value is either 0 or at least 10⁻ᵈ. For a probability, use the program's "< 0.001" style instead of printing 0.000.
- **12-digit cancellation: compute upper tails as lower tails** (FDAES v3.8 on the emulator, 17 Oct 2026; the fleet review, 19 Oct). Home reals carry 12 significant digits, so once a tail is below about 5E−13, `1 − NORMALD_CDF(m, s, t)` and `1 − CHISQUARE_CDF(df, x)` are exactly 0, and a page prints "0.000" beside "< 0.001". The identities the fleet uses:
  - normal: `NORMALD_CDF(m, s, 2*m − t)`;
  - chi-square with 1 df: `2*NORMALD_CDF(0, 1, −(x^0.5))`; with 2 df: `EXP(−x/2)`;
  - Beta: the mirrored distribution; every other family: its own right-tail formula (StatDist's `st_sf`);
  - a difference of two CDFs near 1: its mirror, `F(2m − a) − F(2m − b)` (NormExplorer's `ne_Btw`);
  - a right-tail quantile: `−NORMALD_ICDF(0, 1, α)`, never `NORMALD_ICDF(0, 1, 1 − α)`, which becomes `ICDF(1)` for a tiny α.
  `NORMALD_CDF(0, 1, −8)` itself keeps its digits on the calculator: 6.22096057427E−16 (typed on the G1, 20 Oct 2026).
- **Alternating sums cancel; build probabilities from positive terms** (DNAMixLR beta 3c, 19 Oct 2026). An inclusion–exclusion sum of large terms with alternating signs keeps none of its 12 digits once the answer is much smaller than the terms. Rewrite it as a sum or recursion of non-negative terms. **Overflow** is the same family: `(1 + (x/S)^C)^(K+1)` passed 1E500 in Burr3; work in logs (`EXP(LN(...))`).
- **A trailing-zero stripper must check for a decimal point first** (ScatterLab beta 2c). `STRING(140000000000, 2, 1)` has no "." (12 significant digits at most), so stripping zeros turned it into "14". Confirmed on the G1 (20 Oct 2026): `STRING(1.4ᴇ9,2,1)` = `"1400000000.0"`, `STRING(1.4ᴇ10,2,1)` ends in ".0", `STRING(1.4ᴇ11,2,1)` = `"140000000000"`, `STRING(1.4ᴇ12,2,1)` = `"1.4ᴇ12"`.
- **An inverse CDF at p = 0 or 1, and an overflow, return ±∞, not an error** (typed on the G1, 20 Oct 2026): `NORMALD_ICDF(0,1,1)` = ∞ and `(1.17E6)^101` = +∞. `IFERR` does not see them, so the ∞ flows into the next sum and onto the screen. Clamp a probability into (0, 1) before any `_ICDF`, and work in logs where a power can pass 1E499 (§3, Burr3).
- **`FOR i FROM 2 TO 1 DO … END;` runs zero times** (typed on the G1, 20 Oct 2026: Home shows 0 and nothing prints). Four fleet loops rely on it; ErrorRate beta 1d's explicit guard is now belt and braces.
- **`INSTRING(s, sub)` with `s = ""` is a run-time error, "Invalid input"** (emulator, round 2). `INSTRING("abc", "")` = 1 and `INSTRING("abc", "z")` = 0. So never call INSTRING on a string that can be empty without `IF DIM(s) > 0` first — a CAS answer that failed, a string cut down to nothing, an empty field. A replace loop must stop when the text is used up (§9b has the shape) and must return at once for an empty pattern, which INSTRING finds at position 1 for ever.
- **`LEFT(s, 0)` and `RIGHT(s, 0)` return the WHOLE string**, not `""` (hp-prime-kit measured it on an older build; confirmed on 2026-09-09). A computed count that can be 0 needs a guard (`IF k > 1 THEN … LEFT(s, k - 1)`). **`MID(s, 0, n)` is "Bad argument type"**: MID's start is 1-based. `MID(s, past the end)`, `MID("", 1, 1)` and `MID(s, i, 0)` are all `""`.
- **`AND` and `OR` skip their right side once the left side decides** (typed in Home, round 2): `0 AND INSTRING("", "a")` gives 0 and `1 OR INSTRING("", "a")` gives 1, with no error, although the right side alone is "Invalid input". Measured in Home, not inside a program; the round-2 fix versions guard with a nested `IF DIM(s) > 0 THEN … END` all the same, so nothing in the fleet depends on it.
- **`ROUND` rounds halves away from zero**, and a negative value that rounds to zero prints without a sign: `STRING(ROUND(-0.004, 2), 2, 2)` = `"0.00"`, not `"-0.00"` (typed in Home, round 2). The harness, which rounds in Python, can show a `-0.0` the Prime does not.
- **`CHISQUARE(n,x)` is the DENSITY**, not a tail. And the upper tail is NOT `1 - CHISQUARE_CDF(n,x)` (v7p): that difference is exactly 0 on the Prime's 12 digits once the tail is below about 5E-13, a χ² above about 52 at 1 df. Use the forms that keep their digits: at 1 df, `2 * NORMALD_CDF(0, 1, -(x^0.5))`; at 2 df, `EXP(-x/2)`; at any df, the finite sums of positive terms in §11 (TrendTest beta 3f's `trUpper`). `1 - CHISQUARE_CDF` is fine only where the p is large enough to print, and it is cheapest to never write it.
- **`<>` is valid for not-equal** — corpus-confirmed in CHOOSE_R, Hammurabi and PONG. No need to restructure around it.
- **Confirmed working:** `NORMALD` / `NORMALD_CDF` / `NORMALD_ICDF`, `STUDENT(_CDF)`, `FISHER(_CDF)`, `BINOMIAL(_CDF)` including the 4-argument form, `POISSON(_CDF)`, `COMB`, `IFTE`, `MAKELIST`, `CONCAT`, `RANDOM`, `PIXON_P`, `TYPE` (6 = list), `SIZE`, `CHAR`, `ROUND(v, places)`, `MOUSE`, `VIEW`, `mean`, `stddev`, `variance`.
- **Also confirmed (ChiTable, G2 and G1, 10 Oct 2026):** `CHISQUARE` (the density) with `CHISQUARE_CDF` and `CHISQUARE_ICDF`; `MAKEMAT(0, r, c)` followed by `M(r, c) := v` on an `EXPORT`ed matrix; `DRAWMENU({...})` for soft keys (§6); `INPUT({v}, "title", {lbl}, {help})` where `lbl` is a string variable built by concatenation; file-level `LOCAL` variables shared by every routine in a standalone program; `DIM`, `LEFT`, `MID` on strings.
- **Do not exist:** `GEOMETRIC*` — compute p(1−p)^(k−1) by hand. `LNGAMMA` outside the CAS — carry a Lanczos helper, or use Python's `lgamma` and delete it.
- Prefer native `NORMALD_ICDF` to any hand-rolled inverse normal.
- **`MSGBOX` shows 5 lines.** A 6th line was lost (PyProbe beta 1, 1 Oct 2026); ten lines showed lines 1–5 (GfxProbe T13, emulator, 17 Oct 2026). Keep message boxes to 5 lines; put longer output on a screen of your own.
- **Whole-number df only, for chi-square and F CDFs and quantiles** (GfxProbe T11 and Home checks, emulator, 17 Oct 2026). `CHISQUARE_CDF(2.5, 3)`, `CHISQUARE_ICDF(2.5, 0.5)`, `FISHER_CDF(2.5, 7.5, 2)` and `FISHER_ICDF(2.5, 7.5, 0.5)` are "Invalid input". The densities `CHISQUARE(2.5, 1)` (0.281348225763) and `STUDENT(2.5, 1)` take any df, and so do `STUDENT_CDF(2.5, 1)` (0.797969486361) and `STUDENT_ICDF(2.5, 0.9)` (1.7302509288); all match SciPy to 12 digits. For a fractional chi-square or F df use your own incomplete gamma or beta (StatDist v2.7b's `st_gammaP` / `st_betaI`).
- **`POISSON_CDF(λ, k)` with k < 0 is "Invalid input"** (T12), not 0. Guard the lower bound of a "between" sum.
- **`BINOMIAL` and `BINOMIAL_CDF` take (n, p, k) only** (GfxProbe T20, CASProbe T42): `BINOMIAL(10, 0.3, 2)` = 0.233474 = SciPy; (n, k, p) is an error. HP's Commands.pdf prints (n, k, p); it is wrong for this firmware.
- **Also confirmed on the emulator, 17 Oct 2026:** `MAX` and `SORT` on a list (T10); `MAKELIST` with a LOCAL counter, in both the constant and the counter-reading forms, leaving Home's `K` untouched (T19); `TICKS` (a `WAIT(0.1)` read 107 ms, T18); `IFTE`; a `LOCAL name(args)` routine head (LocalHeadProbe).

## 4 · Input fields

- **There is no blank input field, and the string workaround fails.** A PPL real always holds a value, so a numeric `INPUT` always shows one. A string variable initialised to `""` does *not* give an empty box — the Prime renders the quotation marks as editable text, and deleting them to type a number is a syntax error. *(Device-verified.)*
- **House default is 0**, unless 0 is illegal for that field — areas, α, confidence levels — where the conventional value goes in: 0.90, 0.05, 0.95.
- **Defaults are pedagogy, not placeholders.** A prefill computed from other session values reads as a stray number and generates a bug report. This happened: `x := μ + σ` with μ=22, σ=4 opened a solver at 26 and looked broken. Use flat constants, or state the rule in the field's help line.
- **Guards should teach.** "σ must be positive" is adequate. "These values give σ = −9.18; the sign of z must match the sign of x − μ" is better, because that *is* the student's error.

## 5 · Reserved words and characters

- **Scan every new name** against PPL keywords: `STEP` (use `stp`), `TO`, `FROM`, `DO`, `OR`, `AND`, `MOD`, `e`, `Re`. The syntax error lands at the usage line.
- **Scan every new name against the BUILT-IN COMMANDS too, ignoring case.** Device-found 10 Oct 2026 (G2, 2026-09-09 firmware): `LOCAL csC` is a syntax error at paste time because `csC` is `CSC`, the cosecant — the editor's cursor lands right after the offending name. A program named `ChiSquare` is `CHISQUARE`, the density function. This applies to LOCALs at file level and in functions, to EXPORT variables and to function names. The routine-prefix convention (`cs…`, `tr…`) is no protection when the prefix plus one letter spells a command: `csC`, `csR` (fine today, but rename on sight), `tcE`… The lint tools check this now; run them before every paste. (`LOCAL fp` was once seen to parse, which contradicts this; treat that as the exception and never rely on it.)
- **Write exponent literals with a capital E.** Corpus code uses `1E10` and `-1E10`; lowercase `1e-9` is unverified, and lowercase `e` is a reserved name. Or just write the decimal out.
- **Never put a `//` comment inside an open bracket.** ChiTable beta 3b had two comment lines inside the list of a multi-line `CHOOSE(rmI, "Results menu", { … })`; the Prime's editor reported "Syntax Error" there, and the same file with those two lines removed compiled and ran (emulator, round 2, 17 Oct 2026). A comment after the bracket closes on the same line is fine (NormExplorer beta 42 has two and ran). Put the comment above the statement. `ppl_check_v4.py` reports it as E12, a hard error in `ppl_gate_v1b.py`; the harness parses such a file without complaint, so the check is the only guard.
- **Avoid bare single-letter lowercase identifiers.** `x` is the CAS's symbolic variable, `i` the imaginary unit, `e` already listed. *Honesty note: a suspected stale-CAS-`x` leak was tested and DISPROVED — CAS `x` was 0. This is cheap insurance, not a diagnosed cause; do not cite it as one.*
- **House convention: prefix every local with a routine tag** — `zsX`, `ndPY`, `pcA`, `awlo`. Makes greps and renames tractable.
- **x-bar is `CHAR(57344)`** (U+E000); **p-hat is `CHAR(57345)`** (U+E001). Single precomposed glyphs in HP's private-use area — they position themselves and scale with the font. **The combining macron U+0304 does NOT stack**; it renders as its own character to the *right* of the x. A hand-drawn `LINE_P` bar also works but needs per-font pixel tuning. Use the glyph.
- **Subscript digits render:** `CHAR(8322)` = subscript 2, paired with `CHAR(956)` = μ for labels like μ₂.
- **Symbols, not spelled-out names, in on-screen text** (Roger, 20 Oct 2026; v7n). χ² (`CHAR(967)+CHAR(178)`), ² (178), √ (8730), ≥ ≤ ≠ (8805, 8804, 8800), ± (177), × (215), → (8594), ∞ (8734), θ ρ λ (952, 961, 955), α β μ σ φ, subscripts (8320–8322), x̄ and p̂ (57344, 57345). All render on the 2026-09-09 firmware (GfxProbe T14 and pages already in use). π (960), η (951) and τ (964) are on screen since 20 Oct and still to be seen on a calculator. Never in text the CAS receives, never in a Home variable's name; "+/-" stays where it names the keys. A literal glyph and its `CHAR()` build are the same character on screen. **Seven programs keep their code pure ASCII** (BiNorm3D, ChiTable, DNAMixLR, ErrorRate, FDAES, ScatterLab, and CICatcher's code): there a glyph is built, `("P(age " + CHAR(8805) + " 18)")`, never typed. The first pass of the sweep missed that and typed them; `ascii_fix` rebuilt them, and the gate and the verify scripts ran again.
- Characters taken from the on-device **Shift-Chars menu are pre-verified by construction**.
- **`EXPORT` on a helper publishes it in the catalog.** Keep helpers non-`EXPORT`.
- **`ans` is `Ans`, `ci` is `Ci` (the cosine integral), `G1`…`G6` are the graphics variables.** All three were caught by the checkers in October 2026 before a paste; the first two are the case-insensitive rule above biting on ordinary English words, the third would shadow a GROB. Run `ppl_check_v3.py` (or the whole gate, `ppl_gate_v1.py`) on every file; it reads `HP_Prime_Builtin_Names.txt`.
- **`K` as the `MAKELIST` counter writes Home's K** on every call (ChiTable, GaltonBoard, CentralLimit, DNAMixLR, NormExplorer). A LOCAL counter (`MAKELIST(0, ib, 1, n)`) appears 162 times in 51 corpus programs, nearly always with a constant expression; the fleet also writes `MAKELIST(K*0.5, K, …)`, where the expression reads the counter. GfxProbe T19 (emulator, 17 Oct 2026) showed a LOCAL counter works in both forms and leaves Home's K alone: **new code uses a LOCAL counter**; the older programs' `K` is harmless and changes only when a program is touched for another reason.
- **Non-`EXPORT` does not make a helper private.** Device-found 10 Oct 2026: all programs' routines live in one pool, matched ignoring case, so StudRange's `NiceNum` and Burr3's `NiceNum` were the same name to the calculator, and a call from one program ran the other's code (a runtime error, the Program Editor opening on the other program, a reset). **Every non-`EXPORT` routine carries the program's tag**: `sr_NiceNum`, `b3_fmtp`, `es_Module_Table2x2`, or the glued style `csGrid`, `cltSample`. Before any paste, run `python3 fleet_names_v2.py *.txt` in `D:\HP-Prime`: it lists every routine name defined in more than one program (COLLISION), every helper that does not carry its own file's tag (UNTAGGED), any file mixing two tags (MIXEDTAG) and every name that matches a built-in when case is ignored. (v1 accepted any short prefix as a tag and passed StatDist's `calc_*` stubs; v2 works out each file's tag from its helpers.) The app hooks `START`, `Plot`, `Symb`, `Num`, `Reset`, `Info` keep their fixed names.

## 6 · Graphics

- Screen is 320×240, origin top-left, y increases **down**. The y-flip: `py := BOT - IP(y/ymax*H)`, then clamp.
- **Compose off-screen and blit once.** `DIMGROB_P(G1,...)`, draw every pass to `G1`, then one `BLIT_P(G0,0,0,G1)`. Drawing straight to `G0` tears visibly. Miss one `G1` argument and that element flickers alone — a useful diagnostic.
- **Shading must iterate pixel columns**, not math samples. Sample loops leave white gap columns; this bit two programs before the rule stuck. Iterate pixels, solve for x.
- **Cache the density — for EVERY curve, not just the first.** If three passes need the same pdf, evaluate it once per pixel column into a list. The trap is doing this for the main curve and forgetting the comparison curve: a second curve read by both an overlap fill and a trace costs two `NORMALD` calls per pixel per frame — 544 on a 272-pixel plot, on top of the main curve's 273. That is the one per-frame cost a G1 can actually feel during a live drag.
- **Precompute anything needed twice in the same frame.** Histogram bar heights were computed once to widen the y-scale and again to draw. Build the array first, then use it in both places.
- **Verified GETKEY codes, the only ones to trust:** Esc=4, Left=7, Right=8, Up=2, Down=12, Enter=30, +=50, −=45, 0=42. Route anything else through Enter → `CHOOSE`.
- **Soft keys, device-verified (ChiTable, G2 and G1, 10 Oct 2026):** compose the frame in `G1`, `BLIT_P(G0, 0, 0, G1)`, then `DRAWMENU({"Edit", "Values", "Clear", "", "Cancel", "Run"})` — it paints the screen, so it goes after the blit and is repeated every frame. A tap with `y >= 218` is a soft key; the slot is `MIN(6, IP(x / 53.4) + 1)` (CHOOSE_R's and LibMenu's geometry). The labels never produce a `GETKEY` code, so keep hardware keys as shortcuts for keyboard-only use. **This is for a `GETKEY` + `MOUSE` polling loop.** Under `WAIT(-1)` a strip tap arrives only as a type-3 click (§7).
- **`TEXTOUT_P` returns the x just past the text it drew.** The corpus relies on it (BlackJack, codeviewer), and BayesTree beta 8c lays out its two-test breadcrumb that way (each arrow at the x the number before it returned); on the emulator, round 2, the three numbers and two arrows sat end to end with nothing overlapping. Use the return value to place the next piece of a mixed line instead of estimating widths.
- **Touch works alongside keys.** Poll both: `REPEAT exK := GETKEY; exM := MOUSE; UNTIL exK > -1 OR SIZE(exM(1)) > 0;`. `m(1)` is the first finger; elements 1 and 2 are x and y. Put the plot box coordinates in shared constants so the touch handler and the drawing code cannot disagree.
- **`BLIT_P(G0, G1)` with two arguments** copies the whole GROB; StudRange used it through beta 11 on hardware. The four-argument `BLIT_P(G0, 0, 0, G1)` is the fleet idiom; both work.
- **Dotted and dashed lines do not exist in `LINE_P`.** Draw them: `FOR i FROM a TO b STEP 4 DO PIXON_P(i,y,color); END;`. The one legitimate home of the `STEP` keyword.
- **`ARC_P` rings do not make a solid disc.** Concentric rings at r = 3, 2, 1 plus the centre pixel leave the diagonals white; each dot reads as ⊕ (GfxProbe T09, emulator, 17 Oct 2026; GaltonBoard's pegs and balls). Draw a small disc as overlapping `RECT_P` bars (GaltonBoard beta 3b: three bars for r = 3, two for r = 2, pixel-exact) or one `FILLPOLY_P` polygon.
- **Nice axis ticks** (Heckbert): step 1/2/5×10^e, decimals `MAX(0,-FLOOR(LOG(stp)))`, start `CEILING(xmin/stp)*stp`.
- **`NiceNum` belongs on interactive step sizes too.** Arrows that add σ/4 give 3.75 on N(100,15); `NiceNum(σ/4)` gives 5. Snap to the grid — `(FLOOR(v/stp + 1e-9) + 1) * stp` — so an odd starting value like 847 is pulled onto 850 rather than carrying its oddness forever.
- **Auto-scale the window, and check BOTH axes before drawing a reference curve.** Horizontal fit is not enough: N(0,1) peaks at 0.3989 and a σ=7 curve at 0.057, so the reference clips flat and reads as a grey artefact box. Suppress what cannot be drawn interpretably — **and say on screen that you have**, or the toggle appears broken.
- **Freeze the window inside a live explorer.** If it tracks μ, the bell sits centred forever and moving the mean looks like nothing happening. Lock on entry, offer a re-centre key.
- **Freeze the x-window, but NOT the y-scale.** σ changes the peak height, so a frozen y-scale either clips a grown curve or leaves a shrunk one floating low. Refit the height on σ changes only — μ does not affect a normal's peak height.
- **Corner readouts collide with plot annotations.** A label at a curve feature lands wherever that feature is; a fixed text block does not move aside, and at 320×240 there is nowhere to slide either. Suppress whichever matters less in that mode.
- **Check vertical gaps when adding a line to an existing text block.** 14 px spacing tolerates one insert; 6 px overlaps.
- Hand-placed layouts: audit box edges against line endpoints numerically, and expect one or two pixel-nudge rounds on device.


**Documented and corpus-used; the Status column is GfxProbe beta 1 on the Virtual Calculator, 17 Oct 2026** (the same firmware as the calculators; a held key and two fingers need the hardware).

| Capability | Call | Documented behaviour | Corpus | Status |
| --- | --- | --- | --- | --- |
| Translucent fills | `FILLPOLY_P([G], {{x,y},…}, color, alpha)`, alpha 0–255; a flat `{x1,y1,x2,y2,…}` list also appears in two programs | fills a polygon with transparency | 91 files | **works**, both list forms, alpha 110 (T01–T03) |
| Translucent / gradient triangles | `TRIANGLE_P([G], x1,y1,x2,y2,x3,y3, c1,[c2,c3],[alpha])` | three colours blend between the vertices; alpha | 90 files | **works**: one colour, a smooth three-colour blend, alpha 128 (T04–T06) |
| 3-D surfaces | `TRIANGLE_P([G], points, triangles, {rotmat or −1, "N", eye or −1, {xmin…zmax}}, [zstring])`, points a matrix `[x y z colour]`, triangles a matrix of point indices; `TRIANGLE_P(G)` returns the z-buffer string | a whole mesh in one call with rotation, perspective and depth clipping | Advanced Graph 3D, 3ddrawing | **drew nothing** with our control list (T07); unresolved, unused (BiNorm3D draws with LINE_P) |
| Zoom by copying | `BLIT_P(G0, dx1,dy1,dx2,dy2, G1, sx1,sy1,sx2,sy2)` | stretches the source rectangle into the target rectangle | 180 files | **works**, exactly 2× (T08) |
| Two fingers | `MOUSE` → `{ {x,y,x0,y0,type}, {x,y,x0,y0,type} }`, one list per finger, empty when up | non-blocking | 427 files | `MOUSE` returns 2 lists (T16); the second finger needs hardware |
| Gesture events | `WAIT(-1)` → `{type, x, y, [dx, dy]}` | 0 Down · 1 Move · 2 Up (no x,y) · 3 Click · 5 Stretch · 6 Rotate (angles in 1/32 circle) · 7 Long click (1 s) | WaitLab (hpcalc) | **0, 1, 2, 3 and 7 seen** (T17); 2 is `{2}`; values are integers. 5 and 6 need two fingers |

WaitLab's observed sequences (firmware 5447/6030, 2014; **the strip and tap sequences re-confirmed on 2026-09-09 by MenuTapProbe, 17 Oct 2026**): a tap on the menu strip (y ≥ 219) arrives as `{3,x,y}` only; a tap elsewhere as `{0,x,y} {2} {3,x,y}`; a drag as `{0,x0,y0} {1,x1,y1}… {2}`; a long touch inserts `{7,x,y}` after the press; a flick ends `{1,65535,y}`; a stretch is `{0,a} {0,b} {5,…,dx,dy}… {2}`; a rotate `{0,a} {0,b} {6,angles…} {2}`.

What these unlock once probed: a shaded region as one translucent polygon instead of 272 vertical `LINE_P` fills (and α/β/power regions that visibly overlap), a bivariate normal surface rotated with a finger, pinch-to-zoom on any plot, long-press as "what is this?", a two-finger spread to set an interval width on the axis.

## 7 · Waiting for a keypress

**`FREEZE` is not a pause.** It only suppresses the screen refresh when the *program terminates*. Mid-program it does nothing: a result panel followed by `FREEZE` draws and is instantly repainted by the next `CHOOSE`, and the user reports "it goes straight back to the menu."

**`UNTIL k == -1` and `UNTIL k > -1` look alike and do opposite things.** The first drains and falls through instantly; the second blocks. A wait loop written with the wrong one is a silent no-op.

**Drain, wait, drain.** A keypress left behind by `INPUT` or `CHOOSE` satisfies the next wait loop and skips the screen you just drew:

```
REPEAT k := GETKEY; UNTIL k == -1;   // drain stale
REPEAT k := GETKEY; UNTIL k > -1;    // wait for real
REPEAT k := GETKEY; UNTIL k == -1;   // drain that one
```

**The key-help footer must match what the keys actually do.** Live arrows exist only in an explorer; on a result view any key returns. Advertising arrows there invites a press that loses the plot. Drive the footer from a state flag.

**The Terminal can only be scrolled after the program ends.** While a program waits in a `GETKEY` loop, it takes every key, the arrows included, so arrows only move the program on.

- End the program with a `PRINT`. The Terminal then stays open, and Up/Down scroll it (User Guide, PRINT entry).
- Del erases the Terminal, so warn the user.
- Its scroll bar does not respond to touch.

Verified with PyProbe beta 2a, 1 Oct 2026. For output the user must read while the program is still running, draw your own scrolling screen, as PyProbe beta 2b does.

**But a program with nothing to scroll should end with `RETURN`, not `PRINT`.** A trailing `PRINT` leaves the Terminal on screen after Quit, and the user has to press a key to get back to Home — it reads as "the program did not exit cleanly" (Roger, 10 Oct 2026). Return the summary as a string instead (`RETURN "ChiTable: " + ...`): Home shows it in the history and nothing is left open. StatDist and EpiStats already end this way.

**Touch lists from `WAIT(-1)`: check `SIZE` before reading x and y.** `WAIT(-1)` returns a key code, or a list for a touch. The list is `{type, x, y}` for a press (type 0) or a drag (type 1), but a finger LIFT can arrive as a one-element list, and `kk(2)` on that is a runtime error. The error dialog opens the Program Editor at the failing line, and from there the only way back was a reset (StudRange, 10 Oct 2026). The safe shape:

```
kk := WAIT(-1);
IF TYPE(kk) == 6 THEN                 // a touch
  tx := -1; ty := -1;
  IF SIZE(kk) >= 3 THEN
    IF kk(1) == 0 THEN tx := kk(2); ty := kk(3); END;   // a new press only
  END;
  ...hit-test tx, ty; -1 matches nothing...
END;
```

**Soft keys under `WAIT(-1)` arrive as type 3, and only as type 3** (MenuTapProbe beta 1, emulator, 17 Oct 2026). With `DRAWMENU` on screen, a tap on the strip gives one event, `{3, 78, 230}`: no press and no lift. A tap above the strip gives `{0, x, y}`, `{2}`, `{3, x, y}`. BayesTree beta 7 and StudRange beta 15 read the strip from a type-0 press, so their soft keys did nothing. The shape (BayesTree beta 8b):

```
IF kk(1) == 3 AND SIZE(kk) >= 3 THEN
  IF kk(3) >= 218 THEN slot := MIN(6, IP(kk(2)/53.4) + 1); ... END;   // a soft key
  // type 3 above the strip is the tail of a press already handled: ignore it
END;
```

When a view closes on a type-0 press, that tap's `{2}` and `{3}` are still queued for the next `WAIT(-1)` loop. If the tap was on the footer, the next loop sees a soft-key click. Remember the closing tap and skip one matching type 3 (BayesTree 8b's `btTL…`, StudRange 15a's `srTL…`).

**Three more facts from round 2** (emulator, 17 Oct 2026):
- **The strip is "the menu" for the rest of the run.** BayesTree's ROC view draws no soft keys, but the tree had drawn its DRAWMENU before it opened; a tap on the view's footer (y ≥ 218) still arrived only as `{3, x, y}`, so a view that closes on a type-0 press outside its plot ignored it. Read y ≥ 218 from type 3 in every `WAIT(-1)` loop of a program that ever drew a menu — as a soft key on a screen that shows them, as "back" on one that doesn't.
- **A tap read through `MOUSE` leaves nothing for `WAIT(-1)`.** BayesTree 8b and StudRange 15a put the closing tap of a page held by `xxWaitAny` on their stale-click list, in case its click followed; none did, so the list waited for the next real tap at that spot (±2 px) and skipped it. Closing the 2×2 view on the footer at ROC's spot and then tapping ROC: the first tap did nothing.
- **A queued event comes back at once.** So the stale test is: the click matches the next expected spot **and** `WAIT(-1)` returned it within 100 ms of being called (`TICKS` before and after). A later tap at the same spot is the student's. BayesTree beta 8c and StudRange beta 15b do this; a hardware run still has to show whether a MOUSE-read tap ever leaves a click there.

**`WAIT(-1)` hands back integers.** `STRING()` prints them in hex (`#3C:-16h` for 60). Arithmetic and comparisons are unaffected; add `0.0` before printing.

**A GETKEY drain does not drain touch, and `WAIT(-1)` times out.** BayesTree beta 5 held its node page with `WAIT(-1)` between two `GETKEY` drains; the finger lift from the tap that opened the page is a touch event, so it could satisfy the wait at once, and after about a minute with no event `WAIT(-1)` returns −1 and the page closes by itself. Hold pages with `xxWaitAny()` — drain keys AND the capped `MOUSE` drain, poll `GETKEY` and `MOUSE` together, drain again.

**`MOUSE` and `WAIT(-1)` number their event types differently** (Commands reference, 16 Oct 2026). `MOUSE` list, fifth element: 0 New · 1 Completed · 2 Drag · 3 Stretch · 4 Rotate · 5 LongClick. `WAIT(-1)` list, first element: 0 Down · 1 Move · 2 Up · 3 Click · 5 Stretch · 6 Rotate · 7 Long click. A pinch is 3 in one and 5 in the other; a drag 2 and 1. Say in the comment which table a handler reads.

**Give a finger-lift drain a time limit.** `REPEAT UNTIL MOUSE(1) == -1;` waits for the finger to leave the screen. If the touch reading sticks (PrimeSUD measured a phantom touch at (2147483647, 0) after a `GETKEY` landed on a finger lift, on the Python side), that loop never ends and the program is frozen with no way out but a reset. Put the drain in one helper and cap it:

```
csDrain()
BEGIN
  LOCAL drT;
  drT := TICKS;                                  // milliseconds
  REPEAT UNTIL MOUSE(1) == -1 OR TICKS - drT > 1000;
END;
```

`TICKS` (no parentheses) is the millisecond clock; TowerOfHanoi and Solitaire in the library use it the same way. ChiTable beta 1k, CentralLimit beta 1a and NormExplorer beta 40 drain this way. The key-only waits (`UNTIL kk > -1`) in the older programs are not a hang — any key leaves them — so they were left alone.

## 8 · MicroPython: getting it running

**The interpreter is MicroPython 1.9.4** — confirmed by `sys.implementation` on a G2 with the 2026-09-09 firmware. That release's documentation was last updated December 2018 and tracks CPython 3.4. **Check the 1.9.4 docs, not the current ones.** Most of the quirks below follow from this one fact.

**Python arrived in firmware build 2.1.14566, released 2021/04/28** (HP's release notes, "Add Python app").

- It did not arrive in 2.1.14181. That build is dated 2018/10/16 in the same notes, and it has no Python at all, though it is sometimes quoted.
- v3 had the build as 14567 and that date as November 2018. Both are corrected here.

**What is in each module.** PyProbe beta 2, `dir()` on the 2026-09-09 emulator, 1 Oct 2026. `sys.implementation` = micropython (1, 9, 4).

- **Present:** `math`, `cmath`, `urandom`, `hpprime`, `arit`, `linalg`, `matplotl`, `graphic`, `cas`, `gc`.
- **Absent:** `random` and `time`. Also **`os`**: `import os` fails in a `#PYTHON` block. HP's 2.4.2 notes mention `os.read` fixes; perhaps `os` exists only inside the Python app. That is untested.
- **`urandom`:** `random()`, `uniform()`, `randint()`, `randrange()`, `choice()`, `getrandbits()`, `seed()`.
- **`math` extras:**
  - Present: `erf`, `erfc`, `lgamma`, `gamma`, `log2`, `log10`, `expm1`. `erf` gives the normal CDF directly.
  - Missing: `fsum`, `isclose`, `factorial`, `comb`.
- **`linalg`:** `det`, `inv`, `solve`, `rref`, `eig`, `eigenvects`, `transpose`, `mul`, `dot`, `cross`, `fft`, `ifft`, `linspace`, `arange`, `matrix`, `zeros`, `ones`, `eye`, `identity`, and polynomial helpers. That is enough for regression and ANOVA without hand-written matrix code.
- **`graphic`:**
  - Drawing: `draw_line`, `draw_rectangle`, `draw_filled_rectangle`, `draw_circle`, `draw_filled_circle`, `draw_arc`, `draw_filled_arc`, `draw_polygon`, `draw_filled_polygon`, `draw_string`, `draw_pixel`, `fill_rect`, `get_pixel`, `set_pixel`.
  - Screen: `clear_screen`, `show`, `show_screen`.
  - Named colours: black, white, red, green, blue, cyan, magenta, yellow.
  - Argument orders are not yet tested.
- **`cas`:** `caseval`, `eval_expr`, `get_key`, `xcas`.
- **`arit`:** `gcd`, `lcm`, `iegcd`, `ifactor`, `isprime`, `nextprime`, `prevprime`, `nprimes`, `euler`, `asc`, `char`.

**Do not use `matplotl` for teaching charts** (PyProbe beta 2). Every function is accepted, but the module is unusable:

- `clf()` clears nothing.
- Pictures pile up, even across separate `PYTHON()` runs.
- `axis()` has no visible effect, so the Prime picks the window.
- `text()` draws only a small square, never the letters.
- A colour argument is accepted but ignored.
- Everything is blue or black outline.

Only the shapes are right: `histogram` counts in width-1 classes from the minimum, and `barplot` bars are centred at x = 0, 1, 2…. Draw charts yourself, with PPL `_P` commands or with Python's `hpprime` or `graphic`.

The missing `time` is independently confirmed by hp-prime-kit on a different G2, and they give the workaround: build your own on **`eval('ticks()')`**, which returns milliseconds. Worth knowing that `ticks()` exists — it is the only timing source on the Python side.

**`random` is absent, so `try: from random import random` is a guaranteed fallback, not a precaution.** NormExplorer's sampler carried that guard for eleven builds; the xorshift fallback ran on every call. Import from `urandom` first (beta 41 does).

**`hpprime` has more than `eval`.** In confirmed use:

- `fillrect(gr,x,y,w,h,edge,fill)`, with `gr=0` meaning the screen.
- `keyboard()` for any-key-down.
- `dimgrob(n,w,h,colour)` for an off-screen grob (used to measure text).

Colours are 24-bit `0xRRGGBB` integers.

**Argument orders that ran on the G2** (StudRangePy's plot, header line 16; recorded as observed, 16 Oct 2026): `fillrect(gr, x, y, w, h, edge, fill)`, `line(gr, x1, y1, x2, y2, c)`, `pixon(gr, x, y, c)`, `textout(gr, x, y, text, c)` with `gr = 0` the screen.

The full list is now confirmed present (PyProbe): `arc`, `blit`, `circle`, `dimgrob`, `eval`, `fillpoly`, `fillrect`, `get_cartesian`, `getpix`, `grobh`, `grobw`, `invert`, `keyboard`, `line`, `mouse`, `pixon`, `rect`, `set_cartesian`, `strblit`, `strblit2`, `textout`, `ticks`, most with `_c` (Cartesian-coordinate) variants. Their argument orders are not yet verified; test before relying on them. Nearly all have a PPL equivalent reachable through `eval` anyway.

**Two installation routes, and confusing them is the support question.**

*Route A — embedded in a PPL program.* The Python lives in a `#PYTHON name … #END` block with a PPL wrapper `EXPORT f() BEGIN PYTHON(name); END;`. Install like any PPL program: paste the `.txt`, sync. **There is never a separate `.py` file.** It launches from the Program Catalog and the user need never open the Python app. This is the house method and the right answer for anything you hand to someone else.

*Route B — a standalone `.py` in the Python app.* These do **not** appear in the Program Catalog; they live under Apps → Python → Files. People sync a `.py`, look in the Program Catalog, find nothing, and conclude it failed.

**Paste, do not retype.** Indentation survives a paste into the Connectivity Kit; hand entry invites a tab-and-space mismatch that is miserable to find on a small screen.

## 9 · MicroPython: the bridge

**The pattern.** PPL writes named globals, Python reads them with `hpprime.eval`, and writes back by assembling a PPL assignment as text. `eval` also writes and reads PPL globals directly (`ev('CX:=3.5')`, `ev('CX')`) and calls your own PPL functions (`ev('MYFUNC(1.0)')`).

**`PYTHON(name, a, b, …)` passes values in `sys.argv`, but only use it for small whole numbers and plain text.** PyProbe, 1 Oct 2026, emulator.

- Every value arrives as text, and `argv[0]` is the first value; there is no script name in front.
- Numbers arrive formatted as the Home screen would display them:
  - −2.5 came as `'−2.5'`, with U+2212 as the minus sign.
  - 1E20 came as `'1ᴇ20'`, with U+1D07 as the E.
  - 123456789012 came as `'123﹐456﹐789﹐012'`, with U+FE50 digit-group marks.
  - `float()` rejects all three.
- A 200-value list arrived cut off at 214 characters, which was 47 values. All seven arguments together came to 257 characters.
- So pass a test number or a mode this way. Have Python read real numbers and data lists directly from PPL variables with `hpprime.eval`; they arrive as true floats.
- A different Home number format, such as Fixed 2, would presumably change what arrives. That is untested.

**Cost of a crossing: about 0.2 ms.** *(Measured by hp-prime-kit on a G2 at firmware 2.4.15515 — not by us.)* Thirty to forty lookups cost around 8 ms, which is nothing. This **corrects an earlier blanket rule here** that said never to cross inside a loop: that is too strong. The real limit is per-pixel work — 272 columns × 2 crossings a frame is about 109 ms, which a live redraw will feel. So: cross freely for tens of lookups, keep it out of per-pixel loops, and keep a returned payload fixed-size so 5000 draws cost the same as 200.

**A Python exception does not raise a PPL error.** This is the one that matters. The traceback prints to the Terminal and PPL carries straight on with whatever the bridge variable held before; `IFERR` around `PYTHON(...)` catches nothing. If the program has a fallback, the fallback runs, the result is correct, and the only symptom is that it took longer. In this fleet the Python sampler failed on every run **for eleven consecutive builds** with nothing on screen to show it.

**So the guard does three things, all necessary:**

1. **Clear the output variable first**, so no stale value survives a failure.
2. **Validate by USING the result**, not by asking its type — read the last element inside `IFERR`. Testing `TYPE(...) == 6` also works but adds a firmware assumption, and if that were ever wrong the program would silently take the slow path forever.
3. **Always write the pure-PPL fallback.** It is slower, and it is the difference between degrading and failing in front of a class.

**Then report which one ran.** A diagnostics page naming the sampler that actually produced the last result — plus a live probe that runs a trivial call and checks the answer comes back — turns an invisible failure into a visible one. Any bridged program should carry one.

**Three ways a Python app closes with no message at all.** *(All measured by hp-prime-kit on a G2; we have not reproduced them, but they match the silent-failure character of this bridge.)*
- **A PPL list containing a string, returned raw to Python.** A function returning eight numbers and a text warning closes the app — no exception, no trace. Wrap the call in PPL and let only numbers out: `ev('LOCAL zr:=' + call + '; {zr(1),...,zr(8)}')`. The same applies to `MOUSE`, which returns lists inside lists. **Design any PPL function that Python will call to return a flat list of numbers, or one number.**
- **A top-level import of a module MicroPython does not have.** Imports inside a function do not count. Delete `__pycache__` before packaging too — those are CPython files MicroPython cannot read.
- **A quote inside a string you are concatenating into an `eval` expression.** Clean it first: `s = str(s).replace('"', "'")`.

**When an app closes silently, leave marks in a PPL global.** The screen is gone and there is no trace, but a PPL global survives:
```
def mark(t):
    try: ev('PZ:="' + t + '"')
    except Exception: pass
```
Then go to Home and type `PZ` to see how far it got. *(hp-prime-kit's technique; it is how they isolated the list-with-string crash in a single pass, by probing in order of increasing risk.)*

**Do not use `repr()` on floats crossing the bridge.** It can emit exponent notation PPL will not parse. Use `"%.6f" % x`.

**On `join`:** it works on this firmware in every form tested — string literals, `str(int)`, list comprehensions, `%`-formatted floats, `repr(float)`, `str(float)`, a mixed list, a bare generator expression, and a tuple. A real, repeated `join` TypeError *did* occur during development and was cured by switching to concatenation, but it has never reproduced; cause unknown, a stale build left on the calculator being the least unlikely guess. **Keep building hand-off strings by concatenation** — it is free and immune to whatever that was.

**The emulator cannot catch these.** It runs the real ROM, so the language behaves identically — which makes it excellent for syntax and logic and useless for this class of bug. The desktop simply ran the fallback fast enough that nothing looked wrong. Any new Python path gets tested on hardware with the Terminal open.

## 9a · Where the Python knowledge actually lives

HP's own Python documentation is thin, though the 2.4.2 firmware (2026-09-09) substantially improved the built-in Python help: press Help in each Python app view. Four outside sources are worth knowing, in rough order of value:

- **`JordiRigau/hp-prime-kit`** on GitHub — `docs/topics/micropython.md` in particular. Every claim is labelled measured or unverified, and measured ones name the firmware. Also ships a PPL linter, an interpreter, and a `.hpprgm` builder. The best single source found. *Saved copy:* `Community_Library\github\JordiRigau__hp-prime-kit.zip`.
- **Mike Markowski's HP Prime Programming page** (udel.edu/~mm/hp/primePython/) — the `hpprime.eval` bridge, calling `CHOOSE` and `DRAWMENU` from Python, `AVars()` for typed values, touch via `mouse`. *Saved copies:* the HTML pages, with his `upython.html` module inventory and the `hat.py` and `spiro.ppl` examples, are in `Community_Library\docs\markowski_udel\`. Roger's January 2024 printout is `HPPrimeProgrammingUDelaware.pdf` (in the Project and in `D:\HP-Prime`); its text layer is garbled, so read the HTML copy instead.
- **Neil Streeter's HP Prime Python Activities** (hpcalc literature, June 2025) — HP-adjacent introduction, the `#PYTHON` wrapper, writing in VS Code and pasting. *Saved copy:* `Community_Library\docs\hpprime-python-activities.pdf` (22 pages).
- **Cemetech and the HP Museum forums** — scattered, but where the version information and most failure reports surface.

Note that hp-prime-kit lists the PPL→Python direction (`PYTHON(name)` with `#PYTHON … #END`, our Route A) as **unverified — "here to put the door on record rather than because it was tried."** That is the direction this fleet has shipped three programs on. If anything here gets published, that is the gap worth filling.

## 9b · The CAS behind the fence (v7h: CASProbe beta 1b ran on the Prime's firmware)

**What we know, from the emulator** (HP Prime Virtual Calculator 2.4.2, build 2026-09-09, 17 Oct 2026; CASProbe beta 1a, then beta 1b):

| Call | What happens |
|---|---|
| `CAS(comb(100,50))` written in the program | evaluated, but a CAS integer too big for Home crosses back as a 12-digit real |
| `CAS(s)`, `s` a string variable or parameter | **the text comes back unevaluated** |
| `EXPR("CAS(" + q + s + q + ")")`, q = CHAR(34) | evaluated; big integers still become reals |
| `EXPR("CAS(" + q + "string(" + s + ")" + q + ")")` | **evaluated, and the answer arrives as a PPL string**: all 30 digits of C(100,50), all 300 of C(1000,500), `35/128`, `(2*cxt+1)*(3*cxt+2)` |
| `STRING()` of that answer | adds a pair of quotes; `"" + answer` does not |
| a syntax error in the text | a run-time error that IFERR catches |
| an unknown function | handed back unevaluated, e.g. `cxnosuch(3)` |
| 6,005 characters of CAS text in one call | fine |
| Python `cas.caseval` | no crash, but returns a decimal for C(100,50); stays outside the fence |

**How the Prime prints CAS answers** (it is not desktop Giac's printing, which the harness used until v3b):

| What | The Prime | Desktop Giac 1.9 |
|---|---|---|
| exp | `e^(cxt^2/2)`, `1/2*cxl^2*e^(-cxl)` | `exp(…)` |
| sqrt | `√2`, `erf(49*√2/50)/2+1/2` (U+221A) | `sqrt(2)` |
| solve | `{1/20}`, `{-2,2}`, a system `{[2,1]}` | `list[…]` |
| fsolve | `[0.0950338528553]` | |
| a limit to infinity | `∞` (U+221E) | `+infinity` |
| 1/0 | `±∞` | `infinity` |
| 0/0 | `undef` | `undef` |
| series | `…+cxt^4*order_size(cxt)`; `convert(…,polynom)` drops it | same |
| evalf | 12 significant digits | |
| negative numbers, products | ASCII `-`, `*` | same |

**CAS variables persist.** `cxq:=7` survives into the next call, and so into the student's CAS view, until `purge(cxq)`. Never assign a CAS variable in a fleet program; solve for it or leave it a symbol.

**The fence** (BRIEF_CAS_v2.md has the code):

1. **One call routine, `xxCas(s)`**:
   ```
   IFERR cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")")); THEN cR := ""; END;
   ```
   Drop one pair of surrounding quotes. An answer containing `undef`, `rror` or `∞` (CHAR(8734)) counts as a failure. `s` must never contain a double quote. **Test the answer only when it is not empty** (v7i): after a failed call `cR` is `""`, and `INSTRING("", "undef")` stops the program (§3). Every v7h kit had the bare test, so every CAS program's fallback was broken; the round-2 fix versions carry:
   ```
   IF DIM(cR) > 0 THEN
     IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;
   END;
   ```
   A parser that rewrites a CAS answer (tra → a, `*` → ×, braces off) loops on INSTRING too; the safe replace loop:
   ```
   IF DIM(rpO) == 0 THEN RETURN rpT; END;            // INSTRING(s, "") = 1: no end
   rpR := ""; rpS := rpT; rpK := DIM(rpO);
   rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;
   WHILE rpI > 0 DO
     IF rpI > 1 THEN rpR := rpR + LEFT(rpS, rpI - 1); END;
     rpR := rpR + rpN;
     IF rpI + rpK > DIM(rpS) THEN rpS := ""; ELSE rpS := MID(rpS, rpI + rpK); END;
     rpI := 0; IF DIM(rpS) > 0 THEN rpI := INSTRING(rpS, rpO); END;
   END;
   RETURN rpR + rpS;
   ```
2. **CAS text is built from integers only, by `xxIStr(n)`.** Home's `STRING(-2.5)` gives the U+2212 minus. The CAS happens to read it, but the rule stands: write 0.95 as `95/100`.
3. **Events, never frames.** Call the CAS when a page opens, a tap lands or a finger lifts, and only when the inputs changed; cache the text. Speed on the emulator: 8 ms at most per call; on the G1, unknown.
4. **Text for display; numbers from PPL.** A CAS number is used only through `EXPR(text)` inside IFERR, with the PPL value as the fallback.
5. **Tagged CAS variable names** (`ctq`, `erpz`), never x, n, p, k, t. Never assign them.
6. **A badge**, "exact (CAS)" or "decimal", wherever a CAS answer appears.
7. **Check every answer by value**, against the program's own number. Never by its text: `exp(`, `sqrt(` and `list[` never appear on the Prime. A failed check shows "no closed form shown".
8. **No** `#cas` blocks, `CAS.name()` calls, cross-program calls or Python `cas.caseval`.
9. **The CAS's job must be visible.** A purely numeric answer (a Clopper–Pearson bound with k > 0, a conditional MLE) is computed in PPL.

**Desktop Giac traps** (still worth knowing; the harness uses desktop Giac with a Prime-printing layer since v3b):
- A plain `sum` over an index makes Giac try to solve Gamma equations, even with numeric bounds; `sum(seq(…))` avoids it.
- `fsolve` around a `sum` fails; expand first, or bisect in PPL.
- The binomial→Poisson limit needs a numeric k.
- `factor()` on symbolic square-root forms can be wrong; send the plain expression.
- A full `factor` of a long binomial sum took over 60 s at n = 10,000.
- The Logistic's E[X²] came back with the wrong sign, hence rule 7.

## 10 · Reaching the built-in apps

**Data columns are global and reachable.** `D1` (Statistics 1Var) and `C1`, `C2` (Statistics 2Var) can be read and written from a standalone program. Wrap the first read in `IFERR` — the variable does not exist until the app has been opened once. Writing works too: `D2 := MAKELIST(...)` puts results where every other app can reach them. `STARTAPP("Statistics 1Var")` then launches the app with the data in place.

**App settings are not reachable.** `H1Type` and `SetSample` are Statistics 1Var app variables. Referencing either from a standalone program is a **syntax error at paste time** — not a runtime error, so `IFERR` cannot help. The User Guide documents qualifying as `Function.Xmin`; both `Statistics1Var.H1Type` and `Statistics 1Var.H1Type` were tried on a G2 at 2026-09-09 and both error.

The confusing part: HP's own DiceSimulation example uses `SetSample` and `H1Type` freely — but that example *is* a Statistics-derived app, where those names are in scope.

**So: data is reachable, configuration is not.** Instruct the user for the rest, or write your program *as* a customised app.

**`VIEW "name", Func()`** registers a function in the Prime's own Views menu (Shift-View), which HP's apps use and custom programs rarely do.

## 11 · Numerical methods

- **Normal sampling: Marsaglia polar.** No trig, so it is immune to angle mode.
- **Substitute to cluster quadrature nodes where the mass is.** StudRange's outer integral over s = √(χ²ᵥ/v) is sharply peaked at low v; the 1977 original excluded low df for exactly this reason. Substituting s = u² (Jacobian 2u) fixes it: k=4, v=3, α=.005 returns 15.4499 against a true 15.4503, where the unsubstituted version was 0.34 off.
- **Secant beats bisection when each evaluation is expensive.** 60 bisection steps versus ~9 secant iterations, with a warm start worth the two lines it costs.
- **The computational variance formula is acceptable here, with a guard.** Accumulating Σx and Σx² keeps the bridge payload fixed-size, and it agrees with a two-pass calculation to 14 decimal places at classroom scales. Wrap it in `MAX(0, ...)` before the square root — cancellation driving the result slightly negative is the one failure mode that matters.
- **Guard moment existence** (Burr XII: mean needs K·C>1, variance K·C>2). "No mean" is a teaching feature.
- **A fixed quadrature grid must be checked at every df the form accepts** (v7o). StudRange's 32-node outer grid over s was exact at df 8 to 30 and at df above 100 (the spike branch), and up to 2 percentage points off between: the density of s narrows as 1/√(2 df) and the grid stepped over it. Compare the integrand's width with the step across the whole range; 64 nodes everywhere was the fix (beta 15e).
- **Upper tails as finite sums of positive terms** (v7o). For χ² at any df: even df, e^(-x/2) Σ_{j<df/2} (x/2)^j/j!; odd df, 2 Φ(-√x) + √(2x/π) e^(-x/2) Σ x^(j-1)/(2j-1)!!. Both keep their digits where `1 - CHISQUARE_CDF` is exactly 0 (TrendTest beta 3f, `trUpper`). The same idea as beta 3d's 1-df trick and StatDist's `st_sf`.
- Verify every formula against SciPy before it goes near the calculator.

## 12 · Statistical wording

- **μ and σ are correct when the program computes from a DECLARED distribution.** Entering N(100,15) declares a population, and every `NORMALD_CDF` result is an exact area under it. x̄ and s belong only where a sample is actually summarised — switching to them in a distribution explorer introduces the error rather than fixing it.
- **"Confidence level" is wrong for a central probability interval.** The middle 95% of N(μ,σ) is where a single observation falls 95% of the time; a confidence interval is built from a sample to estimate a parameter and uses a standard error, not σ. Both give ±1.96, which is exactly why students merge them. Say "central proportion."
- **Cohen's d from two real groups uses the pooled s.** That is both the standard denominator and the only thing a one-σ plot can honestly draw — say so rather than letting the reader assume the statistics were chosen to suit the graphics.
- Showing a sample's own x̄ and s beside the μ and σ that generated it is the cheapest sampling-variability lesson available: they differ on every draw.
- **A mean error is not an SD.** Many papers report the mean of the absolute errors (Lamendin's "ME", Prince & Ubelaker's "mean difference"). For normal errors the SD is the mean error × √(π/2) = 1.25 × mean error, and a regression's RMSE (JMP's "Root Mean Square Error") is the SD of its misses. Label every spread on screen with what it is and where it comes from; an unsourced allowance says it is the program's own (FDAES's Johanson "1 tooth 8.00").
- **Label an interval by what it is.** ±2 SD covers 95.45 % of a normal; a pooled estimate's interval is not a confidence interval of a sample statistic. (FDAES's wording is still Roger's open decision D6.)
- **A method's ceiling or floor is not an estimate.** When every tooth a table reads is mature (Willems at all H), the sum says only "at least"; when a regression's constant sets a floor (Lamendin never gives less than 25.5 yr), its P(age ≥ 18) can never fall below a fixed value (72.7 % at SD 12.5). Say so on the page, draw no verdict band, and keep the value out of any pool. Likewise an estimate outside the reference sample's ages is an extrapolation: show it and label it, but do not band or pool it.
- **Group differences are differences between samples until shown otherwise** (v7l). An estimate read from a reference sample takes on that sample's age mix, so two samples with different age ranges give different average errors even when their people do not differ. Sampling error is random and shrinks with n; this bias is systematic and does not. A page that compares a method across groups says which one it is looking at, and does not call a between-sample difference a population difference (Liversidge 2010; Rolseth et al. 2019).
- **A claim with no source on the page is marked, not trusted.** A statement that cannot be traced to a paper in the library (FDAES's Gustafson and ABFO 2011 lines) is shown as "not checked against the sources" until someone reads the source.

## 13 · House style

Blue `RGB(0,60,200)` the distribution curve · Magenta `RGB(200,0,200)` derived quantities (CDF, posteriors, odds) · Red `RGB(255,0,0)` "you are here" markers, T− cells · Green `RGB(0,140,60)` T+/detected, mean marker; help lines `RGB(0,128,0)` · Orange `RGB(255,69,0)` frames, panels, totals · Dodger blue `RGB(30,144,255)` LR lines, footers · Gray `RGB(90,90,90)` tick labels · Grid `RGB(225,228,235)` · Shade fill `RGB(170,205,255)`. Light fills: green `232,246,235`, red `255,235,235`, blue `235,242,255`, orange `255,240,220`.

**Soft-key pages: the "More" key** (Roger, 16 Oct 2026). When a screen needs more than six soft-key actions, slot 6 reads "More" on EVERY page and steps to the next page of labels, wrapping to page 1 — the job the NXT key did on the HP 48 (NEXT on the HP-28). The most-used actions go on page 1; a destructive action never sits where the finger lands after a page turn; a screen whose actions fit in six gets no "More". Shape: `TouchKit_template_v2.txt`; DRAWMENU is verified, the paging is only program state.

**Symbols on screen** (v7n): see §5; the student sees χ², ≥, μ, not "chi-square", ">=", "mu".

**CAS badge** (v7g): "exact (CAS)" when the line came from the CAS, "decimal" when it fell back — dodger blue, beside the value.

Panels: coloured border, light fill, matching text. **The canonical footer is CentralLimit's**: comma-separated, spaces round `=`, dodger blue — `+/- = n, tap top = redraw, Ent = menu, Esc = quit`. Four other forms were in use on 16 Oct 2026 (colons, no spaces, space-separated, grey); the fix versions adopt this one. Arrow glyphs: `⇆`/`⇅` (CHAR(8646)/CHAR(8645)) or the `CHAR(8592)+CHAR(8594)` pair — both render; Roger to pick one. Subscripts: `CHAR(8320)`-style builds or the literal ₀ ₁ ₂ from the Chars menu — both render; same decision.

**Distribution terms.** Programs go out as `.txt` with a header block carrying the author, year, AI-assistance note, licence — free for educational and personal use, keep the header, credit the author, not for sale — and the firmware tested on. **Since 19 Oct 2026 every header also carries a DISCLAIMER line** (Roger): "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes." Forensic-facing programs show it on screen too: FDAES on its opening page, its help and its report template; DNAMixLR on every LR page; ErrorRate on its opening page. Guides carry the same paragraph after their Credit section.

## 14 · Working rules

1. **Verify before delivering.** Formulas against SciPy; layouts audited numerically; structure balance, reserved words, builtin-name parameters, `LOCAL` sizes, `INPUT` counts, `CHOOSE` arguments — all checked programmatically.
2. **Never guess Prime specifics.** This file, then the corpus, then the reference PDFs, then the web. The device's CMDS and Chars menus are ground truth.
3. **Test before theorising.** When a value appears from nowhere, ask for the observed value of the suspect variable *before* proposing a mechanism. A confident wrong diagnosis (a stale CAS `x`) cost several exchanges and sent Roger to `purge(x)` for nothing; the one-line check should have come first.
4. **Ask how it was installed before theorising about the code.** A duplicate paste into the Connectivity Kit gives duplicate `EXPORT` declarations and an error deep in the file, which looks exactly like a firmware or capacity limit. Environment before code.
5. **Never parse PPL block structure by counting `END;`.** `IF`, `FOR`, `WHILE`, `CASE` and function bodies all close with the same token, so a depth counter terminates at the first inner `IF`. A rename script built this way silently mangled a working file. Track the opening keyword; regenerate rather than patch. Identifier rewrites must also skip string literals, or `"x = "` gets renamed along with `x`.
6. **Sweep every reference when something is renamed.** Menu numbers, key assignments and variable names appear in more places than the obvious one — two menu numbers in a user's guide stayed wrong for several builds after a swap.
7. **Version the filename with every update**, for programs and documents alike, Lessons Learned included (v5 → v6).
   - When unsure of the next number, add a letter: beta14 → beta14a.
   - Always work from the most recent version.
   - **Archive** stale copies: move them to a `_superseded…` folder rather than deleting them, so there is never ambiguity about which file is current.
   - The exceptions are files whose names tools depend on, such as `CLAUDE.md` and `INDEX.md`. Those are edited in place.
8. **An outside code review is worth having, but not worth pasting.** A reviewer with only the source text can spot real problems — two genuine per-frame costs were found this way, both verified against the file. But a full-file rewrite produced without the actual file silently drops things: one such rewrite omitted a `LOCAL` declaration that existed in the original, introduced a lowercase exponent literal, and downgraded 81 working Greek glyphs to ASCII on a speculative "paste fidelity" argument against device evidence. **Take the findings, implement them on the verified file.**
9. **Record disproved theories AS disproved.** A note that reads like a diagnosed cause will send the next session down the same dead end. Two confident explanations of the `join` failure were tested and failed; both are now labelled.
10. **When Roger pastes his edited version, sync to his edits first.** His device copy is the source of truth.
11. **Search the whole library, every time.** It persists, and all of it is reachable:
    - the 83 `.txt` programs uploaded to the Project;
    - on Roger's computer (Rogers-HP), `D:\HP-Prime`: the fleet, about 940 zips (mostly hpcalc.org) at the top level, and `Community_Library`. That folder holds hpcalc, GitHub and cnCalc material plus docs; its `INDEX.md` lists everything.

    Reach it through the link to his computer, or a Claude Code session on Rogers-HP. Search it with `libsearch_v1.py` (the index, `Library_Index.db`, covers all of `D:\HP-Prime`; refresh it with `library_index_build_v1.py` after adding files). For anything the index cannot answer, read archives in place with Python's `zipfile` rather than uploading them. (This corrects v3, which said the corpus zips do not persist between sessions.)
12. **Check the whole fleet for duplicate routine names before every paste** (`python3 fleet_names_v2.py *.txt` in `D:\HP-Prime`), as well as the single-file checks (`ppl_check_v3.py`, `lint_ppl.py` — `ppl_gate_v1.py` runs all of them). One program is never the whole picture on a calculator that pools every program's routines (§5).
13. **Version strings inside a file are references too.** The banner, the help page, the companion-file name in a header, the file map's line count — seven were stale on 16 Oct 2026 (StatDist said v2.3 twice in v2.4; StudRange and its twin named beta 12a; NormExplorer's map was 12 lines short). Sweep them with every rename, as rule 6 says for menu numbers.
14. **The gate, before any paste**: `python3 ppl_gate_v1c.py NEW.txt [ORIGINAL.txt]` (v1c, 19 Oct 2026: the kit linter reads a copy with the `#PYTHON` blocks blanked, and `lint_ppl.py` no longer counts the comment lines of the built-in names file or miscounts nested STRING arguments; v1b, 17 Oct 2026: `ppl_check_v4.py`, whose E12 — a `//` comment inside an open bracket, ChiTable beta 3b's syntax error — is a hard error; v1a, 16 Oct 2026: paths made absolute — `lint_ppl.py` used to read a relative path from its own folder, fail, and the gate's filter hid the failure; a lint that prints no summary now fails the gate; the fleet check compares against the newest version of each program only) in `D:\HP-Prime`. It runs `hpprime lint` from hp-prime-kit (0 errors on every device-tested program in the fleet, so an error is real), `ppl_check_v4.py` (E2/E3/E6/E8/E10/E11/E12 must be zero; v3 matched built-ins ignoring case, as the device does — v2 reported `TYPE` and `LEFT` as unknown because the list spells them in lowercase — and no longer mistakes `!=` for `=`), `lint_ppl.py` (block balance, LOCAL sizes, CHOOSE and INPUT shapes), a full parse with the kit's PPL interpreter where it can read the file (it does not read file-level LOCAL after an EXPORT list, forward declarations, `√`, or `#RRGGBB:24h`; a parse failure on those lines is the tool's limit, not an error), and `fleet_names_v2.py` over every program in the folder.

15. **The run harness before the device** (`ppl_run_v3e.py`, `ppl_run_v3e_README.md` beside it): the kit's interpreter with SciPy-backed built-ins and scripted keys, taps and drags; lists copied on assignment as on the calculator (v2); `CAS("...")` answered by desktop Giac and logged (v3); since v3b the Prime's way: `CAS(variable)` unevaluated, `EXPR("CAS(...)")` evaluated, Giac's printing translated to the Prime's (`e^(`, `√`, braces, `∞`), big integers turned to reals unless they are strings; since v3c, soft-key taps under `WAIT(-1)` as type 3 only, and the integer-df built-ins raising on a fractional df; since v3d (17 Oct 2026, round 2), `INSTRING("", …)` raising "Invalid input" and `STRING(x, 2, d)` printing the Prime's scientific form below 10⁻ᵈ (logged in `h.sci_strings`, so a verify script can list every such display). Since v3e (17 Oct 2026, evening), with `home_minus=True` that scientific form carries the Prime's Unicode minus in the exponent (`9.6ᴇ−2`, CASProbe 1c's codes); v3e reproduces CASProbe 1c's emulator tally exactly, and the fleet's other fourteen verify scripts give the same results on v3e as on v3d. Every program with a CAS feature is run once with `cas='giac'` and once with `cas='fail'`; every CAS template it can build is also run through `icas` in its verify script. Harness agreement is not device agreement — the checklist still decides — but it has caught a wrong BINOMIAL argument order (GaltonBoard), a clamp that never fired (ChiTable) and a crossed-bounds negative probability (StatDist) before any paste. It caught none of the emulator's findings before v3b/v3c/v3d modelled them — which is why the emulator run comes before the hardware run. Round 2 again found what no model had: an empty INSTRING, small fixed decimals, a comment the parser rejects.

16. **Numbers a court may read are transcribed twice, blind, and reconciled** (19 Oct 2026). Two independent readings from page images (by strips and by columns), the OCR as a third, sign-blind source, and internal checks the paper itself allows: n equal across tables; a nested model's SD within √((n−2)/(n−3)) of the simpler one's; CI midpoints equal to their estimates; a table's profile means reproducing its printed mean. Every citation is checked against the paper's own first page. Facts about a sample come from the paper with a page, or are written "not stated". `PU_BR_tables_v1_NOTES.md` and `FDAES_source_facts_v1a.md` (in the author's working folder, not in this repository) are the worked example. The same holds for history and attribution: a claim about what an author said or found is checked against that author's text, with the page, or removed. **And for corrections** (v7l): a later paper's account of an earlier error is checked against the earlier paper and against any later work on the same point before it is copied (Maples & Rice's "mean deviation" was superseded by Aykroyd 1995; Lucy & Pollard's "never tested" about Bang & Ramm is wrong). A number taken from a handout, a workshop packet or a textbook table is checked against the original page: retyped tables drift (Mincer's 69.4 and 19.0 for 29.4; the 2013 *Manual*'s Bang & Ramm cells).
17. **A critical sweep before a public push** (19 Oct 2026). Independent reviewers read each program in full against this file, write their own check scripts (never trusting a verify script's expected values), drive the harness on edge inputs, and report bugs with a line, a reproduction and a proposed fix. The fix pass then turns every failing check into a regression test that the old version fails and the new one passes. A version built from a review gets its own second review before delivery: FDAES v3.9's found 25 more items, including errors in the first review's own wording.

18. **A verify script runs from the repository alone** (v7o, 22 Oct 2026). It finds `tools/` and `programs/` by relative path, reads an older version from git history when the file is gone from `programs/`, and every version it compares against is committed before the script is. The 19 Oct scripts hard-coded the author's folders and seven of the files they read survived nowhere, so five of them could not be rerun in full by an independent environment; `verify_StudRange_beta15e.py` and `verify_TrendTest_beta3f.py` are the pattern. What an independent environment needs, and nothing else: hp-prime-kit (`HPKIT`, or the Community_Library zip beside `tools/`), Giac (`apt-get update; apt-get install xcas` on Ubuntu), SciPy, statsmodels.
19. **Check a formula by calling its routine through the harness** (v7o). `h.execute('name(args)')` for a routine that takes arguments; `h.globals_.update({...})` then `h.execute('name()')` for one that works on program state, reading the results back from `h.globals_`. No pages, no taps, no scripted dialogs; 281 comparisons in an afternoon. Routines the harness's SciPy built-ins answer (a bare `BINOMIAL_CDF`) prove only the program's logic, not the Prime's numerics; the ones worth most are the program's own arithmetic (Fisher's ratios, Newcombe, the mixture probability, the studentized range).

## 15 · Current fleet

**One current set, 22 October 2026** (StudRange beta 15e and TrendTest beta 3f from the independent re-check; the rest from 20 October, night) (in `D:\HP-Prime`; `FIXED_FOR_DEVICE` and the staging folders are rebuilt from it). On 20 Oct every program but BayesTree, Norm3 and StudRange got a version that writes symbols instead of spelled-out names (v7n), and NormExplorer one that paces its animation (42b). The 17 Oct emulator rounds (§16; Emulator_Round2_Results_2026-10-17_v4.md; in this repository, [dev/emulator-round1-2026-10-17.md](dev/emulator-round1-2026-10-17.md) and [dev/emulator-round2-2026-10-17.md](dev/emulator-round2-2026-10-17.md)) were followed by the 18 Oct "= <" cleanup (ten lettered versions) and the 19 Oct fleet review and fix pass (Fleet_Review_2026-10-19_v1.md): every program but GaltonBoard got a fix version, and GaltonBoard a header-only one carrying the disclaimer. **The 19 Oct versions have run in the PC harness only** (each verify script re-run independently, and gate v1c); the column says what the emulator last showed for the version before. Older versions are in `_superseded_2026-10-17`, `_superseded_2026-10-18` and `_superseded_2026-10-19`.

Each program has `_CHANGES.md` files with device checklists and a `verify_*.py`. **The 19 Oct versions were loaded on the Virtual Calculator, the G2 and the G1 on 20 Oct 2026**; the first G1 checks are in §3 and §16. **The 20 Oct versions have run in the PC harness only.**

| Program | Version | State |
| --- | --- | --- |
| **ChiTable** | beta 3e | Newcombe's interval for the risk difference (Roger, 19 Oct); χ² p as lower tails. Emulator (3c): compiles; tea table p = 17/35 exact. **20 Oct:** symbols on screen. |
| **GaltonBoard** | beta 3e | Header only (the disclaimer). Emulator (3c): every menu line whole; "1 ball". **20 Oct:** symbols on screen. |
| **BayesTree** | beta 8e | DOR from the clamped rates; a flick no longer sends the slider to 0.999. Emulator (8c): the first tap after a footer close counts. |
| **StudRange** | beta 15e | **22 Oct:** the PPL engine's plot cache on a 64-node grid at every df (it was 2 points off at df 50 to 100). 15d: a note when the PPL fallback answers at α < 0.005; Home's X untouched. Emulator (15b): soft keys, the Quit summary. |
| **StatDist** | v2.7f | Every right tail family by family (`st_sf`, Roger's D9); Gamma/χ² shape > 5000 refused. Emulator (2.7c): Pareto's Formula page exact. **20 Oct:** symbols on screen. |
| **TrendTest** | beta 3f | **22 Oct:** the Pearson and departure p as finite positive sums (`trUpper`), no longer 0 on extreme tables. 3d: `TR_P` as a lower tail; fractional counts refused. Emulator (3c): the CAS page exact. **20 Oct:** symbols on screen. |
| **PowerViz** | v2.5e | "POWER > 0.999"; no negative n₈₀. Emulator (2.5b): "Where n comes from", exact. **20 Oct:** symbols on screen. |
| **EpiStats** | v1.7e | α/power refused outside (0, 1); empty rows and columns "undef"; McNemar, M-H and Breslow-Day as lower tails; NNT near RD 0. Emulator (1.7b): extreme tables never print `ᴇ`. **20 Oct:** symbols on screen. |
| **CICatcher** | beta 2d | Two lines shortened. Emulator (2b): the setup menu whole; the C-P end-point exact. **20 Oct:** symbols on screen. |
| **CentralLimit** (app) | beta 3d | Recovers when D1 is emptied or trimmed; a Reset hook. Emulator (3b): run as an app. **20 Oct:** symbols on screen. |
| **DNAMixLR** | beta 3d | P(E|H) from positive terms (no cancellation); refused unknown counts no longer used; on-screen disclaimer. Emulator (3b): the LR formula exact. **20 Oct:** symbols on screen (θ in the formula too). |
| **ScatterLab** | beta 2d | `slNum` keeps 140000000000 whole. Emulator (2b): the calculus page exact. **20 Oct:** symbols on screen. |
| **ErrorRate Lab** | beta 1e | The CAS page's last line kept; on-screen disclaimer. Emulator (1b): "Why 3" exact. **20 Oct:** symbols on screen. |
| **NormExplorer** | beta 42c | The ROUND-before-STRING sweep (134 sites); tails and right-tail quantiles keep their digits. Emulator (42): most of the checklist passed. **20 Oct:** symbols on screen; 42b paces the standardize animation by `TICKS`. |
| **Norm3 / Burr3** | v2.4b / v2.4c | No `ᴇ` for tiny σ or S; Burr3's pdf in logs (large shapes no longer overflow). Emulator (2.4): passed. **20 Oct:** Burr3 2.4c writes × in its help. |
| **SampDist** | v2.3c | The α clamp and `sd_fix`'s tail. Emulator (2.3): passed. **20 Oct:** symbols on screen. |
| **TestChooser** | beta 2b | Points to EpiStats, not ConTable2/FEP; wording. Emulator (2): passed. **20 Oct:** symbols on screen. |
| **BiNorm3D** | beta 1b | A help sentence and a menu line. Emulator (1): passed. **20 Oct:** symbols on screen. |
| **FDAES** | v3.9c | Held back from this repository. |
| **TouchKit template** | v3 | Unchanged. |
| **GfxProbe** | beta 1 | Ran on the emulator; rerun on the G1 and G2 for T15 (held key), T16 (two fingers) and timing. |
| **CASProbe** | beta 1d | 1c ran on the emulator: 44 pass, 9 fail, 19 values, 0 errors; T43a (empty INSTRING is an error) and T43c passed, and T43b failed only because it matched the text with a hyphen. 1d tests for CHAR(7431) and logs which minus the exponent used; on the emulator (17 Oct, 16:42) it gave 45 pass, 8 fail, as the harness predicted. Rerun on the G1 for speed and T43. |
| **LocalHeadProbe** | beta 1 | Passed on the emulator. |
| **MenuTapProbe** | beta 1 | Records raw WAIT(−1) events with DRAWMENU shown (§7). |
| **Retired** | | ConTable2 and FEP (in EpiStats), StudRangePy (in StudRange). Delete them from the calculators. |
| **PyProbe beta 2b / PyDirect beta 1 / PyVer / JoinTest / GenTest** | | Diagnostics, unchanged. |

**Still to settle on the calculators:** G1 speed of the CAS calls and the morph (the first timings are in §16); held keys (GfxProbe T15) and two fingers (T16); whether a MOUSE-read tap leaves a click for the next `WAIT(−1)` on the hardware (BayesTree 8c and StudRange 15b handle both answers; their checklists test it); CASProbe 1d's T43 (an empty INSTRING, and the codes `STRING(0.096, 2, 1)` prints); and whether AND and OR skip their right side inside a program, not only in Home (nothing depends on it). The 19 Oct review's five Home lines were settled on the G1 on 20 Oct (§3), and a light tap on a soft key registers there (§16). The glyphs π, η and τ, new on screen on 20 Oct, are on the checklists. GfxProbe and CASProbe 1d are staged for the G1 in `D:\HP-Prime\_probes_to_G1_2026-10-20`.

## 16 · Testing on the Virtual Calculator (v7h, v7i)

**What it settles.** The HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) runs the calculators' firmware, so these behave as on the G1 and G2:
- commands and what they accept or reject;
- the CAS and how it prints;
- MicroPython and the bridge;
- drawing and glyphs;
- what `WAIT(-1)` and `MOUSE` report for a tap or a drag.

Round 1 of the fleet ran there on 16–17 Oct 2026 (Emulator_Round1_Results_2026-10-17_v1.md).

**What it cannot settle:**
- G1 speed (the PC is far faster: 100,000 Galton balls in 7 ms);
- a key held down;
- two fingers;
- how a real finger tap compares with a mouse click.

A mouse click shorter than a polling loop's pass can be **missed** by a `GETKEY` + `MOUSE` loop (the StatDist gallery, PowerViz's α+, CICatcher's welcome page). A press of about 0.3 s always registered. **On the G1 a light finger tap on a soft key registers, and a tap followed by a key works** (Roger, 20 Oct 2026).

**First G1 timings** (Roger, 20 Oct 2026, the 19 Oct versions): GaltonBoard's pour, 100 balls in about 35 s, and its ×100 soft key in about 0.5 s; StudRange q(0.05, 3, 12) = 3.7729 in about 7 s; BayesTree's drag fast; NormExplorer's standardize animation smooth but too long, which is why beta 42b times each frame. **A pause tuned on the Virtual Calculator is the pause alone; on the G1 the drawing comes on top of it.** Time a frame with `TICKS` and wait only for the rest.

**How to drive it** (computer use, from the cloud):
- **Load:**
  1. Open the program's file from `FIXED_FOR_DEVICE` in Notepad and copy all of it.
  2. In the Connectivity Kit, right-click Programs, choose New, and type the name.
  3. Paste the text into the editor and click Save. The Kit gives no syntax check. The calculator's own editor does: Program Catalog (Shift 1) → Edit → Check.
- **Replace a program by opening it in the Kit, never by adding a second copy.** Two copies share one pool of routine names (§5).
- **Run:** paste the program's name into Home **without parentheses**, or use the Catalog's Run. `Name()` with empty parentheses in Home is a "Syntax Error"; it is not a fault in the program.
- **Read a log:** evaluate it in Home, select the result, then Edit ▸ Copy (Ctrl+C) in the emulator's menu. The Windows clipboard then holds the calculator's own text.
- **Typing:** letters typed from the PC keyboard leave the emulator in ALPHA lock, so digits typed after them come out as letters (2 → Z). Paste from the clipboard instead. Shift on the skin followed by the PC's 1 opens the Program Catalog.
- **PC Esc after the skin's Shift is Shift+Esc**, which clears the Home history.
- **Apps** (corrected in v7i): saving from the Kit's app editor **does** reach the calculator — Application Library → double-click the app → Program tab → paste → save. Round 1 concluded otherwise because starting the app from the Application Library shows its stock Numeric view; the calculator's **View** key opens the app's own Views menu (CentralLimit beta 3a, round 2). The Program Catalog lists it first as "CentralLimit (App)", where Check works as for any program.
- **Check before running** a new or changed program: Program Catalog (Shift + Program) → tap the program (it opens in the editor) → Check. A compile error shows as "Syntax Error" when run from Home, with no line; Check puts the cursor near it (ChiTable beta 3b, round 2).
- **Quick clicks:** a mouse click on the skin's keys (Esc especially) or on a soft key can be too short for a `GETKEY` + `MOUSE` polling loop; press for about 0.3 s. A drag needs several mouse moves (a one-step drag sends a single move event, which a drag threshold ignores).
- **A quick click on a `CHOOSE` item can end the program** (FDAES v3.8, 17 Oct 2026, evening): the menu returned Cancel, and FDAES treated it as Exit. Choose items with the digit keys or a 0.3-s press. **Brief Enter presses from the PC keyboard can be missed** by a `GETKEY` + `MOUSE` loop (2 of about 20 in the same run); the next press always worked.
- **Paste, don't type, into Home and forms**, and write the clipboard just before each paste: another hand at the same computer can change it. Tapping a field that is already selected and then pasting appends to its value; paste into a selected field without tapping it.
- **Typing goes to the window in front.** Click the emulator's title bar where no other window covers it before pasting; a paste that lands in the Kit's editor changes the program text there (undo with Ctrl+Z, and never save it).
- **Loading many programs in one pass** (the round-2 retest, 14 programs): Notepad's Open dialog (Ctrl+O) stays in the last folder, so open each paste-ready copy in turn, Ctrl+A, Ctrl+C; in the Kit, double-click the program in the tree (each opens its own editor window, cascaded), click into its text, Ctrl+A, Ctrl+V, Save. Check the editor's first lines changed before saving; then run each from Home.
- **An empty screenshot** ("0x0") means the PC's screen is locked or asleep. Computer use cannot unlock it; wait for Roger, and do the work that needs no screen meanwhile.

*Shelved: a three-level Bayes tree for desktop — R/Shiny favoured for the classroom.*

---

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
