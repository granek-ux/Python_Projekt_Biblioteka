from enum import Enum

class StatusEnum(Enum):
    Wolny = 'Wolny'
    Wypozyczona = 'Wypożyczona'
    Zarezerwowana_Wypozyczona = 'Zarezewowana Wypożyczona'
    Zarezerwowana_Wolna = 'Zarezewowana Wolna'

class RegisterEnum(Enum):
    Wypozyczenie = 'Wypożyczenie'
    Oddanie = 'Oddanie'
    Zarezerwowanie = 'Zarezerwowanie'
    Rezerwacja_Oddanie = 'Rezerwacja Oddanie'
    Rezerwacja = 'Rezerwacja'
    Przedluzenie = "Przedluzenie"