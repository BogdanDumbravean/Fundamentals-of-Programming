# ================================================================================== DTO
class basicDTO:
    def __init__(self, item, count):
        self._item = item
        self._count = count

    @property
    def item(self):
        return self._item
    @property
    def count(self):
        return self._count

    def __lt__(self, other):
        return self._count < other._count

class RentedBooksCount(basicDTO):
    '''
    Class for holding information about the number of times a book was rented
    '''
    def __str__(self):
        return "Was rented " + str(self._count) + " times: - " + str(self._item)

class ClientActivityCount(basicDTO):
    '''
    Class for holding information about the number of days a client has rented
    '''
    def __str__(self):
        return str(self._count) + " days of renting, rented by: -" + str(self._item)

class RentedAuthorCount(basicDTO):
    '''
    Class for holding information about the number of times the books of an author was rented
    '''
    def __str__(self):
        return str(self._count) + " times were rented books written by: - " + str(self._item)

class LateRental(basicDTO):
    '''
    Class for holding information about the number of days a book was kept after the due date
    '''
    def __str__(self):
        return str(self._count) + " days past due date of: -" + str(self._item)