# utils.py

import pygame, sys, random
from pygame.locals import *
from constants import *

def terminate():
    """终止游戏并退出"""
    pygame.quit()
    sys.exit()

def checkForQuit():
    """检查是否有退出事件并处理"""
    for event in pygame.event.get(QUIT):  # 获取所有退出事件
        terminate()
    for event in pygame.event.get(KEYUP):  # 获取所有键盘释放事件
        if event.key == K_ESCAPE:  # 如果按下ESC键，退出游戏
            terminate()
        pygame.event.post(event)  # 否则将事件重新放回事件队列

def checkForKeyPress():
    """检查是否按下了任何键"""
    checkForQuit()
    for event in pygame.event.get([KEYDOWN, KEYUP]):  # 获取所有按键和释放事件
        if event.type == KEYDOWN:  # 如果是按键事件，继续等待
            continue
        return event.key  # 返回按下的键
    return None  # 如果没有按键，返回None

def makeTextObjs(text, font, color):
    """创建文本对象及其矩形区域"""
    surf = font.render(text, True, color)  # 渲染文本
    return surf, surf.get_rect()  # 返回文本表面及其矩形

def showTextScreen(text, DISPLAYSURF, BIGFONT, BASICFONT, FPSCLOCK):
    """显示包含给定文本的屏幕"""
    titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
    titleRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(titleSurf, titleRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Enter any KEY', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    pressKeySurf, pressKeyRect = makeTextObjs('Enter any KEY', BASICFONT, TEXTCOLOR)
    pressKeyRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 100)
    DISPLAYSURF.blit(pressKeySurf, pressKeyRect)

    while checkForKeyPress() == None:  # 等待按键
        pygame.display.update()
        FPSCLOCK.tick()
        
def calculateLevelAndFallFreq(score):
    """根据得分计算当前级别和方块下落频率"""
    level = int(score / 10) + 1  # 每10分增加一个级别
    fallFreq = 0.27 - (level * 0.02)  # 根据级别计算下落频率
    return level, fallFreq

def getNewPiece():
    """生成一个新的随机方块"""
    shape = random.choice(list(PIECES.keys()))  # 随机选择一个形状
    newPiece = {'shape': shape,
                'rotation': random.randint(0, len(PIECES[shape]) - 1),  # 随机选择一个旋转角度
                'x': int(BOARDWIDTH / 2) - int(TEMPLATEWIDTH / 2),  # 方块的初始水平位置
                'y': -2,  # 方块的初始垂直位置
                'color': random.randint(0, len(COLORS) - 1)}  # 随机选择一个颜色
    return newPiece

def getBlankBoard():
    """创建一个空白的游戏板"""
    board = []
    for i in range(BOARDWIDTH):
        board.append([BLANK] * BOARDHEIGHT)  # 初始化每一列
    return board

def isOnBoard(x, y):
    """检查给定坐标是否在游戏板范围内"""
    return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT

def isValidPosition(board, piece, adjX=0, adjY=0):
    """检查给定坐标是否在游戏板范围内"""
    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            isAboveBoard = y + piece['y'] + adjY < 0  # 检查方块是否在游戏板上方
            if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK:
                continue
            if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY):  # 检查是否超出左右边界
                return False
            if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK:  # 检查是否与已有方块重叠
                return False
    return True

def isCompleteLine(board, y):
    """检查某一行是否已满"""
    for x in range(BOARDWIDTH):
        if board[x][y] == BLANK:  # 如果有空白位置，该行未满
            return False
    return True  # 如果没有空白位置，该行已满

def removeCompleteLines(board):
    """移除已满的行并返回移除的行数"""
    numLinesRemoved = 0
    y = BOARDHEIGHT - 1
    while y >= 0:
        if isCompleteLine(board, y):  # 如果该行已满
            for pullDownY in range(y, 0, -1):  # 向下移动所有行
                for x in range(BOARDWIDTH):
                    board[x][pullDownY] = board[x][pullDownY - 1]
            for x in range(BOARDWIDTH):
                board[x][0] = BLANK  # 最顶上一行设为空白
            numLinesRemoved += 1  # 记录移除的行数
        else:
            y -= 1  # 检查上一行
    return numLinesRemoved

def convertToPixelCoords(boxx, boxy):
    """将游戏板上的坐标转换为像素坐标"""
    return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE))

def drawBox(DISPLAYSURF, boxx, boxy, color, pixelx=None, pixely=None):
    """在给定的像素坐标绘制一个方块"""
    if color == BLANK:  # 如果颜色为空白，不绘制
        return
    if pixelx == None and pixely == None:  # 如果未提供像素坐标，则转换坐标
        pixelx, pixely = convertToPixelCoords(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1))
    pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4))

def drawBoard(DISPLAYSURF, board):
    """绘制游戏板及其边框"""
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5)
    pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT))
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            drawBox(DISPLAYSURF, x, y, board[x][y])

def drawStatus(DISPLAYSURF, score, level, BASICFONT):
    """在屏幕上显示分数和级别"""
    """Draw the score and level status."""
    scoreSurf = BASICFONT.render(f'Score: {score}', True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 150, 20)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

    levelSurf = BASICFONT.render(f'Level: {level}', True, TEXTCOLOR)
    levelRect = levelSurf.get_rect()
    levelRect.topleft = (WINDOWWIDTH - 150, 50)
    DISPLAYSURF.blit(levelSurf, levelRect)

def drawPiece(DISPLAYSURF, piece, pixelx=None, pixely=None):
    """绘制方块"""
    shapeToDraw = PIECES[piece['shape']][piece['rotation']]
    if pixelx == None and pixely == None:
        pixelx, pixely = convertToPixelCoords(piece['x'], piece['y'])

    for x in range(TEMPLATEWIDTH):
        for y in range(TEMPLATEHEIGHT):
            if shapeToDraw[y][x] != BLANK:
                drawBox(DISPLAYSURF, None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE))

def drawNextPiece(DISPLAYSURF, piece, BASICFONT):
    """绘制下一个将要出现的方块"""
    nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR)
    nextRect = nextSurf.get_rect()
    nextRect.topleft = (WINDOWWIDTH - 120, 80)
    DISPLAYSURF.blit(nextSurf, nextRect)
    drawPiece(DISPLAYSURF, piece, pixelx=WINDOWWIDTH - 120, pixely=100)
