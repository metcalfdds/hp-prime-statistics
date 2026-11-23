# TTestLabG beta 1j: changes (22 November 2026)

Round 18 of 22 November 2026: every program sets the four Home settings that the book's examples assume when it starts, and leaves them set. That afternoon the Virtual Calculator had been set to a comma as its decimal point (Home Settings, Digit Grouping 123.456,789), as a reader in Europe may have it. `STRING` then writes a comma, inside a running program too, and every program's comma routine took the decimals for a whole number: Norm3 showed 0.9772 as 0,9,772, and the two programs with no `#pragma mode` line, NormExplorer and StudRange, stopped the calculator at Run (`docs/dev/comma-decimal-mark-2026-11-22.md`). Three probes showed that a program can assign Home's settings and that they stay set (`diagnostics/SetProbe_beta1.txt`, `SetOdd_beta1.txt`, `SetBook_beta1.txt`). Roger, asked whether a program should put the reader's own settings back when it ends or leave the book's on: "I agree that we should leave the calculator the way Statisticles sets it--and that also helps avoid any potential mis-settings in subsequent Statisticles--we keep putting the calculator in the mode we need it to be in". The round is in `verify/round18/README.md`.

## What changed

1. **One line at the head of `TTESTLABG`** (line 2,165), after the routine's LOCAL lines:

   ```
   HSeparator := 0; HFormat := 0; HAngle := 0; Entry := 0;   // Round 18: the book's four Home settings, left on
   ```

   `HSeparator := 0` is Digit Grouping 123,456.789 (the period as the decimal point), `HFormat := 0` is Number Format Standard, `HAngle := 0` is Radians and `Entry := 0` is Textbook entry. Nothing puts them back: the calculator is left the way the book needs it.
2. **Built from TTestLab beta 1m** by `tools/make_tlg1_v5.py` (v4 for the next pair of versions; its blocks are v4's, unchanged), as the general version always is. The line came over with the code.
3. **Nothing else changed.** With that line and the history note taken out, TTestLabG beta 1i and TTestLabG beta 1j are the same line for line but for the version: the header (one line); the program shows no version on its pages. The history note is lines 20 to 27. No help page, no menu, no number and no other word on a page changed.

## For the book

- The version in the table of "How to use this book" becomes beta 1j, and Appendix F's count of lines becomes 2,197 (it was 2,188).
- Draft 69 asks every reader to choose 123,456.789 and says that two of the programs showed their numbers with commas in the wrong places. With this version the program sets the four settings itself, so that sentence changes with the book's next draft.
- The help pages are word for word the same, so the book's printed help pages stand.

## Checks

- `verify/verify_round18_settings_v1.py` (225 checks, 0 failed, for the 31 programs together; its output is beside it). For TTestLabG: T1, only the round's lines changed; T2, the line is the first statement of each start routine after its LOCAL lines; T3, the first line is the pragma line.
- `tools/ppl_gate_v1e.py` against TTestLabG beta 1i (`verify/round18/gates/TTestLabG_beta1j.txt`): PASS.
- The harness smoke test (the start routine, idle key Esc): TTESTLABG(): warnings 0 (old 0). Started with HSeparator 4, HFormat 1, HAngle 1 and Entry 2, the harness held 0, 0, 0 and 0 afterwards. The harness has no Home settings of its own and always writes a period (`tools/prime_facts_v1.py`, facts 5 and 6), so this shows that the line runs and nothing more.
- `tools/fleet_names_v2.py` and `tools/screen_text_v1.py` over the 31 newest files: no collisions, no place against the rules.
- Not made again: the text-overlap walk and the monkey's runs. Nothing a page draws differs but the version where a page shows it.
- HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 22 Nov 2026 (`verify/round18/vc_checks.txt`): Program Catalog > Edit > Check at 17:58 said "No errors in the program". Run at 18:44 with the calculator just left in RPN entry, with a comma as the decimal point, Fixed 2 and Degrees (SetOdd, and Home Settings read to see it): its menu; afterwards Home Settings read Radians, Standard, 123,456.789 and Textbook.

## On a G1 or a G2

Not yet run on a G1 or a G2. The check, which takes two minutes:

1. Shift, Home. Set Angle Measure to Degrees, Number Format to Fixed 2, Digit Grouping to 123.456,789 and Entry to RPN.
2. Start TTestLabG from the Program Catalog.
3. On its pages a decimal has a period and a number of 1,000 or more has commas, as in the book.
4. Leave the program. Shift, Home: Angle Measure reads Radians, Number Format Standard, Digit Grouping 123,456.789 and Entry Textbook.

## Unresolved

- The program changes four of the calculator's settings and says so nowhere on the calculator: no help page was changed in this round. The book says it.
- What RPN entry does inside a running program was seen only as far as the run above went; no form was filled with the calculator in RPN, because the line has set Textbook before any form opens.
- Whether an app's own angle or number format setting overrides Home's inside a program was not tried.
