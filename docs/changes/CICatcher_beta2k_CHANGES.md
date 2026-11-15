# CICatcher beta 2k: changes (14 November 2026)

Round 14. Built from beta 2j by three exact replacements (`verify/round14/make_round14.py`).

## Why

The status note of the book *Statisticles* had carried one leftover since Round 12: help page 2 said "the catch rate rises", and no page explains a "catch rate". Page 1 calls it the share of intervals the method catches, and "the 'all' rate at the top of the screen". Roger, 14 November 2026: "go ahead and do the program work".

## What changed

| Help page | beta 2j | beta 2k | Line |
| --- | --- | --- | --- |
| 2/6 | "... red lines turn blue and the catch rate / rises. 99 % catches more ..." | "... red lines turn blue and the share / caught rises. 99 % catches more ..." | 1944, 1945 |
| 6/6 | "CQ_COVER (the 'all' catch rate)." | "CQ_COVER (the 'all' rate)." | 2026 |

No other line of code changed; the header and the history note name the version.

## Checks

- `verify/verify_CICatcher_beta2k.py`: **6 checks, 0 failed**: the build makes the file byte for byte; only the three literals and comment lines differ; the six help pages dumped by the harness differ in those three lines; no help page says "catch rate"; every help line fits at the calculator's glyph widths (the two new lines of page 2 are 277 and 290 px of 296); the smoke test.
- Gate against beta 2j: **PASS**.
- **HP Prime Virtual Calculator 2.4.2: Check "No errors in the program"** (`verify/round14/vc_checks.txt`). The help pages were not opened there; the layout check at the measured widths stands for them.

## On a G1 or a G2 (not yet run)

1. Menu > Help, page 2: the first paragraph ends "... red lines turn blue and the share caught rises." inside the frame.
2. Page 6: the last line reads "CQ_COVER (the 'all' rate)."

## Unresolved

Nothing new. The page-2 line "99 % catches more" keeps the space before %, CICatcher's own style (Lessons Learned v7zr).
