import sys
import re

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  printRes = "-v" in args
  # print your output
  src = (500, 0)
  walls = getWalls(lines)
  if printRes: print(walls)
  particles = pourParticles(src, walls)
  if printRes: print(f"\n{particles}")
  print(f"part 1: {len(particles)}")

  walls = getWalls(lines)
  addFloor(src, walls)
  if printRes: print(f"\n\n{walls}")
  particles = pourParticles(src, walls)
  if printRes: print(f"\n{particles}")
  print(f"part 2: {len(particles)}")

def pourParticles(src, walls):
  dropParticle.hmap = {}
  src = (src[0], src[1] - 1)
  pout = []
  p = dropParticle(src, walls)
  while p is not None:
    if len(pout) % 5000 == 0 and len(pout) > 0:
      print(f"\t{len(pout)} particles...")
    pout.append(p)
    p = dropParticle(src, walls)
  return pout

def dropParticle(src, walls):
  xh, yh = src # here
  if xh not in dropParticle.hmap:
    dropParticle.hmap[xh] = {y for x, y in walls if x == xh}
  landing = dropParticle.hmap[xh]
  # print(landing)
  while len(landing) and yh + 1 < min(landing):
    # print(landing)
    yh = min(landing) - 1
    slide = True
    while (xh, yh + 1) in walls and slide:
      if (xh - 1, yh + 1) in walls:
        if (xh + 1, yh + 1) in walls:
          slide = False
        else:
          xh, yh = (xh + 1, yh + 1)
      else:
        xh, yh = (xh - 1, yh + 1)
      pass
    if xh not in dropParticle.hmap:
      dropParticle.hmap[xh] = {y for x, y in walls if x == xh}
    landing = [y for y in dropParticle.hmap[xh] if y > yh]
  restp = (xh, yh)
  if len(landing) and restp != src:
    if xh not in dropParticle.hmap:
      dropParticle.hmap[xh] = {y for x, y in walls if x == xh}
    dropParticle.hmap[xh].add(yh)
    walls.add((xh, yh))
    return (xh, yh)
  else:
    return None
dropParticle.hmap = {}

def addFloor(src, walls):
  ymax = max([y for x, y in walls]) + 2
  walls.update({(i, ymax) for i in irange(src[0] - ymax, src[0] + ymax)})

def getWalls(lines):
  out = set()
  for line in lines:
    coords = [(int(x), int(y)) for x, y in re.findall("(\d+),(\d+)", line)]
    xfro, yfro = coords.pop(0)
    for xto, yto in coords:
      if (xfro == xto):
        out.update({(xto, i) for i in irange(yfro, yto)})
      elif (yfro == yto):
        out.update({(i, yto) for i in irange(xfro, xto)})
      xfro, yfro = xto, yto
  return out

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
