# BurrLab beta 1j: changes

*2 Nov 2026, night. Made from beta 1i by `tools/commas_v1.py` with `tools/commas_config_r5.py` (round 5: commas in big numbers). 4,434 lines.*

## Why

Roger, 2 Nov 2026: "always put comma delimiters in big numbers". `STRING` never groups digits, whatever Home's setting (Virtual Calculator, 2 Nov 2026: with Home showing 1,234,567, `STRING(1234567)` gave "1234567"), so the program now puts the commas in itself. The rule is APA's: commas from 1,000 up, never after the decimal point, never in a year.

## What changed

1. **A comma routine of its own, `bu_Cm`**, the fleet's routine word for word but its name (so the 30 programs, which share one pool of names on the calculator, never meet). It puts a comma every three digits into each run of four or more digits that does not follow a decimal point: 1234567.25 becomes 1,234,567.25, −98765 becomes −98,765; 0.00012345, 1.8ᴇ10 and 1,000 stay as they are. `diagnostics/CommaProbe_beta1a.txt` ran it on the Virtual Calculator: 12 answers of 12 as expected.
2. **Where a number becomes text, it goes through `bu_Cm`** at the call: 95 call(s) of the number formatters (`bu_Fx`) and 0 of `STRING`. So a number carries its commas when it is measured as well as when it is drawn.
3. **At every place text is drawn** (`TEXTOUT_P`, `MSGBOX` and the program's own text routines), 31 other piece(s) of text that could hold a number -- a variable, a list item, a routine's result -- go through it too. The program's own wording is left alone: a string written into the program, or a variable or routine that only ever holds such strings, so a year in a citation keeps no comma.
4. **1 number(s) written into the program's own text get their commas** in the text itself ("from 2 to 5,000", "Drop 1,000 balls (fast)"); a four-digit year (1500 to 2099) never does.
5. **Nothing the CAS or `EXPR` reads goes through it**: there "1,000" would be two numbers. 4 `STRING` or formatter call(s) that build CAS text stay as they were. The routines that build CAS text (`bu_Frac`, `bu_IStr`) are left as they were; where their text is shown instead, it is grouped where they are called.
6. Header: the beta 1j block; the version named on the screen.

Routines changed beyond the wrapping (literal text, the version, the edits above): `bu_DrawRes`, `bu_Opening`. Added: `bu_Cm`.

## Verification

`verify_BurrLab_beta1j.py`, output `verify_BurrLab_beta1j_output.txt`: **11 PASS, 0 FAIL**, run from a repository layout, with beta 1i read from `programs/`, an `_superseded_*` folder or git history. The script calls `tools/comma_check_v1.py`:

- **G** static: `bu_Cm` is the fleet's routine; with every call of it taken out, the code is beta 1i's, routine for routine, but for those named above; nothing the CAS or `EXPR` reads goes through it; no new `!=`; ASCII as before; the header names beta 1j.
- **R1** 30 seeds of the monkey (`tools/monkey_v1b.py`, with 1000, 2500, 12345, 54321.5 and 100000 among the typed values), each on both versions: every run takes beta 1i's path (the same ending, number of screens, boxes and summary once the commas are out). Endings: {'OK': 29, 'END Unsupported': 1}.
- **R2** (information) 0 screen(s) whose texts differ beyond the commas -- none: every screen is beta 1i's once its commas are out.
- **C** every text the program hands the CAS or `EXPR` is beta 1i's, call for call (103 calls on these runs): the commas are for the screen only.
- **M** every number of four or more digits drawn on those runs is grouped (108 different grouped numbers drawn, among them 1,000, 1,500, 2,000, 1,010). **Y** no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it.
- **D** no new firm overlap, straddle or overrun (`text_overlap_v1`: 0 before, 0 now) and no new number cut by its width (`label_fit_v1`: 0 before, 0 now).

## Gate

`ppl_gate_v1d.py BurrLab_beta1j.txt`: no problem that beta 1i does not already have; `fleet_names_v2.py` over the 30: 0 collisions.

## The Virtual Calculator

Virtual Calculator 2.4.2 (Rogers-HP, 2 Nov 2026, night; Claude through computer use): the file the starter-pack tool built from BurrLab_beta1j.txt was copied into the calculator's folder with the calculator closed, then opened in the editor and Checked: **"No errors in the program"**. The file the calculator wrote back was collected after that Check and nothing else; it is the one in starter pack v10 and the Prime Loader v1h (`make_starter_pack_v4.py --checked` found its source equal to `programs/BurrLab_beta1j.txt`). Not yet run on a G1 or a G2.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] A number of 1,000 or more on the screen shows its commas (type 12345 where the program takes a value, or load data with large values).
- [ ] A year in a help page or a citation shows no comma.
