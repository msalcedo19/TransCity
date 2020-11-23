import tkinter as tk
from utils.generator import Generator
from copy import copy
from core.animationObj import AnimationObject
from core.envButtons import *
from core.envMap import paint_map
from core.transitions import animate_route
from const import *
from utils.observer import Observer
import threading
import tkinter.font as tk_font
from utils.RL import Action, States
from entities.station import Station
from entities.bus import Bus
from entities.route import Route
from utils.RL import RL
import random


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

    def __init__(self, master: tk.Tk, generator: Generator, rl: RL = None):
        super().__init__(master)
        self.coords = []
        self.coordsId = []
        self.active = False
        self.isPause = False
        self.system = False
        self.data_resume = {'stations': [], 'resume': []}
        self.generator: Generator = generator

        self.master = master
        self.pack()
        self.create_widgets()
        self.t = None

        self.rl = rl

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
        create_buttons_options(self)

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
        create_buttons_options(self)

    def send_bus(self, bus: Bus):
        bus.activate()
        bus.get_parking().decrease_user()
        self.canvas.itemconfig(bus.get_parking().id_text_object, text=str(bus.get_parking().get_use()))
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

    def close_station(self, p_station: Station):
        if p_station.is_close():
            p_station.open()
            self.canvas.itemconfig(p_station.id_object, fill=p_station.color)
            self.generator.log(action=Action.OPEN_STATION)
        else:
            p_station.close()
            self.canvas.itemconfig(p_station.id_object, fill='red')
            self.generator.log(action=Action.CLOSE_STATION)

    def close_bus(self, blocking_bus: Bus):
        if blocking_bus.is_block():
            blocking_bus.unblock()
            self.generator.log(action=Action.OPEN_BUS)
        else:
            blocking_bus.block()
            self.generator.log(action=Action.CLOSE_BUS)

    def generate_pass(self):
        self.t = threading.Thread(target=self.generator.generate_passengers, args=(self, 250,))
        self.t.daemon = True
        self.t.start()

    def start(self):

        if not self.active and not self.isPause:
            self.data_resume = {'stations': [], 'resume': []}
            self.active = True
            self.refresh_canvas()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.generate_pass()
        elif not self.active and self.isPause:
            self.active = True
            self.generate_pass()
            self.refresh_canvas()
            self.btn_start.configure(state='disabled')
            self.btn_stop.configure(state='active')
            self.btn_resume.configure(state='disabled')

        for bus in self.generator.buses:
            if bus.get_code() < 3:
                self.send_bus(bus)

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
        self.generate_pass()
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

    def show_notification(self, message: str, state: States = None, **kwargs):
        self.pause()

        if not self.system:
            show_notification_window = tk.Toplevel(self)
            show_notification_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux - 50))

            def close_notification():
                try:
                    show_notification_window.withdraw()
                except tk.TclError:
                    pass
            threading.Timer(2, close_notification).start()

            show_notification_window.columnconfigure(0, minsize=width_panel / 2, weight=1)
            show_notification_window.columnconfigure(1, minsize=width_panel / 2, weight=1)

            font_titles = tk_font.Font(family=family1, size=14, weight="bold")
            font_info = tk_font.Font(family=family1, size=12)

            noti_title = tk.Label(show_notification_window, text="Information", font=font_titles, bg=color5)
            noti_title.grid(row=0, columnspan=2, sticky=tk.EW)

            noti_info = tk.Label(show_notification_window, text=message, font=font_info)
            noti_info.grid(row=1, columnspan=2, sticky=tk.EW)
            if state:
                self.generator.log(state=state)

        else:
            def send_bus_to_station(p_station: Station):

                def stn_in_route(route: Route) -> bool:
                    for path in route.get_paths():
                        if path.get_station() and path.get_station() == p_station:
                            return True
                    return False

                bus_available = list(filter(lambda b: not b.is_active() and stn_in_route(b.get_route()),
                                            self.generator.buses))
                if bus_available:
                    p_bus = bus_available[0]
                    print(p_bus.get_code())
                    new_route = copy(p_bus.get_route())
                    for path_in in new_route.get_paths():
                        if path_in.get_station() and path_in.get_station() == p_station:
                            break
                        else:
                            path_in.set_station(stn=None)
                    print(new_route)
                    p_bus.set_route(new_route)
                    self.send_bus(bus=p_bus)

            def close_stn_random():
                stations_random = list(filter(lambda b: not b.is_close(), self.generator.stations))
                stn_selected = stations_random[random.randint(0, len(stations_random)-1)]
                self.close_station(p_station=stn_selected)

            def close_bus_random():
                buses_random = list(filter(lambda b: not b.is_block(), self.generator.buses))
                bus_selected = buses_random[random.randint(0, len(buses_random)-1)]
                self.close_bus(blocking_bus=bus_selected)

            knod = self.rl.train
            if knod.get(state.value):
                if state == States.FULL_STATION:
                    for action in knod[state.value]:
                        if action == Action.SEND_BUS.value:
                            print("send bus estado:{}".format(state.value))
                            send_bus_to_station(p_station=kwargs.get('station'))
                        elif action == Action.CLOSE_STATION.value:
                            print("close station estado:{}".format(state.value))
                            self.close_station(p_station=kwargs.get('station'))
                        elif action == Action.CLOSE_BUS.value:
                            print("close bus estado:{}".format(state.value))
                            if not kwargs.get('bus'):
                                close_bus_random()
                elif state == States.FULL_BUS:
                    for action in knod[state.value]:
                        if action == Action.SEND_BUS.value:
                            print("send bus estado:{}".format(state.value))
                            send_bus_to_station(p_station=kwargs.get('station'))
                        elif action == Action.CLOSE_BUS.value:
                            print("close bus estado:{}".format(state.value))
                            self.close_bus(blocking_bus=kwargs.get('bus'))
                        elif action == Action.CLOSE_STATION.value:
                            print("close station estado:{}".format(state.value))
                            if not kwargs.get('station'):
                                close_stn_random()
                elif state == States.RELEASE_STATION:
                    for action in knod[state.value]:
                        if action == Action.OPEN_STATION.value:
                            print("open station estado:{}".format(state.value))
                            self.close_station(p_station=kwargs.get('station'))
                        elif action == Action.CLOSE_STATION.value:
                            print("close station estado:{}".format(state.value))
                            if kwargs.get('station'):
                                close_stn_random()
                        elif action == Action.CLOSE_BUS.value:
                            print("close bus estado:{}".format(state.value))
                            if not kwargs.get('bus'):
                                close_bus_random()
                elif state == States.RELEASE_BUS:
                    for action in knod[state.value]:
                        if action == Action.OPEN_BUS.value:
                            print("open bus estado:{}".format(state.value))
                            self.close_bus(blocking_bus=kwargs.get('bus'))
                        elif action == Action.CLOSE_STATION.value:
                            print("close station estado:{}".format(state.value))
                            if not kwargs.get('station'):
                                close_stn_random()
                        elif action == Action.CLOSE_BUS.value:
                            print("close bus estado:{}".format(state.value))
                            if kwargs.get('bus'):
                                close_bus_random()
        # self.resume()


class GUI(Observer):

    def __init__(self, generator: Generator):
        super().__init__()
        root = tk.Tk(className='TransCity Simulator')
        root.geometry("{}x{}+50+50".format(width_screen, height_screen))

        def on_closing():
            self.generator.detach(self)
            root.destroy()

        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.resizable(False, False)

        rl = RL()
        app = Application(master=root, generator=generator, rl=rl)

        self.tk = app
        self.generator = generator
        self.generator.attach(self)
        app.mainloop()

    def update(self, station) -> None:
        if station.get_capacity() == station.get_use():
            self.tk.show_notification(message='Station: {}\n FULL'.format(station.get_code()),
                                      state=States.FULL_STATION, station=station)
            station.btn_id.configure(bg='red')

            """def stn_in_route(route: Route) -> bool:
                for path in route.get_paths():
                    if path.get_station() and path.get_station() == station:
                        return True
                return False
            bus_available = list(filter(lambda b: not b.is_active() and stn_in_route(b.get_route()),
                                        self.tk.generator.buses))
            if bus_available:
                p_bus = bus_available[0]
                new_route = p_bus.get_route()
                for path_in in new_route.get_paths():
                    if path_in.get_station() and path_in.get_station() == station:
                        break
                    else:
                        path_in.set_station(stn=None)
                p_bus.set_route(new_route)
                # self.tk.send_bus(bus=p_bus)
                # self.tk.generator.log(action=Action.SEND_BUS)"""
        self.tk.canvas.itemconfig(station.id_text_object, text=str(station.get_use()))


