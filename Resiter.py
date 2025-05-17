from datetime import date

from Enums import RegisterEnum


class Register:
    def __init__(self, reader_id, book_id, date:date, operation:RegisterEnum):
        self.reader_id = reader_id
        self.book_id = book_id
        self.date = date
        self.operation = operation


