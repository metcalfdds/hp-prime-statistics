# BiNorm3D beta 1g: changes (15 November 2026)

Round 16. Built from beta 1f by exact replacements (`verify/round16/make_binorm3d_1g.py`; a replacement that does not match exactly once stops the build). 1,610 lines (beta 1f: 1,281).

## Why

Roger, 15 November 2026, had a book of tables checked against fresh calculations (Zwillinger & Kokoska, 2000; the report is `claude/CRC_table_check_2026-11-15.md` in the Project). Two of its tables are about a shot aimed at a target, the circular normal probabilities and the circular error probabilities (pp. 194 and 195), and the report's sixth suggestion for our programs was "Circular error probability in BiNorm3D: the chance a shot lands inside a circle." Of the six suggestions Roger said: "Add all please."

BiNorm3D already drew the bivariate normal as a surface and from above. The CEP is the same picture read as a target: how big is the circle that half of all (x, y) pairs fall in, and what does a correlation do to it?

**What was read.** The library in `D:\HP-Prime` was searched on 15 November 2026 (`libsearch_v1.py` over `Library_Index.db`): no program there computes a CEP. The HP-65 Stat Pac 1 (program 15) and the HP-55 statistics book have "Bivariate Normal Distribution" programs; they were not read. The view is written from the formula below.

## What changed

| What | Where (line numbers in `BiNorm3D_beta1g.txt`) |
| --- | --- |
| **A third view, the target.** Soft key 3 goes 3-D, Cont, CEP and back to 3-D, and its label names the view the next press gives. The target is the pattern from above, x and y from −3 to 3, with a green circle round the mean that holds half of all (x, y) pairs, and a blue ellipse that holds half too. Beside it: "Green circle: holds half of all (x, y) pairs. Its radius is the CEP:", then "R = 1.101" (at ρ = 0.60). Under it: "CEP: the circular error probable, the 50 % circle", then how many times as long as wide the pattern is, and R at ρ = 0. | `bnDrawT` (967 to 1029), `bnTgGrid` (940 to 961), `bnNextV` (1043 to 1048), `bnShow` (1051 to 1056), `bnMenuBar` (550 to 563) |
| **The CEP itself**, one routine: the share of pairs inside a circle of radius R as an integral over the angle, and Newton's rule for the R that holds half. It also sets the ellipse that holds half. | `bnCepC` (857 to 893, with its comment from 834) |
| **Shots.** In the target view soft key 4 is Shots and soft key 5 is Clear (in the other two views they are Slice and Reset, as before). Shots, or a tap on the plot, fires 50 pairs with the correlation on the screen, drawn as dots, green inside the circle and red outside, and the page counts them: "Shots: 50", "inside: 24 (48 %)". 500 shots at the most; one more press says "500 shots is the most: Clear starts again". | `bnShots` (902 to 936), `bnTgTap` (1032 to 1040), `BiNorm3D` (1527 to 1610) |
| **A new ρ** (ρ−, ρ+, the − and + keys, or Menu > Set ρ) works the CEP out again and removes the shots, which were fired at the old ρ. At ±0.9 the page says "ρ stops at 0.9 here". | `bnSetRho` (1065 to 1083) |
| **The arrows do nothing in the target view** (there is nothing to turn and no slice there). In the 3-D view and the contour view they do what they did. | `BiNorm3D` (1527 to 1610) |
| **The menu's second item** names the next view ("Contour view (from above)", "Target view (CEP circle)", "3-D view"). Eight items, as before. | `bnMenu` (1239 to 1271) |
| **Help has six pages** (five before). Page 5, "The target and the CEP", is new. Page 6, "Keys and touch", is beta 1f's page 5 with four lines changed (the header, the line on the views, the line on BN_CEP, the footer) and one more (the target's keys). Pages 1 to 4 are beta 1f's word for word, with 6 for 5 in the header and the footer. | `bnHelp` (1301 to 1401) |
| **Home gets `BN_CEP`**, the CEP for the last ρ, once the target view has been opened (0 until then). | `bnCepC`; the export near the top of the file |
| **The closing line** names the CEP when the target view was opened: "BiNorm3D: ρ = 0.90, E[Y \| X = x] = 0.90 x, CEP = 0.988; ρ in BN_RHO, the CEP in BN_CEP". A session that never opens the view ends with beta 1f's line. | `BiNorm3D` (1527 to 1610) |
| The opening page has two lines more, on the target view, and says "six pages of help". | `bnWelcome` (1502 to 1521), `bnInit` (1407 to 1499) |

**The arithmetic.** With variances A = 1 + |ρ| along the ridge and B = 1 − |ρ| across it, the share of pairs within R of the mean is

P(R) = (2 / (π √(AB))) ∫₀^(π/2) (1 − exp(−R² g(t))) / (2 g(t)) dt, with g(t) = cos² t / (2A) + sin² t / (2B).

The integrand is smooth and periodic, so the midpoint rule at 16 angles is enough: it agrees with 4,096 midpoints to 1 part in 10¹³. Every term is positive. R solves P(R) = ½ by Newton's rule from R = √(2 ln 2) · (AB)^¼, which is the answer for a round pattern of the same area; the steps are counted, 30 at the most, and the PC harness takes 1 to 5. At ρ = 0 the CEP is √(2 ln 2) = 1.1774; it is 1.1597 at ρ = 0.3, 1.1010 at 0.6 and 0.9879 at 0.9, in standard deviations of X (or of Y). The blue ellipse is Q = 2 ln 2, since 1 − exp(−Q/2) = ½.

**Why R shrinks.** As ρ moves away from 0 the pattern grows longer and narrower. A circle wastes less of itself on a narrow pattern, so a smaller one holds half. The ellipse has the pattern's own shape and always covers less area than the circle; the page says so in one line ("Blue ellipse: half too, in less area.").

## Checks

- `verify/verify_BiNorm3D_beta1g.py`: **44 checks, 0 failed** (output beside it).
  - The build (T1): the script makes the filed file byte for byte.
  - The arithmetic (A1 to A6): `bnCepC` equals a reference built on a different integral (over Z₁, with the normal CDF, solved by Brent's method) to 10⁻⁹ at 17 values of ρ from −0.9 to 0.9; at ρ = 0 it is √(2 ln 2) to 12 digits; a second reference, 2,000,000 simulated pairs at ρ = 0.6, −0.9 and 0, puts half inside the circle within 4 standard errors; the ellipse's 61 points are the pixels of Q = 2 ln 2; help page 5 prints the CEP at ρ = 0.6 and 0.9 as the reference gives them (1.101, 0.988). A1b holds the routine's comment to counts made at the 181 values of ρ from −0.90 to 0.90: Newton takes 1 to 5 steps, the smallest R² g at any step is 0.166, and 16 midpoints give P within 10⁻¹³ of 4,096.
  - The shots (S1 to S5): ten volleys make 500 and an eleventh fires none; the count inside is the number of shots flagged inside, and a shot is flagged exactly when its pixel lies inside the circle; the 500 shots have the correlation they were fired with (r = 0.622 for ρ = 0.60, within 4 standard errors); a new ρ removes them.
  - The views, the keys and every way out (V1 to V10, sixteen checks): soft key 3's round and its labels; the menu's eight items and its Esc; the arrows in each view; keys 4 and 5 in each view; a tap on the plot and a tap beside it; ρ at its stops; Set ρ cancelled, refused (0.95) and taken; Esc and Menu > Quit from each view with the closing line read each time; Frame timing and Reset from the target view.
  - Against beta 1f (R1, R2): the 3-D view and the contour view draw exactly beta 1f's shapes and texts in 120 states (five values of ρ, three pairs of angles, the slice off and at three places), but for soft key 3's label in the contour view; a session of the old features shows the same 37 screens in both versions.
  - The help (H1 to H6): six pages; pages 1 to 4 word for word; pages 5 and 6 as written; every line within 296 px at the measured glyph widths (widest 294).
  - Static and layout (G1 to G4, D1 to D3): no `!=`; code ASCII; LOCAL lines of six names at most; every text of the target view inside its width and the screen; no overlap, no text off the screen, no number cut short, no menu title over 31 characters.
- Gate (`tools/ppl_gate_v1e.py` against beta 1f; `verify/round16/gates/BiNorm3D_beta1g.txt`): **PASS**. hp-prime-kit lint 0 errors; `ppl_check_v5` clean; `lint_ppl` 5 reports, as in beta 1f; no name collision in the fleet (31 files, 2,480 routine names).
- Harness smoke test: no error, 0 warnings. `tools/text_overlap_v1.py --walk`: the same report as beta 1f, with no collision.
- Help layout at the calculator's glyph widths (`verify/round16/helpcheck_r16.json`): 6 screens, no reports.
- Monkey test: **1,000 of 1,000 runs OK** (`verify/round16/mk/BiNorm3D.jsonl`; base 16, `--lists`). In its first 300 sessions the target view came up in 69 (`mk/reach_r16.txt`), so a **directed** set was added: 200 sessions that start on the target view and then take the monkey's random keys, taps and menu picks, **200 of 200 OK**, the view on the screen in all 200 (`tools/monkey_directed_v1.py`; `mk/directed/BiNorm3D_target.jsonl`).
- **HP Prime Virtual Calculator 2.4.2 (build 2026-09-09): Check "No errors in the program", and a run** (`verify/round16/vc_checks.txt`, `verify/round16/screens/BiNorm3D_*.png`). The target at ρ = 0.60 with R = 1.101; 50, 200 and 250 shots with 24, 101 and 132 inside (48 %, 51 %, 53 %); ρ+ to 0.90 with R = 0.988 and "Pattern 4.36 times as long as wide"; one press more, "ρ stops at 0.9 here"; the six help pages, every line inside its frame; the closing line whole in its box.

The monkey tests and the run were made on the file before four comment lines were corrected (the step count and a bound in the comment above `bnCepC`). The lines that are not comments are the same (1,022 of them, compared), and the file as filed was Checked again on the Virtual Calculator, "No errors in the program" (23:26).

## On a G1 or a G2 (not yet run)

1. Start BiNorm3D and press soft key 3 twice (its label reads Cont, then CEP). The target should show "Target: CEP, ρ = 0.60" and "R = 1.101".
2. Press Shots four times. The page should read "Shots: 200" and "inside: n (p %)" with p near 50. Note how long a volley takes, and how long the page takes to come back with 500 shots on it: nothing here has been timed on a calculator.
3. Tap inside the plot: 50 more. Tap on the words beside it: nothing.
4. ρ+ until 0.90: "R = 0.988" and "Pattern 4.36 times as long as wide". Once more: "ρ stops at 0.9 here".
5. Menu > Help, pages 5 and 6: every line inside the frame.
6. Esc. The box should read "BiNorm3D: ρ = 0.90, E[Y | X = x] = 0.90 x, CEP = 0.988; ρ in BN_RHO, the CEP in BN_CEP", whole. At Home, `BN_CEP` should be 0.98792….

## Unresolved

- Nothing has run on a G1 or a G2. The target view redraws the grid, two curves and up to 500 dots; its speed on a G1 is not known.
- The step count in the comment (1 to 5) is the PC harness's, which counts in 16 digits. The Prime keeps 12, and its count may differ by a step. The limit in the code is 30.
- On the Virtual Calculator some key presses did nothing on pages that wait in the fleet's `GETKEY` and `MOUSE` loop (`verify/round16/keyprobe_r16.txt`). BiNorm3D waits in that loop. Whether a calculator loses presses is not known; nothing was changed for it in this round.
