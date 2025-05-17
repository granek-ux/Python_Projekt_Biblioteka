from enum import Enum

class StatusEnum(Enum):
    Wolny = 'Wolny'
    Wyporzyczona = 'Wyporzyczona'
    Zarezewowana = 'Zarezewowana'

class RegisterEnum(Enum):
    Wyporzyczenie = 'Wyporzyczenie'
    Oddanie = 'Oddanie'