# tetris.py

import pygame, random, time
from pygame.locals import *
from constants import *
from utils import *

def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BIGFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 100)
    pygame.display.set_caption('Tetromino_Shenzhen First Polytechnic School 2303')

    DISPLAYSURF.fill(BGCOLOR)
    showTextScreen('Tetris',DISPLAYSURF, BIGFONT, BASICFONT, FPSCLOCK) # 显示开始界面
    while True: # 游戏主循环
        runGame(DISPLAYSURF, FPSCLOCK, BASICFONT, BIGFONT)
        showTextScreen('Game Over', DISPLAYSURF, BIGFONT, BASICFONT, FPSCLOCK) # 显示游戏结束界面

def runGame(DISPLAYSURF, FPSCLOCK, BASICFONT, BIGFONT):
    """运行游戏主循环"""
    board = getBlankBoard()
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()
    movingDown = False  # 是否按住向下键
    movingLeft = False  # 是否按住向左键
    movingRight = False  # 是否按住向右键
    score = 0
    level, fallFreq = calculateLevelAndFallFreq(score)
    fallingPiece = getNewPiece()  # 获取当前下落的方块
    nextPiece = getNewPiece()  # 获取下一个将要出现的方

    while True:# 游戏循环
        if fallingPiece == None:
            fallingPiece = nextPiece
            nextPiece = getNewPiece()
            lastFallTime = time.time() # 重置下落时间

            if not isValidPosition(board, fallingPiece):
                return # 无法放置新方块，游戏结束

        checkForQuit()
        for event in pygame.event.get():# 事件处理
            if event.type == KEYUP:
                if event.key == K_p:
                    DISPLAYSURF.fill(BGCOLOR)
                    showTextScreen('Paused', DISPLAYSURF, BIGFONT, BASICFONT, FPSCLOCK)
                    lastFallTime = time.time()
                    lastMoveDownTime = time.time()
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_LEFT:
                    movingLeft = False
                elif event.key == K_RIGHT:
                    movingRight = False
                elif event.key == K_DOWN:
                    movingDown = False

            elif event.type == KEYDOWN:
                if event.key == K_LEFT and isValidPosition(board, fallingPiece, adjX=-1):
                    fallingPiece['x'] -= 1
                    movingLeft = True
                    movingRight = False
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_RIGHT and isValidPosition(board, fallingPiece, adjX=1):
                    fallingPiece['x'] += 1
                    movingRight = True
                    movingLeft = False
                    lastMoveSidewaysTime = time.time()
                elif event.key == K_UP:
                    fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']])
                    if not isValidPosition(board, fallingPiece):
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']])
                elif event.key == K_DOWN:
                    movingDown = True
                    if isValidPosition(board, fallingPiece, adjY=1):
                        fallingPiece['y'] += 1
                    lastMoveDownTime = time.time()
                elif event.key == K_SPACE:
                    movingDown = False
                    movingLeft = False
                    movingRight = False
                    for i in range(1, BOARDHEIGHT):
                        if not isValidPosition(board, fallingPiece, adjY=i):
                            break
                    fallingPiece['y'] += i - 1

        if (movingLeft or movingRight) and time.time() - lastMoveSidewaysTime > MOVESIDEWAYSFREQ:
            if movingLeft and isValidPosition(board, fallingPiece, adjX=-1):
                fallingPiece['x'] -= 1
            elif movingRight and isValidPosition(board, fallingPiece, adjX=1):
                fallingPiece['x'] += 1
            lastMoveSidewaysTime = time.time()

        if movingDown and time.time() - lastMoveDownTime > MOVEDOWNFREQ and isValidPosition(board, fallingPiece, adjY=1):
            fallingPiece['y'] += 1
            lastMoveDownTime = time.time()

        if time.time() - lastFallTime > fallFreq:
            if not isValidPosition(board, fallingPiece, adjY=1):
                addToBoard(board, fallingPiece)
                score += removeCompleteLines(board)
                level, fallFreq = calculateLevelAndFallFreq(score)
                fallingPiece = None
            else:
                fallingPiece['y'] += 1
                lastFallTime = time.time()

        DISPLAYSURF.fill(BGCOLOR)
        drawBoard(DISPLAYSURF, board)
        drawStatus(DISPLAYSURF, score, level, BASICFONT)
        drawNextPiece(DISPLAYSURF, nextPiece, BASICFONT)
        if fallingPiece != None:
            drawPiece(DISPLAYSURF, fallingPiece)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def addToBoard(board, piece):
    """将方块添加到游戏板上。"""
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK:
                board[x + piece['x']][y + piece['y']] = piece['color']

