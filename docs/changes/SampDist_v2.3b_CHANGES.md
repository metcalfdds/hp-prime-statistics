# SampDist v2.3b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on v2.3a; every v2.3a feature is kept, and every ordinary display is unchanged. Run only in the PC harness (ppl_run_v3e), not yet on the emulator or a calculator.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 20; `findings_B.md`, SampDist) listed two items to fix now:

- **S1. WRONG TEXT (edge): the α floor prints as an exact "= 0.000001".** "`SampDist_v2.3a.txt:594` clamps the α read back from a dragged critical value to `[0.000001, 0.999999]`; `sd_compose` then prints `pv := alp` through `sd_fmtp(pv, 6)`, whose floor only fires BELOW 1e-6." Find critical value, μ 100, σ 15, n 30, α 0.05, Upper tail, red line dragged to the right edge: the panel read `P(x̄ > 144.000) = 0.000001   z = 16.0665   < 0.001%`. The true α at z = 16 is about 2E-58, and the z line already said "< 0.001%".
- **S2. COSMETIC (consistency): "the one `1 − NORMALD_CDF` the v2.3a pass did not turn round."** `SampDist_v2.3a.txt:592`, `fxP := 1 - NORMALD_CDF(mu, se, fxL)`, where `sd_prob` and Mode 1 had become `NORMALD_CDF(mu, se, 2*mu - a)` in v2.3a. The clamp hid the difference on the panel.

The reviewer offered two fixes for S1 (clamp at 1E-7, or print the floor text when the clamp fired) and preferred the first. It is used here: one number, and `NORMALD_ICDF` is fine at 1E-7.

Roger's addition of 19 October (12:48 CDT): the disclaimer line beside the distribution terms.

## What changed (line numbers: v2.3a → v2.3b)

1. **S1, the clamp** (594 → 624): `fxP := MAX(0.0000001, MIN(0.9999999, fxP));`. The comment above `sd_fix` says why (577-579 → 599-606).
2. **S2, the right tail** (592 → 622): `IF tailK == 2 THEN fxP := NORMALD_CDF(mu, se, 2*mu - fxL); END;`, with a comment.
3. **Header:**
   - the disclaimer line after the distribution terms (→ 13-15): "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes." The program has no About or Help page that states the terms, so no line was added on screen.
   - the tested-on lines (26-28 → 29-33): v2.3b has run only in the PC harness;
   - a "v2.3b (19 Oct 2026)" paragraph (→ 35-51);
   - the VERIFIED paragraph names `verify_SampDist_v2.3b.py` (218 → 239-240).

Only `sd_fix` changed: two code lines, both in that routine.

**Before and after** (harness ppl_run_v3e):

| Where (how) | v2.3a | v2.3b |
|---|---|---|
| Critical value, μ 100, σ 15, n 30, α 0.05, Upper tail, red line dragged to the right edge (doubles and 12 digits) | `P(x̄ > 144.000) = 0.000001`, `z = 16.0665   < 0.001%`, `EP_SD_P` = 1E-6 | `P(x̄ > 144.000) < 0.000001`, `z = 16.0665   < 0.001%`, `EP_SD_P` = 1E-7 |
| The same, Lower tail, dragged to the left edge | `= 0.000001` | `< 0.000001`, `EP_SD_P` = 1E-7 |
| α read back at z = 0.5 to 4.5 (upper tail), 12-digit model | relative error up to 3.7E-8 | up to 2.9E-12 |
| Any dragged position with α between 1E-6 and 1 − 1E-6 | — | the same bounds and α as v2.3a (24 positions) |

## Verification

`verify_SampDist_v2.3b.py` was built from the v2.3a script, and every check is kept. Parts A-I run on v2.3b with only the file names changed (absolute paths to `/home/claude/work/out` for the earlier versions and the harnesses, so the script runs from any folder). Part I's code diff (I5) stays v2.3a's change set (v2.3 → v2.3a). Output: `verify_SampDist_v2.3b_output.txt`: **354 checks, 0 failures** (the v2.3a script had 337).

Part J is new:
- **J1, S1.** The review's reproduction above, in doubles and under the review's `twelve_digits()`, both versions; the lower tail at the left edge.
- **J2, S1.** `sd_fix` clamps to [1E-7, 1 − 1E-7] (v2.3a [1E-6, 1 − 1E-6]); `sd_crit` at the new floor and ceiling (NORMALD_ICDF at 1E-7, 5E-8, 1 − 1E-7) = SciPy's ppf for all three tails.
- **J3, S2.** α from a bound at z = 0.5 to 5.1 against SciPy's sf: relative error 1.1E-14 in doubles and 2.9E-12 under 12 digits (v2.3a: 2.5E-12 and 3.7E-8, up to z = 4.5). 24 dragged positions inside the old clamp give v2.3a's bounds and α to 1E-12.
- **J4, the review's `check_SampDist.py`** (30 checks), run on both versions:
  - On v2.3a only S3's check fails (σ = 0.000045 prints the Prime's scientific form).
  - On v2.3b the same S3 check fails, and so do part C's three demonstrations of S1 and S2: the 1 − CDF slip, the clamp showing "= 0.000001", and a comparison written for the old 1E-6 clamp. They passed on v2.3a because the bugs were there. Every other check passes.
  - The review's own reproduction of S1 reads `< 0.000001` on v2.3b.
- **J5.** The routine diff v2.3a → v2.3b: `sd_fix` only, and in it exactly the two code lines of S1 and S2.
- **J6.** No `//` inside an open bracket; the version strings and the disclaimer; every LOCAL line holds at most 6 names; no INSTRING.
- **J7.** No scientific fixed decimal in any v2.3b run of parts I and J (121 runs). The one exception is the harness's own tick label `-5.6ᴇ-17` (a sum of 1-2-5 steps in doubles, exact BCD on the Prime; findings_B), which v2.3 and v2.3a log too.

## Gate

`python3 ppl_gate_v1b.py SampDist_v2.3b.txt _old/SampDist_v2.3a.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 2 E4, 3 E9, as v2.3a. No hard errors (E12 included).
- lint_ppl: 18 problems, as v2.3a.
- Full parse: OK, 26 functions (v2.3a the same).
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh SampDist_v2.3b.txt SampDist_v2.3a.txt`: kit lint 0 errors; the same tallies; parse OK.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.3a (open it in the Kit), then Program Catalog → Check.
2. **S1.** Find critical value: μ 100, σ 15, n 30, α 0.05, Upper tail. Drag the red line to the right edge of the plot. The panel reads `P(x̄ > 144.000) < 0.000001` and `z = 16.0665   < 0.001%`. In Home, `EP_SD_P` is `1E-7`.
3. The same with Lower tail, dragged to the left edge: `< 0.000001`.
4. **S2.** Upper tail, drag the line to about z = 2: the panel's P equals the z line's percentage, and `EP_SD_P` matches `NORMALD_CDF(0,1,-z)` for the z shown.
5. Check that an ordinary drag (z = 1.645) still reads `= 0.050000` (as v2.3a).

## Unresolved

- **S3** (small σ prints the Prime's scientific form, `σ = 4.50ᴇ−5`) is in findings_B but not in the review's "fix now" list, so it is not in this pass. The review's check of it still fails on v2.3b, as on v2.3a.
- Nothing in section 3 of the review (the open decisions) touches SampDist. The reviewer's improvements (Watch with n soft keys, one default population, `EP_SD_N`) belong to v2.4.
