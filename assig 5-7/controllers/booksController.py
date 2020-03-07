from domain.book import Book
from domain.undoDomain import *
from assig9 import filter

class BooksController:
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
    
    def add(self, bookID, title, author, description):
        b = Book(bookID, title, author, description)
        self._validator.validate(b)
        self._repository.add(b)

        undo = FunctionCall(self.remove, bookID)
        redo = FunctionCall(self.add, bookID, title, author, description)
        oper = Operation(undo, redo)
        self._undoCtrl.addOperation(oper)
        return True

    def remove(self, id, removeRentals = False):
        if id < 0:
            raise ValueError("ID must be a natural number!")
        book = self._repository.remove(id)
        if not removeRentals:
            return book

        rentals = self._rentalCtrl.searchByBookID(id)
        for rental in rentals:
            self._rentalCtrl.remove(rental.getID())
        # Record Undo/Redo
        undo = FunctionCall(self.add, id, book.getTitle(), book.getAuthor(), book.getDescription())
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
        return book

    def update(self, id, title, author, description):
        b = Book(id, title, author, description)
        self._validator.validate(b)
        oldB = self._repository.searchByID(id)
        params = [oldB.getTitle(), oldB.getAuthor(), oldB.getDescription()]
        self._repository.update(id, b)

        undo = FunctionCall(self.update, id, params[0], params[1], params[2])
        redo = FunctionCall(self.update, id, title, author, description)
        oper = Operation(undo, redo)
        self._undoCtrl.addOperation(oper)
        return True

    # ===================================================== Partial search
    def partialId(self, obj, string):
        return string.lower() in str(obj.getID()).lower()
    def partialSearchID(self, string):
        return filter(self._repository.getAll(), self.partialId, string)

    def partialTitle(self, obj, string):
        return string.lower() in str(obj.getTitle()).lower()
    def partialSearchTitle(self, string):
        return filter(self._repository.getAll(), self.partialTitle, string)

    def partialAuthor(self, obj, string):
        return string.lower() in str(obj.getAuthor()).lower()
    def partialSearchAuthor(self, string):
        return filter(self._repository.getAll(), self.partialAuthor, string)

    def partialDescr(self, obj, string):
        return string.lower() in str(obj.getDescription()).lower()
    def partialSearchDescription(self, string):
        return filter(self._repository.getAll(), self.partialDescr, string)