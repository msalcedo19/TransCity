import tkinter as tk
from utils.observer import ObserverLogic
from utils.generator import Generator
from utils.images_controller import ImagesController
from copy import copy
import math as mt
from const import width_screen, height_screen, height_canvas, width_canvas
from entities.path import MoveTypeV2, PathType, Path
from entities.bus import Bus
from entities.station import StationType, Station
from functools import partial
from entities.route import Route


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
    panel_info_route: tk.Frame = None

    btn_start: tk.Button
    btn_stop: tk.Button
    btn_resume: tk.Button

    coords: []
    coordsId: []

    def __init__(self, master: tk.Tk, generator: Generator):
        super().__init__(master)
        self.coords = []
        self.coordsId = []
        self.active = False
        self.isPause = False
        self.data_resume = {'stations': [], 'resume': []}
        self.master = master
        self.generator = generator
        self.images = ImagesController()
        self.pack()
        self.create_widgets()

    def rebuild(self):
        self.panel.destroy()
        self.panel = tk.Frame(self, bg="gray")
        self.panel.columnconfigure(0, minsize=260, weight=1)
        self.panel.rowconfigure(1, pad=50)
        self.panel.rowconfigure(3, pad=50)
        self.panel.grid(row=0, column=0, sticky="nsew")

        self.create_buttons_simulation()
        self.create_buttons_buses()
        self.create_buttons_stations()
        self.create_buttons_routes()

    def create_buttons_simulation(self):
        panel_simulation = tk.Frame(self.panel)
        panel_simulation.columnconfigure(0, weight=1)
        panel_simulation.columnconfigure(1, weight=1)

        panel_title_simulation = tk.Frame(panel_simulation)
        panel_title = tk.Label(panel_title_simulation, text="Simulation", bg="gray36")
        panel_title.pack(fill='x')
        panel_title_simulation.grid(sticky=tk.EW, columnspan=2)

        btn_row1 = tk.Frame(panel_simulation)
        btn_row1.columnconfigure(0, weight=1)
        btn_row1.columnconfigure(1, weight=1)

        self.btn_start = tk.Button(btn_row1, text="Start", command=self.start)
        self.btn_start.grid(row=0, column=0, sticky='ew')
        self.btn_stop = tk.Button(btn_row1, text="Stop", command=self.pause)
        self.btn_stop.grid(row=0, column=1, sticky='ew')
        self.btn_stop.configure(state='disabled')

        btn_row2 = tk.Frame(panel_simulation)
        btn_row2.columnconfigure(0, weight=1)
        btn_row2.columnconfigure(1, weight=1)

        def show_coords():
            if self.coordsId:
                for pid in self.coordsId:
                    self.canvas.delete(pid)
                self.coordsId = []
            else:
                for coord in self.coords:
                    (x_end, y_end) = coord
                    pid = self.canvas.create_text(x_end, y_end, text=str((x_end, y_end+10)))
                    self.coordsId.append(pid)

        self.btn_resume = tk.Button(btn_row2, text="Resume", command=self.resume)
        self.btn_resume.grid(row=0, column=0, sticky='ew')
        self.btn_resume.configure(state='disabled')
        btn_coord = tk.Button(btn_row2, text="Coord", command=lambda: show_coords())
        btn_coord.grid(row=0, column=1, sticky='ew')

        btn_row1.grid(row=1, sticky="ew", columnspan=2)
        btn_row2.grid(row=2, sticky="ew", columnspan=2)
        panel_simulation.grid(row=0, sticky="ew")

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
        fin_i = 0
        fin_j = 0
        for i in range(1, mt.ceil(len(stations)/3)+1):
            fin_i += 1
            for j in range(0, 3):
                fin_j = j
                if cant_btn < len(stations):
                    btn = tk.Button(panel_stations, text="Station {}".format(cant_btn+1),
                                    command=partial(self.show_info_station, cant_btn))
                    btn.grid(row=i, column=j, sticky='ew')
                    cant_btn += 1

        if fin_j == 2:
            fin_j = 0
            fin_i += 1
        btn = tk.Button(panel_stations, text="Add stn", command=lambda: create_station())
        btn.grid(row=fin_i, column=fin_j, sticky='ew')

        panel_stations.grid(row=2, sticky="ew")

        def create_station():
            width_screen_route = 300
            height_screen_route = 180
            create_station_window = tk.Toplevel(self)
            create_station_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

            tk.Label(create_station_window,
                     text="""Coordenates""",
                     justify=tk.LEFT,
                     padx=20).pack()

            x_input = tk.Entry(create_station_window, width=5)
            x_input.pack(expand="yes")
            y_input = tk.Entry(create_station_window, width=5)
            y_input.pack(expand="yes")

            def complete():
                stn = Station(location=(int(x_input.get()), int(y_input.get())),
                              use=50, capacity=100, stn_type=StationType.STATION)
                self.generator.stations.append(stn)

                create_station_window.destroy()
                panel_stations.grid_forget()
                self.create_buttons_stations()

            complete_btn = tk.Button(create_station_window, text="Complete", command=partial(complete))
            complete_btn.pack(expand="yes")

    def show_info_station(self, index):
        station = self.generator.stations[index]
        self.canvas.itemconfig(station.id_object, fill='#0CB10B')

        # Falta hacer que se quite el color si se presiono otro boton
        # self.canvas.itemconfig(station.id_object, fill=station.color)

        def on_closing():
            self.canvas.itemconfig(station.id_object, fill=station.color)
            panel_station_window.destroy()

        width_screen_route = 300
        height_screen_route = 180
        panel_station_window = tk.Toplevel(self)
        panel_station_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))
        panel_station_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_station = tk.Frame(panel_station_window)
        station_title = tk.Label(panel_station, text="Station {}".format(index+1), bg="gray36", width=25)
        station_title.pack(fill=tk.X)
        panel_station.pack(fill=tk.X)

        passengers_info = tk.Label(panel_station_window, text="# Passengers:{}".format(station.get_use()), width=25)
        passengers_info.pack()

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
        fin_i = 0
        fin_j = 0
        for i in range(1, mt.ceil(len(buses)/3)+1):
            fin_i += 1
            for j in range(0, 3):
                fin_j = j
                if cant_btn < len(buses):
                    btn = tk.Button(panel_buses, text="Bus {}".format(cant_btn+1),
                                    command=partial(self.show_info_bus, cant_btn))
                    btn.grid(row=i, column=j, sticky='ew')
                    cant_btn += 1
        if fin_j == 2:
            fin_j = 0
            fin_i += 1
        btn = tk.Button(panel_buses, text="Add bus", command=lambda: create_bus())
        btn.grid(row=fin_i, column=fin_j, sticky='ew')

        panel_buses.grid(row=1, sticky="ew")

        def create_bus():
            width_screen_route = 300
            height_screen_route = 180
            create_bus_window = tk.Toplevel(self)
            create_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

            v = tk.IntVar()
            v.set(0)

            routes = self.generator.routes

            def show_choice():
                print(v.get())

            tk.Label(create_bus_window,
                     text="""Choose the route""",
                     justify=tk.LEFT,
                     padx=20).pack()

            for index_route in range(0, len(routes)):
                tk.Radiobutton(create_bus_window,
                               text="Route {}".format(index_route+1),
                               padx=20,
                               variable=v,
                               command=show_choice,
                               value=index_route).pack(anchor=tk.W)
            speed_input = tk.Entry(create_bus_window, width=5)
            speed_input.pack(expand="yes")

            def complete():
                bus = Bus(parking=self.generator.parking_lot[0], capacity=50, use=15, speed=int(speed_input.get()))
                bus.set_route(routes[v.get()])
                self.generator.buses.append(bus)
                panel_buses.grid_forget()
                create_bus_window.destroy()
                panel_buses.grid_forget()
                self.create_buttons_buses()

            complete_btn = tk.Button(create_bus_window, text="Complete", command=partial(complete))
            complete_btn.pack(expand="yes")

    def show_info_bus(self, index):

        bus = self.generator.buses[index]
        self.canvas.itemconfig(bus.get_id(), fill='#0CB10B')

        def on_closing():
            self.canvas.itemconfig(bus.get_id(), fill=bus.color)
            panel_bus_window.destroy()

        width_screen_route = 300
        height_screen_route = 180
        panel_bus_window = tk.Toplevel(self)
        panel_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))
        panel_bus_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_bus = tk.Frame(panel_bus_window)
        panel_bus.columnconfigure(0, minsize=50)
        bus_title = tk.Label(panel_bus, text="Bus {}".format(index + 1), bg="gray36", width=25)
        bus_title.pack(fill=tk.X)

        speed_info = tk.Label(panel_bus, text="Speed: {}".format(bus.get_speed()), width=25)
        speed_info.pack()
        capacity_info = tk.Label(panel_bus, text="Capacity: {}".format(bus.get_capacity()), width=25)
        capacity_info.pack()
        passengers_info = tk.Label(panel_bus, text="# Passengers:{}".format(bus.get_use()), width=25)
        passengers_info.pack()

        panel_bus.pack(fill=tk.X)

    def create_buttons_routes(self):
        routes = self.generator.routes

        panel_routes = tk.Frame(self.panel)
        panel_routes.columnconfigure(0, weight=1)
        panel_routes.columnconfigure(1, weight=1)
        panel_routes.columnconfigure(2, weight=1)

        panel_title_routes = tk.Frame(panel_routes)
        panel_title = tk.Label(panel_title_routes, text="Routes", bg="gray36", width=100)
        panel_title.pack(fill='x')
        panel_title_routes.grid(row=0, columnspan=3)

        cant_btn = 0
        fin_i = 0
        fin_j = 0
        for i in range(1, mt.ceil(len(routes)/3)+1):
            fin_i += 1
            for j in range(0, 3):
                fin_j = j
                if cant_btn < len(routes):
                    btn = tk.Button(panel_routes, text="Route {}".format(cant_btn+1),
                                    command=partial(self.show_info_route, cant_btn))
                    btn.grid(row=i, column=j, sticky='ew')
                    cant_btn += 1
        if fin_j == 2:
            fin_j = 0
            fin_i += 1
        btn = tk.Button(panel_routes, text="Add route", command=lambda: create_route())
        btn.grid(row=fin_i, column=fin_j, sticky='ew')

        panel_routes.grid(row=3, sticky="ew")

        def create_route():
            width_screen_route = 300
            height_screen_route = 180
            create_route_window = tk.Toplevel(self)
            create_route_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

            frame1 = tk.Frame(create_route_window)
            frame2 = tk.Frame(create_route_window)
            create_route_window.columnconfigure(0, minsize=width_screen_route/2, weight=1)
            create_route_window.columnconfigure(1, minsize=width_screen_route/2, weight=1)

            x_input = tk.Entry(frame1, width=5)
            x_input.pack(expand="yes")
            y_input = tk.Entry(frame1, width=5)
            y_input.pack(expand="yes")

            scrollbar = tk.Scrollbar(frame2)
            scrollbar.pack(side='right', fill='y')
            listbox = tk.Listbox(frame2, yscrollcommand=scrollbar.set)
            listbox.pack(side='left', fill='both')

            scrollbar.config(command=listbox.yview)

            def add_point(value1: tk.Entry, value2: tk.Entry):
                val1 = int(value1.get())
                val2 = int(value2.get())
                listbox.insert(tk.END, str((val1, val2)))
                value1.delete(first=0, last=5)
                value2.delete(first=0, last=5)

            def complete():
                route = Route()
                start_point = None
                for index in range(0, listbox.size()):
                    arr = listbox.get(first=index).replace(')', "")
                    arr = arr.replace('(', "")
                    arr = arr.replace(' ', "")
                    arr = arr.split(',')
                    if not start_point:
                        start_point = (int(arr[0]), int(arr[1]))
                    else:
                        new_path = Path(start=start_point, end=(int(arr[0]), int(arr[1])))
                        route.add_path(new_path)
                        start_point = (int(arr[0]), int(arr[1]))
                self.generator.routes.append(route)
                panel_routes.grid_forget()
                self.create_buttons_routes()
                create_route_window.destroy()

            add_btn = tk.Button(frame1, text="add", command=partial(add_point, x_input, y_input))
            add_btn.pack(expand="yes")
            complete_btn = tk.Button(frame1, text="Complete", command=partial(complete))
            complete_btn.pack(expand="yes")

            frame1.grid(row=0, column=0)
            frame2.grid(row=0, column=1)

    def show_info_route(self, index):
        routes: Route = self.generator.routes[index]

        lines_ids = []
        for path in routes.get_paths():
            (x_init, y_init) = path.get_start_point()
            (x_final, y_final) = path.get_end_point()
            pid = self.canvas.create_line(x_init, y_init, x_final, y_final, fill="green", width=3)
            lines_ids.append(pid)

        def on_closing():
            for pid2 in lines_ids:
                self.canvas.delete(pid2)
            panel_route_window.destroy()

        width_screen_route = 300
        height_screen_route = 180
        panel_route_window = tk.Toplevel(self)
        panel_route_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))
        panel_route_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_route = tk.Frame(panel_route_window)
        route_title = tk.Label(panel_route, text="Route {}".format(index+1), bg="gray36")
        route_title.pack(fill=tk.X)
        panel_route.pack()

    def create_widgets(self):
        self.rowconfigure(0, minsize=720, weight=1)
        self.columnconfigure(0, minsize=260, weight=1)
        self.canvas = tk.Canvas(self, width=width_canvas, bg='white')
        self.canvas.grid(row=0, column=1, sticky="ns")

        self.panel = tk.Frame(self, bg="gray")
        self.panel.columnconfigure(0, minsize=260, weight=1)
        self.panel.rowconfigure(1, pad=50)
        self.panel.rowconfigure(3, pad=50)
        self.panel.grid(row=0, column=0, sticky="nsew")

        self.create_buttons_simulation()
        self.create_buttons_buses()
        self.create_buttons_stations()
        self.create_buttons_routes()

    def paint_map(self):
        # images = self.images.get_images()
        paths = self.generator.map_paths
        station_width = 5

        for path in paths:
            (x_init, y_init) = path.get_start_point()
            (x_end, y_end) = path.get_end_point()
            type_path = path.get_path_type()

            if (x_init, y_init - 10) not in self.coords:
                # self.canvas.create_text(x_init, y_init - 10, text=str((x_init, y_init)))
                self.coords.append((x_init, y_init - 10))

            if type_path == PathType.HORIZONTAL:
                self.canvas.create_line(x_init, y_init, x_end, y_end, width=2)
            elif type_path == PathType.VERTICAL:
                if (x_end, y_end - 10) not in self.coords:
                    # self.canvas.create_text(x_end, y_end - 10, text=str((x_end, y_end)))
                    self.coords.append((x_end, y_end - 10))
                self.canvas.create_line(x_init, y_init, x_end, y_end, width=2)
            elif type_path == PathType.DIAGONAL:
                self.canvas.create_line(x_init, y_init, x_end, y_end, width=2)

        stations = None
        if len(self.data_resume['stations']) == 0:
            stations = self.generator.stations
        else:
            stations = self.data_resume['stations']
            self.data_resume = {'stations': [], 'resume': []}
        for station in stations:
            (x, y) = station.get_location()
            id_map = self.canvas.create_oval(x - station_width, y - station_width,
                                             x + station_width, y + station_width, fill='#4571EC')
            id_text = self.canvas.create_text(x, y + 15, text=station.get_use())
            station.id_text_object = id_text
            station.id_object = id_map
            self.data_resume['stations'].append(copy(station))
            # self.canvas.create_image(x, y, image=images['station'])
        for parking in self.generator.parking_lot:
            (x, y) = parking.get_location()
            self.canvas.create_oval(x - station_width, y - station_width,
                                    x + station_width, y + station_width, fill='#000000')
            id_text = self.canvas.create_text(x-16, y + 10, text=str(parking.get_use())+"/"+str(parking.get_capacity()))
            parking.id_text_object = id_text

    def start(self):
        # print("Starting Simulation...")
        if not self.active and not self.isPause:
            self.canvas.delete('all')
            self.data_resume = {'stations': [], 'resume': []}
            self.generator.load_map()
            self.active = True
            self.paint_map()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
        elif not self.active and self.isPause:
            self.canvas.delete('all')
            self.active = True
            self.paint_map()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.btn_resume.configure(state='disabled')

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
        self.btn_resume.configure(state='active')
        self.btn_stop.configure(state='disabled')
        self.active = False
        self.isPause = True

    def resume(self):
        self.btn_start.configure(state='disabled')
        self.btn_resume.configure(state='disabled')
        self.btn_stop.configure(state='active')
        self.active = True
        for obj in self.data_resume['resume']:
            self.animate_route(obj)
        self.data_resume = {'stations': [], 'resume': []}

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
            self.data_resume['resume'].append(animation_object)


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
