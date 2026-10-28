# SeizureLab beta 1a: notes (21 Oct 2026)

| | |
|---|---|
| **File** | `/home/claude/new6/SeizureLab_beta1a.txt`: 2,771 lines, pure ASCII, LF. Entry `EXPORT SeizureLab()`; tag `sz_`; Home exports `SZ_...`. |
| **Earlier version** | Beta 1 is kept, unchanged. |
| **What changed** | `SeizureLab_beta1a_CHANGES.md`: one line per review item. |
| **Where it has run** | **Only in the PC harness so far: not on the emulator or a calculator.** |

The beta 1 NOTES (`SeizureLab_beta1_NOTES.md`) still describe the menus and formulas. Below is what is different, the checks, and
the full device checklist for beta 1a.

## What is different for the user

- **Bayesian page.** It shows "Least n, all +, P ≥ 0.95: this N 22; N → ∞ 28" and "ENFSI Table 4 takes N → ∞ (it assumes N ≥ 50)".
- **Weight page.**
  - It uses √((N − n)/N) and shows the CI's half-width.
  - ENFSI §7's example (N = 100, n = 23, mean 0.265 g, SD 0.023 g) gives 26.50 g, CI 25.63 to 27.37 g (± 0.8728). ENFSI prints 26.500 ± 0.873 g: the factor is the same, √(77/100) = 0.877, and ENFSI rounds t to 2.074.
- **Long computations.** A busy box with a moving bar says "Esc = stop. A large N or strong prior can take a minute or more on a G1". Esc gives "stopped" for the Bayesian least n, or for the rest of the table.
- **Help now has eight pages.** Page 6 is new, "Checking against ENFSI (2009)", with live numbers. Page 7 lists the keys page by page; page 8 gives the sources with the UNODC link.
- **Key legends.** Each page's footer names its own keys:

  | Page | Footer |
  |---|---|
  | Hypergeometric | "+/- = n, Left/Right = x, Ent = menu" |
  | Binomial | "Up/Down = neg, Left/Right = N, Ent = menu" |
  | Bayesian | "+/- = n, Left/Right = x, Ent = menu" |
  | OC | "+/- = n, Left/Right = θ, Up/Down = neg"; the worst false claim is now in the plot's corner |
  | Tables | "Left/Right = table or plot, Ent = menu" |

- **Set up.** It reports every clamp and rounding: negatives allowed (0 to 20), prior a and b (0.1 to 100), and a, b rounded to 2 decimals.

## Formulas: what changed

- **Weight SE** = N (s/√n) √((N − n)/N) (Cochran; ENFSI §7). **D1 is settled** (Roger, 21 Oct): beta 1's √((N − n)/(N − 1)) overstated the variance by N/(N − 1).
- **Bayesian least n.** The same definition; the search is now a bisection.
- **Ties.** P ≤ (1 − c)(1 + 1E-6) for the frequentist test, and P ≥ c − 1E-6(1 − c) for the Bayesian.
  - **Why 1E-6.** On the Prime, at N ≥ 1000, the tails carry about 2E-7 of relative error from 12-digit ln-gamma differences.
  - **Why relative to 1 − c.** A tolerance relative to c would move real answers when c is near 1.

## Sources

| Source | Status |
|---|---|
| ENFSI DWG (2009), *Guidelines on Representative Drug Sampling*, UNODC ST/NAR/38, https://www.unodc.org/documents/scientific/Drug_Sampling.pdf | **Read** by the second review, as text. Cited on help pages 6 and 8 and in the header. The program quotes it once on screen, the Table 4 note "A large seizure is assumed (N ≥ 50)." |
| Cochran (1977), *Sampling Techniques* | Cited for the variance of a mean without replacement. |
| Aitken 1999; Coulson et al. 2001; Tzidony & Ravreby 1992; Frank et al. 1991 | Marked **"not checked against the papers"**. Frank's multi-container method is not implemented. |
| Stoel & Bolck, "A correction to Tzidony and Ravreby (1992)" | Listed in ENFSI's references. Mentioned in the program, **not read**. Roger's library catalogue (`D:\Library_Catalog`) may have these papers. |

## ENFSI tables against the program (review item 12): for the record, not shown on screen

The second reviewer transcribed 427 cells from the guideline (his `enfsi_cmp.py`; verify R12 repeats the comparison):

| Tables | Cells |
|---|---|
| Table 1 | 126 |
| Table 2 | 252 |
| Table 3 | 18 |
| Table 4 | 18, plus the in-text a = 10, b = 1 → 19 |
| Table 5 | 12 |

**426 agree.** The one that does not is **ENFSI Table 2 (p. 14): N = 90, 99%, k = 0.7, 2 negatives**, where the guideline prints
**21** and the program gives **22**. Exact arithmetic: K₀ = 62, P(X ≥ 19 | N = 90, K₀ = 62, n = 21) = 0.011150 > 0.01, and at n = 22,
P(X ≥ 20) = 0.007561. So 22 is the least n. The neighbours (N = 80: 21; N = 100: 22) agree with the program. **Do not change the program
to match this cell.**

## What was checked: `verify_SeizureLab_beta1a.py`, 17,991 checks, 0 failures

**Parts A, B and C are beta 1's checks, on beta 1a.**
- **Updated** to beta 1a's wording, and to the item 2 and item 4 rules.
- **Exact references** honour the documented tie tolerance in exact fractions. Grid sizes are as in beta 1: 3,672 hypergeometric least-n cases with 20 exact ties, 2,820 Bayesian cases with 0 non-monotone, and every menu path at N = 10000, 1, 2 and 13.

**Part R covers the review, item by item.**

| Item | What was checked |
|---|---|
| R1 | The reviewer's seven slow cases give his SciPy values in 9–27 sums (≤ 2 log₂ Kr + 3). The N → ∞ search is checked against beta.sf on four cases. 150 typed priors (N ≤ 300) agree with a full scan, with 0 non-monotone. Esc pressed during Set up and during the Tables page gives "stopped" with no error, and the table's cache is reset. |
| R2 | FPC = 0.8775. The ENFSI example's half-width is 0.8728, and the page shows "95% CI: 25.63 to 27.37 g (± 0.8728)". |
| R3 | Both least n on the Bayesian page; help page 6 with its live numbers; one quotation. |
| R4 | The 12-digit decimal emulation (adapted from the reviewer's `prime12.py`). At N = 5000 the tie gives 0.0500000046777: met with 1E-6, not with 1E-9. Also N = 10000, 1000, 2000 and 10. In the harness, `sz_HypMin(5000, .95, .0501, 0)` = 1. |
| R5 | A phantom reading (2147483647, 0) ends a knob drag. A θ drag held still draws no extra frames. **A key pressed during a drag cannot be modelled** (the harness's key polls answer nothing while a finger is down), so it is checked statically and goes on the device checklist. |
| R6 | Four red LINE_P closing a rectangle, and no red RECT_P. |
| R7 | No arrow glyphs left. |
| R8 | Every text line within width (font 1 at 6.5 px, font 2 at 8 px) in four runs, including the reviewer's extremes; eight help pages. |
| R9 | Each footer, and that its keys act. |
| R10 | Every set-up message, including all clamps at once: still one MSGBOX of 5 lines or fewer. |
| R11 | Header and help sources. |
| R12 | The ENFSI tables: 427 cells, exactly the one known mismatch, confirmed exactly. |
| R13 | Style. |

**Part G** confirms that the changed and new routines are exactly those in the CHANGES file.

**Gate:** PASS (`gate_SeizureLab_beta1a_output.txt`).

## Left out, and why

- **ENFSI's Pcorr.** This scales the weight to the drug-positive units when some units tested negative. Help page 5 says it is not done here. It would be a small addition if Roger wants it.
- **ENFSI's RSD < 10% acceptance rule** for the weight. Not shown.
- **The beta 1 omissions still stand:** no Poisson OC, no CAS, N ≤ 10000, no multi-container sampling.

## DEVICE CHECKLIST (beta 1a; in order; expected values from the harness)

1. **Paste and check.** Paste into the Connectivity Kit, then run Check in the Program Catalog. Expect no syntax error.
2. **Opening page.** Run `SeizureLab`. Expect 23 red squares of 100, the four-line DISCLAIMER and the orange one-liner. No line should run off the right edge.
3. **Hypergeometric page.**
   - Expect:
     - "p₀ = 0.90 (K ≥ p₀N), c = 0.95, K₀ = 89"
     - "Least n (0, 1, 2 negatives): 23, 36, 46"
     - "If K = K₀ = 89: P(X ≥ 23) = 0.0472"
     - "SUPPORTED"
     - "Lower 95% confidence bound: K ≥ 90 (90.0%)"
   - **The 23 bar must be magenta inside a red outline, not solid red.**
   - "x -" gives P = 0.2253, NOT supported. Then "Min n" gives n = 36.
4. **Binomial page.**
   - Expect "Hypergeometric (N = 100): 23, 36, 46", "Binomial (N → ∞): 29, 46, 61", "Binomial: 6 more (0 neg), the safe side".
   - The caption reads "P(≤ 0 neg), cut at 0.2".
   - **Up** gives 1 negative; **Left** gives N / 10, and Right gives back N = 100. **Time the recalculation.**
5. **Bayesian page.**
   - Expect "P(at least 90 of 100 drug | data) = 0.9580", "Least n, all +, P ≥ 0.95: this N 22; N → ∞ 28", "ENFSI Table 4 takes N → ∞ (it assumes N ≥ 50)".
   - **Prior** switches to Jeffreys: "this N 16; N → ∞ 18".
6. **OC page.**
   - Expect "Worst false claim, K₀ = 89: P = 0.0472" in the plot's top corner, the readout "true θ = 0.800 (K = 80): P(support) = 0.0027", and the footer "+/- = n, Left/Right = θ, Up/Down = neg".
   - **Drag the knob**, and while still dragging **press a key**: the drag must end.
   - Drag in the plot, hold the finger still, and the screen should not flicker. **Time a drag frame.** Zoom.
7. **Weight page.**
   - **Example:** expect SE = 0.3134 g, "95% CI: 49.82 to 51.24 g (± 0.7089)", "One-sided 95% lower bound: total ≥ 49.96 g". A tap on the bar shows "t = 2.262 (CI), 1.833 (bound); FPC = 0.9487".
   - **ENFSI check:** Type n = 23, mean 0.265, SD 0.023. Expect 26.50 g, "95% CI: 25.63 to 27.37 g (± 0.8728)", "≥ 25.78 g". Help page 6 states the same.
8. **Tables page.** Watch the moving bar and press **Esc** part-way: expect "stopped" cells, and a full recompute when the page is reopened. Otherwise expect the beta 1 values: Hyper 8, 12, 19, 23, 26, 28, 28, 29 and Bayes 8, 12, 19, 22, 25, 27, 27, 28 for p₀ = 0.90.
9. **Slow case.**
   - Set up N = 10000 and prior a = 1, b = 100.
   - **Time** the "Computing ..." box with its moving bar: 21 sums. Estimate 10–40 s on a G1, but untimed.
   - Repeat and press **Esc**: the Bayesian page shows "Least n: this N stopped; N → ∞ stopped".
10. **Set-up messages.** Type negatives 33 and a = 0.333 together. One MSGBOX should say "Negatives set to 20 (0 to 20). Prior a, b rounded to 2 decimals."
11. **The exact ties.**
    - N = 10, c = 0.90, p₀ = 0.95: Least n = 9.
    - **N = 5000, c = 0.95, p₀ = 0.0501: Least n (0 neg) = 1.** This is the 12-digit case: in emulation, beta 1 would have given 2.
12. **Help.** Eight pages, each line inside its box. Page 6 shows 23, 36, 46; 28 and 22; ± 0.8728 g. Page 8 shows the UNODC link in two lines.
13. **Quit.** Expect `SeizureLab: N = 100, p₀ = 0.90, c = 0.95: test 23 (all positive; Bayes 22)`.
