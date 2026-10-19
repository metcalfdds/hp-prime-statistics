# GaltonBoard beta 3c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3b; every beta 3b feature is kept. The MicroPython block, the pour, the drops, the drag and the scene are byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed (round 2)

Beta 3b ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) on 17 October 2026, round 2. The round-1 fix held: "GaltonBoard's pegs and balls are solid". Two new findings:
- **The main menu is cut at the right edge of the CHOOSE box** (about 30 characters fit): "Overlays: none / binomial / + normal", "Colour bars by distance from Rp (SD)", "Pascal's triangle: off / counts / C(r,k)", "Send bins to D1, D2 (Statistics 1Var)".
- **The exit summary says "Galton Board: 1 balls".**

The same round found two string behaviours, typed in Home, that the PC harness had not modelled:

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: fixed decimals turn **scientific** whenever 0 < \|x\| < 10^-d |

GaltonBoard's CAS never failed on the emulator, so its fallback was not reached. Harness v3d shows it: `gbCas` sets `cR := ""` when the CAS fails and then tests `INSTRING(cR, "undef")`. `gbPsLim` then tests `INSTRING(gbPsTx, "limit")` on that same "". Either one stops the program (`audit_v3d/GaltonBoard_beta3b.txt`).

## What changed (line numbers: beta 3b → beta 3c)

1. **gbCas** (3b 449–469 → 3c 487–512). After the quote strip, the undef / error / infinity tests run only when `DIM(cR) > 0` (3c 508–510). The `IFERR` line and the quote strip are byte-identical.
2. **gbPsLim** (3b 643 → 3c 688–690). The "limit" test runs only on a non-empty answer. Before, a failed CAS call on the Poisson page stopped the program there too.
   - **The other INSTRINGs are safe:** gbIsFr 517, gbFrDig 536 and gbIVal 609 look for one character, `MID(s, i, 1)` with i from 1 to DIM(s), in the constant "0123456789".
   - **LEFT and MID are safe.** The one LEFT, in gbCas at 461, takes 1 character, and runs only when DIM ≥ 2. Every MID starts at 1 or later. There is no RIGHT.
3. **The menu fits its box** (gbMenu, 3b 2091–2095 → 3c 2142–2146). The comment about it sits above the CHOOSE, never inside the list. The new items are 28 characters or fewer:

   | Beta 3b | Beta 3c |
   |---|---|
   | Overlays: none / binomial / + normal (36) | Overlay: none/binom/+normal (27) |
   | Colour bars by distance from Rp (SD) (36) | Colour bars by SDs from Rp (26) |
   | Pascal's triangle: off / counts / C(r,k) (40) | Pascal: off/counts/C(r,k) (25) |
   | Send bins to D1, D2 (Statistics 1Var) (37) | Bins to D1, D2 (Stats 1Var) (27) |

   - **Every other CHOOSE line is 30 or fewer.** The longest is "Where Poisson comes from (CAS)" (30). It was not among the cut lines on the emulator, and the cut lines measured there were 31 characters.
   - **The references still fit.** The help page's "Menu: Pascal's triangle, SD colours, Drop" still names what the items do. After a send, the MSGBOX still names the app in full ("Statistics 1Var, Symbolic view").
4. **"1 ball"** (GaltonBoard, 3b 2319 → 3c 2370–2373). The exit line says "Galton Board: 1 ball, R = …" for one ball and "balls" otherwise. A new LOCAL `mlBl` holds the word, on the second LOCAL line, which now has 3 names.
5. **Fixed decimals** (gbF, 3b 303–306 → 3c 341–344). gbF prints every decimal on the board, the bar panel and the Poisson page. It now rounds first, `STRING(ROUND(fv, fd), 2, fd)`:
   - a bin's share of 1 in 10,000 balls reads "0.000" (3b: "1.000ᴇ-4");
   - P(0) for R = 12 reads "0.0002", beside its exact 1/4096;
   - a tiny expected count reads "0.0" (3b: "4.9ᴇ-13");
   - a far-tail normal area or Poisson bar reads "0.0000" (3b: "1.5049ᴇ-47").

   **The other decimals cannot reach the case:**
   - p is held to 0.05–0.95 (form, arrows and drag);
   - μ = Rp is at least 0.15 (gbMuS);
   - the Poisson axis counts up from 0 in steps of 0.02 or more;
   - gbKfmt's "1.2k" and "1.0M" are at least 1;
   - every other STRING(…, 2, 0) is a count.
6. **Header.** "beta 3c" in the banner. A "WHAT CHANGED in beta 3c" paragraph with beta 3b's line numbers. The status lines now say what rounds 1 and 2 showed, including the MicroPython drop on the emulator.

Nothing else changed. The verify script checks that the routines that differ from 3b are exactly GaltonBoard, gbCas, gbF, gbMenu and gbPsLim, each by exactly the change listed, and that the MicroPython block is unchanged.

**Not changed:** gbPour's closing message, "poured N balls", would also read "poured 1 balls" after a pour stopped at once. gbPour is one of the routines kept byte-identical to beta 2, and it was not in the brief, so it is listed here instead (see Unresolved).

## Verification

`verify_GaltonBoard_beta3c.py`, built from the 3b script and run in harness **ppl_run_v3d**. Output in `verify_GaltonBoard_beta3c_output.txt`: **4203 checks passed, 0 failed.** The 3b script had 4130.

- **Kept:**
  - A–C: Giac's traps; the exact bin probabilities for R 3–12 against `Fraction` and SciPy; the Poisson limits against SymPy;
  - D: end to end in both CAS modes;
  - E: the fence, and the routines byte-identical to beta 2, the MicroPython block among them;
  - F: layout;
  - P and L: the solid pegs and balls, and the labels clear of the overlays.
- **R1:**
  - gbCas and gbPsLim with the CAS failing return "" with no error, and gbCasOK is 0;
  - with Giac, 35/128 is kept, and 1/0, 0/0 and an infinite limit are refused;
  - **beta 3b's gbCas and gbPsLim both stop in v3d** on the failed call (INSTRING).
- **R2:** `cas='fail'`, welcome → a bar's panel → Menu → "Where Poisson comes from" → a tap, Right → Esc. Beta 3c completes, every frame "decimal"; **beta 3b stops in gbCas.**
- **R3:**
  - 20 CHOOSE lines, all 30 or fewer; the four new ones 25–28;
  - beta 3b had exactly the four the emulator cut;
  - in a run, the new lines are the ones shown, and Overlay (1 → 2), Colour bars (0 → 1), Pascal and Bins still do their jobs.
- **R4:** the exit line reads "1 ball", "0 balls" and "10 balls" (beta 3b: "1 balls").
- **R5:**
  - Five boards, both CAS modes, each with the bar panel on the extreme and middle bins and the Poisson page stepped up to its top k: R 12 / p 0.5 / 10,000 balls, R 12 / p 0.05, R 12 / p 0.95, R 3 / p 0.05 / 20,000 balls, R 8 / p 0.5. **Beta 3c: 0 scientific strings.** Beta 3b printed 2, 7, 4, 118 and 0 in the same runs (listed in the output).
  - On the R 12, p 0.5 board, bin 0 reads "observed: 1 of 10000 = 0.000", "= 1/4096 = 0.0002" and "normal area -0.5 to 0.5 = 0.0007".
  - gbF on 9 edge values.
- **S, h.sci_strings over every beta 3c run in the script:** 76 runs, **0 scientific strings**.
- **G:** the routine diff is as listed.

## Gate

In `gate_r2`, `python3 ppl_gate_v1b.py GaltonBoard_beta3c.txt GaltonBoard_beta3b.txt` gives **RESULT: PASS**.
- **ppl_check_v4:** clean, as for 3b.
- **lint_ppl:** 25 problems (3b: 24). The one new problem is "STRING() with 4 args" on gbF's `STRING(ROUND(fv, fd), 2, fd)`. lint_ppl splits at every comma, so this is the tool's limit. The rest are as in 3b: the #PYTHON block's depth, and the grob-parameter noise.
- **fleet_names_v2:** 0 collisions, 0 untagged.

`check.sh`:
- kit lint: the same single "unbalanced" error as 3b, from the #PYTHON block (expected);
- the full parse stops at the file-level `EXPORT`, as 3b's does.

## Device checklist (emulator first, then G2 and G1)

1. **Paste, then Check:** Program Catalog → GaltonBoard → Edit → Check. "No errors".
2. **The menu:** Enter (or the Menu soft key). Every line shows in full: "Overlay: none/binom/+normal", "Colour bars by SDs from Rp", "Pascal: off/counts/C(r,k)", "Bins to D1, D2 (Stats 1Var)", "Where Poisson comes from (CAS)". Pick each of the first four once and check it still does its job.
3. **"1 ball":** run, press Drop once, then Esc. Home shows "Galton Board: 1 ball, R = 8, p = 0.50; …".
4. **Small values:** Rows R = 12, then Drop 1000 balls ten times (or ×100 several times). Tap bin 0. The panel shows "observed: … = 0.00x" and "= 1/4096 = 0.0002" with "exact (CAS)". **No ᴇ anywhere.** Then Menu → Where Poisson comes from, press Right to the last k, and check the bar values: 0.0000, never ᴇ.
5. The round-2 checks still hold: solid pegs and balls, and labels clear of the magenta line.

## Unresolved

- **gbPour's message.** "poured 1 balls: n = …" is possible when a pour stops at once (a very short hold on the funnel). gbPour is kept byte-identical to beta 2 (the device-tested pour), so this is left for Roger. If he wants it, it is a two-line change of the same kind as item 4.
- The fallback (the "decimal" badge) has never been seen on the emulator, because its CAS never failed. The harness shows that it completes.
