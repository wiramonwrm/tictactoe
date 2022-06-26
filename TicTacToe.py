import pygame
import numpy as np
import random

# initializing the constructor
pygame.init()

#setup
game_width = 500
game_height = 500
header_height = 100
center = game_width/2
screen_height = game_height + header_height
line_thickness = 7
margin = 10
colors = {
    'bg': (175, 250, 242),
    'yellow': (225, 239, 52),
    'orange': (245, 168, 69),
    'red': (255, 71, 71),
    'line': (189, 156, 247),
    'header': (50, 117, 168),
    'firstpage': (50, 117, 168),
    'winner': (255, 255, 255),
    'player': (242, 241, 148)
}

screen = pygame.display.set_mode((game_width, screen_height))
screen.fill(colors['bg'])
pygame.display.flip()

player_thick = 12
line_thickness = 7
winner_thick = 15

#game setup values
running = True
game_mode = None
player1 = 1
player2 = 2
currentPlayer = player1
winner = None
n = 3
square = game_width / n
availableSquare = []
board = np.zeros((n,n))
scores = {1: 1, 2: -1, 'tie': 0}

#text setup
pygame.font.init()
Font = pygame.font.SysFont('cooperblack',  30)

class Box:
    def __init__(self, c, i, width, height, color):
        self.x1 = center-box_width/2
        self.y1 = box_height*(i+0.75)
        self.width = width
        self.height = height
        self.x2 = self.x1 + width
        self.y2 = self.y1 + height
        self.color = color

    def checkPos(self, pos):
        if pos[0] in range(int(self.x1), int(self.x2)) and pos[1] in range(int(self.y1), int(self.y2)):
            return True

    def drawBox(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x1, self.y1, self.width, self.height))

text_select_game_mode = Font.render('Select game mode. . .', True, colors['header'], colors['bg'])
box_width = text_select_game_mode.get_rect().width
box_height = 100
box1 = Box(center, 1, box_width, box_height, colors['yellow'])
box2 = Box(center, 2, box_width, box_height, colors['orange'])
box3 = Box(center, 3, box_width, box_height, colors['red'])
text_select_pvp = Font.render('PVP', True, colors['firstpage'], colors['yellow'])
text_select_easy = Font.render('vs Dumby', True, colors['firstpage'], colors['orange'])
text_select_hard = Font.render('vs Smarty', True, colors['firstpage'], colors['red'])

def select_game_mode():
    screen.fill(colors['bg'])
    box1.drawBox(screen)
    box2.drawBox(screen)
    box3.drawBox(screen)
    screen.blit(text_select_game_mode, (center - text_select_game_mode.get_rect().width/2,box_height))
    screen.blit(text_select_pvp, (center - text_select_pvp.get_rect().width/2,box_height*2))
    screen.blit(text_select_easy, (center - text_select_easy.get_rect().width/2,box_height*3))
    screen.blit(text_select_hard, (center - text_select_hard.get_rect().width/2,box_height*4))
    pygame.display.flip()

def game_start():
    screen.fill( colors['bg'])
    pygame.draw.line(screen,  colors['line'], (game_width / 3, header_height), (game_width / 3, screen_height), line_thickness)
    pygame.draw.line(screen,  colors['line'], (game_width / 1.5, header_height), (game_width / 1.5, screen_height), line_thickness)
    pygame.draw.line(screen,  colors['line'], (0, (game_height / 3)+header_height), (game_width, (game_height / 3)+header_height), line_thickness)
    pygame.draw.line(screen,  colors['line'], (0, (game_height / 1.5)+header_height), (game_width, (game_height / 1.5)+header_height), line_thickness)
    pygame.draw.line(screen,  colors['header'], (0, header_height), (game_width, header_height), line_thickness*2)
    screen.blit(text_game_mode, (margin,margin/2))
    screen.blit(text_current_turn, (margin,header_height-50))
    pygame.display.flip()

def getRowColumn(pos):
    global column
    global row
    row = int((pos[1] - header_height) / square)
    column = int(pos[0] / square)
    print(f"Coordinates: {pos}, Row: {row}, Column: {column}")


def checkEmpty(i, j):
    return board[i][j] == 0


def claimSpot(i, j, player):
    board[i][j] = player
    x_start1 = (square * j + margin, square * i + margin + header_height)
    x_end1 = (square * (j + 1) - margin, square * (i + 1) - margin + header_height)
    x_start2 = (square * j + margin, square * (i + 1) - margin + header_height)
    x_end2 = (square * (j + 1) - margin, square * i + margin + header_height)
    o_center = (square * (j + 0.5), square * (i + 0.5) + header_height)
    if player == 1:
        pygame.draw.line(screen, colors['player'], x_start1, x_end1, player_thick + 3)
        pygame.draw.line(screen, colors['player'], x_start2, x_end2, player_thick + 3)
    else:
        pygame.draw.circle(screen, colors['player'], o_center, game_width / 7, player_thick)
    pygame.display.flip()


def checkWin():
    global winner
    if board[0][0] == board[0][1] == board[0][2] != 0:
        winner = board[0][0]
        pygame.draw.line(screen, colors['winner'], (square * 0, square * 0.5 +header_height), (square * 3, square * 0.5+header_height), winner_thick)
    elif board[1][0] == board[1][1] == board[1][2] != 0:
        winner = board[1][0]
        pygame.draw.line(screen, colors['winner'], (square * 0, square * 1.5+header_height), (square * 3, square * 1.5+header_height), winner_thick)
    elif board[2][0] == board[2][1] == board[2][2] != 0:
        winner = board[2][0]
        pygame.draw.line(screen, colors['winner'], (square * 0, square * 2.5+header_height), (square * 3, square * 2.5+header_height), winner_thick)
    elif board[0][0] == board[1][0] == board[2][0] != 0:
        winner = board[0][0]
        pygame.draw.line(screen, colors['winner'], (square * 0.5, square * 0+header_height), (square * 0.5, square * 3+header_height), winner_thick)
    elif board[0][1] == board[1][1] == board[2][1] != 0:
        winner = board[0][1]
        pygame.draw.line(screen, colors['winner'], (square * 1.5, square * 0+header_height), (square * 1.5, square * 3+header_height), winner_thick)
    elif board[0][2] == board[1][2] == board[2][2] != 0:
        winner = board[0][2]
        pygame.draw.line(screen, colors['winner'], (square * 2.5, square * 0+header_height), (square * 2.5, square * 3+header_height), winner_thick)
    elif board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
        pygame.draw.line(screen, colors['winner'], (square * 0, square * 0+header_height), (square * 3, square * 3+header_height), winner_thick)
    elif board[2][0] == board[1][1] == board[0][2] != 0:
        winner = board[2][0]
        pygame.draw.line(screen, colors['winner'], (square * 3, square * 0+header_height), (square * 0, square * 3+header_height), winner_thick)
    elif 0 not in board:
        winner = "Tie"
    pygame.display.flip()
    print(f"The winner is: {winner}")


def switchPlayer():
    global currentPlayer
    currentPlayer = currentPlayer%2 +1


def restart():
    global currentPlayer, winner, game_mode
    currentPlayer = player1
    winner = None
    game_mode = None
    for i in range(3):
        for j in range(3):
            board[i][j] = 0


def randomComputer():
    global row, column
    availableSquare = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                availableSquare.append([i, j])
    x = random.randint(0, len(availableSquare) - 1)
    [row, column] = availableSquare[x]
    print(availableSquare)
    print(x)

def checkWinAi():
    global winner
    if board[0][0] == board[0][1] == board[0][2] != 0:
        winner = board[0][0]
    elif board[1][0] == board[1][1] == board[1][2] != 0:
        winner = board[1][0]
    elif board[2][0] == board[2][1] == board[2][2] != 0:
        winner = board[2][0]
    elif board[0][0] == board[1][0] == board[2][0] != 0:
        winner = board[0][0]
    elif board[0][1] == board[1][1] == board[2][1] != 0:
        winner = board[0][1]
    elif board[0][2] == board[1][2] == board[2][2] != 0:
        winner = board[0][2]
    elif board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
    elif board[2][0] == board[1][1] == board[0][2] != 0:
        winner = board[2][0]
    elif 0 not in board:
        winner = "tie"

def isGameEnd():
    checkWinAi()
    if winner is not None:
        return True


def minimax(board, depth, isMaximizing):
    global bestMove
    global winner
    if isGameEnd():
        score = scores[winner]
        winner = None
        return score
    if isMaximizing:
        bestScore = -100
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = player1
                    score = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    if score > bestScore:
                        bestScore = score
                        # bestMove = [i, j]
        return bestScore

    else:
        bestScore = 100
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = player2
                    score = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    if score < bestScore:
                        bestScore = score
                        # bestMove = [i, j]
        return bestScore


def bestMove():
    bestScore = 100
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                board[i][j] = player2
                score = minimax(board, 0, True)
                board[i][j] = 0
                if score < bestScore:
                    bestScore = score
                    bestMove = [i, j]
    claimSpot(bestMove[0], bestMove[1], player2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_mode is None and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            if box1.checkPos(mouse):
                game_mode = 'Game mode: PVP'
                text_game_mode = Font.render(game_mode, True,  colors['header'],  colors['bg'])
                turn = 'Turn : Player ' + str(currentPlayer)
                text_current_turn = Font.render(turn, True, colors['header'], colors['bg'])
                game_start()
            elif box2.checkPos(mouse):
                game_mode = 'Game mode: Dumb'
                text_game_mode = Font.render(game_mode, True,  colors['header'],  colors['bg'])
                text_current_turn = Font.render('Turn: ', True, colors['header'], colors['bg'])
                game_start()
            elif box3.checkPos(mouse):
                game_mode = 'Game mode: Smart'
                text_game_mode = Font.render(game_mode, True, colors['header'],  colors['bg'])
                text_current_turn = Font.render('Turn: ', True, colors['header'], colors['bg'])
                game_start()
        elif game_mode == 'Game mode: PVP' and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            getRowColumn(mouse)
            if checkEmpty(row, column) and winner == None:
                claimSpot(row, column, currentPlayer)
                checkWin()
                switchPlayer()
                print(currentPlayer)
                turn = 'Turn : Player ' + str(currentPlayer)
                text_current_turn = Font.render(turn, True, colors['header'], colors['bg'])
                screen.blit(text_current_turn, (margin, header_height - 50))
                pygame.display.flip()
                print(board)
            elif winner != None:
                restart()
                print(board)
        elif game_mode == 'Game mode: Dumb' and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            getRowColumn(mouse)
            if checkEmpty(row, column) and winner == None:
                claimSpot(row, column, currentPlayer)
                checkWin()
                switchPlayer()
                print(board)
                if winner == None:
                    randomComputer()
                    claimSpot(row, column, currentPlayer)
                    checkWin()
                    switchPlayer()
                    print(board)
            elif winner != None:
                restart()
                print(board)
        elif game_mode == 'Game mode: Smart' and event.type == pygame.MOUSEBUTTONDOWN:
            mouse = pygame.mouse.get_pos()
            getRowColumn(mouse)
            if checkEmpty(row, column) and winner == None:
                claimSpot(row, column, currentPlayer)
                checkWin()
                switchPlayer()
                print(board)
                if winner == None:
                    bestMove()
                    checkWin()
                    switchPlayer()
                    print(board)
            elif winner != None:
                restart()
                print(board)
        elif game_mode is None:
            select_game_mode()
            mouse = pygame.mouse.get_pos()
            if box1.checkPos(mouse) or box2.checkPos(mouse) or box3.checkPos(mouse):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



