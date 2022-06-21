import numpy as np
import pygame
import random

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

screen = pygame.display.set_mode((width, height))
screen.fill(background_colour)
pygame.display.set_caption('Smartest Tic-Tac-Toe')
pygame.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), line_thickness)
pygame.draw.line(screen, line_color, (width / 1.5, 0), (width / 1.5, height), line_thickness)
pygame.draw.line(screen, line_color, (0, height / 3), (width, height / 3), line_thickness)
pygame.draw.line(screen, line_color, (0, height / 1.5), (width, height / 1.5), line_thickness)
pygame.display.flip()

player1 = 1
player2 = 2
currentPlayer = player1
winner = None


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


def switchPlayer():
    global currentPlayer
    if currentPlayer == player1:
        currentPlayer = player2
    else:
        currentPlayer = player1


def restart():
    global currentPlayer, winner
    currentPlayer = player1
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


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            getRowColumn()
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


