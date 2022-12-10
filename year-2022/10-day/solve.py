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
  ops = getOps(lines)
  print(f"part 1: {getSum(ops)}")
  print(f"part 2: \n{getCode(ops)}")
  tried = [14660]

def getCode(args):
  tcode = ""
  x = 1
  for i, op in enumerate(args):
    if op is not None:
      x += op
    tcode += "█" if x - 1 <= i % 40 <= x + 1 else " "
    if (i + 1) % 40 == 0:
      tcode += "\n"
  return tcode

def getSum(args):
  x = 1
  st = 0
  for i, op in enumerate(args):
    if op is not None:
      x += op
    if (i + 21) % 40 == 0:
      st += (i + 1) * x
  return st

def getOps(args):
  out = []
  val = None
  for comm in args:
    if comm == "noop":
      out.append(val)
      val = None
    elif comm[0:4] == "addx":
      out.extend([val, None])
      val = int(comm[5:])
  return out

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
