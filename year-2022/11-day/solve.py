import sys
import re
from functools import reduce

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-r" in args:
    runs = int(args[args.index("-r") + 1])
  else:
    runs = 20
  prod = lambda x, y: x * y
  itin = makeItinerary(lines)
  itin2 = makeItinerary(lines)
  tally = runTally(itin)
  p1 = reduce(prod, sorted(tally)[-2:])
  print(tally)
  print(f"part 1: {p1}")
  tally = runTally(itin2, 10000, True)
  p2 = reduce(prod, sorted(tally)[-2:])
  print(tally)
  print(f"part 2: {p2}")

def runTally(logs, runs = 20, worryFree = False):
  cdiv = reduce(lambda x, y: x * y, [m["modulo"] for m in logs])
  tally = [0 for _ in range(0, len(logs))]
  for _ in range(0, runs):
    for idx, monkey in enumerate(logs):
      if len(monkey["items"]) > 0:
        for __ in range(0, len(monkey["items"])):
          if worryFree:
            thisItem = monkey["worryup"](monkey["items"].pop(0)) % cdiv
          else:
            thisItem = (monkey["worryup"](monkey["items"].pop(0)) // 3) % cdiv
          logs[monkey["decide"](thisItem)]["items"].append(thisItem)
          tally[idx] += 1
  return tally

def makeItinerary(logs):
  items = []
  divtemp = {}
  monid = -1
  for idx, log in enumerate(logs):
    i = idx % 7
    if i == 0:
      monid = int(log[7:][:-1])
    elif i == 1:
      items.append({})
      items[monid]["items"] = [int(x) for x in log[18:].split(",")]
    elif i == 2:
      expr = re.findall("(old) (.) (\w+)", log[19:])[0]
      if expr[1] == "+":
        op = (lambda x, a=int(expr[2]) : x + a) if expr[2] != "old" else (lambda x : x + x)
      elif expr[1] == "*":
        op = (lambda x, a=int(expr[2]) : x * a) if expr[2] != "old" else (lambda x : x * x)
      else:
        op = None
      items[monid]["worryup"] = op
    elif i == 3:
      items[monid]["modulo"] = int(log[21:])
    elif i == 4:
      divtemp["true"] = int(log[29:])
    elif i == 5:
      items[monid]["decide"] = lambda x, a=divtemp["true"], b=int(log[30:]) , m=items[monid]["modulo"] : a if x % m == 0 else b
      divtemp = {}
    else:
      pass
  return items

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
