"""Round 11: every help screen of a program, laid out at the calculator's own glyph widths (GlyphProbe_v1):
a line past its width argument or the screen's edge, and two texts that overlap, are reported."""
import sys, os, re, json, signal
sys.path.insert(0, 'tools')
sys.path.insert(0, '../tools11')
sys.setrecursionlimit(20000)
from ppl_run_v3e import Harness
import hp11
exec(open('../helpdump_r11.py').read().split('out = {}')[0].split('from ppl_run_v3e import Harness, KEY')[1])  # ROUT
MAIN = {'NormExplorer': 'NormExp()', 'PowerViz': 'POWERVIZ()', 'TTestLab': 'TTESTLAB()', 'TTestLabG': 'TTESTLABG()',
        'DataLoad': 'DATALOAD()', 'Norm3': 'Norm3(0,1,1.96)'}
H = {1: 10, 2: 12, 3: 14, 0: 12}


def w(t, f):
    tot = 0
    for ch in t:
        c = ord(ch)
        f = int(f or 2)
        tot += hp11.GW[c][f - 1] if c in hp11.GW and 1 <= f <= 3 else 8
    return tot


class TO(Exception):
    pass


def alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, alarm)
rep = {}
for f in sys.argv[1:]:
    name = os.path.basename(f).split('_')[0]
    probs, nscr = [], 0
    for r in ROUT[name]:
        try:
            signal.alarm(120)
            h = Harness(f, idle_key=4, on_unverified='warn')
            try:
                h.execute(MAIN.get(name, name + '()'))
            except Exception:
                pass
            h.screens[:] = []
            for i in range(60):
                h.press(30)
            try:
                if name in ('AgreeLab', 'AnovaLab'):
                    for k in range(1, 12):
                        try:
                            h.execute('%s(%d)' % (r, k))
                        except Exception:
                            break
                else:
                    h.call(r)
            except Exception as e:
                probs.append('call %s: %s' % (r, str(e)[:80]))
            signal.alarm(0)
        except TO:
            probs.append('timed out')
            continue
        seen = set()
        for s in h.screens:
            key = '\n'.join(s.lines())
            if key in seen:
                continue
            seen.add(key)
            nscr += 1
            T = [t for t in s.texts if t.text and t.text.strip()]
            title = next((t.text for t in T if ' help' in t.text), '?')
            for t in T:
                ww = w(t.text, t.font)
                lim = 318 - t.x
                if t.width:
                    lim = min(lim, t.width)
                if ww > lim:
                    probs.append('%s: CUT %d > %d px: %r' % (title[:30], ww, lim, t.text[:60]))
            for i in range(len(T)):
                for j in range(i + 1, len(T)):
                    a, b = T[i], T[j]
                    ay0, ay1 = a.y, a.y + H.get(int(a.font or 0), 12)
                    by0, by1 = b.y, b.y + H.get(int(b.font or 0), 12)
                    if ay0 < by1 - 1 and by0 < ay1 - 1:
                        ax0, ax1 = a.x, a.x + min(w(a.text, a.font), a.width or 999)
                        bx0, bx1 = b.x, b.x + min(w(b.text, b.font), b.width or 999)
                        if ax0 < bx1 and bx0 < ax1:
                            probs.append('%s: OVERLAP %r (y %d) / %r (y %d)' % (title[:30], a.text[:30], a.y, b.text[:30], b.y))
    rep[name] = {'screens': nscr, 'problems': probs}
    print(name, nscr, len(probs), flush=True)
    for p in probs[:12]:
        print('   ', p)
# a run over some programs updates their entries and keeps the others' (9 Nov 2026)
_all = json.load(open('../helpcheck_r11.json')) if os.path.exists('../helpcheck_r11.json') else {}
_all.update(rep)
json.dump(_all, open('../helpcheck_r11.json', 'w'), indent=1, ensure_ascii=False)
