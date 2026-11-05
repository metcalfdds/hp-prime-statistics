#!/usr/bin/env python3
"""verify_round7_labels_v1.py -- checks round 7's four label-only programs (4 Nov 2026): TTestLab beta 1e,
TTestLabG beta 1c, ChiTable beta 3i and ErrorRate beta 1g.  EpiStats v1.7h, which changed its arithmetic too, has
its own script (verify_EpiStats_v1.7h.py).

For each program, against the version before it (from programs/, a _superseded folder or git history):
  L1  with comments taken out, the code differs only in the lines the change note names, and each of those lines
      differs only inside its string literals (the text the student sees), never in the code around them;
  L2  the new strings are the ones the change note gives, and the old ones are gone;
  L3  the header's first line names the new version.
The monkey test (1,000 runs each, all OK) and the Virtual Calculator run are in the round's commit message.
Run from the repository:  python3 verify/verify_round7_labels_v1.py"""
import os, re, sys, subprocess, tempfile, glob
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import comma_check_v1 as CC  # noqa: E402
FAIL, NPASS = [], [0]


def check(name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + name + (('   ' + str(detail)[:500]) if detail != '' and not ok else ''))
    (FAIL.append(name) if not ok else NPASS.__setitem__(0, NPASS[0] + 1))


def older(name):
    for p in [os.path.join(ROOT, 'programs', name)] + sorted(glob.glob(os.path.join(ROOT, '..', '_superseded_*', name)), reverse=True) \
            + sorted(glob.glob(os.path.join(ROOT, '_old', name))):
        if os.path.exists(p):
            return p
    rel = 'programs/' + name
    try:
        c = subprocess.run(['git', '-C', ROOT, 'rev-list', '-n', '1', 'HEAD', '--', rel], capture_output=True, text=True).stdout.strip()
        for ref in ((c + ':' + rel, c + '^:' + rel) if c else ()):
            o = subprocess.run(['git', '-C', ROOT, 'show', ref], capture_output=True)
            if o.returncode == 0:
                p = os.path.join(tempfile.mkdtemp(), name)
                open(p, 'wb').write(o.stdout)
                return p
    except Exception:
        pass
    return None


def strings_out(line):
    return re.sub(r'"[^"]*"', '""', line)


R = [  # new file, old file, header line, (old string, new string) pairs
    ('TTestLab_beta1e.txt', 'TTestLab_beta1d.txt', '// TTESTLAB - beta 1e',
     [('Tap Yes or No (or the soft keys); OK = go on', 'Tap Yes or No (or the soft keys); Run = run the test'),
      ('"OK"});', '"Run"});'),
      ('The flowchart: tap Yes or No; OK = go on', 'The flowchart: tap Yes or No; Run = run the test')]),
    ('TTestLabG_beta1c.txt', 'TTestLabG_beta1b.txt', '// TTESTLABG - beta 1c',
     [('Tap Yes or No (or the soft keys); OK = go on', 'Tap Yes or No (or the soft keys); Run = run the test'),
      ('"OK"});', '"Run"});'),
      ('The flowchart: tap Yes or No; OK = go on', 'The flowchart: tap Yes or No; Run = run the test')]),
    ('ChiTable_beta3i.txt', 'ChiTable_beta3h.txt', '// CHITABLE - beta 3i',
     [('Party ID by gender (GSS 1991, Agresti)', 'Party ID by gender (GSS 2000, Agresti)')]),
    ('ErrorRate_beta1g.txt', 'ErrorRate_beta1f.txt', '// ERRORRATE LAB - beta 1g',
     [('Nothing here has run on a calculator yet.', 'It has run on the Virtual Calculator.')]),
]
for new, old, hdr, pairs in R:
    pn, po = os.path.join(ROOT, 'programs', new), older(old)
    print('=== %s against %s' % (new, os.path.relpath(po, ROOT) if po else 'NOT FOUND'))
    if not po:
        check(new + ' older version found', False)
        continue
    sn, so = open(pn, encoding='utf-8').read(), open(po, encoding='utf-8').read()
    cn, co = CC.strip_comments(sn).split('\n'), CC.strip_comments(so).split('\n')
    cn, co = [l for l in cn if l.strip()], [l for l in co if l.strip()]
    ok = len(cn) == len(co)
    changed = [(a, b) for a, b in zip(co, cn) if a != b] if ok else []
    bad = [(a, b) for a, b in changed if strings_out(a) != strings_out(b)]
    check('L1 %s: the code differs only inside string literals, in %d line(s)' % (new, len(changed)),
          ok and not bad and 0 < len(changed) <= len(pairs) + 1, bad[:3] if ok else 'line counts differ')
    miss = [(a, b) for a, b in pairs if a in CC.strip_comments(sn) or b not in sn]
    check('L2 %s: the new strings are there and the old ones gone (%d pair(s))' % (new, len(pairs)), not miss, miss)
    check('L3 %s: the header names the version' % new, hdr in sn.split('\n')[3] or hdr in sn[:400], sn[:200])
print('\n%d PASS, %d FAIL' % (NPASS[0], len(FAIL)))
for f in FAIL:
    print('  FAILED: ' + f)
sys.exit(1 if FAIL else 0)
