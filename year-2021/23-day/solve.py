import sys
import re
from math import prod
from functools import reduce

HALLS = [1,2,4,6,8,10,11]
# guess 1: 17252

def main(args):
    progSize = 20
    pre = lambda x: x
    if "-ex" in args:
        lobby = getLines("data.ex.txt", pred = pre)
    else:
        lobby = getLines("data.in.txt", pred = pre)
    lobby2 = getFolds(lobby)
    E1, H1 = getEnergy(lobby, {})
    print(f"part 1: {E1}", end = "\r")
    E2, H2 = getEnergy(lobby2, {})
    if "-v" in args:
        print("=" * 40)
        print(f"Total energy: {E1}, steps: {len(H1)}\n")
        printHist(H1, E1)
        print("=" * 40)
        print(f"Total energy: {E2}, steps: {len(H2)}\n")
        printHist(H2, E2)
        print("\nANSWERS")
    print(f"part 1: {E1}")
    print(f"part 2: {E2}")

def getEnergy(lobby, cache):
    if getKeys(lobby) in cache:
        return cache[getKeys(lobby)]#(a, b)
    if isSolved(lobby):
        return (0, [(lobby, 0)])
    energy = None
    hist = None
    for w in getWalkers(lobby):
        for m in getMoves(lobby, w):
            newL = acopy(lobby)
            cost = getman(w, m) * getCost(swap(newL, w, m))
            newE, newH = getEnergy(newL, cache)
            if newE is not None:
                newE += cost
                if energy is None:
                    hist = newH
                    energy = newE
                elif newE < energy:
                    energy = newE
                    hist = newH
    hist = (lobby, energy) if hist is None else [(lobby, energy), *hist]
    cache[getKeys(lobby)] = (energy, hist)
    return (energy, hist)

def getKeys(lobby):
    return tuple("".join(l) for l in lobby)

def printHist(h, emax):
    for m, e in h:
        print(f"energy: {emax - e}")
        printMap(m)

def printMap(l):
    for i in l:
        print(''.join(i))
    print()

def isSolved(lobby):
    solved = True
    for c in "ABCD":
        x = (ord(c) - 65) * 2 + 3
        for y in range(2, len(lobby) - 1):
            solved = solved and lobby[y][x] == c
            if not solved: return False
    return solved

def getWalkers(lobby):
    # returns any one that could walk but not necessarily should
    # that's job of getMoves to filter out
    halls = [(x,1) for x in HALLS if lobby[1][x] in "ABCD"]
    roomies = []
    xroom = (i*2+3 for i in [0,1,2,3])
    yroom = range(2, len(lobby) - 1)
    for x in xroom:
        for y in yroom:
            solved = True
            me = lobby[y][x]
            # xme = (ord(me) - 65) * 2 + 3
            # solved = solved and xme == x
            if me != ".": # and not solved:
                roomies.append((x,y))
                break
    return (_ for _ in [*halls, *roomies])

def getCost(t):
    return 10 ** (ord(t) - 65)

def getMoves(lobby, at):
    X, Y = at
    type = lobby[Y][X]
    if type not in "ABCD": raise TypeError(type + " is not a correct type.")
    typeRoom = (ord(type) - 65) * 2 + 3
    
    nb = [(0,-1),(-1,0),(1,0),(0,1)]
    queue = [(x+X,y+Y) for x,y in nb]
    valid = set()
    visited = set()
    # checks which places are reachable
    while len(queue) > 0:
        xh, yh = queue.pop(0)
        if (xh, yh) in visited: continue
        visited.add((xh, yh))
        if lobby[yh][xh] == ".":
            valid.add((xh,yh))
            queue.extend([(x+xh,y+yh) for x,y in nb])
    # checks if its target room is currently solved
    solved = True
    btm = len(lobby) - 1
    for y in reversed(range(2, btm)):
        here = lobby[y][typeRoom]
        solved = solved and (here == type or here == ".")
        if not solved: break
    moves = []
    # print(at, solved, typeRoom, type)
    if (Y == 1 and not solved) or (X == typeRoom and solved):
        # not solved and in hallway, or solved and in solution room
        return (p for p in [])
    elif solved:
        # solved and not in solution room
        dunk = None
        for y in range(2, len(lobby) - 1):
            if lobby[y][typeRoom] == ".":
                dunk = (typeRoom, y)
        if dunk is not None and dunk not in valid and Y != 1:
            # moves = [dunk]
            moves.extend([(x, 1) for x in HALLS])
        else:
            moves = [dunk]
        # print(moves)
    else:
        moves = [(x, 1) for x in HALLS]
    # print(valid)
    return (p for p in moves if p in valid)

# get manhattan distance
def getman(a, b):
    if a[1] == 1 or b[1] == 1:
        return sum([abs(x - y) for x,y in zip(a, b)])
    else:
        s1 = sum([abs(x - y) for x,y in zip(a, b)])
        s2 = sum([abs(x - y) for x,y in zip((b[0], 1), b)])
        s3 = sum([abs(x - y) for x,y in zip((a[0], 1), a)])
        return s1 + min(s2, s3) * 2

def acopy(l):
    c = []
    for i, v1 in enumerate(l):
        c.append([])
        for j, v2 in enumerate(v1):
            c[i].append(v2)
    return c

def swap(l, a, b):
    x1, y1 = a
    x2, y2 = b
    l[y1][x1], l[y2][x2] = l[y2][x2], l[y1][x1]
    return l[y2][x2]

def getFolds(lobby):
    lobby2 = acopy(lobby)
    arr = ["  #D#C#B#A#  ", "  #D#B#A#C#  "]
    a, b = [[c for c in s] for s in arr]
    lobby2.insert(3, b)
    lobby2.insert(3, a)
    return lobby2

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
