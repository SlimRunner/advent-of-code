import sys
import re

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  walls = getWalls(lines)
  src = (500, 0)
  print(walls)
  particles = pourParticles(src, walls)
  print(particles)
  print(f"part 1: {len(particles)}")
  # print(f"part 2: {}")
  # 312 : too low

def pourParticles(src, walls):
  pout = []
  p = dropParticle(src, walls)
  while p is not None:
    pout.append(p)
    p = dropParticle(src, walls)
  return pout

def dropParticle(src, walls):
  xh, yh = src # here
  landing = {y for x, y in walls if x == xh}
  while len(landing) and yh + 1 < min(landing):
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
    landing = {y for x, y in walls if x == xh and y > yh}
  restp = (xh, yh)
  if len(landing):
    walls.add((xh, yh))
    return (xh, yh)
  else:
    return None
  

def getWalls(lines):
  out = set()
  for line in lines:
    coords = [(int(x), int(y)) for x, y in re.findall("(\d+),(\d+)", line)]
    xfro, yfro = coords.pop(0)
    for xto, yto in coords:
      if (xfro == xto):
        out.update({(xto, i) for i in irange(yfro, yto)})
      elif (yfro == yto):
        print
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
