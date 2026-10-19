# CentralLimit beta 3c (app): changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 3b; every beta 3b feature is kept, and START, Plot, the exported CentralLimit and the nine VIEW entries are byte-identical. Run only in the PC harness (ppl_run_v3e); not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 3; details in `findings_F.md`, section 2):

> **C-1. CRASH — a population no longer in D1 is trusted; `D1(idx)` is then out of range.** `cltRecover` (941–952) returns 1 as soon as `cltPop > 0` and never looks at D1 again. … D1 is the student's: the Num view lets them clear the column or delete rows … Then `cltSample` (1570) and `cltOneSample` (1623) index `D1(MIN(cltNpop, 1 + IP(RANDOM*cltNpop)))` past the end: runtime error, Program Editor.

The review proposed a `cltRecover` that checks `SIZE(D1) == cltNpop`, and a `RESET()` hook (its improvement 2).

**And Roger's disclaimer** (19 Oct 2026, through the coordinator): a header line beside the distribution terms, and one line on screen.

## What changed (line numbers: beta 3b → beta 3c)

1. **cltRecover** (941-952 → 963-996). It now reads `SIZE(D1)` every time (inside IFERR: 0 if D1 does not exist) and trusts the population only if `cltPop > 0 AND SIZE(D1) == cltNpop`. Otherwise:
   - **When a population had been built** (cltPop > 0), its sample means go with it: `cltMade := 0; D2 := {}`.
   - **Fewer than 2 values in D1:** `cltPop := 0` and it returns 0. Every caller already handles 0:
     - the dashboard says "No population yet." / "Press Enter or tap Menu.";
     - cltSample and cltOneSample return at once;
     - the built-in plot and the Square-root-law view say "Choose a population first (View menu).";
     - the dashboard and Draw-samples views offer the population menu;
     - the Plot key shows the app's plain Plot view.
   - **2 or more values:** what D1 holds is adopted as "Data in D1", as when the app starts with data already there. cltPopStats sets cltNpop, μ and σ (N divisor), and cltNewPop sets n = 1 and starts a fresh square-root record.

   I checked the review's proposed code against the program and every caller and kept it with one difference. It cleared D2 on every adoption; beta 3c clears D2 only when the population it drops was one this run had built. With nothing built (the app reopened with class data in D1), beta 3c does exactly what beta 3b did and leaves D2 alone.
2. **New `RESET()` hook** (→ 2629-2643, after Plot). It sets no population, no sample means (cltMade 0, D2 {}), and calls cltNewPop for n = 1 with the square-root record cleared. It is not EXPORTed, like START and Plot here. Whether Reset also recompiles the program is unknown, so the hook does it by hand. D1 is left to the app: if it still holds values, the next action adopts them.
3. **The disclaimer.**
   - The header (→ 24-26), beside the distribution terms: "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes."
   - On screen (cltWelcome, → 2338-2340): the opening page, shown each time the app starts, reads `Teaching aid; not for clinical or legal use.` in red, font 1, at y 28, between the title and the first line. The three Help pages are full (lines down to y 206 above the footer), so the opening page carries it.
4. **The header:**
   - the banner;
   - the tested-on line ("Beta 3b and 3c have not run there yet (beta 3c has run only in the PC harness)");
   - a dated "beta 3c (19 Oct 2026) - what changed: C1 (fleet review 19 Oct)" paragraph (→ 41-60), whose line numbers are beta 3b's.

   A comment above each changed statement says why. No comment sits inside a bracket.

**Before and after** (harness: a uniform population of 500 built through the menu, 200 means drawn, then D1 edited as below, then the dashboard driven with +1, 1 sample, n+, a tap on the top panel and two button taps):

| D1 after the edit | beta 3b | beta 3c |
|---|---|---|
| emptied | `index … out of range in D1 (1..0)`: run-time error | "No population yet." / "Press Enter or tap Menu."; cltPop 0, cltMade 0, D2 {} |
| cut to 1 row | `… out of range in D1 (1..1)` | the same as emptied |
| cut to 100 rows | `… out of range in D1 (1..100)` | "Data in D1, N = 100", μ and σ of those 100; the old means dropped, new ones drawn from them |
| lengthened to 600 | no error, but the old population's numbers kept | "Data in D1, N = 600" |
| left alone | "Uniform, N = 500" | the same, with the same means |

## Verification

`verify_CentralLimit_beta3c.py` was built from the beta 3b script, and every check is kept. It runs on beta 3c in harness ppl_run_v3e, which runs v3d scripts unchanged. Output is in `verify_CentralLimit_beta3c_output.txt`: **156 checks, ALL PASS**.

Old checks whose expected value moved (each says so):
- **R5:** the routines that differ from beta 3a now include cltRecover and cltWelcome, and RESET is new. START, Plot, CentralLimit and the VIEW entries are still byte-identical.
- **Part 2's "every template under 1 s in desktop Giac"** is now "under 5 s". It times desktop Giac on the PC, not the program. On the shared machine on 19 Oct the n = 100 peak took 2.4-3.5 s. The review's run of beta 3b's own script failed this check too and called it "a speed note, not a number". The calculator's CAS speed is a device test.

New part 6:
- **U1 (C-1):**
  - the table above, both versions: beta 3b stops in the 3 cut cases; beta 3c never stops;
  - μ and σ of the adopted D1 = NumPy's;
  - after the adoption the old means are gone, and at n = 1 every new mean is a member of the new D1;
  - an unchanged D1 gives the same session as beta 3b;
  - 7 more entries (cltSample, cltOneSample, the Plot key, 4 View entries) × 3 edits: no error in beta 3c (beta 3b stopped in several);
  - the built-in plot's message.
- **U2:**
  - nothing built and 7 values in D1: beta 3c's state after cltRecover is beta 3b's, D2 untouched;
  - no D1: returns 0.
- **U3:**
  - RESET clears population, means, D2, n and the square-root record;
  - with D1 still full, the next action adopts it; with D1 cleared, "No population yet.";
  - RESET is a hook beside START and Plot.
- **U4:** the disclaimer is in the header word for word, and on the opening page; the rest of that page is beta 3b's.
- **U5:** the review's own `check_CentralLimit.py`, run unchanged except for its path:
  - beta 3b: 0 failures;
  - beta 3c: exactly 3, the checks that asserted the old behaviour, now turned round: "START and Plot overridden" (RESET now is too), "D1 cleared … cltSample stops" and "D1 shortened … cltOneSample stops".
  - Its fourth C-1 probe, "cltRecover returns 1 regardless", still passes, for a new reason: beta 3c adopts the 100 rows left in D1 and returns 1.
  - The review wrote its C-1 probes to pass while the crash was there, so on beta 3c they are expected to fail. U1 holds the regression tests in the right direction.
- **U6:** the routine diff (exactly RESET, cltRecover, cltWelcome) and the exact code-line diff. The other routines are byte-identical, comments included.
- **U7:** RESET is not a built-in name; no comment sits inside a bracket; the version strings are swept.
- **U8:** `h.sci_strings` over all 57 beta 3c runs: **empty**.

## Gate

`python3 ppl_gate_v1b.py CentralLimit_beta3c.txt _old/CentralLimit_beta3b.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: 9 E1, 23 E7, as beta 3b. There are no hard errors.
- lint_ppl: 19 problems, as beta 3b. They are the tool's STRING-argument miscounts.
- Full parse: it stops at `#003CC8:24h` (1859; beta 3b 1815). This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches. RESET is an exempt app hook.

`bash check.sh`: kit lint 0 errors; no hard errors; the parse fails on the same construct as beta 3b.

## Device checklist (emulator first, then G2 and G1)

1. Install over beta 3b through the Kit's app editor (Application Library → CentralLimit → Program tab → paste → save). Then Program Catalog → "CentralLimit (App)" → Check.
2. **Opening page:** `Teaching aid; not for clinical or legal use.` in red under the title, clear of the title and the first line.
3. **C-1, cleared:** View → Choose population → Uniform 0, 10, 500 → the dashboard draws. Esc → Num → clear D1 (Shift-Clear on the column) → View → CLT dashboard → "+1", then tap the top panel. Expect "No population yet. Press Enter or tap Menu." and no error.
4. **C-1, trimmed:** rebuild the population, then in Num delete D1's rows down to about 100 (or type a short list) → View → CLT dashboard → "+1", then "1 sample". Expect "Data in D1, N = 100" with new μ and σ, n = 1, and no error. Also press Plot: the app's histogram of the new D1.
5. **RESET:** with a population and means on show, go to Apps, highlight CentralLimit, Reset. Reopen: the dashboard shows "No population yet." if Reset cleared D1, or "Data in D1, N = …" if it did not. Note which, because it tells us whether the app's Reset clears the columns and whether it calls this hook.

## Unresolved (open decisions touching CentralLimit; not changed here)

- **D17 / C-2:** the red "program's sum … agrees to 0 digits" line above n = 49 on the exact page.
- **C-3:** the MGF series in the CAS's order.
- **Not covered by C-1:** a D1 edited in place without changing its length (a value retyped) keeps the old μ, σ and bars until the population is rebuilt. There is no crash (every index stays in range), but the dashboard is stale. Detecting it would mean comparing D1 value by value on every action; that is left for Roger to decide.
- **Review improvements** (not in this pass): a σ/SD column in the square-root-law table, a grey line at n = 4, and the LOCAL MAKELIST counter (K stays, harmless).
