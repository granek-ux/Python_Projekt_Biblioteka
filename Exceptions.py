# propozycja aby wszytkie wyjątki w 1 miescju
# albo tym pliku
#albo w róznych plikach ale w 1 folderze

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