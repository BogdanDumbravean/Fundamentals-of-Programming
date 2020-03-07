import sys
sys.path.append('d:\\Info\\Proiecte Info\\python\\FP\\assig 5-7\\')
from domain import *
from controllers import *
import datetime
import unittest 
 
class TestControllers(unittest.TestCase):
    def setUp(self):
        self.uCtrl = UndoController()

        bookRepository = Repository()
        clientRepository = Repository()
        rentalRepository = Repository()

        self._bv = BookValidator()
        self._cv = ClientValidator()
        self._rv = RentalValidator()

        self.rCtrl = RentalsController(self._rv, rentalRepository, bookRepository, clientRepository, self.uCtrl)

        self.bCtrl = BooksController(bookRepository, self.rCtrl, self.uCtrl, self._bv)
        self.bCtrl.add(1, "B1", "A1", "D1")
        self.bCtrl.add(2, "B2", "A2", "D2")
        self.bCtrl.add(3, "B3", "A1", "D2+1")

        self.cCtrl = ClientsController(clientRepository, self.rCtrl, self.uCtrl, self._cv)
        self.cCtrl.add(10, "N1")
        self.cCtrl.add(20, "N2")
        self.cCtrl.add(30, "N3")
        
        date = datetime.date.today()
        self.rCtrl.add(100, 1, 10, datetime.date.replace(date, 2012, 8, 10), datetime.date.replace(date, 2013, 1, 10), datetime.date.replace(date, 2012, 8, 20))
        self.rCtrl.add(200, 1, 20, datetime.date.replace(date, 2012, 6, 10), datetime.date.replace(date, 2012, 11, 10), datetime.date.replace(date, 2012, 6, 30))
        self.rCtrl.add(300, 2, 30, datetime.date.replace(date, 2013, 8, 10), datetime.date.replace(date, 2014, 1, 10))
        self.rCtrl.add(400, 3, 10, datetime.date.replace(date, 2018, 8, 16), datetime.date.replace(date, 2018, 10, 16))

    def test_books(self):
        self.assertEqual(self.bCtrl.getRepository().getAll(), [Book(1, "B1", "A1", "D1"), Book(2, "B2", "A2", "D2"), Book(3, "B3", "A1", "D2+1")])
        self.assertEqual(self.bCtrl.partialSearchID("2"), [Book(2, "B2", "A2", "D2")])
        self.assertEqual(self.bCtrl.partialSearchID("1"), [Book(1, "B2", "A2", "D2")])
        self.assertEqual(self.bCtrl.partialSearchID("3"), [Book(3, "B2", "A2", "D2")])
        self.assertEqual(self.bCtrl.partialSearchTitle("b"), self.bCtrl.getRepository().getAll())
        self.assertEqual(self.bCtrl.partialSearchAuthor("A"), self.bCtrl.getRepository().getAll())
        self.assertEqual(self.bCtrl.partialSearchDescription("d"), self.bCtrl.getRepository().getAll())
        b2 = Book(2, "B2", "A2", "D2")
        b3 = Book(3, "B3", "A1", "D2+1")
        self.assertEqual(self.bCtrl.partialSearchAuthor("D2"), [])
        self.assertEqual(self.bCtrl.partialSearchDescription("D2"), [b2, b3])
        self.assertTrue(self.bCtrl.add(4, 'b', 'a', 'd'))
        b = Client(-1, '')
        self.assertRaises(TypeError, self._bv.validate, b)
        self.assertRaises(ValueError, self.bCtrl.remove, b.getID())
        b = Book(-1, '', '', '')
        self.assertRaises(ValueError, self._bv.validate, b)
        b = Book(1, '', '', '')
        self.assertRaises(ValueError, self._bv.validate, b)
        b = Book(4, 'B4', 'A4', 'D4')
        self.assertTrue(self.bCtrl.update(4, 'B4', 'A4', 'D4'))
        self.assertEqual(self.bCtrl.remove(4, True), b)
     
    def test_clients(self):
        c2 = Client(20, "N2")
        self.assertEqual(self.cCtrl.partialSearchID("2"), [c2])
        self.assertEqual(self.cCtrl.partialSearchID("0"), self.cCtrl.getRepository().getAll())
        self.assertEqual(self.cCtrl.partialSearchName("N2"), [c2])
        self.assertEqual(self.cCtrl.partialSearchName("N"), self.cCtrl.getRepository().getAll())
        self.assertTrue(self.cCtrl.add(40, 'n')) 
        c = Book(-1, '', '', '')
        self.assertRaises(TypeError, self._cv.validate, c)
        c = Client(-1, '')
        self.assertRaises(ValueError, self._cv.validate, c)
        self.assertRaises(ValueError, self.cCtrl.remove, c.getID())
        c = Client(1, '')
        self.assertRaises(ValueError, self._cv.validate, c)
        c = Client(40, 'N')
        self.assertTrue(self.cCtrl.update(40, 'N'))
        
        date = datetime.date.today()
        self.rCtrl.add(500, 4, 20, datetime.date.replace(date, 2018, 8, 16), datetime.date.replace(date, 2018, 10, 16))
        self.assertEqual(self.cCtrl.remove(40, True), c)

    def test_rentals(self): 
        self.assertEqual(len(self.rCtrl.getRepository().getAll()), 4)
        self.assertEqual(len(self.rCtrl.searchByBookID(1)), 2)
        self.assertEqual(len(self.rCtrl.searchByClientID(10)), 2)
        self.assertTrue(self.rCtrl.add(1000, 1, 10, datetime.date.today(), datetime.date.today()))
        self.assertTrue(self.rCtrl.returnBook(1000, datetime.date.today()))
        self.assertRaises(ValueError, self.rCtrl.returnBook, 1000, datetime.date.today())
        self.assertTrue(self.rCtrl.remove(1000))
        r = Rental('-1', '-1', '-1', datetime.date.today(), datetime.date.today())
        self.assertRaises(ValueError, self._rv.validate, r)
        r = Rental('1', '-1', '-1', datetime.date.today(), datetime.date.today())
        self.assertRaises(ValueError, self._rv.validate, r)
        r = Rental('1', '1', '-1', datetime.date.today(), datetime.date.today())
        self.assertRaises(ValueError, self._rv.validate, r)
 
    def test_rentedBooks(self):
        mrb = self.rCtrl.mostRentedBooks()
        self.assertEqual(mrb[0].count, 2)
        self.assertEqual(mrb[0].item.getTitle(), "B1")
        self.assertEqual(mrb[1].count, 1)
        self.assertEqual(mrb[2].count, 1)

    def test_activeClients(self):
        mac = self.rCtrl.mostActiveClients()
        c = Client(20, "N2")
        self.assertEqual(mac[0].item, c)
        self.assertEqual(mac[0].count, 20)
        c = Client(10, "N1")
        self.assertEqual(mac[1].item, c) 
        c = Client(30, "N3")
        self.assertEqual(mac[2].item, c) 

    def test_rentedAuthors(self):
        mra = self.rCtrl.mostRentedAuthor()
        self.assertEqual(mra[0].count, 3)
        self.assertEqual(mra[0].item, "A1")
        self.assertEqual(mra[1].count, 1)
        self.assertEqual(mra[1].item, "A2")

    def test_lateRentals(self):
        lr = self.rCtrl.lateRentals()
        self.assertEqual(lr[0].count, (datetime.date.today() - self.rCtrl.getRepository().searchByID(300).getDueDate()).days)
        self.assertEqual(lr[0].item, Book(2, "B2", "A2", "D2"))
        self.assertEqual(lr[1].count, (datetime.date.today() - self.rCtrl.getRepository().searchByID(400).getDueDate()).days)
        self.assertEqual(lr[1].item, Book(3, "B3", "A3", "D3"))

    def test_itemGenerator(self):
        ig = Generator()

        self._bv = BookValidator() 
        books = ig.generateBooks(10, 10, 3)
        for b in books:
            self.assertTrue(self._bv.validate(b))

        self._cv = ClientValidator() 
        clients = ig.generateClients(10, 10)
        for c in clients:
            self.assertTrue(self._cv.validate(c))

        self._rv = RentalValidator() 
        for r in ig.generateRentals(10, 10, books, clients):
            self.assertTrue(self._rv.validate(r)) 

    def test_undoController(self):
        self.assertRaises(ValueError, self.uCtrl.redo)
        self.assertTrue(self.uCtrl.undo())
        self.assertTrue(self.uCtrl.redo())
        for i in range(10):
            self.uCtrl.undo()
        self.assertRaises(ValueError, self.uCtrl.undo)
        
if __name__ == '__main__':
    unittest.main() 