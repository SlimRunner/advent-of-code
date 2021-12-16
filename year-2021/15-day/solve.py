import operator

def main():
    G, M = getLines("input.in.txt")
    T = DFS(G, M)
    # printGrid(G)
    # printGrid(M)
    print("\n", T)

def DFS(G, M):
    queue = [(0,0)]
    M[0][0] = 0
    while len(queue) > 0:
        here = queue.pop(0)
        queue.extend(updateGrid(G, M, here))
    w, h = len(M[0]), len(M)
    return M[h-1][w-1]

def getLines(fn):
    output = []
    distmap = []
    with open(fn) as f:
        line = f.readline()
        while line:
            line = line.strip()
            output.append([int(l) for l in line])
            distmap.append([-1 for l in line])
            line = f.readline()
    return (output, distmap)

# map, location, visited
def updateGrid(G, M, L):
    w, h = len(G[0]), len(G)
    # cross paths
    ns = []
    xl, yl = L
    NB = [(0,1),(1,0),(0,-1),(-1,0)]
    LNB = [(x + xl, y + yl) for (x, y) in NB]
    LNB = [(x, y) for (x,y) in LNB if 0 <= x < w and 0 <= y < h]
    for (x, y) in LNB:
        here = G[y][x] + M[yl][xl]
        if M[y][x] == -1:
            M[y][x] = here
            ns.append((x, y))
        elif M[y][x] > here:
            M[y][x] = here
            ns.append((x, y))
    return ns

def printGrid(grid):
    print()
    nmax = len(str(max(max(grid, key=max))))
    for rows in grid:
        pout = ' '.join([
            " "*(nmax-len(str(n))) + (str(n) if n >= 0 else "*")
            for n in rows
        ])
        print(pout)

if __name__ == '__main__':
    main()
