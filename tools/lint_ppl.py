"""
lint_ppl.py — structural lint for an HP Prime PPL source file.

10 Oct 2026: builtin-name collisions are now checked case-insensitively for FILE-LEVEL
LOCALs, EXPORT variables and function names too (csC is CSC; ChiSquare is CHISQUARE), and
the paths follow this file instead of C:\HP-Prime.

Generalised from lint_SampDist.py (29 Jul 2026), which had the checks but
hard-coded SampDist's function count and EXPORT set. This version derives
both from the file, so it runs on any program in the fleet.

Checks the things that fail on the device rather than in Python:
  1  block balance (REPEAT is closed by UNTIL, NOT by END)
  2  LOCAL statement sizes (<= 6 names, the house rule)
  3  LOCAL only at the top of a BEGIN block, never inside IF/CASE/FOR/WHILE
  4  INPUT var/label/help list lengths match, and the return is assigned
  5  CHOOSE index reset to 0 immediately before every call, return not tested
  6  reserved words and builtin names, in LOCALs AND in parameter lists
  7  no mode-1 STRING() with a nonzero digit count
  8  EXPORT limited to the entry point and EP_* results
  9  no raw number concatenated into a display string
 10  no U+0304 combining macron (x-bar must be CHAR(57344))
 11  every drawing call targets a GROB (the Burr3 invariant)
 12  no bare WAIT as a key hold

Usage:  python lint_ppl.py SampDist.txt
        python lint_ppl.py NormExp.txt
"""

import io
import os
import re
import sys

BUILTINS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HP_Prime_Builtin_Names.txt")

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

if len(sys.argv) < 2:
    print(__doc__)
    sys.exit(2)

SRC = sys.argv[1]
if not os.path.isabs(SRC) and not os.path.exists(SRC):
    # 16 Oct 2026: a relative path is read from the current folder first; the
    # script's own folder is only the fallback (it used to be the only place
    # looked, so a relative path from another folder failed and the gate's
    # grep made the failure look like a clean lint).
    SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), SRC)
ENTRY = os.path.splitext(os.path.basename(SRC))[0]

PROBLEMS = []
NCHECK = 0


def bad(msg):
    PROBLEMS.append(msg)


def check(cond, msg):
    global NCHECK
    NCHECK += 1
    if not cond:
        bad(msg)


raw = open(SRC, encoding="utf-8").read()
lines = raw.split("\n")


def strip_line(s):
    """Blank out comments and string literals, preserving column positions."""
    out, in_str, i = [], False, 0
    while i < len(s):
        c = s[i]
        if in_str:
            if c == '"':
                in_str = False
            out.append(" ")
        else:
            if c == '"':
                in_str = True
                out.append(" ")
            elif c == "/" and i + 1 < len(s) and s[i + 1] == "/":
                # pad the comment with spaces rather than truncating, so
                # offsets stay aligned with the raw text
                out.append(" " * (len(s) - i))
                break
            else:
                out.append(c)
        i += 1
    return "".join(out)


code = [strip_line(l) for l in lines]
codetext = "\n".join(code)

print(f"=== {os.path.basename(SRC)}  (entry point: {ENTRY}) ===")

# ---------------------------------------------------------------- 10
print("10. combining macron")
hits = [i + 1 for i, l in enumerate(lines) if "\u0304" in l]
check(not hits, f"U+0304 combining macron on lines {hits} - use CHAR(57344)")

# ---------------------------------------------------------------- 1
print(" 1. block balance")
OPEN = re.compile(r"\b(BEGIN|IF|CASE|FOR|WHILE|IFERR)\b")
CLOSE = re.compile(r"\bEND\b")
REP = re.compile(r"\bREPEAT\b")
UNT = re.compile(r"\bUNTIL\b")

depth = rdepth = 0
for i, l in enumerate(code):
    depth += len(OPEN.findall(l)) - len(CLOSE.findall(l))
    rdepth += len(REP.findall(l)) - len(UNT.findall(l))
    if depth < 0:
        bad(f"line {i+1}: block depth went negative")
        break
check(depth == 0, f"unbalanced blocks: final depth {depth} (want 0)")
check(rdepth == 0, f"unbalanced REPEAT/UNTIL: {rdepth} (want 0)")

# ---------------------------------------------------------------- functions
FNDEF = re.compile(r"^\s*(EXPORT\s+)?([A-Za-z_][A-Za-z_0-9]*)\s*\(([^)]*)\)\s*$")
funcs = []
i = 0
while i < len(code):
    m = FNDEF.match(code[i])
    if m and i + 1 < len(code) and code[i + 1].strip() == "BEGIN":
        name, exported = m.group(2), bool(m.group(1))
        params = [p.strip() for p in m.group(3).split(",") if p.strip()]
        d, j = 0, i + 1
        while j < len(code):
            d += len(OPEN.findall(code[j])) - len(CLOSE.findall(code[j]))
            if d == 0:
                break
            j += 1
        funcs.append((name, exported, params, i, j))
        i = j
    i += 1
print(f"    {len(funcs)} functions: " + ", ".join(f[0] for f in funcs))
check(any(f[0] == ENTRY for f in funcs), f"no function named {ENTRY} found")

# ---------------------------------------------------------------- 2 + 3
print(" 2. LOCAL statement sizes (<=6)")
print(" 3. LOCAL placement (top of BEGIN only)")
LOCALRE = re.compile(r"^\s*LOCAL\s+(.*?);\s*$")
all_locals = {}
for name, exported, params, s, e in funcs:
    seen_exec, depth_in = False, 0
    for k in range(s + 1, e + 1):
        l, st = code[k], code[k].strip()
        if not st:
            continue
        m = LOCALRE.match(l)
        if m:
            names = [p.split(":=")[0].strip()
                     for p in m.group(1).split(",") if p.split(":=")[0].strip()]
            check(len(names) <= 6,
                  f"{name} line {k+1}: LOCAL declares {len(names)} names (max 6, the house rule)")
            check(depth_in == 0, f"{name} line {k+1}: LOCAL inside a nested block")
            check(not seen_exec, f"{name} line {k+1}: LOCAL after executable code")
            all_locals.setdefault(name, []).extend(names)
        elif st not in ("BEGIN", "END;"):
            seen_exec = True
        depth_in += len(OPEN.findall(l)) - len(CLOSE.findall(l))
        if st == "BEGIN":
            depth_in = 0

# ---------------------------------------------------------------- 6
print(" 6. reserved words and builtin collisions")
KEYWORDS = {"STEP", "KEY", "TO", "FROM", "DO", "OR", "AND", "NOT", "MOD", "E",
            "RE", "IM", "CASE", "DEFAULT", "LOCAL", "EXPORT", "BEGIN", "END",
            "RETURN", "IF", "THEN", "ELSE", "FOR", "WHILE", "REPEAT", "UNTIL"}
try:
    btext = open(BUILTINS, encoding="utf-8", errors="replace").read()
    BUILT_UP = {t.upper() for t in re.split(r"[\s,()]+", btext) if t}
except OSError:
    BUILT_UP = set()
    bad("could not read the builtin name table")

for name, exported, params, s, e in funcs:
    for p in params:
        check(p.upper() not in KEYWORDS, f"{name}: parameter '{p}' is a keyword")
        # the parameter parser is stricter than the LOCAL parser (fp / col / ref)
        check(p.upper() not in BUILT_UP,
              f"{name}: parameter '{p}' collides with a builtin name")
    for v in all_locals.get(name, []):
        check(v.upper() not in KEYWORDS, f"{name}: LOCAL '{v}' is a keyword")
        if v.upper() in BUILT_UP:
            bad(f"{name}: LOCAL '{v}' shadows a builtin name (rename)")
        NCHECK += 1
    # 10 Oct 2026: the Prime matches builtin names case-INsensitively at paste time --
    # a program named ChiSquare is CHISQUARE (device-found, ChiSquare beta 1a)
    check(name.upper() not in BUILT_UP or name in ("",),
          f"function '{name}' is a builtin name when case is ignored (rename the program)")

# file-level LOCALs (program-level state) and EXPORT variables, same rules.
# 10 Oct 2026: "LOCAL csR, csC, ..." at file level was rejected on the G2 with the
# cursor after csC -- csC is CSC, the cosecant.
_in_func = [False] * len(code)
for name, exported, params, s, e in funcs:
    for k in range(s, e + 1):
        _in_func[k] = True
for k, l in enumerate(code):
    if _in_func[k]:
        continue
    m = LOCALRE.match(l)
    names = []
    if m:
        names = [p.split(":=")[0].strip() for p in m.group(1).split(",") if p.split(":=")[0].strip()]
        check(len(names) <= 6, f"line {k+1}: file-level LOCAL declares {len(names)} names (max 6)")
    elif re.match(r"\s*EXPORT\s+[A-Za-z_]", l) and not re.search(r"\)\s*;?\s*$", l):
        names = re.findall(r"[A-Za-z_]\w*", re.sub(r":=\s*[^,;]+", "", l.replace("EXPORT", "")))
    for v in names:
        check(v.upper() not in KEYWORDS, f"line {k+1}: file-level '{v}' is a keyword")
        check(v.upper() not in BUILT_UP, f"line {k+1}: file-level '{v}' is a builtin name when case is ignored (rename)")

# ---------------------------------------------------------------- 4
print(" 4. INPUT list lengths and return assigned")
for m in re.finditer(r"INPUT\s*\(", codetext):
    start = m.end() - 1
    d, j = 0, start
    while j < len(codetext):
        if codetext[j] == "(":
            d += 1
        elif codetext[j] == ")":
            d -= 1
            if d == 0:
                break
        j += 1
    stmt = codetext[start:j + 1]
    lineno = codetext[:m.start()].count("\n") + 1
    braces = re.findall(r"\{([^{}]*)\}", stmt)
    check(len(braces) >= 3,
          f"line {lineno}: INPUT has {len(braces)} list args (want vars/labels/help)")
    if len(braces) >= 3:
        # string literals are blanked to spaces, so count top-level commas
        counts = [0 if b == "" else b.count(",") + 1 for b in braces[:3]]
        check(counts[0] == counts[1] == counts[2],
              f"line {lineno}: INPUT var/label/help counts {counts} disagree")
    pre = codetext[max(0, m.start() - 40):m.start()]
    check(":=" in pre,
          f"line {lineno}: INPUT return discarded (cancel proceeds silently)")

# ---------------------------------------------------------------- 5
print(" 5. CHOOSE init-0 pattern")
for m in re.finditer(r"CHOOSE\s*\(\s*([A-Za-z_][A-Za-z_0-9]*)", codetext):
    var = m.group(1)
    lineno = codetext[:m.start()].count("\n") + 1
    assigns = list(re.finditer(rf"\b{re.escape(var)}\s*:=\s*([^;]+);",
                               codetext[:m.start()]))
    check(bool(assigns) and assigns[-1].group(1).strip() == "0",
          f"line {lineno}: CHOOSE index '{var}' not reset to 0 immediately before")
    # never test CHOOSE's return value -- v1 of NormExp did exactly this
    lastline = codetext[max(0, m.start() - 40):m.start()].split("\n")[-1]
    check(":=" not in lastline,
          f"line {lineno}: CHOOSE return value is being captured/tested "
          f"(use the index)")

# ---------------------------------------------------------------- 7
print(" 7. no mode-1 STRING with decimals")
for m in re.finditer(r"STRING\s*\(([^()]*(?:\([^()]*\)[^()]*)*)\)", codetext):
    parts = [a.strip() for a in m.group(1).split(",")]
    lineno = codetext[:m.start()].count("\n") + 1
    if len(parts) == 3:
        if parts[1] == "1":
            check(parts[2] == "0",
                  f"line {lineno}: STRING(...,1,{parts[2]}) is mode 1 with "
                  f"decimals - drops trailing zeros")
    else:
        bad(f"line {lineno}: STRING() with {len(parts)} args, want 3")

# ---------------------------------------------------------------- 8
print(" 8. EXPORT discipline")
exports = re.findall(r"(?m)^EXPORT\s+([A-Za-z_][A-Za-z_0-9]*)", codetext)
for x in exports:
    check(x == ENTRY or x.startswith("EP_"),
          f"EXPORT {x} is neither the entry point nor an EP_* result")
check(ENTRY in exports, f"the entry point {ENTRY} is not EXPORTed")
for name, exported, params, s, e in funcs:
    if name != ENTRY:
        check(not exported, f"helper '{name}' is EXPORTed - it will show in the catalog")

# ---------------------------------------------------------------- 9
print(" 9. no raw number concatenated into a display string")
# derive the string-valued locals: assigned from an expression that contains
# a literal, a STRING()/fmtp()/CHAR() call, or another known string var
strvars = set()
for _ in range(3):                      # transitive closure, cheap
    for m in re.finditer(r"([A-Za-z_][A-Za-z_0-9]*)\s*:=\s*([^;]+);", raw):
        v, rhs = m.group(1), m.group(2)
        if ('"' in rhs or "STRING(" in rhs or "fmtp(" in rhs
                or "CHAR(" in rhs or any(f"{s} " in rhs for s in strvars)):
            strvars.add(v)
def scan_concat(expr, base_depth, lineno, where):
    """Flag bare identifiers concatenated at the expression's top level.

    Only '+' at base_depth is string concatenation: a flat scan also hits the
    arithmetic inside a nested call, and STRING(mu+sg,2,1) is not a
    concatenation of sg.
    """
    global NCHECK
    NCHECK += 1
    d = 0
    for pos, ch in enumerate(expr):
        if ch == "(":
            d += 1
        elif ch == ")":
            d -= 1
        elif ch == "+" and d == base_depth:
            t = re.match(r"\+\s*([A-Za-z_][A-Za-z_0-9]*)\s*(?![\w(])", expr[pos:])
            if t and t.group(1) not in strvars:
                bad(f"line {lineno}: {where} concatenates bare '{t.group(1)}' "
                    f"- formatting would follow the user's Home number setting")


# (a) inside the display calls themselves
for call in ("TEXTOUT_P", "MSGBOX"):
    for m in re.finditer(rf"{call}\s*\(", codetext):
        start = m.end() - 1
        d, j = 0, start
        while j < len(codetext):
            if codetext[j] == "(":
                d += 1
            elif codetext[j] == ")":
                d -= 1
                if d == 0:
                    break
            j += 1
        lineno = codetext[:m.start()].count("\n") + 1
        scan_concat(codetext[start:j + 1], 1, lineno, call)

# (b) in the assignments that BUILD display strings. Both SampDist and
# NormExp assemble s1/s2 first and pass the variable, so scanning only the
# display call misses the concatenation entirely -- caught by injecting a
# real defect and watching the lint stay silent.
for m in re.finditer(r"([A-Za-z_][A-Za-z_0-9]*)\s*:=\s*([^;]+);", codetext):
    if '"' not in raw[m.start(2):m.end(2)]:
        continue                        # not building a string
    lineno = codetext[:m.start()].count("\n") + 1
    scan_concat(m.group(2), 0, lineno, f"assignment to '{m.group(1)}'")

# ---------------------------------------------------------------- 11 + 12
print("11. all drawing calls target a GROB")
for fn in ("LINE_P", "RECT_P", "PIXON_P", "DIMGROB_P"):
    for m in re.finditer(rf"\b{fn}\s*\(\s*([A-Za-z_0-9]+)", codetext):
        lineno = codetext[:m.start()].count("\n") + 1
        check(m.group(1).startswith("G"),
              f"line {lineno}: {fn} targets '{m.group(1)}', not a GROB")
for m in re.finditer(r"\bTEXTOUT_P\s*\(", codetext):
    start = m.end() - 1
    d, j = 0, start
    while j < len(codetext):
        if codetext[j] == "(":
            d += 1
        elif codetext[j] == ")":
            d -= 1
            if d == 0:
                break
        j += 1
    stmt = codetext[start + 1:j]
    lineno = codetext[:m.start()].count("\n") + 1
    parts, d2, cur = [], 0, ""
    for ch in stmt:
        if ch == "(":
            d2 += 1
        elif ch == ")":
            d2 -= 1
        if ch == "," and d2 == 0:
            parts.append(cur)
            cur = ""
        else:
            cur += ch
    parts.append(cur)
    got = parts[1].strip() if len(parts) > 1 else "?"
    check(got.startswith("G"),
          f"line {lineno}: TEXTOUT_P 2nd arg is '{got}', not a GROB")

print("12. no bare WAIT as a key hold")
check(not re.search(r"\bWAIT\s*;", codetext),
      "bare 'WAIT;' found - use REPEAT kk := GETKEY; UNTIL kk > -1")

# ----------------------------------------------------------------------
print()
print(f"{NCHECK} checks, {len(PROBLEMS)} problems")
for p in PROBLEMS:
    print("  PROBLEM " + p)
if not PROBLEMS:
    print("LINT CLEAN")
sys.exit(1 if PROBLEMS else 0)
