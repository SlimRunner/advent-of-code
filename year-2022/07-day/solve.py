import sys
import re
from enum import Enum

class TokenType(Enum):
  C_DIR = 0
  C_LIST = 1
  L_FILE = 2
  L_FOLDER = 3

class Folder:
  def __init__(self, name, parent = None):
    self.name = name
    self.files = {}
    self.children = {}
    self.parent = parent
    self._sizeCache = None
  
  def getFolderSizes(self):
    if self._sizeCache is None:
      selfSize = sum(self.files.values())
    else:
      selfSize = self._sizeCache
    index = []
    for name, child in self.children.items():
      childSize, newSizes = child.getFolderSizes()
      selfSize += childSize
      # index.update(newSizes)
      index.extend(newSizes)
      pass
    # if self.name in index:
    #   raise Exception("file with duplicated name")
    # index[self.name] = selfSize
    index.append(selfSize)
    if self._sizeCache is None:
      self._sizeCache = selfSize
    return (selfSize, index)

  def getInfo(self, recursive = False, ltab = 0):
    tab4 = " " * 2
    padding = tab4 * ltab
    npad = tab4 * (ltab - 1)
    name = self.name
    files = "".join([f"\n{padding}{tab4}{k}: {v} bytes" for k, v in self.files.items()])
    parentInfo = self.parent.name if self.parent else " None"
    if recursive:
      children = "" if len(self.children) else " None"
      for child in self.children.values():
        children += f"\n{tab4}" + child.getInfo(True, ltab + 1)
    else:
      children = "".join([f"\n{padding}{tab4}{k}" for k in self.children.keys()]) if len(self.children) else " None"
    return f"{npad}name: {name}\n{padding}parent: {parentInfo}\n{padding}files:{files}\n{padding}children:{children}"

def main(args):
  pre = lambda x: x.strip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  
  tdump = classifyInput(lines)
  root = buildDirectory(tdump)
  sizes, sindex = root.getFolderSizes()
  p1 = sum([s for s in sindex if s <= 100000])
  print(f"part 1: {p1}")

  sindex.sort()
  needed = sizes - 40000000
  p2 = next(s for s in sindex if s >= needed)
  print(f"part 2: {p2}")
  # p1: 1127800 : too low
  # p2: 34257857 : too high


def buildDirectory(tdump):
  line = tdump.pop()
  if line["type"] != TokenType.C_DIR and line["argv"] != "/":
    return None
  root = Folder(line["argv"])
  path = root
  while len(tdump):
    line = tdump.pop()
    if line["type"] == TokenType.C_DIR:
      argv = line["argv"]
      if argv == "..":
        path = path.parent
      else:
        path = path.children[argv]
    elif line["type"] == TokenType.C_LIST:
      pass
    elif line["type"] == TokenType.L_FILE:
      name, size = line["name"], line["size"]
      path.files[name] = size
    elif line["type"] == TokenType.L_FOLDER:
      name = line["name"]
      path.children[name] = Folder(name, path)
    else:
      raise TypeError("Undefined TokenType")
  return root

def classifyInput(lines):
  out = []
  for line in lines:
    if line[0] == "$" and line[2:4] == "cd":
      out.append({
        "type": TokenType.C_DIR,
        "argv": line[5:]
      })
    elif line[0] == "$" and line[2:4] == "ls":
      out.append({
        "type": TokenType.C_LIST
      })
    else:
      arg1, arg2 = re.findall("[\w\.]+", line)
      if arg1 == "dir":
        out.append({
          "type": TokenType.L_FOLDER,
          "name": arg2
        })
      else:
        out.append({
          "type": TokenType.L_FILE,
          "name": arg2,
          "size": int(arg1)
        })
  return list(reversed(out))

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
