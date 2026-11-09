# StudRange beta 15m: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes StudRange beta 15m from StudRange beta 15l. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 to 4 reworded: what n is for each method, the infinite df, the journal, the two engines and the drag in plain words.  The help is now 5 pages (was 4).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 5 screens (was 4), as the PC harness counts them. A statistic's name stays on one line: the first layout broke "so q" / "crit = ..."; the wrap now keeps a one-letter symbol with the "crit", "obt" or "obs" after it.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, sr_HelpMode 40.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 5 of 5 screens changed; 0 kept their words.

### Before (beta 15l)

```text
StudRange help 1/4: About StudRange
q = (x̄max - x̄min)/√(MSE/m)
Tukey HSD: n = total k means
Newman-Keuls: n = span of pair
Duncan: N-K q, α* = 1-(1-α)^(n-1)
Unequal n: use Tukey-Kramer
df = 0 → ν = ∞ (plain range dist)
Verified vs Harter 1960 tables
After Dunlap et al. 1977, BRMI 9(4)
Teaching aid; not for legal use.
any key or tap = next, Esc = menu
```

```text
StudRange help 2/4: Why q and not t
Two means (k = 2): q = t·√2 exactly,
so q crit = √2 · t crit (two-sided).
k means make k(k−1)/2 pairs. A t-test
on each at α finds SOME difference
far more often than α: that is the
family-wise error rate. q is the range
(the largest pair), so q > q crit has
chance α for the whole family.
any key or tap = next, Esc = menu
```

```text
StudRange help 3/4: Two engines
MicroPython: the fast path, df ≥ 1
  (a q crit in about 1.5 s on a G2)
PPL: the fallback when Python does
  not answer; df ≥ 3, about a minute
Each result page names its engine.
Diagnostics probes Python live.
Python errors are silent here: test
with the Terminal open (hardware).
any key or tap = next, Esc = menu
```

```text
StudRange help 4/4: The plot
Drag in the plot: q obs (p sweeps)
Drag the right edge: α (CDF height)
Tap the q crit box: q obs = q crit
⇆ = q   ⇅ = α   +/− = k   0 = q crit
Soft keys: α− α+ k− k+ df Menu
Ent = plot menu: H0 sim, k = 2 curve
Menu modes: full precision
Plot: fast grid (curve-level)
any key or tap = menu
```

### After (beta 15m)

```text
StudRange help 1/5: About StudRange
q = (x̄max - x̄min)/√(MSE/m)
Tukey HSD: n = k, the number of means
Newman-Keuls: n = the means from the pair's
lower to its higher, both counted
Duncan: Newman-Keuls's q, at
α* = 1-(1-α)^(n-1)
any key or tap = next, Esc = menu
```

```text
StudRange help 2/5: More about StudRange
Unequal n: use Tukey-Kramer
df = 0 means ν = ∞ (the range itself, σ known)
Checked against Harter's 1960 tables
After Dunlap et al. 1977, Behav Res Meth
Instr 9(4)
Teaching aid; not for legal use.
any key or tap = next, Esc = menu
```

```text
StudRange help 3/5: Why q and not t
Two means (k = 2): q = t·√2 exactly, so
q crit = √2 · t crit (two-sided).
k means make k(k−1)/2 pairs. A t-test on each
at α finds SOME difference far more often
than α: that is the family-wise error rate. q
uses the range (the largest mean minus the
smallest), so q > q crit has chance α for the
whole family of pairs.
any key or tap = next, Esc = menu
```

```text
StudRange help 4/5: Two engines
MicroPython: the fast path, df ≥ 1 (a q crit in
  about 1.5 s on a G2)
PPL: the fallback when Python does not
  answer; df ≥ 3, about a minute
Each result page names its engine.
Diagnostics checks that Python is working.
Python's errors are not shown here; to see
them, run it with the Terminal open, on a
calculator.
any key or tap = next, Esc = menu
```

```text
StudRange help 5/5: The plot
Drag in the plot: move q obs (p changes as
you go)
Drag the right edge: set α (as a height on
the CDF)
Tap the q crit box: q obs = q crit
⇆ = q   ⇅ = α   +/− = k   0 = q crit
Soft keys: α− α+ k− k+ df Menu
Ent = plot menu: H0 sim, k = 2 curve
Menu answers: full precision.  Plot: a faster
grid, close but not exact.
any key or tap = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 15l; lint_ppl 18 problems, as in beta 15l (18); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 5 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
  On the Virtual Calculator all five help pages were opened from the menu and read (`verify/round11/screens/`): every line inside its page, nothing cut.
- `tools/monkey_v1b.py --lists --seconds 240`, 1,000 runs of 120 random keys, taps, menu picks and typed values (3,461 s): OK 1,000.

Not yet run on a G1 or a G2.
