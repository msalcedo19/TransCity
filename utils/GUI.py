import tkinter as tk
from utils.observer import ObserverLogic
from utils.generator import Generator
from utils.images_controller import ImagesController
from copy import copy
import math as mt
from const import width_screen, height_screen, height_canvas, width_canvas
from entities.path import MoveTypeV2, PathType, Path
from entities.station import StationType
from functools import partial


class AnimationObject:

    def __init__(self, x, y, actual_path, paths_left, actual_bus, id_object):
        self.x = x
        self.y = y
        self.actual_path = actual_path
        self.paths_left = paths_left
        self.actual_bus = actual_bus
        self.id_object = id_object

    def set_value(self, **kwargs):
        if kwargs.get('x'):
            self.x = kwargs['x']
        if kwargs.get('y'):
            self.y = kwargs['y']
        if kwargs.get('actual_path'):
            self.actual_path = kwargs['actual_path']
        if kwargs.get('paths_left'):
            self.paths_left = kwargs['paths_left']
        if kwargs.get('actual_bus'):
            self.actual_bus = kwargs['actual_bus']
        if kwargs.get('id_object'):
            self.id_object = kwargs['id_object']


class Application(tk.Frame):
    canvas: tk.Canvas
    panel: tk.Frame

    panel_info_bus: tk.Frame = None
    panel_info_station: tk.Frame = None

    btn_start: tk.Button
    btn_stop: tk.Button
    btn_resume: tk.Button

    def __init__(self, master: tk.Tk, generator: Generator):
        super().__init__(master)
        self.active = False
        self.data_resume = []
        self.master = master
        self.generator = generator
        self.images = ImagesController()
        self.pack()
        self.create_widgets()

    def create_buttons_stations(self):
        stations = self.generator.stations

        panel_stations = tk.Frame(self.panel)
        panel_stations.columnconfigure(0, weight=1)
        panel_stations.columnconfigure(1, weight=1)
        panel_stations.columnconfigure(2, weight=1)

        panel_title_stations = tk.Frame(panel_stations)
        panel_title = tk.Label(panel_title_stations, text="Stations", bg="gray36", width=100)
        panel_title.pack(fill='x')
        panel_title_stations.grid(row=0, columnspan=3)

        cant_btn = 0
        for i in range(0, mt.ceil(len(stations)/3)):
            for j in range(0, 3):
                if cant_btn < len(stations):
                    btn = tk.Button(panel_stations, text="Station {}".format(cant_btn+1),
                                    command=partial(self.show_info_station, cant_btn))
                    btn.grid(row=i+1, column=j, sticky='ew')
                    cant_btn += 1

        panel_stations.grid(row=2, sticky="ew")

    def show_info_station(self, index):
        station = self.generator.stations[index]
        self.canvas.itemconfig(station.id_map, fill='#0CB10B')

        # Falta hacer que se quite el color si se presiono otro boton
        def hide_panel_info_station():
            self.canvas.itemconfig(station.id_map, fill=station.color)
            self.panel_info_station.place_forget()

        if self.panel_info_station:
            self.panel_info_station.place_forget()
        self.panel_info_station = tk.Frame(self)

        panel_station = tk.Frame(self.panel_info_station)
        station_title = tk.Label(panel_station, text="Station {}".format(index+1), bg="gray36", width=25)
        station_title.grid(row=0, column=0)
        btn_close = tk.Button(panel_station, text="x", command=lambda: hide_panel_info_station())
        btn_close.grid(row=0, column=1)
        panel_station.grid(row=0, columnspan=2)

        passengers_info = tk.Label(self.panel_info_station, text="# Passengers:{}".format(station.get_passengers()),
                                   width=25)
        passengers_info.grid(row=1, columnspan=2)

        self.panel_info_station.place(x=width_screen-width_canvas, y=(height_canvas/4)+10)

    def create_buttons_simulation(self):
        panel_simulation = tk.Frame(self.panel)
        panel_simulation.columnconfigure(0, weight=1)
        panel_simulation.columnconfigure(1, weight=1)
        panel_simulation.columnconfigure(2, weight=1)

        panel_title_simulation = tk.Frame(panel_simulation)
        panel_title = tk.Label(panel_title_simulation, text="Simulation", bg="gray36", width=260)
        panel_title.pack(fill='x')
        panel_title_simulation.grid(row=0, columnspan=2)

        self.btn_start = tk.Button(panel_simulation, text="Start", command=self.start)
        self.btn_start.grid(row=1, column=0, sticky='ew')

        self.btn_stop = tk.Button(panel_simulation, text="Stop", command=self.pause)
        self.btn_stop.grid(row=1, column=1, sticky='ew')

        btn_resume_frame = tk.Frame(panel_simulation)
        btn_resume_frame.grid(row=2, columnspan=2)
        self.btn_resume = tk.Button(btn_resume_frame, text="Resume", command=self.resume, width=20)
        self.btn_resume.pack(expand=True)

        panel_simulation.grid(row=0, sticky="ew")

    def create_buttons_buses(self):
        buses = self.generator.buses

        panel_buses = tk.Frame(self.panel)
        panel_buses.columnconfigure(0, weight=1)
        panel_buses.columnconfigure(1, weight=1)
        panel_buses.columnconfigure(2, weight=1)

        panel_title_buses = tk.Frame(panel_buses)
        panel_title = tk.Label(panel_title_buses, text="Buses", bg="gray36", width=100)
        panel_title.pack(fill='x')
        panel_title_buses.grid(row=0, columnspan=3)

        cant_btn = 0
        for i in range(0, mt.ceil(len(buses)/3)):
            for j in range(0, 3):
                if cant_btn < len(buses):
                    btn = tk.Button(panel_buses, text="Bus {}".format(cant_btn+1),
                                    command=partial(self.show_info_bus, cant_btn))
                    btn.grid(row=i+1, column=j, sticky='ew')
                    cant_btn += 1

        panel_buses.grid(row=1, sticky="ew")

    def show_info_bus(self, index):

        bus = self.generator.buses[index]
        self.canvas.itemconfig(bus.get_id(), fill='#0CB10B')

        # Falta hacer que se quite el color si se presiono otro boton
        def hide_panel_info_bus():
            self.canvas.itemconfig(bus.get_id(), fill=bus.color)
            self.panel_info_bus.place_forget()

        if self.panel_info_bus:
            self.panel_info_bus.place_forget()
        self.panel_info_bus = tk.Frame(self)

        panel_bus = tk.Frame(self.panel_info_bus)
        panel_bus.columnconfigure(0, minsize=50)
        bus_title = tk.Label(panel_bus, text="Bus {}".format(index + 1), bg="gray36", width=25)
        bus_title.grid(row=0, column=0)
        btn_close = tk.Button(panel_bus, text="x", command=lambda: hide_panel_info_bus())
        btn_close.grid(row=0, column=1)
        panel_bus.grid(row=0, columnspan=2)

        speed_info = tk.Label(self.panel_info_bus, text="Speed: {}".format(bus.get_speed()), width=25)
        speed_info.grid(row=1, columnspan=2)
        capacity_info = tk.Label(self.panel_info_bus, text="Capacity: {}".format(bus.get_capacity()), width=25)
        capacity_info.grid(row=2, columnspan=2)
        passengers_info = tk.Label(self.panel_info_bus, text="# Passengers:{}".format(bus.get_use()), width=25)
        passengers_info.grid(row=3, columnspan=2)

        self.panel_info_bus.place(x=width_screen - width_canvas, y=(height_canvas / 6) - 22)

    def create_widgets(self):
        self.rowconfigure(0, minsize=720, weight=1)
        self.columnconfigure(0, minsize=260, weight=1)
        self.canvas = tk.Canvas(self, width=width_canvas, bg='white')
        self.canvas.grid(row=0, column=1, sticky="ns")

        self.panel = tk.Frame(self, bg="gray")
        self.panel.columnconfigure(0, minsize=260, weight=1)
        self.panel.rowconfigure(1, pad=50)
        self.panel.grid(row=0, column=0, sticky="nsew")

        self.create_buttons_simulation()
        self.create_buttons_buses()
        self.create_buttons_stations()

    def animate_route(self, animation_object: AnimationObject, fun=None):
        """print(self.canvas.coords(animation_object.id_object))
        def up():
            print(animation_object.id_object)
            self.canvas.move(animation_object.id_object, 0, -1)
        fun()
        self.after(50, self.animate_route, animation_object, fun)"""
        def get_alpha(x_init: int, y_init: int, x_fin: int, y_fin: int):
            alpha_fun = 0
            # Movimiento Diagonal
            if y_init > y_fin:
                c = mt.sqrt(mt.pow(x_fin - x_init, 2) + mt.pow(y_init - y_fin, 2))
                alpha_fun = (mt.asin((y_init - y_fin) / c))
            elif y_init < y_fin:
                c = mt.sqrt(mt.pow(x_fin - x_init, 2) + mt.pow(y_init - y_fin, 2))
                alpha_fun = (mt.asin((y_fin - y_init) / c))
            return alpha_fun

        if self.active:
            # Atributos necesarios para realizar la animación
            id_image = animation_object.id_object
            x = animation_object.x
            y = animation_object.y
            path = animation_object.actual_path
            bus = animation_object.actual_bus

            # self.canvas.coords(id_image, (x, y))
            # self.canvas.coords(id_image, (x - 5, y - 5, x + 5, y + 5))
            if fun is not None:
                fun(id_image)
            # print("{} {} {} {}".format(x,y,x_final,y_final))
            # Se verifica si ya esta en el punto de destino del camino, entra al if si aún no ha llegado
            if path.path_state(x, y):
                (x_final, y_final) = path.get_end_point()
                if path.get_type_move() == MoveTypeV2.VERTICAL_ARRIBA:
                    animation_object.set_value(x=x, y=y - 1)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, 0, -1))
                elif path.get_type_move() == MoveTypeV2.VERTICAL_ABAJO:
                    animation_object.set_value(x=x, y=y + 1)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, 0, 1))
                elif path.get_type_move() == MoveTypeV2.HORIZONTAL_IZQUIERDA:
                    animation_object.set_value(x=x - 1, y=y)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, -1, 0))
                elif path.get_type_move() == MoveTypeV2.HORIZONTAL_DERECHA:
                    animation_object.set_value(x=x + 1, y=y)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, 1, 0))
                elif path.get_type_move() == MoveTypeV2.DIAG_IZQ_ARR:
                    (x_inicial, y_inicial) = path.get_start_point()
                    alpha = get_alpha(x_inicial, y_inicial, x_final, y_final)
                    vy = mt.sin(alpha) * 0.7071068
                    vx = mt.cos(alpha) * 0.7071068
                    animation_object.set_value(x=x - vx, y=y - vy)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, -vx, -vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_IZQ_ABJ:
                    (x_inicial, y_inicial) = path.get_start_point()
                    alpha = get_alpha(x_inicial, y_inicial, x_final, y_final)
                    vy = mt.sin(alpha) * 0.7071068
                    vx = mt.cos(alpha) * 0.7071068
                    animation_object.set_value(x=x - vx, y=y + vy)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, -vx, vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ARR:
                    (x_inicial, y_inicial) = path.get_start_point()
                    alpha = get_alpha(x_inicial, y_inicial, x_final, y_final)
                    vy = mt.sin(alpha) * 0.7071068
                    vx = mt.cos(alpha) * 0.7071068
                    animation_object.set_value(x=x + vx, y=y - vy)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, vx, -vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ABJ:
                    (x_inicial, y_inicial) = path.get_start_point()
                    alpha = get_alpha(x_inicial, y_inicial, x_final, y_final)
                    vy = mt.sin(alpha) * 0.7071068
                    vx = mt.cos(alpha) * 0.7071068
                    animation_object.set_value(x=x + vx, y=y + vy)
                    self.after(int(1000/bus.get_speed()), self.animate_route, animation_object,
                               lambda pid: self.canvas.move(pid, vx, vy))
            else:
                station = path.get_station()
                if station and station.get_type() == StationType.STATION:
                    station.set_use(station.get_use() - bus.get_use())
                    bus.set_use(station.get_use() + bus.get_use())
                    self.canvas.itemconfig(station.id_text_object, text=station.get_use())
                elif station and station.get_type() == StationType.PARKING:
                    station = path.get_station()
                    station.increase_use()
                    self.canvas.itemconfig(station.id_text_object,
                                           text=str(station.get_use()) + "/" + str(station.get_capacity()))
                    self.canvas.delete(id_image)

                paths = animation_object.paths_left
                # Si la cantidad de caminos es mayor a cero significa que la ruta aún no ha terminado
                if len(paths) > 0:
                    path = paths[0]
                    (path_x1, path_y1) = path.get_start_point()
                    # (path_x2, path_y2) = path.get_end_point()
                    del paths[0]
                    animation_object.set_value(x=path_x1, y=path_y1, actual_path=path, paths_left=paths, actual_bus=bus)
                    if station and station.get_type() == StationType.STATION:
                        self.after(1000, self.animate_route, animation_object,
                                   lambda pid: self.canvas.coords(pid, path_x1 - 5,
                                                                  path_y1 - 5, path_x1 + 5, path_y1 + 5))
                    else:
                        self.animate_route(animation_object,
                                           lambda pid: self.canvas.coords(pid, path_x1 - 5,
                                                                          path_y1 - 5, path_x1 + 5, path_y1 + 5))
        else:
            self.data_resume.append(animation_object)

    def paint_map(self):
        # images = self.images.get_images()
        paths = self.generator.map_paths
        station_width = 5
        for path in paths:
            (x_init, y_init) = path.get_start_point()
            (x_end, y_end) = path.get_end_point()
            type_path = path.get_path_type()

            if type_path == PathType.HORIZONTAL:
                self.canvas.create_line(x_init, y_init, x_end, y_end)
            elif type_path == PathType.VERTICAL:
                self.canvas.create_line(x_init, y_init, x_end, y_end)
            elif type_path == PathType.DIAGONAL:
                self.canvas.create_line(x_init, y_init, x_end, y_end)
        for station in self.generator.stations:
            (x, y) = station.get_location()
            id_map = self.canvas.create_oval(x - station_width, y - station_width,
                                             x + station_width, y + station_width, fill='#4571EC')
            id_text = self.canvas.create_text(x, y + 15, text=station.get_use())
            station.id_text_object = id_text
            station.id_object = id_map
            # self.canvas.create_image(x, y, image=images['station'])
        for parking in self.generator.parking_lot:
            (x, y) = parking.get_location()
            self.canvas.create_oval(x - station_width, y - station_width,
                                    x + station_width, y + station_width, fill='#000000')
            id_text = self.canvas.create_text(x-16, y + 10, text=str(parking.get_use())+"/"+str(parking.get_capacity()))
            parking.id_text_object = id_text

    def start(self):
        # print("Starting Simulation...")
        if not self.active:
            self.canvas.delete('all')
            self.data_resume = []
            self.generator.load_map()
            self.active = True
            self.paint_map()
            self.btn_start.configure(state='disabled')

        for bus in self.generator.buses:
            bus_route = bus.get_route()

            paths = copy(bus_route.get_paths())
            initial_path = paths[0]
            del paths[0]
            (x1, y1) = initial_path.get_start_point()

            # pid = self.canvas.create_image(x1, y1, image=self.images.get_images()['train'])
            pid = self.canvas.create_oval(x1 - 5, y1 - 5, x1 + 5, y1 + 5, fill=bus.color)
            bus.set_id(pid)
            animation_object = AnimationObject(x1, y1, initial_path, paths, bus, pid)
            self.after(1000, self.animate_route, animation_object)

    def pause(self):
        self.btn_start.configure(state='active')
        self.data_resume = []
        self.active = False

    def resume(self):
        self.btn_start.configure(state='disabled')
        self.active = True
        for obj in self.data_resume:
            self.animate_route(obj)


class GUI(ObserverLogic):

    def __init__(self, generator: Generator):
        super().__init__()
        root = tk.Tk(className='TransCity Simulator')
        root.geometry("{}x{}+50+50".format(width_screen, height_screen))
        app = Application(master=root, generator=generator)

        self.tk = app
        self.generator = generator
        # self.attach(generator)
        app.mainloop()
