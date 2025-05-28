class ReaderNotFound(Exception):
    # kiedy nie znajdzie się czytlenika o podanym id
    pass

class BookNotFound(Exception):
    pass

class BookNotRegistered(Exception):
    #kiedy nie ma ksiązki w bibliotece
    pass

class BookAlreadyTaken(Exception):
    #kiedy nie ma wolej książki
    pass

class NoBookReserved(Exception):
    #kiedy nie ma zarezerwowanej książki
    pass

class ExtendNotPossible(Exception):
    #kiedy nie można przedłużyć wypożyczenia z powodu rezerwacji
    pass

class NoAvailableBooks(Exception):
    #kiedy nie ma wolnych książek
    pass

class NoBorrowedBooks(Exception):
    #kiedy nie ma wypożyczonych książek
    pass

class NoHistory(Exception):
    #kiedy nie ma historii wypożyczeń
    pass

class WrongCode(Exception):
    pass

class WrongPagesNumber(Exception):
    # kiedy liczba stron jest mniejsza lub równa 0
    pass