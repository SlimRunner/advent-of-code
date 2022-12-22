import sys
import re
from pprint import pprint

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  scans, yints, codes = parseBoard(lines)
  (col, row), d = turtleMove(scans, yints, codes)
  p1 = row * 1000 + col * 4 + d
  print(f"part 1: {p1}")
  # print(f"part 2: {}")

def turtleMove(scans, yints, codes):
  here = (scans[0]["bounds"][0], 0)
  facing = 0
  for move in codes:
    isHorz = facing % 2 == 0
    if isinstance(move, int):
      for _ in range(move):
        nextPoint = movePoint(here, getFacing(facing))
        x, y = nextPoint
        a, b = (0, 0) if not isHorz else scans[y]["bounds"]
        c, d = (0, 0) if isHorz else yints[x]
        if isHorz and not isBetween(x, (a, b)):
          nextPoint = (a if x > b else b, y)
        elif not isHorz and not isBetween(y, (c, d)):
          nextPoint = (x, c if y > d else d)
        x, y = nextPoint
        if x not in scans[y]["walls"]:
          here = nextPoint
    else:
      if move == "R":
        facing = (facing + 1) % 4
      else:
        facing = (facing - 1) % 4
  return movePoint(here, (1, 1)), facing

def findYintervals(scans, xmin, xmax):
  yints = [[] for _ in range(xmin, xmax + 1)]
  for y, s in enumerate(scans):
    a, b = s["bounds"]
    for x in range(a, b + 1):
      yints[x].append(y)
  return [(min(e), max(e)) for e in yints]

def isBetween(x, interval):
  a, b = interval
  return a <= x <= b

def movePoint(t, dt):
  x, y = t
  dx, dy = dt
  return (x + dx, y + dy)

def getFacing(n):
  return([1,0,-1,0][n], [0,1,0,-1][n])

def parseBoard(lines):
  xmin, xmax = None, None
  scans = []
  roofs = [0]
  line = lines.pop(0)
  lprev, rprev = None, None
  while len(line):
    lbound = re.search("\S",line).span()[0]
    rbound = len(line) - 1
    xmin = lbound if xmin is None else min(xmin, lbound)
    xmax = rbound if xmax is None else max(xmax, rbound)
    walls = [m.start() for m in re.finditer("#", line)]
    if (lprev is not None) and lbound != lprev:
      off = 0 if lbound < lprev else -1
      roofs.append(len(scans) + off)
    if (rprev is not None) and rbound != rprev:
      off = 0 if rbound > rprev else -1
      roofs.append(len(scans) + off)
    scans.append({
      "bounds": (lbound, rbound),
      "walls": walls
    })
    lprev, rprev = lbound, rbound
    line = lines.pop(0)
  roofs.append(len(scans) - 1)
  yints = findYintervals(scans, xmin, xmax)
  return scans, yints, parseMoves(lines.pop())

def parseMoves(codes):
  return [(c if c in "RL" else int(c)) for c in re.findall("\d+|[RL]", codes)]

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
