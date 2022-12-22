import sys
import re
from pprint import pprint

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
    size = 4
    pairings = {
      0: (3, True),
      1: (4, True),
      2: (5, True),
      3: (0, True),
      4: (1, True),
      5: (2, True),
      6: (10, True),
      7: (11, True),
      8: (12, True),
      9: (13, True),
      10: (6, True),
      11: (7, True),
      12: (8, True),
      13: (9, True)
    }
    cubings = {
      0: (7, True),
      1: (13, True),
      2: (11, False),
      3: (5, False),
      4: (9, False),
      5: (3, False),
      6: (8, True),
      7: (0, True),
      8: (6, False),
      9: (4, False),
      10: (12, True),
      11: (2, False),
      12: (10, False),
      13: (1, True)
    }
  else:
    lines = getLines("data.in.txt", pred = pre)
    size = 50
    pairings = {
      0: (4, True),
      1: (5, True),
      2: (6, True),
      3: (7, True),
      4: (0, True),
      5: (1, True),
      6: (2, True),
      7: (3, True),
      8: (11, True),
      9: (12, True),
      10: (13, True),
      11: (8, True),
      12: (9, True),
      13: (10, True)
    }
    cubings= {
      0: (2, False),
      1: (8, True),
      2: (0, False),
      3: (9, True),
      4: (6, False),
      5: (13, True),
      6: (4, False),
      7: (12, True),
      8: (1, True),
      9: (3, True),
      10: (11, True),
      11: (10, True),
      12: (7, True),
      13: (5, True)
    }
  
  xints, yints, xwalls, codes, ranges = parseBoard(lines)
  edges, index, redir = getEdgeMap(xints, yints, size)
  (col, row), d = turtleMove(xints, yints, xwalls, codes, edges, index, pairings, redir)
  p1 = row * 1000 + col * 4 + d
  print(f"part 1: {p1}")
  
  (col, row), d = turtleMove(xints, yints, xwalls, codes, edges, index, cubings, redir)
  p2 = row * 1000 + col * 4 + d
  print(f"part 2: {p2}")

def turtleMove(xints, yints, xwalls, codes, edges, index, pairings, redir):
  here = (xints[0][0], 0)
  facing = 0
  for move in codes:
    isHorz = facing % 2 == 0
    if isinstance(move, int):
      for _ in range(move):
        if (15, 8) == here:
          pass
        newFacing = facing
        nextPoint = movePoint(here, getFacing(facing))
        x, y = nextPoint
        a, b = (0, 0) if not isHorz else xints[y]
        c, d = (0, 0) if isHorz else yints[x]
        if isHorz and not isBetween(x, (a, b)):
          nextPoint, newFacing = warpbound(here, facing, edges, index, pairings, redir, isHorz)
        elif not isHorz and not isBetween(y, (c, d)):
          nextPoint, newFacing = warpbound(here, facing, edges, index, pairings, redir, isHorz)
        x, y = nextPoint
        if x not in xwalls[y]:
          here = nextPoint
          facing = newFacing
    else:
      if move == "R":
        facing = (facing + 1) % 4
      else:
        facing = (facing - 1) % 4
  return movePoint(here, (1, 1)), facing

def warpbound(here, facing, edges, index, pairings, redir, isHorz):
  if here in index:
    axis = "x" if isHorz else "y"
    i, j = index[here][axis]
    i, direct = pairings[i]
    edge = edges[i] if direct else list(reversed(edges[i]))
    return edge[j], redir[i]
  else:
    return here, facing

def getEdgeMap(xints, yints, size):
  # indices are added from top to bottom and left to right
  # therefore edges are sorted [L,R,U,D]
  xoff = len(xints) // size
  yoff = len(yints) // size
  edges = [[] for _ in range(2 * (xoff + yoff))]
  redir = [0 for _ in range(2 * (xoff + yoff))]
  for y, (x1, x2) in enumerate(xints):
    i = y // size
    edges[i].append((x1, y))
    redir[i] = 0
    edges[i + xoff].append((x2, y))
    redir[i + xoff] = 2
  for x, (y1, y2) in enumerate(yints):
    i = x // size
    edges[i + 2 * xoff].append((x, y1))
    redir[i + 2 * xoff] = 1
    edges[i + 2 * xoff + yoff].append((x, y2))
    redir[i + 2 * xoff + yoff] = 3
  index = {}
  for i in range(len(edges)):
    axis = "y" if i >= 2 * xoff else "x"
    for j in range(len(edges[0])):
      x, y = edges[i][j]
      if (x, y) in index:
        index[(x, y)].update({axis: (i, j)})
      else:
        index[(x, y)] = {axis: (i, j)}
  return edges, index, redir

def isBetween(x, interval):
  a, b = interval
  return a <= x <= b

def movePoint(t, dt):
  x, y = t
  dx, dy = dt
  return (x + dx, y + dy)

def getFacing(n):
  return([1,0,-1,0][n], [0,1,0,-1][n])

def findYintervals(xints, xmin, xmax):
  yints = [[] for _ in range(xmin, xmax + 1)]
  for y, xint in enumerate(xints):
    a, b = xint
    for x in range(a, b + 1):
      yints[x].append(y)
  return [(min(e), max(e)) for e in yints]

def parseBoard(lines):
  ymin, ymax = 0, len(lines) - 3
  xmin, xmax = None, None
  xints = []
  xwalls = []
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
    if (rprev is not None) and rbound != rprev:
      off = 0 if rbound > rprev else -1
    xints.append((lbound, rbound))
    xwalls.append(walls)
    lprev, rprev = lbound, rbound
    line = lines.pop(0)
  yints = findYintervals(xints, xmin, xmax)
  ranges = ((xmin, xmax), (ymin, ymax))
  return xints, yints, xwalls, parseMoves(lines.pop()), ranges

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
