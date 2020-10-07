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
            self.map_paths = []
            self.stations = []
            self.routes = []
            self.buses = []
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
        """path0_hrzs = MapPath(start=(self.start_x_map, self.start_y_map),
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
        (x_med, y_med) = ((self.end_x_map + self.start_x_map) / 2, (self.end_y_map + self.start_y_map) / 2)
        path0_diag = MapPath(start=(self.start_x_map, self.start_y_map),
                             end=((x_med+self.start_x_map)/2, (y_med+self.start_y_map)/2),
                             path_type=PathType.DIAGONAL)
        path1_diag = MapPath(start=((x_med+self.start_x_map)/2, (y_med+self.start_y_map)/2),
                             end=(x_med, y_med),
                             path_type=PathType.DIAGONAL)
        path2_diag = MapPath(start=(x_med, y_med),
                             end=((x_med+self.end_x_map)/2, (y_med+self.end_y_map)/2),
                             path_type=PathType.DIAGONAL)
        path3_diag = MapPath(start=((x_med+self.end_x_map)/2, (y_med+self.end_y_map)/2),
                             end=(self.end_x_map, self.end_y_map), path_type=PathType.DIAGONAL)

        path4_diag = MapPath(start=(self.end_x_map, self.start_y_map),
                             end=((x_med+self.end_x_map)/2, (y_med+self.start_y_map)/2),
                             path_type=PathType.DIAGONAL)
        path5_diag = MapPath(start=((x_med+self.end_x_map)/2, (y_med+self.start_y_map)/2),
                             end=(x_med, y_med),
                             path_type=PathType.DIAGONAL)
        path6_diag = MapPath(start=(x_med, y_med),
                             end=((x_med+self.start_x_map)/2, (y_med+self.end_y_map)/2),
                             path_type=PathType.DIAGONAL)
        path7_diag = MapPath(start=((x_med+self.start_x_map)/2, (y_med+self.end_y_map)/2),
                             end=(self.start_x_map, self.end_y_map), path_type=PathType.DIAGONAL)

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
        self.map_paths.append(path3_diag)
        self.map_paths.append(path4_diag)
        self.map_paths.append(path5_diag)
        self.map_paths.append(path6_diag)
        self.map_paths.append(path7_diag)"""
        self.map_paths = [[(40, 40), (40, 404)], [(40, 404), (40, 677)], [(40, 677), (116, 677)],
                          [(40, 404), (116, 404)], [(40, 40), (268, 40)], [(116, 222), (268, 222)],
                          [(116, 222), (116, 404)], [(116, 404), (116, 677)], [(268, 40), (268, 222)],
                          [(268, 40), (496, 40)], [(268, 222), (496, 222)], [(116, 404), (496, 404)],
                          [(116, 677), (420, 586)], [(420, 586), (572, 586)], [(496, 222), (496, 404)],
                          [(496, 40), (724, 40)], [(724, 40), (952, 40)], [(496, 222), (648, 222)],
                          [(648, 222), (800, 222)], [(496, 404), (800, 404)], [(572, 586), (800, 677)],
                          [(800, 131), (952, 131)], [(800, 404), (952, 404)], [(800, 677), (876, 677)],
                          [(876, 677), (952, 677)], [(800, 222), (800, 131)], [(800, 222), (800, 404)],
                          [(800, 404), (800, 586)], [(800, 586), (800, 677)], [(952, 40), (952, 131)],
                          [(952, 131), (952, 404)], [(952, 404), (952, 677)], [(496, 40), (496, 222)]]

    def load_routes(self):
        path0_route1 = Path(start=(40, 40), end=(40, 677))
        path1_route1 = Path(start=(40, 677), end=(116, 677))
        path2_route1 = Path(start=(116, 677), end=(420, 586))
        path3_route1 = Path(start=(420, 586), end=(572, 586))
        path4_route1 = Path(start=(572, 586), end=(800, 677))
        path5_route1 = Path(start=(800, 677), end=(800, 404))
        path6_route1 = Path(start=(800, 404), end=(496, 404))

        route1 = Route()
        route1.add_path(path0_route1)
        route1.add_path(path1_route1)
        route1.add_path(path2_route1)
        route1.add_path(path3_route1)
        route1.add_path(path4_route1)
        route1.add_path(path5_route1)
        route1.add_path(path6_route1)

        self.routes.append(route1)

    def load_buses(self):

        bus1 = Bus(parking=self.parking_lot[0], capacity=50, use=10, speed=120)
        bus1.set_route(self.routes[0])
        self.buses.append(bus1)

        """bus2 = Bus(parking=self.parking_lot[0], capacity=50, use=15, speed=140)
        bus2.set_route(self.routes[1])
        self.buses.append(bus2)

        bus3 = Bus(parking=self.parking_lot[0], capacity=50, use=5, speed=120)
        bus3.set_route(self.routes[2])
        self.buses.append(bus3)"""

    def load_stations(self):
        stn1 = Station(location=(40, 404),
                       use=50, capacity=100, stn_type=StationType.STATION)
        stn2 = Station(location=(496, 404),
                       use=40, capacity=100, stn_type=StationType.STATION)
        stn3 = Station(location=(496, 586),
                       use=30, capacity=100, stn_type=StationType.STATION)

        stn4 = Station(location=(268, 131),
                       use=20, capacity=100, stn_type=StationType.STATION)
        stn5 = Station(location=(648, 222),
                       use=10, capacity=100, stn_type=StationType.STATION)
        stn6 = Station(location=(724, 40),
                       use=10, capacity=100, stn_type=StationType.STATION)
        stn7 = Station(location=(800, 586),
                       use=10, capacity=100, stn_type=StationType.STATION)
        stn8 = Station(location=(876, 677),
                       use=10, capacity=100, stn_type=StationType.STATION)

        self.stations.append(stn1)
        self.stations.append(stn2)
        self.stations.append(stn3)
        self.stations.append(stn4)
        self.stations.append(stn5)
        self.stations.append(stn6)
        self.stations.append(stn7)
        self.stations.append(stn8)

