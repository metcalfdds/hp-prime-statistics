# PowerViz v2.5i: changes

*Superseded the same afternoon by v2.5j and v2.5k (the t obtained under POWER, and the new box in every test; see `PowerViz_v2.5j_CHANGES.md`). v2.5i was filed but not committed. Its verify script, `verify_PowerViz_v2.5i.py`, is in the author's folder; `verify_PowerViz_v2.5k.py` runs its checks on v2.5k (v2.5i's "df = …" line is now the t line).*

*31 October 2026, late afternoon. Built from v2.5h by `make_v25i.py` (26 exact replacements, each required to match once). 3,781 lines: 2,374 of code and 1,239 of comments. v2.5h was not committed on its own; this version carries it (see `PowerViz_v2.5h_CHANGES.md` and `PowerViz_v2.5g_CHANGES.md`).*

## Why

Roger ran v2.5h on his Prime on 31 Oct 2026, using test 5 with his own SPSS output (Amount of Drugs Use Experience by sex: male n 270, mean 4.8185, SD 3.28798; female n 146, mean 6.4247, SD 3.74872).

- **"when I edit the values and click OK the plot flashes on and then we go to the PowerViz Menu".** A real fault (below).
- **The panel read "β = 3.534E-96"** in his screenshot; it should read "β < 0.001". A second fault (below).
- **"why is one plot centered at 0 and the other at -8 something?"** Not a fault: μ grp1 had been typed as 14.8185. The harness reproduces his screen exactly with that value: d = −2.38, POWER > 0.999, n₈₀ = 5/3 (4.1). With 4.8185, H₁ sits at +1.61, d = 0.46 and power is 0.992.
- Then: "display mu 1 also"; "for the n sizes, better to use a , separator -- right now it looks like a fraction"; "we need to see the std dev's too I think -- rework the output box please"; "the other tests should have both groups too"; and "we need to put in the df also -- even the fractional one".

## What changed (line numbers are v2.5i's)

### A finger left on a form's OK was read as a tap on Menu

- **What happened:** the Edit form's OK sits where PowerViz's sixth soft key, Menu, is. The form closed while the finger was still on the glass, so the live loop's next `MOUSE` reading was that same touch, at slot 6, and the menu opened.
- **Why the drain missed it:** after a form or menu the program drained keys only (`pv_Drain`). Lessons Learned §7 already says a `GETKEY` drain does not drain touch.
- **The fix:** every form and menu opened from the live loop is now followed by `pv_TDrain` too, the capped finger-lift drain, as the start of the program already was. That covers:
  - Edit and Menu (`pv_Soft`, 3533);
  - the n, effect, α and n₈₀ cells (`pv_Touch`, 3559);
  - Enter (the live loop, 3749).
- **Until v2.5i is on the calculator:** press Enter instead of tapping OK.

### "β = 3.534E-96" instead of "β < 0.001"

- `pv_FMTP`'s floor test (1186) read `IF xx != 0 AND ...`. It was the only `!=` in the program.
- The PC harness reads `!=` as "not equal", and there the floor works. On the calculator it evidently did not: the value went on to `STRING(x, 2, 3)`, which prints scientific form below 10⁻³.
- It is `xx <> 0` now, the form the rest of the fleet uses on the device (on 22 lines of v2.5h alone).
- **That `!=` is the cause is likely, not proven.** Device checklist item 21 settles it.

### The two-group tests' readout box (`pv_PanelG`, 1627)

Tests 2, 4 and 5 get a small table with a column per group:

```
         group 1   group 2    d = 0.46, small        POWER
  n          270       146    zcrit = 1.960          0.992
  μ        4.819     6.425    α = 0.050
  σ        3.288     3.749    β = 0.008              df = 265.9
  SE₀ = 0.369                            n₈₀ = 112, 61 (111.96)
```

- **The rows:**
  - n, then μ and σ in tests 2 and 5, or n and p in test 4;
  - test 2's n and σ are the same in both columns, which is what "equal σ and n" means;
  - the two means share their decimals (`pv_MuDec`, 1038), so a typed 4.8185 shows as 4.819.
- **Beside the table:** d or h in magenta (as the arrow), zcrit, α and β; POWER large on the right, and under it the df; the SE line and n₈₀ on the bottom row, as before.
- **The plot** in those three tests ends 13 px higher to make room (PYB 133, set in `pv_Setup`, 1331). The box runs from y 150 to 217, with font 1 rows every 13 px.
- **Taps:**
  - the n row edits n;
  - the μ or p row edits the effect;
  - the σ row opens the whole Edit form (new, `pv_Touch` 3585);
  - d or h edits the effect, zcrit and α the α ladder, n₈₀ the formula page.
- **Tests 1 and 3** (one sample) keep their box. It reads "n = 30", no longer "n = 30/grp".

### df under POWER (`pv_DF`, 1595)

Roger: "we need to put in the df also -- even the fractional one".
- **Test 5:** Welch's t test, the Welch–Satterthwaite df, fractional: (a + b)² / (a²/(n₁ − 1) + b²/(n₂ − 1)), with a = σ₁²/n₁ and b = σ₂²/n₂. It is shown to one decimal, "df = 265.9".
  - SPSS's "Equal variances not assumed" row uses the sample SDs the same way, so typing a sample's SDs and n's gives SPSS's df. With Roger's data it is 265.924, as SPSS printed.
  - The σ's are divided by the larger first, as in `pv_Model`: df does not change, and nothing squares out of range.
- **Test 2:** the pooled t test, 2n − 2.
- **Tests 1, 3 and 4:** no df is shown (test 1 keeps its old box; proportions are z tests).
- PowerViz still works with z, so df changes no number. It is there so the screen can be read beside SPSS's.

### No "/" that reads as a fraction

- **Test 5's n₁ and n₂** read "40, 20" everywhere (`pv_NStr`, 631): the panel, n₈₀, the Power-vs-n screens, the hints, the formula page and the Levene page.
  - Where n sits in a list, the items are now separated by ";": "n = 40, 20; α = 0.050; 1-sided" and "σ = 10, 20; n = 40, 20; α = 0.050 (2-sided)".
- **Tests 2 and 4** read "n = 30 per group" in the Power-vs-effect subtitle and the exit box.
- **Tests 1 and 3** read "n = 30".

### Help

- Help page 2's readout lines say "μ, p, d or h = type the effect" and "α or zcrit = the α ladder;  σ = the Edit form".
- Help page 4 says "box: n, μ, σ by group" and "n₈₀ = 40, 20".

## Not changed

- The engine: every number of every test. Verify A1 checks the eight engine values against v2.5f in 512 states.
- Tests 1 and 3's screens, apart from "n = 30".
- The Levene and two-samples pages, apart from the Levene page's first line.

## Verification

`verify_PowerViz_v2.5i.py`, output `verify_PowerViz_v2.5i_output.txt`: **94 PASS, 0 FAIL**.

- **A, against v2.5f:**
  - tests 1 and 3, screen for screen;
  - tests 2 and 4: the new box shows every text v2.5f's box showed except its n and μ₂/p₂ cells, and its table holds the right values;
  - the curve views and the formula page;
  - help pages 1–3, each allowed difference checked for what it is.
- **H, new:**
  - **A finger held on OK.** The harness is made to leave the finger on the glass when a form or menu closes, as on Roger's calculator.
    - After Edit, the n row and Enter → Return to plot, no stray menu or form opens.
    - A copy without the new `pv_TDrain` opens the PowerViz Menu, so the harness reproduces Roger's report.
  - **The σ row** opens the Edit form.
  - **The floor:** no `!=` in the code, and `pv_FMTP(3.534E-96, 3)` = "< 0.001".
  - **df:** `pv_DF` equals the Welch–Satterthwaite formula in 7 cases, including σ of 1E-200 and 1E200. Roger's data gives 265.924, as SPSS printed. The panel shows "df = 265.9" (test 5) and "df = 58" (test 2, n 30), and nothing in tests 1 and 4.
  - **Roger's own numbers:**
    - the table reads 270, 146; 4.819, 6.425; 3.288, 3.749;
    - d = 0.46, POWER 0.992 (SciPy 0.9916);
    - SE₀ = 0.369, which matches SPSS's .36918;
    - n₈₀ = 112, 61.
  - **His slip** (14.8185) gives "β < 0.001" and "> 0.999".
  - **The plot's bottom edge:** 133 in tests 2, 4 and 5, with the tick labels ending above the box.
- **B, C, E, F, G:** every check of v2.5h's script, with test 5's expected texts updated to the new box and "40, 20".
- **D, layout:** no firm overlap, straddle or overrun that v2.5f lacks.

## Gate

`ppl_gate_v1c.py PowerViz_v2.5i.txt PowerViz_v2.5h.txt`: **RESULT: PASS**.
- No new E1 note.
- The full-parse step stops at the bare `EXPORT EP_…;` lines, as on v2.5h.
- lint_ppl's four problems are the version number in the file name, as on v2.5h.

## Device checklist (G2 first, then G1)

Items 1–12 of `PowerViz_v2.5g_CHANGES.md` and 13–18 of `PowerViz_v2.5h_CHANGES.md` still apply. Then:

19. **Edit, then tap OK:** the plot comes back and stays, with no menu. Repeat by tapping the n row and then OK, and with Enter → Return to plot.
20. **Test 5 with Roger's numbers** (μ 4.8185 and 6.4247, σ 3.28798 and 3.74872, n 270 and 146, α 0.05, 2-sided):
    - the table reads 270 146 / 4.819 6.425 / 3.288 3.749;
    - d = 0.46, small; POWER 0.992; β = 0.008;
    - SE₀ = 0.369; n₈₀ = 112, 61 (111.96); df = 265.9 under POWER;
    - nothing overlaps.
21. **The `!=` question.** Type μ grp1 = 14.8185 again: β should read "β < 0.001". Then, if `!` can be typed in Home, try `2!=0` and write down what it returns.
22. **Tests 2 and 4:** the group 1 / group 2 table; "df = 58" under POWER in test 2 at n = 30, none in test 4; a tap on the σ row (test 2) opens the Edit form.
23. **Tests 1 and 3:** the box reads "n = 30" and is otherwise unchanged.

## Unresolved

- **Whether `!=` is really the cause** of the β display (checklist 21).
- **Three other programs** have the same `IF pv != 0 AND ABS(pv) < thr` floor in their own format helpers: BayesTree beta 8e (line 721), Norm3 v2.4b (255) and StatDist v2.7f (547, and `TYPE(vv) != 0` at 575). If checklist 21 confirms the cause, they need `<>` too.
- **The rest of the fleet** may open forms from a loop that polls `MOUSE`, so the same finger-on-OK fault may be there too. It has not been swept yet.
