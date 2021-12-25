import sys
import re

def main(args):
    pre = lambda x: x
    if "-ex" in args:
        data = getLines("data.ex.txt", pred = pre)
    else:
        data = getLines("data.in.txt", pred = pre)
    p1, p2 = [findStart(i) - 1 for i in data]
    print("part 1: ", warmupWin(p1, p2))
    # print(quantumWin(p1, p2, 0, 0, True, []))

def quantumWin(p1, p2, v1, v2, turn, cache):
    print(p1, p2, v1, v2, turn, cache)
    if v1 > 5: return (1, 0)
    if v2 > 5: return (0, 1)
    # if (p1, p2)
    # a = [sum(i) for i in list(product([1,2,3],[1,2,3],[1,2,3]))]
    # {v:a.count(v) for v in set(a)}
    throws = {3: 1, 4: 3, 5: 6, 6: 7, 7: 6, 8: 3, 9: 1}
    w1, w2 = 0, 0
    for t in throws:
        if turn:
            w1, w2 = quantumWin(
                (p1 + t) % 10, p2,
                v1 + p1 + 1, v2,
                not turn, [])
        else:
            w1, w2 = quantumWin(
                p1, (p2 + t) % 10,
                v1, v2 + p2 + 1,
                not turn, [])
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
