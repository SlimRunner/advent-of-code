import sys

def main(args):
    pre = lambda x: [1 if c == "#" else 0 for c in x]
    if "-ex" in args:
        cmap, size = getLines("data.ex.txt", pred = pre)
    else:
        cmap, size = getLines("data.in.txt", pred = pre)
    print(advance(cmap, size))

def advance(cmap, size):
    w, h = size
    canmove = True
    step = 0
    Emap = [k for k,v in cmap.items() if v == ">"]
    Smap = [k for k,v in cmap.items() if v == "v"]
    Ebuf = []
    Sbuf = []
    Rbuf = []
    while canmove:
        canmove = False
        step += 1
        Rbuf = []
        for loc in Emap:
            towards = ((loc[0] + 1) % w, loc[1])
            if towards not in cmap:
                Ebuf.append(towards)
                Rbuf.append(loc)
        for loc in Rbuf:
            cmap.pop(loc)
        for loc in Ebuf:
            canmove = True
            cmap[loc] = ">"
        Rbuf = []
        for loc in Smap:
            towards = (loc[0], (loc[1] + 1) % h)
            if towards not in cmap:
                Sbuf.append(towards)
                Rbuf.append(loc)
        for loc in Rbuf:
            cmap.pop(loc)
        for loc in Sbuf:
            canmove = True
            cmap[loc] = "v"
        Smap = [k for k,v in cmap.items() if v == "v"]; Sbuf = []
        Emap = [k for k,v in cmap.items() if v == ">"]; Ebuf = []
    return step

def printMap(cmap, size):
    w, h = size
    for y in range(0, h):
        line = []
        for x in range(0, w):
            if (x,y) in cmap:
                line.append(cmap[(x,y)])
            else:
                line.append(".")
        print("".join(line))
    print()

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = {}
    with open(fn) as f:
        line = f.readline().strip()
        w = len(line)
        y = 0
        while line:
            for x, c in enumerate(line):
                if c != ".":
                    output[(x,y)] = c
            y += 1
            line = f.readline().strip()
    return output, (w, y)

if __name__ == '__main__':
    main(sys.argv)
