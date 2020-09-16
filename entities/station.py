class Station:
    __location: (int, int)
    __passengers: int
    __id: int

    def __init__(self, location: (int, int), passengers: int):
        self.__location = location
        self.__passengers = passengers
        self.__id = None

    def set_location(self, x: int, y: int):
        self.__location = (x, y)

    def set_id(self, id_text: int):
        self.__id = id_text

    def get_id(self):
        return self.__id

    def get_location(self) -> (int, int):
        return self.__location

    def get_passengers(self):
        return self.__passengers

    def set_passengers(self, passengers: int):
        self.__passengers = passengers
