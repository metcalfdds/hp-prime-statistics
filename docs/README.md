# Documentation

| File | What it is |
| --- | --- |
| `lessons-learned_v7j.md` | The main reference: PPL, CAS and MicroPython behaviour found on hardware, and the house rules that came out of it. Start here. |
| `micropython-on-the-prime.md` | Field notes on the Python side: what the interpreter is, how the bridge fails, and when it is worth using. |
| `implementation-notes.md` | Why the code looks the way it does. Annotated excerpts, for people who write PPL. |
| `historical-cross-checks.md` | Worked examples from HP's own 1970s statistics programs, used as a second check on NormExplorer and BayesTree, plus reference cases for testing your own programs. |
| `normexplorer-guide.md` | User's guide to NormExplorer (beta 42a), written for students. |
| `chitable-guide.md` | User's guide to ChiTable (beta 3d), the two-way-table chi-square program, including Newcombe's interval for the risk difference. |
| `studrange-guide.md` | User's guide to StudRange (beta 15a, with the MicroPython engine). The program is now beta 15d. Since 15a: the Quit summary counts the plot and the first tap after a page closes is no longer skipped (15b); an exact 0 prints "p < 0.00001" (15c); a note appears when the PPL fallback answers at α < 0.005, and Home's X is left alone (15d). |
| `scatterlab-guide.md` | User's guide to ScatterLab (beta 2a). The program is now beta 2c. Since 2a: the calculus page no longer stops the program and small values print as decimals (2b); 140000000000 prints whole (2c). |
| `binorm3d-guide.md` | User's guide to BiNorm3D (beta 1). The program is now beta 1a: one help sentence and one menu line are corrected. |
| `cicatcher-guide.md` | User's guide to CICatcher (beta 2a). The program is now beta 2c. Since 2a: the setup menu says "Exact (C-P)" for Clopper-Pearson (2b); two menu lines are shortened to fit (2c). |
| `errorrate-guide.md` | User's guide to ErrorRate Lab (beta 1a). The program is now beta 1d. Since 1a: small rates print as decimals and the decimal fallback works if the CAS fails (1b); "1 profile searched" and no "= <" (1c); the CAS page keeps its last line and the opening page shows the disclaimer (1d). |
| `changes/` | One file per program version: what changed and why, with line numbers; the lint and verification output; and the device-test checklist, ordered from least to most risky. |
| `dev/` | The fleet review of 16 October 2026 and the CAS-and-MicroPython plan that drove the touch, graphics and CAS versions, kept as a record of how the work was planned; and the reports of the two emulator rounds of 17 October 2026 (`emulator-round1-2026-10-17.md`, `emulator-round2-2026-10-17.md`; round 2 includes the retest of its fix versions). |

The guides say "not yet run on hardware" in their firmware line until a calculator has run that version, and they name any run on the HP Prime Virtual Calculator. Only the ChiTable and NormExplorer guides were updated for the fix versions of 17–19 October 2026; where a program is newer than its guide, the table says what changed. Each version's file in `changes/` has the details.

**DISCLAIMER: these programs are teaching and demonstration aids. They are not validated for forensic, clinical or legal use; do not rely on their results for legal purposes.**

All of it is free for educational and personal use; see the LICENSE in the repository root.
