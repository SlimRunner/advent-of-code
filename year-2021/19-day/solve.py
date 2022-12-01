import sys
import re
from itertools import combinations
from functools import reduce

def main(args):
    if "-ex" in args:
        R = getInput("data.ex.txt")
    else:
        R = getInput("data.in.txt")
    # print(R)
    D = {k: findDistances(v) for k, v in R.items()}
    print(D)
    # print(reduce(union, D.values()))

def findDistances(data):
    return [distSQ(*distDF(*ot)) for ot in combinations(data, 2)]

def union(a, b):
    return set(a).union(set(b))

def distDF(a, b):
    return tuple(x - y for (x, y) in zip(a, b))

def distSQ(*nums):
    res = 0
    for n in nums:
        res += n * n
    return res

def getInput(fn, **kw):
    output = {}
    idx = -1
    with open(fn) as f:
        line = f.readline()
        while line:
            line = line.strip()
            if line.find("scanner") != -1:
                idx += 1
                output[idx] = []
            elif line:
                # ordered triplet
                ot = re.search("(.+?),(.+?),(.+)", line).groups()
                ot = tuple(int(z) for z in ot)
                output[idx].append(ot)
            line = f.readline()
    return output

if __name__ == '__main__':
    main(sys.argv)
