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

