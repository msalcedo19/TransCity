import tkinter as tk
from utils.observer import ObserverLogic
from utils.generator import Generator
from utils.images_controller import ImagesController
from copy import copy
import math as mt
from const import width_screen, height_screen, height_canvas, width_canvas
from entities.path import MoveTypeV2, PathType
from functools import partial


class Application(tk.Frame):
    canvas: tk.Canvas
    panel: tk.Frame

    panel_info_bus: tk.Frame = None

    btn_start: tk.Button
    btn_stop: tk.Button
    btn_resume: tk.Button

    def __init__(self, master: tk.Tk, generator: Generator):
        super().__init__(master)
        self.master = master
        self.generator = generator
        self.images = ImagesController()
        self.pack()
        self.create_widgets()
        self.active = False

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
        self.btn_resume = tk.Button(btn_resume_frame, text="Resume")
        self.btn_resume.pack(expand=True)

        panel_simulation.grid(row=0, sticky="ew")

    def show_info_bus(self, index):
        bus = self.generator.buses[index]
        if self.panel_info_bus:
            self.panel_info_bus.pack_forget()
        self.panel_info_bus = tk.Frame(self, bg='green')

        panel_bus = tk.Frame(self.panel_info_bus)
        bus_title = tk.Label(panel_bus, text="Bus {}".format(index+1), bg="gray36", width=25)
        bus_title.pack(fill='x')
        panel_bus.grid(row=0, columnspan=2)

        passengers_info = tk.Label(self.panel_info_bus, text="# Pasajero:{}".format(bus.get_use()), width=25)
        passengers_info.grid(row=1, columnspan=2)

        self.panel_info_bus.place(x=width_screen-width_canvas, y=(height_canvas/8)-15)

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

        for i in range(0, len(buses)):
            btn = tk.Button(panel_buses, text="Bus {}".format(i+1), command=partial(self.show_info_bus, i))
            btn.grid(row=1, column=i, sticky='ew')

        panel_buses.grid(row=1, sticky="ew")

    def create_widgets(self):
        self.rowconfigure(0, minsize=720, weight=1)
        self.columnconfigure(0, minsize=260, weight=1)
        self.canvas = tk.Canvas(self, width=width_canvas, bg='white')
        self.canvas.grid(row=0, column=1, sticky="ns")

        self.panel = tk.Frame(self, bg="gray")
        self.panel.columnconfigure(0, minsize=260, weight=1)
        self.panel.grid(row=0, column=0, sticky="nsew")

        self.create_buttons_simulation()
        self.create_buttons_buses()

    def mov_circular(self, x1: int, y1: int, path, paths, bus, image_controller, id_image, t):
        if t < 6.3:
            x = 5*mt.cos(t)
            y = 5*mt.sin(t)
            self.canvas.coords(id_image, (x1+x, y1+y))
            self.after(20, self.mov_circular, x1+x, y1+y, path, paths, bus, image_controller, id_image, t+0.1)
        else:
            self.after(20, self.animate_route, x1, y1+1, path, paths, bus, image_controller, id_image)

    def animate_route(self, x, y, path, paths, bus, image_controller, id_image):
        # self.canvas.move(id_image, bus.get_speed(), bus.get_speed()) Se mueve a un dx en x y un dy en y
        if self.active:
            self.canvas.coords(id_image, (x, y))
            (x_final, y_final) = path.get_end_point()
            # print("{} {} {} {}".format(x,y,x_final,y_final))
            if path.path_state(x, y):
                if path.get_type_move() == MoveTypeV2.VERTICAL_ARRIBA:
                    self.after(20, self.animate_route, x, y - bus.get_speed(), path, paths, bus, image_controller,
                               id_image)
                elif path.get_type_move() == MoveTypeV2.VERTICAL_ABAJO:
                    self.after(20, self.animate_route, x, y + bus.get_speed(), path, paths, bus, image_controller,
                               id_image)
                elif path.get_type_move() == MoveTypeV2.HORIZONTAL_IZQUIERDA:
                    self.after(20, self.animate_route, x - bus.get_speed(), y, path, paths, bus, image_controller,
                               id_image)
                elif path.get_type_move() == MoveTypeV2.HORIZONTAL_DERECHA:
                    self.after(20, self.animate_route, x + bus.get_speed(), y, path, paths, bus, image_controller,
                               id_image)
                elif path.get_type_move() == MoveTypeV2.DIAG_IZQ_ARR:
                    (x_inicial, y_inicial) = path.get_start_point()
                    vy = bus.get_speed()
                    vx = (x_final - x_inicial) / ((y_inicial - y_final) / vy)
                    self.after(20, self.animate_route, x - vx, y - vy, path, paths,
                               bus, image_controller, id_image)
                elif path.get_type_move() == MoveTypeV2.DIAG_IZQ_ABJ:
                    (x_inicial, y_inicial) = path.get_start_point()
                    vy = bus.get_speed()
                    vx = (x_inicial - x_final) / ((y_final - y_inicial) / vy)
                    # vx = bus.get_speed()*math.cos(30)
                    self.after(20, self.animate_route, x - vx, y + vy, path, paths,
                               bus, image_controller, id_image)
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ARR:
                    (x_inicial, y_inicial) = path.get_start_point()
                    vy = bus.get_speed()
                    vx = (x_final - x_inicial) / ((y_inicial - y_final) / vy)
                    self.after(20, self.animate_route, x + vx, y - vy, path, paths,
                               bus, image_controller, id_image)
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ABJ:
                    (x_inicial, y_inicial) = path.get_start_point()
                    vy = bus.get_speed()
                    vx = (x_final - x_inicial) / ((y_final - y_inicial) / vy)
                    self.after(20, self.animate_route, x + vx, y + vy, path, paths,
                               bus, image_controller, id_image)
            else:
                if len(paths) > 0:
                    path = paths[0]
                    (path_x1, path_y1) = path.get_start_point()
                    # (path_x2, path_y2) = path.get_end_point()
                    del paths[0]

                    station = path.get_station()
                    if path.get_type_move() == MoveTypeV2.DETENIDO and station:
                        station.set_passengers(station.get_passengers()-bus.get_use())
                        bus.set_use(0)
                        self.canvas.itemconfig(station.get_id(), text=station.get_passengers())
                        self.after(1000, self.animate_route, path_x1, path_y1, path, paths, bus, image_controller, id_image)
                    else:
                        """key = 'train'
                        # Moverse Verticalmente
                        if path_y1 < path_y2:
                            image_rotated = image_controller.rotate(270, key)
                            image_controller.change_image(key, image_rotated)
                        # Moverse Horizontalmente
                        elif path_x1 < path_x2:
                            image_rotated = image_controller.rotate(0, key)
                            image_controller.change_image(key, image_rotated)"""

                        # self.canvas.delete(id_image)
                        # pid = self.canvas.create_image(path_x1, path_y1, image=image_controller.get_images()['train'])
                        self.animate_route(x=path_x1, y=path_y1, path=path, paths=paths, bus=bus,
                                           image_controller=image_controller, id_image=id_image)

    def paint_map(self):
        # images = self.images.get_images()
        paths = self.generator.map_paths
        station_width = 8
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
            self.canvas.create_oval(x - station_width, y - station_width,
                                    x + station_width, y + station_width, fill='#4571EC')
            id_text = self.canvas.create_text(x, y + 10, text=station.get_passengers())
            station.set_id(id_text)
            # self.canvas.create_image(x, y, image=images['station'])
        for parking in self.generator.parking_lot:
            (x, y) = parking.get_location()
            self.canvas.create_oval(x - station_width, y - station_width, x + station_width, y + station_width, fill='#000000')

    def start(self):
        # print("Starting Simulation...")
        if not self.active:
            self.canvas.delete('all')
            self.generator.load_map()
            self.active = True
            self.paint_map()
        for bus in self.generator.buses:
            bus_route = bus.get_route()

            paths = copy(bus_route.get_paths())
            initial_path = paths[0]
            del paths[0]
            (x1, y1) = initial_path.get_start_point()

            pid = self.canvas.create_image(x1, y1, image=self.images.get_images()['train'])
            self.after(1, self.animate_route, x1, y1, initial_path, paths, bus, self.images, pid)

    def pause(self):
        self.active = False


class GUI(ObserverLogic):

    def __init__(self, generator: Generator):
        super().__init__()
        root = tk.Tk(className='TransCity Simulator')
        root.geometry("{}x{}+50+50".format(width_screen, height_screen))
        app = Application(master=root, generator=generator)

        self.tk = app
        self.generator = generator
        app.mainloop()
