#!/usr/bin/env python3
"""ppl_check_v3.py  --  static checks for HP Prime PPL source, in the spirit of ppl_lint.py.

Usage: python3 -I ppl_check.py whitelist.json file.txt [file2.txt ...]

Checks (E = error, W = warning):
  E1  identifier called like a function that is neither defined in the file nor in the
      command whitelist (hallucinated / misspelled command)
  E2  block balance: BEGIN/IF/FOR/WHILE/CASE/IFERR ... END, REPEAT ... UNTIL
  E3  LOCAL with more than 6 names on one line
  E4  reserved words or single lowercase letters used as variable / parameter names;
      parameter names that collide (case-insensitively) with built-in commands
  E5  non-ASCII characters in executable code (outside strings and comments)
  E6  LOCAL declared after other statements in a function body, or inside IF/FOR/...
  E7  identifier used but never declared (not LOCAL, parameter, file-level, function,
      built-in or whitelist)
  E8  lowercase exponent literal (1e-9); '=' used where '==' was probably meant
  E9  STRING(value, 1, digits): mode 1 ignores the digits argument
  E10 INPUT whose first argument is not a variable name or a list of names
  W1  statement line that does not end in ';' (heuristic, review by eye)
  W2  LOCAL variable declared but never used
  W3  literal text in TEXTOUT_P that probably overruns the right edge
  W4  MSGBOX with more than 5 lines
  W5  IF CHOOSE(...) -- test the index variable instead
  E11 a declared name (LOCAL, parameter, EXPORT variable or function) that matches a built-in
      command when case is ignored: the Prime matches built-ins case-insensitively, so
      LOCAL csC is rejected as CSC and a program named ChiSquare is CHISQUARE (device, 10 Oct 2026)

v3 (16 Oct 2026): E1/E7 match built-ins ignoring case, as the device does (TYPE, LEFT
were reported as unknown because the list spells them in lowercase); E8 no longer fires on `!=` (and the Unicode comparison glyphs); the
not-equal forms `<>` and `!=` both run on the device.
v2 (10 Oct 2026): adds E11; an optional second whitelist file (e.g. HP_Prime_Builtin_Names.txt,
one name per line, # comments) widens the built-in list.
Usage: python3 -I ppl_check.py whitelist.json[,names.txt] file.txt [file2.txt ...]
"""
import sys, re, json

RESERVED = {'STEP','TO','FROM','DO','OR','AND','MOD','NOT','END','IF','THEN','ELSE','CASE','DEFAULT',
            'FOR','WHILE','REPEAT','UNTIL','BEGIN','RETURN','BREAK','CONTINUE','LOCAL','EXPORT','KILL',
            'VIEW','START','DOWNTO','IFERR','e','i','x','y','z','Re','Im'}
KEYWORDS = {'BEGIN','END','IF','THEN','ELSE','FOR','FROM','TO','DOWNTO','STEP','DO','WHILE','REPEAT',
            'UNTIL','CASE','DEFAULT','IFERR','RETURN','BREAK','CONTINUE','LOCAL','EXPORT','AND','OR',
            'NOT','MOD','KILL','VIEW','START'}
GLOBALS = {'G0','G1','G2','G3','G4','G5','G6','G7','G8','G9','K','Ans','HAngle'} \
          | {'D%d' % n for n in range(10)} | {'C%d' % n for n in range(10)} \
          | {'L%d' % n for n in range(10)} | {'M%d' % n for n in range(10)}
IDENT = re.compile(r'[A-Za-z_][A-Za-z0-9_]*')

def strip(line):
    """Return (code, strings): code with string literals replaced by "" and comments removed."""
    if line.lstrip().startswith('#pragma'): return '', []
    line = re.sub(r'#[0-9A-Fa-f]+h\b', '0', line)
    line = re.sub(r'\b\d+(\.\d+)?E[-+]?\d+\b', '0', line)
    out = []; strings = []; i = 0; n = len(line)
    while i < n:
        c = line[i]
        if c == '"':
            j = line.find('"', i+1)
            if j < 0: j = n-1
            strings.append(line[i+1:j]); out.append('""'); i = j+1; continue
        if line.startswith('//', i):
            break
        out.append(c); i += 1
    return ''.join(out), strings

def main():
    wl = set()
    for part in sys.argv[1].split(','):
        if part.endswith('.json'):
            wl |= set(json.load(open(part)))
        else:
            wl |= {ln.strip() for ln in open(part, encoding='utf-8', errors='ignore')
                   if ln.strip() and not ln.startswith('#')}
    wl_lower = {w.lower() for w in wl}
    def e11(ln, kind, nm):
        if nm.lower() in wl_lower and nm not in wl:
            errs.append((ln, 'E11', '%s %r matches built-in %r when case is ignored' % (kind, nm,
                        [w for w in wl if w.lower() == nm.lower()][0])))
    status = 0
    for path in sys.argv[2:]:
        print('=' * 70); print(path)
        src = open(path, encoding='utf-8').read().split('\n')
        # names of #PYTHON blocks are legal arguments to PYTHON(...)
        GLOBALS.update(re.findall(r'^\s*#PYTHON\s+([A-Za-z_]\w*)', '\n'.join(src), re.M))
        errs = []; warns = []
        code_lines = []
        inpy = False
        for ln, raw in enumerate(src, 1):
            if raw.startswith('#PYTHON'): inpy = True
            if inpy:
                code_lines.append((ln, '', [], raw))
                if raw.startswith('#END'): inpy = False
                continue
            code, strs = strip(raw)
            code_lines.append((ln, code, strs, raw))
            # E5 non-ASCII in code
            bad = [ch for ch in code if ord(ch) > 127]
            if bad: errs.append((ln, 'E5', 'non-ASCII in code: %r' % ''.join(sorted(set(bad)))))
            # E8 lowercase exponent, '=' comparisons
            if re.search(r'\b\d+(\.\d+)?e[-+]?\d+\b', code): errs.append((ln, 'E8', 'lowercase exponent literal'))
            c2 = re.sub(r':=|==|<=|>=|<>|!=|≠|≤|≥', '', code)
            if '=' in c2 and re.search(r'\b(IF|UNTIL|WHILE)\b', code):
                errs.append((ln, 'E8', "'=' in a condition; did you mean '=='?"))
            # E9
            if re.search(r'STRING\s*\([^()]*,\s*1\s*,\s*\d', code): errs.append((ln, 'E9', 'STRING(..., 1, digits) ignores digits'))
            # W5
            if re.search(r'\bIF\s+CHOOSE\s*\(', code): warns.append((ln, 'W5', 'IF CHOOSE(...): test the index variable'))
            # E10
            m = re.search(r'INPUT\s*\(\s*(\{[^}]*\}|[A-Za-z_][A-Za-z0-9_]*)', code)
            if m:
                arg = m.group(1).strip('{} ')
                for part in arg.split(','):
                    p = part.strip()
                    if p and not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', p):
                        errs.append((ln, 'E10', 'INPUT target is not a plain variable name: %r' % p))
            # W4
            if 'MSGBOX' in code:
                stmt_text = raw
                k = ln
                while ');' not in stmt_text and k < len(src): stmt_text += src[k]; k += 1
                if stmt_text.count('CHAR(10)') > 4: warns.append((ln, 'W4', 'MSGBOX with more than 5 lines'))
        # ---- structure: functions, params, locals, blocks ----
        stack = []            # (keyword, line)
        funcs = {}            # name -> (params, locals set, body lines)
        cur = None            # current function name
        file_locals = set(); exports = set()
        body_started = False  # a non-LOCAL statement has appeared in the current body
        pending_header = None
        used = {}             # name -> set of line numbers
        calls = {}            # name -> line numbers where name( appears
        for ln, code, strs, raw in code_lines:
            s = code.strip()
            if not s: continue
            toks = IDENT.findall(code)
            # function header: NAME(params) alone on a line at depth 0 (optionally EXPORT / VIEW "..",)
            hdr = re.match(r'^\s*(EXPORT\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)\s*$', code)
            if hdr and not stack:
                name = hdr.group(2); params = [p.strip() for p in hdr.group(3).split(',') if p.strip()]
                funcs[name] = {'params': params, 'locals': set(), 'line': ln, 'uses': set()}
                pending_header = name
                e11(ln, 'function', name)
                for p in params:
                    if p in RESERVED or re.fullmatch(r'[a-z]', p): errs.append((ln, 'E4', 'reserved/single-letter parameter %r' % p))
                    if p.lower() in wl_lower: errs.append((ln, 'E4', 'parameter %r collides with a built-in command' % p))
                    e11(ln, 'parameter', p)
                continue
            # forward declaration NAME(); at depth 0
            if not stack and re.match(r'^\s*[A-Za-z_][A-Za-z0-9_]*\s*\(\s*\)\s*;\s*$', code):
                continue
            # EXPORT variables at file level
            if not stack and re.match(r'^\s*EXPORT\s+[A-Za-z_]', code) and not re.search(r'\)\s*$', code):
                for nm in re.findall(r'[A-Za-z_][A-Za-z0-9_]*', re.sub(r':=\s*[^,;]+', '', code.replace('EXPORT', ''))):
                    exports.add(nm)
                    e11(ln, 'EXPORT variable', nm)
                continue
            # LOCAL
            if re.match(r'^\s*LOCAL\b', code):
                names = re.findall(r'[A-Za-z_][A-Za-z0-9_]*', re.sub(r':=\s*[^,;]+', '', code.replace('LOCAL', '')))
                if len(names) > 6: errs.append((ln, 'E3', 'LOCAL with %d names (max 6)' % len(names)))
                for nm in names:
                    if nm in RESERVED or re.fullmatch(r'[a-z]', nm): errs.append((ln, 'E4', 'reserved/single-letter variable %r' % nm))
                    e11(ln, 'LOCAL', nm)
                if not stack:
                    file_locals.update(names)
                else:
                    if len(stack) != 1 or stack[0][0] != 'BEGIN':
                        errs.append((ln, 'E6', 'LOCAL inside a block'))
                    elif body_started:
                        errs.append((ln, 'E6', 'LOCAL after other statements in the body'))
                    if cur: funcs[cur]['locals'].update(names)
                continue
            # block tracking on this line
            for m in re.finditer(r'\b(BEGIN|IF|IFERR|FOR|WHILE|CASE|REPEAT|END|UNTIL)\b', code):
                kw = m.group(1)
                if kw == 'BEGIN':
                    stack.append(('BEGIN', ln)); cur = pending_header; pending_header = None; body_started = False
                elif kw in ('IF', 'IFERR', 'FOR', 'WHILE', 'CASE', 'REPEAT'):
                    stack.append((kw, ln))
                elif kw == 'END':
                    if not stack: errs.append((ln, 'E2', 'END with nothing open')); continue
                    top = stack.pop()
                    if top[0] == 'REPEAT': errs.append((ln, 'E2', 'END closes a REPEAT opened at line %d (needs UNTIL)' % top[1]))
                    if top[0] == 'BEGIN': cur = None
                elif kw == 'UNTIL':
                    if not stack or stack[-1][0] != 'REPEAT':
                        errs.append((ln, 'E2', 'UNTIL without an open REPEAT'))
                    else: stack.pop()
            if stack and stack[0][0] == 'BEGIN' and not re.match(r'^\s*(BEGIN|END)\b', code):
                body_started = True
            # identifier uses and calls
            for m in IDENT.finditer(code):
                nm = m.group(0)
                if nm in KEYWORDS: continue
                if re.match(r'^[0-9]', nm): continue
                rest = code[m.end():]
                if rest.lstrip().startswith('('):
                    calls.setdefault(nm, []).append(ln)
                used.setdefault(nm, set()).add(ln)
                if cur: funcs[cur]['uses'].add(nm)
            # W1 semicolon heuristic (skip when the next code line continues the expression)
            st = s
            nxt = ''
            for ln2, code2, _, _ in code_lines:
                if ln2 > ln and code2.strip(): nxt = code2.strip(); break
            if re.match(r'^[+\-*/]', nxt) or nxt.startswith(')'): st = st + ';'
            if not re.search(r'(;|THEN|DO|ELSE|BEGIN|CASE|REPEAT|DEFAULT|\{|,|\(|\+|-|\*|/|AND|OR)\s*$', st) \
               and not re.match(r'^(IF|IFERR|FOR|WHILE|UNTIL|END|ELSE|CASE|DEFAULT|#|EXPORT|LOCAL|VIEW|START)\b', st) \
               and not re.match(r'^[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\)$', st):
                warns.append((ln, 'W1', 'line does not end in ;  ->  %s' % st[:60]))
        for kw, ln in stack: errs.append((ln, 'E2', '%s opened here is never closed' % kw))
        # E1: calls to undefined names
        hexlit = re.compile(r'^[0-9A-Fa-f]+h$')
        for nm, lines in calls.items():
            if nm in funcs or nm in wl or nm.lower() in wl_lower or nm in GLOBALS or nm in file_locals or nm in exports: continue
            # list/variable indexing like gbCnt(i) is a call-looking use of a declared variable
            declared = any(nm in f['locals'] or nm in f['params'] for f in funcs.values())
            if declared: continue
            errs.append((lines[0], 'E1', 'call to %r: not defined here and not in the command whitelist' % nm))
        # E7: identifiers used but never declared
        all_declared = set(funcs) | wl | GLOBALS | file_locals | exports | {'G0'}
        for f in funcs.values(): all_declared |= set(f['locals']) | set(f['params'])
        for nm, lines in used.items():
            if nm in all_declared or nm.lower() in wl_lower or hexlit.match(nm) or nm in KEYWORDS: continue
            if re.fullmatch(r'[0-9]+', nm): continue
            errs.append((min(lines), 'E7', 'identifier %r is never declared (typo?)' % nm))
        # W2: unused locals
        for fname, f in funcs.items():
            for nm in sorted(f['locals']):
                if nm not in f['uses'] or len([1 for ln, code, _, _ in code_lines if nm in IDENT.findall(code) and not code.strip().startswith('LOCAL')]) == 0:
                    warns.append((f['line'], 'W2', 'LOCAL %r in %s is never used' % (nm, fname)))
        # W3: TEXTOUT_P literal width
        for ln, code, strs, raw in code_lines:
            m = re.search(r'TEXTOUT_P\s*\((.*)', raw)
            if not m: continue
            args = m.group(1)
            # split top-level commas
            depth = 0; parts = []; curp = ''
            instr = False
            for ch in args:
                if ch == '"': instr = not instr
                if not instr:
                    if ch in '([{': depth += 1
                    if ch in ')]}': depth -= 1
                    if depth < 0: break
                    if ch == ',' and depth == 0: parts.append(curp); curp = ''; continue
                curp += ch
            parts.append(curp)
            if len(parts) < 5: continue
            textexpr = parts[0]
            lits = re.findall(r'"([^"]*)"', textexpr)
            nchar = sum(len(t) for t in lits) + 4 * len(re.findall(r'STRING\(|gbF\(|dmF\(|trF\(|tcF\(', textexpr)) + len(re.findall(r'CHAR\(', textexpr))
            try:
                xpos = int(parts[2].strip()) if re.fullmatch(r'\s*\d+\s*', parts[2]) else None
                font = int(parts[4].strip()) if re.fullmatch(r'\s*\d+\s*', parts[4]) else 1
            except ValueError:
                xpos = None; font = 1
            px = {1: 6, 2: 7.6, 3: 8.6, 4: 10}.get(font, 6)
            if xpos is not None and xpos + nchar * px > 322:
                warns.append((ln, 'W3', 'TEXTOUT_P text ~%d px wide from x=%d (font %d) may run off the screen' % (nchar * px, xpos, font)))
        for ln, c, msg in sorted(errs): print('  %4d  %-4s %s' % (ln, c, msg))
        for ln, c, msg in sorted(warns): print('  %4d  %-4s %s' % (ln, c, msg))
        print('  -> %d errors, %d warnings, %d functions' % (len(errs), len(warns), len(funcs)))
        if errs: status = 1
    sys.exit(status)

main()
