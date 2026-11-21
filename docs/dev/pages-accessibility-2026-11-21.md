# The two loader pages against WCAG 2.1 AA (21 November 2026)

Roger, 21 November 2026, of a list that held "Accessibility of the book and the two loader pages": "Do 'em all". The decks
for the book had been checked the day before; this is the same check for the two pages a student uses, the Prime Loader
and the Data Loader. The standard is WCAG 2.1, Level AA, the one the Department of Justice's rule under Title II of the
ADA names for a public university's web content.

## What was run

`tools/pages_a11y_v1.js` (new; it needs Playwright and `axe-core`), on each page in each state a student can put it in
(as opened; a real HP Prime chosen; every fold opened; "tick the programs yourself"; the Data Loader with its example
loaded), in the light and the dark colors:

1. axe-core's automated rules for WCAG 2.0 and 2.1, levels A and AA;
2. reflow: in a window 320 px wide the page must not scroll sideways (1.4.10);
3. the Tab key: every stop is on the screen and shows a focus mark (2.1.1, 2.4.7);
4. no heading level skipped (a best practice, not a rule of WCAG).

## What was found in Prime Loader v2l and Data Loader v5, and what v2m and v6 change

| Page | Found | WCAG | Changed to |
|---|---|---|---|
| Both | The orange (`#e04000`) and the green (`#008c3c`) used for TEXT had contrasts of 4.28 and 4.36 to 1 on white, and less on the tinted panels (3.9 on the warning panel). The text was the chapter tags beside the programs, every error line, every "verified" line, the Data Loader's readout, and the numerals of the steps. | 1.4.3 (4.5 to 1) | `#c03700` and `#007a35`: 5.5 to 1 on white and at least 4.7 on every surface of the pages. The dark colors already passed and are unchanged. |
| Prime Loader | The box of the log had a name (`aria-label`) and no role, which a screen reader may not announce. Its hidden name still read "The messages that passed on the cable", the words Roger took off the page on 18 November. | 4.1.2 | `role="region"`, named "What was transferred to calculator", as the page calls it. |
| Prime Loader | "Tick the programs yourself" laid the programs out in columns at least 290 px wide, so in a window 320 px wide the page scrolled sideways by 24 px. | 1.4.10 | Columns of `min(290px, 100%)`. |
| Prime Loader | The note for a computer that is not Windows was a heading of level 3 directly under the page's title. | best practice | Level 2, with the look it had (the same font, size and margins, compared in the browser). |
| Data Loader | In a window 320 px wide the page was 379 px wide as it opened: the grid's one column could not shrink, and the menu "Columns are separated by" could not wrap. | 1.4.10 | The columns may shrink (`minmax(0, 1fr)`), the label wraps, and a menu is never wider than its box. The table of columns already scrolled inside its own frame, which WCAG allows for a table. |
| Data Loader | The list of warnings carried `role="status"`, a role a list may not carry. | 4.1.2 | `aria-live="polite"` and `aria-atomic="true"`, which announce the same way and keep the list a list. |

No word that a student reads has changed on either page, no step, and nothing that either page computes, writes or sends.
The Prime Loader's cable code is `prime_usb_v3d.js`, untouched.

## What the check passed without a change

Both pages already had a language, a title, a viewport, labels on every control, a visible focus mark on every stop of the
Tab key, live regions for their messages, and a dark scheme of their own.

## What this does not show

- **No screen reader was run.** A program finds perhaps a third to a half of what WCAG asks. Whether NVDA, JAWS or VoiceOver
  reads the steps in an order that makes sense, and announces the progress of a send without flooding the listener, takes
  a person with a screen reader.
- **The cable's states were not all scanned**: the page while it sends, after a failure, and after a success are drawn by
  script from the calculator's answers. Their colors are the two that were deepened, so their contrast is covered; their
  wording and focus were not looked at with a screen reader.
- **Nothing here ran on a calculator.** v2m changes no byte that travels down the cable, and the test against the mock
  passes, but a pass against the mock is not a calculator: the next send from v2m to a real HP Prime is the proof.
- **WebHID itself** is offered by Chrome and Edge only, which the page says; a student who needs a screen reader that works
  best in Firefox is sent to the Connectivity Kit's steps, as every Firefox user is.

## Results, 21 November 2026

- `node tools/pages_a11y_v1.js` on Prime Loader v2m and Data Loader v6: **32 PASS, 0 FAIL** (`tools/pages_a11y_v1_output.txt`).
  On v2l and v5 the same checks found what the table above lists.
- `node prime-loader/tests/test_loader_v2m.js`: **161 PASS, 0 FAIL** (`prime-loader/tests/test_loader_v2m_output.txt`), the
  same 161 checks as v2l's test, against the mock folder and the pretend calculator.
- `node data-loader/tests/test_core_v2.js`: 34 PASS. `node data-loader/tests/page_check_v6.js`: 37 PASS (v5's 32 and five new).
- Old page against new on a desktop screen (1280 px), pixel by pixel, in three states: 437, 1,650 and 585 pixels differ, about
  0.02% of each picture, and every one of them is orange or green text. The note for a computer that is not Windows has the
  same font, size, color and box as before.

What is left for a person is axe's one "incomplete" item, the Data Loader's table of columns before any data is in it
(`th-has-data-cells`: a table with headers and no rows yet), which is as it should be.
