from domain import Book, Client, Rental
import random
import datetime

class Generator:
    def __init__(self):
        pass

    def generateNames(self):
        firstName = ['Alex', 'Andrei', 'Ioana', 'Oana', 'Cristina', 'Cristi', 'Marcel', 'Corina', 'Florin', 'Sorin', 'Marius', 'Andreea', 'Laura', 'George', 'Matei'] 
        middleName = ['A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'I.', 'J.', 'L.', 'M.', 'N.', 'O.', 'P.', 'R.', 'S.']
        lastName = ['Popescu', 'Ropan', 'Ionescu', "Chitan", 'Moisan', 'Stercan', 'Bodescu', 'Cosbuc', 'Lup', 'Bodnariu', 'Tertis', 'Miron', 'Dobra', 'Sandor', 'Feier', 'Cristea']
        result = []
        for i in firstName:
            for j in lastName:
                name = ''
                name += (i)
                name += (' ')
                name += (random.choice(middleName))
                name += (' ')
                name += (j)
                result.append(name)
        return result

    def generateTitle(self):
        nouns1 = ['Leaf', 'Jelly', 'Road', 'Forest', 'Kingdom', 'Stars', 'Moon', 'Clam', 'Sea', 'Mountain', 'Rain']
        nouns2 = ['Forest', 'Kingdom', 'Land', 'Sea', 'Mountain', 'Sky', 'Desert', 'Moon', 'Planet', 'World', 'Clouds']
        adjectiv = ['Forgotten', 'Blue', 'Fantastic', 'Golden', 'Darkened', 'Little', 'Ascended', 'Red', 'Hardened', 'Stressing', 'Sleepy', 'Long', 'Squishy']
        t = ''
        if random.choice([True, False]):
            t = "The "
        if random.choice([True, False]):
            t += random.choice(adjectiv)
            t += ' '
        t += random.choice(nouns1)
        t += " of the "
        if random.choice([True, False]):
            t += random.choice(adjectiv)
            t += ' '
        t += random.choice(nouns2)
        return t

    def generateDescription(self):
        start = ['A great book', 'The unique book', 'A new bestseller', 'The piece of art', 'An underdog of the fantasy world', 'A symphony for your eyes']
        end = ['we explore the unsolved conundrum', 'we take a look at new possibilities', 'we partake in a new journey', 'you can find your inner self', 'the author takes a new perspective', 'nothing seemed to go well']
        descr = random.choice(start)
        descr += ' where '
        descr += random.choice(end)
        return descr

    def generateBooks(self, dimension, idBasis, authorsNr):
        result = []
        authors = random.sample(self.generateNames(), authorsNr)
        for i in range (dimension):
            b = Book(idBasis + i, self.generateTitle(), random.choice(authors), self.generateDescription())
            result.append(b)
        return result

    def generateClients(self, dimension, idBasis):
        result = []
        names = self.generateNames()
        randomNames = random.sample(names, dimension)
        for i in range (dimension):
            c = Client(idBasis + i, randomNames[i])
            result.append(c)
        return result

    def generateRentals(self, dimension, idBasis, books, clients):
        result = []
        for i in range (dimension):
            rentedDate = datetime.date(random.randint(2000, 2018), random.randint(1, 12), random.randint(1, 28))
            dueDate = rentedDate + datetime.timedelta(days=random.randint(150, 300))
            returnedDate = rentedDate + datetime.timedelta(days=random.randint(60, 400))
            if random.choice([True, False, False]) or returnedDate > datetime.date.today():
                returnedDate = None
            r = Rental(idBasis + i, random.choice(books).getID(), random.choice(clients).getID(), rentedDate, dueDate, returnedDate)
            result.append(r)
        return result