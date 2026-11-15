# -*- coding: utf-8 -*-
"""Round 16, the wording (15 Nov 2026): what four more programs say about the programs they stand beside.

Roger, 15 Nov 2026, asked whether StatDist's "framework after S. Micciche" and the label "Replaces / reworks:" in BurrLab,
RiskLab and AgreeLab should be reworded as Round 15 reworded the six that follow TI-83/84 programs: "reword as the
others---look, be consistent throughout the book".  A credit says what was done, in plain verbs (Lessons Learned v7zv s14).

  StatDist v2.7n   the header said "(framework after S. Micciche)".  THE RECORD (15 Nov 2026, D:\\HP-Prime\\statistic.zip set
                   beside the StatDist files): Micciche's "Statistic Distributions" is 494 lines, 55 exported density and
                   CDF functions, no menus, no plots; of its 134 distinct code lines not one is in StatDist v2.7m
                   (5,091 lines), v2.5 or v2.2 (29 Jul 2026, the oldest copy kept), and none of its function names or
                   its "Use: ..." messages; 11 of the 13 families StatDist adds are families his file has (not Burr XII,
                   not the triangular).  The header now says that.
  AgreeLab beta 1h "Replaces / reworks: no TI program ... nothing is ported" -> "Follows no TI-83/84 program ... written new".
  RiskLab beta 1h  "Replaces / reworks: no Triola program does this.  The TI-83/84 LOGIT program ..." -> "No Triola
                   program does this.  The nearest TI-83/84 program, LOGIT ... was read to see what it computes; RiskLab
                   was written new in PPL, and none of LOGIT's code is in it."
  BurrLab beta 1r  "Replaces / reworks: Burr3 v2.4c (fleet).  No TI program is replaced." -> what was carried over from
                   the fleet's own Burr3, named, and "It follows no TI program."  (The header's earlier paragraph,
                   "REPLACES Burr3 v2.4c in the fleet (its header, its ... idiom and its log-domain pdf and CDF are
                   reused here ...)", already says which code was carried over, as the rule asks, and stays.)
ONLY COMMENTS CHANGE, and the version each program shows.  Every change is an exact replacement in the version before
(read from git, BASE below); a replacement that does not match exactly once stops the build.  Run from the repository's
root:    python3 verify/round16/make_wording_r16.py OUTDIR
"""
import io, os, re, subprocess, sys, textwrap

BASE = '4e8ff66'                     # main before Round 16
DATE = '15 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r16_programs'

EDITS = {
 'AgreeLab': ('beta1g', 'beta1h', [
   ('// Replaces / reworks: no TI program.  ref/triola_ti_programs/ holds no\n'
    '//   agreement program (a search for kappa finds only Bayesian posterior\n'
    '//   programs), so nothing is ported and no TI bug applies.\n',
    '// Follows no TI-83/84 program: ref/triola_ti_programs/ holds no\n'
    '//   agreement program (a search for kappa finds only Bayesian posterior\n'
    '//   programs).  AgreeLab was written new in PPL from the papers listed\n'
    '//   above; no TI code is in it, and no TI bug applies.\n')],
   'The header\'s note on TI programs begins "Follows no TI-83/84 program" and says that AgreeLab was written new in PPL '
   'from the papers it lists (it said "Replaces / reworks: no TI program ... nothing is ported").'),
 'RiskLab': ('beta1g', 'beta1h', [
   ('// Replaces / reworks: no Triola program does this.  The TI-83/84 LOGIT\n'
    '//   program (logit.zip, ref/triola_ti_programs/LOGIT__257.txt) fits a\n'
    '//   one-predictor logistic model to grouped counts by weighted least\n'
    '//   squares; RiskLab fits any 1-4 predictors by full Newton-Raphson to\n'
    '//   convergence, gives SEs, tests and odds ratios, and detects\n'
    '//   separation, none of which LOGIT does.\n',
    '// No Triola program does this.  The nearest TI-83/84 program, LOGIT\n'
    '//   (logit.zip, ref/triola_ti_programs/LOGIT__257.txt), fits a\n'
    '//   one-predictor logistic model to grouped counts by weighted least\n'
    '//   squares; RiskLab fits any 1-4 predictors by full Newton-Raphson to\n'
    '//   convergence, gives SEs, tests and odds ratios, and detects\n'
    '//   separation, none of which LOGIT does.  LOGIT was read to see what it\n'
    '//   computes; RiskLab was written new in PPL, and none of LOGIT\'s code\n'
    '//   is in it.\n')],
   'The header\'s note on the TI-83/84 program LOGIT begins "No Triola program does this.  The nearest TI-83/84 program, '
   'LOGIT ..." and ends "LOGIT was read to see what it computes; RiskLab was written new in PPL, and none of LOGIT\'s '
   'code is in it." (it began "Replaces / reworks:").'),
 'BurrLab': ('beta1q', 'beta1r', [
   ('// Replaces / reworks: Burr3 v2.4c (fleet).  No TI program is replaced.\n',
    '// Takes the place of Burr3 v2.4c, the fleet\'s own earlier program, and\n'
    '//   reuses the parts of it named above (its header, its drag idiom, its\n'
    '//   log-domain pdf and CDF).  It follows no TI program.\n'),
   ('// BurrLab - beta 1q  (9 Nov 2026) -- the Family map and the tail shades on the G1.\n',
    '// BurrLab - beta 1q  (9 Nov 2026) -- the credits in the words of what was done.\n')],
   'The header\'s line "Replaces / reworks: Burr3 v2.4c (fleet).  No TI program is replaced." now reads "Takes the place '
   'of Burr3 v2.4c, the fleet\'s own earlier program, and reuses the parts of it named above ...  It follows no TI '
   'program."  The paragraph above it, which names the code carried over from Burr3, is unchanged: Burr3 is the '
   'author\'s own program, and the rule asks only that a credit say which code was carried over.'),
 'StatDist': ('v2.7m', 'v2.7n', [
   ('// Author: Roger D. Metcalf, UT Arlington, 2026 (framework after\n'
    '//   S. Micciche).  CRCJ 3340 - Statistics and Introduction to\n'
    '//   Research Methods.  Written with AI assistance (Anthropic\n'
    '//   Claude); concept, direction and all hardware testing by the\n'
    '//   author.\n',
    '// Author: Roger D. Metcalf, UT Arlington, 2026.  CRCJ 3340 -\n'
    '//   Statistics and Introduction to Research Methods.  Written with\n'
    '//   AI assistance (Anthropic Claude); concept, direction and all\n'
    '//   hardware testing by the author.\n'
    '// Does on the Prime, with menus and plots, what Salvo Micciche\'s\n'
    '//   "Statistic Distributions" (hpcalc.org, 2015) does with functions\n'
    '//   typed at Home: it adds distributions the Prime does not have\n'
    '//   built in.  Eleven of the 13 families StatDist adds are families\n'
    '//   his file has.  None of his code is in StatDist: on 15 Nov 2026 his\n'
    '//   494 lines were set beside this program and beside v2.5 and v2.2\n'
    '//   (29 Jul 2026, the oldest copy kept), and not one of his code\n'
    '//   lines, function names or messages is in any of them.\n')],
   'The header said "(framework after S. Micciche)".  It now says what StatDist shares with Salvo Micciche\'s "Statistic '
   'Distributions" (hpcalc.org, 2015), eleven of the 13 families it adds to the Prime\'s own, and that none of his code is '
   'in StatDist: his 494 lines were set beside v2.7m, v2.5 and v2.2 (the oldest copy kept) on 15 Nov 2026.'),
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
    body = ('Round 16: the credits in the words of what was done (Roger, 15 Nov 2026: "reword as the others---look, be '
            'consistent throughout the book").  ' + note + '  Only comments changed, and the version shown: no line of '
            'code.')
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
        # the old label may be QUOTED in the history note, but no line may still begin with it, and the author line
        # may not carry the old parenthesis
        bad = [l[:90] for l in s.split('\n') if re.match(r'^// Replaces / reworks', l) or re.search(r'2026 \(framework after', l)]
        if bad:
            die('%s: the old words are still in the file: %s' % (name, ' | '.join(bad)))
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-10s %s -> %s  (%d changes)' % (name, ov, nv, len(eds)))
