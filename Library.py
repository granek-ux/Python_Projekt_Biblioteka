from enum import Enum
from Book import Book
from Enums import StatusEnum
from Exceptions import ReaderNotFound, BookNotRegistered, BookAlreadyTaken
from Reader import Reader


class Library:

    price_for_missig_day = 5 #cena za nie oddanie kisażki za każdy dzień
    def __init__(self):
        self.list_of_readers = []
        self.list_of_book = [] #albo to zroibc jako mapa która posaida id ksiązki/nazwe coś unikalnego i jego liczbę bo mamy przechwywać klika takich samych książek
        self.map_of_rader_book = {}
        #     mapa która jako klucz będzie miała czytelnika np: jego id
        #     a jako wartość liste książek która wypozyczył

        self.map_reader_history = {}
    #     klucz czytelnik
    #     valve jego historia data operacji, tytuł książki, typ operacji(zwrot/wypożyczenie/przedłużenie/rezerwacja)

    def add_reader(self, reader: Reader) -> None:
        self.list_of_readers.append(reader)
        self.map_of_rader_book[reader] = []

    def add_book(self, book: Book) -> None:
        self.list_of_book.append(book)

    def edit_book(self, book: Book) -> None:
    # todo
    #     tu nie wiem co
        pass

    def remove_book(self, book: Book) -> None:
        self.list_of_book.remove(book)

    def _add_history(self, reader_id: int, log: str) -> None:
        if reader_id in self.list_of_readers:
            self.map_reader_history[reader_id].append('\n').append(log)
        else:
            raise ReaderNotFound('Reader has not been registered yet')

    def get_history(self, reader_id: int) -> str:
        return self.map_reader_history[reader_id]

    def reserve_book(self, reader:Reader, book:Book) -> None:

        if reader not in self.list_of_readers:
            raise ReaderNotFound('Reader has not been registered yet')
        if book not in self.list_of_book :
            raise BookNotRegistered("Book not registered in library")
        if book.status != StatusEnum.Wolny:
            raise BookAlreadyTaken('Book is already taken')

        book.status = StatusEnum.Wyporzyczona
        #todo
#         i tu na przykład usunąć z mapy jedną książkę


# można dodać jakiś graf pokazujący jaki czytelnik ile ksiązke wyporzyczył ale to juz dodatkowe ale nie trudne do zrobienia