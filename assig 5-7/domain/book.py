class Book:
    # Data about a book in the library
    
    def __init__(self, bookID=0, title='', author='', descr=''):
        self.__ID = bookID
        self.__title = title
        self.__author = author
        self.__description = descr
    # ================================================ Getters
    def getID(self):
        return self.__ID 
    def getTitle(self):
        return self.__title
    def getAuthor(self):
        return self.__author
    def getDescription(self):
        return self.__description
    # ================================================ Setters
    def setID(self, newID):
        self.__ID = newID
    def setTitle(self, title):
        self.__title = title
    def setAuthor(self, author):
        self.__author = author
    def setDescription(self, descr):
        self.__description = descr
    # ================================================ Others
    def __str__(self):
        return 'Book ' + str(self.__ID) + ': ' + self.__title + ' by ' + self.__author + ' - ' + self.__description

    def itemType(self):
        return 'book'

    def item2string(self):
        return str(self.__ID) + ',' + self.__title + ',' + self.__author + ',' + self.__description

    def string2item(self, string):
        args = string.split(",")
        self.__ID = int(args[0])
        self.__title = args[1]
        self.__author = args[2]
        self.__description = args[3] 
        return self

    def copy(self):
        return Book(self.__ID, self.__title, self.__author, self.__description)

    def __eq__(self, other):
        if type(other) == Book:
            return self.__ID == other.__ID
        return None

    def update(self, book):
        self.__title = book.__title
        self.__author = book.__author
        self.__description = book.__description