import sys
import glob
import re
import math

SN2INT = {"=": -2, "-": -1, "0": 0, "1": 1,"2": 2}
INT2SN = {-2: "=", -1: "-", 0: "0", 1: "1", 2: "2"}

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "ex" in args:
    examples = glob.glob("*.ex.txt")
    einx = (int(args["ex"][0]) if len(args["ex"]) else 0) % len(examples)
    lines = getLines(examples[einx], pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  total = getSum(lines)
  p1 = getSnafu(total)
  print(f"part 1: {p1} ← {total}")
  # print(f"part 2: {}")

def getSnafu(num):
  out = ""
  while num > 0:
    if (num % -5) in INT2SN:
      sdig = num % -5
    else:
      sdig = num % 5
    num = (num - sdig) // 5
    out = INT2SN[sdig] + out
  return out

def getSum(lines):
  total = 0
  for line in lines:
    sz = len(line) - 1
    for i, char in enumerate(line):
      total += 5**(sz - i) * SN2INT[char]
  return total

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
  args = {}
  lkey = None
  for arg in sys.argv:
    if arg[0] == "-":
      lkey = arg[1:]
      args[lkey] = []
    elif len(args) and lkey is not None:
      args[lkey].append(arg)
  main(args)
