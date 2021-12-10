import re
from functools import reduce

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline().strip()
        while line:
            output.append(line)
            line = f.readline().strip()
    return output

code = getLines("input.in.txt")

parenDict = {
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<",
}
parenVal = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
parenPts = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}

corruptLines = []
badBrakets = []
acScores = [] # autocomplete scores
for ln, line in enumerate(code):
    corruptFlag = False
    stack = []
    seek = "([{<"
    for char in line:
        if char in seek:
            stack.append(char)
        elif parenDict[char] == stack[-1]:
            stack.pop()
        else:
            corruptLines.append(ln)
            badBrakets.append(char)
            corruptFlag = True
            break
    if not corruptFlag and len(stack) > 0:
        stack.reverse()
        newScore = reduce(
            lambda a,b: a * 5 + b,
            [parenPts[br] for br in stack]
        )
        acScores.append(newScore)

acScores = sorted(acScores)
code = [l for l in code if not l in corruptLines]

total = 0
for braket in badBrakets:
    total += parenVal[braket]

print(total)
print(acScores[len(acScores) // 2])
