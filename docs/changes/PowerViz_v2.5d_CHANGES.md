# PowerViz v2.5d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on v2.5c; every v2.5c feature is kept, and ordinary displays are unchanged. Run only in the PC harness (ppl_run_v3e); not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 20, "PowerViz P-1 and 'POWER > 0.999' instead of 1.000"; details in `findings_F.md`, section 3):

> **P-1. COSMETIC — the closed-form n is meaningless when α > 0.5 and is still shown.** The Edit form accepts 0 < α < 1. At α = 0.999 one-sided, `pv_NCF` squares a negative `(za·u + zb·w)/|δ|` … and the panel reads `n₈₀ = 2 (45.5)`; the formula page's "Round UP … 46" follows.

In the harness, at α = 0.999 with the default 1-sample mean (d = 0.5), it reads `n₈₀ = 2 (20.2)`, and the formula page says `= 20.23`, then "Round UP (whole people): n = 21", then "1-sided: exact; they differ only by rounding at a whole number". All four tests do it; for example, the 2-sample mean at α = 0.9 gives "Round UP: n = 4" against n₈₀ = 2.

> **Improvement 1 — a top floor in `pv_FMTP`:** power that rounds to 1 prints `POWER 1.000` beside `β < 0.001`; power is never 1 under a normal model.

**And Roger's disclaimer** (19 Oct 2026, through the coordinator): a header line beside the distribution terms, and one line on a help page.

## What changed (line numbers: v2.5c → v2.5d)

1. **P-1, pv_NCF** (650 → 682-688). The formula comes from √n·|δ| = zα·u + zβ·w. When the right side is 0 or below, no √n solves it, and pv_NCF now returns -1, the value that already meant "no formula n".
   - That happens only for a 1-sided α above 0.5: a 2-sided zα is never negative.
   - In that case power is above 0.80 at every n, which the verify's sweep confirms.
   - The panel's n₈₀ line and the Pow-n view's "formula:" label already hide a negative NCF.
2. **P-1, pv_Formula** (2064-2103 → 2114-2172). With NCF < 0 and an effect, the page now shows:
   - the formula with the student's numbers and no value, then `    no root: the bracket is 0 or less, and √n > 0`;
   - `Power is above 0.80 at every n;  trying n: n₈₀ = 2` in place of "Round UP";
   - `1-sided α above 0.5: the test rejects H₀ more` / `often than not even when there is no effect.` in place of the 1-sided/2-sided comparison.

   That comparison block is re-indented inside the new ELSE; its text is unchanged. Every other formula page is v2.5c's, as the verify's U1 checks for 6 ordinary cases, α = 0.5 and α = 0.6 one-sided among them.
3. **The top floor, pv_FMTP** (876-885 → 915-931): `IF xx <= 1 AND ROUND(xx, dd) >= 1 THEN RETURN "> " + STRING(1 - thr, 2, dd)`.
   - A probability that would print as 1 prints `> 0.999` (3 decimals), `> 0.9999` (4) or `> 0.99` (2).
   - Power is never 1 under a normal model, and neither is β. At a large n the computed power IS exactly 1 in the calculator's 12 digits (1 minus a tail below 5E-13), so an exact 1 gets the floor too. This is v2.5c's rule for β's exact 0 (pv_BetaS), mirrored.
   - The brief's wording was "when power rounds to 1 but is not 1". Counting the computed exact 1 as "not 1" is my reading, because otherwise every n large enough to push power past 1 − 5E-13 would still print `POWER 1.000` beside `β < 0.001`, the case the review cites.
4. **The plot's two region labels** (pv_Draw, 1441, 1454 → 1487-1489, 1502-1504) now go through pv_Rel: `power > 0.99` and `β > 0.99`, never `power = > 0.99`.
   - With the new floor these labels can carry a relation in regions large enough to be drawn (power near 1, or β near 1).
   - Ordinary labels (`β = 0.43`, `power = 0.57`) are unchanged.
   - The other pv_FMTP sites either had pv_Rel already or cannot reach 1: the α drag and snap hints are clamped to 0.001-0.5.
5. **The disclaimer.**
   - The header (→ 9-11), after "Provided as is.": "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes."
   - On screen: help page 1 (pv_ShowHelp, → 2217-2219) reads `Teaching aid; not for clinical or legal use.` in red, font 1, at y 208, the free row above the footer.
6. **The header:**
   - the banner;
   - the tested-on lines ("v2.2 to v2.5d have NOT yet been run on a G1 or G2"; "v2.5d has run only in the PC harness");
   - a dated "What changed in v2.5d (19 Oct 2026): P1 and the 'POWER > 0.999' floor (fleet review 19 Oct)" paragraph (→ 33-59), whose line numbers are v2.5c's.

   The header's old "For academic use only … Results have not been rigorously verified" lines stay, as the brief says (D17).

**Before and after** (harness):

| Where | v2.5c | v2.5d |
|---|---|---|
| Panel, 1-sample mean, d 0.5, α 0.999 | `n₈₀ = 2 (20.2)` | `n₈₀ = 2` |
| Formula page, the same | `n = ((15×-3.090 + 15×0.842)/7.5)^2 = 20.23`, `Round UP (whole people): n = 21;  trying n: n₈₀ = 2`, `1-sided: exact; they differ only by rounding …` | `n = ((15×-3.090 + 15×0.842)/7.5)^2`, `no root: the bracket is 0 or less, and √n > 0`, `Power is above 0.80 at every n;  trying n: n₈₀ = 2`, `1-sided α above 0.5: the test rejects H₀ more …` |
| Big POWER, n 100, d 0.5 (power 0.9996) | `1.000` | `> 0.999` |
| Big POWER and exit box, n 5000, d 0.67 | `1.000`; `POWER = 1.0000   (β < 0.0001)` | `> 0.999`; `POWER > 0.9999   (β < 0.0001)` |
| Plot label, α 0.5 (power 0.997) | `power = 1.00` | `power > 0.99` |
| Panel β, typed α 0.0001, d 0.033 (β 0.9998) | `β = 1.000` | `β > 0.999` |
| Pow-n readout, n 200, d 0.67 | `at n = 200: power = 1.000, …` | `at n = 200: power > 0.999, …` |
| Defaults | `POWER 0.572`, `n₈₀ = 56 (55.6)`, the formula page | the same |

## Verification

`verify_PowerViz_v2.5d.py` was built from the v2.5c script, and every check is kept. It runs on v2.5d in harness ppl_run_v3e. Output is in `verify_PowerViz_v2.5d_output.txt`: **174 PASS, 0 FAIL**.

Old checks whose expected value moved (each says so):
- **R5:** the routine list now includes pv_FMTP, pv_Formula, pv_NCF and pv_ShowHelp.
- **T1:** the "new" column is v2.5d's: `POWER = 1.0000` → `POWER > 0.9999` (twice), and β 0.9998 or 0.99999 → `β > 0.999` / `(β > 0.9999)`.
- **T5:** checks the v2.5b → v2.5c diff, so it reads v2.5c's own file. Its version-string, bracket and INSTRING checks read v2.5d.
- B12 still runs v2.4's script against the new file, and passes.

New section **U**:
- **U1 (P-1):**
  - 4 tests × CAS answering and failing: the old NCF, Round-UP line and panel bracket against the new page;
  - the Pow-n view's "formula:" label is gone;
  - 6 ordinary cases are identical to v2.5c, panel and formula page;
  - a sweep of 4 tests × 2 tails × 10 alphas × 4 effects against the replica: wherever the bracket is not positive, pv_NCF is -1, the test is 1-sided with α > 0.5, and power at n = 2 is already above 0.80.
- **U2 (floor):**
  - pv_FMTP at 10 edge values, both versions;
  - the big POWER readout (at most 7 characters at font 5, ending before x 289) and the exit box in 4 scenes;
  - the two plot labels and the Pow-n readout;
  - a sweep of 40 scenes (α 0.001-0.999, n 2-5000): no POWER 1.000 and no "= >" / "= <" anywhere.
- **U3:** the disclaimer is in the header word for word (and the D17 lines are still there); help page 1 shows the line, and every other line of the three pages is v2.5c's.
- **U4:** the review's own `check_PowerViz.py`, run unchanged except for its path, has the same single failure on v2.5c and v2.5d. That failure is the Pow-n subtitle at σ = 1E-6, which runs past 320 px. The review called it "absurd input, left as a FAIL in the log for the record", and it is not on the fix list, so it was not changed. Strictly, it is a review check that fails on the old version and still fails on the new one.
- **U5:**
  - the routine diff (exactly pv_Draw, pv_FMTP, pv_Formula, pv_NCF, pv_ShowHelp);
  - outside them only comments differ;
  - every changed code line is one of the fixes, or comes back unchanged in the re-indented block;
  - no new names.
- **U6:** `h.sci_strings` over all 231 v2.5d runs: **empty**.

## Gate

`python3 ppl_gate_v1b.py PowerViz_v2.5d.txt _old/PowerViz_v2.5c.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 5 E1, 175 E7, 14 E9, as v2.5c. There are no hard errors.
- lint_ppl: 22 problems, as v2.5c. They include the known false "file-level LOCAL declares 7 names" for `ALAD := {…}`.
- Full parse: it stops at the EXPORT list (330; v2.5c 298). This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh`: kit lint 0 errors; no hard errors; the parse fails on the same construct as v2.5c.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.5c (open it in the Kit). Then Program Catalog → Check.
2. **The floor:** One-sample mean, μ₁ = 107.5, n = 100 → the big number reads `> 0.999` in green, whole, inside the panel's right edge. Esc: the exit box reads `POWER = 0.9996   (β = 0.0004)`. Then n = 5000, μ₁ = 110: `> 0.999`, and the exit box `POWER > 0.9999   (β < 0.0001)`.
3. **The plot labels:** α typed 0.5 → the green region's label reads `power > 0.99`.
4. **P-1:** Edit → α = 0.999 (one-sided), μ₁ = 107.5. The panel reads `n₈₀ = 2` with no bracket. Menu → Sample-size formula: the page shows the formula line without "= …", then "no root: the bracket is 0 or less, and √n > 0", "Power is above 0.80 at every n; trying n: n₈₀ = 2", and the two-line reason, with the √ glyph drawn.
5. **Help page 1:** the red `Teaching aid; not for clinical or legal use.` sits above the footer, clear of the line above it.

## Unresolved (open decisions touching PowerViz; not changed here)

- **D17:** the header's old "For academic use only … Results have not been rigorously verified" and "vastly improved by Claude Code Fable 5" lines. Left as they are, beside the new DISCLAIMER line.
- **P-2 (a guess):** whether the effect cell touches the big POWER number at font 2. The new `> 0.999` starts at the same x (222) as `1.000` did, so the left edge is unchanged. Eyeball once.
- **Review improvements** (not in this pass): the upper tail as a lower tail for EP_PWR, the far-tail shading, and "(Cohen's h)" on the Pow-effect view.
