# AgreeLab beta 1b -- changes from beta 1a (28 Oct 2026)

**Layout only.** No number, formula, key handling or logic changed; verify_AgreeLab_beta1b.py (the beta 1a
script with the file name updated) passes with 0 failures and the same numbers.  The check count is 7379
against beta 1a's 7383 because its geometry pass counts distinct (text, x, y, width) keys and two y-axis
labels that used to sit at different rows now share a clamped row.  Gate: PASS.  Pure ASCII, LF.

## Rows moved (routine: old y -> new y)

| Routine | What | Old | New |
|---|---|---|---|
| ag_YAxis | y tick labels (every plot box) | tick - 6 | clamped to [box top - 2, box bottom - 10]: the top label no longer sits on the caption above the Bland-Altman box (`bias ..., 95% limits ...` at 22), the bottom one clears the x labels |
| ag_TDrawTiles | agreement bar (0/1 labels, po/pe labels) | bar 175 (labels 174, 186) | bar 171 (labels 170, 182) |
| ag_TDrawTiles | data-source / info line | 195 | 194 |
| ag_FDrawK (Fleiss page) | agreement bar | 172 (labels 171, 183) | 171 (labels 170, 182) |
| ag_TDrawWts | "Near misses ..." / "Unordered ..." and "Weights assume ..." | 184, 195 | 182, 194 |
| ag_CDrawData (ICC plot) | "targets ->" axis caption | (250, 164), under the x labels | (250, box bottom - 11), inside the box's lower-right corner |
| ag_CDrawData | "Parallel lines ..." / "Lines on top ..." | 172, 183 | 166, 178 |
| ag_CDrawBA (Bland-Altman plot) | legend rows | 166, 177, 188 | 166, 178, 190 |
| ag_Hello | opening band | AgreeLab - beta 1a | AgreeLab - beta 1b |

## Overlap counts (tools/text_overlap_v1.py --run the verify script)

| | Overlaps (firm) | Tight rows | Frame straddles (firm) | Overruns |
|---|---|---|---|---|
| beta 1a | 18 (16) | 24 | 0 (0) | 0 |
| beta 1b | 0 (0) | 15 | 0 (0) | 0 |

What remains (build/AgreeLab/overlap_AgreeLab_beta1b.txt): the Bland-Altman Stats page only -- 16 rows of
text at 11-px pitch from y 22 to 187, which 12 px cannot fit.

## Device checklist
1. Two-rater tiles page (Landis & Koch): the po/pe bar sits below the tiles with its po and pe labels above the grey "Data:" line, and that line clear of the footer.
2. ICC plot (Wright peak-flow): "targets ->" sits inside the lower-right corner of the box; the two grey legend rows are below the x labels and evenly spaced.
3. Bland-Altman plot: the top y label sits inside the box, under the black "bias ..., 95% limits ..." line; the three legend rows are evenly spaced above the footer.
