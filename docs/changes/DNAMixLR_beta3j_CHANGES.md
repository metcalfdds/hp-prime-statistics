# DNAMixLR beta 3j: changes (9 November 2026)

Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites (`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, the explanation is what matters". The build, `verify/round11/make_round11.py`, makes DNAMixLR beta 3j from DNAMixLR beta 3i. Every change is an exact replacement, and a miss stops the build.

## What changed

1. **The help in plain words.** Help pages 1 to 4 reworded: what P(E|H) counts, the ENFSI words, the keys and the formula in plain words.

2. **Every changed page laid out again at the calculator's own widths.** GlyphProbe_v1 measured every character the help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line's width is the sum of its characters' widths. So each changed line now uses the width the page allows, and nothing is cut. The help is still 4 screens, as the PC harness counts them.

3. **Nothing outside the help changed**, apart from comments and the version strings.

Routines touched, with the number of new or changed lines in each: (comments) 6, dmHelpPage 48.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. 4 of 4 screens changed; 0 kept their words.

### Before (beta 3i)

```text
DNAMixLR help 1/4: Alleles and hypotheses
Each locus shows a SET of alleles, called M.
Under a hypothesis, known contributors must
have all their alleles in M; the x unknown
people supply the rest of M and nothing else.
P(E|H): the chance 2x random alleles do that.
LR = P(E|Hp) / P(E|Hd); loci multiply.
Example: mixture 12,13,14,15; victim 12/13.
Hd (victim + 1 unknown): the unknown must be
14/15, P = 2 p14 p15.  Hp (victim + suspect
14/15): P = 1.  LR = 1 / (2 p14 p15).
Genotype entries are POSITIONS in your allele
list (1 = the first allele); 0 means an
allele the mixture does not show.
Teaching aid; not for casework or legal use.
tap or Ent = next page, Esc = menu
```

```text
DNAMixLR help 2/4: Theta (coancestry)
THETA (coancestry, Fst): people in the same
subpopulation share ancestry: an allele seen
in a typed person is likelier in the unknown.
NRC II (1996) 4.2: P(next = a | n seen, n_a
are a) = (n_a th + (1-th) p_a)/(1 + (n-1) th)
ALL typed people condition it, contributors
or not (Curran et al. 1999).  0.01 is usual,
0.03 conservative.  The θ plot shows how
much the LR falls as θ rises.
ENFSI scale: LR 2-10 weak, 10-100 moderate,
100-1,000 moderately strong, 1e3-1e4 strong,
1e4-1e6 very strong, above 1e6 extremely so.
Teaching tool only: casework needs validated
software and a qualified analyst.
tap or Ent = next page, Esc = menu
```

```text
DNAMixLR help 3/4: Keys and touch
Soft keys: Locus, Theta, Table, Ladder, Help,
Menu.  Esc always goes back to the menu.
LOCUS PLOT: tap a bar (or Left/Right) for its
numbers; again (or Ent) for the locus page.
+ or a tap on the title: the waterfall.
THETA PLOT: drag across it (or Left/Right);
LR and the ladder follow.  Ent adopts θ.
TABLE: tap a row (or Up/Down, Ent) to drop
that locus -- as if not typed; tap to restore.
LOCUS PAGE: tap the boxes (or +) for Hp / Hd:
green victim, magenta suspect, red = what the
unknowns must supply.  arrows: loci, -: formula.
LADDER: the LR builds locus by locus.
The LR is NOT the probability that the suspect
contributed: see Prosecutor's fallacy (8).
tap or Ent = next page, Esc = menu
```

```text
DNAMixLR help 4/4: The LR as a formula
THE LR AS A FORMULA: on a locus page press -
(or tap the footer).  The CAS writes the LR
in the allele frequencies p and θ,
from the same model the program uses, and
simplifies it.  At θ = 0 it is the product
rule, e.g. LR = 1/(2 p14 p15).  The number
under it is the program's own LR.  Badge:
exact (CAS), or decimal if the CAS failed.
BAND EDGE (θ plot, orange): the θ at
which the combined LR crosses the next ENFSI
band edge as θ rises from yours: how far
θ must go before the words change.
Found by bisection in the program, not by CAS.
tap or Ent = next page, Esc = menu
```

### After (beta 3j)

```text
DNAMixLR help 1/4: Alleles and hypotheses
Each locus shows a SET of alleles, called M.
Under a hypothesis, known contributors must have all their
alleles in M; the x unknown people supply the rest of M and
nothing else.
P(E|H): the chance that the x unknowns' 2x alleles (two each,
drawn at random) do exactly that.
LR = P(E|Hp) / P(E|Hd); the loci's LRs multiply.
Example: mixture 12,13,14,15; victim 12/13.
Hd (victim + 1 unknown): the unknown must be 14/15, P = 2
p14 p15.  Hp (victim + suspect 14/15): P = 1.  LR = 1 / (2
p14 p15).
Genotype entries are POSITIONS in your allele list (1 = the first
allele); 0 means an allele the mixture does not show.
Teaching aid; not for casework or legal use.
tap or Ent = next page, Esc = menu
```

```text
DNAMixLR help 2/4: Theta (coancestry)
THETA (coancestry, Fst): people in the same subpopulation share
ancestry: an allele seen in a typed person is likelier in the
unknown.
NRC II (1996) 4.2: P(next = a | n seen, n_a are a) = (n_a
th + (1-th) p_a)/(1 + (n-1) th)
Every typed person's alleles count in it, contributor or not
(Curran et al. 1999).  0.01 is usual, 0.03 conservative.  The θ
plot shows how much the LR falls as θ rises.
ENFSI scale: LR 2-10 weak, 10-100 moderate, 100-1,000
moderately strong, 1,000-10,000 strong, 10,000-1,000,000
very strong, above 1,000,000 extremely strong.
Teaching tool only: casework needs validated software and a
qualified analyst.
tap or Ent = next page, Esc = menu
```

```text
DNAMixLR help 3/4: Keys and touch
Soft keys: Locus, Theta, Table, Ladder, Help, Menu.  Esc always
goes back to the menu.
LOCUS PLOT: tap a bar (or Left/Right) for its numbers; again (or
Ent) for the locus page.
+ or a tap on the title: the waterfall.
THETA PLOT: drag across it (or Left/Right); the LR and the Ladder
view change with θ.  Ent keeps that θ.
TABLE: tap a row (or Up/Down, Ent) to drop that locus -- as if
not typed; tap to restore.
LOCUS PAGE: tap the boxes (or +) for Hp / Hd:
green victim, magenta suspect, red = what the unknowns must
supply.  arrows: loci, -: formula.
LADDER: the LR multiplied up one locus at a time.
The LR is NOT the probability that the suspect contributed: see
Prosecutor's fallacy (menu item 8).
tap or Ent = next page, Esc = menu
```

```text
DNAMixLR help 4/4: The LR as a formula
THE LR AS A FORMULA: on a locus page press - (or tap the
footer).  The CAS writes the LR in the allele frequencies p and θ,
from the same model the program uses, and simplifies it.  At
θ = 0 it is the product rule, e.g. LR = 1/(2 p14 p15).  The
number under it is the program's own LR.  Badge:
exact (CAS), or decimal if the CAS failed.
BAND EDGE (θ plot, orange): the θ at which the combined LR
crosses the next ENFSI band edge as θ rises from yours: how far
θ must rise before the LR moves into the next ENFSI band.
Found by bisection in the program, not by CAS.
tap or Ent = next page, Esc = menu
```

## Checks

- `tools/ppl_gate_v1e.py`: PASS. hp-prime-kit lint 0 errors; ppl_check_v5 as in beta 3i; lint_ppl 7 problems, as in beta 3i (7); fleet_names_v2 over the 31 newest files: 0 collisions.
- `tools/case_scan_v1.py`: clean.
- `verify/round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word (titles, page numbers, footers and the version left out).
- `verify/round11/helpcheck_r11.py`, at the measured glyph widths: 4 screens, no line past its width or the screen's edge, no two texts overlapping.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the program".

Not yet run on a G1 or a G2.
