# BurrLab beta 1b — changes from beta 1a (28 Oct 2026) — a TRIAL of a MicroPython engine

Built from `parts/` (beta 1a's parts archived in `parts_beta1a/`, beta 1's in `parts_beta1/`);
`BurrLab_beta1a.txt` untouched (md5 1c0b54b94c50). Gate PASS against beta 1a
(`gate_BurrLab_beta1b_output.txt`; the kit lints a copy with the 371 #PYTHON lines blanked;
lint_ppl's "block depth went negative" is the #PYTHON block, the same noise StudRange beta 15e
shows); fleet_names 0/0/0; case_scan clean over 31 files. `verify_BurrLab_beta1b.py`: 3,059
checks, 0 failures (`verify_BurrLab_beta1b_output.txt`). Harness only; nothing has run on a
calculator. Everything outside the engine plumbing is byte-for-byte beta 1a (same parts).

Why: Roger's first G1 run of beta 1a: the Danish 300 fit took 45 s where the NOTES estimated
10–30 s. Calibration: the fit is about 290k loop statements, so this G1 runs this loop at about
6,500 statements/s, roughly twice as slow as the 30–100× rule gave. Noted in the NOTES.

1. **`#PYTHON bul`** (lines 727–1120): the same Burr fit in MicroPython 1.9.4 — the 18-point
   grid start, the profile Nelder-Mead over (ln C, ln S) with K = n/Σ ln(1 + zᵢ) (raw), the
   48-point grid and 3-D simplex (grouped), the same tolerances (1E-10, 1E-6), iteration caps
   (400/600), box and boundary flags, and the 1 %-step numerical Hessian inverted by cofactors.
   Only `math` and `hpprime` imported; no f-strings, lists only. Modes: 0 probe, 1 raw fit,
   2 grouped fit, 3/4 Hessian. The bridge follows StudRange beta 15e and Lessons v7s §9: inputs
   read element by element with `hpprime.eval` (BU_JOB, BU_IN, BU_X, BU_GE, BU_GC), outputs
   written one element at a time as `BU_OUT(j):=<"%.12f">` by string concatenation, the sentinel
   BU_OUT(12) = 1 written LAST, `mark()` → BU_PZ after every step, a progress bar through
   `hpprime.fillrect`.
2. **The three-part guard in PPL** (`bu_PyRun`, `bu_PyDone`, `bu_PyFit`, `bu_PyHess`): BU_OUT is
   cleared to −1 before the call; the answer is validated by using it (the sentinel inside
   IFERR, finite positive values, and the Python ln L reproduced by the PPL likelihood at the
   same (C, S) — `bu_LLProf` / `bu_GLL` — to 1E-6, with the profile K agreeing to 1E-6: a
   disagreement counts as a failure); the PPL engine (`bu_FitPPL`, the old simplex code, and
   `bu_Hess`) is the fallback. The Hessian goes through Python only when Python fitted.
3. **Engine setting** (`buEng`, Fit menu → "Engine (now: …)", kept for the session):
   Auto (Python first, PPL on any failure or disagreement), PPL only, Python only (no
   fallback: "Python engine failed: see the Terminal; switch to Auto or PPL"), Both (Python,
   then PPL, both timed; one line "Py 1.3 s, PPL 45.2 s: same C, K, S to 6 digits" or
   "C, K, S differ by <largest relative difference>"; the Python result is kept; if Python
   fails: "Python failed (see Terminal); PPL alone 45.2 s").
4. **Timing and the badge**: every fit is timed with TICKS (`bu_Secs`, wrap-around safe, tenths);
   the results page shows "engine: MicroPython 1.9.4, 1.3 s" / "engine: PPL (Python
   unavailable), 45.2 s" / "engine: PPL (chosen), …" / "engine: MicroPython 1.9.4 (compared), …"
   (the engine's Burr fit + Hessian time); the Home summary and BU_ENGINE carry the engine and
   the whole fit's time. Help page 4 explains the four settings and says both engines run the
   same algorithm on the same data. Progress labels shortened to fit the bar's width.
5. The rivals, the A-D statistic and all pages stay in PPL (the rivals are about a third of the
   PPL fit time at n = 300; a later version may move them). Results-page SE caveat shortened to
   one line to make room for the badge and the compare line.

Verified (Part E): the block under CPython with a stub `hpprime` on the four presets and the 20
random samples gives the PPL engine's C, K, S, ln L, flag, SEs and evaluation count to 1E-6
(bit-identical in practice); the four settings with Python answering (badges, times, the Both
line, the summary) and with Python absent (Auto and Both fall back and say so, PPL only runs,
Python only reports the failure in a MSGBOX with no runtime error, a doctored Python answer is
refused); the engine menu, help page 4 and the Home summary through the menus; every beta 1a
check re-run on the PPL path.
