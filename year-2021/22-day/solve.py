import sys
import re
from math import prod
from functools import reduce

def main(args):
    progSize = 20
    pre = lambda x: x
    if "-ex" in args:
        data = getLines("data.ex.txt", pred = pre)
    else:
        data = getLines("data.in.txt", pred = pre)
    area = 0
    boxes = []
    for i, (act, x, y, z) in enumerate(data):
        prog = int((i / len(data)) * progSize)
        print("*" * prog + "." * (progSize - prog), end="\r")
        if "-p1" in args and not (
            -50 <= x[0] <= 50 and -50 <= x[1] <= 50 and
            -50 <= y[0] <= 50 and -50 <= y[1] <= 50 and
            -50 <= z[0] <= 50 and -50 <= z[1] <= 50): continue
        # overlap found
        ovf = False
        ovBoxes = []
        for op, *box in boxes:
            if overArea([x, y, z], box) > 0:
                ovf = True
                ovBox = overBox([x, y, z], box)
                if act == op:
                    ovBoxes.append((not act, *ovBox))
                else:
                    ovBoxes.append((act, *ovBox))
        if ovf:
            boxes.extend(ovBoxes)
        if act:
            boxes.append((act, x, y, z))
    for act, x, y, z in boxes:
        area += getArea(x, y, z) * (1 if act else -1)
    print(" " * progSize)
    print("final area:", area)

def overBox(b1, b2):
    b3 = []
    for comp in zip(b1, b2):
        p1, p2 = zip(*comp)
        b3.append((max(p1), min(p2)))
    return b3

def overArea(b1, b2):
    res = 1
    for comp in zip(b1, b2):
        p1, p2 = zip(*comp)
        res *= max(min(p2) - max(p1), 0)
    return res

# https://www.desmos.com/calculator/65xkacmplj
def getArea(*coords):
    p = 1
    for coord in coords:
        p *= abs(coord[0] - coord[1])
    return p

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            act = line.find("on") != -1
            region = re.findall("(?<=[x-z]=)(-?\d+)\.\.(-?\d+)", line)
            region = [(int(a), int(b) + 1) for (a, b) in region]
            line = line.strip()
            output.append((act, *region))
            line = f.readline()
    return output

if __name__ == '__main__':
    main(sys.argv)
