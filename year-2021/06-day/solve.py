import re

# Demonstrates visually that numbers can be grouped by modulo
# https://www.desmos.com/calculator/yzrkxpesfa
# Visualizes the modulo 3 group
# https://www.desmos.com/calculator/p3q44zsxn6
# Visualizes all modulo n groups up to 7
# https://www.desmos.com/calculator/8x5fseraet

def getLines(fn):
    output = []
    with open(fn) as f:
        text = f.readlines()[0].strip()
        output = [int(x) for x in re.findall("\d+", text)]
    return output

def countSpans(khp, cycles, kernel, spawnHP):
    kernelHP = khp[:]
    # kernel should be treated as the modulo not the upper limit
    mod = lambda n, k: (n + k) % kernel
    kth = kernel
    # hp of members by modulo groups (kernel group count/iter)
    kgCount = [0] * kth
    kgIter = [0] * kth
    # hp of members by spawn groups (spawn group count/iter)
    sth = range(1, spawnHP - kernel + 2)
    sgCount = [0] * kth # (kth * spawnHP // kernel)
    sgIter = [spawnHP] * kth # (kth * spawnHP // kernel)
    for k in kernelHP:
        kgCount[mod(k, 0)] += 1
        kgIter[mod(k, 0)] = k
    for iter in range(1, cycles + 1):
        kgIter = [k - 1 if kgCount[i] > 0 else k for i, k in enumerate(kgIter)]
        sgIter = [s - 1 if sgCount[i] > 0 else s for i, s in enumerate(sgIter)]
        for i, sg, kg in zip(range(0, kth + 1), sgIter, kgIter):
            oldkgCount = kgCount[i]
            oldsgCount = sgCount[i]
            if kg < 0:
                kgIter[i] %= kernel
                sgCount[mod(spawnHP, iter)] += oldkgCount
                # sgIter[...] should already be 8
            if sg < kernel:
                kgCount[i] += oldsgCount
                sgCount[i] = 0
                kgIter[i] = sgIter[i]
                sgIter[i] = spawnHP
    return sum(kgCount) + sum(sgCount)

def solution(states, days):
    return countSpans(states, days, 7, 8)

fishSeed = getLines("input.in.txt")
print(solution(fishSeed, 80))
print(solution(fishSeed, 256))
