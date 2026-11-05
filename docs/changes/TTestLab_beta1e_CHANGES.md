# TTestLab beta 1e: changes (4 November 2026)

**Run, not OK, on the flowchart.** Roger, 4 Nov 2026: "in our apps please make sure we don't have that issue with an 'OK' key---I think use 'Run' or 'Solve' or 'Exit' but NOT 'OK' the way they use it". On the Prime's own screens OK closes the screen (the Probability Wizard's OK, beside Solve, quits it), so a student who has set a problem up and taps OK expects to leave. The flowchart's sixth soft key, which goes on with the test chosen, now reads **Run**; its footer reads "Tap Yes or No (or the soft keys); Run = run the test", and the help page's line says the same. The key's code (6), Enter, and every path are unchanged.

**Checks.** `verify/verify_round7_labels_v1.py`: the code differs from beta 1d only inside the three string literals named here (L1–L3 pass). The gate passes. The monkey test, 1,000 runs: 1,000 OK.

**On the Virtual Calculator** (2.4.2, build 2026-09-09, running in the cloud workspace under Wine, 4 Nov 2026; Lessons Learned v7zm, §16): opened in the editor and Checked: "No errors in the program". The file the calculator wrote back after that Check is the one in starter pack v12. Then TTESTLAB from Home: the flowchart showed Yes, No, Back, and Run; Yes, No, then Run went on to "The data".
