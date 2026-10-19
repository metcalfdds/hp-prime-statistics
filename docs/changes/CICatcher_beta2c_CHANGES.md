# CICatcher beta 2c: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 2b; every beta 2b feature is kept, and no number changed. Run on the PC harness only: not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2, item 20; details in `findings_C.md`, section 2) found no crash and no wrong number in CICatcher: "ship after one menu line". It listed two lines a character or two too wide for their boxes:

> **C-C1. COSMETIC. Menu line cut.** `:1854` "New setup: interval, population, n" is 34 characters. Evidence: the same list-form CHOOSE cut "Proportion: Exact (Clopper-Pearson)" (35) after 31 on the emulator (header 45-47). The student sees "New setup: interval, populatio".

> **C-C2. COSMETIC (guess).** `:1723` "exact ends: bisection on BINOMIAL_CDF (checked)" is 47 characters against the header's own 46-character limit for `cqPage` (296-px clip; 47 × 6.5 = 305 px).

It also listed review item 22: `verify_CICatcher_beta2b.py` stops with `FileNotFoundError` in a folder holding only the current versions, because it opens beta 2, 2a and beta 1's `verify_CICatcher.py` beside itself.

## What changed (line numbers: beta 2b → beta 2c)

1. **C-C1, the main menu** (`cqMenu`, 1854 → 1897). "New setup: interval, population, n" (34 characters) is now **"New: interval, population, n"** (28, the length every other CHOOSE line in the program keeps to).
   - **Why not the review's "New setup: interval, data, n":** the setup asks for the population's true values (μ and σ, or p), not for data; its form is titled "Population and sample". The three things a new setup asks for keep their names, and "New" still matches help page 1's "Menu = new setup, …".
   - A comment above `cqMenu` says why (1884–1891), outside the list.
2. **C-C2, help page 4's last line** (`cqXEngS`, 1723 → 1758). "exact ends: bisection on BINOMIAL_CDF (checked)" (47) is now **"exact ends: bisection on BINOMIAL_CDF, checked"** (46). The meaning is the same: BINOMIAL_CDF passed `cqBinCheck` at the start. The other branch, "exact: OFF (BINOMIAL_CDF failed its check)" (42), is unchanged. A comment above the routine says why (1752–1755).
3. **Header.**
   - The banner says beta 2c (4).
   - **Roger's disclaimer** (19 Oct 2026, 12:48), under the distribution terms (→ 15–17): "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes." A comment only. No page of the program states the terms (no on-screen string mentions them), so no page gets the short "Teaching aid; not for legal use." line.
   - The tested-on lines (16–27 → 19–32): beta 2c has run on the PC harness only; beta 2b passed the emulator retest of 17 Oct; the review re-checked every number.
   - The companion files (29–34 → 34–43) add this file and say which two menu lines the guide still has in their old form.
   - A "beta 2c" paragraph (→ 45–65), with beta 2b's line numbers, the finding IDs and the disclaimer.
4. **Nothing else.** The routines that differ from beta 2b are exactly `cqMenu` and `cqXEngS`, each by its one string. The other 61 routines are byte-identical, comments included.

**The verify script** (`verify_CICatcher_beta2c.py`, review item 22) looks for each older file beside itself, then in `_old` and `_superseded*` folders beside it, then in `/home/claude/work/out` (or the folder named by `VERIFY_PRED_DIR`). A check that needs a file it cannot find prints SKIP and is not counted, so the script runs in a folder holding only the current version.

## Verification

`verify_CICatcher_beta2c.py`, built from the 2b script, in harness **ppl_run_v3e** (with `home_minus` off it prints what v3d printed). Output in `verify_CICatcher_beta2c_output.txt`: **PASS, 158 checks, 0 failures, 0 skipped** (the 2b script: 131).

- **Kept:** every 2b check (A–D the intervals and coverage; E the scripted sessions in both CAS modes and 1,728 CAS templates; F beta 1's suite, 71 checks; G beta 2 and 2a; R1–R5 the round-2 fixes; S the scientific-string audit).
- **Two expected values changed, because they were the findings:**
  - E's "help page 4 shown, with its engine line" expected "… BINOMIAL_CDF (checked)" (C-C2); it now expects "… BINOMIAL_CDF, checked".
  - R3's "every CHOOSE line is 28 characters or fewer" excepted "New setup: interval, population, n" (C-C1); it now has no exception.
- **G (2b)** now compares the beta 2b and 2a files, as the record of 2b.
- **X1, the review's regressions:** `check_CICatcher.py`'s E2 (every CHOOSE item fits, ≤ 31) and its E3 at the header's own 46: beta 2c passes both; **beta 2b fails both** (34 and 47 characters).
- **X2, C-C1 in a run:** the main menu's first line is "New: interval, population, n"; item 1 still opens "Which interval?"; Cancel keeps the run ("…, Exact, p = 0.10, n = 20"); every CHOOSE line shown is 28 characters or fewer. Beta 2b showed the 34-character line.
- **X3, C-C2 as drawn:** all six help pages, 90 lines each run, in three runs (Exact; t, for the engine line; the BINOMIAL check failing): the longest line is 46 characters; page 4 ends "exact ends: bisection on BINOMIAL_CDF, checked", or "exact: OFF (BINOMIAL_CDF failed its check)". Beta 2b drew one 47-character line.
- **X4, the review's own `check_CICatcher.py`:** on beta 2c, 50 checks passed, 0 failed; on beta 2b, only E2 fails, as the review left it.
- **G (2c):** only `cqMenu` and `cqXEngS` differ, each by exactly its one string; the other 61 routines are byte-identical, comments included; outside them only comments differ; the header carries Roger's DISCLAIMER line under the terms, and no on-screen string states the terms.
- **`h.sci_strings`:** 41 beta 2c harness runs, **0 scientific strings**.
- **Item 22:** the same script, run in a folder holding only `CICatcher_beta2c.txt` and itself with no older version reachable (`VERIFY_PRED_DIR` pointing nowhere): **PASS, 129 checks, 0 failures, 6 skipped** (F, G 2a, R1–R4's beta 2a comparisons, G 2b, X1's beta 2b half, G 2c), no FileNotFoundError.

## Gate

In `gate_f19` (the newest version of every program; beta 2b moved to `gate_f19/_old`), `python3 ppl_gate_v1b.py CICatcher_beta2c.txt _old/CICatcher_beta2b.txt`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as beta 2b; no hard errors (E12 included).
- lint_ppl: 1130 checks, 11 problems, the same 11 as beta 2b (STRING-arity miscounts; `lint_ppl_v2.py` no longer reports them).
- Full parse: stops at the first file-level `LOCAL` after the EXPORT list (251), the same statement as beta 2b's (220): the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`check.sh CICatcher_beta2c.txt CICatcher_beta2b.txt`: kit lint 0 errors; ppl_check_v4 clean, no hard errors; the parse fails on the same statement as beta 2b's.

## Device checklist (emulator first, then G2 and G1)

1. Open CICatcher in the Connectivity Kit and paste over it (never a second copy). Program Catalog → CICatcher → Edit → Check: no errors.
2. **C-C1:** run CICatcher, Enter, any setup, OK. Tap Menu (or press Enter). The first line reads **"New: interval, population, n"**, whole. Pick it: "Which interval?" opens; Cancel keeps the run.
3. **C-C2:** Menu → Help, then Enter three times to page 4, "Exact intervals: never below". The last line reads **"exact ends: bisection on BINOMIAL_CDF, checked"**, with "checked" whole inside the frame.

## Unresolved

- **The guide.** `cicatcher-guide_beta2.md` still has the setup item as "Proportion: Exact (Clopper-Pearson)" (from beta 2b) and does not quote the main menu's first line; its next version should show "Proportion: Exact (C-P)" and "New: interval, population, n".
- **Where the boxes cut** is an estimate from character counts: the emulator cut a 35-character CHOOSE line after about 31 and showed GaltonBoard's 30-character "Where Poisson comes from (CAS)" whole; the 46-character limit for a help line is the header's own (296 px at about 6.5 px a character). The emulator decides (checklist steps 2 and 3).
- No open decision in the review's section 3 touches CICatcher. Its improvements (section 4, item 4: coverage over p) are not in this pass.
