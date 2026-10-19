# DNAMixLR beta 3c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 3b; every beta 3b feature is kept. dmKnowns, dmTyped and dmEval are still byte for byte beta 2's; **dmProb is rewritten** (item 3): the same probability, added up without subtraction. Run only in the PC harness (ppl_run_v3e); not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md` section 2, items 6 and 18; `findings_E.md` section 1):

> **B1** -- WRONG NUMBER (state). "`dmSetHyp` (custom path) assigns `dmHp` and `dmHd` at 1338-1339 and only then tests the unknown counts at 1340; the `RETURN` at 1342 leaves the refused values in place." ... "In the same form the 1 / 0 flags are not forced to 1 or 0 (1327, 1338-1339): 'Victim typed? = 2' gives `dmPres = {2, 1, 0}`, which every `== 1` test reads as 'not typed' while `dmAskGen`'s CASE ... asks for the victim's genotype anyway."

> **B2** -- WRONG TEXT. "Both say 'LR = 0: a known contributor under Hp has an allele the mixture does not show. Excluded.' `dmProb` returns 0 for a second reason, line 804 (`pbNU > 2 * pbX`): the known contributors plus the x unknowns cannot account for every allele of M." (Reproduction: preset 1, mixture 12, 13, 14, 15, victim 12/13, suspect 14/14.)

> **B4** -- WRONG TEXT. "`:2868`: 'ENFSI scale: LR 1-10 weak'. `dmVerbal` (436-437) and `dmBand` (1164) use 2 as the lower edge of 'weak'."

**dmProb's sum cancelled** (found while testing B2; the coordinator: "a numerical bug to fix in beta 3c itself"). `dmProb` added up P(E|H) by inclusion-exclusion, an alternating sum whose terms are about p(M)^(2x) while the answer can be a product of rare frequencies. With rare alleles and three or four unknowns (custom hypotheses) the difference fell below the 12th digit:

| Custom hypotheses, theta 0, p = 0.6, 0.0001, 0.0005, 0.0002, 0.0002, 0.0005, 0.0001 | exact LR | beta 3b (harness doubles) | beta 3b's sum in a 12-digit model |
|---|---|---|---|
| S 1/1 + 4 unknowns vs V 5/7 + 4 unknowns | 6.64E-7 | **LR = 0, "Excluded"** | P(E\|Hp) = 0 (exact 7.28E-19) |
| V 1/1 + S 2/3 + 3 unknowns vs V + 4 unknowns | 3.6E5 | **"Hd cannot produce this mixture", no LR** | P(E\|Hd) = 0, P(E\|Hp) 8.0E-13 (exact 2.60E-13) |

**Roger's addition (19 Oct 2026, 12:48):** the header line "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes."; and, because DNAMixLR is forensic-facing, the notice on screen, on its opening or About page and on every page that states a final LR.

## What changed (line numbers: beta 3b → beta 3c)

1. **B1, `dmSetHyp`** (1303-1354 → 1434-1490).
   - The unknown counts are tested **before** anything is stored (3b 1338-1343 → 3c 1478-1485): `IF IP(cuX) < 0 OR IP(cuX) > 4 OR IP(hdX) < 0 OR IP(hdX) > 4 THEN MSGBOX(...); RETURN; END;`, then `dmHp` and `dmHd` are assigned. A refused 5 or −1, under Hp or Hd, now leaves `dmHp`, `dmHd`, `dmPres` and the loci exactly as they were.
   - Every yes/no answer is stored as 1 or 0, `IFTE(IP(x) == 1, 1, 0)`: the typed persons (1327 → 1462) and the six contributor flags (1338-1339 → 1484-1485). A typed 2 is "no", as every `== 1` test already read it.
2. **B2, the reason for an LR of 0.** The locus page (`dmDrawPanel`, 2429-2432 → 2613-2645) and its formula view (`dmDrawFx`, 2346-2350 → 2501-2534) test which of `dmProb`'s rules gave P(E|Hp) = 0, the same way `dmProb` does (`dmKnowns`, `dmUSet`):
   - a known contributor's allele is outside M → "LR = 0: a known contributor under Hp has an / allele the mixture does not show.  Excluded." (unchanged text);
   - the knowns plus the `dmHp(4)` unknowns cannot supply every allele of M → "LR = 0: under Hp the contributors cannot / account for every allele of M.  Excluded."; formula view "LR = 0 for every p and theta: under Hp / the contributors cannot account for every / allele of M, so P(E|Hp) = 0.";
   - neither: with item 3 this can only be an **underflow**, a probability below the smallest number the calculator holds (about 1E-499; frequencies would have to be absurd -- the verify uses p = 1E-100). The page says "LR = 0: P(E|Hp) underflows: it is below the / calculator's smallest number.  Counted as 0." (formula view: "… below the smallest number the calculator / holds (underflow), so it counts as 0.").
   - The caption under the boxes (2474 → 2693): "0 unknown(s) cannot supply 1 allele: P = 0" (beta 3b: "1 alleles").
3. **`dmProb` adds without subtracting** (comment 764-784 → 824-896; code 785-838 → 897-966). **The model is unchanged** (NRC II 4.2 sampling of the 2x unknown alleles, conditioned on every typed allele; the knowns must lie in M; U = the alleles of M no known carries, each needed at least once). Only the way the probability is added up changed:
   - The probability of one order of draws depends only on how many copies c_a of each allele it holds: prod_a g_a(c_a) / D, with g_a(c) = prod_{i<c} [(t_a + i)θ + (1 − θ)p_a] and D = prod_{j<2x} [1 + (nT + j − 1)θ]. There are (2x)!/prod c_a! orders with those counts. So P = (2x)!/D × Σ prod_a g_a(c_a)/c_a!, over the ways to share the 2x draws among the alleles of M with c_a ≥ 1 for every allele of U.
   - That sum is built **one allele at a time**: `pbW(s + 1)` is the total for the alleles taken so far using s draws; allele a passes each total on to s + c, times g_a(c)/c!. Every number added is positive, so nothing cancels; each step costs at most one rounding in the 12th digit.
   - It *is* the inclusion-exclusion sum, rearranged (equal in exact fractions, verify V6).
   - Why not the subset-over-draws method the coordinator suggested? That method draws each allele independently with probability p_a, which holds only at θ = 0. With coancestry the next draw depends on how many copies of each allele were already seen, so the state would have to carry per-allele counts. Tracking per-allele counts directly is exact for every θ, and smaller: no 2^|U| states.
   - **Limits and size:** at most 8 alleles in M and 4 unknowns per hypothesis (2x = 8 draws, |U| ≤ 8). Per call: g for each allele, 8 × 8 = 64 products; the passes, at most 9 × 10 / 2 = 45 multiply-adds per allele, 360 in all; 8 for the final factor -- **about 430 operations**, against up to 2^8 × 16 = 4,096 for the old sum (|U| = 8). Harness timings are in Verification.
   - PPL details: no bit masks; lists built with LOCAL `MAKELIST` counters (no Home K); the two loops over `pbKn`, and the inner FOR whose finish can fall below its start, are guarded by IFs (that FOR form has not been measured on the device, review section 5). `MAX(0, …)` is gone (nothing can go negative).
   - The CAS formula view still writes the inclusion-exclusion form (`dmCasP`, code unchanged): the CAS works in exact fractions, where cancelling costs nothing. Comments updated: the model note in the header, the file map, `dmCasP`'s header, and help page 4's line "from the same model the program uses, and" (was "from the same sum the program adds up, and"; 2896 → 3129).
4. **B4, help page 2** (2868 → 3100): "ENFSI scale: LR 2-10 weak, 10-100 moderate," (same length), matching `dmVerbal` and `dmBand`.
5. **The notice (Roger, 19 Oct 2026).**
   - **Header** (→ 24): the DISCLAIMER line, verbatim, after the distribution terms.
   - **Help page 1** (2850-2856 → 3077-3086): the program opens on its menu and has no About page, so help page 1 carries "Teaching aid; not for casework or legal use." in red at y 193; the example and the genotype note above it move up 3 and 6 px (105-186 → 102-180); the footer stays at 204.
   - **The pages that state the result:**
     - Where: the Results table (`dmCombLines`, 2036-2060 → 2186-2215), every locus page (`dmDrawPanel`, 2441-2442 → 2656-2661) and the prosecutor's fallacy page (`dmDrawFall`, 2772-2773 → 2995-2998).
     - What: the two red lines "The LR is NOT the probability that the / suspect contributed." become "The LR is NOT P(the suspect contributed)." and the notice. No page grows; the Results table is full at 12 loci.
     - The locus page shows the notice at y 84 for every LR, including "LR = 0" and "no LR".
     - The Results table shows it after an exclusion too. `dmCombLines` then returns 3, not 2; no caller reads the value.
   - **The three plots have no free line**, so they show the short form "Teaching aid only" in red at the right of the title row (x 202, y 6):
     - Routines: locus plot `dmDrawLoci` 1546-1548 → 1688-1696; theta plot `dmThStatic` 1841 → 1988-1991; ladder `dmLadFrame` 2585 → 2804-2808.
     - The titles move left: locus plot x 100 → 60, waterfall x 70 → 8, theta plot x 30 → 24. The ladder's title is now "ENFSI ladder by locus".
     - The title tap reads only y < 22, so it is unaffected.
6. **Header:** the banner "beta 3c"; the firmware lines (3b ran in the round-2 retest; 3c only in the harness); a "What changed in beta 3c" paragraph (38-92), in beta 3b's line numbers, with an item for dmProb.

Nothing else changed. The routines that differ from beta 3b are exactly `dmCombLines`, `dmDrawFall`, `dmDrawFx`, `dmDrawLoci`, `dmDrawPanel`, `dmHelpPage`, `dmLadFrame`, `dmProb`, `dmSetHyp` and `dmThStatic` (verify G (3c)).

**Before and after** (harness ppl_run_v3e):

| Where | beta 3b | beta 3c |
|---|---|---|
| Custom, Hp "Unknown contributors: 5" | box "0 to 4", then menu "V + S + 5 unknowns vs V + 1 unknown"; next recalculation LRs 0.118 / 0.388 / 0.0076 | box; menu unchanged; LRs 56.79 / 19.08 / 3.674 |
| "Victim typed? = 2" | `dmPres = {2, 1, 0}` | `{0, 1, 0}` |
| V 12/13 + S 14/14, mixture 12-15 | "a known contributor under Hp has an allele the mixture does not show"; "1 alleles" | "under Hp the contributors cannot account for every allele of M"; "1 allele" |
| S 1/1 + 4U vs V 5/7 + 4U, rare alleles, θ 0 | LR = 0, EXCLUDED | LR = 6.64E-7 (exact) |
| V 1/1 + S 2/3 + 3U vs V + 4U, the same | "Hd cannot produce this mixture" | LR = 357499.6 (exact 357,499.59) |
| Help page 2 | "LR 1-10 weak" | "LR 2-10 weak" |
| Results table, locus page, fallacy page | "The LR is NOT the probability that the / suspect contributed." | "The LR is NOT P(the suspect contributed)." / "Teaching aid; not for casework or legal use." |
| Locus plot, theta plot, ladder | -- | "Teaching aid only" at the top right |

## Verification

`verify_DNAMixLR_beta3c.py`, built from the beta 3b script, every check kept, harness **ppl_run_v3e**; predecessors read from `/home/claude/work/out` by absolute path (review item 22). Output in `verify_DNAMixLR_beta3c_output.txt`: **188 PASS, 0 failures** (the 3b script: 115; new: 18 in V1, 12 in V2, 2 in V3, 4 in V4, 6 in V5, 9 in V6, 22 in G (3c); one kept check is reversed, see below). Run time about 2.5 minutes.

- **Kept:**
  - Part A: every CAS template in desktop Giac = the Python engine.
  - Part B: the PPL's CAS text = the Python builder's; the CAS formula = the new dmProb through dmEval, to 1e-10; dmEdge = brentq; the formula view with Giac and failing; the cache; no CAS call in the theta drag; the stale-key run.
  - Parts G (3a), R1-R6 and G (3b), the last still on the 3a and 3b files.
  - **One kept check changed on purpose:** "dmProb byte-for-byte beta 2" was the bug. It now reads "dmKnowns, dmTyped, dmEval byte for byte beta 2's; dmProb is not", and dmProb is checked by value in V6.
- **V1, B1 (18 checks):** five refused counts (Hp 5, Hp −1, Hd 5, Hd −1, Hp 4.7 with Hd 5).
  - Beta 3c changes nothing after a recalculation. Beta 3b keeps each refused count, and its next recalculation uses it.
  - The review's menu reproduction: beta 3b's menu reads "V + S + 5 unknowns".
  - Flags: a typed 2 is stored as 0. A valid custom pair is stored and recomputed. 4 and 4 unknowns are accepted; a cancelled form changes nothing.
- **V2, B2:**
  - The three reasons, each on both views, against the Python engine's reason. Beta 3b's wrong sentence is shown beside each.
  - The underflow case is confirmed with exact fractions (exact P(E|Hp) = 2.4E-399).
  - "1 allele" / "2 alleles".
  - A sweep under 8 hypothesis pairs (384 loci, including the rare-allele shape): every LR = 0 locus shows the engine's reason, and none is left without a rule. **Every one of the 384 LRs equals the exact LR (fractions), including 25 that beta 3b's sum made 0.**
- **V6, dmProb (7 checks):**
  - The per-allele sum equals the inclusion-exclusion sum **exactly in fractions** in 1,499 random loci (1-8 alleles, 0-4 unknowns, θ 0 to 0.499).
  - The PPL dmProb equals exact fractions in 2,051 evaluations: every preset and custom pair, the CASES genotypes, ordinary and rare frequencies, θ 0 to 0.3, and |U| up to 8 with 4 unknowns. Worst relative difference 1.2E-15.
  - It also equals brute-force enumeration of every order of draws.
  - **12-digit model of the Prime (every operation rounded):** on 85 rare-allele probabilities beta 3c stays within 6.9E-12 (relative) of the exact value; beta 3b's sum is off by up to 6.9E6.
  - The two cancelling cases end to end: beta 3c shows the exact LR and no "LR = 0"; beta 3b shows EXCLUDED and "Hd cannot".
  - The largest case: about 430 operations against 4,096. Harness: 5.6 ms against 96.5 ms per call.
- **V3, B4 (2):** help page 2's line; dmVerbal and dmBand step at 2 and 10.
- **V5, the notice (6):**
  - The DISCLAIMER header line.
  - In five states, every Results table, locus page (picture and formula view) and fallacy page shows the full notice, and the three plots show the short one. It is red, inside x 316, and clear of every other text by a 6.5 / 7.6 px-per-character model, on 53 screens. Beta 3b shows neither.
  - Help page 1: the notice at y 193, between y 180 and the footer at 204.
  - The locus plot's title tap still opens the waterfall.
- **V4, the review's `check_DNAMixLR.py`** on beta 3c and beta 3b (4 checks):
  - Beta 3b scores 104 PASS / 8 FAIL; beta 3c scores 100 / 12. The B1 check now passes.
  - 7 checks still fail, waiting on open items: the six CHOOSE-width checks (D17) and dmBig "10.00E-3" (B5, not in this pass).
  - 5 checks "fail" on 3c because they **recorded** a bug (they passed while it was there): the kept −1, the stored 2, the wrong sentence on the page and in the formula view, and "1 alleles".
- **G (3c):**
  - The routine diff above, each routine by exactly its change.
  - dmProb has no subtraction, no `MAX(0, …)`, no 2^ loop, no Home K, and its loops are guarded.
  - dmKnowns, dmTyped, dmEval, dmUSet and dmCasP are byte for byte 3b's.
  - Banner and header; LOCAL lines ≤ 6 names; no comment inside a bracket; the INSTRING count is unchanged.
- **S:** 184 beta 3c harness runs, 0 scientific STRING results.
- **Time in the harness (PC):**
  - The largest single call: about 7 ms (3c) against 190 ms (3b).
  - 12 loci of 8 alleles, V + S + 2U vs V + 4U, θ 0.01: a recalculation takes 0.20 s against 0.46 s; the theta plot's curves 8.6 s against 15.0 s.
  - The G1 is far slower than the PC. These show the ratio, not the device time.

## Gate

In `gate_f19` (beta 3b moved to `_old/`): `python3 ppl_gate_v1b.py DNAMixLR_beta3c.txt _old/DNAMixLR_beta3b.txt` → **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as 3b; no W3.
- lint_ppl: 18 problems, the same 18 as 3b (STRING arguments split at commas inside ROUND/MAX; `lgG` as a GROB parameter): the tool's limits.
- Full parse: stops at the forward declaration `dmClearLoci();` (line 362; 3b at 303), the tool's limit.
- fleet_names_v2 over the newest 25 files: 0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.

`check.sh NEW OLD`: kit lint 0 errors; no hard ppl_check errors; parse fails on the same statement as 3b.

## Device checklist (emulator first, then G2 and G1)

1. **Install:** paste over beta 3b (open it in the Kit); Program Catalog → DNAMixLR → Edit → Check: no errors.
2. **The worked example is unchanged:** Load the worked example; the menu title reads "LR 3981.5"; the Results table gives 56.79 / 19.08 / 3.674.
3. **The cancelling case:**
   - Hypotheses → Custom → typed 1, 1, 0 → Hp 1, 1, 0, 3 → Hd 1, 0, 0, 4.
   - Coancestry theta → 0.
   - Enter a locus: 7 alleles (10 … 16), p 0.6, 0.0001, 0.0005, 0.0002, 0.0002, 0.0005, 0.0001; victim 1/1, suspect 2/3.
   - The locus page should read "LR = 357499.6" (exact 357,499.59), with P(E|Hp) = 2.60E-13 and P(E|Hd) = 7.28E-19.
   - Beta 3b said "Hd cannot produce this mixture".
   - Note how long the locus page takes to appear on a G1.
4. **B1:**
   - Load the worked example → Hypotheses → Custom → typed 1, 1, 0 → Hp 1, 1, 0, **5** → Hd 1, 0, 0, 1.
   - The box says "0 to 4", and the menu's first line still reads "Hypotheses:  V + S, no unknown  vs  V + 1 unknown".
5. **B2:**
   - Clear all loci → preset 1 → Enter a locus: 12, 13, 14, 15, p 0.1, 0.2, 0.15, 0.05, victim 1/2, suspect 3/3.
   - The page reads "LR = 0: under Hp the contributors cannot / account for every allele of M.  Excluded." and "0 unknown(s) cannot supply 1 allele: P = 0".
   - Press −: the three formula-view lines.
6. **B4:** Help → page 2 reads "ENFSI scale: LR 2-10 weak, 10-100 moderate,".
7. **The notice:**
   - Help page 1: the red last line is whole.
   - Also check the Results table, a locus page (y 84) and the fallacy page.
   - On the locus plot, the theta plot (drag it too) and the ladder, "Teaching aid only" is whole at the top right.
   - A tap on the locus plot's title still opens the waterfall.

## Unresolved

- **D17 (B3):** the Hypotheses sub-menu and the main menu's first line are still longer than about 31 characters (wording is Roger's); the review's six CHOOSE-width checks still fail.
- **Not in this pass:**
  - B5: `dmBig(0.009999)` prints "10.00E-3"; the review check still fails on it.
  - B6: the band-edge text above theta 0.25.
  - B7: the main menu title with an exclusion.
- **B2 wording (Roger):** an LR of 0 from "too few contributors" is still headed "Excluded"; findings_E offers "Hp cannot explain the mixture" instead.
- **The notice:**
  - The three plots carry the short form only.
  - The main menu's title ("LR 3981.5") and the summary returned to Home also state the combined LR, with no notice: a CHOOSE title has no second line, and Home's line is not a page.
  - The caution now reads "The LR is NOT P(the suspect contributed)." on three pages; help page 3 keeps the long sentence.
  - Roger to confirm the wording and placement.
- **dmProb on a calculator:** the 12-digit behaviour is shown in a model here, not on the Prime; step 3 of the checklist is the device test. The theta plot recomputes every locus at 21 thetas twice, so its G1 time at 12 large loci is worth one look.
