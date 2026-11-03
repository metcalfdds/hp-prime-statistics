# CommaProbe beta 1: notes

*2 November 2026. A test program, not a teaching program: the comma routine of round 5 run on the calculator, and how wide a comma, a point and a digit are. The source is `diagnostics/CommaProbe_beta1a.txt` (pure ASCII): beta 1, which gave the results below, with the fleet's pragma line added as its first line and nothing else changed. Copied in as a file, it must be Checked once (Program Catalog, Edit, Check) before it runs; then run `CommaProbe` from Home. Any key or tap ends it.*

## Why

Roger, 2 Nov 2026: "always put comma delimiters in big numbers". `STRING` never groups digits, whatever Home's setting (Virtual Calculator, the same day: with Home showing 1,234,567, `STRING(1234567)` and `STRING(1234567, 2, 0)` gave "1234567"). So each program inserts its own commas, with a routine of a dozen lines built from `DIM`, `MID`, `LEFT`, `INSTRING` and `MOD`. Before 30 programs used it, the probe ran it on the calculator.

## What it does

1. Runs the routine (here `cpCm`) on twelve texts and compares each answer with the one expected: "1234567", "-98765.4321", "1.8053E10", "0.000123", "999", "1000", "12345.678901", "3186173/191520", "n = 1000, p = 0.5", "100000", "1234.5678" and "SSE = 18053333333".
2. Measures, with the x that `TEXTOUT_P` returns, the width of ",", ".", "0", "1", "1,234,567" and "1234567" in fonts 1, 2 and 3.
3. Draws 1,234,567.89 beside 1234567.89 in each font.

## What it showed (Virtual Calculator 2.4.2, Rogers-HP, 2 Nov 2026)

- **The routine gave all 12 answers as expected**, the same as the PC harness: 1,234,567; -98,765.4321; 1.8053E10 and 0.000123 untouched; 999 untouched and 1,000 grouped; 12,345.678901 (no comma after the point); 3,186,173/191,520; "n = 1,000, p = 0.5"; 100,000; 1,234.5678; "SSE = 18,053,333,333".
- **Widths in pixels**:

  | Font | comma | point | a digit | 1,234,567 | 1234567 |
  |---|---|---|---|---|---|
  | 1 | 3 | 3 | 6 | 48 | 42 |
  | 2 | 3 | 3 | 7 | 55 | 49 |
  | 3 | 4 | 4 | 8 | 64 | 56 |

  A comma is as narrow as a point, so a number's commas cost 3 px each in the small and medium fonts. A digit is 6 px in font 1, a little more than the 5.5 px the fleet's width estimates use.
- The grouped numbers read cleanly in all three fonts.

Still to see on a G1 and a G2 (the 2026-09-09 firmware).
