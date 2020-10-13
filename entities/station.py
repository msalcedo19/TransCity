from enum import Enum


class StationType(Enum):
    PARKING = 0
    STATION = 1


class Station:
    __location: (int, int)
    __capacity: int
    __use: int
    __type: StationType
    __isClose: bool
    __code: int

    def __init__(self, location: (int, int), use: int, capacity: int, code: int, stn_type: StationType = 1):
        self.__location = location
        self.__use = use
        self.__capacity = capacity
        self.color = '#4571EC'
        self.__type = stn_type
        self.__isClose = False
        self.__code = code

        self.id_text_object = None
        self.id_object = None

    def get_code(self):
        return self.__code

    def set_location(self, x: int, y: int):
        self.__location = (x, y)

    def get_location(self) -> (int, int):
        return self.__location

    def get_use(self):
        return self.__use

    def set_use(self, use: int):
        self.__use = use

    def get_capacity(self):
        return self.__capacity

    def set_capacity(self, cap: int):
        self.__capacity = cap

    def get_type(self):
        return self.__type

    def increase_use(self):
        self.__use += 1

    def close(self):
        self.__isClose = True

    def open(self):
        self.__isClose = False

    def is_close(self):
        return self.__isClose
