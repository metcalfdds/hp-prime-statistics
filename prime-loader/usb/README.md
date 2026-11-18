# A real HP Prime on its USB cable, from a web page

**Status, 18 November 2026, 18:00.** The Prime Loader's own cable code has run on the author's G2 and G1, and its logs are in `logs/` (the eight of 18 November; the table below). **What works:** a group of programs goes down the cable in seconds, every download verified, on both calculators; and "making room" takes the book's other programs off both (after Advanced 1 went to the G1, its Program Catalog held only the three). **What does not, yet:** a verified program does not always RUN. On the G2, two of four programs opened the editor at Run and ran after a Check; on the G1, EpiStats, with two programs sent behind it, reset the calculator at Run, and sent alone it ran. The last program of a send has always run ("What ran afterwards", below). Why is not known. So `prime_usb_v3b.js` now rests the calculator after each program, and the Loader (`../PrimeLoader_v2h.html`) sends EpiStats in a group of its own, asks for a restart first, and says to unplug the cable when the programs are on, because the G1 was very slow on its cable. **Not yet seen on a calculator:** v2h and the rest; whether the rest cures the Check is not known until one has run it. All 30 programs at once did not go on either calculator (the G1 full after 15, the G2 stopped at the 14th), which is why there are groups. The Connectivity Kit's steps stay on the page as way 2), "The official HP way".

**Before that, 17 November 2026, late.** The author's G2 and his G1 took test programs of every size the book has straight down their cables from a test page, with no Connectivity Kit, by one route, and each one the test page read back was the same: every size on the G2, and up to 140,000 characters on the G1, whose largest (289,813 characters, the size of EpiStats) went in and was acknowledged and was not read back, because the page stopped waiting too soon (the table below).

## What the calculators did with the Loader (the eight logs of 18 November 2026)

All on firmware build 15751; the first four with Loader v2d (whose cable code is `prime_usb_v3.js`), the next two with the first build of v2f (`prime_usb_v3a.js`, longer wait), the last two with v2g (`prime_usb_v3a.js`: groups, and making room).

| Log | Calculator, browser | Sent | What happened |
|---|---|---|---|
| `PrimeLoader_v2d_G2_Chrome_2026-11-18_1532.txt` | G2, Chrome | Chapter 12: ChiTable, FitCheck, TestChooser (441,568 characters) | All three verified. 1,037 reports there and back, 4.6 s. No "send again". Each verify took 0.6, 1.3 and 0.4 s. ChiTable then ran at once from the Program Catalog (Roger: "program started right up!"). |
| `PrimeLoader_v2d_G1_Edge_2026-11-18_1535.txt` | G1, Edge | Chapter 12 | All three verified. 16,778 reports, 10.2 s. No "send again". The G1 sent each answer in runs of 240 reports and went on at each acknowledgement. |
| `PrimeLoader_v2d_G1_Chrome_2026-11-18_1541.txt` | G1, Chrome | All 30 | 15 verified (2,104,376 characters, 47 s). The 16th, NormExplorer, was acknowledged in full (5,899 reports, 77 acknowledgements) and came back as a file of 36 bytes: its head and its name, not compressed, and no text. The Program Catalog listed it at 0 KB, and showed 4.35 MB of programs. **A full calculator says nothing; it keeps the name.** |
| `PrimeLoader_v2d_G2_Chrome_2026-11-18_1550.txt` | G2, Chrome | All 30 | 9 verified. Each verify took longer as the load went on: 0.4 s (AgreeLab), 1.2, 0.6, 0.2, 3.2 (BurrLab), 4.4 (ChiTable, which had taken 0.6 s at 15:32), 3.4, 2.2 (DataLoad, 40,856 characters), 8.0 (DNAMixLR). EpiStats's answer had not begun when the page gave up at 14.6 s. From DataLoad on, a "send again" or two in most programs. |
| `PrimeLoader_v2f_G2_Chrome_2026-11-18_1604.txt` | G2, Chrome | All 30 | The G2 began this run still sending: pieces of BurrLab's answer from the run before, and "send again: report 02 of message 12" every half second, through the whole load. 9 verified among it; EpiStats stood at 539 of 567 reports. **A calculator left with an answer nobody took keeps offering it**, as the G1 did on 17 November. |
| `PrimeLoader_v2f_G2_Chrome_2026-11-18_1611.txt` | G2, Chrome, after off and on | All 30 | 13 verified, slower and slower: 0.4 s to verify the first, then 1.7, 1.1, 0.3, 2.8, 3.9, 3.3, 2.0, 7.5, 22 (EpiStats, which the longer wait let through), 9.9, 12, 22 (FitCheck). At the 14th, GaltonBoard, the G2 took one report, said "send again" for the second every half second, and took nothing more; the browser's write stood for 60 s. It was still on its cable. |
| `PrimeLoader_v2g_G2_Chrome_2026-11-18_1654.txt` | G2, Chrome | Chapters 1–3: DataLoad, NormExplorer, ScatterLab, TestChooser (422,732 characters) | 26 deletes sent, 0.3 s apart (8.2 s; the log prints the first 20, each acknowledged, and counts the rest). All four verified: 993 reports, 12.3 s; three times a report was sent again. All through the run the G2 said "send again: report 02 of message 28" (31 times in the log), a leftover of GaltonBoard at 16:11; the page's own message 28 was DataLoad. **Afterwards DataLoad and ScatterLab would not run** (Run opened the editor) until each was Checked; NormExplorer and TestChooser ran. |
| `PrimeLoader_v2g_G1_Edge_2026-11-18_1659.txt` | G1, Edge | Advanced 1 as v2g had it: EpiStats, ErrorRate, TrendTest (510,679 characters) | 27 deletes sent (8.5 s; the log prints the first 20, each acknowledged): the first deletes in the newer framing on a G1. All three verified: 19,298 reports, 20.3 s; the G1 took 3.95 s to begin EpiStats's answer. **Afterwards the Program Catalog held only the three** (Roger), so the deletes took. ErrorRate and TrendTest ran; **at Run on EpiStats the calculator reset.** |

### What ran afterwards

Every program here was verified, character for character. "Before the next" is the time from the last acknowledgement of the program to the first report of the next one, by the log.

| Calculator | Program | Characters | Before the next | From the Program Catalog |
|---|---|---|---|---|
| G2, 15:32 | ChiTable | 182,459 | 0.98 s | Ran ("program started right up!") |
| G2, 16:46 | DataLoad | 40,856 | 0.54 s | Run opened the editor; ran after Check |
| G2, 16:46 | NormExplorer | 185,782 | 0.98 s | Ran |
| G2, 16:46 | ScatterLab | 115,148 | 0.77 s | Run opened the editor; ran after Check |
| G2, 16:46 | TestChooser | 80,946 | the last | Ran |
| G1, 16:59 | EpiStats | 289,813 | 4.84 s, of which the G1 spent 3.95 s compressing its answer to the page and 0.46 s sending it | The calculator reset at Run. After the reset it showed its list of two names and then opened the editor |
| G1, 16:59 | ErrorRate | 115,298 | 1.94 s | Ran |
| G1, 16:59 | TrendTest | 105,568 | the last | Ran |
| G1, 17:28 | EpiStats, sent alone | 289,813 | the last | Ran, with no Check (no log was saved) |

What this shows and what it does not: **the last program of a send has always run** (four of four), and a program with another close behind it sometimes has not (three of six). hp-prime-kit measured that a G2 compiles a program that arrives this way, on programs of up to 16,558 bytes sent one at a time (`usb.send-program`). The guess is that a program sent close behind stops that work. It is a guess: nothing here separates it from other causes, and the times alone do not order the cases (a G1 ran ErrorRate after 1.94 s and not EpiStats after 4.84 s). What `prime_usb_v3b.js` does about it is under "The Loader's cable route".

**On its cable the G1 was "very slow"; unplugged, it "went back to normal speed"** (Roger, 17:30 and 17:33, running EpiStats after the page had closed the device). On 29 October the G2 took 40 to 75% longer plugged into the Connectivity Kit (Lessons Learned §14 rule 20). So the page's first word when the programs are on is to unplug.

Neither calculator holds all 30 of the book's programs: the G1 filled at about 2.1 million characters, and the G2 stopped at about 1.9 million. Why the G2 slows as it fills is not known.


Roger, 17 November 2026: "we do need to make some sort of very simple loader to interface somehow with Connectivity Kit to get the programs on a physical calcuator", and then: "the calculator is connected to the computer somehow--do we need the Kit?" At 20:14, with the first log: "the program seems stuck". At 21:51, with the fifth: "took a while for the 140k and 289k characters". At 22:01: "maybe we shoould keep the instructions for the COnnectivity Kit as a backup".

The Virtual Calculator keeps its programs as files in a folder, which is why the [Prime Loader](../README.md) can load it with one click. A real HP Prime keeps its programs inside the calculator, and they travel down its USB cable. Until now that has meant HP's Connectivity Kit: start the Kit, plug the calculator in, and drag each file onto the calculator's name.

Chrome and Edge let a web page talk to a USB device of the HID class when the user picks the device from the browser's own list (WebHID). An HP Prime is such a device. So a page can send the programs itself.

## What the calculators did with the test pages (the five logs of 17 November 2026)

A G2 (`03F0:2441`, reports of 1,024 bytes) and a G1 (`03F0:1541`, reports of 64 bytes), both on firmware build 15751, from Chrome 157 and Edge 157 on Windows.

**The first test page** (`PrimeUSBTest_v1`; the G2 in Chrome at 20:05 and in Edge at 20:17, the G1 in Chrome at 20:27):

| What was tried | G2 | G1 |
|---|---|---|
| "Who are you" (`00 FA`) | answered: 108 bytes, **version 01** | the same |
| A program **not compressed** (`F7 01`), old framing, then asked for back with `F8 01` or `F8 03`, the name ending in a NUL | the same program came back at 1, 17 and 80 reports | at 10 reports |
| ... a longer one | **not kept** at 274 reports; the cable stood for 49 s on the way, the next request had no answer, and the ones after it brought back the program before | **not kept** at 263 reports, with no pause |
| A program **compressed** (`F7 03`), old framing, with or without the report `01` after it | **not kept** | the same |
| A delete (`EB 01`) | the program was there before and not after | the same |
| The newer framing (`FF EC`), then a compressed program in it | acknowledged, with position 1,015 after its one report; **not kept** | acknowledged, with position 370 after its six reports |

Then that page waited for an answer that did not come, and each repeated acknowledgement from the calculator started its wait again; when the G2 went off the cable the next write to it never came back.

**The second test page** (`PrimeUSBTest_v2`; the G2 in Chrome at 21:43, 80 s; the G1 in Chrome at 21:47, 220 s):

| What was tried | G2 | G1 |
|---|---|---|
| Old framing, not compressed: exactly 254 reports, then exactly 255 | both came back the same (the answer of 256 reports is numbered `00` to `FE` and then `00`) | the same |
| `FD 01 00 00 00 01 03` in the **old** framing | answered with the same seven bytes; from then on "who are you" says **version 03**, and a program comes back compressed (`F7 03`, a zlib stream that begins `78 01`) | the same |
| A program compressed by the browser (`F7 03`, a stream that begins `78 9C`), now that it speaks 03, in either framing | **not kept**; the person at the calculator did not find it in the list | the same |
| The newer framing (`FF EC`) | no report of its own in answer; "who are you" is then answered in the newer framing | the same |
| **Newer framing, not compressed (`F7 01`)**: 300; 8,269; 40,856 and 140,000 characters | each came back the same | each came back the same (the last in 4,445 reports) |
| ... 289,813 characters, the size of EpiStats, the book's largest | came back the same (567 reports, 4.3 s) | went in 9,201 reports and was acknowledged (80 s); the G1 then sent it back four times, a message of the G2's own length each time; the page had stopped waiting 0.1 s before each one began, and said "no answer" |
| A delete (`EB 03`) | the program was there before and not after | the same for a small program |
| The old framing, asked again after the newer | still answered, with version 03 | the same |

## The route that works

1. `00 FA`, "who are you", in the old framing. Both answer with version 01.
2. `00 FD 01 00 00 00 01 03`, in the old framing. Both answer the same seven bytes and speak version 03 from then on.
3. `FF EC 00 00 00 00 00 00`. Nothing comes back. The newer framing is open: a message's first report is `01`, the message's number and its size (four bytes each, low byte first) and then its first bytes; the reports after it are numbered `02` to `FD` and `02` again.
4. Each program as `F7 01`, **not compressed**, in the newer framing: `F7 01`, the length of what follows (four bytes, high byte first), `06`, the name's length in bytes, a two-byte checksum (CRC-16/XMODEM over the message without its last six bytes, the checksum's own bytes zero), the name and then the source, both UTF-16.
5. `F8 03` with the name ending in a NUL: the calculator sends the program back, compressed, and it must be the same text.

## What a calculator does on its own account

Each line is from the two logs of the second test, and `tests/mock_prime_v3b.js` does each by default.

- **It acknowledges every 77th report of a message as it arrives** (`FE 01`, the number of the report it wants next, `00`, the room of the reports it has, the message's number), and the whole message with the number of its last report. The room is 1,015 bytes for a G2's first report and 1,023 for each after; 55 and 63 for a G1.
- **It has a clock.** When the sender stops in the middle of a message, it says where it stands within 0.7 s: the report it wants next and the room of what it has. On the G2 the first such word in a message was a "send again" (`FE 00`), on the G1 an acknowledgement. While nothing is happening it repeats its last acknowledgement with `FF` for the report, every 0.6 s on the G2 and about every second on the G1.
- **The clock can speak while reports are on their way.** The G2 said "send again, report 02" just as the second report of its longest message went out, 0.6 s after its last acknowledgement, and then took that report. So a "send again" is not always a lost report.
- **A report out of turn is answered at once with "send again"**, naming the report it wants and what it has; the G2 said so once for each place it stood at.
- **When it sends, it stops once 240 reports' worth is unacknowledged** (241 reports of a G1 the first time, 240 each time after), and goes on when it is acknowledged with the number of the last report that came and the room of all that have come. A G1 took that acknowledgement after 240 reports and after 241.
- **It compresses a program before sending it back**, which takes time: 0.9 s on the G2 and 3.1 s on the G1 for 289,813 characters, 1.5 s on the G1 for 140,000.
- **A G1 whose answer was left unacknowledged after 241 reports answered nothing more in the newer framing.** Asked "who are you" in the old framing, it sent the remaining 1,862 reports of that answer numbered in the old way (`F2` ... `FE`, `00`, `01` ...) and then answered.

## What did not work, and what the pages got wrong

- **A compressed program is not kept**, in either framing, whether the calculator speaks 01 or 03. hp-prime-kit's G2 (firmware 2.4.15515) kept one compressed by zlib at level 1, whose stream begins `78 01`; the browser's begins `78 9C`. Whether that is why is not known. Nothing that loads a calculator here compresses.
- **The old framing ends at 255 reports.** Not compressed, 20 of the book's 31 programs fit that on a G2 and 11 do not; none fits a G1 (`tests/test_usb_core_v3b.js`, A14).
- The first page **waited without end** (above). Since then every wait is counted once from when it starts, and the browser's `disconnect` ends them all.
- The second page **stopped after 76 reports** where the calculator acknowledges the 77th, so each 77 reports cost the 0.7 s after which the calculator's clock spoke: 80 s for the G1's largest program.
- It **gave a G1 3.0 s** to begin an answer that took 3.1.
- It **went back at every "send again"**, and so, after the G2's clock spoke, sent seven reports a second time, each of which brought the next "send again".
- It **threw away what was waiting** before a request, which is how the G1's answer came to stand unacknowledged.

`prime_usb_v3b.js` sends 77 reports and waits for the acknowledgement; allows an answer 3 s and 0.04 ms a character to begin (14.6 s for EpiStats); at a "send again" sends ONE report again and listens to what the calculator says to it; and before each request takes any answer that is waiting to its end and acknowledges it.

## What is known from others, and from whom

Four projects, each under the MIT licence, worked out what travels on the cable and published it. The code in this folder is written from what they measured and read, and from the logs above. None of their code is here.

| Source | What it holds | On what |
|---|---|---|
| [hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit) (Jordi Rigau), `docs/topics/usb.md`, `hpkit/usb.py` | The device. The old framing. A program sent as `F7 03` with its source compressed, and a report `01` after it, **kept**: up to 16,558 bytes in six reports. Its calculator answered "who are you" with **version 03**. The opening of the newer framing. | One G2, firmware 2.4.15515, from Windows, 3 to 5 Nov 2026, between sessions of the Connectivity Kit |
| [hp-prime-web](https://github.com/APie357/hp-prime-web) (APie357), `docs/PROTOCOL.md` | A program sent as `F7 01`, not compressed. A program read back with `F8 01` when the name ends in a NUL. A delete, `EB 01`. | One G2, 9 and 10 Nov 2026 |
| [PrimeDev](https://github.com/BeatSkip/PrimeDev) (Oscar Spierings), `PrimeWeb/Frames`, `PrimeWeb/Utility/MessageUtils.cs` | The newer framing: message numbers, acknowledgements. The bytes `FD 01 00 00 00 01 03`, as message 1 of a session, under a command it names "max protocol version". | Its code is written for a G2; what it was tried on is not in what we read |
| [hp-prime-emulator](https://github.com/golba98/hp-prime-emulator) (golba98), `docs/reverse-engineering`, `docs/device` | A reading, as data, of HP's Connectivity Kit 2.4.2 r15751: the Kit asks `00 FA` and sends `FF EC`; a message's reports are numbered `01`, then `02` to `FD` and `02` again; a window of 76; a retry after 500 ms. Its own G1 kept a program of 15,926 bytes in the old framing and not one of 16,284. | The Kit's program file, not run; one G1, firmware build 15157 |

## What is not known yet

- **Why a verified program sometimes will not run until it is Checked, and whether a rest after each program cures it** ("What ran afterwards", above). v3b's rest is chosen, not measured. Until a calculator has run it, the page keeps its line about Check.
- **Why the G1 reset at Run on EpiStats.** It had ErrorRate and TrendTest sent behind it. Sent alone, it ran.
- **Whether the G2 took the deletes.** They were acknowledged; nobody has yet looked at its Program Catalog after a group. (On the G1 the catalog held only the group: the deletes in the newer framing work there.)
- **Whether a calculator still saying "send again" for an old message does harm.** The G2 did so all through the 16:46 run, for message 28 of 16:11, and the page's message numbers start at 1 each time, so its own message 28 (DataLoad) met it. Every download verified all the same. A restart before loading (the page's first step now) should clear it; that has not been watched.
- **Whether deletes can go faster than 0.3 s apart.** Nothing shorter has been tried; 26 of them are 8 s of a load.
- **Why the G2 answers later as it fills, and what it does when it has no room.** It stopped taking reports; it did not keep an empty program as the G1 did.
- **Whether a calculator that was left with an answer nobody took can be set right from the page.** On 18 November it took switching the G2 off and on.
- **Whether the 0.4 s between a program's last acknowledgement and the request for it back can be shorter.** No shorter gap has been tried.
- **Other firmware.** Both calculators are on build 15751. A calculator that still says version 01 after the `FD` is sent nothing, and the page points to the Kit.
- **An app and a data file.** CentralLimit is three files in a folder, and a matrix is not a program; nobody reports sending either this way. They stay with the Kit.
- **A calculator left in the middle of a message** by a page that was closed while sending. The Loader stops only between two programs, and asks before the page is left while it is sending.
- **The G2 when it sends more than 240 reports' worth.** None of the book's programs is that long compressed (EpiStats came back in 130 reports).
- **The Connectivity Kit open at the same time.** The page says to close it.

## The files

| File | What it is |
|---|---|
| `prime_usb_v3b.js` | What travels on the cable: the messages, the two framings, a `Link` that opens a session (`begin`), sends a program, reads one back and deletes one; `load`, which puts a list of programs on a calculator and reads each back; `Tracer`, which writes the reports that pass as lines of a log; and `HidPort`, which wraps the browser's WebHID device. Each fact is marked with its source, the logs among them. No DOM. |
| `logs/` | What the two test pages wrote on the author's G2 and G1, 17 Nov 2026: three logs of the first, two of the second. No serial number is in them. |
| `tests/mock_prime_v3b.js` | A pretend calculator, written apart from `prime_usb_v3b.js`. By default it does what the two calculators did; what the logs do not show has a switch. |
| `tests/kit_reference_v1.py` | Writes hp-prime-kit's own message for every program in `programs/`, for the next test to compare with. |
| `tests/test_usb_core_v3b.js` | The messages against hp-prime-kit's, byte for byte, and against hp-prime-web's published byte examples; the numbers in the logs; a `Link` and a `load` against the mock; that no wait is without an end; all the book's programs onto a pretend G1 and a pretend G2; the log. |
| `tests/vc_2026-11-17/` | The test programs on the Virtual Calculator (below). |

The two test pages, their ladders, the first two versions of this code and their tests are in the repository's history: the first at commit `819489a`, the second at `0ca5146`.

## The Loader's cable route

`../PrimeLoader_v2h.html` shows it to every student in a browser that has WebHID, for "A real HP Prime". There the step is called "Two ways to load *Statisticles* onto a physical Prime G1 or G2 calculator", and its two ways are "1) The *Statisticles* way: straight down the USB cable" and "2) The official HP way: the Connectivity Kit", whose steps are folded below the first (Roger's names, 18 November 2026; [../README.md](../README.md) has his words and the sentence the page puts under the title).

- **A restart first, if the student can** (Roger, 18 November: "if possible, they should do a paperclip reset first before anything else"): the Reset button in the hole on the back, with a paper clip; or off and on.
- **A group first.** Step 2 offers eight groups of programs, none over about 1.2 million characters; Advanced 1 is EpiStats alone. **Making room:** before the group goes, the page sends a delete (`EB`, the name, no answer) for each of the book's programs that is not in it, 0.3 s apart. It never names a program that is not the book's.
- **Send to the calculator** asks the browser for the calculator (its small window, the first time), opens the session as above, and sends each program of the choice, then verifies the download: it asks for the program back and compares. A program counts as loaded only when the two are the same; the first that is not ends the load, and the page says which programs are on the calculator and what to do. It gives the calculator 30 s and 0.1 ms a character to begin its answer (59 s for EpiStats), since the G2 took 22 s over one.
- **A rest after each program** (v3b): once a download is verified, the page leaves the calculator alone before it sends the next program, for 2 s and 0.5 s more for each 100,000 characters on a G2, or 2 s more on a G1 (`lullFor`: 2.9 s after NormExplorer on a G2, 4.3 s after ErrorRate on a G1). The numbers are chosen, not measured. The page says "Giving the calculator 3 seconds to get NormExplorer ready", and the log says what each program was given. Stop works during a rest.
- **When the programs are on,** the first step is to unplug the cable; then the Program Catalog, Run, and what to do if Run opens the program's text (Check).
- **A program that comes back empty** is "full": the calculator had no room and kept the name. **A report that stands for a minute** with no "disconnect" from the browser is "stopped responding".
- Programs ticked one by one are added, and nothing is taken off for them.
- CentralLimit and data files are named as not travelling this way, and the Kit's steps open for them.
- **Stop** takes effect between two programs.
- **What passed on the cable** is the log: the page's version, the browser, the calculator's model and report size, the choice, what each step did, and a line for each report that starts a message, acknowledges or controls, with the first twelve bytes of a message at most; the reports that carry a message on are counted. After forty ordinary lines in one step the rest are counted and left out; a "send again" is always written; and when a load fails, the last thirty lines that were left out are written after the failure. **Save the details** writes it to a file. It does not hold the calculator's serial number: the code never reads it, and it lies in the last sixteen of the 108 bytes of the answer to "who are you", of which the log shows six.

Against the mock, with a calculator's own delays before an answer begins, the 30 programs took 58 s on a pretend G1 and 26 s on a pretend G2 (17 Nov 2026, 22:50; the mock takes a report at once, which a calculator does not).

## The test programs on the Virtual Calculator (17 November 2026)

The smallest and the largest of the first test's programs (`ZZUSBA`, 300 characters, and `ZZUSBD`, 289,813) were built as `.hpprgm` files with hp-prime-kit and put in the folder of the Virtual Calculator 2.4.2 (build 2026-09-09) in the cloud workspace, 19:49 to 19:53:

- The Program Catalog listed ZZUSBA at 2 KB and ZZUSBD at 567 KB.
- Edit took 16 seconds to open ZZUSBD, and Check said "No errors in the program" (`tests/vc_2026-11-17/ZZUSBD_check.png`).
- Run showed a small box, "ZZUSBA 1" for the one and "ZZUSBD 5" for the other (`ZZUSBA_run_box.png`, `ZZUSBD_run_box.png`).

This says the test programs are programs to HP's own compiler, the largest included. It says nothing about the cable.

## Tests (18 November 2026; all against the mock)

```
python3 tests/kit_reference_v1.py REF          # hp-prime-kit's messages, into a scratch folder
node tests/test_usb_core_v3b.js REF             # 93 PASS, 0 FAIL   (about two minutes)
node ../tests/test_loader_v2h.js ../PrimeLoader_v2h.html ../../starter-pack/HP_Prime_Statistics_Starter_Pack_v23.zip     # the cable is its part 13
```

What a pass means: the messages are the ones hp-prime-kit builds, byte for byte, for all 31 programs, and the ones hp-prime-web's tests expect; the requests and the deletes begin with the bytes the two calculators answered; the positions and the reports' numbers are the ones in the logs; the code and the mock, which were written apart, agree on the route; the calculator's clock speaking in the middle of a message, a report lost on the way, an answer that takes 3.3 s to begin, an answer left standing and a calculator left standing by an earlier page are each survived; no wait is without an end; and every one of the book's programs goes onto a pretend G1 (131,683 reports for the 31 texts in `programs/`; 127,913 for the 30 that the Loader sends, CentralLimit being an app) and a pretend G2 (8,125; 7,892) and comes back the same. What a pass does not mean: that a calculator agrees. The mock is the two calculators as far as five logs go.
