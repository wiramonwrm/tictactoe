import unittest
import random
from MVC import n, Model, player1, player2

class Test(unittest.TestCase):
    def test_checkEmpty(self):
        model = Model()
        for i in range(n):
            for j in range(n):
                self.assertTrue(model.checkEmpty(i, j))
        model.board[1][0] = 1
        model.board[0][1] = 1
        model.board[1][1] = 1
        model.board[2][0] = 1
        self.assertFalse(model.checkEmpty(1,0))
        self.assertFalse(model.checkEmpty(0,1))
        self.assertFalse(model.checkEmpty(1,1))
        self.assertFalse(model.checkEmpty(2,0))

    def test_claimSpot(self):
        model = Model()
        for i in range(n):
            for j in range(n):
                model.claimSpot(i, j, player1)
                self.assertEqual(model.board[i][j], 1)
        for i in range(n):
            for j in range(n):
                model.claimSpot(i, j, player2)
                self.assertEqual(model.board[i][j], 2)

    def test_checkWin(self):
        model = Model()
        for i in range(n):
            model.board[0][i] = model.board[1][i] = model.board[2][i] = player1
            model.checkWin()
            self.assertEqual(model.winner, player1)
            model.board[0][i] = model.board[1][i] = model.board[2][i] = 0
            model.checkWin()
            self.assertEqual(model.winner, None)
        for j in range(n):
            model.board[j][0] = model.board[j][1] = model.board[j][2] = player2
            model.checkWin()
            self.assertEqual(model.winner, player2)
            model.board[j][0] = model.board[j][1] = model.board[j][2] = 0
            model.checkWin()
            self.assertEqual(model.winner, None)
        model.board[0][0] = model.board[1][1] = model.board[2][2] = player1
        model.checkWin()
        self.assertEqual(model.winner, player1)
        model.board[0][0] = model.board[1][1] = model.board[2][2] = 0
        model.checkWin()
        self.assertEqual(model.winner, None)
        model.board[0][2] = model.board[1][1] = model.board[2][0] = player2
        model.checkWin()
        self.assertEqual(model.winner, player2)
        model.board[0][2] = model.board[1][1] = model.board[2][0] = 0
        model.checkWin()
        self.assertEqual(model.winner, None)
        #Corner not winner
        model.board[0][0] = model.board[0][2] = model.board[2][0] = model.board[2][2] = player1
        model.checkWin()
        # print(model.board)
        self.assertEqual(model.winner, None)
        model.board[0][1] = model.board[1][0] = model.board[1][2] = model.board[2][1] = player2
        # print(model.board)
        model.checkWin()
        self.assertEqual(model.winner, None)

    def test_findFreeSpot(self):
        model = Model()
        taken = random.randint(0, 3)
        for i in range(taken):
            for j in range(taken):
                model.board[i][j] = 1
        print(model.board)
        print((model.findFreeSpot()))
        self.assertEqual(len(model.findFreeSpot()), 9 - taken**2)


    def test_restart(self):
        model = Model()
        for i in range(3):
            for j in range(3):
                model.board[i][j] = random.randint(1, 2)
                model.currentPlayer = player2
        model.restart()
        for i in range(3):
            for j in range(3):
                self.assertEqual(model.board[i][j], 0)

if __name__ == '__main__':
    unittest.main()