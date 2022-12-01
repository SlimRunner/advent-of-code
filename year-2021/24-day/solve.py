import sys
import re

# hasattr and getattr -> params are (class, "method")

class Reg(object):
    """docstring for Reg."""

    def __init__(self, value):
        super(Reg, self).__init__()
        self.value = value
    
    def inp(self, other):
        self.value = other
    
    def add(self, other):
        self.value = int(self.value + other)
    
    def mul(self, other):
        self.value = int(self.value * other)
    
    def div(self, other):
        if other == 0: raise ValueError("divisor cannot be zero")
        if self.value == 0: return
        sign = lambda x: x // abs(x)
        self.value = int(abs(self.value) // abs(other)) * sign(self.value) * sign(other)
    
    def mod(self, other):
        if other == 0: raise ValueError("divisor cannot be zero")
        self.value = int(self.value % other)
    
    def eql(self, other):
        self.value = 1 if self.value == other else 0

class SymReg(object):
    """docstring for SymReg."""

    def __init__(self, value):
        super(SymReg, self).__init__()
        if isinstance(value, SymReg):
            self.value = value
        elif isinstance(value, int):
            self.value = value
        elif isinstance(value, str):
            self.value = value if not SymReg.isNumber(value) else int(value)
        else:
            raise TypeError("value is not a valid integer or symbolic type")
        self.type = ""
        self.setType()
    
    @staticmethod
    def isNumber(value):
        return re.match("^-?\d+$", value) is not None
    
    @staticmethod
    def isParenBound(expr):
        return re.match("^\(.+\)$", expr) is not None
    
    @staticmethod
    def isNum(num, nMatch):
        if isinstance(num, str) and SymReg.isNumber(num):
            return int(num) == nMatch
        elif isinstance(num, int):
            return num == nMatch
        return False
    
    @staticmethod
    def enclose(expr):
        if SymReg.isParenBound(expr):
            return expr
        else:
            return "(" + expr +")"
    
    @staticmethod
    def isItConst(val):
        return True if isinstance(val, int) else False
    
    def isConst(self):
        return self.type == "const"
    
    def isExpr(self):
        return self.type == "expr"
    
    def setType(self):
        self.type = "const" if isinstance(self.value, int) else "expr"
    
    def getType(self):
        return self.type
    
    def inp(self, other):
        if isinstance(other, int):
            self.value = other
        elif isinstance(other, str):
            self.value = other if not SymReg.isNumber(other) else int(other)
        else:
            raise TypeError("value is not a valid integer or symbolic type")
        self.setType()
    
    def add(self, other):
        if SymReg.isNum(other, 0): return
        if SymReg.isNum(self.value, 0):
            self.value = other
            self.setType()
            return
        if self.isConst() and SymReg.isItConst(other):
            self.value = int(self.value + other)
        else:
            if self.isConst():
                # other is expr
                self.value = other + "+" + str(self.value)
            elif SymReg.isItConst(other):
                # self is expr
                self.value = self.value + "+" + str(other)
            else:
                self.value = self.value + "+" + other
        self.setType()
    
    def mul(self, other):
        if SymReg.isNum(other, 1): return
        if SymReg.isNum(self.value, 1):
            self.value = other
            self.setType()
            return
        if SymReg.isNum(other, 0) or SymReg.isNum(self.value, 0):
            self.value = 0
            self.setType()
            return
        if self.isConst() and SymReg.isItConst(other):
            self.value = int(self.value * other)
        else:
            if self.isConst():
                # other is expr
                self.value = str(self.value) + "*" + SymReg.enclose(other)
            elif SymReg.isItConst(other):
                # self is expr
                self.value = str(other) + "*" + SymReg.enclose(self.value)
            else:
                self.value = SymReg.enclose(self.value) + "*" + SymReg.enclose(other)
        self.setType()
    
    def div(self, other):
        if SymReg.isNum(other, 0): raise ValueError("divisor cannot be zero")
        if SymReg.isNum(other, 1): return
        if SymReg.isNum(self.value, 0):
            self.value = 0
            self.setType()
            return
        if self.isConst() and SymReg.isItConst(other):
            self.value = int(self.value) * int(other)
            sign = lambda x: x // abs(x)
            self.value = int(abs(self.value) // abs(other)) * sign(self) * sign(other)
        else:
            if self.isConst():
                # other is expr
                self.value = str(self.value) + "/" + SymReg.enclose(other)
            elif SymReg.isItConst(other):
                # self is expr
                self.value = SymReg.enclose(self.value) + "/" + str(other)
            else:
                self.value = SymReg.enclose(self.value) + "/" + SymReg.enclose(other)
        self.setType()
    
    def mod(self, other):
        if SymReg.isNum(other, 0): raise ValueError("divisor cannot be zero")
        if SymReg.isNum(other, 1) or SymReg.isNum(self.value, 0):
            self.value = 0
            self.setType()
            return
        if self.isConst() and SymReg.isItConst(other):
            self.value = int(self.value) % int(other)
        else:
            if self.isConst():
                # other is expr
                if self.value == 0: return
                self.value = "mod(" + str(self.value) + "," + other + ")"
            elif SymReg.isItConst(other):
                # self is expr
                self.value = "mod(" + self.value + "," + str(other) + ")"
            else:
                self.value = "mod(" + self.value + "," + other + ")"
        self.setType()
    
    def eql(self, other):
        if self.isConst() and SymReg.isItConst(other):
            self.value = 1 if self.value == other else 0
        else:
            if self.isConst():
                self.value = "eql(" + str(self.value) + "," + other + ")"
            elif SymReg.isItConst(other):
                self.value = "eql(" + self.value + "," + str(other) + ")"
            else:
                self.value = "eql(" + self.value + "," + other + ")"
        self.setType()

def main(args):
    pre = (lambda x:
        tuple(r if r.find(" ") == -1 else (r[:r.find(" ")], r[r.find(" ") + 1:])
        for r in re.search("(\w+)\s(.+)", x).groups()))
    if "-ex" in args:
        ins, sz = getLines("data.ex.txt", pred = pre)
    else:
        ins, sz = getLines("data.in.txt", pred = pre)
    # for i in range(1,10):
    #     o = run(ins, str(i) * sz, sz)
    # print(run(ins, "13579246899999", sz))
    regs = symRun(ins)
    print(regs["z"].value)
    print(run(ins, "666", sz))
    # print(run(ins, strp(0, sz), sz))
    
    # Brute Force (it may take days if you're lucky)
    # for i in range19(11111111111111,99999998177556):
    #     o = run(ins, strp(i, sz), sz)
    #     print(strp(i, sz), o, end="\r")
    # print(strp(i, sz), o)

def range19(a, b):
    while a <= b:
        if strp(b, 14).find("0") == -1:
            yield b
        b -= 1

def strp(num, size):
    sn = str(num)
    if len(sn) < size:
        return "0"*(size-len(sn)) + sn
    return sn

def symRun(inset):
    iv = 0
    getVar = lambda x: chr(x + 65)
    regs = {chr(i+119):SymReg(0) for i in range(0,4)}
    for ins in inset:
        comm, par = ins
        if comm != "inp":
            trg, val = par
            if val in "wxyz":
                getattr(regs[trg], comm)(regs[val].value)
            else:
                getattr(regs[trg], comm)(int(val))
        else:
            getattr(regs[par], "inp")(getVar(iv))
            iv += 1
    return regs

def run(inset, buffer, size):
    if len(buffer) < 1:
        raise ValueError(
            "buffer is " +
            str(len(buffer)) +
            " digits long. It must be " +
            str(size) + " digits long")
    buffer = [int(c) for c in reversed(buffer)]
    regs = {chr(i+119):Reg(0) for i in range(0,4)}
    # print("regs:", *[v.value for v in regs.values()])
    for ins in inset:
        comm, par = ins
        if comm != "inp":
            trg, val = par
            if val in "wxyz":
                getattr(regs[trg], comm)(getattr(regs[val], "value"))
            else:
                getattr(regs[trg], comm)(int(val))
            # print(comm, *par, " -> ", *[v.value for v in regs.values()])
        else:
            print("regs:", *[v.value for v in regs.values()])
            getattr(regs[par], "inp")(buffer.pop())
            print("regs:", *[v.value for v in regs.values()])
            print()
            # print(comm, par, " -> ", *[v.value for v in regs.values()])
    # print("regs:", *[v.value for v in regs.values()])
    return regs["z"].value

def getLines(fn, **kw):
    pred = (lambda x: x) if "pred" not in kw else kw["pred"]
    output = []
    isize = 0
    with open(fn) as f:
        line = f.readline()
        while line:
            line = line.strip()
            output.append(pred(line))
            if output[-1][0] == "inp": isize += 1
            line = f.readline()
    return output, isize

if __name__ == '__main__':
    main(sys.argv)
