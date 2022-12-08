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
  # print(f"lines: {lines}") # test message
  coord = {}
  visiv = {}
  i, j = 0, 0
  for line in lines:
    i = 0
    for char in line:
      coord[(i, j)] = char
      visiv[(i, j)] = False
      i = i + 1
    j = j + 1
  
  w = i
  h = j
  vis = 2 * (w + h) - 4
  scr = 0

  for x in range(1, w - 1):
    for y in range(1, h - 1):
      vis += 1 if isVisible(coord, x, y, w, h) else 0
      scr = max(scr, getScenic(coord, x, y, w, h))

  print(f"part 1: {vis}")
  print(f"part 2: {scr}")

def isVisible(coord, x, y, w, h):
  here = coord[(x, y)]
  vtemp = True
  for X in range(x + 1, w):
    if X is not x:
      vtemp = vtemp and here > coord[(X, y)]
  vis = vtemp
  vtemp = True
  for X in range(0, x):
    if X is not x:
      vtemp = vtemp and here > coord[(X, y)]
  vis = vis or vtemp
  vtemp = True
  for Y in range(0, y):
    if Y is not y:
      vtemp = vtemp and here > coord[(x, Y)]
  vis = vis or vtemp
  vtemp = True
  for Y in range(y + 1, h):
    if Y is not y:
      vtemp = vtemp and here > coord[(x, Y)]
  vis = vis or vtemp
  return vis

def getScenic(coord, x, y, w, h):
  here = coord[(x, y)]
  vis = 0
  for X in range(x + 1, w):
    if X is not x:
      vis += 1
      if here <= coord[(X, y)]:
        break
  score = vis
  vis = 0
  for X in reversed(range(0, x)):
    if X is not x:
      vis += 1
      if here <= coord[(X, y)]:
        break
  score *= vis
  print(vis)
  vis = 0
  for Y in reversed(range(0, y)):
    if Y is not y:
      vis += 1
      if here <= coord[(x, Y)]:
        break
  score *= vis
  vis = 0
  for Y in range(y + 1, h):
    if Y is not y:
      vis += 1
      if here <= coord[(x, Y)]:
        break
  score *= vis
  return score

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
