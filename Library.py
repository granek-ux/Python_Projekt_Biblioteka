import enum
from enum import Enum
from Book import Book
from Enums import StatusEnum, RegisterEnum
from Exceptions import ReaderNotFound, BookNotRegistered, BookAlreadyTaken
from Reader import Reader
from Resiter import Register
from datetime import date


class Library:
    price_for_missig_day = 5  # cena za nie oddanie kisażki za każdy dzień

    def __init__(self):
        self.list_of_readers = []
        self.list_of_book = []  # albo to zroibc jako mapa która posaida id ksiązki/nazwe coś unikalnego i jego liczbę bo mamy przechwywać klika takich samych książek
        self.map_of_rader_book = {}
        #     mapa która jako klucz będzie miała czytelnika np: jego id
        #     a jako wartość liste książek która wypozyczył
        # self.book_quantity = {}

        self.list_of_registers = []

    #     klucz czytelnik
    #     valve jego historia data operacji, tytuł książki, typ operacji(zwrot/wypożyczenie/przedłużenie/rezerwacja)

    def add_reader(self, reader: Reader) -> None:
        self.list_of_readers.append(reader)
        self.map_of_rader_book[reader] = []

    def _find_Reader(self,name:str, surname:str) -> Reader:
        matches = [r for r in self.list_of_readers if r.name == name and r.surname == surname]
        if len(matches) == 0:
            raise ReaderNotFound
        elif len(matches) == 1:
            reader = matches[0]
        else:
            print('Wybierz czyelnika: ')
            id = 1
            for r in matches:
                print(f"numer: {id} to: {r}")
                id += 1
            id_wanted = int(input("podaj żądane Id: "))
            reader = matches[id_wanted - 1]

        return reader

    def remove_reader(self, name:str, surname:str) -> None:
        reader = self._find_Reader(name, surname)
        self.list_of_readers.remove(reader)

    def edit_reader(self, name:str, surname:str):

        reader = self._find_Reader(name, surname)

        print("Co chcesz edytować:")
        print("1. imie: ")
        print("2. nazwisko: ")
        print("3. adres: ")
        print("4. numer telefonu: ")

        code = (int)(input())
        match (code):
            case 1:
                print(f"Stare imie: {reader.name}")
                name = input("Podaj nowe imie: ")
                reader.name = name
            case 2:
                print(f"Stare nazwsiko: {reader.surname}")
                sname = input("Podaj nowe nazwsiko: ")
                reader.surname = sname
            case 3:
                print(f"Stary adres: {reader.address}")
                adres = input("Podaj nowe adres: ")
                reader.address = adres
            case 4:
                print(f"Stary numer telefonu: {reader.telephone_number}")
                tln = int(input("Podaj nowy numer telefonu: "))
                reader.telephone_number = tln


    def add_book(self, book: Book) -> None:
        self.list_of_book.append(book)
        # if (book.title in self.book_quantity.keys()):
        #     self.book_quantity[book.title] =  self.book_quantity[book.title] + 1
        # else:
        #     self.book_quantity[book.title] = 1



    def _findBook(self, title:str, author:str, status:StatusEnum = StatusEnum.Wolny)->Book:
        matches = [b for b in self.list_of_book if b.title == title and b.author == author and b.status == status]
        if len(matches) == 0:
            raise BookNotRegistered
        elif len(matches) == 1:
            book = matches[0]
        else:
            print('Wybierz książkę: ')
            id = 1
            for b in matches:
                print(f"numer: {id} to: {b}")
                id += 1
            id_wanted = int(input("podaj żądane Id: "))
            book = matches[id_wanted - 1]

        return book

    def edit_book(self, title:str, author:str) -> None:
        book = self._findBook(title, author)
        print('Co chcesz edytować?: ')
        print("1. Tytuł")
        print("2. Autor")
        print("3. isbm")
        print("4. ilość stron")
        code = (int)(input())
        match (code):
            case 1:
                print(f"Stary tytuł: {book.title}")
                title = input("Podaj nowy tytuł: ")
                book.title = title
            case 2:
                print(f"Stary Autor: {book.author}")
                author = input("Podaj nowego Autora: ")
                book.author = author
            case 3:
                print(f"Stary ISBM: {book.isbn}")
                ismb = int(input("Podaj nowy ISBM: "))
                book.isbn = ismb
            case 4:
                print(f"Stara ilość stron: {book.pages}")
                pages = int(input("Podaj nową ilość stron: "))
                book.pages = pages

    def remove_book(self, title:str, author:str) -> None:
        book = self._findBook(title, author)

        self.list_of_book.remove(book)
        # self.book_quantity[book.title] =  self.book_quantity[book.title] - 1

    def _add_history(self, reader_id: int, log: str) -> None:
        if reader_id in self.list_of_readers:
            self.map_reader_history[reader_id].append('\n').append(log)
        else:
            raise ReaderNotFound('Reader has not been registered yet')

    def get_history(self, reader_id: int) -> str:
        return self.map_reader_history[reader_id]

    def borrow_book(self, rname:str, rsurname:str, btitle:str, bauthor:str) -> None:
        reader = self._find_Reader(rname, rsurname)   
        book = self._findBook(title = btitle, author = bauthor)

        book.status = StatusEnum.Wyporzyczona
        today = date.today()
        regi = Register(reader.id, book.id,today, RegisterEnum.Wyporzyczenie)

        reader.list_of_registers.append(regi)
        reader.list_of_Borrowed_Books.append(book)

    def calculateCosts(self, date_of_borow: date) -> int:
        dayToday = date.today()
        diff = dayToday - date_of_borow
        if (diff.days > 30):
            return diff.days - 30 * Library.price_for_missig_day

        return 0

    def return_book(self, rname: str, rsurname: str) -> None:
        reader = self._find_Reader(rname, rsurname)

        print('Wybierz książkę: ')
        lookingid = 1
        for book in reader.list_of_Borrowed_Books:
            print(f"numer: {lookingid} to: {str(book)}")
            lookingid += 1
        id_wanted = int(input("podaj żądane Id: "))
        book = reader.list_of_Borrowed_Books[id_wanted - 1]

        book.status = StatusEnum.Wolny
        today = date.today()
        regi = Register(reader.id, book.id, today, RegisterEnum.Oddanie)

        reader.list_of_registers.append(regi)
        reader.list_of_Borrowed_Books.remove(book)

        # borrow_date =1
        # latest_register_of_book = max(
        #     (r for r in reader.list_of_registers if r.book_id == target_book_id and r.operation == "wypożyczenie"),
        #     key=lambda r: r.date,
        #     default=None  # jeśli nie ma takiego wpisu
        # )
        for register in reader.list_of_registers[::-1]:
            if register.book_id == book.id and register.operation == RegisterEnum.Wyporzyczenie:
                date_of_borow = register.date
                cost = self.calculateCosts(date_of_borow)
                cost = 5
                reader.charge += cost
                break

        # latest_register_of_book = None
        # for register in reader.list_of_registers:
        #     if register.book_id == target_book_id and register.operation == "wypożyczenie":
        #         if latest_register_of_book is None or register.date > latest_register_of_book.date:
        #             latest_register_of_book = register







    # def return_book(self, rname:str, rsurname:str, btitle:str, bauthor:str) -> None:
    #     reader = self._find_Reader(rname, rsurname)
    #     book = self._findBook(title=btitle, author=bauthor, status= StatusEnum.Wyporzyczona)
    #
    #     book.status = StatusEnum.Wolny
    #     today = date.today()
    #     regi = Register(reader.id, book.id,today, "Oddanie")
    #
    #     reader.list_of_registers.add(regi)





# można dodać jakiś graf pokazujący jaki czytelnik ile ksiązke wyporzyczył ale to juz dodatkowe ale nie trudne do zrobienia
