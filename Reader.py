class Reader:
    # działa jak static w java to nextID
    nextId = 1

    def __init__(self, name:str, surname:str, address:str, telephone_number:int) -> None:
        self._id = Reader.nextId
        Reader.nextId += 1
        self.name = name
        self.surname = surname
        self.address = address
        self.telephone_number = telephone_number
