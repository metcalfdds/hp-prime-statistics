# ChiTable beta 3i: changes (4 November 2026)

The party-identification example is the **2000** General Social Survey (Agresti 2007, *An Introduction to Categorical Data Analysis*, 2nd ed., Table 2.5), not 1991: its label now reads "Party ID by gender (GSS 2000, Agresti)", and the comment above the examples says 2000. Nothing else changed.

**Checks.** `verify/verify_round7_labels_v1.py` L1–L3 pass; the gate passes; the monkey test, 1,000 runs: 1,000 OK.

**On the Virtual Calculator** (2.4.2, build 2026-09-09, running in the cloud workspace under Wine, 4 Nov 2026; Lessons Learned v7zm, §16): opened in the editor and Checked: "No errors in the program". The file the calculator wrote back after that Check is the one in starter pack v12. Then Examples → 3: the observed and expected counts as before (χ² = 30.07); the What it means page reads "Party ID by gender (GSS 2000, Agresti)".
