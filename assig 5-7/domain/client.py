class Client:
    # Data about a client of the library
    
    def __init__(self, id=0, name=''):
        self.__ID = id
        self.__name = name
    # ================================================ Getters
    def getID(self):
        return self.__ID
    def getName(self): 
        return self.__name
    # ================================================ Setters
    def setID(self, newID):
        self.__ID = newID
    def setName(self, name):
        self.__name = name
    # ================================================ Others
    def update(self, client):
        self.__name = client.__name

    def itemType(self):
        return 'client'

    def item2string(self):
        return str(self.__ID) + ',' + self.__name

    def string2item(self, string):
        args = string.split(",")
        self.__ID = int(args[0])
        self.__name = args[1]
        return self
    
    def copy(self):
        return Client(self.__ID, self.__name)

    def __eq__(self, other):
        if type(other) == Client:
            return self.__ID == other.__ID
        return False

    def __str__(self):
        return 'Client ' + str(self.__ID) + ': ' + self.__name