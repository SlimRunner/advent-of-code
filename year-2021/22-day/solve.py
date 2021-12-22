import sys
import re

def main(args):
    pre = lambda x: x
    if "-ex" in args:
        data = getLines("data.ex.txt", pred = pre)
    else:
        data = getLines("data.in.txt", pred = pre)
    # print(data)
    # use a function that generates a polyhedra and at the end compute the volume of that
    # for now use naive approach
    c = [[[False for _ in range(-50, 51)] for _ in range(-50, 51)] for _ in range(-50, 51)]
    print(len(c), len(c[0]), len(c[0][0]))
    count = 0
    for ins in data:
        do, (x1, x2), (y1, y2), (z1, z2) = ins
        if not (
            -50 <= x1 <= 50 and -50 <= x2 <= 50 and
            -50 <= y1 <= 50 and -50 <= y2 <= 50 and
            -50 <= z1 <= 50 and -50 <= z2 <= 50): continue
        x1, x2, y1, y2, z1, z2 = [min(max(i, -50), 50) + 50 for i in [x1, x2, y1, y2, z1, z2]]
        for z in range(z1, z2 + 1):
            for y in range(y1, y2 + 1):
                for x in range(x1, x2 + 1):
                    if c[z][y][x] != do:
                        if do:
                            count += 1
                        else:
                            count -= 1
                    c[z][y][x] = do
    print(count)

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            act = line.find("on") != -1
            region = re.findall("(?<=[x-z]=)(-?\d+)\.\.(-?\d+)", line)
            region = tuple((int(a), int(b)) for (a, b) in region)
            line = line.strip()
            output.append((act, *region))
            line = f.readline()
    return output

if __name__ == '__main__':
    main(sys.argv)
