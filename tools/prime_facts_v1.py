#!/usr/bin/env python3
"""prime_facts_v1.py -- what the Prime does that the harness (ppl_run_v3e.py) does not model yet, added to it by a
patch.  Roger Metcalf & Claude, 1 Nov 2026.

WHY.  The harness is a PC model of the calculator.  When the Virtual Calculator shows a behaviour the harness gets
wrong, the verify scripts and the monkey test must see it at once, before the harness's next version absorbs it.
This module holds those facts, each with where and when it was seen, and applies them to the harness class.

THE FACTS (Virtual Calculator 2.4.2, build 2026-09-09, Rogers-HP, typed in Home, 1 Nov 2026):
  1. STRING(x, 2, d) is "Error: Invalid input" for d of 13 or more, whatever x:
       STRING(2*10^(-44), 2, 44), STRING(5*10^(-13), 2, 13) and STRING(0.5, 2, 13) all gave "Invalid input";
       STRING(5*10^(-12), 2, 12) gave "0.000000000005" and STRING(5*10^(-12), 2, 11) gave "5.00000000000ᴇ-12"
       (scientific, as the harness already models for x below 10^-d).
     The harness printed any number of decimals.  SampDist v2.3d stopped with "Error: Invalid input" at
     sigma = 1E12 (its density labels took d = 13), on the same calculator the same evening.
     Only mode 2 (fixed) was tried for this; the other modes are not patched for it.
  2. STRING(x, 3, d), scientific, writes the calculator's small capital E: STRING(4*10^8, 3, 1) = "4.0ᴇ8",
     STRING(0.00015, 3, 1) = "1.5ᴇ-4", STRING(150000000, 3, 1) = "1.5ᴇ8" (and STRING(0.00015, 2, 1) = "1.5ᴇ-4", as
     the harness already writes it).  The harness wrote a plain "E" in mode 3.  The exponent's minus sign was not
     read from the screen; it is written as the harness writes mode 2's (Home's minus with home_minus=True,
     CASProbe beta 1c T43b, 17 Oct 2026).

  3. RANDSEED(value) seeds the random numbers (HP Prime User Guide, 2018 edition, Probability - Random:
     "RANDSEED(value)"; the edition bundled with the Virtual Calculator 2.4.2).  Added 4 Nov 2026: the harness
     stopped on it as "not covered", so the monkey test could not see past BurrLab's and ResampLab's seed field.
     Modelled as seeding the harness's own generator; it returns 0.  (This file keeps its name, v1: the verify
     scripts and the monkey import it by name, Lessons Learned s14 rule 7.)

  4. A CHOOSE title shows 31 characters and no more (Virtual Calculator 2.4.2, build 2026-09-09, under Wine in the
     cloud workspace, 15 Nov 2026).  AnovaLab beta 1i's "Dunnett d crit: about 14-41 s on a G1", 37 characters, stood
     in the box's title bar as "Dunnett d crit: about 14-41 s o"; "Dunnett: about 37-112 s on a G1", 31 characters,
     stood whole; and the box of the cut title was the narrower of the two, so the limit is a count of characters and
     not a width.  The harness keeps every title whole.  Modelled as a record, not an error: every title longer than
     31 characters that a program shows goes into the list Harness.cut_titles as (title, the 31 characters shown, the
     routine, the program's file name), and every title shown into the dictionary Harness.shown_titles (file name ->
     set of titles), for a verify script or the monkey to read.  (Items are a separate matter: a menu item is cut at
     the box's width, about 30 characters; CLAUDE.md.)

  5. STRING writes the decimal mark that Home's Digit Grouping sets (Virtual Calculator 2.4.2, build 2026-09-09, under
     Wine in the cloud workspace, 22 Nov 2026).  With Digit Grouping 123.456,789, STRING(1234.5678) typed in Home gave
     "1234,5678", and a running program's numbers came out the same way, pragma line or not: Norm3 showed
     P(X <= x0) = 0,9,772 for 0.9772 and StatDist v2.7n showed 0,758,036 for 0.758036, because the fleet's comma
     routine takes a run of four or more digits that no period stands before for a whole number.  An INPUT form took
     and showed 1.234,5.  NOT PATCHED: the harness has no Home setting for the mark and always writes a period, so a
     verify script or the monkey says nothing about a calculator set to a comma.  (Lessons Learned v7zy.)

  6. A program reads and assigns Home's settings (the same calculator, 22 Nov 2026; diagnostics/SetProbe_beta1.txt,
     SetOdd_beta1.txt, SetBook_beta1.txt): HSeparator, HAngle, HFormat, HDigits and Entry.  A change acts at once
     (HAngle:=1 made SIN(90) 1; HFormat:=1 with HDigits:=2 made STRING(0.046) "0.05") and stays after the program ends
     unless the program puts it back.  The book's settings are all code 0.  NOT PATCHED: the harness has none of the five.

  7. The current app's own Angle Measure, when it is not System, is the unit of SIN, ASIN and the rest, in Home and in a
     running program, whatever HAngle says (the same calculator, 23 Nov 2026, round 19; verify/round19/vc_record.txt).
     With the Solve app current and its Symbolic Setup's Angle Measure at Degrees, Home Settings read "Angle Measure:
     See Symbolic Setup" with no choice, ASIN(1) in Home gave 90 before and after HAngle:=0, and PowerViz v2.5u, which
     sets HAngle := 0 at its start and converted ASIN's answer by HAngle, showed Cohen's h = 11.54 for p0 0.5 and p1 0.6
     (0.2014 is right); the setting stayed through Calculator > Exit and a new start.  MODELLED as an attribute,
     Harness.app_angle: None (the default, an app at System: the harness as before) or 'rad', 'deg' or 'grad', which
     then decides the unit and HAngle does not.  Set it on a harness to test a program against an app set to Degrees.

  8. ROUND rounds the decimal number the calculator holds, and a tie away from zero (the same calculator, 28 Nov 2026,
     round 21; diagnostics/RoundProbe_beta1a.txt, run in the cloud workspace's Virtual Calculator 2.4.2): 162.45/10 is
     16.245 and ROUND(162.45/10, 2) is 16.25; ROUND(16.245, 2) 16.25, ROUND(-16.245, 2) -16.25, ROUND(0.125, 2) 0.13,
     ROUND(2.5, 0) 3, ROUND(3.5, 0) 4, ROUND(-2.5, 0) -3 and ROUND(16.245, -4) 16.25.  The harness's binary floats hold
     162.45/10 as 16.244999999999997, and its ROUND gave 16.24: TTestLab beta 1n's one-sample step 4 showed SE =
     162.45/root 100 = 16.24, where a student and the calculator give 16.25.  The calculator also held more digits than
     it shows: (1 + 1E-15) - 1 gave 1E-15, and ROUND((0.0078125 + 123101)^2, 0) gave 15153858124 where STRING showed
     15153858124.5.  MODELLED: ROUND takes its argument as the decimal of 15 significant digits nearest the harness's
     float (the binary error lies below that) and rounds it half away from zero, to n decimals or, for n < 0, to -n
     significant digits; a list or anything else not a real goes to the harness's own ROUND as before.  NOT
     MODELLED: the rest of the harness's arithmetic stays binary, so (1 + 1E-12) - 1 is 1.00008890058E-12 there.

USE.  import prime_facts_v1; prime_facts_v1.apply()      -- once, before the first Harness is made.
      It returns the harness module.  Applying it twice does nothing more.
"""

FACTS = ['STRING(x, 2, d): "Invalid input" for d >= 13 (Virtual Calculator, 1 Nov 2026)',
         'STRING(x, 3, d): the small capital E, "4.0\u1d078" (Virtual Calculator, 1 Nov 2026)',
         'RANDSEED(value) seeds the random numbers (User Guide 2018; added 4 Nov 2026)',
         'CHOOSE: a title shows 31 characters; longer ones are listed in Harness.cut_titles (Virtual Calculator, '
         '15 Nov 2026)',
         'STRING writes the decimal mark of Home\'s Digit Grouping, "1234,5678" with 123.456,789: recorded, not '
         'patched (Virtual Calculator, 22 Nov 2026)',
         'a program reads and assigns HSeparator, HAngle, HFormat, HDigits and Entry: recorded, not patched '
         '(Virtual Calculator, 22 Nov 2026)',
         'the current app\'s own Angle Measure, when not System, is the unit of SIN and ASIN whatever HAngle says: '
         'Harness.app_angle (Virtual Calculator, 23 Nov 2026)',
         'ROUND rounds the decimal the calculator holds, a tie away from zero: ROUND(162.45/10, 2) = 16.25 '
         '(Virtual Calculator, 28 Nov 2026)']
TITLE_MAX = 31


def apply():
    import ppl_run_v3e as R
    if getattr(R.Harness, '_prime_facts_v1', False):
        return R
    orig = R.Harness._string_home

    def _string_home(self, a):
        # fact 1: fixed format takes at most 12 decimals
        if len(a) >= 3 and not isinstance(a[1], str) and not isinstance(a[2], str):
            try:
                mode, d = int(a[1]), int(a[2])
            except (TypeError, ValueError):
                mode, d = None, None
            if mode == 2 and d is not None and d > 12:
                raise R.PPLError('Invalid input: STRING(x, 2, %d) -- the Prime takes at most 12 decimals '
                                 '(Virtual Calculator, 1 Nov 2026; prime_facts_v1)' % d)
            # fact 2: scientific form with the small capital E, and the exponent's minus as mode 2's
            if mode == 3 and isinstance(a[0], float):
                r = orig(self, a)
                if isinstance(r, str) and 'E' in r:
                    mant, ex = r.split('E', 1)
                    if ex.startswith('-') and getattr(self, 'home_minus', False):
                        ex = u'\u2212' + ex[1:]
                    if ex.startswith('+'):
                        ex = ex[1:]
                    r = mant + u'\u1d07' + ex
                return r
        return orig(self, a)

    R.Harness._string_home = _string_home
    # fact 3: RANDSEED
    ob = R.Harness._build_table

    def _build_table(self):
        t = ob(self)
        t['RANDSEED'] = lambda a, site: (self.rng.seed(a[0] if a else 0), 0.0)[1]
        t['ROUND'] = lambda a, site: _round_decimal(self, a)       # fact 8
        return t

    # fact 8: ROUND rounds the decimal number the calculator holds, a tie away from zero
    def _round_decimal(machine, a):
        import decimal
        x = a[0] if a else None
        if not isinstance(x, float) or x != x or x in (float('inf'), float('-inf')) or len(a) > 2:
            return R.interp.BUILTINS['ROUND'](machine, a)
        n = int(a[1]) if len(a) > 1 else 0
        if x == 0.0:
            return 0.0
        with decimal.localcontext() as c:
            c.prec = 80
            d = decimal.Decimal(repr(x))
            last = d.adjusted() - 14                     # the exponent of its 15th significant digit
            d = d.quantize(decimal.Decimal(1).scaleb(last), rounding=decimal.ROUND_HALF_UP)
            if d == 0:
                return 0.0
            t = -n if n >= 0 else d.adjusted() + n + 1     # the exponent of the last digit kept
            if t <= last:                                  # nothing to round off (1E300 to 2 decimals)
                return float(d)
            return float(d.quantize(decimal.Decimal(1).scaleb(t), rounding=decimal.ROUND_HALF_UP))
    R.Harness._build_table = _build_table
    # fact 4: a CHOOSE title of more than 31 characters is cut; keep a record of each one shown
    oc = R.Harness._choose
    R.Harness.cut_titles = []
    R.Harness.shown_titles = {}

    def _choose(self, nodes, frame):
        import os
        n0 = len(self.dialogs)
        try:
            return oc(self, nodes, frame)
        finally:
            fn = os.path.basename(str(self.files[0])) if getattr(self, 'files', None) else ''
            for c in self.dialogs[n0:]:
                if isinstance(c, R.Choose):
                    R.Harness.shown_titles.setdefault(fn, set()).add(c.title)
                    if len(c.title) > TITLE_MAX:
                        R.Harness.cut_titles.append((c.title, c.title[:TITLE_MAX], c.func, fn))
    R.Harness._choose = _choose
    # fact 7: the current app's own Angle Measure decides the unit of the trigonometric functions when it is set
    R.Harness.app_angle = None
    oau = R.Harness._angle_unit

    def _angle_unit(self):
        import math
        aa = getattr(self, 'app_angle', None)
        if aa is not None:
            return {'rad': 1.0, 'deg': math.pi / 180, 'grad': math.pi / 200}[aa]
        return oau(self)
    R.Harness._angle_unit = _angle_unit
    R.Harness._prime_facts_v1 = True
    return R


if __name__ == '__main__':
    print(__doc__)
