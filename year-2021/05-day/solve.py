import re
import itertools

def getLines(fn):
    output = []
    isFirst = True
    nMax, nMin = 0, 0
    findCoords = "(\d+),(\d+)\s*\->\s*(\d+),(\d+)"
    with open(fn) as f:
        line = f.readline()
        while line:
            coords = [int(x) for x in re.search(findCoords, line).groups()]
            if isFirst:
                nMax = max(coords)
                nMin = min(coords)
            else:
                nMax = nMax if nMax > max(coords) else max(coords)
                nMin = nMin if nMin < min(coords) else min(coords)
            output.append(coords)
            line = f.readline()
            isFirst = False
    return (output, nMax, nMin)


def solution(**kwargs):
    doDiags = kwargs.get("doDiags", False)
    coords, nMax, nMin = getLines("data.in.txt")
    visitMap = {}

    for coord in coords:
        x1, y1, x2, y2 = coord
        if x1 == x2:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if (x1, y) in visitMap:
                    visitMap[(x1, y)] += 1
                else:
                    visitMap[(x1, y)] = 1
        elif y1 == y2:
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if (x, y1) in visitMap:
                    visitMap[(x, y1)] += 1
                else:
                    visitMap[(x, y1)] = 1
        elif doDiags and abs(x2 - x1) == abs(y2 - y1):
            xs = 1 if x2 > x1 else -1
            ys = 1 if y2 > y1 else -1
            xR1, xR2 = x1, x2 + xs
            yR1, yR2 = y1, y2 + ys
            for x, y in zip(range(xR1, xR2, xs), range(yR1, yR2, ys)):
                if (x, y) in visitMap:
                    visitMap[(x, y)] += 1
                else:
                    visitMap[(x, y)] = 1
    count = len([v for k,v in visitMap.items() if v > 1])
    return count

print("p1: ", solution())
print("p2: ", solution(doDiags = True))
