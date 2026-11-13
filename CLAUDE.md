# Working notes for an AI assistant in this repository

These notes, like the Lessons Learned, were written with and for Claude Code and read best there. They are meant to help any AI assistant that works on this repository, but they were not tested with another one, and the setup steps assume a Claude Code cloud session on Ubuntu.

## What this is

Thirty-one teaching programs for the HP Prime calculator in PPL (five carry MicroPython), each a plain `.txt` file in `programs/`, and the HP Prime Data Loader web page (`data-loader/`) that feeds one of them, DataLoad; with a four-tool gate, a PC harness, one verify script per program version, a change note and device checklist per version, and the Lessons Learned document on how the Prime actually behaves. Read `START_HERE.md`, then `docs/lessons-learned_v7zr.md` (or the newest letter) before writing any PPL. The author is Roger Metcalf; the HP programs are his, and every change goes through a pull request he merges.

## How to work here cheaply

The author's cloud credit is spent on tokens, not on processor time. So:

- **Before any task, choose the way that does the job properly at the least cost**, and say the expected cost before starting anything likely to exceed a few dollars. Compute is cheap and tokens are dear: a script that runs for an hour and prints ten lines beats ten minutes of reading. If two methods give the same result, take the cheaper one; if the cheaper one gives a weaker result, say what it loses and let the author choose.
- **Prefer a script that runs long and prints little.** Run checks and sweeps in the background, filter their output to the lines that decide something, and read a summary, never a whole log.
- **Do not read whole programs into the conversation.** A program is 1,000 to 6,000 lines. Grep for the routine you need and read that routine. Check a formula by calling its routine through the harness (`h.execute('es_WilsonCI(5,20)')`, or `h.globals_.update({...})` then `h.execute('csCompute()')`), not by reading or driving its pages.
- **Do not spawn parallel agents** for reading; they multiply the cost. One session, one thread.
- **Never stop a background task in a way that echoes its script back** (the TaskStop echo was the most expensive moment of a whole day). Prefer `pkill -x python3` over `pkill -f <pattern>`, which also kills the shell that contains the pattern.
- **Say the usage** in tokens at each milestone when asked; the author watches a dollar meter.

## Setting up a fresh session (about five minutes)

```
pip install scipy statsmodels sympy
apt-get update && apt-get install -y xcas          # gives icas, the Giac the harness uses for CAS calls
git clone --depth 1 https://github.com/JordiRigau/hp-prime-kit /tmp/kit/hp-prime-kit-HEAD
export HPKIT=/tmp/kit/hp-prime-kit-HEAD              # the harness finds the kit here
```

The gate (`tools/ppl_gate_v1e.py`) finds the kit only as a zip, `Community_Library/github/JordiRigau__hp-prime-kit.zip`, beside `tools/` or one folder up. Do not put it inside this repository: copy `tools/` to a scratch folder, zip the kit beside that copy, and run the gate from there, pointing it at `programs/`.

## The checks

- **Gate, before any paste**: `python3 ppl_gate_v1e.py NEW.txt [ORIGINAL.txt]`; every program in `programs/` passes. "PARSE FAIL" on the √ character, `#RRGGBB:24h` colours or forward declarations is the kit's limit, not an error; the kit linter's "0 errors" is the line that matters.
- **Text overlap** (since 28 Oct 2026): `python3 tools/text_overlap_v1.py --run verify/verify_<Name>.py` or `--walk programs/<Name>.txt`; no firm overlaps, straddles or overruns on any page.
- **Fleet names**: `python3 tools/fleet_names_v2.py programs/*.txt` (all programs share one pool of routine names on the calculator).
- **Verify scripts**: the newest ones run from `verify/` as they are and read older versions from git: round 6's, one for each of the 11 programs it changed (`verify_<Name>_<version>.py`, 2 Nov 2026, night; BurrLab's beta 1k, never committed, sits beside them as `verify/BurrLab_beta1k.txt`), round 5's, one for each program, and before them `verify_StudRange_beta15f.py` and `verify_TrendTest_beta3g.py`. A round-5 script checks what round 5 changed, the commas, against the version before (`tools/comma_check_v1.py`); the program's earlier script still holds its arithmetic and dialog checks. The 19 October scripts hard-code the author's folders (`/home/claude/work/...`) and need files that are not in the repository; `verify/README.md` and `docs/dev/independent-review-2026-10-22.md` say what they need and what happened when they were rerun.
- **Monkey test** (since 1 Nov 2026; the book's vetting point 6): `python3 tools/monkey_v1b.py programs/<Name>.txt "CALL()" --runs 1000 --lists [--writes D,C]` (v1b applies `tools/prime_facts_v1.py`, the device facts the harness does not model yet). A long job goes in chunks written as they end (`tools/monkey_chunks_v1.py`; a program paced by the clock, such as GaltonBoard, gets 120 s a run). Since 2 Nov 2026 every verify script's D part runs `tools/label_fit_v1.py` beside `text_overlap_v1` (a number cut short by its width argument), and `tools/monkey_labels_v1.py` checks every program's labels under random use (`docs/dev/label-check-2026-11-02.md`). Every run must end OK (STATE only for what `--writes` names); a broken run's seed replays it (`--replay SEED`). Number fields are `{name,[0]}`, which refuses a typed list on the calculator.
- **Python**: `cd python && python3 test_hpstats.py` checks `hpstats.py`, the fleet's arithmetic, against SciPy, statsmodels and brute force.
- **Harness smoke test**: load each program in `tools/ppl_run_v3e.py` with `idle_key=4` and call its main routine; zero warnings and no `PPLError` is the pass.

## Conventions

- A changed program gets the next letter (`beta 15d` → `beta 15e`), replaces the old file in `programs/` (git keeps the old one), updates its header and its "What changed" block, and gets `docs/changes/<name>_CHANGES.md` (why, what changed with line numbers, verification, gate, device checklist, unresolved), a `verify/verify_<name>.py` with its output beside it, a line in `verify/README.md`, and a bullet in the README's test-status note plus its row in the program list.
- **After any change in `programs/`, rebuild the starter pack** with the next number, in two passes (`docs/changes/StarterPack_v5_NOTES.md`): build without `--checked` (`python3 tools/make_starter_pack_v4.py v7 --kit $HPKIT`); load it on the Virtual Calculator (close it, copy the files in, start it), Check each changed program and run nothing, close it, and copy those files back into the checked-files folder (a checked file keeps the file-level values of its last run, so a run would ship that run's numbers: `docs/changes/StarterPack_v6_NOTES.md`); then build again with `--checked FOLDER`, which stops unless every program has a checked file holding its exact source. Move the older zip out of `starter-pack/`, and rebuild the Prime Loader from the new pack (the newest `prime-loader/build_loader_v1*.py`, then its test).
- **GitHub Pages** (1 Nov 2026): the repository is published at https://metcalfdds.github.io/hp-prime-statistics/ (Settings → Pages, `main`, root). `.nojekyll` keeps Jekyll off, because PPL list syntax such as `{{x,y}}` in the Markdown breaks its Liquid templates. The front page, `index.html`, links to `prime-loader/` and to the Data Loader by its file name: when `data-loader/DataLoader_vN.html` gets a new number, change that link. `prime-loader/index.html` is written by the loader's build and sends the browser on to the current page, so the address the book prints never changes. A pack that lags `programs/` gives students old versions.
- **The data loader** (`data-loader/`): edit `page_template_v3.html` or `dl_core_v1.js` under a new version number, rebuild the page with its `build_page_vN.py`, and run `node tests/test_core_v1.js` (the encoder against hp-prime-kit's, the Rossi file byte for byte) and `node tests/page_check_v3.js` (the page in Chromium; Playwright). A change to what the page writes must be loaded with DataLoad on the Virtual Calculator before it is called tested.
- Lessons Learned is versioned by letter too (`v7y` → `v7z`), with a "What changed" block at the top; the links in `README.md`, `docs/README.md` and `START_HERE.md` are updated with it.
- Executable code stays ASCII (`ppl_check_v5.py`'s E5); π is `3.14159265359`. Strings may carry any glyph GfxProbe has shown renders. Every routine and local name carries the program's prefix (`st_`, `cs`, `tr`, `dm` …) so the fleet shares one name pool safely.
- **Commas in big numbers** (2 Nov 2026; Roger: "always put comma delimiters in big numbers"). Every number of 1,000 or more that reaches the screen goes through the program's comma routine (`<prefix>Cm`, word for word `tools/comma_helper_reference_v1.txt`) where it becomes text, so it is measured with its commas before it is drawn. Never in text the CAS or `EXPR` reads, never in a year, never in a name with digits in it ("x1000"). A changed program keeps to this by hand or through `tools/commas_v1.py`'s rules, and its verify script runs `tools/comma_check_v1.py`. Prose follows the same rule: 1,000 and up get commas (APA).
- **Sensible ranges for what a student types** (2 Nov 2026, night; round 6, `docs/dev/caps-2026-11-02.md`). A typed value outside its range is refused with a sentence that says the range, and nothing changes; never clamp it without a word. Alpha is from 0.001 to 0.2 in every program (help line "From 0.001 to 0.2; 0.05 is usual"), and a drag stops at the same ends. A cap goes where the program stops being right or readable (a cell that shows 9,999,999 whole; StudRange's df at 100,000); values in the data's own units stay open. Find the fields with `tools/caps_probe_v1.py`. A menu item (`CHOOSE`) is at most 30 characters: the box sizes itself to about 214 px and cuts the rest.
- Compute upper tails as lower tails or as finite sums of positive terms; never `1 - CDF` where the p may be small.
- Take a standard deviation from the deviations x − x̄ in a second pass, never from Σx² − n x̄², which loses its digits when the mean is large next to s (the Prime keeps 12); a simulated sample adds up the z behind each value (Lessons Learned v7zi §11).
- A number a student can type is refused with a sentence before it is used when the program cannot draw it: 50 digits or more, a scale too small next to its location for 12 digits, and anything a family's formulas cannot hold (Lessons Learned v7zi; SampDist, CICatcher, Norm3, NormExplorer, StatDist).
- Nothing is reported as device-tested unless it ran on the Virtual Calculator, a G1 or a G2; the harness is a PC model. It counts in 16 digits (the Prime keeps 12), prints any number of decimals (`STRING(x, 2, d)` refuses d ≥ 13 on the Prime) and reads `!=` as "not equal" (on the Prime it is a factorial and a test: write `<>`). A device fact the harness lacks goes into `tools/prime_facts_v1.py` the same day; the verify scripts and the monkey test apply it.
- **General and advanced versions** (31 Oct 2026). A program's general version (TTestLabG for TTestLab) is built from the advanced one by a script of exact replacements (`tools/make_tlg1_v2.py`): a new name and tag, the companion guide's conventions, general examples. Change the advanced program first, then rebuild the general one with the script's next version, and derive its verify script from the advanced one's the same way, reading every failure before changing an expectation.
- **A verify script must drive every cancel and refusal path** (Esc at each menu, Cancel on each form, each refused read), not only the arithmetic: TTestLab's 59 arithmetic checks passed while ten dialog faults waited for the independent review (31 Oct 2026). A new program gets that review before it is called finished.

## GitHub

- Work on a branch; push with `git push -u origin <branch>`; open the pull request with `gh api repos/metcalfdds/hp-prime-statistics/pulls --input body.json` (GraphQL, and so `gh pr create`, is blocked). The author merges with two clicks; the session's policy does not allow merging.
- The clone is shallow and tracks only `main`: after pushing a branch, add a fetch refspec and set upstream, or the stop hook complains about an unpushed commit that is in fact pushed.
- Never commit hp-prime-kit, `__pycache__`, or anything from the author's working folders.

## Files from the author's computer

His working folder is `D:\HP-Prime` on Rogers-HP. The cheap route for a batch of files is one zip in Dropbox, fetched with the Dropbox connector's download link and `curl` (the link is single-use; one GET, no HEAD). The environment's network policy must allow `*.dropboxusercontent.com`, which the author sets under the environment's Network access. Extract into a fresh folder in the scratchpad, never into the repository.
