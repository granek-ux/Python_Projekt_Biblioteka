from Enums import StatusEnum


class Book:

    def __init__(self, id: int, title: str, author: str, isbn: int, pages: int) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pages = pages
        self.status = StatusEnum.Wolny
        self.borrow_date = None

    def __str__(self):
        return f"id: {self.id}, {self.title}, {self.author}, {self.isbn}, {self.pages}"


