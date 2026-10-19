# ErrorRate Lab beta 1d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 1c; every beta 1c feature is kept, ordinary displays are unchanged, and the MicroPython block is byte-identical. Run only in the PC harness (ppl_run_v3e); not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 19; details in `findings_F.md`, section 1) listed four items for ErrorRate:

- **E-1, wrong text.** "a 20-character prefix leaves 24 columns for the CAS text at RMP 1 in 10⁹; the wrap pushes the page to 15 lines and drops 'RMP values are illustrative, not casework.'" The trawl's Exact page at RMP 1 in a billion read `P(at least one) = 1-(999999999/1000000000)` with `^N` on a line of its own, and its last line was gone.
- **E-2, cosmetic.** "a rule line above 100 % shown as a percentage": at 29 errors in 30 the panel read `39.54/n = 131.8 %`, and at n = 1 or 2 the "Why 3" page read `Rule: 3/n = 300.0 %`. Right arithmetic, a meaningless rate. The review also noted that the rule's `" = " + erlPctS(...)` was the one site erlEq did not cover.
- **E-4, cosmetic.** "the Engines page says 'CAS (exact text): not called yet' after a CAS page that made calls" (a "Why 3" page with k > 6, which asks the CAS for alpha but shows no CAS lines).
- **E-5, a guess to make safe.** "`erlPoiTerms` 1265: `FOR ptI FROM 1 TO ptJ - 1` runs with ptJ = 1 (FROM 1 TO 0)." Zero passes is what the User Guide's wording and the kit's interpreter give, but no one has watched the Prime run such a loop; one stray pass would put a false factor into the k = 1 limit.

**And Roger's disclaimer** (19 Oct 2026, 12:48, through the coordinator): a header line beside the distribution terms, and, because ErrorRate is forensic-facing (error rates and random match probabilities), the notice on screen too.

## What changed (line numbers: beta 1c → beta 1d)

1. **E-1, the trawl's Exact page** (erlTrExact, 2096 → 2165-2170). The prefix is `"  P(1 or more) = "`, 17 characters, so 27 are left for the answer. The longest answer the RMP menu can produce, `1-(999999999/1000000000)^N`, is 26 characters; a Prime that printed it the other way round, `-(999999999/1000000000)^N+1`, would be 27 and still fit. Every RMP on the menu (1 in 1,000 to 1 in 1 billion) now takes one line, the page keeps its 14 lines, and "RMP values are illustrative, not casework." stays on it.
2. **E-2, the rule at 100 % or more.**
   - New `erlRuleEq()` (→ 748-759, after erlRuleS). It returns `" is 100 % or more"` when rule/n ≥ 1, and otherwise `erlEq(erlPctS(rule/n))`, so the "=" is written only when no relation is there (`" > 99.9999 %"` can no longer follow an "=").
   - The panel (erlDrawText, 1001-1005 → 1053-1061): `39.54/n is 100 % or more: no use at this k, n`; below 100 % the line is as before (`3/n = 10.0 %, n × bound = 2.85 → 3.00`).
   - The "Why 3" page's Rule line (erlCasDraw, 1323 → 1386-1392): `Rule: 3/n is 100 % or more: no use here.` at n = 1, 2, 3; otherwise as before.
   - The summary returned to Home (ErrorRate, 2674 → 2762-2764): `(39.54/n is 100 % or more)`. The review listed the panel and the "Why 3" line; the summary prints the same rule the same way, so it is the third site of the same item.
3. **E-4, the Engines page** (erlEngPage, 2203-2235 → 2277-2317). It counts the CAS calls made before the page (`egN0`, read before its own live check adds one). When erlCasOK is still -1 but calls were made, the line reads `CAS (exact text): called, no Why 3 CAS lines` (46 characters). That covers a "Why 3" page at k > 6 or k = n, and the Bayes and trawl pages, which call the CAS but do not set erlCasOK. "not called yet", "exact on the last page" and "FAILED on the last page" are unchanged. (The review proposed `IF erlCasOK == -1 AND erlCasN > 0`; erlCasN already includes the page's own live check at that point, so that test would always be true. Counting before the live check fixes this.)
4. **E-5, erlPoiTerms** (1265 → 1321-1328): `IF ptJ > 1 THEN FOR … END; END;`. The text for k = 1 to 6 is unchanged.
5. **The disclaimer.**
   - The header (→ 15-17), beside the distribution terms: "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes."
   - On screen (erlWelcome, → 2615-2618): the opening page reads `Teaching aid; not for casework or legal use.` in red, font 1, at y 29, in the gap between the title (y 10) and the first line (y 44). It is 44 characters, inside the page's 296-px width.
   - "RMP values are illustrative, not casework." stays on the trawl page.
6. **The header:**
   - the banner;
   - the tested-on line ("Beta 1b, 1c and 1d have not run there yet (beta 1d has run only in the PC harness)");
   - the verify name;
   - the companion files;
   - a dated "What changed in beta 1d (19 Oct 2026): E1, E2, E4, E5 (fleet review 19 Oct)" paragraph (→ 46-76), whose line numbers are beta 1c's.

   A comment above each changed statement says what it does and why. Every comment sits at bracket depth 0. The file is still pure ASCII.

Nothing else changed. The verify's U6 shows that the routines differing from beta 1c are exactly ErrorRate, erlCasDraw, erlDrawText, erlEngPage, erlPoiTerms, erlTrExact and erlWelcome, plus the new erlRuleEq. Outside them only comments differ, and the changed code lines are exactly the 4 removed and 23 added that it lists.

**Before and after** (harness, reached as noted):

| Where | beta 1c | beta 1d |
|---|---|---|
| Trawl Exact page, RMP 1 in 1 billion, CAS answering | `  P(at least one) = 1-(999999999/1000000000)` / `^N`; 15 lines, the last one dropped | `  P(1 or more) = 1-(999999999/1000000000)^N`; 14 lines, "RMP values are illustrative, not casework." on the page |
| Panel, 29 errors in 30 | `39.54/n = 131.8 %, n × bound = 29.95 → 39.54` | `39.54/n is 100 % or more: no use at this k, n` |
| Panel, 0 of 1 / 0 of 3 / 1 of 4 | `3/n = 300.0 %, …` / `3/n = 100.0 %, …` / `4.74/n = 118.6 %, …` | `3/n is 100 % or more: no use at this k, n` (and `4.74/n …`) |
| "Why 3" page, 0 errors in 1 | `Rule: 3/n = 300.0 %.  n × bound = 0.950.` | `Rule: 3/n is 100 % or more: no use here.` |
| Summary to Home, 29 errors in 30 | `… (39.54/n = 131.8 %); see ER_UPPER` | `… (39.54/n is 100 % or more); see ER_UPPER` |
| Engines page after "Why 3" at k = 7, or after the Bayes page only | `CAS (exact text): not called yet` | `CAS (exact text): called, no Why 3 CAS lines` |
| Opening page | (no notice) | `Teaching aid; not for casework or legal use.` |
| 0 errors in 30, alpha 0.05 (the defaults) | `3/n = 10.0 %, n × bound = 2.85 → 3.00` | the same |

## Verification

`verify_ErrorRate_beta1d.py` was built from the beta 1c script, and every check is kept. It runs on beta 1d in harness ppl_run_v3e. Output is in `verify_ErrorRate_beta1d_output.txt`: **300 checks, ALL PASS** (beta 1c's script: 250).

Old checks whose expected value moved with beta 1d (each says so in its message):
- **R5:** the routines that differ from beta 1a now include beta 1d's.
- **T5:** beta 1b's text is also rewritten `P(at least one) = ` → `P(1 or more) = ` (E-1), and the new disclaimer line is set aside before the two sessions are compared.
- **T6:** checks the 1b → 1c diff, so it now reads beta 1c's own file.
- **T7:** the version strings are beta 1d's, and the INSTRING and bracket checks read beta 1d.

New section **U**:
- **U1 (E-1)** — the review's check 3c as a regression test. The 7 RMPs × N = 1, 10⁶, 10⁸, with the CAS answering and failing:
  - beta 1d: always 14 lines, the answer on one line, the closing line present, every line ≤ 46 characters;
  - beta 1c, CAS answering: fails at 1 in a billion (3 of 21).
  - A 27-character answer still fits.
- **U2 (E-2):**
  - the panel at 8 records, before and after;
  - the "Why 3" line at n = 1, 3, 4, and alpha 0.001 at n = 6;
  - the summary;
  - a sweep of 6 alphas × n 1-60 and 100-10,000 × 5 values of k: every record whose rule is ≥ 100 % says so, and the rest print a rate below 100 % with "=" or ">" alone;
  - a rule just under 100 % reads ` > 99.9999 %` (beta 1c's form: ` = > 99.9999 %`);
  - the widest line (9,999 of 10,000, alpha 0.001) fits.
- **U3 (E-4):** the Engines page after 7 histories, beta 1c → 1d.
- **U4 (E-5):**
  - erlPoiTerms is unchanged for k = 1-6.
  - In a copy of each file whose FOR runs once when its finish is below its start (`TO MAX(1, ptJ - 1)`, modelling a Prime that does so), beta 1c's k = 1 text gains `*(erlq-1)` and its limit changes. Beta 1d's text is unchanged, and the page stays `exact (CAS)` with `e^(-erll)*(erll+1)`.
- **U5:** the disclaimer is in the header word for word, and on the opening page (and so on ErrorRate()'s first screen), with the rest of that page unchanged.
- **U6:** the routine diff and the code-line diff, 1c → 1d. The #PYTHON block is byte-identical.
- **U7:**
  - erlRuleEq and egN0 are not built-ins;
  - no LOCAL line has more than 6 names;
  - no comment sits inside a bracket;
  - the file is ASCII;
  - the INSTRING lines are as before;
  - no new MAKELIST uses K.
- **U8:** the review's own `check_ErrorRate.py`, run unchanged except for its file path: **beta 1c 1 failure (its E-1 check), beta 1d 0**.
- **U9:** `h.sci_strings` over all 124 beta 1d runs: **empty**.

## Gate

`python3 ppl_gate_v1b.py ErrorRate_beta1d.txt _old/ErrorRate_beta1c.txt` in `gate_f19` (the newest version of every program; the other fix-19 versions present when it ran): **RESULT: PASS**.
- hp-prime-kit lint: 1 error, the #PYTHON block's "unbalanced", as beta 1c (the review confirmed it is the block's `#END`).
- ppl_check_v4: clean, as beta 1c. There are no hard errors, E12 included.
- lint_ppl: 17 problems, as beta 1c.
- Full parse: it stops at the EXPORT list (259; beta 1c 223), as beta 1c does. This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh`: kit lint has 1 error, inside the #PYTHON block only; check_v4 has no hard errors; the parse stops on the same construct as beta 1c (line 259 vs 223, the EXPORT list).

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 1c (open it in the Kit; do not add a second copy). Then Program Catalog → Check.
2. **Opening page:** `Teaching aid; not for casework or legal use.` in red under the title, not touching the title or the magenta line below it.
3. **E-1:** More → Trawl → RMP "1 in 1 billion" → Exact. The CAS line reads `  P(1 or more) = 1-(999999999/1000000000)^N` on ONE line, and the last line reads "RMP values are illustrative, not casework.". Note how the Prime prints the answer.
4. **E-2:** "n, k": 30, 29, 0.05. The green panel line reads `39.54/n is 100 % or more: no use at this k, n`. Then 1, 0, 0.05 and Why 3: `Rule: 3/n is 100 % or more: no use here.`. Quit: Home's summary ends `(… is 100 % or more); see ER_UPPER`.
5. **E-4:** "n, k" 30, 7 → Why 3 → back → More → Eng: `CAS (exact text): called, no Why 3 CAS lines`.
6. **E-5, and the open question:** n, k 30, 1 → Why 3: the limit line reads `e^(-μ)×(μ+1) = 1/20` under "exact (CAS)". Then type `FOR I FROM 2 TO 1 DO PRINT(I); END;` in Home: nothing should print (the review's section 5). This settles whether the guard was ever needed; it is harmless either way.

## Unresolved (open decisions touching ErrorRate; not changed here)

- **D17 / E-3:** the developer lines on student pages ("Nothing here has run on a calculator yet." on Help page 9; the Engines page's "The CAS call form is the one CASProbe beta 1b found …"). Kept.
- **D17:** a typed "1" means 100 % in the rate form but 1 % in the alpha form (`erlAskRate` `arP > 1` vs `erlAskNK` `>= 1`). Unchanged.
- **The trawl's top end** reading `100.0 %` (beta 1c's "seen, not changed"). Unchanged.
- **Seen, not changed:** two dotted-line loops can also run FROM a start TO a smaller finish when the marker sits at the plot's left edge (erlDrawPlot 933, erlTrDraw 2028 in beta 1c). One stray pass would draw a single pixel, so they are cosmetic either way and were left alone.
- **Review improvements** (section 4; not in this pass): checking CAS answers by value (fence rule 7), the LOCAL MAKELIST counter, and a grey caveat line on the main screen.
