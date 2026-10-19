# DNAMixLR beta 3b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3a; every beta 3a feature is kept, and dmProb, dmKnowns, dmTyped and dmEval are still byte-for-byte beta 2's. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed (round 2)

Beta 3a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) on 17 October 2026, round 2:

> Main menu: "Results table (tap a row to drop it)" is still cut ("…to dro").

The same round found two string behaviours, typed in Home, that the PC harness had not modelled:

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: fixed decimals turn **scientific** whenever 0 < \|x\| < 10^-d |

On the emulator, **TrendTest beta 3b stopped with "Error: Invalid input"** in its replace loop. The pattern was the last character of the text, so what was left became "", and the next `INSTRING` raised. DNAMixLR's `dmRepl` is the same loop. Its `dmCas` fallback has the kit's fault: `cR := ""`, then `INSTRING(cR, "undef")`. `dmFxMake` then searches that "" for a decimal point. Harness v3d stops beta 3a on each of these.

## What changed (line numbers: beta 3a → beta 3b)

1. **dmCas** (3a 509–529 → 3b 557–582). After the quote strip, the undef / error / infinity tests run only when `DIM(cR) > 0`. The `IFERR` line and the quote strip are byte-identical.
2. **dmRepl** (3a 535–547 → 3b 594–607) is now the round-2 brief's loop:
   - an empty pattern returns the text unchanged;
   - `INSTRING` is asked only while text is left.

   A formula that ends in a symbol, such as `1/2/dmq4/dmq3` for the θ = 0 line, now reads "theta = 0: LR = 1/2/p15/p14". Beta 3a stopped there.
3. **dmFxMake** (3a 2219 and 2231 → 3b 2287–2289 and 2301–2303). The decimal-point test runs only on a non-empty answer.
4. **dmDrawFx** (3a 2322 → 3b 2396–2400). The "signs pair off" note asked `INSTRING(dmFxT, …)` as the third term of an `AND`. Whether the Prime skips the rest of an `AND` once one side is false is not known (nothing in the fleet has measured it). The INSTRING is now inside its own `IF`, behind `DIM(dmFxT) > 0`.

   **The other string calls are safe:**
   - The six LEFTs take:
     - 1 character (dmCas 521; dmPicture 2185);
     - 26 (1409) and 22 (2026);
     - `rpI - 1` behind `rpI > 1` (dmRepl);
     - a break point of at least 1 (dmWrap 585).
   - Every MID starts at 2 or later, or at 1 inside a loop from 1.
5. **The menu fits its box** (DNAMixLR, 3a 3002 → 3b 3082). "Results table (tap a row to drop it)" (36 characters) is now **"Results (tap a row to drop)"** (27). The comment sits above the CHOOSE, not inside the list.
6. **Fixed decimals.**
   - **dmF** (3a 361–364 → 3b 404–407) prints every log10 LR, the percentages, the frequencies on the locus page and the thetas on the plots. It now returns `STRING(ROUND(fv, fd) + 0, 2, fd)`; "+ 0" turns a rounded −0 into 0. An LR of 1.0003 has log10 0.00013, which printed "1.288ᴇ-4" (3 decimals) and "1.29ᴇ-4" (the bar label); it now reads 0.000.
   - **The y labels of the two LR plots** (dmDrawLoci 3a 1495 → 3b 1557, dmThStatic 1789 → 1852) are summed up from a negative bottom, so the tick at 0 can land a hair off it. Beta 3a drew **"-2.8ᴇ-17"** on the LR-by-locus axis for two loci with log10 LR of −0.26 and 0.0001. Both labels now go through dmF and read "0.0".
   - **dmThS** (3a 431–437 → 3b 478–485). A typed θ below 0.0001 (any θ from 0 to 0.5 is accepted) gets two significant digits: 0.00004 reads "0.000040", where beta 3a printed "4.0000ᴇ-5". Its 3- and 4-decimal forms round first.
   - **An allele box** (dmPicture, 3a 2184 → 3b 2248–2250). A frequency below 0.0005 would read ".000", as if the allele could not occur. It now reads ".0004" (beta 3a: "4.000ᴇ-4").
   - **Left as they were:**
     - **dmBig and dmPStr** already write small numbers in their own "mantissa E exponent" form, built by hand.
     - **The theta axis** runs 0.00 to 0.05.
     - **The counts** are whole numbers.
     - **The frequency lines on the locus page** ("plain p = 0.000 becomes …") show 3 decimals through dmF, so a frequency under 0.0005 reads 0.000 there. That is honest at 3 decimals; see Unresolved.
7. **Header.** "beta 3b" in the banner. The firmware lines now say what rounds 1 and 2 showed. A "What changed in beta 3b" paragraph uses beta 3a's line numbers.

Nothing else changed. The verify script checks that the routines that differ from 3a are exactly DNAMixLR, dmCas, dmDrawFx, dmDrawLoci, dmF, dmFxMake, dmPicture, dmRepl, dmThS and dmThStatic, each by exactly the change listed.

## Verification

`verify_DNAMixLR_beta3b.py`, built from the 3a script and run in harness **ppl_run_v3d**. Output in `verify_DNAMixLR_beta3b_output.txt`: **115 PASS, 0 failure(s).** The 3a script had 39.

- **Kept:**
  - Part A: every CAS template in desktop Giac equals the Python engine;
  - Part B: the PPL's CAS text equals the Python builder's; the formula equals dmEval; dmEdge equals brentq; the formula view with Giac and with a failing CAS; the cache; no CAS call in the θ drag; the stale-key run; the protected core byte-for-byte;
  - Part G: beta 3 in v3d still echoes its own text.
- **R1:**
  - dmCas with the CAS failing returns "" with no error;
  - with Giac, undef and infinity are refused;
  - **beta 3a's dmCas stops** on the same failed call.
- **R2, dmRepl directly.** 11 cases against Python's `str.replace`: the pattern at the end, at the start, the whole text, an empty pattern (text unchanged), an empty text, and repeats.
  - **Beta 3a stops** on the pattern at the end.
  - The formula view with Giac, and with a canned θ = 0 answer ending in a symbol, opens with "exact (CAS)" and "theta = 0: LR = 1/2/p15/p14". **Beta 3a stops** in dmRepl.
- **R3, `cas='fail'` end to end** (menu → worked example → a bar → locus page → formula view → Quit): completes with "decimal" and "The CAS did not answer: no formula here." **Beta 3a stops.**
- **R4:**
  - the menu shows "Results (tap a row to drop)", and item 4 opens the table;
  - every fixed menu line is 30 characters or fewer (the hypotheses line: see Unresolved).
- **R5, fixed decimals.** Three setups, each in both CAS modes, through every view (Results, both plots, ladder, fallacy, help) and every locus page with its formula view:
  - two loci (LR 1.0003 and 0.549);
  - those two plus a locus with an allele at p = 0.0004;
  - the three loci with a typed θ = 0.00004.

  **Beta 3b: 0 scientific strings.** Beta 3a printed 10, 11 and 29 in the same runs: "-2.8ᴇ-17", "1.29ᴇ-4", "1.288ᴇ-4", "4.000ᴇ-4" and "4.0000ᴇ-5". Beta 3b reads axis "-0.3, -0.2, -0.1, 0.0", "log10 LR = 0.000", ".0004" and "theta = 0.000040".
- **R6, edge values:** dmF (7) and dmThS (8).
- **S, h.sci_strings over every beta 3b run in the script:** 48 runs, **0 scientific strings**.
- **G:** the routine diff is as listed. dmRepl is the brief's loop, character for character.

## Gate

In `gate_r2`, `python3 ppl_gate_v1b.py DNAMixLR_beta3b.txt DNAMixLR_beta3a.txt` gives **RESULT: PASS**.
- **ppl_check_v4:** clean, as for 3a.
- **lint_ppl:** 18 problems (3a: 15). The 3 new ones are "STRING() with 4 args" on the ROUND forms in dmF and dmThS. lint_ppl splits at every comma, so this is the tool's limit.
- **fleet_names_v2:** 0 collisions, 0 untagged.

`check.sh`:
- kit lint: 0 errors;
- the full parse stops on the same statement as 3a's (`dmClearLoci();`, a forward declaration: the tool's limit).

## Device checklist (emulator first, then G2 and G1)

1. **Paste, then Check:** Program Catalog → DNAMixLR → Edit → Check. "No errors".
2. **The menu:** the fourth line reads "Results (tap a row to drop)" in full. Pick it: the table opens.
3. **The formula view, as in 3a:** Load the worked example → Plot: LR by locus → tap bar 1 twice → `-`. It shows `LR = (3×th+1)×(4×th+1)/(2×(th×p15-th-p15)×(p14×th-p14-th))`, `theta = 0: LR = 1/(2×p15×p14)` (or the calculator's order), and "exact (CAS)". Right and Left through the loci. Nothing stops.
4. **Small values:** Coancestry theta → 0.00004. The menu line reads "Coancestry theta = 0.000040", and so does every page's theta. Then theta back to 0.01. **No ᴇ anywhere.**
5. **An LR near 1, if time allows:** hypotheses preset 4 (V + S + 1 unknown vs V + 2 unknowns). Enter a locus with 4 alleles (p 0.05, 0.3, 0.05, 0.05), victim 1/1, suspect 2/2. Its bar label and locus page read 0.00 / "log10 LR = 0.000" (LR 1.000), never "1.29ᴇ-4".

## Unresolved

- **The hypotheses line of the main menu** is built from the hypotheses. At start and with the worked example it reads "Hypotheses:  V + S, no unknown  vs  V + 1 unknown", 49 characters. The cut lines on the emulator were all cut after about 31, so this line is probably cut too ("…no unknown "), hiding Hd. Rounds 1 and 2 did not report it, so it is not changed here. A shorter form needs Roger's choice of wording, for example "Hp V+S / Hd V+1 unknown" (23), or a two-word item "Hypotheses (Hp vs Hd)" that leaves the detail to the Results page header, which already shows "Hp: … Hd: …".
- **Frequencies under 0.0005 on the locus page lines** read "p = 0.000" at 3 decimals. The allele boxes now say ".0004". Such frequencies are below the usual minimum allele frequency (5/2N) for all but the largest databases.
- **Whether the Prime's AND skips its right side** once the left is false is not measured. Item 4 makes DNAMixLR independent of it. A one-line probe (`IF 0 AND INSTRING("", "a") > 0 THEN … END;`) would settle it for the fleet.
- The CAS fallback has never been seen on the emulator, because its CAS never failed. The harness shows that it completes.
