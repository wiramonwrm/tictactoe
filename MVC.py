import pygame
import numpy as np
import random

# setup
game_width = 500
game_height = 500
header_height = 100
center = game_width / 2
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
    'first_page': (50, 117, 168),
    'winner': (255, 255, 255),
    'player': (242, 241, 148)
}
screen = pygame.display.set_mode((game_width, screen_height))
pygame.display.flip()

player_thick = 12
line_thickness = 7
winner_thick = 15

# game setup values
running = True
game_mode = None
player1 = 1
player2 = 2
currentPlayer = player1
winner = None
n = 3
square = game_width / n
scores = {1: 1, 2: -1, 'tie': 0}

# text setup
pygame.font.init()
Font = pygame.font.SysFont('cooperblack', 30)

class Box:
    def __init__(self, center_point, i, width, height, color):
        self.x1 = center_point - box_width / 2
        self.y1 = box_height * (i + 0.75)
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


class Model:
    def __init__(self):
        self.board = np.zeros((n, n))
        self.winner = winner

    def checkEmpty(self, i, j):
        return self.board[i][j] == 0

    def claimSpot(self, i, j, player):
        self.board[i][j] = player

    def checkWin(self):
        if self.board[0][0] == self.board[0][1] == self.board[0][2] != 0:
            self.winner = self.board[0][0]
        elif self.board[1][0] == self.board[1][1] == self.board[1][2] != 0:
            self.winner = self.board[1][0]
        elif self.board[2][0] == self.board[2][1] == self.board[2][2] != 0:
            self.winner = self.board[2][0]
        elif self.board[0][0] == self.board[1][0] == self.board[2][0] != 0:
            self.winner = self.board[0][0]
        elif self.board[0][1] == self.board[1][1] == self.board[2][1] != 0:
            self.winner = self.board[0][1]
        elif self.board[0][2] == self.board[1][2] == self.board[2][2] != 0:
            self.winner = self.board[0][2]
        elif self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            self.winner = self.board[0][0]
        elif self.board[2][0] == self.board[1][1] == self.board[0][2] != 0:
            self.winner = self.board[2][0]
        elif 0 not in self.board:
            self.winner = "tie"
        else:
            self.winner = None

    def restart(self):
        self.winner = None
        self.board = np.zeros((n, n))

    def findFreeSpot(self):
        availableSquare = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    availableSquare.append([i, j])
        return availableSquare

    def randomComputer(self):
        # if len(self.findFreeSpot()) > 0 :
            x = random.randint(0, len(self.findFreeSpot()) - 1)
            row, column = self.findFreeSpot()[x]
            return row, column

    def isGameEnd(self):
        self.checkWin()
        if self.winner is not None:
            return True

    def minimax(self, board, depth, isMaximizing):
        if self.isGameEnd():
            score = scores[self.winner]
            self.winner = None
            return score
        if isMaximizing:
            bestScore = -100
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = player1
                        score = self.minimax(self.board, depth + 1, False)
                        board[i][j] = 0
                        if score > bestScore:
                            bestScore = score
            return bestScore

        else:
            bestScore = 100
            for i in range(3):
                for j in range(3):
                    if board[i][j] == 0:
                        board[i][j] = player2
                        score = self.minimax(self.board, depth + 1, True)
                        board[i][j] = 0
                        if score < bestScore:
                            bestScore = score
            return bestScore

    def bestMove(self):
        bestScore = 100
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 0:
                    self.board[i][j] = player2
                    score = self.minimax(self.board, 0, True)
                    self.board[i][j] = 0
                    if score < bestScore:
                        bestScore = score
                        row, column = i, j
        return row, column

class View:
    def select_game_mode(self):
        screen.fill(colors['bg'])
        text_select_pvp = Font.render('PVP', True, colors['first_page'], colors['yellow'])
        text_select_easy = Font.render('vs Random', True, colors['first_page'], colors['orange'])
        text_select_hard = Font.render('vs Smarty', True, colors['first_page'], colors['red'])
        box1.drawBox(screen)
        box2.drawBox(screen)
        box3.drawBox(screen)
        screen.blit(text_select_game_mode, (center - text_select_game_mode.get_rect().width / 2, box_height))
        screen.blit(text_select_pvp, (center - text_select_pvp.get_rect().width / 2, box_height * 2))
        screen.blit(text_select_easy, (center - text_select_easy.get_rect().width / 2, box_height * 3))
        screen.blit(text_select_hard, (center - text_select_hard.get_rect().width / 2, box_height * 4))
        pygame.display.flip()

    def game_start(self, game_mode):
        screen.fill(colors['bg'])
        self.text_current_turn = Font.render("", True, colors['header'], colors['bg'])
        pygame.draw.line(screen, colors['line'], (game_width / 3, header_height), (game_width / 3, screen_height),
                         line_thickness)
        pygame.draw.line(screen, colors['line'], (game_width / 1.5, header_height), (game_width / 1.5, screen_height),
                         line_thickness)
        pygame.draw.line(screen, colors['line'], (0, (game_height / 3) + header_height),
                         (game_width, (game_height / 3) + header_height), line_thickness)
        pygame.draw.line(screen, colors['line'], (0, (game_height / 1.5) + header_height),
                         (game_width, (game_height / 1.5) + header_height), line_thickness)
        pygame.draw.line(screen, colors['header'], (0, header_height), (game_width, header_height), line_thickness * 2)
        text_game_mode = Font.render(game_mode, True, colors['header'], colors['bg'])
        screen.blit(text_game_mode, (margin, margin / 2))
        pygame.display.flip()

    def change_turn(self, currentPlayer):
        text_current_turn = Font.render('Turn : Player ' + str(currentPlayer), True, colors['header'], colors['bg'])
        screen.blit(text_current_turn, (margin, header_height - 50))
        pygame.display.flip()


    def draw_claimed(self, board):
        for i in range(n):
            for j in range(n):
                if board[i][j] == 1:
                    x_start1 = (square * j + margin, square * i + margin + header_height)
                    x_end1 = (square * (j + 1) - margin, square * (i + 1) - margin + header_height)
                    x_start2 = (square * j + margin, square * (i + 1) - margin + header_height)
                    x_end2 = (square * (j + 1) - margin, square * i + margin + header_height)
                    pygame.draw.line(screen, colors['player'], x_start1, x_end1, player_thick + 3)
                    pygame.draw.line(screen, colors['player'], x_start2, x_end2, player_thick + 3)
                elif board[i][j] ==2:
                    o_center = (square * (j + 0.5), square * (i + 0.5) + header_height)
                    pygame.draw.circle(screen, colors['player'], o_center, game_width / 7, player_thick)
        pygame.display.flip()

    def draw_winner(self, board):
        if board[0][0] == board[0][1] == board[0][2] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 0, square * 0.5 + header_height),
                             (square * 3, square * 0.5 + header_height), winner_thick)
        elif board[1][0] == board[1][1] == board[1][2] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 0, square * 1.5 + header_height),
                             (square * 3, square * 1.5 + header_height), winner_thick)
        elif board[2][0] == board[2][1] == board[2][2] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 0, square * 2.5 + header_height),
                             (square * 3, square * 2.5 + header_height), winner_thick)
        elif board[0][0] == board[1][0] == board[2][0] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 0.5, square * 0 + header_height),
                             (square * 0.5, square * 3 + header_height), winner_thick)
        elif board[0][1] == board[1][1] == board[2][1] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 1.5, square * 0 + header_height),
                             (square * 1.5, square * 3 + header_height), winner_thick)
        elif board[0][2] == board[1][2] == board[2][2] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 2.5, square * 0 + header_height),
                             (square * 2.5, square * 3 + header_height), winner_thick)
        elif board[0][0] == board[1][1] == board[2][2] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 0, square * 0 + header_height),
                             (square * 3, square * 3 + header_height), winner_thick)
        elif board[2][0] == board[1][1] == board[0][2] != 0:
            pygame.draw.line(screen, colors['winner'], (square * 3, square * 0 + header_height),
                             (square * 0, square * 3 + header_height), winner_thick)
        pygame.display.flip()

class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()
        self.running = running
        self.game_mode = game_mode
        self.currentPlayer = currentPlayer

    def run(self):
        while (self.running):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if self.game_mode is None and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if box1.checkPos(mouse):
                        self.game_mode = 'Game mode: PVP'
                        self.view.game_start(self.game_mode)
                        self.view.change_turn(self.currentPlayer)
                    elif box2.checkPos(mouse):
                        self.game_mode = 'Game mode: Random Computer'
                        self.view.game_start(self.game_mode)
                    elif box3.checkPos(mouse):
                        self.game_mode = 'Game mode: Smart'
                        self.view.game_start(self.game_mode)
                elif self.game_mode == 'Game mode: PVP' and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    row = int((mouse[1] - header_height) / square)
                    column = int(mouse[0] / square)
                    if self.model.checkEmpty(row, column) and self.model.winner is None:
                        self.model.claimSpot(row, column, self.currentPlayer)
                        self.view.draw_claimed(self.model.board)
                        self.model.checkWin()
                        self.view.draw_winner(self.model.board)
                        self.currentPlayer = self.currentPlayer % 2 + 1
                        self.view.change_turn(self.currentPlayer)
                        pygame.display.flip()
                        print(self.model.board)
                    elif self.model.winner is not None:
                        self.model.restart()
                        self.view.select_game_mode()
                        self.game_mode = None
                        self.currentPlayer = player1
                        print(self.model.board)
                elif self.game_mode == 'Game mode: Random Computer' and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    row = int((mouse[1] - header_height) / square)
                    column = int(mouse[0] / square)
                    if self.model.checkEmpty(row, column) and self.model.winner is None:
                        self.model.claimSpot(row, column, self.currentPlayer)
                        self.view.draw_claimed(self.model.board)
                        self.model.checkWin()
                        self.view.draw_winner(self.model.board)
                        print(self.model.board)
                        if self.model.winner is None:
                            row, column = self.model.randomComputer()
                            self.model.claimSpot(row, column, player2)
                            self.view.draw_claimed(self.model.board)
                            self.model.checkWin()
                            self.view.draw_winner(self.model.board)
                            print(self.model.board)
                    elif self.model.winner is not None:
                        self.model.restart()
                        self.view.select_game_mode()
                        self.game_mode = None
                        self.currentPlayer = player1
                        print(self.model.board)
                elif self.game_mode == 'Game mode: Smart' and event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    row = int((mouse[1] - header_height) / square)
                    column = int(mouse[0] / square)
                    if self.model.checkEmpty(row, column) and self.model.winner is None:
                        self.model.claimSpot(row, column, self.currentPlayer)
                        self.view.draw_claimed(self.model.board)
                        self.model.checkWin()
                        self.view.draw_winner(self.model.board)
                        print(self.model.board)
                        if self.model.winner is None:
                            row, column = self.model.bestMove()
                            self.model.claimSpot(row, column, player2)
                            self.view.draw_claimed(self.model.board)
                            self.model.checkWin()
                            self.view.draw_winner(self.model.board)
                            print(self.model.board)
                    elif self.model.winner is not None:
                        self.model.restart()
                        self.view.select_game_mode()
                        self.game_mode = None
                        self.currentPlayer = player1
                        print(self.model.board)
                elif self.game_mode is None:
                    self.view.select_game_mode()
                    mouse = pygame.mouse.get_pos()
                    if box1.checkPos(mouse) or box2.checkPos(mouse) or box3.checkPos(mouse):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.model.restart()
                    self.view.select_game_mode()
                    self.game_mode = None
                    self.currentPlayer = player1


if __name__ == '__main__':
    c = Controller()
    c.run()
