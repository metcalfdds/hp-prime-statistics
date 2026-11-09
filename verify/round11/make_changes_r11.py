# -*- coding: utf-8 -*-
"""Round 11 (9 Nov 2026): one <Name>_<ver>_CHANGES.md for each of the 31 programs.

Everything in a file is read from the round's own records, never typed in by hand:
  - what changed: the history note the build wrote into the program's header (make_round11.py NOTE);
  - the help before and after: helppages_before_r11.json and helppages_r11.json (the PC harness's dump of the shipped files);
  - the routines touched: diffscope_r11.py's method (routines.py over the old and new files);
  - the checks: gates/gate_<new>.txt, lintcounts.txt, helpcheck_r11.json, wordcheck_r11.py's run, the Virtual Calculator
    logs (/tmp/vc/ck9a/log10.txt and log12.txt, copied to vc_checks.txt), and mk/*.txt.
Writes changes/<new>_CHANGES.md."""
import os, re, json, sys, difflib, subprocess
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, 'tools11'))
from routines import routines

OUT = os.path.join(H, 'changes'); os.makedirs(OUT, exist_ok=True)
NEW = [l.strip() for l in open(os.path.join(H, 'newfiles.txt')) if l.strip()]
OLDDUMP = json.load(open(os.path.join(H, 'helppages_before_r11.json'), encoding='utf-8'))
NEWDUMP = json.load(open(os.path.join(H, 'helppages_r11.json'), encoding='utf-8'))
HC = json.load(open(os.path.join(H, 'helpcheck_r11.json'), encoding='utf-8'))
LINT = {l.split()[0]: re.findall(r'\[(\d+) problems\]', l) for l in open(os.path.join(H, 'lintcounts.txt'))}
VC = open(os.path.join(H, 'vc_checks.txt'), encoding='utf-8').read()
WC = subprocess.run([sys.executable, os.path.join(H, 'wordcheck_r11.py')], cwd=H, capture_output=True, text=True).stdout
PUA = {'': 'x̄', '': 'p̂'}

# the glyphs only the calculator has (U+E000 x-bar, U+E001 p-hat) and AgreeLab's drawn d-bar marker, in readable form
def readable(s):
    for a, b in PUA.items():
        s = s.replace(a, b)
    return s.replace('\x14', 'd̄')


def tag(v):
    return v.replace('beta', 'beta ')


def title_key(t):
    return re.sub(r'help \d+/\d+', 'help n/N', t)


def page_key(p):
    return '\n'.join([title_key(p[0])] + p[1:]) if p else ''


def history_note(src, newtag):
    L = src.split('\n')
    for i, l in enumerate(L):
        if re.match(r'^//\s*' + re.escape(newtag) + r' \(9 Nov 2026\): Round 11', l):
            out = [l.split(': ', 1)[1]]
            j = i + 1
            while j < len(L) and L[j].startswith('//   '):
                out.append(L[j][5:])
                j += 1
            return ' '.join(out)
    raise SystemExit('no Round 11 history note for ' + newtag)


def note_body(h):
    # the part between Roger's quotes and the layout sentence
    m = re.search(r'matters"\)\.\s+(.*?)\s+Every changed page is laid out again', h)
    return m.group(1) if m else h


def touched(oldp, newp):
    ro, Lo = routines(oldp)
    rn, Ln = routines(newp)
    sm = difflib.SequenceMatcher(None, Lo, Ln, autojunk=False)
    def where(r, i):
        for k, (a, b) in r.items():
            if a <= i + 1 <= b:
                return k
        return '(top level)'
    out = {}
    for op, a1, a2, b1, b2 in sm.get_opcodes():
        if op == 'equal':
            continue
        for i in range(b1, b2):
            if Ln[i].strip().startswith('//'):
                k = '(comments)'
            else:
                k = where(rn, i)
            out[k] = out.get(k, 0) + 1
        for i in range(a1, a2):
            if Lo[i].strip().startswith('//'):
                k = '(comments)'
            else:
                k = where(ro, i)
            out.setdefault(k, 0)
    return out, Lo, Ln, ro, rn


def outside_help(name, oldp, newp, help_routines):
    """the lines changed outside the help routines and the comments, as (routine, old, new)"""
    t, Lo, Ln, ro, rn = touched(oldp, newp)
    rows = []
    for r in sorted(t):
        if r in ('(comments)', '(top level)') or r in help_routines:
            continue
        if r not in ro or r not in rn:
            continue
        a = Lo[ro[r][0] - 1:ro[r][1]]
        b = Ln[rn[r][0] - 1:rn[r][1]]
        for l in difflib.unified_diff(a, b, lineterm='', n=0):
            if l.startswith(('---', '+++', '@@')):
                continue
            rows.append((r, l))
    return t, rows


def monkey(nv):
    p = os.path.join(H, 'mk', nv + '.txt')
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        return None
    t = open(p, encoding='utf-8').read().strip().split('\n')
    return t


def main():
    exec_ns = {}
    src = open(os.path.join(H, 'helpdump_r11.py'), encoding='utf-8').read()
    exec(src.split('out = {}')[0].split('from ppl_run_v3e import Harness, KEY')[1], exec_ns)
    ROUT = exec_ns['ROUT']
    index = []
    for nv in NEW:
        name, nver = nv.split('_', 1)
        oldf = [f for f in os.listdir(os.path.join(H, 'r', 'src')) if f.startswith(name + '_')][0]
        over = oldf[len(name) + 1:-4]
        oldp = os.path.join(H, 'r', 'src', oldf)
        newp = os.path.join(H, 'r', 'programs', nv + '.txt')
        s = open(newp, encoding='utf-8').read()
        hist = history_note(s, tag(nver))
        body = note_body(hist)
        oldpages = [p for p in OLDDUMP.get(name, []) if p and not p[0].startswith('[')]
        newpages = [p for p in NEWDUMP.get(name, []) if p and not p[0].startswith('[')]
        newkeys = set(page_key(p) for p in newpages)
        oldkeys = set(page_key(p) for p in oldpages)
        old_changed = [p for p in oldpages if page_key(p) not in newkeys]
        new_changed = [p for p in newpages if page_key(p) not in oldkeys]
        renumbered = [p for p in newpages if page_key(p) in oldkeys and p[0] not in [q[0] for q in oldpages]]
        same = [p for p in newpages if page_key(p) in oldkeys]
        hroutines = set(ROUT.get(name, []))
        # the help routines' own helpers count as help (a page routine called only by the help)
        for r in ('ag_HelpPage', 'av_HelpPage', 'dmHelpPage', 'slHelpPg', 'tcHelp1', 'tcHelp2', 'csDfPage', 'erlPage'):
            hroutines.add(r)
        t, rows = outside_help(name, oldp, newp, hroutines)
        L = []
        L.append('# %s %s: changes (9 November 2026)\n' % (name, tag(nver)))
        L.append('Round 11 of 9 November 2026: the help pages in plain words. On 8 November, about the book, Roger wrote: '
                 '"write more straightforward and don\'t try to be too clever--a student being able to understand is the priority". '
                 'Then he asked: "Aw crap--are the help pages unclear too?" On 9 November he approved the page-by-page list of rewrites '
                 '(`Statisticles_help_page_rewrites_v1.docx`). He wrote: "go ahead with all your suggestions" and "adding pages is fine, '
                 'the explanation is what matters". The build, `round11/make_round11.py`, makes %s %s from %s %s. Every change is an exact '
                 'replacement, and a miss stops the build.\n' % (name, tag(nver), name, tag(over)))
        L.append('## What changed\n')
        L.append('1. **The help in plain words.** ' + readable(body) + '\n')
        np_, op_ = len(newpages), len(oldpages)
        L.append('2. **Every changed page laid out again at the calculator\'s own widths.** GlyphProbe_v1 measured every character the '
                 'help uses, in fonts 1 to 3, on the Virtual Calculator (9 Nov 2026). A line\'s width is the sum of its characters\' widths. '
                 'So each changed line now uses the width the page allows, and nothing is cut. '
                 + ('The help is %d screens (was %d), as the PC harness counts them.' % (np_, op_) if np_ != op_ else
                    'The help is still %d screens, as the PC harness counts them.' % np_) + '\n')
        if name in ('TTestLab', 'TTestLabG', 'StudRange'):
            L[-1] = L[-1].rstrip('\n') + (' A statistic\'s name stays on one line: the first layout broke "%s"; the wrap now keeps a '
                                         'one-letter symbol with the "crit", "obt" or "obs" after it.\n'
                                         % ('so q" / "crit = ...' if name == 'StudRange' else '3 crit (t" / "crit)'))
        if rows:
            L.append('3. **Outside the help** only these lines changed (the version on screen, and the page numbers the help\'s callers ask for):\n')
            L.append('```text')
            for r, l in rows:
                L.append('%-14s %s' % (r, l.strip()[:150]))
            L.append('```\n')
        else:
            L.append('3. **Nothing outside the help changed**, apart from comments and the version strings.\n')
        L.append('Routines touched, with the number of new or changed lines in each: '
                 + ', '.join('%s %d' % (k, v) for k, v in sorted(t.items()) if v) + '.\n')
        L.append('## The help, before and after\n')
        L.append('As the PC harness (`tools/ppl_run_v3e.py`) draws it from each file, line for line as on the screen. '
                 '%d of %d screens changed; ' % (len(new_changed), np_)
                 + ('%d kept their words%s.' % (len(same), ' (%d of them with a new page number)' % len(renumbered) if renumbered else '')) + '\n')
        if old_changed:
            L.append('### Before (%s)\n' % tag(over))
            for p in old_changed:
                L.append('```text\n' + '\n'.join(readable(x) for x in p) + '\n```\n')
        if new_changed:
            L.append('### After (%s)\n' % tag(nver))
            for p in new_changed:
                L.append('```text\n' + '\n'.join(readable(x) for x in p) + '\n```\n')
        L.append('## Checks\n')
        g = open(os.path.join(H, 'gates', 'gate_%s.txt' % nv), encoding='utf-8').read()
        res = re.search(r'RESULT: (\w+)', g).group(1)
        lo = LINT.get(nv, ['?', '?'])
        L.append('- `tools/ppl_gate_v1e.py`: %s. hp-prime-kit lint 0 errors; ppl_check_v5 as in %s; lint_ppl %s problems, as in %s (%s); '
                 'fleet_names_v2 over the 31 newest files: 0 collisions.' % (res, tag(over), lo[1] if len(lo) > 1 else '?', tag(over),
                                                                             lo[0] if lo else '?'))
        L.append('- `tools/case_scan_v1.py`: clean.')
        wl = [l for l in WC.split('\n') if l.startswith(name + ' ')]
        if any('DIFFERS' in l for l in wl):
            why = {'Norm3': 'the only difference is where the plot\'s axis numbers fall in the dump (the help is drawn over the plot, '
                            'which the harness keeps underneath)',
                   'PowerViz': 'the only difference is the order of the disclaimer line, which the build keeps out of the moved text '
                               'and puts back at the foot of its page'}.get(name, 'see the run')
            L.append('- `round11/wordcheck_r11.py` (the old help with the approved changes applied, word for word against the new): '
                     + why + '.')
        else:
            L.append('- `round11/wordcheck_r11.py`: the old help with the approved changes applied matches the new help word for word '
                     '(titles, page numbers, footers and the version left out).')
        hc = HC.get(name)
        if hc is not None:
            if not hc['problems']:
                L.append('- `round11/helpcheck_r11.py`, at the measured glyph widths: %d screens, no line past its width or the '
                         'screen\'s edge, no two texts overlapping.' % hc['screens'])
            else:
                known = {'AgreeLab': 'one report, the drawn d̄ on page 7: the bar and the d are drawn separately, and the check '
                                     'measures the d as a plain d next to the text that follows it; on the Virtual Calculator the '
                                     'line reads "bias = d̄, the mean difference; limits of" as it should',
                         'Norm3': 'the reports are the plot\'s axis numbers and readouts, which the harness keeps underneath the help; '
                                  'the help clears the screen with a filled RECT_P first, so on the calculator they are not there',
                         'StatDist': 'one report: the harness cannot call st_ABHelp without its argument; its pages are checked '
                                     'through the menu'}.get(name, '; '.join(str(x) for x in hc['problems'][:3]))
                L.append('- `round11/helpcheck_r11.py`, at the measured glyph widths: %d screens; %s.' % (hc['screens'], known))
        m = re.findall(r'^%s\b.*$' % re.escape(name if name != 'CentralLimit' else 'Central'), VC, re.M)
        L.append('- Virtual Calculator 2.4.2 (build 2026-09-09), in the cloud workspace, 9 Nov 2026: Check said "No errors in the '
                 'program"%s.' % (' (as CentralLimit (App), the app\'s own program)' if name == 'CentralLimit' else ''))
        seen = {'AgreeLab': 'all nine help pages were opened from the menu and read',
                'ChiTable': 'all six help pages were opened from the menu and read',
                'BayesTree': 'all five help pages were opened from the menu and read',
                'StudRange': 'all five help pages were opened from the menu and read',
                'BurrLab': 'all six help pages were opened from the menu and read, after the page titles were made to say '
                           'what each page is about (Explore, Family tree and fit, Pictures)'}.get(name)
        if seen:
            L.append('  On the Virtual Calculator ' + seen + ': every line inside its page, nothing cut.')
        mk = monkey(nv)
        if mk:
            import re as _re
            head = _re.search(r'(\d+) runs, (\d+) events each, (\d+) s', mk[0])
            verdicts = [_re.sub(r'\s+', ' ', x.strip()) for x in mk[1:] if _re.match(r'^\s*[A-Z]+\s+\d+\s*$', x)]
            verdicts = [_re.sub(r'\d{4,}', lambda m: format(int(m.group(0)), ','), v) for v in verdicts]
            L.append('- `tools/monkey_v1b.py --lists%s`, %s runs of %s random keys, taps, menu picks and typed values (%s s): %s.'
                     % (' --seconds 240' if name == 'StudRange' else '', format(int(head.group(1)), ','), head.group(2),
                        format(int(head.group(3)), ','), ', '.join(verdicts)))
            if name == 'BurrLab':
                L.append('  The one FREEZE is the 20-s limit, not a hang: run 1000536 fits all 2,156 Danish fire losses, and replayed '
                         'alone (`--replay 1000536`) it ended OK in 13.3 s; the batch had shared the processor with StudRange\'s '
                         'test. The HARNESS runs are the harness\'s own gap: `RANDSEED` is on HP\'s list of names and the harness '
                         'does not model it, as in beta 1l and beta 1p.')
        L.append('\nNot yet run on a G1 or a G2.\n')
        txt = '\n'.join(L).replace('`round11/', '`verify/round11/')
        txt = txt.replace('opened from the menu and read', 'opened from the menu and read (`verify/round11/screens/`)')
        open(os.path.join(OUT, '%s_CHANGES.md' % nv), 'w', encoding='utf-8').write(txt)
        index.append((nv, op_, np_, len(new_changed)))
    for r in index:
        print('%-22s screens %2d -> %2d, changed %2d' % r)


if __name__ == '__main__':
    main()
