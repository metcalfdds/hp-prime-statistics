# BayesTree beta 8j: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes BayesTree beta 8j from BayesTree beta 8i. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1, 2 and 4 reworded: "slot 6", the soft-key pages, the views and the exact answers in plain words.  The help is now 5 pages (was 4).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 5 screens (was 4), as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, bt_HelpView 45.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 5 screens changed; 1 kept their words (1 of them with a new page number).

### Before (beta 8i)

```text
BayesTree help 1/4: The tree
Slide the red knob in the top strip: the prior
  (a log-odds scale, so 0.001 and 0.01 get room).
Drag a branch pair up or down (the grip marks):
  the D+ pair sets sens, the D− pair sets spec.
Tap a box: what that count is, and its formula.
Tap a branch number: what that probability is.
Tap the mosaic: the same test at three priors.
Mosaic: green TP, red FN, orange FP, gray TN.
Leaf bars: share of N (a log stub below 1 %).
Soft keys: More (slot 6) turns to the next page:
  Values Counts ROC PPV 2×2 | Diag Fagan Icons
  3 prev Help | Test2 Reset Forens Leaves Exact.
⇆ = spec, ⇅ = sens, +/- = prior, Ent = menu,
Esc quits BayesTree.
any key or tap = next page, Esc = done
```

```text
BayesTree help 2/4: The views
ROC: tap or drag the curve; sens and spec move
  together (the threshold trade-off); ⇆ too.
PPV vs prevalence: tap or drag = the prior.
Fagan nomogram: prior (left) and LR (center)
  line up with the posterior (right).  Drag the
  left axis.  Magenta LR+ → PPV, blue LR− → 1−NPV.
Second test: test 1's PPV is test 2's prior;
  the root is the T+ people of test 1 (gray).
  (Assumes the tests err independently.)
Reset to one test: back to test 1 alone.
Icon array: 1,000 people, the T+ band first.
Leaves: counts or probabilities (menu).
any key or tap = next page, Esc = done
```

```text
BayesTree help 4/4: Exact answers (CAS)
Between the leaves: PPV and NPV as exact
  fractions from the CAS (1 − PPV if forensic).
  'exact (CAS)': the CAS answered.  'decimal':
  it could not, so the decimal is shown.
The CAS is asked only when you stop -- after a
  key, a lift or a view, never during a drag.
Magenta mark on the slider: the break-even prior,
  where PPV = 1/2.  Left of it (the red track)
  most positive results are false.
Two tests: the mark is the prior BEFORE test 1 at
  which two positives give 1/2: 1/(1 + LR₁ × LR₂).
Tap the fractions or soft key Exact (page 3):
  natural frequencies, Bayes with your numbers,
  and the CAS solving PPV = 1/2 for the prior.
any key or tap = done
```

### After (beta 8j)

```text
BayesTree help 1/5: The tree
Slide the red knob in the top strip: the prior (a log-odds scale, so
  0.001 and 0.01 get room).
Drag a branch pair up or down (the grip marks): the D+ pair sets
  sens, the D− pair sets spec.
Tap a box: what that count is, and its formula.
Tap a branch number: what that probability is.
Tap the mosaic: the same test at three priors.
any key or tap = next page, Esc = done
```

```text
BayesTree help 2/5: The tree (continued)
Mosaic: green TP, red FN, orange FP, gray TN.
Leaf bars: each leaf's share of N (a share below 1 % gets a short
bar on a log scale).
Soft keys: More (the 6th key) shows the next set of keys: Values
  Counts ROC PPV 2×2 | Diag Fagan Icons 3 prev Help | Test2
  Reset Forens Leaves Exact.
⇆ = spec, ⇅ = sens, +/- = prior, Ent = menu, Esc quits
BayesTree.
any key or tap = next page, Esc = done
```

```text
BayesTree help 3/5: The views
ROC: tap or drag the curve; sens and spec move together (the
  threshold trade-off); ⇆ too.
PPV vs prevalence: tap or drag = the prior.
Fagan nomogram: prior (left) and LR (center) line up with the
  posterior (right).  Drag the left axis.  Magenta LR+ → PPV, blue
  LR− → 1−NPV.
Second test: test 1's PPV is test 2's prior; the tree now starts from
  the people who were positive on test 1 (gray). (Assumes the
  tests err independently.)
Reset to one test: back to test 1 alone.
Icon array: 1,000 people, the T+ band first.
Leaves: counts or probabilities (menu).
any key or tap = next page, Esc = done
```

```text
BayesTree help 5/5: Exact answers (CAS)
Between the leaves: PPV and NPV as exact fractions from the CAS
  (1 − PPV if forensic). 'exact (CAS)': the CAS answered.  'decimal':
  it could not, so the decimal is shown.
The CAS is asked only when you stop: after a key press, a finger
  lift, or a change of view; never during a drag.
Magenta mark on the slider: the break-even prior, where
  PPV = 1/2.  Left of it (the red track) most positive results
  are false.
Two tests: the mark is the prior BEFORE test 1 at which two
  positives give 1/2: 1/(1 + LR₁ × LR₂).
Tap the fractions or soft key Exact (page 3): natural frequencies,
  Bayes with your numbers, and the CAS solving PPV = 1/2 for
  the prior.
any key or tap = done
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 8i; lint_ppl 4 problems, as in beta 8i (4); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 5 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
  On the Virtual Calculator all five help pages were opened from the menu and read (`verify/round11/screens/`): every line inside its page, nothing cut.
- `tools/monkey_v1b.py --lists`, 1,000 runs of 120 random keys, taps, menu picks and typed values (790 s): OK 1,000.

Not yet run on a G1 or a G2.
