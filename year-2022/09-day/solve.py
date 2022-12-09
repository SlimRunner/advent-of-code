import sys
import re

def main(args):
  pre = lambda x: x
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  trail = getTrail(lines, 1)
  print(f"part 1: {len(trail)}")
  trail = getTrail(lines, 9)
  print(f"part 2: {len(trail)}")

def pullTail(head, tail):
  sign = lambda x : (1 if x > 0 else (0 if x == 0 else -1))
  x, y = head
  w, z = tail
  dX = sign(x-w)
  dY = sign(y-z)
  dist = (x-w)*(x-w) + (y-z)*(y-z)
  if dist > 2:
    return (w + dX, z + dY)
  return (w, z)

def getTrail(todo, sz):
  tmap = {(0, 0): 1}
  x, y = (0, 0)
  rope = [{"x": 0 , "y": 0} for i in range(0, sz)]
  for comm in todo:
    d, l = (comm[0], int(comm[2:]))
    for i in range(0, l):
      # using math coordinates
      if d == "U":
        x += 1
      if d == "D":
        x -= 1
      if d == "L":
        y -= 1
      if d == "R":
        y += 1
      rope[0]["x"], rope[0]["y"] = pullTail((x, y), (rope[0]["x"], rope[0]["y"]))
      for j in range(0, sz - 1):
        rope[j+1]["x"], rope[j+1]["y"] = pullTail((rope[j]["x"], rope[j]["y"]), (rope[j+1]["x"], rope[j+1]["y"]))
      tmap[(rope[-1]["x"], rope[-1]["y"])] = 1
      # printRope(rope, (x, y), (10, 6), (0,0))
      # printRope(rope, (x, y), (26, 21), (5, 11))
      # print('')
  return tmap

def printRope(rope, head, dims, off):
  w, h = dims
  x, y = off
  coords = [["." for i in range(0, w)] for j in range(0, h)]
  idx = len(rope)
  for seg in reversed(rope):
    coords[seg["x"] + x][seg["y"] + y] = str(idx)
    idx -= 1
  coords[head[0] + x][head[1] + y] = 'H'
  for line in reversed(coords):
    print(''.join(line))

def getLines(fn, **kw):
  pred = (lambda x: x) if "pred" not in kw else kw["pred"]
  output = []
  with open(fn) as f:
    line = f.readline()[:-1]
    while line:
      output.append(pred(line))
      line = f.readline()[:-1]
  return output

if __name__ == '__main__':
  main(sys.argv)
