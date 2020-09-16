from entities.route import Route
from entities.parking import Parking


class Bus:
    """Clase que representa al objeto bus.

        Atributos:
        speed -- Velocidad del bus
        route -- Ruta asignada
        parking -- Parqueadero donde se encuentra el bus
        capacity -- Capacidad de pasajeros
        use -- Cantidad actual de pasajeros

        """
    __speed: float = 0
    __route: Route
    __parking: Parking
    __capacity: int
    __use: int

    def __init__(self, parking: Parking, capacity: int, use: int, speed: float):
        self.__speed = speed
        self.__route = Route()
        self.__parking = parking
        self.__capacity = capacity
        self.__use = use

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

    def set_parking(self, parking: Parking):
        self.__parking = parking

    def get_use(self):
        return self.__use

    def set_use(self, use: int):
        self.__use = use

