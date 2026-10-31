# TestChooser beta 2c: changes

*31 October 2026. Built from beta 2b by `make_tc2c.py` (6 exact replacements, each required to match once). 1,852 lines. Harness only.*

## Why

TTestLab beta 1 now works the lecture's five steps for the pooled-variances, separate-variances and dependent-samples t. Asked whether TestChooser's t-test pages should point to it, Roger said: "good idea to do that".

## What changed

**The two t-test details pages:**

| test | line | beta 2b | beta 2c |
|---|---|---|---|
| 1, unpaired t | On the Prime | Inference > Hyp. test > T-Test: mu1 - mu2. | Fleet: TTestLab.  Inference: T-Test μ₁-μ₂. |
| 1, unpaired t | Afterwards | Also T-Int: mu1 - mu2 for the difference. | Also T-Int: μ₁ - μ₂ for the difference. |
| 3, paired t | On the Prime | Form the differences, then Inference > | Fleet: TTestLab, pairs in D1 and D2. |
| 3, paired t | Afterwards | Hyp. test > T-Test: 1 μ, with μ₀ = 0. | Or Inference > T-Test: 1 μ, diffs, μ₀ = 0. |

**Four spellings beta 2b's symbol sweep missed** (Roger, 20 Oct 2026: "use the symbols we developed"):
- "mu1 - mu2", twice, on test 1's page (above);
- "mu0" on test 21's page: "One group's mean against a given μ₀.";
- "pi0" on test 22's page: "One proportion vs π₀; counts vs expected.".

The R call `wilcox.test(x, mu)` is kept, as in beta 2b. μ₁ and μ₂ are new to TestChooser; their subscripts are device-verified (Lessons Learned §5).

## Not changed

- "Welch form if SDs differ" on test 1's page. Decision D12 (Welch's t by default) is still open. Roger has chosen the standard Welch formula for TTestLab; D12 is about TestChooser's wording.
- Every other line, the quiz, the table, the flowchart, the keys, the layout. The routines that differ from beta 2b: `tcDetail` only.

## Verification

`verify_TestChooser_beta2c.py`, output `verify_TestChooser_beta2c_output.txt`: **17 PASS, 0 FAIL**.
- The four new lines and the two symbol fixes, as drawn, in the old colours.
- Every details line of all 24 tests fits: at most 42 characters, inside x 312.
- Only `tcDetail` changed: 6 code lines, all detail strings. The hatching list `tcNotP` is unchanged and still matches the "Not on the Prime" lines.
- No spelled-out mu1, mu2, mu0 or pi0 left; no glyph outside beta 2b's and the verified list.
- TTestLab has what the pages promise (pooled and separate t; pairs from D1 and D2).
- text_overlap_v1 over the 24 details pages: no firm finding in beta 2b or beta 2c.

The 252 checks of `verify_TestChooser_beta2a.py` cover the logic, which beta 2b and 2c do not touch.

## Gate

`ppl_gate_v1c.py TestChooser_beta2c.txt TestChooser_beta2b.txt`: **RESULT: PASS**.
- ppl_check: clean (as beta 2b).
- lint_ppl's 52 "problems" are its known complaint about grobs passed as parameters; beta 2b has the same 52.

## Device checklist

1. Browse the table: open the unpaired t cell. "On the Prime:" reads "Fleet: TTestLab.  Inference: T-Test μ₁-μ₂.", whole, and "Afterwards:" reads "Also T-Int: μ₁ - μ₂ for the difference.".
2. The paired t cell: "Fleet: TTestLab, pairs in D1 and D2." and "Or Inference > T-Test: 1 μ, diffs, μ₀ = 0.".
3. The one-sample t cell (μ₀) and the one-proportion cell (π₀): the subscripts render.
