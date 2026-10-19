# BayesTree beta 8d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on beta 8c; every beta 8c feature is kept, and every ordinary display is unchanged. Not yet run on hardware or on the emulator.*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18). `bt_fmtp` writes `< 0.001`, or `> -0.001`, below its floor. 38 displays and `bt_FrLn` put that after `= `. For example, at a prior of 1 in 10,000:
- the tree's panel read `PPV = < 0.001`;
- the node page read `PPV = TP / (TP + FP) = < 0.001` and `prior = < 0.001 (1 in 10000)`;
- the summary returned to Home read `BayesTree: PPV = < 0.001, …`.

A test with sens 0.5 and spec 0.4996 read `Youden J = > -0.001`. The right form drops the "=": `PPV < 0.001`.

## What changed (line numbers: beta 8c → beta 8d)

1. **New `bt_Eq(eqS)`** (→ 693-699, after `bt_fmtp`). It returns `" = 0.161"`, or `" < 0.001"` / `" > -0.001"` when `bt_fmtp` has already written the relation. It reads `LEFT(eqS, 1)` only inside `IF DIM(eqS) > 0`, and it uses no INSTRING.
2. **The 38 displays.** Each `"label = " + bt_fmtp(…)` becomes `"label" + bt_Eq(bt_fmtp(…))`:
   - **the node page:** 1142, 1148, 1172, 1187, 1192, 1200, 1206, 1240, 1263, 1270 → 1182, 1189, 1214, 1230, 1236, 1245, 1252, 1287, 1311, 1319;
   - **the 2 × 2 view:** 1360, 1365 → 1410, 1416;
   - **the diagnostic view:** 1409, 1412, 1414-1417 → 1461, 1465, 1468-1474. The diagnostic OR and Cohen κ are strings already, so they read `"diagnostic OR" + bt_Eq(sDOR)` and `"Cohen κ" + bt_Eq(sKap)`.
   - **the prevalence view:** the prior readout at the cursor and the PPV and NPV, 1536-1538 → 1594-1598. The view starts at the tree's prior, which can be 0.0001.
   - **ROC:** 1639, 1675 → 1700, 1737;
   - **Fagan:** 1875, 1876 → 1938, 1940;
   - **three prevalences:** 2011 → 2076;
   - **the tree's panel:** 2780, 2783, 2786, 2824, 2825, 2830, 2831, 2836 → 2855-2918;
   - **the summary:** 3028 → 3111.
3. **`bt_FrLn`** (2031-2036 → 2096-2111) writes the Exact page's `    = 19/118 = 0.161` lines.
   - **No fraction** (the CAS failing): the lead's closing `" = "` gives way to `bt_Eq`. The page reads `    < 0.001  (decimal)`, not `    = < 0.001  (decimal)`. `RIGHT(flA, 3)` and `LEFT(flA, DIM(flA) - 3)` are read only when `DIM(flA) > 3`.
   - **A fraction:** `bt_Eq` sits between the fraction and the decimal: `    = 1/989902 < 0.001` and `    prior = 1/998002 < 0.0001 = 0.000 %`.
4. **Header:**
   - the banner (4);
   - the tested-on lines (13-14, 19-20);
   - a "beta 8d" paragraph (→ 23-46).
   - A comment above each changed statement says what it does. Every comment sits at bracket depth 0.

**Before and after** (harness ppl_run_v3e, reached as noted):

| Where (how) | beta 8c | beta 8d |
|---|---|---|
| Diagnostic view (`bt_DiagView`, prior 1 in 10,000, sens = spec = 0.01) | `prevalence = < 0.001`, `F1 = < 0.001`, `diagnostic OR = < 0.001   (LR+/LR−)`, `Cohen κ = > -0.001` | `prevalence < 0.001`, `F1 < 0.001`, `diagnostic OR < 0.001   (LR+/LR−)`, `Cohen κ > -0.001` |
| the same, sens 0.5, spec 0.5004 | `Youden J = < 0.001   (se+sp−1; …)`, `Cohen κ = < 0.001`, `MCC = < 0.001` | `Youden J < 0.001   (…)`, `Cohen κ < 0.001`, `MCC < 0.001` |
| the same, spec 0.4996 | `Youden J = > -0.001 …` | `Youden J > -0.001 …` |
| 2 × 2 view; forensic at prior 0.999 | `cols:  PPV = < 0.001`; `… = 1 − PPV = < 0.001` | `cols:  PPV < 0.001`; `… = 1 − PPV < 0.001` |
| Prevalence view (prior 0.001; prior 0.0001) | `PPV = < 0.001`; `prior = < 0.001:` | `PPV < 0.001`; `prior < 0.001:` |
| Fagan, three prevalences | `→ PPV = < 0.001`, `PPV = < 0.001` | `→ PPV < 0.001`, `PPV < 0.001` |
| Tree panel (Enter values: prior 0.0001, sens = spec = 0.01) | `PPV = < 0.001`, `odds = < 0.001 × LR+ = < 0.001` | `PPV < 0.001`, `odds < 0.001 × LR+ < 0.001` |
| Tree panel, forensic, prior 0.999; prior 0.999, sens = spec = 0.01 | `1−PPV = < 0.001`; `NPV = < 0.001` | `1−PPV < 0.001`; `NPV < 0.001` |
| Summary to Home | `BayesTree: PPV = < 0.001, NPV = 0.990 (…)` | `BayesTree: PPV < 0.001, NPV = 0.990 (…)` |
| Exact page, CAS failing / answering | `    = < 0.001  (decimal)` / `    = 1/989902 = < 0.001` | `    < 0.001  (decimal)` / `    = 1/989902 < 0.001` |
| Exact page, two tests of 0.999 / 0.999 | `    prior = 1/998002 = < 0.0001 = 0.000 %`, `    your numbers: p = 1/998002 = < 0.0001` | `    prior = 1/998002 < 0.0001 = 0.000 %`, `    your numbers: p = 1/998002 < 0.0001` |
| Node pages (`bt_NodeInfo`, every node, plain and forensic) | `prior = < 0.001 (1 in 10000)`, `PPV = TP / (TP + FP) = < 0.001`, `which is 1 − PPV = < 0.001.`, `NPV = TN / (TN + FN) = < 0.001` | `prior < 0.001 (1 in 10000)`, `PPV = TP / (TP + FP) < 0.001`, `which is 1 − PPV < 0.001.`, `NPV = TN / (TN + FN) < 0.001` |
| Defaults (prior 0.1, sens 0.9, spec 0.95) | `PPV = 2/3`, `NPV = 171/173`; summary `BayesTree: PPV = 0.667 = 2/3, NPV = 0.988 (…)` | the same |

**Left alone (checked):**
- **Lines whose values cannot reach the floor.** These are sens, spec, 1 − sens, 1 − spec, 1 − prior, RMP, LR+, LR−, accuracy, balanced accuracy and NND. Every assignment of sens, spec or prior from the student clamps to at most 0.999 and at least 0.001 or 0.01 (prior 0.0001). That is 8 lines (beta 8c 2518-2520, 2559-2561, 2582-2583), so these lines stay at 0.001 or more.
- **The icon view's shares** are counts out of at most 1,000 icons, so each share is at least 0.001, or exactly 0, which prints `0.000`.
- **Two lines have no "=" directly before the relation**, and they stay as they are: `D+ = N × prior = 1000 × < 0.001` and `count = 0  (< 0.001 of N)`.

## Verification

`verify_BayesTree_beta8d.py` was built from the beta 8c script, and every check is kept. It runs on beta 8d in harness **ppl_run_v3e**, which gives v3d's results. Part G (8c) still compares the beta 8c and 8b files. Output is in `verify_BayesTree_beta8d_output.txt`: **235 PASS, 0 FAIL**. The beta 8c script gave 185; run unchanged on beta 8d, it gives 184 PASS, and its one failure is G's routine list, as intended.

- **T1.** Every row of the table, in beta 8c and in beta 8d:
  - the six views, called directly;
  - the tree and the summary, through the menu and the Values form;
  - the Exact page with the CAS failing, answering, and with two tests;
  - 26 node pages each for three cases.

  Beta 8d's text is beta 8c's with `= <` written `<`, and nothing else.
- **T2.** A sweep of 160 states (5 priors × 4 sens × 4 spec, plain and forensic). Each covers the tree, the summary, and the diagnostic, 2 × 2, prevalence, Fagan and three-prevalence views. 57 are identical and 103 differ only by that rewrite (74 distinct lines).
- **T3.** `bt_Eq`, including `""` → `" = "`. Also `bt_FrLn` with and without a fraction, and with a lead that does not end in `" = "`.
- **T4.** The input clamps above, and no `= <` / `= >` anywhere in the T2 sweep.
- **T5.** The code:
  - The code lines removed are exactly the 38 sites and `bt_FrLn`'s two (37 lines). The code lines added are those sites through `bt_Eq`, `bt_FrLn`'s new branch, and `bt_Eq` itself (49 lines).
  - `bt_Eq` and `eqS` are not built-ins, ignoring case. `bt_Eq` is defined once, after `bt_fmtp` and before its first use.
  - The banner and the tested-on lines say beta 8d. No code line names beta 8c.
  - No comment sits inside an open bracket.
  - INSTRING is as in beta 8c. Every LOCAL line holds 6 names or fewer.
- **R8 (kept).** No `STRING(x, 2, d)` of beta 8d printed in scientific form in any of the 1,445 harness runs.

## Gate

`python3 ppl_gate_v1b.py BayesTree_beta8d.txt BayesTree_beta8c.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 1 E4, 2 E5, 1 E9, the same as beta 8c. There are no hard errors, E12 included.
- lint_ppl: 20 problems, the same as beta 8c.
- Full parse: it stops at `√` (1450), as beta 8c does at 1399. This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 8c (open it in the Kit). Then Program Catalog → Check.
2. **Values:** prior 0.0001, sens 0.01, spec 0.01.
   - The panel reads `PPV < 0.001`.
   - The Diagnostics view reads `prevalence < 0.001` and `F1 < 0.001`.
   - The PPV-vs-prevalence view reads `prior < 0.001:` and `PPV < 0.001`.
   - Esc: Home shows `BayesTree: PPV < 0.001, …`. None of these shows `= <`.
3. **Exact page, the same values:** the decimal line reads `    = 1/989902 < 0.001` with the CAS answering. Then the defaults (prior 0.1, sens 0.9, spec 0.95): the panel still reads `PPV = 2/3`, with its "=".
