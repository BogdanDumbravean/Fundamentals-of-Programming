from texttable import Texttable
import sys
from copy import deepcopy

class Board:
    def __init__(self):
        self.data = []
        for i in range(8):
            self.data.append([0]*8)
        self.patterns = []
        self.loadPatterns()

    def loadPatterns(self):
        '''
        Reads the patterns from the file
        '''
        f = open(sys.path[0] + "\\patterns.txt", 'r')
        line = f.readline()
        while len(line) > 2:
            self.patterns.append(line.split())
            line = f.readline()
        f.close()

    def placePattern(self, pattern, x, y):
        '''
        Places a pattern on the board at pos <x,y>
        Input:  pattern - string with name of pattern
                x - row of start position
                y - column of start position
        '''
        for p in self.patterns:
            if p[0] == pattern:
                pattern = p
                break

        n = int(pattern[1])
        m = int(pattern[2])
        pattern = pattern[3:]

        for i in range(n):
            for j in range(m):
                if pattern[i * m + j] == '1' and x+i > 7 or y+j > 7:
                    raise ValueError("Move Outside Board")
                elif pattern[i * m + j] == '1' and self.data[x+i][y+j] == 1:
                    raise ValueError("Overlaping")
        # if it's fine, place pattern
        for i in range(n):
            for j in range(m):
                if(pattern[i*m + j] == '1'):
                    self.data[x+i][y+j] = int(pattern[i * m + j])

        return True

    def tick(self, n):
        '''
        Makes n updates to the matrix
        Input:  n - number of updates to make
        '''
        for pas in range(n):
            b = deepcopy(self.data)
            for i in range(8):
                for j in range(8):  # go through all items of matrix
                    c = 0
                    for ik in range(-1, 2):
                        for jk in range(-1, 2):     # check neighbours
                            if ik == 0 and jk == 0:
                                continue

                            inou = i + ik
                            jnou = j + jk
                            if inou in range(8) and jnou in range(8) and self.data[inou][jnou] == 1:      # count alive cells
                                c += 1

                    if self.data[i][j] == 1 and c < 2 or c > 3:
                        b[i][j] = 0
                    elif self.data[i][j] == 0 and c == 3:
                        b[i][j] = 1
            self.data = b

        return True

    def __str__(self):
        t = Texttable()
        aux = {0:' ', 1:'X'}
        for i in self.data:
            line = []
            for j in i:
                line.append(aux[j])
            t.add_row(line)

        return t.draw()

import unittest

class test(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_place(self):
        self.assertTrue(self.board.placePattern("beacon", 0, 0))
        self.assertTrue(self.board.placePattern("blinker", 0, 2))
        self.assertTrue(self.board.placePattern("block", 4, 4))
        self.assertRaises(ValueError, self.board.placePattern, "point", 0, 0)
        self.assertRaises(ValueError, self.board.placePattern, "beacon", 5, 5)

    def test_tick(self):
        self.board.placePattern("blinker", 0, 0)
        self.assertTrue(self.board.tick(1))
        self.assertRaises(ValueError, self.board.placePattern, "point", 0, 1)
        self.assertTrue(self.board.tick(2))
        self.assertTrue(self.board.tick(3))

if __name__ == "__main__":
    unittest.main()