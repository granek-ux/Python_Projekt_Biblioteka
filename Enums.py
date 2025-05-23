from enum import Enum

class StatusEnum(Enum):
    Wolny = 'Wolny'
    Wyporzyczona = 'Wypożyczona'
    Zarezewowana_Wypozyczona = 'Zarezewowana Wypożyczona'
    Zarezewowana_Wolna = 'Zarezewowana Wolna'

class RegisterEnum(Enum):
    Wyporzyczenie = 'Wyporzyczenie'
    Oddanie = 'Oddanie'
    Zarezerwowanie = 'Zarezerwowanie'
    Rezerwacja_Oddanie = 'Rezerwacja Oddanie'
    Rezerwacja = 'Rezerwacja'