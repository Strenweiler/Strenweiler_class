
import random, time, pygame, sys
from pygame.locals import *
from Tetris_PROJECT.Beginning_end import *
from Game_Main import *
from Def_SHAPE_TEMPLATE import *
from Beginning_end import *
from Primary_Function import *


def makeTextObjs(text, font, color): 
	surf = font.render(text, True, color) 
	return surf, surf.get_rect() 


def terminate(): 
	pygame.quit() 
	sys.exit() 


def checkForKeyPress(): 
	# Go through event queue looking for a KEYUP event. 
	# Grab KEYDOWN events to remove them from the event queue. 
	checkForQuit() 
	
	for event in pygame.event.get([KEYDOWN, KEYUP]): 
		if event.type != KEYDOWN: 
			continue
		return event.key 
	return None


def showTextScreen(text): 
	# This function displays large text in the 
	# center of the screen until a key is pressed. 
	# Draw the text drop shadow 
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR) 
	titleRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2)) 
	DISPLAYSURF.blit(titleSurf, titleRect) 
	
	# Draw the text 
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR) 
	titleRect.center = (int(WINDOW_WIDTH / 2) - 3, int(WINDOW_HEIGHT / 2) - 3) 
	DISPLAYSURF.blit(titleSurf, titleRect) 
	
	# Draw the additional "Press a key to play." text. 
	pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR) 
	pressKeyRect.center = (int(WINDOW_WIDTH / 2), int(WINDOW_HEIGHT / 2) + 100) 
	DISPLAYSURF.blit(pressKeySurf, pressKeyRect) 
	
	while checkForKeyPress() == None: 
		pygame.display.update() 
		FPSCLOCK.tick() 


def checkForQuit(): 
	for event in pygame.event.get(QUIT): # get all the QUIT events 
		terminate() # terminate if any QUIT events are present 
	for event in pygame.event.get(KEYUP): # get all the KEYUP events 
		if event.key == K_ESCAPE: 
			terminate() # terminate if the KEYUP event was for the Esc key 
		pygame.event.post(event) # put the other KEYUP event objects back 


def calculateLevelAndFallFreq(score): 
	# Based on the score, return the level the player is on and 
	# how many seconds pass until a falling piece falls one space. 
	level = int(score / 10) + 1
	fallFreq = 0.27 - (level * 0.02) 
	return level, fallFreq 

def getNewPiece(): 
	# return a random new piece in a random rotation and color 
	shape = random.choice(list(PIECES.keys())) 
	newPiece = {'shape': shape, 
				'rotation': random.randint(0, len(PIECES[shape]) - 1), 
				'x': int(BOARD_WIDTH / 2) - int(TEMPLATEWIDTH / 2), 
				'y': -2, # start it above the board (i.e. less than 0) 
				'color': random.randint(0, len(COLORS)-1)} 
	return newPiece 


def addToBoard(board, piece): 
	# fill in the board based on piece's location, shape, and rotation 
	for x in range(TEMPLATEWIDTH): 
		for y in range(TEMPLATEHEIGHT): 
			if PIECES[piece['shape']][piece['rotation']][y][x] != BLANK: 
				board[x + piece['x']][y + piece['y']] = piece['color'] 


def getBlankBoard(): 
	# create and return a new blank board data structure 
	board = [] 
	for i in range(BOARDWIDTH): 
		board.append([BLANK] * BOARDHEIGHT) 
	return board 


def isOnBoard(x, y): 
	return x >= 0 and x < BOARDWIDTH and y < BOARDHEIGHT 


def isValidPosition(board, piece, adjX=0, adjY=0): 
	# Return True if the piece is within the board and not colliding 
	for x in range(TEMPLATEWIDTH): 
		for y in range(TEMPLATEHEIGHT): 
			isAboveBoard = y + piece['y'] + adjY < 0
			if isAboveBoard or PIECES[piece['shape']][piece['rotation']][y][x] == BLANK: 
				continue
			if not isOnBoard(x + piece['x'] + adjX, y + piece['y'] + adjY): 
				return False
			if board[x + piece['x'] + adjX][y + piece['y'] + adjY] != BLANK: 
				return False
	return True

def isCompleteLine(board, y): 
	# Return True if the line filled with boxes with no gaps. 
	for x in range(BOARDWIDTH): 
		if board[x][y] == BLANK: 
			return False
	return True


def removeCompleteLines(board): 
	# Remove any completed lines on the board, move everything above them down, and return the number of complete lines. 
	numLinesRemoved = 0
	y = BOARDHEIGHT - 1 # start y at the bottom of the board 
	while y >= 0: 
		if isCompleteLine(board, y): 
			# Remove the line and pull boxes down by one line. 
			for pullDownY in range(y, 0, -1): 
				for x in range(BOARDWIDTH): 
					board[x][pullDownY] = board[x][pullDownY-1] 
			# Set very top line to blank. 
			for x in range(BOARDWIDTH): 
				board[x][0] = BLANK 
			numLinesRemoved += 1
			# Note on the next iteration of the loop, y is the same. 
			# This is so that if the line that was pulled down is also 
			# complete, it will be removed. 
		else: 
			y -= 1 # move on to check next row up 
	return numLinesRemoved 


def convertToPixelCoords(boxx, boxy): 
	# Convert the given xy coordinates of the board to xy 
	# coordinates of the location on the screen. 
	return (XMARGIN + (boxx * BOXSIZE)), (TOPMARGIN + (boxy * BOXSIZE)) 


def drawBox(boxx, boxy, color, pixelx=None, pixely=None): 
	# draw a single box (each tetromino piece has four boxes) 
	# at xy coordinates on the board. Or, if pixelx & pixely 
	# are specified, draw to the pixel coordinates stored in 
	# pixelx & pixely (this is used for the "Next" piece). 
	if color == BLANK: 
		return
	if pixelx == None and pixely == None: 
		pixelx, pixely = convertToPixelCoords(boxx, boxy) 
	pygame.draw.rect(DISPLAYSURF, COLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 1, BOXSIZE - 1)) 
	pygame.draw.rect(DISPLAYSURF, LIGHTCOLORS[color], (pixelx + 1, pixely + 1, BOXSIZE - 4, BOXSIZE - 4)) 


def drawBoard(board): 
	# draw the border around the board 
	pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (XMARGIN - 3, TOPMARGIN - 7, (BOARDWIDTH * BOXSIZE) + 8, (BOARDHEIGHT * BOXSIZE) + 8), 5) 
	
	# fill the background of the board 
	pygame.draw.rect(DISPLAYSURF, BGCOLOR, (XMARGIN, TOPMARGIN, BOXSIZE * BOARDWIDTH, BOXSIZE * BOARDHEIGHT)) 
	# draw the individual boxes on the board 
	for x in range(BOARDWIDTH): 
		for y in range(BOARDHEIGHT): 
			drawBox(x, y, board[x][y]) 


def drawStatus(score, level): 
	# draw the score text 
	scoreSurf = BASICFONT.render('Score: %s' % score, True, TEXTCOLOR) 
	scoreRect = scoreSurf.get_rect() 
	scoreRect.topleft = (WINDOWWIDTH - 150, 20) 
	DISPLAYSURF.blit(scoreSurf, scoreRect) 
	
	# draw the level text 
	levelSurf = BASICFONT.render('Level: %s' % level, True, TEXTCOLOR) 
	levelRect = levelSurf.get_rect() 
	levelRect.topleft = (WINDOWWIDTH - 150, 50) 
	DISPLAYSURF.blit(levelSurf, levelRect) 


def drawPiece(piece, pixelx=None, pixely=None): 
	shapeToDraw = PIECES[piece['shape']][piece['rotation']] 
	if pixelx == None and pixely == None: 
		# if pixelx & pixely hasn't been specified, use the location stored in the piece data structure 
		pixelx, pixely = convertToPixelCoords(piece['x'], piece['y']) 
	
	# draw each of the boxes that make up the piece 
	for x in range(TEMPLATEWIDTH): 
		for y in range(TEMPLATEHEIGHT): 
			if shapeToDraw[y][x] != BLANK: 
				drawBox(None, None, piece['color'], pixelx + (x * BOXSIZE), pixely + (y * BOXSIZE)) 


def drawNextPiece(piece): 
	# draw the "next" text 
	nextSurf = BASICFONT.render('Next:', True, TEXTCOLOR) 
	nextRect = nextSurf.get_rect() 
	nextRect.topleft = (WINDOWWIDTH - 120, 80) 
	DISPLAYSURF.blit(nextSurf, nextRect) 
	# draw the "next" piece 
	drawPiece(piece, pixelx=WINDOWWIDTH-120, pixely=100) 