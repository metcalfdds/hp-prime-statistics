# FitCheck beta 1i: changes (15 November 2026)

Round 16. Built from beta 1h by exact replacements (`verify/round16/make_fitcheck_1i.py`; a replacement that does not match exactly once stops the build). 3,892 lines (beta 1h: 3,390).

## Why

Three reasons, in the order they came up.

1. **An outlier test for a small sample.** Roger, 15 November 2026, had a book of tables checked against fresh calculations (Zwillinger & Kokoska, 2000; the report is `docs/dev/crc-table-check-2026-11-15.md`). Its table of Dixon's ratios (p. 251) is off by more than rounding in 60 of 272 values: it is Dixon's 1951 table, whose errors are documented (McBane, 2006), with a misprint of its own (.745 for .765). The report's fourth suggestion for our programs was "An outlier test (Dixon's ratios with exact p-values) in FitCheck", and of the six suggestions Roger said: "Add all please." A program that integrates gives a p for the sample's own ratio, where a table gives a yes or no at one level from numbers that may be wrong.
2. **A refused sample damaged the loaded one.** Found while FitCheck's loader was being read for the new page. With a sample loaded, "My values in D1" with every value the same was refused, as it should be, but the loader had already replaced the stored values, and "The last sample again" then stopped with an error in the Q-Q page (in the PC harness: "index 5 out of range"). This is old code, beta 1h's and before.
3. **Axis numbers that left the screen or were cut.** Found by this round's layout check, run with data in the thousands and the millions: the last number of the ECDF's axis and of the chi-square curve's axis could begin so far right that it ran past the screen's edge, and a data value wider than its 40 pixels was cut on the Q-Q plot's y axis and the ECDF's x axis. Old code too.

**What was read.** The library in `D:\HP-Prime` was searched on 15 November 2026: no program there has Dixon's test (the TI STATLITE program's "Outlier test" is the 1.5 × IQR fences). On the web, the same day: which ratio goes with which n, from NIST's Dataplot reference manual ("DIXON TEST") and the manual of the R package `dixonTest`, which agree; McBane (2006) for the distribution of the ratios as a double integral and for the errors in the printed tables. The page is written from that integral; no code was read.

## What changed

| What | Where (line numbers in `FitCheck_beta1i.txt`) |
| --- | --- |
| **The Outlier page.** The normality pages' fifth soft key, empty until now, reads Outlier. It opens a page with every value as a dot on a strip, the tested value in red, its gap as a red bracket and the range as a blue one, and under them the ratio as a formula in the sample's own ranks ("Low end: (x(3) − x(1)) / (x(13) − x(1)) = 0.593"), the p at that end, the p for either end, the other end's ratio, a sentence at α = 0.05 ("x(1) = −8.375: flagged as an outlier at α = 0.05." in red, or "not flagged" in green) and "A flagged value is one to check, not to delete." | `fc_DrawDx` (2355 to 2486), `fc_NorLoop` (2850 to 2927) |
| **The test.** Dixon's ratio by sample size: r₁₀ for 3 to 7 values, r₁₁ for 8 to 10, r₂₁ for 11 to 13, r₂₂ for 14 to 30. The ratio is worked out at both ends and the larger is tested. | `fc_DxCalc` (2314 to 2343), `fc_DxRat` (2219 to 2231), `fc_DxNm` (2249 to 2252), `fc_DxFmt` (2237 to 2246) |
| **Its p, computed.** The chance that a normal sample of n gives a ratio this large at one end is a double integral over the tested value and the value at the range's far end, done with 20 × 20 Gauss–Legendre points. The 20 nodes and weights are written by the build from NumPy. | `fc_DxTail` (2262 to 2308, with its comment from 2182); `fc_Init` (389 to 438) |
| **Where the test is not offered**, the key gives a sentence and works nothing out: more than 30 values ("Dixon's outlier test is for a small sample: 3 to 30 values. This sample has 432 values."), and a sample in bins ("… so it has no single values to test."). | `fc_DrawDx` |
| **A new preset, Darwin's 15 differences** (crossed minus self-fertilized, the pairs RankLab has). It is the seventh item of "Load a preset", "Darwin's differences: outlier", and the fourth of the Normality menu. | `fc_PreDarwin` (3291 to 3300), `fc_Presets` (3374 to 3399), `fc_MNorm` (3771 to 3788) |
| **Two menus are a line longer, and three items moved down one.** In "Load a preset" the draft lottery is item 8 (it was 7) and the illustrative binomial item 9 (it was 8). In the Normality menu "My values in D1" is item 4 before a sample is loaded and item 5 after (it was 3 and 4). | `fc_Presets`, `fc_MNorm` |
| **The mended loader.** A sample's spread is now tested on a sorted copy before anything stored is replaced, for single values and for bins, so a refused sample leaves the loaded one as it was. | `fc_NormSet` (1434 to 1492), `fc_NormSetBin` (1499 to 1527) |
| **The mended axes.** A number is measured before it is drawn. The last number of an axis is kept on the screen, and an axis with a number too wide for its place is written in the Prime's scientific form (1.2ᴇ6). Where every number fitted, nothing moved. | `fc_AxLb` (2503 to 2512), `fc_AxWide` (2518 to 2532), `fc_DrawCurve` (1911 to 1980), `fc_DrawQQ` (2561 to 2643), `fc_DrawECDF` (2700 to 2783) |
| **Help has 12 pages** (8 before). Pages 7, 8 and 9 are the outlier test's: "Outliers: Dixon's test", "Outliers: which ratio", "Outliers: the p and its limits". Page 10, "Keys and presets", is the first two paragraphs of beta 1h's page 7 with Outlier among the soft keys; page 11, "Home variables", has them on a page of their own; page 12, "Credits", is beta 1h's page 8. Page 1 has one clause more. Pages 2 to 6 are beta 1h's word for word. | `fc_Help` (3614 to 3684) |
| **Home gets `FC_R` and `FC_PR`**, Dixon's ratio and its either-end p. A session that never opens the Outlier page leaves them as they were. | `fc_DxCalc`; the exports near the top of the file |
| **The closing line** adds the test once the page has been opened: "FitCheck: W = 0.9008, p = 0.0978; Dixon r22 = 0.593, p = 0.0321 (either end);". | `FitCheck` (3836 to 3892) |
| The opening page names the version and the test ("… Dixon's outlier test; the exact binomial test"). | `fc_Opening` (3687 to 3710) |

**The ratios.** With the values in order, x(1) ≤ … ≤ x(n), and the low end tested:

- r₁₀ = (x(2) − x(1)) / (x(n) − x(1)), for 3 to 7 values;
- r₁₁ = (x(2) − x(1)) / (x(n−1) − x(1)), for 8 to 10;
- r₂₁ = (x(3) − x(1)) / (x(n−1) − x(1)), for 11 to 13;
- r₂₂ = (x(3) − x(1)) / (x(n−2) − x(1)), for 14 to 30.

The high end is the mirror image. The first digit says whether the gap ends at the nearest value or at the second-nearest; the second says how many values the range leaves off at its far end. The later ratios are there because a second outlier, beside the first or at the far end, would hide the first.

**The p and what it means.** The page gives the p of the tested end alone and, as its headline, the p "for either end", which is twice that and at most 1. Twice the one-end p is an upper limit, not the exact chance that either end's ratio is this large: for r₁₀ the two ends cannot both give a ratio above 0.5, so there the doubling is exact, and for the other ratios it is a little conservative (simulated at the two-sided 5 % point: 0.0466 to 0.0500 for sample sizes from 5 to 30). The page says "Either end: twice that, at most." The sentence at α = 0.05 goes by the p as the page shows it, to four decimals.

**Accuracy.** Against a fine-grid reference, at every n from 3 to 30, the p's relative error is at most 0.026 % where the p is above 0.001 and at most 0.14 % where it is above 0.0001 (the header promises 0.05 % and 0.2 %). The reference is itself held to a grid twice as fine, to the closed form at n = 3, to 1,000,000 simulated samples at each of ten sizes, and to McBane's eight printed values of r₁₁.

**Darwin's differences.** n = 15 takes r₂₂. At the low end r₂₂ = 9.125 / 15.375 = 0.593, with a one-end p of 0.0161 and an either-end p of 0.0321, so the lowest difference, −8.375, is flagged. The plain r₁₀ at that end would be 0.134 with a one-end p of 0.42: the second low value, −6, hides the first. That is the page's lesson, and the preset's note says where to look ("Two differences are negative, far below the rest. The Outlier key tests the lowest of them (Dixon's ratio).").

## Checks

- `verify/verify_FitCheck_beta1i.py`: **66 checks, 0 failed** (output beside it).
  - The build (T1): the script makes the filed file byte for byte.
  - The arithmetic (A1 to A12): `fc_DxTail` against the reference at 1,389 ratios, n from 3 to 30; its edges; the reference against a finer grid, the closed form at n = 3, simulation and McBane's values; the printed two-sided Q table for n = 3 to 10 is the one-sided point at α/2 to within 0.0053, and its two largest gaps are the two entries McBane names; on 168 random samples the ratio at each end and its kind are as NumPy has them and the larger end is the one tested; Darwin's 15 differences are RankLab's pairs and, times 8, Fisher's whole numbers; the two-sided simulation above; Shapiro–Wilk on the same sample is untouched (W = 0.9008, p = 0.0978, as SciPy).
  - The Outlier page (P1 to P11): Darwin's page line for line; the brackets and the red dot pixel for pixel; a high-end case; tied values ("A ratio of 1 here means tied values: p means little."); the two ends equal, and equal at the decimals shown; the sentence following the p as shown, at 0.0500 and 0.0499; the two refusals; numbers near 0.0000002 and near 1,234,570 keep the decimals their scale needs; 84 random samples, three at every n from 3 to 30, each page the model's line for line.
  - Every way in and out (V1 to V14): Outlier from the Q-Q, ECDF and Tests pages and back by each of those keys; the closing line with and without the page; Esc, Enter and Menu from the page; taps, arrows and + on it (nothing changes); Bins from it; a new sample clears the test and "The last sample again" keeps it; both menus with their new items; Esc at each of three menus; the mended fault, for single values and for bins; "My values in D1" refused with two values; `FC_R` and `FC_PR` at Home.
  - Against beta 1h (R1, R2): over 40 seeds of the monkey, beta 1h and beta 1i with its three new entrances shut give the same verdict, boxes and closing line and the same 1,320 screens text for text, but for the opening pages; the items that moved do, through the real menus, what they did at their old places.
  - The axes (L1 to L7): the faults as beta 1h drew them and as beta 1i draws them; where every number fitted the pages are the same pixel for pixel.
  - The help (H1 to H8): twelve pages; pages 2 to 6 and 12 word for word; pages 7 to 11 as written; no line longer than 46 characters or wider than 296 px (widest 260), no page over 14 lines.
  - Static and layout (G1 to G8, D1 to D3): no `!=`; code ASCII; LOCAL lines of six names at most; no source line over 250 characters (beta 1h had two); the 20 nodes and weights are NumPy's to 12 decimals; every menu item at most 30 characters; the header's file map true; commas; no overlap or text off the screen on 566 different screens; no number cut short; no menu title over 31 characters.
- Gate (`tools/ppl_gate_v1e.py` against beta 1h; `verify/round16/gates/FitCheck_beta1i.txt`): **PASS**. hp-prime-kit lint 0 errors; `ppl_check_v5` clean; `lint_ppl` 10 reports, beta 1h's 9 and one more of the same kind for the new Home variable `FC_R`; no name collision in the fleet (31 files, 2,480 routine names).
- Harness smoke test: no error, 0 warnings. `tools/text_overlap_v1.py --walk`: no collision, as in beta 1h.
- Help layout at the calculator's glyph widths (`verify/round16/helpcheck_r16.json`): 12 screens, no reports.
- Monkey test: **1,000 of 1,000 runs OK** (`verify/round16/mk/FitCheck.jsonl`; base 16, `--lists --writes D`), run on the file as filed. In its first 300 sessions the Outlier page gave its verdict in 19 (`mk/reach_r16.txt`), so two **directed** sets were added, each of 200 sessions that begin on the Outlier page and then take the monkey's random keys, taps and menu picks: Darwin's differences (**200 of 200 OK**, the page in all 200) and the monkey's own list in D1 (**200 of 200 OK**; the page in 82, the list refused in the others) (`tools/monkey_directed_v1.py`; `mk/directed/FitCheck_outlier_darwin.jsonl`, `FitCheck_outlier_mydata.jsonl`).
- **HP Prime Virtual Calculator 2.4.2 (build 2026-09-09): Check "No errors in the program", and a run** (`verify/round16/vc_checks.txt`, `verify/round16/screens/FitCheck_*.png`). Darwin's differences from the Normality menu, with its note; the Q-Q page with the Outlier key; the Outlier page with the numbers above; the two refusals (the Rossi ages, the crimtab heights); an empty D1 refused; the twelve help pages, every line inside its frame; the closing line with the test in it, whole in its box, and the longest line the program can give (a fit on bins, W and Dixon's test: 104 characters), whole there too in five lines.

## On a G1 or a G2 (not yet run)

1. Normality > Preset: Darwin's differences, a key, then the Outlier soft key. Note how long "working" stands: the p is 400 evaluations of a product of normal tails, and nothing here has been timed on a calculator. The page should read "Dixon's r₂₂ = 0.593, p = 0.0321 (either end)" and "x(1) = −8.375: flagged as an outlier at α = 0.05.".
2. Q-Q, then Outlier again: the page should come back at once (the test is worked out once for a sample).
3. Menu, Normality > Preset: Rossi ages, a key, Outlier: the sentence about 3 to 30 values, and nothing worked out.
4. Menu, Normality > The last sample again: the Rossi ages' Q-Q page.
5. Menu > Help, pages 7 to 12: every line inside the frame.
6. Menu > Quit after step 1 alone: "FitCheck: W = 0.9008, p = 0.0978; Dixon r22 = 0.593, p = 0.0321 (either end);", whole. At Home, `FC_R` = 0.5934… and `FC_PR` = 0.0321….

## Unresolved

- Nothing has run on a G1 or a G2, and the Outlier page's wait there is not known.
- **The book names some menu items by number.** Three items of FitCheck moved down one (the table above). Draft 37 must be searched for them.
- Rorabacher (1991), the source of the Q table most chemistry texts print, was seen by title only; its volume and pages are still to be confirmed before the book cites it.
- "Either end" is twice the one-end p, an upper limit. The exact two-sided p for r₁₁, r₂₁ and r₂₂ would need the joint distribution of the two ends' ratios, which is not computed.
- On the Virtual Calculator some key presses did nothing on pages that wait in the fleet's `GETKEY` and `MOUSE` loop (`verify/round16/keyprobe_r16.txt`). Whether a calculator loses presses is not known; nothing was changed for it in this round.
