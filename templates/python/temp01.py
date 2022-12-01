import sys
import re

def main(args):
    pre = lambda x: x
    if "-ex" in args:
        lines = getLines("data.ex.txt", pred = pre)
    else:
        lines = getLines("data.in.txt", pred = pre)
    if "-somearg" in args:
        pass # process or react to argument
    # print your output
    # print(f"part 1: {}")
    # print(f"part 2: {}")

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    with open(fn) as f:
        line = f.readline()[:-1]
        l = len(line)
        while line:
            line = line + " " * (l - len(line))
            output.append([pred(c) for c in line])
            line = f.readline()[:-1]
    return output

if __name__ == '__main__':
    main(sys.argv)
