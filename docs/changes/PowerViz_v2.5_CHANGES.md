# PowerViz v2.4 → v2.5: what changed

*16 October 2026 · the CAS version, built on v2.4 (every v2.4 change kept).*
*Source: `/home/claude/work/out/PowerViz_v2.4.txt` (1,823 lines) → `/home/claude/work/out/PowerViz_v2.5.txt` (2,370 lines, UTF-8, LF). Verification: `/home/claude/work/out/verify_PowerViz_v2.5.py` (output in `verify_PowerViz_v2.5_output.txt`).*
*Not yet run on hardware. **Nothing about the CAS has run on a calculator**: every CAS call goes through `pv_Cas` (line 371), and the page falls back to the textbook formula and PPL's numbers. "v2.5 nnn" = a new line.*

## Design decisions to know about

- **The CAS does the algebra, and PPL does the numbers.** The z values are not whole numbers, and no decimal may go into CAS text (BRIEF_CAS rule 1), so the CAS solves the power equation with **za and zb as symbols** (`pvza`, `pvzb`). It is asked twice:
  1. the symbolic solve for the test on screen, "n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2";
  2. the same equation with the student's σ, means or proportions put in exactly, z still symbols: "n = (3×zα+3×zβ)^2".

  **PPL** then puts in the z values the plot itself uses (`NORMALD_ICDF(0,1,1−α/tails)` and z(0.80)) and gets the number, 55.64.
- **The number beside n₈₀ is PPL's, so it needs no CAS.** The panel shows "n₈₀ = 56 (55.6)": 56 is found by trying n with the power engine (unchanged), and 55.6 is the closed form `pv_NCF` (v2.5 535). That is a handful of operations, worked out with n₈₀ in `pv_Setup` when the inputs change. It follows every drag live and works without the CAS. One decimal is shown, more when one decimal would round the value up to the very integer it sits below ("n₈₀ = 305 (304.99)", `pv_NCFS`).
- **The CAS is asked only when the formula page opens**, and only for changed inputs. The symbolic solve is cached per test (`FSYK`). The numeric one is cached per {test, μ₀, μ₁, σ, p₀, p₁} (`FSNK`). **Changing α, the tails or n never needs the CAS**, because z stays a symbol (verified: B3). No drag, key or frame on the main view ever calls it (verified: B4, 0 calls).
- **The equation keeps √n apart from the per-observation SDs** (SE₀ = u/√n, SE₁ = w/√n, `pv_Eq` v2.5 510). Written as √(p(1−p)/n), Giac 1.9 returns two roots for the proportion tests, one of them false. Written apart, it returns one.
- **No `factor()`.** Giac 1.9's `factor` on the symbolic one-proportion form returns a **wrong** expression (it divides by zα² − zα: −34.49 instead of 152.47 at the defaults; verified, A5). On the two-proportion form it errors. Plain `solve` gives clean, correct forms for all four tests.
- **The two proportions follow the program's own model**: H₀'s SE pooled, √(2p̂(1−p̂)/n), and H₁'s unpooled, √((p₁(1−p₁)+p₂(1−p₂))/n). The effect is the difference p₂ − p₁, as on the axis. This is statsmodels' `samplesize_proportions_2indep_onetail` exactly (verified).
- **Why ⌈n*⌉ and n₈₀ can differ by one.**
  - One-sided: the program's power **is** Φ((δ − zα·SE₀)/SE₁), so the formula is exact and ⌈n*⌉ = n₈₀ in every case tested (222 of 222).
  - Two-sided: the formula leaves out the far tail. That tail's sliver of extra power can let the search stop sooner: n₈₀ is never larger than ⌈n*⌉, and was smaller in 6 of 221 cases (5 by 1, 1 by 2, all at α = 0.20 with n in the hundreds or thousands).
  - The page says which of these happened, for the numbers on screen.
- **Defensive renames outside the CAS work** (v2.4 code, never run on hardware). These are not part of the task; Roger may undo them.
  - The main loop's and `pv_PowNView`'s `LOCAL mm1` (the first finger) became `mmF`: the file-level `MM1` is μ₁.
  - `pv_Draw`'s `LOCAL pW` (an area-label count) became `pWd`: the file-level `PW` is the power.
  - If the device matches variable names ignoring case, as it does built-in and routine names, `mm1 := mm(1)` would overwrite μ₁ with a touch list on every pass. Now no two names in the file differ only by case, except the kit's `dD`/`dV` and the older `dd`/`dv`, which live in different routines.
- **The kit's parameters are `pv_N` and `pv_S`**, the literal tag replacement. With `pvN`, the parameter would equal the CAS symbol `pvn` ignoring case. No PPL identifier equals a CAS symbol ignoring case (scripted check).

## (a) Every change

1. **Header** (v2.5 1-62): "v2.5", the firmware line names v2.2-v2.5 as not run and says "run CASProbe beta 1 first"; a dated "v2.5 - what changed" list; v2.4's and older notes kept. The controls block names the n₈₀ tap and the menu item (v2.5 ~180-195).
2. **File-level state** (v2.5 284-296): `pvCasOK` (badge), `FSY/FSYK` (symbolic formula and its test), `FSN/FSNK` (numeric formula and its inputs), `FCMS` (ms), `NCF` (closed-form n). Initialised in `pv_Init` (v2.5 338).
3. **The CAS kit** (v2.5 352-395): `pv_IStr` and `pv_Cas` exactly as BRIEF_CAS gives them (quote strip included), written with this file's `LOCAL pv_Name()` heads.
4. **Helpers** (v2.5 399-597): `pv_RatS` (a typed value as "(25/10)"; "" beyond 6 decimals), `pv_Rep`, `pv_Strip`, `pv_CasUse` (accepts an answer only if both z symbols are in it, n is gone, there is no comma for a second root and **no decimal point**, so an approximate-mode answer is refused), `pv_DName` (the difference's name: (μ₁−μ₀), (μ₂−μ₁), (p₁−p₀), (p₂−p₁)), `pv_Disp` (pvza→zα, pvzb→zβ, pvs→σ, pvd→the difference, pvp/pvr→the proportions, pvm→p̂ (CHAR 57345), sqrt→√ via `SQG`, * → ×), `pv_Eq` (the solve text from a list {σ, δ, p_a, p_b, p̂}), `pv_NCF`, `pv_NCFS`, `pv_NumD` (a number as typed, up to 4 decimals), `pv_Wrap` (breaks at a space, else after + × /).
5. **`pv_Setup`** (v2.5 ~876-884): `NCF := pv_NCF()` beside `N80 := pv_N80()`, under the same cache key.
6. **`pv_Draw`** (v2.5 ~1345-1362, ~1371):
   - the n₈₀ line becomes "n₈₀ = 56 (55.6)", pulled left when long so it ends inside the panel;
   - a sixth hit box (action 4) covers that line;
   - local `pW` → `pWd`.
7. **`pv_Touch`** (v2.5 2181): a tap on the n₈₀ line opens `pv_Formula`.
8. **`pv_Formula`** (v2.5 1804-1974), the new page "Where n comes from", with the badge in its header. Up to 15 lines:
   1. what power 0.80 means;
   2. the power equation and the SEs of the test;
   3. "CAS, solved for n:" and the symbolic formula;
   4. "CAS, with σ = 15, |μ₁−μ₀| = 5 (z kept exact):" and n = (3×zα+3×zβ)^2;
   5. "PPL: zα = z(0.95) = 1.645, zβ = z(0.80) = 0.842" and "n = ((15×1.645 + 15×0.842)/5)^2 = 55.64";
   6. "Round UP (whole people): n = 56;  trying n: n₈₀ = 56";
   7. the 1-sided or 2-sided explanation.

   Two more cases: no effect gives "No effect (…): no n is enough."; with no CAS, the textbook form is shown with "decimal". The footer shows the CAS time.
9. **Power-vs-n view** (`pv_PCDraw`, v2.5 ~1460-1468): under the green "n₈₀ = 56" label, magenta "formula: 55.6 → 56". The Pow-n drag is unchanged.
10. **Menu** (v2.5 2049-2078): "Sample-size formula" is item 6 (runs `pv_Setup` first). Change test, Help and Return move to 7-9.
11. **Help**: a third page, "help 3/3: the n formula". Page 1's Menu line names the formula; pages 1-2 are relabelled "1/3", "2/3", and page 2's footer reads "next page".
12. **Renames**: `mm1` → `mmF` in `POWERVIZ` and `pv_PowNView`.

## Gate output (final run)

```
=================== PowerViz_v2.5.txt ===================
--- 1. kit lint (errors) ---
kit lint: 0 errors
--- 2. ppl_check_v2 tally (NEW)  ---
      5 E1     173 E7      14 E9
--- 2. ppl_check_v2 tally (ORIG) ---
      3 E1     132 E7      14 E9
--- 2b. ppl_check_v2 HARD errors in NEW (E2 E3 E6 E8 E10 E11), must be empty ---
none
--- 3. lint_ppl structural ---
1062 checks, 19 problems
  PROBLEM line 227: file-level LOCAL declares 7 names (max 6)     (ALAD:={...7 values...}, one name; v2.2-v2.4's false positive)
  + 14 x "STRING() with N args, want 3"                             (see below)
--- 4. full parse (kit interpreter) ---
PowerViz_v2.5.txt                PARSE FAIL PPLError: <ppl>:223: expected a name after EXPORT
   ORIG: PowerViz_v2.4.txt                PARSE FAIL PPLError: <ppl>:185: expected a name after EXPORT
--- 5. line count, size ---
2370 lines, 88111 bytes

bare-head copy ("LOCAL " stripped from the 62 routine heads):  ppl_check tally  14 E9   (v2.4's bare copy: 14 E9)
ppl_gate_v1.py: 2. tally as above, hard errors none; 3. lint_ppl 1062 checks, 19 problems (the same lines);
                5. fleet_names_v2: 0 untagged, 0 mixed-tag, 0 built-in matches

ppl_gate_v1a.py (absolute paths): 2. as above; 3. as above; 5. fleet_names_v2 over 27 files (newest of
                each program): 0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.  RESULT: PASS
                (1. kit lint and 4. parse are skipped there -- no kit zip in out/; check.sh ran both above)
```
- **The E1/E7 growth is the routine-head form, as in v2.4.** `ppl_check` does not read `LOCAL pv_Name()` as a routine head, so every LOCAL inside one counts as undeclared (E7), and an indexed LOCAL list counts as a call (E1). On the bare-head copy the tally is **14 E9, the same as v2.4's bare copy**. The 14 E9 are v2.4's `STRING(n,1,0)` on integers; the new code shows whole numbers with `pv_IStr`.
- **The 14 "STRING() with N args" lint lines are the lint matching `STRING(` inside `INSTRING(`**, plus the kit's own one-argument `STRING(CAS(pv_S))`. Each flagged line was checked by script.
- The parse failure is the kit interpreter's known limit (file-level LOCAL after an EXPORT list); v2.4 fails the same way. Harness v3 loads and runs the whole file.
- **fleet_names_v2 over the newest version of each of 26 programs in `out/`** (the parallel CAS versions included): **0 collisions, 0 untagged, 0 mixed-tag, 0 built-in matches.** The 14 new `pv_` routines are defined before use; the routine heads are now 62 (v2.4: 48), all in the `LOCAL pv_Name()` form.

## Verification (`python3 verify_PowerViz_v2.5.py`: 55 checks, ALL PASSED)

**Part A: the CAS templates through desktop Giac 1.9 against SymPy, SciPy and statsmodels.**
- A1: the four symbolic solves, built as `pv_Eq` builds them, all equal ((zα·u + zβ·w)/δ)² with the program's u, w (SymPy, 20 random points each):
  - test 1 `((pvs*pvza+pvs*pvzb)/pvd)^2`;
  - test 2 `((sqrt(2)*pvs*pvza+sqrt(2)*pvs*pvzb)/pvd)^2`;
  - test 3 `((sqrt(-pvp^2+pvp)*pvza+sqrt(-pvr^2+pvr)*pvzb)/pvd)^2`;
  - test 4 `((sqrt(2)*sqrt(-pvm^2+pvm)*pvza+sqrt(-pvp^2+pvp-pvr^2+pvr)*pvzb)/pvd)^2`.
- A2: **32 numeric templates** (σ 15, 2.5, 1, 0.75; means with negatives and decimals; proportions 0.02-0.98 and 0.123), evaluated at the plot's z for 7 α × 2 tails (448 values), all equal the PPL closed form.
  - The closed form equals statsmodels in all 448 cases: `normal_sample_size_one_tail` for tests 1 and 3, `NormalIndPower.solve_power` (ratio 1) for test 2 (its root finder did not converge in 15 cases with n > 1000, where its closed-form helper was used), and `samplesize_proportions_2indep_onetail` for test 4, one- and two-sided.
  - No CAS text holds a decimal point.
  - The defaults give: test 1 `(3*pvza+3*pvzb)^2`, test 2 `(3*sqrt(2)*pvza+3*sqrt(2)*pvzb)^2`, test 3 `(5*pvza+2*sqrt(6)*pvzb)^2`, test 4 `(3*sqrt(22)/2*pvza+7*pvzb)^2`.
- A3, ⌈n*⌉ against the brute-force n₈₀ of the program's own model:
  - **1-sided, equal in 222 of 222.**
  - **2-sided, 215 equal, 5 one smaller, 1 two smaller, never larger.** The cases: test 1 α 0.2 n* 1014.27 → 1015 vs 1014; test 2 α 0.2: 2028.54 → 2029 vs 2027, and 507.13 → 508 vs 507; test 4 α 0.2: 898.4, 114.1, 205.0 → n₈₀ one smaller each.
  - ⌈statsmodels NormalIndPower two-sided⌉ (both tails) = n₈₀ in 95 cases (17 skipped where its solver did not converge).
- A4: `pv_RatS` is exact (15, 25/10, −5, 55/100, …) and gives up beyond 6 decimals.
- A5: the `factor()` trap shown numerically.

**Part B: the program in harness v3, with `cas='giac'`, `cas='fail'` and canned answers.**
- B1/B2, all 4 tests × both tails:
  - the panel reads "n₈₀ = 56 (55.6)", "71 (70.6)", "112 (111.3)", "142 (141.3)", "153 (152.5)", "194 (193.8)", "305 (304.99)", "388 (387.3)";
  - each n₈₀ line is inside the panel and clear of the SE line (estimated);
  - each formula page has the CAS solve, the CAS numbers, the PPL n, "Round UP … = n₈₀" and the right 1-/2-sided explanation, with nothing past x 318 or y 212;
  - test 1's lines were checked word for word.
- B3, five openings of the page: **2 + 0 + 0 + 0 + 1 CAS calls**. Reopening, changing n (Up) and changing α (α+) cost nothing. A μ₁ change cost one call. After α+, the PPL line reads z(0.9) = 1.282.
- B4: an H1 drag, an n drag, the arrows and the soft keys made **0 CAS calls**; the bracket followed the drag.
- B5, **`cas='fail'`**: no error. The page says "decimal", shows the textbook form and "(no CAS line with p₀ = 0.5, p₁ = 0.6)", and keeps PPL's n. The panel is the same as with the CAS.
- B6: 2-sided, α 0.20, μ₁ 101 gives "n₈₀ = 1014 (1014.27)", "Round UP … n = 1015; trying n: n₈₀ = 1014" and "lets n₈₀ stop 1 sooner."
- B7: with no effect, "n₈₀: no effect" appears with no bracket, the page says "no n is enough", only the symbolic call is made, and there is no error.
- B8: the menu has 9 items and "Sample-size formula" opens the page; help has 3 pages, all inside the screen.
- B9: the Pow-n view shows magenta "formula: 55.6 → 56".
- B10: answers wrapped in quotes are stripped by the kit and stay exact. An approximate-mode answer ("9.0*pvza^2+…") is refused: "decimal", and no CAS number line.
- B11: in stale-key mode, menu → formula page skips nothing.
- B12, **v2.4's own 65-check verification run against v2.5**: it runs to the end, and 64 pass. The 1 failure, "Help: two drawn pages", is the intended third page; the regression copy scripts one extra key for it.

Desktop Giac took about 30 ms per call. That says nothing about the calculator.

## (b) DEVICE TEST CHECKLIST: least to most risky (G2 first; then 8-10 again on the G1 with a stopwatch)

1. **Run CASProbe beta 1 first**, on both calculators.
   - If it reports a different call form, change only the IFERR line in `pv_Cas` (line 376).
   - Note three of its answers:
     - how a `solve` answer is wrapped (`{…}`, `[…]`, `list[…]`; `pv_Strip` removes all three);
     - whether it writes `sqrt(…)` or `√` (both display fine);
     - the G1's time for a `solve`.
2. **Paste.** The routine heads are still `LOCAL pv_Name()`; if the editor stops on one, run LocalHeadProbe and strip "LOCAL " from the 62 heads (v2.4's note). A stop anywhere else is new: note the line.
3. **The panel (PPL, no CAS).** 1-Sample Mean, defaults: bottom right, in green, "n₈₀ = 56 (55.6)". It must not touch the SE line on its left. Check the ₈ glyph (as in v2.4).
   - Two Proportions: "n₈₀ = 305 (304.99)".
   - Drag H₁ or the critical line: the bracket changes with the drag, with no extra lag.
4. **Keys and soft keys as in v2.4** (v2.4 checklist 4-6): unchanged.
5. **Menu**: 9 items, "Sample-size formula" 6th. Help: 3 pages; page 3 is "the n formula".
6. **Pow-n view**: under "n₈₀ = 56", magenta "formula: 55.6 → 56". Check that the arrow (CHAR 8594) renders.
7. **The no-CAS look** (cannot be forced on the device; only if step 8 shows "decimal"): the page then reads "(no CAS: the formula as textbooks print it)" with "n = ((zα+zβ)×σ/(μ₁−μ₀))^2", and the numbers are still there.
8. **The formula page (first CAS step).** Tap the n₈₀ line. You should see, for 1-Sample Mean at the defaults:
   - "exact (CAS)" in the header;
   - "CAS, solved for n:" / "n = ((σ×zα+σ×zβ)/(μ₁−μ₀))^2";
   - "CAS, with σ = 15, |μ₁−μ₀| = 5 (z kept exact):" / "n = (3×zα+3×zβ)^2";
   - "PPL: zα = z(0.95) = 1.645, zβ = z(0.80) = 0.842" / "n = ((15×1.645 + 15×0.842)/5)^2 = 55.64";
   - "Round UP (whole people): n = 56;  trying n: n₈₀ = 56";
   - "1-sided: the formula is exact, so the two agree."

   **The Prime's Giac may arrange the formula differently** (for example σ^2×(zα+zβ)^2/(μ₁−μ₀)^2). That is fine if it is the same formula; note what it shows. **G1: note the "CAS: … ms" in the footer.**
9. **The cache.** Close the page and open it again: the footer should show only a few ms (nothing was asked). Press α+ and reopen: still a few ms, but "zα = z(0.9) = 1.282" and a new n. Press Right (μ₁ 106) and reopen: one call's time, and "|μ₁−μ₀| = 6".
10. **The other tests.**
    - One Proportion: "n = ((√(-p₀^2+p₀)×zα+√(-p₁^2+p₁)×zβ)/(p₁−p₀))^2" and "n = (5×zα+2×√(6)×zβ)^2", n 152.46 → 153.
    - Two Proportions: the p̂ glyph, the formula wrapped onto two lines after "/", "n = (3×√(22)/2×zα+7×zβ)^2", n 304.99 → 305.
    - Check that the √ (SQG) renders; if not, change `SQG` in `pv_Init`.
11. **The far tail.** Edit μ₁ = 101, α = 0.20, Tails = 2-sided, then tap n₈₀: "n₈₀ = 1014 (1014.27)" on the panel, and on the page "Round UP … n = 1015; trying n: n₈₀ = 1014" and "lets n₈₀ stop 1 sooner."
12. **After the run:** in the CAS view, the CAS settings should be unchanged, and `pvn`, `pvza` should not be defined (a `solve` assigns nothing). Esc exits as in v2.4.

## (c) Not confirmed / left as it was

- **Everything about the CAS on the device**: the call form, how a `solve` answer is wrapped, whether `STRING()` of a symbolic answer is re-parsable text (it only has to be displayable), the quotes, and the speed. A failure of any kind gives the textbook form and "decimal". The panel's n and n₈₀ never depend on the CAS.
- **The Prime's Giac is older than 1.9.** It may solve the same equation into a different but equal arrangement, or (less likely) return two roots. A second root is refused (`pv_CasUse` rejects a comma), and then the textbook form is shown.
- **Whether `CAS("…")` can see a program's local variables**: no PPL name equals a CAS symbol ignoring case, so it does not matter.
- **Whether PPL variable names are case-insensitive**: unknown. Hence the defensive `mm1`/`pW` renames (v2.4 code).
- **Glyphs**:
  - √ (`SQG`, CHAR 8730) is unverified (GfxProbe T14 e), and ₈ (CHAR 8328) is unverified, both as in v2.4;
  - p̂ (CHAR 57345) is verified;
  - → (CHAR 8594) renders per Lessons Learned §13;
  - δ is avoided (unverified): the page names the difference "(μ₁−μ₀)" and so on.
- **Text widths** are harness estimates (5.5 px a character, font 1). The tightest spots:
  - "Round UP (whole people): n = 305;  trying n: n₈₀ = 305" (est. 297 px);
  - the panel's "n₈₀ = 305 (304.99)" beside the two-proportion SE line (est. 25 px gap).
- **Left as it was**: the `LOCAL pv_Name()` routine heads (LocalHeadProbe); `!=` in `pv_FMTP`; Home's `K` in the `MAKELIST` calls of `pv_Init`; the exit MSGBOX and `RETURN PW`.
- **Not added**: no `#cas` blocks, no `CAS.name()`, no Python `cas`, no `factor`, no new soft key (the six still fit; the formula is reached by a tap on n₈₀ or through the Menu).
