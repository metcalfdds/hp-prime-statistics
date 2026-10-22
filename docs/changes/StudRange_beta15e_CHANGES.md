# StudRange beta 15e: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 22 October 2026. Built on beta 15d; every beta 15d feature is kept, every page and every line of text is unchanged, and the #PYTHON srq block is byte-identical. One line of arithmetic changed, in the PPL engine's plot cache. Passed the gate; run in the PC harness (ppl_run_v3e); not yet on the emulator or a calculator.*

## Why

An independent re-check of the fleet on 22 October 2026, in a fresh environment (the gate with hp-prime-kit, the harness with Giac, SciPy 1.18.1, statsmodels 0.15), called the programs' own statistical routines through the harness and compared 281 answers with SciPy, statsmodels and brute-force enumeration. Every formula agreed. One number did not:

> **The PPL engine's plot cache is off by up to 2 percentage points from df about 50 to 100.** `sr_Cache` passes the outer Simpson grid over s with 32 nodes for df 8 and above (64 only below df 8). The density of s narrows as df grows, to a width of about 1/√(2 df), and between df 50 and 100 the 32-node grid over u = √s (u from 0.001 to √(1 + 9/√df)) steps over it. The cached CDF behind the Plot page's curve, its shading and the p it reads at the observed q is then wrong: at df 90, k 6, `sr_SRCDF` returns 0.968 at SciPy's 95th percentile (true 0.950); at df 70, 0.943; at df 100, 0.968. With 64 nodes, which the Critical value page (`sr_CritMode`) and the P-value page (`sr_PvMode`) already pass, every df tested from 8 to 1000 agrees with SciPy to five decimals. Above df 100 the spike branch of `sr_SRCDF` (beta 15) was already exact at 32 nodes; it is the 8 to 100 branch that needed the finer grid.

This contradicts beta 15's note that "df 100 and below: unchanged" was safe; it was safe for the pages that pass 64 nodes, not for the cache. It affects only the PPL engine, which answers when MicroPython does not (`srEng == 2`, red badge). On a calculator whose Python answers, the cache comes from `sr_PyRun(3)` and nothing here applies.

## What changed (line numbers: beta 15d → beta 15e)

1. **sr_Cache** (1364 → 1386): `IF cbV<8 THEN nsp:=64; ELSE nsp:=32; END;` is now `nsp:=64;`, with a comment saying why. The inner grid (`nzp`, 24/32/48 by k) is unchanged; the inner grid was not the cause (48 nodes gave the same error as 24 at the same df).
2. **The header** (2, 23-30, 62-78, 344): version, the hardware note (15e has run only in the PC harness), and a "What changed in beta 15e" block.
3. **Nothing else.** No text a student sees changed; no page, key or tap changed; the #PYTHON block is byte-identical (same MD5 of the `#PYTHON … #END` lines in both files).

**Cost.** The PPL cache build evaluates 65 CDF values plus the q-range search, each now over 64 instead of 32 nodes, so the build takes about twice as long when the fallback runs (harness: 6.3 s → 12.1 s at k 6, df 20). The beta 15d note S-1 declined a finer grid for the Critical value page because that page's grid was already 64 and finer still would be "about four times as slow on a G1"; this change only brings the cache up to the grid the pages already use. If the G1 build is too slow, the rule `IF cbV<8 OR cbV>24 THEN nsp:=64; ELSE nsp:=32; END;` keeps 32 nodes where they were exact (df 8 to 24) and was not taken only because the plain rule is easier to check.

## Verification

`verify/verify_StudRange_beta15e.py`, output beside it. It runs from the repository as is (it finds `tools/ppl_run_v3e.py` by relative path and reads beta 15d from git history when the file is absent).

- **Section A**, `sr_SRCDF` at SciPy's q(0.95; k, df) with 32 and with 64 nodes, k 3 (inner grid 24) and k 6 (inner grid 48), df 8 to 101. At 32 nodes: 0.9500 at df 8 to 20, then 0.9498, 0.9503, 0.9519, 0.9460, 0.9433, 0.9540, 0.9675, 0.9684 at df 30 to 100, and 0.9499 at df 101 (the spike branch). At 64 nodes: 0.9500 at every df.
- **Section B**, `sr_Cache` on the PPL path, beta 15d and beta 15e, the 65-point cache against SciPy on its own q grid (k, df; max |error|):

| k | df | beta 15d | beta 15e |
| --- | --- | --- | --- |
| 6 | 20 | 0.00003 | 0.00001 |
| 6 | 50 | 0.00191 | 0.00001 |
| 6 | 70 | 0.00689 | 0.00001 |
| 6 | 90 | 0.01755 | 0.00001 |
| 6 | 100 | 0.01910 | 0.00001 |
| 6 | 240 | 0.00009 | 0.00001 |
| 3 | 60 | 0.00395 | 0.00003 |
| 10 | 80 | 0.00664 | 0.00013 |
| 4 | 5 | 0.00012 | 0.00012 |

- df 5 (k 4) already used 64 nodes and is identical in both; df 240 (the spike branch) was already exact. The harness build time roughly doubles (6.3 s → 12.6 s at k 6, df 20; 7.0 s → 13.5 s at k 10, df 80).
- **The Critical value and P-value pages** were not touched and were checked in the same review: `sr_SRCrit(0.05, k, df, 64)` with the page's own inner grid matched SciPy's `studentized_range.ppf` to four decimals at (k, df) = (10, 60), (8, 60), (12, 60), (10, 20), (10, 120), (6, 60); the 32-node grid gave 4.69 for 4.65 at (10, 60), which is how the cache's error was first seen.

## Gate

`ppl_gate_v1c.py StudRange_beta15e.txt StudRange_beta15d.txt`: PASS. hp-prime-kit lint 0 errors (405 #PYTHON lines blanked); ppl_check_v4 clean, original clean; lint_ppl 1127 checks, 18 problems, the same 18 as beta 15d (the #PYTHON block's depth and the `dvG` LINE_P line); full parse fails on the forward declarations, as beta 15d's does (tool limit); fleet names 19 files, 1132 routine names, 0 collisions.

## Device checklist (emulator first, then G2 and G1)

Only the PPL engine changed, so every step below needs Python NOT to answer. On a calculator whose Python answers, skip to step 5.

1. **Force the fallback.** From Diagnostics, or with the Terminal closed so `sr_PyRun` times out, take the Plot page to k 6, df 90. The red PPL badge should show. The build message "Building distribution cache..." should take about twice as long as beta 15d took at the same k and df; note the seconds on a G1.
2. **The number.** On the Plot page at k 6, df 90, set the observed q to 4.22 (SciPy's 95th percentile is 4.2185). The p read from the cache should be about 0.05; beta 15d gave about 0.032 here.
3. **The curve.** At k 6, df 90, the CDF curve should rise smoothly to 1. Beta 15d's cache was 1.8 points high around q 4.2 and this may have shown as a bump; it has not been looked at on a screen.
4. **Small df unchanged.** k 4, df 5 (the branch that already used 64 nodes): same curve, same p, same build time as beta 15d.
5. **Python path unchanged.** With Python answering (green badge), k 6, df 90: same curve and p as beta 15d, same build time (the Python cache is untouched).
6. **Critical value and HSD pages unchanged.** k 10, df 60, α 0.05 on both engines: q crit 4.6463 (SciPy 4.6463); beta 15d gave the same on these pages.

## Unresolved (open decisions touching StudRange; not changed here)

- **D13** and **S-1** stand as in beta 15d: the Critical value page's note at α < 0.005, and the Harter year.
- **The P-value page at large k** (beta 15d, "Seen, not changed"): unchanged.
- **The build time on a G1** with 64 nodes at every df is not known; step 1 above measures it. If it is too slow, the df 8 to 24 exception above is the fallback.
