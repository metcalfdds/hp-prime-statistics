# GaltonBoard beta 3d: changes

*19 October 2026. Roger Metcalf, 2026. Written with AI assistance (Anthropic Claude).*

## Why

Roger, 19 Oct 2026, 12:48: every program in the fleet should say plainly that it is a teaching and demonstration aid, not to be relied on for legal purposes.

The fleet review of the same day found nothing to fix in GaltonBoard beta 3c ("ship as is"). It left two wordings for Roger to decide (D17): "poured 1 balls" and the "sqrt Rp(1-p)" readout.

## What changed

1. The header: a DISCLAIMER line under the distribution terms:
   > DISCLAIMER: a teaching and demonstration aid. Not validated for forensic, clinical or legal use; do not rely on its results for legal purposes.
2. The header: the banner reads beta 3d; the firmware paragraph records that beta 3c passed the emulator retest on 17 Oct 2026; and a "WHAT CHANGED in beta 3d" paragraph.

**Nothing else changed.** With every `//` comment line removed, beta 3d and beta 3c are byte-identical (checked by script, 19 Oct 2026). No screen changed.

## Verification

- **Code identity:** beta 3c's 2,374 lines and beta 3d's 2,387 lines are identical once the 13 added comment lines are removed. `verify_GaltonBoard_beta3c.py` and its results therefore carry over unchanged.
- **Gate:** `ppl_gate_v1b.py GaltonBoard_beta3d.txt _old/GaltonBoard_beta3c.txt` gives RESULT: PASS.
  - The hp-prime-kit lint reports the 1 known "error" inside the `#PYTHON` block, as on beta 3c.
  - No hard errors.
  - fleet_names_v2 over the 25 current files: 0 collisions.

## Device checklist

None beyond beta 3c's: the code is unchanged. Paste, then Check.

## Unresolved

- D17: the two wordings above.
- The MicroPython drop still needs a hardware run with the Terminal open.
