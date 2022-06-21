import numpy as np
import pygame
import math

# initializing the constructor
pygame.init()

(width, height) = (500, 500)
background_colour = (175, 250, 242)
line_color = (189, 156, 247)
winner_line = (255, 255, 255)
player_color = (242, 241, 148)
player_thick = 12
line_thickness = 7
winner_thick = 15
margin = 20
n = 3
square = width / n
availableSquare = []
board = np.array([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
])
running = True

player = 1
ai = 2
currentPlayer = player
winner = None
scores = {1: 1, 2: -1, 'tie': 0}

screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Dumbest Tic-Tac-Toe')
pygame.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), line_thickness)
pygame.draw.line(screen, line_color, (width / 1.5, 0), (width / 1.5, height), line_thickness)
pygame.draw.line(screen, line_color, (0, height / 3), (width, height / 3), line_thickness)
pygame.draw.line(screen, line_color, (0, height / 1.5), (width, height / 1.5), line_thickness)
pygame.display.flip()


def getRowColumn():
    mouse = pygame.mouse.get_pos()
    global column
    global row
    row = int(mouse[1] / square)
    column = int(mouse[0] / square)
    print(f"Coordinates: {mouse}, Row: {row}, Column: {column}")


def checkEmpty(i, j):
    if board[i][j] == 0:
        return True


def claimSpot(i, j, player):
    board[i][j] = player
    x_start1 = (square * j + margin, square * i + margin)
    x_end1 = (square * (j + 1) - margin, square * (i + 1) - margin)
    x_start2 = (square * j + margin, square * (i + 1) - margin)
    x_end2 = (square * (j + 1) - margin, square * i + margin)
    o_center = (square * (j + 0.5), square * (i + 0.5))
    if player == 1:
        pygame.draw.line(screen, player_color, x_start1, x_end1, player_thick + 3)
        pygame.draw.line(screen, player_color, x_start2, x_end2, player_thick + 3)
    else:
        pygame.draw.circle(screen, player_color, o_center, width / 7, player_thick)
    pygame.display.flip()


def checkWin():
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

def checkWin2():
    global winner
    if board[0][0] == board[0][1] == board[0][2] != 0:
        winner = board[0][0]
        pygame.draw.line(screen, winner_line, (square * 0, square * 0.5), (square * 3, square * 0.5), winner_thick)
    elif board[1][0] == board[1][1] == board[1][2] != 0:
        winner = board[1][0]
        pygame.draw.line(screen, winner_line, (square * 0, square * 1.5), (square * 3, square * 1.5), winner_thick)
    elif board[2][0] == board[2][1] == board[2][2] != 0:
        winner = board[2][0]
        pygame.draw.line(screen, winner_line, (square * 0, square * 2.5), (square * 3, square * 2.5), winner_thick)
    elif board[0][0] == board[1][0] == board[2][0] != 0:
        winner = board[0][0]
        pygame.draw.line(screen, winner_line, (square * 0.5, square * 0), (square * 0.5, square * 3), winner_thick)
    elif board[0][1] == board[1][1] == board[2][1] != 0:
        winner = board[0][1]
        pygame.draw.line(screen, winner_line, (square * 1.5, square * 0), (square * 1.5, square * 3), winner_thick)
    elif board[0][2] == board[1][2] == board[2][2] != 0:
        winner = board[0][2]
        pygame.draw.line(screen, winner_line, (square * 2.5, square * 0), (square * 2.5, square * 3), winner_thick)
    elif board[0][0] == board[1][1] == board[2][2] != 0:
        winner = board[0][0]
        pygame.draw.line(screen, winner_line, (square * 0, square * 0), (square * 3, square * 3), winner_thick)
    elif board[2][0] == board[1][1] == board[0][2] != 0:
        winner = board[2][0]
        pygame.draw.line(screen, winner_line, (square * 3, square * 0), (square * 0, square * 3), winner_thick)
    elif 0 not in board:
        winner = "Tie"
    pygame.display.flip()
    print(f"The winner is: {winner}")

def isGameEnd():
    checkWin()
    if winner is not None:
        return True


def minimax(board, depth, isMaximizing):
    global bestMove
    global winner
    if isGameEnd():
        # checkWin()
        score = scores[winner]
        winner = None
        return score
    if isMaximizing:
        bestScore = -100
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = player
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
                    board[i][j] = ai
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
                board[i][j] = ai
                score = minimax(board, 0, True)
                board[i][j] = 0
                if score < bestScore:
                    bestScore = score
                    bestMove = [i, j]
    claimSpot(bestMove[0], bestMove[1], ai)


def switchPlayer():
    global currentPlayer
    if currentPlayer == player:
        currentPlayer = ai
    else:
        currentPlayer = player


def restart():
    global currentPlayer, winner
    currentPlayer = player
    winner = None
    for i in range(3):
        for j in range(3):
            board[i][j] = 0
    screen.fill(background_colour)
    pygame.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), line_thickness)
    pygame.draw.line(screen, line_color, (width / 1.5, 0), (width / 1.5, height), line_thickness)
    pygame.draw.line(screen, line_color, (0, height / 3), (width, height / 3), line_thickness)
    pygame.draw.line(screen, line_color, (0, height / 1.5), (width, height / 1.5), line_thickness)
    pygame.display.flip()


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            getRowColumn()
            print(board)
            if checkEmpty(row, column) and winner == None:
                claimSpot(row, column, currentPlayer)
                checkWin2()
                switchPlayer()
                print(board)
                if winner == None:
                    bestMove()
                    checkWin2()
                    switchPlayer()
                    print(board)
            elif winner != None:
                restart()
                print(board)
