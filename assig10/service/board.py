import copy
import sys
sys.path.append('d:\\Info\\Proiecte Info\\python\\FP\\assig10\\')
from domain import *
from texttable import Texttable

class Board():
    '''
    0 - empty square
    1 - X
    2 - O
    '''
    def __init__(self):
        self._data = []
        for i in range(15):
            aux = [0] * 15
            self._data.append(aux)

    def copy(self):
        b = Board()
        b._data = copy.deepcopy(self._data)
        return b

    def getValAtPos(self, square):
        '''
        0 - empty
        1 - X
        2 - O
        '''
        return self._data[square.row][square.col]

    def getSquaresWithVal(self, val):
        '''
        Return a list of squares with the given value (0, 1, 2)
        '''
        res = []
        for i in range(15):
            for j in range(15):
                if self._data[i][j] == val:
                    res.append(Square(i, j))
        return res

    def isWon(self):
        d = self._data
        
        for x in range(15):
            for y in range(15):
                pline = -1
                pcol = -1
                pdiag1 = -1
                pdiag2 = -1
                if x < 11:
                    pcol = 1
                    for i in range(5):
                        pcol *= d[x + i][y]
                    if y > 3:
                        pdiag1 = 1
                        for i in range(5):
                            pdiag1 *= d[x + i][y - i]
                    if y < 11:
                        pdiag2 = 1
                        for i in range(5):
                            pdiag2 *= d[x + i][y + i]
                if y < 11:
                    pline = 1
                    for i in range(5):
                        pline *= d[x][y + i]
                
                if pline in [1, 32] or pdiag1 in [1, 32] or pcol in [1, 32] or pdiag2 in [1, 32]:
                    return True
        
        return False

    def move(self, square, symbol):
        '''
        square - Square instance
        symbol - One of X, O, ' '
        '''
        if square.row not in range(15) or square.col not in range(15):
            raise GameException("Move outside board!")
        if symbol not in ['X', 'O', ' ']:
            raise GameException("Invalid symbol!")
        d = self._data
        if d[square.row][square.col] != 0 and symbol != ' ':
            raise GameException("Square already occupied!")

        ds = {'X':1, 'O':2, ' ':0}
        d[square.row][square.col] = ds[symbol]

    def __str__(self):
        t = Texttable()
        t.header([' ', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'])
        d = {0:' ', 1:'X', 2:'O'}

        for i in range(15):
            lst = self._data[i][:]
            for j in range(15):
                lst[j] = d[lst[j]]
            t.add_row([i + 1] + lst)

        return t.draw()

import unittest

class test_Board(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test(self):
        self.assertFalse(self.board.isWon())
        self.board.move(Square(1, 1), 'X')
        self.board.move(Square(2, 2), 'X')
        self.board.move(Square(3, 3), 'X')
        self.board.move(Square(4, 4), 'X')
        self.board.move(Square(5, 5), 'X')
        self.assertTrue(self.board.isWon())
        self.assertEqual(len(self.board.getSquaresWithVal(1)), 5)

if __name__ == "__main__":
    unittest.main()