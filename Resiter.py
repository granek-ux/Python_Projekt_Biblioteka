from datetime import date

class Register:
    def __init__(self, reader_id, book_id, date:date, operation):
        self.reader_id = reader_id
        self.book_id = book_id
        self.date = date
        self.operation = operation


