from Book import Book
from Reader import Reader


class Library:
    def __init__(self):
        self.list_of_readers =[]
        self.list_of_book =[]
        self.map_of_rader_book ={}
    #     mapa która jako klucz będzie miała czytelnika np: jego id
    #     a jako wartość liste książek która wypozyczył

    def add_reader(self, reader: Reader) -> None:
        self.list_of_readers.append(reader)

    def add_book(self, book: Book) -> None:
        self.list_of_book.append(book)

    def remove_book(self, book:Book) -> None:
        self.list_of_book.remove(book)
