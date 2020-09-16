from enum import Enum
from entities.station import Station


class TypeMove(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    DIAGONAL = 2
    DETENIDO = 4


class Path:
    """Clase que representa al objeto camino.

        Atributos:
        startPoint -- Punto donde inicia el tramo del camino (x,y)
        endPoint -- Punto donde finaliza el tramo del camino (x,y)
        typeMov -- Tipo de movimiento que se realiza durante el tramo
        reverse -- Indica si se recorrera el tramo en sentido contrario (endPoint a startPoint)
        station -- Indica la estación asociada a ese tramo

        """
    __startPoint: (int, int)
    __endPoint: (int, int)

    __typeMove: TypeMove
    __reverse: bool
    __station: Station

    def __init__(self, move: TypeMove, start: (int, int), end: (int, int), reverse: bool, station: Station = None):
        self.__startPoint = start
        self.__endPoint = end
        self.__typeMove = move
        self.__reverse = reverse
        self.__station = station

    def set_start_point(self, x: int, y: int):
        self.__startPoint = (x, y)

    def set_end_point(self, x: int, y: int):
        self.__endPoint = (x, y)

    def set_reverse(self, reverse: bool):
        self.__reverse = reverse

    def get_start_point(self) -> (int, int):
        return self.__startPoint

    def get_end_point(self) -> (int, int):
        return self.__endPoint

    def get_type_move(self) -> int:
        return self.__typeMove

    def get_reverse(self):
        return self.__reverse

    def get_station(self):
        return self.__station
