# ErrorRate Lab beta 1b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 1a; every beta 1a feature is kept, and the MicroPython block is byte-identical. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

Beta 1a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) on 17 October 2026, in round 1. Its "Why 3" page showed a real CAS limit, `ln(20)` = 2.9957, under "exact (CAS)". The page never needed its decimal fallback, because the emulator's CAS never failed.

Round 2 typed these in Home on the same emulator (BRIEF_R2FIX_v1 §0):

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `INSTRING("abc", "")` | 1 |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: scientific |
| `STRING(0.001, 2, 3)`, `STRING(0, 2, 3)` | `"0.001"`, `"0.000"` |

So fixed decimals turn scientific whenever 0 < |x| < 10^-d, and INSTRING on an empty string stops the program.

What that means for beta 1a:
- **A failed CAS call would stop the program.** `erlCas` sets `cR := ""` when the call fails, then tests `INSTRING(cR, "undef")`. That is "Invalid input". Harness v3d shows this: beta 1a's verify script stops in part C at `erlCas` with `cas='fail'` (`audit_v3d/ErrorRate_beta1a.txt`). With a failing CAS, the Why 3 page (k = 0 and k > 0), the Bayes page, the trawl's Exact page and the Engines page all stop the program instead of falling back to decimals.
- **Two displays print `ᴇ`.**
  - At N = 1 and RMP 1 in a billion, the trawl's "expected chance matches N × RMP" reads `1.000ᴇ-9`.
  - A small true rate reads `2.0ᴇ-2 %`. This happens with a typed rate of 0.02 %, or a Bayes-page drag whose step (0.05 % at n = 50) is finer than the main window's one decimal.

## What changed (line numbers: beta 1a → beta 1b)

1. **`erlCas`** (1a 493–514 → 1b 536–561). The reject test now runs only on a non-empty answer, as BRIEF_R2FIX §2a gives it (1b 555–559):
   ```
   IF DIM(cR) > 0 THEN
     IF INSTRING(cR, "undef") > 0 OR INSTRING(cR, "rror") > 0 OR INSTRING(cR, CHAR(8734)) > 0 THEN cR := ""; END;
   END;
   ```
   The IFERR line and the quote strip are byte-identical, and so is the INSTRING line itself (it only moved in by two spaces).
2. **`erlRepl`** (1a 406–428 → 1b 444–471). An empty pattern now hands the text back as it is (1b 451–453). The loop would never end on one, because `INSTRING(s, "") = 1`. Its two INSTRING calls (1b 458, 468) already ran only while text was left (`IF DIM(rpT) > 0 THEN`), so they are unchanged. Every caller passes a fixed pattern (`erlq`, `erll`, `exp(`, `*`), so the new line is insurance, not a bug fix.
3. **`erlFix`** (1a 263–268 → 1b 292–300) is now `STRING(ROUND(fxV, fxD), 2, fxD)`.
   - It feeds the trawl panel's N × RMP and the Exact page's μ. These are as small as 1E-9 (N = 1, RMP 10^-9) and now read `0.000`. That is an honest display of an expected count to three decimals.
   - Its other callers (the bound to 5 decimals, n × bound, −ln α, the rule constants) never go below 10^-d for the allowed inputs (α 0.001–0.5, n ≤ 10,000; the smallest bound is 6.9E-5 at 5 decimals). For them ROUND changes nothing.
4. **`erlRateS`** (1a 341–346 → 1b 373–384) rounds before it prints.
   - A rate that is **not 0 but rounds to 0** at the window's decimals goes through `erlPctS`, giving `0.0200 %`. "An examiner whose true rate is 0.0 %" and "P(true rate > 0.0 %)" would both be untrue, so ROUND alone was not enough here.
   - The new LOCAL `rsR` passed the gate's built-in check.
5. **Header**: version beta 1b, a dated "beta 1b" paragraph that quotes the finding, the tested-on paragraph (beta 1a passed round 1 with ln(20); beta 1b has not run), harness v3d, and the companion-file list.

Nothing else changed. The verify script (R5) checks that the routines differing from beta 1a are exactly `erlCas`, `erlFix`, `erlRateS` and `erlRepl`. Outside them only comments differ, the other 83 routines are byte-identical with their comments, and the #PYTHON block is byte-identical.

### The sweep (BRIEF_R2FIX §2a, §2b)

**INSTRING (3 lines).**
- 1b 458 and 468 (`erlRepl`) were already guarded by `DIM(rpT) > 0`.
- 1b 558 (`erlCas`) is now guarded (item 1).

**LEFT / MID (no RIGHT).** None needed a change:

| Line (1b) | Call | Why it is safe |
|---|---|---|
| 330 | `MID(cmS, cmI, 1)` | cmI runs from 1 |
| 460 | `LEFT(rpT, rpP − 1)` | only when rpP > 1 |
| 465 | `MID(rpT, rpP + rpLn)` | the start is at least 2 |
| 489–493 | `LEFT(shT, 6/7)`, `MID(shT, 7/8)` | constants, and only when DIM > 7 |
| 507 | `MID(bkS, bkI, 1)` | bkI runs from 2 |
| 549–550 | `LEFT(cR, 1)`, `MID(cR, DIM, 1)`, `MID(cR, 2, DIM − 2)` | only when DIM ≥ 2. A count of 0 gives `""`, which the emulator confirmed |
| 819 | `LEFT(".001", yaI)` | yaI is 1–3 |
| 1179–1180 | `LEFT(awT, awB)`, `MID(awT, awB + 1)` | erlBreak returns at least 2 or the width. Every prefix is ≤ 25 characters, so the width is ≥ 19 |

**STRING(…, 2, …) (11 sites).**
- Changed: 299 (`erlFix`) and 383 (`erlRateS`), as above.
- Unchanged, because they cannot reach 0 < |x| < 10^-d:
  - 364 and 370 (`erlPctS`): anything under 0.0001 % already returns "< 0.0001 %", and 4 decimals start at 0.1 %.
  - 389–390 (`erlAlFmt`): α ≥ 0.01 with 2 decimals, α ≥ 0.001 with 3.
  - 396–397 (`erlLvS`): at least 50.
  - 845 (main ticks) and 1475 (Bayes ticks): each tick is a whole multiple of a 1-2-5 step, and the decimals come from that step, so the first tick is at least 10^-d.
  - 1966 (`twI/4`): 0, 0.25, … 1.

## Verification

`verify_ErrorRate_beta1b.py` was built from the beta 1a script, and every check is kept. It runs on harness **ppl_run_v3d**. Output is in `verify_ErrorRate_beta1b_output.txt`: **211 PASS, 0 FAIL** (beta 1a's script: 170; under v3d it stopped in part C).

- **A–E and G (kept):** the statistics against SciPy and statsmodels, the quoted numbers, every CAS template through desktop Giac against SymPy, the #PYTHON block under CPython, the four end-to-end sessions (E2 is `cas='fail'`), and beta 1 against beta 1a.
- **R1:** `erlCas` after a failed call returns `""` with no error. Beta 1a in v3d stops on the same call: "INSTRING: Invalid input". An empty CAS string also gives `""`.
- **R2, `cas='fail'` page by page:**
  - Why 3 (k = 0), "The equation for k > 0" (k = 2), Bayes and the trawl Exact page each open with "decimal". The Engines page opens with "no answer (the CAS call failed)". None raises an error.
  - **Beta 1a in v3d stops on every one of the five**, and the whole E session stops after 21 main frames. Beta 1b runs that session to Quit.
- **R3, `erlRepl` directly:**
  - the pattern at the end (`ab*`), at the start (`*ab`) and as the whole string (`*`, `erlq`);
  - an empty pattern (`abc` back), an empty text (`""`), both empty, absent (`abc`), repeated (`2*p*p`) and an empty replacement;
  - `erlShow("erlq*erlq")` = `p×p`.
- **R4, small numbers:**
  - `erlFix`: 1E-9 → `0.000`, 0.0996 → `0.100`.
  - The trawl at N = 1, RMP 1 in a billion: `N × RMP = 0.000`, `μ = 0.000`. Beta 1a: `1.000ᴇ-9`.
  - `erlRateS(0.0002)` = `0.0200 %`. Beta 1a: `2.0ᴇ-2 %`.
  - A 0-of-50 session with a typed rate of 0.02 %, the Bayes page, and a drag to its first step (0.05 %) shows no scientific text. Beta 1a shows `2.0ᴇ-2 %` and `5.0ᴇ-2 %`.
- **R5:** the routine diff, as listed above.
- **R6, `h.sci_strings` from every harness run:**
  - all 31 runs of beta 1b: **none**;
  - beta 1 and 1a, for comparison: `STRING(1E-9, 2, 3)`, `STRING(0.02, 2, 1)` and `STRING(0.05, 2, 1)`.

**Extra run (not in the script):** the whole script was also run once with AND and OR evaluating both sides, using a scratch wrapper (the harness, like Python, skips the right side; what the Prime does is unmeasured). All 211 checks pass that way too, so no fix here depends on AND skipping its right side.

## Gate

`python3 ppl_gate_v1b.py ErrorRate_beta1b.txt ErrorRate_beta1a.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: clean (the original: clean). There are no hard errors, E12 included.
- lint_ppl: 17 problems, against 16 for beta 1a. The new one is "line 299: STRING() with 4 args". The lint counts the commas inside `STRING(ROUND(fxV, fxD), 2, fxD)`, the same misreading as its INSTRING-as-STRING lines. The rest are beta 1a's known noise, including the #PYTHON block's depth −1.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh`:
- Kit lint: 1 error, the #PYTHON block's "unbalanced", the same as beta 1a (expected for a Python-block file). The 43 warnings are identical to beta 1a's.
- Parse: fails at the EXPORT list (line 202), as beta 1a's does (line 173). That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. Paste through the Connectivity Kit, replacing beta 1a (open it, do not add a second copy). Then Program Catalog → Edit → Check: no errors.
2. Why 3 with 0 of 30 at α = 0.05: still `p = 1-(1/20)^(1/30)`, `ln(20)` and "exact (CAS)", as in round 1.
3. **Trawl, smallest numbers.** More → Trawl → RMP "1 in 1 billion" → N, type 1. The panel's last line should read `expected chance matches N × RMP = 0.000`, with no `ᴇ`. Then Exact: the red line ends `μ = 0.000.`
4. **Small rates.**
   - Menu → "Set n, k and α": 50, 0, 0.05. Menu → "Set the true rate": 0.0002. The panel should read "An examiner whose true rate is 0.0200 % has …".
   - Bayes: "P(true rate > 0.0200 %) = …".
   - Drag slowly from the very left edge of the Bayes plot: the rate reads `0.0 %` (exactly 0), then `0.1 %`, `0.2 %` …, **never** `ᴇ`.
5. The decimal fallback can't be forced on the emulator (its CAS doesn't fail). Harness v3d covers it (R2). If a CAS page ever shows "decimal" on a calculator, it must also show the formula, with no error box.
6. On the G2 and G1, repeat 2–4, then beta 1a's checklist items 3–5: the k = 2 page, the timings, and `erlq` / `erll` empty in the CAS view.

## Unresolved

- **The Bayes page's step can be finer than the decimals its rate is printed with.** The Bayes window can be half the main window, so with 0 of 50 its finger snaps to 0.05 % while the rate is shown to one decimal. Two neighbouring steps can then read alike: 0.05 % and 0.10 % both read "0.1 %". This is not new (beta 1a did the same above 0.1 %), and beta 1b only stops it printing `ᴇ` or a false "0.0 %". Giving the Bayes page its own decimals would be a small display change. Roger to decide.
- `errorrate-guide_beta1.md` still says "run CASProbe beta 1 first" (noted in beta 1a's CHANGES, not part of this task).
