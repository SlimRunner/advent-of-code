def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline().strip()
        while line:
            output.append([int(c) for c in line])
            line = f.readline().strip()
    return output

def capmax(grid, limit):
    total = 0
    h = len(grid)
    w = len(grid[0])
    for y in range(0, h):
        for x in range(0, w):
            if grid[y][x] >= limit:
                grid[y][x] = 0
                total += 1
    return total

def increase(grid, limit):
    h = len(grid)
    w = len(grid[0])
    stack = []
    for _ in range(0, 1):
        for y in range(0, h):
            for x in range(0, w):
                grid[y][x] += 1
                if grid[y][x] == limit:
                    stack.append((x, y))
    while len(stack) > 0:
        loc = stack.pop()
        stack.extend(bumpNeighbors(grid, loc, limit))

def bumpNeighbors(grid, loc, limit):
    NB = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
    h, w = len(grid), len(grid[0])
    x, y = loc
    stack = []
    for neig in NB:
        xn, yn = neig[0] + x, neig[1] + y
        if 0 <= xn < w and 0 <= yn < h:
            grid[yn][xn] += 1
            if grid[yn][xn] == limit:
                stack.append((xn, yn))
    return stack

def printGrid(grid):
    print()
    for rows in grid:
        pout = ''.join([
            str(n) if n < 10 else chr(55 + n)
            for n in rows
        ])
        print(pout)

grid = getLines("input.in.txt")
gLen = len(grid) * len(grid[0])
zsum = 0
zstep = 0
t = 0
while zstep < gLen:
    if t == 100:
        printGrid(grid)
        print(zsum, "zeroes at t = 100")
    increase(grid, 10)
    zstep = capmax(grid, 10)
    zsum += zstep
    t += 1
printGrid(grid)
print("sync at t =", t)
