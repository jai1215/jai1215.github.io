import sys
import time
import numpy as np

start = time.time()
def logging_time(original_fn):
    def wrapper_fn(*args, **kwargs):
        start_time = time.time()
        result = original_fn(*args, **kwargs)
        end_time = time.time()
        print("WorkingTime[{}]: {} sec".format(original_fn.__name__, end_time-start_time))
        return result
    return wrapper_fn


def printBoard(board):
    print(file=sys.stderr, flush=True)
    print('====='*5, file=sys.stderr, flush=True)
    print(file=sys.stderr, flush=True)
    
    for y, line in enumerate(board):
        print(f'{y:2d} | ', end='', file=sys.stderr, flush=True)
        for x in line:
            if x == 0:
                print('. ', end='', file=sys.stderr, flush=True)
            elif x == 1:
                print('# ', end='', file=sys.stderr, flush=True)
            elif x == -1:
                print('- ', end='', file=sys.stderr, flush=True)
            else:
                print(f'?{x}', end='', file=sys.stderr, flush=True)

        print('', file=sys.stderr, flush=True)
        
def checkSkip(skipX, skipY, board):
    width = len(board[0])
    height = len(board)
    for x in range(width):
        skip = True
        if not skipX[x]:
            for y in range(height):
                if board[y][x] == 0:
                    skip = False
                    break
        skipX[x] = skip
    for y in range(height):
        skip = True
        if not skipY[y]:
            for x in range(width):
                if board[y][x] == 0:
                    skip = False
                    break
        skipY[y] = skip
            
def makeSol(board):
    width = len(board[0])
    height = len(board)
    sol = []
    for i in range(width):
        subSol = []
        cnt = 0
        for j in range(height):
            if board[j][i] == 0:
                return False, []
            elif board[j][i] == 1:
                if cnt != 0:
                    subSol.append(cnt)
                cnt = 0
            else:
                cnt += 1
        if cnt != 0:
            subSol.append(cnt)
        if len(subSol) == 0:
            subSol = [0]
        sol.append(subSol)
    for i in range(height):
        subSol = []
        cnt = 0
        for j in range(width):
            if board[i][j] == 0:
                return False, []
            elif board[i][j] == 1:
                if cnt != 0:
                    subSol.append(cnt)
                cnt = 0
            else:
                cnt += 1
        if cnt != 0:
            subSol.append(cnt)
        if len(subSol) == 0:
            subSol = [0]
        sol.append(subSol)
    return True, sol

def checkRng(xHints, yHints, board, rngX, rngY, uptX, uptY):
    for x, rng in enumerate(rngX):
        newRngStart = rng[0]
        newRngEnd   = rng[1]
        toggle = 0
        for i in range(rng[0], rng[1]):
            if(board[i][x] == 0):
                break
            elif board[i][x] == -1:
                newRngStart += (toggle+1)
                if toggle > 0:
                    del xHints[x][0]
                toggle = 0
            elif board[i][x] == 1:
                toggle += 1
        toggle = 0
        for i in range(rng[1]-1, newRngStart-1, -1):
            if(board[i][x] == 0):
                break
            elif board[i][x] == -1:
                newRngEnd -= (toggle+1)
                if toggle > 0:
                    del xHints[x][-1]
                toggle = 0
            elif board[i][x] == 1:
                toggle += 1
        if len(xHints[x]) == 0:
            for i in range(newRngStart, newRngEnd):
                if board[i][x] == 0:
                    board[i][x] = -1
                    uptY[i] = True
                
        if newRngStart >= newRngEnd:
            rngX[x] = (0, 0)
        else:
            rngX[x] = (newRngStart, newRngEnd)
    
    for y, rng in enumerate(rngY):
        newRngStart = rng[0]
        newRngEnd   = rng[1]
        toggle = 0
        for i in range(rng[0], rng[1]):
            if(board[y][i] == 0):
                break
            elif board[y][i] == -1:
                newRngStart += (toggle+1)
                if toggle > 0:
                    del yHints[y][0]
                toggle = 0
            elif board[y][i] == 1:
                toggle += 1
        toggle = 0
        for i in range(rng[1]-1, newRngStart-1, -1):
            if(board[y][i] == 0):
                break
            elif board[y][i] == -1:
                newRngEnd -= (toggle+1)
                if toggle > 0:
                    del yHints[y][-1]
                toggle = 0
            elif board[y][i] == 1:
                toggle += 1
        if len(yHints[y]) == 0:
            for i in range(newRngStart, newRngEnd):
                if board[y][i] == 0:
                    board[y][i] = -1
                    uptX[i] = True
        if newRngStart >= newRngEnd:
            rngY[y] = (0, 0)
        else:
            rngY[y] = (newRngStart, newRngEnd)
                    

def checkLine(board, hint, pos, rng, uptX, uptY):
    checkY = True if pos[1] == -1 else False
    # lenBoard = len(board) if checkY else len(board[0])
    lenBoard = rng[1]-rng[0]
    # print("hint", hint, pos, rng, file=sys.stderr, flush=True)
    start = time.time()
    
    checkBoard = [0] * lenBoard
    if checkY:
        for i in range(lenBoard):
            checkBoard[i] = board[i+rng[0]][pos[0]]
    else:
        for i in range(lenBoard):
            checkBoard[i] = board[pos[1]][i+rng[0]]
    guide = runCombination(hint, lenBoard, checkBoard)
    
    if checkY:
        for i in range(lenBoard):
            if guide[i] == -1 or guide[i] == 1:
                if guide[i] != board[i+rng[0]][pos[0]]:
                    board[i+rng[0]][pos[0]] = guide[i]
                    uptY[i+rng[0]] = True
        uptX[pos[0]] = False
                    
    else:
        for i in range(lenBoard):
            if guide[i] == -1 or guide[i] == 1:
                if guide[i] != board[pos[1]][i+rng[0]]:
                    board[pos[1]][i+rng[0]] = guide[i]
                    uptX[i+rng[0]] = True
        uptY[pos[1]] = False
    end = time.time()
    # print(f'{end-start:3.4f}',guide, file=sys.stderr, flush=True)
    
    
def getRange(item, width):
    start = [0]
    for i, j in enumerate(item[:-1]):
        start.append(start[i]+j+1)

    shift = width-item[-1]-start[-1]
    end   = [s+shift for s in start]
    return start, end

# @profile
def incIdx(start, end, idx, item):
    while True:
        idx[-1] += 1
        lidx = len(idx)-1
        for i in range(lidx, -1, -1):
            if idx[i] > end[i]:
                idx[i] = start[i]
                if i == 0:
                    return False
                idx[i-1] += 1
                
        checkCollision = False
        for i, mask in enumerate(item[:-1]):
            if idx[i]+mask >= idx[i+1]:
                checkCollision = True
                break
        if not checkCollision:
            return True

def runCombination(item, width, checkBoard):
    start, end = getRange(item, width)
    idx = list(start)
    cnt = 0
    guide = [0] * width
    while True:
        subTry = [0] * width
        for i, sub in enumerate(item):
            for s in range(sub):
                subTry[idx[i]+s] = 1
        
        #Check given board        
        skip = False
        for i in range(width):
            if checkBoard[i] == -1 and subTry[i] == 1:
                skip = True
                break
            if checkBoard[i] == 1 and subTry[i] == 0:
                skip = True
                break
        
        #Add to Total board when not skip
        if not skip:
            cnt += 1
            for i in range(width):
                guide[i] += subTry[i]
            # print(idx, subTry, guide, file=sys.stderr, flush=True)
                
        #Increase index
        if not incIdx(start, end, idx, item):
            break
    for i in range(width):
        if guide[i] == 0:
            guide[i] = -1
        elif guide[i] == cnt:
            guide[i] = 1
        else:
            guide[i] = 0
    return guide

# width = 20
# checkBoard = [0, 0, 0, 0, -1, -1, 0, 1, 1, 1, 0, -1, -1, 1,1,1, -1, 1, -1, 1]
# item = [2, 3, 3, 1, 1]
# runCombination(item, width, checkBoard)
# exit(1)
    
width, height = [int(i) for i in input().split()]

board = [[0 for _ in range(width)] for _ in range(height)]
yHints = []
xHints = []
for i in range(width):
    xHints.append([int(i) for i in input().split()])
for i in range(height):
    yHints.append([int(i) for i in input().split()])

print(f"{width}x{height}", file=sys.stderr, flush=True)
print(f"{xHints}", file=sys.stderr, flush=True)
print(f"{yHints}", file=sys.stderr, flush=True)

sol = []
# for i in range(5):
skipLineY = [False]*height
skipLineX = [False]*width
updatedLineY = [True]*height
updatedLineX = [True]*width

def cntNonZero(hints, width):
    ret = []
    for h in hints:
        powerN = max(h)+sum(h) + len(h) - 1 - width
        ret.append(powerN)
    return ret

def cntZero(board, height, width):
    retX, retY = [0]*width, [0]*height
    for y in range(height):
        for x in range(width):
            if board[y][x] == 0 :
                retX[x] += 1
                retY[y] += 1
    return np.array(retX), np.array(retY)

nonZeroX = np.array(cntNonZero(xHints, height))
nonZeroY = np.array(cntNonZero(yHints, width))
rngX = [(0, height) for i in range(width)]
rngY = [(0, width) for i in range(height)]

threshold = 0.2
cnt = 0
while True:
    cntZeroX, cntZeroY = cntZero(board, height, width)
    curZerosX = nonZeroX + cntZeroX
    curZerosY = nonZeroY + cntZeroY
    curZerosX = curZerosX.argsort()[::-1]
    curZerosY = curZerosY.argsort()[::-1]
    for i in range(int(height*threshold)):
    # for i in range(int(height)):
        i = curZerosY[i]
        if not skipLineY[i] and updatedLineY[i] and len(yHints[i]) > 0:
            checkLine(board, yHints[i], (-1, i), rngY[i], updatedLineX, updatedLineY)
    for i in range(int(width*threshold)):
    # for i in range(int(width)):
        i = curZerosX[i]
        if not skipLineX[i] and updatedLineX[i]  and len(xHints[i]) > 0:
            checkLine(board, xHints[i], (i, -1), rngX[i], updatedLineX, updatedLineY)
    printBoard(board)
    checkSkip(skipLineX, skipLineY, board)
    checkRng(xHints, yHints, board, rngX, rngY, updatedLineX, updatedLineY)
    check, sol = makeSol(board)
    threshold = min(1, threshold+0.1)
        
    if check:
        break
    cnt += 1
    # if cnt == 10:
    #     exit(1)
        
for s in sol:
    print(" ".join([str(ss) for ss in s]))
    
end = time.time()

print(f"{end - start:.5f} sec", file=sys.stderr, flush=True)

