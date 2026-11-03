# BayesTree beta 8g: changes

*2 Nov 2026, night. Made from beta 8f by `tools/commas_v1.py` with `tools/commas_config_r5.py` (round 5: commas in big numbers). 3,429 lines.*

## Why

Roger, 2 Nov 2026: "always put comma delimiters in big numbers". `STRING` never groups digits, whatever Home's setting (Virtual Calculator, 2 Nov 2026: with Home showing 1,234,567, `STRING(1234567)` gave "1234567"), so the program now puts the commas in itself. The rule is APA's: commas from 1,000 up, never after the decimal point, never in a year.

## What changed

1. **A comma routine of its own, `bt_Cm`**, the fleet's routine word for word but its name (so the 30 programs, which share one pool of names on the calculator, never meet). It puts a comma every three digits into each run of four or more digits that does not follow a decimal point: 1234567.25 becomes 1,234,567.25, −98765 becomes −98,765; 0.00012345, 1.8ᴇ10 and 1,000 stay as they are. `diagnostics/CommaProbe_beta1a.txt` ran it on the Virtual Calculator: 12 answers of 12 as expected.
2. **Where a number becomes text, it goes through `bt_Cm`** at the call: 201 call(s) of the number formatters (`bt_NumS`, `bt_Pct`, `bt_fmtc`, `bt_fmtp`, `bt_fmtB`, `bt_fmtq`) and 7 of `STRING`. So a number carries its commas when it is measured as well as when it is drawn.
3. **At every place text is drawn** (`TEXTOUT_P`, `MSGBOX` and the program's own text routines), 15 other piece(s) of text that could hold a number -- a variable, a list item, a routine's result -- go through it too. The program's own wording is left alone: a string written into the program, or a variable or routine that only ever holds such strings, so a year in a citation keeps no comma.
4. **5 number(s) written into the program's own text get their commas** in the text itself ("from 2 to 5,000", "Drop 1,000 balls (fast)"); a four-digit year (1500 to 2099) never does.
5. **Nothing the CAS or `EXPR` reads goes through it**: there "1,000" would be two numbers. 15 `STRING` or formatter call(s) that build CAS text stay as they were. The routines that build CAS text (`bt_Book`, `bt_IStr`, `bt_LadStep`, `bt_RC`, `bt_RCnt`, `bt_RT`, `bt_Rat`, `bt_Same`, `bt_Sig2`, `bt_SlP`, `bt_Strip`) are left as they were; where their text is shown instead, it is grouped where they are called.
6. The CAS's exact fractions get their commas too (999/3,863), before their length is tested (bt_FrLn, bt_FrS), and in the summary returned to Home.
7. Header: the beta 8g block; the version named on the screen.

Routines changed beyond the wrapping (literal text, the version, the edits above): `BayesTree`, `bt_FaganView`, `bt_FrLn`, `bt_FrS`, `bt_HelpView`, `bt_IconView`, `bt_ThreeView`. Added: `bt_Cm`.

## Verification

`verify_BayesTree_beta8g.py`, output `verify_BayesTree_beta8g_output.txt`: **11 PASS, 0 FAIL**, run from a repository layout, with beta 8f read from `programs/`, an `_superseded_*` folder or git history. The script calls `tools/comma_check_v1.py`:

- **G** static: `bt_Cm` is the fleet's routine; with every call of it taken out, the code is beta 8f's, routine for routine, but for those named above; nothing the CAS or `EXPR` reads goes through it; no new `!=`; ASCII as before; the header names beta 8g.
- **R1** 30 seeds of the monkey (`tools/monkey_v1b.py`, with 1000, 2500, 12345, 54321.5 and 100000 among the typed values), each on both versions: every run takes beta 8f's path (the same ending, number of screens, boxes and summary once the commas are out). Endings: {'OK': 30}.
- **R2** (information) 4 screen(s) whose texts differ beyond the commas: the tree's short panel, where an exact fraction that just fitted its 18 characters without a comma no longer does ("1−PPV = 604/242,875") and the panel gives its digit count instead ("1−PPV: 9 digits").
- **C** every text the program hands the CAS or `EXPR` is beta 8f's, call for call (828 calls on these runs): the commas are for the screen only.
- **M** every number of four or more digits drawn on those runs is grouped (167 different grouped numbers drawn, among them 1,000, 3,365, 3,420, 3,421). **Y** no year, or other number the program writes as text, is drawn with a comma, nor a name with digits in it.
- **D** no new firm overlap, straddle or overrun (`text_overlap_v1`: 0 before, 0 now) and no new number cut by its width (`label_fit_v1`: 0 before, 0 now).

## Gate

`ppl_gate_v1d.py BayesTree_beta8g.txt`: no problem that beta 8f does not already have; `fleet_names_v2.py` over the 30: 0 collisions.

## The Virtual Calculator

Virtual Calculator 2.4.2 (Rogers-HP, 2 Nov 2026, night; Claude through computer use): the file the starter-pack tool built from BayesTree_beta8g.txt was copied into the calculator's folder with the calculator closed, then opened in the editor and Checked: **"No errors in the program"**. The file the calculator wrote back was collected after that Check and nothing else; it is the one in starter pack v10 and the Prime Loader v1h (`make_starter_pack_v4.py --checked` found its source equal to `programs/BayesTree_beta8g.txt`). Not yet run on a G1 or a G2.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] A number of 1,000 or more on the screen shows its commas (type 12345 where the program takes a value, or load data with large values).
- [ ] A year in a help page or a citation shows no comma.
