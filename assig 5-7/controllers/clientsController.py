from domain.client import Client
from domain.undoDomain import *

class ClientsController:
    def __init__(self, repository, rentalController, undoController, validator):
        self._repository = repository
        self._validator = validator
        self._rentalCtrl = rentalController
        self._undoCtrl = undoController

    def getRepository(self):
        '''
        Returns specific repository
        '''
        return self._repository

    def add(self, clientID, name):
        b = Client(clientID, name)
        self._validator.validate(b)
        self._repository.add(b)

        undo = FunctionCall(self.remove, clientID)
        redo = FunctionCall(self.add, clientID, name)
        oper = Operation(undo, redo)
        self._undoCtrl.addOperation(oper)
        return True

    def remove(self, id, removeRentals = False):
        if id < 0:
            raise ValueError("ID must be a natural number!")
        client = self._repository.remove(id)
        if not removeRentals:
            return client

        rentals = self._rentalCtrl.searchByClientID(id)
        for rental in rentals:
            self._rentalCtrl.remove(rental.getID())
        # Record Undo/Redo
        undo = FunctionCall(self.add, id, client.getName())
        redo = FunctionCall(self.remove, id)
        oper = Operation(undo, redo)
        co = CascadeOperation()
        co.add(oper)
        for r in rentals:
            params = [r.getID(), r.getBookID(), r.getClientID(), r.getRentedDate(), r.getDueDate(), r.getReturnedDate()]
            undo = FunctionCall(self._rentalCtrl.add, params[0], params[1], params[2], params[3], params[4], params[5])
            redo = FunctionCall(self._rentalCtrl.remove, r.getID())
            oper = Operation(undo, redo)
            co.add(oper)
        self._undoCtrl.addOperation(co)
        return client

    def update(self, clientID, name):
        c = Client(clientID, name)
        self._validator.validate(c)
        oldName = self._repository.searchByID(clientID).getName()
        self._repository.update(clientID, c)

        undo = FunctionCall(self.update, clientID, oldName)
        redo = FunctionCall(self.update, clientID, name)
        oper = Operation(undo, redo)
        self._undoCtrl.addOperation(oper)
        return True

    # ===================================================== Partial search
    def partialSearchID(self, string):
        newList = []
        for item in self._repository.getAll():
            if string.lower() in str(item.getID()).lower():
                newList.append(item)
        return newList
    def partialSearchName(self, string):
        newList = []
        for item in self._repository.getAll():
            if string.lower() in item.getName().lower():
                newList.append(item)
        return newList