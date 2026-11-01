# Two shortcuts the manuals don't mention

*1 November 2026. Everything below was tested on the HP Prime Virtual Calculator 2.4.2 (build 2026-09-09), 64-bit, on Windows, on 31 October 2026.*

Two things make HP's free Virtual Calculator far easier to use with a class:

1. **Loading programs by copying files** into the calculator's own folder: all 30 programs at once, with no Connectivity Kit and no pasting of code.
2. **Loading a big data set as one matrix file**, made from a spreadsheet, so nobody types data into a calculator.

HP's own manuals and teaching guides describe neither. The first is known from a handful of community projects, credited below. The second, as far as we have been able to find, is new here. This page says how each one works, what we found when we tried it, and who found what.

---

## 1. Programs: copy the files into the calculator's own folder

**What HP describes.** HP's documents send programs and apps from the Connectivity Kit (drop the files into its Content pane, right-click, Send) or have you paste a program's text into the calculator (*HP Prime Advanced Workshop*, 2014; *HP Prime APSI 2015 Webinar: Programming in HP PPL*; the User Guide). Both work, one program at a time.

**The shortcut.** On Windows, the Virtual Calculator keeps its whole memory as files in one folder, `Documents\HP Prime\Calculators\Prime`, and reads that folder when it starts. A program file (`.hpprgm`) copied in while the calculator is closed is in its Program Catalog the next time it opens. An app's folder (`.hpappdir`) copied the same way is in the Application Library. MicroPython programs load the same way.

1. Start the Virtual Calculator once, then close it with its **Calculator menu → Exit**. The first start makes the folder.
2. Copy the `.hpprgm` files (and any `.hpappdir` folders) into `Documents\HP Prime\Calculators\Prime`.
3. Start the calculator. **Shift**, then **Program**, lists the programs.
4. **A file from this repository's starter pack (v5 or later) or the Prime Loader runs at once.** A program file made any other way (hp-prime-kit's `hpprime write`, say) needs one Check first: highlight it, tap Edit, then tap Check. The calculator says "No errors in the program". Until then that program will not run.

**What we found** (31 October 2026, loading 28 programs and an app at once: [StarterPack_v1_NOTES.md](changes/StarterPack_v1_NOTES.md)):

- **Close it first.** The calculator reads its folder only when it starts. A file copied into a running calculator appears only after a restart.
- **One Check per program, unless the file was already checked.** A file without the calculator's compiled block needs Check: before it, the catalog's Run did nothing and typing the name in Home gave "Syntax Error". After Check the program ran, and its file had grown by the compiled block the calculator writes back (ChiTable 325 KB → 345 KB). **A file that carries that block runs at once**, even on a calculator that has never seen the program (1 November 2026: [StarterPack_v5_NOTES.md](changes/StarterPack_v5_NOTES.md)). So the starter pack, since v5, and the Prime Loader carry checked files, and students never Check.
- **Type the name as its `EXPORT` line spells it.** TTestLabG's is `TTESTLABG`: typed as `TTestLabG` in Home, it gave "Syntax Error". The starter pack's list gives each program's name. And when a program is not on the calculator, Home may run a different one: with TTestLabG missing, `TTESTLABG` started TTestLab, read as `TTESTLAB*G`. Tapping the name in the Program Catalog avoids both.
- **Don't start it a second time while it is running.** We did, by mistake: it opened a second calculator, `Prime_1`, with a folder of its own (and then a third, `Prime_2`). Copy into `Prime`.
- **A renamed `.txt` will not load.** An `.hpprgm` is a binary file (the program's text, in UTF-16, inside a Connectivity Kit header). Ours are built with hp-prime-kit's `hpprime write` and read back against their source.
- **Older guidance points elsewhere.** A 2014 forum post puts the emulator's programs in `AppData\Roaming\HP_Prime`. We have tried only version 2.4.2's folder, and not the Mac or Linux builds.
- **Real calculators: no.** A G1 or G2 has no folder on the PC. The Connectivity Kit's own `Calculators` folder is a mirror, not a mailbox (hp-prime-kit), so copying into it sends nothing: drag the files onto the calculator's name in the Kit's Calculators list instead. That drag works for the Virtual Calculator too ("Virtual Prime" in the list; tried 1 November 2026), and for the G1 and G2. **Make sure Apple's Bonjour Service is running first**: the Kit finds calculators through it (HP's release notes: the Kit and Virtual Calculator "now include Apple Bonjour installers to enable mDns networking on Windows"), and where it has stopped the Kit may not see the calculator. [`tools/windows-launcher`](../tools/windows-launcher/README.md) checks it and starts the Kit.

**Who found it.**

- **[hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit)**, by Jordi Rigau (MIT licence), measured it on 6 September 2026, on the Virtual Calculator 2.4.15515: "The emulator's folder really is a mailbox" (`docs/topics/deploy.md`). Its `hpprime install` command copies a file in. Its finding that a program arriving as a file has to be compiled once is the Check step above. **This is where we learned it.**
- **[hpprime-stoichiometry](https://github.com/abaccin/hpprime-stoichiometry)**, by abaccin (Apache 2.0), ships `deploy.ps1`. This PowerShell script stops the Virtual Calculator and the Kit, copies its app into the calculator's folder and the Kit's, and starts both again.
- **[HP-DOOM](https://github.com/Rudicito/HP-DOOM)**, by Rudicito, ships `copy-to-emulator.sh`, which copies the game's app folder into the emulator's folder on Linux, under Wine.
- **That a checked file needs no Check is ours.** hp-prime-kit had measured only files without the compiled block. **Claude** tested the other case on 1 November 2026: TTestLabG's checked file, copied into a calculator that had forgotten the program, ran from Home at once, and the control (ResampLab without its block) gave "Syntax Error".

**What this repository adds: the [starter pack](../starter-pack/README.md).** All 30 programs and the CentralLimit app come in one zip, built from `programs/` by `tools/make_starter_pack_v4.py`, since v5 as checked files. Every file is read back against its source, and the whole set was loaded and checked on the Virtual Calculator. The pack began as Roger's wish: "I wish we could just load up a version of the Virtual Prime with the programs already loaded". Claude built and tested it with hp-prime-kit's tools.

**And for students: the [Prime Loader](../prime-loader/README.md)** (1 November 2026). This web page does the copying for them. A student picks a chapter and clicks Load; the page moves what was on the calculator to a backup and writes that chapter's programs into the folder. In Firefox, which never lets a page write into a folder, it walks the student through downloading one file and unpacking it there with Windows' Extract All (tried on Roger's computer: Extract All, pointed at the Prime folder, puts the files straight into it). Roger described it ("they start the launcher first, it clears the Prime/Virtual Prime, loads the chosen programs, and all the student has to do is start the calculator"); Claude designed and wrote it.

---

## 2. Data: one matrix file instead of typing

**What HP describes.** *A Fluorescent Light Experiment* (GT Springer, HP Educational Solutions, 2016; [hpcalc.org](https://www.hpcalc.org/details/7907)) works through an example:

- copy NOAA's Mauna Loa CO₂ annual means from a web page into Excel;
- copy two columns;
- paste them into the Virtual Calculator's Statistics 2Var app (C1(1) selected, then the calculator window's **Edit → Paste**).

The app is then saved under its own name and sent to the class, wirelessly or by cable. It is a good route for a few columns of numbers. *We have not yet tried it ourselves.*

**The new route.**

1. Open the **[HP Prime Data Loader](../data-loader/README.md)**, one web page that works offline, and paste columns from Excel, SPSS or a CSV file (or open the file).
2. The page shows each column, codes text columns as 1, 2, 3 … (alphabetical, with the codes on screen) and marks blank cells. It then downloads the calculator's own matrix file, `M1.hpmat` (or M0–M9).
3. Copy that file into the calculator's folder as in part 1, with the calculator closed.
4. Run **DataLoad**. It puts each column, or each group's scores, into the Statistics lists D1–D9 (or C1–C9) that the other programs read, leaves out the blanks, and draws a box plot of each list.

**What we found** (31 October 2026: [data-loader/README.md](../data-loader/README.md), [DataLoad_beta1_NOTES.md](changes/DataLoad_beta1_NOTES.md)):

- **The Rossi re-arrest data, 432 rows × 5 columns, loaded whole.** DataLoad's summaries matched Python's. TTestLab, reading the lists DataLoad filled, matched SciPy: t(421.19) = −1.68, p = 0.094.
- **A 10 × 3 matrix with text codes, an `NA` and a short column** loaded as it should.
- **The calculator accepts the file as written.** Its own matrix files carry a different type word in the header (`14 9B`, against the kit's `14 80`). It read the kit's form, and kept it, with every cell, when it rewrote M1 on exit.
- **Open the Statistics 1Var app once before the first load:** its lists do not exist until then.
- **Lists left from an earlier load are read as data** by AnovaLab, RankLab and AgreeLab. DataLoad offers to clear them.
- **Not yet tried on a G1 or G2.** There, the matrix file would go through the Connectivity Kit.

**Who found what.**

- **The format is hp-prime-kit's work.** The `.hpmat` format is documented there (a 16-byte header, then one twelve-digit BCD number per cell), and its `matrix write` command writes one. The page's encoder was checked against the kit's on 20,011 numbers, and on the Rossi file byte for byte.
- **The idea was Roger's:** "maybe we could make some sort of 'data loader' to copy a dataset and then put it in a format to paste to the Prime folder."
- **The route is new, and it is Claude's.** The Data Loader page, its text codes and blank marker, and DataLoad, which splits the matrix into Statistics lists by column or by group, were designed and written by **Claude (Anthropic; Claude Opus 5.5)** on 31 October 2026. Claude also tested them on the Virtual Calculator.
- **We have not found it described anywhere else:** not in HP's documents, the hpcalc.org Prime archive, the GitHub projects we collected, or the forum threads we read. If you know of earlier work, please tell us in [GitHub issues](https://github.com/metcalfdds/hp-prime-statistics/issues) and we will credit it.

---

## Sources

- hp-prime-kit, `docs/topics/deploy.md` ("The emulator's folder really is a mailbox"; "A program that arrives as a file has to be compiled once") and its `.hpmat` notes: [github.com/JordiRigau/hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit).
- abaccin, hpprime-stoichiometry, `deploy.ps1`: [github.com/abaccin/hpprime-stoichiometry](https://github.com/abaccin/hpprime-stoichiometry).
- Rudicito, HP-DOOM, `copy-to-emulator.sh`: [github.com/Rudicito/HP-DOOM](https://github.com/Rudicito/HP-DOOM).
- HP Calculators, *HP Prime Advanced Workshop*, version 1.0, 2014, page 22; *HP Prime APSI 2015 Webinar: Programming in HP PPL*, version 1.2, 2015, page 11.
- GT Springer, *A Fluorescent Light Experiment*, version 1.0, HP Educational Solutions, 2016, pages 4–6: [hpcalc.org/details/7907](https://www.hpcalc.org/details/7907).
- "how to copy a Default program to my PC?", HP Museum forum, 31 January 2014: [hpmuseum.org/forum/post-4070.html](https://www.hpmuseum.org/forum/post-4070.html).

*Free for educational and personal use. © 2026 Roger Metcalf. Written with AI assistance (Anthropic Claude).*
