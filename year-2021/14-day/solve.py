import re

def main():
    seed, rules = getLines("input.in.txt")
    for i in range(0, 10):
        seed = applyRules(seed, rules)
    freq = {}
    for char in seed:
        if char in freq:
            freq[char] += 1
        else:
            freq[char] = 1
    diff = freq[max(freq, key = freq.get)] - freq[min(freq, key = freq.get)]
    print(diff)

def getLines(fn):
    template = ''
    
    with open(fn) as f:
        template = f.readline().strip()
        subs = []
        f.readline()
        line = f.readline()
        while line:
            line = line.strip()
            sepLoc = line.find(" -> ")
            pairing = (line[:sepLoc], line[sepLoc+4:])
            subs.append(pairing)
            line = f.readline()
    return (template, subs)

def applyRules(seed, rules):
    idx = 0
    pairs = []
    while idx < len(seed) - 1:
        pair = seed[idx] + seed[idx + 1]
        for rule in rules:
            if rule[0].find(pair) >= 0:
                pair = rule[1] + pair[1]
                break
        pairs.append(pair)
        idx += 1
    pairs.insert(0, seed[0])
    return "".join(pairs)

if __name__ == '__main__':
    main()
