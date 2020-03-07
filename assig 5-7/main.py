from domain import *
from controllers import *
from UI import BookListUI, ClientListUI, RentalListUI 
import datetime

class Main:
    # The starting class
    
    def __init__(self, bookContr, clientContr, rentalContr, undoContr):
        self.books = bookContr
        self.clients = clientContr
        self.renting = rentalContr 
        self.undoCtrl = undoContr

    def printMenu(self):
        print("========================================================") 
        print("Choose one of the options:")
        print("1 - Manage books")
        print("2 - Manage clients")
        print("3 - Manage renting")
        print("4 - Statistics")
        print("5 - Undo")
        print("6 - Redo")
        print("0 - Exit")

    def start(self):
        while(True):
            self.printMenu()
            id = input("\nEnter the ID: ")
            if id == '0':
                return
            options = {'1':self.books.manageBookList, '2':self.clients.manageClientList, '3':self.renting.manageRentalList, '4':self.renting.manageStatistics, '5':self.undoCtrl.undo, '6':self.undoCtrl.redo}
            if id not in options:
                print("Invalid ID!")
                continue
            try:
                options[id]()
            except ValueError as ve:
                print(ve.args[0])

g = Generator()
repoChooser = RepositoryChooser()

bookRepository = repoChooser.chooseRepository(Book(), "book_file")
clientRepository = repoChooser.chooseRepository(Client(), "client_file")
rentalRepository = repoChooser.chooseRepository(Rental(), "rental_file") 

bookValidator = BookValidator()
clientValidator = ClientValidator() 
rentalValidator = RentalValidator()

undoController = UndoController()
rentalController = RentalsController(rentalValidator, rentalRepository, bookRepository, clientRepository, undoController)
bookController = BooksController(bookRepository, rentalController, undoController, bookValidator)
clientController = ClientsController(clientRepository, rentalController, undoController, clientValidator)

if repoChooser.readSettings()["repo_type"] == "memory":
    books = g.generateBooks(20, 100, 5)
    for b in books:
        bookController.add(b.getID(), b.getTitle(), b.getAuthor(), b.getDescription())

    clients = g.generateClients(30, 200)
    for c in clients:
        clientController.add(c.getID(), c.getName())

    rentals = g.generateRentals(50, 300, bookController.getRepository().getAll(), clientController.getRepository().getAll())
    for r in rentals:
        rentalController.add(r.getID(), r.getBookID(), r.getClientID(), r.getRentedDate(), r.getDueDate(), r.getReturnedDate())

bookUI = BookListUI(bookController)
clientUI = ClientListUI(clientController)
rentalUI = RentalListUI(rentalController, bookController, clientController)

main = Main(bookUI, clientUI, rentalUI, undoController)
main.start()
