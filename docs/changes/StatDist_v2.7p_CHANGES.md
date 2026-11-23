# StatDist v2.7p: changes (23 November 2026)

Round 19. Round 18's monkey found StatDist v2.7o's Formula page (CAS) waiting for Student's t at df = 206.3: the PC harness stopped the CAS call for E[X²] at its limit of 60 s, and Giac 1.9.0 on the PC had not finished the same integral after ten minutes at df = 17.83 (`verify/round18/probes/probe_statdist_cas.py`). Roger, 23 Nov 2026, 06:37: "StatDist--fix as you suggest". The suggestion was to ask the CAS for E[X²] only when df is a whole number or a half.

Round 19 then asked the same questions of every continuous family with parameters typed to two decimals (`verify/round19/probe_fm_families.py`, `probe_fm_params.py`) and found two more families waiting in Giac on the PC: Fisher F at df1 = 7 and df2 = 17.83, and Burr XII at C = 2.37. On the Virtual Calculator (`verify/round19/vc_record.txt`), v2.7o was:

- still "Asking the CAS" fourteen minutes after the Formula page was asked for F at 7 and 17.83, and two presses of On did not stop it;
- stopped altogether, its screen black and its program ended, about 14 s after the page was asked for Burr XII at C = 2.37, K = 3 and S = 1, twice;
- quick for Student's t: "no closed form shown" in 2 s at df 17.83 and in 5 s at 206.3.

So the same fix went to all three families, with each rule taken from what the calculator did.

## What changed

1. **`st_FmCont`, the continuous families' Formula page** (lines 4,497 to 4,564):
   - line 4,497: a new local, `fcQ`;
   - lines 4,502 to 4,526: the comment, then `fcQ := 1`, and three tests that set it to 0 and add one gray line to the page:
     - Student t, when 2 df is not a whole number: "The CAS is asked here only when df is a whole number or a half."
     - Fisher F, when df1 or df2 is not a whole number: "The CAS is asked here only when df1 and df2 are whole numbers, because other values can keep it working for many minutes."
     - Burr XII, when C or K is not a whole number: "The CAS is asked here only when C and K are whole numbers, because other values can keep it working for minutes, or stop the calculator."
   - lines 4,531, 4,541, 4,559 and 4,564: the page's four CAS calls (E[X]; whether E[X] is infinite; E[X²]; whether E[X²] is infinite) are made only when `fcQ` is 1. Otherwise each answer is empty, and the page goes on as it always did when the CAS gave an integral back undone: "no closed form shown" and the program's own value, or "no closed form shown (the program: undef)" where the moment does not exist.
2. **The header and a history note** (lines 4 and 45 to 51). The program shows no version on its pages.

Nothing else changed: no other family, no number, no help page, no menu. With t at a whole or half df, F at whole dfs and Burr XII at whole C and K the page is the old version's line for line (S2 below). The Burr XII rule started as "whole numbers or halves", because Giac on the PC had answered halves at once; on the Virtual Calculator v2.7p's first build was still "Asking the CAS" after 3 minutes at C = 2.5 and K = 3.5, so the rule became whole numbers (the scale S may be any value: 2, 3 and 1.83 took 2 s).

## For the book

- The version in the table of "How to use this book" becomes v2.7p, and Appendix F's count of lines becomes 5,146 (it was 5,112).
- The help pages are word for word the same. A book page that shows the Formula page for t, F or Burr XII with a df or a shape that is not a whole number would now show the gray line.

## Checks

- `verify/verify_round19_v1.py` (its output is beside it): B, the build (`verify/round19/make_round19.py`) makes the filed program byte for byte; T1, every changed line is the build's; G, the gate against v2.7o (`verify/round19/gates/StatDist_v2.7p.txt`); S1, t at df 17.83, 206.3, 30.1 and 0.83, F at 7 and 17.83 and at 7.5 and 17.5, and Burr XII at 2.37, 3, 1 and at 2.5, 3.5, 1.5: no integral goes to the CAS, the gray line is on the page, and "no closed form shown"; v2.7o at df 17.83 still runs past the harness's 60 s; S2, t at df 24, 17.5 and 1, F at 7 and 18, Burr XII at 2, 3, 1 and at 2, 3, 1.83: the CAS is asked as before, every call ends within 5 s, and the page is v2.7o's line for line; S3, Normal, Gamma and Beta with two decimals: v2.7o's page line for line; R, round 18's seed 18000984 replayed: OK; M, `StatDist()` with no warnings; N, `tools/fleet_names_v2.py` and `tools/screen_text_v1.py` over the 31 programs.
- The monkey (`verify/round19/monkey_r19.py`, base 19, `--lists`, 240 s a run): see `verify/round19/monkey_r19.txt`.
- The Virtual Calculator 2.4.2, 23 Nov 2026 (`verify/round19/vc_record.txt`, `verify/round19/screens/`): the Check said "No errors in the program"; v2.7p's Formula page came in 3 s or less for F at 7 and 17.83 and for Burr XII at 2.5, 3.5, 1.5, with the gray line, where v2.7o had waited fourteen minutes and more than three; asked as before, t at 2.5 and 17.5, F at 7 and 18 and Burr XII at whole C and K took 3 s at most.

## On a G1 or a G2

Not yet run on a G1 or a G2. The check, which takes two minutes:

1. StatDist, Advanced Continuous, Fisher F, lower tail; df1 = 7, df2 = 17.83; OK.
2. Enter, 2 (Formula page). The page comes at once and has the gray line "The CAS is asked here only when df1 and df2 are whole numbers, ...".
3. Esc, Enter, 5 (Edit parameters): df2 = 18. Enter, 2: the page asks the CAS, and E[X] reads 9/8. Note how long it takes.

## Unresolved

- How long a G1's or a G2's CAS takes at the guarded values was not tried, and neither was F at halves on the calculator (Giac on the PC took 24 s at 7.5 and 17.5; the rule keeps F to whole numbers).
- The rules come from the values tried. A whole df or a whole C and K that the CAS takes long over has not been seen, but not every one was tried.
- On, pressed while the Virtual Calculator's CAS worked, did not stop it. Whether a G1 or a G2 can be stopped then is not known.
