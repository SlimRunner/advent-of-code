def main():
    points, rules = getLines("input.in.txt")
    f1 = foldit(points, rules[0:1])
    fn = foldit(points, rules)
    
    print("fold 1: ", len(f1), "points\n")
    printCode(list(fn))

def getLines(fn):
    pts = []
    rules = []
    with open(fn) as f:
        line = f.readline()
        while line:
            line = line.strip()
            if line.find("fold") >= 0:
                rule = line.replace("fold along ", "")
                sepLoc = rule.find("=")
                value = int(rule[sepLoc+1:])
                rules.append((0 if "x" in rule else 1, value))
            elif len(line) > 0:
                sepLoc = line.find(",")
                pair = [int(line[:sepLoc]), int(line[sepLoc+1:])]
                pts.append(pair)
            line = f.readline()
    return pts, rules

def getDesmosPoints(pts):
    output = "\\left["
    for p in pts:
        output += "\\left(" + str(p[0]) + "," + str(p[1]) + "\\right),"
    output = output[:-1] + "\\right]"
    return output

def printCode(points):
    lPoints = {}
    for p in points:
        if p[1] not in lPoints:
            lPoints[p[1]] = [p[0]]
        else:
            lPoints[p[1]].append(p[0])
    xmax = max(points, key = lambda x: x[0])[0]
    ymax = max(points, key = lambda x: x[1])[1]
    for y in range(0, ymax + 1):
        line = [" "] * (xmax + 1)
        if y in lPoints:
            for dot in lPoints[y]:
                line[dot] = "*"
        print("".join(line))

def foldit(points, rules):
    folded = set()
    for point in points:
        for rule in rules:
            xy, value = rule
            if point[xy] > value:
                # this function was derived from a matrix transformation
                # T * R * T' * v
                # T translates with the magnitude of rule value
                # R mirrors about an axis (x or y where needed)
                # T' undoes T
                # v is the final vector
                point[xy] = -point[xy] + 2 * value
        orderedPair = tuple(point)
        if orderedPair not in folded:
            folded.add(orderedPair)
    return folded

if __name__ == '__main__':
    main()
