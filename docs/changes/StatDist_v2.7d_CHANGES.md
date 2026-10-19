# StatDist v2.7d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026, evening. Built on v2.7c; every v2.7c feature is kept, and every ordinary display is unchanged. Not yet run on hardware or on the emulator (v2.7b passed emulator round 2).*

## Why

**No "=" before a relation** (Roger approved the pass, 17 Oct 2026, 21:18).
- `st_fmtp` writes `< 0.000001`, or `> -0.000001`, below its floor.
- `st_fmtx` writes `< 0.0001` for a value that needs more than three decimals and is below 0.0001.

The displays put that after `= `. Each of these took only ordinary inputs:
- a far tail read `P(X <= -6) = < 0.000001`, on the panel, on the Numbers page and in the summary returned to Home;
- a density read `f(x) = < 0.0001`, and a bar `P(X = 95) = < 0.000001: the red bar`;
- σ = 0.001 read `variance = < 0.0001`;
- σ = 0.00005 read `σ = < 0.0001` and `mean = < 0.0001, sd = < 0.0001`.

**A normal approximation that read 0.** The coordinator asked for this check across the fleet after FDAES's emulator run. The panel's normal approximation (Binomial, Poisson) took its right tail as `1 - NORMALD_CDF`, which is exactly 0 once the tail is below the CDF's last digit. Binomial(100, 0.5) at x = 95 read `normal approx. = 0.0000`, where the left tail at x = 3 read `< 0.0001`.

## What changed (line numbers: v2.7c → v2.7d)

1. **New `st_Eq(eqS)`** (→ 466-478, after `st_fmtp`). It returns `" = 0.158655"`, or `" < 0.000001"` when the relation is already there. It reads `LEFT(eqS, 1)` only inside `IF DIM(eqS) > 0`, and it uses no INSTRING.
2. **`st_ParStr`** (1523-1550 → 1565-1592). Each value carries its own `" = "`: `psA := st_Eq(st_fmtx(dPl(1)))`, and so on. The 27 templates drop theirs: `"μ" + psA + ", σ" + psB`.
3. **The panel** (`st_Panel`):
   - mean and sd (2777 → 2820);
   - the bar or density line (2782-2790 → 2826-2837);
   - the answer (2796-2808 → 2844-2860), which is also `stLast`, the summary;
   - the normal approximation (2832 → 2887).
4. **The Numbers page** (`st_Numbers`):
   - mean, sd and variance (3156, 3158 → 3212, 3215);
   - the CDF lines and the bounds `at b = …` (3165-3174 → 3223-3233);
   - `At x = …` and the answer (3184-3196 → 3244-3260).
5. **The Formula page's check lines:** `st_FmRes` (3573 → 3638) and `st_FmCont`'s `at x = …` (3653 → 3719).
   - The check line keeps its two leading spaces: it is `" " + st_Eq(…)`, so it reads `  = 0.5, the program's value: agree` or `  < 0.000001, …`.
6. **The normal approximation's right tail** (2821 → 2875) is `NORMALD_CDF(stMu, pnZ, 2*stMu - (stXv + 0.5))`. This is the lower tail, and the same number by symmetry.
7. **Header:**
   - the banner (4);
   - a "WHAT CHANGED in v2.7d" paragraph (→ 33-57);
   - the help title (2352 → 2394).
   - A comment above each changed statement says what it does. Every comment sits at bracket depth 0.

**Before and after** (harness; the panel and the Numbers page, set up as part 7 of the verify does):

| Case | v2.7c | v2.7d |
|---|---|---|
| Normal(0, 1), Lower tail, x = −6 | `f(x) = < 0.0001: a density, …`, `P(X <= -6) = < 0.000001`; Numbers `P(X <= -6.0000) = < 0.000001`; Home `StatDist: P(X <= -6) = < 0.000001` | `f(x) < 0.0001: …`, `P(X <= -6) < 0.000001`; `P(X <= -6.0000) < 0.000001`; `StatDist: P(X <= -6) < 0.000001` |
| Normal(0, 1), a < X < b, −7 to −6 | `f(a) = < 0.0001, f(b) = < 0.0001`, `P(-7 < X < -6) = < 0.000001`; `CDF(b) = < 0.000001 at b = -6.0000` | `f(a) < 0.0001, f(b) < 0.0001`, `P(-7 < X < -6) < 0.000001`; `CDF(b) < 0.000001 at b = -6.0000` |
| Normal(0, 0.001) | Numbers `variance = < 0.0001` | `variance < 0.0001` |
| Normal(0.00002, 0.00005) | `μ = < 0.0001, σ = < 0.0001`, `mean = < 0.0001, sd = < 0.0001` | `μ < 0.0001, σ < 0.0001`, `mean < 0.0001, sd < 0.0001` |
| Binomial(100, 0.5), Upper tail, x = 95, normal approx. on | `P(X = 95) = < 0.000001: the red bar`, `P(X > 95) = P(X >= 96) = < 0.000001`, `normal approx. = 0.0000 (continuity corr.)` | `P(X = 95) < 0.000001: …`, `P(X > 95) = P(X >= 96) < 0.000001`, `normal approx. < 0.0001 (continuity corr.)` |
| Binomial(100, 0.5), Lower tail, x = 3, normal approx. on | `P(X <= 3) = < 0.000001`, `normal approx. = < 0.0001` | `P(X <= 3) < 0.000001`, `normal approx. < 0.0001` |
| Poisson(4), Upper tail, x = 30 | `P(X > 30) = P(X >= 31) = < 0.000001` | `P(X > 30) = P(X >= 31) < 0.000001` |
| Normal(0, 1), x = 0.00005 | Numbers `At x = < 0.0001:` | `At x < 0.0001:` |
| Formula page, Normal(0, 0.0005), variance 2.5E-7 | `  = < 0.000001, the program's value: agree` | `  < 0.000001, the program's value: agree` |
| every family at its defaults (Normal: `P(X <= 0) = 0.500000`); Normal(0, 1) at x = 1 | `P(X <= 1) = 0.841345` | the same |

**Seen, not changed:**
- **The right tail of every family.** `P(X > x)` is `1 - CDF` in `st_Prob`, so a far right tail reads `= 0.000000` where the same tail on the left reads `< 0.000001`. Normal(0, 1) at x = 10 reads `P(X > 10) = 0.000000`, in both versions; SciPy gives 7.6E-24. For a family with a bounded range (Uniform, Beta, Triangular, the discrete ones past their top), 0 is the true answer, so the floor cannot simply be applied. A fix needs each of the 27 families' own upper tail. That is Roger's call.
- **A typed x below 0.0001** reads `P(X <= < 0.0001) = 0.500020`. There is no "=" before the relation, so it was left as it is.

## Verification

`verify_StatDist_v2.7d.py` was built from the v2.7c script, and every check is kept. It runs on v2.7d in harness ppl_run_v3d, as before. Output is in `verify_StatDist_v2.7d_output.txt`: **134 checks, 0 failures, RESULT: ALL PASS** (v2.7c's script: 100).
- **Parts 1-6 (kept).**
  - Run unchanged on v2.7d, the v2.7c script fails only on its three version checks: the help title, 6g's routine list and 6g's version line.
  - In the new script, the help title is v2.7d, and 6g keeps comparing the v2.7c and v2.7b files.
- **Part 7 (new):**
  - **7a.** Every row of the table, on both versions. v2.7d's text is v2.7c's with `= <` written `<`. The approximation line also changes, by item 6. Nothing else changes. The summary (`stLast`) is checked too.
  - **7b.** The normal approximation's right tail at five settings, in doubles and in the Prime's 12 digits (NORMALD_CDF rounded to 12 significant digits).
    - v2.7c read `= 0.0000` at Bin(100, 0.5) x 95 and Bin(400, 0.3) x 200, and with 12 digits also at Bin(50, 0.4) x 45.
    - v2.7d prints `< 0.0001` exactly where SciPy's tail is below 0.0001.
    - `NORMALD_CDF(m, s, 2m − x)` equals SciPy's upper tail.
  - **7c.** 27 families × 3 tails × 3 settings (defaults, far left, far right), 243 states: the panel and the Numbers page are v2.7c's with `= <` written `<`, and nothing else. 194 are identical and 49 differ only so (19 distinct lines). `st_ParStr` is checked for all 27 families, at their defaults and with every fractional parameter set to 0.00005.
  - **7d.** `st_Eq`, including `""` → `" = "` and `"undef (no mean)"`.
  - **7e.** The Formula page's check lines, with the CAS answering (desktop Giac).
  - **7f.** The code:
    - The code lines removed and added are exactly the sites above, the lower tail, the help title and `st_Eq`.
    - `st_Eq` and `eqS` are not built-ins, ignoring case.
    - The banner and the help title say v2.7d. No code line names v2.7c.
    - No comment sits inside an open bracket.
    - INSTRING is as in v2.7c. Every LOCAL line holds 6 names or fewer.
  - **7g.** What was seen and not changed, as above.
  - **7h.** No scientific STRING result in any harness run of v2.7d.

## Gate

`python3 ppl_gate_v1b.py StatDist_v2.7d.txt StatDist_v2.7c.txt`, in a scratch copy of `gate_r2` with the newest version of every program: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as v2.7c. There are no hard errors, E12 included.
- lint_ppl: 26 problems, as v2.7c.
- Full parse: it stops at the EXPORT list, as v2.7c does.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

## Device checklist (emulator first, then G2 and G1)

1. Paste over v2.7c (open it in the Kit). Then Program Catalog → Check. Help's title reads "Statistical Distributions v2.7d".
2. **Normal(0, 1), Lower tail, x = −6:**
   - the panel reads `P(X <= -6) < 0.000001` and `f(x) < 0.0001: a density, not a probability`, with no `=`;
   - Numbers reads `P(X <= -6.0000) < 0.000001`;
   - Esc: Home shows `StatDist: P(X <= -6) < 0.000001`;
   - x = 1 still reads `P(X <= 1) = 0.841345`.
3. **Binomial(100, 0.5), Upper tail, x = 95, normal overlay on:** the note reads `normal approx. < 0.0001 (continuity corr.)`, never `0.0000`.
