import re

def getLines(fn):
    output = []
    with open(fn) as f:
        text = f.readlines()[0].strip()
        output = [int(x) for x in re.findall("\d+", text)]
    return output

def solution(states, days):
    for _ in range(days):
        idx = 0
        iterLen = len(states)
        while idx < iterLen:
            states[idx] -= 1
            if states[idx] < 0:
                states[idx] = 6
                states.append(8)
            idx += 1
    return len(states)

print(solution(getLines("input.in.txt"), 80))
