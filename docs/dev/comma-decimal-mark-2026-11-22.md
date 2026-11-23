# A comma as Home's decimal mark: what four programs did (22 November 2026)

The book's readers may be in Europe, where most languages write the decimal point as a comma, and a Prime can be set that way: Home Settings, Digit Grouping, 123.456,789 (the list also has 123'456,789, 123 456,789, 123˙456,789 and 123456,789). Until this afternoon no program of the fleet had been run with that setting. Four were run, and none of them was right.

## The calculator

HP's Virtual Calculator 2.4.2 (build 2026-09-09) under Wine in a cloud session (`tools/vc_cloud_v1`), with the program files of starter pack v23 copied into its folder while it was closed. Each run with the comma has a run with 123,456.789 beside it, on the same calculator in the same hour. **Not tried:** a G1, a G2, the Virtual Calculator under Windows, the other 27 programs, and the other four comma styles.

## What was seen

| Setting | What was done | What the calculator did |
| --- | --- | --- |
| comma | Home: `1.5+1` on the keyboard | The line read `1,5+1`; the answer `2,5` |
| comma | Home: `STRING(1234.5678)` | The line read `STRING(1.234,5678)`; the answer `"1234,5678"` |
| period | Home: `Norm3(100,15,130)` | Norm3 started: μ = 100.000, σ = 15.000, x₀ = 130.00, z = 2.00, pdf = 0.0036, P(X ≤ x₀) = 0.9772, P(X > x₀) = 0.0228; the y-axis read 0.01, 0.02, 0.03 |
| comma | Home: the same keys | The line read `Norm3(100;15;130)`, and Norm3 started: μ = 100,000, σ = 15,000, x₀ = 130,00, z = 2,00, **pdf = 0,0,036, P(X ≤ x₀) = 0,9,772, P(X > x₀) = 0,0,228**; the y-axis read ×1,0ᴇ−2 with 1, 2, 3 |
| comma | StatDist v2.7n from the Program Catalog: Common Continuous, Normal, Lower tail; 1234.5, 2.5 and 1236.25 typed | The INPUT form took and showed 1.234,5, 2,5 and 1.236,25. The result page: **μ = 1,234,5, σ = 2,5; f(x) = 0,1,249; P(X ≤ 1,236,25) = 0,758,036**; the x-axis read 1,228 to 1,240 and the y-axis 0,05, 0,10, 0,15 |
| period | StudRange beta 15n, Run | Its menu, as always |
| comma | StudRange beta 15n, Run (twice, in two sessions) | The Virtual Calculator stopped both times, with Wine's box "The program HPPrime.exe has encountered a serious problem and needs to close" |
| period | NormExplorer beta 42j, Run | Its menu, as always |
| comma | NormExplorer beta 42j, Run (once) | The Virtual Calculator stopped in the same way |

## What it means

1. **A program's numbers follow Home's decimal mark.** `STRING` writes a comma when Home does, inside a running program too, and the pragma line makes no difference to that: Norm3 and StatDist both begin with `#pragma mode( separator(.,;) integer(h32) )`. The line settles how the program's own text is read. It does not settle how the program writes a number.
2. **So the comma routine goes wrong.** Every program's `<prefix>Cm` (`tools/comma_helper_reference_v1.txt`) takes a run of four or more digits for a whole number unless a period stands before it. After a decimal comma the decimals are such a run, and they get a comma of their own: 0,9772 becomes 0,9,772. The arithmetic is right (0.758036 is Φ(0.7)); the number is written wrongly. A whole number of 1,000 or more still gets the routine's comma (1,228), which a reader who writes a decimal comma reads as one and a bit. Anything else in a program that looks for a period in a number's text (a routine that strips trailing zeros, an axis label) is open to the same fault: Norm3's y-axis changed its form.
3. **The two programs without the pragma line do not start.** 29 of the 31 programs begin with the line; NormExplorer beta 42j and StudRange beta 15n do not (`grep -L "^#pragma mode" programs/*.txt`). Both started with the period and both stopped the calculator with the comma. What a real calculator does then was not seen.
4. **A typed line needs no other keys**: with the comma setting the same keys give `Norm3(100;15;130)` and `1,5+1`.

## A slip in the test

The first run of StatDist "with the comma" showed periods everywhere, and it was a run with the period: the step that sets the digit grouping had been called from the Program Catalog, where its tap opened a program's editor, so the setting had not changed. The capture of the settings page showed it. Every run in the table was made after a capture that shows the setting. And `ChiTable()` typed in Home gave "Error: Syntax Error" with either setting, so that message says nothing about the comma (`Norm3(100,15,130)` typed in Home ran); why ChiTable's typed name was refused was not looked into.

## What was done, and what was not

- The book (Draft 69, "Setting up your calculator") asks every reader to choose 123,456.789 while working with the book and the programs, and says why.
- Lessons Learned v7zy has the finding, and `tools/prime_facts_v1.py` records it as fact 5. The harness is not patched: it has no Home setting for the mark and always writes a period, so no verify script and no monkey run says anything about a calculator set to a comma.
- **Not done, and the author's to decide.** Two ways to make the programs right were thought of and neither was tried: (a) each program sets Home's mark to the period when it starts and puts the reader's own mark back when it ends (the Home variable `HSeparator`; every way out of the program must put it back), so that every screen looks like the book on every calculator; (b) the comma routine, and the other places that look for a period, learn to look for Home's mark. Either is a change to all 31 programs with their verify scripts, a new starter pack and a new Prime Loader, and it needs a calculator set to a comma to be called tested. The pragma line for NormExplorer and StudRange is one line in each, with the same train behind it.
