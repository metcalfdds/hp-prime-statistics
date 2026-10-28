# SeizureLab beta 1a: what changed from beta 1 (21 Oct 2026)

`/home/claude/new6/SeizureLab_beta1a.txt` (2,771 lines); `SeizureLab_beta1.txt` is untouched. Every item of the second review
(`REVIEW2_SeizureLab_beta1.md`) is applied below, with Roger's decisions as the lead relayed them. Each line gives the review
item number.

## Review items

| Item | Change |
|---|---|
| 1 | **The Bayesian least-n searches are bisections.** `sz_BaySrch` (new) doubles its step outwards from the large-N guess until the answer is bracketed, then halves. The condition is monotone in n (verify A11 grid; R1, 150 typed priors), so no step fallback was needed. |
| 1 | **Speed on the reviewer's slow cases.** They now take 9 to 27 sums each, against 116 to 3,537 before: N = 10000 with prior Beta(1, 100) takes 21 sums. The answers are unchanged (5668, 5046, 9746, 323, 957, 142). |
| 1 | **Esc stops them.** `sz_EscHit` (new) polls Esc between sums and draws a moving progress tick. Set up, Prior and the Tables page show "stopped"; a stopped table is recomputed the next time the page opens. |
| 1 | **The busy box is honest.** It now says "Esc = stop. A large N or strong prior can take a minute or more on a G1." |
| 2 | **The weight factor is √((N − n)/N)** (Roger's D1; theory, the reviewer's simulation, and ENFSI §7's 0.877 = √(77/100)). The code, the page text, help page 5 and the header all changed. The example now reads SE 0.3134 g and bound ≥ 49.96 g. |
| 2, 3 | **A new help page 6, "Checking against ENFSI (2009)".** It has live numbers: 23, 36, 46; Table 4's 28 against the beta-binomial's 22; and ENFSI §7's example, which the student can type in to get 26.50 ± 0.8728 g against ENFSI's printed 26.500 ± 0.873 g. Same factor; ENFSI rounds t to 2.074. |
| 2 | **The weight page shows the CI half-width** ("(± 0.8728)"), so the ENFSI example can be compared directly. |
| 3 | **The Bayesian page shows "this N 22; N → ∞ 28" side by side**, plus the line "ENFSI Table 4 takes N → ∞ (it assumes N ≥ 50)". The header attribution was corrected. |
| 4 | **The tie tolerance is 1E-6 relative to 1 − c** (`sz_Le`: P ≤ (1 − c)(1 + 1E-6); `sz_Ge`: P ≥ c − 1E-6(1 − c)). In the 12-digit emulation the reviewer's flip case (N = 5000, p0 = 0.0501, c = 0.95) gives P = 0.0500000046777, which now counts as met: least n = 1, as in exact arithmetic. A tolerance relative to c was rejected: at c = 0.9999 it moved a least n (5665 instead of 5668). |
| 5 | **Both OC drag loops are guarded.** `sz_DragOn` (new) ends a drag on any key or on an off-screen reading (a phantom touch). The θ drag draws a frame only when θ changes. |
| 6 | **The observed bar's outline is four red LINE_P.** A one-colour RECT_P filled it red. |
| 7 | **CHAR(8592) and CHAR(8645) are gone.** The legends and help use words ("Left/Right", "Up/Down"). |
| 8 | **Every text line fits its width.** Font 1 is budgeted at 6.5 px and font 2 at 8 px a character, checked at the defaults and at the reviewer's extreme inputs. The changes: <ul><li>titles shortened;</li><li>`sz_Fit` (new) chooses a shorter wording when a line would pass 46 characters;</li><li>"the your own prior" is now "Beta(…), typed" on its own line;</li><li>the opening disclaimer is reflowed;</li><li>help lines are at most 45 characters;</li><li>the prior's a and b are rounded to 2 decimals.</li></ul> |
| 9 | **Each page's footer names its own keys.** The OC page's worst-case line moved into the plot corner, freeing y 192 for its legend. Help page 7 now lists the keys page by page. |
| 10 | **The set-up form now reports every clamp**: negatives allowed outside 0 to 20, a prior outside 0.1 to 100, a prior rounded to 2 decimals. The other messages were shortened, so all of them together still fit one MSGBOX of 5 lines or fewer. |
| 11 | **Sources.** The header and help page 8 cite the ENFSI guideline with its UNODC link (ST/NAR/38) and Cochran (1977) for the weight. Both mention Stoel & Bolck's correction to Tzidony & Ravreby (not read), and mark Aitken, Coulson, Tzidony & Ravreby and Frank as "not checked against the papers". |
| 12 | **ENFSI Table 2's misprint goes in the NOTES only**, not on screen: N = 90, 99%, k = 0.7, 2 negatives prints 21, and exact arithmetic gives 22. |
| 13 | **Style.** The darker szWRNG shade is explained in a comment. "Lower 95% confidence bound" replaces "95% lower bound". The footers and help were reworded. |

## Found while fixing

- **The binomial page's caption** reads "P(≤ d neg), cut at …".
- **The OC page's p₀ label** moves to the left of its line near the right edge, so it can no longer leave the screen.
- **The OC columns use ⌊θN + 1E-9⌋.** The second review saw a binary artefact here (774.9999999999999); it cannot happen on the Prime.

## Routines

- **Changed:** sz_BayDraw, sz_BayMin, sz_BayMinL, sz_BinDraw, sz_BinTap, sz_Busy, sz_Ge, sz_Help, sz_HypDraw, sz_Init, sz_Le, sz_NStr, sz_OCDraw, sz_OCFit, sz_OCPage, sz_Open, sz_PrName, sz_PrNext, sz_Recalc, sz_Setup, sz_TabCalc, sz_TabDraw, sz_TabPlot, sz_WtCalc, sz_WtDraw.
- **New:** sz_BayOK, sz_BaySrch, sz_DragOn, sz_EscHit, sz_Fit.
- **File-level additions:** szStop, szPrg, szDgX.

Every other routine is byte-identical to beta 1 (verify part G).

## Checks

| Check | Result |
|---|---|
| `verify_SeizureLab_beta1a.py` | 17,991 checks, 0 failures (output beside it). Parts A, B and C are beta 1's (references updated to the item 2 and item 4 rules); part R has one block per review item; part G is the routine diff. |
| Gate, `python3 ppl_gate_v1c.py SeizureLab_beta1a.txt SeizureLab_beta1.txt` | PASS (`gate_SeizureLab_beta1a_output.txt`). Kit lint 0 errors, ppl_check clean, fleet_names 0 collisions / 0 untagged / 0 built-in matches. The known noise is unchanged: lint_ppl's 6 EXPORT/filename lines, and the parse limit at the file-level LOCAL after EXPORT. |
