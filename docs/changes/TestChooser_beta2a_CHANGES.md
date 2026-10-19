# TestChooser beta 2a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 2; every beta 2 feature is kept, and no test, quiz case or key changed. Run only in the PC harness (ppl_run_v3e), not yet on the emulator or a calculator. Beta 2 passed the emulator on 17 October.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 17; `findings_B.md`, TestChooser) listed these to fix now:

- **T1. WRONG TEXT: "three details pages send students to retired programs."** Lessons Learned §15 and v7g: "ConTable2 and FEP are retired: EpiStats v1.6 module 1 and EpiStats2x2(a,b,c,d) replace them. Delete them from the calculators." Beta 2 still read:
  - chi-square 2×2 (291): `Fleet: FEP (Fisher), ConTable2, EpiStats.`
  - McNemar (302): `Fleet: ConTable2.  By hand, 1 df:`
  - RR / OR (314): `Fleet: EpiStats, ConTable2; Inference X2.`
- **T2. COSMETIC: "the menu's third item is 31 characters."** `Quiz: which test fits the case?` (1759). The emulator cut items of 31 to 36 characters.
- **T3. COSMETIC: "the two '(none)' survival cells are hatched differently."** `tcNotP` (1737) follows the third detail line. Test 18 (before/after survival) says "Not on the Prime" on its fourth line, so it was not hatched, while its twin, test 19, was. The legend says hatched means "not on the Prime", which is true of both.
- **The factual wordings:**
  - log-rank (349): it is "most powerful if hazards are proportional", and does not "assume" them;
  - Cochran's rule (295): "no more than 20 % of cells below 5 and none below 1", not "most expected counts at least 5";
  - `cochran.qtest` (308) is in the RVAideMemoire package, not base R.
- **Kept, as the brief says:** "Welch form if SDs differ" (259). D12 (Welch by default) is open.

Roger's addition of 19 October (12:48 CDT): the disclaimer line beside the distribution terms.

## What changed (line numbers: beta 2 → beta 2a)

1. **T1** (`tcDetail`). The pages now name EpiStats and its module names: module 1 is "2×2 Table Analysis", with Fisher's exact and its Paired reading (McNemar, `es_McNemar`); module 2 is "Risk Analysis (RR, OR, NNT)". The details page shows each line under a heading (What / Assumes / On the Prime / Afterwards / If an assumption fails), so each new line stays in its slot.
   - chi-square 2×2, "Afterwards" (291 → 330): `Fleet: EpiStats > 2x2 Table; ChiTable.`
   - McNemar, "On the Prime" (302 → 341): `Fleet: EpiStats > 2x2 Table > Paired.` With "By hand, 1 df:" no longer fitting there, the next line, "Afterwards" (303 → 342), carries it together with the statistic: `By hand, 1 df: X2 = (|b-c| - 1)^2/(b+c).` That is es_McNemar's continuity-corrected statistic, as before.
   - RR / OR, "On the Prime" (314 → 353): `Fleet: EpiStats > Risk; Inference X2.`
2. **T2** (`TestChooser`, 1759 → 1800): `Quiz: which test fits?` (22 characters). The item number is unchanged, so no key or script changes.
3. **T3** (`tcInit`, 1734-1737 → 1773-1778): `tcNotP(18)` is 1, and the comment above it says why. Thirteen cells are hatched, not twelve. The header's beta 2 paragraph notes "(thirteen since beta 2a, T3)".
4. **The wordings** (`tcDetail`):
   - log-rank, two groups, "Assumes" (349 → 388): `Most powerful if hazards are proportional.`
   - chi-square r × c, "Assumes" (295 → 334): `Expected < 5 in <= 20% of cells; none < 1.` The rule's name is left out on purpose: "Cochran" on this page could be confused with Cochran's Q, test 9.
   - Cochran's Q, "On the Prime" (308 → 347): `Not on the Prime.  R: RVAideMemoire pkg.` The function's name does not fit the 42-character line with the package. "Not on the Prime" has to start the line, as on the other twelve pages. The package is what a student has to install.
5. **Header:**
   - the banner (4);
   - the disclaimer line after the distribution terms (→ 25-27). The help pages do not state the terms, so no line was added on screen.
   - the tested-on lines (26-27 → 29-33);
   - a "beta 2a (19 Oct 2026)" paragraph (→ 35-67).

Only `tcDetail`, `tcInit` and `TestChooser` changed: 9 code lines (7 detail strings, 1 menu string, the `tcNotP` list).

**Seen, not changed:** test 17 (log-rank, three or more groups) reads "Chi-square, k − 1 df; prop. hazards." on its "Assumes" line. The review did not list it, so it is left for Roger with the log-rank wording.

## Verification

`verify_TestChooser_beta2a.py` was built from `verify_TestChooser.py`, and every check is kept. It runs on beta 2a in harness ppl_run_v1, as before. Two of its expected values were the bug T3, so they change with it:
- "tcNotP equals the line-3 rule" becomes "the tests whose details say Not on the Prime", because test 18 says it on line 4;
- "twelve hatched tests" becomes thirteen.

Output: `verify_TestChooser_beta2a_output.txt`: **252 checks passed, 0 failed** (beta 2's script had 230).

`t_beta2a` is new (harness ppl_run_v3e):
- **The review's `check_TestChooser.py`** (26 checks), loaded once per version.
  - Its part C lists the menu items as written in beta 2. Here they are read from each version's own CHOOSE, so the check tests the file it runs on.
  - On beta 2 exactly its three failing checks fail: A (T3), B (T1) and C (T2).
  - On beta 2a all 26 pass.
- **The pages as drawn:** tests 6, 7, 8, 9, 10 and 16 show the new lines at their headings, and every detail line is at most 42 characters. Test 1 keeps "Welch form if SDs differ". No code line names ConTable2 or FEP. EpiStats v1.7c really has the modules the pages name (checked in its source).
- **T3:** `tcNotP` equals the tests whose details say "Not on the Prime" (13), and 18 and 19 are both hatched. The table's hatching dots in G2 go from 1,339 to 1,472, one more cell.
- **T2:** the menu reads `Guide me: the flowchart`, `Browse the table (Glantz)`, `Quiz: which test fits?`, `Help`, `Quit` (longest 25), and the renamed item still opens the quiz.
- **The routine diff:** `TestChooser`, `tcDetail` and `tcInit` only (of 52 routines), and the 9 code lines above.
- **Static rules:** no `//` inside an open bracket; the banner, paragraph, status line and disclaimer; every LOCAL line holds at most 6 names; no INSTRING.
- **No scientific fixed decimal** in any of the 174 ppl_run_v3e runs.

## Gate

`python3 ppl_gate_v1b.py TestChooser_beta2a.txt _old/TestChooser_beta2.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as beta 2. No hard errors (E12 included).
- lint_ppl: 52 problems, as beta 2.
- Full parse: it stops at the file-level LOCAL after the EXPORT (174), as beta 2 does at the same line (135). This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh TestChooser_beta2a.txt TestChooser_beta2.txt`: the same.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 2 (open it in the Kit), then Program Catalog → Check.
2. **T2.** The menu's third item reads `Quiz: which test fits?`, whole. It opens the quiz.
3. **T1.** Table → Nominal row:
   - the 2×2 cell → its page reads "Afterwards: Fleet: EpiStats > 2x2 Table; ChiTable.";
   - the McNemar cell (before/after) → "On the Prime: Fleet: EpiStats > 2x2 Table > Paired." and "Afterwards: By hand, 1 df: X2 = (|b-c| - 1)^2/(b+c).";
   - the association cell → "Fleet: EpiStats > Risk; Inference X2.".
   - Every line is whole within the frame.
4. **T3.** Table, Survival row: the before/after and repeated cells are both hatched.
5. **Wordings.**
   - Survival / two groups: "Assumes: Most powerful if hazards are proportional."
   - Nominal / three or more groups: "Assumes: Expected < 5 in <= 20% of cells; none < 1."
   - Nominal / repeated: "On the Prime: Not on the Prime.  R: RVAideMemoire pkg."

## Unresolved

- **D12** (Welch's t by default, Delacre 2017, Ruxton 2006): open. "Welch form if SDs differ" is kept as the brief says.
- From findings_B's "Decisions for Roger" (D4), not in this pass: quiz case 10 also accepting chi-square r × c; case 16's reason line naming the trend version.
- Test 17's "prop. hazards" on its "Assumes" line (see above).
