# EpiStats v1.7h: changes (4 November 2026)

**The monkey test's first run on EpiStats.** 1,000 runs of random keys, taps, menu picks, and typed values (`tools/monkey_v1b.py`, `--lists`) on v1.7g: **838 OK, 161 HARNESS, 1 CRASH**, the same on v1.7g and on a v1.7h with only its label changed.

- 161 runs typed a list into a number field, which then went into the arithmetic: the forms were untyped. **Every field of all 12 forms now takes a real number only**, `{name,[0]}`. On the Virtual Calculator, `{1,2}` typed into the two-means form's δ gave "Error: Invalid input", and the field kept its value: so the typed form works for a routine's own LOCALs too (Lessons Learned v7zm, §4).
- 1 run crashed: δ = 1E-300 in the two-means sample size, whose square underflows to 0, so n divided by zero. **The four sample-size forms now refuse**, with a sentence, a number of more than 50 digits, and an effect so small that n would pass 100,000,000, checked as a ratio before anything is squared or divided; **n is at least 1** (σ = 1E-300 squared underflows, and n came out 0).

With lists refused, the monkey went further and found three more things, fixed in the same version:

- The incidence-rate form: 1E300 cases over a person-time of 1E-300 overflowed. Cases are now at most 9,999,999, as in the 2 × 2 forms, and a person-time from 0.000001 to 1E15.
- The Clinical Impact page drew an attributable fraction of −14,285,700.0 % at x = 230, past the screen's edge. Every percentage below −9,999 % now reads "< −9,999%", and above 99,999 % "> 99,999%" (`es_FmtPct`); the incidence page's attributable proportions the same.
- The entry grid's corner cut "N = 1,000,212"; an N of 1,000,000 or more now takes two lines there. On the two sample-size pages a total N of 1,000,000 or more gets its own line.

And the About page named v1.7f, a version behind (rule 13); it and the menu title name v1.7h.

**Checks.** `verify/verify_EpiStats_v1.7h.py`: 11 PASS, 0 FAIL: every form typed; only the routines named here differ from v1.7g; SciPy's n for ordinary values, as v1.7g gave; the refusals; v1.7g's crash reproduced; an effect just above the cap computed; the percentages; the incidence form; no new overlap or cut number (comma_check's 30 seeds). The gate passes. **The monkey test, 1,000 runs: 1,000 OK.**

**On the Virtual Calculator** (2.4.2, build 2026-09-09, running in the cloud workspace under Wine, 4 Nov 2026; Lessons Learned v7zm, §16): opened in the editor and Checked: "No errors in the program". The file the calculator wrote back after that Check is the one in starter pack v12. On it: `{1,2}` refused in δ; δ = 1E-300 refused with "The difference is too small a part of σ: n would pass 100,000,000 per group. Use a larger difference."; δ = 0.001, σ = 2 gave n = 62,791,038 per group (SciPy: 62,791,038) with N = 125,582,076 on its own line; a person-time of 0.0000001 refused with "Person-time must be from 0.000001 to 1E15."; the About page reads EpiStats v1.7h.
