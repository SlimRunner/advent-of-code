import re

def main():
    S, R = getLines("input.in.txt")
    LC = {}
    P = getPairs(S, LC)
    for i in range(0,10):
        P = applyRules(P, R, LC)
    print("10 iterations:", dictDiff(LC, LC))
    for i in range(10,40):
        P = applyRules(P, R, LC)
    print("40 iterations:",dictDiff(LC, LC))

def getLines(fn):
    template = ''
    with open(fn) as f:
        template = f.readline().strip()
        subs = []
        f.readline()
        line = f.readline()
        while line:
            line = line.strip()
            sepLoc = line.find(" -> ")
            pairing = (line[:sepLoc], line[sepLoc+4:])
            subs.append(pairing)
            line = f.readline()
    return (template, subs)

def dictDiff(a, b):
    return a[max(a, key = a.get)] - b[min(b, key = b.get)]

def addVK(d, k, v):
    if k in d:
        d[k] += v
    else:
        d[k] = v

def getPairs(seed, lCount):
    pairs = {}; idx = 0
    while idx < len(seed) - 1:
        addVK(lCount, seed[idx], 1)
        pair = seed[idx] + seed[idx + 1]
        if pair in pairs:
            pairs[pair] += 1
        else:
            pairs[pair] = 1
        idx += 1
    addVK(lCount, seed[idx], 1)
    return pairs

def applyRules(P, R, LC):
    NP = {}
    for p,v in P.items():
        for r in R:
            if r[0].find(p) >= 0:
                np = p[0] + r[1]
                addVK(LC, r[1], v)
                if np in NP:
                    NP[np] += v
                else:
                    NP[np] = v
                np = r[1] + p[1]
                if np in NP:
                    NP[np] += v
                else:
                    NP[np] = v
    return NP

if __name__ == '__main__':
    main()
