import os
import pickle

from Book import Book
from Library import Library
from colorama import init, Fore, Style
import shutil
from pprint import pprint
from datetime import date, datetime

from Reader import Reader


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
        print('Możesz w miej zrobić:')
        print('\033[32m1. Dodać Czytelnika\033[0m')
        print('\033[31m2. Usunąć czytelnika\033[0m')
        print('3. Edytuj czytlenika')
        print('4. Wyświelt czytleników')
        print('5. Dodaj książkę')
        print('6. Usuń książkę')
        print('7. Edytuj książke')
        print('8. Wyświtl ksiązki')
        print('9. Wyjść')
        print('10 Wypożyczenie książki')
        print('11 Zwrot książki')

        code = (int)(input())
        match (code):
            case 1:
                print('\033[31mDodaleś Czytelnika\033[0m')
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
                print("\n".join(str(p) for p in lib.list_of_readers))
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

# cos = Library()
# odczyt z pliku
with open("test.plk", "rb") as file:
    lib = pickle.load(file)

# print("\n".join(str(p) for p in lib.list_of_readers))

# lib = Library()

# print("\n".join(str(p) for p in lib.list_of_book))
#
# lib.list_of_book = []


lib = interface(lib)




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