# TTestLabG beta 1k: changes (28 November 2026)

Round 21 of 28 November 2026 (`verify/round21/README.md`): the general version of TTestLab beta 1n (`TTestLab_beta1n_CHANGES.md`), built from it by `tools/make_tlg1_v6.py` (v5's blocks with five changes for the new steps; v5 and its blocks left `tools/`, and git keeps them). The read-through of the book's Draft 127 found, as its item A10, that the steps which work the arithmetic out do not always check on a calculator from the numbers they show, and Roger, at 01:31, accepted that item with the rest: "You're right about all these things—please go ahead and fix them and reorganize and rearrange as necessary".

## What was wrong

Beta 1j showed each number on steps 2 and 4 as the exact value rounded to 4 significant digits. On the draft lottery, the book's Figure 11.2, three of its lines did not check:

```
a = s₁²/N₁ = 61.90,  b = s₂²/N₂ = 55.17
df = 13,707 / 37.81 = 362.56
   = √(106.1²/182 + 100.8²/184)
   = √(61.90 + 55.17) = √117.1
```

106.1²/182 is 61.85, not 61.90; (61.90 + 55.17)² is 13,705, not 13,707; and 13,707/37.81 is 362.52, not 362.56. Each number was right, as the exact value rounded, but the line worked from the rounded numbers before it was not.

## What changed

1. **The chain** (lines 435 to 693, new): TTestLab beta 1n's, renamed (`tz_DcK` at line 457 to `tz_Work` at line 685). Each number on steps 2 and 4 is worked out from the numbers shown before it, rounded to the digits it is shown with, and `tz_Work()` takes the smallest k, from 4 to 8 significant digits for SE, at which that chain still gives the program's own SE, df and t or z.
2. **Step 2 of the separate-variances test** (`tz_Step2`, lines 1263 to 1299) writes a and b from s on lines of their own and works df from them. The draft lottery now reads:

   ```
   a = s₁²/N₁ = 106.1437²/182 = 61.9038
   b = s₂²/N₂ = 100.7567²/184 = 55.1734
   df = 13,707 / 37.806 = 362.56
   ```

3. **Step 4** (`tz_Step4`, lines 1343 to 1405, and `tz_Step4N`, lines 1632 to 1683), as in TTestLab beta 1n. The draft lottery's:

   ```
      = √(106.1437²/182 + 100.7567²/184)
      = √(61.9038 + 55.1734) = √117.0772
      = 10.820
   t obt = (x̄₁ - x̄₂)/SE
         = (206.3242 - 160.9239)/10.820
         = 45.4003/10.820 = 4.20
   ```

   Beta 1j showed a mean or SD worked out from raw scores to 4 significant digits on step 4 (`tz_Val`, its blocks 27 to 29); the chain now shows them with the digits the next line needs (206.3242), in both versions alike, and step 1 still shows 206.3.
4. **Help page 2** (`tz_Help`, line 2332): "Steps 2 and 4 work each number from those shown, so all check.", where beta 1j said "Step 4 keeps 4 significant digits at each step."
5. The header: the version (line 4) and the history note (lines 20 to 33). No other routine, menu, number or word changed.

The program is 2,499 lines (beta 1j: 2,196) and 110,627 characters (97,939).

## For the book

- The table of the *Statisticles* in "How to use this book" names TTestLabG beta 1k.
- **Figure 11.2** (the draft lottery's steps 2 and 4) is taken again, and its caption's numbers change: "13,707/37.81 = 362.56" becomes "13,707/37.806 = 362.56", "√117.1 = 10.82" becomes "√117.0772 = 10.820", and "t = 45.40/10.82 = 4.20" becomes "t = 45.4003/10.820 = 4.20".
- No menu item moved.

## Checks

- `verify/verify_TTestLabG_beta1k.py` (made from TTestLab's script by `verify/round21/make_verify_tlg_1k.py`, which changes only the names, the examples and the help line) and its saved output: **26 checks, 0 failures**. The same parts as TTestLab's (A, C with the seven examples and 1,759 random cases, C3, H, D, B with 300 seeds against beta 1j), and E2, the draft lottery's steps 2 and 4, line by line as Figure 11.2 is to print them.
- `tools/prime_facts_v1.py`'s fact 8 (ROUND rounds the decimal the calculator holds, a tie away from zero) applies here too.
- `tools/ppl_gate_v1e.py` against beta 1j (`verify/round21/gates/gate_TTestLabG_beta1k.txt`): **PASS**.
- `tools/screen_text_v1.py` and `tools/fleet_names_v2.py` over the newest files: nothing against the rules, no collision.
- The monkey (`tools/monkey_v1b.py`, 1,000 runs with random lists; `verify/monkey_TTestLabG_beta1k_output.txt`): **1,000 of 1,000 OK** (406 s).
- HP Prime Virtual Calculator 2.4.2 in the cloud workspace, 28 Nov 2026 (`verify/round21/vc_record.txt`): Program Catalog > Edit > Check at 03:33 said "No errors in the program", and the checked file went into starter pack v29 before anything was run. Then, at 03:52, the draft lottery's steps 2 and 4 read line for line as above and as the harness draws them (`verify/round21/vc/12_tlg_lottery_step2_x3.png` and `13_tlg_lottery_step4_x3.png`, the book's new Figure 11.2), help page 2's new line stood inside the screen, and Quit returned "TTestLabG: t(362.56) = 4.20, p < 0.001, two-tailed".

## On a G1 or a G2

Not yet run on a G1 or a G2. The check, which takes five minutes:

1. Start TTestLabG, choose **Example: draft lottery**, and tap **2 df**: a = 106.1437²/182 = 61.9038, b = 100.7567²/184 = 55.1734, and df = 13,707 / 37.806 = 362.56.
2. In Home, work 106.1437²/182 (61.90376…), (61.9038 + 55.1734)² (13,707.07…) and 13707/37.806 (362.56…): rounded as the screen shows them, they are the screen's numbers.
3. Tap **4 t**: √117.0772 = 10.820, and 45.4003/10.820 = 4.20.
4. Menu, **Help**, page 2: the line on steps 2 and 4 ends inside the screen.

## Unresolved

The same as TTestLab beta 1n's: a t or z of 100,000 or more can differ on step 4 from step 5's in its last decimals (7 of the 1,759 random cases, C3); the harness's arithmetic other than ROUND is still binary; not yet on a G1 or a G2.
