class UndoController:
    def __init__(self):
        self._operations = []
        self._index = -1
        self._CF = False

    def addOperation(self, operation):
        if self._CF == True:
            return 

        if self._index < len(self._operations):
            self._operations = self._operations[:self._index + 1]
        self._index += 1
        self._operations.append(operation)

    def undo(self):
        if self._index < 0:
            raise ValueError("No more undos!")
            
        self._CF = True
        self._operations[self._index].undo()
        self._CF = False
        self._index -= 1
        return True
    
    def redo(self):
        if self._index + 1 >= len(self._operations):
            raise ValueError("No more redos!")
            
        self._index += 1
        self._CF = True
        self._operations[self._index].redo()
        self._CF = False
        return True
