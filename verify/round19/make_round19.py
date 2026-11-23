# -*- coding: utf-8 -*-
"""Round 19 (23 Nov 2026): the two faults round 18's monkey left open, fixed the way Roger chose, and a third that the
book's Solve example found the same day.

WHY.  Round 18's monkey (verify/round18/README.md, "What the monkey found") left two faults for the author:
  * StatDist v2.7o's Formula page (CAS) for Student's t asks the CAS for E[X^2], and with a df such as 17.83 or 206.3
    Giac on a PC had not finished that integral in ten minutes (verify/round18/probes/probe_statdist_cas.py); whole and
    half df are quick.  A df like 17.83 is what Welch's t-test gives.
  * EpiStats v1.7n's stratified rate ratio divided by zero when a stratum was given a person-time of 1E-300, and with
    0.001 its interval's EXP overflowed (verify/round18/probes/probe_epistats_mh.py).  The stratified rates grid took
    any person-time from 0 to 100,000.
Roger, 23 Nov 2026, 06:37: "1) StatDist--fix as you suggest 2) EpiStats--change the smallest number it asccepts".

WHAT.
  * StatDist v2.7p: the Formula page asks the CAS for E[X], E[X^2] (or, where they are infinite, whether they are) only
    with parameters that keep it quick: Student's t when 2 df is a whole number, Fisher F when df1 and df2 are whole,
    Burr XII when C and K are whole.  Otherwise a gray line says when the CAS is asked, and the page goes
    straight to "no closed form shown" and the program's own values, as it already did when the CAS gave an integral
    back undone (t at df = 9.5).  The probes found F and Burr XII waiting too: verify/round19/probe_fm_families.py
    (every continuous family, parameters to two decimals) and probe_fm_params.py (whole, half and decimal values).
  * EpiStats v1.7o: in the stratified rates grid a person-time is 0, or from 1 to 100,000.  A typed value between 0 and
    1 is refused with a sentence that gives the range and says what to do, and nothing changes; the help lines of the
    two forms give the range.  Why 1: verify/round19/floor_sweep_r19.py, which works the Mantel-Haenszel interval for
    every pair of strata built from a grid of cases and person-times.  At a floor of 1 no interval leaves the Prime's
    range (1E499); at 0.5, 0.1 and 0.001 some do.  Zero stays, because an empty cell is what the grid starts with.
  * PowerViz v2.5v: Cohen's h in radians whatever unit the calculator's trigonometry is in.  v2.5u converted ASIN's
    answer by HAngle, but the current app's own Angle Measure, when it is not System, decides the unit and HAngle does
    not: with the Solve app set to Degrees (the book's bloodstain example, Draft 74) the Virtual Calculator showed
    "h = 11.54, large" for p0 0.5 and p1 0.6, where 0.20, small, is right.  pv_AsinR and pv_SinR now measure the unit
    as the fleet's other trigonometric programs do, by ASIN(1) against pi/2 (BiNorm3D, TDist3D).  Roger's rule:
    "when you find a problem like that that needs to be fixed--FIX IT".
  * Round 11's bump on all three: the header line, a history note, and the version wherever a quoted string holds it.

Each program is built from the version before (read from git, BASE) by exact replacements: each old text must be found
exactly once, or the build stops.

Run from the repository's root:    python3 verify/round19/make_round19.py OUTDIR
"""
import io, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'round18'))
import make_round18 as R18  # noqa: E402   (bump, tag, nxt, die)

BASE = 'b8a2c4d'                     # main before round 19 (PR 33 merged)
DATE = '23 Nov 2026'
R18.DATE = DATE
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r19_programs'
OLD = {'StatDist': 'v2.7o', 'EpiStats': 'v1.7n', 'PowerViz': 'v2.5u'}

PT_MSG = ('A person-time can be 0, or from 1 to 100,000, so give one of less than 1 in smaller units '
          '(person-months instead of person-years, say).')

REPL = {
    'StatDist': [
        ('  LOCAL fcLim, fcV, fcX, fcH, fcR;\n',
         '  LOCAL fcLim, fcV, fcX, fcH, fcR, fcQ;\n'),
        ('  fcLim := "x from " + st_FmLimS(fcD(2)) + " to " + st_FmLimS(fcD(3*fcN)) + ":";\n',
         '  fcLim := "x from " + st_FmLimS(fcD(2)) + " to " + st_FmLimS(fcD(3*fcN)) + ":";\n'
         '  // v2.7p (round 19): the CAS is asked for these integrals only with parameters that keep it\n'
         '  // quick.  Giac on a PC had not finished in 60 s with Student\'s t at df = 17.83 or 206.3 (at\n'
         '  // 17.83, not in ten minutes), Fisher F at df1 = 7 and df2 = 17.83, or Burr XII at C = 2.37,\n'
         '  // and F at df 7.5 and 17.5 took 24 s; whole numbers took under a second, and so did halves\n'
         '  // for t (verify/round19/probe_fm_families.py, probe_fm_params.py).  On the Virtual Calculator\n'
         '  // v2.7o was still "Asking the CAS" after 14 minutes with F at 7 and 17.83, and with Burr XII\n'
         '  // at C = 2.37 the calculator itself stopped, twice; Burr XII at C = 2.5 and K = 3.5 was still\n'
         '  // asking after 3 minutes, while t at df 2.5, 17.5, 17.83 and 206.3, F at 7 and 18 and Burr XII\n'
         '  // at whole C and K took 5 s at most (verify/round19/vc_record.txt).  Otherwise\n'
         '  // the page says so and goes straight to "no closed form shown" and the program\'s own\n'
         '  // values, as it did when the CAS gave an integral back undone.\n'
         '  fcQ := 1;\n'
         '  IF stId == 7 AND FP(2 * stPar(1)) <> 0 THEN\n'
         '    fcQ := 0;\n'
         '    st_FmWrap("The CAS is asked here only when df is a whole number or a half.", stGRY);\n'
         '  END;\n'
         '  IF stId == 9 AND (FP(stPar(1)) <> 0 OR FP(stPar(2)) <> 0) THEN\n'
         '    fcQ := 0;\n'
         '    st_FmWrap("The CAS is asked here only when df1 and df2 are whole numbers, because other values can keep it working for many minutes.", stGRY);\n'
         '  END;\n'
         '  IF stId == 10 AND (FP(stPar(1)) <> 0 OR FP(stPar(2)) <> 0) THEN\n'
         '    fcQ := 0;\n'
         '    st_FmWrap("The CAS is asked here only when C and K are whole numbers, because other values can keep it working for minutes, or stop the calculator.", stGRY);\n'
         '  END;\n'),
        ('    fcM := st_FmAsk("simplify(" + st_FmInt(fcD, 1, "stqx") + ")" + fcSf, stMu);\n',
         '    IF fcQ == 1 THEN fcM := st_FmAsk("simplify(" + st_FmInt(fcD, 1, "stqx") + ")" + fcSf, stMu); END;\n'),
        ('    fcR := st_Cas("exp(-(simplify(" + st_FmInt(fcH, 1, "stqx") + ")" + fcSf + "))");\n',
         '    fcR := "";\n'
         '    IF fcQ == 1 THEN fcR := st_Cas("exp(-(simplify(" + st_FmInt(fcH, 1, "stqx") + ")" + fcSf + "))"); END;\n'),
        ('    fcE := st_FmAsk("simplify(" + st_FmInt(fcD, 2, "stqx") + ")" + fcSf, fcV);\n',
         '    IF fcQ == 1 THEN fcE := st_FmAsk("simplify(" + st_FmInt(fcD, 2, "stqx") + ")" + fcSf, fcV); END;\n'),
        ('    fcR := st_Cas("exp(-(simplify(" + st_FmInt(fcD, 2, "stqx") + ")" + fcSf + "))");\n',
         '    fcR := "";\n'
         '    IF fcQ == 1 THEN fcR := st_Cas("exp(-(simplify(" + st_FmInt(fcD, 2, "stqx") + ")" + fcSf + "))"); END;\n'),
    ],
    'EpiStats': [
        # the four-value form of the stratified rates grid: the range in the two help lines
        ('                {"Cases exposed", "Cases unexposed",\n'
         '                 "Person-time exposed", "Person-time unexposed"},\n',
         '                {"Cases exposed", "Cases unexposed",\n'
         '                 "Person-time exposed, 0 or 1 to 100,000", "Person-time unexposed, 0 or 1 to 100,000"},\n'),
        # ... and the refusal, after the cap
        ('            MSGBOX("A count can be at most 100,000.");\n'
         '        END;\n'
         '        RETURN 0;\n'
         '    END;\n',
         '            MSGBOX("A count can be at most 100,000.");\n'
         '        END;\n'
         '        RETURN 0;\n'
         '    END;\n'
         '    // v1.7o (round 19): a person-time is 0, or from 1 to 100,000.  A person-time of 1E-300 made\n'
         '    // the stratified rate ratio divide by zero (its variance\'s denominator underflowed), and one\n'
         '    // of 0.001 next to 100,000 made its interval overflow; at 1 no interval leaves the Prime\'s\n'
         '    // range (verify/round19/floor_sweep_r19.py).  The form\'s fields C and D are the person-times.\n'
         '    IF esMod == 7 AND ((avC > 0 AND avC < 1) OR (avD > 0 AND avD < 1)) THEN\n'
         '        MSGBOX("' + PT_MSG + '");\n'
         '        RETURN 0;\n'
         '    END;\n'),
        # the grid's one-cell form: the range in its help line ...
        ('            IF esMod == 7 AND gdC == 2 THEN gdHlp := gdRows(gdR) + " person-time, 0 to 100,000"; END;\n',
         '            IF esMod == 7 AND gdC == 2 THEN gdHlp := gdRows(gdR) + " person-time, 0 or 1 to 100,000"; END;\n'),
        # ... and the refusal
        ('                    IF esMod == 7 AND gdC == 2 THEN\n'
         '                        esCel(esSel) := gdV;          // v1.6: person-time, as typed\n'
         '                    ELSE\n',
         '                    IF esMod == 7 AND gdC == 2 THEN\n'
         '                      // v1.7o (round 19): a person-time is 0, or from 1 to 100,000, as in es_AskAll\n'
         '                      IF gdV > 0 AND gdV < 1 THEN\n'
         '                        MSGBOX("' + PT_MSG + '");\n'
         '                      ELSE\n'
         '                        esCel(esSel) := gdV;          // v1.6: person-time, as typed\n'
         '                      END;\n'
         '                    ELSE\n'),
    ],
    'PowerViz': [
        ("// arcsin in RADIANS whatever the Home angle mode (HAngle:\n// 0 radians, 1 degrees, 2 gradians).  Needed for Cohen's h.\nLOCAL pv_AsinR(av)\nBEGIN\n LOCAL ar;\n ar := ASIN(av);\n IF HAngle==1 THEN ar := ar*3.14159265358979/180; END;\n IF HAngle==2 THEN ar := ar*3.14159265358979/200; END;\n RETURN ar;\nEND;\n\n// sine of an angle given in RADIANS whatever the Home angle mode\n// (v2.4; the power-vs-effect view turns h back into p with it).\nLOCAL pv_SinR(srad)\nBEGIN\n IF HAngle==1 THEN RETURN SIN(srad*180/3.14159265358979); END;\n IF HAngle==2 THEN RETURN SIN(srad*200/3.14159265358979); END;\n RETURN SIN(srad);\nEND;\n",
         "// The unit the calculator's trigonometry is in, as a number of\n// radians: 1 in radians, pi/180 in degrees, pi/200 in grads.\n// v2.5v: measured, not read from HAngle.  The current app's own\n// Angle Measure, when it is not System, decides the unit, and\n// HAngle (which this program sets to 0 at its start) does not:\n// with the Solve app set to Degrees, ASIN(1) is 90 in Home and in\n// a program, and v2.5u showed h = 11.54 for p0 0.5 and p1 0.6\n// (Virtual Calculator, 23 Nov 2026).  BiNorm3D and TDist3D\n// measure the unit the same way.\nLOCAL pv_AngU()\nBEGIN\n RETURN 1.5707963267949/ASIN(1);\nEND;\n\n// arcsin in RADIANS whatever unit the calculator is in.  Needed\n// for Cohen's h.\nLOCAL pv_AsinR(av)\nBEGIN\n RETURN ASIN(av)*pv_AngU();\nEND;\n\n// sine of an angle given in RADIANS whatever unit the calculator\n// is in (v2.4; the power-vs-effect view turns h back into p with\n// it).\nLOCAL pv_SinR(srad)\nBEGIN\n RETURN SIN(srad/pv_AngU());\nEND;\n"),
    ],
}

NOTES = {
    'StatDist': ('Round 19: the Formula page (CAS) asks the CAS for its integrals only with parameters that keep it quick: '
                 'Student\'s t when 2 df is a whole number, Fisher F when df1 and df2 are whole, Burr XII when C and K are whole.  '
                 'Round 18\'s monkey found the page waiting for t at df = 206.3; Giac on a PC had not finished at df = 17.83 in ten '
                 'minutes, and round 19\'s probes found F (df 7 and 17.83) and Burr XII (C = 2.37) waiting too.  On the Virtual '
                 'Calculator v2.7o was still asking after 14 minutes with that F, and with that Burr XII the calculator stopped.  '
                 'Otherwise a gray line says when the CAS is asked, and the page shows "no closed form shown" and the program\'s own '
                 'values.  '
                 'Roger, 23 Nov 2026: "StatDist--fix as you suggest".  Only st_FmCont changed, and the version.'),
    'EpiStats': ('Round 19: in the stratified rates grid a person-time is 0, or from 1 to 100,000.  Round 18\'s monkey typed a '
                 'person-time of 1E-300, and the Mantel-Haenszel rate ratio divided by zero; 0.001 made its interval overflow.  '
                 'A value between 0 and 1 is refused with a sentence that gives the range, in the four-value form (es_AskAll) '
                 'and in the one-cell form (es_Grid), and the two forms\' help lines give the range.  Roger, 23 Nov 2026: '
                 '"EpiStats--change the smallest number it asccepts".  No other statement, number or word on a page changed, '
                 'only the version.'),
    'PowerViz': ('Round 19: Cohen\'s h is in radians whatever unit the calculator\'s trigonometry is in.  v2.5u '
                 'converted ASIN\'s answer by HAngle, but the current app\'s own Angle Measure, when it is not System, '
                 'decides the unit and HAngle does not: with the Solve app set to Degrees the Virtual Calculator showed '
                 '"h = 11.54, large" for p0 0.5 and p1 0.6 (0.20, small, is right).  pv_AngU measures the unit as '
                 '1.5707963267949/ASIN(1), and pv_AsinR and pv_SinR use it.  Found by the book\'s Solve example '
                 '(Draft 74), 23 Nov 2026.  No word on a page changed, only the version.'),
}


def old_text(name, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (BASE, name, ov)], check=True,
                          capture_output=True).stdout.decode('utf-8')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, ov in OLD.items():
        nv = R18.nxt(ov)
        s = old_text(name, ov)
        for i, (a, b) in enumerate(REPL[name]):
            if s.count(a) != 1:
                R18.die('%s: replacement %d found %d times' % (name, i + 1, s.count(a)))
            s = s.replace(a, b)
        s = R18.bump(name, s, ov, nv, NOTES[name])
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-9s %s -> %s  %d replacements' % (name, ov, nv, len(REPL[name])))
