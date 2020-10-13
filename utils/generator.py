from entities.bus import Bus
from entities.route import Route
from entities.path import Path, MapPath, PathType
from entities.station import Station, StationType
from const import *


class Generator:
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
        stn1 = Station(capacity=10, location=(40, 40), use=0, stn_type=StationType.PARKING, code=1)
        stn2 = Station(capacity=5, location=(952, 404), use=0, stn_type=StationType.PARKING, code=2)

        self.parking_lot.append(stn1)
        self.parking_lot.append(stn2)

    def load_map_paths(self):
        # Caminos Horizontales
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
        path0_route1 = Path(start=(40, 40), end=(40, 404), station=self.stations[0])
        path1_route1 = Path(start=(40, 404), end=(40, 677))
        path7_route1 = Path(start=(40, 677), end=(116, 677))
        path2_route1 = Path(start=(116, 677), end=(420, 586))
        path3_route1 = Path(start=(420, 586), end=(572, 586))
        path4_route1 = Path(start=(572, 586), end=(800, 677))
        path5_route1 = Path(start=(800, 677), end=(800, 404))
        path6_route1 = Path(start=(800, 404), end=(496, 404))

        route1 = Route()
        route1.add_path(path0_route1)
        route1.add_path(path1_route1)
        route1.add_path(path7_route1)
        route1.add_path(path2_route1)
        route1.add_path(path3_route1)
        route1.add_path(path4_route1)
        route1.add_path(path5_route1)
        route1.add_path(path6_route1)

        path0_route2 = Path(start=(952, 40), end=(496, 40))
        path1_route2 = Path(start=(496, 40), end=(496, 404), station=self.stations[1])
        path2_route2 = Path(start=(496, 404), end=(800, 404))
        path3_route2 = Path(start=(800, 404), end=(800, 677))
        path4_route2 = Path(start=(800, 677), end=(876, 677), station=self.stations[7])
        path5_route2 = Path(start=(876, 677), end=(952, 677))
        path6_route2 = Path(start=(952, 677), end=(952, 404), station=self.parking_lot[1])

        route1 = Route()
        route1.add_path(path0_route1)
        route1.add_path(path1_route1)
        route1.add_path(path7_route1)
        route1.add_path(path2_route1)
        route1.add_path(path3_route1)
        route1.add_path(path4_route1)
        route1.add_path(path5_route1)
        route1.add_path(path6_route1)

        route2 = Route()
        route2.add_path(path0_route2)
        route2.add_path(path1_route2)
        route2.add_path(path2_route2)
        route2.add_path(path3_route2)
        route2.add_path(path4_route2)
        route2.add_path(path5_route2)
        route2.add_path(path6_route2)

        self.routes.append(route1)
        self.routes.append(route2)

    def load_buses(self):

        bus1 = Bus(parking=self.parking_lot[0], capacity=50, use=10, speed=120, color='#C72402', code=1)
        bus1.set_route(self.routes[0])
        self.buses.append(bus1)

        bus2 = Bus(parking=self.parking_lot[0], capacity=50, use=15, speed=140, color='green', code=2)
        bus2.set_route(self.routes[1])
        self.buses.append(bus2)

        """bus3 = Bus(parking=self.parking_lot[0], capacity=50, use=5, speed=120)
        bus3.set_route(self.routes[2])
        self.buses.append(bus3)"""

    def load_stations(self):
        stn1 = Station(location=(40, 404),
                       use=50, capacity=100, stn_type=StationType.STATION, code=1)
        stn2 = Station(location=(496, 404),
                       use=40, capacity=100, stn_type=StationType.STATION, code=2)
        stn3 = Station(location=(496, 586),
                       use=30, capacity=100, stn_type=StationType.STATION, code=3)

        stn4 = Station(location=(268, 131),
                       use=20, capacity=100, stn_type=StationType.STATION, code=4)
        stn5 = Station(location=(648, 222),
                       use=10, capacity=100, stn_type=StationType.STATION, code=5)
        stn6 = Station(location=(724, 40),
                       use=10, capacity=100, stn_type=StationType.STATION, code=6)
        stn7 = Station(location=(800, 586),
                       use=10, capacity=100, stn_type=StationType.STATION, code=7)
        stn8 = Station(location=(876, 677),
                       use=10, capacity=100, stn_type=StationType.STATION, code=8)

        self.stations.append(stn1)
        self.stations.append(stn2)
        self.stations.append(stn3)
        self.stations.append(stn4)
        self.stations.append(stn5)
        self.stations.append(stn6)
        self.stations.append(stn7)
        self.stations.append(stn8)

