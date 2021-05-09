
class PlayerClass0():
    def __init__(self, DEBUG):
        self.P = 0
        self.data = self.loadData()
        self.idx = 0
    
    def loadData(self):
        ret = []
        FIN = open("cmdList.txt").read().split('\n')
        P = self.P
        out = "Standard Output Stream:"
        readNext = False
        idx = 0
        for f in FIN:
            if readNext:
                fs = f.split()
                if P == 0:
                    if fs[-1] == "MINE":
                        ret.append(f)
                else:
                    if fs[-1] != "MINE":
                        ret.append(f)
                readNext = False
                idx += 1
            elif f == out:
                readNext = True
        return ret
    
    def run(self, status):
        self.idx += 1
        return self.data[self.idx-1]

class PlayerClass1():
    def __init__(self, DEBUG):
        self.P = 1
        self.data = self.loadData()
        self.idx = 0
    
    def loadData(self):
        ret = []
        FIN = open("cmdList.txt").read().split('\n')
        P = self.P
        out = "Standard Output Stream:"
        readNext = False
        idx = 0
        for f in FIN:
            if readNext:
                fs = f.split()
                if P == 0:
                    if fs[-1] == "MINE":
                        ret.append(f)
                else:
                    if fs[-1] != "MINE":
                        ret.append(f)
                readNext = False
                idx += 1
            elif f == out:
                readNext = True
        return ret
    
    def run(self, status):
        self.idx += 1
        return self.data[self.idx-1]

if __name__ == "__main__":
    player = PlayerClass0(True, 0)
