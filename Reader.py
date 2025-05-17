class Reader:

    def __init__(self, id: int, name: str, surname: str, address: str, telephone_number: int) -> None:
        self._id = id
        self.name = name
        self.surname = surname
        self.address = address
        self.telephone_number = telephone_number
        self.list_of_registers = []
    #     histoira

    @property
    def id(self):
        return self._id


    def __str__(self):
        return f"Imie: {self.name}, Nazwisko: {self.surname}, Adres: {self.address}, Numer telefonu: {self.telephone_number}"
