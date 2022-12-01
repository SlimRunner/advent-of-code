import sys
import re
from itertools import product

def main(args):
    pre = lambda x: x
    if "-ex" in args:
        data = getLines("data.ex.txt", pred = pre)
    else:
        data = getLines("data.in.txt", pred = pre)
    p1, p2 = [findStart(i) - 1 for i in data]
    print("part 1: ", warmupWin(p1, p2))
    print(quantumWin(p1, p2, 3, 2))
    # my answer: 309196008717909
    # 4961122
    # 143173

def quantumWin(p1, p2, dn, lim):
    tr = [list(range(1, dn + 1)) for _ in range(1, dn + 1)]
    tset = [sum(i) for i in list(product(*tr))]
    slate = {v:tset.count(v) for v in set(tset)}
    # stack = [((0,0), (p1, p2), k, v, True) for k,v in slate.items()]
    # foo = {}
    # return (qRecWin(0, 0, p1, p2, 0, 0, True, slate, 21, foo), foo)
    return qRecWin(0, 0, p1, p2, 0, 0, True, slate, lim, {})

def qRecWin(s1, s2, p1, p2, throw, fact, turn, slate, lim, cache):
    if (p1, p2, throw % 10) in cache:
        return tuple(i * fact for i in cache[(p1, p2, throw % 10)])
    win1, win2 = 0, 0
    for t, freq in slate.items():
        print(t)
        if turn:
            pn = (p1 + throw) % 10
            if (s1 + pn + 1) >= lim:
                w1, w2 = (fact, 0)
            w1, w2 = qRecWin(
                s1 + pn + 1, s2, pn, p2,
                t + throw, freq + fact,
                not turn, slate, lim, cache)
        else:
            pn = (p2 + throw) % 10
            if (s2 + pn + 1) >= lim:
                w1, w2 = (0, fact)
            w1, w2 = qRecWin(
                s1, s2 + pn + 1, p1, pn,
                t + throw, freq + fact,
                not turn, slate, lim, cache)
        win1 += w1
        win2 += w2
    cache[(p1, p2, throw % 10)] = (win1, win2)
    return (win1, win2)

def qIterWin(p1, p2, dn, lim):
    tr = [list(range(1, dn + 1)) for _ in range(1, dn + 1)]
    tset = [sum(i) for i in list(product(*tr))]
    slate = {v:tset.count(v) for v in set(tset)}
    print(slate)
    stack = [((0,0), (p1, p2), k, v, True) for k,v in slate.items()]
    w1, w2 = 0, 0
    i = 0
    m, M = len(stack), len(stack)
    mode = {}
    while len(stack) > 0:
        # L = len(stack)
        # if L in mode:
        #     mode[L] += 1
        # else:
        #     mode[L] = 1
        # m = min(m, len(stack))
        # M = max(M, len(stack))
        # if (i % 100000) == 0: print("(", m, M, max(mode, key=mode.get), ")", len(stack), end = "\r")
        # if (i % 100000) == 0:
        #     print(w1, w2)
            # print(stack[-1])
        i += 1
        (s1, s2), (p1, p2), throw, freq, turn = stack.pop()
        if turn:
            p1 = (p1 + throw) % 10
            s1 += p1 + 1
        else:
            p2 = (p2 + throw) % 10
            s2 += p2 + 1
        if s1 >= lim:
            w1 += freq
            continue
        elif s2 >= lim:
            w2 += freq
            continue
        else:
            stack.extend([
                ((s1, s2), (p1, p2), k + throw, v + freq, not turn)
                for k,v in slate.items()])
    return (w1, w2)

def warmupWin(p1, p2):
    turn = True
    v1 = 0
    v2 = 0
    i = 0
    while v1 < 1000 and v2 < 1000:
        i += 1
        if turn:
            p1 = (p1 + die100(i)) % 10
            v1 += p1 + 1
            turn = False
        else:
            p2 = (p2 + die100(i)) % 10
            v2 += p2 + 1
            turn = True
        vw = v1 if v1 < 1000 else v2
    return i * 3 * vw

def findStart(s):
    return int(s[s.find(": ") + 2:])

def die100(n):
    return 9 * n - 3

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
