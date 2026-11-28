# TTestLab beta 1n: changes (28 November 2026)

Round 21 of 28 November 2026 (`verify/round21/README.md`). The read-through of the book's Draft 127 found, as its item A10, that the steps which work the arithmetic out do not always check on a calculator from the numbers they show, and Roger, at 01:31, accepted that item with the rest: "You're right about all these things—please go ahead and fix them and reorganize and rearrange as necessary".

## What was wrong

Steps 2 and 4 write the formula, put the numbers in, and work it out line by line, so that a student can follow the arithmetic and check it. Beta 1m showed each number on them as the exact value rounded to 4 significant digits, and a line worked from rounded numbers can miss in its last digit or two. TTestLab's own age-at-arrest example (the book's Figure 11.4) showed, on step 4:

```
   = √1.745 × √0.05499 = 1.321 × 0.2345
   = 0.3097
```

and 1.321 × 0.2345 is 0.30977, which a student rounds to 0.3098. TTestLabG's draft lottery (the book's Figure 11.2) was further off: 106.1²/182 is 61.85 where its step 4 said 61.90, (61.90 + 55.17)² is 13,705 where step 2 said 13,707, and 13,707/37.81 is 362.52 where step 2 said 362.56 (`TTestLabG_beta1k_CHANGES.md`).

## What changed

1. **The chain** (lines 475 to 733, new). Each number on steps 2 and 4 is now worked out from the numbers shown before it, as a student with a calculator would work it, and rounded to the digits it is shown with; each result is shown with fewer significant digits than the numbers it is worked from. `tt_WkAt(k)` works the chain with SE at k significant digits (the numbers it comes from at k + 1, and at k + 2 or k + 3 where they are squared and pooled first), and `tt_Work()` takes the smallest k, from 4 to 8, at which the chain gives the program's own SE, df and t or z at the digits shown, so the answers on the screen are still the exact ones. A number that is exact (a typed value, a mean that ends, the sum or difference of two numbers shown) is shown whole, without zeros after its last digit; one that had to be rounded keeps its zeros (1.74480). A number that would need more than 11 decimals, or is 1E12 or more, is shown in the calculator's scientific form with its significant digits (1.142ᴇ−8), because the fixed form holds no more (beta 1m showed such a number as 0.0000000000). New routines: `tt_DcK` (line 497), `tt_TrD`, `tt_WkD`, `tt_RdC`, `tt_RdK`, `tt_ExC`, `tt_Txt`, `tt_TyD`, `tt_WV`, `tt_Dev`, `tt_WkAt` and `tt_Work` (line 725).
2. **Step 2 of the separate-variances test** (`tt_Step2`, lines 1338 to 1369) writes a and b from s on lines of their own, "a = s₁²/N₁ = 106.1437²/182 = 61.9038", and works df from them, "df = 13,707 / 37.806 = 362.56"; the numerator is (a + b)² worked from the a and b on that screen.
3. **Step 4** (`tt_Step4`, lines 1430 to 1493, and `tt_Step4N`, lines 1718 to 1769) shows the chain's numbers. The t and z lines take three lines (the formula, the numbers, the quotient); the pooled test's roots, their values and SE take a line each; the one-sample test's mean and SD stand on one line and N and μ₀ on the next; the two-proportion test's pooled p and its root take two lines each, and its 1 − p is the complement of the p it shows, exactly. So the largest numbers the forms take still fit: means of −9,999.99999 and 9,999.99999, two n of 1,000,000, a pooled p below 0.0001 (part D of the verify script). The age-at-arrest example's step 4 now reads:

   ```
      = √1.74480 × √0.0549853
      = 1.3209 × 0.23449
      = 0.3097
   t obt = (x̄₁ - x̄₂)/SE
         = (15.89 - 16.57)/0.3097
         = −0.68/0.3097 = −2.20
   ```

4. **Help page 2** (`tt_Help`, line 2366) says "Steps 2 and 4 work each number from those shown above it, so / each step checks; rounding sooner can change t obt (example 1)", where beta 1m said "Step 4 keeps 4 significant digits at each step; rounding sooner / can change t obt (see example 1)".
5. **The age-at-arrest note** (`tt_BookNote`, line 1411) names the root as step 4 now shows it: "The lecture rounds √0.0549853 to √.05, SE to .29," (it said √0.05499).
6. The header: the version (line 4) and the history note (lines 21 to 37). No other routine, menu, number or word changed: steps 1, 3 and 5, t crit, p, Cohen's d and the decision are beta 1m's.

The program is 2,534 lines (beta 1m: 2,228) and 111,961 characters (98,945).

## For the book

- The table of the *Statisticles* in "How to use this book" names TTestLab beta 1n.
- Figure 11.4 (the age example's step 4) is taken again, because its lines are new; its caption's "(15.89 − 16.57)/0.3097 = −2.20" still holds.
- No menu item moved.

## Checks

- `verify/verify_TTestLab_beta1n.py` and its saved output: **26 checks, 0 failures**. A, the header and the history note; every routine of beta 1m is beta 1m's, word for word, but the five the note names; the twelve new routines; no `!=`; ASCII code. C, every relation on steps 2 and 4 read off the screen as a student reads it and worked in exact decimal arithmetic, rounded half away from zero to the digits shown, for the six examples and 1,759 random cases of all six tests, typed and from raw scores; the last numbers (SE, df, t or z) against the exact ones (SciPy and Python's own arithmetic, not the program's); and k the smallest that does it. C3, the limit below. E, the book's Figure 11.4 line by line. H, help page 2, and every help line inside the screen by the calculator's glyph widths. D, the largest numbers the forms take, typed and from raw scores: no firm overlap or overrun (`text_overlap_v1`), and every text inside the screen by the glyph widths (the widest ends at x = 303). B, the monkey on beta 1m and beta 1n, seed by seed, 300 runs: every run takes beta 1m's path, every one of the 1,538 screens whose texts differ is a step 2 or step 4 page or help page 2, every number of 1,000 or more has its commas, and nothing new overlaps or is cut short (the two new help lines pass the edge by `text_overlap_v1`'s average widths and stand inside it by the calculator's own, H2).
- **A device fact, put into the harness the same day** (`tools/prime_facts_v1.py`, fact 8). A one-sample step 4 with s = 162.45 and N = 100 showed SE = 16.24 in the harness, where a student works 16.245 and rounds it to 16.25. On the Virtual Calculator, ROUND(162.45/10, 2) is 16.25: the calculator rounds the decimal it holds, and a tie away from zero (`diagnostics/RoundProbe_beta1a.txt`, `verify/round21/vc_record.txt`). The harness's binary floats hold 162.45/10 as 16.244999999999997; with the fact, its ROUND gives 16.25 too.
- `tools/ppl_gate_v1e.py` against beta 1m (`verify/round21/gates/gate_TTestLab_beta1n.txt`): **PASS** (the kit's lint 0 errors, no hard error, the fleet's names clean).
- `tools/screen_text_v1.py` and `tools/fleet_names_v2.py` over the newest files: nothing against the rules, no collision.
- The monkey (`tools/monkey_v1b.py`, 1,000 runs with random lists; `verify/monkey_TTestLab_beta1n_output.txt`): **1,000 of 1,000 OK** (366 s).
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) in the cloud workspace, 28 Nov 2026 (`verify/round21/vc_record.txt`): Program Catalog > Edit > Check at 03:33 said "No errors in the program", and the checked file went into starter pack v29 before anything was run. Then, at 03:53, the age-at-arrest example's step 4 read line for line as above and as the harness draws it (`verify/round21/vc/22_tl_age_step4_x3.png`, the book's new Figure 11.4); help page 2's two new lines stood inside the screen; and the two-proportion test with 1 of 999,999 and 151 of 1,000,000, typed into its form, showed every line of step 4 inside the screen, down to z obt = −0.00015/0.00001233 = −12.17 (`36_tl_2p_step4_x3.png`).

## On a G1 or a G2

Not yet run on a G1 or a G2. The check, which takes five minutes:

1. Start TTestLab, choose **Example: age at arrest**, and tap **4 t**. Step 4 reads √1.74480 × √0.0549853, then 1.3209 × 0.23449, then 0.3097, and t obt = −0.68/0.3097 = −2.20.
2. In Home, work 1.3209 × 0.23449 (0.30974…) and −0.68/0.3097 (−2.1957…): rounded as the screen shows them, they are 0.3097 and −2.20.
3. Menu, **Examples**, **Drug use by sex (separate)**, and tap **2 df** and **4 t**: every line again works out from the line before it.
4. Menu, **Choose the test**, **Two proportions: z**; type 1 success of 999,999 cases and 151 of 1,000,000, and tap **4 z**: every line ends inside the screen, and p and 1 − p add to 1.
5. Menu, **Help**, page 2: the two lines on steps 2 and 4 end inside the screen.

## Unresolved

- **A t or z of 100,000 or more.** Where even SE at 8 significant digits does not give the exact t or z (7 of the 1,759 random cases, all typed dependent samples with an SD far below the mean, t from 167,735 to 10,878,370), step 4 shows the chain at 8 digits: every line still checks, and its t can differ from step 5's in the last decimals (by at most 1E−7 of t and the two roundings, C3). A student's data does not come near this; the forms take it.
- The harness's arithmetic other than ROUND is still binary, while the Virtual Calculator gave (1 + 1E−15) − 1 = 1E−15: a chain step that rests on a tie in a later digit could still differ between the harness and the calculator. With fact 8 in place, none of the 1,759 cases did.
- A sum with more than 12 significant digits (0.0078125 + 123,101) is shown on step 4 to 12 significant digits, while the Virtual Calculator held 13 (`vc_record.txt`); step 2's (a + b)² is worked from a and b, as the calculator works it.
