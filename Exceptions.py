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

#todo
# wiecej wyjątków!!!!!!!!
# z gpt do przemyślenia
# Możesz dodać następujące wyjątki, aby łącznie było ich co najmniej 10:
# ReaderAlreadyExists – gdy próbujesz dodać czytelnika, który już istnieje.
# BookAlreadyExists – gdy próbujesz dodać książkę, która już jest w bazie.
# MaxBooksLimitReached – gdy czytelnik przekroczył limit wypożyczonych książek.
# BookNotAvailable – gdy książka jest już wypożyczona przez kogoś innego.
# ReservationExpired – gdy rezerwacja książki wygasła.
# InvalidBookId – gdy podano nieprawidłowy identyfikator książki.
# InvalidReaderId – gdy podano nieprawidłowy identyfikator czytelnika.
# BookReturnLate – gdy książka została zwrócona po terminie.
# ReservationNotAllowed – gdy rezerwacja nie jest możliwa z powodu ograniczeń.
