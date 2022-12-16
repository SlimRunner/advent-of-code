import sys
import re

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
    yat = 11
    lim = (0, 20)
  else:
    lines = getLines("data.in.txt", pred = pre)
    yat = 2000000
    lim = (0, 4000000)
  # print your output
  coords = getCoords(lines)
  # printEqns(coords) # paste in Desmos and count manually
  parts = reducePartitions(getPartitions(coords, yat))
  occ = rowSlots(coords, yat)
  print(f"part 1: {sumDist(parts) - occ}")
  print(f"part 2: {findSpot(coords, lim)}")

def findSpot(coords, rnge):
  y, parts = findSlot(coords, rnge)
  if parts is None or len(parts) > 2:
    return None
  x = (parts[0][1] + parts[1][0]) // 2
  return x * 4000000 + y

def findSlot(coords, rnge):
  fro, to = rnge
  for y in range(fro, to + 1):
    p = trimPartitions(reducePartitions(getPartitions(coords, y)), fro, to)
    if len(p) > 1:
      return (y, p)
  return None

def rowSlots(coords, row):
  a = len({s[0] for s, b, _ in coords if row == s[1]})
  b = len({b[0] for s, b, _ in coords if row == b[1]})
  return a + b

def sumDist(parts):
  total = 0
  for a, b in parts:
    total += b - a + 1
  return total

def reducePartitions(parts):
  if parts[0][1] == False:
    return None
  c = 0
  isL = True
  lp = 0
  out = []
  for p, f in parts:
    c += 1 if f else -1
    if c == 1 and isL:
      lp = p
      isL = False
    if c == 0 and not isL:
      out.append((lp, p))
      isL = True
  if len(out) > 1:
    for i in reversed(range(1, len(out))):
      if out[i][0] - out[i - 1][1] <= 1:
        a = out[i - 1][0]
        _, b = out.pop(i)
        out[-1] = (a, b)
  return out

def trimPartitions(parts, fro, to):
  out = []
  for a, b in parts:
    if fro <= a <= to and fro <= b <= to:
      out.append((a, b))
    elif b > fro or a < to:
      out.append((max(a, fro), min(b, to)))
  return out

# sensor -> (at, closest, manhattan)
def getPartitions(sensors, row):
  P = []
  for sensor, beacon, dist in sensors:
    xs, ys = sensor
    torow = abs(ys - row)
    if torow <= dist:
      rdel = dist - torow
      a = xs - rdel
      b = xs + rdel
      P.append((a, True))
      P.append((b, False))
  return sorted(P, key=lambda x : x[0])

def fixRange(x, y):
  return (min(x, y), max(x, y))

def irange(x, y):
  a = min(x, y)
  b = max(x, y)
  return range(a, b + 1)

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
