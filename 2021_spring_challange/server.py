from PlayerClass0   import *
from PlayerClass0_1 import *
# from cmdBot import *
from genMapInfo import *
from tqdm import trange

def testSet(testNum):
    treeData   = [30, 24, 21, 33]
    zeroGround = [12, 15, 18, 23]
    testNum = random.randint(0, 4) 
    if testNum == 0:
        treeData   = [22, 25, 31, 34]
        zeroGround = [1, 4, 9, 15, 20, 27, 29, 36]
    elif testNum == 1: 
        treeData   = [30, 24, 21, 33]
        zeroGround = [12, 15, 18, 23]
    elif testNum == 2:
        treeData   = [19, 25, 28, 34]
        zeroGround = [10, 16]
    elif testNum == 3:
        treeData   = [19, 22, 28, 31]
        zeroGround = [21, 23, 30, 32]
    elif testNum == 4:
        treeData   = [21, 34, 25, 30]
        zeroGround = [4, 12, 26, 1, 18, 35]


    m = random.randint(0, 1) 
    o = (m+1)%2
    server.addTree(m, treeData[0], 1)
    server.addTree(m, treeData[1], 1)
    server.addTree(o, treeData[2], 1)
    server.addTree(o, treeData[3], 1)

    for z in zeroGround:
        server.fixBonus(z, 0)

class SERVER():
    def __init__(self, MAP_INFO):
        self.MAP_INFO = MAP_INFO
        self.ALL_TREE = []
        self.TREE = [[],[]]
        self.PLAYER = []
        self.MAP = []
        self.BOT = []
        self.NUT = 20
        #Generate Player
        for i in range(2):
            P = dict ()
            P['WAIT'] = False
            P['POINT'] = 0
            P['SUN'] = 0
            P['TREE'] = [0, 0, 0, 0]
            self.PLAYER.append(P)

        #Generate MAP
        for i in range(37):
            m = dict()
            if i < 7:
                m['bonus'] = 4
            elif i < 19:
                m['bonus'] = 2
            else:
                m['bonus'] = 0
            self.MAP.append(m)
    
    def calcTreeNum(self, T):
        ret = [0, 0, 0, 0]
        for t in T:
            ret[t['size']] += 1
        return ret

    def addTree(self, player, idx, size, dormant=False):
        t = dict()
        t['player'] = player
        t['size'] = size
        t['idx'] = idx
        t['dormant'] = dormant
        self.MAP[idx]['tree'] = t
        self.ALL_TREE.append(t)
        self.TREE[player].append(t)
        self.PLAYER[player]['TREE'] = self.calcTreeNum(self.TREE[player])
    
    def getCost(self, P, size):
        treeNum = self.PLAYER[P]['TREE']
        if size == -1:
            return 0 + treeNum[size+1]
        elif size == 0:
            return 1 + treeNum[size+1]
        elif size == 1:
            return 3 + treeNum[size+1]
        elif size == 2:
            return 7 + treeNum[size+1]

    def fixBonus(self, idx, value):
        self.MAP[idx]['bonus'] = -1
    
    def setTREE_dormant(self, idx):
        ALL_TREE = self.ALL_TREE
        for t in ALL_TREE:
            if t['idx'] == idx:
                t['dormant'] = True
                return
        
    def removeTree(self, P, idx):
        ALL_TREE = self.ALL_TREE
        for i, t in enumerate(ALL_TREE):
            if t['idx'] == idx:
                del ALL_TREE[i]
                break

        TREE = self.TREE[P]
        for i, t in enumerate(TREE):
            if t['idx'] == idx:
                del TREE[i]
                break

        del(self.MAP[idx]['tree'])
        
    def growTree(self, idx):
        ALL_TREE = self.ALL_TREE
        for t in ALL_TREE:
            if t['idx'] == idx:
                t['size'] += 1
                return t['size']-1

    def calcCMDSub(self, P, cmd):
        #Update Wait Status
        # print(cmd)
        if cmd[0] == "WAIT":
            self.PLAYER[P]['WAIT'] = True
            return
        #Update Seed
        if cmd[0] == "SEED":
            self.setTREE_dormant(cmd[1])
            cost = self.getCost(P, -1)
            self.PLAYER[P]['SUN'] -= cost
            self.addTree(P, cmd[2], 0, True)
            assert self.PLAYER[P]['SUN'] >= 0
            return
        #Update Grow
        if cmd[0] == "GROW":
            self.setTREE_dormant(cmd[1])
            size = self.growTree(cmd[1])
            cost = self.getCost(P, size)
            self.PLAYER[P]['TREE'][size  ] -= 1
            self.PLAYER[P]['TREE'][size+1] += 1
            self.PLAYER[P]['SUN'] -= cost
            assert self.PLAYER[P]['SUN'] >= 0
        #Update Complete
        if cmd[0] == "COMPLETE":
            self.removeTree(P, cmd[1])
            # print(self.NUT, self.MAP[cmd[1]]['bonus'], cmd[1])
            self.PLAYER[P]['POINT'] += (self.NUT+self.MAP[cmd[1]]['bonus'])
            self.PLAYER[P]['SUN'] -= 4
            self.PLAYER[P]['TREE'][3] -= 1
    
    def calcCMD(self, cmd0, cmd1):
        cmd0 = cmd0.split()
        for i, c in enumerate(cmd0[1:]):
            try:
                cmd0[i+1] = int(c)
            except:
                cmd0[i+1] = c
        cmd1 = cmd1.split()
        for i, c in enumerate(cmd1[1:]):
            try:
                cmd1[i+1] = int(c)
            except:
                cmd1[i+1] = c
        #Special Condition
        if (cmd0[0] == "SEED") & (cmd1[0] == "SEED"):
            if cmd0[2] == cmd1[2]:
                self.setTREE_dormant(cmd0[1])
                self.setTREE_dormant(cmd1[1])
                return
        #Normal Condition
        self.calcCMDSub(0, cmd0)
        self.calcCMDSub(1, cmd1)
        if cmd0[0] == "COMPLETE":
            self.NUT -= 1
        if cmd1[0] == "COMPLETE":
            self.NUT -= 1
    
    def makeShadow(self, DAY):
        ret = [0]*37
        TREE = self.ALL_TREE
        ShadowInfo = self.MAP_INFO['shadow']
        DIR = DAY%6
        for t in TREE:
            # print(t['idx'], t['size'], ShadowInfo[t['idx']], ShadowInfo[t['idx']][DIR][:t['size']])
            tSize = t['size']
            if tSize == 0:
                continue
            sInfo = ShadowInfo[t['idx']][DIR]
            for s in sInfo[:tSize]:
                if s == -1:
                    continue
                if ret[s] < tSize:
                    ret[s] = tSize
        return ret
    
    def calcSunPoint(self, P, S_MAP):
        TREE = self.TREE[P]
        ret = 0
        for t in TREE:
            if t['size'] > S_MAP[t['idx']]:
                ret += t['size']
        return ret

    def cmdList (self, P):
        TREE = self.TREE[P]
        SUN = self.PLAYER[P]['SUN']
        ret = []
        #GROW+SEED+COMPLETE
        for t in TREE:
            if t['dormant']:
                continue
                #COMPLETE
            if t['size'] == 3:
                if SUN >= 4:
                    ret.append("COMPLETE %d" % t['idx'])
            else:
                #GROW
                cost = self.getCost(P, t['size'])
                if SUN >= cost:
                    ret.append("GROW %d" % t['idx'])

            #SEED
            if t['size'] > 0:
                if SUN >= self.getCost(P, -1):
                    t_area = self.MAP_INFO['area'][t['idx']]
                    t_area = t_area[t['size']-1]
                    for p in t_area:
                        if p == -1:
                            continue
                        elif 'tree' in self.MAP[p]:
                            continue
                        elif self.MAP[p]['bonus'] == -1:
                            continue
                        else:
                            ret.append("SEED %d %d" % (t['idx'], p))
        #WAIT
        ret.append("WAIT")
        return ret

    def generateInp (self, P, DAY, NUT):
        PLAYER = self.PLAYER
        me = P
        op = 1 if me == 0 else 1
        MAP = []
        for i in range(37):
            m = dict()
            m['idx'] = i
            bonus = self.MAP[i]['bonus']
            if bonus == -1:
                m['rich'] = 0
            elif bonus == 0:
                m['rich'] = 1
            elif bonus == 2:
                m['rich'] = 2
            elif bonus == 4:
                m['rich'] = 3
            MAP.append(m)
        ret = dict()
        ret['MAP'] = MAP
        ret['DAY'] = DAY
        ret['TIME'] = DAY%6
        ret['NUTRIENTS'] = NUT
        ret['SUN'] = PLAYER[me]['SUN']
        ret['SCORE'] = PLAYER[me]['POINT']
        ret['OPP_SUN'] = PLAYER[op]['SUN']
        ret['OPP_SCORE'] = PLAYER[op]['POINT']
        ret['OPP_WAITING'] = PLAYER[op]['WAIT']
        ret['N_TREES'] = len(self.ALL_TREE)
        ret['TREE'] = self.ALL_TREE
        ret['MY_TREE'] = self.TREE[me]
        ret['OP_TREE'] = self.TREE[op]
        #P_MOVE = status['P_MOVE'] 
        #P_MOVES = status['P_MOVES'] 
        ret['P_MOVES'] = self.cmdList(P)
        ret['P_MOVE'] = len(ret['P_MOVES'])
        return ret
    
    def run(self):
        DAY = 0
        MAP = self.MAP
        PLAYER = self.PLAYER
        TREE = self.TREE
        BOT = self.BOT
        TURN = 0

        #Give Initial Point
        shadow_map = self.makeShadow(DAY)
        self.PLAYER[0]['SUN'] += self.calcSunPoint(0, shadow_map)
        self.PLAYER[1]['SUN'] += self.calcSunPoint(1, shadow_map)

        while DAY < 24:
            #Print Game Information
            # print("[%3d/%2d] SUN : " % (TURN, DAY), self.PLAYER[0]['SUN'], self.PLAYER[1]['SUN'])
            # print("[%3d/%2d] PNT : " % (TURN, DAY), self.PLAYER[0]['POINT'], self.PLAYER[1]['POINT'])

            #Generate Input Information
            status0, status1 = dict(), dict()
            if not self.PLAYER[0]['WAIT']:
                status0 = self.generateInp(0, DAY, self.NUT)
            if not self.PLAYER[1]['WAIT']:
                status1 = self.generateInp(1, DAY, self.NUT)

            #Run Bot
            cmd0, cmd1 = "WAIT", "WAIT"
            if not self.PLAYER[0]['WAIT']:
                cmd0 = self.BOT[0].run(status0)
            if not self.PLAYER[1]['WAIT']:
                cmd1 = self.BOT[1].run(status1)

            # print(">", cmd0, cmd1)
            self.calcCMD(cmd0, cmd1)

            #Update DAY
            if self.PLAYER[0]['WAIT'] & self.PLAYER[1]['WAIT']:
                DAY += 1
                if DAY == 24:
                    break

                #Reset Wait
                self.PLAYER[0]['WAIT'] = False
                self.PLAYER[1]['WAIT'] = False
                #Calc New SUN
                shadow_map = self.makeShadow(DAY)
                # print(shadow_map)
                self.PLAYER[0]['SUN'] += self.calcSunPoint(0, shadow_map)
                self.PLAYER[1]['SUN'] += self.calcSunPoint(1, shadow_map)
                #Reset Dormant
                for t in self.ALL_TREE:
                    t['dormant'] = False
                # print("treeNum[%d]"%0, self.PLAYER[0])
                # print("treeNum[%d]"%1, self.PLAYER[1])

            TURN += 1
        # print("SUN :",self.PLAYER[0]['SUN'],self.PLAYER[1]['SUN'])
        self.PLAYER[0]['POINT'] += (self.PLAYER[0]['SUN']//3)
        self.PLAYER[1]['POINT'] += (self.PLAYER[1]['SUN']//3)
        return (self.PLAYER[0]['POINT'], self.PLAYER[1]['POINT'])
def genSeedParam():
    PARAM = dict()
    PARAM['t_weight'] = [1, 1, 1, 1]
    for i in range(3):
        PARAM['t_weight'][i+1] = PARAM['t_weight'][i]*random.uniform(1,2)
    PARAM['rich_weight'] = [0, 1, 1, 1]
    for i in range(2):
        PARAM['rich_weight'][i+2] = PARAM['rich_weight'][i+1]*random.uniform(0.5, 1)
    PARAM['dist_weight'] = random.uniform(0.5,1)
    PARAM['dir_weight'] = random.uniform(0.5,1)
    return PARAM

def genCompleteParam():
    PARAM = dict()
    PARAM['t_weight'] = [0.5, 0.5, 0.5, 0.5]
    for i in range(3):
        PARAM['t_weight'][i+1] = PARAM['t_weight'][i]*random.uniform(1,2.5)
    PARAM['rich_weight'] = [0, 0, 0, 0]
    for i in range(3):
        PARAM['rich_weight'][i+1] = PARAM['rich_weight'][i]+random.uniform(0.1, 2)
    PARAM['dir_weight'] = random.uniform(0.5,1)
    return PARAM


def genParam():
    PARAM  = {'N3TREE': 4.214990363260124, 'N2TREE': 4.6484097861807925, 'N1TREE': 2.8953849083215153, 'N0TREE': 1.6051889387738545, 'P3TREE': 3.223750616920615, 'P2TREE': 3.1873067243682245, 'P1TREE': 2.973276346614215, 'P0TREE': 2.7967370068187463, 'D4_SUB': 18.26442874819276, 'N3_DAY': 21.69986468070954, 'N2_DAY': 19.399745581203764, 'N1_DAY': 18.582896302570763, 'N0_DAY': 15.563996366559259, 'P3_DAY': 1.9903466279674804, 'P2_DAY': 0.024571685187697145, 'P1_DAY': 0.7684355195850935, 'P0_DAY': 1.6342274335832325, 'D5': 2.7847871520676515, 'SEED': {'t_weight': [1, 1.6693820681948957, 1.6836939320689264, 2.410656838875838], 'rich_weight': [0, 1, 0.5047876001795205, 0.422037171179147], 'dist_weight': 0.6141772550040409, 'dir_weight': 0.9116738433903484}}

    PARAM['N3TREE'] = random.uniform(3.5,5)
    PARAM['N2TREE'] = random.uniform(3.5,6)
    PARAM['N1TREE'] = random.uniform(1.5,3.5)
    PARAM['N0TREE'] = random.uniform(1,3)

    PARAM['P3TREE'] = random.uniform(2.3, 3.3)
    PARAM['P2TREE'] = random.uniform(2, 3.3)
    PARAM['P1TREE'] = random.uniform(2, 3.3)
    PARAM['P0TREE'] = random.uniform(2, 3.3)

    #PARAM['D4_SUB'] = random.uniform(18,25)
    #PARAM['N3_DAY'] = random.uniform(19,22)
    #PARAM['N2_DAY'] = random.uniform(17,21)
    #PARAM['N1_DAY'] = random.uniform(14,19)
    #PARAM['N0_DAY'] = random.uniform(8,16)

    #PARAM['P3_DAY'] = random.uniform(0 ,5)
    #PARAM['P2_DAY'] = random.uniform(0 ,5)
    #PARAM['P1_DAY'] = random.uniform(0 ,5)
    #PARAM['P0_DAY'] = random.uniform(0 ,5)

    #PARAM['D5'] = random.uniform(1,20)
    return PARAM

if __name__ == "__main__":
    MAP_INFO = genMapInfo()
    # print(MAP_INFO['shadow'])
    DEBUG = False

    FOUT = open("paramTest.txt", "wt")
    for games in range(1000):
        GAMES = 1000
        win0, win1 = 0, 0
        point0, point1 = 0, 0
        # param = genParam()
        # param['SEED'] = genSeedParam()
        param1 = {'N3TREE': 3.593424033095925, 'N2TREE': 4.025380536656719, 'N1TREE': 1.6875764423191195, 'N0TREE': 1.3344011070588302, 'P3TREE': 2.452107158206813, 'P2TREE': 3.055260266663076, 'P1TREE': 2.808985370609426, 'P0TREE': 2.8100771047738573, 'D4_SUB': 18.26442874819276, 'N3_DAY': 21.69986468070954, 'N2_DAY': 19.399745581203764, 'N1_DAY': 18.582896302570763, 'N0_DAY': 15.563996366559259, 'P3_DAY': 1.9903466279674804, 'P2_DAY': 0.024571685187697145, 'P1_DAY': 0.7684355195850935, 'P0_DAY': 1.6342274335832325, 'D5': 2.7847871520676515, 'SEED': {'t_weight': [1, 1.6693820681948957, 1.6836939320689264, 2.410656838875838], 'rich_weight': [0, 1, 0.5047876001795205, 0.422037171179147], 'dist_weight': 0.6141772550040409, 'dir_weight': 0.9116738433903484}, 'COMPLETE': {'t_weight': [0.5, 0.5636622125373422, 0.905095588140056, 1.32410752389845], 'rich_weight': [0, 0.30179060990363765, 0.9283408631503773, 1.3524893407212302], 'dir_weight': 0.7678390697449116}}
        param2 = {'N3TREE': 3.593424033095925, 'N2TREE': 4.025380536656719, 'N1TREE': 1.6875764423191195, 'N0TREE': 1.3344011070588302, 'P3TREE': 2.452107158206813, 'P2TREE': 3.055260266663076, 'P1TREE': 2.808985370609426, 'P0TREE': 2.8100771047738573, 'D4_SUB': 18.26442874819276, 'N3_DAY': 21.69986468070954, 'N2_DAY': 19.399745581203764, 'N1_DAY': 18.582896302570763, 'N0_DAY': 15.563996366559259, 'P3_DAY': 1.9903466279674804, 'P2_DAY': 0.024571685187697145, 'P1_DAY': 0.7684355195850935, 'P0_DAY': 1.6342274335832325, 'D5': 2.7847871520676515, 'SEED': {'t_weight': [1, 1.6693820681948957, 1.6836939320689264, 2.410656838875838], 'rich_weight': [0, 1, 0.5047876001795205, 0.422037171179147], 'dist_weight': 0.6141772550040409, 'dir_weight': 0.9116738433903484}, 'COMPLETE': {'t_weight': [0.5, 0.5636622125373422, 0.905095588140056, 1.32410752389845], 'rich_weight': [0, 0.30179060990363765, 0.9283408631503773, 1.3524893407212302], 'dir_weight': 0.7678390697449116}}
        win_ratio = 0
        # for i in range(GAMES):
        for i in trange(GAMES):
            server = SERVER(MAP_INFO)
            #TEST MAP
            testSet(0)

            #Add Player
            server.BOT.append(PlayerClass0  (DEBUG, param1))
            server.BOT.append(PlayerClass0_1(DEBUG, param2))
            #run
            p0, p1 = server.run()
            point0 += p0
            point1 += p1
            if p0 > p1:
                win0 += 1
            elif p1 > p0:
                win1 += 1
            win_ratio = 0
            if win0+win1 > 0:
                win_ratio = (win0/(win0+win1))
            if i > 100:
                if  win_ratio < 0.3:
                    break
            elif i > 400:
                if win_ratio < 0.45:
                    break
        print("[%4d] %4d %4d %3.1f %% - (%3.1f point %3.1f point) - %s" % (games, win0, win1, win0/(win0+win1)*100, point0/GAMES, point1/GAMES, str(param)))
        if win_ratio > 0.4:
            FOUT.write("[%4d] %4d %4d %3.1f %% - (%3.1f point %3.1f point) - %s\n" % (games, win0, win1, win0/(win0+win1)*100, point0/GAMES, point1/GAMES, str(param)))
            FOUT.flush()
    FOUT.close()

