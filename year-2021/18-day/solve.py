import sys
import ast
from functools import reduce
from itertools import combinations, permutations
import copy

def main(args):
    # hs: hierachy string
    # hm: hierachy map
    pre = ast.literal_eval
    if "-ex" in args:
        data = getLines("data.ex.txt", pred = pre)
    else:
        data = getLines("data.in.txt", pred = pre)
    if "-p1" in args:
        L = listSum(data)
        print(L)
        Ls = fModulus(L)
        print(Ls)
    if "-p2" in args:
        nmax = None
        for (i, j) in permutations(range(0, len(data)), 2):
            p = copy.deepcopy(data[i])
            q = copy.deepcopy(data[j])
            m = fModulus(starSum(p, q))
            if nmax is None:
                nmax = m
            else:
                nmax = max(m, nmax)
        print(nmax)

def fModulus(L):
    A, B = L
    if isinstance(A, list):
        A = fModulus(A)
    if isinstance(B, list):
        B = fModulus(B)
    return 3 * A + 2 * B

def findDepth(L, depth, **kw):
    dcurr = 0 if "level" not in kw else kw["level"]
    pl = [] if "path" not in kw else kw["path"]
    if dcurr == depth:
        if isinstance(L, list):
            return (L, True, pl)
        else:
            return (None, False, [])
    elif isinstance(L, list):
        for i, l in enumerate(L):
            g, f, p = findDepth(l, depth, level = dcurr + 1, path = [*pl, i])
            if f: return (g, f, p)
    return (None, False, [])

def listSum(G):
    return reduce(starSum, G)

def starSum(a, b):
    c = [a, b]
    starReduce(c)
    return c

def starReduce(G):
    exp, sp = (True, True)
    while exp or sp:
        exp = explode(G)
        if exp: continue
        sp = split(G)

def explode(G):
    # A and B are going to explode
    # n1 and n2 are going to change
    # n1 is neighbor of A and n2 of B
    # n1, A, B, n2
    S, pmx = getFlat(str(G))
    # sub-group, was found, path to group
    g, f, pg = findDepth(G, max(4, pmx - 1))
    if not f: return False
    A, B, *_r = [i for i, (v, p) in enumerate(S) if p[:-1] == pg]
    if len(_r) > 0: raise ValueError("List has a non-integer pair.")
    n1, n2 = A - 1, B + 1
    # zero out pair
    assignNest(G, S[A][1][:-1], 0)
    if n1 >= 0:
        assignNest(G, S[n1][1], S[n1][0] + S[A][0])
    if n2 < len(S):
        assignNest(G, S[n2][1], S[n2][0] + S[B][0])
    return True

def split(G):
    S, pmx = getFlat(str(G))
    imax = next((i for i, [s, _] in enumerate(S) if s > 9), None)
    imas = [(i,s) for i, [s, _] in enumerate(S)]
    if imax is None: return False
    half = S[imax][0] // 2
    odd = S[imax][0] % 2
    ng = [half, half + odd]
    assignNest(G, S[imax][1], ng)
    return True

def getFlat(s):
    maxD = 0
    L = []
    p = []
    i = 0
    while i < len(s):
        c = s[i]
        if c == "[":
            p.append(0)
        elif c == "]":
            p.pop()
        elif c == ",":
            p[len(p) - 1] += 1
        elif c in "0123456789":
            if s[i + 1] in "0123456789":
                i += 1
                c += s[i]
            L.append([int(c), p.copy()])
        maxD = max(maxD, len(p))
        i += 1
    return (L, maxD)

def assignNest(l, p, v, **kw):
    lvl = 0 if "level" not in kw else kw["level"]
    i = p.pop(0)
    if len(p) != 0:
        assignNest(l[i], p, v)
    else:
        l[i] = v

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            line = line.strip()
            output.append(pred(line))
            line = f.readline()
    return output

if __name__ == '__main__':
    main(sys.argv)
