# Round 21: worked steps that check on a calculator (28 November 2026)

TTestLab beta 1n, TTestLabG beta 1k, a device fact for the harness (`tools/prime_facts_v1.py`, fact 8), starter pack v29, the Prime Loader v2s and Lessons Learned v7zza. Roger, 28 Nov 2026, 01:31, to the read-through of the book's Draft 127: "You're right about all these things—please go ahead and fix them and reorganize and rearrange as necessary". Its item A10 was this round's.

## What was wrong

Steps 2 and 4 of TTestLab and TTestLabG write a formula, put the numbers in and work it out line by line, so that a student can follow the arithmetic and check it on a calculator. Each number on them was the exact value rounded to 4 significant digits, and a line worked from rounded numbers can miss in its last digit or two. The book's Figure 11.2, TTestLabG's draft lottery, showed "df = 13,707 / 37.81 = 362.56", and 13,707/37.81 is 362.52; "a = s₁²/N₁ = 61.90", and 106.1²/182 is 61.85. TTestLab's age-at-arrest example, the book's Figure 11.4, showed "1.321 × 0.2345" and then "0.3097", and that product is 0.30977.

## What changed

- **TTestLab beta 1n** (`make_round21.py`, exact replacements from beta 1m, read from git; the new routines and steps are the `r21_*.txt` files; `../../docs/changes/TTestLab_beta1n_CHANGES.md` has the line numbers). Each number on steps 2 and 4 is worked out from the numbers shown before it, as a student with a calculator works it, rounded half away from zero to the digits it is shown with, and each result has fewer significant digits than what it is worked from. The program takes the fewest digits (4 to 8 for SE) at which that chain still gives its own SE, df and t or z, so the answers on the screen are still the exact ones. A number that is exact is shown whole; one too small or too large for 11 decimals is shown in the scientific form. Step 2 of Welch's test writes a and b from s; the t and z lines of step 4 take three lines, and the two-proportion test's pooled p and its root two each, so that the largest numbers the forms take still fit. Help page 2 says what steps 2 and 4 do.
- **TTestLabG beta 1k**, built from beta 1n by `tools/make_tlg1_v6.py` (`../../docs/changes/TTestLabG_beta1k_CHANGES.md`). The draft lottery now reads "df = 13,707 / 37.806 = 362.56", "√117.0772 = 10.820" and "45.4003/10.820 = 4.20", and every line checks.
- **A device fact** (`tools/prime_facts_v1.py`, fact 8). In the harness a one-sample step 4 with s = 162.45 and N = 100 showed SE = 16.24, where a student works 16.245 and rounds it to 16.25. `diagnostics/RoundProbe_beta1a.txt`, run on the Virtual Calculator, showed that the calculator holds 162.45/10 as 16.245 and that ROUND rounds a tie away from zero, to 16.25; the harness's binary floats hold it as 16.244999999999997. Fact 8 makes the harness's ROUND round the decimal the calculator holds. The same probe showed the calculator keeping more digits than the 12 it shows ((1 + 1E−15) − 1 gave 1E−15), which the harness does not model.
- **Starter pack v29** (`../../docs/changes/StarterPack_v29_NOTES.md`): v28 but for the two programs' checked files and READ_ME_FIRST.txt's lines for them.
- **The Prime Loader v2s** (`../../prime-loader/README.md`, "What v2s changes"): v2r's page, word for word, built from pack v29; its test and the cable core's test count the two programs' new characters and reports.
- **Lessons Learned v7zza** (`make_ll_v7zza.py`): the house rule that a worked step checks from the numbers it shows, ROUND's tie, and the digits the Virtual Calculator held.

## The files here

| File | What it is |
| --- | --- |
| `make_round21.py`, `r21_helpers.txt`, `r21_step2_new.txt`, `r21_step4_new.txt`, `r21_step4n_new.txt` | Builds `programs/TTestLab_beta1n.txt` from beta 1m (from git) by exact replacements, putting in the chain's routines and the new steps. |
| `make_verify_tlg_1k.py` | Makes `../verify_TTestLabG_beta1k.py` from `../verify_TTestLab_beta1n.py`: the names, the examples and the help line. |
| `make_v2s.py` | Makes the Prime Loader's v2s build, template and test from v2r's by exact replacements, with the cable's counted numbers for pack v29. |
| `make_ll_v7zza.py` | Makes Lessons Learned v7zza from v7zz by exact replacements. |
| `vc_r21.py`, `vc_record.txt`, `vc/` | The Virtual Calculator: the ROUND probe, the two Checks, then the runs, step by step, and the captures. |
| `gates/` | The gate's output against beta 1m and beta 1j. |
| `pages_a11y_r21_output.txt` | `tools/pages_a11y_v1.js` on the two pages (the Prime Loader's v2s): 32 PASS, 0 FAIL. |

## What passed

- `../verify_TTestLab_beta1n.py` and `../verify_TTestLabG_beta1k.py`: 26 PASS, 0 FAIL each, with the harness as it now stands (fact 8 in place). Part C read every relation on steps 2 and 4 off the screen for every example and 1,759 random cases of all six tests and found each line worked out from the ones above it; in 7 of the cases, each a t of 100,000 or more, even 8 digits do not give the exact t, and step 4's t is then within 1E−7 of it (C3). The gate: PASS against beta 1m and beta 1j (`gates/`: the kit's lint 0 errors, no hard error, the fleet's names clean). `tools/screen_text_v1.py`: nothing against the rules; `tools/fleet_names_v2.py`: no collision.
- The monkey: 1,000 of 1,000 OK for each program (`../monkey_TTestLab_beta1n_output.txt`, `../monkey_TTestLabG_beta1k_output.txt`). The first 1,000 runs of TTestLabG had ended 998 OK and 2 CRASH, both in fact 8's own first code and not in the program: a ROUND of a number past about 1E78 to 2 decimals asked Python's decimal module for more digits than it held (`--replay 1000270`). Fact 8 now gives such a number back as it stands, as the calculator does, and both programs' 1,000 runs were made again.
- `prime-loader/usb/tests/test_usb_core_v3d.js` 95 PASS, 0 FAIL; `prime-loader/tests/test_loader_v2s.js` 173 PASS, 0 FAIL; `tools/pages_a11y_v1.js` 32 PASS, 0 FAIL (`pages_a11y_r21_output.txt`).
- The Virtual Calculator 2.4.2 in the cloud workspace (`vc_record.txt`): the ROUND probe; the Check of both programs ("No errors in the program") before anything was run; then the draft lottery's steps 2 and 4 and the age-at-arrest example's step 4, line for line the harness's, captured at three times for the book's Draft 129 (Figures 11.2 and 11.4); help page 2 of both programs inside the screen; and the two-proportion test with 1 of 999,999 and 151 of 1,000,000 typed into its form, every line of step 4 inside the screen.

Not run: a G1 or a G2 (the change notes' device checklists).
