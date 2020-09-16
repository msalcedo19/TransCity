
class Parking:
    """Clase que representa al objeto parqueadero.

        Atributos:
        capacity -- Capacidad de buses
        use -- Cantidad actual de buses
        location -- Ubicación del parqueadero (x,y)

        """

    __capacity: int
    __use: int
    __location: (int, int)

    def __init__(self, capacity: int, location: (int, int)):
        self.__capacity = capacity
        self.__use = 0
        self.__location = location

    def get_capacity(self):
        return self.__capacity

    def set_capacity(self, cap: int):
        self.__capacity = cap

    def get_use(self):
        return self.__use

    def set_use(self, use: int):
        self.__use = use

    def increase_use(self):
        self.__use += 1

    def set_location(self, x: int, y: int):
        self.__location = (x, y)

    def get_location(self) -> (int, int):
        return self.__location
