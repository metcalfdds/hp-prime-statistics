# -*- coding: utf-8 -*-
"""Round 14 (14 Nov 2026), the wording part: CICatcher's help pages 2 and 6.

The status note of the book *Statisticles* had carried one leftover since Round 12: CICatcher's help page 2 still said "the
catch rate rises", a term no page explains (page 1 calls it the share of intervals the method catches, and "the 'all' rate
at the top of the screen").  Roger, 14 Nov 2026: "go ahead and do the program work".

Every change is an exact replacement in the version before (read from git, BASE below); a replacement that does not match
exactly once stops the build.  The program then gets its next version: the header line, a history note, and every version
string in a literal (as Rounds 11 and 12 did).  Run from the repository's root:
    python3 verify/round14/make_round14.py OUTDIR
ScatterLab beta 2k and TTestLab beta 1k, the round's other two programs, are new code and have their own notes and scripts.
"""
import io, os, re, subprocess, sys, textwrap

BASE = '26912a9'                     # main before Round 14
DATE = '14 Nov 2026'
OUT = sys.argv[1] if len(sys.argv) > 1 else 'r14_programs'

EDITS = {
 'CICatcher': ('beta2j', 'beta2k', [
   ('"value, so EVERY line grows, red lines turn blue and the catch rate",',
    '"value, so EVERY line grows, red lines turn blue and the share",'),
   ('"rises. 99 % catches more, but its longer lines give a less",',
    '"caught rises. 99 % catches more, but its longer lines give a less",'),
   ('"CQ_COVER (the \'all\' catch rate)."},', '"CQ_COVER (the \'all\' rate)."},')],
   'Help page 2/6 says "the share caught rises" where it said "the catch rate rises", and help page 6/6 says "the \'all\' '
   'rate" where it said "the \'all\' catch rate": page 1 explains the share of intervals the method catches and "the '
   '\'all\' rate at the top of the screen", and no page explained a "catch rate".'),
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
    if hv is not None:
        L[hv] = L[hv].replace(ot, nt)
        L[hv] = re.sub(r'\((\d+ Nov 2026[^)]*)\)', '(%s)' % DATE, L[hv], count=1)
    hist = [i for i, l in enumerate(L) if re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', l)]
    if not hist:
        die(name + ': no history line for ' + ot)
    body = ('Round 14: one leftover of the book\'s read (Roger, 14 Nov 2026: "go ahead and do the program work").  '
            + note + '  No other line changed.')
    L.insert(hist[0], '// %s (%s): ' % (nt, DATE) + '\n//   '.join(textwrap.wrap(body, 100)))
    s = '\n'.join(L)
    s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace(ot, nt).replace(ov, nv), s)
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
        io.open(os.path.join(OUT, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8', newline='').write(s)
        print('%-10s %s -> %s  (%d changes)' % (name, ov, nv, len(eds)))
