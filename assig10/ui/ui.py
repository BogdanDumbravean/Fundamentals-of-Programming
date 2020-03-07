from domain.square import Square 

class UI:
    def __init__(self, g):
        self._game = g

    def _readMove(self): 
        while True:
            try:
                tokens = input("Enter move >> ").split(' ')
                if len(tokens) != 2:
                    raise ValueError
                x = int(tokens[1]) - 1
                y = ord(tokens[0]) - ord('A')
                self._game._board.copy().move(Square(x, y), 'X')
                return Square(int(x), int(y))                
            except Exception:
                print("Invalid move!")

    def _getDifficulty(self):
        '''
        Get difficulty from player
        1 - Easy
        2 - Hard
        '''
        ok = False
        while not ok:
            print("Difficulty: \n1 - Easy \n2 - Hard")
            try:
                diff = int(input("Enter difficulty: "))
            except Exception as e:
                print(e.args[0])
                continue
            if diff != 1 and diff != 2:
                print("Incorrect Input!")
                continue
            ok = True
        return diff

    def start(self):
        b = self._game.board

        playerSymbol = 'X'
        computerSymbol = 'O'

        self._game.setDifficulty(self._getDifficulty())

        playerMove = True
        while not b.isWon():
            print(b)
            if playerMove:
                move = self._readMove()
                try:
                    self._game.moveHuman(move, playerSymbol)
                except Exception as e:
                    print(e.args[0])
            else:
                self._game.moveComputer(computerSymbol, playerSymbol)
            playerMove = not playerMove
        
        print("Game over!")
        print(b)
        if playerMove == True:
            print("Computer wins!")
        else:
            print("Player wins!")