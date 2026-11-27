# Appendix F. For HP programmers

*From* Statisticles, *Draft 105 (26 November 2026), by Roger D. Metcalf, written with Claude (Anthropic). In Draft 106, the refocus of 26 November 2026, this appendix left the book, and the author sent it here: "The programming part can go to GitHub and a future website." It is kept as Draft 105 printed it, so its cross-references (a chapter, Appendix E, Appendix G, a figure) are Draft 105's, not the current draft's; its history of PPL and its Chart Gallery are in the current draft's Appendix E, "Hewlett-Packard calculators, from the HP-35 to the Prime". The works it cites are listed at the end. Licensed CC BY-NC-SA 4.0, like the book.*


This appendix is for readers who write programs for the HP Prime themselves. If that's you, welcome: much of what follows is what we wish someone had told us when we started. Our *Statisticles* were written to teach statistics, but writing them meant working out a great deal about how the Prime actually behaves in the real world, and much of that is not in HP's manuals. What we worked out is collected here, and in much more detail in the book's GitHub repository, so that other programmers can use it. Our *Statisticles* are free for educational and personal use under their own license (`LICENSE.txt` in the repository): keep the author's notice with any file you pass on, give credit when you build on a program, and just don't sell our *Statisticles* or make one of them part of a product for sale.

## PPL, and the HP languages before it

PPL, the HP Prime Programming Language, will look familiar to anyone who has programmed before, because it is a little bit like several older languages at once. PPL is a little bit like BASIC, because `PRINT` and `INPUT` do what their names say, and a few lines typed into the Prime's editor already make a working program. PPL is somewhat like Pascal, because the body of every routine stands between `BEGIN` and `END`, the statements are separated by semicolons, and `:=` stores a value in a variable (HP Development Company, 2017, p. 596). PPL is somewhat like Python, too, because a `LOCAL` variable has no type of its own and simply takes whatever it is given, whether that is a number, a list, or a string.

The Prime even has MicroPython on board, and has had since 2021, so a program can be written in PPL, in Python, or in some of each, as five of our *Statisticles* are. There is a little bit of Forth, a language of the 1970s that keeps its numbers on a stack (a pile of numbers in which the last number put on is the first one taken off), in the family as well, and the story of Hewlett-Packard's earlier languages tells you where.

That story begins with no language at all. A program for Hewlett-Packard's first calculators was simply a list of the keys that you would otherwise have pressed by hand. The company's first calculator, the HP 9100A of 1968, which sat on a desk (Appendix E), held a program of 196 key presses and read its programs from magnetic cards, and the HP 9100A worked in RPN (Reverse Polish Notation), with a stack of three numbers, named X, Y, and Z, shown on its screen ([The Museum of HP Calculators, n.d.-c](https://hpmuseum.org/hp9100.htm)).

RPN is named in honor of the Polish logician Jan Łukasiewicz, who worked out in the 1920s how to write an expression with no parentheses at all, by putting each operation before or after the numbers it works on. Hewlett-Packard put the operation after the numbers, so you key in the numbers first and then press the key that tells the calculator what to do with them, and the numbers wait on the stack until they are needed ([The Museum of HP Calculators, n.d.-g](https://hpmuseum.org/rpn.htm)). The HP-35 of 1972 put RPN into a shirt pocket, with a stack of four numbers, X, Y, Z, and T ([The Museum of HP Calculators, n.d.-e](https://hpmuseum.org/timeline.htm); [The Museum of HP Calculators, n.d.-g](https://hpmuseum.org/rpn.htm)). The Museum of HP Calculators explains why RPN suited the pocket calculator of that day: the technology did not yet allow a pocket calculator to work through parentheses and the order of operations the way algebra is written, and with RPN and its stack a pocket calculator could still evaluate any expression ([The Museum of HP Calculators, n.d.-g](https://hpmuseum.org/rpn.htm)).

The HP-65 of 1974 was programmed as the HP 9100A had been. A program for the HP-65, of up to 100 lines, was a list of key presses, shown in the display as the codes of the keys, and labels, two flags (switches that a program can set and then test), and four tests let a program make decisions ([The Museum of HP Calculators, n.d.-a](https://www.hpmuseum.org/hp65.htm)).

The bigger machines on the desk were the first to be given languages with words in them. The HP 9820A of 1972 was Hewlett-Packard's first algebraic calculator, on which you typed an expression the way it is written on paper, parentheses and all, and you wrote programs in a simple high-level language, with statements such as `PRT` to print and `GTO` to go to another line ([The Museum of HP Calculators, n.d.-i](https://hpmuseum.org/hp9820.htm)). One mark of that language is still on the Prime: the HP 9820A stored a result with an arrow that points from the value to the variable, as in `2+4A→C`, and PPL still has that arrow, written `▶`, beside its `:=` ([The Museum of HP Calculators, n.d.-i](https://hpmuseum.org/hp9820.htm); HP Development Company, 2017, p. 613). In the same year the HP 9830 became the first of the company's calculators to be programmed in BASIC, and the first with a keyboard laid out like a typewriter's ([The Museum of HP Calculators, n.d.-e](https://hpmuseum.org/timeline.htm)). In 1976 the HP 9825 replaced the HP 9820A and brought a new language named HPL, which kept the algebraic statements of the HP 9820A, added arrays, strings, and `for` loops, and could be set up to control laboratory instruments ([The Museum of HP Calculators, n.d.-j](https://hpmuseum.org/hp9825.htm)).

BASIC then moved from the desk into the hand, in machines that Hewlett-Packard called handheld computers. The HP-71B of 1984 had BASIC built in, and Hewlett-Packard sold a plug-in module for the HP-71B that added a second language, Forth, together with an assembler and an editor, so that Forth and BASIC ran side by side in one small machine ([The Museum of HP Calculators, n.d.-k](https://hpmuseum.org/hp71.htm); Miller, 1984).

For the very powerful calculators that Hewlett-Packard was designing in the 1980s, the company wanted a new language. The company looked at the languages that already existed, BASIC among them, and judged that none of them suited a machine that fits in a pocket, and so, in the words of the Museum of HP Calculators, HP "combined elements of RPN, Lisp and Forth" and called the result Reverse Polish Lisp, or RPL ([The Museum of HP Calculators, n.d.-h](https://hpmuseum.org/rpl.htm)). From Forth, RPL took a stack with no fixed number of levels and the way its code is run, and from Lisp, a much older language in which a program is itself a piece of data, it took the idea of objects, so that a number, a formula, and a program are all objects that can sit on the stack. An RPL program is written between a pair of double angle brackets, with words such as `IF`, `THEN`, `ELSE`, `FOR`, and `NEXT` inside it, and it is entered, stored, and edited like any other object ([The Museum of HP Calculators, n.d.-h](https://hpmuseum.org/rpl.htm)).

The HP-18C of 1986 was the first calculator whose own software was written in RPL, although only Hewlett-Packard's programmers could use the language there, and the HP-28C of 1987 was the first to put RPL in its owner's hands ([The Museum of HP Calculators, n.d.-e](https://hpmuseum.org/timeline.htm); [The Museum of HP Calculators, n.d.-h](https://hpmuseum.org/rpl.htm)). The HP 48 calculators that followed, the HP 48SX of Appendix E among them, were RPL machines too ([The Museum of HP Calculators, n.d.-h](https://hpmuseum.org/rpl.htm)).

The calculator that Hewlett-Packard built for classrooms in the mid-1990s, the HP 38G of Appendix E, went another way. The HP 38G took its equations in algebraic form instead of RPN, although it was built on the software of the HP 48G, an RPL calculator, and its owners wrote programs with commands for branching, for loops, and for prompts (Beers et al., 1996, pp. 1, 18; [The Museum of HP Calculators, n.d.-h](https://hpmuseum.org/rpl.htm)). The Prime followed the HP 38G's way, just as it kept the names of the HP 38G's aplets (Appendix E). The Prime's language, which HP's user guide calls the HP Prime Programming Language, or HP PPL, writes every expression algebraically (HP Development Company, 2017, p. 596).

RPN has not gone away, though. The Prime offers three ways of typing in Home view, which are textbook, algebraic, and RPN (the three choices of the Entry setting that "Setting up your calculator" in How to use this book describes), and when RPN is chosen the numbers go onto a stack ahead of the operation that uses them, much as they did on the HP-35, and much as they do in Forth (HP Development Company, 2017, pp. 38–41). So the Prime of today carries something from every stage of this history: the stack of 1972, the store arrow of the desktop machines, an algebraic language that is somewhat like Pascal and a little bit like BASIC, and Python beside it.

## Where everything is

Everything is in [the repository](<https://github.com/metcalfdds/hp-prime-statistics>), https://github.com/metcalfdds/hp-prime-statistics:

- `programs/` holds our *Statisticles* as plain text files, ready to paste into HP's Connectivity Kit. The starter pack in `starter-pack/` holds the same programs as calculator files.
- `docs/changes/` holds a note for every version of every program: what changed and why, the checks it passed, and what to look at on a real calculator.
- `docs/` also holds the Lessons Learned, everything we found out about the Prime, each finding with its date and the calculator it was seen on (a G1, a G2, or the Virtual Calculator), and a short version of it written for an AI assistant, which the next section explains.
- `templates/` holds TouchKit, a starting point for a new program with the touch and key handling described below already in place: a wait for a key or a tap, soft keys with "More" pages, hit boxes, and a bar chart you can drag.
- `diagnostics/` holds short programs that find out what your own calculator does, and `tools/` and `verify/` hold the checks that every program passed (both are described at the end of this appendix).

## Writing PPL with an AI assistant

An AI assistant can be a great help in writing PPL, but only if it knows how the Prime really behaves, because PPL looks a little like Python and BASIC and follows rules of its own, and an assistant that has not been told those rules will write what would work in the languages it knows better. The assistant may write `a != b` for "a is not equal to b," for example, and the Prime reads that as a factorial followed by a test, so the line quietly does something else (PPL's "not equal" is `<>`, and three of our own *Statisticles*, BayesTree, Norm3, and StatDist, once carried that very mistake, which their current versions no longer have). The assistant may also put a `LOCAL` declaration inside an `IF` or a `CASE`, or call a routine with more than 16 arguments, and the Prime refuses both (the list "Names and syntax," later in this appendix, has these rules and others like them).

Mistakes of that kind are why we wrote down everything we learned, and the repository's `docs/` folder holds it in two forms for you to give your assistant before you ask it for any code. The Lessons Learned is the whole record, about 60,000 words, with the date of each finding, the calculator it was seen on, and how it was checked, and an assistant that can read a long document can take all of it at once. `docs/ppl-rules-for-any-assistant.md` is the short version, about 4,000 words of the same rules without their history, ending with a small program that passes our gate (the set of automatic checks that every one of our programs had to pass before it went onto a calculator), and it is meant for an assistant with a smaller context window, which is the amount of text that an assistant can keep in view at one time, such as a model running on your own computer. The short version carries its own directions: put the whole file in the assistant's system prompt, allow a context of at least 32,768 tokens, ask for one small program at a time, and ask the assistant to imitate the example at the end.

Then check whatever the assistant gives you, the same way we checked our *Statisticles*. Run the gate on the code (`tools/ppl_gate_v1e.py`, described under "How we tested," near the end of this appendix; `tools/README.md` explains how to set it up), paste any lines it reports back to the assistant, and ask the assistant to fix them. After that, run the program on the Virtual Calculator, and on a real calculator if you have one, because a program can pass the gate and still do the wrong thing, and only the calculator can show you that the program works. We wrote both documents with Claude Code, Anthropic's coding assistant, and they read best there; they are meant to help any assistant, but we have not yet tried them with another one, so we would be glad to hear how they work with yours, on the repository's Issues page.

## Chart Gallery: what the Prime can draw

Every picture in Figure F.1 is a screen of one of our *Statisticles*, captured from the Virtual Calculator: the calculator's own firmware drew every one of them, in PPL, with the commands this appendix describes. Each screen also appears, larger and with its numbers explained, in the chapter or appendix that uses the program. The gallery is here to show off what the Prime's screen can do. As far as we are aware, no one else has produced statistical graphics like these on an HP calculator.

Pictures like these have ancestors in the handbooks. Jahnke and Emde, in their *Tables of Functions* (Appendix E), drew functions as surfaces by hand (Jahnke & Emde, 1945), as BiNorm3D and TDist3D do now. Abramowitz and Stegun printed charts of the bivariate normal distribution (Abramowitz & Stegun, 1964). The *Handbook of Data Visualization* has a chapter on mosaic plots like ChiTable's (Hofmann, 2008), and the *Handbook of Graphical Models* has one on Bayesian networks for forensic evidence and DNA mixtures (Dawid & Mortera, 2019), the ground of BayesTree and DNAMixLR.

![Figure F.1. Twelve screens, each drawn in PPL. Top row: BiNorm3D's bivariate normal surface, which turns under a finger; TDist3D's surface of Student's *t*; ChiTable's mosaic of a two-way table; SurvLab's Kaplan–Meier curves with their confidence bands. Middle row: PowerViz's two curves with α, β, and power shaded; BayesTree's tree of counts; GaltonBoard's piles of balls beside the binomial's expected counts; StatDist's gallery of distribution families. Bottom row: AnovaLab's dots for six groups, with each group's mean and interval; RiskLab's ROC curve; AgreeLab's tiles for two raters; ScatterLab's two 95% bands around its least-squares line.](img/gallery_F_12.png)

## Where to find a feature

To see how one kind of thing is done, start with these programs. The table after this list tells you what else is in each one.

- **3-D plots you rotate with a finger:** BiNorm3D (the bivariate normal surface, a wireframe drawn with `LINE_P` alone) and TDist3D (Student's *t* as one surface over *t* and the degrees of freedom, computed once, so that each new frame of the turning picture only has to be drawn, not computed again). TDist3D is the calculator's version of the author's Maple plot in Figure 9.3; the Maple worksheet, and a plain-text transcription of it, are in the repository's `extras/maple/`.
- **Animation:** GaltonBoard (balls poured at a pace set by the clock) and ResampLab (permutation tests and the bootstrap you can watch). BurrLab shows a progress bar and a blinking hourglass during a long fit.
- **Dragging:** ChiTable (an observed bar, with the expected bars following), CICatcher (the confidence level), PowerViz (the shaded regions), ScatterLab (points added, dragged, and deleted), ExhibitLab (an operating-characteristic curve), RiskLab (an ROC cut-off), AgreeLab, Norm3, SampDist, TrendTest, and BayesTree, whose tree and mosaic re-flow as you drag.
- **Tapping:** TestChooser (a flowchart whose path draws itself to a test), AnovaLab (two groups to compare), EpiStats (a stratum dropped from the forest plot), RankLab (a rank strip), SurvLab (a cursor that reads *S*(*t*)), and Norm3 (the S-curve, for the inverse).
- **Soft keys and menus:** ChiTable (soft keys in a `GETKEY`-and-`MOUSE` loop, checked on a G1 and a G2), NormExplorer ("More" pages of soft keys), and the TouchKit template.
- **MicroPython:** StudRange (with a PPL fallback and a badge that says which one ran), BurrLab (the same fit in PPL and in MicroPython, timed side by side), NormExplorer (a sampler with a PPL fallback), ErrorRate (a simulation of 10,000 proficiency programs), and GaltonBoard (5,000 balls).
- **The CAS:** ChiTable (Fisher's *p* as an exact fraction), PowerViz (solving for *n*), and ErrorRate (the rule of three as a limit).
- **Keeping 12 digits** (the Prime keeps 12 significant digits, so a calculation has to be arranged so that it does not lose them): DNAMixLR and TrendTest (sums of positive terms), StatDist (right tails, and its own incomplete gamma and beta functions), StudRange (a change of variable), ChiTable (an exact test counted in logarithms), NormExplorer (the sums of *z* sent across the bridge between Python and PPL), and TTestLab (a cap on *N*).
- **Statistics written in PPL:** FitCheck (Shapiro–Wilk, Anderson–Darling, and Lilliefors), AnovaLab (two-way ANOVA, Type III), RiskLab (logistic regression), SurvLab (Kaplan–Meier), RankLab (exact null distributions), and StatDist (27 distributions).
- **Numerical integration:** AnovaLab (Dunnett's test, by Gauss–Legendre quadrature, with the nodes written into the program by its build script), CICatcher (the exact multiplier of a tolerance interval), FitCheck (Dixon's ratio, a double integral), BiNorm3D (the circular error probable), and StudRange (the studentized range).
- **Home, apps, and data:** CentralLimit (written as an app), EpiStats and Norm3 (called with arguments), ExhibitLab (results left in Home variables), and DataLoad (matrix files spread into lists).
- **Text on the screen:** BayesTree (a line of mixed pieces placed with the *x* that `TEXTOUT_P` returns) and AgreeLab (a d̄ drawn as a d with a bar over it; "Symbols and special characters," below, has the routine).

## What is in each program

The table below gives, for each program, the things in it that another programmer may want to look at or borrow. The number of lines is that of the version in this book.

| Program | Lines | Worth a look |
|-----------|------|------------------------------------------|
| AgreeLab | 3,081 | A table of tiles you drag a count between; a d̄ drawn as a d with a bar over it, because the font has no such letter |
| AnovaLab | 4,756 | Tap two groups to compare them; two-way ANOVA for unbalanced designs (Type III); reads every D list that holds data; Dunnett's test by quadrature, with a page that asks before a long computation |
| BayesTree | 3,458 | A tree and a mosaic that re-flow as you drag; a line of mixed pieces laid out with the *x* that `TEXTOUT_P` returns; old taps under `WAIT(-1)` told apart from new ones by the time they arrive |
| BiNorm3D | 1,618 | A wireframe surface you turn with a finger, drawn with `LINE_P` (the 3-D mesh of `TRIANGLE_P` drew nothing for us); a target view that fires random shots and counts those inside a circle |
| BurrLab | 4,728 | A maximum-likelihood fit in PPL or MicroPython, timed side by side; a progress bar, a blinking hourglass, and Esc for anything long; a curve computed at every third pixel column |
| CentralLimit | 2,796 | Written as an app, not a program, with the app's own `START` and `Plot` hooks; the idea comes from Colin Croft's HP 39G aplet |
| ChiTable | 3,870 | Soft keys in a `GETKEY`-and-`MOUSE` loop, checked on a G1 and a G2; drag an observed bar and the expected bars follow; an exact test counted in logarithms; Fisher's *p* as an exact fraction from the CAS |
| CICatcher | 2,496 | Drag the confidence level, and fifty intervals rescale exactly, without new samples; the exact multiplier of a tolerance interval by integration |
| DataLoad | 1,101 | Reads the matrix files M1 to M9 and spreads their columns into the lists D1 to D9 or C1 to C9; offers to clear lists left from an earlier load |
| DNAMixLR | 3,478 | Probabilities built from sums of positive terms, because an alternating sum (one whose terms are added and subtracted by turns) loses its 12 digits when its large terms cancel |
| EpiStats | 6,293 | The longest program; `EpiStats2x2(a, b, c, d)` can be called from Home; a forest plot in which a tap drops a stratum |
| ErrorRate | 2,864 | A MicroPython simulation of 10,000 proficiency programs; the rule of three shown as the limit it is, worked out by the CAS |
| ExhibitLab | 2,910 | Leaves its results in Home variables (`EX_N`, `EX_P`, and others) for use after it ends; an operating-characteristic curve you drag |
| FitCheck | 3,913 | The Shapiro–Wilk, Anderson–Darling, and Lilliefors tests, and a Q–Q plot, in PPL; the *p*-value of Dixon's ratio as a double integral |
| GaltonBoard | 2,540 | Animation paced by the clock (`TICKS`); hold a finger on the funnel to pour; balls drawn as bars of `RECT_P`, because rings of `ARC_P` leave holes; 5,000 balls in MicroPython |
| Norm3 | 1,132 | Takes arguments, so the Program Catalog asks for them; drag *x*₀; tap the S-curve for the inverse |
| NormExplorer | 4,238 | A live explorer with "More" pages of soft keys; a MicroPython sampler with a PPL fallback; the sums of standard-normal *z* sent across the bridge, so that the standard deviation keeps its digits |
| PowerViz | 4,203 | The α, β, and power regions reshaded live during a drag; the CAS solves for *n*, with the equation written so that the CAS keeps the right root |
| RankLab | 5,107 | Exact null distributions drawn with the observed value marked; a rank strip you can tap; a sequence drawn as squares, one color for each run |
| ResampLab | 3,067 | Permutation tests and the bootstrap you can watch, ×10 to ×1,000; exact enumeration when the count is small enough |
| RiskLab | 3,176 | Logistic regression with up to four predictors; an ROC curve with a draggable cut-off and a live 2 × 2 table |
| SampDist | 1,946 | The nearer bound follows the finger; where we found that a stepped loop can stall in 12 digits |
| ScatterLab | 2,742 | Add, drag, and delete points with a finger, and least squares follows; where we found that a trailing-zero stripper must look for the decimal point first |
| StatDist | 5,111 | 27 distributions; its own incomplete gamma and beta functions for fractional degrees of freedom; right tails that keep their digits; a window that cannot overflow |
| StudRange | 2,767 | MicroPython does the arithmetic and PPL is the fallback, with a badge that says which one ran (about 1.5 seconds on a G2, compared with about a minute in PPL); a quadrature made accurate by a change of variable |
| SurvLab | 2,755 | Kaplan–Meier curves with a finger cursor that reads *S*(*t*) |
| TDist3D | 1,179 | A surface computed once, so that each new frame only has to be drawn, not computed again; turned with a finger |
| TestChooser | 1,928 | A tappable flowchart whose path draws itself to a test |
| TrendTest | 2,303 | Drag a dot; the upper tail of χ² as a finite sum of positive terms |
| TTestLab | 2,228 | Five steps, a screen each, for six tests; the three newest tests were added as routines of their own beside the old ones; number fields that refuse a typed list (`{name,[0]}`); *N* capped so that `STUDENT_CDF` keeps its digits |
| TTestLabG | 2,196 | Made from TTestLab by a script of exact replacements, with its own name, so that both can sit on one calculator |

## How our Sudoku works inside

Our Sudoku, the bonus program of Appendix G, is not one of our *Statisticles*, but a puzzle program brings problems of its own, and the way the program solves them may interest another programmer. Sudoku beta 2a is 1,961 lines of PPL.

- **The solver.** Before every move, the solver looks for the tightest spot on the board: an empty square in which the fewest digits fit, or a row, a column, or a box in which some missing digit fits in the fewest squares. When only one choice is left, the move is forced, and the solver makes the move; when no choice is left, an earlier guess was wrong, so the solver takes back its last guess and tries that guess's next digit, which is called backtracking. The counts of which digits still fit where are kept up to date as each digit goes in or comes out (`suEPut` and `suETake`), so the solver never has to count the whole board again. On a hard puzzle the search can run for a long time, so every 250 steps it shows how many steps it has taken, and **Esc** stops it; in Watch, where every step is painted, any key or tap skips to the end.
- **How the puzzles were made.** The 24 puzzles were made on a PC by a Python program, `su_gen.py`. A full grid is filled at random, and then clues are taken away in pairs, from squares placed symmetrically about the center, for as long as the puzzle still has exactly one answer. Each puzzle was graded by the kind of reasoning that it needs, by the Prime's own solver copied line for line into Python: an Easy puzzle needs only squares in which one digit fits, a Medium puzzle also needs, at least five times, a digit that fits in only one square of a row, a column, or a box, a Hard puzzle needs guesses, with at most 30 of them taken back, and an Expert puzzle more than 30. Each level's clues were also kept within a range of their own (36 to 40 for Easy, 28 to 34 for Medium, 24 to 28 for Hard, and 26 or fewer for Expert), and the one answer of every puzzle was confirmed by a second, plain backtracking count.
- **The shuffle.** The digits are renamed by the Fisher–Yates shuffle in the form that computers use: from the last place down to the second, each place swaps with a place chosen at random from the places at or before it.
- **The touch screen.** The board's squares are 24 pixels wide, the digit pad is at the right, and the soft keys are read only as clicks on the menu strip (as "What we learned about the calculator" explains below). The pencil marks are tiny digits drawn from 37 short strokes, each digit three pixels wide and five tall.
- **Tables that are computed, never typed.** A build script writes the 27 rows, columns, and boxes, each square's 20 neighbors, the 24 puzzles and their answers, the strokes of the pencil marks, and the help pages, which are wrapped at the letter widths measured on the Virtual Calculator, so nothing in those tables was typed by hand.
- **My games.** Each finished game is kept in five lists that stay with the program between runs. The plot's axes step by round numbers (1, 2, or 5 times a power of ten), the least-squares line and *r* come from the deviations from the means, worked out in a second pass, and the copy into C1 to C5 of *Statistics 2Var* reaches each column inside `IFERR`, because a column does not exist until that app has been opened once.
- **How it was tested.** In the PC harness (described under "How we tested" below), Sudoku beta 2a passed 161 checks of what it draws and does, including what happens when a dialog is cancelled, 1,000 runs of random keys and taps, and 300 more runs that began on the My games page with 13 games on it. On the Virtual Calculator, on 26 November 2026, Sudoku passed Check, and an Easy puzzle was finished with Hint, kept as game 1 of My games, plotted, and copied into *Statistics 2Var*; its first runs on a G1 and a G2 are still to come.

## What we learned about the calculator

Each of these is in the Lessons Learned, with the program that found it and how it was checked.

**Names and syntax**

- All programs share one pool of routine names, matched ignoring case, and a helper that is not `EXPORT`ed is still in the pool. Two programs with a helper of the same name can run each other's code. Give every helper the program's tag (`csGrid`, `sr_NiceNum`); `tools/fleet_names_v2.py` finds clashes in a folder of programs.
- Built-in names are matched ignoring case, too: `LOCAL csC` is a syntax error, because `csC` is `CSC`, the cosecant.
- `!=` does not mean "not equal" on the Prime: it is a factorial followed by a test, so write `<>` instead.
- A `//` comment inside an open bracket is a syntax error, so put the comment on a line of its own above the statement.
- A function takes at most 16 arguments. We keep `LOCAL` to six names a line, and a `LOCAL` inside `IF` or `CASE` is rejected.
- `{name,[0]}` makes an `INPUT` field take numbers only; a plain name accepts a list typed into it.

**Numbers and text**

- The Prime keeps 12 significant digits. Once a tail probability is below about $5 \times 10^{-13}$, `1 - NORMALD_CDF(...)` is exactly 0, so compute an upper tail as a lower tail (`NORMALD_CDF(m, s, 2*m - t)`). And take a standard deviation from the deviations from the mean, in a second pass, and not from the shortcut $\Sigma x^2 - n\bar{x}^2$, which loses its digits when the mean is large next to the standard deviation.
- `STRING(x, 1, d)` ignores `d`. Fixed decimals need mode 2, which turns scientific below $10^{-d}$ (with its own E and a Unicode minus sign) and takes at most 12 decimals, so `STRING(ROUND(x, d), 2, d)` is the safe way to write a number with `d` decimals.
- `INSTRING` on an empty string is an error, and `LEFT(s, 0)` returns the whole string.
- The chi-square and *F* cumulative distribution functions and quantiles take whole-number degrees of freedom only. `BINOMIAL` takes its arguments in the order (*n*, *p*, *k*), which is not the order that HP's command reference gives. `LNGAMMA` exists only in the CAS.
- Variables declared at the file level keep their values between runs, until the program is checked or sent again.
- A program can read and assign the calculator's Home settings, which are variables like any other: `HSeparator` (Digit Grouping), `HFormat` and `HDigits` (Number Format), `HAngle` (Angle Measure), and `Entry`. Prime programmers know this, and programs that others have published save a setting, change it, and put it back when they end. A change acts at once, and it stays after the program ends unless the program puts it back.
- `STRING` writes the decimal mark that Digit Grouping sets, inside a running program too. The first line `#pragma mode( separator(.,;) integer(h32) )` settles how the program's own text is read, not how its numbers are written, so with a comma as the decimal mark a routine that looks for a period in a number's text goes wrong: ours showed 0.9772 as 0,9,772.
- So each of our *Statisticles* begins with `HSeparator := 0; HFormat := 0; HAngle := 0; Entry := 0;` and leaves those four settings that way. Two things are read before that line runs, and so with the reader's own settings: the form in which the Program Catalog asks for a routine's numbers, and a line typed in Home view.

**Symbols and special characters**

- Statistics needs letters with a bar or a hat over them, and the Prime's font has four of those letters ready-made. $\bar{x}$ is `CHAR(57344)` and $\hat{p}$ is `CHAR(57345)`. HP put those two characters in the part of the character set that Unicode leaves for private use, where HP's font also has an italic i, a superscript −1, and a bold italic x and y (`CHAR(57347)` to `CHAR(57350)`). $\hat{y}$ and $\bar{y}$ are ordinary Unicode letters, `CHAR(375)` and `CHAR(563)`. Each of the four is one character, so each one sits in a line of text like any other letter and grows with the font. Of our 31 *Statisticles*, 23 print $\bar{x}$ and 13 print $\hat{p}$. Only ScatterLab prints $\hat{y}$ and $\bar{y}$, which have been seen on the Virtual Calculator and not yet on a G1 or a G2.
- NormExplorer once drew the bar of its $\bar{x}$ by hand, in four of its early versions, before we found HP's character. So ask the font before you draw a symbol by hand. SymProbe, in `diagnostics/`, shows what the font draws for $\hat{y}$, for $\bar{y}$, and for the first 32 characters of the private range.
- Unicode's combining marks do not combine on the Prime. The combining bar, `CHAR(772)`, is drawn as a character of its own to the right of the letter that the bar was meant to cover.
- The other symbols on our screens are ordinary characters of the font: $\chi^2$ is `CHAR(967) + CHAR(178)`, and √, ≥, ≤, ≠, ±, ×, →, ∞, the Greek letters that our *Statisticles* use, and the subscripts 0, 1, and 2 are all in the font. A symbol typed into a string and the same symbol built with `CHAR()` are the same character on the screen. Keep symbols out of any text that the CAS will read.
- The font has no $\bar{d}$, the mean of a set of differences, so our *Statisticles* draw one. `TEXTOUT_P` returns the x where its text ends. The routine below, from AgreeLab, draws the text that comes before the $\bar{d}$, then the d, then a line 3 pixels above the top of the d's text cell, from the d's left edge to 2 pixels short of where the d ends, and then the text that comes after. A bar drawn any lower runs into the stem of the d. ResampLab has the same routine. DbarProbe, in `diagnostics/`, draws the bar at four heights in two fonts, so that you can check the height on your own calculator. (The font has no capital $\bar{Y}$ either.)

```
ag_TxDb(tbA, tbB, tbX, tbY, tbC, tbW)
BEGIN
  LOCAL tbE, tbD;
  tbE := TEXTOUT_P(tbA, G1, tbX, tbY, 1, tbC, tbW);
  tbD := TEXTOUT_P("d", G1, tbE, tbY, 1, tbC);
  LINE_P(G1, tbE, tbY - 3, tbD - 2, tbY - 3, tbC);
  TEXTOUT_P(tbB, G1, tbD, tbY, 1, tbC, MAX(1, tbX + tbW - tbD));
END;
```

**Keys, touch, and the screen**

- `FREEZE` is not a pause, so to hold a page on the screen, drain the keyboard (read and throw away any key presses that are already waiting), wait for a key, and then drain the keyboard again.
- Under `WAIT(-1)`, a tap on the soft-key strip arrives only as a click, `{3, x, y}`, and a finger lift can arrive as a list of one element, so check `SIZE` before reading x and y. `MOUSE` and `WAIT(-1)` number their touch events differently.
- `TEXTOUT_P` returns the x just past the text it drew, which places the next piece of a line. Our GlyphProbe measured the width of 132 characters in the three fonts, so that help text can be wrapped by pixels.
- Draw a page off-screen and copy it once with `BLIT_P`: a whole screen takes about 1 millisecond on a G2 and 5 on a G1.
- A one-color `RECT_P` fills its rectangle, so draw a frame with four `LINE_P` (BurrLab learned this on a G1). Rings of `ARC_P` do not make a solid disc. `MSGBOX` shows five lines.
- A `CHOOSE` menu shows eight items, and a longer menu scrolls. An item is cut off after about 30 characters, and the menu's title after 31 characters.
- When a program is run from the Program Catalog, the text that the program returns appears in a box of five lines of about 26 characters each, and the rest of the text is dropped. Keep the returned line to about 100 characters.
- On the Virtual Calculator, a page that waits for a key by polling `GETKEY` missed about one key press in eight, and a page that waits with `WAIT(-1)` missed none. Whether a G1 or a G2 misses key presses in such a loop has not been counted yet. KeyProbe, in `diagnostics/`, does the counting.

**MicroPython**

- The Prime runs MicroPython 1.9.4, a 2018 release, so read that version's documentation. `random`, `time`, and `os` are missing; use `urandom`.
- A Python error does not raise a PPL error, and `IFERR` around `PYTHON(...)` catches nothing. Clear the result first, check it by using it, and keep a PPL fallback. NormExplorer's sampler failed this way, silently, for eleven builds.
- `hpprime.eval` sees only `EXPORT`ed names. A call into Python pays for itself when Python hands back a few numbers, not hundreds.

**The CAS**

- `CAS(s)` with a string variable hands back the text unevaluated. `EXPR("CAS(\"string(" + s + ")\")")` evaluates it and returns the answer as a string, with every digit.
- CAS variables persist from one call to the next, and into the student's CAS view, so a program should never assign one.
- The Prime prints CAS answers its own way (`e^(`, `√`, and braces), not the way the desktop version of Giac does (Giac is the computer algebra program on which the Prime's CAS is built).

**Speed**

- A G2 runs PPL three to four times as fast as a G1.
- If a Prime turns slow, reset it. Our G2 had become about 15 times slower than normal until a paperclip reset, and it took 40% to 75% longer on the same tests while it was connected to the Connectivity Kit.

**Loading programs down the cable**

These notes are about the Prime Loader, the book's web page that sends our *Statisticles* down the USB cable to a real calculator (How to use this book), and they are not in the Lessons Learned. These notes come from the logs of the author's G2 and G1, 17 and 18 November 2026, which are kept in the repository's `prime-loader/usb/` folder beside the code (`prime_usb_v3d.js`). The code was written from four public descriptions of the cable (hp-prime-kit, hp-prime-web, PrimeDev, and hp-prime-emulator, all on GitHub) and from those logs, and carries none of those projects' code.

- To a computer, the Prime is a USB "human interface device," like a keyboard: HP's vendor number, 03F0, with product number 2441 for a G2 and 1541 for a G1. A G2 speaks in reports of 1,024 bytes, and a G1 in reports of 64 bytes. Chrome and Edge can reach such a device from a web page (WebHID); Firefox and Safari cannot. Bonjour, the Apple service through which HP's Connectivity Kit finds a calculator (Appendix B), is not involved at any step.
- The calculator knows two framings (two ways of wrapping a message into USB reports), an old one and a newer one. Both calculators answered "who are you" in the old framing, took the message `FD 01 00 00 00 01 03`, and after `FF EC` spoke the newer framing. In the old framing a program of 255 reports was kept, and a program of 263 reports (G1) or 274 reports (G2) was not kept, so the old framing is too short for our larger *Statisticles*.
- Send each program uncompressed. A program that the browser compressed first was acknowledged by both calculators and then not kept.
- The calculator acknowledges every 77th report, so send 77 reports and wait. The calculator sometimes says "send again" about a report that is still on its way. Send that one report again and listen; never send a run of reports again.
- Asked for a program back, the calculator compresses the program first, and a big program takes a while: for the 289,813 characters of EpiStats, a G1 needed 3.1 seconds before the G1 began to answer, and a G2 needed 0.9 seconds. Wait in proportion to the size of the program.
- Acknowledge every answer the calculator gives. A G1 whose answer was left unacknowledged answered nothing more in the newer framing until the G1 was asked "who are you" again in the old framing.
- Every wait needs an end. The first test page waited forever for an answer that the calculator never sent. The Loader counts each wait from the moment the wait starts, and pulling the cable ends every wait at once.
- A full calculator says nothing. The author's G1, sent the 30 programs that go down the cable (every *Statisticle* but CentralLimit, which is an app), kept 15 of them (about 2.1 million characters; the G1's Program Catalog then showed 4.35 MB of programs). The G1 acknowledged every report of the 16th program and kept only the program's name: asked for the 16th program back, the G1 sent an empty program, and the catalog listed that program at 0 KB. So the Loader calls an empty copy "full."
- A calculator answers later and later as the calculator fills. The author's G2, sent the same 30 programs, took longer to verify the programs as the load went on (0.4 seconds for the first program, 22 seconds for the 10th and for the 13th), and at the 14th program the G2 took one report and then nothing more for a minute, while still on its cable, and we do not know why the G2 did that.
- So neither calculator holds all of our *Statisticles* at once, and the Loader sends the programs one group at a time, and it calls each group a Sample (no Sample is over about 1.2 million characters). Before a Sample goes on, the Loader takes the *Statisticles* of the other Samples off. A delete is the message `EB` with the program's name, and the calculator sends no answer to a delete. On the author's G1 and G2, after a Sample had gone on, the Program Catalog held that Sample's programs and none of the other *Statisticles*.
- A program that has arrived whole does not always run. Every download described here was verified, character for character. On the G2, sent four programs, **Run** opened the editor for two of the four, and each of the two ran after a **Check**; the other two ran at once. On the G1, sent three programs, two ran, and at **Run** on EpiStats the calculator reset; EpiStats sent by itself then ran with no **Check**. The Loader now leaves the calculator alone for a few seconds after each program, and sends EpiStats in a Sample of its own. With the rest after each program, 11 of 13 programs started with no Check over three runs on the two calculators, against 4 of 7 programs before. The program that still needed a Check was a different program each time, and that program has been the first one sent, a middle one, and the last one sent. We do not know why. hp-prime-kit's notes say that a very large program "may need an explicit compile before it will run," a statement that those notes call reported and not measured. Our *Statisticles* are 40,000 to 290,000 characters long.
- A calculator on its cable is slow. The author's G1 ran EpiStats very slowly while the G1 was plugged in, and at its normal speed once the cable was unplugged. The G1's slowdown on its cable is the same slowdown that the Speed list above reports for the G2.
- A restart first is cheap insurance. A G2 that had been left with an answer nobody took kept offering that old answer all through the next load, until the G2 was switched off and on.
- The calculator's serial number travels in its "who are you" answer, but the Loader never reads, logs, or shows the serial number.

## Programs that measure your calculator

The programs in `diagnostics/` are short, and each one answers a question about the calculator it runs on:

- **GfxProbe** tries the graphics and touch features the manuals describe: translucent fills, the 3-D mesh, scaled copies, a second finger, the events of `WAIT(-1)`, and how many lines a message box shows.
- **CASProbe** finds out how a program can use the CAS safely.
- **MenuTapProbe** shows what `WAIT(-1)` reports for a tap on the soft keys.
- **SpeedProbe** times eleven kinds of work in about 20 seconds. Run it on a G1 and a G2 and compare.
- **PyVer** and **PyProbe** report the MicroPython version and what its modules contain.
- **SymProbe**, **CommaProbe**, and **DbarProbe** show which symbols the font has, how wide a comma and a digit are, and a d with a bar drawn over it. GlyphProbe, which measured the widths of the characters, is in `verify/round11/`.
- **LocalHeadProbe** finds out whether `LOCAL name(a, b)` is a legal routine head.
- **KeyProbe** counts how many of your key presses each of six kinds of waiting loop receives.

## How we tested

- **The Virtual Calculator** runs the Prime's own firmware, so a program that works there behaves the same way on a calculator, apart from speed, memory, and the display. We ran it on Windows, and on Linux under Wine.
- **A harness on a PC** (`tools/ppl_run_v3e.py`) runs a program with scripted keys, taps, and drags, with SciPy behind the statistics functions and the desktop version of Giac behind the CAS. The harness is a model of the Prime, not the Prime: it counts in 16 digits where the Prime keeps 12, so the calculator's behavior was added to it as each difference was found (`tools/prime_facts_v1.py`), and nothing counts as tested until it has run on the Virtual Calculator or a calculator.
- **The monkey test** (`tools/monkey_v1b.py`) runs a program 1,000 times with random keys, taps, menu picks, cancels, and odd values typed into its forms, and reports every way it broke. A page that random keys seldom reach gets directed runs as well: a scripted set of keys opens the page, and the random keys start from there.
- **The gate** (`tools/ppl_gate_v1e.py`) runs every check before a program is pasted: the built-in names, the tags, the comment rule, and the linter of hp-prime-kit (a linter is a program that checks code for mistakes without running the code).
- **Real calculators**, a G1 and a G2, are where we tested the speed and the touch screen.

## Where else to look

- [**Jordi Rigau's hp-prime-kit**](<https://github.com/JordiRigau/hp-prime-kit>) (https://github.com/JordiRigau/hp-prime-kit): a linter, an interpreter, and a builder of calculator files, with careful notes on the Prime's MicroPython that say which claims were measured.
- **Mike Markowski's HP Prime programming pages** at the University of Delaware: the bridge between Python and PPL, with examples.
- **Neil Streeter's *HP Prime Python Activities***, at hpcalc.org.
- **HP's handout *Programming in HP PPL***, from a webinar of 2015, at hpcalc.org: functions that the user defines, a program that draws the Sierpinski triangle, and an app that rolls Sicherman dice (HP Calculators and Educational Solutions, 2015). Appendix C's section on HP's free resources says more about the handout.
- **hpcalc.org** and the forum of **the Museum of HP Calculators** (see the Acknowledgments).

If you find something we got wrong, or measure something on your own calculator, please tell us through the **Issues** tab of the repository. We'd love to hear from you.

A last word of thanks. Some of our *Statisticles* owe their start to programs that other people wrote, and each one says so in its help pages or in the notes at the top of its file. For RankLab, AnovaLab, FitCheck, ResampLab, SurvLab, and ExhibitLab we looked at programs for the TI-83/84 Plus: the ones that come with Mario Triola's textbook for those calculators (Triola, 2007), Michael Lloyd's rank tests among them, and others from the TI program libraries. The U.S. Copyright Office's Circular 61 says that copyright protects the expression in a computer program and not its functional aspects, such as its algorithms, functions, and logic (U.S. Copyright Office, 2021). Even so, *we did not reuse any of that code*: we took from each program what it computes, not how it is written, and wrote our own version for the Prime, in the Prime's own language, to compute similar results.

StudRange's arithmetic follows the FORTRAN function that Dunlap, Powell, and Konnerth published in 1977 (Dunlap et al., 1977). StatDist does with menus and plots what Salvo Micciché's *Statistic Distributions* does with functions typed in Home view (Micciché, 2015), and RankLab's runs test does what Hewlett-Packard's own program for the runs test (the HP-65's manual calls the program "The Run Test for Randomness") did on the HP-65 and the HP-67 (Hewlett-Packard Company, 1975). StatDist and the runs test were both written new, with none of the earlier code. The idea for CentralLimit comes from Colin Croft's aplet for the HP 39G (Croft, 2003), and the idea for GaltonBoard comes from Galton's quincunx and from QUINCUNX, a small demonstration program that came with Epi Info 6, the free epidemiology software of the U.S. Centers for Disease Control and Prevention (Dean et al., 1996). Jordi Rigau's hp-prime-kit is the checker behind our gate, and every program in this book passed it. To each of these authors, and to the many HP users whose programs showed us what the Prime can do, ***thank you!***

## References

Abramowitz, M., & Stegun, I. A. (Eds.). (1964). *Handbook of mathematical functions with formulas, graphs, and mathematical tables*. National Bureau of Standards.

Beers, T. W., Byrne, D. K., Donnelly, J. A., Jones, R. W., & Yuan, F. (1996). A graphing calculator for mathematics and science classes. *Hewlett-Packard Journal, 47*(3), Article 6. <https://www.mrynet.com/FTP/operatingsystems/DEC/www.hpl.hp.com/hpjournal/96jun/jun96a6.pdf>

Croft, C. (2003). *Central limits theorem* [Computer software for the HP 39G and HP 40G]. hpcalc.org. <https://www.hpcalc.org/details/5644>

Dawid, A. P., & Mortera, J. (2019). Graphical models for forensic analysis. In M. Maathuis, M. Drton, S. Lauritzen, & M. Wainwright (Eds.), *Handbook of graphical models* (pp. 473–495). CRC Press.

Dean, A. G., Dean, J. A., Coulombier, D., Brendel, K. A., Smith, D. C., Burton, A. H., Dicker, R. C., Sullivan, K., Fagan, R. F., & Arner, T. G. (1996). *Epi Info, version 6: A word-processing, database, and statistics program for public health on IBM-compatible microcomputers* (Version 6.03). Centers for Disease Control and Prevention. <https://stacks.cdc.gov/view/cdc/23189>

Dunlap, W. P., Powell, R. S., & Konnerth, T. K. (1977). A FORTRAN IV function for calculating probabilities associated with the studentized range statistic. *Behavior Research Methods & Instrumentation, 9*(4), 373–375. <https://doi.org/10.3758/BF03202264>

HP Calculators and Educational Solutions. (2015). *HP Prime APSI 2015 webinar: Programming in HP PPL* (Version 1.2) [Handout, 14 pages]. hpcalc.org. Accessed 25 November 2026. <https://www.hpcalc.org/details/7905>

HP Development Company. (2017). *HP Prime Graphing Calculator* (3rd ed.) \[User guide; document part number 813269-003\]. HP Development Company. hpcalc.org. Accessed 25 November 2026. <https://www.hpcalc.org/details/7445>

Hewlett-Packard Company. (1975). *HP-65 Stat Pac 2* \[Manual for a set of prerecorded program cards; Part No. 00065-90275\].

Hofmann, H. (2008). Mosaic plots and their variants. In C. H. Chen, W. Härdle, & A. Unwin (Eds.), *Handbook of data visualization* (pp. 617–642). Springer.

Jahnke, E., & Emde, F. (1945). *Tables of functions with formulae and curves* (4th ed.). Dover Publications.

Micciché, S. (2015). *Statistic distributions* [Computer software for the HP Prime]. hpcalc.org. <https://www.hpcalc.org/details/7639>

Miller, R. M. (1984, July). Plug-in module adds FORTH language and assembler to a handheld computer. *Hewlett-Packard Journal*. <https://hpmuseum.org/journals/71forth.htm>

The Museum of HP Calculators. (n.d.-a). *HP-65*. Accessed 16 November 2026. <https://www.hpmuseum.org/hp65.htm>

The Museum of HP Calculators. (n.d.-c). *HP 9100A/B*. Accessed 17 November 2026. <https://hpmuseum.org/hp9100.htm>

The Museum of HP Calculators. (n.d.-e). *Feature time line*. Accessed 17 November 2026. <https://hpmuseum.org/timeline.htm>

The Museum of HP Calculators. (n.d.-g). *RPN*. Accessed 21 November 2026. <https://hpmuseum.org/rpn.htm>

The Museum of HP Calculators. (n.d.-h). *RPL*. Accessed 21 November 2026. <https://hpmuseum.org/rpl.htm>

The Museum of HP Calculators. (n.d.-i). *HP 9820A*. Accessed 21 November 2026. <https://hpmuseum.org/hp9820.htm>

The Museum of HP Calculators. (n.d.-j). *HP 9825*. Accessed 21 November 2026. <https://hpmuseum.org/hp9825.htm>

The Museum of HP Calculators. (n.d.-k). *HP-71B*. Accessed 21 November 2026. <https://hpmuseum.org/hp71.htm>

Triola, M. F. (2007). *Elementary statistics using the TI-83/84 Plus calculator* (2nd ed.). Addison Wesley.

U.S. Copyright Office. (2021). *Copyright registration of computer programs* (Circular 61). <https://www.copyright.gov/circs/circ61.pdf>
