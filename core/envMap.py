import tkinter as tk
from entities.station import Station


def paint_map(self):
    def create_path(*coordenates):
        self.canvas.create_line(*coordenates, width=15, fill="white", joinstyle=tk.ROUND,
                                capstyle=tk.ROUND)
        self.canvas.create_line(*coordenates, width=1, fill="black", joinstyle=tk.ROUND,
                                dash=(3, 1))

    paths = self.generator.map_paths
    for path in paths:
        (x0, y0) = path[0]
        (x1, y1) = path[1]
        create_path(x0, y0, x1, y1)
        if (x0, y0 - 10) not in self.coords:
            self.coords.append((x0, y0 - 10))
        if (x1, y1 - 10) not in self.coords:
            self.coords.append((x1, y1 - 10))

    def create_station(x: int, y: int, station: Station, color: str):
        station_width = 8
        pid = self.canvas.create_oval(x - station_width, y - station_width,
                                      x + station_width, y + station_width, fill=color)
        id_text = self.canvas.create_text(x, y, text=station.get_use(), fill='white')

        station.id_text_object = id_text
        station.id_object = pid

    stations = self.generator.stations
    for stn in stations:
        (x0, y0) = stn.get_location()
        create_station(x0, y0, stn, stn.color)

    stations = self.generator.parking_lot
    for stn in stations:
        (x0, y0) = stn.get_location()
        create_station(x0, y0, stn, "black")
