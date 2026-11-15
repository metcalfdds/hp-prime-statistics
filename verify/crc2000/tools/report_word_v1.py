# report_word_v1.py FILE... : "slips" -> "misfigures" in the report (the author, 15 Nov 2026, 10:40). Exact replacements, each must be found once.
import sys
R = [
 ("### Slips in the text, seen in passing and not counted", "### Errors in the text, seen in passing and not counted"),
 ("- **separate slips**: one cell, one label or one heading set wrong.", "- **separate misfigures** (the author's word; a misfigure is an incorrect number or figure, and `model.json` and the scripts call them slips): one cell, one label or one heading set wrong."),
 ("| Pages with | 0 slips | 1 | 2 | 3 or more |", "| Pages with | 0 misfigures | 1 | 2 | 3 or more |"),
 ("The variance of the slips is 2.76 times their mean", "The variance of the misfigures is 2.76 times their mean"),
 ("| Separate slips per page |", "| Separate misfigures per page |"),
 ("the Poisson interval for slips,", "the Poisson interval for misfigures,"),
 ("apart from the four slips listed.", "apart from the four errors listed."),
]
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        assert s.count(a) == 1, (f, a, s.count(a))
        s = s.replace(a, b)
    assert 'slips' not in s.replace('call them slips', ''), f
    open(f, 'w', encoding='utf-8').write(s)
    print('ok', f, s.count('misfigure'))
