# BiNorm3D beta 1a: changes

*Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude). 19 October 2026. Built on beta 1; every beta 1 feature is kept, and no number changed. Run only in the PC harness (ppl_run_v3e), not yet on the emulator or a calculator. Beta 1 passed the emulator on 17 October.*

## Why

The fleet review of 19 October 2026 (`Fleet_Review_2026-10-19_v1.md`, section 2 item 20; `findings_B.md`, BiNorm3D) listed two items to fix now:

- **N1. WRONG TEXT: "help page 4 has lost a verb."** `BiNorm3D_beta1.txt:981-984` read, as four screen lines: "Criminal justice: offenders chosen for a / programme because their risk score was / extreme score closer to the average next / time, programme or not." The sentence needs "... risk score was extreme WILL score closer to the average next time".
- **N2. COSMETIC: "one menu line is 31 characters."** `BiNorm3D_beta1.txt:872-873`: "Grid while dragging (now 15×15)" / "(now 11×11)". Round 2 on the emulator cut lines of 31 to 36 characters at the box's edge, so the closing ")" was at risk.

Roger's addition of 19 October (12:48 CDT): the disclaimer line beside the distribution terms.

## What changed (line numbers: beta 1 → beta 1a)

1. **N1, help page 4** (`bnHelp`, 981-986 → 1004-1012, with the comment). The paragraph now reads, in six lines of at most 46 characters:
   "Criminal justice: offenders chosen for a / programme because their risk score was / extreme **will** score closer to the average / next time, programme or not.  That drop is / not the programme's effect; only a comparison / group picked the same way shows what it added."
   Only the verb is new. The reviewer's draft also changed "comparison group" to "control group"; that was not needed to fit, so the original wording is kept.
2. **N2, the menu** (`bnMenu`, 872-873 → 895-896): "Grid while dragging: 15×15" (or 11×11), 26 characters. It is the same item with the same action. It keeps the words "Grid while dragging", so the header's "Menu > Grid while dragging turns this off" and help page 5's list still name it. (The reviewer's draft, "Coarse grid while dragging: on" / "off", would have dropped the grid sizes.)
3. **Header:**
   - the banner (4);
   - the disclaimer line after the distribution terms (→ 16-18). The program has no About or Help page that states the terms, so no line was added on screen.
   - the tested-on lines (17-18 → 20-24);
   - a "beta 1a (19 Oct 2026)" paragraph (→ 31-45);
   - a comment above each changed statement.

Only `bnHelp` and `bnMenu` changed: 6 display-string code lines out and 6 in.

**Before and after** (harness ppl_run_v3e):

| Where | beta 1 | beta 1a |
|---|---|---|
| Help, page 4, third line | `extreme score closer to the average next` | `extreme will score closer to the average` |
| Help, page 4, last three lines | `time, programme or not.  That drop is not the` / `programme's effect; only a comparison group` / `picked the same way shows what it added.` | `next time, programme or not.  That drop is` / `not the programme's effect; only a comparison` / `group picked the same way shows what it added.` |
| Menu, item 5 (bnCrs = 0 / 1) | `Grid while dragging (now 15×15)` / `(now 11×11)` (31) | `Grid while dragging: 15×15` / `11×11` (26) |

## Verification

`verify_BiNorm3D_beta1a.py` was built from `verify_BiNorm3D.py`, and every check is kept. Parts A, B and C run on beta 1a with only the file name changed, in harness ppl_run_v1, as before. Output: `verify_BiNorm3D_beta1a_output.txt`: **70 PASS, 0 FAIL, "ALL CHECKS PASSED"** (the beta 1 script had 58).

Part D is new (harness ppl_run_v3e):
- **D1. The review's `check_BiNorm3D.py`** (56 checks) on both versions:
  - On beta 1 exactly its two failing checks fail: F (N1, the verb) and H (N2, a menu line over 30 characters).
  - On beta 1a all 56 pass.
- **D2.** Help page 4 as drawn: the sentence reads through, in six lines of at most 46 characters. Each line ends before x = 308 at 6.2 px a character (widest 297). The menu item reads `Grid while dragging: 15×15` and `11×11` for the two settings, and choosing it still toggles the setting. Every menu item is at most 30 characters.
- **D3.** The routine diff: `bnHelp` and `bnMenu` only (of 30 routines), 6 code lines each way, all display text.
- **D4.** No `//` inside an open bracket; the banner, the beta 1a paragraph, the status line and the disclaimer; every LOCAL line holds at most 6 names; no INSTRING.
- **D5.** No scientific fixed decimal in any of the 31 ppl_run_v3e runs of part D (both versions).

## Gate

`python3 ppl_gate_v1b.py BiNorm3D_beta1a.txt _old/BiNorm3D_beta1.txt` in `gate_f19`: **RESULT: PASS**.
- hp-prime-kit lint: 0 errors.
- ppl_check_v4: clean, as beta 1. No hard errors (E12 included).
- lint_ppl: 5 problems, as beta 1.
- Full parse: it stops at the file-level LOCAL after the EXPORT (146), as beta 1 does at the same line (125). This is the tool's limit.
- fleet_names_v2 over 25 files: 0 collisions, 0 untagged, 0 mixed-tag files, 0 built-in matches.

`bash check.sh BiNorm3D_beta1a.txt BiNorm3D_beta1.txt`: the same.

## Device checklist (emulator first, then G2 and G1)

1. Paste over beta 1 (open it in the Kit), then Program Catalog → Check.
2. **N1.** Menu → Help, page 4: the blue paragraph reads "... their risk score was / extreme will score closer to the average / next time, ...". All six lines are whole, and the last ends "what it added." inside the frame.
3. **N2.** Menu: item 5 reads `Grid while dragging: 15×15` and is whole in the box. Choose it, then open the Menu again: it reads `11×11`.
4. Nothing else on the screens changed. One drag in 3-D and one in the contour view is enough to confirm.

## Unresolved

- Nothing in section 3 of the review (the open decisions) touches BiNorm3D.
- **N3** (at φ = 20-30° the ρ = 0.9 peak rises to row 1) is cosmetic and was not in the fix-now list, so it is left as it is.
