import re

def getLines(fn):
    output = []
    with open(fn) as f:
        text = f.readlines()[0].strip()
        output = [int(x) for x in re.findall("\d+", text)]
    return sorted(output)

locs = getLines("input.in.txt")

def solve(list, pred):
    first = list[0]
    A = sum([pred(abs(x - first)) for x in locs])
    for i in range(1, len(locs)):
        B = sum([pred(abs(x - i)) for x in locs])
        if A < B: break
        A = B
    last = i - 1
    return sum([pred(abs(x - last)) for x in locs])

print(solve(locs, lambda n: n))
print(solve(locs, lambda n: n * (n + 1) // 2))
