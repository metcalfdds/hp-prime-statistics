# BayesTree beta 8f: changes

*1 November 2026. Edited from beta 8e by hand. 3,363 lines. Fixes for what the monkey test found (the book's vetting point 6, "bulletproof under careless and random use"); for three layout faults the overlap check found on the new verify script's screens; and for a fault that trying the fixes on the Virtual Calculator turned up: on the Prime `!=` is not "not equal".*

## What the monkey test found

`tools/monkey_v1a.py` (400 runs, 150 events each, seed 11; `docs/dev/monkey-fleet-2026-11-01.md`): 352 OK, 47 HARNESS, 1 CRASH.

1. **A typed list** (47 runs). The three forms' fields were plain names, which take any type, so `{1,2}` typed as a prior went on into the arithmetic.
2. **A division by zero on a node's page** (1 run, seed 11000398). The run typed a prior of 25, a spec of 98.6 and an N of −5 into Enter values, then counts, then a second test with a sens of 7, and tapped the tree. With two tests and a small N, test 1's positives can round to 0 people, and the tree's root then holds 0. A tap on a node opened its page, which printed the node's share of N as count/N = 0/0. On the calculator `1/0` is "Error: X/0".
3. **Typed values outside their range were moved without a word.** The run's prior of 25 became 0.999, its spec of 98.6 0.999, its N of −5 10, and its sens of 7 (a student's "70 %") 0.999. The tree then showed a test the student had not asked for, and said nothing.

## What the Virtual Calculator found (1 Nov 2026, evening)

4. **`!=` is a factorial and a test on the Prime.** Typed in Home: `{3!=0, 0!=0, 3<>0, 0<>0}` gave `{0, 0, 1, 0}`, and `999!=0` gave "Error: Numerical overflow". bt_fmtp's display floor was `IF pv != 0 AND ABS(pv) < thr` (beta 8e line 721), so on the calculator:
   - the floor never ran: at a prior of 0.0001 the tree read "PPV = 9.991ᴇ-4", "prior 1.000ᴇ-4" and "1.000ᴇ-4 × LR+", where the harness showed "PPV < 0.001";
   - at a prior, sens and spec of 0.999, Esc ended the program with "BayesTree Error: Numerical overflow", twice.
   The harness reads `!=` as "not equal" and could show neither. (PowerViz's floor had the same fault, fixed in v2.5i on the evidence of Roger's calculator.)

## What changed (line numbers are beta 8f's; beta 8e's are in the header)

1. **The node page at N = 0** (`bt_NodeInfo`, 1481-1485). When N on the tree is 0, the page says "count = 0  (N is 0 here)" where the share of N was.
2. **A proportion outside 0 to 1 is refused with a sentence** (new `bt_PBad`, 1115-1124; Enter values 2783-2785; Second test 2880-2881): "sens is a proportion from 0 to 1: type 0.7 for 70 %. Nothing changed." (and the same for the prior, with "0.02 for 2 %", spec, sens 2 and spec 2). Values from 0 to 1 keep the program's limits as before (prior 0.0001 to 0.999, sens and spec 0.01 to 0.999), with no box. A number with more than 50 digits gets the fleet's sentence for it.
3. **N and the counts** (2786-2788, 2836-2848). An N outside 10 to 1,000,000: "N is the number of people at the root of the tree: 10 to 1,000,000. Nothing changed." A negative count: "A count is a number of people: 0 or more. Nothing changed." Four counts adding to more than 1,000,000 (or one count above it, checked first, so a 51-digit count never reaches the sum): "The four counts add to more than 1,000,000 people: too many for the tree. Nothing changed." beta 8e made an N below 10 into 10 and a negative count into 0.
4. **Every form field takes a real number only** (2777, 2833, 2875; 10 fields): `{pr2,[0]}`, …, the User Guide's allowed-types form.
5. **`<>`, not `!=`** (bt_fmtp, 774; cause 4). The floor now runs on the calculator as it always did in the harness.
6. **Three layout faults** (found by text_overlap_v1 over this version's verify screens; all three are in beta 8e):
   - the tree's odds line (3154-3161): "odds 999.000 × LR+ = 998001.000" (a prior of 0.999) ran into the spec number at x 168. Odds of 100 or more are whole numbers now (new `bt_fmtO`, 1130-1134): "odds 999 × LR+ = 998001". With two near-certain tests the line would still be too long ("998001 × LR+ = 997002999"), and only then is the word "odds" left out;
   - the Diagnostics page's DOR line (1608) with a capped sens or spec, "diagnostic OR = 998001   (sens or spec at its 0.999 cap)", ran past the right edge. It reads "(at the 0.999 cap)"; the sens and spec lines above it say which;
   - the two-test breadcrumb (2956-2969). A try that ran past x 102 was painted over to x 103 only, so the end of its last number (">.999" from x 80) stayed beside the slider's "prior 0.999" (a prior of 0.999 and two tests of 0.999). It is painted over as far as it reached now.
7. Header: the banner, the tested-on lines, and the beta 8f block.

Nothing else changed.

## Verification

`verify_BayesTree_beta8f.py`, output `verify_BayesTree_beta8f_output.txt`: **35 PASS, 0 FAIL**, run from a repository layout, with beta 8e read from git history (rule 18). It is a new script in the repository's layout (the 19 October scripts read the author's folders), and every run in it has `prime_facts_v1.py`'s device facts.

- **R** beta 8f against beta 8e over 50 states (priors, sens and spec at their limits and inside them, N 10 to 1,000,000, two tests, forensic labels, the leaves as probabilities): the tree, eight views and the 13 node pages, screen for screen, 450 runs. Every text is beta 8e's but for the two lines of change 6 that changed wording, which are checked by value: R2, every odds line at most 26 characters, odds of 100 or more whole; R3, the DOR line's cap note.
- **B** the Exact page and the tree's exact panel with the desktop CAS (icas): identical in both versions, three cases.
- **M** one check per finding, each also run on beta 8e, where it fails:
  - M1: the 3 forms' 10 fields are all `{name,[0]}`; beta 8e's were bare names.
  - M2: two tests at N = 10 (prior 0.0001, sens 0.01, spec 0.999; test 1's positives 0.01 people): all 13 node pages open, and the six count pages say "count = 0  (N is 0 here)"; beta 8e stops with a division by zero.
  - M3: the monkey's own run, seed 11000398, replayed with `monkey_v1b.py`: beta 8f OK, beta 8e CRASH.
  - M4: 13 refused values (prior 25 and −0.1, sens 7 and 70, spec 98.6 and 1.0001, sens 1E60, N 9.9, −5, 1,000,001 and 1E60, sens 2 = 7, spec 2 = −0.5): the sentence, and nothing changed (the summary and every screen as with OK on the untouched form); beta 8e showed no box and changed the tree.
  - M5: the ends accepted as before (prior, sens and spec 0 and 1; N 10, 1,000,000 and 10.7), no box, every screen as in beta 8e.
  - M6: Enter counts with −3, with counts adding to 1,000,001, with 1E60: the sentence, nothing changed; counts adding to exactly 1,000,000 accepted as in beta 8e.
  - M7: Cancel on each form changes nothing and shows no box.
  - M8: every new box fits 4 lines at 32 characters a line.
- **G** static: only `BayesTree`, `bt_DiagView`, `bt_NodeInfo`, `bt_fmtp` (its one line) and the new `bt_PBad` and `bt_fmtO` differ from beta 8e (and `bt_BEp`'s block, which the new routines follow; its code is beta 8e's character for character); G4, no `!=` in the code (beta 8e had one); every routine tagged `bt_`; at most six names per LOCAL line; beta 8e's glyphs.
- **D** text_overlap_v1 over every beta 8f screen drawn: no firm overlap, straddle or overrun. On the same runs beta 8e has the three of change 6.

**The monkey test again** (`monkey_v1b.py`, 1,000 runs, 150 events each, seed 11): beta 8f **1,000 OK**; beta 8e 860 OK, 139 HARNESS (a typed list reaching `MAX` or `IP`) and 1 CRASH (the division by zero of seed 11000398).

## Gate

`ppl_gate_v1d.py BayesTree_beta8f.txt BayesTree_beta8e.txt`: **RESULT: PASS**. Kit lint 0 errors, no hard errors, the same E4/E5/E9 tally as beta 8e; lint_ppl v3's 4 lines are beta 8e's (the file name and the EXPORT). The full parse stops at the √ in a string, the kit's limit, as for beta 8e. `fleet_names_v2.py` over all 30 programs: 2,264 routine names, 0 collisions.

## The Virtual Calculator (1 Nov 2026, 17:57–18:12 CST)

Virtual Calculator 2.4.2 (build 2026-09-09), calculator `Prime`, Rogers-HP, by Claude through computer use. Built by hp-prime-kit, copied in with the calculator closed.

1. **Check:** "No errors in the program", the build with `!=` and the final one.
2. **The build with `!=`** (everything else as now):
   - Enter values, sens 7: "sens is a proportion from 0 to 1: type 0.7 for 70 %. Nothing changed." (3 lines); the tree as before;
   - prior 0.0001, sens 0.01, spec 0.999, N 10, then Second test 0.9 / 0.95: the root reads 0; a tap on D+ opened "D+ — really have it" with "count = 0  (N is 0 here)", no error;
   - prior, sens and spec 0.999: "odds 999 × LR+ = 998001", ending well before the spec number; More → Diag: "diagnostic OR = 998001   (at the 0.999 cap)", inside the screen;
   - but at a prior of 0.0001 the tree read "PPV = 9.991ᴇ-4", and at 0.999 × 3 Esc gave "Error: Numerical overflow" (twice). Then the Home tests of cause 4.
3. **The final build:** at 0.999 × 3, Esc ended normally: "BayesTree: PPV = 1.000 = 998001/998002, …"; at a prior of 0.0001 the tree read "prior < 0.001", "PPV = 0.002" and "odds < 0.001 × LR+ = 0.002".
4. **The checked file** (326,700 bytes, +8,926) was collected after a Check and nothing else, and read back equal to `programs/BayesTree_beta8f.txt`. Starter pack v7 carries it.

## Device checklist (G1 and G2)

1. Enter values, sens = 7: "sens is a proportion from 0 to 1: type 0.7 for 70 %. Nothing changed." The tree is unchanged.
2. Enter values, sens = `{1,2}`: the form refuses it ("Invalid input") and stays open.
3. Enter values: prior 0.0001, sens 0.01, spec 0.999, N 10. Second test 0.9 / 0.95. Tap the D+ box: "count = 0  (N is 0 here)", no error.
4. Enter values, prior 0.999, sens 0.999, spec 0.999: the odds line under the root reads "odds 999 × LR+ = 998001" and ends before the spec number. Esc: the summary in Home, no error.
5. More → Diag with sens 0.999: "diagnostic OR = … (at the 0.999 cap)" inside the screen.
6. Enter values, prior 0.0001: the tree reads "PPV = 0.002" and "prior < 0.001" (not "1.000ᴇ-4").
7. Enter counts −3 in any cell: the counts box; the tree is unchanged.

## Unresolved

- With two tests, the D+ node's page still says "Before any test is run. The prior is the prevalence." although the stage's N is test 1's positives and its prior is test 1's PPV (seen on the Virtual Calculator at N = 0). The wording is beta 8e's; for the next version.
- Norm3 v2.4b and StatDist v2.7f still carry `!=` (`docs/dev/monkey-fleet-2026-11-01.md`, round 2).
