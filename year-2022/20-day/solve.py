import sys
import re

class Node:
  def __init__(self, data):
    self.item = data
    self.next = None
    self.prev = None

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  node, index, zeroth = makeIndex(lines)
  decriptNodes(index)
  p1 = sum([traverseNode(zeroth, i * 1000).item for i in [1,2,3]])
  print(f"part 1: {p1}")
  node, index, zeroth = makeIndex(lines, 811589153)
  for i in range(10):
    decriptNodes(index)
  p2 = sum([traverseNode(zeroth, i * 1000).item for i in [1,2,3]])
  print(f"part 2: {p2}")

def decriptNodes(index):
  size = len(index) - 1
  for node in index:
    move = getShortCycle(node.item, size)
    if move >= 0:
      nodesplice(node, traverseNode(node, move))
    else:
      nodesplice(node, traverseNode(node, move - 1))

def getShortCycle(steps, modulus):
  md = steps % modulus
  if md > (modulus // 2):
    return md - modulus
  else:
    return md

def traverseNode(node, nth):
  advance = nth >= 0
  for _ in range(abs(nth)):
    if advance:
      node = node.next
    else:
      node = node.prev
  return node

def nodesplice(a, b):
  # works only for forward splices
  A, B, C, P, Q = a.prev, a, a.next, b, b.next
  if Q != B and B != P:
    # print([i.item for i in [A, B, C, P, Q]])
    # TURN: A <---> B <---> C ... P <---> Q
    # INTO: A <---> C ... P <---> B <---> Q
    A.next = C
    C.prev = A
    P.next = B
    Q.prev = B
    B.prev = P
    B.next = Q

def makeIndex(lines, factor = 1):
  zeroth = None
  index = []
  lines = list(reversed(lines))
  newNode = Node(int(lines.pop()) * factor)
  if newNode.item == 0: zeroth = newNode
  index.append(newNode)
  while len(lines):
    newNode = Node(int(lines.pop()) * factor)
    if newNode.item == 0: zeroth = newNode
    index.append(newNode)
    index[-2].next = index[-1]
    index[-1].prev = index[-2]
  index[0].prev = index[-1]
  index[-1].next = index[0]
  return (index[0], index, zeroth)

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
