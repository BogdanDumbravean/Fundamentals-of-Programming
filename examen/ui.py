import sys

class UI:
    def __init__(self, board):
        self.board = board

    def placePattern(self, cmd):
        if len(cmd) != 3:
            raise ValueError("Not a valid command!")

        ok = False  
        for p in self.board.patterns:       # check if pattern exists in textfile
            if cmd[1] in p:
                ok = True
                break
        if not ok:
            raise ValueError("Not a valid command! Not a pattern")

        pos = cmd[2].split(',')
        if len(pos) != 2:
            raise ValueError("Not a valid command! Not a good position")

        x = 0
        y = 0
        try:
            x = int(pos[0])
            y = int(pos[1])
        except:
            raise ValueError("Not a valid command! Position is made of two numbers")

        self.board.placePattern(cmd[1], x, y)

    def tick(self, cmd):
        n = 1
        if len(cmd) == 1:
            n = 1
        elif len(cmd) != 2:
            raise ValueError("Not a Valid Command!")
        else:
            try:
                n = int(cmd[1])
            except:
                raise ValueError("Not a Valid Command! Must be an int")
        if n < 0:
            raise ValueError("Not a Valid Command! Number of steps must be positive")

        self.board.tick(n)

    def saveGame(self, cmd):
        if len(cmd) != 2:
            raise ValueError("Not a Valid Command!")
        f = open(cmd[1], 'w+')
        for i in self.board.data:
            for j in i:
                f.write(str(j))
        f.close()

    def loadGame(self, cmd):
        if len(cmd) != 2:
            raise ValueError("Not a Valid Command!")
        f = 0
        f = open(cmd[1], 'r')
        line = f.read()
        i = 0
        for c in line:
            self.board.data[i // 8][i % 8] = int(c)
            i += 1

    def read(self):
        while True:
            print(self.board)
            cmd = input().split()
            d = {"place":self.placePattern, "tick":self.tick, "save":self.saveGame, "load":self.loadGame}

            if cmd[0] == "exit":               # Exit program
                return

            if cmd[0] not in d:
                print("Not a valid command!")
                continue
            try:
                d[cmd[0]](cmd)
            except Exception as e:
                print(e.args[0])

