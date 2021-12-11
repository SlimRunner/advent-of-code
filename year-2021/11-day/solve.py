import re

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline().strip()
        while line:
            output.append([int(c) for c in line])
            line = f.readline().strip()
    return output

def convSum(grid):
    carryStack = []
    needCarry = False
    NB = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
    h = len(grid)
    w = len(grid[0])
    for y in range(0, h):
        for x in range(0, w):
            val = grid[y][x]
            if val == 0:
                for neig in NB:
                    xn, yn = neig[0] + x, neig[1] + y
                    if 0 <= xn < w and 0 <= yn < h:
                        grid[yn][xn] += 1
                        if (grid[yn][xn] > 9):
                            carryStack.append((xn, yn))
                            grid[yn][xn] = 0
    return carryStack

def carrySum(grid, locs):
    carryStack = []
    if len(locs) == 0: return False
    NB = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]
    h = len(grid)
    w = len(grid[0])
    for loc in locs:
        x, y = loc
        for neig in NB:
            xn, yn = neig[0] + x, neig[1] + y
            if 0 <= xn < w and 0 <= yn < h:
                grid[yn][xn] += 1
                if (grid[yn][xn] > 9):
                    carryStack.append((xn, yn))
                    grid[yn][xn] = 0
    return carryStack

grid = getLines("input.in.txt")
print(grid)

total = 0
for _ in range(0, 100):
    grid = [[(n + 1) % 10 for n in row] for row in grid]
    cg = convSum(grid)
    if len(cg) > 0:
        cg = carrySum(grid, cg)
    while len(cg) > 0:
        cg = carrySum(grid, cg)
    total += sum([n.count(0) for n in grid])

print(grid)
print(total)
