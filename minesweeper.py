########################################
#
#   Minesweeper
#   By: Maya Kundakci (mkundakc)
#
########################################
from cmu_graphics import *
import copy
import random 
import math
from PIL import Image
import csv

#class that stores variables for different game settings
class GameSettings:
    def __init__(self, difficulty):
        if difficulty == 'easy':
            self.rows = 9
            self.cols = 9
            self.width = 500
            self.height = 580
            self.boardWidth = 500
            self.boardHeight = 500
            self.mines = 10
            self.flags = 10
            self.revealSpeed = 5
    
        if difficulty == 'medium':
            self.rows = 16
            self.cols = 16
            self.width = 650
            self.height = 730
            self.boardWidth = 650
            self.boardHeight = 650
            self.mines = 40
            self.flags = 40
            self.revealSpeed = 10
        
        if difficulty == 'hard':
            self.rows = 16
            self.cols = 30
            self.width = 1200
            self.height = 720
            self.boardWidth = 1200
            self.boardHeight = 640
            self.mines = 99
            self.flags = 99
            self.difficulty = 'hard'
            self.revealSpeed = 100
        
        if difficulty == 'extreme':
            self.rows = 24
            self.cols = 32
            self.width = 960
            self.height = 800
            self.boardWidth = 960
            self.boardHeight = 720
            self.mines = 120
            self.flags = 120
            self.revealSpeed = 1500

        self.cellWidth = self.boardWidth / self.cols
        self.cellHeight = self.boardHeight / self.rows
        self.score = 0
        self.player = ''
        self.boardLeft = 0
        self.boardTop = 80
        
def onAppStart(app):
    easy = GameSettings('easy')
    medium = GameSettings('medium')
    hard = GameSettings('hard')
    extreme = GameSettings('extreme')
    app.flag = Image.open("flagg.png")
    app.flag = CMUImage(app.flag)
    app.mine = Image.open("mine.png")
    app.mine = CMUImage(app.mine)
    app.clock = Image.open("clock.png")
    app.clock = CMUImage(app.clock)
    app.exit = Image.open("exit.png")
    app.exit = CMUImage(app.exit)
    app.restart = Image.open("restart.png")
    app.restart = CMUImage(app.restart)
    app.wrong = Image.open("wrong.png")
    app.wrong = CMUImage(app.wrong)
    app.difficulty = None
    app.pink = Image.open("pink.png")
    app.pink = CMUImage(app.pink)
    app.myPink = Image.open("myPink.png")
    app.myPink = CMUImage(app.myPink)
    app.sakura = Image.open("sakura.png")
    app.sakura = CMUImage(app.sakura)
    app.trophy = Image.open("trophy.png")
    app.trophy = CMUImage(app.trophy)
    app.helpScreen = Image.open("helpscreen.png")
    app.helpScreen = CMUImage(app.helpScreen)
    app.width = 800
    app.height = 600
    app.originalColor = rgb(81, 125, 12)
    app.originalButtonColor = rgb(150, 214, 51)
    app.easyColor = rgb(81, 125, 12)
    app.mediumColor = rgb(81, 125, 12)
    app.hardColor = rgb(81, 125, 12)
    app.extremeColor = rgb(81, 125, 12)
    app.leaderboardColor = rgb(81, 125, 12)
    app.helpColor = rgb(81, 125, 12)
    app.hintColor = rgb(81, 125, 12)
    app.exitColor = None
    app.restartColor = rgb(81, 125, 12)
    app.restartButtonColor = rgb(150, 214, 51)
    app.exitButtonColor = rgb(150, 214, 51)
    app.saveButtonColor = rgb(150, 214, 51)
    app.originalLead = rgb(124, 169, 102)
    app.easyLead = rgb(124, 169, 102)
    app.mediumLead = rgb(124, 169, 102)
    app.hardLead = rgb(124, 169, 102)
    app.extremeLead = rgb(124, 169, 102)
    app.selectedLead = 'easy'
    app.easyScores = []
    app.mediumScores = []
    app.hardScores = []
    app.extremeScores = []
    app.leaderboardEasy = []
    app.leaderboardMedium = []
    app.leaderboardHard = []
    app.leaderboardExtreme = []
    app.onePlayer, app.oneScore = ('XXX', 'XXX')
    app.twoPlayer, app.twoScore = ('XXX', 'XXX')
    app.threePlayer, app.threeScore = ('XXX', 'XXX') 
    app.fourPlayer, app.fourScore = ('XXX', 'XXX')
    app.fivePlayer, app.fiveScore = ('XXX', 'XXX')
    app.sixPlayer, app.sixScore = ('XXX', 'XXX')
    app.sevenPlayer, app.sevenScore = ('XXX', 'XXX')
    app.eightPlayer, app.eightScore = ('XXX', 'XXX')


    
def newGame(app, difficulty):
    app.gameBoard = []
    app.neighbours = {}
    app.flagLocs = []
    app.wrongFlags = []
    app.revealedMines = []
    app.revealedTiles = set()
    app.firstMove = True
    app.gameOver = False
    app.win = False
    app.paused = False
    app.hint = False
    app.revealScore = False
    app.timer = 0
    app.hintTimer = 0
    app.stepsPerSecond = 1
    app.revealColor = 200
    app.timer = 0
    app.stepsPerSecond = 1
    app.flowerDim = 0
    app.difficulty = difficulty
    app.currSetting = GameSettings(f'{app.difficulty}')
    app.width = app.currSetting.width
    app.height = app.currSetting.height
    game_createBoard(app)
    game_placeMines(app)
    setActiveScreen('game')

def restartGame(app):
    setActiveScreen('start')
    newGame(app, app.difficulty)
    setActiveScreen('game')

def start_redrawAll(app):
    drawRect(0,0, app.width, app.height, fill = rgb(150, 214, 51))
    drawLabel("Minesweeper", 400, 140, bold = True, size = 50, 
              fill = rgb(58, 95, 11))
    drawRect(400, 250, 250, 75, fill = app.easyColor, align = 'center',
              opacity = 60, border = rgb(2, 48, 32), borderWidth = 3)
    drawLabel("Easy", 400, 250, bold = True, size = 40, 
              fill =  rgb(58, 95, 11))
    drawRect(400, 335, 250, 75, fill =app.mediumColor, align = 'center',
              opacity = 60, border = rgb(2, 48, 32), borderWidth = 3)
    drawLabel("Medium", 400, 335, bold = True, size = 40, 
              fill =  rgb(58, 95, 11))
    drawRect(400, 420, 250, 75, fill = app.hardColor, align = 'center',
              opacity = 60, border = rgb(2, 48, 32), borderWidth = 3)
    drawLabel("Hard", 400, 420, bold = True, size = 40, 
              fill =  rgb(58, 95, 11))
    drawRect(400, 505, 250, 75, fill = app.extremeColor, align = 'center',
              opacity = 60, border = rgb(2, 48, 32), borderWidth = 3)
    drawLabel("Extreme", 400, 505, bold = True, size = 40, 
              fill =  rgb(58, 95, 11))
    drawRect(700, 60, 120, 50, fill = app.helpColor, opacity = 60,
              align = 'center', border = rgb(2, 48, 32), borderWidth = 2)
    drawLabel("Help", 700, 60, bold = True, size = 25, 
              fill =  rgb(58, 95, 11))
    drawRect(120, 60, 160, 50, fill = app.leaderboardColor, opacity = 60,
              align = 'center', border = rgb(2, 48, 32), borderWidth = 2)
    drawLabel("Leaderboard", 120, 60, bold = True, size = 25, 
              fill =  rgb(58, 95, 11))

def start_onMousePress(app, mouseX, mouseY, button):
    if (640 <= mouseX <= 760) and (35 <= mouseY <= 85):
        setActiveScreen('help')
    if (80 <= mouseX <= 200) and (35 <= mouseY <= 85):
        setActiveScreen('leaderboard')
        readScore(app)
        return leaderboard_onMousePress(app, 230, 80, 0)
    (app)
    if 275 <= mouseX <= 525:
        if 212.5 <= mouseY <= 287.5:    
            newGame(app, 'easy')
        if 297.5 <= mouseY <= 372.5:    
            newGame(app, 'medium')
        if 382.5 <= mouseY <= 457.5:    
            newGame(app, 'hard')
        if 467.5 <= mouseY <= 542.5:   
            newGame(app, 'extreme')

#button toggle
def start_onMouseMove(app, mouseX, mouseY):
    if (640 <= mouseX <= 760) and (35 <= mouseY <= 85):
        app.helpColor = rgb(91, 148, 1)
    else: 
        app.helpColor = app.originalColor
    if (80 <= mouseX <= 200) and (35 <= mouseY <= 85):
        app.leaderboardColor = rgb(91, 148, 1)
    else:
        app.leaderboardColor = app.originalColor
    if 212.5 <= mouseY <= 287.5 and 275 <= mouseX <= 525:    #easysettings
        app.easyColor = rgb(91, 148, 1)
    else: 
        app.easyColor = app.originalColor
    if 297.5 <= mouseY <= 372.5 and 275 <= mouseX <= 525:    #mediumsettings
        app.mediumColor = rgb(91, 148, 1)
    else:
        app.mediumColor = app.originalColor
    if 382.5 <= mouseY <= 457.5 and 275 <= mouseX <= 525:    #hardsettings
        app.hardColor = rgb(91, 148, 1)
    else:
        app.hardColor = app.originalColor
    if 467.5 <= mouseY <= 542.5 and 275 <= mouseX <= 525:    #extremesettings
        app.extremeColor = rgb(91, 148, 1)
    else:
        app.extremeColor = app.originalColor
        
def game_onStep(app):
    if (app.gameOver or app.win) == False:
        if app.timer < 999 and app.paused == False:
            app.timer += 1
            if app.hint == True:
                app.hintTimer += 1

    if (app.gameOver) == True:
        app.stepsPerSecond = app.currSetting.revealSpeed 
        if len(app.newMines) > 0: #revealing mines
            app.revealedMines.append(app.newMines[-1])
            app.newMines.pop()
    if app.win == True:
        calculateScore(app)
        app.stepsPerSecond = 5
        if  app.revealColor < 250:
            app.revealColor += 10
        if app.flowerDim < app.currSetting.cellWidth:
            app.flowerDim += app.currSetting.cellWidth/4
    if app.revealColor == 250:
        app.revealScore = True

#button toggle
def game_onMouseMove(app, mouseX, mouseY):
    if app.win == False and len(app.newMines) != 0:
        if (app.width/24 <= mouseX <= app.width/24 + app.width/8) and (app.currSetting.boardTop/2
            - app.currSetting.boardTop/4 <= mouseY <= app.currSetting.boardTop * 3/4): #if click hint
            app.hintColor = rgb(91, 148, 1)
        else:
            app.hintColor = app.originalColor

        if (app.width * 8/9 <= mouseX <= app.width * 8/9 + app.currSetting.boardTop/2) and (app.currSetting.boardTop/2
            - app.currSetting.boardTop/4 <= mouseY <= app.currSetting.boardTop * 3/4): #if click exit
            app.exitColor = rgb(91, 148, 1)
        else:
            app.exitColor = None

        if (app.width * 7/9 <= mouseX <= app.width * 7/9 + app.currSetting.boardTop/2) and (app.currSetting.boardTop/2
            - app.currSetting.boardTop/4 <= mouseY <= app.currSetting.boardTop * 3/4): #if click restart
            app.restartColor = rgb(91, 148, 1)
        else:
            app.restartColor = app.originalColor

    if len(app.newMines) == 0: #if all mines are revealed gameover splash screen
        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
        app.height*2/3 - app.height/18 < mouseY < app.height*2/3 + app.height/18): 
            app.exitButtonColor = rgb(147, 230, 23)
        else:
            app.exitButtonColor = app.originalButtonColor

        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
            app.height*8/15 - app.height/18 < mouseY < app.height*8/15 + app.height/18):
            app.restartButtonColor = rgb(147, 230, 23)
        else:
            app.restartButtonColor = app.originalButtonColor
    
    if app.revealScore == True: 
        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
            app.height * 7/15 - app.height/20 < mouseY < app.height * 7/15 + app.height/20):
            app.saveButtonColor = rgb(147, 230, 23)
        else:
            app.saveButtonColor = app.originalButtonColor

        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
            app.height * 9/15 - app.height/20 < mouseY < app.height * 9/15 + app.height/20):
            app.restartButtonColor = rgb(147, 230, 23)
        else:
            app.restartButtonColor = app.originalButtonColor
        
        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
            app.height * 11/15 - app.height/20 < mouseY < app.height * 11/15 + app.height/20):
            app.exitButtonColor = rgb(147, 230, 23)
        else:
            app.exitButtonColor = app.originalButtonColor

#creates board without mines
def game_createBoard(app): 
    app.gameBoard = [[1]*app.currSetting.cols for row in range(app.currSetting.rows)]

#places mines onto created board
def game_placeMines(app):
    app.newMines = []
    while len(app.newMines)< app.currSetting.mines:
        mineX, mineY = random.randrange(0, app.currSetting.rows), random.randrange(0, app.currSetting.cols)
        if (mineX, mineY) not in app.newMines:
            app.gameBoard[mineX][mineY] = -1
            app.newMines.append((mineX, mineY))
    app.memoryBoard = copy.deepcopy(app.gameBoard)
    storeNeighbours(app)

def calculateScore(app):
    if app.difficulty == 'easy':
        bestScore = 100000
    if app.difficulty == 'medium':
        bestScore = 500000
    if app.difficulty == 'hard':
        bestScore = 1000000
    if app.difficulty == 'extreme':
        bestScore = 1000000
    totalTime = app.hintTimer + app.timer
    app.currSetting.score = rounded(bestScore/totalTime)


def gameWin(app):
    if len(app.revealedTiles) == app.currSetting.rows*app.currSetting.cols - app.currSetting.mines:
        app.win = True #win condition is revealed tiles == all tiles - mines
        app.flagLocs = []
    else:
        app.win = False

def game_onMousePress(app, mouseX, mouseY, button):
    #if is not won or all mines have not been revealed user has access to boardTop functions
    if app.win == False and len(app.newMines) != 0:
        if (app.width/24 <= mouseX <= app.width/24 + app.width/8) and (app.currSetting.boardTop/2
            - app.currSetting.boardTop/4 <= mouseY <= app.currSetting.boardTop * 3/4): #if click hint
            app.hint = not app.hint

        if (app.width * 8/9 <= mouseX <= app.width * 8/9 + app.currSetting.boardTop/2) and (app.currSetting.boardTop/2
            - app.currSetting.boardTop/4 <= mouseY <= app.currSetting.boardTop * 3/4): #if click exit
            return exitToMenu(app)

        if (app.width * 7/9 <= mouseX <= app.width * 7/9 + app.currSetting.boardTop/2) and (app.currSetting.boardTop/2
            - app.currSetting.boardTop/4 <= mouseY <= app.currSetting.boardTop * 3/4): #if click restart
            return restartGame(app)

    if len(app.newMines) == 0: #if all mines are revealed gameover splash screen
        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
        app.height*2/3 - app.height/18 < mouseY < app.height*2/3 + app.height/18): 
            return exitToMenu(app)

        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
            app.height*8/15 - app.height/18 < mouseY < app.height*8/15 + app.height/18):
            return restartGame(app)
    

    if app.revealScore == True: #if game is won and flowers have bloomed, splash screen
        if (app.width/2 - app.width/5 <= mouseX <= app.width/2 + app.width/5) and (
            app.height * 7/15 - app.height/20 <= mouseY <= app.height * 7/15 + app.height/20):
            return setScreen(app)

        if (app.width/2 - app.width/5 <= mouseX <= app.width/2 + app.width/5) and (
            app.height * 9/15 - app.height/20 <= mouseY <= app.height * 9/15 + app.height/20):
            return restartGame(app)
        
        if (app.width/2 - app.width/5 < mouseX < app.width/2 + app.width/5) and (
            app.height * 11/15 - app.height/20 < mouseY < app.height * 11/15 + app.height/20):
            return exitToMenu(app)

    if mouseY > app.currSetting.boardTop and (app.gameOver == False) and (app.win == False): #if game is being played
        index = game_getCell(app, mouseX, mouseY)
        x, y = index
        selectedCell = app.gameBoard[x][y]
        if button == 0:
            if app.firstMove == True: 
                firstMove(app, index)
                app.firstMove = False
            else:
                if selectedCell == 0:
                    if neighbourFlags(app, index):
                        handleClicked(app, index)
                if selectedCell != (0 or 11): #if cell hasn't been revealed or flagged
                    if selectedCell == -1:
                            app.revealedMines.append(index)
                            app.newMines.remove(index)
                            return game_gameOver(app)
                    if selectedCell == 1: #if not bomb
                        caveGen(app, index)  
        if button == 2:
            handleFlag(app, index)
    gameWin(app)


def setScreen(app):
    setActiveScreen("saveScore")
    app.width = 800
    app.height = 600

 #algorithm for when a revealed tile with #flags = #numberontile is clicked, neighbours are revealed
def handleClicked(app, index):
    row, col = index
    for dx, dy in app.moves:
        newX, newY = row + dx, dy + col
        if isLegal(app, newX, newY):
            newIndex = (newX, newY)
            if app.gameBoard[newX][newY] == -1:
                app.revealedMines.append(newIndex)
                app.newMines.remove(newIndex)
                return game_gameOver(app)
            elif app.gameBoard[newX][newY] == 1:
                caveGen(app, newIndex)

def exitToMenu(app):
    app.width = 800
    app.height = 600
    setActiveScreen('start')

def handleFlag(app, index): #flag / unflag based on clicks & number of flags remaining
    x, y = index
    selectedCell = app.gameBoard[x][y]
    if index not in app.revealedTiles:
        if selectedCell != 11 and app.currSetting.flags > 0:
            app.gameBoard[x][y] = 11
            app.currSetting.flags -= 1
            app.flagLocs.append((x, y))
        elif selectedCell == 11:
            app.flagLocs.remove((x, y))
            app.gameBoard[x][y] = app.memoryBoard[x][y]
            app.currSetting.flags += 1

def firstMove(app, index): #first move is safe and is a cave generation 
    x, y = index
    selectedCell = app.gameBoard[x][y]
    if selectedCell == (1 or 0) and app.neighbours[index] == 0:
        return caveGen(app, index)
    else:
        if selectedCell == -1:
            app.newMines.remove((x,y))
            app.gameBoard[x][y] = 1
            while len(app.newMines)< app.currSetting.mines:
                mineX, mineY = random.randrange(0, app.currSetting.rows), random.randrange(0, app.currSetting.cols)
                if (mineX, mineY) not in app.newMines:
                    app.gameBoard[mineX][mineY] = -1
                    app.newMines.append((mineX, mineY))
            app.memoryBoard = copy.deepcopy(app.gameBoard)
            app.neighbours = dict()
            storeNeighbours(app)
        if selectedCell == 1:
            for (dx, dy) in app.moves:
                newX = x + dx
                newY = y + dy
                newIndex = (newX, newY)
                if isLegal(app, newX, newY):
                    selectedCell = app.gameBoard[newX][newY]
                    if selectedCell == -1:
                        app.newMines.remove((newX, newY))
                        app.gameBoard[newX][newY] = 1
                        while len(app.newMines)< app.currSetting.mines:
                            mineX, mineY = random.randrange(0, app.currSetting.rows), random.randrange(0, app.currSetting.cols)
                            if (mineX, mineY) not in app.newMines and (mineX != newX 
                                and mineY != newY):
                                app.gameBoard[mineX][mineY] = -1
                                app.newMines.append((mineX, mineY))
                        app.memoryBoard = copy.deepcopy(app.gameBoard)
                        app.neighbours = dict()
                        storeNeighbours(app)
        return firstMove(app, index)
    
def storeNeighbours(app):
    for i in range(app.currSetting.rows):
        for j in range(app.currSetting.cols):
            index = (i, j)
            game_countMines(app, index)
    
def game_countMines(app, index): #counts neighbouring mines
    app.count = 0
    x, y = index
    app.moves = [(1,0), (0,1), (-1,0), (0,-1), (1,1), (-1,-1), (-1,1), (1, -1)]
    for (dx, dy) in app.moves: 
        newX = dx + x
        newY = dy + y
        if isLegal(app, newX, newY):
            if app.gameBoard[newX][newY] == -1:
                app.count += 1
    app.neighbours[index] = app.count
                
def caveGen(app, index): #recursive cave generation for floodfill
    x, y = index
    if isLegal(app, x, y):
        if not app.gameBoard[x][y] == -1:
            if index not in app.revealedTiles:
                if index in app.flagLocs:
                    app.flagLocs.remove(index)
                    app.currSetting.flags += 1
                app.revealedTiles.add(index)
                app.gameBoard[x][y] = 0
                if app.neighbours[index] == 0:
                    for (dx, dy) in app.moves:
                        newX = x + dx
                        newY = y + dy
                        newIndex = (newX, newY)
                        caveGen(app, newIndex)

def isLegal(app, newX, newY):
    if 0 <= newX < app.currSetting.rows and 0 <= newY < app.currSetting.cols:
        return True
    else:
        return False

def game_gameOver(app):
    app.gameOver = True

def game_revealBombs(app): #if game is over bombs are revealed
    for row, col in app.revealedMines:
        cellLeft, cellTop = game_getCellLeftTop(app, row, col)
        if app.gameBoard[row][col] == 11:
            pass
        else:
            drawImage(app.mine, cellLeft, cellTop, width=app.currSetting.cellWidth,
                      height=app.currSetting.cellHeight)

def game_wrongFlags(app): #wrong flags are crossed with Xs
    for row, col in app.flagLocs:
        if app.memoryBoard[row][col] != -1:
            app.wrongFlags.append((row, col))
            app.flagLocs.remove((row,col))
    flagBoom(app)

def revealedNeighbours(app, index):
    row, col = index
    count = 9
    for x in range(-1, 2):
        for y in range(-1, 2):
            newX = row + x
            newY = col + y
            if isLegal(app, newX, newY) and app.gameBoard[newX][newY] == 0:
                count -= 1
            elif isLegal(app, newX, newY) == False:
                count -= 1
    return count

def neighbourFlags(app, index):
    row, col = index
    count = 0
    for x in range(-1, 2):
        for y in range(-1, 2):
            newX = row + x
            newY = col + y
            if isLegal(app, newX, newY) and app.gameBoard[newX][newY] == 11:
                count += 1
    if count == app.neighbours[index]:
        return True
    else:
        return False

def flagBoom(app):
    for row, col in app.wrongFlags:
        cellLeft, cellTop = game_getCellLeftTop(app, row, col)
        drawImage(app.wrong, cellLeft, cellTop, width=app.currSetting.cellWidth,
                  height=app.currSetting.cellHeight)

def game_clearBoard(app):
    for (row, col) in app.newMines:
        cellLeft, cellTop = game_getCellLeftTop(app, row, col)
        if app.flowerDim > 0:
            if (row + col) % 5 == 0:
                drawImage(app.pink, cellLeft + app.currSetting.cellWidth/2, cellTop + app.currSetting.cellWidth/2,
                           width=app.flowerDim, height=app.flowerDim, align = 'center')
            elif (row+col) % 3 == 0:
                drawImage(app.sakura, cellLeft + app.currSetting.cellWidth/2, cellTop + app.currSetting.cellWidth/2,
                           width=app.flowerDim, height=app.flowerDim, align = 'center')
            elif (row + col) % 2 == 0:
                drawImage(app.myPink, cellLeft + app.currSetting.cellWidth/2, cellTop + app.currSetting.cellWidth/2,
                           width=app.flowerDim, height=app.flowerDim, align = 'center')

def game_drawFlag(app):
    for row, col in app.flagLocs:
        cellLeft, cellTop = game_getCellLeftTop(app, row, col)
        drawImage(app.flag, cellLeft + app.currSetting.cellWidth/6, 
                  cellTop + app.currSetting.cellHeight/6,
                  width=app.currSetting.cellWidth*2/3, height=app.currSetting.cellHeight*2/3)

def game_drawBoard(app):
    for row in range(app.currSetting.rows):
        for col in range(app.currSetting.cols):
            game_drawCell(app, row, col)

def game_drawCell(app, row, col):
    cellLeft, cellTop = game_getCellLeftTop(app, row, col)
    if app.win == False:
        if (row, col) in app.revealedTiles or app.gameBoard[row][col] == 0: #if there is no bomb, change color
            color = rgb(217,195,162) if (row + col) % 2 == 0 else rgb(205,185,156)
            drawRect(cellLeft, cellTop, app.currSetting.cellWidth, app.currSetting.cellHeight,
                fill=color)
            if (row, col) in app.revealedTiles and app.neighbours[(row, col)] != 0: #if there are neighbouring bombs, label
                howMany = app.neighbours[(row, col)]
                if howMany == 1:
                    labelColor = 'blue'
                if howMany == 2:
                    labelColor = 'green'
                if howMany == 3:
                    labelColor = 'red'
                if howMany == 4:
                    labelColor = 'darkBlue'
                if howMany == 5:
                    labelColor = 'brown'
                if howMany == 6:
                    labelColor = 'cyan'
                if howMany == 7:
                    labelColor = 'black'
                if howMany == 8:
                    labelColor = 'grey'
                drawLabel(app.neighbours[(row, col)], cellLeft + app.currSetting.cellWidth/2, cellTop + 
                          app.currSetting.cellHeight/2, fill = labelColor,
                          size = app.currSetting.cellWidth/2)
        else: 
            color = rgb(150, 214, 51) if (row + col) % 2 == 0 else rgb(176, 245, 69)
            drawRect(cellLeft, cellTop, app.currSetting.cellWidth, app.currSetting.cellHeight,
                        fill=color)
    else:
        if (row, col) in app.revealedTiles:
            drawRect(cellLeft, cellTop, app.currSetting.cellWidth, app.currSetting.cellHeight,
                fill= rgb(150, app.revealColor, 51))
        else:
            color = rgb(150, 250, 51)
            drawRect(cellLeft, cellTop, app.currSetting.cellWidth, app.currSetting.cellHeight,
                        fill=color)

def game_getCell(app, x, y):
    dx = x - app.currSetting.boardLeft
    dy = y - app.currSetting.boardTop
    row = math.floor(dy / app.currSetting.cellWidth)
    col = math.floor(dx / app.currSetting.cellHeight)
    if (0 <= row < app.currSetting.rows) and (0 <= col < app.currSetting.cols):
        return (row, col)
    else:
        return None

def game_getCellLeftTop(app, row, col):
    cellLeft = app.currSetting.boardLeft + col * app.currSetting.cellWidth
    cellTop = app.currSetting.boardTop + row * app.currSetting.cellHeight
    return (cellLeft, cellTop)

def game_redrawAll(app):
    drawRect(0,0, app.width, app.currSetting.boardTop, fill = rgb(81, 125, 12))
    drawLabel(f'{app.currSetting.flags}', app.width*1/3 + app.currSetting.boardTop/2, app.currSetting.boardTop/2, fill = 'white',
               bold = True, size = app.currSetting.boardTop/3)
    drawImage(app.flag, (app.width * 1/3), app.currSetting.boardTop/2, width = app.currSetting.boardTop/2, 
              height = app.currSetting.boardTop/2, align = 'center')
    drawImage(app.clock, (app.width * 2/3) - app.currSetting.boardTop* 2/3, app.currSetting.boardTop/2, width = app.currSetting.boardTop/2, 
              height = app.currSetting.boardTop/2, align = 'center')
    drawLabel(f'{app.timer}', app.width*2/3, app.currSetting.boardTop/2, fill = 'white',
               bold = True, size = app.currSetting.boardTop/3)
    drawRect(app.width/24, app.currSetting.boardTop/2 - app.currSetting.boardTop/4, app.width/8,
              app.currSetting.boardTop/2, border = 'white', fill = app.hintColor)
    drawLabel("Hint", app.width/24 + app.width/16, app.currSetting.boardTop/2, fill = 'white',
               size = app.currSetting.boardTop/4, bold = True)
    drawRect(app.width * 8/9, app.currSetting.boardTop/2 - app.currSetting.boardTop/4, app.currSetting.boardTop/2,
              app.currSetting.boardTop/2, fill = app.exitColor)
    drawImage(app.exit, app.width * 8/9, app.currSetting.boardTop/2 - app.currSetting.boardTop/4, width = app.currSetting.boardTop/2, 
              height = app.currSetting.boardTop/2)
    drawRect(app.width * 7/9, app.currSetting.boardTop/2 - app.currSetting.boardTop/4, app.currSetting.boardTop/2,
              app.currSetting.boardTop/2, border = 'white', fill = app.restartColor)
    drawImage(app.restart, app.width * 7/9 + app.currSetting.boardTop/12, app.currSetting.boardTop/2 - app.currSetting.boardTop/6, width = app.currSetting.boardTop/3, 
              height = app.currSetting.boardTop/3)
    game_drawBoard(app)
    game_drawFlag(app)

    if app.hint == True and app.firstMove == True:
        drawRect(app.width/2, app.height*8/15, app.width*2/5, app.height/9,
        fill = rgb(150, 214, 51), align = 'center', border = 'black')
        drawLabel("Click any tile!", app.width/2, app.height*8/15, size = app.height/21)
    
    if (app.hint == True and app.firstMove == False
        and app.gameOver == False and app.win == False):
        boardSolver(app)

    if app.gameOver == True:
        game_wrongFlags(app)
        game_revealBombs(app)
        
    if app.win == True:
        game_clearBoard(app)
        
    if app.revealScore == True: #if game is won and flowers have bloomed! 
        drawRect(app.width/2, app.height/2, app.width/2, app.height*2/3,
        fill = rgb(91, 170, 25), align = 'center', border = rgb(2, 48, 32))
        drawRect(app.width/2, app.height * 7/15, app.width*2/5, app.height/10,
        fill = app.saveButtonColor, align = 'center', border = rgb(2, 48, 32))
        drawRect(app.width/2, app.height * 9/15, app.width*2/5, app.height/9,
        fill = app.restartButtonColor, align = 'center', border = rgb(2, 48, 32))
        drawRect(app.width/2, app.height * 11/15, app.width*2/5, app.height/9,
        fill = app.exitButtonColor, align = 'center', border = rgb(2, 48, 32))
        drawLabel("Save Score", app.width/2, app.height*7/15, size = app.height/21)
        drawLabel("Restart", app.width/2, app.height*9/15, size = app.height/21)
        drawLabel("Main Menu", app.width/2, app.height*11/15, size = app.height/21)
        drawLabel(f'Score: {app.currSetting.score}', app.width/2, app.height* 11/30, 
                bold = True, fill = 'white', size = app.height/24)
        drawImage(app.trophy, app.width/2 - app.width/6, app.height * 7/24, 
                  width= app.height/15, height=app.height/15, align = 'center')
        drawImage(app.trophy, app.width/2 + app.width/6, app.height * 7/24, 
                  width= app.height/15, height=app.height/15, align = 'center')
        drawLabel("Win!", app.width/2, app.height * 7/24, bold = True, 
                  fill = 'white', size = app.height/12)
        
    if len(app.newMines) == 0: #display gameover
        drawRect(app.width/2, app.height/2, app.width/2, app.height/2,
        fill = rgb(91, 170, 25), align = 'center', border = rgb(2, 48, 32))
        drawRect(app.width/2, app.height*8/15, app.width*2/5, app.height/9,
        fill = app.restartButtonColor, align = 'center', border = rgb(2, 48, 32))
        drawLabel("Restart", app.width/2, app.height*8/15, size = app.height/21)
        drawRect(app.width/2, app.height*2/3, app.width*2/5, app.height/9,
        fill = app.exitButtonColor, align = 'center', border = rgb(2, 48, 32))
        drawLabel("Main Menu", app.width/2, app.height*2/3, size = app.height/21)
        drawLabel("Game", app.width/2, app.height/3, 
                  bold = True, fill = 'red', size = app.height/12)
        drawLabel("Over", app.width/2, app.height* 5/12, 
                  bold = True, fill = 'red', size = app.height/12)

def boardSolver(app): #algortihm for hint generation
    found = False
    #if a flag is wrong, highlight wrong flag:
    for row, col in app.flagLocs:
        if app.memoryBoard[row][col] != -1:
            highlightCell(app, (row, col))
            found = True
            break

    for row in range(app.currSetting.rows):
        for col in range(app.currSetting.cols):
            index = (row, col)
            # If the cell is revealed and has neighbouring mines
            if app.gameBoard[row][col] == 0 and app.neighbours[index] > 0:
                if found:
                    break
                if app.neighbours[index] == revealedNeighbours(app, index):
                    if neighbourFlags(app, index) == False: #if mine has not already been flagged
                        highlightCell(app, index)
                        found = True
                        break

                elif app.neighbours[index] != revealedNeighbours(app, index): 
                    if neighbourFlags(app, index) == True:
                        highlightCell(app, index)
                        found = True
                        break
        if found:
            break
    else: #if not solveable, edits board to be solveable 
        for i in range(app.currSetting.rows):
            for j in range(app.currSetting.cols):
                if app.gameBoard[i][j] == 1:
                    index = (i, j)
                    caveGen(app, index)
                    found = True
                    break

def highlightCell(app, index):
    row, col = index
    cellLeft, cellTop = game_getCellLeftTop(app, row, col)
    drawRect(cellLeft, cellTop, app.currSetting.cellWidth,
              app.currSetting.cellHeight, fill = None, border = 'yellow')


def help_redrawAll(app):
    drawImage(app.helpScreen,0,0)
    drawRect(750, 10, 40, 40, fill = app.exitColor)
    drawImage(app.exit, 750, 10, width = 40, height = 40)

def help_onMousePress(app, mouseX, mouseY, button):
    if (10 <= mouseY <= 50) and (750 <= mouseX <= 790):
        setActiveScreen('start')

def help_onMouseMove(app, mouseX, mouseY):
    if (10 <= mouseY <= 50) and (750 <= mouseX <= 790):
        app.exitColor = rgb(137, 201, 38)
    else:
        app.exitColor = None

def leaderboard_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = rgb(150, 214, 51))
    drawRect(200, 50, 400, 500, fill = rgb(69, 110, 49))
    if app.selectedLead != 'easy':
        drawRect(225, 70, 80, 40, fill = app.easyLead, border = rgb(124, 175, 102), borderWidth = 1)
    else:
        drawRect(225, 70, 80, 40, fill = 'darkGreen', border = rgb(124, 175, 102), borderWidth = 1)
    if app.selectedLead != 'medium':
        drawRect(315, 70, 80, 40, fill = app.mediumLead, border = rgb(124, 175, 102), borderWidth = 1)
    else:
        drawRect(315, 70, 80, 40, fill = 'darkGreen', border = rgb(124, 175, 102), borderWidth = 1)
    if app.selectedLead != 'hard':
        drawRect(405, 70, 80, 40, fill = app.hardLead, border = rgb(124, 175, 102), borderWidth = 1)
    else:
        drawRect(405, 70, 80, 40, fill = 'darkGreen', border = rgb(124, 175, 102), borderWidth = 1)
    if app.selectedLead != 'extreme':
        drawRect(495, 70, 80, 40, fill = app.extremeLead, border = rgb(124, 175, 102), borderWidth = 1)
    else:
        drawRect(495, 70, 80, 40, fill = 'darkGreen', border = rgb(124, 175, 102), borderWidth = 1)

    drawLabel('Easy', 265, 90, size = 15, fill = 'white')
    drawLabel('Medium', 355, 90, size = 15, fill = 'white')
    drawLabel('Hard', 445, 90, size = 15, fill = 'white')
    drawLabel('Extreme', 535, 90, size = 15, fill = 'white')

    drawRect(750, 10, 40, 40, fill = app.exitColor)
    drawImage(app.exit, 750, 10, width = 40, height = 40)
    drawRect(225, 130, 350, 400, fill =  rgb(124, 169, 102))
    drawLabel("Leaderboard", 400, 150, size = 30, fill = 'white')
    drawRect(235, 170, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 215, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 260, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 305, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 350, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 395, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 440, 330, 35, fill = rgb(104, 142, 85))
    drawRect(235, 485, 330, 35, fill = rgb(104, 142, 85))

    count = 1
    position = 185
    for i in range(8):
        drawLabel(f'{count}.', 250, position, size = 30, fill = 'white')
        if count == 1:
            drawLabel(f'{app.onePlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.oneScore}', 550, position, size = 25, fill = 'white', align = 'right')
        if count == 2:
            drawLabel(f'{app.twoPlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.twoScore}', 550, position, size = 25, fill = 'white', align = 'right')
        if count == 3:
            drawLabel(f'{app.threePlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.threeScore}', 550, position, size = 25, fill = 'white', align = 'right')
        if count == 4:
            drawLabel(f'{app.fourPlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.fourScore}', 550, position, size = 25, fill = 'white', align = 'right')
        if count == 5:
            drawLabel(f'{app.fivePlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.fiveScore}', 550, position, size = 25, fill = 'white', align = 'right')
        if count == 6:
            drawLabel(f'{app.sixPlayer}', 270, position, size = 25, fill = 'white', align = 'left')  
            drawLabel(f'{app.sixScore}', 550, position, size = 25, fill = 'white', align = 'right')  
        if count == 7:
            drawLabel(f'{app.sevenPlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.sevenScore}', 550, position, size = 25, fill = 'white', align = 'right')
        if count == 8:
            drawLabel(f'{app.eightPlayer}', 270, position, size = 25, fill = 'white', align = 'left') 
            drawLabel(f'{app.eightScore}', 550, position, size = 25, fill = 'white', align = 'right')
        count += 1
        position += 45

def leaderboard_onMousePress(app, mouseX, mouseY, button): #toggling between different difficulties
    if (10 <= mouseY <= 50) and (750 <= mouseX <= 790):
            setActiveScreen('start')
    if (70 <= mouseY <= 110):
        if (225 <= mouseX <= 305):
            app.selectedLead = 'easy'
            sortEasy(app)
            app.onePlayer, app.oneScore = app.leaderboardEasy[0] 
            app.twoPlayer, app.twoScore = app.leaderboardEasy[1] 
            app.threePlayer, app.threeScore = app.leaderboardEasy[2] 
            app.fourPlayer, app.fourScore = app.leaderboardEasy[3] 
            app.fivePlayer, app.fiveScore = app.leaderboardEasy[4] 
            app.sixPlayer, app.sixScore = app.leaderboardEasy[5] 
            app.sevenPlayer, app.sevenScore = app.leaderboardEasy[6] 
            app.eightPlayer, app.eightScore = app.leaderboardEasy[7]
        if (315 <= mouseX <= 395):
            app.selectedLead = 'medium'
            sortMedium(app)
            app.onePlayer, app.oneScore = app.leaderboardMedium[0] 
            app.twoPlayer, app.twoScore = app.leaderboardMedium[1] 
            app.threePlayer, app.threeScore = app.leaderboardMedium[2] 
            app.fourPlayer, app.fourScore = app.leaderboardMedium[3] 
            app.fivePlayer, app.fiveScore = app.leaderboardMedium[4] 
            app.sixPlayer, app.sixScore = app.leaderboardMedium[5] 
            app.sevenPlayer, app.sevenScore = app.leaderboardMedium[6] 
            app.eightPlayer, app.eightScore = app.leaderboardMedium[7]
        if (405 <= mouseX <= 485):
            app.selectedLead = 'hard'
            sortHard(app)
            app.onePlayer, app.oneScore = app.leaderboardHard[0] 
            app.twoPlayer, app.twoScore = app.leaderboardHard[1] 
            app.threePlayer, app.threeScore = app.leaderboardHard[2] 
            app.fourPlayer, app.fourScore = app.leaderboardHard[3] 
            app.fivePlayer, app.fiveScore = app.leaderboardHard[4] 
            app.sixPlayer, app.sixScore = app.leaderboardHard[5] 
            app.sevenPlayer, app.sevenScore = app.leaderboardHard[6] 
            app.eightPlayer, app.eightScore = app.leaderboardHard[7]
        if (495 <= mouseX <= 575):
            app.selectedLead = 'extreme'
            sortExtreme(app)
            app.onePlayer, app.oneScore = app.leaderboardExtreme[0] 
            app.twoPlayer, app.twoScore = app.leaderboardExtreme[1] 
            app.threePlayer, app.threeScore = app.leaderboardExtreme[2] 
            app.fourPlayer, app.fourScore = app.leaderboardExtreme[3] 
            app.fivePlayer, app.fiveScore = app.leaderboardExtreme[4] 
            app.sixPlayer, app.sixScore = app.leaderboardExtreme[5] 
            app.sevenPlayer, app.sevenScore = app.leaderboardExtreme[6] 
            app.eightPlayer, app.eightScore = app.leaderboardExtreme[7]

def leaderboard_onMouseMove(app, mouseX, mouseY):
    if (10 <= mouseY <= 50) and (750 <= mouseX <= 790):
        app.exitColor = rgb(137, 201, 38)
    else:
        app.exitColor = None
    if (70 <= mouseY <= 110) and (225 <= mouseX <= 305):
        app.easyLead = rgb(98, 145, 74)
    else:
        app.easyLead = app.originalLead
    if (70 <= mouseY <= 110) and (315 <= mouseX <= 395):
        app.mediumLead = rgb(115, 153, 96)
    else:
        app.mediumLead = app.originalLead
    if (70 <= mouseY <= 110) and (405 <= mouseX <= 485):
        app.hardLead = rgb(115, 153, 96)
    else:
        app.hardLead = app.originalLead
    if (70 <= mouseY <= 110) and (495 <= mouseX <= 575):
        app.extremeLead = rgb(115, 153, 96)
    else:
        app.extremeLead = app.originalLead

#the following functions determine the top 8 in the leaderboard, if not enough saves adds XXXs
def sortEasy(app): 
    if len(app.easyScores) > 0:
        app.leaderboardEasy = sorted(app.easyScores, key=lambda x: x[1])
        app.leaderboardEasy.reverse()
    if len(app.leaderboardEasy) < 8:
        howMany = 8 - len(app.leaderboardEasy)
        for i in range(howMany):
            app.leaderboardEasy.append(('XXX', 'XXX'))

def sortMedium(app):
    if len(app.mediumScores) > 0:
        app.leaderboardMedium = sorted(app.mediumScores, key=lambda x: x[1])
        app.leaderboardMedium.reverse()
    if len(app.leaderboardMedium) < 8:
        howMany = 8 - len(app.leaderboardMedium)
        for i in range(howMany):
            app.leaderboardMedium.append(('XXX', 'XXX'))   

def sortHard(app):
    if len(app.hardScores) > 0:
        app.leaderboardHard = sorted(app.hardScores, key=lambda x: x[1])
        app.leaderboardHard.reverse()
    if len(app.leaderboardHard) < 8:
        howMany = 8 - len(app.leaderboardHard)
        for i in range(howMany):
            app.leaderboardHard.append(('XXX', 'XXX'))  

def sortExtreme(app):
    if len(app.extremeScores) > 0:
        app.leaderboardExtreme = sorted(app.extremeScores, key=lambda x: x[1])
        app.leaderboardExtreme.reverse()
    if len(app.leaderboardExtreme) < 8:
        howMany = 8 - len(app.leaderboardExtreme)
        for i in range(howMany):
            app.leaderboardExtreme.append(('XXX', 'XXX'))  

def saveScore_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill = rgb(150, 214, 51))
    drawRect(200, 50, 400, 500, fill = rgb(81, 125, 12), border = 'darkGreen', borderWidth = 3)
    drawRect(750, 10, 40, 40, fill = app.exitColor)
    drawLabel(f'Difficulty: {app.difficulty[0].upper() + app.difficulty[1:]}', app.width/2, 150, 
                bold = True, fill = 'white', size = 40)
    drawLabel(f'Score: {app.currSetting.score}', app.width/2, 230, 
                bold = True, fill = 'white', size = 40)
    drawLabel('Player Name:', app.width/2, 320, 
                bold = True, fill = 'white', size = 40)
    drawImage(app.exit, 750, 10, width = 40, height = 40)
    drawRect(400, 400, 300, 70, align='center', fill = rgb(150, 214, 51), borderWidth = 4,
             border = 'black')
    drawRect(400, 480, 300, 70, align='center', fill = app.exitButtonColor, borderWidth = 4,
             border = 'black')
    drawLabel(f'{app.currSetting.player}', 400, 400, bold = True, fill = 'white', size = 35)
    drawLabel('Save Score', 400, 480, bold = True, fill = 'white', size = 35)


def saveScore_onMousePress(app, mouseX, mouseY, button):
    if (250 <= mouseX <= 550) and (445 <= mouseY <= 525):
        if len(app.currSetting.player) > 0:
            saveScore(app)
            setActiveScreen('start')
    if (10 <= mouseY <= 50) and (750 <= mouseX <= 790):
        setActiveScreen('start')

def saveScore_onMouseMove(app, mouseX, mouseY):
    if (10 <= mouseY <= 50) and (750 <= mouseX <= 790):
        app.exitColor = rgb(137, 201, 38)
    else:
        app.exitColor = None
    if (250 <= mouseX <= 550) and (445 <= mouseY <= 525):
        app.exitButtonColor = rgb(137, 201, 38)
    else:
        app.exitButtonColor = app.originalButtonColor

def saveScore_onKeyPress(app, key):
    if key == 'backspace' and len(app.currSetting.player) > 0:
            app.currSetting.player = app.currSetting.player[:-1]
    if len(app.currSetting.player) < 9:
        if len(key) == 1:
            app.currSetting.player += key.upper()


#writes csv file to save file
def saveScore(app):
    list = [ app.difficulty, app.currSetting.player, app.currSetting.score]
    with open('highscores.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(list)

#reads csv file to display on leaderboard
def readScore(app):
    app.easyScores = []
    app.mediumScores = []
    app.hardScores = []
    app.extremeScores = []
    with open('highscores.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'easy':
                app.easyScores.append((row[1], row[2]))
            if row[0] == 'medium':
                app.mediumScores.append((row[1], row[2]))
            if row[0] == 'hard':
                app.hardScores.append((row[1], row[2]))
            if row[0] == 'extreme':
                app.extremeScores.append((row[1], row[2]))

def main():
    runAppWithScreens("start")

main()
########################################
# 
#   Citations: 
#   1)  To sort a list of tuples:
#       https://stackoverflow.com/questions/10695139/sort-a-list-of-tuples-by-2nd-item-integer-value
#
#   2)  Created images using:
#       https://www.pixilart.com/draw
#
#   3)  CSV file reading:
#       https://www.geeksforgeeks.org/reading-and-writing-csv-files-in-python/
#
#   4)  Icons:
#       trophy.png:  https://www.flaticon.com/free-icon/trophy_3112946
#       sakura.png:  https://www.vhv.rs/viewpic/TRTThxb_blossom-flower-flowers-pixel-tumblr-flower-pixel-art/
#       clock.png:   https://www.vecteezy.com/png/18803554-alarm-clock-cartoon-icon
#       flagg.png:   https://www.cleanpng.com/png-computer-icons-red-flag-clip-art-4621770/download-png.html
#       mine.png:    https://www.iconfinder.com/icons/2002908/achievement_badge_star_bomb_craft_danger_mine_icon
#       pink.png:    https://www.vecteezy.com/png/13399687-pink-flower-pixel-style
#       restart.png: https://flaticons.net/customize.php?dir=Application&icon=Command-Reset.png
#       exit.png:    https://www.freepnglogos.com/pics/x-png
#
########################################