# su_gen.py -- Sudoku beta 2: makes the base puzzles (our own, from random grids) and grades them with the
# program's own solver (su_engine.py, the line-for-line Python copy of the PPL engine).
#   A full grid is filled at random; clues are taken away in pairs (k, 80 - k, so the puzzle keeps the
#   usual half-turn symmetry) as long as exactly one answer remains; the result is graded:
#     Easy    the only-digit step alone solves it (no only-square step, no guess); 36 to 40 clues
#     Medium  the only-square step is needed at least 5 times, but no guess; 28 to 34 clues
#     Hard    guesses are needed, with at most 30 taken back; 24 to 28 clues
#     Expert  guesses with more than 30 taken back; 26 clues or fewer
#   and kept only if an independent brute-force count (brute_count) also finds exactly one answer.
# Run:  python3 su_gen.py 2027   (the seed used on 26 Nov 2026; writes base_puzzles.json in the current folder,
#       6 puzzles a level). Sudoku_beta2_build.py then checks each one again before writing it into the program.
import random, json, sys, su_engine as E

def brute_count(g, limit=2):                     # independent check: plain backtracking, first empty square
    g = list(g)
    def ok(i, d):
        r, c = divmod(i, 9)
        for j in range(9):
            if g[r * 9 + j] == d or g[j * 9 + c] == d: return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for a in range(3):
            for b in range(3):
                if g[(br + a) * 9 + bc + b] == d: return False
        return True
    n = [0]
    def rec():
        try: i = g.index(0)
        except ValueError: n[0] += 1; return n[0] >= limit
        for d in range(1, 10):
            if ok(i, d):
                g[i] = d
                if rec(): return True
                g[i] = 0
        return False
    rec(); return n[0]

def full_grid(rng):
    g = [0] * 81
    def rec(i):
        if i == 81: return True
        r, c = divmod(i, 9); ds = list(range(1, 10)); rng.shuffle(ds)
        for d in ds:
            if all(g[r * 9 + j] != d for j in range(9)) and all(g[j * 9 + c] != d for j in range(9)) and \
               all(g[(3 * (r // 3) + a) * 9 + 3 * (c // 3) + b] != d for a in range(3) for b in range(3)):
                g[i] = d
                if rec(i + 1): return True
                g[i] = 0
        return False
    rec(0); return g

def grade(p):
    e = E.Engine(p); n, first, st = e.solve(1)
    return st

def level_of(p):
    st = grade(p)
    if st['guesses'] == 0 and st['hidden'] == 0: return 'Easy', st
    if st['guesses'] == 0: return 'Medium', st
    return ('Hard' if st['undos'] <= 30 else 'Expert'), st

def dig(sol, rng, target):
    p = list(sol); order = list(range(41)); rng.shuffle(order)      # pairs k, 80 - k (rotational symmetry)
    for i in order:
        j = 80 - i
        if sum(1 for x in p if x) <= target: break
        a, b = p[i], p[j]; p[i] = p[j] = 0
        e = E.Engine(p); n, _, _ = e.solve(2)
        if n != 1: p[i], p[j] = a, b
    return p

if __name__ == '__main__':
    rng = random.Random(int(sys.argv[1]) if len(sys.argv) > 1 else 2026)
    want = {'Easy': (38, 6), 'Medium': (30, 6), 'Hard': (24, 6), 'Expert': (22, 6)}
    got = {k: [] for k in want}
    tries = 0
    while any(len(got[k]) < want[k][1] for k in want) and tries < 3000:
        tries += 1
        sol = full_grid(rng)
        for lev in [k for k in want if len(got[k]) < want[k][1]]:
            p = dig(sol, rng, want[lev][0])
            L, st = level_of(p)
            clues = sum(1 for x in p if x)
            okc = {'Easy': 36 <= clues <= 40, 'Medium': 28 <= clues <= 34 and st['hidden'] >= 5,
                   'Hard': 24 <= clues <= 28, 'Expert': clues <= 26}
            if L in got and len(got[L]) < want[L][1] and okc[L] and brute_count(p) == 1:
                got[L].append({'p': ''.join(map(str, p)), 's': ''.join(map(str, sol)), 'clues': clues, 'st': st})
                break
    print('tries', tries, {k: len(v) for k, v in got.items()})
    json.dump(got, open('base_puzzles.json', 'w'), indent=1)
