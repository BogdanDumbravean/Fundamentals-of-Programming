import sys
sys.path.append('d:\\Info\\Proiecte Info\\python\\FP\\assig 5-7\\')
from domain import *
import datetime
import unittest

class Test_classes(unittest.TestCase):
    def testBook(self):
        book = Book(1, 'Title', 'Author', 'Description')
        self.assertEqual(str(book), 'Book 1: Title by Author - Description')
        book.update(Book(1, 'T', 'A', 'D'))
        self.assertEquals (str(book), 'Book 1: T by A - D')
        self.assertEquals(Book(1, 'a', 'b', 'c'), Book(1, 'c', 'b', 'a'))

    def testClient(self):
        client = Client(1, 'Name') 
        self.assertEquals (str(client), 'Client 1: Name')
        client.update(Client(1, 'N'))
        self.assertEquals (str(client), 'Client 1: N')

    def testRental(self):
        date1 =  datetime.date.today().replace(2000, 10, 20)
        rental = Rental(2, 1, 1, date1, date1)
        self.assertEquals (str(rental), 'Rental 2: book 1 by client 1 since ' + str(date1) + ' due ' + str(date1) + ' Not returned!')
        rental.update(Rental(rental.getID, rental.getBookID(), rental.getClientID(), rental.getRentedDate(), rental.getDueDate(), date1))
        self.assertEquals (str(rental), 'Rental 2: book 1 by client 1 since ' + str(date1) + ' due ' + str(date1) + ' Returned at ' + str(date1))
 
    def testRepository(self):
        repo = Repository()
        b = Book(1, 'T', 'A', 'D')
        c = Client(11, 'N')
        today = datetime.date.today()
        r = Rental(111, 1, 11, today, today)

        repo.add(b) 
        repo.add(c)
        repo.add(r)
        self.assertEqual(repo.getAll(), [b, c, r])
        repo.remove(111)
        self.assertEqual(repo.getAll(), [b, c])
        repo.update(11, Client(11, 'Name'))
        
        self.assertEqual(repo.searchByID(11).getName(), 'Name')
        self.assertEqual(repo.searchByID(11), c)
        self.assertEqual(repo.searchByID(2), None)

if __name__ == '__main__':
    unittest.main()