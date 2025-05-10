import pickle

from Book import Book
from Library import Library


def interface()-> None:
    print('\033[31mWitaj w bibliotece\033[0m'.center(50,' '))
    # ewentualnie biblioteka dla łatwiejszej składni
    #bo ta domyślna to mało wygodna
    print('Możesz w miej zrobić:')
    print('\033[32m1. Dodać Czytelnika\033[0m')
    print('\033[31m2. Usunąć czytelnika')
    print('3. Wyjść ')





    code = (int) (input())
    match(code):
        case 1:
            print('\033[31mDodaleś Czytelnika\033[0m')
        case 2:
            print('Usunałes')
        case 3:
            print("Do Widzenia".center(50,' '))

interface()

cos = Library()

#Propozycja
#zapis do pliku po każdym działaniu programu aby nie tracić danych
#zapis do pliku
with open("person.pkl", "wb") as file:
    pickle.dump(cos, file)

# odczyt z pliku
with open("test.plk", "rb") as file:
    cos = pickle.load(file)

