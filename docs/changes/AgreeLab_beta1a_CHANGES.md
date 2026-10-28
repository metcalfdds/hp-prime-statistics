# AgreeLab beta 1a: changes from beta 1 (26 Oct 2026)

Source: `REVIEW2_AgreeLab_beta1.md` and the lead's decisions. Beta 1 is unchanged. Beta 1a has 2,945 lines and 101 routines.
Verify (`verify_AgreeLab_beta1a.py`): 7383 checks, 0 failures. Gate (against beta 1): PASS.

| # | Review finding | Fix in beta 1a | Regression check |
|---|---|---|---|
| 1 | A 1-px drift across a tile edge moved a count | `ag_TTap`: a move needs a different tile AND finger travel of at least MAX(8, cz/2) px (\|dx\| + \|dy\|); anything less is a tap on the press tile | B17: a 1-px drift moves nothing; a 16-px drag moves 1. By routine: at k = 4, 15 px is a tap and 16 px a move; at k = 6, 10 px is a tap and 11 px a move |
| 2 | An edited preset kept its published source | New `ag_TEdit` runs on the first change (move, +/-, ToDiag/FromDg, a typed count that differs): the source line reads "edited from <source>" in red, the title gains " (edited)", and the Home summary ends ", edited from <source>". A table typed in is never marked. Reloading the preset clears the mark | B17, B18 |
| 3 | ICCs were refused when the error MS = 0 | Sums of squares below 1E-10 of the total are set to 0. Every form is then computed from its formula: a constant offset gives ICC(3,1) = 1, ICC(2,1) = 0.118, ICC(1,1) = −0.579; perfect agreement gives every ICC = 1. Where F is infinite the row reads "no F interval (error MS = 0)" (or within / target MS = 0), and the message says "F is infinite". "Undefined" is now shown only when every rating is the same. Line 854's "every target has the same mean" refusal is gone: those single-rating forms are computed, and the average forms show "undefined (denominator 0)" | ICC review offset, perfect, target-MS-0 and 15 small-integer sets (routine level); B20, B22 (pages) |
| 4 | ICC(2,k) printed 4.8E15 with an off-screen marker | Every ICC denominator is guarded (≤ 1E-10 of the largest MS means undefined): the value shows "--" and the row "undefined (denominator 0)" (`agIDf`; −99 in `AG_ICC`). A marker is drawn only for a defined value inside [axis min, 1]; "< −999" for values below that. `ag_Fx` writes numbers of 1E11 and up by hand as "1.234E11", so STRING's scientific form never appears | ICC(2,k) denominator 0 (routine); B21: no scientific string, no off-screen shape; `ag_Fx` 1.234E11, −5E15, 3.3E30 |
| 5 | Unlabelled approximate CIs for the Bland-Altman limits | The Stats page says "approx. SE of a limit (B & A 1986)" and "approx. 95% CI, lower/upper limit", plus "approximate: too narrow for small n (Help 7)" when n < 30. The plot legend reads "bands: approx. CIs". Help page 7 marks the CI APPROXIMATE and gives the review's simulated coverage (about 92% at n = 3-5, 94% at n = 17). **The exact Carkeet (2015) noncentral-t interval is NOT implemented:** a noncentral-t quantile in PPL would cost many incomplete-beta series per root step on a G1, and it could not be verified in this pass | B5, B13 page 7 |
| 6 | Kappa CI and p at the edges | The CI is clipped to [−1, 1] and says so ("95% CI (clipped):" on Tiles, ", clipped" on Kappa, and the same on Wts). No SE, CI or p is shown (and none is exported: AG_SE 0, AG_P −1) when N < 10, a row or column total is 0, or SE = 0; the reason is shown. p above 0.99995 prints "p > 0.9999" (FitCheck's form) | routine checks on every table: clip flag, inference flag, 0/12/9/0, N = 2, ag_PE boundary; B19 pages |
| 7 | `ag_Poll` did not drain a finger | `ag_Drain()` after `ag_KDrain()` at the top of `ag_Poll` | source check; the stale-key runs |
| low | The B & A line | "with 2s (as in 1986): −79.65 to 75.41". On the peak-flow preset only: "the paper, rounding, prints −79.7 to 75.5" | B5 |
| low | The tiles footer | "+/- = count, drag = move, Ent = menu, Esc = back" | B1 |

Also changed:
- `ag_TSet` takes a fifth argument, the short source name.
- An unused local `baC` was removed.
- The Bland-Altman Stats page is spaced at 11 px.
