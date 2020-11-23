from enum import Enum


class StationType(Enum):
    PARKING = 'P'
    STATION = 'S'


class Station:
    """Clase que representa al objeto estación.

        Atributos:
        location -- Coordenadas donde se encuentra la estación
        capacity -- Capacidad máxima de la estación
        use -- Cantidad de buses/pasajeros en la estación
        type -- Tipo de estación (Parqueadero de buses o estación de pasajeros)
        isClose -- Indica si la estación se encuentra cerrada
        users -- Pasajeros/Buses que se encuentran en la estación
        code -- Identificador único de la estación

        """

    __location: (int, int)
    __capacity: int
    __use: int
    __type: StationType
    __isClose: bool
    __code: int
    __users: []

    def __init__(self, location: (int, int), use: int, capacity: int, code: int, stn_type: StationType = 'S'):
        self.__location = location
        self.__use = use
        self.__capacity = capacity
        self.color = '#4571EC'
        self.__type = stn_type
        self.__isClose = False
        self.__code = code
        self.__users = []

        self.id_text_object = None
        self.id_object = None
        self.btn_id = None
        self.btn_close = None

    def __eq__(self, other_stn):
        return self.__code == other_stn.get_code()

    def __str__(self):
        return "Station " + str(self.__code)

    def encode(self):
        users = []
        for user in self.__users:
            users.append(user.get_code())
        return dict(location=self.__location, capacity=self.__capacity, use=self.__use, isClose=self.__isClose,
                    type=self.__type.value, color=self.color, users=users)

    def new_user(self, user):
        self.__users.append(user)
        self.increase_user()

    def del_user(self, user):
        self.__users.remove(user)
        self.decrease_user()

    def users(self):
        return self.__users

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

    def increase_user(self):
        self.__use += 1

    def decrease_user(self):
        self.__use -= 1

    def close(self):
        self.__isClose = True

    def open(self):
        self.__isClose = False

    def is_close(self):
        return self.__isClose
