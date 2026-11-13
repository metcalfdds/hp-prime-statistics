# CICatcher beta 2j: changes (13 November 2026)

Round 12 of 13 November 2026: help-page fixes found in the pre-submission read of the book *Statisticles*, which prints every program's help pages exactly as the programs show them. Roger, 13 November 2026: "Go ahead and fix the help files as we need to do that in any case". The build is `verify/round12/make_round12.py`: each change is an exact replacement in CICatcher beta 2i (a miss stops it), then the version (header, history note, version strings).

## What changed

1. Help page 2/6: two sentences where one had "so ... so".

2. **Nothing else changed**, apart from the header, the history note and the version strings.

Lines of CICatcher beta 2j that differ from CICatcher beta 2i: line 4 (comment); lines 46-47 (comment); line 1946 (code). Routines whose code changed, with the number of lines: cqHelp 1.

## The help, before and after

As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen; only the screens that changed.

### Screen 2, before (beta 2i)

```text
CICatcher help 2/6: Level and width; z and t
Drag the right edge (or ⇅): a higher level uses a bigger critical
value, so EVERY line grows, red lines turn blue and the catch rate
rises. 99 % catches more, but its longer lines give a less
precise answer.
z:  ± z × σ/√(n) uses the TRUE σ, so every z line has the
same length.
t:  ± t × s/√(n) uses the sample's s.
s changes from sample to sample, so t lines differ in length, so
t's critical value is bigger than z's to make up for that:
t(9) = 2.262 against z = 1.960.
z with s at n = 10 would catch only 91.8 %.
t critical value: not needed yet (no t run)
any key or tap = next page, Esc = done
```

### Screen 2, after (beta 2j)

```text
CICatcher help 2/6: Level and width; z and t
Drag the right edge (or ⇅): a higher level uses a bigger critical
value, so EVERY line grows, red lines turn blue and the catch rate
rises. 99 % catches more, but its longer lines give a less
precise answer.
z:  ± z × σ/√(n) uses the TRUE σ, so every z line has the
same length.
t:  ± t × s/√(n) uses the sample's s.
s changes from sample to sample, so t lines differ in length.
t's critical value is bigger than z's to make up for that:
t(9) = 2.262 against z = 1.960.
z with s at n = 10 would catch only 91.8 %.
t critical value: not needed yet (no t run)
any key or tap = next page, Esc = done
```

## Checks

- `tools/ppl_gate_v1e.py` against CICatcher beta 2i: PASS. lint_ppl 5 problems, as in CICatcher beta 2i; fleet_names_v2 over the 31 newest files: no collisions.
- `verify/round12/helpcheck_r12.json` (Round 11's `helpcheck_r11.py`, at the glyph widths GlyphProbe_v1 measured): 6 screens, no reports.
- The help dumps (`helppages_before_r12.json`, `helppages_r12.json`): the screens above are the only ones that changed, and they changed only as listed.
- The harness smoke test (main routine, idle key Esc): OK    warnings 0 (old 0).
- `tools/text_overlap_v1.py --walk`: same report as the old version (the walks differ only in their timing): screens 136/237 collisions 0 (firm 0) straddles 0 overruns 0 ghosts 0.
- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 13 Nov 2026: Check said "No errors in the program".

## On a G1 or a G2

Not yet run on a G1 or a G2. To look at: the help page that changed.
