# ErrorRate beta 1j: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes ErrorRate beta 1j from ErrorRate beta 1i. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 2 and 5 to 9 reworded: the plot, the database page, the cautions, the sources and the examples in plain words ("10,000 programs" is now "10,000 examiners").  The help is now 10 pages (was 9).

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is 10 screens (was 9), as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, erlHelp 76.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 7 of 10 screens changed; 3 kept their words (3 of them with a new page number).

### Before (beta 1i)

```text
ErrorRate help 2/9: Reading the main plot
Blue: the chance of a record this good (k
or fewer errors in n) at each true rate.
Orange dashes: α = 0.05.  Where the curve
crosses it (red) is the upper bound.
Green band: rates the record allows.
Red band: rates it rules out (one-sided).
Green dots: the rule-of-three line, 3/n.
Magenta: the rate under your finger, and
the chance of the record at that rate.
Drag along the plot (or ⇆) = the rate.
Drag the right edge = n (⇅ = n + or - 1,
+/- = n up or down a step).
Log y (page 2): the k = 0 curve is a line.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 5/9: Absence of evidence
Sim gives 10,000 examiners the SAME true
rate (the one under your finger), and each
takes n tests.  The bars count their errors;
green bars are records at least as good as
this one (k or fewer errors).
At 5 %, about 2,150 of the 10,000 finish
30 tests with no errors at all.  A clean
record from a small n is weak evidence.
MicroPython runs 10,000.  If it fails, PPL
runs 1,000 and the badge says so.
Each run jumps from one error to the next:
the clean run before an error has a
geometric length, ln(U)/ln(1 - p).
any key or tap = next page, Esc = done
```

```text
ErrorRate help 6/9: Database trawls
Search a database of N profiles for a match
to a crime-scene profile with a random match
probability RMP.  If the source is not in
the database, each profile matches by
chance with probability RMP, so
P(at least one chance match) = 1-(1-RMP)^N.
Expected chance matches: N × RMP.  When
that is 1, P is 63.2 %, not 100 %.
As N grows: P → 1 - e^(-N × RMP) (CAS).
A cold hit from a big database needs more
support than the RMP alone.
RMP values offered are illustrative only.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 7/9: Honest caveats
Proficiency tests are not blind casework:
examiners who know they are being tested
do better (PCAST sec. 4.6, pp. 57-58).
The bound assumes independent tests of
equal difficulty.  Easy or similar items
make it too optimistic.
Count only conclusive answers (PCAST p. 51).
It describes THIS examiner on THESE tests,
not a whole discipline, and not one case.
A false-positive rate needs different-
source tests; a miss rate, same-source ones.
One-sided 95 % is the upper end of a two-
sided 90 % interval, not of a 95 % one.
Change α with the n, k soft key.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 8/9: Keys and touch
Page 1: n, k = set n, k and α; Rate = type
a true rate; Why 3 = the algebra (CAS);
Bayes = the posterior; Sim = simulate.
Page 2: Trawl = database search; Log y;
Help; Eng = engines; Quit.  More = pages.
Drag the plot = rate; drag right edge = n.
⇆ = rate, ⇅ = n + or - 1, +/- = n step,
Ent = menu, Esc = quit.
Bayes: Unif, Jeff, a, b; drag = rate.
Sim: Again, Rate-, Rate+.  Trawl: RMP, N,
Exact; drag or ⇆ = N.
Home after quitting: ER_UPPER, ER_N, ER_K,
ER_ALPHA, ER_RATE, ER_PASS, ER_RULE,
ER_BMEAN, ER_BUPPER, ER_SIM, ER_TRAWL.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 9/9: Three engines
PPL draws every screen, reads every touch
and computes every number that is drawn.
The CAS writes exact text: fractions such
as 1/32, closed forms such as 1-(1/20)^(1/30),
limits such as ln(20).  Its lines carry the
badge 'exact (CAS)'.  If the CAS fails, the
page shows decimals and says 'decimal'.
MicroPython simulates 10,000 programs;
if it fails, PPL simulates 1,000 and the
badge says 'PPL fallback'.
Eng (page 2) checks the CAS and Python
live and says which ran last.
It has run on the Virtual Calculator.
any key or tap = back
```

### After (beta 1j)

```text
ErrorRate help 2/10: Reading the main plot
Blue: the chance of a record this good (k or fewer errors in n) at
each true rate.
Orange dashes: α = 0.05.  Where the curve crosses it (red) is the
upper bound.
Green band: true error rates that fit this record.
Red band: rates it rules out (one-sided).
Green dots: the rule-of-three line, 3/n.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 3/10: Reading the main plot (continued)
Magenta: the rate under your finger, and the chance of the
record at that rate.
Drag along the plot (or ⇆) = the rate.
Drag the right edge = n (⇅ = n + or - 1, +/- = n up or down
a step).
Log y (soft key, page 2): on a log scale the k = 0 curve is a
straight line.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 6/10: Absence of evidence
Sim gives 10,000 examiners the SAME true rate (the one under
your finger), and each takes n tests.  The bars count their errors;
green bars are records at least as good as this one (k or
fewer errors).
At 5 %, about 2,150 of the 10,000 finish 30 tests with no errors
at all.  A clean record from a small n is weak evidence.
MicroPython runs 10,000.  If it fails, PPL runs 1,000 and the
badge says so.
To save time, each simulated examiner skips from one error to
the next: the number of clean tests before an error is geometric,
drawn as ln(U)/ln(1 - p).
any key or tap = next page, Esc = done
```

```text
ErrorRate help 7/10: Database trawls
Search a database of N profiles for a match to a crime-scene
profile with a random match probability RMP.  If the source is
not in the database, each profile matches by chance with
probability RMP, so
P(at least one chance match) = 1-(1-RMP)^N.
Expected chance matches: N × RMP.  When that is 1, P is 63.2
%, not 100 %.
As N grows: P → 1 - e^(-N × RMP) (CAS).
A cold hit (a match found only by searching a database) from a
big database needs more support than the RMP alone.
RMP values offered are illustrative only.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 8/10: Cautions
Proficiency tests are not blind casework:
examiners who know they are being tested do better (PCAST sec.
4.6, pp. 57-58).
The bound assumes independent tests of equal difficulty.  Easy
or similar items make the bound too low (too optimistic).
Count only conclusive answers (PCAST p. 51).
It describes THIS examiner on THESE tests, not a whole
discipline, and not one case.
A false-positive rate needs different-source tests; a miss rate,
same-source ones.
One-sided 95 % is the upper end of a two-sided 90 % interval,
not of a 95 % one.
Change α with the n, k soft key.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 9/10: Keys and touch
Page 1: n, k = set n, k and α; Rate = type a true rate; Why 3 = the
algebra (CAS);
Bayes = the posterior; Sim = simulate.
Page 2: Trawl = database search; Log y;
Help; Eng = engines; Quit.  More shows the other set of
soft keys.
Drag the plot = rate; drag right edge = n.
⇆ = rate, ⇅ = n + or - 1, +/- = n step, Ent = menu, Esc = quit.
Bayes: Unif, Jeff, a, b; drag = rate.
Sim: Again, Rate-, Rate+.  Trawl: RMP, N, Exact; drag or ⇆ = N.
Home after quitting: ER_UPPER, ER_N, ER_K, ER_ALPHA, ER_RATE,
ER_PASS, ER_RULE, ER_BMEAN, ER_BUPPER, ER_SIM, ER_TRAWL.
any key or tap = next page, Esc = done
```

```text
ErrorRate help 10/10: Three engines
PPL draws every screen, reads every touch and computes every
number that is drawn.
The CAS writes exact text: fractions such as 1/32, closed forms
such as 1-(1/20)^(1/30), limits such as ln(20).  Its lines carry
the badge 'exact (CAS)'.  If the CAS fails, the page shows decimals
and says 'decimal'.
MicroPython simulates 10,000 examiners;
if it fails, PPL simulates 1,000 and the badge says 'PPL fallback'.
Eng (page 2) checks that the CAS and Python are working, and
says which one ran last.
It has run on the Virtual Calculator.
any key or tap = back
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 1i; lint_ppl 11 problems, as in beta 1i (11); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 10 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".
- `tools/monkey_v1b.py --lists`, 1,000 runs of 120 random keys, taps, menu picks and typed values (877 s): OK 1,000.

Not yet run on a G1 or a G2.
