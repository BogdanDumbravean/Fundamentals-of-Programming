from domain.rental import Rental
import datetime

class RentalValidator:
    def validate(self, rental):
        if type(rental) != Rental:
            raise TypeError("Can only validate rentals!")

        if type(rental.getID()) != int or rental.getID() <= 0:
            raise ValueError("ID must be a natural number!")
        if type(rental.getBookID()) != int or rental.getBookID() <= 0:
            raise ValueError("Book ID must be a natural number!")
        if type(rental.getClientID()) != int or rental.getClientID() <= 0:
            raise ValueError("Client ID must be a natural number!")
  
        if rental.getReturnedDate() != None and (rental.getReturnedDate() - rental.getRentedDate()).days < 0:
            raise ValueError("Cannot return book before it was rented")

        return True