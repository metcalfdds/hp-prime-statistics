# ChiTable beta 3: changes from beta 2

*16 October 2026. **Not yet run on hardware, and nothing in it about the CAS has run on any calculator.** Beta 1j is the version both calculators ran (G2 and G1, 2026-09-09 firmware, 10 Oct 2026). Every beta 2 feature is kept.*

Beta 3 adds **exact answers from the CAS** behind the fence in BRIEF_CAS.md and Lessons Learned v7g §9b:

- every CAS call goes through one routine, `csCas`;
- CAS text is built from whole numbers only, by `csIStr`;
- the CAS is asked on page entry and only when the table has changed;
- every exact answer keeps the program's own decimal as its fallback;
- a badge, **exact (CAS)** or **decimal**, says which one is on screen.

**Untouched, checked byte for byte against beta 2 by the verify script:** `csCompute`, `csFisher`, `csFishW` (moved, not changed), `csCheck`, `csTotals`, `csAskAll`, `csNewTable`, `csSetAlpha`, `csDrain`, `csWaitAny`, `csBarDrag`, `csMorph`, `csCurve`, `csCvDraw`, `csBars`, `csMosaic`, `csEntry`.

The file grows from 2,716 to 3,244 lines, and from 62 routines to 75.

## 1 · Changes

Line numbers are beta 2's, then beta 3's.

### The three that matter most

1. **Fisher's exact p as a fraction** (new `csXFisher` 797). It is shown on results page 6 and on the Fisher plot: "p = 17/35 = 0.4857" for the lady tasting tea, [[3, 1], [1, 3]].
   - **The tables it adds:** exactly the ones `csFisher` adds. `csFishW` gives every table's probability, and a table counts when it is at most the observed one's times 1.0000001: csFisher's tolerance, which R and SciPy also use. Ties are therefore included; in the tea table, a = 1 ties with the observed a = 3.
   - **The CAS text:** the tables that count form one or two runs of a, the two tails. Each run becomes `sum(seq(comb(r1,csj)*comb(r2,c1-csj),csj,lo,hi))`, and the whole is divided by `comb(N,c1)`.
   - **Why `seq`:** a plain `sum` over the symbol `csj` sends Giac solving Gamma equations, even with whole-number bounds. This was seen in desktop Giac and the verify script shows it.
   - **The answer is checked:** it must be a fraction (`csIsFr`), or the decimal stays.
   - **Size guard:** if C(N, c1) has more than 100 digits (`csXDigC` estimates this in PPL, at most 2,000 LOG calls), the CAS is not asked at all.
2. **A new last results page, "Where the numbers come from"** (`csPageExact` 1733). It is page 7 of 7 for a 2 × 2, page 6 of 6 otherwise.
   - **2 × 2:** χ² = N(ad − bc)² / (r₁ r₂ c₁ c₂). The page shows the student's counts put in, then ad − bc and the product of the totals (the CAS, as exact integers of any size), then one fraction and csCompute's decimal. Next, Fisher's p as counting: P(a) = C(r₁, a) C(r₂, c₁ − a) / C(N, c₁) with the numbers in, then "34 of the 70 equally likely ways" and "p = 34/70 = 17/35 = 0.4857".
   - **2 × 3 / 3 × 2:** the first cell's (O − R·C/N)²/(R·C/N) written out, then the whole Σ (O − E)²/E as one fraction (`csXChi` 839).
3. **The CAS kit and its cache** (new section, 666–939).
   - `csIStr` (673) and `csCas` (691) are BRIEF_CAS's shapes. `csCas` uses the updated kit, which drops one surrounding pair of quotes, since HP's Commands reference says numerical-mode answers come back as strings.
   - **One change from the kit:** the parameter of `csIStr` is `csIv`, not `csN`, because `csN` is already this program's grand total.
   - **The cache** (`csXEnsure` 880) is keyed on the table's shape and counts (`csXKeyOf` 771). Turning pages asks nothing new. A changed table (a drag, ×10 N, Restore, a new table) asks again, once, at the next page entry.

### The rest

4. **`csFishW` moved** from the Fisher plot section (beta 2 2127) to just after `csFisher` (597), unchanged. `csXFisher` and results page 6 need it, and a PPL routine must be defined before its first use. A pointer comment stays at the old place.
5. **Results page 6** (`csPage2x2` 1268 → 1683):
   - `csXEnsure(0)` at the top.
   - **The Fisher p takes two lines:** the label at y 85 (beta 2 had label and p on one line), and the p as `csXPText(33)` at y 98 with its badge at x 236.
   - **The lines below move down:** 104 117 130 143 162 180 193 → 111 124 137 150 167 184 197. The last line still ends above the strip at 218.
6. **`csResults`** (1307 → 1833): `rsN` is 6 or 7 (was 5 or 6). Page 6 is `csPage2x2` only for a 2 × 2; the last page is `csPageExact`.
7. **Fisher plot:**
   - `csFishDraw` (2162 → 2657): the title "Every 2 × 2 with these margins" → "Tables with these margins", so the badge fits beside it at (236, 7). The bottom line "red + magenta = Fisher two-sided p = …" → "red + magenta: " + `csXPText(32)`.
   - `csFishPlot` (2272 → 2773): `csXEnsure(0)` as the plot opens, and again after a Menu action that changed the counts.
8. **Help:**
   - page 1's page list now ends "… meaning, 2x2, exact answers." (3073);
   - `csDfPage`'s footer reads "Any key = page 5" (3052);
   - **new page 5, "Exact answers (CAS)":** the exact χ², Fisher as counting with the tea example, and the badge.
9. **Display helpers.**
   - `csBadge` (899) draws "exact (CAS)" or "decimal" in dodger blue.
   - `csXPText` (914) and `csXX2Txt` (929) choose among three forms: the fraction and decimal when they fit; the decimal plus "(140-digit fraction)" when they do not, so a fraction is never cut silently; the decimal alone when there is no exact answer.
   - `csIsFr` (717) accepts only digits with at most one "/" and a leading "−", so a decimal handed back as a Home real counts as "no exact answer".
   - `csFrDig` (740) counts digits.
10. **New file-level state** (341–354), 12 names on two lines, all checked case-insensitively against the built-ins: `csCasOK`, `csXKey`, `csXFSt` (0 not asked, 1 exact, 2 CAS failed, 3 too big, 4 none), `csXCSt`, `csXFr`, `csXSum`, `csXX2`, `csXAd`, `csXPr`, `csXS`, `csXT`, `csXDg`. All are initialised in `csInit` (3150).
11. **Header:** "beta 3", a dated "What changed" paragraph, "WHAT IT DOES" item 3 (seven pages), and the exact formulas under THE ARITHMETIC. The tested-on line says betas 2 and 3 have not run, and that the CAS lines have never run on a calculator.
12. **Guide:** `chitable-guide_beta3.md`. It has the same structure as beta 2's, with a new "Exact answers" section, the 7-page list, help page 5, the exact values of the examples, beta 3 first-run checks, and the CAS notes in the library check.

**CAS variable:** `csj`, a tagged name. No `#cas` block, `CAS.name()` call, purge or Python `cas` is used.

## 2 · Gate (final run, after the kit's quote-stripping update)

```
=================== ChiTable_beta3.txt ===================
--- 1. kit lint (errors) ---            kit lint: 0 errors
--- 2. ppl_check tally (NEW)  ---       1 W3
--- 2. ppl_check tally (ORIG) ---       1 W3      (the same beta 1l line, csPageTest's df line)
--- 2b. HARD errors (E2 E3 E6 E8 E10 E11) --- none
--- 3. lint_ppl ---   2328 checks, 13 problems
  beta 2's 8 (STRING() with 4 args at the csEntry MSGBOX, PIXON_P 'dvG', file-name and
  EXPORT-discipline noise), plus 5 false alarms, all in the CAS kit:
    696  cR := STRING(CAS(csS));                   the kit's 1-argument STRING (Standard form)
    707  IF INSTRING(cR, "undef") > 0 OR ...       x2: INSTRING contains the letters "STRING"
    725  IF INSTRING("0123456789", fsC) == 0 THEN    (lint_ppl matches STRING( inside INSTRING()
    745  IF INSTRING("0123456789", MID(...)) > 0       and counts its arguments)
--- 4. full parse (kit interpreter) ---   PARSE FAIL at the file-level LOCAL after the EXPORT
    list, the kit's limit, as beta 2.  With the file-level EXPORT and LOCAL lines masked:
    beta 2 PARSE OK (62 functions), beta 3 PARSE OK (75 functions)
--- 5. ---   3244 lines, 144817 bytes; no non-ASCII in code
ppl_gate_v1.py: ppl_check_v3 1 W3 = original, hard errors none, lint_ppl as above
fleet_names_v2 over the latest version of every program in out/ (27 files, including the
    parallel CAS versions BayesTree beta 8, EpiStats v1.7, ErrorRate beta 1, CASProbe beta 1 ...):
    1233 routine names, 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches
```

## 3 · Verification (`verify_ChiTable_beta3.py`; full output in `verify_ChiTable_beta3_output.txt`)

**5,955 checks, 0 failed.** Desktop Giac 1.9 (`icas`), Python `fractions`, SciPy 1.18 and the run harness `ppl_run_v3.py`.

**A. Giac's trap.**
- `sum(comb(4,csj)*comb(4,4-csj),csj,0,1)+…` → 34, with 4 lines of "Warning: solving in csj equation Gamma(csj+1)^2*Gamma(-csj+5)^2=0".
- `sum(seq(…))` → 34 with none. That is the form the program uses.

**B. The program's own CAS text.** Each template was captured from the harness and answered by Giac. The 18 chosen tables include ties, zero cells, the smallest table, the extremes and large N.

| Table | Fisher p (exact) | SciPy | χ² exact | runs summed |
|---|---|---|---|---|
| tea [[3,1],[1,3]] | **17/35** | 0.485714 | 2 | a 0–1 and 3–4 (the tie) |
| [[4,0],[0,4]] | 1/35 | 0.0285714 | 8 | 0, 4 |
| [[2,2],[2,2]] | 1 | 1 | 0 | 0–4 |
| [[1,0],[0,1]] | 1 | 1 | 2 | 0–1 (a tie) |
| [[5,0],[3,7]] (zero cell) | 1/39 | 0.025641 | 105/16 | 0, 5 |
| [[6,2],[2,6]] | 283/2145 | 0.131935 | 4 | 0–2, 6–8 |
| [[10,0],[0,10]] | 1/92378 | 1.08e-5 | 20 | 0, 10 |
| example 1 | 149-digit fraction (74 / 75) | 0.257782 | 697832977/475195203 | 0–44, 53–68 |
| example 2 | 140-digit fraction (68 / 72) | 0.000117698 | **5549501668/421789635** | 0–38, 64–68 |
| example 2 × 10 | not asked (C(6740, 680): 956 digits) | 2.78e-38 | 11099003336/84357927 | — |

For every table these all agree:
- **Fisher:** the exact-integer rule (10⁷·w ≤ (10⁷ + 1)·w_obs) as a Fraction, Giac's answer, `scipy.stats.fisher_exact`, and csFisher's decimal.
- **The runs:** the a values in the program's template match the exact-integer decision, with at most two runs.
- **χ²:** the shortcut, Σ (O − E)²/E as Fractions, Giac, `chi2_contingency(correction=False)` and csX2.
- **The integers:** ad − bc, r₁r₂c₁c₂, the ways and C(N, c₁) are exact.
- **The digit estimate** `csXDg` is within 1 of `len(str(comb(N, c1)))`.

**r × c tables** (examples 3 and 4, a small one, zero cells, example 3 × 10): Giac's fraction equals the exact Σ. Example 3 gives **3668733438511/122005828000** = 30.0701, from a 231-character template. A transposed table gives the same fraction.

**C. Random tables.** 300 random 2 × 2 tables (counts 0–40, a quarter with a forced zero) and 150 random 2 × 3 / 3 × 2 tables (0–60): every comparison in B holds.

**D. End to end in the harness.**

| Run | cas = 'giac' | cas = 'fail' |
|---|---|---|
| Tea typed in the grid (Values form, Run), pages 6–7, the Fisher plot, Quit | page 6 "p = 17/35 = 0.4857" + exact (CAS). Page 7: "= 8 × (3 × 3 - 1 × 1)²", "= 8 × 8² / 256", "= 2 = 2.000", "34 of the 70 equally likely ways", "p = 34/70 = 17/35 = 0.4857". Plot: "red + magenta: p = 17/35 = 0.4857" + exact (CAS). **6 CAS calls**; the plot used the cache | page 6 "p = 0.4857" + decimal. Page 7: "= 2.000", "(the CAS did not answer: the decimal only)". Plot "red + magenta: p = 0.4857" + decimal. **4 attempts**, no error |
| Answers wrapped in quotes (Giac's answer given an extra pair, as the Commands reference warns) | `csCas` dropped them: "p = 17/35 = 0.4857" | — |
| Example 2, pages back and forth, ×10 N, N / 10 | page 7: "= 5549501668/421789635 = 13.157", "p = 0.0001 (140-digit fraction)". After ×10: "C(6740, 680) has about 956 digits: too big", with no Fisher call sent. 15 calls in all: 6, then 3, then 6. Turning pages added none | every page-7 frame: decimal badge, no error |
| Examples 3 and 4 | page 6/6: "= 3668733438511/122005828000 = 30.070", "first cell: (762 - 1557 × 1246 / 2757)²" | "= 30.070" + decimal |

Desktop Giac took about 30 ms per call, process start included. That says nothing about a G1.

**E. The fence.**
- **Call graph:** only `csXFisher` and `csXChi` call `csCas`, and only `csPage2x2`, `csPageExact` and `csFishPlot` call `csXEnsure`. `csCas` is the one `CAS(` in the code.
- **Nothing in a loop reaches `csCas`:** not `csBarDrag`, `csMorph`, `csCurve`, `csCvDraw`, `csCvFit`, `csBars`, `csMosaic`, `csResBars`, `csFishDraw`, `csPlotLoop`, `csGrid`, `csEntry`, `csScaleN`, `csResMenu`, `csCompute` or `csFisher`.
- **Measured:** page 6 twice gives 1 call. A bar drag (12 → 8) gives 0 calls, and page 6 afterwards gives 1. The morph (10 frames) and a drag of the critical line (α 0.05 → 0.147) give 0.

## 4 · Device test checklist: from least to most risky

Stop at the first failure. Everything above it is known good.

1. **Run CASProbe beta 1 first, on the G2 and the G1.**
   - **Call form:** if it reports a form other than `STRING(CAS(s))` (T04–T10), change the one IFERR line in `csCas` (line 696).
   - **Gate:** if T07 (the kit routine as written) or T11/T13 (a fraction kept as text) fail, expect every beta 3 line to show the **decimal** badge. That is the designed fallback, not a bug.
2. **Paste and compile.** Run ChiTable. The menu has 14 items, Quit is E. Quit at once: Home shows "ChiTable: no table".
3. **Beta 2's checklist, items 2–16** (`ChiTable_beta2_CHANGES.md` §5): the code they test is byte-identical, so they should pass as before.
4. **Results page 6** (Examples → Death penalty × victim's race, page 6/7).
   - **What you should see:** "Fisher's exact test, two-sided:" then, on its own line, "p = 0.0001 (140-digit fraction)" and a blue badge at the right.
   - **Layout:** the RD, RR, OR, CI, phi and two grey lines sit 4–7 px lower than in beta 2, and the last one ("RD, RR and OR describe…") is fully above the soft keys.
5. **Help → page 5** ("Exact answers (CAS)"): 13 lines, none clipped at the right, footer "Any key = menu". Page 4's footer now says "Any key = page 5".
6. **The CAS steps:**
   - (a) **New table 2 × 2, Values {3, 1, 1, 3}, Run, then Right to page 6.**
     - **What you should see:** "p = 17/35 = 0.4857" and **exact (CAS)**.
     - **If it says "p = 0.4857" and decimal:** the CAS did not answer, or not as text. Note what CASProbe said.
   - (b) **Right to page 7/7. What you should see:**
     - "1. χ², the 2 × 2 shortcut:" with exact (CAS);
     - "= 8 × (3 × 3 - 1 × 1)²", "/ (4 × 4 × 4 × 4)", "= 8 × 8² / 256", "= 2 = 2.000";
     - "P(a) = C(4, a) × C(4, 4 - a) / C(8, 4)";
     - "34 of the 70 equally likely ways", "p = 34/70 = 17/35 = 0.4857".
     - On a G1, note how long the page takes to appear (5 CAS calls).
   - (c) **Left, Right, Left, Right.** The page should come back at once each time (the cache).
   - (d) **Esc, main menu → Plot: Fisher exact.** **What you should see:** the title "Tables with these margins" with exact (CAS) beside it, and "red + magenta: p = 17/35 = 0.4857" under the plot.
   - (e) **Examples → victim's race, page 7. What you should see:**
     - "= 674 × 8116² / 3374317080" and "= 5549501668/421789635 = 13.157";
     - "their ways, over all C(674, 68) ways:" and "p = 0.0001 (140-digit fraction)".
     - On a G1, time it.
   - (f) **Menu → ×10 N, Enter, page 7. What you should see:** "C(6740, 680) has about 956 digits: too big" and "p < 0.0001 (the decimal)". The χ² line still fits: "= 11099003336/84357927 = 131.570".
   - (g) **Menu → N / 10.** Page 7 is example 2's again.
   - (h) **Examples → Gender × party ID (2 × 3), page 6/6. What you should see:** "first cell: (762 - 1557 × 1246 / 2757)²" and "= 3668733438511/122005828000 = 30.070".
   - (i) **The fence on the device:** drag a bar on the bars plot. It must feel exactly as in beta 2 (no CAS pause). Then page 6: one short pause at most.
7. **Home after Quit:** CS_X2 etc. as before. The fractions are display only and not exported.

## 5 · Not confirmed / left as it was

- **Everything about the CAS on the calculator:**
  - the call form;
  - whether `STRING(CAS(s))` hands back "17/35" or a decimal (a decimal → the decimal badge);
  - whether the Prime's older Giac knows `seq` inside `sum`;
  - G1 timing (six calls on page 7 for a 2 × 2).
  
  CASProbe tests `comb`, fractions and the guard, but not `sum(seq(...))` with `comb`. Checklist step 6(a) is the first real test of that form.
- **The quotes.** The kit's quote-stripping is tested in the harness by wrapping every answer in an extra pair of quotes. Whether the device ever adds them is CASProbe's to say.
- **CAS settings.** `HSeparator` and the exact/approximate mode are not read or set. Only integers and `/` are sent, never a decimal point (fence rule 1). If Roger's CAS is in approximate mode and the answers come back as decimals, `csIsFr` rejects them and the decimal shows.
- **Thresholds.** 100 digits is the "too big" threshold for asking the CAS for Fisher's p, and 15 characters for S + T on the counting line. Both are judgement calls (decisions for Roger).
- **Text widths** were checked with the harness's estimates for tables up to 6-digit counts. Two beta 2 lines (page 6's p1/p2 and OR lines with 5- to 8-digit numbers) can still be clipped by their width argument, as in beta 2. Not touched.
- **Not done:**
  - an exact Fisher p for 2 × 3 (Freeman–Halton);
  - exact Yates;
  - an exact V or G² (G² needs logs, so it is not a fraction).
