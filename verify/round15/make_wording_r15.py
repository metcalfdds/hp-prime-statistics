# -*- coding: utf-8 -*-
"""Round 15, the wording (15 Nov 2026): what five programs say about the TI-83/84 programs they follow.

Roger, 14 Nov 2026, 23:52: "IS there an issue with 'reworking' the TI and Triola and Lloyd programs?"  The record (the TI
sweep of 20 Oct 2026): the TI programs were decoded and read to see what each one computes and where it goes wrong, and our
programs were then written new in PPL; none of the TI code is in them.  "Reworks" says more than that, so the book's
Appendix F got a paragraph in his own words on 15 Nov ("we did not reuse any of that code ... wrote our own version for the
Prime ... to compute similar results"), and this round puts the same statement where the programs said "reworks": the help
pages of RankLab, AnovaLab and ResampLab, and the file headers of those three, ExhibitLab and SurvLab.  (FitCheck, the sixth,
is built by make_fitcheck_1h.py, which also gives it its new standard errors.)  ONLY WORDS CHANGE: comments, and help text.

Every change is an exact replacement in the version before (read from git, BASE below); a replacement that does not match
exactly once stops the build.  Each program then gets its next version: the header line, a history note, and every version
string in a literal (as Rounds 11 and 12 did).  Run from the repository's root:
    python3 verify/round15/make_wording_r15.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap

BASE = 'a7df6e7'                     # main before Round 15
DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r15_programs'

EDITS = {
 'RankLab': ('beta1h', 'beta1i', [
   ('        "Reworks Michael Lloyd\'s TI-83/84 programs",\n'
    '        "for Triola (SRTEST, RSTEST, KWTEST, SRCORR,",\n'
    '        "ZZRANK) without their tie, zero, rs errors."};',
    '        "Does what Michael Lloyd\'s TI-83/84 programs",\n'
    '        "for Triola do (SRTEST, RSTEST, KWTEST, SRCORR,",\n'
    '        "ZZRANK), without their tie, zero, rs errors.",\n'
    '        "Written new for the Prime: none of their code."};'),
   ('// Replaces / reworks: the rank-test programs of Mario Triola\'s\n',
    '// Does on the Prime what these TI-83/84 programs do.  They were read to\n'
    '//   see what each one computes; RankLab was then written new in PPL, and\n'
    '//   none of their code is in it.  They are the rank-test programs of Mario Triola\'s\n')],
   'Help page 7/7 ends "Does what Michael Lloyd\'s TI-83/84 programs for Triola do (...), without their tie, zero, rs '
   'errors.  Written new for the Prime: none of their code." (four lines; it was three).  The '
   'header\'s note on those programs begins the same way.'),
 'AnovaLab': ('beta1g', 'beta1h', [
   ('    av_Tx("Reworks Triola\'s TI-83/84 ANOVA, ANOVA2FD,", 10, 30, #000000h);\n'
    '    av_Tx("ANOVA2RB, RANOVA, TUKEY, SCHEFFE2, BONFRNI,", 10, 43, #000000h);\n'
    '    av_Tx("SDHYP, SDINT, STDTEST, STDEVCI and FINTRVAL.", 10, 56, #000000h);\n'
    '    av_Tx("Not repeated: 0 and negatives as missing,", 10, 72, avRED);\n'
    '    av_Tx("the wrong n in Tukey\'s SE, swapped F bounds,", 10, 85, avRED);\n'
    '    av_Tx("a solver that fails for n > 75, equal-n only.", 10, 98, avRED);\n'
    '    av_Tx("Tukey\'s q: StudRange\'s PPL engine (Dunlap,", 10, 114, avBLUE);\n'
    '    av_Tx("Powell & Konnerth 1977, with a u" + avSq + " step).", 10, 127, avBLUE);\n'
    '    av_Tx("Data: Plaster 1989; Fienberg 1971; Beall 1942;", 10, 143, avGRAY);\n'
    '    av_Tx("New Haven Register 1977 (R datasets).", 10, 156, avGRAY);\n'
    '    av_Tx("A teaching aid: not validated for forensic,", 10, 172, avRED);\n'
    '    av_Tx("clinical or legal use.", 10, 185, avRED);\n',
    '    av_Tx("Does what Triola\'s TI-83/84 programs ANOVA,", 10, 30, #000000h);\n'
    '    av_Tx("ANOVA2FD, ANOVA2RB, RANOVA, TUKEY, SCHEFFE2,", 10, 43, #000000h);\n'
    '    av_Tx("BONFRNI, SDHYP, SDINT, STDTEST, STDEVCI and", 10, 56, #000000h);\n'
    '    av_Tx("FINTRVAL do.  Written new: none of their code.", 10, 69, #000000h);\n'
    '    av_Tx("Not repeated: 0 and negatives as missing,", 10, 85, avRED);\n'
    '    av_Tx("the wrong n in Tukey\'s SE, swapped F bounds,", 10, 98, avRED);\n'
    '    av_Tx("a solver that fails for n > 75, equal-n only.", 10, 111, avRED);\n'
    '    av_Tx("Tukey\'s q: StudRange\'s PPL engine (Dunlap,", 10, 127, avBLUE);\n'
    '    av_Tx("Powell & Konnerth 1977, with a u" + avSq + " step).", 10, 140, avBLUE);\n'
    '    av_Tx("Data: Plaster 1989; Fienberg 1971; Beall 1942;", 10, 156, avGRAY);\n'
    '    av_Tx("New Haven Register 1977 (R datasets).", 10, 169, avGRAY);\n'
    '    av_Tx("A teaching aid: not validated for forensic,", 10, 185, avRED);\n'
    '    av_Tx("clinical or legal use.", 10, 198, avRED);\n'),
   ('// Replaces / reworks (Triola\'s TI-83/84 CD and related TI programs,\n'
    '//   decoded in ref/triola_ti_programs/; credited with thanks):\n',
    '// Does on the Prime what these TI-83/84 programs do.  They were decoded and\n'
    '//   read (ref/triola_ti_programs/) to see what each one computes; AnovaLab\n'
    '//   was then written new in PPL, and none of their code is in it.  From\n'
    '//   Triola\'s TI-83/84 CD and related TI programs, credited with thanks:\n'),
   ('// The variance test and interval (Triola\'s S2TEST / S2INT reworked).', '// The variance test and interval (what Triola\'s S2TEST / S2INT do).'),
   ('// 12. VARIANCES (Triola\'s S2TEST / S2INT reworked)', '// 12. VARIANCES (what Triola\'s S2TEST / S2INT do)')],
   'Help page 9/9 begins "Does what Triola\'s TI-83/84 programs ANOVA, ... and FINTRVAL do.  Written new: none of their '
   'code." (four lines; it was three), and the nine lines under it each sit 13 px lower (the last at '
   'y 198).  The header\'s note on those programs begins the same way, and two section comments say "what Triola\'s '
   'S2TEST / S2INT do".'),
 'ResampLab': ('beta1h', 'beta1i', [
   ('Davison & Hinkley 1997; Hesterberg 2015.  Reworks Triola\'s TI bootstrap project and the TI BOOT program.", hpY + 4, rsBLUE);',
    'Davison & Hinkley 1997; Hesterberg 2015.  Does what Triola\'s TI bootstrap project and the TI BOOT program do; written new, with none of their code.", hpY + 4, rsBLUE);'),
   ('// Replaces / reworks:\n'
    '//   Triola, Elementary Statistics Using the TI-83/84 Plus, 2nd ed., the\n',
    '// Does on the Prime what these do.  They were read to see what each one\n'
    '//   computes; ResampLab was then written new in PPL, and none of their code\n'
    '//   is in it:\n'
    '//   Triola, Elementary Statistics Using the TI-83/84 Plus, 2nd ed., the\n'),
   ('//   BOOT (TI-83 library, boot.zip): percentile and BCa bootstrap.  Its BCa\n'
    '//     arithmetic is sound and is kept (Efron\'s jackknife acceleration and\n'
    '//     the adjusted percentiles).  Not repeated here: (1) its z0 counts\n',
    '//   BOOT (TI-83 library, boot.zip): percentile and BCa bootstrap.  Its BCa\n'
    '//     arithmetic is sound, and ResampLab uses the same published method\n'
    '//     (Efron\'s jackknife acceleration and the adjusted percentiles).  Not\n'
    '//     repeated here: (1) its z0 counts\n')],
   'Help page 5/5: "Does what Triola\'s TI bootstrap project and the TI BOOT program do; written new, with none of their '
   'code."  The header\'s note begins the same way, and says that ResampLab uses the same '
   'published method as BOOT\'s BCa arithmetic (Efron\'s), where it said the arithmetic "is kept".'),
 'ExhibitLab': ('beta1g', 'beta1h', [
   ('// Replaces / reworks: the Triola TI-83/84 programs OCBIN, OCHYPER and\n'
    '//   OCPOISSN (operating-characteristic curves; credited).  Their bugs are\n',
    '// Does on the Prime what the Triola TI-83/84 programs OCBIN, OCHYPER and\n'
    '//   OCPOISSN do (operating-characteristic curves; credited).  They were read\n'
    '//   to see what each one computes; ExhibitLab was then written new in PPL,\n'
    '//   and none of their code is in it.  Their bugs are\n')],
   'The header\'s note on the Triola TI-83/84 programs OCBIN, OCHYPER and OCPOISSN begins "Does on the Prime what ... '
   'do" and says that ExhibitLab was written new, with none of their code.  Nothing on screen changes.'),
 'SurvLab': ('beta1f', 'beta1g', [
   ('// Replaces / reworks: the TI-83/84 program KAPMEIT1 (kaplanmeiertest1.zip,\n'
    '//   Triola program library; decoded in ref/triola_ti_programs), which\n'
    '//   takes grouped data (days, number failed, number censored), lists the\n',
    '// Does on the Prime what the TI-83/84 program KAPMEIT1 does (kaplanmeiertest1.zip,\n'
    '//   Triola program library).  KAPMEIT1 was decoded (ref/triola_ti_programs) and\n'
    '//   read to see what it computes; SurvLab was then written new in PPL, and none\n'
    '//   of KAPMEIT1\'s code is in it.  KAPMEIT1\n'
    '//   takes grouped data (days, number failed, number censored), lists the\n')],
   'The header\'s note on the TI-83/84 program KAPMEIT1 begins "Does on the Prime what ... does" and says that SurvLab '
   'was written new, with none of KAPMEIT1\'s code.  Nothing on screen changes.'),
}


def tag(v):
    return v.replace('beta', 'beta ')


def die(msg):
    sys.exit('BUILD STOPPED: ' + msg)


def bump(name, s, ov, nv, note):
    """Round 11's bump: the header line, a history note before the old version's, and every version string in a literal."""
    ot, nt = tag(ov), tag(nv)
    L = s.split('\n')
    hv = None
    for i, l in enumerate(L[:40]):
        if re.match(r'^//\s*[A-Za-z0-9 ]+ - ' + re.escape(ot) + r'\b', l):
            hv = i
            break
    if hv is None:
        die(name + ': no header line for ' + ot)
    L[hv] = L[hv].replace(ot, nt)
    L[hv] = re.sub(r'\((\d+ Nov 2026[^)]*)\)', '(%s)' % DATE, L[hv], count=1)
    hist = [i for i, l in enumerate(L) if re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', l)]
    if not hist:
        die(name + ': no history line for ' + ot)
    body = ('Round 15: the credits say exactly what was done with the TI-83/84 programs this one follows (Roger, 14-15 Nov '
            '2026).  They were read to see what each one computes, and this program was then written new in PPL: none of '
            'their code is in it.  ' + note + '  Only words changed: no line of code but the help text.')
    L.insert(hist[0], '// %s (%s): ' % (nt, DATE) + '\n//   '.join(textwrap.wrap(body, 100)))
    s = '\n'.join(L)
    s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace(ot, nt).replace(ov, nv), s)
    # a version on screen with its date: the new date (Round 11's bump did the same)
    s = re.sub(r'"[^"\n]*%s[^"\n]*"' % re.escape(nt), lambda m: re.sub(r'\b\d{1,2} Nov 2026', DATE, m.group(0)), s)
    return s


def old_text(name, ov):
    return subprocess.run(['git', 'show', '%s:programs/%s_%s.txt' % (BASE, name, ov)], check=True,
                          capture_output=True).stdout.decode('utf-8')


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, (ov, nv, eds, note) in EDITS.items():
        s = old_text(name, ov)
        for a, b in eds:
            n = s.count(a)
            if n != 1:
                die('%s: %d matches for %r' % (name, n, a[:80]))
            s = s.replace(a, b)
        s = bump(name, s, ov, nv, note)
        if re.search('(?i)rework', s):
            die('%s: the word is still in the file: %s' % (name, ' | '.join(l[:90] for l in s.split('\n') if re.search('(?i)rework', l))))
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-10s %s -> %s  (%d changes)' % (name, ov, nv, len(eds)))
