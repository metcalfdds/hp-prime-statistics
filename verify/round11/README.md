# Round 11: the help pages in plain words (9 November 2026)

On 8 November 2026, about *Statisticles*, Roger wrote: "write more straightforward and don't try to be too clever--a student being able to understand is the priority". Then he asked whether the help pages were unclear too. A page-by-page list of proposed rewrites went to him (`Statisticles_help_page_rewrites_v1.docx`). On 9 November he approved it: "go ahead with all your suggestions", "adding pages is fine, the explanation is what matters", and of TTestLab, "please drop 'as the lecture'". This folder holds the build that made the 31 new versions, the checks, and what they found. Each program's own note is `docs/changes/<Name>_<version>_CHANGES.md`.

## What is here

| File | What it is |
| --- | --- |
| `proposals.py` | The approved wording: for each program, each change as old text and new text. |
| `make_round11.py` | The build. It applies `proposals.py` by exact replacement (a miss stops it), lays every changed page out again at the calculator's own widths, splits a page that no longer fits, renumbers the pages and the callers that ask for a page, and gives each program its next version (header, history note, version strings). |
| `tools11/` | The build's parts: `hp11.py` (glyph widths, a reader for PPL string expressions, the wrap), `pagea.py` (a help page as blocks and items; the layout and the split), `listpage.py` (help pages held as lists), `routines.py`, `props.py`, `readmat.py`. |
| `GlyphProbe_v1.txt` | The probe that measured the widths: it draws each of 132 characters in fonts 1, 2 and 3 and keeps where `TEXTOUT_P` ended, in matrix M9; then six whole lines, each in the three fonts. |
| `glyph_widths_vc.json`, `glyphprobe_items.json` | The widths (Virtual Calculator 2.4.2, 9 Nov 2026) and the probe's character list and test lines. All 18 test-line widths were exactly the sums of their characters' widths. |
| `helpdump_r11.py` | Dumps every help screen of a program, as the PC harness draws it, to JSON. `helppages_before_r11.json` is the dump of the old versions, `helppages_r11.json` of the new. |
| `helpcheck_r11.py`, `helpcheck_r11.json` | Lays every help screen out at the measured widths and reports a line past its width argument or the screen's edge, and two texts that overlap. |
| `wordcheck_r11.py` | The old help with the approved changes applied, against the new help, word for word (titles, page numbers, footers and versions left out). |
| `diffscope_r11.py` | Lists the routines each new version touches. |
| `make_changes_r11.py` | Writes the 31 CHANGES files from the records above. |
| `gates/` | `tools/ppl_gate_v1e.py` on each new version against its old one: all PASS. |
| `lintcounts.txt` | lint_ppl's problem count, old version and new: the same for every program. |
| `vc_checks.txt` | The Checks on the Virtual Calculator. |
| `mk/` | The monkey test's results (`tools/monkey_v1b.py --lists`, 1,000 runs each) for the seven programs whose help gained pages. |
| `screens/` | The help pages of AgreeLab, ChiTable, BayesTree, StudRange and BurrLab as the Virtual Calculator showed them (960 × 720; AgreeLab's page 8 is a smaller crop). |

## Results

- Gate: PASS for all 31. lint_ppl's problem counts are the old versions' counts. `tools/case_scan_v1.py`: clean.
- `diffscope_r11.py`: each new version changes its help routines, its comments, its version strings, and (AnovaLab, ChiTable) the page numbers its callers ask for. Nothing else.
- `wordcheck_r11.py`: 29 programs match word for word. Norm3's dump differs only in where the plot's axis numbers fall (the harness keeps the plot under the help, which the calculator clears), and PowerViz's only in the order of its disclaimer line.
- `helpcheck_r11.py`: clean, apart from three known reports: AgreeLab's drawn d̄ (the check measures the bar's d as a plain letter beside the next text; the Virtual Calculator shows the line correctly), Norm3's plot labels under the help (as above), and StatDist's `st_ABHelp`, which the harness cannot call without its argument.
- Virtual Calculator 2.4.2: "No errors in the program" for the 30 programs and the app.
- The monkey test: see `mk/`.

## To run it again

The scripts expect the layout of the working folder they ran in: `r/src/` with the old versions (git has them: the commit before round 11), `r/programs/` for the output, and `r/tools/` a copy of this repository's `tools/`; `helpdump_r11.py` and `helpcheck_r11.py` run from `r/`. hp-prime-kit is found through `HPKIT` (CLAUDE.md, "Setting up a fresh session").
