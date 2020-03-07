from random import choice
import sys
sys.path.append('d:\\Info\\Proiecte Info\\python\\FP\\assig10\\')
from domain import *
from service.minimax import MinimaxGomoku

class Game:
    def __init__(self, board):
        '''
        diff -  1 - Easy
                2 - Hard
        '''
        self._board = board
        self._difficulty = 1
        self._minimax = MinimaxGomoku(board)

    @property
    def board(self):
        return self._board

    def setDifficulty(self, val):
        '''
        1 - Easy
        2 - Hard
        '''
        self._difficulty = val

    def moveHuman(self, square, symbol): 
        self.board.move(square, symbol)

    def moveComputer(self, computerSymbol, playerSymbol):
        if self._difficulty == 2:
            aux = self._minimax.moveComputerMinimax(True, computerSymbol, playerSymbol, 2)[0]
            self.board.move(aux, computerSymbol)
            return aux
            
        options = self._board.getSquaresWithVal(0)
        if len(options) == 0:
            raise GameException("Board is full!")

        randomMove = []  # Use lastly for a random move near the play area

        ds = {'X':1, 'O':2}
        for option in self._board.getSquaresWithVal(ds[computerSymbol]):
            '''
            1. create copy
            2. try move
            3. check for win 
            '''
            b = self.board.copy()
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        aux = Square(option.row + i, option.col + j)
                        b.move(aux, computerSymbol)
                        if b.isWon():
                            self.board.move(aux, computerSymbol)
                            return aux
                        randomMove.append(aux)
                    except Exception:
                        pass

        '''
        Prevent human win!
        '''
        for option in self._board.getSquaresWithVal(ds[playerSymbol]):
            '''
            1. create copy
            2. try move
            3. check for win
            '''
            for i in range(-1, 2):
                for j in range(-1, 2):
                    try:
                        aux = Square(option.row + i, option.col + j)
                        b.move(aux, playerSymbol)
                        if b.isWon():
                            self.board.move(aux, computerSymbol)
                            return aux
                        randomMove.append(aux)
                    except Exception:
                        pass

        if len(randomMove) != 0:
            aux = choice(randomMove)
            self.board.move(aux, computerSymbol)
            return aux
        else:
            aux = choice(options)
            self.board.move(aux, computerSymbol)
            return aux


import unittest
from service.board import Board

class test_Board(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.game = Game(self.board)

    def test(self):
        self.assertFalse(self.board.isWon())
        self.game.moveHuman(Square(1, 5), 'O')
        self.game.moveComputer('X', 'O')
        self.game.moveComputer('X', 'O')
        self.game.moveComputer('X', 'O')
        self.assertEqual(len(self.board.getSquaresWithVal(1)), 3)
        self.assertEqual(len(self.board.getSquaresWithVal(2)), 1)

if __name__ == "__main__":
    unittest.main()