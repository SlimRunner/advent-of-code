import sys
import glob
import re

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    examples = glob.glob("*.ex.txt")
    einx = (int(args["ex"][0]) if len(args["ex"]) else 0) % len(examples)
    lines = getLines(examples[einx], pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  print(f"lines: {lines}") # test message
  # print(f"part 1: {}")
  # print(f"part 2: {}")

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
