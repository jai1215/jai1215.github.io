
def genMapInfo():
    ret = dict()
    FIN = open("MAP_info.txt", 'rt').read().split('\n')
    MAP = []
    for f in FIN:
        f = list(map(int, f.split()))
        MAP.append(f)
    ret['shadow'] = []

    for i in range(37):
        m = []
        for d in range(6):#direction
            prv = MAP[i][d+1]
            shadow = [prv]
            for j in range(2):
                if prv == -1:
                    shadow.append(-1)
                else:
                    prv = MAP[prv][d+1]
                    shadow.append(prv)
            m.append(shadow)
        ret['shadow'].append(m)
    
    ret['area'] = []

    for i in range(37):
        m = []
        d0 = set(MAP[i][1:])
        m.append(d0)

        d1 = set()
        for p in d0:
            if p == -1:
                continue
            else:
                d1 = d1 | set(MAP[p][1:])
        m.append(d1)
        
        d2 = set()
        for p in d1:
            if p == -1:
                continue
            else:
                d2 = d2 | set(MAP[p][1:])
        m.append(d2)
        ret['area'].append(m)
    return ret

if __name__ == "__main__":
    minfo = genMapInfo()
    print(minfo['shadow'])