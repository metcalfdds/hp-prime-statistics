# CICatcher beta 2b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 2a; every beta 2a feature is kept, and the user's guide (`cicatcher-guide_beta2.md`) still applies, apart from the one setup-menu line below. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed (round 2)

Beta 2a ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09, the calculators' firmware) on 17 October 2026, round 2:

> Setup menu: "Proportion: Exact (Clopper-Pearson)" is cut ("…Clopper-Pear").

The same round found two string behaviours, typed in Home, that the PC harness had not modelled:

| Typed in Home | The Prime's answer |
|---|---|
| `INSTRING("", "a")` | **Error: Invalid input** |
| `STRING(0.096, 2, 1)` | `"9.6ᴇ-2"`: fixed decimals turn **scientific** whenever 0 < \|x\| < 10^-d |

CICatcher's CAS never failed on the emulator, so the fallback was not reached there. Harness v3d shows the problem: `cqCas` sets `cR := ""` when the CAS fails, then tests `INSTRING(cR, "undef")`, and the program stops (`audit_v3d/CICatcher_beta2a.txt`).

## What changed (line numbers: beta 2a → beta 2b)

1. **cqCas** (2a 505–528 → 2b 555–583). After the quote strip, the undef / error / infinity tests run only when `DIM(cR) > 0` (2b 576–578). The `IFERR` line, the quote strip and the badge lines (`cqCasOK`) are byte-identical.
   - **No other INSTRING.** The file has no INSTRING besides these three tests, which share one line.
   - **LEFT and MID are safe.** The one LEFT (2a 517) takes 1 character, and runs only when DIM ≥ 2. Every MID starts at 1 or later (cqCas; cqTimes, from 1 to DIM).
2. **The setup menu** (cqSetup, 2a 1562 → 2b 1621). "Proportion: Exact (Clopper-Pearson)" (35 characters) is now **"Proportion: Exact (C-P)"** (23). The comment about it sits above the CHOOSE, not inside the list.
   - **Why not the brief's "Proportion: Clopper-Pearson":** the word "Exact" is what the rest of the program uses. The header line reads "Exact, p = 0.10, n = 20", the start-up message says "Exact is off", help page 4 is "Exact intervals: never below", and the guide says Exact throughout. Help page 4 spells out "Exact (Clopper-Pearson)".
   - **The other CHOOSE lines** are 28 characters or fewer, except the main menu's first, "New setup: interval, population, n" (34). That line was shown in full in rounds 1 and 2, so it is not changed.
3. **Fixed decimals.**
   - **cqF** (2a 264–267 → 2b 307–310) prints x̄, s, p̂, every interval end, "missed by" and the closed form's decimal. It now returns `STRING(ROUND(fmV, fmD) + 0, 2, fmD)`.
     - An Exact interval for 1 "yes" in 100 starts at 0.00025; beta 2a printed "2.531ᴇ-4".
     - A Wilson end for 0 "yes" answers can come out a hair below 0 in binary arithmetic; beta 2a printed "-5.55ᴇ-17" in the harness. "+ 0" turns the rounded −0 into 0, so it reads "0.00", not "-0.00".
   - **cqPct** (2a 291–295 → 2b 341–345), the caught-percentages, rounds first. 1 of 2,000 caught reads 0.1. A share under 0.05 % takes a very unlucky run, but the guard costs nothing.
   - **cqNumS** (2a 271–280 → 2b 318–328) prints a parameter as typed. A typed μ or σ below 0.0001 now gets two significant digits ("0.000030", "0.000010") instead of "3.0000ᴇ-5". p is held to 0.01–0.99, so it never reaches this.
   - **Left as they were, and why:**
     - the level, 50 to 99.9 % (cqLvS);
     - the counts (d = 0);
     - the axis labels, which are whole multiples of the step: `daK * cqStp`, so 0 is exactly 0.
4. **Header.**
   - "beta 2b" in the banner.
   - The firmware lines: what rounds 1 and 2 showed, and the harness is now v3d.
   - The companion-file list adds this file and notes the guide's one changed menu line.
   - A "beta 2b" paragraph with beta 2a's line numbers.

Nothing else changed. The verify script checks that the routines that differ from 2a are exactly cqCas, cqF, cqNumS, cqPct and cqSetup, each by exactly the change listed.

## Verification

`verify_CICatcher_beta2b.py`, built from the 2a script and run in harness **ppl_run_v3d**. Beta 1's suite (F) now runs in v3d too. Output in `verify_CICatcher_beta2b_output.txt`: **PASS, 131 checks, 0 failures.** The 2a script had 55.

- **Kept:**
  - A–D: the exact interval against statsmodels, the coverage bookkeeping, coverage by enumeration, and 20,000 PPL samples;
  - E: the scripted sessions in both CAS modes, and 1,728 CAS templates;
  - F: beta 1's suite, 71 checks, all passing;
  - G: beta 2 in v3d still echoes its own text.
- **R1:**
  - cqCas with the CAS failing returns "" with no error, and cqCasOK is 0;
  - with Giac, `1-(1/40)^(1/20)` is kept, and 1/0, 0/0 and an infinite limit are refused;
  - **beta 2a's cqCas stops in v3d** on the same failed call (INSTRING).
- **R2:** the E session with `cas='fail'` (Exact, +50, the 0-yes line, the level drag, Up, six help pages, Quit) runs to Quit, with all 8 closed-form frames "decimal". **Beta 2a stops in the same session.**
- **R3:**
  - 13 CHOOSE lines; the new Exact item is 23 characters;
  - beta 2a's two lines over 30 were the cut one and "New setup: interval, population, n";
  - in a run, the new line is shown and item 5 still sets Exact ("Exact, p = 0.10, n = 20").
- **R4:** five setups, each with +50 twice, eight picked lines, a level drag from 50 % to 99.9 % and the four arrow keys, in both CAS modes. The setups:
  - Exact, p 0.01, n 100;
  - Wald, p 0.05, n 20;
  - Wilson, p 0.01, n 5;
  - z with a typed μ = 0.00003 and σ = 0.00001;
  - t with μ = 0.0004, σ = 0.0002, n = 2.

  **Beta 2b: 0 scientific strings.** Beta 2a printed 7, 0, 1, 144 and 8 in the same runs. The Wilson 0-yes line reads "p̂ = 0/5 = 0.00: 0.00 to 0.60" (beta 2a: "-5.55ᴇ-17 to 0.60"). The typed parameters read "μ = 0.000030, σ = 0.000010".
- **R5, the helpers on edge values:** cqF (8), cqNumS (9), cqPct (5).
- **S, h.sci_strings over every beta 2b run in the script:** 37 runs, **0 scientific strings**.
- **G:** the routine diff is as listed.

## Gate

In `gate_r2`, `python3 ppl_gate_v1b.py CICatcher_beta2b.txt CICatcher_beta2a.txt` gives **RESULT: PASS**.
- **ppl_check_v4:** clean, as for 2a.
- **lint_ppl:** 11 problems (2a: 8). The 3 new ones are "STRING() with 4 args" on the ROUND forms in cqF, cqNumS and cqPct. lint_ppl splits at every comma, so this is the tool's limit.
- **fleet_names_v2:** 0 collisions, 0 untagged.

`check.sh`:
- kit lint: 0 errors;
- the full parse stops at the file-level `EXPORT`, as 2a's does.

## Device checklist (emulator first, then G2 and G1)

1. **Paste, then Check:** Program Catalog → CICatcher → Edit → Check. "No errors".
2. **The setup menu:** Menu → New setup. All five lines show in full, the last "Proportion: Exact (C-P)". Pick it: the header reads "Exact, p = 0.10, n = 20".
3. **Small values:** New setup → Exact, p 0.01, n 100 → +50. Tap a line with one "yes": its interval starts at "0.000", never with a ᴇ.
4. **Wilson, 0 "yes":** New setup → Wilson, p 0.01, n 5 → +50. Tap a line with 0/5 and drag the level edge up and down. The lower end reads "0.00", never "-0.00" or a ᴇ.
5. **The CAS step from 2a still holds:** Exact at the defaults, +50, a 0-yes line shows `upper = 1-(1/40)^(1/20) = 0.1684` with "exact (CAS)".

## Unresolved

- **The guide.** `cicatcher-guide_beta2.md` still lists the item as "Proportion: Exact (Clopper-Pearson)". It needs one line changed in its next version.
- **Means with a σ below about 0.0001.** cqVDec stops at 4 decimals, so x̄ and the interval ends read "0.0000", rounded and not scientific, while the header shows the typed values. That was already so in 2a, apart from the ᴇ. Widening cqVDec would be a display change, not a round-2 fix.
- The fallback (the "decimal" badge) has never been seen on the emulator, because its CAS never failed. The harness shows that it completes.
