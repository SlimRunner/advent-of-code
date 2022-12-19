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
  streamit = doIt(makeStreams(streams))
  rockit = doIt(makeRocks())
  hmap = [-1 for _ in range(7)]
  p1 = makeAvalanche(hmap, streamit, rockit, 2022)
  print(f"part 1: {p1}")

  streamit = doIt(makeStreams(streams))
  rockit = doIt(makeRocks())
  hmap = [-1 for _ in range(7)]
  p2 = makeAvalanche(hmap, streamit, rockit, 1000000000000)
  print(f"part 2: {p2}")

def makeAvalanche(hmap, streamit, rockit, nth):
  hoff = 0
  cache = {}
  tower = {(x, y) for x, y in enumerate(hmap)}
  for i in range(nth):
    si, stream = next(streamit)
    ri, rock = next(rockit)
    ckey = tuple(hmap) + (si, ri)
    if ckey in cache:
      keys = list(cache)
      vals = list(cache.values())
      vals = vals[keys.index(ckey):]
      lsize = len(vals)
      irest = nth - i
      hoff += sum(vals) * (irest // lsize) + sum(vals[0:irest % lsize])
      break
    hdiff = dropit(hmap, tower, rock, stream, streamit)
    tower = {(x, y - hdiff) for x, y in tower}
    hoff += hdiff
    cache[ckey] = hdiff
  return hoff

def dropit(hmap, tower, rock, stream, streamit):
  wa, wb = 0, len(hmap)
  nextRock = moveRock(rock, stream, 0)
  if isWithinWalls(nextRock, wa, wb) and (not hasOverlap(nextRock, tower)):
    rock = nextRock
  nextRock = moveRock(rock, 0, -1)
  while not hasOverlap(nextRock, tower):
    rock = nextRock
    _, stream = next(streamit)
    nextRock = moveRock(rock, stream, 0)
    if isWithinWalls(nextRock, wa, wb) and (not hasOverlap(nextRock, tower)):
      rock = nextRock
    nextRock = moveRock(rock, 0, -1)
  tower.update(rock)
  # adding one since n - (-1) = n + 1
  # basically I'm assuming hmap is guaranteed to be <= -1
  hnew = max(max([y for _, y in rock]) + 1, 0)
  for x, y in rock:
    hmap[x] = max(hmap[x], y)
  for i in range(len(hmap)):
    hmap[i] -= hnew
  return hnew

def doIt(L):
  while True:
    for i, l in enumerate(L):
      yield (i, l)

def makeStreams(streams):
  return [ord(s) - 61 for s in streams]

def makeRocks():
  rk = reversed([
    [1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0],
    [1,1,1,0,0,0,1,0,0,0,1,0,0,0,0,0],
    [0,1,0,0,1,1,1,0,0,1,0,0,0,0,0,0],
    [1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0]])
  return [{(2 + i % 4, i // 4 + 3) for i, f in enumerate(r) if f == 1} for r in rk]

def isWithinWalls(rock, a, b):
  return len([0 for x, _ in rock if x < a or x >= b]) == 0

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
