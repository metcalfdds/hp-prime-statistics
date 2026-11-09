# CICatcher beta 2i: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes CICatcher beta 2i from CICatcher beta 2h. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 to 4 reworded: what 95 % is of, why a higher level widens every line, Wald and Wilson, and the exact interval in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 6 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 7, cqHelp 48.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 6 screens changed; 2 kept their words.

### Before (beta 2h)

```text
CICatcher help 1/6: 95 % of WHAT?
Each line is the interval from ONE sample.
The green line is the truth (μ or p): the
method never sees it. Blue lines caught it,
red lines missed it.
The 95 % is the METHOD'S long-run catch rate,
not a property of any one interval. Keep
adding samples: the 'all' rate in the header
settles near the target.
Any one interval either caught μ or missed it.
So say 'we are 95 % confident' -- meaning the
method catches the truth 95 % of the time --
not 'a 95 % chance μ is in THIS interval'.
any key or tap = next page, Esc = done
```

```text
CICatcher help 2/6: Level and width; z and t
Drag the right edge (or ⇅): a higher level
uses a bigger critical value, so EVERY line
grows, red lines turn blue and the catch rate
rises. 99 % catches more but says less.
z: x̄ ± z × σ/√(n) uses the TRUE σ,
so every z line has the same length.
t: x̄ ± t × s/√(n) uses the sample's s.
s changes from sample to sample, so t lines
differ in length, and t* is bigger than z* to
pay for it: t(9) = 2.262 against z = 1.960.
z with s at n = 10 would catch only 91.8 %.
t critical value: not needed yet (no t run)
any key or tap = next page, Esc = done
```

```text
CICatcher help 3/6: Wald and Wilson
Wald: p̂ ± z × √(p̂(1 - p̂)/n), the
textbook interval. Center and width both
come from p̂, which fails when n × p is small:
at p = 0.10, n = 20 Wald catches only 87.6 %
(exact binomial; it claims 95 %).
12.2 % of those samples have p̂ = 0: the
Wald interval has ZERO width and must miss.
Wilson (score) takes its SE from the p being
tested, not from p̂: never zero width, center
pulled toward 1/2. Same p and n: 95.7 %.
Wald wants n × p and n × (1 - p) of 10 or
more; at p = 0.10, n = 100 it reaches 93.2 %.
Gray on the axis: impossible values (below 0,
above 1). Only Wald lines can reach them.
any key or tap = next page, Esc = done
```

```text
CICatcher help 4/6: Exact intervals
Exact (Clopper-Pearson) uses no normal curve:
it keeps every p under which your count is in
neither tail of Binomial(n, p) holding α/2.
A count has only n + 1 possible values, so no
interval can catch exactly 95 % at every p.
Exact makes sure it is NEVER LESS: at n = 20
its worst case over every p is 95.8 %.
At p = 0.10, n = 20 it catches 98.9 % (Wilson
95.7 %, Wald 87.6 %); at 80 % or 90 % it still
catches 95.7 %. The price: longer lines.
0 yeses: from 0 to 1 - (α/2)^(1/n), 0.168 at
n = 20 and 95 %. Tap such a line: the panel
shows that end as the CAS writes it.
exact ends: bisection on BINOMIAL_CDF, checked
any key or tap = next page, Esc = done
```

### After (beta 2i)

```text
CICatcher help 1/6: 95 % of WHAT?
Each line is the interval from ONE sample.
The green line is the truth (μ or p): the method never sees it. A
blue line caught it (the interval contains it); a red line missed it.
The 95 % is the share of intervals the METHOD catches in the
long run, not a property of any one interval. Keep adding
samples: the 'all' rate at the top of the screen settles near the
confidence level.
Any one interval either caught μ or missed it.
So say 'we are 95 % confident' -- meaning the method catches
the truth 95 % of the time -- not 'a 95 % chance μ is in
THIS interval'.
any key or tap = next page, Esc = done
```

```text
CICatcher help 2/6: Level and width; z and t
Drag the right edge (or ⇅): a higher level uses a bigger critical
value, so EVERY line grows, red lines turn blue and the catch rate
rises. 99 % catches more, but its longer lines give a less
precise answer.
z: x̄ ± z × σ/√(n) uses the TRUE σ, so every z line has the
same length.
t: x̄ ± t × s/√(n) uses the sample's s.
s changes from sample to sample, so t lines differ in length, so
t's critical value is bigger than z's to make up for that:
t(9) = 2.262 against z = 1.960.
z with s at n = 10 would catch only 91.8 %.
t critical value: not needed yet (no t run)
any key or tap = next page, Esc = done
```

```text
CICatcher help 3/6: Wald and Wilson
Wald: p̂ ± z × √(p̂(1 - p̂)/n), the textbook interval. Center and
width both come from p̂, which fails when n × p is small:
at p = 0.10, n = 20 Wald catches only 87.6 % (exact binomial; it
claims 95 %).
12.2 % of those samples have p̂ = 0: the Wald interval has ZERO
width and must miss.
Wilson (score) takes its SE from each possible p, not from p̂,
and keeps every p within z SEs of p̂: never zero width, center
pulled toward 1/2. Same p and n: 95.7 %.
Wald needs n × p and n × (1 - p) to be 10 or more; at p = 0.10,
n = 100 it reaches 93.2 %.
Gray on the axis: impossible values (below 0, above 1). Only
Wald lines can reach them.
any key or tap = next page, Esc = done
```

```text
CICatcher help 4/6: Exact intervals
Exact (Clopper-Pearson) uses no normal curve:
it keeps every p for which your count is not in either α/2 tail of
Binomial(n, p).
A count has only n + 1 possible values, so no interval can catch
exactly 95 % at every p.
Exact makes sure it is NEVER LESS: at n = 20 its worst case over
every p is 95.8 %.
At p = 0.10, n = 20 it catches 98.9 % (Wilson 95.7 %, Wald 87.6
%); at 80 % or 90 % it still catches 95.7 %. The cost: longer lines
(wider intervals).
0 yeses: from 0 to 1 - (α/2)^(1/n), 0.168 at n = 20 and 95 %.
Tap such a line: the panel shows that end as the CAS writes it.
exact ends: bisection on BINOMIAL_CDF, checked
any key or tap = next page, Esc = done
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 2h; lint_ppl 5 problems, as in beta 2h (5); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 6 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
