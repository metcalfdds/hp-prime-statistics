# HP 50g versions

A few of the fleet's calculating programs in User RPL for the HP 50g, as plain-text listings the calculator compiles itself. The touch-and-graphics programs stay on the Prime; these are the ones whose value is the arithmetic.

**Status: not yet run on a 50g or on the HP 50g Virtual Calculator.** There is no RPL gate or harness in this repository. Each listing's arithmetic is checked against `python/hpstats.py`; the RPL itself is checked by reading until the author runs it. Expected results are listed so the first run is a test.

| Program | What it does | Prime original |
| --- | --- | --- |
| `TBL2X2_50g.txt` | Chi-square (Pearson and Yates) with p from `UTPC`, the odds ratio with Woolf's 95% interval, Haldane's 0.5 at a zero cell; input form, tagged results on the stack | the example in `docs/ppl-rules-for-any-assistant.md`; ChiTable's 2 × 2 page |

## Loading a listing

**Virtual Calculator (Emu48-based, Windows):** File, Load Object, choose the `.txt`. The `%%HP: T(3)A(R)F(.);` header on line 1 tells it to translate `\<<`, `\>>` and `\->` into the calculator's characters; the object lands on the stack. Store it under a name: type `'TBL2X2'` then `STO`.

**Real 50g by SD card:** copy the `.txt` to a FAT-formatted card (2 GB or smaller is the safe size), put the card in the 50g, open the Filer (left-shift FILES), go to port 3 (the card), highlight the file and press RECV or copy it into HOME. If it arrives as a string, press `OBJ→` to compile it, then store it under a name. Lines starting with `@` are comments and are dropped on compile.

**Running:** type the name or press its soft key in VAR. Fill the form (defaults are the test table below), press OK. Results arrive as tagged objects; `FIX 4` makes them readable.

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
