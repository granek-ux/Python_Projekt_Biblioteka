from datetime import date, timedelta

import pandas as pd
from tabulate import tabulate

from Book import Book
from Enums import StatusEnum, RegisterEnum
from Exceptions import ReaderNotFound, BookNotFound, NoBookReserved, ExtendNotPossible, NoHistory
from Reader import Reader
from Register import Register


class Library:
    price_for_missig_day = 5  # cena za nie oddanie kisażki za każdy dzień

    def __init__(self):
        self.list_of_readers = []
        self.list_of_book = []  # albo to zroibc jako mapa która posaida id ksiązki/nazwe coś unikalnego i jego liczbę bo mamy przechwywać klika takich samych książek
        # self.map_of_rader_book = {}
        #     mapa która jako klucz będzie miała czytelnika np: jego id
        #     a jako wartość liste książek która wypozyczył
        # self.book_quantity = {}

        # self.list_of_registers = []

    #     klucz czytelnik
    #     valve jego historia data operacji, tytuł książki, typ operacji(zwrot/wypożyczenie/przedłużenie/rezerwacja)

    def add_reader(self, reader: Reader) -> None:
        self.list_of_readers.append(reader)
        # self.map_of_rader_book[reader] = []

    def _find_Reader(self, name: str, surname: str) -> Reader:
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

    def remove_reader(self, name: str, surname: str) -> None:
        reader = self._find_Reader(name, surname)
        self.list_of_readers.remove(reader)

    def edit_reader(self, name: str, surname: str):

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

    def _findBook(self, title: str, author: str, status: StatusEnum = StatusEnum.Wolny) -> Book:
        matches = [b for b in self.list_of_book if b.title == title and b.author == author and b.status == status]
        if len(matches) == 0:
            raise BookNotFound
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

    def edit_book(self, title: str, author: str) -> None:
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

    def remove_book(self, title: str, author: str) -> None:
        book = self._findBook(title, author)

        self.list_of_book.remove(book)
        # self.book_quantity[book.title] =  self.book_quantity[book.title] - 1

    @staticmethod
    def _found_Book_By_isbn(looking_isbn: int, list_of_book: list) -> Book:
        for book in list_of_book:
            if book.isbn == looking_isbn:
                if book.status == StatusEnum.Wolny:
                    return book

        lowest_date = date.max
        found_book = None
        for book in list_of_book:
            if book.isbn == looking_isbn:
                if book.status == StatusEnum.Wyporzyczona:
                    if book.borrow_date < lowest_date:
                        lowest_date = book.borrow_date
                        found_book = book

        return found_book

    def _borrow_final(self, reader: Reader, book: Book) -> None:
        if book.status == StatusEnum.Wolny:
            book.status = StatusEnum.Wyporzyczona
            reader.list_of_Borrowed_Books.append(book)
            book.borrow_date = date.today()
            today = date.today()
            regi = Register(reader.id, book.id, today, RegisterEnum.Wyporzyczenie)
            reader.list_of_registers.append(regi)
            book.borrow_date = today
            return
        else:
            print(f"Wszystkie książki wypożyczone, wróci na stan: {book.borrow_date + timedelta(days=30)}")
            print(f"Czy chcesz zarezerwować? y/n")
            answer = input().lower().strip()

            if answer == 'y':
                book.status = StatusEnum.Zarezewowana_Wypozyczona
                reader.list_of_Reserved_Books.append(book)
                today = date.today()
                regi = Register(reader.id, book.id, today, RegisterEnum.Zarezerwowanie)
                reader.list_of_registers.append(regi)
            elif answer == 'n':
                return

    def borrow_book(self, rname: str, rsurname: str, btitle: str, bauthor: str) -> None:
        reader = self._find_Reader(rname, rsurname)
        matching_books = []
        found_isbn = []
        for book in self.list_of_book:
            if book.status == StatusEnum.Wolny or book.status == StatusEnum.Wyporzyczona:
                if book.title == btitle and book.author == bauthor:
                    if not book.isbn in found_isbn:
                        found_isbn.append(book.isbn)
                    matching_books.append(book)

        if len(found_isbn) == 0:
            raise BookNotFound

        if len(found_isbn) == 1:
            book = self._found_Book_By_isbn(found_isbn[0], matching_books)
            self._borrow_final(reader, book)
            return

        final_list = []
        for isbn in found_isbn:
            final_list.append(self._found_Book_By_isbn(isbn, matching_books))

        df = pd.DataFrame([vars(book) for book in final_list])
        df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
        df_better.index += 1
        print(tabulate(df_better, headers='keys', tablefmt='psql'))
        while True:
            code = int(input("Podaj numer książki którą chcesz wypożyczyć: "))
            if code in df_better.index:
                break
        book = final_list[code - 1]

        self._borrow_final(reader, book)

    def calculateCosts(self, date_of_borow: date) -> int:
        dayToday = date.today()
        diff = dayToday - date_of_borow
        if (diff.days > 30):
            return diff.days - 30 * Library.price_for_missig_day

        return 0

    def return_book(self, rname: str, rsurname: str) -> None:
        reader = self._find_Reader(rname, rsurname)

        print('Wybierz książkę: ')
        book_list = []
        for book in reader.list_of_Borrowed_Books:
            book_list.append(book)

        if len(book_list) == 0:
            raise BookNotFound

        df = pd.DataFrame([vars(book) for book in book_list])
        df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
        df_better.index += 1
        print(tabulate(df_better, headers='keys', tablefmt='psql'))

        while True:
            code = int(input("Podaj numer książki którą chcesz zarządzać: "))
            if code in df_better.index:
                break
        book = book_list[code - 1]

        if book.status == StatusEnum.Wyporzyczona:
            book.status = StatusEnum.Wolny
        elif book.status == StatusEnum.Zarezewowana_Wypozyczona:
            book.status = StatusEnum.Zarezewowana_Wolna

        today = date.today()
        regi = Register(reader.id, book.id, today, RegisterEnum.Oddanie)

        reader.list_of_registers.append(regi)
        reader.list_of_Borrowed_Books.remove(book)

        book.borrow_date = today

        for register in reader.list_of_registers[::-1]:
            if register.book_id == book.id and (
                    register.operation == RegisterEnum.Wyporzyczenie or register.operation == RegisterEnum.Przedluzenie):
                date_of_borow = register.date
                cost = self.calculateCosts(date_of_borow)
                # cost = 5
                reader.charge += cost
                break

    def extend_borrow(self, rname: str, rsurname: str) -> None:
        reader = self._find_Reader(rname, rsurname)

        print('Wybierz książkę: ')
        book_list = []
        for book in reader.list_of_Borrowed_Books:
            book_list.append(book)

        if len(book_list) == 0:
            raise BookNotFound

        df = pd.DataFrame([vars(book) for book in book_list])
        df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
        df_better.index += 1
        print(tabulate(df_better, headers='keys', tablefmt='psql'))

        while True:
            code = int(input("Podaj numer książki którą chcesz zarządzać: "))
            if code in df_better.index:
                break
        book = book_list[code - 1]

        if book.status == StatusEnum.Wyporzyczona:
            # zwrć i wyporzycz
            today = date.today()
            regi = Register(reader.id, book.id, today, RegisterEnum.Przedluzenie)

            reader.list_of_registers.append(regi)
            # reader.list_of_Borrowed_Books.remove(book)

            book.borrow_date = None

            for register in reader.list_of_registers[::-1]:
                if register.book_id == book.id and (
                        register.operation == RegisterEnum.Wyporzyczenie or register.operation == RegisterEnum.Przedluzenie):
                    date_of_borow = register.date
                    cost = self.calculateCosts(date_of_borow)
                    # cost = 5
                    reader.charge += cost
                    break

        elif book.status == StatusEnum.Zarezewowana_Wypozyczona:
            # akcja niemożliwa, koniec
            raise ExtendNotPossible


#todo check this function
    def reader_history(self, rname: str, rsurname: str) -> None:
        reader = self._find_Reader(rname, rsurname)

        if len(reader.list_of_registers) == 0:
            raise NoHistory

        better_list = []

        for register in reader.list_of_registers:
            book_name = ""
            for book in self.list_of_book:
                if book.id == register.book_id:
                    book_name = book.title
                    break
            tmp_regi = {'date': register.date,
                        'book_name': book_name,
                        'operation': register.operation.value
                        }
            better_list.append(tmp_regi)

        df = pd.DataFrame([vars(register) for register in better_list])
        df_better = df[['date', 'book_name', 'operation']]
        print(tabulate(df_better, headers='keys', tablefmt='psql'))

    def manage_reservation(self, rname: str, rsurname: str) -> None:
        reader = self._find_Reader(rname, rsurname)

        wanted_book_list = []
        for book in reader.list_of_Reserved_Books:
            if book.status == StatusEnum.Zarezewowana_Wolna or book.status == StatusEnum.Zarezewowana_Wypozyczona:
                wanted_book_list.append(book)

        if len(wanted_book_list) == 0:
            raise NoBookReserved

        print('Wybierz książkę: ')

        df = pd.DataFrame([vars(book) for book in wanted_book_list])
        df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
        df_better.index += 1
        print(tabulate(df_better, headers='keys', tablefmt='psql'))

        while True:
            code = int(input("Podaj numer książki którą chcesz zarządzać: "))
            if code in df_better.index:
                break
        book = wanted_book_list[code - 1]

        if book.status == StatusEnum.Zarezewowana_Wypozyczona:
            print("czy chcesz odwolac rezerwacje? y/n")
            answer = input().lower().strip()
            if answer == 'y':
                book.status = StatusEnum.Wyporzyczona
                reader.list_of_Reserved_Books.remove(book)
                today = date.today()
                regi = Register(reader.id, book.id, today, RegisterEnum.Rezerwacja_Oddanie)
                reader.list_of_registers.append(regi)
            elif answer == 'n':
                return

        elif book.status == StatusEnum.Zarezewowana_Wypozyczona:
            print("czy chcesz wyporzyczyć? y/n")
            answer = input().lower().strip()
            if answer == 'y':
                book.status = StatusEnum.Wyporzyczona
                reader.list_of_Reserved_Books.remove(book)
                today = date.today()
                regi = Register(reader.id, book.id, today, RegisterEnum.Wyporzyczenie)
                reader.list_of_registers.append(regi)
            elif answer == 'n':
                print("czy chcesz odwolac rezerwacje? y/n")
                answer = input().lower().strip()
                if answer == 'y':
                    book.status = StatusEnum.Wolny
                    reader.list_of_Reserved_Books.remove(book)
                    today = date.today()
                    regi = Register(reader.id, book.id, today, RegisterEnum.Rezerwacja_Oddanie)
                    reader.list_of_registers.append(regi)
                elif answer == 'n':
                    return

# można dodać jakiś graf pokazujący jaki czytelnik ile ksiązke wyporzyczył ale to juz dodatkowe ale nie trudne do zrobienia
