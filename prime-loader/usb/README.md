# A real HP Prime on its USB cable, from a web page

**Status, 17 November 2026, late.** That evening the author's G2 and his G1 took test programs of every size the book has straight down their cables from a test page, with no Connectivity Kit, by one route, and each program came back from the calculator the same. That route is now in the Prime Loader (`../PrimeLoader_v2b.html`), behind its test address, which ends `?usb=1`. **The Loader's own cable code has not run on a calculator yet**: it paces its sending differently from the test page, and it has never carried one of the book's programs. Until it has put a chapter on a G2 and on a G1, and a program of that chapter has run, students see only the Connectivity Kit's steps, and those steps stay on the page after that as the second way.

Roger, 17 November 2026: "we do need to make some sort of very simple loader to interface somehow with Connectivity Kit to get the programs on a physical calcuator", and then: "the calculator is connected to the computer somehow--do we need the Kit?" At 20:14, with the first log: "the program seems stuck". At 21:51, with the fifth: "took a while for the 140k and 289k characters". At 22:01: "maybe we shoould keep the instructions for the COnnectivity Kit as a backup".

The Virtual Calculator keeps its programs as files in a folder, which is why the [Prime Loader](../README.md) can load it with one click. A real HP Prime keeps its programs inside the calculator, and they travel down its USB cable. Until now that has meant HP's Connectivity Kit: start the Kit, plug the calculator in, and drag each file onto the calculator's name.

Chrome and Edge let a web page talk to a USB device of the HID class when the user picks the device from the browser's own list (WebHID). An HP Prime is such a device. So a page can send the programs itself.

## What the calculators did (the five logs in `logs/`)

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

Each line is from the two logs of the second test, and `tests/mock_prime_v3.js` does each by default.

- **It acknowledges every 77th report of a message as it arrives** (`FE 01`, the number of the report it wants next, `00`, the room of the reports it has, the message's number), and the whole message with the number of its last report. The room is 1,015 bytes for a G2's first report and 1,023 for each after; 55 and 63 for a G1.
- **It has a clock.** When the sender stops in the middle of a message, it says where it stands within 0.7 s: the report it wants next and the room of what it has. On the G2 the first such word in a message was a "send again" (`FE 00`), on the G1 an acknowledgement. While nothing is happening it repeats its last acknowledgement with `FF` for the report, every 0.6 s on the G2 and about every second on the G1.
- **The clock can speak while reports are on their way.** The G2 said "send again, report 02" just as the second report of its longest message went out, 0.6 s after its last acknowledgement, and then took that report. So a "send again" is not always a lost report.
- **A report out of turn is answered at once with "send again"**, naming the report it wants and what it has; the G2 said so once for each place it stood at.
- **When it sends, it stops once 240 reports' worth is unacknowledged** (241 reports of a G1 the first time, 240 each time after), and goes on when it is acknowledged with the number of the last report that came and the room of all that have come. A G1 took that acknowledgement after 240 reports and after 241.
- **It compresses a program before sending it back**, which takes time: 0.9 s on the G2 and 3.1 s on the G1 for 289,813 characters, 1.5 s on the G1 for 140,000.
- **A G1 whose answer was left unacknowledged after 241 reports answered nothing more in the newer framing.** Asked "who are you" in the old framing, it sent the remaining 1,862 reports of that answer numbered in the old way (`F2` ... `FE`, `00`, `01` ...) and then answered.

## What did not work, and what the pages got wrong

- **A compressed program is not kept**, in either framing, whether the calculator speaks 01 or 03. hp-prime-kit's G2 (firmware 2.4.15515) kept one compressed by zlib at level 1, whose stream begins `78 01`; the browser's begins `78 9C`. Whether that is why is not known. Nothing that loads a calculator here compresses.
- **The old framing ends at 255 reports.** Not compressed, 20 of the book's 31 programs fit that on a G2 and 11 do not; none fits a G1 (`tests/test_usb_core_v3.js`, A14).
- The first page **waited without end** (above). Since then every wait is counted once from when it starts, and the browser's `disconnect` ends them all.
- The second page **stopped after 76 reports** where the calculator acknowledges the 77th, so each 77 reports cost the 0.7 s after which the calculator's clock spoke: 80 s for the G1's largest program.
- It **gave a G1 3.0 s** to begin an answer that took 3.1.
- It **went back at every "send again"**, and so, after the G2's clock spoke, sent seven reports a second time, each of which brought the next "send again".
- It **threw away what was waiting** before a request, which is how the G1's answer came to stand unacknowledged.

`prime_usb_v3.js` sends 77 reports and waits for the acknowledgement; allows an answer 3 s and 0.04 ms a character to begin (14.6 s for EpiStats); at a "send again" sends ONE report again and listens to what the calculator says to it; and before each request takes any answer that is waiting to its end and acknowledges it.

## What is known from others, and from whom

Four projects, each under the MIT licence, worked out what travels on the cable and published it. The code in this folder is written from what they measured and read, and from the logs above. None of their code is here.

| Source | What it holds | On what |
|---|---|---|
| [hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit) (Jordi Rigau), `docs/topics/usb.md`, `hpkit/usb.py` | The device. The old framing. A program sent as `F7 03` with its source compressed, and a report `01` after it, **kept**: up to 16,558 bytes in six reports. Its calculator answered "who are you" with **version 03**. The opening of the newer framing. | One G2, firmware 2.4.15515, from Windows, 3 to 5 Nov 2026, between sessions of the Connectivity Kit |
| [hp-prime-web](https://github.com/APie357/hp-prime-web) (APie357), `docs/PROTOCOL.md` | A program sent as `F7 01`, not compressed. A program read back with `F8 01` when the name ends in a NUL. A delete, `EB 01`. | One G2, 9 and 10 Nov 2026 |
| [PrimeDev](https://github.com/BeatSkip/PrimeDev) (Oscar Spierings), `PrimeWeb/Frames`, `PrimeWeb/Utility/MessageUtils.cs` | The newer framing: message numbers, acknowledgements. The bytes `FD 01 00 00 00 01 03`, as message 1 of a session, under a command it names "max protocol version". | Its code is written for a G2; what it was tried on is not in what we read |
| [hp-prime-emulator](https://github.com/golba98/hp-prime-emulator) (golba98), `docs/reverse-engineering`, `docs/device` | A reading, as data, of HP's Connectivity Kit 2.4.2 r15751: the Kit asks `00 FA` and sends `FF EC`; a message's reports are numbered `01`, then `02` to `FD` and `02` again; a window of 76; a retry after 500 ms. Its own G1 kept a program of 15,926 bytes in the old framing and not one of 16,284. | The Kit's program file, not run; one G1, firmware build 15157 |

## What is not known yet

- **Whether the Loader's own sending works on a calculator**: 77 reports, the acknowledgement, 77 more, with no pause between. The calculators have been sent 77 reports at a time only with 0.7 s between.
- **Whether a program that arrives this way runs without a Check.** The Loader's last words say what to do if one does not.
- **Whether the 0.4 s between a program's last acknowledgement and the request for it back can be shorter.** It is 12 s of a load of 30 programs. No shorter gap has been tried.
- **Other firmware.** Both calculators are on build 15751. A calculator that still says version 01 after the `FD` is sent nothing, and the page points to the Kit.
- **An app and a data file.** CentralLimit is three files in a folder, and a matrix is not a program; nobody reports sending either this way. They stay with the Kit.
- **A calculator left in the middle of a message** by a page that was closed while sending. The Loader stops only between two programs, and asks before the page is left while it is sending.
- **The G2 when it sends more than 240 reports' worth.** None of the book's programs is that long compressed (EpiStats came back in 130 reports).
- **The Connectivity Kit open at the same time.** The page says to close it.

## The files

| File | What it is |
|---|---|
| `prime_usb_v3.js` | What travels on the cable: the messages, the two framings, a `Link` that opens a session (`begin`), sends a program, reads one back and deletes one; `load`, which puts a list of programs on a calculator and reads each back; `Tracer`, which writes the reports that pass as lines of a log; and `HidPort`, which wraps the browser's WebHID device. Each fact is marked with its source, the logs among them. No DOM. |
| `logs/` | What the two test pages wrote on the author's G2 and G1, 17 Nov 2026: three logs of the first, two of the second. No serial number is in them. |
| `tests/mock_prime_v3.js` | A pretend calculator, written apart from `prime_usb_v3.js`. By default it does what the two calculators did; what the logs do not show has a switch. |
| `tests/kit_reference_v1.py` | Writes hp-prime-kit's own message for every program in `programs/`, for the next test to compare with. |
| `tests/test_usb_core_v3.js` | The messages against hp-prime-kit's, byte for byte, and against hp-prime-web's published byte examples; the numbers in the logs; a `Link` and a `load` against the mock; that no wait is without an end; all the book's programs onto a pretend G1 and a pretend G2; the log. |
| `tests/vc_2026-11-17/` | The test programs on the Virtual Calculator (below). |

The two test pages, their ladders, the first two versions of this code and their tests are in the repository's history: the first at commit `819489a`, the second at `0ca5146`.

## The Loader's cable route

`../PrimeLoader_v2b.html` shows it only at the test address (`.../prime-loader/?usb=1`), in a browser that has WebHID, for "A real HP Prime". There it is the first way, and the Connectivity Kit's steps are the second, folded below it.

- **Send to the calculator** asks the browser for the calculator (its small window, the first time), opens the session as above, and sends each program of the choice, then asks for it back and compares. A program counts as loaded only when it came back the same; the first that does not ends the load, and the page says which programs are on the calculator and what to do.
- The programs are added. Nothing is deleted from a calculator.
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

## Tests (17 November 2026, late; all against the mock)

```
python3 tests/kit_reference_v1.py REF          # hp-prime-kit's messages, into a scratch folder
node tests/test_usb_core_v3.js REF             # 82 PASS, 0 FAIL   (about 25 s)
node ../tests/test_loader_v2b.js ../PrimeLoader_v2b.html ../../starter-pack/HP_Prime_Statistics_Starter_Pack_v23.zip     # the cable is its part 13
```

What a pass means: the messages are the ones hp-prime-kit builds, byte for byte, for all 31 programs, and the ones hp-prime-web's tests expect; the requests and the deletes begin with the bytes the two calculators answered; the positions and the reports' numbers are the ones in the logs; the code and the mock, which were written apart, agree on the route; the calculator's clock speaking in the middle of a message, a report lost on the way, an answer that takes 3.3 s to begin, an answer left standing and a calculator left standing by an earlier page are each survived; no wait is without an end; and every one of the book's programs goes onto a pretend G1 (131,683 reports for the 31 texts in `programs/`; 127,913 for the 30 that the Loader sends, CentralLimit being an app) and a pretend G2 (8,125; 7,892) and comes back the same. What a pass does not mean: that a calculator agrees. The mock is the two calculators as far as five logs go.
