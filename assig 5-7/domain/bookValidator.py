from domain.book import Book

class BookValidator:
    def validate(self, book):
        if type(book) != Book:
            raise TypeError("Can only validate books!")

        if book.getID() <= 0 or type(book.getID()) != int:
            raise ValueError("ID must be a natural number!")
  
        if book.getTitle() == "" or book.getAuthor() == "" or book.getDescription() == "":
            raise ValueError("The information cannot be null!")

        return True