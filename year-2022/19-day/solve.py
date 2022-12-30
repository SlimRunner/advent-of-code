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
  # print(dijkstra([(0, 0, 0, 0), (1, 0, 0, 0)], bps[0], 24))
  # print(dijkstra([(0, 0, 0, 0), (1, 0, 0, 0)], bps[1], 24))
  # print(getPrices((0,1,1,1), bps[0]))
  # print(windowShop(getPrices((0,1,1,1), bps[0]), bps[0]))

  startTime = time.time()
  yields24 = findMaxYields(bps, 24)
  p1 = sum([(i + 1) * yld for i, yld in enumerate(yields24)])
  print("Runtime: %s" % (time.time() - startTime))
  print(f"part 1: {p1}")

  # startTime = time.time()
  # yields32 = findMaxYields(bps[:3], 32)
  # print("Runtime: %s" % (time.time() - startTime))
  # p2 = reduce(lambda x, y: x * y, yields32)
  # print(f"part 2: {p2}")
  # 13340 : too low for p2
  # 15180 : too low for p2

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
  hW = [0,0,0,1 ] #tuple(1 / (p + 1) for p in getPrices((1,1,1,1), blueprint))
  rW = [0,0,0,1] #tuple(1 / p for p in windowShop(getPrices((1,1,1,1), blueprint), blueprint))
  # print(hW)
  # print(rW)
  def wsum(vals, weights):
    return vals[-1]
    if len(vals) != len(weights):
      raise ValueError("Arrays are not the same size")
    return sum((v * w for v, w in zip(vals, weights)))
  bestNode = None
  maxlen = 0
  optimal = None
  queue = deque([(*inventory, 0, None, None)])
  while len(queue):
    harvest, robots, time, legShopList, parent = queue.pop()
    nextNode = Node((harvest, robots, time), parent)
    # print(harvest)
    # print(robots)
    # print(time)
    # print()
    if time >= maxdepth:
      # print(depthmap, end = "\r")
      if optimal is None:
        optimal = harvest[-1]
        bestNode = nextNode
      else:
        if optimal < harvest[-1]: bestNode = nextNode
        optimal = max(optimal, harvest[-1])
    else:
      newHarvest = tuple(mat + yld for mat, yld in zip(harvest, robots))
      allTrue = lambda x, y: x and y
      # shopFlag = reduce(lambda x, y: x | y, [((1 if not rob else 0) << i) for i, rob in enumerate(robots)])
      wishList = [rob == 0 for rob in robots]
      shopQuota = windowShop(harvest, blueprint)
      shopList = [win == 1 for win in shopQuota]
      dontSave = reduce(allTrue, shopList)
      if legShopList is None:
        couldBuildEarlier = [False for _ in range(len(harvest))]
      else:
        couldBuildEarlier = [legShop > 0 for legShop in legShopList]
      if dontSave:
        newQueue = deque()
      else:
        newQueue = deque([(newHarvest, robots, time + 1, shopQuota, nextNode)])
      if shopList[-1]:
        shopList = [i == len(shopList) - 1 for i in range(len(shopList))]
      for i, (wishShop, canShop) in enumerate(zip(wishList, shopList)):
        # canOutdoBest = (lambda x: x * (x + 1) // 2)(maxdepth - time) > (0 if optimal is None else optimal)
        # canOutdoBest = True if depthmap[time + 1] is None else newHarvest[-1] >= depthmap[time + 1]
        if canShop and not couldBuildEarlier[i]:
          # 1 -> shopQuota[i]
          quota = tuple(1 if i == j else 0 for j in range(len(blueprint)))
          price = getPrices(quota, blueprint)
          nextHarvest = tuple(a - b for a, b in zip(newHarvest, price))
          nextRobots = tuple(a + b for a, b in zip(robots, quota))
          canOutdoBest = nextHarvest[-1] + (lambda x: x * (x + 1) // 2)(maxdepth - time) > (0 if optimal is None else optimal)
          if canOutdoBest:
            newShopQuota = [0, 0, 0, 0]
            # newQueue.append((nextHarvest, nextRobots, time + 1, newShopQuota, nextNode))
            if wishShop:
              # priority
              newQueue.append((nextHarvest, nextRobots, time + 1, newShopQuota, nextNode))
            else:
              newQueue.appendleft((nextHarvest, nextRobots, time + 1, newShopQuota, nextNode))
      queue.extend(newQueue)
      # maxlen = max(maxlen, len(queue))
    # print(f"time: {time} with {len(queue)} nodes", end='\r')
  # print(maxlen)
  # printTrace(bestNode, False)
  # print(bestHarv)
  return optimal

def printTrace(node, verbose = False):
  itab = " " * 4
  mats = ["ore", "clay", "obsidian", "geode"]
  winTrace = []
  print("=" * 32)
  names = ["ore", "clay", "obsidian", "geode"]
  while node is not None:
    # here = node.data
    winTrace.append(node.data)
    # harvest, robots, time = here
    # print(f"at minute {time} collected {harvest} with {robots} robots")
    # for i, (h, r) in enumerate(zip(harvest, robots)):
    #   print("")
    node = node.prev
  winTrace.reverse()
  prevStep = None
  for step in winTrace:
    journal = ""
    harvest, robots, time = step
    if prevStep is not None:
      prevHarvest, prevRobots, _ = prevStep
      delRobots = tuple(y - x for x, y in zip(prevRobots, robots))
      delHarvest = prevRobots
      delSpent = tuple(x + y - z for x, y, z in zip(prevHarvest, delHarvest, harvest))
      midHarvest = tuple(y - x for x, y in zip(delSpent, prevHarvest))
      if verbose:
        journal += f"at minute {time}"
        for i, (gain, total) in enumerate(zip(delRobots, robots)):  
          if gain > 0:
            unit = lambda v, n = names[i]: n + (" robots" if v > 1 else " robot")
            journal += f"\n{itab}{gain} {unit(gain)} was built giving a total of {total} {unit(total)}"
        for i, (gain, total) in enumerate(zip(delSpent, midHarvest)):
          if gain > 0:
            unit = names[i]
            journal += f"\n{itab}{gain} {unit} was spent building which reduced {unit} to {total}"
        for i, (gain, total) in enumerate(zip(delHarvest, harvest)):
          if gain > 0:
            unit = names[i]
            journal += f"\n{itab}{gain} {unit} was collected which increased {unit} to {total}"
        journal += f"\n{itab}result -> {harvest} minerals, {robots} robots"
      else:
        delHarvest = tuple(y - x for x, y in zip(prevHarvest, harvest))
        journal = f"{time}: (mineral,robot) -> {harvest} {robots}, deltas -> {delHarvest} {delRobots}"
    else:
      delHarvest = harvest
      delRobots = robots
      if verbose:
        journal += f"at the start -> {harvest}, {robots}"
        for i, gain in enumerate(robots):
          if gain > 0:
            unit = unit = names[i] + (" robots" if gain > 1 else " robot")
            journal += f"\n{itab}{gain} {unit} was available"
        for i, gain in enumerate(harvest):
          if gain > 0:
            unit = names[i]
            journal += f"\n{itab}{gain} {unit} was provided"
        journal += f"\n{itab}result -> {harvest} minerals, {robots} robots"
      else:
        journal = f"{time}: (mineral,robot) -> {harvest} {robots}"
    print(journal)    
    prevStep = step
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
