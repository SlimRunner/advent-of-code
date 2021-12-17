import sys
from math import prod

def main(args):
    H = getLines("input.in.txt")
    B = list(hex2bin(H))
    PK = []
    print(''.join(B))
    H, S = binParser(B)
    print(str(H).replace("\'", "\""))
    print("vsum: ", sumVersions(H))

def sumVersions(H):
    if H["type"] == 4: return H["ver"]
    ds = [sumVersions(d) for d in H["data"]]
    return sum(ds) + H["ver"]

def operateBin(H):
    D = H["data"]
    if H["type"] == 4: return D
    
    ds = [operateBin(d) for d in D]
    
    if H["type"] == 0:
        return sum(ds)
    elif H["type"] == 1:
        return prod(ds)
    elif H["type"] == 2:
        return min(ds)
    elif H["type"] == 3:
        return max(ds)
    elif H["type"] == 5:
        return 1 if ds[0] > ds[1] else 0
    elif H["type"] == 6:
        return 1 if ds[0] < ds[1] else 0
    elif H["type"] == 7:
        return 1 if ds[0] == ds[1] else 0

def binParser(B):
    if ''.join(B).replace("0", "") == "": return None
    packs = []
    pack = {}
    S = 0
    go = True
    while go:
        v, b = popBits(B, 3)
        pack = {"ver": v}
        v, b = popBits(B, 3)
        pack["type"] = v
        S += 6
        if pack["type"] == 4:
            d, s = getPackets(B)
            S += s
            pack["data"] = d
            go = False
        else:
            lt, _ = popBits(B, 1)
            # lt == 0: bit length
            # lt == 1: packet count
            D = []
            L, _ = popBits(B, 11 if lt else 15)
            if lt: # packet count
                for _ in range(0, L):
                    TUP = binParser(B)
                    if TUP is None: break
                    d, s = TUP
                    S += s
                    D.append(d)
            else: # bit length
                s = 0
                while s < L:
                    TUP = binParser(B)
                    if TUP is None: break
                    d, si = TUP
                    s += si
                    D.append(d)
                S += s
            pack["data"] = D
            go = False
        packs.append(pack)
    return *packs, S

def getPackets(B):
    size = 0
    frSz = 5 # fragment size
    data = ""
    go = True
    while go:
        size += frSz
        _, b = popBits(B, frSz)
        if b[0] == '1':
            data += b[1:]
        else:
            data += b[1:]
            data = int(data, 2)
            # popBits(B, 4 - (size % 4))
            go = False
    return data, size

def checkPack(p, v, t):
    return p["version"] == v and p["type"] == t

def popBits(B, n):
    b = ''.join(B[:n])
    for i in range(0, n): del B[0]
    return (int(b, 2), b)

def hex2bin(hex):
    arr = [bin(int(n, 16))[2:] for n in hex]
    b = ''.join(["0" * (4-len(n)) + n for n in arr])
    return b

def getLines(fn):
    output = []
    with open(fn) as f:
        output = f.readlines().pop().replace("\n", "")
    return output

if __name__ == '__main__':
    main(sys.argv)
