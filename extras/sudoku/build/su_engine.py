# Sudoku beta 2: a line-for-line Python copy of the PPL engine (suEInit, suEPut, suETake, suEBest, suESolve),
# used by the build script to grade the base puzzles and by the verify script to check the PPL against it.
ROW = [0] + [(k - 1) // 9 + 1 for k in range(1, 82)]
COL = [0] + [(k - 1) % 9 + 1 for k in range(1, 82)]
BOX = [0] + [3 * ((k - 1) // 27) + ((k - 1) % 9) // 3 + 1 for k in range(1, 82)]
UNIT = [0] * (27 * 9 + 1)                      # UNIT[(u-1)*9+n] = the n-th square of unit u
for k in range(1, 82):
    UNIT[(ROW[k] - 1) * 9 + COL[k]] = k
    UNIT[(9 + COL[k] - 1) * 9 + ROW[k]] = k
    UNIT[(18 + BOX[k] - 1) * 9 + 3 * ((ROW[k] - 1) % 3) + ((COL[k] - 1) % 3) + 1] = k
PEER = [0] * (81 * 20 + 1)                     # PEER[(k-1)*20+j], j = 1..20, in square order
for k in range(1, 82):
    ps = [p for p in range(1, 82) if p != k and (ROW[p] == ROW[k] or COL[p] == COL[k] or BOX[p] == BOX[k])]
    assert len(ps) == 20
    for j, p in enumerate(ps, 1): PEER[(k - 1) * 20 + j] = p

class Engine:
    def __init__(self, clues):                 # clues: 81 digits, 0 = blank; returns with .bad set if two clues clash
        self.V = [0] * 82; self.H = [0] * 244; self.C = [0] * 82; self.P = [0] * 244; self.bad = 0
        for k in range(1, 82):
            d = clues[k - 1]
            if d:
                us = (ROW[k], 9 + COL[k], 18 + BOX[k])
                if any(self.H[(u - 1) * 9 + d] for u in us): self.bad = k; return
                for u in us: self.H[(u - 1) * 9 + d] = 1
                self.V[k] = d
        for k in range(1, 82):
            if self.V[k] == 0:
                n = 0
                for d in range(1, 10):
                    if self.cand(k, d):
                        n += 1
                        for u in (ROW[k], 9 + COL[k], 18 + BOX[k]): self.P[(u - 1) * 9 + d] += 1
                self.C[k] = n
    def cand(self, k, d):
        H = self.H
        return H[(ROW[k] - 1) * 9 + d] == 0 and H[(9 + COL[k] - 1) * 9 + d] == 0 and H[(18 + BOX[k] - 1) * 9 + d] == 0
    def put(self, k, d):
        us = (ROW[k], 9 + COL[k], 18 + BOX[k])
        for e in range(1, 10):                 # k leaves the empty squares
            if self.cand(k, e):
                for u in us: self.P[(u - 1) * 9 + e] -= 1
        for j in range(1, 21):                 # its empty peers lose d
            p = PEER[(k - 1) * 20 + j]
            if self.V[p] == 0 and self.cand(p, d):
                self.C[p] -= 1
                for u in (ROW[p], 9 + COL[p], 18 + BOX[p]): self.P[(u - 1) * 9 + d] -= 1
        for u in us: self.H[(u - 1) * 9 + d] = 1
        self.V[k] = d
    def take(self, k, d):
        us = (ROW[k], 9 + COL[k], 18 + BOX[k])
        self.V[k] = 0
        for u in us: self.H[(u - 1) * 9 + d] = 0
        for j in range(1, 21):
            p = PEER[(k - 1) * 20 + j]
            if self.V[p] == 0 and self.cand(p, d):
                self.C[p] += 1
                for u in (ROW[p], 9 + COL[p], 18 + BOX[p]): self.P[(u - 1) * 9 + d] += 1
        n = 0
        for e in range(1, 10):
            if self.cand(k, e):
                n += 1
                for u in us: self.P[(u - 1) * 9 + e] += 1
        self.C[k] = n
    def best(self):
        fewest, kind, which, need = 10, 0, 0, 0
        k = 1
        while k <= 81 and fewest > 1:
            if self.V[k] == 0 and self.C[k] < fewest: fewest, kind, which = self.C[k], 1, k
            k += 1
        u = 1
        while u <= 27 and fewest > 1:
            d = 1
            while d <= 9 and fewest > 1:
                i = (u - 1) * 9 + d
                if self.H[i] == 0 and self.P[i] < fewest: fewest, kind, which, need = self.P[i], 2, u, d
                d += 1
            u += 1
        return kind, which, need, fewest
    def solve(self, want=1, log=None):
        """Depth-first search as the PPL's suESolve.  want=1: stop at the first answer; want=2: look for a second.
        Returns (solutions, first answer as 81 digits or None, stats dict)."""
        LK, LW, LN, LO, LC, LD, LF = ([0] * 82 for _ in range(7))
        depth = 0; sols = 0; first = None
        st = dict(steps=0, undos=0, naked=0, hidden=0, guesses=0)
        while True:
            kind, which, need, fewest = self.best()
            if kind == 0:
                sols += 1
                if sols == 1: first = self.V[1:82]
                if sols >= want: return sols, first, st
                fewest = 0                     # look further: treat the answer as a dead end
            if kind != 0 and fewest > 0:
                depth += 1
                LK[depth], LW[depth], LN[depth], LO[depth], LF[depth] = kind, which, need, 0, fewest
            placed = 0
            while placed == 0 and depth > 0:
                opt = LO[depth]
                if opt > 0:
                    self.take(LC[depth], LD[depth]); st['undos'] += 1
                    if log is not None: log.append(('undo', LC[depth], LD[depth]))
                found = 0
                while found == 0 and opt < 9:
                    opt += 1
                    if LK[depth] == 1: k, d = LW[depth], opt
                    else: k, d = UNIT[(LW[depth] - 1) * 9 + opt], LN[depth]
                    if self.V[k] == 0 and self.cand(k, d): found = 1
                if found:
                    self.put(k, d)
                    LO[depth], LC[depth], LD[depth] = opt, k, d
                    st['steps'] += 1
                    if LF[depth] >= 2: st['guesses'] += 1; how = 'guess'
                    elif LK[depth] == 1: st['naked'] += 1; how = 'naked'
                    else: st['hidden'] += 1; how = 'hidden'
                    if log is not None: log.append((how, k, d))
                    placed = 1
                else:
                    depth -= 1
            if placed == 0: return sols, first, st

def solve_str(s, want=1):
    e = Engine([int(c) for c in s])
    if e.bad: return -1, None, None
    return e.solve(want)
