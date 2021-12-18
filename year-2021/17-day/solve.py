import sys

def main(args):
    comm = getLines("data.in.txt")
    print(comm)
    print("No code this time. I solved it in Desmos by brute force.")
    print("https://www.desmos.com/calculator/lnqrhfozbp")
    # part 1: https://www.desmos.com/calculator/y7gtbadrgr
    # tried 14,155
    # tried 155
    # dang I'm stupid it's the height not the y velocity
    # count hits: https://www.desmos.com/calculator/lg6saozhxi
    # tried 433. For got points passed the area in x
    # part 2: https://www.desmos.com/calculator/lnqrhfozbp
    # using example: https://www.desmos.com/calculator/ihnqasxyd2

def getLines(fn):
    output = []
    with open(fn) as f:
        output = f.readlines().pop().strip()
    return output

if __name__ == '__main__':
    main(sys.argv)
