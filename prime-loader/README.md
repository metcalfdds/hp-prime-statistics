# HP Prime Loader

**For students: pick your chapter, click Load (or, in Firefox, download and unpack one file), start the Virtual Calculator, tap a program, tap Run.** That's all. The chapter's programs are waiting in the Program Catalog with nothing else to get lost in, and nothing needs checking or compiling first.

**Open it here: <https://metcalfdds.github.io/hp-prime-statistics/prime-loader/>.** That address never changes: it always opens the newest version (this folder's `index.html` sends the browser on to it). The page is one file, `PrimeLoader_v1l.html`, and also works offline on a Windows computer with HP's free Virtual Calculator: download it (on GitHub: open the file, then "Download raw file") and open it in any browser.

- **In Edge or Chrome** the page puts the programs on the calculator itself, with one click on Load.
- **In Firefox (or Safari)** the page gives you one file to download, named for your chapter (`HP_Prime_Chapter_11.zip`), and walks you through unpacking it with Windows' own **Extract All** into the calculator's folder. That takes about two minutes. Firefox never lets a web page write into a folder on your computer, by its makers' design, and many schools require Firefox, so this route is a full part of the page, not a fallback. The page explains the difference to the student in plain words.

Every step on the page says, in plain words, what is happening and why. A "Something not working?" section at the bottom covers the questions students are likely to have: how to open the page in Edge; no HP Prime folder (start the calculator once; OneDrive); "the calculator looks open"; "Syntax Error"; getting old programs back; a real HP Prime.

## What it does

1. **You pick** one or more of the companion guide's 15 chapters, or programs one by one. You can add the sample data set, or your own data file from the [Data Loader](../data-loader/README.md).
2. **You click Load.** The first time, a window opens at Documents: click **HP Prime**, then **Select Folder**, then let the page edit files there. After that it remembers.
3. **The page checks that the Virtual Calculator is closed.** It looks for the lock file the calculator keeps in `HP Prime\Temp` while it runs. A running calculator writes its memory back when it exits, which would undo the load.
4. **It clears the calculator, safely.** Every program on it, every app that is not HP's, and any matrix about to be replaced are moved to `HP Prime\Loader backups\<date time>`. Each file is copied, read back, and only then removed. HP's own apps, settings and lists are left alone.
5. **It writes the chosen files** into `HP Prime\Calculators\Prime` and reads each one back.
6. **You start the Virtual Calculator.** The page says what to do next: Shift, Program, tap a program, Run. It also says how to start CentralLimit (an app) and how to use DataLoad for data.

**Firefox or Safari:** steps 2 to 6 become: download the chapter's zip; close the calculator; Extract All, with Browse pointed at `Documents\HP Prime\Calculators\Prime`; start the calculator. Programs already on the calculator stay (nothing is cleared or backed up on this route).

**HP's Connectivity Kit, and a real HP Prime (G1 or G2):** the page downloads the same files as a zip, and its help says how to use them with the Kit:
1. start the Kit;
2. start the Virtual Calculator, or plug in the real Prime;
3. drag each file onto the calculator's name (**Virtual Prime** for the Virtual Calculator) in the **Calculators** list at the top left of the Kit's window, not into the Content box below it.

This works the same for the Virtual Calculator, a G1 and a G2, and for a real Prime it is the only way. Its help opens with a highlighted reminder to **make sure Apple's Bonjour Service is running**: the Kit uses Bonjour to find calculators (HP's release notes: the Kit and Virtual Calculator "now include Apple Bonjour installers to enable mDns networking on Windows"), and where Bonjour has stopped, the Kit may not see the calculator. The reminder says how to check it in Windows' Services app and points instructors to [`tools/windows-launcher`](../tools/windows-launcher/README.md), which checks Bonjour before opening the Kit.

## How it works

Copying files into the Virtual Calculator's own folder while it is closed loads them. HP's manuals don't say so; [hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit) measured it, and [docs/two-shortcuts.md](../docs/two-shortcuts.md) gives the details and the credits. The page writes into that folder through the browser's File System Access API, which Edge and Chrome have and Firefox and Safari do not.

Every program file is embedded in the page, taken byte for byte from the starter pack it was built from (named at the foot of the page), so the page needs no network. Since v1a (starter pack v5) these are **checked files**: each is the file the Virtual Calculator itself wrote back after the program was Checked once there. It carries the calculator's compiled block, so it runs at once with no Check (measured 1 November 2026: [StarterPack_v5_NOTES.md](../docs/changes/StarterPack_v5_NOTES.md)). The build reads each embedded file with hp-prime-kit and tells the page whether every program carries its block. If one does not, the page keeps the Check step in its next steps.

Designed and written by Claude (Anthropic; Claude Opus 5.5) on 1 November 2026, from Roger's description: "a launcher program that maybe asks 'what programs/data do you want loaded?' and a choose list or something like that — they start the launcher first, it clears the Prime/Virtual Prime, loads the chosen programs, and all the student has to do is start the calculator".

## Tested so far (1 November 2026)

**On Roger's computer** (Windows 11, Virtual Calculator 2.4.2 build 2026-09-09).

The Firefox route's key step, 1 November 2026:

- A zip holding SampDist's checked file was put in Downloads, as Firefox would put it. Roger chose Extract All, then Browse → Documents → HP Prime → Calculators → Prime. The box read `C:\Users\metca\Documents\HP Prime\Calculators\Prime`, with no folder named after the zip added.
- After Extract, `SampDist.hpprgm` was in the Prime folder itself, and the calculator listed it in its Program Catalog.
- Dragging a program file onto the Virtual Calculator's window was refused (the "no" cursor), so that is not a route.

The Connectivity Kit route, 1 November 2026:

- Roger started the Kit, started the Virtual Calculator, and dragged `Norm3.hpprgm`, a checked file, from File Explorer onto **Virtual Prime** in the Kit's Calculators list. Norm3 then ran, asking for mu, sd and x₀.
- The Kit's drag label read "Move", but the file stayed in its folder: the Kit copies.
- Roger: the same drag works for the G1 and G2.

The Edge route, with v1 and starter pack v4 (unchecked files):

- Roger opened the page in Edge, picked chapter 11 and clicked Load. The folder window opened at Documents; he chose `HP Prime` and allowed edits.
- The page found the calculator running and said so. He closed the calculator and clicked Try again.
- The page moved the 29 programs and the CentralLimit app that were on the calculator to `Loader backups\2026-11-01 0827`, and wrote DataLoad, ResampLab and TTestLabG, each byte for byte the pack's file.
- The calculator, started, listed exactly those three in its Program Catalog.
- Two things came out of the run. "Calculator menu" was not clear, so the page now says "the small word Calculator at the top left of its window, or its X". And a computer whose default browser is Firefox opens the page there: the page shows its Edge-or-Chrome note.

**In Chromium:** `tests/test_loader_v1p.js`, **59 PASS, 0 FAIL** with starter pack v18 (`tests/test_loader_v1p_output.txt`; v1o's, the same checks, gave 59 with pack v17; v1n's gave 59 with pack v16; v1m's gave 59 with pack v15, one check more than v1l's, chapter 11 now loads four programs; v1l's gave 58 with pack v14; v1k's, the same checks, gave 58 with pack v13; v1j's, the same checks, gave 58 with pack v12; v1i's, the same checks, gave 58 with pack v11; v1h's, the same checks, gave 58 with pack v10; v1g's, the same checks, gave 58 with pack v9; v1f's, the same checks, gave 58 with pack v8; v1e's, the same checks, gave 58 with pack v7; v1d's test, which ran four times in a row with pack v6, after the test was made to wait for the own-data list, which one run in four had read too early). It drives the page in Chromium 141 against a mock `HP Prime` folder in the browser's private file system: HP's apps, settings, a list, a matrix, old programs, an old CentralLimit app, and the lock file. The folder picker is replaced by one that returns that folder. Checked:

- a running calculator is refused, with nothing written;
- chapter 11, then chapter 7 with the sample data, then your own `M3.hpmat`: every file byte for byte against the pack;
- only the chosen programs are left on the calculator;
- the backups hold every old file byte for byte, and HP's files are untouched;
- the folder is remembered after a reload;
- picking the wrong folder gets a sentence saying which one to pick, and picking Documents finds HP Prime inside it;
- cancelling the picker is handled;
- "all 30" loads all 30, and the zip holds all of them byte for byte;
- a browser without the API gets the note and the zip;
- the page opens as a local file with no errors;
- with a checked pack, the next steps say tap and Run, with Check only as a fallback;
- **Firefox** (a browser without the folder API, with Firefox's user-agent):
  - its own route shows, naming Firefox and giving the reason in plain words;
  - Download stays off until a chapter is picked;
  - chapter 12 downloads as `HP_Prime_Chapter_12.zip`, holding ChiTable and FitCheck at its top level, byte for byte;
  - two chapters make `HP_Prime_Chapters_7_12.zip`;
  - the app and data notes appear when needed;
- the Connectivity Kit help opens with the Bonjour reminder;
- v1c: the Data Loader link is the Data Loader page's web address, and `index.html` sends the browser on to the page;
- the plain-language sections are present (before you start, why for each step, six help topics).

The page was also looked at in light and dark, at desktop and phone widths: nothing runs off the side.

**v1b with the checked pack, on Roger's computer (1 November 2026, 08:59-09:03):** Roger opened `PrimeLoader_v1b.html` in Edge, picked chapter 7 and clicked Load. The page moved the six programs then on the calculator to `Loader backups\2026-11-01 0859` and wrote SampDist, GaltonBoard and the CentralLimit app, each byte for byte pack v5's. Claude then started the calculator: its Program Catalog listed GaltonBoard and SampDist; `GaltonBoard` and `SampDist` typed in Home ran at once (the board; the Sampling Distribution menu); CentralLimit, started from Apps, showed its welcome page and then its own Views menu. **Nothing was checked.**

**On the web (1 November 2026):** after the repository went on GitHub Pages, v1b opened from its web address in Chromium worked as Edge/Chrome (a secure page with folder access, no errors) and as Firefox (its own route; chapter 11's zip held the checked TTestLabG, DataLoad and ResampLab). v1c is v1b with the Data Loader link changed and `index.html` added.

**v1p (13 November 2026)** is v1o built from starter pack v18, whose ChiTable beta 3m (round 13) gives the exact test for its 2 × 3 and 3 × 2 tables on results page 5, and calls a count equal to its expected count "just as expected" (`docs/changes/ChiTable_beta3m_CHANGES.md`). The catalog names that version; the page template is v1c's, unchanged.

**v1o (13 November 2026)** is v1n built from starter pack v17, whose twelve programs changed by round 12 carry their new versions: help-page fixes that the book's pre-submission read found (AnovaLab, BayesTree, CICatcher, DataLoad, EpiStats, FitCheck, PowerViz, RankLab, RiskLab, SampDist, StatDist, TTestLab). All 31 files are the Virtual Calculator's own checked files; the page template is unchanged.

**v1n (9 November 2026)** is v1m built from starter pack v16, whose 31 programs carry round 11: the help pages in plain words (Roger: "a student being able to understand is the priority"), each changed page laid out again at the calculator's own glyph widths, measured on the Virtual Calculator, so nothing is cut; a page that no longer fitted became two. All 31 files are the ones the Virtual Calculator 2.4.2 wrote back after a Check ("No errors in the program"), with no run in between. The catalog names those versions. The page template is v1c's, unchanged.

**v1m (7 November 2026, night)** is v1l built from starter pack v15, which carries a 31st program, TDist3D beta 1 (Student's t as a surface turned with a finger: every t curve at once, a red slice with its critical value and tail chance, a Curves view), offered with Chapters 9 and 11, and BurrLab beta 1p (the Family map's border drawn as four lines, not a one-colour `RECT_P` that filled it dark gray on the G1; deeper tints; the tail shades opaque). All 31 files are the ones the Virtual Calculator 2.4.2 wrote back after a Check. The catalog names those versions and the EVERYTHING card counts 31. The page template is v1c's, unchanged.

**v1l (5 November 2026)** is v1k built from starter pack v14, whose 30 programs carry round 9: one header on every help page, "<Name> help n/N: <Topic>", American spelling on screen, and "Roger D. Metcalf"; and round 10 of the same day: 19 of them refuse a typed value that no real problem needs (a mean or x from -10,000 to 10,000; an SD, a df or a rate at most 1,000; a typed sample size at most 10,000), with a sentence that gives the range. The calculator handles far larger numbers, and the tests typed values up to 1E100; the limits keep the programs quick. All 30 files are the ones the Virtual Calculator 2.4.2 wrote back after a Check ("No errors in the program"). The catalog names those versions; the page is unchanged; its test: 58 PASS, 0 FAIL.

**v1k (4 November 2026, night)** is v1j built from starter pack v13, whose 18 changed programs carry round 8: the monkey test's 1,000 runs on every program that had not had them (each now passes 1,000 of 1,000), and "t-test" written with its hyphen on every screen. The catalog names the new versions and says "t-tests"; Chapter 11 is "t-Tests: Two Samples" and Chapter 1 "Data, Sampling, and Study Design", as in the book. The page itself is unchanged, and so are the other 12 programs' files. All 18 changed files were Checked on the Virtual Calculator 2.4.2 in the cloud workspace, and each reads back as its source.

**v1j (4 November 2026)** is v1i built from starter pack v12, whose 5 changed programs carry round 7: TTestLab beta 1e and TTestLabG beta 1c name the flowchart's go-ahead key Run, not OK; EpiStats v1.7h passes its first monkey test; ChiTable beta 3i and ErrorRate beta 1g correct a label and a help line. The page itself is unchanged, and so are the other 25 programs' files. The five checked files were written back by the Virtual Calculator 2.4.2 running in the cloud workspace (Lessons Learned v7zm, §16), each after a Check ("No errors in the program").

**v1i (2 November 2026, night)** is v1h built from starter pack v11, whose 11 changed programs carry round 6: what a student types is kept to sensible ranges and refused with a sentence outside them (alpha from 0.001 to 0.2 everywhere), every menu item fits its box, and BurrLab beta 1l draws a y axis on every plot; the page itself is unchanged, and so are the other 19 programs' files. All 11 checked files were collected after a Check alone.

**v1h (2 November 2026, night)** is v1g built from starter pack v10, whose 30 programs carry round 5: every number of 1,000 or more on the screen shows its commas, and AgreeLab and ResampLab draw d̄; the page itself is unchanged. All 30 files are checked ones, from the Virtual Calculator on 2 November 2026, night.

**v1g (2 November 2026)** is v1f built from starter pack v9, whose PowerViz v2.5l, ScatterLab beta 2f, ChiTable beta 3f and GaltonBoard beta 3f carry the monkey test's fourth round; the page itself is unchanged, and so are the other 26 programs' files. All four checked files were collected after a Check alone.

**v1f (1 November 2026, night)** is v1e built from starter pack v8, whose CICatcher beta 2e, Norm3 v2.4d, NormExplorer beta 42e and StatDist v2.7h carry the monkey test's third round and what the Virtual Calculator found (density labels over the axis); the page itself is unchanged, and so are the other 26 programs' files. All four checked files were collected after a Check alone.

**v1e (1 November 2026, evening)** is v1d built from starter pack v7, whose SampDist v2.3e and BayesTree beta 8f carry the monkey test's fixes and what the Virtual Calculator found; the page itself is unchanged, and so are the other 28 programs' files. Both checked files were collected after a Check alone.

**v1d (1 November 2026)** is v1c built from starter pack v6, whose TTestLab beta 1c and TTestLabG beta 1a carry the monkey test's fixes; the page itself is unchanged. Each of those two checked files was collected after a Check and nothing else (a checked file keeps the values of its last run).

**Not yet:** a Mac; a computer that has never run the Virtual Calculator before.

## Files

| File | What it is |
|---|---|
| `PrimeLoader_v1p.html` | The page, built: open this one. About 2 MB, all 31 programs inside, checked. |
| `index.html` | Written by the build: sends a browser at `.../prime-loader/` on to the current page, so the book's link never changes. |
| `loader_template_v1c.html` | The page's source, with slots for the two cores, the catalog, the files and the Data Loader's web address. |
| `loader_core_v1.js` | The file work: find the folder, check the lock, back up, clear, write, read back; and the zip reader for the embedded files (every CRC checked). No DOM: the page and the tests share it. |
| `build_loader_v1p.py` | `python3 build_loader_v1p.py ../starter-pack/HP_Prime_Statistics_Starter_Pack_v18.zip --kit PATH_TO_hp-prime-kit`. Holds the chapter list (from the companion guide's Chapter Plan), each program's one line, and the name to type in Home. Stops if the catalog and the pack disagree, and says how many files are checked. Uses `../data-loader/dl_core_v1.js` for the zip it offers. |
| `tests/test_loader_v1p.js` | The Chromium test: `node tests/test_loader_v1p.js PrimeLoader_v1p.html ../starter-pack/HP_Prime_Statistics_Starter_Pack_v18.zip` (Playwright). |

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
