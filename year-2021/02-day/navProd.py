import re

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            commLine = re.search("(\w+)\s+(\d+)", line).groups()
            output.append(commLine)
            line = f.readline()
    return output

def part1(commList):
    tally = {
        "forward": 0,
        "down": 0,
        "up": 0
    }
    for comm in commList:
        cType = comm[0]
        cVal = int(comm[1])
        tally[cType] += cVal
    return (tally["down"] - tally["up"]) * tally["forward"]

def part2(commList):
    tally = {
        "disp": 0,
        "aim": 0,
        "depth": 0
    }
    for comm in commList:
        cType = comm[0]
        cVal = int(comm[1])
        if cType == "forward":
            tally["disp"] += cVal
            tally["depth"] += cVal * tally["aim"]
        elif cType == "down":
            tally["aim"] += cVal
        elif cType == "up":
            tally["aim"] -= cVal
    return tally["disp"] * tally["depth"]

commLines = getLines("navReport.in.txt")

print(part1(commLines))
print(part2(commLines))
