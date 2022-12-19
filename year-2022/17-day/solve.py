import sys
import re
from functools import reduce
from itertools import cycle

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    streams = getLines("data.ex.txt", pred = pre)[0]
  else:
    streams = getLines("data.in.txt", pred = pre)[0]
  # ------
  streams = doIt([ord(s) - 61 for s in streams])
  tower = set()
  p1 = abs(makeAvalanche(streams, tower, 2022)) + 1
  # print()
  # print(tower)
  print(f"part 1: {p1}")
  # print(f"part 2: {}")

def doIt(L):
  while True:
    for i in L:
      yield i

def makeAvalanche(streams, tower, count):
  mxh = 1
  for _ in range(count):
    mxh = min(dropRock(streams, tower, mxh), mxh)
  return mxh

def makeRocks():
  rk = reversed([
    [1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [1,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]])
  return [{(2 + (i % 4), -(i // 4)) for i, f in enumerate(r) if f == 1} for r in rk]

def dropRock(streams, tower, maxh):
  rock = dropRock.rocks[dropRock.index]
  nextRock = adjustRock(rock, maxh - 4)
  while (not hasOverlap(nextRock, tower)) and isAboveFloor(nextRock):
    rock = nextRock
    nextRock = moveRock(rock, next(streams), 0)
    if isWithinWalls(nextRock) and (not hasOverlap(nextRock, tower)): rock = nextRock
    nextRock = moveRock(rock, 0, 1)
  dropRock.index = (dropRock.index + 1) % 5
  tower.update(rock)
  # min is the max height of tower because of screen coordinates
  return min([y for _, y in rock])
dropRock.index = 0
dropRock.rocks = makeRocks()

def isWithinWalls(rock):
  return len([0 for x, _ in rock if x < 0 or x >= 7]) == 0

def isAboveFloor(rock):
  return len([0 for _, y in rock if y > 0]) == 0

def adjustRock(rock, top):
  # maxR = [1, 2, 2, 4, 3][index]
  return {(x, y + top) for x, y in rock}

def moveRock(rock, xd, yd):
  return {(x + xd, y + yd) for x, y in rock}

def hasOverlap(a, b):
  for ia in a:
    if ia in b:
      return True
  return False

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
