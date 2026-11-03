# SymProbe beta 1: notes

*2 November 2026. A test program, not a teaching program: which decorated letters the Prime's own font holds. The source is `diagnostics/SymProbe_beta1a.txt` (pure ASCII; every glyph is built with `CHAR()`): beta 1, which gave the results below, with the fleet's pragma line added as its first line, and nothing else changed. Copied in as a file, it must be Checked once (Program Catalog, Edit, Check) before it runs; then run `SymProbe` from Home. Any key or tap ends it.*

## Why

Roger, 2 Nov 2026: "if there's any special character like y-bar or y-hat and so forth that is not in the Prime's "Chars", then make the custom character like you did for x-bar and x-hat." Before drawing a character by hand, the probe asks the font.

## What it draws

1. Unicode's own decorated y: `CHAR(375)` ŷ (U+0177), `CHAR(563)` ȳ (U+0233) and `CHAR(562)` Ȳ (U+0232), beside x̄ and p̂, in fonts 2 and 1.
2. HP's private-use glyphs `CHAR(57344)` to `CHAR(57375)` (U+E000 to U+E01F), 16 to a row, in fonts 2 and 1.
3. Overlays: a letter, then a macron (`CHAR(175)`, `CHAR(713)`) or a circumflex (`CHAR(710)`, `^`) drawn at the same spot, for y and d, in fonts 2 and 1.
4. The width `TEXTOUT_P` returns for y, d, the macron, the circumflex and x̄.

## What it showed (Virtual Calculator 2.4.2, Rogers-HP, 2 Nov 2026)

- **ŷ (375) and ȳ (563) are in the font**, in fonts 1 and 2, each one character wide. ScatterLab beta 2f uses them in place of the words "y-hat" and "y-bar".
- **Ȳ (562), capital Y with macron, is not**: an empty box.
- **The private-use area holds x̄ (E000), p̂ (E001), an italic i (E003), a superscript −1 (E004), a bold italic x (E005) and y (E006).** E002 and E007 to E01F are empty boxes. There is no d̄, ȳ or ŷ there.
- **A drawn macron over y reads as ȳ**, and a circumflex over y as ŷ; neither is needed now. **Over d, a macron at the same spot touches the top of the d's stem**, so a hand-made d̄ needs its bar drawn higher than the letter's own cell puts it.
- Widths returned by `TEXTOUT_P` (px): font 2, y 6, d 7, macron 5, circumflex 7, x̄ 6; font 1, y 5, macron 4.

Still to see on a G1 and a G2 (the 2026-09-09 firmware): the first two rows, whose ŷ and ȳ should be letters, not boxes.
