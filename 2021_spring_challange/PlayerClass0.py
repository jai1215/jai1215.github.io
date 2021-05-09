import sys
import math
import random

class PlayerClass0():
    def __init__(self, DEBUG, PARAM):
        self.DEBUG = DEBUG
        self.PARAM = PARAM
        pass

    def run(self, status):
        def pprint(s, info=""):
            if self.DEBUG:
                print(info, s, file=sys.stderr, flush=True)

        def sizeOf(TREE, idx):
            for t in TREE:
                if t['idx'] == idx:
                    return t['size']

        def shadowingCompletePri(idx, DAY, MAP, PARAM):
            SHADOW = [[[1, 7, 19], [2, 9, 22], [3, 11, 25], [4, 13, 28], [5, 15, 31], [6, 17, 34]], [[7, 19, -1], [8, 21, -1], [2, 10, 24], [0, 4, 13], [6, 16, 32], [18, 35, -1]], [[8, 20, -1], [9, 22, -1], [10, 24, -1], [3, 12, 27], [0, 5, 15], [1, 18, 35]], [[2, 8, 20], [10, 23, -1], [11, 25, -1], [12, 27, -1], [4, 14, 30], [0, 6, 17]], [[0, 1, 7], [3, 10, 23], [12, 26, -1], [13, 28, -1], [14, 30, -1], [5, 16, 33]], [[6, 18, 36], [0, 2, 9], [4, 12, 26], [14, 29, -1], [15, 31, -1], [16, 33, -1]], [[18, 36, -1], [1, 8, 21], [0, 3,         11], [5, 14, 29], [16, 32, -1], [17, 34, -1]], [[19, -1, -1], [20, -1, -1], [8, 9, 23], [1, 0, 4], [18, 17, 33], [36, -1, -1]], [[20, -1, -1], [21, -1, -1], [9, 23, -1], [2, 3, 12], [1, 6, 16], [7, 36, -1]], [[21, -1, -1], [22, -1, -1], [23, -1, -1], [10, 11, 26], [2, 0, 5], [8, 7, 36]], [[9, 21, -1], [23, -1, -1], [24, -1, -1], [11, 26, -1], [3, 4, 14], [2, 1, 18]], [[10, 9, 21], [24, -1, -1], [25, -1, -1], [26, -1, -1], [12, 13, 29], [3, 0, 6]], [[3, 2, 8], [11, 24, -1], [26, -1, -1], [27, -1, -1], [13, 29, -1], [4, 5, 16]], [[4, 0, 1], [12, 11, 24], [27, -1, -1], [28, -1, -1], [29, -1, -1], [14, 15, 32]], [[5, 6, 18], [4, 3, 10], [13, 27, -1], [29, -1, -1], [30, -1, -1], [15,         32, -1]], [[16, 17, 35], [5, 0, 2], [14, 13, 27], [30, -1, -1], [31, -1, -1], [32, -1, -1]], [[17, 35, -1], [6, 1, 8], [5, 4, 12], [15, 30, -1], [32, -1, -1], [33, -1, -1]], [[35, -1, -1], [18, 7, 20], [6, 0, 3], [16, 15, 30], [33, -1, -1], [34, -1, -1]], [[36, -1, -1], [7, 20, -1], [1, 2, 10], [6, 5, 14], [17, 33, -1], [35, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [20, 21, 22], [7, 1, 0], [36, 35, 34], [-1, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [21, 22, -1], [8, 2, 3], [7, 18, 17], [19, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [22, -1, -1], [9, 10, 11], [8, 1, 6], [20, 19, -1]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [23, 24, 25], [9, 2, 0], [21, 20, 19]], [[22, -1, -1], [-1, -1, -1], [-1, -1, -1], [24, 25, -1], [10, 3, 4], [9, 8, 7]], [[23, 22, -1], [-1, -1, -1], [-1, -1, -1], [25, -1, -1], [11, 12, 13], [10, 2, 1]], [[24, 23, 22], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [26, 27, 28], [11, 3, 0]], [[11, 10, 9], [25, -1, -1], [-1, -1, -1], [-1, -1, -1], [27, 28, -1], [12, 4, 5]], [[12, 3, 2], [26, 25, -1], [-1, -1, -1], [-1, -1, -1], [28, -1, -1], [13, 14, 15]], [[13, 4, 0], [27, 26, 25], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [29, 30, 31]], [[14, 5, 6], [13, 12, 11], [28, -1, -1], [-1, -1, -1], [-1, -1, -1], [30, 31, -1]], [[15, 16, 17], [14, 4, 3], [29, 28, -1], [-1, -1, -1], [-1, -1, -1], [31, -1, -1]], [[32, 33, 34], [15, 5, 0], [30, 29, 28],         [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]], [[33, 34, -1], [16, 6, 1], [15, 14, 13], [31, -1, -1], [-1, -1, -1], [-1, -1, -1]], [[34, -1, -1], [17, 18, 7], [16, 5, 4], [32,         31, -1], [-1, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [35, 36, 19], [17, 6, 0], [33, 32, 31], [-1, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [36, 19, -1], [18, 1, 2], [17, 16,         15], [34, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [19, -1, -1], [7, 8, 9], [18, 6, 5], [35, 34, -1], [-1, -1, -1]]]
            TIME = (DAY+1)%6
            dir_weight = 1
            total_loss = 0
            t_weight = PARAM['t_weight']
            rich_weight = PARAM['rich_weight']
            rich_weight = rich_weight[MAP[idx]['rich']]
            S = SHADOW[idx]
            for direction in range(6):
                sun_dir = (TIME+direction)%6
                s = S[sun_dir]
                for distance in range(3):
                    s_idx = s[distance]
                    if s_idx != -1:
                        m = MAP[s_idx]
                        if 'tree' in m:
                            if m['tree']['mine']:
                                total_loss -= (t_weight[m['tree']['size']]*dir_weight)
                            else:
                                total_loss += (t_weight[m['tree']['size']]*dir_weight)
                    else:
                        break
                dir_weight *= PARAM['dir_weight']
            total_loss *= rich_weight
            return total_loss

        def shadowingSeedPri(idx, DAY, MAP, PARAM):
            SHADOW = [[[1, 7, 19], [2, 9, 22], [3, 11, 25], [4, 13, 28], [5, 15, 31], [6, 17, 34]], [[7, 19, -1], [8, 21, -1], [2, 10, 24], [0, 4, 13], [6, 16, 32], [18, 35, -1]], [[8, 20, -1], [9, 22, -1], [10, 24, -1], [3, 12, 27], [0, 5, 15], [1, 18, 35]], [[2, 8, 20], [10, 23, -1], [11, 25, -1], [12, 27, -1], [4, 14, 30], [0, 6, 17]], [[0, 1, 7], [3, 10, 23], [12, 26, -1], [13, 28, -1], [14, 30, -1], [5, 16, 33]], [[6, 18, 36], [0, 2, 9], [4, 12, 26], [14, 29, -1], [15, 31, -1], [16, 33, -1]], [[18, 36, -1], [1, 8, 21], [0, 3,         11], [5, 14, 29], [16, 32, -1], [17, 34, -1]], [[19, -1, -1], [20, -1, -1], [8, 9, 23], [1, 0, 4], [18, 17, 33], [36, -1, -1]], [[20, -1, -1], [21, -1, -1], [9, 23, -1], [2, 3, 12], [1, 6, 16], [7, 36, -1]], [[21, -1, -1], [22, -1, -1], [23, -1, -1], [10, 11, 26], [2, 0, 5], [8, 7, 36]], [[9, 21, -1], [23, -1, -1], [24, -1, -1], [11, 26, -1], [3, 4, 14], [2, 1, 18]], [[10, 9, 21], [24, -1, -1], [25, -1, -1], [26, -1, -1], [12, 13, 29], [3, 0, 6]], [[3, 2, 8], [11, 24, -1], [26, -1, -1], [27, -1, -1], [13, 29, -1], [4, 5, 16]], [[4, 0, 1], [12, 11, 24], [27, -1, -1], [28, -1, -1], [29, -1, -1], [14, 15, 32]], [[5, 6, 18], [4, 3, 10], [13, 27, -1], [29, -1, -1], [30, -1, -1], [15,         32, -1]], [[16, 17, 35], [5, 0, 2], [14, 13, 27], [30, -1, -1], [31, -1, -1], [32, -1, -1]], [[17, 35, -1], [6, 1, 8], [5, 4, 12], [15, 30, -1], [32, -1, -1], [33, -1, -1]], [[35, -1, -1], [18, 7, 20], [6, 0, 3], [16, 15, 30], [33, -1, -1], [34, -1, -1]], [[36, -1, -1], [7, 20, -1], [1, 2, 10], [6, 5, 14], [17, 33, -1], [35, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [20, 21, 22], [7, 1, 0], [36, 35, 34], [-1, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [21, 22, -1], [8, 2, 3], [7, 18, 17], [19, -1, -1]], [[-1, -1, -1], [-1, -1, -1], [22, -1, -1], [9, 10, 11], [8, 1, 6], [20, 19, -1]], [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [23, 24, 25], [9, 2, 0], [21, 20, 19]], [[22, -1, -1], [-1, -1, -1], [-1, -1, -1], [24, 25, -1], [10, 3, 4], [9, 8, 7]], [[23, 22, -1], [-1, -1, -1], [-1, -1, -1], [25, -1, -1], [11, 12, 13], [10, 2, 1]], [[24, 23, 22], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [26, 27, 28], [11, 3, 0]], [[11, 10, 9], [25, -1, -1], [-1, -1, -1], [-1, -1, -1], [27, 28, -1], [12, 4, 5]], [[12, 3, 2], [26, 25, -1], [-1, -1, -1], [-1, -1, -1], [28, -1, -1], [13, 14, 15]], [[13, 4, 0], [27, 26, 25], [-1, -1, -1], [-1, -1, -1], [-1, -1, -1], [29, 30, 31]], [[14, 5, 6], [13, 12, 11], [28, -1, -1], [-1, -1, -1], [-1, -1, -1], [30, 31, -1]], [[15, 16, 17], [14, 4, 3], [29, 28, -1], [-1, -1, -1], [-1, -1, -1], [31, -1, -1]], [[32, 33, 34], [15, 5, 0], [30, 29, 28],         [-1, -1, -1], [-1, -1, -1], [-1, -1, -1]], [[33, 34, -1], [16, 6, 1], [15, 14, 13], [31, -1, -1], [-1, -1, -1], [-1, -1, -1]], [[34, -1, -1], [17, 18, 7], [16, 5, 4], [32,         31, -1], [-1, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [35, 36, 19], [17, 6, 0], [33, 32, 31], [-1, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [36, 19, -1], [18, 1, 2], [17, 16,         15], [34, -1, -1], [-1, -1, -1]], [[-1, -1, -1], [19, -1, -1], [7, 8, 9], [18, 6, 5], [35, 34, -1], [-1, -1, -1]]]
            TIME = (DAY+4)%6
            dir_weight = 1
            total_loss = 0
            t_weight = PARAM['t_weight']
            rich_weight = PARAM['rich_weight']
            S = SHADOW[idx]
            for direction in range(6):
                sun_dir = (TIME+direction)%6
                s = S[sun_dir]
                dist_weight = 1
                for distance in range(3):
                    s_idx = s[distance]
                    if s_idx != -1:
                        m = MAP[s_idx]
                        if 'tree' in m:
                            total_loss += (t_weight[m['tree']['size']]*dist_weight*dir_weight*rich_weight[m['rich']])
                    else:
                        break
                    dist_weight *= PARAM['dist_weight']
                dir_weight *= PARAM['dir_weight']
            return total_loss

        MAP = status['MAP']
        DAY = status['DAY'] 
        TIME = status['TIME'] 
        NUTRIENTS = status['NUTRIENTS'] 
        SUN = status['SUN'] 
        SCORE = status['SCORE'] 
        OPP_SUN = status['OPP_SUN'] 
        OPP_SCORE = status['OPP_SCORE'] 
        OPP_WAITING = status['OPP_WAITING'] 
        N_TREES = status['N_TREES'] 
        TREE = status['TREE'] 
        MY_TREE = status['MY_TREE'] 
        OP_TREE = status['OP_TREE'] 
        P_MOVE = status['P_MOVE'] 
        P_MOVES = status['P_MOVES'] 

        for t in MY_TREE:
            t['mine'] = True
            MAP[t['idx']]['tree'] = t
        for t in OP_TREE:
            t['mine'] = False
            MAP[t['idx']]['tree'] = t
        

        ################ Main Code Start ####################
        TREE_POWER0 = sum([M['size'] for M in MY_TREE])
        TREE_POWER1 = sum([M['size'] for M in OP_TREE])
        # print("TREE POWER:", TREE_POWER0, TREE_POWER1, file=sys.stderr, flush=True)
        N_TREE = [0,0,0,0]
        for t in MY_TREE:
            N_TREE[t['size']] += 1

        CMD =[[],[],[],[],[]]
        SEED_LIST = set()
        for p in P_MOVES:
            ps = p.split()
            if 'SEED' in ps:
                p = {'from':int(ps[1]), 'to':int(ps[2])}
                size = sizeOf(MY_TREE, p['from'])
                SEED_LIST.add(p['to'])
                CMD[0].append(p)
            elif 'GROW' in ps:
                idx = int(ps[1])
                size = sizeOf(MY_TREE, idx)
                CMD[size+1].append(idx)
            elif 'COMPLETE' in ps:
                CMD[4].append(int(ps[1]))
        
        CMD[0].sort(key=lambda x:x['to'])
        CMD[1].sort()
        CMD[2].sort()
        CMD[3].sort()
        CMD[4].sort()

        PARAM = self.PARAM
        #N Tree Weight
        weight = [0, 0, 0, 0, 0, 10]
        weight[4] = N_TREE[3] * 10
        weight[3] = ((PARAM['N3TREE']-N_TREE[3])**PARAM['P3TREE']) * 17 if N_TREE[3] < PARAM['N3TREE'] else 0.1
        weight[2] = ((PARAM['N2TREE']-N_TREE[2])**PARAM['P2TREE']) * 15 if N_TREE[2] < PARAM['N2TREE'] else 0.1
        weight[1] = ((PARAM['N1TREE']-N_TREE[1])**PARAM['P1TREE']) * 12 if N_TREE[1] < PARAM['N1TREE'] else 0.1
        weight[0] = ((PARAM['N0TREE']-N_TREE[0])**PARAM['P0TREE']) * 10 if N_TREE[0] < PARAM['N0TREE'] else 0.1
        #Time Weight
        weight[4] = weight[4] * (1+DAY/PARAM['D4_SUB'])
        weight[3] = weight[3] * (1-((DAY-PARAM['N3_DAY'])/DAY)**PARAM['P3_DAY']) if DAY > PARAM['N3_DAY'] else weight[3]
        weight[2] = weight[2] * (1-((DAY-PARAM['N2_DAY'])/DAY)**PARAM['P2_DAY']) if DAY > PARAM['N2_DAY'] else weight[2]
        weight[1] = weight[1] * (1-((DAY-PARAM['N1_DAY'])/DAY)**PARAM['P1_DAY']) if DAY > PARAM['N1_DAY'] else weight[1]
        weight[0] = weight[0] * (1-((DAY-PARAM['N0_DAY'])/DAY)**PARAM['P0_DAY']) if DAY > PARAM['N0_DAY'] else weight[0]
        #Time Weight2
        weight[4] = weight[4]*10000 if DAY == 23 else weight[4]
        weight[3] = 0 if DAY > 22 else weight[3]
        weight[2] = 0 if DAY > 21 else weight[2]
        weight[1] = 0 if DAY > 20 else weight[1]
        weight[0] = 0 if DAY > 19 else weight[0]

        weight[5] = weight[5]/SUN*PARAM['D5'] if SUN > 10 else weight[5]

        weight[0] = 0 if DAY == 0  else weight[0]
        weight[4] = 0 if DAY <= 12 else weight[4]

        #length Weight
        for i in range(5):
            weight[i] = weight[i] if len(CMD[i]) != 0 else 0

        total_weight = sum(weight)
        for i, w in enumerate(weight):
            weight[i] = w/total_weight
        for i, w in enumerate(weight[1:]):
            weight[i+1] = weight[i] + weight[i+1]
        
        #pprint(weight)

        r = random.random()
        if r < weight[0]:
            # Find minimum loss sed
            min_idx  = -1
            min_loss = 10000
            for idx in SEED_LIST:
                loss = shadowingSeedPri(idx, DAY, MAP, PARAM['SEED'])
                if loss < min_loss:
                    min_loss = loss
                    min_idx = idx
            new_seed_cmd = []
            for s_cmd in CMD[0]:
                if s_cmd['to'] == min_idx:
                    new_seed_cmd.append(s_cmd)
            CMD[0] = new_seed_cmd
            cmd = "SEED %d %d" % (CMD[0][0]['from'], CMD[0][0]['to'])
        elif r < weight[1]:
            cmd = "GROW %d" % (CMD[1][0])
        elif r < weight[2]:
            cmd = "GROW %d" % (CMD[2][0])
        elif r < weight[3]:
            cmd = "GROW %d" % (CMD[3][0])
        elif r < weight[4]:
            # Find minimum loss sed
            min_idx  = -1
            min_loss = 10000
            for idx in CMD[4]:
                loss = shadowingCompletePri(idx, DAY, MAP, PARAM['COMPLETE'])
                if loss < min_loss:
                    min_loss = loss
                    min_idx = idx
            # d = random.randint(0, len(CMD[4])-1)
            # cmd = "COMPLETE %d" % CMD[4][d]
            cmd = "COMPLETE %d" % min_idx
        else:
            cmd = "WAIT"
        
        # print(cmd, cmd)
        return cmd
        ################ Main Code End   ####################