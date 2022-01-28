def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            output.append(int(line))
            line = f.readline()
    return output

def rollingSum(inList, kSize):
    return []

def countIncrease(nList):
    count = 0
    index = 1
    while index < len(nList):
        if nList[index - 1] < nList[index]:
            count += 1
        index += 1
    return count

def countKernelIncrease(nList, kSize):
    count = 0
    index = kSize
    s0 = sum(nList[0: kSize])
    s1 = sum(nList[1: kSize + 1])
    while index < len(nList):
        if s0 < s1:
            count += 1
        s0 += nList[index] - nList[index - kSize]
        index += 1
        if index < len(nList):
            s1 += nList[index] - nList[index - kSize]
    return count

rNums = getLines("data.in.txt")
print(countIncrease(rNums))
print(countKernelIncrease(rNums, 3))
