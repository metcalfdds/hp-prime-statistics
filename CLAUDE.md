# Working notes for an AI assistant in this repository

These notes, like the Lessons Learned, were written with and for Claude Code and read best there. They are meant to help any AI assistant that works on this repository, but they were not tested with another one, and the setup steps assume a Claude Code cloud session on Ubuntu.

## What this is

Thirty teaching programs for the HP Prime calculator in PPL (five carry MicroPython), each a plain `.txt` file in `programs/`, and the HP Prime Data Loader web page (`data-loader/`) that feeds one of them, DataLoad; with a four-tool gate, a PC harness, one verify script per program version, a change note and device checklist per version, and the Lessons Learned document on how the Prime actually behaves. Read `START_HERE.md`, then `docs/lessons-learned_v7zf.md` (or the newest letter) before writing any PPL. The author is Roger Metcalf; the HP programs are his, and every change goes through a pull request he merges.

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

The gate (`tools/ppl_gate_v1c.py`) finds the kit only as a zip, `Community_Library/github/JordiRigau__hp-prime-kit.zip`, beside `tools/` or one folder up. Do not put it inside this repository: copy `tools/` to a scratch folder, zip the kit beside that copy, and run the gate from there, pointing it at `programs/`.

## The checks

- **Gate, before any paste**: `python3 ppl_gate_v1c.py NEW.txt [ORIGINAL.txt]`; every program in `programs/` passes. "PARSE FAIL" on the √ character, `#RRGGBB:24h` colours or forward declarations is the kit's limit, not an error; the kit linter's "0 errors" is the line that matters.
- **Text overlap** (since 28 Oct 2026): `python3 tools/text_overlap_v1.py --run verify/verify_<Name>.py` or `--walk programs/<Name>.txt`; no firm overlaps, straddles or overruns on any page.
- **Fleet names**: `python3 tools/fleet_names_v2.py programs/*.txt` (all programs share one pool of routine names on the calculator).
- **Verify scripts**: the newest ones (`verify_StudRange_beta15f.py`, `verify_TrendTest_beta3g.py`) run from `verify/` as they are and read older versions from git. The 19 October scripts hard-code the author's folders (`/home/claude/work/...`) and need files that are not in the repository; `verify/README.md` and `docs/dev/independent-review-2026-10-22.md` say what they need and what happened when they were rerun.
- **Python**: `cd python && python3 test_hpstats.py` checks `hpstats.py`, the fleet's arithmetic, against SciPy, statsmodels and brute force.
- **Harness smoke test**: load each program in `tools/ppl_run_v3e.py` with `idle_key=4` and call its main routine; zero warnings and no `PPLError` is the pass.

## Conventions

- A changed program gets the next letter (`beta 15d` → `beta 15e`), replaces the old file in `programs/` (git keeps the old one), updates its header and its "What changed" block, and gets `docs/changes/<name>_CHANGES.md` (why, what changed with line numbers, verification, gate, device checklist, unresolved), a `verify/verify_<name>.py` with its output beside it, a line in `verify/README.md`, and a bullet in the README's test-status note plus its row in the program list.
- **After any change in `programs/`, rebuild the starter pack** with the next number, in two passes (`docs/changes/StarterPack_v5_NOTES.md`): build without `--checked` (`python3 tools/make_starter_pack_v4.py v6 --kit $HPKIT`); load it on the Virtual Calculator (close it, copy the files in, start it), Check each changed program, close it, and copy those files back into the checked-files folder; then build again with `--checked FOLDER`, which stops unless every program has a checked file holding its exact source. Move the older zip out of `starter-pack/`, and rebuild the Prime Loader from the new pack (`prime-loader/build_loader_v1c.py`, then its test).
- **GitHub Pages** (1 Nov 2026): the repository is published at https://metcalfdds.github.io/hp-prime-statistics/ (Settings → Pages, `main`, root). `.nojekyll` keeps Jekyll off, because PPL list syntax such as `{{x,y}}` in the Markdown breaks its Liquid templates. The front page, `index.html`, links to `prime-loader/` and to the Data Loader by its file name: when `data-loader/DataLoader_vN.html` gets a new number, change that link. `prime-loader/index.html` is written by the loader's build and sends the browser on to the current page, so the address the book prints never changes. A pack that lags `programs/` gives students old versions.
- **The data loader** (`data-loader/`): edit `page_template_v3.html` or `dl_core_v1.js` under a new version number, rebuild the page with its `build_page_vN.py`, and run `node tests/test_core_v1.js` (the encoder against hp-prime-kit's, the Rossi file byte for byte) and `node tests/page_check_v3.js` (the page in Chromium; Playwright). A change to what the page writes must be loaded with DataLoad on the Virtual Calculator before it is called tested.
- Lessons Learned is versioned by letter too (`v7y` → `v7z`), with a "What changed" block at the top; the links in `README.md`, `docs/README.md` and `START_HERE.md` are updated with it.
- Executable code stays ASCII (`ppl_check_v4.py`'s E5); π is `3.14159265359`. Strings may carry any glyph GfxProbe has shown renders. Every routine and local name carries the program's prefix (`st_`, `cs`, `tr`, `dm` …) so the fleet shares one name pool safely.
- Compute upper tails as lower tails or as finite sums of positive terms; never `1 - CDF` where the p may be small.
- Nothing is reported as device-tested unless it ran on the Virtual Calculator, a G1 or a G2; the harness is a PC model.
- **General and advanced versions** (31 Oct 2026). A program's general version (TTestLabG for TTestLab) is built from the advanced one by a script of exact replacements (`tools/make_tlg1_v1.py`): a new name and tag, the companion guide's conventions, general examples. Change the advanced program first, then rebuild the general one with the script's next version, and derive its verify script from the advanced one's the same way, reading every failure before changing an expectation.
- **A verify script must drive every cancel and refusal path** (Esc at each menu, Cancel on each form, each refused read), not only the arithmetic: TTestLab's 59 arithmetic checks passed while ten dialog faults waited for the independent review (31 Oct 2026). A new program gets that review before it is called finished.

## GitHub

- Work on a branch; push with `git push -u origin <branch>`; open the pull request with `gh api repos/metcalfdds/hp-prime-statistics/pulls --input body.json` (GraphQL, and so `gh pr create`, is blocked). The author merges with two clicks; the session's policy does not allow merging.
- The clone is shallow and tracks only `main`: after pushing a branch, add a fetch refspec and set upstream, or the stop hook complains about an unpushed commit that is in fact pushed.
- Never commit hp-prime-kit, `__pycache__`, or anything from the author's working folders.

## Files from the author's computer

His working folder is `D:\HP-Prime` on Rogers-HP. The cheap route for a batch of files is one zip in Dropbox, fetched with the Dropbox connector's download link and `curl` (the link is single-use; one GET, no HEAD). The environment's network policy must allow `*.dropboxusercontent.com`, which the author sets under the environment's Network access. Extract into a fresh folder in the scratchpad, never into the repository.
