# HP Prime Loader

**For students: say which calculator and which programs, and click one button.** Then start the calculator, tap a program, tap Run. Nothing needs checking or compiling first.

**Open it here: <https://metcalfdds.github.io/hp-prime-statistics/prime-loader/>.** That address never changes: it always opens the newest version (this folder's `index.html` sends the browser on to it). The page is one file, `PrimeLoader_v2g.html`, and also works offline: download it (on GitHub: open the file, then "Download raw file") and open it in any browser.

## What it does (v2g, 18 November 2026)

*v2g is the page after the cable's first day on the author's two calculators (18 November 2026; the six logs are in [usb/logs/](usb/logs/)). The cable is now shown to every student, not at a test address. A real HP Prime is offered **groups of chapters**, because neither calculator held all 30 programs at once, and the cable takes the book's other programs off before it sends a group. The Virtual Calculator takes all the programs, with nothing to choose. v2b to v2f led here over the two days before (the cable at a test address, the two ways' names, Roger's sentence, the sentence for Firefox and Safari); their files are in the repository's history.*

Roger, 17 November: "i'm thinking we need to make this process as simple as is possible", and "we do need to make some sort of very simple loader ... to get the programs on a physical calcuator". On 18 November, when both calculators had filled up: "for the Virtual Calculator: load all programs at once; then for a physical G1 or G2 choose 1) Ch 1-3, 2) Ch 4-6, 3) Ch 7--9. 4) Ch 10-12, 5) Ch 13-15, 6) Advanced 1, 7) Advanced 2, 8) Advanced 3", and "we should just make the choice of VIrtual Calculato automatically load all".

**1. Which calculator?** The Virtual Calculator on this computer, or a real HP Prime (a G1 or a G2) on its USB cable.

**2. Which programs?**

| Calculator | Choice | What goes on | What happens to what is already there |
|---|---|---|---|
| Virtual Calculator | **All 31 programs**; there is nothing to choose | Every program of the book, and the CentralLimit app. | Stays. A file of the same name is replaced, and the old copy goes to the backup. |
| A real HP Prime | **A group of chapters**, one of eight: Chapters 1–3, 4–6, 7–9, 10–12, 13–15, and Advanced 1, 2 and 3 | A chapter group is the programs of its chapters and TestChooser, the which-test flowchart. An advanced group is three or four of the 11 programs no chapter uses. The largest, Chapters 7–9, is 10 programs and the app: 1,200,488 characters by cable. | **By the cable, the book's programs that are not in the group are taken off the calculator first, to make room** (Roger: "Yes, take them off"). A program of the student's own is never taken off, and one taken off comes back with its group. By the Kit the page can take nothing off, and tells the student to make room by hand. |
| Either | *Only the programs I tick* (under "More choices") | The programs ticked in a list of all 31. | Stays. |
| Either | *Data* (under "More choices") | The book's sample data set, or a data file from the [Data Loader](../data-loader/README.md), and DataLoad with it, whatever else is chosen. A data file is opened and checked before it is taken. | Stays; on the Virtual Calculator the matrix it replaces goes to the backup. |

**Why groups.** On 18 November the author's G1, sent all 30 programs down the cable, verified 15 (2,104,376 characters), then took the 16th and kept only its name; its Program Catalog showed 4.35 MB of programs. His G2 answered later with every program (0.4 s for the first, 22 s for the 10th and the 13th) and at the 14th took one report and then nothing for a minute. So no group is over about 1.2 million characters. The build makes the groups (`build_loader_v2g.py`, `CHAPTER_GROUPS`): the five chapter groups from the chapter plan, and the programs of no chapter dealt into three groups of about equal size. "One chapter", which v2a to v2f offered, is gone from the page for both calculators (its code is still in the template, unreached).

On the Virtual Calculator nothing is ever deleted: whatever is replaced is in `Documents\HP Prime\Loader backups\<date time>`, copied, read back, and only then removed from the calculator's folder. HP's own apps, settings and lists are never touched.

**3. One button.**

- **The Virtual Calculator, in Edge or Chrome: Load.** The first time, a window opens at Documents: click **HP Prime**, then **Select Folder**, then let the page edit files there. After that it remembers. The page checks that the calculator is closed (it looks for the lock file the calculator keeps in `HP Prime\Temp` while it runs: a running calculator writes its memory back when it exits, which would undo the load), writes the files into `HP Prime\Calculators\Prime`, and reads each one back.
- **The Virtual Calculator, in Firefox or Safari: Download.** Firefox never lets a web page write into a folder, by its makers' design, and many schools require Firefox, so this route is a full part of the page. The programs download as one zip (`HP_Prime_all_programs.zip`), and the page walks the student through Windows' own **Extract All** into the calculator's folder.
- **A real HP Prime, in Chrome or Edge: Send to the calculator**, straight down the USB cable, with HP's Connectivity Kit kept as the second way (below).
- **A real HP Prime, in Firefox or Safari: Download, and HP's Connectivity Kit.** A zip of the group (`HP_Prime_Chapters_7-9.zip`) and six steps: download, unpack, start the Kit and plug the calculator in, drag each file onto the calculator's name, close the Kit, run. A folded note says how to check that Bonjour is running. Above the steps one sentence says that Chrome or Edge can send the programs down the cable.

**From the Data Loader.** The Data Loader's last step links to `.../prime-loader/?data=1`. The page then opens with no program chosen and a notice that says what to click, so that the student's data and DataLoad are all that Load adds. `index.html` carries the `?data=1` on.

A phone, a computer that is not Windows, and a browser too old to unpack the programs each get a notice at the top. A "Something not working?" section covers a missing Virtual Calculator, opening the page in Edge, no HP Prime folder, "the calculator looks open", "Syntax Error", a program that is gone, and the Kit for the Virtual Calculator.

**Straight down the cable, without the Kit.** Chrome and Edge let a page talk to a calculator on its cable (WebHID); [usb/README.md](usb/README.md) has the route and every log. For a real HP Prime in those browsers step 3 is called **"Two ways to load *Statisticles* onto a physical Prime G1 or G2 calculator"** (Roger, 18 November 2026; *Statisticles* is the book's name for its programs), and under the title stands his sentence, as the book has it:

> We believe our method should work, and we have tested it, and are continually testing it. It is easier to use than the Connectivity Kit, and it avoids the Kit's mDNS (Bonjour) issue. But just in case you have trouble with the *Statisticles* way, we also present 2), the official HP way. (And if something does go wrong, please be sure to let us know on our GitHub page, github.com/metcalfdds/hp-prime-statistics/issues.) CentralLimit and data files go only by 2).

"And we have tested it" went in on 18 November, when Loader v2d had put Chapter 12 on the author's G2 (Chrome) and G1 (Edge), each download verified, and ChiTable had run at once with no Check; a line under 1) says so. The two ways are **"1) The *Statisticles* way: straight down the USB cable"** and **"2) The official HP way: the Connectivity Kit"** (his names), never "the first way" or "the other way".

1) The *Statisticles* way: plug in, close the Kit, click **Send to the calculator**. For a group the page first makes room: it sends a delete for each of the book's programs that is not in the group (20 to 27 of them, by the group; 0.3 s apart, as the calculators took them on 17 November). Then it sends each program and **verifies the download** (Roger: "instead of saying 'asking for program back' say 'verifying download'"): it asks the calculator for the program back and compares the two, character for character. A program counts as loaded only when the two are the same; the first that is not ends the load, and the page says which programs are on the calculator and what to do. Three endings have words of their own:

- **"The calculator is full"**: the calculator took the program and gave it back empty, as the G1 did. The page says to delete the 0 KB entry, make room and send again.
- **"The calculator stopped responding"**: a report has stood for a minute with the calculator still on its cable, as the G2 did. Unplug, off and on, send again.
- **"The calculator went off the cable"**: the browser said so.

CentralLimit, which is an app of three files, and data files do not travel this way; the page says so and opens the Kit's steps for them. **Stop** takes effect between two programs. "What passed on the cable" is a log that can be saved and sent to an instructor; it does not hold the calculator's serial number. This way does not go through Bonjour: the page reaches the calculator through the browser's WebHID, as a USB device, and looks for nothing on a network. A load with the Bonjour Service stopped has not been tried.

**The Connectivity Kit's steps are kept whole** (Roger, 17 November 2026: "maybe we shoould keep the instructions for the COnnectivity Kit as a backup"). In Firefox or Safari they are the page's main line. In Chrome or Edge they are way 2), folded below way 1) under "2) The official HP way: the Connectivity Kit", and they open by themselves when the cable cannot do what is wanted.

**What has run on a calculator, and what has not** (18 November 2026, the author's G2 and G1, firmware build 15751):

- Chapter 12 (three programs, 441,568 characters) by Loader v2d: G2 in Chrome 4.6 s, G1 in Edge 10.2 s, every download verified; ChiTable ran at once.
- All 30 programs: neither calculator took them (above). That is why v2g has groups.
- **Not yet run on a calculator: v2g itself**, which means the groups, making room (a delete in the newer framing has been seen to work on the G2 only; the G1's deletes on 17 November were in the old framing), and the longer wait for a download to verify.

### What v2g was tested with

`tests/test_loader_v2g.js`: **156 PASS, 0 FAIL** in Chromium against a mock of `Documents\HP Prime` and a pretend calculator, with starter pack v23 (`tests/test_loader_v2g_output.txt`; about twelve minutes, most of it the cable's waits). The mock folder holds HP's apps and settings, an old book program, an old copy of the app, a matrix, and a program of the student's own, and every file the page writes is compared with the pack byte for byte:

- a running calculator is refused, with nothing written;
- all the programs: 30 program files and the app's three, byte for byte; the student's own program and the matrix untouched; the backup holds exactly what was replaced; a second time, and with the sample data;
- the Virtual Calculator is offered neither a chapter nor a group;
- ticked programs (two the student had taken off) and a data file on its own: added, and nothing moved off;
- a badly named data file, a renamed CSV, a file cut short and one too short are each refused with the reason; the student's own M1 wins over the sample;
- the wrong folder, Documents picked in place of HP Prime, and a cancelled picker;
- a real HP Prime in a browser without WebHID: the eight groups, every program in one, no "All the programs"; the Kit's six steps as the main line; the zips of Chapters 7–9 (with the app) and of Chapters 10–12 byte for byte; the note that tells the student to make room by hand; the notes for the app and for data, each saying that it has not been tried on a real calculator;
- from the Data Loader (`?data=1`): the notice, no program chosen, the file and DataLoad added, and `index.html` carrying the address on;
- Firefox's route (the zip of everything, byte for byte), a phone, a Mac, an old browser, a narrow window, and the page opened as a file;
- **the cable** (part 13, against `usb/tests/mock_prime_v3a.js`, which by default does what the two calculators did): the title, Roger's sentence and the two names, word for word; Chapters 1–3 to a pretend G2: what the calculator holds is each program's source exactly as the pack's file holds it, character for character, sent not compressed in the newer framing after one `FD`, no report twice; a second group without unplugging takes the first group's programs off and leaves the student's own; **the eight groups one after another onto one pretend G2**, the calculator holding after each that group and the student's own program and nothing else of the book; the largest group to a pretend G1 in reports of 64 bytes; the 30 programs counted (4,028,362 characters; 127,913 reports of a G1, 7,892 of a G2), and no group over 1,300,000 characters;
- **the cable's slips**: no group picked; no calculator picked; the Kit left open; a calculator that does not answer; one that still says version 01 (nothing is sent); a program the calculator acknowledges and does not keep, and one damaged on the way (the load stops there, the one before is ticked, the ones after are never sent, and the page does not say Done); **a calculator with no room left** ("The calculator is full"); **one that stops responding while still on its cable**; the cable pulled out in the middle of a program, with a write that never comes back and with one that fails at once; Stop and a second click on Send while a download is being verified; the calculator's clock saying "send again" in the middle of every program; an app or data in the choice;
- the plain address in Chrome (the two ways, and a group sent) and in a browser without WebHID (the Kit, and the sentence that names Chrome and Edge, by the browser's own name).

**Not yet run in Edge on a Windows computer** for the Virtual Calculator's folder work: it was driven in Chromium against a mock folder, as for every version. Still marked on the page as not yet tried on a real calculator: the CentralLimit app's folder dragged in the Kit, and a data file dragged in the Kit.

**For the book's next draft** (`cable_sections_v1f.md`, held with the book's source): Appendix B's "The easy way: the Prime Loader" says "pick a chapter"; the Virtual Calculator now takes all the programs. Appendix B's "On a real calculator" becomes "Two ways to load *Statisticles* onto a physical Prime G1 or G2 calculator", with the groups, and Appendix F, "For HP programmers", gets what the cable taught.

## The review of 17 November 2026 (v1v)

*v1v's files are in the repository's history: v2a replaced them the same night, v2b replaced v2a's a few hours later, and v2c to v2g replaced those the next day.*

Roger asked for the students' helpers to be reviewed: "they must be bullet proof and as simple as possible". The tests passed, 59 of 59, but every one of them did what a careful student does. Tried with the slips a student makes, v1u did these things, and v1v does not:

| What a student does | v1u | v1v |
| --- | --- | --- |
| Adds a data file, picks no chapter, clicks Load | Every program was moved to the backup. The student had data, no DataLoad, and an empty Program Catalog. | The file and DataLoad are added. The programs stay. |
| Picks Chapter 13 (or 4 to 10, or 12) and the sample data | The data went on without DataLoad, and the next steps said "run DataLoad". | DataLoad is added, and the summary says why. |
| Adds a file named M1.hpmat that is not a matrix file (a renamed CSV, a download cut short) | Taken as it was. | Opened and checked (`LoaderCore.checkHpmat`): refused with the reason. |
| Ticks the sample data and adds an M1.hpmat of their own | Both were written to M1, one over the other, without a word. | The student's own file is used, and the summary says the sample is left out. |
| Opens the page on a phone | The download-and-unpack steps were shown, as if they could work. | A notice at the top: the page needs the Windows computer, and its address. |
| Opens the page on a Mac | Windows steps, with one sentence lower down that Macs are untested. | A notice at the top says so, and points to the Connectivity Kit. |
| Uses a browser too old to unpack the programs | "Could not make the file: DecompressionStream is not defined". | A notice at the top, and the buttons stay off. |

`tests/test_loader_v1v.js`: **81 PASS, 0 FAIL** (`tests/test_loader_v1v_output.txt`). The check "loading only data clears the programs too (a clean slate)" is gone: it described the first fault as if it were intended.

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

**In Chromium:** `tests/test_loader_v1v.js`, **81 PASS, 0 FAIL** with starter pack v23 (`tests/test_loader_v1v_output.txt`; v1u's 59 checks with the review's changes and additions, above; v1u's gave 59 with pack v23; v1t's, the same checks, gave 59 with pack v22; v1s's, the same checks, gave 59 with pack v21; v1r's, the same checks, gave 59 with pack v20; v1q's gave 59 with pack v19; v1p's gave 59 with pack v18; v1o's gave 59 with pack v17; v1n's gave 59 with pack v16; v1m's gave 59 with pack v15, one check more than v1l's, chapter 11 now loads four programs; v1l's gave 58 with pack v14; v1k's, the same checks, gave 58 with pack v13; v1j's, the same checks, gave 58 with pack v12; v1i's, the same checks, gave 58 with pack v11; v1h's, the same checks, gave 58 with pack v10; v1g's, the same checks, gave 58 with pack v9; v1f's, the same checks, gave 58 with pack v8; v1e's, the same checks, gave 58 with pack v7; v1d's test, which ran four times in a row with pack v6, after the test was made to wait for the own-data list, which one run in four had read too early). It drives the page in Chromium 141 against a mock `HP Prime` folder in the browser's private file system: HP's apps, settings, a list, a matrix, old programs, an old CentralLimit app, and the lock file. The folder picker is replaced by one that returns that folder. Checked:

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

**v1v (17 November 2026, evening)** is the review's version: the page template's v1d and the loader core's v2, on starter pack v23 as before (no program changed). "The review of 17 November 2026", above, has what changed and why. Not yet run in Edge on a Windows computer: the folder work was driven in Chromium against a mock folder, as for every version, and the first load on Roger's computer is the check that counts.

**v1u (17 November 2026)** is v1t built from starter pack v23, whose sixteen programs changed by round 17 carry their new versions. Round 17 changed words on the screen only, to the book's house form for a statistic's letter ("F-test", "df = (n - 1)", "p-value"): AgreeLab beta 1i, AnovaLab beta 1j, CICatcher beta 2m, EpiStats v1.7m, ExhibitLab beta 1i, FitCheck beta 1j, PowerViz v2.5t, RankLab beta 1k, ResampLab beta 1j, ScatterLab beta 2m, StudRange beta 15n, TDist3D beta 1b, TTestLab beta 1l, TTestLabG beta 1i, TestChooser beta 2h and TrendTest beta 3n. The page's catalog names the new versions (it reads each one from `programs/`); 31 of 31 files are checked files; the test is v1t's, unchanged, and gives the same 59.

**v1t (15 November 2026, night)** is v1s built from starter pack v22, whose nine programs changed by round 16 carry their new versions: AnovaLab beta 1i (Dunnett's test of every group against a control), RankLab beta 1j (Page's *L* and the runs test), FitCheck beta 1i (Dixon's outlier test), CICatcher beta 2l (tolerance intervals), BiNorm3D beta 1g (a target view with the circular error probable), and StatDist v2.7n, AgreeLab beta 1h, RiskLab beta 1h and BurrLab beta 1r, whose headers say what was done with the programs they stand beside (`docs/changes/StarterPack_v22_NOTES.md`). The build script is v1s's but for its name and its notes. The page template is v1c's, unchanged.

**One change in the test, and why.** The Chromium of the cloud workspace this was run on (Chrome for Testing 153.0.8010.12, Playwright 1.63) ends with SIGTRAP when a folder handle is read back from IndexedDB, which is how the page remembers the calculator's folder. `tests/idb_handle_probe_v1.js` shows it with a page that holds nothing of ours (`tests/idb_handle_probe_v1_output.txt`): a string is stored and read, the handle is stored, and reading the handle ends the browser. So `test_loader_v1t.js` keeps the handle's name in IndexedDB and opens the folder again by that name; the 59 checks are v1s's, and the remembering still goes through IndexedDB and a reload. The page itself is not changed. **Not known from here:** whether Chrome or Edge on a student's computer does the same with a folder picked from the disk (a headless browser has no picker). v1s and the versions before it were used on Rogers-HP with the folder remembered between visits; the check is to open the page in Edge, load a chapter, close the tab, and load another chapter from a new tab.

**v1s (15 November 2026)** is v1r built from starter pack v21, whose seven programs changed by round 15 carry their new versions: ScatterLab beta 2l (a 95% confidence interval for ρ), FitCheck beta 1h (a standard error beside the skewness and the kurtosis), and RankLab beta 1i, AnovaLab beta 1h, ResampLab beta 1i, ExhibitLab beta 1h and SurvLab beta 1g, whose credits say what was done with the TI-83/84 programs they follow (`docs/changes/StarterPack_v21_NOTES.md`). The build script is v1r's but for its name and its notes. The page template is v1c's, unchanged.

**v1r (14 November 2026, night)** is v1q built from starter pack v20, whose TTestLab beta 1k and TTestLabG beta 1h (round 14, part 2) add the one-sample *t*-test and the one- and two-proportion *z*-tests (`docs/changes/TTestLab_beta1k_CHANGES.md`). Chapter 9 now lists TTestLabG, and its "Coming: one-sample t in TTestLabG" is gone. Each program's version in the page's data is now read from `programs/` when the page is built: v1q's table still named an older version for 14 of the 31 programs (the page does not show versions, so no student saw them). The page template is v1c's, unchanged.

**v1q (14 November 2026)** is v1p built from starter pack v19, whose CICatcher beta 2k and ScatterLab beta 2k (round 14) carry a help-page wording fix and, in ScatterLab, the slope's test, two 95% bands and Anscombe's quartet (`docs/changes/ScatterLab_beta2k_CHANGES.md`). The catalog names those versions; the page template and the loader's core are unchanged.

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
| `PrimeLoader_v2g.html` | The page, built: open this one. About 2.4 MB, all 31 programs inside, checked. |
| `index.html` | Written by the build: sends a browser at `.../prime-loader/` on to the current page, with whatever follows the address (`?data=1`, `?usb=1`), so the book's link never changes. |
| `loader_template_v2g.html` | The page's source, with slots for the three cores, the catalog, the files and the Data Loader's web address. |
| `loader_core_v3.js` | The file work: find the folder, check the lock, plan what to move (`planAdd`: only what is replaced; `planBook`: the book's programs, for one chapter, which the page has not offered since v2g), back up, write, read back; the check of a data file; and the zip reader for the embedded files (every CRC checked). No DOM: the page and the tests share it. |
| `build_loader_v2g.py` | `python3 build_loader_v2g.py ../starter-pack/HP_Prime_Statistics_Starter_Pack_v23.zip --kit PATH_TO_hp-prime-kit`. Holds the chapter list (from the companion guide's Chapter Plan), the groups for a real HP Prime (`CHAPTER_GROUPS`; the advanced programs are dealt into three by size), each program's one line, and the name to type in Home. Stops if the catalog and the pack disagree, or if the source inside a program's file is not the one in `programs/`, and says how many files are checked. Uses `../data-loader/dl_core_v2.js` for the zip it offers and `usb/prime_usb_v3a.js` for the cable. |
| `tests/test_loader_v2g.js` | The Chromium test: `node tests/test_loader_v2g.js PrimeLoader_v2g.html ../starter-pack/HP_Prime_Statistics_Starter_Pack_v23.zip` (Playwright; about twelve minutes, most of it the cable's waits). |
| `usb/` | A real HP Prime on its USB cable, from a web page: the code, a pretend calculator to test it with, and the logs of two real ones. [usb/README.md](usb/README.md). |
| `tests/idb_handle_probe_v1.js` | Shows the browser fault the test steps round: a folder handle read back from IndexedDB ends Chrome for Testing 153 (see above). |

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
