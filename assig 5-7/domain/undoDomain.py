class CascadeOperation:
    def __init__(self):
        self._operations = []

    def add(self, op):
        self._operations.append(op)

    def undo(self):
        for o in self._operations:
            o.undo()

    def redo(self):
        for o in self._operations:
            o.redo()

class Operation:
    def __init__(self, undoFunction, redoFunction):
        self._undoFunction = undoFunction
        self._redoFunction = redoFunction

    def undo(self):
        self._undoFunction.call()

    def redo(self):
        self._redoFunction.call()

class FunctionCall:
    def __init__(self, function, *params):
        self._func = function
        self._params = params

    def call(self):
        self._func(*self._params)