# HP 50g versions

A few of the fleet's calculating programs in User RPL for the HP 50g, as plain-text listings the calculator compiles itself. The touch-and-graphics programs stay on the Prime; these are the ones whose value is the arithmetic.

**Status: not yet run on a 50g or on the HP 50g Virtual Calculator.** There is no RPL gate or harness in this repository. Each listing's arithmetic is checked against `python/hpstats.py`; the RPL itself is checked by reading until the author runs it. Expected results are listed so the first run is a test.

| Program | What it does | Prime original |
| --- | --- | --- |
| `TBL2X2_50g.txt` | Chi-square (Pearson and Yates) with p from `UTPC`, the odds ratio with Woolf's 95% interval, Haldane's 0.5 at a zero cell; input form, tagged results on the stack | the example in `docs/ppl-rules-for-any-assistant.md`; ChiTable's 2 × 2 page |

## Loading a listing

The steps below for the card are from the HP 50g User's Guide, chapter 26 ("Using SD cards", pages 26-7 to 26-11); the ones for the Virtual Calculator from its File menu.

**Virtual Calculator (Emu48-based, Windows):** File, Load Object, choose the `.txt`. The `%%HP: T(3)A(R)F(.);` header on line 1 tells it to translate `\<<`, `\>>` and `\->` into the calculator's characters; the program lands on the stack. Store it: type `'TBL2X2'`, press STO. Test it from VAR.

**Real 50g, the sure route (a compiled object, no text translation involved):**

1. On the Virtual Calculator, with the program tested, recall it to the stack (VAR, right-shift, its soft key), then File, Save Object, name `TBL2X2`. That writes the 50g's own binary object format, which the real calculator recognises.
2. The card: FAT16 or FAT32 (the guide names only those two; 2 GB or smaller is the safe size). The calculator can also format a card itself (ON held, D pressed, then 0 for FORMAT; the result is FAT32). Copy the saved file to the card's top level. Names longer than 8.3 are accepted but shown truncated in the Filer.
3. Insert the card in the slot on the bottom edge, below the number keys, **label side down** (facing away from you with the keyboard up). It slides most of the way freely, then needs a firm push; fully in, only the top edge shows. To remove it later, turn the calculator off first, then press the edge in and it springs out.
4. The card is **port 3**. Press left-shift FILES to open the Filer; its tree shows port 3 only when a card is in. Open it, highlight TBL2X2 and press the RCL soft key: the program comes to the stack. Or, from the stack line, type `:3:TBL2X2` and press RCL (right-shift STO). Then `'TBL2X2'` STO to keep it in HOME.
5. Run it from VAR. `:3:TBL2X2` followed by EVAL runs it straight from the card without storing it.

**Real 50g, the text route, untried:** copy the `.txt` itself to the card. The Filer lists a PC text file as type String; RCL brings it to the stack as a string, and OBJ→ should compile it. Whether the compiler accepts the `\<<` and `\->` transliterations and the `%%HP` header line in that path is not stated in the guide and has not been tried; if it works, it saves step 1, and either way the answer belongs in the Lessons Learned.

**Running:** type the name or press its soft key in VAR. Fill the form (defaults are the test table below), press OK. Results arrive as tagged objects; `FIX 4` (left-shift MODE, Number Format) makes them readable.

## Expected results for TBL2X2

| a b c d | X2 | p | Yates | pYates | OR | ORlo | ORhi |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 10 20 30 15 (the defaults) | 8.0357 | 0.0046 | 6.7522 | 0.0094 | 0.2500 | 0.0938 | 0.6661 |
| 5 0 2 7 | 7.7778 | 0.0053 | 4.9778 | 0.0257 | 33.0000 | 1.3060 | 833.8727 |
| 3 1 1 3 (the tea table) | 2.0000 | 0.1573 | 0.5000 | 0.4795 | 9.0000 | 0.3666 | 220.9270 |

The second table also leaves the note "0.5 added to every cell: a cell was 0". A row or column total of 0 gives a message box and no results.

## Differences from the Prime version

- The 50g has upper-tail functions built in (`UTPN`, `UTPC`, `UTPT`, `UTPF`), so the p is `1 X2 UTPC` and the Prime's "never 1 - CDF" rule does not arise.
- Results go on the stack as tagged objects rather than on a drawn screen; that is the 50g's idiom, and it keeps the program to forty lines.
- The square root is written `.5 ^` so the listing stays ASCII; the 50g's own √ would do.
