import sys
import re
import copy

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  pass
  pairep = comPairs(getPairs(lines))
  p1 = sum([(i + 1) for i, p in enumerate(pairep) if p > 0])
  print(f"part 1: {p1}")
  # print(f"part 2: {}")
  # print(dlistify(list(pairs[22][1:-1]), []))
  # 4585: too low

def comPairs(pairs):
  return [compare(a, b) for a, b in pairs]

def getPairs(pairs):
  out = []
  for i in range(0, len(pairs), 3):
    a, b = listify(pairs[i]), listify(pairs[i + 1])
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
