import sys
import re
import os
import time
from math import lcm

RIGHT = 1
DOWN = 2
LEFT = 4
UP = 8

BLIZ2INT = ">v<^"
INT2BLIZ = {">": RIGHT, "v": DOWN, "<": LEFT, "^": UP}
INT2XY = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  terr, bliz, start, goal = makeMap(lines)
  warps = makeWarps(terr)
  p1 = BFS(start, goal, terr, bliz, warps)
  print(f"part 1: {p1}")
  # print(f"part 2: {}")
  # p1: 555 ; too high
  # p1: 529 ; too high
  # p1: 462 ; too high
  # p1: 401 ; too high

def BFS(start, goal, terr, bliz, warps):
  visited = {}
  # os.system("cls")
  # printGrid(terr, bliz, start)
  # print(f"minute: {0}")
  # time.sleep(0.05)
  queue = nextMoves((start, 0, 0, bliz), terr, warps, start, goal)
  while len(queue):
    queue = trimSearch(queue, goal, 500, 1000)
    # print(len(queue))
    if len(queue) == 0: print(nth)
    here, nth, cost, nBliz = queue.pop(0)
    # os.system("cls")
    # printGrid(terr, nBliz, here)
    # print(f"minute: {nth}")
    # time.sleep(0.05)
    if here == goal:
      return nth
    queue.extend(nextMoves((here, nth, cost, nBliz), terr, warps, start, goal))
  return None

def trimSearch(queue, goal, lower, upper):
  if len(queue) >= upper:
    costs = []
    xg, yg = goal
    for node in queue:
      (x, y), _, hcost, _ = node
      costs.append(hcost)  
    Q = [q for _, q in sorted(zip(costs, queue))][0: lower]
    # print((len(queue), len(Q)))
    return Q
  return queue

def nextMoves(here, terr, warps, start, goal):
  (xh, yh), nth, cost, bliz = here
  bliz = moveBlizz(bliz, warps, nth)
  MOVES = [(xh + x, yh + y) for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
  newMoves = [
    ((x, y), nth + 1, cost + abs(goal[0] - x) + abs(goal[1] - y) + nth + 1, bliz)
    for x, y in MOVES
    if (y >= 0) and ((x, y) not in bliz) and
    terr[y][x] == 0 and (x, y) != start
  ]
  while not len(newMoves):
    nth += 1
    bliz = moveBlizz(bliz, warps, nth)
    newMoves = [
      ((x, y), nth + 1, cost + abs(goal[0] - x) + abs(goal[1] - y) + nth + 1, bliz)
      for x, y in MOVES
      if (y >= 0) and ((x, y) not in bliz) and
      terr[y][x] == 0 and (x, y) != start
    ]
  return newMoves

def makeWarps(terr):
  ymax = len(terr)
  xmax = len(terr[0])
  warps = {}
  for y in [0, ymax - 1]:
    for x in range(xmax):
      if terr[y][x]:
        warps[(x, y)] = (x, ymax - y - (0 if y else 2))
  for x in [0, xmax - 1]:
    for y in range(ymax):
      if terr[y][x]:
        warps[(x, y)] = (xmax - x - (0 if x else 2), y)
  return warps

def moveBlizz(bliz, warps, nth):
  if nth in moveBlizz.cache:
    return moveBlizz.cache[nth]
  nBliz = {}
  for key, btype in bliz.items():
    bAll = [i for i, p in enumerate([1, 2, 4, 8]) if btype & p]
    for bEach in bAll:
      nKey = move(key, INT2XY[bEach])
      if nKey in warps:
        nKey = warps[nKey]
      if nKey in nBliz:
        nBliz[nKey] |= 1 << bEach
      else:
        nBliz[nKey] = 1 << bEach
  moveBlizz.cache[nth] = nBliz
  return nBliz
moveBlizz.cache = {}

def move(a, b):
  return (a[0] + b[0], a[1] + b[1])

def makeMap(lines):
  start = None
  goal = None
  blizz = {}
  terrain = []
  ymax = len(lines) - 1
  for y, line in enumerate(lines):
    terrain.append([])
    for x, char in enumerate(line):
      if y == 0 and char == ".": start = (x, y)
      if y == ymax and char == ".": goal = (x, y)
      terrain[y].append(1 if char == "#" else 0)
      if char != "." and char != "#":
        blizz[(x, y)] = INT2BLIZ[char]
  return terrain, blizz, start, goal

def printGrid(grid, bliz, here = None):
  print()
  arrows = "→↓←↑"
  out = ""
  ymax = len(grid)
  xmax = len(grid[0])
  line = ["" for _ in range(xmax)]
  for y in range(ymax):
    for x in range(xmax):
      # dot or blizzard
      blz = [arrows[i] for i, p in enumerate([1, 2, 4, 8]) if (x, y) in bliz and bliz[(x, y)] & p]
      db = ("." if not len(blz) else (blz[0] if len(blz) == 1 else str(len(blz))))
      line[x] = "▄" if grid[y][x] else db
      if here == (x, y): line[x] = "▼"
    out += " ".join(line) + "\n"
  print(out[:-1])

def getLines(fn, **kw):
  pred = (lambda x: x) if "pred" not in kw else kw["pred"]
  output = []
  with open(fn) as f:
    line = f.readline()
    while line:
      output.append(pred(line))
      line = f.readline()
  return output

if __name__ == '__main__':
  main(sys.argv)
