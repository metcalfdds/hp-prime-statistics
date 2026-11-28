#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_verify_tlg_1k.py -- round 21: verify/verify_TTestLabG_beta1k.py from verify/verify_TTestLab_beta1n.py, the advanced
version's script with the general version's names (CLAUDE.md: derive the general version's verify script from the
advanced one's the same way).  Only the block between the two "what differs" rulers changes, and the title.
Run from the repository's root:   python3 verify/round21/make_verify_tlg_1k.py"""
import io, sys
s = io.open('verify/verify_TTestLab_beta1n.py', encoding='utf-8').read()


def rep(a, b):
    global s
    if s.count(a) != 1: sys.exit('STOPPED: %d matches for %r' % (s.count(a), a[:70]))
    s = s.replace(a, b)


rep('"""verify_TTestLab_beta1n.py -- checks TTestLab beta 1n (28 Nov 2026, round 21)',
    '"""verify_TTestLabG_beta1k.py -- checks TTestLabG beta 1k (28 Nov 2026, round 21; made from verify_TTestLab_beta1n.py\nby round21/make_verify_tlg_1k.py)')
rep("NAME, OLDNAME = 'TTestLab_beta1n.txt', 'TTestLab_beta1m.txt'", "NAME, OLDNAME = 'TTestLabG_beta1k.txt', 'TTestLabG_beta1j.txt'")
rep("VER, OLDVER, PROGNAME, ENTRY, TAG = 'beta 1n', 'beta 1m', 'TTestLab', 'TTESTLAB()', 'tt'",
    "VER, OLDVER, PROGNAME, ENTRY, TAG = 'beta 1k', 'beta 1j', 'TTestLabG', 'TTESTLABG()', 'tz'")
rep("EXAMPLES = (1, 2, 3, 4, 5, 6)                      # tt_Example's numbers", "EXAMPLES = (1, 2, 3, 4, 5, 6, 7)                   # tz_Example's numbers")
rep("CHANGED = ('Step2', 'Step4', 'Step4N', 'BookNote', 'Help')", "CHANGED = ('Step2', 'Step4', 'Step4N', 'Help')")
rep("check('A2 the routines that changed are the five the note names: %s'", "check('A2 the routines that changed are the four the note names: %s'")
rep("HELP_NEW = ('Steps 2 and 4 work each number from those shown above it, so',\n            'each step checks; rounding sooner can change t obt (example 1)')",
    "HELP_NEW = ('Steps 2 and 4 work each number from those shown, so all check.',)")
rep("HELP_OLD = ('Step 4 keeps 4 significant digits at each step; rounding sooner', 'can change t obt (see example 1)')",
    "HELP_OLD = ('Step 4 keeps 4 significant digits at each step.',)")
rep("tmp = tempfile.mkdtemp(prefix='tl1n_')", "tmp = tempfile.mkdtemp(prefix='tg1k_')")
rep("Run from anywhere:   python3 verify/verify_TTestLab_beta1n.py        (beta 1m comes from git)",
    "Run from anywhere:   python3 verify/verify_TTestLabG_beta1k.py        (beta 1j comes from git)")
io.open('verify/verify_TTestLabG_beta1k.py', 'w', encoding='utf-8').write(s)
print('verify_TTestLabG_beta1k.py written')
