import sys
import re
from time import sleep

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  pass
  pipes = getPipes(lines)
  addRefs(pipes)
  # print(pipes)
  # flow = Astar(pipes["AA"], 0, 0)
  # print your output
  # print(f"part 1: {}")
  # print(f"part 2: {}")

def Astar(room, rate, time):
  # gets stuck going back and forth between two nodes
  print(room['n'], time)
  # print(time)
  if time >= 30:
    return 0
  outflow = rate
  flow, tunnels = room["f"], room["t"]
  for path in tunnels:
    outflow = max(Astar(path, rate, time + 1), outflow)
  if flow > 0:
    for path in tunnels:
      outflow = max(Astar(path, flow + rate, time + 2), outflow)
  return outflow

def addRefs(pipes):
  for _, p in pipes.items():
    p["t"] = [pipes[i] for i in p["t"]]

def getPipes(report):
  out = {}
  for bullet in report:
    rx = "^Valve (\\w+) has flow rate=(\\d+); tunnels? leads? to valves? (.+)"
    v, f, t = re.findall(rx, bullet)[0] #valve, flow, tunnels
    out[v] = {"n": v, "f": int(f), "t": [x.strip() for x in t.split(",")]}
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
