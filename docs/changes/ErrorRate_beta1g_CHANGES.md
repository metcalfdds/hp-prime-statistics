# ErrorRate beta 1g: changes (4 November 2026)

The Engines help page ended "Nothing here has run on a calculator yet", which was no longer true. It now ends "It has run on the Virtual Calculator." Nothing else changed; it has still not run on a G1 or G2.

**Checks.** `verify/verify_round7_labels_v1.py` L1–L3 pass; the gate passes.

**On the Virtual Calculator** (2.4.2, build 2026-09-09, running in the cloud workspace under Wine, 4 Nov 2026; Lessons Learned v7zm, §16): opened in the editor and Checked: "No errors in the program". The file the calculator wrote back after that Check is the one in starter pack v12. Then ErrorRate from Home: the welcome page; the main plot (0 errors in 30 tests, upper bound 9.50 %); Why 3, with its lines marked exact (CAS); Eng, whose live checks read "1/2+1/3 = 5/6, as it should" for the CAS and "MicroPython answers"; and the help pages through Three engines, with the new last line.
