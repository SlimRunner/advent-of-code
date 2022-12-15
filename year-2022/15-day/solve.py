import sys
import re

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  # print your output
  coords = getCoords(lines)
  printEqns(coords) # paste in Desmos and count manually
  # parts = getPartitions(coords, 10)
  # locked = sumDist(parts)
  # print(parts)
  # print(locked)
  # print(f"part 1: {}")
  # print(f"part 2: {}")

def sumDist(parts):
  total = 0
  L = 0
  switch = False
  clear = False
  for p in parts:
    x, v = p
    if switch != v and v:
      if clear:
        total += x - L + 1
      else:
        L = x
      clear = not clear
    pass
  return total


# sensor -> (at, closest, manhattan)
def getPartitions(sensors, row):
  P = []
  for sensor, beacon, dist in sensors:
    xs, ys = sensor
    torow = abs(ys - row)
    if torow <= dist:
      a = xs - torow
      b = xs + torow
      P.append((a, True))
      P.append((b, False))
  return sorted(P, key=lambda x : x[0])

def fixRange(x, y):
  return (min(x, y), max(x, y))

def getCoords(lines):
  out = []
  rx = "x=(-?\d+).+?y=(-?\d+).+?x=(-?\d+).+?y=(-?\d+)"
  for line in lines:
    x1, y1, x2, y2 = [int(i) for i in re.findall(rx, line)[0]]
    md = getMand((x1, y1), (x2, y2))
    out.append([(x1, y1), (x2, y2), md])
  return out

def printEqns(coords):
  for s, b, d in coords:
    x, y = s
    print(f"\\left|x-{x}\\right|+\\left|y-{y}\\right|\\le{d}")

def getMand(a, b):
  x1, y1 = a
  x2, y2 = b
  return abs(x2 - x1) + abs(y2 - y1)
  pass

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
