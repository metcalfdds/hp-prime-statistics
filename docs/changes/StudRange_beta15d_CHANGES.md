# StudRange beta 15d: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 15c; every beta 15c feature is kept, every number is unchanged, and the #PYTHON srq block is byte-identical. Run only in the PC harness (ppl_run_v3e); not yet on the emulator or on hardware.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 20: "StudRange S-3 (spaces round '='), S-1 as a note on the result page, Home's X as a counter"; details in `findings_F.md`, section 4):

> **S-1. WRONG NUMBER (low: PPL fallback only, deep tail) — the Critical value form accepts α down to 1E-4 but the fallback's accuracy ends near α = 0.005 for small df and large k.** k = 20, df = 3: … α 1E-4 → 94.658 vs SciPy 92.944 (1.8 % high). … The Python engine is right there (5e-6), so a student only meets this when Python has failed. Two fixes, Roger's choice: (a) a finer grid … (b) one line on the result page when `srEng == 2 AND ta < 0.005`.

Roger's decision (the brief, D13): add the note, and leave the Harter year as it stands.

> **S-3. COSMETIC (house style) — the HSD result line has no spaces round "="**: `"α="+…+"  k="+…+"  m="+…+"  ν="+…`.

> **Improvement 2 — `MAKELIST(0, X, 1, …)` uses Home's X as the counter** (877–879, 1334–1335): X is the Function app's plot variable and the one a student most likely has set … A LOCAL counter (T19).

**And Roger's disclaimer** (19 Oct 2026, through the coordinator): a header line beside the distribution terms, and one line on the About page.

## What changed (line numbers: beta 15c → beta 15d)

1. **S-1, a plain note where the fallback may be off.**
   - **The pages:** the Critical value page (sr_CritMode, 1516-1525 → 1555-1580) and the Tukey HSD page (sr_HSDMode, 1570-1579 → 1627-1651).
   - **When:** the PPL engine answered (`srEng == 2`) and α is below 0.005.
   - **What:** two lines take the place of the page's two blank lines. On the Critical value page they read `PPL fallback at α < 0.005:` and `q crit may be off by a few %`; on the HSD page the second line is `q crit, HSD may be off a few %`. Each page keeps 8 lines and its spacing. Otherwise the pages are exactly beta 15c's, the numbers included.
   - **Why "a few %" and no figure:** k has no upper limit on the form, and a sweep of the ported PPL engine against SciPy (k 2-50, df 3-100, α 1E-4 to 0.005) gives at most 1.8 % for k ≤ 20 but 5 % at k 30 and 8 % at k 50 (α 1E-4).
   - **Kept:** the two pages build their lines in a LOCAL list (crH/crL, hdH/hdL) so the first line is written once. The finer-grid option (a) was not taken: it is about four times as slow on a G1, and the brief chose the note.
2. **S-3** (sr_HSDMode, 1571 → 1627): `α = 0.0500  k = 4  m = 8  ν = 28`. That is 32 characters at font 3. With large values (k 20, m 100, ν 1980) it is 37, which ends near x 290 at the harness's 7.5 px a character.
3. **Home's X** (sr_BuildZ 877-879 → 908-916, sr_Cache 1334-1335 → 1330-1374). MAKELIST counts with the LOCAL `bzI` / `cbI`, so building the PPL engine's tables no longer writes Home's X. The tables and the plot cache are identical (verify 10c). This also clears ppl_check_v4's one E7 ("identifier 'X' is never declared").
4. **The disclaimer.**
   - The header (→ 16-18), beside the distribution terms: "DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes."
   - On screen (sr_HelpMode, About page 1/4, → 2459): a ninth line, `Teaching aid; not for legal use.` (32 characters at font 3). With nine lines sr_ShowRes spaces them 18 px apart (y 30-174) instead of 22; the eight lines before it are unchanged.
5. **The header:**
   - both banners (line 2 and the "StudRange beta 15d — Studentized Range Distribution" block at 326);
   - the tested-on lines ("this beta 15d have NOT yet been run on hardware … beta 15d has run only in the PC harness");
   - a "What changed in beta 15d (19 Oct 2026): S1, S3 and Home's X (fleet review 19 Oct; line numbers are beta 15c's)" paragraph (→ 61-88).

   A comment above each changed statement says why. No comment sits inside a bracket.

**Before and after** (harness):

| Where | beta 15c | beta 15d |
|---|---|---|
| HSD page, line 1 (defaults) | `α=0.0500  k=4  m=8  ν=28` | `α = 0.0500  k = 4  m = 8  ν = 28` |
| Critical value page, PPL engine, α 1E-4, k 20, df 3 | `q crit = 94.6581`, a blank line, …, a blank line | `q crit = 94.6581`, `PPL fallback at α < 0.005:`, `q crit may be off by a few %`, … |
| The same with Python answering, or α ≥ 0.005 | | unchanged (no note) |
| Home's X after a PPL critical value or plot cache | written by MAKELIST, as K is (LL §5, a device fact; the harness does not model it) | not touched: the counters are LOCAL |
| About page 1/4 | 8 lines | 9 lines, the last `Teaching aid; not for legal use.` |

## Verification

`verify_StudRange_beta15d.py` was built from the beta 15c script, and every check is kept. It runs on beta 15d in harness ppl_run_v3e. Output is in `verify_StudRange_beta15d_output.txt`: **160 checks, 0 failures**.

Old checks whose expected value moved (each says so):
- **7g (15b vs 15a):** the routines that differ now also include sr_BuildZ, sr_Cache and sr_HelpMode.
- **9c:** checks the 15b → 15c diff, so it reads beta 15c's own file.
- **9d:** the version strings are beta 15d's, and the bracket check reads beta 15d.

New section 10:
- **10a (S-3):** the HSD line before and after, at the defaults and at k 20, m 100, ν 1980; the other lines and EP_HSD are unchanged; no label is glued to its "=" anywhere in the code.
- **10b (S-1):**
  - The Critical value page at 6 states:
    - PPL engine at α 1E-4 (k 20, df 3) and 0.0049: the note;
    - α 0.005 and 0.05: no note, beta 15c's page;
    - Python at 1E-4 and 0.001: no note, beta 15c's page.
  - The HSD page at 3 states, the same way.
  - q crit and EP_HSD are unchanged everywhere.
  - Why: PPL 94.658 vs Python and SciPy 92.944 at k 20, df 3, α 1E-4.
  - The note lines are 30 characters at most.
- **10c (X):**
  - beta 15c counts with X in 5 MAKELIST calls. This is a code check: the harness does not model MAKELIST writing its counter, so the overwrite itself is on the device checklist.
  - beta 15d gives the same q crit, node table, 65-point CDF/pdf cache and window as beta 15c, with X untouched;
  - no MAKELIST counts with X, and bzI and cbI are LOCAL.
- **10d:** the disclaimer is in the header word for word, and on the About page (9 lines, 18 px apart, the first eight unchanged).
- **10e:**
  - the routine diff: exactly sr_BuildZ, sr_Cache, sr_CritMode, sr_HSDMode, sr_HelpMode;
  - the #PYTHON block is byte-identical;
  - outside those routines only comments differ;
  - every removed code line is one of the listed sites, and the added lines carry every fix.
- **10f:** the new names bzI, cbI, crH, crL, hdH and hdL are not built-ins, and no LOCAL line has more than 6 names.
- **10g:** the review's own `check_StudRange.py`, run unchanged except for its path: 0 failures on beta 15c and on beta 15d. The review found no failing check here; S-1 was a finding from its printouts, and 10b is its regression test.
- **8c (kept):** `h.sci_strings` over all 71 beta 15d runs: **none**.

## Gate

`python3 ppl_gate_v1b.py StudRange_beta15d.txt _old/StudRange_beta15c.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 1 error, the #PYTHON block's "unbalanced" (as beta 15c; the review confirmed it is the block's text).
- ppl_check_v4: clean (beta 15c: 1 E7, the undeclared X). There are no hard errors.
- lint_ppl: 18 problems, as beta 15c.
- Full parse: it stops at line 360 (beta 15c 327), the same construct, the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh`: kit lint has 1 error, inside the #PYTHON block only; no hard errors; the parse fails on the same construct as beta 15c.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 15c (open it in the Kit). Then Program Catalog → Check.
2. **S-3:** Tukey HSD with the defaults: the first line reads `α = 0.0500  k = 4  m = 8  ν = 28`, whole, inside the screen.
3. **S-1, with Python answering:** Critical value, α 0.0001, k 20, df 3: a green engine badge, q crit ≈ 92.944, and no note.
4. **S-1, the fallback:** the note can only be seen when Python does not answer (or on a firmware without it). If Python is available, skip this step. Otherwise the same entry shows a red badge, q crit 94.658, and the two lines `PPL fallback at α < 0.005:` / `q crit may be off by a few %` under it, all eight lines fitting above the footer.
5. **X** (only the PPL engine builds the tables that used X, so this needs Python not to answer; skip it otherwise): in Home, `X:=7.25`; take a Critical value (red PPL badge); back in Home, `X` still reads 7.25. Beta 15c would have changed X (MAKELIST writes its counter, as Lessons Learned section 5 records for K).
6. **About page 1/4:** nine lines, the last `Teaching aid; not for legal use.`, all above the footer.

## Unresolved (open decisions touching StudRange; not changed here)

- **D13:** Harter 1959 (Critical value page) vs 1960 (Help). Left as it stands. The finer fallback grid (S-1 option a) was not taken.
- **S-4 (a guess):** the plot's q-crit box text at font 2 may cross the box's right edge by two pixels. Eyeball once.
- **Seen, not changed:** the PPL engine's P-value page at large k. At k = 50 its p is off by up to about 5E-5 at every p (so the 5th decimal is off), and by 35 % relative at p = 1E-4. At k ≤ 20 it is within 8E-6. The note was not extended to the P-value page: S-1 concerns α, and the P-value page has no α. Roger may want the same note there for k > 20.
- **Review improvements** (not in this pass): the simulation's overflow count, Tukey's underlining, the P-value page's thumbnail, the em dash and other glyphs to eyeball.
