from entities.bus import Bus
from entities.route import Route
from entities.path import Path, MapPath, PathType
from entities.station import Station, StationType
from entities.user import User
from const import *
import random
import time
from utils.observer import ObserverLogic
import csv
import json


class Generator(ObserverLogic):
    buses: []
    routes: []
    map_paths: []
    stations: []
    parking_lot: []
    users: []
    paths: []
    __loaded: bool

    def __init__(self):
        self.buses = []
        self.routes = []
        self.map_paths = []
        self.stations = []
        self.parking_lot = []
        self.users = []
        self.paths = []
        self.__loaded = False
        self.start_x_map = padding_left_canvas
        self.end_x_map = width_canvas - padding_right_canvas
        self.start_y_map = padding_top_canvas
        self.end_y_map = height_canvas - padding_bottom_canvas

    def save(self):
        data = {}
        data['buses'] = []
        for bus in self.buses:
            data['buses'].append(bus.encode())
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)

    def log(self):
        with open('./data/stations.csv', mode='a') as csv_file:
            fieldnames = ['code', 'location', 'capacity', 'use', 'type', 'isClose']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for stn in self.stations:
                stn: Station = stn
                writer.writerow({'location': stn.get_location(), 'capacity': stn.get_capacity(), 'use': stn.get_use(),
                                'type': stn.get_type(), 'isClose': stn.is_close(), 'code': stn.get_code()})

        with open('./data/buses.csv', mode='a') as csv_file:
            fieldnames = ['code', 'speed', 'parking', 'capacity', 'use', 'route']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for bus in self.buses:
                bus: Bus = bus
                writer.writerow({'code': bus.get_code(), 'speed': bus.get_speed(),
                                 'parking': bus.get_parking().get_code(), 'capacity': bus.get_capacity(),
                                 'use': bus.get_use(), 'route': bus.get_route().get_code()})

        with open('./data/users.csv', mode='a') as csv_file:
            fieldnames = ['code', 'route', 'source', 'destination', 'start_date_trip', 'end_date_trip']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for user in self.users:
                user: User = user
                writer.writerow({'code': user.get_code(), 'source': user.get_src().get_code(),
                                 'destination': user.get_dest().get_code(), 'route': user.get_route().get_code(),
                                 'start_date_trip': user.get_start_trip(), 'end_date_trip': user.get_end_trip()})

        with open('./data/routes.csv', mode='a') as csv_file:
            fieldnames = ['code', 'isBlock', '#paths', 'paths']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for route in self.routes:
                route: Route = route
                paths = ''
                for path in route.get_paths():
                    paths += str(path.get_code())+'-'
                writer.writerow({'code': route.get_code(), 'isBlock': route.is_block(),
                                 '#paths': len(route.get_paths()), 'paths': paths})

        with open('./data/paths.csv', mode='a') as csv_file:
            fieldnames = ['code', 'start', 'end', 'isBlock', 'station', 'typeMove']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, lineterminator='\n')

            writer.writeheader()
            for path in self.paths:
                path: Path = path
                stn = path.get_station()
                stn_code = None
                if stn:
                    stn_code = stn.get_code()
                writer.writerow({'code': path.get_code(), 'start': path.get_start_point(),
                                 'end': path.get_end_point(), 'isBlock': path.is_block(),
                                 'station': stn_code})

    def load_map(self):
        if self.__loaded:
            self.map_paths = []
            self.stations = []
            self.routes = []
            self.buses = []
            self.parking_lot = []
            self.users = []
            self.paths = []
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
                          [(116, 222), (116, 404)], [(116, 404), (116, 677)], [(268, 40), (268, 131)],
                          [(268, 40), (496, 40)], [(268, 222), (496, 222)], [(116, 404), (496, 404)],
                          [(116, 677), (420, 586)], [(420, 586), (496, 586)], [(496, 222), (496, 404)],
                          [(496, 40), (724, 40)], [(724, 40), (952, 40)], [(496, 222), (648, 222)],
                          [(648, 222), (800, 222)], [(496, 404), (800, 404)], [(572, 586), (800, 677)],
                          [(800, 131), (952, 131)], [(800, 404), (952, 404)], [(800, 677), (876, 677)],
                          [(876, 677), (952, 677)], [(800, 222), (800, 131)], [(800, 222), (800, 404)],
                          [(800, 404), (800, 586)], [(800, 586), (800, 677)], [(952, 40), (952, 131)],
                          [(952, 131), (952, 404)], [(952, 404), (952, 677)], [(496, 40), (496, 222)],
                          [(268, 131), (268, 222)], [(496, 586), (572, 586)], [(496, 404), (496, 586)]]

    def load_routes(self):
        path0_route1 = Path(start=(40, 40), end=(40, 404), station=self.stations[0], code=1)
        path1_route1 = Path(start=(40, 404), end=(40, 677), code=2)
        path1_1_route1 = Path(start=(40, 677), end=(116, 677), code=3)
        path2_route1 = Path(start=(116, 677), end=(420, 586), code=4)
        path3_route1 = Path(start=(420, 586), end=(572, 586), code=5)
        path4_route1 = Path(start=(572, 586), end=(800, 677), code=6)
        path5_route1 = Path(start=(800, 677), end=(800, 404), code=7)
        path6_route1 = Path(start=(800, 404), end=(496, 404), station=self.stations[1], code=8)
        path7_route1 = Path(start=(496, 404), end=(496, 222), code=9)
        path8_route1 = Path(start=(496, 222), end=(800, 222), code=10)
        path9_route1 = Path(start=(800, 222), end=(800, 131), code=11)
        path10_route1 = Path(start=(800, 131), end=(952, 131), code=12)
        path11_route1 = Path(start=(952, 131), end=(952, 404), station=self.parking_lot[1], code=13)

        route1 = Route(code=1)
        route1.add_path(path0_route1)
        route1.add_path(path1_route1)
        route1.add_path(path1_1_route1)
        route1.add_path(path2_route1)
        route1.add_path(path3_route1)
        route1.add_path(path4_route1)
        route1.add_path(path5_route1)
        route1.add_path(path6_route1)
        route1.add_path(path7_route1)
        route1.add_path(path8_route1)
        route1.add_path(path9_route1)
        route1.add_path(path10_route1)
        route1.add_path(path11_route1)

        path0_route2 = Path(start=(952, 40), end=(496, 40), code=14)
        path1_route2 = Path(start=(496, 40), end=(496, 404), station=self.stations[1], code=15)
        path2_route2 = Path(start=(496, 404), end=(800, 404), code=16)
        path3_route2 = Path(start=(800, 404), end=(800, 677), code=17)
        path4_route2 = Path(start=(800, 677), end=(876, 677), station=self.stations[7], code=18)
        path5_route2 = Path(start=(876, 677), end=(952, 677), code=19)
        path6_route2 = Path(start=(952, 677), end=(952, 404), station=self.parking_lot[1], code=20)

        route2 = Route(code=2)
        route2.add_path(path0_route2)
        route2.add_path(path1_route2)
        route2.add_path(path2_route2)
        route2.add_path(path3_route2)
        route2.add_path(path4_route2)
        route2.add_path(path5_route2)
        route2.add_path(path6_route2)

        self.routes.append(route1)
        self.routes.append(route2)

        self.paths.append(path0_route1)
        self.paths.append(path1_route1)
        self.paths.append(path2_route1)
        self.paths.append(path4_route1)
        self.paths.append(path5_route1)
        self.paths.append(path6_route1)
        self.paths.append(path7_route1)
        self.paths.append(path8_route1)
        self.paths.append(path9_route1)
        self.paths.append(path10_route1)
        self.paths.append(path11_route1)
        self.paths.append(path0_route2)
        self.paths.append(path1_route2)
        self.paths.append(path2_route2)
        self.paths.append(path3_route2)
        self.paths.append(path4_route2)
        self.paths.append(path5_route2)
        self.paths.append(path6_route2)

    def load_buses(self):

        bus1 = Bus(parking=self.parking_lot[0], capacity=50, use=0, speed=120, color='#C72402', code=1,
                   route=self.routes[0])
        self.buses.append(bus1)

        bus2 = Bus(parking=self.parking_lot[0], capacity=50, use=0, speed=140, color='green', code=2,
                   route=self.routes[1])
        self.buses.append(bus2)

        """bus3 = Bus(parking=self.parking_lot[0], capacity=50, use=5, speed=120)
        bus3.set_route(self.routes[2])
        self.buses.append(bus3)"""

    def load_stations(self):
        stn1 = Station(location=(40, 404),
                       use=0, capacity=100, stn_type=StationType.STATION, code=1)
        stn2 = Station(location=(496, 404),
                       use=0, capacity=100, stn_type=StationType.STATION, code=2)
        stn3 = Station(location=(496, 586),
                       use=0, capacity=100, stn_type=StationType.STATION, code=3)

        stn4 = Station(location=(268, 131),
                       use=0, capacity=100, stn_type=StationType.STATION, code=4)
        stn5 = Station(location=(648, 222),
                       use=0, capacity=100, stn_type=StationType.STATION, code=5)
        stn6 = Station(location=(724, 40),
                       use=0, capacity=100, stn_type=StationType.STATION, code=6)
        stn7 = Station(location=(800, 586),
                       use=0, capacity=100, stn_type=StationType.STATION, code=7)
        stn8 = Station(location=(876, 677),
                       use=0, capacity=100, stn_type=StationType.STATION, code=8)

        self.stations.append(stn1)
        self.stations.append(stn2)
        self.stations.append(stn3)
        self.stations.append(stn4)
        self.stations.append(stn5)
        self.stations.append(stn6)
        self.stations.append(stn7)
        self.stations.append(stn8)

    def generate_passengers(self):

        for i in range(0, 16):
            src = None
            dest = None
            num_random = random.randint(0, len(self.routes)-1)
            route = self.routes[num_random]
            station_src: Station = None
            for path in route.get_paths():
                station = path.get_station()
                if station and station.get_type() == StationType.STATION:
                    if src:
                        dest = station
                    elif not dest:
                        src = station
                        station_src = path.get_station()

            user = User(src=src, dest=dest, route=route, code=i+1)
            user.start_trip()
            self.users.append(user)
            station_src.new_user(user)
            self.notify(station_src)
            time.sleep(0.6)



