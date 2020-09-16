from entities.bus import Bus
from entities.route import Route
from entities.path import Path, TypeMove
from entities.station import Station
from entities.parking import Parking
from utils.observer import Observer
from const import width_canvas, height_canvas


class Generator(Observer):
    buses: []
    routes: []
    paths: []
    stations: []
    parking_lot: []
    __loaded: bool

    def __init__(self):
        self.buses = []
        self.routes = []
        self.paths = []
        self.stations = []
        self.parking_lot = []
        self.__loaded = False

    def update(self) -> None:
        print("Generador notificado...")

    def load_map(self):
        if self.__loaded:
            self.buses = []
            self.routes = []
            self.paths = []
            self.stations = []
            self.parking_lot = []
        self.load_stations()
        self.load_paths()
        self.load_parking_lot()
        self.load_buses()
        self.__loaded = True

    def load_parking_lot(self):
        stn1 = Parking(capacity=10, location=(40, 40))
        stn2 = Parking(capacity=5, location=(width_canvas - 40, height_canvas - 40))

        self.parking_lot.append(stn1)
        self.parking_lot.append(stn2)

    def load_paths(self):
        path0 = Path(move=TypeMove.VERTICAL, start=(40, 40), end=(40, height_canvas / 2), reverse=False)
        path1 = Path(move=TypeMove.HORIZONTAL, start=(40, height_canvas / 2),
                     end=(width_canvas / 2, height_canvas / 2), reverse=False)
        path2 = Path(move=TypeMove.HORIZONTAL, start=(width_canvas / 2, height_canvas / 2),
                     end=(width_canvas - 40, height_canvas / 2), reverse=False)
        path3 = Path(move=TypeMove.VERTICAL, start=(width_canvas - 40, height_canvas / 2),
                     end=(width_canvas - 40, height_canvas - 40), reverse=False)

        path4 = Path(move=TypeMove.HORIZONTAL, start=(40, 40), end=(width_canvas / 2, 40), reverse=False)
        path5 = Path(move=TypeMove.VERTICAL, start=(width_canvas / 2, 40),
                     end=(width_canvas / 2, height_canvas / 2), reverse=False)
        path6 = Path(move=TypeMove.VERTICAL, start=(width_canvas / 2, height_canvas / 2),
                     end=(width_canvas / 2, height_canvas - 40), reverse=False)
        path7 = Path(move=TypeMove.HORIZONTAL, start=(width_canvas / 2, height_canvas - 40),
                     end=(width_canvas - 40, height_canvas - 40), reverse=False)

        path8 = Path(move=TypeMove.DIAGONAL, start=(40, 40), end=(width_canvas / 4, height_canvas / 4), reverse=False)
        path9 = Path(move=TypeMove.DIAGONAL, start=(width_canvas / 4, height_canvas / 4),
                     end=(width_canvas / 2, height_canvas / 2), reverse=False)
        path101 = Path(move=TypeMove.DETENIDO, start=(width_canvas / 2, height_canvas / 2),
                       end=(0, 0), reverse=False, station=self.stations[1])
        path10 = Path(move=TypeMove.DIAGONAL, start=(width_canvas / 2, height_canvas / 2),
                      end=(3 * width_canvas / 4, 3 * height_canvas / 4), reverse=False)
        path11 = Path(move=TypeMove.DIAGONAL, start=(3 * width_canvas / 4, 3 * height_canvas / 4),
                      end=(width_canvas - 40, height_canvas - 40), reverse=False)

        path12 = Path(move=TypeMove.HORIZONTAL, start=(width_canvas - 40, height_canvas - 40),
                      end=(40, height_canvas - 40), reverse=True)
        path13 = Path(move=TypeMove.VERTICAL, start=(40, height_canvas - 40),
                      end=(40, 40), reverse=True)

        self.paths.append(path0)
        self.paths.append(path1)
        self.paths.append(path2)
        self.paths.append(path3)

        self.paths.append(path4)
        self.paths.append(path5)
        self.paths.append(path6)
        self.paths.append(path7)

        self.paths.append(path8)
        self.paths.append(path9)
        self.paths.append(path10)
        self.paths.append(path11)

        self.paths.append(path12)
        self.paths.append(path13)

        self.paths.append(path101)

    def load_buses(self):

        route1 = Route()
        route1.add_path(self.paths[0])
        route1.add_path(self.paths[1])
        route1.add_path(self.paths[2])
        route1.add_path(self.paths[3])
        route1.add_path(self.paths[12])
        route1.add_path(self.paths[13])

        route2 = Route()
        route2.add_path(self.paths[4])
        route2.add_path(self.paths[5])
        route2.add_path(self.paths[6])
        route2.add_path(self.paths[7])
        route2.add_path(self.paths[12])
        route2.add_path(self.paths[13])

        route3 = Route()
        route3.add_path(self.paths[8])
        route3.add_path(self.paths[9])
        route3.add_path(self.paths[14])
        route3.add_path(self.paths[10])
        route3.add_path(self.paths[11])
        route3.add_path(self.paths[12])
        route3.add_path(self.paths[13])

        bus1 = Bus(parking=self.parking_lot[0], capacity=50, use=10, speed=20/10)
        bus1.set_route(route1)
        self.buses.append(bus1)

        bus2 = Bus(parking=self.parking_lot[0], capacity=50, use=15, speed=35/10)
        bus2.set_route(route2)
        self.buses.append(bus2)

        bus3 = Bus(parking=self.parking_lot[0], capacity=50, use=5, speed=25/10)
        bus3.set_route(route3)
        self.buses.append(bus3)

    def load_stations(self):
        stn1 = Station(location=(width_canvas / 4, height_canvas / 4), passengers=50)
        stn2 = Station(location=(width_canvas / 2, height_canvas / 2), passengers=40)
        stn3 = Station(location=(3 * width_canvas / 4, 3 * height_canvas / 4), passengers=30)

        stn4 = Station(location=(width_canvas - width_canvas / 4, height_canvas / 4), passengers=20)
        stn5 = Station(location=(width_canvas / 4, height_canvas - height_canvas / 4), passengers=10)

        self.stations.append(stn1)
        self.stations.append(stn2)
        self.stations.append(stn3)
        self.stations.append(stn4)
        self.stations.append(stn5)

