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
  pairs = copy.copy(lines)
  print(f"part 1: {consumePairs(pairs)}")
  # print(f"part 2: {}")
  # print(dlistify(list(pairs[22][1:-1]), []))
  # 4585: too low

def consumePairs(pairs):
  i = 1
  s = 0
  while len(pairs):
    a, b = dlistify(list(pairs[0][1:-1]), []), dlistify(list(pairs[1][1:-1]), [])
    pairs = pairs[3:]
    if reducePairs(a, b):
      print(f"{i} correct")
      s += i
    else:
      print(f"{i} WRONG")
      pass
    i += 1
  return s

def reducePairs(a, b):
  # WIP
  # x, y = a.pop(0), b.pop(0)
  # df = compare(a, b)
  # while df == 0:
  #   x, y = a.pop(0), b.pop(0)
  # -------------
  while len(a):
    # print(a,b)
    x = a.pop(0)
    if len(b) > 0:
      y = b.pop(0)
    else:
      return False
    x, y = likify(x, y)
    if isinstance(x, int):
      if x > y:
        return False
    else:
      return reducePairs(x, y)
  return True

def likify(x, y):
  if type(x) != type(y):
    if isinstance(x, int):
      return ([x], y)
    else:
      return (x, [y])
  else:
    return (x, y)

def dlistify(s, l):
  buff = ""
  while len(s) > 0:
    c = s.pop(0)
    if c == "[":
      l.append(dlistify(s, []))
    elif c == "]":
      if len(buff) > 0:
        l.append(int(buff))
        buff = ""
      return l
    elif c == ",":
      if len(buff) > 0:
        l.append(int(buff))
        buff = ""
    elif c in "0123456789":
      buff += c
  if len(buff) > 0:
    l.append(int(buff))
  return l

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
