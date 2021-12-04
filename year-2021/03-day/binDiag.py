from math import prod

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            output.append(line.rstrip())
            line = f.readline()
    return output

# oxygen generator rating
def getOGR(nList):
    length = len(nList[0])
    filterList = nList[0:]
    offset = 0
    while offset < length and len(filterList) > 1:
        lZeroes = []
        lOnes = []
        tally = 0
        for num in filterList:
            if num[offset] == "1":
                lOnes.append(num)
                tally += 1
                pass
            elif num[offset] == "0":
                lZeroes.append(num)
                tally -= 1
                pass
        if tally >= 0:
            filterList = lOnes
        else:
            filterList = lZeroes
        offset += 1
    binRes = filterList.pop() if len(filterList) > 0 else None
    return binToDec(binRes)

# CO2 scrubber rating
def getCSR(nList):
    length = len(nList[0])
    filterList = nList[0:]
    offset = 0
    while offset < length and len(filterList) > 1:
        lZeroes = []
        lOnes = []
        tally = 0
        for num in filterList:
            if num[offset] == "1":
                lOnes.append(num)
                tally += 1
                pass
            elif num[offset] == "0":
                lZeroes.append(num)
                tally -= 1
                pass
        if tally >= 0:
            filterList = lZeroes
        else:
            filterList = lOnes
        offset += 1
    binRes = filterList.pop() if len(filterList) > 0 else None
    return binToDec(binRes)

def binToDec(bNum):
    output = 0
    for offset, bit in enumerate(bNum[::-1]):
        if bit == "1": output |= 1 << offset
    return output

def getBinFreq(nList):
    length = len(nList[0])
    tally = [0] * length
    output = 0
    for binum in nList:
        for idx, bit in enumerate(binum):
            tally[idx] += 1 if bit == "1" else -1
    tally.reverse()
    for idx, freq in enumerate(tally):
        if freq >= 0:
            output |= 1 << idx
    return (output, output ^ ((1 << length) - 1))

binRep = getLines("binRep.in.txt")
gamma, epsilon = getBinFreq(binRep)
print((gamma, epsilon))
print(prod((gamma, epsilon)))

oxyRate = getOGR(binRep)
co2Rate = getCSR(binRep)
print((oxyRate, co2Rate))
print(prod((oxyRate, co2Rate)))
