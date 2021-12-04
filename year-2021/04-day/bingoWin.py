def getLines(fn):
    output = []
    with open(fn) as f:
        nums = [int(x) for x in f.readline().strip().split(",")]
        cards = []
        width = 0
        line = f.readline()
        idx = 0
        while line:
            if line.strip() == "":
                cards.append([])
                idx = len(cards) - 1
            else:
                if width == 0: width = len(line.split())
                cards[idx].extend([int(x) for x in line.strip().split()])
            line = f.readline()
    height = len(cards[0]) // width
    return (nums, cards, width, height)

def genWinPattern(w, h):
    output = []
    wbf = (1 << w) - 1
    hbf = sum([1 << i for i in range(0, w * h, w)])
    for x in range(0, w):
        output.append(wbf << x * w)
    for y in range(0, h):
        output.append(hbf << y)
    return output

def bitMatch(value, bitfield):
    for target in bitfield:
        if value & target == target: return True

def bingoFirstWin(fn):
    calls, cards, w, h = getLines(fn)
    marks = [0] * len(cards)
    winPatterns = genWinPattern(w, h)
    for nthCall, call in enumerate(calls):
        for idx, card in enumerate(cards):
            try:
                match = cards[idx].index(call)
                marks[idx] |= 1 << match
                if bitMatch(marks[idx], winPatterns):
                    return (cards[idx], calls[0:nthCall + 1])
            except Exception as e:
                pass

winner, calls = bingoFirstWin("bingoCards.in.txt")
diff = list(set(winner) - set(calls))
print(sum(diff) * calls.pop())
