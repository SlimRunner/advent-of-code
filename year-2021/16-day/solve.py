import sys
from math import prod

def main(args):
    visargs = "-a" in args
    H = getLines("input.in.txt")
    B = list(hex2bin(H))
    T = packetParser(B.copy())
    if visargs or "-h" in args:
        print("\nhex stream")
        print(H)
    if visargs or "-b" in args:
        print("\nbit stream")
        print(''.join(B))
    if visargs or "-t" in args:
        print("\npacket tree")
        print(str(T).replace("\'", "\""))
    print()
    print("vsum: ", sumVersions(T))
    print("ops : ", operateBin(T))

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

def packetParser(B):
    v = popBits(B, 3)[0]
    t = popBits(B, 3)[0]
    P = {"ver": v, "type": t, "size": 6}
    if t == 4:
        P["data"], s = getPackets(B)
        P["size"] += s
    else:
        lt = popBits(B, 1)[0]
        n = 15 if lt == 0 else 11
        L = popBits(B, n)[0]
        P["size"] += n + 1
        if lt:
            # packet count
            P["data"] = [packetParser(B) for _ in range(0, L)]
            P["size"] += sum(p["size"] for p in P["data"])
        else:
            # bit length
            NB = popElem(B, L)
            pc = []
            while len(NB) > 0:
                pc.append(packetParser(NB))
            P["data"] = pc
            P["size"] += L
    return P

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

def popElem(B, n):
    b = B[:n]
    for i in range(0, n): del B[0]
    return b

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
