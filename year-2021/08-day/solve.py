from collections import Counter
import re

def getLines(fn):
    output = []
    with open(fn) as f:
        line = f.readline()
        while line:
            commLine = [x.strip() for x in re.search("(.+)\|(.+)", line).groups()]
            inSig = re.findall("\w+", commLine[0])
            outSig = re.findall("\w+", commLine[1])
            output.append((inSig, outSig))
            line = f.readline()
    return output

def solve1(signals):
    total = 0
    for signal in signals:
        total += len([x for x in signal[1] if len(x) in (2, 4, 3, 7)])
    return total

def solve2(signals):
    sort = lambda s: ''.join(sorted(s))
    lDict = {2: 1, 4: 4, 3: 7, 7: 8}
    uLen = [k for k, v in lDict.items()]
    total = 0
    for signal in signals:
        found = {lDict[len(x)]: sort(x) for x in signal[0] if len(x) in uLen}
        unk5 = [x for x in signal[0] if len(x) == 5]
        unk6 = [x for x in signal[0] if len(x) == 6]
        idx = 0
        while len(unk6) > 0:
            idx = idx % len(unk6)
            if len(unk6) == 3:
                if all([c in unk6[idx] for c in found[4]]):
                    found[9] = sort(unk6.pop(idx))
            elif len(unk6) == 2:
                if all([c in unk6[idx] for c in found[1]]):
                    found[0] = sort(unk6.pop(idx))
                    found[6] = sort(unk6.pop())
            else:
                raise AttributeError("There should only be 3 6-length signals")
            idx += 1
        while len(unk5) > 0:
            idx = idx % len(unk5)
            if len(unk5) == 3:
                if all([c in unk5[idx] for c in found[1]]):
                    found[3] = sort(unk5.pop(idx))
            elif len(unk5) == 2:
                unionLen = len(Counter(unk5[idx]) + Counter(found[6]))
                if unionLen == 7:
                    found[2] = sort(unk5.pop(idx))
                    found[5] = sort(unk5.pop())
                else:
                    found[5] = sort(unk5.pop(idx))
                    found[2] = sort(unk5.pop())
            else:
                raise AttributeError("There should only be 3 5-length signals")
            idx += 1
        found = {v:k for k,v in found.items()}
        total += sum([
            found[sort(s)] * 10**(3-i)
            for i, s in enumerate(signal[1])
        ])
    return total

signals = getLines("input.in.txt")
print(solve1(signals))
print(solve2(signals))

# (0, 6, 9) are ambiguous
# (2, 3, 5) are ambiguous
# (1, 4, 7, 8) are unique

# present segments from 4 finds 9 from (0, 6, 9)
# missing segment from 1 finds 6 from (0, 6)
# the last one is 0

# present segments from 1 finds 3 from (2, 3, 5)
# 6 union 2 contains all segments
# 6 union 5 is missing one segment
