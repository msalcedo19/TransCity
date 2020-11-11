from enum import Enum
from entities.station import Station


class MoveTypeV2(Enum):
    VERTICAL_ARRIBA = 'VERTICAL_ARRIBA'
    VERTICAL_ABAJO = 'VERTICAL_ABAJO'
    HORIZONTAL_DERECHA = 'HORIZONTAL_DERECHA'
    HORIZONTAL_IZQUIERDA = 'HORIZONTAL_IZQUIERDA'
    DETENIDO = 'DETENIDO'
    DIAG_DER_ARR = 'DIAG_DER_ARR'
    DIAG_DER_ABJ = 'DIAG_DER_ABJ'
    DIAG_IZQ_ARR = 'DIAG_IZQ_ARR'
    DIAG_IZQ_ABJ = 'DIAG_IZQ_ABJ'


class PathType(Enum):
    VERTICAL = 0
    HORIZONTAL = 1
    DIAGONAL = 2


class Path:
    """Clase que representa al objeto camino el cual pertenece a una ruta de un bus.

        Atributos:
        startPoint -- Punto donde inicia el tramo del camino (x,y)
        endPoint -- Punto donde finaliza el tramo del camino (x,y)
        typeMov -- Tipo de movimiento que se realiza durante el tramo
        station -- Indica la estación asociada a ese tramo
        block -- Indica si la estación se encuentra bloqueada
        code -- Identificador único del camino

        """
    __typeMove: MoveTypeV2
    __startPoint: (int, int)
    __endPoint: (int, int)
    __station: Station
    __block: bool
    __code: int

    def __init__(self, start: (int, int), end: (int, int), code: int, station=None):
        self.__startPoint = start
        self.__endPoint = end
        self.__station = station
        self.define_move_type()
        self.__block = False
        self.__code = code

    def encode(self):
        station = None
        if self.__station:
            station = self.__station.get_code()
        return dict(start=self.__startPoint, end=self.__endPoint, isBlock=self.__block, station=station,
                    typeMove=self.__typeMove.value)

    def get_code(self):
        return self.__code

    def block(self):
        self.__block = True

    def unblock(self):
        self.__block = False

    def is_block(self):
        return self.__block

    def define_move_type(self):
        """Define el tipo de movimiento que hara el bus por este tramo."""

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
        """Determina si las coordenadas actuales del bus coinciden con las coordenadas finales del tramo.

            Parámetros:
            x -- Coordenada en x
            y -- Coordenada en y

            """
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

    def set_station(self, stn: Station):
        self.__station = stn
