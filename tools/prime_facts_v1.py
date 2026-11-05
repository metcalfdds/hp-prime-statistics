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

USE.  import prime_facts_v1; prime_facts_v1.apply()      -- once, before the first Harness is made.
      It returns the harness module.  Applying it twice does nothing more.
"""

FACTS = ['STRING(x, 2, d): "Invalid input" for d >= 13 (Virtual Calculator, 1 Nov 2026)',
         'STRING(x, 3, d): the small capital E, "4.0\u1d078" (Virtual Calculator, 1 Nov 2026)',
         'RANDSEED(value) seeds the random numbers (User Guide 2018; added 4 Nov 2026)']


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
        return t
    R.Harness._build_table = _build_table
    R.Harness._prime_facts_v1 = True
    return R


if __name__ == '__main__':
    print(__doc__)
