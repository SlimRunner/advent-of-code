import re
from itertools import product
from functools import reduce

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline().strip()
        while line:
            output.append([int(c) for c in line])
            line = f.readline().strip()
    return output

def findBasinSize(grid, seed):
    #predicate has two params
    total = 0
    neig = [(0,1),(0,-1),(1,0),(-1,0)]
    w, h = len(grid[0]), len(grid)
    visited = [[False] * w for _ in range(0, h)]
    stack = seed
    while len(stack) > 0:
        x0, y0 = stack.pop()
        if not visited[y0][x0]:
            visited[y0][x0] = True
            total += 1
            for x, y in neig:
                x += x0
                y += y0
                cases = (
                    0 <= x < w and
                    0 <= y < h and
                    grid[y][x] < 9 and
                    (grid[y0][x0] - grid[y][x]) <= 1 and
                    not visited[y][x]
                )
                if cases: stack.append((x, y))
    # printGrid(grid, visited, False)
    # printGrid(grid, visited, True)
    return total

def getValleys(grid):
    w, h = len(grid[0]), len(grid)
    valleys = []
    total = 0

    for y in range(0, h):
        S = y + 1 if y + 1 < h else None
        N = y - 1 if y > 0 else None
        for x in range(0, w):
            E = x + 1 if x + 1 < w else None
            W = x - 1 if x > 0 else None
            X = list(product([x], [N, S]))
            Y = list(product([W, E], [y]))
            neighbors = X + Y
            isValley = all([
                grid[y][x] < grid[xy[1]][xy[0]]
                for xy in neighbors
                if all([i is not None for i in xy])
            ])
            if isValley:
                valleys.append((x, y))
                total += grid[y][x] + 1
    return (total, valleys)

def printGrid(grid, marked, flip):
    print()
    for rows, show in zip(grid, marked):
        pout = ''.join([
            str(n) if s != flip else "*"
            for n, s in zip(rows, show)
        ])
        print(pout)

grid = getLines("input.in.txt")

vTotal, valleys = getValleys(grid)
print(vTotal)
basins = sorted([findBasinSize(grid, [vs]) for vs in valleys])[-3:]
print(reduce((lambda x, y: x * y), basins))
