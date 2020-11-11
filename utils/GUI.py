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
import tkinter.font as tk_font
from core.envButtons import Action


class Application(tk.Frame):
    canvas: tk.Canvas
    panel: tk.Frame

    panel_info_bus: tk.Frame = None
    panel_info_station: tk.Frame = None
    panel_info_route: tk.Frame = None

    btn_start: tk.Button
    btn_stop: tk.Button
    btn_resume: tk.Button
    btn_save: tk.Button
    btn_load: tk.Button
    btn_coord: tk.Button

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

    def refresh_canvas(self):
        self.canvas.delete('all')
        self.coords = []
        self.coordsId = []
        paint_map(self)

    def refresh_panel(self):
        self.panel.destroy()
        self.panel = tk.Frame(self)
        self.panel.columnconfigure(0, minsize=260, weight=1)
        self.panel.grid(row=0, column=0, sticky="nsew")

        create_buttons_simulation(self)
        create_buttons_buses(self)
        create_buttons_stations(self)
        create_buttons_routes(self)

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
            self.refresh_canvas()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.t = threading.Thread(target=self.generator.generate_passengers)
            self.t.daemon = True
            self.t.start()
        elif not self.active and self.isPause:
            self.active = True
            self.refresh_canvas()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.btn_resume.configure(state='disabled')

        for bus in self.generator.buses:
            if bus.get_code() != 2:
                self.launch_bus(bus)

    def launch_bus(self, bus):
        bus.activate()
        bus_route = bus.get_route()

        paths = copy(bus_route.get_paths())
        initial_path = paths[0]
        del paths[0]
        (x1, y1) = initial_path.get_start_point()

        bus_height = 9
        bus_width = 5
        pid = self.canvas.create_polygon(x1, y1, x1 + bus_width, y1, x1 + bus_width,
                                         y1 + bus_height, x1, y1 + bus_height, x1, y1, fill=bus.get_color())
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

    def load(self):
        self.generator.clean()
        self.generator.load()

        self.refresh_panel()
        self.refresh_canvas()

        self.btn_start.configure(state='active')
        self.btn_save.configure(state='active')
        self.btn_coord.configure(state='active')

    def save(self):
        self.generator.save()

    def show_notification(self, message: str):
        self.pause()
        show_notification_window = tk.Toplevel(self)
        show_notification_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux))
        threading.Timer(2, show_notification_window.withdraw).start()

        show_notification_window.columnconfigure(0, minsize=width_panel / 2, weight=1)
        show_notification_window.columnconfigure(1, minsize=width_panel / 2, weight=1)

        font_titles = tk_font.Font(family=family1, size=12, weight="bold")
        font_info = tk_font.Font(family=family1, size=10)

        noti_title = tk.Label(show_notification_window, text="Information", font=font_titles, bg=color5)
        noti_title.grid(row=0, columnspan=2, sticky=tk.EW)

        noti_info = tk.Label(show_notification_window, text=message, font=font_info)
        noti_info.grid(row=1, columnspan=2, sticky=tk.EW)


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
        if station.get_capacity() == station.get_use():
            self.tk.show_notification(message='Station: {}\n FULL'.format(station.get_code()))
            station.btn_id.configure(bg='red')
            bus_available = list(filter(lambda b: not b.is_active(), self.tk.generator.buses))
            bus_available[1].set_route(bus_available[1].get_route())
            self.tk.launch_bus(bus=bus_available[1])
            self.tk.generator.log(Action.SEND_BUS)
        self.tk.canvas.itemconfig(station.id_text_object, text=str(station.get_use()))


