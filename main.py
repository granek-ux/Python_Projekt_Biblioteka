import os
import subprocess
import sys
import pickle
from Book import Book
from Enums import StatusEnum
from Exceptions import *
from Library import Library
from colorama import init, Fore, Style
import shutil
import pandas as pd
from tabulate import tabulate
from Reader import Reader


def check_and_install(package):
    try:
         __import__(package)
         print(f"{package} jest już zainstalowane.")
    except ImportError:
         print(f"{package} nie jest zainstalowane. Próbuję zainstalować...")
         subprocess.check_call([sys.executable, "-m", "pip", "install", package])
         print(f"{package} zostało pomyślnie zainstalowane.")

def reader_interface(library:Library) ->Library:
    while True:
        try:
            print(Fore.LIGHTGREEN_EX + '\nWybierz kategorie: ' + 'Jesteś w sekcji czytelnika: ' +Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX + 'możesz w niej zrobić' +Style.RESET_ALL)
            print('1. Dodać nowego czytelnika')
            print('2. Usunąć czytelnika')
            print('3. Edytować czytelnika')
            print('4. Wyświetlić wszystkich czytelników')
            print('5. Wyświetlenie historii czytelnika')
            print('6. Cofnij do głównego Menu (q)')
            code = input(Fore.LIGHTYELLOW_EX + '> ' +Style.RESET_ALL)
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

                    # print('\033[31mDodaleś Czytelnika\033[0m')
                    print(Fore.LIGHTBLUE_EX + 'Dodaleś Czytelnika' + Style.RESET_ALL)
                case '2':
                    name = input("Podaj imie czytelnika:")
                    surname = input("Podaj nazwisko czytelnika:")
                    try:
                        library.remove_reader(name, surname)
                        print(Fore.LIGHTBLUE_EX+'Usunałes'+Style.RESET_ALL)
                    except ReaderNotFound:
                        text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                        print(text)


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
                    name = input("Podaj imie czytelnika: ")
                    surname = input("Podaj nazwisko czytelnika: ")
                    try:
                        library.reader_history(name, surname)
                    except ReaderNotFound:
                        text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                        print(text)
                    except NoHistory:
                        text = Fore.RED + 'BRAK HISTORII CZYTELNIKA' + Style.RESET_ALL
                        print(text)
                case '6':
                    return library
                case 'q':
                    return library
                case _:
                    raise WrongCode
        except WrongCode:
            print(Fore.RED + 'Podany zły kod' + Style.RESET_ALL)

def show_Books(library:Library):
    print(Fore.LIGHTGREEN_EX + '\nMożesz wyśiwtlić: ' +Style.RESET_ALL)
    print("1. Wszystkie dostępne książki")
    print('2. Wszytskie wypożyczone książki')
    while True:
        code = input(Fore.LIGHTYELLOW_EX + '> ' +Style.RESET_ALL)
        try:
            match code.strip():
                case '1':
                    df = pd.DataFrame([vars(book) for book in library.list_of_book if book.status == StatusEnum.Wolny])
                    if df.empty:
                        raise NoAvailableBooks
                    df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
                    print(tabulate(df_better, headers='keys', tablefmt='psql'))
                    return
                case '2':
                    df = pd.DataFrame([vars(book) for book in library.list_of_book if book.status == StatusEnum.Wypozyczona or book.status == StatusEnum.Zarezerwowana_Wypozyczona])
                    if df.empty:
                        raise NoBorrowedBooks
                    df_better = df[['title', 'author', 'isbn', 'pages', 'status']]
                    print(tabulate(df_better, headers='keys', tablefmt='psql'))
                    return
                case _:
                    raise WrongCode
        except NoAvailableBooks:
            text = Fore.RED + 'BRAK DOSTĘPNYCH KSIĄŻEK' + Style.RESET_ALL
            print(text)
            return
        except NoBorrowedBooks:
            text = Fore.RED + 'BRAK WYPOŻYCZONYCH KSIĄŻEK' + Style.RESET_ALL
            print(text)
            return
        except WrongCode:
            print(Fore.RED + 'Podany zły kod' + Style.RESET_ALL)


def book_interface(library:Library)->Library:
    while True:
        try:
            print(Fore.LIGHTGREEN_EX+'\nJesteś w sekcji książek: '+Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX+'możesz w niej zrobić: '+Style.RESET_ALL)
            print('1. Dodać nową książkę')
            print('2. Usunąć książkę')
            print('3. Edytować książkę')
            print('4. Wyświetlić książki')
            print('5. Cofnij do głównego Menu (q)')
            code = input(Fore.LIGHTYELLOW_EX + '> ' +Style.RESET_ALL)
            match code.strip():
                case '1':
                    maxid = 0
                    for booktmp in lib.list_of_book:
                        if booktmp.id > maxid:
                            maxid = booktmp.id

                    title = input("Podaj tytuł: ")
                    author = input("Podaj autora: ")
                    isbn = int(input("Podaj isbn: "))
                    pages = int(input("Podaj ilość stron: "))
                    if pages <= 0:
                        raise WrongPagesNumber
                    book = Book(id=maxid + 1, title=title, author=author, isbn=isbn, pages=pages)

                    lib.add_book(book)
                    print(Fore.LIGHTBLUE_EX+"ksiązka została dodana"+Style.RESET_ALL)
                case '2':
                    title = input("Podaj tytuł: ")
                    author = input("Podaj autora: ")
                    try:
                        library.remove_book(title, author)
                    except BookNotFound:
                        text = Fore.RED + 'KSIĄŻKA NIE ZNALEZIONA' + Style.RESET_ALL
                        print(text)
                case '3':
                    title = input("Podaj tytuł: ")
                    author = input("Podaj autora: ")
                    try:
                        library.edit_book(title, author)
                    except BookNotFound:
                        text = Fore.RED + 'KSIĄŻKA NIE ZNALEZIONA' + Style.RESET_ALL
                        print(text)
                case '4':
                    try:
                        show_Books(library)
                    except BookNotFound:
                        text = Fore.RED + 'KSIĄŻKA NIE ZNALEZIONA' + Style.RESET_ALL
                        print(text)
                    except ReaderNotFound:
                        text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                        print(text)
                        
                case '5':
                    return library
                case 'q':
                    return library
                case _:
                    raise WrongCode
        except WrongCode:
            print(Fore.RED + 'Podany zły kod' + Style.RESET_ALL)
        except WrongPagesNumber:
            text = Fore.RED + 'Liczba stron musi być większa od 0' + Style.RESET_ALL
            print(text)

def rent_interface(library:Library)->Library:
    while True:
        try:
            print(Fore.LIGHTGREEN_EX+'\nJesteś w sekcji Wypożyczenia: ' +Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX+'możesz w niej zrobić: ' +Style.RESET_ALL)
            print('1. Wypożyczyć książkę')
            print('2. Zwrócić książkę')
            print('3. Przedłuż wypożyczenie')
            print('4. Wyjść do głównego menu (q)')
            code = input(Fore.LIGHTYELLOW_EX + '> ' +Style.RESET_ALL)
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
                    name = input("Podaj imie: ")
                    surname = input("Podaj nazwisko: ")

                    try:
                        library.extend_borrow(name, surname)
                    except ReaderNotFound:
                        text = Fore.RED + 'CZYTELNIK NIE ZNALEZIONY' + Style.RESET_ALL
                        print(text)

                case '4':
                    return library
                case 'q':
                    return library
                case _:
                    raise WrongCode
        except WrongCode:
            print(Fore.RED + 'Podany zły kod' + Style.RESET_ALL)

def Reservation_interface(library:Library)->Library:
    while True:
        try:
            print(Fore.LIGHTGREEN_EX+ '\nJesteś w sekcji Rezerwacji: '+Style.RESET_ALL)
            print(Fore.LIGHTGREEN_EX+ 'możesz w niej zrobić: '+Style.RESET_ALL)
            print('1. Odebrać rezerwacje')
            print('2. Wyjść do głównego menu (q)')
            code = input(Fore.LIGHTYELLOW_EX + '> ' +Style.RESET_ALL)
            match code.strip():
                case '1':
                    name = input("Podaj imie: ")
                    surname = input("Podaj nazwisko: ")
                    try:
                        library.manage_reservation(name, surname ) #, title, author)
                    except NoBookReserved:
                        text = Fore.RED + 'BRAK ZAREZERWOWANYCH KSIĄŻEK' + Style.RESET_ALL
                        print(text)
                case '2':
                    return library
                case _:
                    raise WrongCode
        except WrongCode:
            print(Fore.RED + 'Podany zły kod' + Style.RESET_ALL)


def interface(library:Library) -> Library:
    init()
    width = shutil.get_terminal_size().columns
    text = 'Witaj w bibliotece'
    ready_text = Fore.MAGENTA + text + Style.RESET_ALL

    print(ready_text.center(width))
    while True:
        try:
            print(Fore.LIGHTGREEN_EX + '\nWybierz kategorie: ' + Style.RESET_ALL)
            print('1. Czytelnik')
            print('2. Książki')
            print('3. Wypożyczenia')
            print('4. Rezerwacje')
            print('5. Wyjście z Programu (q)')
            code = input(Fore.LIGHTYELLOW_EX + '> ' +Style.RESET_ALL)
            match code:
                case '1':
                    reader_interface(library)
                case '2':
                    book_interface(library)
                case '3':
                    rent_interface(library)
                case '4':
                    Reservation_interface(library)
                case '5':
                    print(Fore.MAGENTA + "Do Widzenia".center(50, ' '))
                    return library
                case 'q':
                    print(Fore.MAGENTA + "Do Widzenia".center(50, ' '))
                    return library
                case _:
                    raise WrongCode

            with open("Dane.plk", "wb") as file:
                pickle.dump(library, file)
        except WrongCode:
            print(Fore.RED + 'Podany zły kod' + Style.RESET_ALL)
        except Exception:
            print(Style.BRIGHT +Fore.RED +  "Coś poszło nie tak w trakcie programu" + Style.RESET_ALL)



check_and_install("tabulate")
check_and_install("pandas")
check_and_install("colorama")


with open("Dane.plk", "rb") as file:
    lib = pickle.load(file)

lib = interface(lib)

with open("Dane.plk", "wb") as file:
    pickle.dump(lib, file)

