class Book:
    # działa jak static w java to nextID
    nextId = 1

    def __init__(self, title: str, author: str, isbn: int, pages: int)->None:
        self._id = Book.nextId
        Book.nextId += 1
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pages = pages
