import sys
import re
from functools import cmp_to_key as sortleg
from functools import reduce
import operator
from pprint import pprint

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  pass
  pairs = getPairs(lines)
  ordering = [compare(a, b) for a, b in pairs]
  p1 = sum([(i + 1) for i, p in enumerate(ordering) if p > 0])
  print(f"part 1: {p1}")

  separators = [[[2]], [[6]]]
  nlists = getLists(lines) + separators
  nlists.sort(key = sortleg(compare), reverse=True)
  p2 = reduce(operator.mul, [i + 1 for i, n in enumerate(nlists) if n in separators])
  print(f"part 2: {p2}")

def getLists(lines):
  out = []
  for i in range(0, len(lines), 3):
    a, b = listify(lines[i]), listify(lines[i + 1])
    out.extend((a, b))
  return out

def getPairs(lines):
  out = []
  for i in range(0, len(lines), 3):
    a, b = listify(lines[i]), listify(lines[i + 1])
    out.append((a, b))
  return out

def compare(x, y):
  x, y = likify(x, y)
  if isinstance(x, int):
    return y - x
  else:
    xl, yl = len(x), len(y)
    sl = min(xl, yl)
    c = 0
    for i in range(sl):
      c = compare(x[i], y[i])
      if c != 0:
        break
    if c == 0:
      return yl - xl
    else:
      return c

def likify(x, y):
  if type(x) != type(y):
    if isinstance(x, int):
      return ([x], y)
    else:
      return (x, [y])
  else:
    return (x, y)

def listify(text):
  return relistify(list(text)[1:])

def relistify(chars):
  out = []
  buff = ""
  while len(chars) > 0:
    c = chars.pop(0)
    if c == "[":
      out.append(relistify(chars))
    elif c == "]":
      if len(buff) > 0:
        out.append(int(buff))
        buff = ""
      break
    elif c == ",":
      if len(buff) > 0:
        out.append(int(buff))
        buff = ""
    elif c in "0123456789":
      buff += c
  return out

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
