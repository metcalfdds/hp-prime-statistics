# A real HP Prime on its USB cable, from a web page

**Status, 17 November 2026, night.** The first test page ran on the author's G2 and his G1 that evening. A program sent **not compressed** went down the cable and came back the same, on both. A program sent **compressed** was not kept by either. The page then stood still, which was its own fault. The second test page, `PrimeUSBTest_v2.html`, cannot stand still, and asks what the first run left open; **it has not run on a calculator yet.**

Roger, 17 November 2026: "we do need to make some sort of very simple loader to interface somehow with Connectivity Kit to get the programs on a physical calcuator", and then: "the calculator is connected to the computer somehow--do we need the Kit?" And at 20:14, with the first log: "the program seems stuck".

The Virtual Calculator keeps its programs as files in a folder, which is why the [Prime Loader](../README.md) can load it with one click. A real HP Prime keeps its programs inside the calculator, and they travel down its USB cable. Until now that has meant HP's Connectivity Kit: start the Kit, plug the calculator in, and drag each file onto the calculator's name. That route works for a G1 and a G2 and stays on the Loader page.

Chrome and Edge let a web page talk to a USB device of the HID class when the user picks the device from the browser's own list (WebHID). An HP Prime is such a device. So a page could send the programs itself. This folder is that attempt.

## What the calculators did (the three logs in `logs/`)

A G2 (`03F0:2441`, reports of 1,024 bytes) and a G1 (`03F0:1541`, reports of 64 bytes), both on firmware build 15751, from Chrome 157 and Edge 157 on Windows, with `PrimeUSBTest_v1.html`. The two runs on the G2, one in each browser, agree step for step.

| What was tried | G2 | G1 |
|---|---|---|
| "Who are you" (`00 FA`) | answered: 108 bytes, **version 01** | the same |
| A program **not compressed** (`F7 01`), old framing, then asked for back with `F8 01` or `F8 03`, the name ending in a NUL | the same program came back at 1, 17 and 80 reports | at 10 reports |
| ... a longer one | **not kept** at 274 reports; the cable stood for 49 s on the way, the next request had no answer, and the ones after it brought back the program before | **not kept** at 263 reports, with no pause |
| A program **compressed** (`F7 03`), old framing, with or without the report `01` after it | **not kept**: none of four requests brought it back | the same |
| A delete (`EB 01`) | the program was there before and not after | the same |
| The newer framing (`FF EC`), then a compressed program in it | the message was acknowledged, with position 1,015 after its one report; **not kept** (the calculator's list was empty afterwards) | acknowledged, with position 370 after its six reports |
| A request for a file, asked a second way at once | | the G1 sent the same file several times: six copies for two requests |

Then the page waited for an answer that did not come. Each repeated acknowledgement from the calculator started its wait again, so the wait had no end; and when the G2 went off the cable, three and a half minutes into the first run, the next write to it never came back (`logs/..._G2_Chrome_...`, its last two lines). What made the G2 go is not known. An HP Prime switches itself off after about five minutes without a key, and how long before the test its last key was pressed is not recorded; the second page asks for a key just before it starts and again half way.

**What follows from it.** An acknowledgement's position is the room of the reports taken, not the message's length (1,015 = 1,024 − 9; 370 = 55 + 5 × 63). The old framing stops somewhere above 80 reports on a G2 and 10 on a G1; hp-prime-emulator's own G1 kept 254 reports and not 259, so the reading here is 255, the most there are before the reports' numbers start again. At 255 reports, not compressed, **20 of the book's 31 programs fit a G2 and 11 do not** (AnovaLab, BayesTree, BurrLab, ChiTable, DNAMixLR, EpiStats, FitCheck, NormExplorer, PowerViz, RankLab, StatDist), RiskLab fits with one report to spare (254), and **none fits a G1**, whose smallest, DataLoad, would be 1,298 reports (`tests/test_usb_core_v2.js`, check A14 and the line before it). So a G1 needs another route for every program, and a G2 for eleven.

## What is known from others, and from whom

Four projects, each under the MIT licence, worked out what travels on the cable and published it. The code in this folder is written from what they measured and read, and from the logs above. None of their code is here.

| Source | What it holds | On what |
|---|---|---|
| [hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit) (Jordi Rigau), `docs/topics/usb.md`, `hpkit/usb.py` | The device. The old framing. A program sent as `F7 03` with its source compressed, and a report `01` after it, **kept**: up to 16,558 bytes in six reports. Its calculator answered "who are you" with **version 03**. The opening of the newer framing, whose acknowledgements repeat about every 0.5 s. | One G2, firmware 2.4.15515, from Windows, 3 to 5 Nov 2026, between sessions of the Connectivity Kit |
| [hp-prime-web](https://github.com/APie357/hp-prime-web) (APie357), `docs/PROTOCOL.md` | A program sent as `F7 01`, not compressed. A program read back with `F8 01` when the name ends in a NUL. A delete, `EB 01`. | One G2, 9 and 10 Nov 2026 |
| [PrimeDev](https://github.com/BeatSkip/PrimeDev) (Oscar Spierings), `PrimeWeb/Frames`, `PrimeWeb/Utility/MessageUtils.cs` | The newer framing: message numbers, acknowledgements. The bytes `FD 01 00 00 00 01 03`, as message 1 of a session, under a command it names "max protocol version". | Its code is written for a G2; what it was tried on is not in what we read |
| [hp-prime-emulator](https://github.com/golba98/hp-prime-emulator) (golba98), `docs/reverse-engineering`, `docs/device` | A reading, as data, of HP's Connectivity Kit 2.4.2 r15751: the Kit asks `00 FA`, sends `FF EC`, and the calculator's answer chooses a mode; in the first mode a message's reports are numbered `01`, then `02` to `FD` and `02` again, at most 76 go ahead of an acknowledgement, and there is a retry after 500 ms. Its own G1 kept a program of 15,926 bytes in the old framing and not one of 16,284. | The Kit's program file, not run; one G1, firmware build 15157 |

## What is not known, and what the second test asks

- **Whether a calculator keeps a compressed program once it has been told the page speaks version 03.** hp-prime-kit's G2 answered 03 and kept one; ours answer 01 and do not. PrimeDev holds the bytes of a message that would say so. Nobody has written down what a calculator does with them. This is the question the rest hangs on: compressed, every one of the 31 programs is 17 to 101 reports of a G2.
- **Whether the newer framing carries a long program**, compressed or not. Its reports' numbers go round, so nothing in it stops at 255. What a calculator does at the Kit's window of 76 reports, and what it wants from the other side when it is the one sending, is not written down either.
- **Where exactly the old framing stops**: 254 reports, 255, or fewer.
- **Whether the old framing is still answered once the newer one has been asked for**, and whether, with the version raised there, the old framing then keeps a compressed program, as it did for hp-prime-kit.
- **An app.** CentralLimit is three files in a folder, and nobody reports sending an app this way. It stays with the Kit.

## The files

| File | What it is |
|---|---|
| `prime_usb_v2.js` | What travels on the cable: the messages, the two framings, a `Link` that sends a program, reads one back and deletes one, and `HidPort`, which wraps the browser's WebHID device. Each fact is marked with its source, the logs among them. Every wait has one end, and a calculator that goes off the cable ends them all. No DOM. |
| `usb_ladder_v2.js` | The second test: four routes, each from a program of a few lines up, each program read back; and the log of every report the calculator sends. No DOM. |
| `usb_test_template_v2.html`, `build_usb_test_v2.py` | The test page and its build. |
| `PrimeUSBTest_v2.html` | The built page: one file, which opens from a folder or from the web. |
| `logs/` | What the first page wrote on the author's G2 (Chrome, then Edge) and G1, 17 Nov 2026. |
| `tests/mock_prime_v2.js` | A pretend calculator, written apart from `prime_usb_v2.js`. By default it does what the two calculators did in the logs, and beyond them what the leading reading says; each "beyond" has a switch. |
| `tests/kit_reference_v1.py` | Writes hp-prime-kit's own message for every program in `programs/`, for the next test to compare with. |
| `tests/test_usb_core_v2.js` | The messages against hp-prime-kit's, byte for byte, and against hp-prime-web's published byte examples; the framing; a `Link` against the mock; and that no wait is without an end. |
| `tests/test_usb_ladder_v2.js` | The test against the mock with one switch thrown at a time: what the page will conclude on each such calculator. |
| `tests/test_usb_page_v2.js` | The built page in Chromium, with the mock in `navigator.hid`'s place. |
| `prime_usb_v1.js`, `tests/mock_prime_v1.js`, `tests/test_usb_core_v1.js` | The first version, kept for one reason: `PrimeLoader_v2a.html` is built with it and tested against it (below). They go when the Loader is built again. |

## The second test page

`PrimeUSBTest_v2.html` is for the author, or for an instructor with a calculator to spare. It is not for students.

1. Back the calculator up with the Connectivity Kit if it holds anything that would be missed. Then **close the Kit**: Windows gives the calculator to one program at a time.
2. Turn the calculator on, leave it at its Home screen, and plug it in.
3. Open the page in Edge or Chrome, click **Connect**, and pick the calculator in the browser's list.
4. Press the **Home** key on the calculator, and click **Run the test**. Two or three times the page asks something of the person at the calculator: whether a program is in its list, or only to press Home again.
5. Click **Save the log** and send the log.

| Route | How the program is sent | What the first run found |
|---|---|---|
| C | not compressed (`F7 01`), old framing: a few lines, then exactly 254 reports, then exactly 255 | kept up to 80 reports of the G2 and 10 of the G1 |
| A | compressed (`F7 03`), old framing, after telling the calculator `FD 01 00 00 00 01 03` | not kept (with no `FD`) |
| E | not compressed, in the newer framing (`FF EC`) | not tried |
| D | compressed, in the newer framing, after the same `FD`, and after PrimeDev's other form of it, `FD 03`, if that does nothing | not kept (with no `FD`) |

Each of A, E and D begins with a program of 300 characters; one that is kept climbs through 8,269 characters (the largest program hp-prime-kit sent), 40,856 (the size of DataLoad, our smallest), 140,000, and 289,813 (the size of EpiStats, our largest). In the newer framing the sizes climb compressed if the compressed program was kept, and not compressed otherwise. In the old framing nothing is sent that needs more reports than a message has been kept at, because the calculator's answer to one report too many was to hold the cable for 49 s. At the very end, with the newer framing open, the old one is asked once more, and A is tried in it again: with the version raised that is hp-prime-kit's own case, and with it not raised the short `FD` is tried there, last, where nothing that follows depends on what it does.

On the calculator the test writes four programs at most, `ZZUSBC`, `ZZUSBA`, `ZZUSBE` and `ZZUSBD`, and deletes them at the end. Each is comment lines and one function that returns a number. The function comes last, so a program cut short on the way does not compile. A delete counts as done only when a request for the program has no answer on a calculator that still says who it is.

**The log** holds, besides what the test did, a line for every report that starts a message, acknowledges or controls, in either direction, with the first twelve bytes at most of a message and six of an answer to "who are you"; reports that carry a message on are counted, with their numbers. So if the reading of `FD` is wrong, the log shows what the calculator did instead. It does not hold the calculator's serial number: the code never reads it, and it lies in the last sixteen of that answer's 108 bytes (`tests/test_usb_core_v2.js`, checks E1 to E3).

## The test programs on the Virtual Calculator (17 November 2026)

The cable is not there to be tried without a calculator, but the test programs are. The smallest and the largest of the first test's programs (`ZZUSBA`, 300 characters, and `ZZUSBD`, 289,813) were built as `.hpprgm` files with hp-prime-kit and put in the folder of the Virtual Calculator 2.4.2 (build 2026-09-09) in the cloud workspace, 19:49 to 19:53:

- The Program Catalog listed ZZUSBA at 2 KB and ZZUSBD at 567 KB.
- Edit took 16 seconds to open ZZUSBD, and Check said "No errors in the program" (`tests/vc_2026-11-17/ZZUSBD_check.png`).
- Run showed a small box, "ZZUSBA 1" for the one and "ZZUSBD 5" for the other (`ZZUSBA_run_box.png`, `ZZUSBD_run_box.png`).

The second test's programs are made the same way and differ in their first line and in the number they return. This says the test programs are programs to HP's own compiler, the largest included. It says nothing about the cable.

## Tests (17 November 2026, night; all against the mock)

```
python3 tests/kit_reference_v1.py REF          # hp-prime-kit's messages, into a scratch folder
node tests/test_usb_core_v2.js REF             # 69 PASS, 0 FAIL
node tests/test_usb_ladder_v2.js               # 44 PASS, 0 FAIL   (about three minutes)
node tests/test_usb_page_v2.js PrimeUSBTest_v2.html     # 34 PASS, 0 FAIL   (about a minute)
```

What a pass means: the messages are the ones hp-prime-kit builds, byte for byte, for all 31 programs, and the ones hp-prime-web's tests expect; the page and the mock, which were written apart, agree; each way the mock can differ or fail is seen and named; and the three things that stopped the first page cannot stop this one (`test_usb_core_v2.js`, checks D1 to D8, and `test_usb_page_v2.js`, U3: a calculator that repeats its acknowledgements while no answer comes, one that goes off the cable, and a write that never comes back). What a pass does not mean: that a calculator agrees. The mock's default is the two calculators as far as three logs go; the rest of it is a reading.

At its real waits the page took 28 s on the mock of a G2 and 48 s to 141 s on mocks of a G1, the longest being a G1 that takes no `FD` and acknowledges on a clock, so that EpiStats's size goes not compressed in 9,201 reports (measured in Chromium, 17 Nov 2026, 21:20 to 21:30; the person's answers were clicked at once).

## The Loader's own USB route

`PrimeLoader_v2a.html` holds a "send straight down the cable" panel for a real HP Prime. It is switched off: it shows only at the page's test address, which ends `?usb=1`. **It sends each program compressed in the old framing, which is the way the logs show neither calculator keeps**, so as it stands it would stop at its first program and say so. It is built with `prime_usb_v1.js` and has not been changed, because what it should send instead is what the second test is for. It will be built again, on the version of this code that the calculators' answers leave standing, and switched on for students only when that has loaded a chapter that then ran.
