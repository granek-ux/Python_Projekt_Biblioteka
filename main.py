import os
import pickle
from unittest import case

from Book import Book
from Exceptions import *
from Library import Library
from colorama import init, Fore, Style
import shutil
import pandas as pd
from tabulate import tabulate
from pprint import pprint
from datetime import date, datetime

from Reader import Reader

def reader_interface(library:Library) ->Library:
    while True:
        print('Jesteś w sekcji czytelnika:')
        print('możesz w niej zrobić')
        print('1. Dodać nowego czytelnika')
        print('2. Usunąć czytelnika')
        print('3. Edytować czytelnika')
        print('4. Wyświetlić wszystkich czytelników')
        print('5. Cofnij do głównego Menu')
        code = input()
        match code.strip():
            case '1':
                maxid = 0
                for reader_tmp in lib.list_of_readers:
                    if reader_tmp.id > maxid:
                        maxid = reader_tmp.id

                name = input("Podaj imie: ")
                surname = input("Podaj nazwisko: ")
                address = input("Podaj address: ")
                telephone_number = int(input("Podaj numer telefonu: "))
                reader = Reader(id=maxid, name=name, surname=surname, address=address, telephone_number=telephone_number)
                lib.add_reader(reader)

                print('\033[31mDodaleś Czytelnika\033[0m')
                print(lib.list_of_readers)
            case '2':
                name = input("Podaj imie czytelnika:")
                surname = input("Podaj nazwisko czytelnika:")
                try:
                    library.remove_reader(name, surname)
                except ReaderNotFound:
                    text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)

                print('Usunałes')
            case '3':
                name = input("Podaj imie czytelnika:")
                surname = input("Podaj nazwisko czytelnika:")
                try:
                    library.edit_reader(name, surname)
                except ReaderNotFound:
                    text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)
            case '4':
                df = pd.DataFrame([vars(reader) for reader in lib.list_of_readers])
                df_better = df[['name', 'surname', 'address', 'telephone_number', 'charge']]
                print(tabulate(df_better, headers='keys', tablefmt='psql'))
            case '5':
                return library
            case _:  # to jest domyślny case i zorbiłem na string aby uniknąć wyjątków jak ktoś wpisze napis
                print('Podany zły kod')


def book_interface(library:Library)->Library:
    while True:
        print('Jesteś w sekcji książek:')
        print('możesz w niej zrobić:')
        print('1. Dodać nową książkę')
        print('2. Usunąć książkę')
        print('3. Edytować książkę')
        print('4. Wyświetlić wszystkie książki')
        print('5. Cofnij do głównego Menu')
        code = input()
        match code.strip():
            case '1':
                maxid = 0
                for booktmp in lib.list_of_book:
                    print(type(booktmp))
                    if booktmp.id > maxid:
                        maxid = booktmp.id

                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")
                isbn = int(input("Podaj isbn: "))
                pages = int(input("Podaj ilość stron: "))
                book = Book(id=maxid + 1, title=title, author=author, isbn=isbn, pages=pages)

                lib.add_book(book)
                print("ksiązka została dodana")
            case '2':
                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")
                try:
                    library.remove_book(title, author)
                except BookNotFound:
                    text = Fore.RED + 'KSIĄŻKA NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)
            case '3':
                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")
                try:
                    library.edit_book(title, author)
                except BookNotFound:
                    text = Fore.RED + 'KSIĄŻKA NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)
            case '4':
                df = pd.DataFrame([vars(book) for book in lib.list_of_book])
                df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
                print(tabulate(df_better, headers='keys', tablefmt='psql'))
            case '5':
                return library
            case _:
                print('Podany zły kod')

def rent_interface(library:Library)->Library:
    while True:
        print('Jesteś w sekcji Wyporzyczenia:')
        print('możesz w niej zrobić:')
        print('1. Wyporzyczyć książkę')
        print('2. Zwrócić książkę')
        print('3. Wyjść do głównego menu')
        code = input()
        match code.strip():
            case '1':
                name = input("Podaj imie: ")
                surname = input("Podaj nazwisko: ")
                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")
                try:
                    library.borrow_book(name, surname, title, author)
                except ReaderNotFound:
                    text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)
                except BookNotFound:
                    text = Fore.RED + 'KSIĄŻKA NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)

            case '2':
                name = input("Podaj imie: ")
                surname = input("Podaj nazwisko: ")

                try:
                    library.return_book(name, surname)
                except ReaderNotFound:
                    text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                    print(text)
            case '3':
                return library
            case _:
                print('Podany zły kod')

def new_interface(library:Library) -> Library:
    init()
    width = shutil.get_terminal_size().columns
    text = 'Witaj w bibliotece'
    ready_text = Fore.MAGENTA + text + Style.RESET_ALL

    print(ready_text.center(width))
    while True:
        try:
            print(Fore.LIGHTGREEN_EX + 'Wybierz kategorie: ' + Style.RESET_ALL)
            print('1. Czytelnik')
            print('2. Książki')
            print('3. Wypożyczenia')
            print('4. Wyjście z Programu')
            code = input()
            match code:
                case '1':
                    reader_interface(library)
                case '2':
                    book_interface(library)
                case '3':
                    rent_interface(library)
                case '4':
                    print("Do Widzenia".center(50, ' '))
                    return library
                case _:
                    print('Podany zły kod')
        except Exception:
            print(Style.BRIGHT +Fore.RED +  "Coś poszło nie tak w trakcie programu" + Style.RESET_ALL)

def interface(library:Library) -> Library:
    init()
    width = shutil.get_terminal_size().columns
    text = 'Witaj w bibliotece'
    ready_text = Fore.MAGENTA + text + Style.RESET_ALL

    print(ready_text.center(width))
    # ewentualnie biblioteka dla łatwiejszej składni
    # bo ta domyślna to mało wygodna
    while True:
        print("\n")
        # podzielić to na 3 sekcje
        # 1 to czcytlenice
        # 2 ksiżski
        # 3 wyporzycenia
        print('Możesz w niej zrobić:')
        print('\033[32m1. Dodać Czytelnika\033[0m')
        print('\033[31m2. Usunąć czytelnika\033[0m')
        print('3. Edytuj czytlenika')
        print('4. Wyświelt czytleników')
        print('5. Dodaj książkę')
        print('6. Usuń książkę')
        print('7. Edytuj książke')
        print('8. Wyświtl książki')
        print('9. Wyjść')
        print('10 Wypożyczenie książki')
        print('11 Zwrot książki')

        code = (int)(input())
        match (code):
            case 1:
                maxid = 0
                for readertmp in lib.list_of_readers:
                    if readertmp.id > maxid:
                        maxid = readertmp.id

                name = input("Podaj imie: ")
                surname = input("Podaj nazwisko: ")
                address = input("Podaj address: ")
                telephone_number = int(input("Podaj numer telefonu: "))
                reader = Reader(id = maxid, name = name, surname = surname, address = address, telephone_number = telephone_number)
                lib.add_reader(reader)

                print('\033[31mDodaleś Czytelnika\033[0m')
                print(lib.list_of_readers)
            case 2:
                name = input("Podaj imie czytelnika:")
                surname = input("Podaj nazwisko czytelnika:")
                library.remove_reader(name, surname)

                print('Usunałes')
            case 3:
                name = input("Podaj imie czytelnika:")
                surname = input("Podaj nazwisko czytelnika:")
                library.edit_reader(name, surname)

            case 4:
                # print("\n".join(str(p) for p in lib.list_of_readers))
                # df = pd.DataFrame(lib.list_of_readers)
                df = pd.DataFrame([vars(reader) for reader in lib.list_of_readers])
                df_better = df[['name', 'surname', 'address', 'telephone_number','charge']]
                # Display the DataFrame
                print(tabulate(df_better, headers = 'keys', tablefmt = 'psql'))
            case 5:
                maxid = 0
                for booktmp in lib.list_of_book:
                    print(type(booktmp))
                    if booktmp.id > maxid:
                        maxid = booktmp.id

                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")
                isbn = int(input("Podaj isbn: "))
                pages = int(input("Podaj ilość stron: "))
                book = Book(id = maxid+1, title = title, author = author, isbn = isbn, pages = pages)

                lib.add_book(book)
                print("ksiązka została dodana")
            case 6:
                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")


                library.remove_book(title, author)
            case 7:
                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")
                library.edit_book(title, author)
            case 8:
                print("\n".join(str(p) for p in lib.list_of_book))
            case 9:
                print("Do Widzenia".center(50, ' '))
                return library
            case 10:
                name = input("Podaj imie: ")
                surname = input("Podaj nazwisko: ")
                title = input("Podaj tytuł: ")
                author = input("Podaj autora: ")

                library.borrow_book(name, surname, title, author)
            case 11:
                name = input("Podaj imie: ")
                surname = input("Podaj nazwisko: ")

                library.return_book(name, surname)

# cos = Library()
# odczyt z pliku
with open("test.plk", "rb") as file:
    lib = pickle.load(file)

# print("\n".join(str(p) for p in lib.list_of_readers))

# lib = Library()

# print("\n".join(str(p) for p in lib.list_of_book))
#
# lib.list_of_book = []


# lib = interface(lib)

lib = new_interface(lib)



# Propozycja
# zapis do pliku po każdym działaniu programu aby nie tracić danych

# zapis do pliku
with open("test.plk", "wb") as file:
    pickle.dump(lib, file)


# dt1 = datetime(2024, 5, 1, 12, 30)
# dt2 = datetime(2025, 5, 17, 8, 15)
#
# roznica = dt2 - dt1
# print(roznica)            # pełna różnica (np. 380 days, 19:45:00)
# print(roznica.days)       # tylko dni
# print(roznica.total_seconds())