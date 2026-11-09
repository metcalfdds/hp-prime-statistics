# -*- coding: utf-8 -*-
"""Round 11 (9 Nov 2026): the help pages in plain words.

Roger, 8 Nov 2026, on the book's wording: "write more straightforward and don't try to be too clever--a student being
able to understand is the priority"; then "Aw crap--are the help pages unclear too?"; and on 9 Nov, of the page-by-page
list of rewrites (Statisticles_help_page_rewrites_v1.docx): "go ahead with all your suggestions", "adding pages is fine,
the explanation is what matters", "please drop 'as the lecture'".

Every changed help page is laid out again at the calculator's own glyph widths (GlyphProbe_v1, Virtual Calculator,
9 Nov 2026), so a line uses the page's width and nothing is cut; a page that no longer fits becomes two.  The approved
wording comes from helpsweep/proposals.py, applied by exact text (a miss stops the build)."""
import io, os, re, sys, textwrap
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, 'tools11'))
import hp11
from hp11 import Parser, find_consts, W, lit, norm
from pagea import Page, if_blocks
import pagea
import props
from routines import routines

SRC = os.path.join(H, 'r', 'src')
DST = os.path.join(H, 'r', 'programs'); os.makedirs(DST, exist_ok=True)
hp11.GW[0x14] = hp11.GW[ord('d')]          # AgreeLab's drawn d-bar: the width of its d

VER = {}
NOTE = {}
DONE = {}
REPORT = []


def tag(v):
    return v.replace('beta', 'beta ')


def die(msg):
    sys.exit('BUILD STOPPED: ' + msg)


def must_replace(s, a, b, n=1, who=''):
    if s.count(a) != n:
        die('%s: %d (want %d) x %r' % (who, s.count(a), n, a[:120]))
    return s.replace(a, b)


# ------------------------------------------------------------------ pages drawn at fixed y, in IF k == n blocks
def ifpages(name, s, routine, var, call, cm, font, maxw, step, ymax, title_re, loose=True, topics=None,
            pre=None, post=None, specials=None, exclude_re=None):
    """rewrites the changed pages of one IF-block help routine.  Returns (new source, map old page -> new pages, N)."""
    pagea.LOOSE[0] = loose
    L = s.split('\n')
    consts = find_consts(s)
    hp11.set_rev(consts)
    r, _ = routines_from_text(s)
    a, b = r[routine]
    blocks = if_blocks(L, a, b, var)
    par = Parser(consts, cmfuncs=cm)
    P = props.for_prog(name)
    built = {}
    for k, (ba, bb) in blocks.items():
        if k not in P:
            continue
        if pre:
            pre(k, L, ba, bb)
        pg = Page(L, ba, bb, call, par, font=font, maxw=maxw, step=step, exclude=exclude_re)
        for o, n in P[k]:
            try:
                pg.apply(o, n)
            except KeyError as e:
                die('%s page %d: %s' % (name, k, e))
        pg.reflow_all()
        placed = pg.place(ymax=ymax)
        pg.check(placed)
        for p in placed:
            bad = pg.width_report(p)
            if bad:
                die('%s page %d: too wide %r' % (name, k, bad))
        built[k] = (pg, placed)
        REPORT.append('%s page %d: %d lines -> %s' % (name, k, len(pg.lines), '+'.join(str(len(p)) for p in placed)))
    # the new numbering
    newnum, n = {}, 0
    for k in sorted(blocks):
        cnt = len(built[k][1]) if k in built else 1
        newnum[k] = list(range(n + 1, n + cnt + 1))
        n += cnt
    N = n
    # rebuild the routine's blocks, last first so line numbers hold
    for k in sorted(blocks, reverse=True):
        ba, bb = blocks[k]
        blk = L[ba - 1:bb]
        ind = re.match(r'^(\s*)', blk[0]).group(1)
        # the title line (a page whose title is drawn outside its block has none here, and cannot be split)
        if title_re is None:
            if k in built and len(built[k][1]) > 1:
                die('%s page %d needs a second page, and its title is outside its block' % (name, k))
            if k in built:
                pg, placed = built[k]
                text_idx = set(l.idx for l in pg.lines)
                code = pg.emit(placed[0])
                if post:
                    code = post(k, 0, code)
                first = min(text_idx) - (ba - 1)
                rest = [l for j, l in enumerate(blk) if (ba - 1 + j) not in text_idx]
                # the text goes where the first text line was; everything else keeps its order
                out, put = [], False
                for j, l in enumerate(blk):
                    if (ba - 1 + j) in text_idx:
                        if not put:
                            out += code
                            put = True
                        continue
                    out.append(l)
                L[ba - 1:bb] = out
            continue
        ti = next(i for i, l in enumerate(blk) if title_re.search(l))
        tline = blk[ti]
        m = title_re.search(tline)
        topic = m.group('topic')
        if k not in built:
            new_t = title_re.sub(lambda mm: mm.group('lead') + '%d/%d: ' % (newnum[k][0], N) + mm.group('topic'), tline)
            blk[ti] = new_t
            blk[0] = re.sub(r'== \d+ THEN', '== %d THEN' % newnum[k][0], blk[0])
            L[ba - 1:bb] = blk
            continue
        pg, placed = built[k]
        out = []
        for pi, page in enumerate(placed):
            num = newnum[k][pi]
            tp = topic if pi == 0 else (topics or {}).get((k, pi), topic + ' (continued)')
            out.append(re.sub(r'== \d+ THEN', '== %d THEN' % num, blk[0]))
            nt = title_re.sub(lambda mm: mm.group('lead') + '%d/%d: ' % (num, N) + tp_code(tp, mm), tline)
            out.append(nt)
            # every line of the block that is not a text call, the title or the IF/END stays (and is reported)
            text_idx = set(l.idx for l in pg.lines)
            for j, l in enumerate(blk[1:-1], start=ba):
                if j in text_idx or j == ba - 1 + ti:
                    continue
                if l.strip() and not l.strip().startswith('//'):
                    if pi == 0:
                        out.append(l)
                        REPORT.append('%s page %d: kept a non-text line: %s' % (name, k, l.strip()[:80]))
            code = pg.emit(page)
            if post:
                code = post(k, pi, code)
            out += code
            out.append(blk[-1])
        L[ba - 1:bb] = out
    s2 = '\n'.join(L)
    return s2, newnum, N, built


def tp_code(tp, mm):
    """the topic as it appears in the title's code: the original topic code when unchanged"""
    return tp


def routines_from_text(s):
    import tempfile
    p = os.path.join(H, '_tmp_routines.txt')
    io.open(p, 'w', encoding='utf-8').write(s)
    return routines(p)


def top_args(call_text):
    """the top-level arguments of the first call on a line: (prefix up to '(', [args], suffix after ')')"""
    i = call_text.index('(')
    depth, j, start, args, instr = 0, i, i + 1, [], False
    while j < len(call_text):
        ch = call_text[j]
        if ch == '"':
            instr = not instr
        elif not instr:
            if ch == '(':
                depth += 1
            elif ch == ')':
                depth -= 1
                if depth == 0:
                    args.append(call_text[start:j])
                    return call_text[:i + 1], args, call_text[j:]
            elif ch == ',' and depth == 1:
                args.append(call_text[start:j])
                start = j + 1
        j += 1
    raise ValueError('unbalanced: ' + call_text)


def check_title(name, expr, par, maxw, font=2):
    try:
        segs = par.parse(expr.strip())
    except Exception:
        return
    if all(x.kind == 't' for x in segs):
        t = ''.join(x.text for x in segs)
        if W(t, font) > maxw:
            die('%s: the title %r is %d px, over %d' % (name, t, W(t, font), maxw))


def renum(text, old_k, old_N, k, N):
    return re.sub(r'(?<![\d/])%d/%d(?![\d/])' % (old_k, old_N), '%d/%d' % (k, N), text)


def sections(name, s, routine, start_re, end_re, turn, call, cm, font, maxw, ymax, loose=True, topics=None,
             title_arg=0, post=None, ytext=None, split_turn=None, footer_re=None, rep_re=None, foot_custom=None, skip=(), exclude_re=None):
    """help pages drawn one after another in one routine.  A page starts at the line matching start_re (holding
    "<Name> help k/N", the title) and its text ends before the next line matching end_re.  A split page repeats the
    program's own page turn: by default the lines from page 1's end line up to page 2's title (a BLIT_P, the wait,
    the clearing), or the 'turn' lines after the end line (TDist3D's style, where the end call draws the footer)."""
    pagea.LOOSE[0] = loose
    L = s.split('\n')
    consts = find_consts(s)
    hp11.set_rev(consts)
    r, _ = routines_from_text(s)
    a, b = r[routine]
    par = Parser(consts, cmfuncs=cm)
    P = props.for_prog(name)
    starts = [i for i in range(a - 1, b) if start_re.search(L[i])]
    pages = {}
    oldN = None
    for i in starts:
        m = re.search(r'%s help (\d+)/(\d+)' % re.escape(name), L[i])
        k, oldN = int(m.group(1)), int(m.group(2))
        e = i + 1
        while not end_re.search(L[e]):
            e += 1
        pages[k] = (i, e)
    ks = sorted(pages)
    built = {}
    for k, (i, e) in pages.items():
        if k not in P or k in skip:
            continue
        pg = Page(L, i + 2, e, call, par, font=font, maxw=maxw, ylimit=ytext, exclude=exclude_re)
        for o, n in P[k]:
            try:
                pg.apply(o, n)
            except KeyError as ex:
                die('%s page %d: %s' % (name, k, ex))
        pg.reflow_all()
        placed = pg.place(ymax=ymax.get(k, ymax['*']) if isinstance(ymax, dict) else ymax)
        pg.check(placed)
        for p in placed:
            if pg.width_report(p):
                die('%s page %d: too wide %r' % (name, k, pg.width_report(p)))
        built[k] = (pg, placed)
        REPORT.append('%s page %d: %d lines -> %s' % (name, k, len(pg.lines), '+'.join(str(len(p)) for p in placed)))
    newnum, n = {}, 0
    for k in range(1, oldN + 1):             # every page, those drawn by another routine too
        cnt = len(built[k][1]) if k in built else 1
        newnum[k] = list(range(n + 1, n + cnt + 1))
        n += cnt
    N = n
    # the program's own page turn, for split pages
    if turn:
        e1 = pages[ks[0]][1]
        own_turn = lambda num: [renum(L[e1], ks[0], oldN, num - 1, N)] + L[e1 + 1:e1 + 1 + turn]
    else:
        e1, s2 = pages[ks[0]][1], pages[ks[1]][0] if len(ks) > 1 else None
        own_turn = lambda num: L[e1:s2]
    for k in sorted(pages, reverse=True):
        i, e = pages[k]
        k1 = newnum[k][0]
        if k not in built:
            L[i] = renum(L[i], k, oldN, k1, N)
            L[e] = renum(L[e], k, oldN, k1, N)
            for j in range(i + 1, e):
                L[j] = renum(L[j], k, oldN, k1, N)
            continue
        pg, placed = built[k]
        body = L[i + 1:e]
        text_idx = set(l.idx for l in pg.lines)
        keep = [l for j, l in enumerate(body, start=i + 1) if j not in text_idx]
        feet = [l for l in keep if footer_re and footer_re.search(l)]
        reps = [l for l in keep if rep_re and rep_re.search(l) and l not in feet]
        once = [l for l in keep if l not in feet and l not in reps]
        for l in once:
            if l.strip() and not l.strip().startswith('//') and len(placed) > 1:
                REPORT.append('%s page %d: on its first part only: %s' % (name, k, l.strip()[:80]))
        out = [renum(L[i], k, oldN, k1, N)] + once + reps
        for pi, page in enumerate(placed):
            num = newnum[k][pi]
            code = pg.emit(page)
            if post:
                code = post(k, pi, code)
            if pi > 0:
                st = renum(L[i], k, oldN, num, N)
                pre_, args, suf = top_args(st)
                tp = (topics or {}).get((k, pi))
                ta = args[title_arg]
                if tp is not None:
                    ta = (' ' if ta.startswith(' ') else '') + lit('%s help %d/%d: %s' % (name, num, N, tp))
                elif ta.rstrip().endswith('"'):
                    ta = ta.rstrip()[:-1] + ' (continued)"'
                else:
                    ta = ta + ' + " (continued)"'
                args[title_arg] = ta
                st = pre_ + ','.join(args) + suf
                check_title(name, args[title_arg], par, 296)
                if split_turn:
                    out += split_turn(k, num, N, st)
                else:
                    out += own_turn(num)
                    out.append(st)
                out += reps
                REPORT.append('%s: new page %d/%d (from page %d)' % (name, num, N, k))
            out += code
            last = pi == len(placed) - 1
            if feet:
                out += [renum(l, k, oldN, num, N) for l in feet] if (last or foot_custom is None) else foot_custom(num, N)
        out.append(renum(L[e], k, oldN, newnum[k][-1], N))
        L[i:e + 1] = out
    s = '\n'.join(L)
    if N != oldN:
        # pages drawn by other routines: their titles too
        for k in range(1, oldN + 1):
            if k not in pages:
                s = re.sub(r'(%s help )%d/%d\b' % (re.escape(name), k, oldN), lambda m: m.group(1) + '%d/%d' % (newnum[k][0], N), s)
                REPORT.append('%s: page %d (another routine) is now %d/%d' % (name, k, newnum[k][0], N))
    return s, newnum, N, oldN, built


# ------------------------------------------------------------------ pages given as a list of lines
from listpage import ListPage, split_top, find_list


def fmt_list(rows, ind, kind):
    """a list literal, one element a line, in the file's own layout"""
    if kind == 'lines':
        return '{' + (',\n' + ind).join(r for r in rows) + '}'
    return '{' + ', '.join(rows) + '}'


def listcalls(name, s, call_re, cap, font, maxw, colors=True, marker=None, loose=True, cm=(), turn='', topics=None,
              title_in_call=True, foot_arg=None, end_re=None, region=None):
    """help pages drawn by a routine that takes (title, {lines}[, {colours}][, footer]).  call_re finds each call's start;
    the call's statement is copied for a split page, with ' (continued)' on its title, and 'turn' (e.g. the Esc test)
    written between the two."""
    pagea.LOOSE[0] = loose
    consts = find_consts(s)
    hp11.set_rev(consts)
    par = Parser(consts, cmfuncs=list(cm))
    P = props.for_prog(name)
    calls = []
    lo, hi = (0, len(s))
    if region:
        r_, _ = routines_from_text(s)
        ra, rb = r_[region]
        L_ = s.split('\n')
        lo, hi = sum(len(x) + 1 for x in L_[:ra - 1]), sum(len(x) + 1 for x in L_[:rb])
    for m in call_re.finditer(s, lo, hi):
        st = s.rfind('\n', 0, m.start()) + 1
        a, b = find_list(s, m.end() - 1 if s[m.end() - 1] == '{' else m.end())
        if colors:
            ca, cb = find_list(s, b)
        else:
            ca = cb = None
        if end_re:
            end = end_re.search(s, cb if colors else b).end()
        else:
            end = s.index(';', cb if colors else b) + 1
        mm = re.search(r'%s help (\d+)/(\d+)' % re.escape(name), s[st:end])
        if not mm and not title_in_call:
            mm = list(re.finditer(r'%s help (\d+)/(\d+)' % re.escape(name), s[:st]))[-1]
        calls.append((int(mm.group(1)), int(mm.group(2)), st, a, b, ca, cb, end))
    oldN = calls[0][1]
    built = {}
    for k, N0, st, a, b, ca, cb, end in calls:
        if k not in P:
            continue
        exprs = split_top(s[a + 1:b - 1])
        cols = split_top(s[ca + 1:cb - 1]) if colors else None
        if cols is not None and len(cols) > len(exprs):
            REPORT.append('%s page %d: %d colours for %d lines; the extra colour (never used) is dropped' % (name, k, len(cols), len(exprs)))
            cols = cols[:len(exprs)]
        if cols is not None and len(cols) != len(exprs):
            die('%s page %d: %d lines but %d colours' % (name, k, len(exprs), len(cols)))
        lp = ListPage(exprs, cols, par, font=font, maxw=maxw, marker=marker)
        for o, n in P[k]:
            try:
                lp.apply(o, n)
            except KeyError as ex:
                die('%s page %d: %s' % (name, k, ex))
        lp.reflow_all()
        pages = lp.pages(cap)
        lp.check(lp.place(ymax=(cap - 1) * 10, y_first=0))
        for pi, p in enumerate(lp.place(ymax=(cap - 1) * 10, y_first=0)):
            if lp.width_report(p):
                die('%s page %d: too wide %r' % (name, k, lp.width_report(p)))
        built[k] = pages
        REPORT.append('%s page %d: %d lines -> %s' % (name, k, len(exprs), '+'.join(str(len(p)) for p in pages)))
    newnum, n = {}, 0
    for k in range(1, oldN + 1):
        cnt = len(built[k]) if k in built else 1
        newnum[k] = list(range(n + 1, n + cnt + 1))
        n += cnt
    N = n
    if N != oldN and not title_in_call:
        die('%s: a page needs a second page; its title is outside the list (do it by hand)' % name)
    for k, N0, st, a, b, ca, cb, end in sorted(calls, key=lambda c: -c[2]):
        stmt = s[st:end]
        if not title_in_call:
            if k in built:
                ind = re.match(r'\s*', s[s.index('\n', a) + 1:]).group(0) if '\n' in s[a:b] else '    '
                s = s[:st] + s[st:a] + fmt_list([r[0] for r in built[k][0]], ind, 'lines') + s[b:end] + s[end:]
            continue
        if k not in built:
            s = s[:st] + renum(stmt, k, oldN, newnum[k][0], N) + s[end:]
            continue
        ind = re.match(r'\s*', s[s.index('\n', a) + 1:]).group(0) if '\n' in s[a:b] else '    '
        parts = []
        for pi, rows in enumerate(built[k]):
            num = newnum[k][pi]
            lines_lit = fmt_list([r[0] for r in rows], ind, 'lines')
            new = s[st:a] + lines_lit
            if colors:
                cl, prev = [], None
                for r in rows:
                    if r[1] not in (None, 'none'):
                        prev = r[1]
                    cl.append(r[1] if r[1] not in (None, 'none') else None)
                # a gap's colour: the colour of the line after it (any colour draws nothing for an empty string)
                for j in range(len(cl) - 1, -1, -1):
                    if cl[j] is None:
                        cl[j] = next((c for c in cl[j + 1:] if c), prev)
                new += s[b:ca] + fmt_list(cl, ind, 'cols') + s[cb:end]
            else:
                new += s[b:end]
            new = renum(new, k, oldN, num, N)
            if pi > 0:
                tp = (topics or {}).get((k, pi))
                mt = re.search(r'("%s help %d/%d: )([^"]*)(")' % (re.escape(name), num, N), new)
                if not mt:
                    die('%s page %d: cannot find the title to continue' % (name, k))
                topic = tp if tp is not None else mt.group(2) + ' (continued)'
                new = new[:mt.start()] + mt.group(1) + topic + mt.group(3) + new[mt.end():]
                check_title(name, lit('%s help %d/%d: %s' % (name, num, N, topic)), par, 296)
                REPORT.append('%s: new page %d/%d (from page %d)' % (name, num, N, k))
            parts.append(new)
        joined = parts[0]
        for p in parts[1:]:
            joined += ('\n' + turn if turn else '') + '\n' + p
        s = s[:st] + joined + s[end:]
    if N != oldN:
        for k in range(1, oldN + 1):
            if not any(c[0] == k for c in calls):
                s = re.sub(r'(%s help )%d/%d\b' % (re.escape(name), k, oldN), lambda m: m.group(1) + '%d/%d' % (newnum[k][0], N), s)
    return s, newnum, N, oldN, built


# ------------------------------------------------------------------ the version bump and the note
def bump(name, s, ov, nv):
    ot, nt = tag(ov), tag(nv)
    L = s.split('\n')
    hv = None
    for i, l in enumerate(L[:40]):
        if re.match(r'^//\s*[A-Za-z0-9 ]+ - ' + re.escape(ot) + r'\b', l):
            hv = i
            break
    if hv is not None:
        L[hv] = L[hv].replace(ot, nt)
        L[hv] = re.sub(r'\((\d+ Nov 2026[^)]*)\)', '(9 Nov 2026)', L[hv], count=1)
        L[hv] = re.sub(r' -- Round \d+[^.]*\.', ' -- Round 11, plain help pages.', L[hv])
    hist = [i for i, l in enumerate(L) if re.match(r'^//\s*' + re.escape(ot) + r'\s*\(', l)]
    if not hist and hv is None:
        die(name + ': no header line and no history line for ' + ot)
    at = hist[0] if hist else hv + 1
    body = ('Round 11: the help pages in plain words (Roger, 8-9 Nov 2026: "write more straightforward and don\'t try to be '
            'too clever--a student being able to understand is the priority"; "adding pages is fine, the explanation is what '
            'matters").  ' + NOTE[name] + '  Every changed page is laid out again at the calculator\'s own glyph widths '
            '(GlyphProbe_v1, Virtual Calculator, 9 Nov 2026), so no line is cut.')
    note = '// %s (9 Nov 2026): ' % nt + '\n//   '.join(textwrap.wrap(body, 100))
    L.insert(at, note)
    s = '\n'.join(L)
    s = re.sub(r'"[^"\n]*"', lambda m: m.group(0).replace(ot, nt).replace(ov, nv), s)
    # a version on screen with its date: the new date
    s = re.sub(r'"[^"\n]*%s[^"\n]*"' % re.escape(nt), lambda m: re.sub(r'\b\d{1,2} Nov 2026', '9 Nov 2026', m.group(0)), s)
    return s


# ================================================================== AgreeLab
def b_AgreeLab(s):
    call = re.compile(r'^(?P<pre>\s*ag_Tx\()(?P<expr>.*)(?P<mid>, )(?P<x>\d+), (?P<y>\d+)(?P<post>, [^,]+\);.*)$')
    # the d-bar line of page 7 becomes an ag_Tx line carrying a marker for the drawn d, and goes back after
    s = must_replace(s, '    ag_TxDb("bias = ", "; limits of agreement = bias " + agPM, 10, 72, agGRN, 306);   // beta 1c: d-bar',
                     '    ag_Tx("bias = " + CHAR(20) + "; limits of agreement = bias " + agPM, 10, 72, agGRN);', who='AgreeLab')

    def post(k, pi, code):
        out = []
        for c in code:
            if 'CHAR(20)' in c:
                m = re.match(r'^(\s*)ag_Tx\((.*) \+ CHAR\(20\) \+ (.*), (\d+), (\d+), (agGRN)\);$', c)
                if not m:
                    die('AgreeLab: the d-bar line: ' + c)
                c = '%sag_TxDb(%s, %s, %s, %s, %s, 306);   // beta 1c: d-bar' % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
            out.append(c)
        return out
    title = re.compile(r'(?P<lead>"AgreeLab help )\d+/\d+: (?P<topic>[^"]*)')
    s, nn, N, built = ifpages('AgreeLab', s, 'ag_HelpPage', 'hpN', call, ['ag_Cm'], 1, 300, 13, 205, title, post=post)
    if N != 9:
        die('AgreeLab: the page count changed (%d): fix ag_Help and its callers' % N)
    NOTE['AgreeLab'] = ('Help pages 2, 6 and 7 reworded: "a low bar", "rater offsets count" and "(.,k)" said in words, d-bar named as the '
                        'mean difference, and the Bland-Altman trend in words.')
    return s


def fix_pagecount(s, name, helpfn, oldN, N, newnum):
    """the help routine's page count and every caller that opens a given page"""
    if N == oldN:
        return s
    s = must_replace(s, 'hsP := MAX(1, MIN(%d, hsN));' % oldN, 'hsP := MAX(1, MIN(%d, hsN));' % N, who=name)
    s = must_replace(s, 'WHILE hsP >= 1 AND hsP <= %d DO' % oldN, 'WHILE hsP >= 1 AND hsP <= %d DO' % N, who=name)
    def rep(m):
        k = int(m.group(2))
        return m.group(1) + str(newnum[k][0]) + ')'
    s = re.sub(r'(\b%s\()(\d+)\)' % re.escape(helpfn), rep, s)
    return s


def b_xxTx(name, s, routine, tx, cm, oldN, helpfn, note):
    call = re.compile(r'^(?P<pre>\s*%s\()(?P<expr>.*)(?P<mid>, )(?P<x>\d+), (?P<y>\d+)(?P<post>, [^,]+\);.*)$' % tx)
    title = re.compile(r'(?P<lead>"%s help )\d+/\d+: (?P<topic>[^"]*)' % name)
    s, nn, N, built = ifpages(name, s, routine, 'hpN', call, cm, 1, 300, 13, 205, title)
    s = fix_pagecount(s, name, helpfn, oldN, N, nn)
    NOTE[name] = note + ('' if N == oldN else '  The help is now %d pages (was %d).' % (N, oldN))
    return s


def b_AnovaLab(s):
    return b_xxTx('AnovaLab', s, 'av_HelpPage', 'av_Tx', ['av_Cm'], 8, 'av_Help',
                  'Help pages 2, 3, 4 and 7 reworded: Levene\'s "robust" and Bartlett\'s "misled" explained, Holm and Scheffe in words, '
                  'Type III SS and effect coding in words, and the Home variables listed one by one.')


def b_TDist3D(s):
    call = re.compile(r'^(?P<pre>\s*tdLn\()(?P<expr>.*)(?P<mid>, )(?P<y>\d+)(?P<post>, [^,]+\);.*)$')
    s, nn, N, oldN, built = sections('TDist3D', s, 'tdHelp', re.compile(r'^\s*tdPage\("TDist3D help'),
                                     re.compile(r'tdPgEnd\('), 1, call, [], 1, 296, 205)
    NOTE['TDist3D'] = ('Help pages 1 to 4 reworded: "row" is now "curve", "stacks", "the price of estimating sigma", "climb a ladder" '
                       'and "raises the eye" in plain words.' + ('' if N == oldN else '  The help is now %d pages (was %d).' % (N, oldN)))
    return s


def b_seq(name, s, routine, pagefn, lnfn, endfn, maxw, note, turn=1, cm=(), ymax=205, topics=None):
    call = re.compile(r'^(?P<pre>\s*%s\()(?P<expr>.*)(?P<mid>, )(?P<y>\d+)(?P<post>, [^,]+\);.*)$' % lnfn)
    s, nn, N, oldN, built = sections(name, s, routine, re.compile(r'^\s*%s\("%s help' % (pagefn, name)),
                                     re.compile(r'%s\(' % endfn), turn, call, list(cm), 1, maxw, ymax, topics=topics)
    NOTE[name] = note + ('' if N == oldN else '  The help is now %d pages (was %d).' % (N, oldN))
    return s


def b_BiNorm3D(s):
    return b_seq('BiNorm3D', s, 'bnHelp', 'bnPage', 'bnLn', 'bnPgEnd', 296,
                 'Help pages 1 and 5 reworded: "X says nothing about Y" and "raises the eye" in plain words.', cm=['bnCm'])


TX = re.compile(r'^(?P<pre>\s*TEXTOUT_P\()(?P<expr>.*)(?P<mid>,\s*G1,\s*)(?P<x>\d+)(?P<sep>,\s*)(?P<y>\d+)(?P<post>,\s*1,\s*[^,()]+(,\s*\d+)?\);.*)$')


def b_CentralLimit(s):
    s, nn, N, oldN, built = sections('CentralLimit', s, 'cltHelp', re.compile(r'TEXTOUT_P\("CentralLimit help'),
                                     re.compile(r'BLIT_P\(G0'), 0, TX, ['cltCm'], 1, 300, 207, ytext=215,
                                     footer_re=re.compile(r', 226, 1,'), topics={(1, 1): 'The dashboard (continued)'},
                                     foot_custom=lambda num, N: ['  TEXTOUT_P("Any key or tap: the next page", G1, 8, 226, 1, #1E90FFh);'])
    NOTE['CentralLimit'] = ('Help pages 1 and 2 reworded: what a bar counts, why the axis is shared, the sigma/SD ratio, "the pile" '
                            'and the n keys in plain words.' + ('' if N == oldN else '  The help is now %d pages (was %d).' % (N, oldN)))
    return s


def seq_footers(s, routine, foot_re, fmt):
    """rewrite the help routine's footers in order: fmt(i, n) gives the i-th of n footers' text"""
    r, _ = routines_from_text(s)
    a, b = r[routine]
    L = s.split('\n')
    idx = [i for i in range(a - 1, b) if foot_re.search(L[i])]
    for c, i in enumerate(idx):
        L[i] = foot_re.sub(lambda m: m.group(1) + (fmt(c + 1, len(idx)) or m.group(2)) + m.group(3), L[i])
    return '\n'.join(L)


def note_n(name, note, N, oldN):
    NOTE[name] = note + ('' if N == oldN else '  The help is now %d pages (was %d).' % (N, oldN))


def b_ChiTable(s):
    s, nn, N, oldN, built = sections('ChiTable', s, 'csHelp', re.compile(r'TEXTOUT_P\("ChiTable help'), re.compile(r'BLIT_P\(G0'), 0,
                                     TX, ['csCm'], 1, 296, 205, ytext=215, footer_re=re.compile(r', 222, 1, csFOOT'),
                                     topics={(3, 1): 'Touch, keys, plots (continued)'})
    s = seq_footers(s, 'csHelp', re.compile(r'(TEXTOUT_P\(")(Any key = page \d+|Any key = back[^"]*|Any key[^"]*)(")'),
                    lambda i, n: 'Any key = page %d' % (i + 1) if i < n else None)
    if N != oldN:
        s = must_replace(s, 'TEXTOUT_P("Any key = page 5", G1, 12, 222, 1, csFOOT, 296);   // beta 3: was "= menu"',
                         'TEXTOUT_P("Any key = page %d", G1, 12, 222, 1, csFOOT, 296);   // beta 3: was "= menu"' % N, who='ChiTable')
    note_n('ChiTable', 'Help pages 1, 3 and 5 reworded: the expected count, the alpha steps and the exact answers in plain words.', N, oldN)
    return s


def b_GaltonBoard(s):
    s, nn, N, oldN, built = sections('GaltonBoard', s, 'gbHelp', re.compile(r'TEXTOUT_P\("GaltonBoard help'), re.compile(r'BLIT_P\(G0'), 0,
                                     TX, ['gbCm'], 1, 296, 211, ytext=218, footer_re=re.compile(r', 224, 1, gbFOOT'),
                                     foot_custom=lambda num, N: ['  TEXTOUT_P("Any key or tap: the next page", G1, 12, 224, 1, gbFOOT);'])
    note_n('GaltonBoard', 'Help pages 1, 2 and 3 reworded: what a bin is, the keys and the exact answers in plain words.', N, oldN)
    return s


def b_TrendTest(s):
    s, nn, N, oldN, built = sections('TrendTest', s, 'trHelp', re.compile(r'TEXTOUT_P\("TrendTest help'), re.compile(r'BLIT_P\(G0'), 0,
                                     TX, ['trCm'], 1, 296, 206, ytext=215, footer_re=re.compile(r', 220, 1, trFOOT'))
    s = seq_footers(s, 'trHelp', re.compile(r'(TEXTOUT_P\(")(any key = page \d+, Esc = menu|any key = menu)(")'),
                    lambda i, n: 'any key = page %d, Esc = menu' % (i + 1) if i < n else 'any key = menu')
    note_n('TrendTest', 'Help pages 1, 2 and 3 reworded: why one df has more power, what the departure from a line means, the '
                        'Scores key, the plots and the keys in plain words.', N, oldN)
    return s


def b_SampDist(s):
    s = must_replace(s, 'TEXTOUT_P("Results persist in Home as EP_SD_*", G1, 8, 200, 1, hBk);',
                     'TEXTOUT_P("Results are kept in Home as EP_SD_ names.", G1, 8, 200, 1, hBk);', who='SampDist')
    props.DROP.add(('SampDist', 'Results persist in Home as EP_SD_*'))
    s, nn, N, oldN, built = sections('SampDist', s, 'sd_showHelp', re.compile(r'TEXTOUT_P\("SampDist help'), re.compile(r'BLIT_P\(G0'), 0,
                                     TX, ['sd_Cm'], 1, 300, 207, ytext=215, footer_re=re.compile(r', 226, 1, RGB\(30,144,255\)'),
                                     exclude_re=re.compile(r'Results are kept in Home as EP_SD_'),
                                     rep_re=re.compile(r'LINE_P\(G1, 6, 17'))
    note_n('SampDist', 'Help pages 1 and 2 reworded: the standard error written with a root sign, and the graph\'s keys in plain words.', N, oldN)
    return s


def b_NormExplorer(s):
    # page 2 is a table, a key at x 20 and its meaning beside it: its lines are changed in place (each measured)
    for a, b in [('"EXPLORER SOFT KEYS  (More turns the page)"', '"EXPLORER SOFT KEYS  (More shows the second set)"'),
                 ('"PAGE 2: WHAT " + CHAR(8592) + " " + CHAR(8594) + " MOVE"', '"SECOND SET OF KEYS: WHAT " + CHAR(8592) + " AND " + CHAR(8594) + " MOVE"'),
                 ('"the lower bound (or x\u2080), the upper"', '"A = the lower bound (or x\u2080), B = the upper"'),
                 ('"\u03bc; or \u03c3, \u2190 narrower \u2192 wider"', '"\u03bc = the mean; \u03c3 = \u2190 narrower, \u2192 wider"'),
                 ('"Tap the chosen key again for the usual:"', '"Tap the chosen key again to go back to the usual keys:"'),
                 ('"The window is held while you explore."', '"The plot\'s window stays fixed while you explore."')]:
        s = must_replace(s, a, b, who='NormExplorer')
    s, nn, N, oldN, built = sections('NormExplorer', s, 'ne_HelpPages', re.compile(r'TEXTOUT_P\("NormExplorer help'), re.compile(r'BLIT_P\(G0'), 0,
                                     TX, ['ne_Cm'], 1, 280, 207, ytext=215, footer_re=re.compile(r', 221, 1, neFOOT'),
                                     rep_re=re.compile(r'LINE_P\(G1, 20, 34'), skip={2})
    note_n('NormExplorer', 'Help pages 2 and 3 reworded: "turns the page", the second set of soft keys, "held" and the drag in plain words.', N, oldN)
    return s


def b_DNAMixLR(s):
    s, nn, N, built = ifpages('DNAMixLR', s, 'dmHelpPage', 'hgP', TX, ['dmCm'], 1, 296, None, 193, None,
                              exclude_re=re.compile(r'Teaching aid; not for casework'))
    NOTE['DNAMixLR'] = 'Help pages 1 to 4 reworded: what P(E|H) counts, the ENFSI words, the keys and the formula in plain words.'
    return s


def b_ScatterLab(s):
    call = re.compile(r'^(?P<pre>\s*slHT\()(?P<expr>.*)(?P<mid>, )(?P<y>\d+)(?P<post>, [^,]+\);.*)$')
    s, nn, N, built = ifpages('ScatterLab', s, 'slHelpPg', 'hgP', call, ['slCm'], 1, 296, None, 205,
                              re.compile(r'(?P<lead>"ScatterLab help )\d+/\d+: (?P<topic>[^"]*)'))
    if N != 6:
        die('ScatterLab: the page count changed')
    NOTE['ScatterLab'] = 'Help page 2 reworded: "the squared misses" in plain words.'
    return s


def b_TTx(name, s, frame, wait, note):
    s, nn, N, oldN, built = sections(name, s, name[:2].lower() + '_Help' if False else HELPR[name], re.compile(r'%s\("%s help' % (frame, name)),
                                     re.compile(r'BLIT_P\(G0'), 0, TX, [CMF[name]], 1, 296, 207, loose=False, ytext=215,
                                     footer_re=re.compile(r',\s*222,\s*1,'))
    note_n(name, note, N, oldN)
    return s


HELPR = {'TTestLab': 'tt_Help', 'TTestLabG': 'tz_Help', 'DataLoad': 'dd_Help'}
CMF = {'TTestLab': 'tt_Cm', 'TTestLabG': 'tz_Cm', 'DataLoad': 'dd_Cm'}


def b_TTestLab(s):
    return b_TTx('TTestLab', s, 'tt_Frame', 'tt_WaitAny', 'Help pages 1 and 2 reworded: the soft keys named, the menu items listed, '
                 'the pairs in D1 and D2 explained, and "as the lecture" dropped (Roger, 9 Nov 2026).')


def b_TTestLabG(s):
    return b_TTx('TTestLabG', s, 'tz_Frame', 'tz_WaitAny', 'Help pages 1 and 2 reworded: the soft keys named, the menu items listed, '
                 'the pairs in D1 and D2 explained, and the printed-table rule in plain words.')


def b_DataLoad(s):
    return b_TTx('DataLoad', s, 'dd_Frame', 'dd_WaitAny', 'Help page 1 reworded: "the fleet\'s programs" is now "our programs".')


def b_PowerViz(s):
    s, nn, N, oldN, built = sections('PowerViz', s, 'pv_ShowHelp', re.compile(r'TEXTOUT_P\("PowerViz help'), re.compile(r'BLIT_P\(G0'), 0,
                                     TX, ['pv_Cm'], 1, 300, {1: 195, '*': 207}, loose=False, ytext=215,
                                     footer_re=re.compile(r',222,1,cfot'), exclude_re=re.compile(r'Teaching aid; not for clinical'))
    note_n('PowerViz', 'Help pages 1 to 5 reworded: the alpha steps, the drag, the n formula and Levene\'s test in plain words.', N, oldN)
    return s


def b_TestChooser(s):
    for rt in ('tcHelp1', 'tcHelp2'):
        s, nn, N, oldN, built = sections('TestChooser', s, rt, re.compile(r'TEXTOUT_P\("TestChooser help'), re.compile(r'^END;'), 0,
                                         TX, ['tcCm'], 1, 296, 184, loose=False, ytext=196)
        if N != oldN:
            die('TestChooser: a page needs splitting (%s)' % rt)
    NOTE['TestChooser'] = 'Help pages 1 and 2 reworded: "tiny n", "linked", "light it up", the corner box and the hatched cells in plain words.'
    return s


def one_page(name, s, routine, title_re, call, cm, maxw, ymax, ytext, loose=False):
    """a help of one page: its lines laid out again in place; it must still fit"""
    pagea.LOOSE[0] = loose
    L = s.split('\n')
    consts = find_consts(s)
    hp11.set_rev(consts)
    r, _ = routines_from_text(s)
    a, b = r[routine]
    par = Parser(consts, cmfuncs=cm)
    t = next(i for i in range(a - 1, b) if title_re.search(L[i]))
    pg = Page(L, t + 2, b, call, par, font=1, maxw=maxw, ylimit=ytext)
    for o, n in props.for_prog(name).get(1, []):
        try:
            pg.apply(o, n)
        except KeyError as ex:
            die('%s: %s' % (name, ex))
    pg.reflow_all()
    placed = pg.place(ymax=ymax)
    pg.check(placed)
    if len(placed) > 1:
        die('%s: its one help page no longer fits' % name)
    code = pg.emit(placed[0])
    idx = sorted(l.idx for l in pg.lines)
    out, put = [], False
    for j in range(len(L)):
        if j in idx:
            if not put:
                out += code
                put = True
            continue
        out.append(L[j])
    REPORT.append('%s: %d lines -> %d' % (name, len(pg.lines), len(placed[0])))
    return '\n'.join(out)


def b_Norm3(s):
    s = one_page('Norm3', s, 'n3_Help', re.compile(r'"Norm3 help: '), TX, ['n3_Cm'], 300, 205, 215)
    NOTE['Norm3'] = 'Its help page reworded: "snaps" and "its quantile" in plain words.'
    return s


def b_RiskLab(s):
    s, nn, N, oldN, built = listcalls('RiskLab', s, re.compile(r'hK := rl_HPage\("RiskLab help'), 14, 1, 296,
                                      cm=['rl_Cm'], turn='  IF hK == 4 THEN RETURN; END;')
    note_n('RiskLab', 'Help pages 2, 4, 5 and 6 reworded: the AUC, the cut-off, calibration and the fairness measures in plain words.', N, oldN)
    return s


def b_SurvLab(s):
    s, nn, N, oldN, built = listcalls('SurvLab', s, re.compile(r'hK := sv_HPage\("SurvLab help'), 14, 1, 296,
                                      cm=['sv_Cm'], turn='  IF hK == 4 THEN RETURN; END;')
    note_n('SurvLab', 'Help page 2 reworded: "n.r. = open" in plain words.', N, oldN)
    return s


def b_CICatcher(s):
    s, nn, N, oldN, built = listcalls('CICatcher', s, re.compile(r'hpK := cqPage\("CICatcher help'), 14, 1, 296,
                                      cm=['cqCm'], turn='  IF hpK == 4 THEN RETURN; END;')
    note_n('CICatcher', 'Help pages 1 to 4 reworded: what 95 % is of, why a higher level widens every line, Wald and Wilson, '
                        'and the exact interval in plain words.', N, oldN)
    return s


def b_ErrorRate(s):
    s = must_replace(s, '"ErrorRate help 7/9: Honest caveats"', '"ErrorRate help 7/9: Cautions"', who='ErrorRate')
    props.DROP.add(('ErrorRate', 'ErrorRate help 7/9: Honest caveats'))
    s, nn, N, oldN, built = listcalls('ErrorRate', s, re.compile(r'^\s*erlPage\("ErrorRate help', re.M), 14, 1, 296,
                                      cm=['erlCm'], turn='  hpK := erlWaitAny();\n  IF hpK == 4 THEN RETURN; END;')
    note_n('ErrorRate', 'Help pages 2 and 5 to 9 reworded: the plot, the database page, the cautions, the sources and the '
                        'examples in plain words ("10,000 programs" is now "10,000 examiners").', N, oldN)
    return s


def b_ExhibitLab(s):
    s, nn, N, oldN, built = listcalls('ExhibitLab', s, re.compile(r'hpL := \{'), 14, 1, 296, cm=['sz_Cm'],
                                      turn='  IF hpK == 4 THEN RETURN; END;', end_re=re.compile(r'sz_HelpPg\([^;]*\);'),
                                      region='sz_Help')
    s = seq_footers(s, 'sz_Help', re.compile(r'(, hpC, ")(Any key = page \d+, Esc = menu|[^"]*)(")'),
                    lambda i, n: 'Any key = page %d, Esc = menu' % (i + 1) if i < n else None)
    note_n('ExhibitLab', 'Help pages 1, 2, 3 and 7 reworded: what the claim means, the two kinds of answer, the finite-population '
                         'correction and the keys in plain words.', N, oldN)
    return s


def b_EpiStats(s):
    s, nn, N, oldN, built = listcalls('EpiStats', s, re.compile(r'es_HelpPage\("EpiStats help'), 14, 1, 300, colors=False,
                                      cm=['es_Cm'], end_re=re.compile(r'\);'))
    if N != oldN:
        die('EpiStats: a page needs a second page; its help menu and page references must change by hand')
    NOTE['EpiStats'] = ('Help pages 1, 5, 6, 11, 13 and 14 reworded: the help-page numbers named as numbers, the confidence '
                        'intervals, Mantel-Haenszel, the PPV plot and the forest plot in plain words.')
    return s


def b_StatDist(s):
    s, nn, N, oldN, built = listcalls('StatDist', s, re.compile(r'st_HPage\("StatDist help'), 13, 2, 300, colors=False,
                                      cm=['st_Cm'], end_re=re.compile(r'"\);'))
    note_n('StatDist', 'Help pages 1, 2 and 3 reworded: the menus, the drag, the zoom keys and the three sets of soft keys in plain words.', N, oldN)
    return s


def b_StudRange(s):
    s, nn, N, oldN, built = listcalls('StudRange', s, re.compile(r'hk:=sr_ShowRes\("StudRange help'), 10, 3, 300, colors=False,
                                      loose=False, cm=['sr_Cm'], end_re=re.compile(r'",\s*\d\);'),
                                      turn='  IF hk==4 THEN RETURN 0; END;', topics={(1, 1): 'More about StudRange'})
    note_n('StudRange', 'Help pages 1 to 4 reworded: what n is for each method, the infinite df, the journal, the two engines '
                        'and the drag in plain words.', N, oldN)
    return s


def b_RankLab(s):
    # each page is an IF block: hlT := its title; hlL := its lines ("*" = magenta); a split needs new blocks
    s2, nn, N, oldN, built = listcalls('RankLab', s, re.compile(r'hlL := \{'), 14, 1, 300, colors=False, marker='*',
                                       cm=['rk_Cm'], end_re=re.compile(r';'), region='rk_Help', title_in_call=False)
    NOTE['RankLab'] = 'Help pages 1, 2, 5 and 6 reworded: "slot 4", the Halo preset, the exact p and the keys in plain words.'
    return s2


def b_BayesTree(s):
    """four pages in IF hpPg == k blocks (hpT, the title; hpTx, the lines); page 1 now needs two pages, so the
    blocks are written again, the loop's count and the forensic page's red line (page 3, now 4) move with them"""
    pagea.LOOSE[0] = True
    consts = find_consts(s)
    hp11.set_rev(consts)
    par = Parser(consts, cmfuncs=['bt_Cm'])
    P = props.for_prog('BayesTree')
    L = s.split('\n')
    r, _ = routines_from_text(s)
    a, b = r['bt_HelpView']
    blocks = {}
    i = a - 1
    while i < b:
        m = re.match(r'^(\s*)IF hpPg == (\d+) THEN\s*$', L[i])
        if m:
            j = i + 1
            while not re.match(r'^%sEND;' % m.group(1), L[j]):
                j += 1
            if any('hpTx := {' in x for x in L[i:j + 1]):
                blocks[int(m.group(2))] = (i + 1, j + 1)
            i = j
        i += 1
    pages = {}
    for k, (ba, bb) in blocks.items():
        txt = '\n'.join(L[ba - 1:bb])
        tm = re.search(r'hpT := "BayesTree help %d/4: ([^"]*)";' % k, txt)
        la, lb = find_list(txt, txt.index('hpTx := {') + 8)
        exprs = split_top(txt[la + 1:lb - 1])
        if k in P:
            lp = ListPage(exprs, None, par, font=1, maxw=300)
            for o, n in P[k]:
                lp.apply(o, n)
            lp.reflow_all()
            parts = lp.pages(14)
            lp.check(lp.place(ymax=13 * 10, y_first=0))
            REPORT.append('BayesTree page %d: %d lines -> %s' % (k, len(exprs), '+'.join(str(len(p)) for p in parts)))
            pages[k] = (tm.group(1), [[e for e, c in p] for p in parts])
        else:
            pages[k] = (tm.group(1), [exprs])
    N = sum(len(v[1]) for v in pages.values())
    out, num, red = [], 0, None
    ind = re.match(r'(\s*)', L[blocks[1][0] - 1]).group(1)
    for k in sorted(pages):
        topic, parts = pages[k]
        for pi, rows in enumerate(parts):
            num += 1
            if k == 3:
                red = num
            t = topic if pi == 0 else topic + ' (continued)'
            check_title('BayesTree', lit('BayesTree help %d/%d: %s' % (num, N, t)), par, 300)
            out.append('%sIF hpPg == %d THEN' % (ind, num))
            out.append('%s  hpT := "BayesTree help %d/%d: %s";' % (ind, num, N, t))
            out.append('%s  hpTx := {%s};' % (ind, (',\n' + ind + '           ').join(rows)))
            out.append('%sEND;' % ind)
    first, last = blocks[min(blocks)][0], blocks[max(blocks)][1]
    L[first - 1:last] = out
    s = '\n'.join(L)
    s = must_replace(s, 'WHILE hpPg >= 1 AND hpPg <= 4 DO', 'WHILE hpPg >= 1 AND hpPg <= %d DO' % N, who='BayesTree')
    s = must_replace(s, '    IF hpPg == 3 THEN\n      TEXTOUT_P("Teaching aid; not for casework or legal use."',
                     '    IF hpPg == %d THEN\n      TEXTOUT_P("Teaching aid; not for casework or legal use."' % red, who='BayesTree')
    s = must_replace(s, '    IF hpPg < 4 THEN', '    IF hpPg < %d THEN' % N, who='BayesTree')
    NOTE['BayesTree'] = ('Help pages 1, 2 and 4 reworded: "slot 6", the soft-key pages, the views and the exact answers in plain '
                         'words.  The help is now %d pages (was 4).' % N)
    return s


def pairs(name, s, pp):
    for a, b in pp:
        s = must_replace(s, a, b, who=name)
    return s


def b_BurrLab(s):
    s = pairs('BurrLab', s, [
        ('the sample mean never settles (menu 4).', 'the sample mean never settles down to one value (menu 4).'),
        ('The window freezes while a finger is down and refits on the lift.',
         'The plot holds still while your finger is on the screen and is fitted again when you lift it.'),
        ('Tap the map to set (C, K); its colors are the moment cases.',
         'Tap the map to set (C, K); its colors show whether the mean and the variance exist there.'),
        ('A fit that runs to the Weibull or Pareto limit is named as such.', 'If the best fit is at the Weibull or Pareto limit, the fit is named that.'),
        ('Anderson-Darling (a statistic, honestly without a p).', 'Anderson-Darling (the statistic only, with no p-value).'),
        ('Python only: no fallback; a bridge failure shows a message,', 'Python only: no fallback; if the Python engine fails, a message says so,')])
    # pages 1 and 2 no longer fit (bu_Para wraps at 47 characters, 12 px a line, and the footer is at y 204): each
    # becomes two, so the help is six pages
    s = pairs('BurrLab', s, [
        ('"/4: " + IFTE(hpPg == 1, "The Burr XII model", IFTE(hpPg == 2, "Family, fit, pictures", IFTE(hpPg == 3, "How rare is this?", "Fit engines"))));',
         '"/6: " + IFTE(hpPg == 1, "The Burr XII model", IFTE(hpPg == 2, "Explore", IFTE(hpPg == 3, "Family tree and fit", '
         'IFTE(hpPg == 4, "Pictures", IFTE(hpPg == 5, "How rare is this?", "Fit engines"))))));'),
        ('    IF hpPg == 4 THEN\n      hpY := bu_Para("Fit engines', '    IF hpPg == 6 THEN\n      hpY := bu_Para("Fit engines'),
        ('    IF hpPg == 3 THEN\n      hpY := bu_Para("How rare is this?', '    IF hpPg == 5 THEN\n      hpY := bu_Para("How rare is this?'),
        ('    IF hpPg == 2 THEN\n      hpY := bu_Para("Family tree:', '    IF hpPg == 3 THEN\n      hpY := bu_Para("Family tree:'),
        ('      hpY := bu_Para("Pictures: histogram,', '    END;\n    IF hpPg == 4 THEN\n      hpY := bu_Para("Pictures: histogram,'),
        ('      hpY := bu_Para("Explore: soft keys choose', '    END;\n    IF hpPg == 2 THEN\n      hpY := bu_Para("Explore: soft keys choose'),
        ('      IF hpPg > 4 THEN hpRun := 0; END;', '      IF hpPg > 6 THEN hpRun := 0; END;')])
    # the paragraphs that now open a page start at the top
    s = re.sub(r'(IF hpPg == 2 THEN\n      hpY := bu_Para\("Explore: soft keys choose.*?", )hpY \+ 2(, bu[A-Z]+\);)', r'\g<1>24\2', s, flags=re.S)
    s = re.sub(r'(IF hpPg == 4 THEN\n      hpY := bu_Para\("Pictures: histogram,.*?", )hpY \+ 2(, bu[A-Z]+\);)', r'\g<1>24\2', s, flags=re.S)
    if s.count(', 24, bu') < 6:
        die('BurrLab: a moved paragraph does not start at the top')
    NOTE['BurrLab'] = 'The help is now 6 pages (was 4): pages 1 and 2 each became two.  Help pages 1, 2 and 4 reworded: the mean that never settles, the plot during a drag, the map\'s colors, the fit\'s limits and the Python engine in plain words.'
    return s


def b_ResampLab(s):
    s = pairs('ResampLab', s, [
        ('Once: the pooled values are dealt again into groups of the same sizes, and their difference d drops onto the histogram.',
         'Once: the pooled values are shuffled into new groups of the same sizes, and the new difference d is added to the histogram.'),
        ('"Assumes: under " + rsH0 + " the labels are exchangeable (random assignment)."',
         '"Assumes: under " + rsH0 + " the labels could be swapped without changing anything, which is true when the groups were made by random assignment."'),
        ('(a stack = picked more than once)', '(a stack of dots = a value picked more than once)'),
        ('Basic: those ends reflected about the estimate.', 'Basic: the same two ends, mirrored around the estimate.'),
        ('"Small samples give too narrow intervals: n " + rsGE + " 15 or so."', '"With small samples the intervals are too narrow: use n of about 15 or more."')])
    NOTE['ResampLab'] = 'Help pages 1 and 3 reworded: the shuffle, "exchangeable", the stacked dots, the basic interval and small samples in plain words.'
    return s


def b_FitCheck(s):
    s = pairs('FitCheck', s, [
        ('fc_TL("The curve is only a fair guide when the E are not too small:', 'fc_TL("The " + fcX2S + " curve gives a trustworthy p only when the E are not too small:'),
        ('a normal sample hugs the line " + fcXbar', 'a normal sample lies close to the line " + fcXbar'),
        ('(D\'Agostino & Stephens 1986): weights the tails.', '(D\'Agostino & Stephens 1986): gives extra weight to the tails.'),
        ('so a p of 10^-145 (Castaneda) is still printed as a number.  The plot puts x on a scale of SDs from E (the Castaneda reasoning).',
         'so a p of 10^-145 (the Castaneda jury preset) is still printed as a number.  The plot shows how many SDs x is from E, the reasoning '
         'the Supreme Court used in Castaneda v. Partida (1977).')])
    NOTE['FitCheck'] = 'Help pages 3, 5 and 6 reworded: when the chi-square p can be trusted, the Q-Q line, Anderson-Darling\'s tails and the Castaneda reasoning in plain words.'
    return s


BUILDERS = {'AgreeLab': ('beta1f', 'beta1g', b_AgreeLab), 'AnovaLab': ('beta1e', 'beta1f', b_AnovaLab),
            'TDist3D': ('beta1', 'beta1a', b_TDist3D), 'BiNorm3D': ('beta1e', 'beta1f', b_BiNorm3D),
            'CentralLimit': ('beta3f', 'beta3g', b_CentralLimit), 'ChiTable': ('beta3k', 'beta3l', b_ChiTable),
            'GaltonBoard': ('beta3h', 'beta3i', b_GaltonBoard), 'TrendTest': ('beta3l', 'beta3m', b_TrendTest),
            'SampDist': ('v2.3i', 'v2.3j', b_SampDist), 'NormExplorer': ('beta42i', 'beta42j', b_NormExplorer),
            'DNAMixLR': ('beta3i', 'beta3j', b_DNAMixLR), 'ScatterLab': ('beta2i', 'beta2j', b_ScatterLab),
            'TTestLab': ('beta1h', 'beta1i', b_TTestLab), 'TTestLabG': ('beta1f', 'beta1g', b_TTestLabG), 'DataLoad': ('beta1e', 'beta1f', b_DataLoad),
            'PowerViz': ('v2.5q', 'v2.5r', b_PowerViz), 'TestChooser': ('beta2f', 'beta2g', b_TestChooser),
            'Norm3': ('v2.4f', 'v2.4g', b_Norm3), 'RiskLab': ('beta1e', 'beta1f', b_RiskLab),
            'SurvLab': ('beta1e', 'beta1f', b_SurvLab), 'CICatcher': ('beta2h', 'beta2i', b_CICatcher),
            'ErrorRate': ('beta1i', 'beta1j', b_ErrorRate), 'ExhibitLab': ('beta1f', 'beta1g', b_ExhibitLab),
            'EpiStats': ('v1.7j', 'v1.7k', b_EpiStats), 'StatDist': ('v2.7k', 'v2.7l', b_StatDist),
            'StudRange': ('beta15l', 'beta15m', b_StudRange), 'RankLab': ('beta1f', 'beta1g', b_RankLab),
            'BayesTree': ('beta8i', 'beta8j', b_BayesTree), 'BurrLab': ('beta1p', 'beta1q', b_BurrLab),
            'ResampLab': ('beta1g', 'beta1h', b_ResampLab), 'FitCheck': ('beta1e', 'beta1f', b_FitCheck)}


ASCII_CODE = {'BiNorm3D', 'ChiTable', 'DNAMixLR', 'ErrorRate', 'ScatterLab', 'CICatcher'}   # Lessons Learned §5


def build(only=None):
    for name, (ov, nv, fn) in BUILDERS.items():
        if only and name not in only:
            continue
        hp11.LITERAL[0] = name not in ASCII_CODE
        s = io.open(os.path.join(SRC, '%s_%s.txt' % (name, ov)), encoding='utf-8').read()
        s = fn(s)
        s = bump(name, s, ov, nv)
        io.open(os.path.join(DST, '%s_%s.txt' % (name, nv)), 'w', encoding='utf-8').write(s)
        DONE[name] = nv
    print('\n'.join(REPORT))
    print('built:', ', '.join('%s_%s' % kv for kv in DONE.items()))


if __name__ == '__main__':
    build(sys.argv[1:] or None)
