# CASProbe beta 1d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, after beta 1c ran on the HP Prime Virtual Calculator. Built on beta 1c; only T43b's test changed, and every other test keeps its number and its code. The two `#PYTHON` blocks are byte-identical, and the probe's own call forms (`cxCall`, `cxObj`, `cxPickForm`) are unchanged. Beta 1d ran on the emulator the same evening (below); it has not run on hardware. Read `CASProbe_beta1c_CHANGES.md` for T43 and the round-2 guards, `CASProbe_beta1a_NOTES.md` for the test list.*

## Why: what the emulator showed

Beta 1c ran on the HP Prime Virtual Calculator 2.4.2 (firmware 2026-09-09) on 17 Oct 2026, "Run every test" (the T34 run). The checklist expected 45 pass and 8 fail. The summary said:

> pass 44, fail 9, value 19, error 0, skip 0

The one unexpected FAIL was T43b. The log:

```
T43a PASS INSTRING of an empty string is an error
T43b FAIL STRING(0.096, 2, 1) is not 9.6E-2
  = 9.6ᴇ−2, codes 57 46 54 7431 8722 50
T43c PASS STRING(ROUND(0.096, 1), 2, 1) = 0.1
```

and the summary line "STRING(0.096, 2, 1): NOT scientific".

**The probe was wrong, not the Prime.**
- The Prime **does** print the scientific form. Code 7431 is U+1D07, the small capital E.
- The exponent's minus is **code 8722** (U+2212, Home's minus sign), not the ASCII hyphen, 45.
- T43b compared the text against `"9.6" + CHAR(7431) + "-2"`, with an ASCII hyphen. So it FAILed, and the summary wrongly said "NOT scientific".
- This is the same minus T01 already records at the start of Home's `STRING(-2.5)`. Round 2's Home checks had written it as a hyphen (`"9.6ᴇ-2"`), and so had beta 1c's notes and harness v3d.

Everything else in beta 1c behaved as expected. The known FAILs were T01, T04, T05, T06, T07, T10, T32 and T34a.

## What changed (line numbers: beta 1c → beta 1d)

1. **T43b, the test** (in `cxT43`, 1638–1671 → 1669–1713).
   - **PASS** when the text holds `CHAR(7431)`, the scientific form, whatever the sign character (1657 → 1690–1692). The INSTRING runs inside `IF DIM(sxB) > 0`, the round-2 guard, although `STRING()` of 0.096 is never `""`.
   - **FAIL** text: "STRING(0.096, 2, 1) is not scientific" (1661 → 1696). At 47 characters the record wraps onto a second log line, as `cxNote` does with any long line.
   - **A new note line** under the codes line records which minus the exponent used (1699–1705). It is written only when the text is scientific, and reads one of:
     - `  exponent minus: CHAR(8722), Home's minus`
     - `  exponent minus: ASCII 45, a hyphen`
     - `  exponent minus: none`
   - One new LOCAL, `sxM` (1640 → 1671; five on the line).
   - **`cxSci`** is set by the same test, so the summary line (2263, unchanged code) reads "STRING(0.096, 2, 1): scientific" on the emulator.
2. **The T43 comment block** (1634–1636 → 1659–1667). It used to say the emulator printed "9.6E-2" and "PASS = exactly that". It now gives the codes `57 46 54 7431 8722 50`, the new PASS rule, and why beta 1c FAILed.
3. **Version strings and header.**
   - These now read beta 1d:
     - the banner (3);
     - the progress page title, `cxBegin` (494 → 519);
     - the summary page title, `cxSummary` (2039 → 2081);
     - the menu title (2144 → 2186);
     - the log's first line, "CASProbe beta 1d, 17 Oct 2026 build" (2154 → 2196).
   - The firmware line (12–13 → 12–15) adds beta 1c's emulator result (44 / 9 / 19 / 0) and names harness v3e.
   - **A new "WHAT CHANGED IN BETA 1d" paragraph** (55–77) quotes the finding.
     - The file is ASCII, so the paragraph writes the E and the minus as `E` and `-`, and says so.
     - It notes that the beta 1c paragraph below it wrote the exponent's minus as a hyphen.
   - **Left as history, on purpose (rule 13 sweeps the references to the current version):**
     - the log marker `-- T43 (added in beta 1c) --`, like `-- T35-T42 (added in beta 1a) --`;
     - the "beta 1c:" comments on the round-2 guards;
     - "T43 (beta 1c, no CAS)" in the test list;
     - the beta 1c, 1b and 1a paragraphs;
     - the `#PYTHON` block comments, which still say beta 1b because the blocks stay byte-identical.

**Nothing else changed.** The routines that differ from beta 1c are exactly four: `CASProbe`, `cxBegin` and `cxSummary`, where only the version string changed, and `cxT43`. Outside them, only comments differ. There is no new file-level LOCAL.

## Verification

`verify_CASProbe_beta1d.py`, built from `verify_CASProbe_beta1c.py`, runs in **harness v3e** with `home_minus=True`, as before. Output is in `verify_CASProbe_beta1d_output.txt`: **ALL CHECKS PASS, 199 checks** (beta 1c's script had 186), exit code 0. The script now exits 1 if any check fails.

**C0, the emulator's runs:**
- **beta 1b** gives the emulator's 42 pass, 8 fail, 19 values, 0 errors, as before.
- **beta 1c in v3e reproduces the emulator's beta 1c run exactly** (new check):
  - 44 pass, 9 fail, 19 values, 0 errors;
  - FAIL T01, T04, T05, T06, T07, T10, T32, **T43b**, T34a;
  - the two T43b lines quoted above, character for character (`= 9.6ᴇ−2, codes 57 46 54 7431 8722 50`);
  - "STRING(0.096, 2, 1): NOT scientific".
- **The same beta 1c in harness v3d** gives 45 pass and 8 fail, with T43b PASS and codes `… 7431 45 50`. v3d printed a hyphen there, which is why the harness passed what the emulator failed.
- **beta 1d:** 45 pass, 8 fail, 19 values, 0 errors, with beta 1b's 8 FAILs.
- **beta 1d's log is beta 1c's line for line** (timings aside), except:
  - the version line;
  - T43b's record (FAIL → PASS);
  - the one new note line, "exponent minus: CHAR(8722), Home's minus";
  - the summary line, "NOT scientific" → "scientific";
  - the tally (44 pass, 9 fail → 45 pass, 8 fail).
  - Against beta 1b, as in beta 1c's script, the T43 block is now 8 lines.

**C1–C9, kept:**
- every test the emulator passed passes, along with T43a–c;
- T43b's three lines are exactly `T43b PASS STRING(0.096, 2, 1) is scientific`, `  = 9.6ᴇ−2, codes 57 46 54 7431 8722 50 ` and `  exponent minus: CHAR(8722), Home's minus`;
- the menu, the summary page and all 44 progress pages say beta 1d;
- `cas='fail'` (C3) still runs T43a–c, all PASS;
- C9: beta 1b stops 21 tests with ERROR, and beta 1d stops none;
- every log line is 46 characters or fewer.

**D10 and D11, device variants:**
- **D10:** with `STRING(0.096, 2, 1)` = "0.1", the FAIL reads "T43b FAIL STRING(0.096, 2, 1) is not scientific". There is no exponent-minus note, and the summary says "NOT scientific".
- **D11 (new)** gives three other answers for `STRING(0.096, 2, 1)`:

| Answer | T43b | Note line | Summary | Tally |
|---|---|---|---|---|
| `9.6ᴇ-2`, a hyphen (what v3d printed, and what beta 1c expected) | PASS | `exponent minus: ASCII 45, a hyphen` | scientific | 45 / 8 |
| `9.6ᴇ2`, no sign (not seen; it exercises the "none" branch) | PASS | `exponent minus: none` | scientific | 45 / 8 |
| `9.6E-2`, an ASCII E | **FAIL** | none | NOT scientific | 44 / 9 |

  By T43b's rule, only the Prime's own E (7431) counts as scientific.

**G, the code:**
- the routine diff from beta 1c is the four above;
- in `CASProbe`, `cxBegin` and `cxSummary`, only "CASProbe beta 1c" → "CASProbe beta 1d" changed;
- `cxT43`'s code diff is exactly the LOCAL, the test, the FAIL text and the note;
- against beta 1b, the differing routines are still beta 1c's 14;
- the `#PYTHON` blocks are byte-identical to beta 1c's and beta 1b's;
- the only code line that says beta 1c is the T43 log marker.

**H, the string audit:**
- 44 INSTRINGs: beta 1c's 41, plus T43b's three on `sxB`, each guarded.
- LEFT counts and MID starts are unchanged.
- The three fixed-decimal STRINGs are unchanged.
- The only scientific `STRING` in all 24 beta 1d runs is T43b's own. `h.sci_strings` keeps the hyphen form, `9.6ᴇ-2`, in v3e; the program itself received U+2212.

## Gate

`python3 ppl_gate_v1b.py CASProbe_beta1d.txt CASProbe_beta1c.txt` was run in a scratch copy of `gate_r2`, with beta 1d added (beta 1c, the original, is left out of the fleet check by the gate). It gives **RESULT: PASS**.
- **ppl_check_v4:** clean, as beta 1c. No hard error, E12 included: no `//` comment sits inside an open bracket.
- **lint_ppl:** 76 problems against beta 1c's 73. The 3 new ones are T43b's three INSTRINGs, which lint_ppl reads as 2-argument STRINGs: the same noise beta 1c's notes describe. The rest are line for line beta 1c's, except that the "no function named" lines name the new file.
- **fleet_names_v2** over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches. `sxM` is the only new name.
- **`check.sh`** runs the parts the gate skips without the kit zip:
  - the hp-prime-kit lint: **1 error**, "unbalanced", with the same 82 warnings as beta 1c. The kit counts a `#PYTHON` block's lines.
  - the full parse fails at line 203, "expected a name after EXPORT", where beta 1c fails at its line 178 (the same line, 25 lines further down). That is the tool's limit.

## Emulator (17 Oct 2026, 16:42)

Beta 1d ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), "Run every test", T34 run: **pass 45, fail 8, value 19, error 0, skip 0**, slowest call 9 ms (T24). The log's T43 lines:

```
T43a PASS INSTRING of an empty string is an error
T43b PASS STRING(0.096, 2, 1) is scientific
  = 9.6ᴇ−2, codes 57 46 54 7431 8722 50
  exponent minus: CHAR(8722), Home's minus
T43c PASS STRING(ROUND(0.096, 1), 2, 1) = 0.1
```

and the summary line "STRING(0.096, 2, 1): scientific". The FAILs are T01, T04, T05, T06, T07, T10, T32 and T34a, as in beta 1b and 1c. This matches harness v3e's run exactly.

## Device checklist (emulator first, then G2 and G1)

1. **Paste.** Replace beta 1c in the Kit; the two share every routine name. Then Program Catalog → CASProbe → Edit → Check: no error.
2. **On the emulator, Run every test.** Expect **45 pass, 8 fail, 19 values, 0 errors**. The FAILs are T01, T04, T05, T06, T07, T10, T32 and T34a, as in beta 1b.
3. **T43 in the log:**
   - `T43a PASS INSTRING of an empty string is an error`
   - `T43b PASS STRING(0.096, 2, 1) is scientific`, then `= 9.6ᴇ−2, codes 57 46 54 7431 8722 50`, then `exponent minus: CHAR(8722), Home's minus`
   - `T43c PASS STRING(ROUND(0.096, 1), 2, 1) = 0.1`
   - in the summary: "INSTRING of an empty string: an error" and "STRING(0.096, 2, 1): scientific".
4. **On the G2, then the G1:** the same lines. **A different code on T43b's codes line is a finding**: say, 45 for the minus (the note would then read "ASCII 45, a hyphen"), or an E other than 7431 (T43b would FAIL). It would mean the calculator's firmware prints differently from the emulator's. A FAIL on T43a is a finding too. Copy the log (Edit ▸ Copy on CX_LOG).
5. **On the G1,** note the "slowest call" on the summary page (the open question since beta 1).

## Harness v3e

`ppl_run_v3e.py` (README: `ppl_run_v3e_README.md`) is v3d with one change in `_string_home`'s scientific branch. When the harness models Home's minus (`home_minus=True`), a negative exponent now gets U+2212 instead of the hyphen: `STRING(0.096, 2, 1)` = `9.6ᴇ−2`, codes 57 46 54 7431 8722 50, as on the emulator. A negative mantissa already had U+2212 there.
- **`home_minus` still defaults to False.** The fleet's verify scripts read screen text with hyphens, and only `verify_CASProbe_*` sets it. With it off, v3e prints exactly what v3d printed.
- **`h.sci_strings`** and the one-per-run warning keep the hyphen form, as in v3d.
- **Not changed, not measured:** STRING's Standard (mode 1) and Scientific (mode 3) forms still write an ASCII `E` and hyphen.
- **Regression.** All 15 verify scripts that import `ppl_run_v3d` were run twice in scratch copies of `out/`: as written, and with the import switched to `ppl_run_v3e`.
  - **14 of them give the same results**, check for check. BayesTree beta 8c, CICatcher beta 2b, CentralLimit beta 3b, ChiTable beta 3c, DNAMixLR beta 3b, EpiStats v1.7b, ErrorRate beta 1b, FDAES v3.7a, GaltonBoard beta 3c, PowerViz v2.5b, ScatterLab beta 2b, StatDist v2.7c, StudRange beta 15b and TrendTest beta 3c all pass in both. The only differing output lines are PC timings and one detail list printed in set order (BayesTree R6).
  - **`verify_CASProbe_beta1c.py` is the one difference, and the intended one.** Under v3e, beta 1c gives the emulator's 44 pass and 9 fail, so 5 of its 186 checks, all about T43b, now fail. `verify_CASProbe_beta1d.py` replaces it.
- `verify_CASProbe_beta1d.py` also imports `ppl_run_v3d` for its one v3d comparison. If v3d is archived away from `out/`, that check is skipped with a note: 198 checks, all pass.
