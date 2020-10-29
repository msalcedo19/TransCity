from entities.route import Route
from entities.station import Station


class Bus:
    """Clase que representa al objeto bus.

        Atributos:
        speed -- Velocidad del bus
        route -- Ruta asignada
        parking -- Parqueadero donde se encuentra el bus
        capacity -- Capacidad de pasajeros
        use -- Cantidad actual de pasajeros
        color -- color del bus
        code -- identificador único del bus
        users -- usuarios que se encuentran actualmente dentro del bus

        """
    __speed: float = 0
    __route: Route
    __parking: Station
    __capacity: int
    __use: int
    __color: str
    __code: int
    __users: []

    def __init__(self, parking: Station, capacity: int, use: int, speed: float, color: str, code: int, route: Route):
        super().__init__()
        self.__speed = speed
        self.__route = route
        self.__parking = parking
        self.__capacity = capacity
        self.__use = use
        self.__color = color
        self.__id_object = None
        self.__code = code
        self.__users = []

    def encode(self):
        return dict(code=self.__code, speed=self.__speed, route=self.__route.encode(), parking=self.__parking.encode())

    def add_user(self, user):
        self.__users.append(user)
        self.increase_use()

    def del_user(self, user):
        self.__users.remove(user)
        self.decrease_user()

    def users(self):
        return self.__users

    def set_id(self, id_bus: int):
        self.__id_object = id_bus

    def get_id(self):
        return self.__id_object

    def get_code(self):
        return self.__code

    def get_capacity(self):
        return self.__capacity

    def set_capacity(self, cap: int):
        self.__capacity = cap

    def set_route(self, route: Route):
        self.__route = route

    def get_route(self) -> Route:
        return self.__route

    def set_speed(self, speed: int):
        self.__speed = speed

    def get_speed(self) -> float:
        return self.__speed

    def set_parking(self, parking: Station):
        self.__parking = parking

    def get_parking(self):
        return self.__parking

    def get_use(self):
        return self.__use

    def increase_use(self):
        self.__use += 1

    def decrease_user(self):
        self.__use -= 1

    def set_use(self, use: int):
        self.__use = use

    def get_color(self):
        return self.__color

