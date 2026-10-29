# RankLab beta 1b -- changes from beta 1a (28 Oct 2026)

**Layout only.** No number, formula, key handling or logic changed; verify_RankLab_beta1b.py (the beta 1a
script with the file name updated) passes 6064 checks, 0 failures, the same numbers as beta 1a.  Gate: PASS.
Pure ASCII, LF.  The FILE MAP block was rebuilt (filemap_RankLab.py) for the new line numbers.

## Rows moved (routine: old y -> new y)

| Routine | What | Old | New |
|---|---|---|---|
| rk_Prog | the progress panel drawn on G0 during a long loop | a 260 x 58 panel at (30, 92)-(290, 150) that cut through the rows of the page beneath it (the opening page's and the help pages' lines showed on both sides and above and below it) | a working page under the title bar, (0, 20)-(319, 239), orange border, light orange fill -- SurvLab's sv_Busy shape |
| rk_Prog | message / bar / "Esc = stop" line inside it | 98 / 118-130 / 135 | 104 / 124-136 / 142 |
| rk_PgDunn | "mean" / "rank" y-axis label | 24, 35 | 24, 36 |
| rk_PgScat | "x = ... (rank)" caption under the x labels | 165 | 166 |
| rk_PgScat | the two readout rows | 180, 191 | 180, 192 |
| rk_PgNull | the three legend rows in the orange panel (165-202) | 167, 178, 189 | 167, 179, 191 |
| rk_PgNull | the red observed-value label at the top of the box | kept 6 px/char from the right edge | 7 px/char (it crossed the edge by 1-4 px at the checker's widths) |
| rk_Welcome | title | RankLab - rank tests, beta 1 | RankLab - rank tests, beta 1b |

**For the lead's eye:** the rk_Prog change is the one visible change of look -- a full working page instead of
a small panel.  A panel that leaves whole rows of the page beneath it intact cannot be placed, because the
opening page (rows 13 px apart from 76), the help pages (13 px apart from 26) and the result pages all put
their rows at different heights; any panel edge cuts a row of one of them.  Revert to the old six lines of
rk_Prog if the small panel is preferred.

## Overlap counts (tools/text_overlap_v1.py --run the verify script)

| | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns |
|---|---|---|---|---|
| beta 1a | 7 (7) | 9 | 3 (0) | 0 |
| beta 1b | 0 (0) | 0 | 0 (0) | 0 |

Nothing remains (build/RankLab/overlap_RankLab_beta1b.txt).

## Device checklist
1. Load a long data set (or any exact null with n > 20): the progress page fills the screen under the title bar with its message, bar and "Esc = stop" line; Esc still stops it.
2. Null-distribution plot (e.g. the signed-rank S+ page): the red "S+ = ..." label stays inside the box at the right edge; the three legend rows in the orange panel are evenly spaced.
3. Dunn page: "mean" / "rank" at the top left are not touching; Spearman scatter page: the "x = ..." caption clears the x tick labels, the two readout rows clear each other and the footer.
