# Round 17: the words on the screen follow the book's rules for a statistic's letter (17 November 2026)

Sixteen programs, and in each of them only words inside quotation marks. No arithmetic, no menu's order, no page count and no line that is not text changed.

Roger, 17 November 2026, reading Draft 46 of the book: "The p-value and t-test, t-distribution etc should be hyphenated and italicized", and "make sure expressions like n-1 are in parentheses". The book prints every program's help pages word for word, so the programs' own text was read for the same two rules, and Roger, asked whether to change it now or later: "Now, as Round 17". A calculator's screen has no italics, so a program keeps the rest of each rule:

- **(a)** an expression like n - 1 stands in parentheses of its own: `df = (n - 1)`, `(k - 1) df`, `df = (N₁ + N₂ - 2)`. A sentence is turned so that no parenthesis stands inside another ("Breslow-Day, (k-1) df:").
- **(b)** a hyphen joins a statistic's letter to its noun: F-test, z-test, t-table, t-curve, t-interval, F-quantiles, z-values, p-tail. "t critical value" and "t crit" take none (the book's form of 10 November).
- **(c)** the p of p-value is a small letter, at the start of a title too.

The Prime's own names stay as the Prime spells them (Linear t test, T-Test: 1 μ), and comments keep their wording: they are not on the screen.

Before the round, `tools/screen_text_v1.py` found 116 places against these rules in 16 programs (77 of them in the quoted strings of the code; the others only in what the pages drew, where a line is put together from pieces): `screen_text_before.txt`. After it: 0 in 31 programs.

| Program | Version | What reads differently |
| --- | --- | --- |
| AgreeLab | beta 1i | "ICC intervals (F-quantiles)", "no F-interval" |
| AnovaLab | beta 1j | F-curve, F-test, q-distribution; "(k - 1) and (N - k) df", "(k - 1) comparisons", "df = (n - 1)", "df = (n₁ - 1) and (n₂ - 1)"; three menu items ("F-curve and p", "F-curve of an effect", "F-curve (treatments)") |
| CICatcher | beta 2m | "(a t-interval needs 2 or more)" |
| EpiStats | v1.7m | "M-H χ², 1 df: is the common OR 1?", "Breslow-Day, (k-1) df:" |
| ExhibitLab | beta 1i | "SD, divisor (n - 1), grams", "t on (n - 1)" |
| FitCheck | beta 1j | "df = (k-1-m)", "(k-1)", "(k-2)", "(k-3)", written without spaces because its help text flows and a line must not end inside one |
| PowerViz | v2.5t | "F-test of s₁²/s₂²", "z-values (PPL)", "z-test: σ₁, σ₂ taken as known" |
| RankLab | beta 1k | "magenta = the p-tail(s)" |
| ResampLab | beta 1j | "BCa and t-intervals" |
| ScatterLab | beta 2m | "df = (n - 2) = 14", "df = (n - 2);  H₀" |
| StudRange | beta 15n | "p-value from q" (the first menu item and its form), "p-value: Studentized Range" (its result) |
| TDist3D | beta 1b | "ν = (n − 1)", "Every t-curve at once" |
| TTestLab | beta 1l | "t-table, row df = 60", "df = (N - 1)", "df = (N₁ + N₂ - 2)" |
| TTestLabG | beta 1i | the same, built from TTestLab beta 1l; "the smaller of (N₁-1), (N₂-1)" |
| TestChooser | beta 2h | "Cochran's Q-test", "χ², (k - 1) df.", "ANOVA; (k - 1) df." |
| TrendTest | beta 3n | "Departure = Pearson - trend, (k-2) df", "(k-1) df", "(k-2) df" |

Each program's change note (`docs/changes/<Name>_<version>_CHANGES.md`) has every line that changed, as it said and as it says.

## What is here

| File | What it is |
| --- | --- |
| `make_round17.py` | The build of fifteen programs. Each change is an exact replacement in the version before, read from git (`BASE`, the commit before this round), looked for in the code of a line and never in its comment; a replacement that is not found the number of times named stops the build. It then runs `tools/make_tlg1_v4.py`, which builds TTestLabG beta 1i from TTestLab beta 1l. |
| `screen_text_before.txt` | `tools/screen_text_v1.py` on the 31 programs as they were, with the walks: the 116 places. |
| `records_r17.py` | Gathers the round's other records: `gates/` (`tools/ppl_gate_v1e.py` on each new version against its old one), `helppages_before_r17.json` and `helppages_r17.json` (every help screen of the old and the new versions as the PC harness draws them), `helpcheck_r17.json` (every new help screen laid out at the glyph widths GlyphProbe_v1 measured), `checks_r17.txt` (S, the harness smoke test; T, the generic walks of the old and the new version; W, `screen_text_v1.py` with the texts the walks of all 31 programs drew; F, the fleet's names), `overlap_<Name>.txt` and `drawn/`. |
| `drawn_texts_r17.py`, `drawn/` | The distinct texts that the walk of each of the 31 programs drew, one list a program (22,990 texts, under 1 MB). The walks themselves, as `text_overlap_v1.py --json` writes them, come to 381 MB (GaltonBoard's alone is 350 MB) and are not kept; `screen_text_v1.py --walk` reads either. |
| `make_changes_r17.py` | Writes the sixteen change notes from those records and from the verify script's output. |
| `count_lines_r17.py` | Counts the fleet's lines the way the README's sentence gives them (PPL code, MicroPython, comments), for `programs/` or for any commit. |
| `walk_detail_r17.py`, `overlap_TTestLabG_detail.txt` | The one finding the walk of TTestLabG beta 1i has that the walk of beta 1h had not, text for text, and its width at the calculator's glyph widths. |
| `vc_checks.txt` | The Checks on the Virtual Calculator, the four runs made afterwards, and what was not looked at there. |
| `screens/` | Six captures from the Virtual Calculator, each 320 × 240 as the calculator drew it: TTestLab's steps 2 and 3 ("df = (N₁ + N₂ - 2)", "t-table, row df = 60"), ScatterLab's Inference page ("df = (n - 2) = 14"), PowerViz's help 5 of 7, and TDist3D's opening page and help 1 of 4. The book's Figures 11.3 and 13.4 are `TTestLab_crit.png` and `ScatterLab_inference.png`, enlarged three times. |
| `../verify_round17_screen_text_v1.py` | The verify script for all sixteen: 160 checks, 0 failed; its saved output is beside it. |

## To run again

From the repository's root, with hp-prime-kit at `$HPKIT` (see `CLAUDE.md`):

```
python3 verify/round17/make_round17.py OUTDIR                 # the sixteen programs, under a minute
python3 verify/verify_round17_screen_text_v1.py               # about 12 minutes; T4 T6 ... or --only=Name,Name for a part
python3 verify/round17/records_r17.py                         # about 26 minutes: StudRange's two walks take most of it
python3 verify/round17/walk_detail_r17.py                     # TTestLabG's two walks, text for text: half a minute
python3 verify/round17/make_changes_r17.py .                  # the change notes
python3 tools/screen_text_v1.py programs/*.txt                # the check itself: seconds (--walk verify/round17/drawn adds the drawn texts)
python3 verify/round17/count_lines_r17.py                     # the README's line counts
```

## What the checks found

- **A sentence that grew by two characters made a new page.** FitCheck's help page 4 of 12 was full; "df = k - 2" with its parentheses pushed the page's last words, "1).", onto a thirteenth page. The sentence was turned, and the page count is 12 as before. After any change of words, dump the help pages again.
- **A line that flows can break inside an expression.** FitCheck's notes wrap at a space, and "(k - 3)" came out as "(k" at the end of one line and "- 3)." at the start of the next. FitCheck's expressions are written without spaces. The verify script's T6 now refuses a new line that ends inside an expression in parentheses.
- **A line with a width argument is cut, not wrapped.** TDist3D's first help sentence came to 299 px in a box of 296 with the parentheses added. The sentence was turned (285 px).
- **A hyphen is twice as wide as a space** at font 1 (6 px and 3 px on the Virtual Calculator: `../round11/glyph_widths_vc.json`), so "F-test" is 3 px wider than "F test". The tightest changed line is PowerViz's help 5 of 7, "... the program puts in the z-values (PPL), giving": 301 px, 7 px short of the screen's edge.
- **The glyph widths hold.** Five changed lines were looked at on the Virtual Calculator, the tightest of the round among them. In each, the width measured from the glyph table put the line's end 1 to 2 px beyond its last dark pixel (PowerViz's line: 313 by the table, 312 on the screen, of 320). `vc_checks.txt` has the five.
- **The generic walk counts by a rougher rule.** `text_overlap_v1.py --walk` takes 6.5 px for every character at font 1. TTestLabG's line "By hand: df = the smaller of (N₁-1), (N₂-1) = 181," has 50 characters where it had 46, and by that rule it passes 320, so the walk of beta 1i counts 19 overruns where beta 1h's counts 18. The finding is marginal by the walk's own second measure, and the line is 225 px wide at the calculator's glyph widths (`overlap_TTestLabG_detail.txt`). StudRange's two walks differ only in how many screens each got through before its time budget ran out (465 and 484), with the same 74 distinct screens and the same findings. The other fourteen programs' two reports are the same.
- **A walk is no file for a repository.** The 31 walks came to 381 MB. The check needs only the distinct texts each walk drew, 22,990 of them, and reads those lists as well as it reads the walks.
- **A symbol put together from pieces is not in any one string.** TDist3D builds "ν = n − 1" with `tdMin := CHAR(8722)`. The check reads a name that has one value as that value, and reads the walks' drawn texts beside the code's strings.
- **A verify script that catches every error hides its own.** An early version of this round's script named a routine that did not exist; `except Exception` swallowed the `NameError`, and the symbols were drawn as "0". The script now catches the harness's three errors and its own time-out, and nothing else.

## How the changed words were seen

Of the 46 changed wordings, 21 were shown by the help pages; 16 more only by the monkey's sessions (30 seeds a program, 10 for StudRange); 9 more only by a directed lead, a scripted way to the page (`verify_round17_screen_text_v1.py`, T6, counts them). Every one was on a screen of the new version at least once, and every one fits where it is drawn. Over the same seeds the old and the new versions showed the same screens, text for text, once the changed words are read back (T7).

## For the book

- **Help pages.** Ten programs show other words on 17 help pages (AnovaLab, EpiStats, ExhibitLab, FitCheck, PowerViz, ScatterLab, TDist3D, TTestLab, TTestLabG, TrendTest); the other six programs' help pages are the same. No program gained or lost a page.
- **Menu items.** No item moved. Three items of AnovaLab's menus have a hyphen now ("F-curve and p", "F-curve of an effect", "F-curve (treatments)"), and StudRange's first item says "p-value from q" (it said "P-value from q"), as do the form it opens and, with "p-value: Studentized Range", the page of its result.
- **Pictures.** Two of the book's captures showed words that changed, and both were taken again (`screens/`): Figure 11.3, TTestLab's critical value, and Figure 13.4, ScatterLab's Inference page.
- **Text.** The book's own text quotes none of the changed wordings outside its help pages.

## Seen, not changed

- Two formulas in text this round did not touch end a line inside their parentheses, as they did before: FitCheck's help 2 of 12 ("χ² = sum of (O -" and then "E)²/E"), and ResampLab's note on the plus-one p ("(count + 1)/(B +" and then "1)"). They wait for the next change of those two programs.
- AnovaLab's help 4 of 10 and TTestLab's help 2 of 3 each end a line just after an opening parenthesis of a remark ("(k" before "2-12, df 3-1,000", "(a" before "df the table lacks"). A remark is not an expression, and both are as they were.

## Not done

- No file of this round has run on a G1 or a G2.
- On the Virtual Calculator the sixteen were Checked, and four were run afterwards (TTestLab, ScatterLab, PowerViz, TDist3D) for the book's two pictures and for the three changed lines with the least room. The other changed pages were not looked at there; their words were measured at the glyph widths read on that calculator (`vc_checks.txt`, 4).
