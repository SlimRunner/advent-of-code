import sys
import re

def main(args):
    pre = lambda x: int(x, 10)
    if "-ex" in args:
        elves = getLines("data.ex.txt", pred = pre)
    else:
        elves = getLines("data.in.txt", pred = pre)
    print(f"part 1: {elves[-1]}")
    print(f"part 2: {sum(elves[-3:])}")

def getSums(l):
  pass

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    with open(fn) as f:
        line = f.readline()
        output.append(0)
        while line:
            trimLine = line[:-1]
            if trimLine:
              output[-1] += int(trimLine)
            else:
              output.append(0)
            line = f.readline()
    return sorted(output)

if __name__ == '__main__':
    main(sys.argv)
