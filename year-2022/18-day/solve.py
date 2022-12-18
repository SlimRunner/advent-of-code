import sys
import re
from functools import reduce

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  # ------------------------
  cubes = {tuple(int(i) for i in re.findall("(\\d+),(\\d+),(\\d+)", line)[0]) for line in lines}
  cSurf = getSurface(cubes)
  aSurf = getSurface(getPockets(cubes))
  print(f"part 1: {cSurf}")
  print(f"part 2: {cSurf - aSurf}")

def getSurface(cubes):
  return len(cubes) * 6 - countTwins(cubes.copy()) * 2

def countTwins(cubes):
  counter = 0
  while len(cubes):
    cube = cubes.pop()
    xc, yc, zc = cube
    for x, y, z in [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]:
      xi, yi, zi = xc + x, yc + y, zc + z
      if (xi, yi, zi) in cubes:
        counter += 1
  return counter

def getPockets(cubes):
  cmin = reduce(lambda x, y: (min(x[0], y[0]), min(x[1], y[1]), min(x[2], y[2])), cubes)
  cmax = reduce(lambda x, y: (max(x[0], y[0]), max(x[1], y[1]), max(x[2], y[2])), cubes)
  x1, y1, z1 = tuple((i - 1 for i in cmin))
  x2, y2, z2 = tuple((i + 1 for i in cmax))
  volume = {(x, y, z) for x in irange(x1, x2) for y in irange(y1, y2) for z in irange(z1, z2)}
  floodFill(volume, cubes, (x1, y1, z1))
  return volume

def floodFill(volume, bounds, start):
  qmap = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]
  queue = [start]
  volume.remove(start)
  while len(queue):
    xh, yh, zh = queue.pop(0)
    for q in qmap:
      x, y, z = q
      x += xh
      y += yh
      z += zh
      if (x, y, z) not in bounds and (x, y, z) in volume:
        queue.append((x, y, z))
        volume.remove((x, y, z))
  for b in bounds:
    volume.remove(b)
  return volume
  

def irange(x, y):
  a = min(x, y)
  b = max(x, y)
  return range(a, b + 1)

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
