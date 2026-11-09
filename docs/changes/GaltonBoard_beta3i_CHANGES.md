# GaltonBoard beta 3i: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes GaltonBoard beta 3i from GaltonBoard beta 3h. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 2 and 3 reworded: what a bin is, the keys and the exact answers in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 3 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, gbHelp 32.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 3 of 3 screens changed; 0 kept their words.

### Before (beta 3h)

```text
GaltonBoard help 1/3: Reading the Galton board
Each ball makes R left/right choices, going
right with probability p.  Its bin is the
count of rights, so bins are Binomial(R, p):
P(k) = C(R,k) p^k (1-p)^(R-k),  mean Rp,
SD = √(Rp(1-p)).  Magenta squares: n P(k).
The BELL comes from the number of ROWS: each
bin is a sum of R small left/right steps, and
a sum of many steps is nearly normal (de
Moivre-Laplace).  Sweep rows 3 to 12 (up key).
More BALLS do not make a bell: they only make
the blue bars match the magenta squares, and
x̄ and s settle toward Rp and √(Rp(1-p)).
Green area: the normal curve; gray when Rp or
R(1-p) < 5 (the approximation is poor there).
Any key or tap: keys and touch
```

```text
GaltonBoard help 2/3: Keys and touch
Soft keys: Drop = one ball, watch it fall;
×10 = ten in the air; ×100 = fast, no animation;
Pour = a stream (tap again to stop); Rows; Menu.
Hold a finger on the funnel: pour; lift = stop.
Drag sideways over the pegs: p follows your
finger; lift = a new board (the counts clear).
Tap a bar: P(k) and the normal area k-0.5 to
k+0.5.  Tap it again: every path to that bin,
C(R,k) of them (R up to 8).
Keys: - = 1, + = 100, 0 = pour, arrows = p and
rows (both clear), Ent = menu, Esc = quit.
Menu: Pascal's triangle, SD colors, and
MicroPython (the board holds 5,000 balls).
Any key or tap: exact answers (page 3)
```

```text
GaltonBoard help 3/3: Exact answers (CAS)
Tap a bar: P(k) as an EXACT fraction, worked
out by the calculator's CAS: with p = 1/2,
P(k) = C(R,k)/2^R, so 8 rows, bin 4 = 70/256
= 35/128.  p = 0.3 is used as 3/10.
Menu > Where Poisson comes from: keep μ = Rp
fixed and add rows; p = μ/R shrinks and the
binomial bars close in on the Poisson.  The CAS
takes the limit for your k and gets
μ^k e^(-μ)/k!: the Poisson formula, derived.
Arrows or a tap on a bar pick k.
Badge 'exact (CAS)': the CAS worked it out.
'decimal': it could not, or p is not a simple
fraction; the program's own decimal is shown.
Any key or tap to go back
```

### After (beta 3i)

```text
GaltonBoard help 1/3: Reading the Galton board
Each ball makes R left/right choices, going right with probability
p.  Its bin is the count of rights, so bins are Binomial(R, p):
P(k) = C(R,k) p^k (1-p)^(R-k),  mean Rp, SD = √(Rp(1-p)).
Magenta squares: n P(k).
The BELL comes from the number of ROWS: each bin is a sum of
R small left/right steps, and a sum of many steps is nearly
normal (de Moivre-Laplace).  Try rows 3 to 12 (the Up key).
More BALLS do not make a bell: they only make the blue bars
match the magenta squares, and x̄ and s settle toward Rp and
√(Rp(1-p)).
Green area: the normal curve; gray when Rp or R(1-p) < 5 (the
approximation is poor there).
Any key or tap: keys and touch
```

```text
GaltonBoard help 2/3: Keys and touch
Soft keys: Drop = one ball, watch it fall;
×10 = ten balls at once; ×100 = fast, no animation;
Pour = a stream (tap again to stop); Rows; Menu.
Hold a finger on the funnel: pour; lift = stop.
Drag sideways over the pegs: p changes with your finger; lifting
it starts a new board (the counts are cleared).
Tap a bar: P(k) and the normal area k-0.5 to k+0.5.  Tap it again:
every path to that bin, C(R,k) of them (R up to 8).
Keys: - = one ball, + = 100 balls, 0 = pour, arrows = p and rows
(both clear), Ent = menu, Esc = quit.
Menu: Pascal's triangle, SD colors, and MicroPython (the board
holds 5,000 balls).
Any key or tap: exact answers (page 3)
```

```text
GaltonBoard help 3/3: Exact answers (CAS)
Tap a bar: P(k) as an EXACT fraction, worked out by the
calculator's CAS: with p = 1/2, P(k) = C(R,k)/2^R, so 8 rows, bin
4 = 70/256 = 35/128.  p = 0.3 is used as 3/10.
Menu > Where Poisson comes from: keep μ = Rp fixed and add
rows; p = μ/R shrinks and the binomial bars come closer and
closer to the Poisson.  The CAS takes the limit for your k and
gets μ^k e^(-μ)/k!: the Poisson formula, derived.
Arrows or a tap on a bar pick k.
Badge 'exact (CAS)': the CAS worked it out.
'decimal': it could not, or p is not a simple fraction; the
program's own decimal is shown.
Any key or tap to go back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 3h; lint_ppl 16 problems, as in beta 3h (16); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 3 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
