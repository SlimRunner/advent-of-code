import sys
import re

def main(args):
  pre = lambda x: x.rstrip('\n')
  if "-ex" in args:
    lines = getLines("data.ex.txt", pred = pre)
  else:
    lines = getLines("data.in.txt", pred = pre)
  
  callouts = getRefs(lines)
  p1 = resolveRefs(callouts, callouts["root"])
  print(f"part 1: {p1}")
  
  exprTree = buildEqn(lines)
  expr, rhs =  parseExpr(exprTree, exprTree["root"])
  x = solveEqn(expr, rhs)
  print(f"part 2: {x}")

def resolveRefs(callouts, monke):
  if isinstance(monke, int):
    return monke
  else:
    lhs = resolveRefs(callouts, monke["lhs"])
    rhs = resolveRefs(callouts, monke["rhs"])
    return monke["func"](lhs, rhs)

def solveEqn(expr, rhs):
  op, const, isRight = expr["op"], expr["const"], expr["isRight"]
  if not isinstance(expr["expr"], str):
    rhs = invertOp(op, rhs, const, isRight)
    return solveEqn(expr["expr"], rhs)
  else:
    return invertOp(op, rhs, const, isRight)

def parseExpr(exprs, root):
  if isinstance(root, int):
    return root
  elif root["type"] == "expression":
    lhs, op, rhs = root["expr"]
    lhs = parseExpr(exprs, exprs[lhs])
    rhs = parseExpr(exprs, exprs[rhs])
    return getOperation(op, lhs, rhs)
  elif root["type"] == "variable":
    return root["varname"]
  else:
    raise TypeError("Expected an integer, expression, or variable.")

def buildEqn(lines):
  monkes = {}
  for line in lines:
    rxsplit = "(\w+): (.+)"
    rxops = "(\w+) +(.) +(\w+)"
    key, token = re.findall(rxsplit, line)[0]
    if key == "humn":
      expr = {
        "type": "variable",
        "varname": "x"
      }
    elif re.match("^\d+$", token):
      expr = int(token)
    else:
      tk1, op, tk2 = re.findall(rxops, token)[0]
      if key == "root": op = "="
      expr = {
        "type": "expression",
        "expr": (tk1, op, tk2)
      }
    monkes[key] = expr
  return monkes

def invertOp(op, x, y, isRight):
  if isRight:
    return {
      "+": x - y,
      "-": x + y,
      "*": x // y,
      "/": x * y
    }[op]
  else:
    return {
      "+": x - y,
      "-": -x + y,
      "*": x // y,
      "/": y // x
    }[op]

def getOperation(op, x, y):
  if isinstance(x, int) and isinstance(y, int):
    return {
      "+": x + y,
      "-": x - y,
      "*": x * y,
      "/": x // y
    }[op]
  elif op != "=":
    xint = isinstance(x, int)
    expr = y if xint else x
    num = x if xint else y
    return {
      "op": op,
      "expr": expr,
      "const": num,
      "isRight": not xint
    }
  else:
    xint = isinstance(x, int)
    expr = y if xint else x
    num = x if xint else y
    return (expr, num)

def getRefs(lines):
  monkes = {}
  for line in lines:
    rxsplit = "(\w+): (.+)"
    rxops = "(\w+) +(.) +(\w+)"
    key, token = re.findall(rxsplit, line)[0]
    if re.match("^\d+$", token):
      expr = int(token)
    else:
      tk1, op, tk2 = re.findall(rxops, token)[0]
      func = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x // y,
      }[op]
      expr = {
        "func": func,
        "lhs": tk1,
        "rhs": tk2
      }
    monkes[key] = expr
  for k in monkes.keys():
    if not isinstance(monkes[k], int):
      nlk, nrk = monkes[k]["lhs"], monkes[k]["rhs"]
      monkes[k]["lhs"] = monkes[nlk]
      monkes[k]["rhs"] = monkes[nrk]
  return monkes

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
