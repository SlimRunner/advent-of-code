import sys
import re
import copy

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  s, e, grid, vrid, srid = makeMap(lines)
  #    2
  # 3  0  1
  #    4
  pass
  at = lambda h, g: g[h[1]][h[0]]
  steps, aces, rg = BFS(grid, vrid, srid, s, e)
  if "-vg" in args:
    printGrid(grid, 3)
  elif "-vv" in args:
    printGrid(vrid, 3)
  elif "-vs" in args:
    printGrid(srid, 3)
  else:
    print(steps, s)
    print(f"part 1: {steps}" + (" (goal)" if rg else " (failed)"))
    s, e, grid, vrid, srid = makeMap(lines)
    i = -1
    stalt = steps
    # print(aces[i], f": {at(aces[i], grid)}")
    for a in reversed(aces):
      steps, ace2, rg = BFS(copy.deepcopy(grid), copy.deepcopy(vrid), copy.deepcopy(srid), a, e)
      if rg and stalt > steps:
        stalt = steps
        print(stalt, a)
    print(f"part 2: {stalt}")

def BFS(grid, vrid, srid, start, goal):
  at = lambda h, g = grid: g[h[1]][h[0]]
  steps = None
  queue = [start]
  sueue = [0]
  reachedGoal = False
  aces = []

  while len(queue):
    # print(queue)
    # print(sueue)
    # print()
    step = sueue.pop(0)
    here = queue.pop(0)
    x, y = here
    vrid[y][x] = 2
    srid[y][x] = step
    if here != goal:
      nxt, ace = bfsMoves(grid, vrid, srid, here)
      aces.extend(ace)
      # ace.extend(bfsAces(grid, here))
      # print(nxt)
      if goal in nxt:
        queue = [goal]
        sueue = [step + 1]
      else:
        queue.extend(nxt)
        sueue.extend([step + 1] * len(nxt))
    else:
      reachedGoal = True
    # printGrid(srid)
  return (max(max(srid, key=max)), aces, reachedGoal)
  # 333: too low

def bfsMoves(grid, vrid, srid, here):
  H, W = len(grid), len(grid[0])
  X, Y = here
  at = lambda h, g: g[h[1]][h[0]]
  moves = [(x + X, y + Y) for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]]
  mout = []
  aout = []
  h = at(here, grid)
  for m in moves:
    if (0<=m[0]<W and 0<=m[1]<H) and (at(m, grid) == 0 and abs(at(m, grid) - h) <= 1 and at(m, vrid) < 1):
      aout.append(m)
    if (0<=m[0]<W and 0<=m[1]<H) and (at(m, grid) - h <= 1 and at(m, vrid) < 1): #at(m, srid) <= at(here, vrid)
      x, y = m
      vrid[y][x] = 1
      mout.append(m)
  return (mout, aout)

def makeMap(args):
  output = []
  vout = []
  sout = []
  start = ()
  end = ()
  {(i, j): () for j, row in enumerate(args) for i, char in enumerate(row)}
  for j, row in enumerate(args):
    output.append([])
    vout.append([])
    sout.append([])
    for i, char in enumerate(row):
      vout[j].append(0)
      sout[j].append(0)
      h = ord(char) - 97
      if char == "S":
        start = (i, j)
        output[j].append(0)
      elif char == "E":
        end = (i, j)
        output[j].append(25)
      else:
        output[j].append(h)
  return (start, end, output, vout, sout)

def printGrid(grid, pmax = -1):
  print()
  nmax = max(pmax, len(str(max(max(grid, key=max)))))
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
    line = f.readline()
    while line:
      output.append(pred(line))
      line = f.readline()
  return output

if __name__ == '__main__':
  main(sys.argv)
