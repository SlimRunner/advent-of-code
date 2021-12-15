def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline().strip()
        while line:
            sepLoc = line.find("-")
            pairing = (line[:sepLoc], line[sepLoc+1:])
            output.append(pairing)
            line = f.readline().strip()
    return output

def findUnique(nodePairs):
    output = {}
    for nodes in nodePairs:
        a, b = nodes
        if a not in output: output[a] = len(output)
        if b not in output: output[b] = len(output)
    return output

def makeNodeArray(nodePairs):
    uniqueNodes = [
        n for n in findUnique(nodePairs)
        if n not in ["start", "end"]]
    uniqueNodes.insert(0, "start")
    uniqueNodes.append("end")
    uniqueNodes = {k:i for i, k in enumerate(uniqueNodes)}
    uniqueSize = len(uniqueNodes)
    output = [[0] * uniqueSize for _ in range(0, uniqueSize)]
    for nodes in nodePairs:
        a, b = [uniqueNodes[n] for n in nodes]
        output[a][b] += 1
        output[b][a] += 1
    bigCaves = [i for k, i in uniqueNodes.items() if k.isupper()]
    return (output, bigCaves)

def countPaths(nodes, exempt, visited, cave):
    # TIL: this is called backtracking
    if cave == len(nodes) - 1: return 1
    visited[cave] = True
    tour = [
        i for i, p in enumerate(caveMap[cave])
        if p != 0 and (not visited[i] or i in exempt)
    ]
    paths = 0
    for t in tour:
        paths += countPaths(nodes, exempt, visited, t)
    visited[cave] = False
    return paths

def countPathsTwin(nodes, exempt, visited, cave, twin):
    # TIL: this is called backtracking
    if cave == len(nodes) - 1: return 1
    visited[cave] = True
    tour = [
        i for i, p in enumerate(caveMap[cave])
        if p != 0 and (not visited[i] or i in exempt)
    ]
    paths = 0
    for t in tour:
        paths += countPathsTwin(nodes, exempt, visited, t, twin)
    visited[cave] = False
    return paths

if __name__ == "__main__":
    nodePairs = getLines("input.in.txt")
    nSize = len(nodePairs)
    caveMap, bigCaves = makeNodeArray(nodePairs)
    print(caveMap, '\n', bigCaves)
    
    paths1 = countPaths(caveMap, bigCaves, [False] * nSize, 0)
    paths2 = countPathsTwin(caveMap, bigCaves, [False] * nSize, 0, False)
    print(paths1)
    print(paths2)
