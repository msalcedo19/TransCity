from entities.station import Station
from entities.route import Route
from datetime import datetime


class User:
    """Clase que representa al objeto usuario/pasajero.

        Parámetros:
        destination -- Estación de destino del pasajero
        source -- Estación de inicio del pasajero
        start_date_trip -- Fecha en la que el pasajero empezo el viaje
        end_date_trip -- Fecha en la que el pasajero termino su viaje
        code -- Identificador único del usuario

        """
    __destination: Station
    __source: Station
    __route: Route
    __start_date_trip: datetime
    __end_date_trip: datetime
    __code: int

    def __init__(self, dest: Station, src: Station, route: Route, code: int):
        self.__destination = dest
        self.__source = src
        self.__route = route
        self.__code = code
        self.__end_date_trip = None

    def get_code(self):
        return self.__code

    def end_trip(self):
        self.__end_date_trip = datetime.now()

    def start_trip(self):
        self.__start_date_trip = datetime.now()

    def get_src(self):
        return self.__source

    def get_dest(self):
        return self.__destination

    def get_route(self):
        return self.__route

    def get_start_trip(self):
        return self.__start_date_trip

    def get_end_trip(self):
        return self.__end_date_trip
