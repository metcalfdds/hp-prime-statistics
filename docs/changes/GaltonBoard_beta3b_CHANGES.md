# GaltonBoard beta 3b: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 17 October 2026. Built on beta 3a; every beta 3a feature is kept, including the CAS call form, the Python block, the pour and the drops. Not yet run on hardware or on the emulator.*

## Why: what the emulator showed

GaltonBoard beta 2 and GfxProbe beta 1 ran on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09) on 17 October 2026 (`Emulator_Round1_Results_2026-10-17_v1.md`). Beta 3a draws the same way.

- **GfxProbe T09: "no".** ARC_P at r = 3, 2 and 1 plus the centre pixel, drawn as a solid dot, shows a white **X**: concentric circles leave holes on the diagonals. In GaltonBoard, "every peg shows the diagonal-hole pattern (each looks like ⊕), and so would the falling balls."
- **Cosmetic.** "The bin-count labels sit on the magenta binomial line, so '9' was half hidden."
- GfxProbe T01 and T03 passed FILLPOLY_P. RECT_P has run on both calculators.

## What changed (line numbers: beta 3a → beta 3b)

1. **Solid balls: `gbDisc`** (3a 300–308 → 3b 326–342). Three overlapping RECT_P bars, 7 × 3, 3 × 7 and 5 × 5 px, cover exactly the pixels of a disc of radius 3, the same 7 px ball. The routine's comment draws the pixel map for students.
   - It was ARC_P r 3, 2, 1 plus PIXON_P: four calls. It is now three.
   - RECT_P was chosen over a FILLPOLY_P octagon because it is exact at 7 px and has run on the G1 and G2. FILLPOLY_P has run only on the emulator.
2. **Solid pegs** (gbScene, 3a 937–940 → 3b 1009–1014). Two RECT_P bars, 5 × 3 and 3 × 5, cover exactly a disc of radius 2, the same 5 px peg in the same grey. That is two calls instead of three per peg.
3. **Bin counts clear of the overlays.**
   - New `gbLblTop` (3b 858–887) finds the highest pixel the overlays reach under a label: the magenta square (2 px round its centre), the magenta lines to the neighbouring squares (at the label's two edges, where a straight line is highest), and, when the normal is shown, the green curve in every pixel column of the label.
   - `gbBar` (3a 825–855 → 3b 889–927) now puts the count 2 px above the **higher** of the bar top and that point (3b 916–918).
   - If that leaves no room below the pegs (y 127), the count goes inside the bar, as before.
4. **Header.** A "WHAT CHANGED in beta 3b" paragraph and the status line.

Nothing else changed. The routines that differ from beta 3a are exactly `gbBar`, `gbDisc`, `gbScene` and the new `gbLblTop`; outside them only comments differ. `gbScene` differs from beta 2 only in the peg lines.

## Verification

`verify_GaltonBoard_beta3b.py` (built from the 3a script; harness **ppl_run_v3c**). Output in `verify_GaltonBoard_beta3b_output.txt`: **4130 checks passed, 0 failed.**

- **Kept:**
  - A–C: the exact bin probabilities for R 3–12 against Python `Fraction` and SciPy, and the Poisson limits against SymPy;
  - D: end to end with `cas='giac'` and `cas='fail'`, the "decimal" fallback, and no CAS call in any animation;
  - E: the fence, and the routines that are byte-identical to beta 2, except gbScene's peg lines (checked separately);
  - F: layout;
  - G: beta 3 in v3c still shows the CAS finding.
- **P, pegs and balls:**
  - R 3, 8 and 12: no ARC_P or grey PIXON_P in the scene; every peg is two grey RECT_P covering exactly the 21 pixels of a radius-2 disc;
  - `gbDisc` is three red RECT_P covering exactly the 37 pixels of a radius-3 disc;
  - drawing calls, one drop: 25 frames, 733 calls (3a: 863, 282 of them ARC_P); the busiest frame 172 (3a: 209);
  - drawing calls, ×10 (up to 8 balls in the air): 52 frames, 4075 calls (3a: 4727, 1524 ARC_P); busiest frame 255 (3a: 297);
  - no frame draws more than in 3a; the scene makes 130 calls at R 8 (3a: 166) and 226 at R 12 (3a: 304).
- **L, labels:**
  - 14 boards (R 3–9, p 0.3–0.72, overlays 1 and 2, n 6–1000), 3 seeds each: **253 counts above their bars, 0 collisions** with a magenta square, a magenta line or the green curve;
  - beta 3a in the same 42 boards had **142 collisions**, e.g. R 8, p 0.5, n 110: "29" and "23" on the line, the emulator's finding;
  - with 2000 balls every label stays at y ≥ 127.

## Gate

`python3 ppl_gate_v1a.py GaltonBoard_beta3b.txt GaltonBoard_beta3a.txt` gives **RESULT: PASS**.
- ppl_check_v3: clean.
- lint_ppl: the same problems as 3a. The one "PIXON_P targets 'dcG'" became three "RECT_P targets 'dcG'", the known not-a-GROB noise on a grob parameter.
- fleet_names_v2: 0 collisions, 0 untagged.

With the unpacked hp-prime-kit, the kit lint gives the same single "unbalanced" error as 3a (the #PYTHON block).

## Device checklist (emulator first, then G2 and G1)

1. Paste and run. Look closely at the pegs: each is a solid grey dot, with no white cross or ⊕.
2. Drop (soft key): the falling ball is a solid red disc. On the PC it lands within half a second, so this is easier to see with Pour or ×10.
3. ×10, then ×100 with the overlays on binomial + normal (menu). No count label touches the magenta line or squares or the green curve. The emulator's case was R 8, p 0.50, about 110 balls.
4. On the G1: ×10 and Pour should feel no slower than beta 2 or 3a, because there are fewer drawing calls per frame.

## Not changed (listed, not edited)

The menu's CHOOSE list (3b line 2083) has four items wider than about 30 characters, which the emulator showed CHOOSE cuts at its right edge (ChiTable, TrendTest):
- "Overlays: none / binomial / + normal" (36)
- "Colour bars by distance from Rp (SD)" (36)
- "Pascal's triangle: off / counts / C(r,k)" (40)
- "Send bins to D1, D2 (Statistics 1Var)" (37)

The emulator run did not report them clipped, but they are wider than the two that were. Shortening them is a one-line change for the next version; it was not part of this fix.
