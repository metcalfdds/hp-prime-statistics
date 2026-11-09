import collections
_P = None
DROP = set()      # (program, old) done by hand in the build
def load():
    global _P
    if _P is None:
        ns = {}
        exec(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)), '..', 'proposals.py'), encoding='utf-8').read(), ns)
        _P = ns['P']
    return _P
def for_prog(prog):
    d = collections.OrderedDict()
    for p, pg, o, n, w in load():
        if p == prog and not o.startswith('[') and (p, o) not in DROP:
            if p == 'AgreeLab' and o.startswith('bias ='):      # the drawn d-bar (make_round11's marker CHAR(20))
                o, n = 'bias = \x14;', 'bias = \x14, the mean difference;'
            d.setdefault(pg, []).append((o, n))
    return d
