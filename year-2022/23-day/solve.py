import sys
import re
from enum import Enum
from functools import reduce

NORTH = 1
WEST = 2
SOUTH = 4
EAST = 8
DIR8 = [NORTH, NORTH | WEST, WEST, WEST | SOUTH, SOUTH, SOUTH | EAST, EAST, EAST | NORTH]

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  visualize = "-v" in args
  # ---------------------------

  elves = getElves(lines)
  if visualize: print2D(elves, 0)
  plans = doIt([
    (NORTH, (NORTH, NORTH | WEST, NORTH | EAST)),
    (SOUTH, (SOUTH, SOUTH | WEST, SOUTH | EAST)),
    (WEST, (WEST, WEST | NORTH, WEST | SOUTH)),
    (EAST, (EAST, EAST | NORTH, EAST | SOUTH))
  ])
  elves, _ = iterRules(elves, plans, 10)
  p1 = countBlanks(elves)
  print(f"part 1: {p1} blanks")
  if visualize:
    print2D(elves, 0)
  elves, iterRest = doRules(elves, plans)
  p2 = iterRest + 10
  print(f"part 2: {p2} rounds")
  if visualize:
    print2D(elves, 0)

def countBlanks(elves):
  total = 0
  xint, yint, (x1, x2), (y1, y2) = make2Dindex(elves)
  ysize = y2 - y1 + 1
  for x in range(x1, x2 + 1):
    if x in xint:
      total += ysize - xint[x]
    else:
      total += ysize
  return total

def doRules(elves, plans):
  count = 0
  elves, moved = moveElves(elves, plans)
  count = 1 if moved else 0
  while moved:
    elves, moved = moveElves(elves, plans)
    count += 1
  return (elves, count)

def iterRules(elves, plans, count):
  for i in range(count):
    elves, moved = moveElves(elves, plans)
    if not moved:
      return elves, i
  return (elves, count)

def moveElves(elves, plans):
  elvesTo, allowed = propMove(elves, plans)
  eMoved = set()
  anybodyMoved = False
  for elve in elves:
    if allowed[elvesTo[elve]]:
      anybodyMoved = True
      eMoved.add(elvesTo[elve])
    else:
      eMoved.add(elve)
  return (eMoved, anybodyMoved)

def propMove(elves, plans):
  # rules is a 4-length iterator
  andAll = lambda x, y: x and y
  orAny = lambda x, y: x or y
  d8 = [mapRule(r) for r in DIR8]
  elvesTo = {}
  allowed = {}
  for i in range(4):
    move, rules = next(plans)
    delta = mapRule(move)
    for elve in elves:
      if elve in elvesTo:
        continue
      around = (moveBy(elve, m) for m in d8)
      haveNeighbor = (n in elves for n in around)
      if not reduce(orAny, haveNeighbor):
        elvesTo[elve] = elve
        allowed[elve] = False
        continue
      slots = (moveBy(elve, mapRule(r)) for r in rules)
      enablers = (slot not in elves for slot in slots)
      fulfillRules = reduce(andAll, enablers)
      if fulfillRules:
        elveTo = moveBy(elve, delta)
        elvesTo[elve] = elveTo
        if elveTo in allowed:
          allowed[elveTo] = False
        else:
          allowed[elveTo] = True
      elif i == 3: # rules are not fulfilled in last attempt
        elvesTo[elve] = elve
        allowed[elve] = False
  next(plans)
  return elvesTo, allowed

def moveBy(here, delta):
  x1, y1 = here
  x2, y2 = delta
  return (x1 + x2, y1 + y2)

def mapRule(rule):
  x, y = 0, 0
  if rule & NORTH: y -= 1
  if rule & SOUTH: y += 1
  if rule & WEST: x -= 1
  if rule & EAST: x += 1
  return (x, y)

def getElves(lines):
  out = set()
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == "#":
        out.add((x, y))
  return out

def make2Dindex(locs):
  xind, yind = {}, {}
  x1, x2, y1, y2 = None, None, None, None
  for x, y in locs:
    if x1 is None: x1 = x
    if x2 is None: x2 = x
    if y1 is None: y1 = y
    if y2 is None: y2 = y
    x1 = min(x1, x)
    x2 = max(x2, x)
    y1 = min(y1, y)
    y2 = max(y2, y)
    if x in xind:
      xind[x] += 1
    else:
      xind[x] = 1
    if y in yind:
      yind[y] += 1
    else:
      yind[y] = 1
  return (xind, yind, (x1, x2), (y1, y2))

def doIt(lst):
  while True:
    for l in lst:
      yield l

def print2D(coords, padding = 0):
  # print(coords)
  _, _, (xmin, xmax), (ymin, ymax) = make2Dindex(coords)
  xmax += padding
  xmin -= padding
  ymax += padding
  ymin -= padding
  for y in range(ymin, ymax + 1):
    pout = ' '.join(["▄" if (x, y) in coords else "." for x in range(xmin, xmax + 1)])
    print(pout)
  print()

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
