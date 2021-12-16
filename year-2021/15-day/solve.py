import operator

def main():
    M = getLines("input.in.txt")
    
    print(M)

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            line = line.strip()
            output.append([int(l) for l in line])
            line = f.readline()
    return output

def traverse(M):
    h, w = len(M), len(M[0])
    V = [[False for cl in range(0, w)] for rw in range(0, h)]
    paths = [[(0,0), V, 0]]
    while IDK:
        NP = []
        for i, [l, v, s] in enumerate(paths):
            x, y = l
            v[y][x] = True
            np, ns = seekSmall(M, l, v)
            NP.append([])
            
            
        paths = seekSmall(M, L, V)

def travBT(M, L, V):
    xl, yl = L
    if L == (len(M), len(M[0])):
        return M[yl][xl]
    S = 0
    paths = seekSmall(M, L, V)
    for p in paths:
        
    return S

# map, location, visited
def seekSmall(M, L, V):
    # cross paths
    xl, yl = L
    NB = [(0,1),(0,-1),(1,0),(-1,0)]
    LB = [(x + xl, y + yl) for (x, y) in NB]
    nm = [M[y][x] for (x, y) in LB if not V[y][x]]
    small, val = getSmall(nm)
    LB = [lb for i, lb in enumerate(LB) if i in small]
    return (LB, val)

def getSmall(L):
    idxs = []
    m = L[0]
    for i, l in enumerate(L):
        if m == l:
            idxs.append(i)
        elif l < m:
            m = l
            idxs.clear()
            idxs.append(i)
        else:
            pass
    return (idxs, m)

if __name__ == '__main__':
    main()
