import pickle
from Book import Book
from Library import Library
from colorama import init, Fore, Style
import shutil


def interface(library:Library) -> Library:
    init()
    width = shutil.get_terminal_size().columns
    text = 'Witaj w bibliotece'
    ready_text = Fore.MAGENTA + text + Style.RESET_ALL

    print(ready_text.center(width))
    # ewentualnie biblioteka dla łatwiejszej składni
    # bo ta domyślna to mało wygodna
    while True:
        print('Możesz w miej zrobić:')
        print('\033[32m1. Dodać Czytelnika\033[0m')
        print('\033[31m2. Usunąć czytelnika')
        print('3. Wyjść ')

        code = (int)(input())
        match (code):
            case 1:
                print('\033[31mDodaleś Czytelnika\033[0m')
            case 2:
                print('Usunałes')
            case 3:
                print("Do Widzenia".center(50, ' '))
                return library

# cos = Library()
# odczyt z pliku
with open("test.plk", "rb") as file:
    lib = pickle.load(file)


lib = interface(lib)


# Propozycja
# zapis do pliku po każdym działaniu programu aby nie tracić danych

# zapis do pliku
with open("person.pkl", "wb") as file:
    pickle.dump(lib, file)
