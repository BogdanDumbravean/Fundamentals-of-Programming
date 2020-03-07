import datetime
from domain.DTOs import *
from domain.rental import Rental
from domain.undoDomain import *
from assig9 import sort

class RentalsController:
    def __init__(self, validator, repository, booksRepository, clientsRepository, undoController):
        self._validator = validator
        self._list = repository
        self._books = booksRepository
        self._clients = clientsRepository
        self._undoCtrl = undoController

    def getRepository(self):
        '''
        Returns specific repository
        '''
        return self._list

    def searchByBookID(self, bookId):
        '''
        Searches rentals by a book's id and returns a list of indexes of the rentals of said book
        '''
        result = []
        for rental in self._list.getAll():
            if rental.getBookID() == bookId:
                result.append(rental)
        return result

    def searchByClientID(self, clientId):
        '''
        Searches rentals by a client's id and returns a list of indexes of the rentals of said client
        '''
        result = []
        for rental in self._list.getAll():
            if rental.getClientID() == clientId:
                result.append(rental)
        return result

    def add(self, id, bookId, clientId, rentedDate, dueDate, returnedDate = None):
        rental = Rental(id, bookId, clientId, rentedDate, dueDate, returnedDate)
        self._validator.validate(rental)
        self._list.add(rental)

        undo = FunctionCall(self.remove, id)
        redo = FunctionCall(self.add, id, bookId, clientId, rentedDate, dueDate, returnedDate)
        oper = Operation(undo, redo)
        self._undoCtrl.addOperation(oper)
        return True

    def remove(self, id):
        self._list.remove(id)
        return True

    def returnBook(self, id, returnedDate):
        aux = self._list.searchByID(id)
        if aux.getReturnedDate() != None:
            raise ValueError("Book was already returned")
        rental = Rental(id, aux.getBookID(), aux.getClientID(), aux.getRentedDate(), aux.getDueDate(), returnedDate)
        self._validator.validate(rental)
        self._list.update(id, rental)

        undo = FunctionCall(self.updateRentalReturnDate, id, None)
        redo = FunctionCall(self.updateRentalReturnDate, id, returnedDate)
        oper = Operation(undo, redo)
        self._undoCtrl.addOperation(oper)
        return True

    def updateRentalReturnDate(self, id, returnedDate):
        aux = self._list.searchByID(id)
        rental = Rental(id, aux.getBookID(), aux.getClientID(), aux.getRentedDate(), aux.getDueDate(), returnedDate)
        self._validator.validate(rental)
        self._list.update(id, rental)

    def greater(self, a, b):
        return a > b

    def mrbFilter(self, ob, other):
        if ob.getBookID() in other.keys():
            other[ob.getBookID()] += 1
        else:
            other[ob.getBookID()] = 1

    def mostRentedBooks(self):
        '''
        Statistics of most rented books by number of rentals
        Input:  -
        Output: list of objects which contains the book and the number of times it was rented
        '''
        aux = {}
        for rental in self._list.getAll():
            if rental.getBookID() in aux.keys():
                aux[rental.getBookID()] += 1
            else:
                aux[rental.getBookID()] = 1

        for book in self._books.getAll(): 
            if book.getID() not in aux.keys():
                aux[book.getID()] = 0

        result = []
        for val in aux.keys():
            result.append(RentedBooksCount(self._books.searchByID(val), aux[val]))
        sort(result, self.greater)
        return result

    def mostActiveClients(self):
        '''
        Statistics of most active clients by number of days rented
        Input:  -
        Output: list of objects which contains the client and the number of days they rented
        '''
        aux = {}
        for rental in self._list.getAll():
            if rental.getClientID() in aux.keys():
                if rental.getReturnedDate() != None:
                    aux[rental.getClientID()] += (rental.getReturnedDate() - rental.getRentedDate()).days
                #else:
                #    aux[rental.getClientID()] += (datetime.date.today() - rental.getRentedDate()).days
            else:
                if rental.getReturnedDate() != None:
                    aux[rental.getClientID()] = (rental.getReturnedDate() - rental.getRentedDate()).days
                else:
                    aux[rental.getClientID()] = 0#(datetime.date.today() - rental.getRentedDate()).days

        for client in self._clients.getAll():
            if client.getID() not in aux.keys():
                aux[client.getID()] = 0

        result = []
        for val in aux.keys():
            result.append(ClientActivityCount(self._clients.searchByID(val), aux[val]))
        return sorted(result, reverse=True)

    def mostRentedAuthor(self):
        '''
        Statistics of most rented author by number of rentals
        Input:  -
        Output: list of objects which contains the author and the number of times one of their books was rented
        '''
        aux = {}
        for rental in self._list.getAll():
            author = self._books.searchByID(rental.getBookID()).getAuthor()
            if author in aux.keys():
                aux[author] += 1
            else:
                aux[author] = 1

        for book in self._books.getAll():
            author = self._books.searchByID(book.getID()).getAuthor()
            if author not in aux.keys():
                aux[author] = 0

        result = []
        for val in aux.keys():
            result.append(RentedAuthorCount(val, aux[val]))
        return sorted(result, reverse=True)

    def lateRentals(self):
        '''
        Statistics of late returns by number of days behind
        Input:  -
        Output: list of objects which contains the book and the number of days they are held after the due date
        '''
        aux = {}
        for rental in self._list.getAll():
            if rental.getReturnedDate() == None and datetime.date.today() > rental.getDueDate():
                aux[rental.getBookID()] = (datetime.date.today() - rental.getDueDate()).days

        result = []
        for val in aux.keys():
            result.append(LateRental(self._books.searchByID(val), aux[val]))
        return sorted(result, reverse=True)