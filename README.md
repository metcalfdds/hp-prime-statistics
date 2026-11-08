# HP Prime statistics

## Welcome one and all...and especially HHC 2026 visitors!

*A note from Roger: I am very sorry I cannot be with you at HHC 2026 in person this year, and I send my regrets and my best wishes for a wonderful conference. I hope you enjoy exploring what is here, and I would love to hear from you through [GitHub issues](https://github.com/metcalfdds/hp-prime-statistics/issues).*

Thank you for stopping by. Here is a set of **30 teaching programs for the HP Prime**, written for university statistics, research methods, criminal justice, and forensic science courses, plus **a long set of notes on how we believe the Prime really behaves**: what we found the hard way on a G1, a G2, and the Virtual Calculator--things all the manuals do not tell us.

Most of the programs are built around the touch screen. You drag a bound on a statistical distribution curve and the shading follows, pour balls through a Galton board with a finger, rotate a 3-D bivariate normal distribution wireframe plot, slide a cut-off along an ROC curve and watch who gets flagged "high risk". The aim is to let students *see* the statistics move.

--------------------------------------------------------------------------------------------------------------------

**Very special thanks** to two sites that hold the HP calculator community together:

- **[hpcalc.org](https://www.hpcalc.org)**, Eric Rechlin’s archive of HP calculator software. Its collection of Prime programs was our reference library while we worked out how the Prime actually does things out in the real world.
- **[The Museum of HP Calculators](https://www.hpmuseum.org)**, David G. Hicks’s history of HP’s calculators, and its forum, where much of what is known about the Prime has been worked out in public.

We have no official affiliation with either site, or with HP. I’m just a grateful user.


--------------------------------------------------------------------------------------------------------------------

Hundreds of community PPL programs from several HP-related public forums were read as references while figuring out how the Prime really works in the wild. Several entries in the notes exist because a corpus program showed a construct working that the many various manuals do not describe. Note that none of those programs were copied, incorporated, used without permission/authorization, or reproduced here, and credit is noted where others' intellectual property and/or concepts were followed. 

**The programs here probably would not be possible without the foundation laid by dozens and dozens of HP users and the hundreds of programs they have graciously made freely available over the years--if you find anything here helpful or useful, it is due to and a tribute to the myriad of other folks who have gone before. Thank you all--especially Eric Rechlin!**

----------------------------------------------------------------------------------------------------------------------

**New here?** [START_HERE.md](START_HERE.md) is a one-page guide: what to read in five minutes, five programs to try first, and how to help.

**No calculator? Try all 30 on HP's free Virtual Calculator.** Download the **[starter pack](https://github.com/metcalfdds/hp-prime-statistics/raw/main/starter-pack/HP_Prime_Statistics_Starter_Pack_v14.zip)** (one 1.5 MB zip, for the Virtual Calculator on Windows). Unzip it, copy one folder's files into the Virtual Calculator's own folder, and start it: the programs are in its Program Catalog, CentralLimit already made into its app. No Connectivity Kit, and no copying and pasting of code. [The steps](starter-pack/README.md) fit on one page.

**Your own data, without typing it in.** The **[HP Prime Data Loader](data-loader/README.md)** is one web page that works offline: paste columns from Excel, SPSS or a CSV file, and it writes the calculator's own matrix file. On the calculator, **DataLoad** puts each column, or each group's scores, into the Statistics lists that the other programs read, and draws a box plot of each. The starter pack carries DataLoad and a sample data set (new, 31 October 2026).

**Neither shortcut is in HP's manuals.** [Two shortcuts the manuals don't mention](docs/two-shortcuts.md) says how each one works, what we found when we tried it, and who found what. Loading by copying files we learned from [hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit); two other community projects use it too. The Data Loader route is new here, designed and written by Claude.

**Newest, for students: the [HP Prime Loader](https://metcalfdds.github.io/hp-prime-statistics/prime-loader/)** (1 November 2026; [how it works](prime-loader/README.md)). One web page, at a fixed address that also suits a book, and it works offline too: pick your chapter, click Load, start the Virtual Calculator, tap a program, tap Run. In Edge or Chrome it moves whatever was on the calculator to a backup and puts on only that chapter's programs (and data, if you like); in Firefox, which many schools require and which never lets a page write into a folder, it walks the student through downloading one file and unpacking it into the calculator with Windows' Extract All. Every step explains itself in plain words. Nothing needs checking: since starter pack v5 every program is the file the Virtual Calculator wrote back after checking it, and such a file runs at once (measured 1 November 2026). Tried on Roger's computer in Edge, with Extract All and through the Connectivity Kit; 56 checks in Chromium.

### What is here, at a glance

| Area | Programs |
| --- | --- |
| **Distributions** | NormExplorer, Norm3, BurrLab, StatDist (27 distributions), StudRange (Tukey's q) |
| **Sampling, estimation and power** | CentralLimit (an app), SampDist, CICatcher, GaltonBoard, PowerViz |
| **Tables and tests** | ChiTable, TrendTest, TTestLab (t-tests in five steps) and TTestLabG (its general version), TestChooser (a tappable flowchart), EpiStats |
| **Correlation and regression** | ScatterLab, BiNorm3D |
| **Student's t** (new, 7 November 2026) | TDist3D (the t family as a surface you turn) |
| **Bayes and forensic science** | BayesTree, DNAMixLR, ErrorRate Lab |
| **Criminal justice and forensic statistics** (new, October 2026) | RankLab, AnovaLab, ExhibitLab, SurvLab, FitCheck, ResampLab, AgreeLab, RiskLab |
| **Getting your data in** (new, 31 October 2026) | DataLoad, with the [Data Loader](data-loader/README.md) web page |

Together, these 31 programs currently run to more than **90,000 lines**: 60,700 of PPL code, 1,170 of MicroPython (in five of them), and 24,700 lines of comments, written so a student can follow what each part does. The largest is EpiStats at about 6,100 lines -- I wrote the original, elementary, unsophisticated version of this program for coursework I had in Harvard's STAT S-103 Intro to Epidemiology & Biostats and Claude took it to a whole other level, and I hope future students in that class or other similar classes will find it helpful; and then eight other late October programs average about 3,000 lines each. These were built with tremendous assistance from Anthropic Claude (mostly Opus 5.5 and Fable 5.1) over **many** months of intense, but fun, work.

And around the programs:

- **[The notes](docs/lessons-learned_v7zp.md)**: hard limits, commands that differ from the manual, touch and graphics idioms, the MicroPython bridge and how it fails silently, calling the CAS safely, numerical methods for 12-digit reals. Useful even if you never run a statistics program, and written so you can hand them to an AI assistant before it writes PPL for you.
- **[Two shortcuts the manuals don't mention](docs/two-shortcuts.md)**: loading the Virtual Calculator by copying files into its folder, and a big data set as one matrix file, with who found what.
- **[Tools](tools/)**: the checks every program passes before it is pasted (a lint gate, a fleet-wide name check, a check that no two lines of text overlap on screen, a PC harness that drives a program like a student), in plain Python 3.
- **[Diagnostics](diagnostics/)**: small probe programs that test what your own calculator does.
- **[How fast is the Prime?](#how-fast-is-the-prime-what-we-measured)**: what we timed on a G1 and a G2, and why a slow Prime may only need a reset.
- **[A touch template](templates/TouchKit_template_v3.txt)** to start a program of your own.
- **[The same arithmetic in Python](python/hpstats.py)**, tested against SciPy.

### Real data, from courtrooms and published studies

The newest programs use published data with their sources on screen: the 1970 draft lottery (I was in that lottery), *Castaneda v. Partida*'s grand juries ("29 standard deviations"), the cheques in *Arizona v. Nelson* against Benford's law, the Rossi re-arrest study, ProPublica's COMPAS data from Broward County, mock-jury sentences, the ENFSI drug-sampling tables, Darwin's corn, Bortkiewicz's horse kicks, the months served by 41 BJS homicide offenders and 2,156 Danish fire-insurance claims. [docs/data/](docs/data/) lists every source and how it was checked.

Everything here is **free for educational and personal use**. See [LICENSE](LICENSE.txt).  © 2026 Roger D Metcalf

### How far have they been tested?

Three different questions, with three different answers:

- **Is the arithmetic right? Yes, as far as we can test it, I think so.** Every program passes the lint gate and runs in the PC harness, with its numbers extensively checked against SciPy, stats models, and exact arithmetic. Where a program refers to published data, it has been able to reproduce the published results. Every program but the newest, DataLoad and TTestLabG (31 October 2026), has also had an independent review (TTestLabG is built from TTestLab, which has); TTestLab's (`docs/dev/review2-TTestLab-beta1a.md`) found ten faults in its dialogs and wording that its 59 arithmetic checks had not, all fixed the same night in beta 1b.
  
- **Do they run on a real calculator? Yes, we think so, but we are still checking.** Every program has run and been extensively tested on the HP Prime Virtual Calculator by Claude, and the current versions have had cursory checks on a G1 and a G2 by human me. The full device checklists, one per version in [docs/changes/](docs/changes/), are still being worked through, and some screens, especially graphics, can be slow. **Reports from your own calculator are the most welcome contribution of all.** The full dated record is in [docs/test-status.md](docs/test-status.md).
  
- **Do they survive careless use? We now test that too** (1 November 2026). The **monkey test** (`tools/monkey_v1b.py`) drives a program the way a student who doesn't want to be there might: random keys, taps, menu picks and cancels, and odd values typed into the forms (a list where a number belongs, 1E300, 0, negatives). TTestLab, TTestLabG, SampDist, BayesTree, CICatcher, Norm3, NormExplorer, StatDist, PowerViz, ScatterLab, ChiTable and GaltonBoard now pass 1,000 random runs with none broken; trying the fixes on the Virtual Calculator found three things the PC model of the calculator cannot show (`!=` is not "not equal" on the Prime, `STRING` takes at most 12 decimals, and a loop step can vanish in 12 digits). StatDist's 27 distributions were also swept parameter by parameter from 1E−300 to 1E300. Every program's labels were then checked under random use, which found crowded or cut labels in 15 of 30 at values no test script had tried ([docs/dev/label-check-2026-11-02.md](docs/dev/label-check-2026-11-02.md)). The first pass over the other book programs found what to fix next: [docs/dev/monkey-fleet-2026-11-01.md](docs/dev/monkey-fleet-2026-11-01.md).

- **Can they be used on real cases? No!** Software used in casework must first be formally validated: tested on known samples under a laboratory's quality system, with its limits documented, certified, and then used by a qualified analyst. None of these programs has been through that process.
  
**DISCLAIMER: so...these programs are teaching and demonstration aids, provided as-is, with no guarantees. They are not validated for forensic, clinical, or legal use; do not rely on their results for casework, legal decisions, or any other purpose.**

These programs were originally intended just to demonstrate statistical concepts to undergraduate university students, but the project eventually morphed into a much larger suite of programs that show off some of the capabilities of the HP Prime, and also to push the hardware to see what the limits are for programs that are "reasonable" to run on a calculator. Some of these programs are rather large-- 3,000 up to 6,000 lines of code-- and so may load slowly and may slow down the Connectivity Kit--it might be best to keep only a couple of these programs on your calculator at any one time. And please note that we are always open to suggestions for new programs.

Remember, too, these programs are **works-in-progress**--some parts, especially graphics, may work very slowly, some parts may or may not even work at all, and they are provided strictly as-is --again, you should not rely on the results from these programs for **anything.** I think the numerical results are very accurate, but, even so, use at your own risk, no guarantees. Your mileage may vary.

---

## Installing (note in particular the instructions for CentralLimit because it is an App, not a Program)

Every program is a plain `.txt` file, on purpose.

**On the Virtual Calculator, the [starter pack](starter-pack/README.md) is quicker:** all 31 programs as ready-made calculator files, CentralLimit already made into its app, copied into the calculator's folder while it is closed. Since v5 nothing needs checking: every file in the pack was checked on the Virtual Calculator before it was packed. The [Prime Loader](prime-loader/README.md) does the copying, chapter by chapter. The steps below are for a G1 or G2, or for one program at a time.

1. Open the **HP Connectivity Kit** and connect your calculator.
2. Create a new program in the Program Catalog.
3. Open this repository's `.txt` file in any text editor, select all, copy.
4. Paste into the Connectivity Kit's program editor, and sync.

**Do not rename the file to `.hpprgm`.** That format is binary (UTF-16LE with a header), and a `.txt` renamed to it will not import. Pasting is the reliable route. (The starter pack's `.hpprgm` files are built properly, by `tools/make_starter_pack_v4.py`, and read back against their source.)

**Install only one version of each program.** Every program on a Prime shares one pool of routine names, so two versions of the same program on one calculator can run each other's code. Delete the old one first.

**The same arithmetic in Python.** [`python/hpstats.py`](python/hpstats.py) holds the fleet's formulas (intervals, 2 × 2 tables, the trend test, the DNA mixture probability with θ, the studentized range, Burr XII, chi-square tails as positive sums) as plain, tested functions, for checking a program, for teaching, or for citing. Its README has the list; `python3 test_hpstats.py` checks every one against SciPy, statsmodels or brute force.

**Upgrading from an earlier version?** ConTable2 and FEP are now part of EpiStats, and StudRangePy is now part of StudRange. Delete those three from the calculator.

> ⚠️ **CentralLimit: read this before installing it.**
> CentralLimit is an **app** (a copy of Statistics 1Var with its own program), not an ordinary program. Install it this way, in this order:
> 1. **Delete any ordinary program called CentralLimit** from the calculator (Program Catalog → highlight it → Delete). It may be there from an earlier version, or from pasting it as a plain program by mistake.
> 2. **Make the app:** Apps → highlight Statistics 1Var *without opening it* → **Save** → name it `CentralLimit` → OK.
> 3. **Paste the program into the app:** in the Connectivity Kit, Application Library → double-click CentralLimit → **Program** tab → select all → paste `CentralLimit_beta3e.txt` → save. On the calculator, Check it (it is the first entry in the Program Catalog while the app is active).
> 4. **Reset the calculator** (a soft reset: on the Virtual Calculator, its **Calculator menu → Reset**; on a G1 or G2, press the reset button in the small hole on the back with a straightened paper clip). Closing and reopening the Virtual Calculator is not enough. Without the reset, the deleted program's routines can stay in memory and the app keeps opening on its spreadsheet.
> 5. **Start it:** Apps → highlight CentralLimit *without touching it* → tap **Start**. You should see a welcome page and then its menu. Touching the icon only reopens the spreadsheet; press **View** from there to reach the CentralLimit menu.
>
> *Found the hard way on 27 October 2026, on the Virtual Calculator and then a G1.*

**CentralLimit is an app, not a plain program.** The installation steps are in its header. On the Virtual Calculator the Connectivity Kit route worked too, once the app's copy of Statistics 1Var exists (step 1 in the header): Application Library → double-click CentralLimit → Program tab → paste → save. Starting the app shows the stock Numeric view; the calculator's **View** key opens the app's own menu.

**MicroPython.** BurrLab, StudRange, NormExplorer, GaltonBoard and ErrorRate carry a `#PYTHON … #END` block inside the program file. There is **no separate `.py` file**, and nothing goes into the Python app. With Python firmware (2.1.14566, April 2021, or later) the Python part runs, and a badge on screen says so. Without it, the programs fall back to pure PPL automatically.

---

## The programs

**Exact answers from the CAS.** Twelve programs can now show an exact or symbolic answer beside their decimal one: Fisher's p as a fraction, a binomial probability as C(n, k)·pᵏ…, the limit that turns into the rule of three, a least-squares line as exact fractions. The calculator's CAS works it out on demand, the program checks it against its own number, and a badge says "exact (CAS)" or "decimal". If the CAS is busy or fails, the decimal answer stands.

**What the programs accept** (5 November 2026). A calculator is for the numbers of a real course, so every program refuses what no real problem needs (Roger: "cap everything at reasonable values"). A mean, an x value, a bound or a cut-off: −10,000 to 10,000. An SD or another scale, degrees of freedom, a rate: above 0, at most 1,000. StatDist's binomial n: at most 1,000. A sample size typed into a form: at most 10,000 (PowerViz: 2 to 5,000; a value outside is set to the nearer end, with a sentence that says so). A count in a table: at most 100,000. α: 0.001 to 0.2. A random seed: 0 to 9,999. The calculator itself handles much larger numbers, and the programs were tested with them (the tests typed values up to 10¹⁰⁰); the entries are capped at reasonable values so that the programs stay quick. The hint line under each field gives its range, and a value outside it is refused with a sentence that gives it again; nothing changes. Data loaded into the lists (DataLoad, or typed into the Statistics 1Var app) are not limited, and ErrorRate's database size goes to 100,000,000, because national DNA databases hold tens of millions of profiles. How the fields were found: [docs/dev/caps-2026-11-05.md](docs/dev/caps-2026-11-05.md).

**Commas in big numbers** (2 November 2026). Every number of 1,000 or more that a program writes on the screen now carries its commas (12,345.678; 1,000,000), by APA's rule: never after the decimal point, never in a year ("Fleiss 1971"), and never in text the calculator's CAS reads, where "1,000" would be two numbers. The calculator's `STRING` never puts them in, whatever Home's digit-grouping setting, so each program does it with a small routine of its own. AgreeLab and ResampLab also write d̄ now, drawn as a d with a bar over it, because the calculator's font has no such letter. How it was done and checked: [docs/dev/commas-2026-11-02.md](docs/dev/commas-2026-11-02.md).

Almost every program now responds to a finger: drag a bound, a bar, a curve or a dot and watch the numbers follow. Where a screen needs more than six soft-key actions, the right-hand key reads **More** and pages to the next set, as the NXT key did on the HP 48. Every touch action also has a key route.

### Distributions

**NormExplorer** (beta 42i; 5 November: reasonable limits on what you type, and one header on every help page, "NormExplorer help n/N: Topic"): a normal-distribution workbench.
- Any μ and σ, four kinds of probability question and three inverse ones, a z-formula solver, Cohen's d, and a standardize animation.
- A live explorer: drag either bound of a shaded interval. "More" brings up a second page, so the arrow keys can move a bound, μ or σ.
- Reads your own data from the Statistics apps.

**Norm3** (v2.4f; 5 November: one header on every help page, "Norm3 help: Touch and keys"; it takes arguments; the Program Catalog asks for them): drag x₀ and watch the area and the S-curve together. Tap the S-curve for the inverse.

**BurrLab** (beta 1p; 7 November: its first run on a real G1 showed the Family map as a solid gray box — a one-colour `RECT_P` fills — and the tail shades too pale to see; the map's border is four lines now, the tints deeper, the shades solid; 5 November: reasonable limits on what you type, and one header on every help page, "BurrLab help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK; replaces Burr3): the Burr XII as the model for a long right tail. Fit it to data by maximum likelihood, in PPL or MicroPython (or both, timed side by side), and see it ranked by AIC against the lognormal, Weibull, gamma, exponential and Lomax; drag C and K and watch it turn into the Pareto, the log-logistic or the Weibull; watch a running mean wander forever when the tail is too heavy for a mean to exist; ask how rare a value is. Data: BJS months served, Rossi weeks to re-arrest, Danish fire claims. **Why the Burr XII, and how the fit differs from fitting a normal:** [docs/burrlab-guide.md](docs/burrlab-guide.md).

**StatDist** (v2.7k; 5 November: reasonable limits on what you type, and one header on every help page, "StatDist help n/N: Topic"): 27 distributions, each result a plot you can touch. Drag x or k, the shading follows, and the window snaps to round values. Overlays show the normal approximation, N(0, 1) behind t, and the CDF as an S-curve. A Gallery opens six examples with one tap.

**StudRange** (beta 15l; 5 November: reasonable limits on what you type, and one header on every help page, "StudRange help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): the studentized range (Tukey's q).
- p from q, the critical value from α, Tukey HSD, and an interactive plot.
- **MicroPython does the arithmetic, PPL is the fallback**, and a badge says which engine ran.
- Python adds an H₀ simulation that shows why q, and not t, is the right yardstick.
- Descends from a 1977 FORTRAN IV subroutine (Dunlap, Powell & Konnerth, *Behavior Research Methods & Instrumentation* 9(4):373–375).
- Accuracy against SciPy: within 5×10⁻⁶ for k 2–20 and df 1–20,000. This version also fixes wrong values at df = 1 and at very large df in the earlier versions.

### Sampling, estimation and power

**CentralLimit** (beta 3f; 5 November: one header on every help page, "CentralLimit help n/N: Topic", an app; **see the install warning under [Installing](#installing-note-in-particular-the-instructions-for-centrallimit-because-it-is-an-app-not-a-program)**): watch one sample happen, its members lighting up and their mean dropping into the pile. Then drag along the top panel to choose n, and see the square-root law on its own page. After Colin Croft's HP 39G aplet (2003).

**SampDist** (v2.3i; 5 November: reasonable limits on what you type, and one header on every help page, "SampDist help n/N: Topic"): the sampling distribution of x̄, with the population drawn faintly behind it.
- **n×4** halves the width.
- The nearer bound follows your finger.
- "Watch sample means" drops forty of them onto the axis.

**CICatcher** (beta 2h; 5 November: reasonable limits on what you type, and one header on every help page, "CICatcher help n/N: Topic"): fifty confidence intervals stack up, blue if it catches the truth (the green line) and red if it misses. **Drag the confidence level**: every interval stretches or shrinks, and the catch count updates exactly without new samples. Covers z, t, Wald, Wilson and the exact Clopper–Pearson interval.

**GaltonBoard** (beta 3h; 5 November: one header on every help page, "GaltonBoard help n/N: Topic"): Galton's quincunx. The board holds 5,000 balls; then it shows the results.
- **Pour mode:** hold a finger on the funnel and a stream of balls cascades through the pegs.
- **Drag sideways** to change p.
- **Fill to 5,000** runs in MicroPython.
- Tap a bar for its binomial probability and the normal area.

**PowerViz** (v2.5q; 5 November: reasonable limits on what you type, and one header on every help page, "PowerViz help n/N: Topic"; 4 November, night: "t-test" on every screen): **drag the H₁ curve**, and the α, β and power regions reshade live; a magenta arrow shows the effect size, d. Drag the critical line to set α, and drag up or down for n. n₈₀ appears in the panel and on the power-versus-n curve; the readout shows each group's n, μ and σ side by side and the t obtained with its df, as SPSS prints it (Welch's in the unequal-σ test). Five tests: one mean; two means with equal σ and n; **two means with unequal σ and unequal n**, where each group has its own σ and n and the formula page shows the best split, n₂/n₁ = σ₂/σ₁; one proportion; and two proportions. **Levene's test:** how often it would notice unequal spreads at your n (simulated, from the σ's and n's: SPSS's Levene F needs every score, and the page says so), beside the exact F test, and **two real samples** (the 1970 draft lottery, insect sprays, or your own D1 and D2) with Levene's test, the pooled and Welch t-tests and Cohen's d, each read out in plain words for students.

### Tables and tests

**ChiTable** (beta 3k; 5 November: reasonable limits on what you type, and one header on every help page, "ChiTable help n/N: Topic"): chi-square for a 2 × 2, 2 × 3 or 3 × 2 table.
- The full statistics: expected counts, G², Cramér's V, adjusted residuals, and for a 2 × 2 Fisher, RR, OR and the risk difference with Newcombe's interval.
- **Drag an observed bar**, and every expected bar moves with χ² and p.
- **Drag the critical line** on the χ² curve.
- An independence morph, a Fisher bar plot, and the Florida death-penalty tables as a Simpson's-paradox page.
- [docs/chitable-guide.md](docs/chitable-guide.md) is the user's guide.

**TrendTest** (beta 3l; 5 November: reasonable limits on what you type, and one header on every help page, "TrendTest help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): chi-square for linear trend in a 2 × k table. **Drag a dot** to change a level's proportion and watch the trend test respond. Includes a confidence band and Wilson intervals.

**TTestLab** (beta 1h; 5 November: reasonable limits on what you type, and one header on every help page, "TTestLab help n/N: Topic", new 31 October 2026; 1 November: every form field takes numbers only, and numbers too large for the calculator to work with are refused with a sentence, after the monkey test below; 4 November: the flowchart's go-ahead key reads Run, not OK, because on the Prime's own screens OK closes the screen; 4 November, night: "t-test" on every screen): the t-tests of a criminal-justice statistics course, worked the way a lecture works them, in **five steps, a screen each**: the hypotheses and the data; the distribution and df; the critical value and the decision rule on a t curve with the rejection region shaded; the standard error and t obtained with the numbers put in; the decision, with t obtained and the p value drawn on the curve, and Cohen's d.
- **Pooled-variances, separate-variances (Welch, SPSS's "Equal variances not assumed") and dependent-samples t**, with any mix of equal or unequal SDs and Ns, from each group's mean, SD and N or from raw scores in D1 and D2; two-tailed or one-tailed either way.
- **Which t-test?** A tappable flowchart: are the samples independent? are the variances equal?
- **Pooled or separate?** Both tests side by side, and what goes wrong with the pooled test when the smaller group has the larger SD.
- **The printed t table beside the exact value** (df 73 reads row 60), and where a hand calculation rounded too early, what that did to t.
- Examples: age at arrest (JDCC), matched jails (Census of Jails), and drug use by sex from an SPSS output, which it matches to SPSS's printed t = −4.351 on 265.924 df.

**TTestLabG** (beta 1f; 5 November: reasonable limits on what you type, and one header on every help page, "TTestLabG help n/N: Topic", new 31 October 2026; 1 November: the same fixes as TTestLab beta 1c; 4 November: Run, not OK, as TTestLab beta 1e; 4 November, night: "t-test", as TTestLab beta 1f): **the general version of TTestLab**, for an intro course in any subject and the companion guide in progress. The same five steps, arithmetic and screens (built from TTestLab beta 1c by `tools/make_tlg1_v2.py`), with its own name so both can sit on one calculator, and these differences:
- **Separate variances (Welch) is the default**; pooled stays a choice. The flowchart says: not sure the variances are equal? Answer No.
- **t critical is the exact one for the df.** A printed table is a note: a df it lacks takes the next smaller row (the larger t crit); a fractional df is rounded down first. Step 2 also gives the hand shortcut for separate variances, the smaller N − 1.
- **A p that rounds to α prints its 4 significant digits** ("p = 0.04970: just below α = 0.050"), and means worked out from raw scores print to 4 significant digits.
- Examples: **Darwin's plants** (his 1876 *Zea mays* pairs, crossed and self-fertilised), **the 1970 draft lottery** (Selective Service: were the birthdays drawn at random?), age at arrest (JDCC) and matched jails (Census of Jails). Ran on the Virtual Calculator beside TTestLab; 106 checks: [TTestLabG_beta1_NOTES.md](docs/changes/TTestLabG_beta1_NOTES.md), [TTestLabG_beta1a_CHANGES.md](docs/changes/TTestLabG_beta1a_CHANGES.md).

**TestChooser** (beta 2f; 5 November: one header on every help page, "TestChooser help n/N: Topic"; 4 November, night: "t-test" on every screen): which statistical test? It is a tappable flowchart: tap the outcome's scale and the design, and the path draws itself to a test. There is also a tappable table, and a 20-case criminal-justice and forensic quiz. After Glantz's *Primer of Biostatistics*. Its t-test pages point to TTestLab.

**EpiStats** (v1.7j; 5 November: reasonable limits on what you type, and one header on every help page, "EpiStats help n/N: Topic"; 4 November: its first monkey test, 1,000 runs of random use, all OK: every form field takes numbers only, and sample sizes and rates that the calculator cannot work out are refused with a sentence): epidemiology.
- **2 × 2 tables** in cohort, diagnostic and paired layouts: McNemar, Yule's Q, and a bar for every possible table behind Fisher's test. Call `EpiStats2x2(a,b,c,d)` from Home.
- **Risk and odds** with Wilson intervals, plus an NNT icon array.
- **Incidence rates and sample size.**
- **Stratified Mantel–Haenszel analysis** with Breslow–Day, and a forest plot where a tap drops a stratum.

### Correlation and regression

**ScatterLab** (beta 2i; 5 November: reasonable limits on what you type, and one header on every help page, "ScatterLab help n/N: Topic"): build a scatterplot with your finger. Add, drag or delete points, and the least-squares line, r, r², SSE and the residuals follow. Guess mode lets you fit a line by eye first, then shows that least squares really does have the smallest SSE.

**BiNorm3D** (beta 1e; 5 November: one header on every help page, "BiNorm3D help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): the bivariate normal as a wireframe you turn with a finger. It adds a contour view, and a slice that shows regression to the mean.

### Student's t (new, 7 November 2026)

**TDist3D** (beta 1; 7 November, night: first version; 1,000 runs of the monkey test, all OK; run on the Virtual Calculator, not yet on a G1 or a G2): Student's t distribution as one surface you turn with a finger — every t curve at once, t across and the degrees of freedom ν away from you, from the heavy tails of ν = 0.5 at the front to the normal curve at the back. It is the calculator's version of the Maple surface in *Statisticles*. A red slice marks one ν and gives its peak, its critical value (the number that replaces 1.960), and the chance of a value beyond ±2 (0.295 at ν = 1, 0.046 for the normal); ν climbs a ladder from 0.5 to 1,000 or is typed. A Curves view shows the family end on, the way a textbook draws it. Pure PPL: the surface never changes, so everything is computed once and a frame is drawing only. **What ν does, and why t is wider than z:** [docs/tdist3d-guide.md](docs/tdist3d-guide.md).

### Bayes and forensic science

**BayesTree** (beta 8i; 5 November: reasonable limits on what you type, and one header on every help page, "BayesTree help n/N: Topic"): a natural-frequency Bayes tree.
- **Slide the prevalence** and the tree and a mosaic re-flow: watch a 95 %-accurate test's PPV collapse at low prevalence.
- Sensitivity and specificity can be dragged on the branches.
- A Fagan nomogram, a second test, and forensic labels.

**DNAMixLR** (beta 3i; 5 November: one header on every help page, "DNAMixLR help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): the likelihood ratio for a mixed DNA profile, locus by locus, with the NRC II θ correction (Weir et al. 1997; Curran et al. 1999).
- **Drag θ** and watch the LR fall down an ENFSI verbal ladder.
- Tap a locus for its numbers, and drop loci from the table.
- A prosecutor's-fallacy page.
- **A teaching tool only:** casework needs validated software and a qualified analyst.

**ErrorRate Lab** (beta 1i; 5 November: one header on every help page, "ErrorRate help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): "Zero errors in 30 proficiency tests: how good is the examiner?"
- The **upper 95 % confidence bound** on the error rate, the convention PCAST (2016) asked forensic disciplines to report. The rule of three appears as the limit it is.
- A Bayesian view.
- A MicroPython simulation of 10,000 proficiency programmes.
- The chance of a coincidental match in a database search.

### Criminal justice and forensic statistics (new, October 2026)

Data sources for every preset are listed, with the checks made on them, in [docs/data/](docs/data/).

**RankLab** (beta 1f; 5 November: reasonable limits on what you type, and one header on every help page, "RankLab help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): the rank tests. Sign test, Wilcoxon signed-rank (exact, ties handled), Mann-Whitney, Kruskal-Wallis with Dunn's pairs, Friedman with Kendall's W, Spearman and Kendall (exact for small n), Hodges-Lehmann. A rank strip you can tap, and the exact null distribution with the observed value marked. Data: the 1970 draft lottery, Darwin's corn, the Rossi re-arrest study, mock-jury sentences, Connecticut judges' ratings.

**AnovaLab** (beta 1e; 5 November: reasonable limits on what you type, and one header on every help page, "AnovaLab help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): one-way ANOVA with Welch, Levene and Bartlett, and Holm, Bonferroni, Scheffé and Tukey-Kramer comparisons; two-way ANOVA for unbalanced designs (Type III); randomized blocks; tests and intervals for variances. Tap two groups to compare them; an interaction plot. Data: mock-jury sentences by attractiveness and crime, the draft lottery by month, insect sprays.

**ExhibitLab** (beta 1f; 5 November: reasonable limits on what you type, and one header on every help page, "ExhibitLab help n/N: Topic"; renamed from SeizureLab on 4 November 2026, because "seizure" reads as a medical word to many students; if SeizureLab is still on your calculator, delete it; 4 November, night: 1,000 runs of the monkey test, all OK; its Home results are now EX_N, EX_NMIN, EX_P, EX_LB, EX_PB, EX_TOT and EX_TLB): how many units of a drug seizure must be tested? Hypergeometric, binomial and Bayesian answers, an operating-characteristic curve you drag, and the total net weight with its interval. Checked against the tables of the ENFSI *Guidelines on Representative Drug Sampling* (2009): 426 of 427 cells agree, and the one that does not is a misprint in the guideline.

**SurvLab** (beta 1e; 5 November: one header on every help page, "SurvLab help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): time to re-arrest. Kaplan-Meier curves with Greenwood and log-log intervals, a finger cursor that reads S(t), quantiles when the median is never reached, log-rank and Gehan-Breslow tests, hazard ratios and a life table. Data: Rossi, Berk & Lenihan's 432 released prisoners, by financial aid.

**FitCheck** (beta 1e; 5 November: reasonable limits on what you type, and one header on every help page, "FitCheck help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): goodness of fit. Chi-square with cell merging, Benford's law (*Arizona v. Nelson*'s cheques), the exact binomial test (*Castaneda v. Partida*'s grand juries, "29 standard deviations"), Poisson fits (horse kicks, Richmond homicides), and normality: Q-Q plot, Shapiro-Wilk, Anderson-Darling, Lilliefors.

**ResampLab** (beta 1g; 5 November: reasonable limits on what you type, and one header on every help page, "ResampLab help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): permutation tests and the bootstrap you can watch. Shuffle once and see the dots move; ×10, ×100, ×1000; exact enumeration when it is small enough; percentile, basic and BCa intervals. Data: mock-jury sentences, Darwin's corn, months served for homicide (BJS).

**AgreeLab** (beta 1f; 5 November: one header on every help page, "AgreeLab help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): examiner agreement. Cohen's kappa on touch tiles (drag a count off the diagonal and watch kappa fall), weighted kappa, Fleiss' kappa, the six intraclass correlations and a Bland-Altman plot; the "kappa paradox" explained. Data: Landis & Koch's two neurologists, Fleiss (1971), Bland & Altman (1986), Shrout & Fleiss (1979).

**RiskLab** (beta 1e; 5 November: one header on every help page, "RiskLab help n/N: Topic"): the statistics behind recidivism risk tools. Logistic regression, the ROC curve with a draggable cut-off and a live 2 × 2 table, calibration, and fairness by group, using ProPublica's published COMPAS data from Broward County (as counts) and the Rossi study. It shows, with real numbers, why a score cannot be both equally calibrated and equally wrong for two groups whose base rates differ.

### Getting your data in (new, 31 October 2026)

**DataLoad** (beta 1e; 5 November: one header on every help page, "DataLoad help n/N: Topic"; 4 November, night: 1,000 runs of the monkey test, all OK): typing a long data set into a calculator is not feasible, so this does it from a spreadsheet. The **[HP Prime Data Loader](data-loader/README.md)**, one web page that works offline, turns columns pasted from Excel, SPSS or a CSV file into the calculator's own matrix file (M1 to M9). DataLoad then puts the matrix's columns into the Statistics 1Var lists D1-D9 (or the Statistics 2Var lists C1-C9), either column by column or as scores by group (the SPSS layout: each group's scores to its own list, the smallest code to D1), leaves out blank cells, and offers to clear lists left from an earlier load, which AnovaLab, RankLab and AgreeLab would otherwise read as more groups. Then a box plot of every list and a histogram of any list you tap, with the Statistics 1Var app's own quartiles. On the Virtual Calculator it loaded the Rossi re-arrest data (432 x 5) and a text-coded matrix with blanks, its summaries matched Python, and TTestLab read the lists it filled (t(421.19) = -1.68, p = 0.094, as SciPy gives). Not yet run on a G1 or G2, and not yet independently reviewed. How this route compares with the copy-and-paste route HP describes, and who found what: [Two shortcuts](docs/two-shortcuts.md).

*FDAES (forensic dental age estimation) is held back from this repository for now.*

---

## How fast is the Prime? What we measured

These programs push the HP Prime hard, and some screens take a moment to draw. That is the hardware, not a fault, and it is worth knowing what to expect. Every figure below was measured on our own calculators (firmware 2026-09-09), with a stopwatch or with a program's own timing readout.

**First: if your Prime feels slow, reset it.** Our G2 had become about **15 times slower** than normal, with no warning and no error, after a long day of loading programs and one MicroPython program that hung. A paperclip reset brought it back to life. Unplugging it from the Connectivity Kit also helps: while the Kit is connected it keeps querying the calculator, and our G2 took 40-75 % longer on the same tests when it was plugged in to the computer. Time anything only after a reset and unplugged.

**What takes time**

- **Redrawing a curve.** One key press on BurrLab's Explore page recomputes the curve and redraws the page: about **0.43 s on a G1 and 0.10 s on a G2** (BurrLab beta 1i, after a reset; the program's own readout, More > Timing). Beta 1h took about 0.9 s on the G1: beta 1i computes the curve at every 3rd pixel column instead of every column.
- **A big fit.** BurrLab's maximum-likelihood fit of 300 Danish fire claims takes about **45 seconds on a G1** in PPL. A progress bar shows it working, a blinking hourglass shows it has not stopped, and Esc stops it. BurrLab can also run the fit in MicroPython (Fit menu, Engine).
- **Simulations.** GaltonBoard pours 100 balls in about 35 s on a G1 (its ×100 key, which skips the animation, takes half a second).

**What we learned about the hardware** ([SpeedProbe](diagnostics/SpeedProbe_beta1.txt): eleven timed tests; run it on your own calculator)

- **The G2 is three to four times faster than the G1 at PPL.** A loop of 5,000 simple sums takes 870 ms on our G1 and 245 ms on our G2; calling a routine 3,000 times, 478 ms and 158 ms; making a 300-element list 200 times, 611 ms and 149 ms. That agrees with the published benchmarks (Savage: 0.43 s G1, 0.19 s G2).
- **Copying a whole screen image is fast on both** (BLIT_P of 320 × 240: about 1 ms on the G2, 5 ms on the G1), so drawing pages off-screen and copying them once costs almost nothing.
- **Every pass of a PPL loop costs time** (about 0.17 ms on a G1, 0.05 ms on a G2, for one simple statement). A redraw that touches every pixel column pays it 268 times; computing fewer points and joining them with lines is the cheapest speed-up there is.
- **MicroPython is much faster at arithmetic, but crossing the bridge has a price.** StudRange's studentized-range quantile takes about 1.5 s on a G2 with Python (7 s on a G1), where the PPL engine takes about a minute, because Python does the work and hands back one number. When we moved BurrLab's curves to Python, which hands back hundreds of values one at a time, a key press got slower, so the curves went back to PPL. **Rule of thumb: Python pays when it returns a few numbers, not hundreds.**
- **On the Virtual Calculator everything is fast.** The emulator on a PC runs the same firmware far faster, so it is good for checking that a program works, but, of course, is pretty much useless for judging its speed. Time things on a real G1 or G2.

**What the programs do about it**

Progress bars, a blinking hourglass and Esc on anything long; the new value shown the moment a key is pressed (BurrLab); caps on the size of data a page will take; cached plot layers so a key press redraws only what changed; Python engines with a PPL fallback where Python helps (BurrLab's fit, StudRange), with a badge saying which engine answered and how long it took. BurrLab's Engine setting "Both" runs a fit both ways and shows the two times side by side.

**Your measurements are welcome.** If you time something on your own G1 or G2, especially on other firmware, please report it through GitHub issues.

---

## Diagnostics

Short programs for finding out what your own calculator does.

- **`GfxProbe`** tests the graphics and touch features the manuals document but that we have not confirmed:
  - translucent and blended fills;
  - the 3-D triangle mesh;
  - scaled blits;
  - a second finger;
  - the WAIT(−1) gesture events;
  - plus how many lines a message box really shows.
  It writes its answers to `GP_LOG`.
- **`CASProbe`** (beta 1d) finds out how a program can use the CAS safely:
  - the call form;
  - what text comes back;
  - how errors look;
  - two string facts from round 2: `INSTRING` on an empty string (an error), and the scientific form of small fixed decimals;
  - how fast it is on a G1;
  - and, last, behind a warning page, whether Python's `cas.caseval` is stable.
  It writes `CX_LOG`. On the 2026-09-09 firmware it found that `CAS(s)` hands a string variable's text back unevaluated; the working form is in the notes, §9b. Beta 1d (which corrects one of beta 1c's tests) ran on the emulator on 17 October 2026: 45 pass, 8 fail.
- **`MenuTapProbe`** (40 lines) shows what `WAIT(-1)` reports for a tap on the soft-key strip: a click, and nothing else.
- **`LocalHeadProbe`** is ten lines: is `LOCAL name(a, b)` a legal routine head?
- **`PyVer`** reports your MicroPython version and probes ten modules. It takes two minutes.
- **`PyProbe`** (beta 2b) asks what the Prime's MicroPython can actually do: how values pass from PPL into Python, what the `matplotl` charts really draw, and what each module contains. Run on the Virtual Calculator only.
- **`SpeedProbe`** (beta 1) times eleven kinds of work (arithmetic, LN and EXP, list reads and writes, making lists, routine calls, lines, text and whole-screen copies) in about 20 seconds and leaves the times in `SP_MS`. Run it on a G1 and a G2 and compare. It is how we found our G2 running about 15 times slower than normal until a paperclip reset ([How fast is the Prime?](#how-fast-is-the-prime-what-we-measured)).
- `JoinTest` and `GenTest` isolate a specific `str.join` failure. They are kept because they document a real investigation, including the part where it did not reproduce.

`templates/TouchKit_template_v3.txt` is the house touch kit as a starting point for a new program: drain, wait-for-key-or-tap, soft keys with "More" pages, hit boxes, and a draggable bar chart.

---

## The notes

[**docs/lessons-learned_v7zp.md**](docs/lessons-learned_v7zp.md) is the substantial document here: everything learned the expensive way across dozens and dozens of build iterations on G1 and G2 hardware. It covers:
- hard limits;
- command behaviour that contradicts the manual;
- graphics and input idioms;
- the MicroPython bridge;
- how to let the CAS into a program without letting it break one;
- numerical methods;
- testing on the HP Prime Virtual Calculator;
- a list of disproved theories, recorded as disproved.

The lessons learned document can be uploaded to your favorite AI to assist with coding.

A few things from it that are hard to find elsewhere:

- **The Prime runs MicroPython 1.9.4**, a December 2018 release tracking CPython 3.4. Check *those* docs, not the current ones. This single fact explains most of the surprises.
- **A Python exception does not raise a PPL error.** The traceback goes to the Terminal, and PPL carries on with whatever the bridge variable held before. `IFERR` around `PYTHON(...)` catches nothing. In this fleet a sampler failed on every run for eleven consecutive builds with nothing on screen to show it.
- **`FREEZE` is not a pause.** It suppresses the screen refresh at program *end*. Mid-program it does nothing.
- **The Prime's reals hold 12 significant digits, so `1 − CDF` is exactly 0 once a tail is below about 5×10⁻¹³.** Compute an upper tail as a lower tail (for the normal, `NORMALD_CDF(m, s, 2m − t)`), and a right-tail quantile as `−NORMALD_ICDF(0, 1, α)`. Alternating sums lose their digits the same way; build probabilities from positive terms.
- **`STRING(x, 1, digits)` ignores the digits argument.** Mode 1 is Standard. Fixed decimals need mode 2, and mode 2 turns scientific below 10⁻ᵈ: `STRING(0.096, 2, 1)` is `9.6ᴇ−2`, with a Unicode minus. `STRING(ROUND(x, d), 2, d)` is safe.
- **`INSTRING` on an empty string is a run-time error,** "Invalid input". A failed CAS answer, a string cut down to nothing, an empty field: check `DIM(s) > 0` first. Every CAS program here had one such line in its fallback until round 2 found it.
- **A `//` comment inside an open bracket is a syntax error.** Two comment lines inside a multi-line `CHOOSE` list stopped ChiTable compiling. Put the comment above the statement.
- **Built-in names are matched case-insensitively.** `LOCAL csC` is a syntax error because `csC` is `CSC`, the cosecant. A program named `ChiSquare` is `CHISQUARE`. Scan every name, prefix or not.
- **Every program's routines go into one shared pool.** A helper that is not `EXPORT`ed is still visible to every other program on the calculator. Two programs that define the same name (`NiceNum`, `fmtp`...) can run each other's code: a runtime error, the Program Editor open on the *other* program, and a reset to get out. Every helper here carries its program's tag, and `tools/fleet_names_v2.py` checks a folder of programs for duplicates.
- **`MOUSE` and `WAIT(-1)` number their touch events differently.** In `MOUSE`, drag is 2; in `WAIT(-1)`, drag is 1. A handler has to say which table it reads.
- **Soft keys under `WAIT(-1)` arrive only as a click.** A tap on the `DRAWMENU` strip is `{3, x, y}`: no press, no lift. A loop that waits for a press there never sees the key. Once a menu has been drawn, a tap on that strip arrives the same way even on a screen that shows no soft keys. And a tap read through `MOUSE` leaves no click behind for `WAIT(-1)`.
- **A program cannot hand the CAS a string variable.** `CAS(s)` gives the text back unevaluated; `EXPR("CAS(\"string(" + s + ")\")")` works. The Prime prints `e^(`, `√` and `{…}`, not desktop Giac's `exp(`, `sqrt(` and `list[…]`.
- **Chi-square and F CDFs take whole-number df only**; the t distribution takes any.
- **A finger lift can arrive from `WAIT(-1)` as a one-element list.** Read `kk(2)` from it and the program stops with an error. Check `SIZE` first, and give any "wait for the finger to lift" loop a time limit.
- **`STRING()` of a number follows the Home number format,** which can include digit-grouping marks and a special minus sign. Text built for the CAS or for Python should not come from it.
- **Data columns are reachable from a standalone program; app settings are not.** `D1`, `C1` and `C2` can be read and written. `H1Type` and `SetSample` are a syntax error at paste time.
- **The desktop emulator runs the real ROM**, so any difference you see on hardware is necessarily timing, memory or display. No amount of further emulator testing will find it.

[docs/changes/](docs/changes/) has one file per program version: what changed, the lint and verification output, and the device-test checklist. [docs/dev/](docs/dev/) has the fleet review and the CAS plan that drove the 16 October versions, the reports of the two emulator rounds of 17 October, and the independent second reviews (`review2-*.md`).

---

## Tools

[tools/](tools/) has the checks every program here passes before it is pasted, in plain Python 3:
- the fleet-wide name-collision check;
- the built-in-name and structure checks;
- the gate that runs them all;
- a PC run harness that drives a program with scripted keys, taps and drags, with SciPy behind the statistics built-ins and desktop Giac behind `CAS(...)`, made to behave as the Prime's firmware does where the emulator showed a difference;
- the starter-pack builder, which turns `programs/` into ready-made Virtual Calculator files and reads each one back against its source;
- the monkey test, which throws random keys, taps and typed values at a program in the harness and reports every way it broke;
- a painter (`page_render_v1.py`, 7 November 2026) that draws every screen the harness recorded as a PNG, following the calculator's own rules (a one-colour `RECT_P` fills), so a page can be looked at before the Virtual Calculator sees it.

[data-loader/](data-loader/) has the Data Loader page, its number encoder and its tests (20,011 numbers against hp-prime-kit's encoder, and the page itself in Chromium).

[prime-loader/](prime-loader/) has the Prime Loader page, its source, the build script that embeds the starter pack's files and the chapter list, and its Chromium test.

**On Windows, a Connectivity Kit launcher that starts Bonjour first:** [tools/windows-launcher/](tools/windows-launcher/). If the Kit sometimes fails to see your calculator because Apple's Bonjour Service has stopped, double-click `Start_HP_Prime.cmd` instead of the Kit's own shortcut.

[verify/](verify/) has the scripts that checked each program's numbers.

---

## Credits

Concept, direction, and hardware testing: **Roger Metcalf**, © 2026.

Implementation, numerical work and documentation: re-written, edited, expanded, and **vastly** improved with incredible and amazing AI assistance from **Anthropic Claude** --mostly Opus 5.5 and Fable 5.1. Sonnet 5.5 does a lot of the cleanup and mechanical sorts of tasks.  Most of the notes and the user guides here were essentially written by Claude.

Hundreds of community PPL programs from several HP-related public forums were read as references while working out how the Prime actually behaves. Several entries in the notes exist because a corpus program showed a construct working that the various manuals do not describe. None of those programs are copied, incorporated, used without permission/authorization, or are reproduced here, and credit is noted where others' intellectual property and/or concepts were followed. The programs here probably would not have been possible without the foundation laid by dozens and dozens of HP users and the hundreds of programs they have graciously made freely available over the years--if you find anything here helpful or useful, it is due to the myriad of other folks who have gone before. Thank you all--especially Eric Rechlin!

The interesting studentized range algorithm is after Dunlap, Powell & Konnerth (1977). Accuracy figures were verified against SciPy, and several were also cross-checked against historical sources: Harter's 1960 tables of the studentized range, and the worked examples HP printed in the manuals for its own 1970s statistics programs on the HP-41, HP-55, HP-65 and HP-67/97 ([docs/historical-cross-checks.md](docs/historical-cross-checks.md)). Our StudRange program demonstrates the advantage of MicroPython in some situations--under PPL only, the complex calculation takes about a minute on a G2, but the Python version runs in a couple of seconds. 

Several MicroPython findings credited in the notes come from [JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit), measured independently on a different G2. The kit is also where we learned that the Virtual Calculator can be loaded by copying files into its own folder, the method the starter pack uses. The `.hpmat` matrix file the Data Loader writes is the one the kit documents. [abaccin's hpprime-stoichiometry](https://github.com/abaccin/hpprime-stoichiometry) and [Rudicito's HP-DOOM](https://github.com/Rudicito/HP-DOOM) use the same folder copy.

The Data Loader and DataLoad, the route for big data sets, are new. Roger asked for "some sort of 'data loader'"; Claude (Opus 5.5) designed, wrote and tested them on 31 October 2026 ([docs/two-shortcuts.md](docs/two-shortcuts.md)).

Corrections and reproductions are welcome. Where a claim here is unverified, it says so.  © 2026 Roger D Metcalf
