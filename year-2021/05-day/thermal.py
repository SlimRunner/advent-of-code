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


coords, nMax, nMin = getLines("thermalLines.in.txt")
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

print(len([v for k,v in visitMap.items() if v > 1]))
