from entities.bus import Bus
from entities.route import Route
from entities.path import Path, MapPath, PathType
from entities.station import Station, StationType
from utils.observer import Observer
from const import *


class Generator(Observer):
    buses: []
    routes: []
    map_paths: []
    stations: []
    parking_lot: []
    __loaded: bool

    def __init__(self):
        self.buses = []
        self.routes = []
        self.map_paths = []
        self.stations = []
        self.parking_lot = []
        self.__loaded = False
        self.start_x_map = padding_left_canvas
        self.end_x_map = width_canvas - padding_right_canvas
        self.start_y_map = padding_top_canvas
        self.end_y_map = height_canvas - padding_bottom_canvas

    def update(self) -> None:
        print("Generador notificado...")

    def load_map(self):
        if self.__loaded:
            self.buses = []
            self.routes = []
            self.map_paths = []
            self.stations = []
            self.parking_lot = []
        self.load_map_paths()
        self.load_stations()
        self.load_parking_lot()
        self.load_map_paths()
        self.load_routes()
        self.load_buses()
        self.__loaded = True

    def load_parking_lot(self):
        stn1 = Station(capacity=10, location=(40, 40), use=0, stn_type=StationType.PARKING)
        stn2 = Station(capacity=5, location=(width_canvas - 40, height_canvas - 40),
                       use=0, stn_type=StationType.PARKING)

        self.parking_lot.append(stn1)
        self.parking_lot.append(stn2)

    def load_map_paths(self):
        # Caminos Horizontales
        path0_hrzs = MapPath(start=(self.start_x_map, self.start_y_map),
                             end=((self.end_x_map+self.start_x_map)/2, self.start_y_map),
                             path_type=PathType.HORIZONTAL)
        path1_hrzs = MapPath(start=((self.end_x_map+self.start_x_map)/2, self.start_y_map),
                             end=(self.end_x_map, self.start_y_map),
                             path_type=PathType.HORIZONTAL)

        path2_hrzs = MapPath(start=(self.start_x_map, (self.end_y_map+self.start_y_map)/2),
                             end=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                             path_type=PathType.HORIZONTAL)
        path3_hrzs = MapPath(start=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                             end=(self.end_x_map, (self.end_y_map+self.start_y_map)/2),
                             path_type=PathType.HORIZONTAL)

        path4_hrzs = MapPath(start=(self.start_x_map, self.end_y_map),
                             end=((self.end_x_map+self.start_x_map)/2, self.end_y_map),
                             path_type=PathType.HORIZONTAL)
        path5_hrzs = MapPath(start=((self.end_x_map+self.start_x_map)/2, self.end_y_map),
                             end=(self.end_x_map, self.end_y_map),
                             path_type=PathType.HORIZONTAL)

        # Caminos Verticales
        path0_vert = MapPath(start=(self.start_x_map, self.start_y_map),
                             end=(self.start_x_map, (self.end_y_map+self.start_y_map)/2), path_type=PathType.VERTICAL)
        path1_vert = MapPath(start=(self.start_x_map, (self.end_y_map+self.start_y_map)/2),
                             end=(self.start_x_map, self.end_y_map), path_type=PathType.VERTICAL)

        path2_vert = MapPath(start=((self.end_x_map+self.start_x_map)/2, self.start_y_map),
                             end=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                             path_type=PathType.VERTICAL)
        path3_vert = MapPath(start=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                             end=((self.end_x_map+self.start_x_map)/2, self.end_y_map), path_type=PathType.VERTICAL)

        path4_vert = MapPath(start=(self.end_x_map, self.start_y_map),
                             end=(self.end_x_map, (self.end_y_map+self.start_y_map)/2), path_type=PathType.VERTICAL)
        path5_vert = MapPath(start=(self.end_x_map, (self.end_y_map+self.start_y_map)/2),
                             end=(self.end_x_map, self.end_y_map), path_type=PathType.VERTICAL)

        # Caminos Diagonales
        path0_diag = MapPath(start=(self.start_x_map, self.start_y_map),
                             end=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                             path_type=PathType.DIAGONAL)
        path1_diag = MapPath(start=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                             end=(self.end_x_map, self.end_y_map), path_type=PathType.DIAGONAL)
        path2_diag = MapPath(start=(self.start_x_map, self.end_y_map),
                             end=(self.end_x_map, self.start_y_map), path_type=PathType.DIAGONAL)

        self.map_paths.append(path0_hrzs)
        self.map_paths.append(path1_hrzs)
        self.map_paths.append(path2_hrzs)
        self.map_paths.append(path3_hrzs)
        self.map_paths.append(path4_hrzs)
        self.map_paths.append(path5_hrzs)

        self.map_paths.append(path0_vert)
        self.map_paths.append(path1_vert)
        self.map_paths.append(path2_vert)
        self.map_paths.append(path3_vert)
        self.map_paths.append(path4_vert)
        self.map_paths.append(path5_vert)

        self.map_paths.append(path0_diag)
        self.map_paths.append(path1_diag)
        self.map_paths.append(path2_diag)

    def load_routes(self):
        path0_route1 = Path(start=(40, 40), end=(40, height_canvas / 2))
        path1_route1 = Path(start=(40, height_canvas / 2),
                            end=(width_canvas / 2, height_canvas / 2))
        path2_route1 = Path(start=(width_canvas / 2, height_canvas / 2),
                            end=(width_canvas - 40, height_canvas / 2))
        path3_route1 = Path(start=(width_canvas - 40, height_canvas / 2),
                            end=(width_canvas - 40, height_canvas - 40))

        path0_route2 = Path(start=(40, 40), end=(width_canvas / 2, 40))
        path1_route2 = Path(start=(width_canvas / 2, 40), end=(width_canvas / 2, height_canvas / 2))
        stn: Station = self.stations[3]
        path2_route2 = Path(start=(width_canvas / 2, height_canvas / 2), end=stn.get_location(),
                            station=self.stations[3])
        path3_route2 = Path(start=stn.get_location(), end=(width_canvas - 40, 40))
        path4_route2 = Path(start=(width_canvas - 40, 40), end=(width_canvas - 40, height_canvas - 40))

        (x_med, y_med) = ((self.end_x_map + self.start_x_map) / 2, (self.end_y_map + self.start_y_map) / 2)
        path0_route3 = Path(start=(40, 40), end=(x_med / 2, y_med / 2))
        path1_route3 = Path(start=(x_med / 2, y_med / 2), end=(x_med, y_med))
        stn: Station = self.stations[1]
        path2_route3 = Path(start=(width_canvas / 2, height_canvas / 2), end=stn.get_location(),
                            station=self.stations[1])
        path3_route3 = Path(start=stn.get_location(), end=(3 * width_canvas / 4, 3 * height_canvas / 4),)
        path4_route3 = Path(start=(3 * width_canvas / 4, 3 * height_canvas / 4),
                            end=(width_canvas - 40, height_canvas - 40))

        path_retorno1 = Path(start=(width_canvas - 40, height_canvas - 40),
                             end=(40, height_canvas - 40))
        path_retorno2 = Path(start=(40, height_canvas - 40), end=(40, 40), station=self.parking_lot[0])

        route1 = Route()
        route1.add_path(path0_route1)
        route1.add_path(path1_route1)
        route1.add_path(path2_route1)
        route1.add_path(path3_route1)
        route1.add_path(path_retorno1)
        route1.add_path(path_retorno2)

        route2 = Route()
        route2.add_path(path0_route2)
        route2.add_path(path1_route2)
        route2.add_path(path2_route2)
        route2.add_path(path3_route2)
        route2.add_path(path4_route2)
        route2.add_path(path_retorno1)
        route2.add_path(path_retorno2)

        route3 = Route()
        route3.add_path(path0_route3)
        route3.add_path(path1_route3)
        route3.add_path(path2_route3)
        route3.add_path(path3_route3)
        route3.add_path(path4_route3)
        route3.add_path(path_retorno1)
        route3.add_path(path_retorno2)

        self.routes.append(route1)
        self.routes.append(route2)
        self.routes.append(route3)

    def load_buses(self):

        bus1 = Bus(parking=self.parking_lot[0], capacity=50, use=10, speed=80)
        bus1.set_route(self.routes[0])
        self.buses.append(bus1)

        bus2 = Bus(parking=self.parking_lot[0], capacity=50, use=15, speed=140)
        bus2.set_route(self.routes[1])
        self.buses.append(bus2)

        bus3 = Bus(parking=self.parking_lot[0], capacity=50, use=5, speed=120)
        bus3.set_route(self.routes[2])
        self.buses.append(bus3)

    def load_stations(self):
        (x_med, y_med) = ((self.end_x_map + self.start_x_map) / 2, (self.end_y_map + self.start_y_map) / 2)
        stn1 = Station(location=((x_med+self.start_x_map)/2, (y_med+self.start_y_map)/2),
                       use=50, capacity=100, stn_type=StationType.STATION)
        stn2 = Station(location=((self.end_x_map+self.start_x_map)/2, (self.end_y_map+self.start_y_map)/2),
                       use=40, capacity=100, stn_type=StationType.STATION)
        stn3 = Station(location=((x_med+self.end_x_map) / 2, (y_med+self.end_y_map) / 2),
                       use=30, capacity=100, stn_type=StationType.STATION)

        stn4 = Station(location=((self.end_x_map+x_med)/2, (self.start_y_map+y_med) / 2),
                       use=20, capacity=100, stn_type=StationType.STATION)
        stn5 = Station(location=((x_med+self.start_x_map) / 2, (y_med+self.end_y_map) / 2),
                       use=10, capacity=100, stn_type=StationType.STATION)

        self.stations.append(stn1)
        self.stations.append(stn2)
        self.stations.append(stn3)
        self.stations.append(stn4)
        self.stations.append(stn5)

