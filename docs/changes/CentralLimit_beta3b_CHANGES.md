# CentralLimit beta 3b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3a; every beta 3a feature is kept. **The app is unchanged**: START, Plot, the exported `CentralLimit` and all nine VIEW entries are byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

**Beta 3a ran on the HP Prime Virtual Calculator 2.4.2** (build 2026-09-09, the calculators' firmware) **as an app for the first time** on 17 October 2026, in round 2. It was installed by pasting into the Connectivity Kit's app editor (Program tab), and the calculator's View key then showed its Views menu. These all worked, with "exact (CAS)":
- the dashboard, n+ and drawing samples;
- the exact-curve page (n = 16: `2330931341/6810804000`);
- the MGF page.

The CAS never failed there, so the decimal fallback was not reached.

Round 2 also typed these in Home (BRIEF_R2FIX_v1 §0):

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `INSTRING("abc", "")` | 1 |
| `LEFT("abc", 0)` | `"abc"`, the whole string |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: scientific |

The emulator also cut a population-menu item: "Geometric (whole numbers, skewed)" read "…skewe" (brief §4 item 3).

What that means for beta 3a (harness v3d models both string facts; `audit_v3d/CentralLimit_beta3a.txt`):

- **A failed CAS call stops the app.** Beta 3a's verify stops in part 3 at `cas='fail'`, because `cltCas` tests `INSTRING(cR, "undef")` on `cR = ""`. Both CAS pages, reached from the View menu or the dashboard's menu, would stop with "Error: Invalid input" instead of showing "no closed form shown" and the decimals.
- **`cltRepl` stops when a CAS name ends the answer.** For example, `cltShow("-9*cltqs")` stops. The emulator's answers end in a constant or `^2`, so it did not happen there. It is the same loop shape that crashed TrendTest and ScatterLab.
- **Four guards depended on AND.** `cltExact` and `cltMgf` guarded four INSTRINGs with `DIM(s) > 0 AND INSTRING(s, …)`. That is safe only if AND skips its right side when the left is false, which has never been measured on the Prime. The harness, like Python, does skip it.
- **Displays that print `ᴇ` in v3d:**
  - A population with μ = 0.0006 (D1 = −1, 1, −2, 2, 0.003) shows `μ = 6.00ᴇ-4` and `(μ = 6.000ᴇ-4)`. A normal population centred on 0 does the same.
  - A bar holding 1 member of 3000 shows `share = 3.3ᴇ-2% of 3000`.
  - A "% in 1 SE" share of 0.5 % shows `5ᴇ-1% in 1 SE`.
  - A tick a hair off zero shows `-5.6ᴇ-17`. That is the PC's binary arithmetic, but it costs nothing to rule out.

## What changed (line numbers: beta 3a → beta 3b)

1. **`cltCas`** (3a 603–630 → 3b 644–675). The reject test runs only on a non-empty answer (3b 668–673), as BRIEF_R2FIX §2a gives it. The IFERR line and the quote strip are byte-identical, and so is the INSTRING line itself (moved in by two spaces).
2. **`cltRepl`** (3a 661–679 → 3b 706–729) is the §2a replace loop:
   - an empty pattern hands the text back (3b 715);
   - INSTRING is asked only while text is left (3b 717, 726).

   The `LEFT(rpT, rpP − 1)` under `rpP > 1` and the "past the end → `""`" branch were already there.
3. **`cltExact`** (3a 1968–2092 → 3b 2021–2151) and **`cltMgf`** (3a 2104–2216 → 3b 2163–2280). Each `DIM(s) > 0 AND INSTRING(s, …)` is now an outer `IF DIM(s) > 0 THEN` around an inner INSTRING test: 3a 2017 → 3b 2072, 2044 → 2101, 2127 → 2187, 2139 → 2201. They are right whether or not AND skips its right side.
4. **`cltF`** (3a 349–355 → 3b 387–396) is `STRING(ROUND(fv, fd), 2, fd)`. After ROUND the value is 0 or at least 10^-d, so the fixed form holds. It formats μ, σ, the means' mean and SD, σ/√n, the law table and the exact page's decimals.
5. **`cltTipDraw`** (3a 1140–1197 → 3b 1190–1249): the bar box's edges and its share go through `cltF` (3b 1229, 1232, 1237). A share of 1 in 3000 now reads `0.0% of 3000`, with `count = 1` on the line above it.
6. **`cltDash`** (3a 1199–1483 → 3b 1251–1536): the shared x-axis tick labels (3b 1491) and the "% in 1 SE / 2 SE" shares (3b 1518–1519) go through `cltF`.
7. **`cltChoosePop`** (3a 1634 → 3b 1687): "Geometric (whole numbers, skewed)" is now **"Geometric (counts, skewed)"** (26 characters). Every population item is ≤ 26 characters now. `cltName(4)` is still "Geometric".
8. **Header**:
   - version beta 3b and a dated "beta 3b" paragraph that quotes the finding;
   - the tested-on paragraph (beta 3a ran on the emulator as an app in round 2; beta 3b has not run);
   - one line under the install steps: on the Virtual Calculator, pasting into the Kit's app editor (Program tab) worked too.

Nothing else changed. The verify script (R5) checks that the routines differing from beta 3a are exactly the eight above. Outside them only comments differ, the other 61 routines are byte-identical with their comments, and the app (START, Plot, `CentralLimit`, nine VIEW entries) is byte-identical.

### The sweep (BRIEF_R2FIX §2a, §2b)

**INSTRING (10 lines in 3b).**
- Guarded now: 672 (`cltCas`), 717 and 726 (`cltRepl`), 2073, 2102, 2188 and 2202 (inside their DIM IFs).
- Safe as they were:
  - 689 (`cltIVal`) and 2016 (`cltDigits`): the first argument is the constant `"0123456789"`, and the second is one character MID'd inside the text.
  - 2080: runs only after the answer passed its value check, so it is non-empty.

**LEFT / MID.** None needed a change:

| Line (3b) | Call | Why it is safe |
|---|---|---|
| 663–664 | `cltCas`'s LEFT / MID | only when DIM ≥ 2 |
| 688 | `MID(ivS, ivI, 1)` | while ivI ≤ DIM |
| 719, 724 | `cltRepl`'s LEFT / MID | LEFT only when rpP > 1; MID only when the start is inside the text |
| 755 | `MID(wrR, wrI, 1)` | wrI ≥ wrW − 15 ≥ 1 |
| 760–761 | `cltWrap`'s LEFT / MID | wrB ≥ 1; start ≥ 2 |
| 2016 | `MID(dgS, dgI, 1)` | dgI runs from 1 |

No RIGHT.

**STRING(…, 2, …).**
- Changed: 395 (`cltF`); 1229, 1232 and 1237 (bar box); 1491 and 1518–1519 (dashboard), now through `cltF`.
- Unchanged, because they cannot reach 0 < |x| < 10^-d:
  - Whole numbers with 0 decimals at 1236, 1237 (`tdTot`), 1292, 1327, 1337, 1423, 1428–1433, 1500, 1510, 1514, 1888, 1918, 2228 and 2234.
  - 1224–1226: geometric bins, where `tdLo + 0.5` is a whole number.
  - 1878: the law page's y ticks. They start at 0 and step by a 1-2-5 step whose decimals they use, so the first tick is at least 10^-d.

## Verification

`verify_CentralLimit_beta3b.py` was built from the beta 3a script, and every check is kept. It runs on harness **ppl_run_v3d**. Output is in `verify_CentralLimit_beta3b_output.txt`: **RESULT: ALL PASS, 124 checks** (beta 3a's script: 77; under v3d it stopped in part 3).

- **Parts 1–4 (kept):**
  - the 12-digit Irwin–Hall sum;
  - every CAS template through desktop Giac against SymPy;
  - the program end to end for n = 1 … 100, with `cas='giac'` (both pages "exact (CAS)") and `cas='fail'` ("decimal", "no closed form shown", the M(1) line, now with no error);
  - beta 3 against beta 3a.
- **Part 5, R1:** `cltCas` after a failed call returns `""` with no error. Beta 3a in v3d stops on the same call.
- **Part 5, R2, `cas='fail'`:**
  - View "Exact curve (uniform)" and View "Why the bell? (MGF)" at n = 1, 9, 16 and 100 open with "decimal" and no error.
  - So does View "CLT dashboard" → Enter → Exact curve → Esc → Enter → Why the bell? → Esc → Esc, with the script used up.
  - **Beta 3a in v3d stops on every one of these.**
  - In a harness whose **AND / OR evaluate both sides**, beta 3b's pages still open. Beta 3a with only the `cltCas` fix applied would stop there, at `DIM(exT) > 0 AND INSTRING(exT, …)`. That is why item 3 was needed.
- **Part 5, R3, `cltRepl` directly:**
  - the pattern at the end (`ab*`), at the start (`*ab`) and as the whole string (`cltqs` → `s`);
  - repeated, an empty pattern, an empty text, both empty, absent, an empty replacement;
  - `cltShow` of `-9*cltqs` = `-9×s`, of `cltqs` = `s`, and of the MGF series and limit. Beta 3a stops on `-9*cltqs`.
- **Part 5, R4, small numbers:**
  - `cltF`: 0.0031 → `0.00`, 2.8E-17 → `0.0`.
  - The D1 population: `μ = 0.00  σ = 1.41`, then `(μ = 0.001)`.
  - The one-member bar of 3000: `share = 0.0% of 3000`.
  - 1 mean of 200 within 1 SE: `1% in 1 SE,`.
  - Beta 3a shows `6.00ᴇ-4`, `6.000ᴇ-4`, `3.3ᴇ-2%` and `5ᴇ-1%` at those places.
- **Part 5, R5:** the routine diff and the app's byte-identity, as above.
- **Part 5, R6, `h.sci_strings` from every run:**
  - all 24 runs of beta 3b: **none**;
  - beta 3 / 3a, for comparison: 6, as listed under Why.
- **Part 5, R7:** the population menu reads "Geometric (counts, skewed)"; the longest item is 26 characters.

**Extra run (not in the script):** the whole script was also run once with AND and OR evaluating both sides, using a scratch wrapper. Every beta 3b check passed. The only failure is R2's comparison check, by design, since its "AND skips" half cannot hold in that mode. ErrorRate beta 1b's and PowerViz v2.5b's scripts pass in full that way too.

## Gate

`python3 ppl_gate_v1b.py CentralLimit_beta3b.txt CentralLimit_beta3a.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: 9 E1, 23 E7, the same as beta 3a (the app's Statistics-app names). There are no hard errors, E12 included.
- lint_ppl: 19 problems, against 18. The new one is "line 395: STRING() with 4 args": the lint counts the commas inside `ROUND(…)`. The rest are beta 3a's INSTRING-as-STRING noise.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh`:
- Kit lint: **0 errors**, and the 159 warnings are identical to beta 3a's.
- Parse: stops at `H1 := {…, #003CC8:24h}` (3b line 1815), the same line as beta 3a's 1762. That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. **Install as in round 2.** In the Connectivity Kit's app editor, open CentralLimit's Program tab and replace its text with beta 3b. On the calculator: Program Catalog → CentralLimit's program → Check, with no errors. Start the app; the View key shows the nine Views.
2. **View → Choose population**: the fourth item reads "Geometric (counts, skewed)" in full.
3. **Round 2 again:**
   - the dashboard, n+ and drawing samples;
   - View → Exact curve (uniform) at n = 16: `exact: 2330931341/6810804000 = 0.342240261` and "exact (CAS)";
   - View → Why the bell?: `e^(t^2/2)` and "exact (CAS)".
4. **A μ of about 0.**
   - Num view: D1 = −1, 1, −2, 2, 0.003.
   - View → Choose population → "My own data, already in D1": the top line reads `μ = 0.00  σ = 1.41`, with no `ᴇ`.
   - n+ to draw samples: `mean of the x̄'s = … (μ = 0.001)`.
5. **A one-member bar.** Choose population → Exponential, mean 5, N 3000. Hold the rightmost bar in the top panel for 0.6 s: `count = 1`, `share = 0.0% of 3000`, with no `ᴇ`.
6. **Two Home checks** (they settle open questions for the whole fleet):
   - `0 AND INSTRING("","a")`: "Error: Invalid input" means AND evaluates both sides, and `0` means it skips the right side. Write down which; beta 3b works either way.
   - `STRING(ROUND(-0.004,2),2,2)`: `"0.00"` or `"-0.00"`.
7. The decimal fallback can't be forced on the emulator (its CAS doesn't fail). Harness v3d covers it (R2).
8. On the G2 and G1, repeat 2–5, then beta 3a's checklist items 3–4: the "Asking the CAS" timing at n = 4 and 9, and `cltqs`, `cltqt`, `cltqn`, `cltqu` empty in the CAS view.

## Unresolved

- **Whether the Prime's AND and OR skip their right side** is not measured (checklist step 6). Beta 3b no longer depends on it. Other fleet programs may still guard INSTRING with `DIM(s) > 0 AND INSTRING(s, …)`, and they are safe only if AND skips. This is worth a sweep once the answer is known.
- **Negative values that round to 0.** In the harness, a tick a hair below zero now reads `-0.0` (Python's signed zero after ROUND); beta 3a read `-5.6ᴇ-17` there. On the Prime the ticks are exact decimal multiples, so 0 should print `0.0`. Checklist step 6's second line settles what the Prime prints for a negative value that rounds to 0.
- The header's install steps still describe the calculator route. The Kit route that worked on the emulator is noted under them, not substituted. Roger to decide which to lead with.
