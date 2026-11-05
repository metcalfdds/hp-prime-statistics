# TTestLabG beta 1d: changes (4 November 2026)

Made from beta 1c by `make_round8c.py`: **"t test" now reads "t-test"** on every screen and in the comments (8 places), as in the book (Roger, 4 Nov 2026). The same number of characters, so no line moves. Nothing else changed.

## The monkey test

`tools/monkey_v1b.py`, 1,000 runs: **1000 of 1,000 OK**.

## Checks

- `verify/verify_round8_v2.py` (output `verify_round8_v2_output.txt`): 63 PASS, 0 FAIL. For TTestLabG: T1 (the forms typed), T2 (beyond the typing, and with every "t test" of the old version read as "t-test", only the routines named in the script differ), T3 (the header), T4 (line by line, the old file with the hyphens, the header and the note, and nothing else).
- `tools/ppl_gate_v1d.py` against beta 1c: pass.

## The Virtual Calculator

Virtual Calculator 2.4.2 (build 2026-09-09), running in the cloud workspace under Wine, 4 Nov 2026 (Lessons Learned §16): the file built from `TTestLabG_beta1d.txt` was copied into the calculator's folder with the calculator closed, opened in the editor and Checked: **"No errors in the program"**. The file the calculator wrote back on Exit reads back as `TTestLabG_beta1d.txt` exactly; it is the one in starter pack v13 and the Prime Loader v1k. Then TTESTLABG from the Program Catalog: the flowchart titled "Which t-test?" (the book's Figure 11.3 is that screen); PowerViz's help pages 4 and 5 were looked at too, and every line fits. Not yet run on a G1 or a G2.

## Device checklist

- [ ] Check: "No errors in the program".
- [ ] Every "t test" on the screen reads "t-test", and no line runs off the screen.
