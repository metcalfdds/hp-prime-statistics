# CICatcher beta 2a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 2 (16 Oct 2026); every beta 2 feature is kept, and the user's guide (`cicatcher-guide_beta2.md`) still applies. Not yet run on hardware or on the emulator. The beta 2 device checklist is in `CICatcher_beta2_NOTES.md`.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 2's `cqCas` (`cR := STRING(CAS(cqCS));`) returned its own input. The panel would have shown the unreduced `upper = 1-(50/2000)^(1/20)` under the badge "exact (CAS)", as if the CAS had answered. The value is right, but the CAS did nothing. The harness reproduces this (verify, part G).
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime writes a square root with the root sign (T14b), so n = 2 would read `1-√(1/40)`. The panel's n is 5 or more, so the forms shown are powers such as `1-(1/40)^(1/20)`.

## What changed (line numbers: beta 2 → beta 2a)

1. **`cqCas`** (beta 2 484–508 → beta 2a 498–528): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + cqCS + ")" + CHAR(34) + ")"));` (2a line 510). The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞ and ±∞). Beta 2's added badge line (`cqCasOK`) is kept. The comments say why.
2. **No answer reader changed.** The answer is only shown (`cqTimes`: * → ×; `cqCFDraw`), and it prints alike on the Prime. No CAS text assigns a variable.
3. **Header**: version beta 2a, the firmware paragraph (the harness is now v3b), the companion-file list, a "beta 2a" note. The CAS-kit box names the call form.

Nothing else changed. The verify script checks this: the only routine that differs from beta 2 is `cqCas`, and outside it only comments differ.

## Verification

`verify_CICatcher_beta2a.py` (from the beta 2 script, harness **ppl_run_v3b**), output in `verify_CICatcher_beta2a_output.txt`: **PASS, 55 checks, 0 failures** (beta 2's script: 49).

- A–D (unchanged):
  - the exact interval through the program's own cqCPInt / cqCPB against statsmodels;
  - the coverage bookkeeping;
  - coverage by exact enumeration and every number help page 4 quotes;
  - 20,000 PPL samples.
- E, the scripted session (Exact, +50, tap a line with 0 "yes" answers, drag the level, Up, Help, Quit):
  - **cas='giac'**: `upper = 1-(1/40)^(1/20) = 0.1684` with "exact (CAS)". The CAS is asked once per (end, n, level), never inside the drag: the frames drawn at the drag's own levels show the decimal form. The calls are `string(1-(50/2000)^(1/20))`, `string(1-(10/2000)^(1/20))` and `string(1-(5/2000)^(1/20))`. Every answer arrives quoted. No CAS variable is assigned, and no CAS call takes a variable.
  - **cas='fail'**: `upper = 1 - (α/2)^(1/n) = 0.1684` and "decimal" throughout, no error.
  - 1,728 templates (n 5–100, 9 levels, both ends) evaluate to the closed form. 2a: none has "sqrt" in the Prime's printing, and none is longer than desktop Giac's, so the panel's 20/28-character limits still hold.
- F: beta 1's suite passes on beta 2a.
- G (2a): beta 2 itself in v3b shows `upper = 1-(50/2000)^(1/20)`, the echoed input.

**Gate**: `python3 ppl_gate_v1a.py CICatcher_beta2a.txt CICatcher_beta2.txt`: **RESULT: PASS**.
- ppl_check_v3 is clean.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 2 checklist)

1. Exact, defaults (p 0.10, n 20, 95 %), +50, then tap a line with 0 "yes" answers. The panel should read `upper = 1-(1/40)^(1/20) = 0.1684` and "exact (CAS)". If it reads `1-(50/2000)^(1/20)`, the call form is not working (the old echo): note it.
2. Drag the level slider with that line picked. While the finger is down the line shows `1 - (α/2)^(1/n)` and "decimal". On the lift it asks the CAS again and shows the reduced form (99 %: `1-(1/200)^(1/20)`).
3. On the G1, time the pause after the lift.
