from entities.bus import Bus
from entities.route import Route
from entities.path import Path, MapPath, PathType
from entities.station import Station
from entities.parking import Parking
from utils.observer import Observer
from const import width_canvas, height_canvas, padding_canvas


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

    def update(self) -> None:
        print("Generador notificado...")

    def load_map(self):
        if self.__loaded:
            self.buses = []
            self.routes = []
            self.map_paths = []
            self.stations = []
            self.parking_lot = []
        self.load_stations()
        self.load_map_paths()
        self.load_parking_lot()
        self.load_map_paths()
        self.load_routes()
        self.load_buses()
        self.__loaded = True

    def load_parking_lot(self):
        stn1 = Parking(capacity=10, location=(40, 40))
        stn2 = Parking(capacity=5, location=(width_canvas - 40, height_canvas - 40))

        self.parking_lot.append(stn1)
        self.parking_lot.append(stn2)

    def load_map_paths(self):
        # Caminos Horizontales
        path0 = MapPath(start=(40, 40), end=(width_canvas - 40, 40),
                        path_type=PathType.HORIZONTAL)
        path1 = MapPath(start=(40, height_canvas/2),
                        end=(width_canvas - 40, height_canvas/2),
                        path_type=PathType.HORIZONTAL)
        path2 = MapPath(start=(40, height_canvas - 40), end=(width_canvas - 40, height_canvas - 40),
                        path_type=PathType.HORIZONTAL)

        # Caminos Verticales
        path3 = MapPath(start=(40, 40), end=(40, height_canvas - 40), path_type=PathType.VERTICAL)
        path4 = MapPath(start=(width_canvas/2, 40), end=(width_canvas/2, height_canvas - 40),
                        path_type=PathType.VERTICAL)
        path5 = MapPath(start=(width_canvas - 40, 40), end=(width_canvas - 40, height_canvas - 40),
                        path_type=PathType.VERTICAL)

        # Caminos Diagonales
        path6 = MapPath(start=(40, 40), end=(width_canvas - 40, height_canvas - 40), path_type=PathType.DIAGONAL)
        path7 = MapPath(start=(width_canvas - 40, 40), end=(40, height_canvas - 40), path_type=PathType.DIAGONAL)

        self.map_paths.append(path0)
        self.map_paths.append(path1)
        self.map_paths.append(path2)
        self.map_paths.append(path3)

        self.map_paths.append(path4)
        self.map_paths.append(path5)
        self.map_paths.append(path6)
        self.map_paths.append(path7)

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
        path2_route2 = Path(start=(width_canvas / 2, height_canvas / 2),
                            end=(width_canvas / 4, 3*height_canvas/4))
        path3_route2 = Path(start=(width_canvas / 4, 3 * height_canvas / 4),
                            end=(40, height_canvas - 40))

        path0_route3 = Path(start=(40, 40), end=(width_canvas / 4, height_canvas / 4))
        path1_route3 = Path(start=(width_canvas / 4, height_canvas / 4),
                            end=(width_canvas / 2, height_canvas / 2))
        path2_route3 = Path(start=(width_canvas / 2, height_canvas / 2),
                            end=(width_canvas / 2, height_canvas / 2), station=self.stations[1])
        path3_route3 = Path(start=(width_canvas / 2, height_canvas / 2),
                            end=(3 * width_canvas / 4, 3 * height_canvas / 4),)
        path4_route3 = Path(start=(3 * width_canvas / 4, 3 * height_canvas / 4),
                            end=(width_canvas - 40, height_canvas - 40))

        path_retorno1 = Path(start=(width_canvas - 40, height_canvas - 40),
                             end=(40, height_canvas - 40))
        path_retorno2 = Path(start=(40, height_canvas - 40),
                             end=(40, 40), station=self.parking_lot[0])

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

        bus1 = Bus(parking=self.parking_lot[0], capacity=50, use=10, speed=20/10)
        bus1.set_route(self.routes[0])
        self.buses.append(bus1)

        bus2 = Bus(parking=self.parking_lot[0], capacity=50, use=15, speed=35/10)
        bus2.set_route(self.routes[1])
        self.buses.append(bus2)

        bus3 = Bus(parking=self.parking_lot[0], capacity=50, use=5, speed=25/10)
        bus3.set_route(self.routes[2])
        self.buses.append(bus3)

    def load_stations(self):
        stn1 = Station(location=((width_canvas+padding_canvas) / 4, (height_canvas+padding_canvas) / 4), passengers=50)
        stn2 = Station(location=(width_canvas / 2, height_canvas / 2), passengers=40)
        stn3 = Station(location=(((3 * width_canvas)-padding_canvas) / 4, ((3 * height_canvas)-padding_canvas) / 4),
                       passengers=30)

        stn4 = Station(location=(((3*width_canvas)-padding_canvas)/4, (height_canvas+padding_canvas) / 4),
                       passengers=20)
        stn5 = Station(location=((width_canvas+padding_canvas) / 4, ((3*height_canvas)-padding_canvas) / 4),
                       passengers=10)

        self.stations.append(stn1)
        self.stations.append(stn2)
        self.stations.append(stn3)
        self.stations.append(stn4)
        self.stations.append(stn5)

