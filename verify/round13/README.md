# Round 13: ChiTable's exact test for the 2 × 3 and 3 × 2 tables (13 November 2026, evening)

When an expected count is below 5, the chi-square p is shaky. ChiTable has given Fisher's exact test for a 2 × 2 table since beta 3; for its other two shapes, results page 5 said only "Fisher (2x2) or merge cells." Roger, 13 November 2026: "Could we do an exact test for a bigger table?" ChiTable beta 3m adds it for the 2 × 3 and 3 × 2 tables: Fisher's rule with more columns (Freeman and Halton 1951), the p that R's `fisher.test` gives, counted on the calculator for up to 10,000 tables. Larger tables are not for this project (Roger: "layer on and not for this project, doing larger tables in python or Maple"). Looking at the new line on the Virtual Calculator found one more thing, fixed in the same version: page 5 called a count equal to its expected count "MORE than expected". What changed, line by line, and the device checklist are in `docs/changes/ChiTable_beta3m_CHANGES.md`.

## What is here

| File | What it is |
| --- | --- |
| `make_chitable_3m.py` | The build. Each change is an exact replacement in ChiTable beta 3l, read from git (`BASE`, the commit before this round); a replacement that does not match exactly once stops it. |
| `../verify_ChiTable_beta3m.py` | The round's verify script (T1, T2, X1 to X5); its saved output is beside it. Its references are a brute-force count in Python's exact integers and R's `fisher.test` (R 4.3.3, `Rscript`). SciPy 1.18.1's `fisher_exact` takes an R × C table but answers it by simulation, a different number on each call, so it is not one of them. |
| `checks_r13.py`, `checks_r13.txt` | The harness smoke test (main routine, idle key Esc) of beta 3m beside beta 3l; `tools/text_overlap_v1.py --walk` on both; `tools/label_fit_v1.py` on both walks and on the verify script's own run; `tools/fleet_names_v2.py` over the fleet with beta 3m. |
| `comma_check_r13.txt` | `tools/comma_check_v1.py` on beta 3l and beta 3m, 100 seeds: every run takes beta 3l's path, every number of four or more digits has its commas, the CAS texts are beta 3l's, no year has a comma. Its D line is label_fit's help line (below). |
| `helppages_before_r13.json`, `helppages_r13.json` | Every help screen of beta 3l and beta 3m, as the PC harness draws them (`verify/round11/helpdump_r11.py`): screen 1 is the only one that changed. |
| `helpcheck_r13.json` | Every help screen of beta 3m laid out at the glyph widths GlyphProbe_v1 measured (`verify/round11/helpcheck_r11.py`): 6 screens, no reports. |
| `gates/` | `tools/ppl_gate_v1e.py` on beta 3m against beta 3l. |
| `mk/` | The monkey's 1,000 runs on the final file (`tools/monkey_chunks_v1.py`, base 13, `--lists`): all OK. |
| `vc_checks.txt` | The Checks and the runs on the Virtual Calculator. |
| `screens/` | Pages as the Virtual Calculator showed them (320 × 240, enlarged three times): help page 1; page 5 for a 2 × 3 table and for the same table turned on its side; page 5 for the table with no association, before and after the fix; pages 5 and 6 for a small 2 × 2 table; and the final Check. |

## label_fit's one new line

`tools/label_fit_v1.py` measures text at a flat 5.5 px a character, made for numbers, and reports any line whose cut-off part would hold a digit. Help page 1's new line "any E below 5).  If not, use the exact test (page 6 for a 2x2," comes to 338.5 px that way, against its width of 296. At the glyph widths measured on the Virtual Calculator it is 266 px (beta 3l's line was 289 px), and the Virtual Calculator draws it whole (`screens/ChiTable_help1_r13.png`). The tool's other line, help's "Curve: drag the red dotted line ...", is beta 3l's.
