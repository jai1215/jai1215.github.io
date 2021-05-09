import sys
import math
import random

class PlayerClass1():
    def __init__(self, DEBUG):
        self.DEBUG = DEBUG
        pass

    def run(self, status):
        def pprint(s, info=""):
            if self.DEBUG:
                print(info, s, file=sys.stderr, flush=True)

        def sizeOf(TREE, idx):
            for t in TREE:
                if t['idx'] == idx:
                    return t['size']
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

        ################ Main Code Start ####################
        TREE_POWER0 = sum([M['size'] for M in MY_TREE])
        TREE_POWER1 = sum([M['size'] for M in OP_TREE])
        # print("TREE POWER:", TREE_POWER0, TREE_POWER1, file=sys.stderr, flush=True)

        SEED = []
        GROW = []
        COMPLETE = []
        for p in P_MOVES:
            ps = p.split()
            if 'SEED' in ps:
                p = {'from':int(ps[1]), 'to':int(ps[2])}
                SEED.append(p)
            elif 'GROW' in ps:
                idx = int(ps[1])
                size = sizeOf(MY_TREE, idx)
                GROW.append({'idx':idx, 'size':size})

            elif 'COMPLETE' in ps:
                COMPLETE.append(p)
        SEED.sort(key=lambda x:x['to'])
        if DAY < 16:
            GROW.sort(key=lambda x:x['size'], reverse=True)
            GROW.sort(key=lambda x:x['idx'])
        else:
            GROW.sort(key=lambda x:x['idx'])
            GROW.sort(key=lambda x:x['size'], reverse=True)

        pprint(SEED, info="SEED")
        pprint(GROW, info="GROW")
        #pprint(COMPLETE)

        #      seed, grow, com, wait
        weight = [0, 5, 0, 2]
        if DAY < 1:
            weight = [0, 2, 0, 1]
        elif DAY < 3:
            weight = [3, 12, 0, 1]
        elif DAY < 6:
            weight = [3, 8, 0, 1]
        # elif DAY < 12:
        #     weight = [1, 5, 1, 1]
        elif DAY < 16:
            weight = [1, 7, 0, 1]
        elif DAY < 22:
            weight = [0, 3, 6, 1]
        else:
            weight = [0, 3, 12, 1]

        weight[0] = weight[0] if len(SEED)     != 0 else 0
        weight[1] = weight[1] if len(GROW)     != 0 else 0
        weight[2] = weight[2] if len(COMPLETE) != 0 else 0
        weight[3] = weight[3]/SUN if SUN != 0 else 1

        total_weight = sum(weight)
        for i, w in enumerate(weight):
            weight[i] = w/total_weight
        for i, w in enumerate(weight[1:]):
            weight[i+1] = weight[i] + weight[i+1]
        
        #pprint(weight)

        r = random.random()
        if r < weight[0]:
            # d = random.randint(0, len(SEED)-1)
            cmd = "SEED %d %d" % (SEED[0]['from'], SEED[0]['to'])
        elif r < weight[1]:
            # d = random.randint(0, len(GROW)-1)
            cmd = "GROW %d" % (GROW[0]['idx'])
        elif r < weight[2]:
            d = random.randint(0, len(COMPLETE)-1)
            cmd = COMPLETE[d]
        else:
            cmd = "WAIT"
        # print(cmd, cmd)
        return cmd
        ################ Main Code End   ####################