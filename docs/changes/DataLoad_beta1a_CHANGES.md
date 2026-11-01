# DataLoad beta 1a: changes (31 October 2026)

*From beta 1's run on the Virtual Calculator (`DataLoad_beta1_NOTES.md`). beta 1a never reached `programs/`: its own run found one more thing (beta 1b).*

## Changes

1. **Lists left from an earlier load.** Before it fills lists 1 … k, DataLoad looks at all nine. If any list after k holds data, the question has three answers, clearing first:
   - "Fill D1-D2, clear D3-D5" (empties them; the line DataLoad returns ends ", D3-D5 cleared");
   - "Fill D1-D2, keep D3-D5";
   - "Cancel".
   When only lists 1 … k hold data it is still "Replace D1-D5" / "Cancel". New routines `dd_Names` (a set of lists, short: "D1, D2", "D3-D5", "D1, D3-D5, D8"), `dd_Span` ("D1" or "D1-D4") and `dd_ClearRest`; new file-level `ddCLR`.
2. **The question names only the lists that hold data:** "D1, D2 hold data", "D1 holds data", "D4, D7 hold data".
3. **What each list holds names its matrix:** "M1 col 1", "M1 col 3 = 0", so lists from two loads cannot be taken for one. A list DataLoad did not fill this session reads "(earlier data)".
4. **A column that is blank throughout empties its list** (`D2 := {}`), instead of leaving the old values.
5. **The form:** title "Which columns? (M1 has 5)", labels "Scores:" and "Groups:", help lines "The column number of the scores" and "Column of the group codes (0/1, 1/2/3 …)". Its return is kept in `gok` and tested (the house pattern).
6. **The summary page:** n at x 114 and the box plots from x 150 (were 104 and 146), to make room for the longer descriptions.
7. **Help page 3:** RankLab under "D1-D9 (groups)", AgreeLab on its own line, and in orange: "AnovaLab, RankLab and AgreeLab read EVERY list that holds data: clear lists left from before." NormExplorer's C1/C2 line no longer calls them x, y only.
8. American spelling throughout ("color", "analyze").

Tried and dropped: starting the matrix menu on the matrix in use (`pc := ddSRC + 1` before `CHOOSE`). Whether `CHOOSE` takes its variable's value as the highlight is not known, `lint_ppl` flags an index not reset to 0, and Lessons Learned §2 says to start it at 0. The menu starts on M0, as before.

## Checks

- Gate: PASS; `lint_ppl` the same 4 entry-point notes as beta 1, nothing new.
- `verify_DataLoad_beta1a.py`: 55 PASS, 0 FAIL. New: E4, E5 (the question's wording), K1–K9 (clear, keep and cancel with D1–D5 holding data; only later lists holding data; `dd_Names` on seven sets; the C lists; the form; spelling); D3 now expects an empty list.

## The run on the Virtual Calculator (31 Oct 2026, 19:51–19:55 CDT)

Same calculator. beta 1's `DataLoad.hpprgm` was set aside to `Documents\HP Prime\_set_aside_2026-10-31\vc_before_dataload_beta1a`, beta 1a's copied in, Check: "No errors in the program".

1. Look, with beta 1's lists still there: D1–D5 "(earlier data)", clear of the n column.
2. M2, Columns, with D1–D5 holding data: "D1-D5 hold data", items "Fill D1-D3, clear D4, D5", "Fill D1-D3, keep D4, D5", "Cancel". Clear: the summary showed only D1–D3, "M2 col 1/2/3", n 9, 10, 5.
3. M1, Scores by group: the form read "Which columns? (M1 has 5)", "Scores:", "Groups:", both help lines whole. "D1-D3 hold data" → "Fill D1-D2, keep D3": D1, D2 "M1 col 3 = 0/1", n 216 each, and D3 kept as "M2 col 3", n 5.
4. The same again with "Fill D1-D2, clear D3": D1 and D2 only. Quit: "DataLoad: M1 col 1 by col 3 → D1-D2, D3 cleared".
5. Help page 3: every line inside the screen, the warning in orange.
6. **Found:** DataLoad run again and quit at once returned the same line, "… D3 cleared", though it had loaded nothing: the line lives in a file-level variable, which keeps its value between runs. Fixed in beta 1b.
