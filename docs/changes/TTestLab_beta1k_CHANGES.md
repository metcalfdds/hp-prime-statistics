# TTestLab beta 1k: changes (14 November 2026, night)

Round 14, part 2. Built from beta 1j by exact replacements (`verify/round14/make_ttestlab_1k.py`; a replacement that does not match exactly once stops the build).

## Why

The book *Statisticles* teaches the one-sample *t*-test and the one-proportion *z*-test in Chapter 9 and the two-proportion *z*-test in Chapter 11. Until now it said, "TTestLab compares two samples. For one sample, use the *Inference* app." Roger, 14 November 2026, about the book's list of program work: "go ahead and do the program work"; and, about its pictures: "we're featuring the Prime". With beta 1k TTestLab works all three tests in its own five steps, and its three new examples are the book's own worked examples.

## What changed

| What | Where (line numbers in `TTestLab_beta1k.txt`) |
| --- | --- |
| Three more tests: `ttTY` 4 the one-sample *t*, 5 the one-proportion *z*, 6 the two-proportion *z*. Their numbers have variables of their own (`ttMO`, `ttSO`, `ttNO`, `ttMU`, `ttXO`; `ttKA`, `ttNA`, `ttKB`, `ttNB`, `ttP0`) | 238 to 245 |
| The arithmetic: `tt_One` (mean and SD of the scores, two passes), `tt_Whole` (a whole number in a range), `tt_CalcN` (the three tests; every refusal is a sentence). `tt_Calc` sends the new tests there; its old lines are untouched inside `IF ttTY <= 3` | 691, 704, 716; 779 |
| A *z*-test's curve, critical value and *p*: `tt_SL` ("t" or "z"), `tt_Dens` (Student's *t* or the standard normal curve), `tt_ZCrit` (`-NORMALD_ICDF(0,1,a)`, a lower tail mirrored), `tt_ZP` (lower tails only). `tt_Curve` draws through `tt_Dens` and labels through `tt_SL` | 525 to 558; 922 |
| The hypotheses in each test's symbols: `tt_HS`; the Tails menu uses it ("Two-tailed: p₁ ≠ p₂") | 560; 1763 |
| The pages: `tt_Step1N`, `tt_Step2N`, `tt_Step3Z`, `tt_Step4N`, `tt_Step5N`, with `tt_VN` (a number as typed, or to 4 digits when it came from D1) and `tt_Par` (a negative number in brackets). `tt_Page` sends the new tests to them; the one-sample *t* keeps `tt_Step3` | 1231 to 1530; 2122 |
| The soft keys of a *z*-test read "2 dist" and "4 z" (`tt_ShowSteps`); `tt_TName` and `tt_TDf` know the new tests ("z" has no df) | 904; 847, 886 |
| Choosing: `tt_Pick` (a short menu, "Which test?"; two means go on to the flowchart) and `tt_Fam` (a change of test asks for new numbers unless both are independent *t*-tests) | 1710, 1720; used in `tt_Menu`, 2079 |
| The forms: `tt_AskDataN` (one sample: the mean, SD, N and μ₀, or scores in D1 and μ₀; one proportion: x, n, p₀; two proportions: x and n twice). `tt_AskData` sends the new tests there | 1795; 1865 |
| Examples 4 to 6 (`tt_Example`): Student's sleep data, the grand juries of *Castaneda v. Partida*, the Rossi experiment | 1953 |
| The start menu: "Choose the test", the three older examples, "Examples: one sample, z-tests" (a list of the three new ones; Esc there comes back) and Help: six items, all on the screen | 2180 |
| Help: three pages; page 3 is "One sample, proportions" | 2024 |
| "Pooled or separate?" on a test that has no such choice: a box that says so | 1532 |
| Cohen's *d* past 999.99 in size prints as "> 999.99" or "< −999.99" (`tt_DS`), on the older tests' step 5 as well: with an SD typed far too small its digits ran into the label beside it (found by the label monkey; beta 1j has the fault) | 573; 1191, 1452 |

What a student sees, test by test:

- **One-sample *t*.** Step 1: H₀: μ = μ₀ with its value, the sample (typed numbers, or the first ten scores from D1 in two rows) and "The mean H₀ claims". Step 2: df = N − 1, and why one df goes. Step 3 is the *t*-tests' own page (the printed table's row and the exact value). Step 4: SE = s/√N and t obt = (x̄ − μ₀)/SE with the numbers put in. Step 5: the decision, "Report t(9) = 4.06, p = 0.003, two-tailed", and Cohen's *d* = (x̄ − μ₀)/s.
- **One-proportion *z*.** Step 2 says the curve is the standard normal curve, with no df, and checks the book's rule: n p₀ and n(1 − p₀) both at least 5 ("Yes: the normal curve fits." or, in red, "No: the curve fits poorly, so p is only rough. Use an exact binomial test (FitCheck)."). Step 3: z critical. Step 4: p̂ = x/n, SE = √(p₀(1 − p₀)/n), z obt, and a line on why the SE uses p₀. Step 5: the decision, "Report z = ...", and the difference p̂ − p₀.
- **Two-proportion *z*.** Step 1 has a column for each sample (x, n, p̂). Step 2 checks that each sample has at least 5 successes and 5 failures (if not: "Use Fisher's exact test (ChiTable)."). Step 4: the two proportions, the pooled p, SE = √(p(1 − p)(1/n₁ + 1/n₂)), z obt. Step 5: the decision, the report line, and the difference p̂₁ − p̂₂.
- **Ranges.** A typed mean and μ₀ from −10,000 to 10,000, an SD at most 1,000, N from 2 to 10,000 (as the older tests); with scores in D1, μ₀ may be any number below 50 digits. A count is a whole number from 0 to its n; n is a whole number from 1 to 1,000,000; p₀ is from 0.00001 to 0.99999. A number outside its range is refused with a sentence that gives the range, and nothing changes.
- **A *p* that rounds to α** shows its four digits in step 5 of the new tests ("(p = 0.04992: just below α = 0.050.)"), so "p = 0.050" never stands beside REJECT unexplained. For the one-sample *t*, the note that the printed table's row decides the other way takes that line when it applies.

The three older tests' pages, forms and numbers are beta 1j's, but for that one line of step 5: of the 54 routines of beta 1j, 14 changed (13 by the lines the new tests need, `tt_Step5` by that line), and 19 routines are new.

## Checks

- **Gate** (`tools/ppl_gate_v1e.py`): PASS. hp-prime-kit lint 0 errors; `lint_ppl` 4 problems, the same four as beta 1j (about the file's name); fleet names: 31 files, 2,410 routine names, 0 collisions.
- **`verify/verify_TTestLab_beta1k.py`**: 63 checks, 0 failed (`verify/verify_TTestLab_beta1k_output.txt`).
  - A, static: only the 14 routines meant to change did; the 19 new ones are the ones the header names; all 6 forms' fields are `{name,[0]}`; no menu item over 30 characters.
  - B, the older tests: 12 scripted sessions on beta 1j and beta 1k (every older example through its five pages and back, "Pooled or separate?", the flowchart with typed numbers and with D1 and D2, a refused N) draw the same screens, forms and boxes and return the same text.
  - C, arithmetic through `tt_Calc`, every tail and α the menus offer: the one-sample *t* from summaries (2,160 cases) and from scores (360, against `scipy.stats.ttest_1samp`), the one-proportion *z* (2,160, against statsmodels' `proportions_ztest` with the SE from p₀), the two-proportion *z* (2,160, pooled); z critical against the normal quantile.
  - E, the book: Student's sleep data give t(9) = 4.06, p = 0.003, SE 0.3890, t critical 2.262, d = 1.28 (Chapter 9); *Castaneda v. Partida* gives z = −29.11 with n p₀ = 688.2 and n(1 − p₀) = 181.8 (Chapters 5 and 12); the Rossi counts give z = −1.965, p = 0.049, pooled p 0.2639, SE 0.04241 (Chapter 11); Chapter 9's practice problems 2 and 3 come out as t(15) = −1.00 with t critical −1.753, and z = 2.00, p = 0.023.
  - F, every cancel and refusal of the new code: 15 ways out before the first page (Esc at each menu, Cancel on each form, D1 missing, short, or holding a 50-digit score), each returning "TTestLab: cancelled" with nothing drawn; Cancel and Esc inside a session leave the test, its numbers and its pages as they were; 25 refused numbers, each with its sentence, word for word, once.
  - P, the notes: the count check of step 2 both ways for each *z*-test, "just below" and "just above" α, the table-row note, the soft keys, the Tails menu in each test's symbols, 37 scores in D1 ("... and 27 more"), a *d* of 200,000,000 printed as "> 999.99" on the new step 5 and on the older one, and no menu of more than eight items (a ninth is cut off at the bottom of the calculator's screen: see TTestLabG's note).
  - H, help: three pages with the one header; pages 1 and 2 are beta 1j's but for the page count and one footer; every line inside the screen at the calculator's glyph widths.
  - D, layout over 303 distinct screens, with the largest numbers the forms allow: no firm overlap, no number cut short, every text ending by x = 314, commas in every number of 1,000 or more.
- **Monkey test** (`tools/monkey_chunks_v1.py ... 14 0 1000 --lists`): 1,000 of 1,000 runs OK (`verify/round14/mk/TTestLab.jsonl`).
- **Label monkey** (`tools/monkey_labels_v1.py 300`): on the build before the last it found one firm overlap, "Cohen's d = −34,200,918,…" over "magenta area = p" (beta 1j has it too; `tt_DS` is the fix). On the final file: no number cut short and no firm overlap. It still lists 8 lines as running off the screen by its estimate of 6.5 px a character: seven help lines (six of them the version before's) and step 1's H₀ line. At the calculator's glyph widths all of them fit (checks H3 and D3), and the Virtual Calculator drew them whole.
- **Virtual Calculator 2.4.2** (build 2026-09-09, under Wine in the cloud workspace, 14 November 2026, 22:02): Program Catalog > Edit > Check: "No errors in the program". The checked file went into starter pack v20 before any run. Then run from the catalog (22:05 to 22:09): the start menu and its list of new examples, each new example's five steps, the Tails menu, the form for one proportion and its Cancel, the box for "Pooled or separate?", the three help pages, and the result the program returns. The numbers on those pages are the harness's. Fourteen of the screens were read at full size in the run of a first build (21:29 to 21:34; two changes followed, the start menu's list and Cohen's *d*, each with its own Check and run). The program's own pages, 25 of the 37 captures and 12 of the 14 read, are the same pixel for pixel in the last run; the other captures are menus, a form and boxes with the Program Catalog or its clock behind them. Screens: `verify/round14/screens/TTestLab_*.png`; the record: `verify/round14/vc_checks.txt`.

## On a G1 or a G2 (not yet run)

From least to most risky:

1. Program Catalog, TTestLab, Edit, Check: "No errors in the program".
2. Run. The start menu has six items, all on the screen. "Examples: one sample, z-tests" opens a list of three; Esc there comes back to the start menu.
3. Student's sleep: step 1 shows ten scores in two rows of five; step 4 ends "= 1.580/0.3890 = 4.06"; step 5 reads "Report t(9) = 4.06, p = 0.003, two-tailed".
4. Grand juries: the soft keys read "2 dist" and "4 z"; step 2 shows "n p₀ = 870 × 0.791 = 688.2"; step 5 shows "z obt = −29.115" with the magenta line at the plot's left edge.
5. Re-arrest: step 4 ends "= −0.08333/0.04241 = −1.96"; step 5 reads "Report z = −1.96, p = 0.049, two-tailed".
6. Menu, Choose the test, One mean, Raw scores in D1, with ten or more scores in D1: the form asks for μ₀ only. Cancel there leaves the test on screen as it was.
7. One mean with a negative μ₀ (mean 3, SD 2, N 9, μ₀ −4): step 4 shows "(3 − (−4))/0.6667". The bracket depends on the calculator's own minus sign (`CHAR(8722)`); the Virtual Calculator was not asked this.
8. One proportion with x = 2.5: a box, "x, the number of successes, must be a whole number from 0 to n. Choose Edit the numbers to change it.", then the menu.
9. Menu, Pooled or separate?, on a *z*-test: the box that says the test has no such choice.
10. Help: three pages; on page 3 the π of "Z-Test: 1 π" is drawn.
11. Time steps 3 and 5: the curve now asks `tt_Dens` for each of its 297 columns, one call more than before for each. On a G1 note whether the page is slower than beta 1j's.

## Unresolved

- Not run on a G1 or a G2.
- Each value of step 4 shows 4 significant digits, so a student who divides the numbers on the page can differ from it in the last digit (−0.4013/0.01378 is −29.12 by hand; the page says −29.11, which is right). Help page 2 already says that step 4 keeps 4 digits; the older tests behave the same way.
- The two proportion tests share the counts of sample 1, so the form for one proportion opens with whichever x and n were last on screen.
- A *t* that rounds to zero from below prints "−0.00" in the PC harness (so did beta 1j); what the calculator prints there was not seen.
- The menus and boxes of a run started from the Program Catalog are drawn over the catalog on the Virtual Calculator, not over the step page (seen in `TTestLab_tails_twoprop.png`). The menu code is beta 1j's.
