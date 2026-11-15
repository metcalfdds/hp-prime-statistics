# -*- coding: utf-8 -*-
"""Round 14: verify_TTestLabG_beta1h.py from verify_TTestLab_beta1k.py, by exact replacements (a miss stops it), as the
general program is made from the advanced one.  Only the lines that name the program change: its files, its entry
point and tag, how many older examples it has and which they are, that it has no printed-table note, and the years its
examples' sources carry.   Run from the repository's root:   python3 verify/round14/make_verify_tlg_1h.py
"""
import io, sys
s = io.open('verify/verify_TTestLab_beta1k.py', encoding='utf-8').read()

def rep(a, b, n=1):
    global s
    if s.count(a) != n: sys.exit('STOPPED: %d matches (wanted %d) for %r' % (s.count(a), n, a[:80]))
    s = s.replace(a, b)

rep('"""verify_TTestLab_beta1k.py -- checks TTestLab beta 1k (14 Nov 2026, round 14): three more tests in the same five',
    '"""verify_TTestLabG_beta1h.py -- checks TTestLabG beta 1h (14 Nov 2026, round 14), the general version, built from\n'
    'TTestLab beta 1k by tools/make_tlg1_v3.py.  This script is verify_TTestLab_beta1k.py with the program\'s names changed\n'
    '(verify/round14/make_verify_tlg_1h.py); "beta 1j" below reads beta 1g, the general version before.  Three more tests in the same five')
rep("NAME, OLDNAME = 'TTestLab_beta1k.txt', 'TTestLab_beta1j.txt'", "NAME, OLDNAME = 'TTestLabG_beta1h.txt', 'TTestLabG_beta1g.txt'")
rep("VER, PROGNAME, ENTRY, TAG = 'beta 1k', 'TTestLab', 'TTESTLAB()', 'tt'", "VER, PROGNAME, ENTRY, TAG = 'beta 1h', 'TTestLabG', 'TTESTLABG()', 'tz'")
rep("NOLD = 3                                           # the older examples: start-menu items 2 to NOLD + 1",
    "NOLD = 4                                           # the older examples: start-menu items 2 to NOLD + 1")
rep("EX_POOLED, PAIRS = 1, (2,)                         # which older example is pooled, and which are dependent samples",
    "EX_POOLED, PAIRS = 3, (1, 4)                       # which older example is pooled, and which are dependent samples")
rep("HAS_TABLE = True                                   # the advanced version reads the printed t table's row too",
    "HAS_TABLE = False                                  # the general version gives the exact t critical only")
rep("YEARS = ('Student 1908', 'Delacre et al. 2017')    # numbers the program writes as text: no comma",
    "YEARS = ('Student 1908', 'Darwin 1876', 'Selective Service, 1970', 'Delacre 2017')    # numbers the program writes as text: no comma")
rep('Run from anywhere:   python3 verify/verify_TTestLab_beta1k.py', 'Run from anywhere:   python3 verify/verify_TTestLabG_beta1h.py')
io.open('verify/verify_TTestLabG_beta1h.py', 'w', encoding='utf-8', newline='').write(s)
print('verify_TTestLabG_beta1h.py written')
