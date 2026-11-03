# Every program's labels under random use (round 4, 2 November 2026)

*Round 4 of the monkey work fixed PowerViz, ScatterLab, ChiTable and GaltonBoard, and checked every program's labels. This is that check: what it ran, what it found, and what was done about it.*

## Why a new check

The fleet's layout check, `tools/text_overlap_v1.py`, has run over every program since 28 October, driven by each program's verify script or by a generic walk from the program's own start-up values. At those values labels are short. The cut numbers and crowded labels show at the odd values a careless student types, and `text_overlap_v1` cannot see a number cut short by `TEXTOUT_P`'s width argument at all: it measures a text as the smaller of its width and that argument. So round 4 added two things:

- **`tools/label_fit_v1.py`**: every text measured at the narrow glyph widths (5.5 / 6.5 / 7.5 px a character for fonts 1 / 2 / 3, 3 px a decimal point), and reported when the part past its width argument holds a digit, or when a text that is a number alone is cut at all: the calculator would cut it. ScatterLab beta 2d printed y = 100000 as "10000" this way. (The first version read only texts that are a number alone; below, "The same runs again".)
- **The check under random use** (`tools/monkey_labels_v1.py`): each current program run 100 times by the monkey (`tools/monkey_v1b.py`: random keys, taps, menu picks and typed values, 1E300 and 1E−300 among them), with `text_overlap_v1`'s recorder on, then `label_fit_v1` over every screen drawn. GaltonBoard got 25 runs (its animations are slow in the harness).

A generic walk at the start-up values (`text_overlap_v1.py --walk`, 30 runs a program) found nothing in any program: no firm overlap and no cut number. The random runs found the rest.

## What the random runs found

"Firm" is `text_overlap_v1`'s firm finding: still there at the narrow glyph widths. Counts are distinct findings over the program's 100 runs.

| Program | Firm findings | Cut numbers | Where | Done |
|---|---|---|---|---|
| ChiTable beta 3e | 2 overruns | 0 | the observed χ²'s label on the curve page past the right edge (`csCvDraw`) | **fixed in beta 3f** |
| GaltonBoard beta 3e | 18 overlaps, 3 straddles | 0 | the bin panel's edge beside the left readouts (`gbBinInfo`); a peg count "9" under "10" (`gbPour`) | **fixed in beta 3f** |
| PowerViz v2.5l (first build) | 1 overlap | 0 | test 4's SE line reaching "n₈₀ = 3826" (`pv_Draw`) | **fixed in v2.5l** |
| ScatterLab beta 2e | 0 | 0 | none here; its side panel's cut number showed on the Virtual Calculator (below) | **fixed in beta 2f** |
| BiNorm3D beta 1b | 47 overlaps | 0 | the 3-D view's axis letter "y" over "cut at x₀ = 1.50" and "11×11 while dragging" (`bnDraw3D`) | next round |
| BurrLab beta 1i | 0 | 1 | "1000000" in a 36 px width | next round |
| DataLoad beta 1b | 1 overlap, 1 overrun | 0 | `dd_Confirm`; "91.42" past the right edge (`dd_DrawHisto`) | next round |
| EpiStats v1.7e | 8 overlaps, 1 straddle | 0 | the footer notes over the plot's labels (`es_Foot`) | next round |
| ErrorRate beta 1e | 33 overlaps, 5 straddles | 0 | "α = 0.05" over the percentages (`erlDrawMain`); "density" over "95 %" (`erlBayesDraw`) | next round |
| Norm3 v2.4d | 24 straddles | 0 | y labels and the title across the frame | next round |
| NormExplorer beta 42e | 19 overlaps, 1 straddle, 3 overruns | 0 | the μ marker over "μ = 0.00" and the readouts (`ne_NormDraw`) | next round |
| RiskLab beta 1b | 1 straddle | 0 | "0.96" across the top edge (`rl_FairDraw`) | next round |
| SampDist v2.3e | 1 overlap, 2 straddles, 2 overruns | 0 | "n = 1.23456789012E12: σ…" off the screen (`sd_drawCmp`) | next round |
| StatDist v2.7h | 11 overlaps, 4 overruns | 0 | the "a" and "b" markers when the bounds are close (`st_Draw`) | next round |
| StudRange beta 15f | 9 overlaps | 0 | y labels of 2E11 … 1E12 on top of each other (`sr_Yard`); "60" over "0.00" (`sr_PlotMode`) | next round |
| TestChooser beta 2c | 1 overlap | 0 | "roughly normal" over "Nominal" (`tcShow`) | next round |
| every other program | 0 | 0 | | |

Norm3, NormExplorer, SampDist and StatDist passed this check in their verify scripts (round 3, 1 November): their findings appear only at values those scripts did not try. That is the point of running the check under random use.

## The same runs again, reading every line (2 November, evening)

The table above came from the first version of `label_fit_v1`, which read only texts that are a number alone. On the Virtual Calculator, ScatterLab beta 2e then printed an SSE of 18,053,333,333 on its side panel as "SSE = 1805333333": a label and a number on one line, cut by the panel's 86 px, which that check did not read. A number ten times too small, behind a label, is the worst kind of cut. The check now reports any text whose cut-off part holds a digit, and every current program was run again the same way (100 runs each, seeds 3000 on; GaltonBoard 25).

The firm findings were the same. The cut texts:

| Program | Cut texts | Where | Done |
|---|---|---|---|
| ScatterLab beta 2f | 0 | (beta 2e: the side panel, `slPanel`) | **fixed in beta 2f** (`slFitN`: "SSE = 1.8053ᴇ10") |
| BurrLab beta 1i | 1 | "1000000" in a 36 px width, as before | next round |
| ChiTable beta 3f | 1 | "Row 3" in a mosaic column 8 px wide, drawn as "R" (`csMosaic`) | next round |
| DNAMixLR beta 3e | 1 | a worked line of the mixture formula, "(1×0.000000025 + 1.0000×0.150) / (1 + 3×0.000000025) = 0.1500", past its width | next round |
| EpiStats v1.7e | 1 | "Crude OR = 16796842042.5  (816151920.57-345687972411)" past its width | next round |
| every other program | 0 | | |

All 30 programs in one process ran out of memory at BurrLab (the process was killed and left nothing for the rest); run one program to a process, as below.

## Not labels, seen on the way

The same runs give each program's monkey verdicts. None of these programs has had its own monkey round yet (`monkey-fleet-2026-11-01.md` lists their round-1 findings, a typed list in most); their causes are read in that round. These runs shared the machine with others, and under a busy machine a FREEZE can be a slow run, not a hang (Lessons Learned v7zj), so they are recounted then, run alone:

| Program | Broken runs of 100 |
|---|---|
| EpiStats | 22 HARNESS |
| ErrorRate | 21 HARNESS |
| StudRange | 1 CRASH, 14 FREEZE, 17 HARNESS |
| TrendTest | 14 HARNESS |
| AnovaLab | 8 HARNESS |
| BurrLab | 3 FREEZE, 4 HARNESS |
| ResampLab, SeizureLab | 6 HARNESS each |
| AgreeLab | 5 HARNESS |
| DataLoad | 4 HARNESS (and 5 STATE: its own D1–D9, announced) |
| DNAMixLR | 3 HARNESS |
| SurvLab | 2 HARNESS |
| FitCheck | 1 HARNESS |

## How to rerun

From the repository, `HPKIT` set, on a processor of its own (the monkey's time limit is wall-clock):

```
for n in $(ls programs | sed -E 's/_(beta|v)[0-9].*//' | sort -u); do
  python3 tools/monkey_labels_v1.py 100 $n --out labels_out      # one program to a process: all 30 in one ran out of memory
done
python3 tools/monkey_labels_v1.py 100 Norm3 --out labels_out     # one program
```

Each program's findings are written to `labels_out/<Name>.json`. The runs use seeds 3000, 3001, …; for one finding's coordinates, rerun those seeds one at a time with the recorder on and print the collision (round 4 found PowerViz's SE line at seed 3077, GaltonBoard's peg count at 3005 and its panel at 3000).
