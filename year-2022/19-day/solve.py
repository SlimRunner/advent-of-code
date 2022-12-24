import sys
import re
from functools import reduce

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  bp = getBlueprints(lines)
  print(f"part 1: {simBPs(bp, 24)}")
  # print(f"part 2: {}")

def simBPs(blueprints, count):
  total = 0
  for id, specs in enumerate(blueprints):
    rob = [1,0,0,0]
    load = [0,0,0,0]
    for _ in range(count):
      print(load, rob)
      stepThruBP(specs, load, rob)
    total += (id + 1) * load[-1]
  return total

def stepThruBP(specs, loadout, robots):
  # if loadout meets blueprint build
  newunits = buildRobot(specs, loadout)
  # if have robots harvest
  harvestOre(robots, loadout)
  # update robots
  for i in range(0, len(robots)):
    robots[i] += newunits[i]

def buildRobot(specs, loadout):
  out = [0,0,0,0]
  for i, req in enumerate(specs):
    units = reduce(lambda x, y: max(x, y), [l // r for r, l in zip(req, loadout) if r != 0])
    if units > 0:
      out[i] += units
      for j in range(len(req)):
        if req[j] > 0:
          loadout[j] -= units * req[j]
  return out

def harvestOre(robots, loadout):
  for i in range(0, len(loadout)):
    loadout[i] += robots[i]

def getBlueprints(blueprints):
  rx = ("Blueprint \d+: " +
    "Each ore robot costs (\d+) ore\. " +
    "Each clay robot costs (\d+) ore\. " +
    "Each obsidian robot costs (\d+) ore and (\d+) clay\. " +
    "Each geode robot costs (\d+) ore and (\d+) obsidian\.")
  out = []
  for specs in blueprints:
    matches = re.findall(rx, specs)[0]
    ore, clay, obs1, obs2, geo1, geo2 = [int(i) for i in matches]
    out.append([
      [ore, 0, 0, 0],
      [clay, 0, 0, 0],
      [obs1, obs2, 0, 0],
      [geo1, 0, geo2, 0],
    ])
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
