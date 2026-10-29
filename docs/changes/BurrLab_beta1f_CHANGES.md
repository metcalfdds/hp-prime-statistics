# BurrLab beta 1f — changes from beta 1e (29 Oct 2026): the Python curve bridge fixed

Built from `parts/` (beta 1e's parts in `parts_beta1e/`); `BurrLab_beta1e.txt` untouched (md5
73c6b5aff8c9). Gate PASS vs beta 1e (`gate_BurrLab_beta1f_output.txt`); case_scan clean; pure
ASCII; `verify_BurrLab_beta1f.py` 3,468 checks, 0 failures (`verify_BurrLab_beta1f_output.txt`).

## The two device faults (beta 1e)

1. Every Up/Down on Explore flashed a Python ValueError traceback, then PPL drew the plot.
   Cause: mode 5 called `num("buPB")`, `num("buPL")`, `num("buPT")` -- file-level LOCALs, which
   `hpprime.eval` cannot see (it reads EXPORTed names only); float() of the reply failed. The PC
   stub resolved any harness global, so the verify missed it.
2. On the G2 BurrLab hung at the menu and On did not break it (paperclip reset).

## What changed

1. **Mode 5's inputs travel in BU_IN** (9 values: C, K, S, x max, columns, view, frame bottom, top,
   left). The block reads and writes only BU_JOB, BU_IN, BU_X, BU_GE, BU_GC, BU_OUT, BU_YP, BU_PZ.
2. **The block catches its own errors**: `run()` wraps `main()` in try/except; an error writes
   BU_PZ = "error: <message>" (double quotes made single) and BU_OUT(12) = -2; nothing is printed.
   PPL falls back silently; the readout says "py FAIL, PPL" (Auto and Python only alike).
3. **Inputs validated before any loop** (`need()`): mode 0..5; mode 5 BU_IN size 9, C, K, S, x max
   finite and positive, columns 1..320, view 0/1, frame height 1..240, left + columns ≤ 320;
   fits: box sane, list sizes 0..20,000, n ≥ 4, bins ≥ 2. Every Python loop is bounded by these
   (or by the simplex/Hessian caps already there).
4. **Fail once** (`buPyBad`, a new file-level LOCAL): after one failure -- no sentinel, or a curve
   the guard refuses -- `bu_PyRun` returns at once and PPL answers for the rest of the session;
   choosing an engine (Fit menu > Engine) clears it. BU_PZ keeps the first failure's message.
5. **No PPL loop waits on Python** (audited; checked in the verify): PYTHON() is one call and the
   answer is read once, so there was no loop to give a TICKS cap or Esc check.

## The verify (`verify_BurrLab_beta1f.py`)

* **Strict stub**: `hpprime.eval` sees only the program's `EXPORT NAME;` lines; any other name is
  returned as its own text (float() fails, as on the device), an assignment to one raises. An
  exception escaping the block is recorded as a "traceback on screen".
* **Part J**: the block's names (grep) all EXPORTed and BU_; no buXxx in the block; beta 1e's block
  under the stub reproduces the device error ("ValueError: could not convert string to float:
  'buPB'"); beta 1f's fits and curves run with nothing refused and no traceback.
* **Part K**: 13 injected faults through the menus (Explore, Up, Up, Down, Esc, Family, Esc,
  Explore, Up, Esc, Quit): 5 bad inputs (1E9 columns, C = NaN, frame bottom 999, zero height,
  view 7), an exception at 5 points (reading BU_JOB, BU_IN, mid-loop, writing BU_YP early and
  late), a missing sentinel, a wrong answer with a sentinel, PYTHON() returning at once. Each: runs
  to Quit, exactly one PYTHON() call in the session, no traceback, BU_PZ / sentinel -2 as expected,
  ≥ 5 interactive Explore pages, PPL statements ≤ 1.05 × the Python-absent path (32,735) + 500. A
  fit failure: PPL fits, one call. The engine re-choice tries Python again.
* `BU_PROG=BurrLab_beta1e.txt python3 verify_BurrLab_beta1f.py` → 112 failures
  (`verify_BurrLab_beta1e_under_strict_stub.txt`): the check catches the beta 1e bug.

Counts unchanged: Python answering 695 PPL statements per Explore redraw (beta 1e 693), PPL path
4,243.
