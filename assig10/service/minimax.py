from domain.square import Square
from random import choice

class MinimaxGomoku:
    def __init__(self, board):
        self._board = board

    def _getMoves(self):
        moves = []  

        for option in self._board.getSquaresWithVal(0):     # Get squares near 'X' or 'O'
            for k in range(9):
                i = k // 3 - 1
                j = k % 3 - 1
                if option.row + i not in range(0, 15) or option.col + j not in range(0, 15):
                    continue
                if self._board.getValAtPos(Square(option.row + i, option.col + j)) != 0:
                    moves.append(option)
                    break
        
        return moves

    def _gomokuShapeScore(self, consecutive, openEnds, currentTurn):
        if openEnds == 0 and consecutive < 5:
            return 0
        if consecutive == 4:
            if openEnds == 1:
                if currentTurn:
                    return 100000000
                return 50
            elif openEnds == 2:
                if currentTurn:
                    return 100000000
                return 500000
            
        elif consecutive == 3:
            if openEnds == 1:
                if currentTurn:
                    return 7
                return 5
            elif openEnds == 2:
                if currentTurn:
                    return 10000
                return 50
            
        elif consecutive == 2:
            if openEnds == 1:
                return 2
            elif openEnds == 2:
                return 5
            
        elif consecutive == 1:
            if openEnds == 1:
                return 0.5
            elif openEnds == 2:
                return 1
        else:
            return 200000000

    def _analyzeHorizontal(self, computerTurn, symbolNr):
        '''
        computerTurn - bool
        symbolNr - 1 or 2
        '''
        score = 0
        countConsecutive = 0
        openEnds = 0

        for i in range(15):
            for j in range(15):         # Board has 15x15 squares
                if (self._board.getValAtPos(Square(i, j)) == symbolNr):
                    countConsecutive += 1
                elif (self._board.getValAtPos(Square(i, j)) == 0 and countConsecutive > 0):
                    openEnds += 1
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 1
                elif (self._board.getValAtPos(Square(i, j)) == 0):
                    openEnds = 1
                elif (countConsecutive > 0):
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 0
                else: 
                    openEnds = 0
            
            if (countConsecutive > 0):
                score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
            countConsecutive = 0
            openEnds = 0
        
        return score

    def _analyzeVertical(self, computerTurn, symbolNr):
        '''
        computerTurn - bool
        symbolNr - 1 or 2
        '''
        score = 0
        countConsecutive = 0
        openEnds = 0

        for i in range(15):
            for j in range(15):         # Board has 15x15 squares
                if (self._board.getValAtPos(Square(j, i)) == symbolNr):
                    countConsecutive += 1
                elif (self._board.getValAtPos(Square(j, i)) == 0 and countConsecutive > 0):
                    openEnds += 1
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 1
                elif (self._board.getValAtPos(Square(j, i)) == 0):
                    openEnds = 1
                elif (countConsecutive > 0):
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 0
                else: 
                    openEnds = 0
            
            if (countConsecutive > 0):
                score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
            countConsecutive = 0
            openEnds = 0
        
        return score

    def _analyzePrimaryDiagonal(self, computerTurn, symbolNr):
        '''
        computerTurn - bool
        symbolNr - 1 or 2
        '''
        score = 0
        countConsecutive = 0
        openEnds = 0

        # Get the values above the diagonal and on the diagonal
        for a in range(11):
            i = 0
            j = a
            for b in range(15 - a):
                if (self._board.getValAtPos(Square(i, j)) == symbolNr):
                    countConsecutive += 1
                elif (self._board.getValAtPos(Square(i, j)) == 0 and countConsecutive > 0):
                    openEnds += 1
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 1
                elif (self._board.getValAtPos(Square(i, j)) == 0):
                    openEnds = 1
                elif (countConsecutive > 0):
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 0
                else: 
                    openEnds = 0
                    
                i += 1
                j += 1
            
            if (countConsecutive > 0):
                score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
            countConsecutive = 0
            openEnds = 0

        # Get the values below the diagonal
        for a in range(1, 11):              # Go only where it's possible to get 5
            i = a
            for j in range(15 - a):         # Board has 15x15 squares
                if (self._board.getValAtPos(Square(i, j)) == symbolNr):
                    countConsecutive += 1
                elif (self._board.getValAtPos(Square(i, j)) == 0 and countConsecutive > 0):
                    openEnds += 1
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 1
                elif (self._board.getValAtPos(Square(i, j)) == 0):
                    openEnds = 1
                elif (countConsecutive > 0):
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 0
                else: 
                    openEnds = 0

                i += 1
            
            if (countConsecutive > 0):
                score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
            countConsecutive = 0
            openEnds = 0
        
        return score

    def _analyzeSecondaryDiagonal(self, computerTurn, symbolNr):
        '''
        computerTurn - bool
        symbolNr - 1 or 2
        '''
        score = 0
        countConsecutive = 0
        openEnds = 0

        # Above and on diagonal
        for a in range(4, 15):          # Go only where it's possible to get 5
            i = 0
            j = a
            for b in range(a):         # Board has 15x15 squares
                if (self._board.getValAtPos(Square(i, j)) == symbolNr):
                    countConsecutive += 1
                elif (self._board.getValAtPos(Square(i, j)) == 0 and countConsecutive > 0):
                    openEnds += 1
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 1
                elif (self._board.getValAtPos(Square(i, j)) == 0):
                    openEnds = 1
                elif (countConsecutive > 0):
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 0
                else: 
                    openEnds = 0

                i += 1
                j -= 1
            
            if (countConsecutive > 0):
                score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
            countConsecutive = 0
            openEnds = 0

        # Below the diagonal
        for a in range(1, 11):          # Go only where it's possible to get 5
            i = a
            j = 14
            for b in range(15 - a):         # Board has 15x15 squares
                if (self._board.getValAtPos(Square(i, j)) == symbolNr):
                    countConsecutive += 1
                elif (self._board.getValAtPos(Square(i, j)) == 0 and countConsecutive > 0):
                    openEnds += 1
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 1
                elif (self._board.getValAtPos(Square(i, j)) == 0):
                    openEnds = 1
                elif (countConsecutive > 0):
                    score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
                    countConsecutive = 0
                    openEnds = 0
                else: 
                    openEnds = 0

                i += 1
                j -= 1
            
            if (countConsecutive > 0):
                score += self._gomokuShapeScore(countConsecutive, openEnds, computerTurn)
            countConsecutive = 0
            openEnds = 0
        
        return score

    def _analyzeGomoku(self, computerTurn, symbol):
        ds = {'X':1, 'O':2}
        val = ds[symbol]
        return self._analyzeHorizontal(computerTurn, val) + self._analyzeVertical(computerTurn, val) + self._analyzePrimaryDiagonal(computerTurn, val) + self._analyzeSecondaryDiagonal(computerTurn, val)
    
    def moveComputerMinimax(self, computerTurn, computerSymbol, playerSymbol, depth):
        '''
        computerTurn - bool
        computerSymbol, playerSymbol - 'O'(2) and 'X'(1)
        depth - int
        '''
        color = ''
        bestScore = 0
        if computerTurn:
            color = computerSymbol
            bestScore = 1000000000
        else:
            color = playerSymbol
            bestScore = -1000000000

        bestMove = Square(-1, -1)
        analysis = 0
        moves = self._getMoves()
        goodMoves = []
        for i in range(len(moves) - 1, -1, -1):
            self._board.move(moves[i], color)
            if depth == 1:
                analysis = self._analyzeGomoku(computerTurn, color)
            else:
                if self._board.isWon():
                    return [bestMove, bestScore]
                response = self.moveComputerMinimax(not computerTurn, computerSymbol, playerSymbol, depth - 1)
                analysis = response[1]
            
            self._board.move(moves[i], ' ')
            if (analysis < bestScore and computerTurn) or (analysis > bestScore and not computerTurn):
                bestScore = analysis
                bestMove = moves[i]
                goodMoves.append(moves[i])
            elif analysis == bestScore:
                goodMoves.append(moves[i])

        theBestScore = -1000000000
        for move in goodMoves:
            self._board.move(moves[i], color)
            analysis = self._analyzeGomoku(computerTurn, color)
            if analysis > theBestScore:
                bestMove = move
            self._board.move(moves[i], ' ')
        return [bestMove, bestScore]