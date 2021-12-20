import sys

def main(args):
    pre = lambda x: [1 if c == "#" else 0 for c in x]
    if "-ex" in args:
        algo, image = getLines("data.ex.txt", pred = pre)
    else:
        algo, image = getLines("data.in.txt", pred = pre)
    C = 50 if "-p2" in args else 2
    if "-set" in args:
        v = args.index("-set") + 1
        C = int(args[v])
    enhance = recConvo(image, algo, C)
    if "-v" in args:
        printGrid(image)
        printGrid(enhance)
    print("\ncount:", countZeroes(enhance))

def countZeroes(grid):
    c = 0
    for row in grid:
        for col in row:
            if col == 1: c += 1
    return c

def recConvo(grid, algo, n):
    img = grid
    for _ in range(0, n):
        img = getConvo(img, algo)
    return img

def getConvo(grid, algo):
    w, h = len(grid[0]), len(grid)
    litEdge = getEdge(grid, w, h)
    outg = []
    for y in range(-3, h + 3):
        outg.append([])
        for x in range(-3, w + 3):
            kerb = getKerbit(grid, (x, y), litEdge)
            outg[y + 3].append(algo[kerb])
    return outg

def getEdge(grid, w, h):
    stage = 0
    x, y = 0, 0
    prev = grid[0][0]
    while stage < 4:
        if stage == 0:
            x += 1
            if x == w - 1: stage = 1
        elif stage == 1:
            y += 1
            if y == h - 1: stage = 2
        elif stage == 2:
            x -= 1
            if x == 0: stage = 3
        elif stage == 3:
            y -= 1
            if y == 0: stage = 4
        if prev != grid[y][x]: return False
    return grid[0][0] != 0

def getKernel(grid, at, edge):
    # kernel of a 9x9
    w, h = len(grid[0]), len(grid)
    X, Y = at
    kern = []
    for y in range(Y - 1, Y + 2):
        for x in range(X - 1, X + 2):
            if 0 <= x < w and 0 <= y < h:
                kern.append(grid[y][x])
            else:
                kern.append(edge)
    return kern

def getKerbit(grid, at, edge):
    # kernel of a 9x9
    w, h = len(grid[0]), len(grid)
    X, Y = at
    bits = 0
    for y in range(Y - 1, Y + 2):
        for x in range(X - 1, X + 2):
            offb = 8 - ((x - X + 1) + (y - Y + 1) * 3)
            if 0 <= x < w and 0 <= y < h:
                if grid[y][x] != 0: bits |= 1 << offb
            elif edge:
                bits |= 1 << offb
    return bits

def printGrid(grid):
    print()
    nmax = len(str(max(max(grid, key=max))))
    for rows in grid:
        pout = ' '.join([
            "▄" if n else "."
            for n in rows
        ])
        print(pout)

def print2DList(grid):
    print()
    nmax = len(str(max(max(grid, key=max))))
    for rows in grid:
        pout = ' '.join([
            " "*(nmax-len(str(n))) + (str(n) if n >= 0 else "*")
            for n in rows
        ])
        print(pout)

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    with open(fn) as f:
        line = f.readline().strip()
        algo = pred(line); f.readline()
        line = f.readline()
        while line:
            line = line.strip()
            output.append(pred(line))
            line = f.readline()
    return (algo, output)

if __name__ == '__main__':
    main(sys.argv)
