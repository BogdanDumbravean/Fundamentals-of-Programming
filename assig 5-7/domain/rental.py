import datetime

class Rental:
    # Data about a rental from the library
    
    def __init__(self, id=0, bookID=0, clientID=0, rentedDate=datetime.date.today(), dueDate=datetime.date.today(), returnedDate=None):
        self.__ID = id
        self.__bookID = bookID
        self.__clientID = clientID
        self.__rentedDate = rentedDate 
        self.__dueDate = dueDate
        self.__returnedDate = returnedDate
    # ===================================================== Getters
    def getID(self):
        return self.__ID
    def getBookID(self):
        return self.__bookID
    def getClientID(self):
        return self.__clientID
    def getRentedDate(self):
        return self.__rentedDate
    def getDueDate(self):
        return self.__dueDate
    def getReturnedDate(self):
        return self.__returnedDate 
    # ===================================================== Others
    def update(self, item):
        # Updates only the returned date
        self.__returnedDate = item.__returnedDate

    # ===================================================== String conversions
    def itemType(self):
        return 'rental'

    def item2string(self):
        string = str(self.__ID) + ',' + str(self.__bookID) + ',' + str(self.__clientID) + ',' + str(self.__rentedDate) + ',' + str(self.__dueDate)
        if self.__returnedDate != None:
            string += ',' + str(self.__returnedDate)
        return string

    def string2date(self, string):
        args = string.split('-')
        return datetime.date(int(args[0]), int(args[1]), int(args[2]))

    def string2item(self, string):
        args = string.split(",")
        self.__ID = int(args[0])
        self.__bookID = int(args[1])
        self.__clientID = int(args[2])
        self.__rentedDate = self.string2date(args[3])
        self.__dueDate = self.string2date(args[4])
        if len(args) == 5:
            self.__returnedDate = None
        else:
            self.__returnedDate = self.string2date(args[5])
        return self

    def stringReturnedDate(self):
        if self.__returnedDate == None:
            return " Not returned!"
        return " Returned at " + str(self.__returnedDate)

    def copy(self):
        return Rental(self.__ID, self.__bookID, self.__clientID, self.__rentedDate, self.__dueDate, self.__returnedDate)

    def __eq__(self, other):
        if type(other) == Rental:
            return self.__ID == other.__ID
        return None

    def __str__(self):
        return 'Rental ' + str(self.__ID) + ': book ' + str(self.__bookID) + ' by client ' + str(self.__clientID) + ' since ' + str(self.__rentedDate) + ' due ' + str(self.__dueDate) + self.stringReturnedDate()