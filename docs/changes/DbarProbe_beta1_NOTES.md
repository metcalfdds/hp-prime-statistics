# DbarProbe beta 1: notes

*2 November 2026. A test program, not a teaching program: where to draw the bar of a hand-made d̄. The source is `diagnostics/DbarProbe_beta1.txt` (pure ASCII). Copied in as a file, it must be Checked once (Program Catalog, Edit, Check) before it runs; then run `DbarProbe` from Home. Any key or tap ends it.*

## Why

Roger, 2 Nov 2026: a symbol the Prime's Chars menu lacks gets a custom character. SymProbe beta 1 showed that the font has ŷ and ȳ but no d with a bar, and AgreeLab ("bias = mean d") and ResampLab ("observed mean d") name the mean difference d̄. So those two programs draw a d and then a line above it. A macron drawn at the same spot as the d runs into the top of its stem (SymProbe), so the bar has to sit higher than the letter's own text cell puts it.

## What it draws

In fonts 1 and 2, four d's, each with a bar from its left edge to 2 px short of where `TEXTOUT_P` says it ends: 3, 2, 1 and 0 px above the top of the text cell (y − 3 … y). Beside them, x̄ (the font's own glyph), x, d and b, for the height of a stem and of a real bar.

## What it showed (Virtual Calculator 2.4.2, Rogers-HP, 2 Nov 2026)

- **At y − 3 the bar clears the d's stem in both fonts** and reads as d̄.
- At y − 2 it just touches the stem in font 1 (a gap of a pixel or less in font 2).
- At y − 1 and y it runs into the stem: the letter looks like a d with a flag, not a d̄.

So AgreeLab beta 1c (`ag_TxDb`) and ResampLab beta 1d (`rs_TxDb`) draw the bar 3 px above the top of the d's cell, in font 1.

Still to see on a G1 and a G2.
