import tkinter as tk
from utils.generator import Generator
from copy import copy
from core.animationObj import AnimationObject
from core.envButtons import create_buttons_routes, create_buttons_stations, create_buttons_buses, \
    create_buttons_simulation
from core.envMap import paint_map
from core.transitions import animate_route
from const import *
from utils.observer import Observer
import threading


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
        self.generator: Generator = generator

        self.master = master
        self.pack()
        self.create_widgets()
        self.t = None
        paint_map(self)
    def refresh(self):
        self.canvas.delete('all')
        paint_map(self)

    def create_widgets(self):
        self.rowconfigure(0, minsize=720, weight=1)
        self.canvas = tk.Canvas(self, width=width_canvas, bg='#1C8F37')
        self.canvas.grid(row=0, column=1, sticky="ns")

        self.panel = tk.Frame(self)
        self.panel.columnconfigure(0, minsize=260, weight=1)
        self.panel.grid(row=0, column=0, sticky="nsew")

        create_buttons_simulation(self)
        create_buttons_buses(self)
        create_buttons_stations(self)
        create_buttons_routes(self)

    def start(self):

        if not self.active and not self.isPause:
            self.data_resume = {'stations': [], 'resume': []}
            self.active = True
            self.refresh()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.t = threading.Thread(target=self.generator.generate_passengers)
            self.t.daemon = True
            self.t.start()
        elif not self.active and self.isPause:
            self.active = True
            self.refresh()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.btn_resume.configure(state='disabled')

        for bus in self.generator.buses:
            bus_route = bus.get_route()

            paths = copy(bus_route.get_paths())
            initial_path = paths[0]
            del paths[0]
            (x1, y1) = initial_path.get_start_point()

            bus_height = 9
            bus_width = 5
            pid = self.canvas.create_polygon(x1, y1, x1 + bus_width, y1, x1 + bus_width,
                                             y1 + bus_height, x1, y1 + bus_height, x1, y1,  fill=bus.get_color())
            bus.set_id(pid)
            animation_object = AnimationObject(x1, y1, initial_path, paths, bus, pid)
            self.after(1000, animate_route, self, animation_object)

    def pause(self):
        if self.active:
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
            animate_route(self, obj)
        self.data_resume = {'stations': [], 'resume': []}

    def log(self):
        self.generator.load()
        create_buttons_buses(self)
        create_buttons_stations(self)
        create_buttons_routes(self)
        paint_map(self)

    def save(self):
        self.generator.save()


class GUI(Observer):

    def __init__(self, generator: Generator):
        super().__init__()
        root = tk.Tk(className='TransCity Simulator')
        root.geometry("{}x{}+50+50".format(width_screen, height_screen))

        def on_closing():
            self.generator.detach(self)
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        app = Application(master=root, generator=generator)

        self.tk = app
        self.generator = generator
        self.generator.attach(self)
        app.mainloop()

    def update(self, station) -> None:
        self.tk.canvas.itemconfig(station.id_text_object, text=str(station.get_use()))


