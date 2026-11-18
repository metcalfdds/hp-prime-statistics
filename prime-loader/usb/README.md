# A real HP Prime on its USB cable, from a web page

**Status, 17 November 2026: written and tested against a pretend calculator. Nothing here has run on a real HP Prime.** The first run is the test page, `PrimeUSBTest_v1.html`, on the author's G2.

Roger, 17 November 2026: "we do need to make some sort of very simple loader to interface somehow with Connectivity Kit to get the programs on a physical calcuator", and then: "the calculator is connected to the computer somehow--do we need the Kit?"

The Virtual Calculator keeps its programs as files in a folder, which is why the [Prime Loader](../README.md) can load it with one click. A real HP Prime keeps its programs inside the calculator, and they travel down its USB cable. Until now that has meant HP's Connectivity Kit: start the Kit, plug the calculator in, and drag each file onto the calculator's name. That route works for a G1 and a G2 and stays on the Loader page.

Chrome and Edge let a web page talk to a USB device of the HID class when the user picks the device from the browser's own list (WebHID). An HP Prime is such a device. So a page could send the programs itself. This folder is that attempt.

## What is known, and from whom

Nobody here measured anything. Three projects, each under the MIT licence, worked out what travels on the cable and published it, and the code in this folder is written from what they measured. None of their code is here.

| Source | What it measured | On what |
|---|---|---|
| [hp-prime-kit](https://github.com/JordiRigau/hp-prime-kit) (Jordi Rigau), `docs/topics/usb.md`, `hpkit/usb.py` | The device (vendor `03F0`, product `2441`, reports of 1,024 bytes). The old framing. The information request. A program sent as `F7 03` with its source compressed, and a report `01` after it: 310 bytes in one report, up to 16,558 bytes in six. The opening of the newer framing. A request for a file (`F8 03`, no NUL after the name) was answered once and never again. | One G2, firmware 2.4.15515, from Windows, 3 to 5 Nov 2026 |
| [hp-prime-web](https://github.com/APie357/hp-prime-web) (APie357), `docs/PROTOCOL.md` | A program sent as `F7 01`, not compressed, "over 16 KB" accepted. A program read back with `F8 01` when the name ends in a NUL; without the NUL the calculator stays silent. A program deleted with `EB 01`. From others' tests of a G1: firmware dropped, without a word, uploads over about 15,928 bytes. | One G2 (it reports `V2.060.650`), 9 and 10 Nov 2026 |
| [PrimeDev](https://github.com/BeatSkip/PrimeDev) (Oscar Spierings), `PrimeWeb/Frames` | The newer framing that the Connectivity Kit itself uses on firmware build 10591 and later: message numbers, acknowledgements, at most 240 reports a message. | Its code is written for a G2; what it was tried on is not in what we read |

## What is not known

- **Whether any of it holds for a program the size of ours.** The largest program anybody reports sending is about 16,000 bytes. Ours are 40,856 to 289,813 characters. Compressed by a browser they are 17 to 101 reports each; not compressed they are 80 to 567 (`tests/test_usb_core_v1.js`, check A12 and the line after it).
- **Whether the calculator caps a message at about 253 reports.** The G1's 15,928 bytes comes to about 253 of its 64-byte reports (253 × 63 = 15,939 bytes, the message's head included). If a G2 caps a message at the same count, 253 reports of 1,023 bytes, a program of ours fits only when it is sent compressed. That is a reading of one number, not a measurement.
- **Which request reads a program back on a given firmware.** hp-prime-kit's G2 stopped answering; hp-prime-web's answers when the name ends in a NUL.
- **Anything about a G1.** Its reports are 64 bytes, and by the reading above none of our programs would fit one message of the old framing. The Connectivity Kit is the G1's route until somebody measures otherwise.
- **An app.** CentralLimit is three files in a folder, and nobody reports sending an app this way. It stays with the Kit.

## The files

| File | What it is |
|---|---|
| `prime_usb_v1.js` | What travels on the cable: the messages, the two framings, a `Link` that sends a program, reads one back and deletes one, and `HidPort`, which wraps the browser's WebHID device. Each fact is marked with its source. No DOM. |
| `usb_ladder_v1.js` | The test: test programs of five sizes, sent four ways, each read back. No DOM. |
| `usb_test_template_v1.html`, `build_usb_test_v1.py` | The test page and its build. |
| `PrimeUSBTest_v1.html` | The built page: one file, which opens from a folder or from the web. |
| `tests/mock_prime_v1.js` | A pretend calculator, written apart from `prime_usb_v1.js` from the same three descriptions. It has a switch for each way a real calculator may differ or fail. |
| `tests/kit_reference_v1.py` | Writes hp-prime-kit's own message for every program in `programs/`, for the next test to compare with. |
| `tests/test_usb_core_v1.js` | The messages against hp-prime-kit's, byte for byte, and against hp-prime-web's published byte examples; the framing; a `Link` against the mock. |
| `tests/test_usb_ladder_v1.js` | The ladder against the mock with one switch thrown at a time: what the test page will conclude on each such calculator. |
| `tests/test_usb_page_v1.js` | The built page in Chromium, with the mock in `navigator.hid`'s place. |

## The test page

`PrimeUSBTest_v1.html` is for the author, or for an instructor with a calculator to spare. It is not for students.

1. Back the calculator up with the Connectivity Kit if it holds anything that would be missed. Then **close the Kit**: Windows gives the calculator to one program at a time.
2. Turn the calculator on, leave it at its Home screen, and plug it in.
3. Open the page in Edge or Chrome, click **Connect**, pick the calculator in the browser's list, and click **Run the test**.
4. Click **Save the log** and send the log.

The test first sends a test program of 300 characters each way, and finds a request that brings it back: the two whose name ends in a NUL (`F8 01`, `F8 03`) are both tried, and the one that returns the program compressed is kept; the two without a NUL are tried only if neither of those is answered, because hp-prime-kit's G2 stopped answering after such a request. Each way of sending that worked then climbs: 8,269 characters (the largest program hp-prime-kit sent), 40,856 (the size of DataLoad, our smallest), 140,000, and 289,813 (the size of EpiStats, our largest). A way stops at its first failure. After a failure the page asks the calculator who it is, in the old framing too if the newer one is silent, and if there is no answer it sends nothing more. The old framing's test programs are deleted before the newer framing is asked for, since nothing says how to leave it.

| Way | How the program is sent | From |
|---|---|---|
| A | compressed (`F7 03`), old framing, the report `01` after it | hp-prime-kit |
| B | compressed, old framing, nothing after it | hp-prime-kit, less its last report |
| C | not compressed (`F7 01`), old framing | hp-prime-web |
| D | compressed, in the newer framing | PrimeDev; the Connectivity Kit's framing |

On the calculator the test writes four programs at most, `ZZUSBA`, `ZZUSBB`, `ZZUSBC` and `ZZUSBD`, and deletes them at the end. Each is comment lines and one function that returns its step number. The function comes last, so a program cut short on the way does not compile. If the calculator answers no request for a program, the page asks the person at the calculator to run the test program and say whether it shows its number.

The log holds what was sent and what came back, in numbers. It does not hold the calculator's serial number: the code never reads it.

## The test programs on the Virtual Calculator (17 November 2026)

The cable is not there to be tried without a calculator, but the test programs are. The smallest (`ZZUSBA`, step 1, 300 characters) and the largest (`ZZUSBD`, step 5, 289,813 characters) were built as `.hpprgm` files with hp-prime-kit and put in the folder of the Virtual Calculator 2.4.2 (build 2026-09-09) in the cloud workspace, 19:49 to 19:53:

- The Program Catalog listed ZZUSBA at 2 KB and ZZUSBD at 567 KB.
- Edit took 16 seconds to open ZZUSBD, and Check said "No errors in the program" (`tests/vc_2026-11-17/ZZUSBD_check.png`).
- Run showed a small box, "ZZUSBA 1" for the one and "ZZUSBD 5" for the other (`ZZUSBA_run_box.png`, `ZZUSBD_run_box.png`). That box is what the test page asks a person to look for when nothing can be read back.
- A file put in the folder this way needs one Check before Run does anything, as [two-shortcuts.md](../../docs/two-shortcuts.md) says of any unchecked file; hp-prime-kit reports that a program sent down the cable is compiled as it arrives. The page's question says what to do if Run does nothing.

This says the test programs are programs to HP's own compiler, the largest included. It says nothing about the cable.

## Tests (17 November 2026, all against the mock; none on a calculator)

```
python3 tests/kit_reference_v1.py REF          # hp-prime-kit's messages, into a scratch folder
node tests/test_usb_core_v1.js REF             # 55 PASS, 0 FAIL
node tests/test_usb_ladder_v1.js               # 43 PASS, 0 FAIL   (about two minutes)
node tests/test_usb_page_v1.js PrimeUSBTest_v1.html     # 31 PASS, 0 FAIL   (about half a minute)
```

What a pass means: the messages are the ones hp-prime-kit builds, byte for byte, for all 31 programs, and the ones hp-prime-web's tests expect; the page and the mock, which were written apart, read the three descriptions the same way; and each way the mock can fail is seen and named. What a pass does not mean: that a calculator agrees.

Things the tests turned up that a calculator may or may not share:

- **`FE` is two things.** In the old framing a long message's report numbers run `00` to `FE` and start again at `00`. In the newer framing `FE` begins an acknowledgement. A message of more than 254 reports therefore has a report that looks like an acknowledgement. Compressed, none of our programs reaches 254 reports; not compressed, 11 of the 31 pass it (`tests/test_usb_core_v1.js` counts them).
- **The browser compresses harder than hp-prime-kit.** hp-prime-kit uses zlib's level 1, as the calculator's own messages do (their stream begins `78 01`); a browser's `CompressionStream` has one level, and its stream begins `78 9C`. Any zlib reader takes both, but that the calculator's does is one more thing the test checks.

## The Loader's own USB route

`PrimeLoader_v2a.html` holds a "send straight down the cable" panel for a real HP Prime. It is switched off: it shows only at the page's test address, which ends `?usb=1`, and it says on the page that it has not been proved on a calculator. It sends each program way A, asks for it back, and counts it as loaded only when what comes back is, character for character, what was sent. The first program that cannot be read back stops the run. It will be switched on for students when the test page has passed on a G2 and the route has loaded a chapter that then ran.
