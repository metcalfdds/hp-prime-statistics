# BurrLab beta 1e — changes from beta 1d (29 Oct 2026): the Explore curves in MicroPython

Built from `parts/` (beta 1d's parts in `parts_beta1d/`); `BurrLab_beta1d.txt` untouched (md5
f7dd1e2a4178). Gate PASS vs beta 1d (`gate_BurrLab_beta1e_output.txt`); fleet_names 0/0/0;
case_scan clean over 34 files; `verify_BurrLab_beta1e.py` 3,343 checks, 0 failures (beta 1d's
on the PPL path, which is what the plain harness takes, plus Part I through the bridge).

## The finding recorded (Roger, beta 1d, one Up press on Explore)

G1 "c 757 d 137 w 4 ms", G2 "c 868 d 117 w 2 ms": compute is 85 % of the press, drawing is
cheap (about 130 ms for 146 primitives and three full-screen blits), the key path has no wait,
and **the G2 is not faster than the G1 on this PPL loop**: 3,464 statements in 0.76–0.87 s is
about 4,000–4,600 statements/s on both (the G2's advantage is in the C-coded built-ins and
drawing, not in interpreting PPL). Planning rule from now: PPL loops cost the same on both
calculators, about 4,500 statements/s; only MicroPython or built-ins buy speed.

## What changed

1. **`#PYTHON bul` mode 5**: the Explore curve (the pdf, or the CDF in CDF view) at every pixel
   column with the same one-pass arithmetic as `bu_CachePPL`, turned into pixel rows with the
   same scale rule (1.08 × the pdf's maximum over columns 4..), merged into LINE_P segments by
   the same run rule as `bu_SegPPL`, and handed back one number at a time into `BU_YP`
   (StudRange's `EP_SRCDF` shape; whole numbers, so no formatting risk), with the segment count
   in `BU_OUT(3)`, the scaled y maximum in `BU_OUT(1)` (a capital-E mantissa form that keeps 13
   digits whatever the size), the value at column 10 in `BU_OUT(2)` and the sentinel last.
   `bu_PyCache`: BU_YP cleared to −1 first; the answer checked by the sentinel, a plausible
   count, the last row inside the frame and column 10 against the PPL formula to 1E-9; on any
   failure `bu_CachePPL` (values → rows → segments) answers. Marks in BU_PZ ("finished mode 5").
2. **The cache is the segment list** (`buSeg`, `buNSeg`) for both engines: `bu_Curve` is one
   LINE_P per segment (121 at C = 2, K = 1.5), the tail shade is a SUB of the segment list from
   the x₀ column (binary search) plus the baseline (one FILLPOLY_P; pdf view only — the pdf
   tail under the CDF curve made no sense), the x₀ dot is the exact row at its column
   (`bu_RowAt`). Family and Rare draw from the same cache, so they take the same engine path.
3. **Engine selector respected**: Auto (Python, PPL on failure), PPL only, Python only (a
   failure shows "py FAIL, PPL" in the readout and PPL draws the page — a blank page would be
   worse), Both (both engines, every segment coordinate compared; "py = PPL" or "py-PPL n px").
4. **Readout** now a More-page toggle ("Timing", also in Enter's menu): the footer shortens to
   "K chosen" and the readout sits at its right end, "c 25 d 120 w 2 ms, py". Out of the plot.
5. The in-frame "K×C = …: mean and variance" line is gone (the curve crossed it; status row C
   says it); "capped at 50 S" takes its row.

## Measured (harness statements per redraw; primitives unchanged from beta 1d: 146 / 16)

| Event | beta 1d (PPL) | beta 1e, PPL path | beta 1e, Python answering (PPL statements) |
| --- | --- | --- | --- |
| Explore, C/K/S press | 3,464 | 4,243 (the segment pass) | **693** |
| Explore, x₀ move | 474 | 208 | 208 |
| Family, C/K change | 2,053 | 2,750 | ~700 |
| Rare, x move | 3,455 | 4,124 | ~800 |

Expected on the calculators (4,500 statements/s, bridge crossings about 0.2 ms each, ~500
crossings): c about 0.25–0.35 s with Python, 0.95 s on the PPL path (the fallback is a little
slower than beta 1d because it also builds the segment list; it is the fallback). The
remaining PPL cost with Python answering is the moments (Lanczos log-gamma, 180 statements),
the text rows and the shade.

Verified (Part I): on the 12 shapes the Python segments equal the PPL engine's exactly, the
curve pixels equal beta 1c's, Python's column-10 value equals SciPy's to 1E-9 and its rows
equal SciPy-derived rows (at most 2 rounding-edge columns); the readout names the engine in
all four settings with Python answering and absent; a disagreeing Both run reports the
difference; a wrong column-10 value is refused and PPL answers; the Timing toggle works
through the page loop; Family and Rare caches come from Python.
