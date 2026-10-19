# PowerViz v2.5b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on v2.5a; every v2.5a feature is kept. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

PowerViz v2.5a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) in round 2 on 17 October 2026. "Where n comes from" showed "exact (CAS)" and `n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2`. The CAS never failed there, so the decimal fallback was not reached.

Round 2 also typed these in Home (BRIEF_R2FIX_v1 §0):

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `INSTRING("abc", "")` | 1 |
| `LEFT("abc", 0)` | `"abc"`, the whole string |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: scientific |

So fixed decimals turn scientific whenever 0 < |x| < 10^-d. INSTRING on an empty string stopped TrendTest's and ScatterLab's CAS pages on the emulator ("Error: Invalid input"), in replace loops like PowerViz's `pv_Rep`.

What that means for v2.5a (harness v3d, which models both facts; `audit_v3d/PowerViz_v2.5a.txt`):

- **A failed CAS call stops the program.** v2.5a's verify script stops at B5, the `cas='fail'` run of the formula page. `pv_Cas` sets `cR := ""`, then tests `INSTRING(cR, "undef")`. Behind it, `pv_Strip("")` would have stopped on `INSTRING(stz, "list")` too.
- **`pv_Rep` stops when a CAS name ends the answer.** After the last replacement the rest of the text is `""`, and the loop asks INSTRING of it. The emulator's answers end in `)^2`, so this did not happen there. It is the same loop shape that crashed TrendTest and ScatterLab.
- **Three displays print `ᴇ`:**
  - with μ₁ = 100.001 and σ = 15 (d = 0.0000667), the power-vs-effect view reads `at d = 6.67ᴇ-5` and the exit summary `d = 6.667ᴇ-5`;
  - a typed σ of 0.0004 reads `4.000ᴇ-4` in the SE line.

## What changed (line numbers: v2.5a → v2.5b)

1. **`pv_Cas`** (2.5a 384–411 → 2.5b 418–449). The reject test runs only on a non-empty answer (2.5b 441–447), as BRIEF_R2FIX §2a gives it, in the file's one-space indent. The IFERR line and the quote strip are byte-identical. So is the INSTRING line itself, moved in by one space.
2. **`pv_Rep`** (2.5a 434–449 → 2.5b 472–492) is the §2a replace loop:
   - an empty pattern hands the text back (`INSTRING(s, "") = 1` would loop for ever);
   - INSTRING is asked only while text is left (2.5b 484, 489);
   - the rest of the text becomes `""` once the pattern ended it (2.5b 488).

   It keeps `MID(rpt, 1, rpi − 1)` under `rpi > 1` rather than LEFT, because `LEFT(s, 0)` is the whole string. The new LOCAL is `rpk`, the pattern length.
3. **`pv_Strip`** (2.5a 451–465 → 2.5b 494–512). `INSTRING(stz, "list")` is asked only of a non-empty `stz` (2.5b 508–510). A failed call (`""`) and an empty solve (`{}`) both leave nothing.
4. **`pv_FMT`** (2.5a 786–789 → 2.5b 837–844) is `STRING(ROUND(xx,dd),2,dd)`. It formats means, effect sizes, zcrit, SE, the formula's n and the axis ticks. After ROUND the value is 0 or at least 10^-d, so the fixed form holds. A tiny effect reads 0.00 / 0.000: honest, and pv_EffWord already says "tiny".
5. **`pv_NumS`** (2.5a 712–724 → 2.5b 761–775) and **`pv_NumD`** (2.5a 595–606 → 2.5b 642–655) round the same way. They print typed values in the SE line and on the formula page.
6. **Header**: version v2.5b, a dated "v2.5b" paragraph that quotes the finding, and the tested-on paragraph (v2.4 passed round 1; v2.5a's formula page passed round 2; v2.5b has not run).

Nothing else changed. The verify script (R5) checks that the routines differing from v2.5a are exactly `pv_Cas`, `pv_FMT`, `pv_NumD`, `pv_NumS`, `pv_Rep` and `pv_Strip`. Outside them only comments differ, and the other 57 routines are byte-identical with their comments.

### The sweep (BRIEF_R2FIX §2a, §2b)

**INSTRING (10 lines in 2.5b).**
- Guarded now: 446 (`pv_Cas`), 484 and 489 (`pv_Rep`), 509 (`pv_Strip`).
- Safe as they were:
  - 504: the first argument is the constant `"[]{} "`.
  - 523–525 (`pv_CasUse`): the routine returns 0 on an empty answer first.
  - 669–670 (`pv_Wrap`): the first argument is one character, `MID(wrt, wri, 1)` with 27 ≤ wri ≤ 54 < DIM(wrt), or a constant.

**LEFT / MID.** None needed a change:

| Line (2.5b) | Call | Why it is safe |
|---|---|---|
| 437–438 | `pv_Cas`'s LEFT / MID | only when DIM ≥ 2 |
| 486, 488 | `pv_Rep`'s MIDs | start 1 under rpi > 1; the rest only while it is inside the text |
| 503 | `MID(sts, sti, 1)` | sti runs from 1 |
| 509 | `MID(stz, 5, …)` | after "list" at position 1 |
| 674–675 | `pv_Wrap`'s MIDs | starts 1 and wrc + 1 ≥ 2 |
| 1970 | `MID(fdn, 2, DIM(fdn) − 2)` | `pv_DName()` is a bracketed name, e.g. `(μ₁−μ₀)` |

No RIGHT.

**STRING(…, 2, …).**
- Changed: 843 (`pv_FMT`), 774 (`pv_NumS`), 654 (`pv_NumD`).
- Unchanged, because they cannot reach 0 < |x| < 10^-d:
  - 857–858: `pv_FMTP`'s "< 0.001" uses thr = 10^-d exactly.
  - 860: `pv_FMTP` prints only 0 or values with |x| ≥ 10^-d.
  - 1499 (`i2/5`) and 1518 (`i2*0.25`): ticks 0, 0.2, 0.5, ….
- Left on purpose: the "you entered …" MSGBOX echoes at 1779, 1783, 1789, 1794, 1799, 1818 and 1844 (see Unresolved). Their "set to" values (0.02, 0.98, whole n) are fixed.

## Verification

`verify_PowerViz_v2.5b.py` was built from the v2.5a script, and every check is kept. It runs on harness **ppl_run_v3d**. Output is in `verify_PowerViz_v2.5b_output.txt`: **106 PASS, 0 FAIL** (v2.5a's script: 62; under v3d it stopped at B5).

- **A, B and G (kept):** every CAS template through desktop Giac against SymPy and statsmodels, and the program end to end for every test and tail. B2 is the formula page with the CAS answering (`cas='giac'`): "exact (CAS)", `n = (3×zα+3×zβ)^2`, and test 3's `n = (5×zα+2×√6×zβ)^2`. B5 is `cas='fail'`. **B12** runs v2.4's own verify script on v2.5b in v3d: 64 PASS, and the one FAIL is the intended help-page count. **G** compares v2.5 with v2.5a.
- **R1:** `pv_Cas` after a failed call returns `""` with no error. v2.5a in v3d stops on the same call.
- **R2, `cas='fail'`:** the formula page for tests 1–4 (1-sided), test 2 (2-sided), the menu route and the no-effect case each opens with "decimal" and the textbook form, with no error. **v2.5a in v3d stops on all seven**: "INSTRING: Invalid input".
- **R3, `pv_Rep` directly:**
  - the pattern at the end (`pvza+pvzb` → `pvza+zβ`), at the start, and as the whole string (`pvd` → `δ`);
  - repeated (`3*σ*σ`), an empty pattern (text back), an empty text, both empty, absent, a trailing `*`, an empty replacement.
  - `pv_Strip` on `""`, `{}`, `list[…]`, a braced solve and `list`.
  - The formula page with canned CAS answers that **end in `pvzb`**: v2.5b shows `n = (zα+zβ)^2×σ^2/(μ₁−μ₀)^2×zβ/zβ` under "exact (CAS)". v2.5a stops in `pv_Rep`.
- **R4, small numbers:**
  - `pv_FMT`: 0.0033 → `0.00`, 2.8E-17 → `0.0`. `pv_NumS(0.0004)` = `0.000`, `pv_NumD(0.00004)` = `0.0000`.
  - With μ₁ = 100.001: `at d = 0.00: power = 0.050` and the summary `d = 0.000`.
  - With σ = 0.0004: `SE₀ = σ/√n = 0.000/√30 = 0.0000730`.
  - v2.5a shows `6.67ᴇ-5`, `6.667ᴇ-5` and `4.000ᴇ-4` at those three places.
- **R5:** the routine diff, as listed above.
- **R6, `h.sci_strings` from every run:**
  - the 34 v2.5b runs and B12's subprocess: **none**;
  - v2.5 and v2.5a, for comparison: `STRING(6.67E-5, 2, 2)`, `STRING(6.67E-5, 2, 3)`, `STRING(0.0004, 2, 3)` and `STRING(0.0033, 2, 2)`.
- The audit's one scientific result for v2.5a, `STRING(0.1, 2, 1)`, came from an earlier build of v3d. The current v3d judges a value at the Prime's 12 digits, and it does not reproduce under v2.5a's own script.

**Extra run (not in the script):** the whole script was also run once with AND and OR evaluating both sides, using a scratch wrapper (the harness, like Python, skips the right side; what the Prime does is unmeasured). All 106 checks pass that way too. `pv_Strip`'s new guard is a nested IF for that reason.

## Gate

`python3 ppl_gate_v1b.py PowerViz_v2.5b.txt PowerViz_v2.5a.txt` (in `gate_r2`) gives **RESULT: PASS**.
- ppl_check_v4: 5 E1, 174 E7, 14 E9, against 5 / 173 / 14. There are no hard errors, E12 included. The extra E7 is the new local `rpk`: E7 flags every local of a `LOCAL pv_Name()` routine (LocalHeadProbe passed).
- lint_ppl: 22 problems, against 19. The 3 new ones are "STRING() with 4 args" on the three ROUND lines; the lint counts the commas inside `ROUND(…)`. The rest are v2.5a's known noise: the INSTRING-as-STRING lines, and ALAD's one-name 7-value list read as 7 names.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh`:
- Kit lint: **0 errors**, and the 103 warnings are identical to v2.5a's.
- Parse: fails at the EXPORT list (line 274), as v2.5a's does (line 240). That is the tool's limit.

## Device checklist (emulator first, then G2 and G1)

1. In the Connectivity Kit, open PowerViz and paste v2.5b over it (do not add a second copy). Program Catalog → Edit → Check: no errors.
2. One mean, defaults, tap the n₈₀ panel. As in round 2, you should see "exact (CAS)", `n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2`, then `n = (3×zα+3×zβ)^2`.
3. **Tiny effect.** Edit: μ₁ = 100.001. Menu → Power vs effect size: the label reads `at d = 0.00: power = 0.050 …`, with no `ᴇ`. Back, then Esc: the summary reads `effect = 0.0010   d = 0.000`.
4. **Tiny σ.** Run again, Edit: σ = 0.0004, μ₁ = 100.0001. The SE line reads `SE₀ = σ/√n = 0.000/√30 = 0.0000730`.
5. In Home, type `STRING(ROUND(-0.004,2),2,2)` and write down whether it reads `"0.00"` or `"-0.00"` (see Unresolved).
6. The decimal fallback can't be forced on the emulator (its CAS doesn't fail). Harness v3d covers it (R2). If the formula page ever shows "decimal" on a calculator, it must show the textbook form with no error box.
7. On the G2 and G1, repeat 2–4, then v2.5a's checklist items 3–4: the timing, and `pvn` empty in the CAS view.

## Unresolved

- **The "you entered …" messages** (2.5b 1779–1844) echo a rejected typed value with `STRING(v, 2, d)`. A typed proportion of 0.0001 therefore shows "you entered 1.000ᴇ-4". I left them: the scientific form is the true value, and rounding would misquote the student ("you entered 0.000"). Roger to decide whether that wording is wanted.
- **Negative values that round to 0.** The harness prints `ROUND(-0.004, 2)` as `-0.00` (Python's signed zero). It would show only for a tiny negative effect, such as μ₁ just below μ₀. What the Prime prints is unmeasured; checklist step 5 settles it.
