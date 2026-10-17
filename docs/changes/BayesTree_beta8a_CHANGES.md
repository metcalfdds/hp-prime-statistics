# BayesTree beta 8a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 8 (16 Oct 2026); every beta 8 feature is kept. Not yet run on hardware or on the emulator.*

## Why

CASProbe beta 1a and 1b ran on the HP Prime Virtual Calculator (2.4.2, build 2026-09-09) on 17 Oct 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`, "CASProbe beta 1a, then beta 1b"):

- `CAS(s)` with `s` a string variable or parameter hands the text back **unevaluated** (T06, T07). Beta 8's `bt_Cas` (`cR := STRING(CAS(bt_S));`) returned its own input. `bt_IsFr` then refused it, so the tree, the Exact page and the summary always showed decimals: no 2/3, no 19/118, no break-even 1/20.
- `STRING(EXPR("CAS(" + CHAR(34) + "string(" + s + ")" + CHAR(34) + ")"))` works (T08). The answer is a PPL string, so `STRING()` adds quotes (T12).
- The Prime prints a solve with braces: `{1/20}` (T18), `{[2,1]}` for a system (T36). Fractions print as on the desktop.

## What changed (line numbers: beta 8 → beta 8a)

1. **`bt_Cas`** (beta 8 277–299 → 8a 293–320): the IFERR line is the BRIEF_CAS_v2 form, `cR := STRING(EXPR("CAS(" + CHAR(34) + "string(" + bt_S + ")" + CHAR(34) + ")"));`. The surrounding quotes are dropped as before. The reject test adds `INSTRING(cR, CHAR(8734)) > 0` (∞ and ±∞). The comments say why.
2. **No answer reader needed a code change.** `bt_Strip` already drops braces as well as brackets, so the Prime's `{1/20}` becomes `1/20`. Its leading-`list` removal is harmless dead code on the Prime, kept for desktop Giac. `bt_IsFr` takes only digits, `/` and `-`. Their **comments** now say what the emulator showed (8a, in bt_Strip's and bt_IsFr's heads). No CAS text assigns a variable: `btq`, `bts`, `btc`, `btl` and `btm` are only solved for or left symbolic.
3. **Header**: version beta 8a, the firmware paragraph, a "beta 8a — what changed" note.

Nothing else changed. The verify script checks this: the only routine that differs from beta 8 is `bt_Cas`, and outside it only comments differ.

## Verification

`verify_BayesTree_beta8a.py` (from the beta 8 script; Part A through `prime_eval`, Part B in harness **ppl_run_v3b**), output in `verify_BayesTree_beta8a_output.txt`: **78 PASS, 0 FAIL** (beta 8's script: 72; the 6 new checks are marked 8a).

- A2, A3: 1188 CAS texts, read as bt_Cas receives them on the calculator, equal Python fractions: PPV, NPV, 1 − PPV and the break-even, for 1 and 2 tests. Among them: 19/118, 1881/1882, 1/20, 36/37, 1/325, 3/5. No text holds a decimal point.
- A4 (8a): the symbolic solves arrive in braces, `{(-btc+1)/(-btc+bts+1)}` and `{1/(btl*btm+1)}`. bt_Strip's result equals SymPy's solution.
- B, end to end:
  - **cas='giac'**: the panel shows `PPV = 2/3`, `NPV = 171/173`, "exact (CAS), tap". Every CAS text asks for `string(...)`. No CAS variable is assigned, and no CAS call takes a variable (B1, 8a).
  - The Exact pages give `95/590 = 19/118 = 0.161`, `prior = 1/20`, and `p = (-sp+1)/(-sp+se+1)`.
  - Drags still ask the CAS only on the lift.
  - Forensic, two tests, Enter counts, the PPV view, the slow-CAS switch and stale-key mode are unchanged.
  - **cas='fail'**: decimals, "decimal, tap", "(no CAS: by hand)", no error.
- B17 (8a): canned answers in the calculator's form (quoted strings, the solve as `"{1/19}"`) give the same panel. A decimal answer is refused as "exact".
- B16: beta 7's verification run against 8a gives 48 PASS and the same 4 intended differences as against beta 8.
- G (8a): beta 8 itself in v3b shows the emulator's finding: decimals only, and a "non-literal" warning.

**Gate**: `python3 ppl_gate_v1a.py BayesTree_beta8a.txt BayesTree_beta8.txt`: **RESULT: PASS**.
- ppl_check_v3 gives 1 E4, 2 E5 and 1 E9, the same as beta 8; none is a hard error.
- lint_ppl has no new problem except one more "STRING() with 2 args" on the reject line in the CAS routine. That is the lint reading each `INSTRING(` as a `STRING()` call: the line now has three INSTRING tests where it had two. Every other problem is in the original too.
- fleet_names_v2 over 28 files: 0 collisions, 0 untagged, 0 built-in matches.

## Device checklist (after the beta 8 checklist)

1. Start BayesTree and Close the menu. The tree panel should read `PPV = 2/3`, `NPV = 171/173`, "exact (CAS), tap". "decimal, tap" means the call form is not working on this calculator: note it and skip the CAS steps.
2. Enter values 0.01 / 0.95 / 0.95, then Exact answers. Page 1 shows `= 19/118 = 0.161` and `prior = 1/20`. Page 2 shows the CAS solve `p = (-sp+1)/(-sp+se+1)`, or however the calculator writes it; note the form.
3. On the G1, look at the Exact page's last line ("CAS: the last update took … ms"). If it is over 1500 ms, the tree should switch to "tap for exact" by itself.
4. Afterwards, in the CAS view, `btq` has no value.
