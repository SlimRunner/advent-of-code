import sys
import re
from functools import reduce
from collections import deque
import time

class Node:
  def __init__(self, data, parent):
    self.data = data
    self.prev = parent

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  if "-somearg" in args:
    pass # process or react to argument
  # print your output
  bps = getBlueprints(lines)
  # print("🤖")
  print(dijkstra([(0, 0, 0, 0), (1, 0, 0, 0)], bps[1], 32))

  # startTime = time.time()
  # yields24 = findMaxYields(bps, 24)
  # p1 = sum([(i + 1) * yld for i, yld in enumerate(yields24)])
  # print("Runtime: %s" % (time.time() - startTime))
  # print(f"part 1: {p1}")

  # startTime = time.time()
  # yields32 = findMaxYields(bps[:3], 32)
  # print("Runtime: %s" % (time.time() - startTime))
  # p2 = reduce(lambda x, y: x * y, yields32)
  # print(f"part 2: {p2}")
  # 13340 : too low for p2

def findMaxYields(blueprints, maxdepth):
  entry = [(0, 0, 0, 0), (1, 0, 0, 0)]
  out = []
  for i, bp in enumerate(blueprints):
    thisYield = dijkstra(entry, bp, maxdepth)
    print(f"ID: {i + 1} yields {thisYield} at best")
    out.append(thisYield)
  return out
  # return [dijkstra(entry, bp, maxdepth) for bp in (blueprints)]

def dijkstra(inventory, blueprint, maxdepth):
  bestNode = None
  depthmap = [None for _ in range(maxdepth + 1)]
  maxlen = 0
  optimal = None
  bestMomentum = None
  queue = deque([(*inventory, 0, 0, None)])
  while len(queue):
    harvest, robots, time, momentum, parent = queue.pop()
    nextNode = Node((harvest, robots, time), parent)
    # print(harvest)
    # print(robots)
    # print(time)
    # print()
    if depthmap[time] is None:
      depthmap[time] = momentum #harvest[-1]
    else:
      depthmap[time] = max(depthmap[time], momentum) #max(depthmap[time], harvest[-1])
    if time >= maxdepth:
      # print(depthmap, end = "\r")
      if optimal is None:
        optimal = harvest[-1]
        bestMomentum = momentum
        bestNode = nextNode
      else:
        if optimal < harvest[-1]: bestNode = nextNode
        bestMomentum = max(bestMomentum, momentum)
        optimal = max(optimal, harvest[-1])
    else:
      newHarvest = tuple(mat + yld for mat, yld in zip(harvest, robots))
      newMomentum = momentum + newHarvest[-1]
      allTrue = lambda x, y: x and y
      # shopFlag = reduce(lambda x, y: x | y, [((1 if not rob else 0) << i) for i, rob in enumerate(robots)])
      wishList = [rob == 0 for rob in robots]
      shopList = [win == 1 for win in windowShop(harvest, blueprint)]
      dontSave = reduce(allTrue, shopList)
      if dontSave:
        newQueue = deque()
      else:
        newQueue = deque([(newHarvest, robots, time + 1, newMomentum, nextNode)])
      for i, (wishShop, canShop) in enumerate(zip(wishList, shopList)):
        # canOutdoBest = (lambda x: x * (x + 1) // 2)(maxdepth - time) > (0 if optimal is None else optimal)
        # canOutdoBest = True if depthmap[time + 1] is None else newHarvest[-1] >= depthmap[time + 1]
        canOutdoBest = True if depthmap[time + 1] is None else newMomentum >= depthmap[time + 1]
        if canShop and canOutdoBest:
          quota = tuple(1 if i == j else 0 for j in range(len(blueprint)))
          price = getPrices(quota, blueprint)
          nextHarvest = tuple(a - b for a, b in zip(newHarvest, price))
          nextRobots = tuple(a + b for a, b in zip(robots, quota))
          newQueue.append((nextHarvest, nextRobots, time + 1, newMomentum, nextNode))
          # if wishShop:
          #   # priority
          #   newQueue.appendleft((nextHarvest, nextRobots, time + 1))
          # else:
          #   newQueue.append((nextHarvest, nextRobots, time + 1))
      queue.extend(newQueue)
      # maxlen = max(maxlen, len(queue))
    # print(f"time: {time} with {len(queue)} nodes", end='\r')
  # print(maxlen)
  # printTrace(bestNode)
  print(depthmap)
  return optimal

def printTrace(node):
  print("=" * 32)
  names = ["ore", "clay", "obsidian", "geode"]
  while node is not None:
    here = node.data
    harvest, robots, time = here
    print(f"at minute {time} collected {harvest} and has {robots} robots")
    # for i, (h, r) in enumerate(zip(harvest, robots)):
    #   print("")
    node = node.prev
  print("=" * 32)

# returns [] of how many robots could be bought per model
def windowShop(harvest, blueprint):
  key = harvest + tuple((c for mo in blueprint for c in mo))
  if key in windowShop.cache:
    return windowShop.cache[key]
  quota = (min([(mat // cost) for cost, mat in zip(model, harvest) if cost != 0]) for model in blueprint)
  windowShop.cache[key] = tuple(quota)
  return windowShop.cache[key]
windowShop.cache = {}

# returns [] of material price given an [] of quantity of robots to aquire per model
def getPrices(quota, blueprint):
  key = quota + tuple((c for mo in blueprint for c in mo))
  if key in getPrices.cache:
    return getPrices.cache[key]
  prices = (sum(prices) for prices in zip(*[[cost * qty for cost in model] for qty, model in zip(quota, blueprint)]))
  getPrices.cache[key] = tuple(prices)
  return getPrices.cache[key]
getPrices.cache = {}

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
      (ore, 0, 0, 0),
      (clay, 0, 0, 0),
      (obs1, obs2, 0, 0),
      (geo1, 0, geo2, 0),
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
