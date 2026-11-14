# -*- coding: utf-8 -*-
"""check_tbl2x2_v2.py -- the example program of docs/ppl-rules-for-any-assistant.md, version 2 (14 Nov 2026): checks that the
example in the document is this file byte for byte, then runs it in the PC harness (tools/ppl_run_v3e.py, strict, idle key Esc)
with the default table, Cancel, a count over 100,000, and a row of zeros.  The gate's own output is gate_v1e.txt beside this file
(tools/ppl_gate_v1e.py, run where the hp-prime-kit zip sits, as CLAUDE.md says).  Run from the repository's top folder."""
import io, os, sys
sys.path.insert(0, 'tools')
import ppl_run_v3e as P
HERE = os.path.dirname(os.path.abspath(__file__)); F = os.path.join(HERE, 'TBL2X2.txt')
doc = io.open('docs/ppl-rules-for-any-assistant.md', encoding='utf-8').read()
code = doc[doc.rindex('```\n//') + 4:doc.rindex('```')]
print('example in the document == TBL2X2.txt:', code == io.open(F, encoding='utf-8').read())
def run(label, ans):
    h = P.Harness(F, strict=True, idle_key=4)
    if ans is not None: h.answer(ans)
    try: out = 'returned %r' % (h.execute('TBL2X2()'),)
    except Exception as e: out = '%s: %s' % (type(e).__name__, str(e)[:120])
    print('%-14s %s | warnings %d | message boxes %s' % (label, out, len(h.warnings), [m.text if hasattr(m, 'text') else str(m) for m in getattr(h, 'msgboxes', [])]))
run('default table', P.ACCEPT)
run('Cancel', P.CANCEL)
run('count 200000', [200000, None, None, None])
run('a row of 0', [0, 0, None, None])
