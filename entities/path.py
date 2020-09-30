from enum import Enum


class MoveTypeV2(Enum):
    VERTICAL_ARRIBA = 0
    VERTICAL_ABAJO = 1
    HORIZONTAL_DERECHA = 2
    HORIZONTAL_IZQUIERDA = 3
    DETENIDO = 4
    DIAG_DER_ARR = 5
    DIAG_DER_ABJ = 6
    DIAG_IZQ_ARR = 7
    DIAG_IZQ_ABJ = 8


class PathType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    DIAGONAL = 2


class MapPath:
    __startPoint: (int, int)
    __endPoint: (int, int)
    __pathType: PathType
    __id: int

    def __init__(self, start: (int, int), end: (int, int), path_type: PathType):
        self.__startPoint = start
        self.__endPoint = end
        self.__pathType = path_type
        self.__id = None

    def set_id(self, id: int):
        self.__id = id

    def set_start_point(self, x: int, y: int):
        self.__startPoint = (x, y)

    def set_end_point(self, x: int, y: int):
        self.__endPoint = (x, y)

    def get_start_point(self) -> (int, int):
        return self.__startPoint

    def get_end_point(self) -> (int, int):
        return self.__endPoint

    def set_path_type(self, path_type: PathType):
        self.__pathType = path_type

    def get_path_type(self) -> PathType:
        return self.__pathType


class Path:
    """Clase que representa al objeto camino.

        Atributos:
        startPoint -- Punto donde inicia el tramo del camino (x,y)
        endPoint -- Punto donde finaliza el tramo del camino (x,y)
        typeMov -- Tipo de movimiento que se realiza durante el tramo
        station -- Indica la estación asociada a ese tramo

        """
    __mapPath: MapPath
    __typeMove: MoveTypeV2

    def __init__(self, start: (int, int), end: (int, int) = None, station=None):
        self.__startPoint = start
        self.__endPoint = end
        self.__station = station
        self.define_move_type()

    def define_move_type(self):
        if self.__endPoint is None:
            self.__typeMove = MoveTypeV2.DETENIDO
        else:
            (x_init, y_init) = self.__startPoint
            (x_final, y_final) = self.__endPoint

            # No movimiento
            if x_init == x_final and y_init == y_final:
                self.__typeMove = MoveTypeV2.DETENIDO
            # Movimiento vertical
            elif x_init == x_final:
                if y_init > y_final:
                    self.__typeMove = MoveTypeV2.VERTICAL_ARRIBA
                else:
                    self.__typeMove = MoveTypeV2.VERTICAL_ABAJO
            # Movimiento Horizontal
            elif y_init == y_final:
                if x_init > x_final:
                    self.__typeMove = MoveTypeV2.HORIZONTAL_IZQUIERDA
                else:
                    self.__typeMove = MoveTypeV2.HORIZONTAL_DERECHA
            # Movimiento Diagonal
            else:
                if x_init > x_final and y_init > y_final:
                    self.__typeMove = MoveTypeV2.DIAG_IZQ_ARR
                elif x_init > x_final and y_init < y_final:
                    self.__typeMove = MoveTypeV2.DIAG_IZQ_ABJ
                elif x_init < x_final and y_init > y_final:
                    self.__typeMove = MoveTypeV2.DIAG_DER_ARR
                elif x_init < x_final and y_init < y_final:
                    self.__typeMove = MoveTypeV2.DIAG_DER_ABJ

    # Retorna False si ya llego al punto de destino, True de lo contrario.
    def path_state(self, x: int, y: int):
        if self.__endPoint is not None:
            (x_final, y_final) = self.__endPoint
            x_aux = (x - x_final)/2
            y_aux = (y - y_final)/2
            dist = pow(pow(x_aux, 2) + pow(y_aux, 2), 0.5)
            if dist >= 0.3:
                return True
        return False

    def set_start_point(self, x: int, y: int):
        self.__startPoint = (x, y)

    def set_end_point(self, x: int, y: int):
        self.__endPoint = (x, y)

    def get_start_point(self) -> (int, int):
        return self.__startPoint

    def get_end_point(self) -> (int, int):
        return self.__endPoint

    def get_type_move(self) -> MoveTypeV2:
        return self.__typeMove

    def get_station(self):
        return self.__station
