# -*- coding: utf-8 -*-
"""walk_detail_r17.py -- what the generic walk of TTestLabG beta 1i finds that the walk of beta 1h did not (17 Nov 2026).
records_r17.py's line T for TTestLabG says "not the old version's report": 19 overruns where the old version had 18.  This script
walks both versions again (the old one read from git, BASE), compares the two lists of overruns text for text, and measures every finding
that is only in one of them at the glyph widths GlyphProbe_v1 read on the Virtual Calculator (verify/round11/tools11/hp11.py).
The walk's own widths are estimates, 6.5 px a character at font 1 (tools/text_overlap_v1.py, CW), and a finding is "firm" only
when it is still there at 5.5 px a character.
Writes verify/round17/overlap_TTestLabG_detail.txt.  Run from the repository's root, with hp-prime-kit at $HPKIT; about 30 s."""
import json, os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.dirname(os.path.dirname(HERE)); os.chdir(REPO)
sys.path.insert(0, os.path.join(REPO, 'verify', 'round11', 'tools11'))
import hp11  # noqa: E402
BASE = '39bb935'; OLD = 'TTestLabG_beta1h.txt'; NEW = 'TTestLabG_beta1i.txt'
tmp = tempfile.mkdtemp(prefix='r17walk_')
open(os.path.join(tmp, OLD), 'w', encoding='utf-8').write(subprocess.run(['git', 'show', '%s:programs/%s' % (BASE, OLD)], capture_output=True, text=True, check=True).stdout)
subprocess.run([sys.executable, 'tools/text_overlap_v1.py', '--walk', os.path.join(tmp, OLD), '--json', os.path.join(tmp, 'old.json')], capture_output=True, text=True, check=True)
o = json.load(open(os.path.join(tmp, 'old.json'), encoding='utf-8'))['results'][OLD]['findings']
subprocess.run([sys.executable, 'tools/text_overlap_v1.py', '--walk', os.path.join('programs', NEW), '--json', os.path.join(tmp, 'new.json')], capture_output=True, text=True, check=True)
n = json.load(open(os.path.join(tmp, 'new.json'), encoding='utf-8'))['results'][NEW]['findings']
def key(x): return (x['text'], x['x'], x['y'], x['right'], x['firm'])
def gw(t): return sum(hp11.GW[ord(c)][0] for c in t)
out = ['TTestLabG: the overruns of the two generic walks, text for text (verify/round17/walk_detail_r17.py)', '']
for kind in ('collisions', 'straddles', 'ghosts'):
    out.append('%-10s new %d, old %d' % (kind, len(n[kind]), len(o[kind])))
    assert len(n[kind]) == len(o[kind]), kind
a, b = {key(x) for x in n['overruns']}, {key(x) for x in o['overruns']}
out.append('%-10s new %d (firm %d), old %d (firm %d)' % ('overruns', len(a), sum(k[4] for k in a), len(b), sum(k[4] for k in b)))
out.append('')
for label, s in (('only in the new version\'s walk', a - b), ('only in the old version\'s walk', b - a)):
    out.append('%s: %d' % (label, len(s)))
    for t, x, y, right, firm in sorted(s):
        w = gw(t)
        out.append('   "%s"' % t)
        out.append('   at x = %d, y = %d, font 1; %d characters; the walk\'s estimate of its right edge: %d (%s); at the calculator\'s glyph widths it is '
                   '%d px wide and ends at x = %d, %d px inside the screen\'s 320' % (x, y, len(t), right, 'firm' if firm else 'marginal: not there at 5.5 px a character', w, x + w, 320 - (x + w)))
        assert not firm and x + w < 318, t
assert len(a - b) == 1 and not (b - a) and sum(k[4] for k in a) == sum(k[4] for k in b)
out += ['', 'The line grew by the four parentheses of "(N₁-1), (N₂-1)", from 46 characters to 50, and 50 characters at the walk\'s 6.5 px',
        'pass 320.  The same line with the largest count the forms allow (N is at most 1,000,000), "... = 999,999,", is %d px wide and ends at x = %d.'
        % (gw(u'By hand: df = the smaller of (N₁-1), (N₂-1) = 999,999,'), 8 + gw(u'By hand: df = the smaller of (N₁-1), (N₂-1) = 999,999,'))]
open(os.path.join(HERE, 'overlap_TTestLabG_detail.txt'), 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out))
shutil.rmtree(tmp, ignore_errors=True)
