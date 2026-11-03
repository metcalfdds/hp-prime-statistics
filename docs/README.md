# Documentation

| File | What it is |
| --- | --- |
| `lessons-learned_v7zj.md` | The main reference: PPL, CAS and MicroPython behaviour found on hardware, and the house rules that came out of it. Start here. |
| `test-status.md` | The dated record of what has been tested, on what, and what each round found (moved from the top of the README, 27 Oct 2026). |
| `two-shortcuts.md` | Loading the Virtual Calculator by copying files into its folder, and a big data set as one matrix file: how each works, what we found, and who found what (1 Nov 2026). HP's manuals describe neither. |
| `data/` | The sources of every preset in the October 2026 programs, and the checks made on them. |
| `micropython-on-the-prime.md` | Field notes on the Python side: what the interpreter is, how the bridge fails, and when it is worth using. |
| `implementation-notes.md` | Why the code looks the way it does. Annotated excerpts, for people who write PPL. |
| `historical-cross-checks.md` | Worked examples from HP's own 1970s statistics programs, used as a second check on NormExplorer and BayesTree, plus reference cases for testing your own programs. |
| `ppl-rules-for-any-assistant.md` | The Lessons Learned condensed to about 3,000 words of flat rules for an AI assistant with a small context window (a local model in LM Studio, say), with a 2 × 2 table analyzer that passes the gate as the example to imitate. |
| `burrlab-guide.md` | Why the Burr XII, and how BurrLab's maximum-likelihood fit works, written for students (BurrLab beta 1i). |
| `normexplorer-guide.md` | User's guide to NormExplorer (beta 42c), written for students. The program is now beta 42e: numbers it cannot draw are refused with a sentence, the Diagnostics page takes a tap, and density labels too wide for the margin are written as 6ᴇ-5. |
| `chitable-guide.md` | User's guide to ChiTable (beta 3f), the two-way-table chi-square program, including Newcombe's interval for the risk difference. |
| `studrange-guide.md` | User's guide to StudRange (beta 15a, with the MicroPython engine). The program is now beta 15d. Since 15a: the Quit summary counts the plot and the first tap after a page closes is no longer skipped (15b); an exact 0 prints "p < 0.00001" (15c); a note appears when the PPL fallback answers at α < 0.005, and Home's X is left alone (15d). |
| `scatterlab-guide.md` | User's guide to ScatterLab (beta 2a). The program is now beta 2f. Since 2a: the calculus page no longer stops the program and small values print as decimals (2b); 140000000000 prints whole (2c); the calculus page writes ² and √ (2d); the forms take numbers only, points the plot cannot hold are refused with a sentence, and an axis whose numbers are too long is labelled in units (×1ᴇ5) or from its lowest tick, never cut, and the side panel's numbers fit it; ŷ and ȳ are letters, not words (2f; the guide has a paragraph on it). |
| `binorm3d-guide.md` | User's guide to BiNorm3D (beta 1). The program is now beta 1b: one help sentence and one menu line are corrected (1a); the conditional page writes χ² and √ (1b). |
| `cicatcher-guide.md` | User's guide to CICatcher (beta 2a). The program is now beta 2e. Since 2a: the setup menu says "Exact (C-P)" for Clopper-Pearson (2b); two menu lines are shortened to fit (2c); the formula help writes ± and √ (2d); a μ, σ or n the window cannot hold is refused with a sentence (2e). |
| `errorrate-guide.md` | User's guide to ErrorRate Lab (beta 1a). The program is now beta 1d. Since 1a: small rates print as decimals and the decimal fallback works if the CAS fails (1b); "1 profile searched" and no "= <" (1c); the CAS page keeps its last line and the opening page shows the disclaimer (1d); the help writes α (1e). |
| `changes/` | One file per program version: what changed and why, with line numbers; the lint and verification output; and the device-test checklist, ordered from least to most risky. |
| `dev/` | The fleet review of 16 October 2026 and the CAS-and-MicroPython plan that drove the touch, graphics and CAS versions, kept as a record of how the work was planned; and the reports of the two emulator rounds of 17 October 2026 (`emulator-round1-2026-10-17.md`, `emulator-round2-2026-10-17.md`; round 2 includes the retest of its fix versions); the independent second reviews, `review2-<Program>-<version>.md`, each by a reviewer that had not seen the program; the monkey test's record over the fleet, round by round (`monkey-fleet-2026-11-01.md`); and every program's labels under random use (`label-check-2026-11-02.md`). |

The guides say "not yet run on hardware" in their firmware line until a calculator has run that version, and they name any run on the HP Prime Virtual Calculator. Only the ChiTable and NormExplorer guides were updated for the fix versions of 17–19 October 2026; where a program is newer than its guide, the table says what changed. Each version's file in `changes/` has the details.

**DISCLAIMER: these programs are teaching and demonstration aids. They are not validated for forensic, clinical or legal use; do not rely on their results for legal purposes.**

All of it is free for educational and personal use; see the LICENSE in the repository root.
