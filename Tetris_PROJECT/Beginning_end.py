#其他PY模块
import Game_Main as GM
import Def_SHAPE_TEMPLATE as DST
import Primary_Function as PF
from Main import *
#game 基础模块
import random, time, pygame, sys
from pygame.locals import *
import Tetris_PROJECT.Beginning_end as Beginning_end 



def run_game():
    """设置游戏开始时的变量"""

    #游戏板当前状态
    board = getBlankBoard()
    
    #记录上帧[X][-Y]移动与下落的时间
    lastMoveDownTime = time.time()
    lastMoveSidewaysTime = time.time()
    lastFallTime = time.time()

    #记录是否在相应方向移动的布尔变量
    movingDown = False
    movingLeft = False
    movingRight = False

    #当前得分
    score = 0

    level, fallFreq = calculateLevelAndFallFreq(score)

    fallingPiece = getNewPiece()
    nextPiece = getNewPiece()

    while True:
        if fallingPiece == None:
            fallingPiece = nextPiece
            lastFallTime = time.time()

            if not isValidPosition(board, fallingPiece):
                return
            
        checkForQuit()
        for event in pygame.event.get(): # event handling loop 
                if event.type == KEYUP: 
                    if (event.key == K_p): 
                        # Pausing the game 
                        DISPLAYSURF.fill(BGCOLOR) 
                        #pygame.mixer.music.stop() 
                        showTextScreen('Paused') # pause until a key press 
                        #pygame.mixer.music.play(-1, 0.0) 
                        lastFallTime = time.time() 
                        lastMoveDownTime = time.time() 
                        lastMoveSidewaysTime = time.time() 
                    elif (event.key == K_LEFT or event.key == K_a): 
                        movingLeft = False
                    elif (event.key == K_RIGHT or event.key == K_d): 
                        movingRight = False
                    elif (event.key == K_DOWN or event.key == K_s): 
                        movingDown = False
        
                elif event.type == KEYDOWN: 
                    # moving the piece sideways 
                    if (event.key == K_LEFT or event.key == K_a) and isValidPosition(board, fallingPiece, adjX=-1): 
                        fallingPiece['x'] -= 1
                        movingLeft = True
                        movingRight = False
                        lastMoveSidewaysTime = time.time() 
        
                    elif (event.key == K_RIGHT or event.key == K_d) and isValidPosition(board, fallingPiece, adjX=1): 
                        fallingPiece['x'] += 1
                        movingRight = True
                        movingLeft = False
                        lastMoveSidewaysTime = time.time() 
        
                    # rotating the piece (if there is room to rotate) 
                    elif (event.key == K_UP or event.key == K_w): 
                        fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']]) 
                        if not isValidPosition(board, fallingPiece): 
                            fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']]) 
                    elif (event.key == K_q): # rotate the other direction 
                        fallingPiece['rotation'] = (fallingPiece['rotation'] - 1) % len(PIECES[fallingPiece['shape']]) 
                        if not isValidPosition(board, fallingPiece): 
                            fallingPiece['rotation'] = (fallingPiece['rotation'] + 1) % len(PIECES[fallingPiece['shape']]) 
        
                    # making the piece fall faster with the down key 
                    elif (event.key == K_DOWN or event.key == K_s): 
                        movingDown = True
                        if isValidPosition(board, fallingPiece, adjY=1): 
                            fallingPiece['y'] += 1
                        lastMoveDownTime = time.time() 
        
                    # move the current piece all the way down 
                    elif event.key == K_SPACE: 
                        movingDown = False
                        movingLeft = False
                        movingRight = False
                        for i in range(1, BOARD_HEIGHT): 
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
            
        # let the piece fall if it is time to fall 
        if time.time() - lastFallTime > fallFreq: 
            # see if the piece has landed 
            if not isValidPosition(board, fallingPiece, adjY=1): 
                    # falling piece has landed, set it on the board 
                addToBoard(board, fallingPiece) 
                score += removeCompleteLines(board) 
                level, fallFreq = calculateLevelAndFallFreq(score) 
                fallingPiece = None
            else: 
                # piece did not land, just move the piece down 
                fallingPiece['y'] += 1
                lastFallTime = time.time() 
            
                # drawing everything on the screen 
        DISPLAYSURF.fill(BGCOLOR) 
        drawBoard(board) 
        drawStatus(score, level) 
        drawNextPiece(nextPiece) 
        if fallingPiece != None: 
            drawPiece(fallingPiece) 
            
        pygame.display.update() 
        FPSCLOCK.tick(FPS)        

        

    
