import tkinter as tk
from entities.station import *
from entities.bus import *
from entities.path import Path
from functools import partial
import math as mt
import tkinter.font as tk_font
from const import *
import random


def create_buttons_options(self):
    font_titles = tk_font.Font(family=family1, size=14, weight="bold")

    panel_options = tk.Frame(self.panel)
    panel_options.columnconfigure(0, minsize=width_panel / 2, weight=1)
    panel_options.columnconfigure(1, minsize=width_panel / 2, weight=1)

    panel_title = tk.Label(panel_options, text="Settings", font=font_titles, bg=color5)
    panel_title.grid(row=0, columnspan=2, sticky=tk.EW)

    btn_col1 = tk.Frame(panel_options)
    btn_col2 = tk.Frame(panel_options)

    self.btn_load = tk.Button(btn_col1, text="Load", command=self.load)
    self.btn_load.pack(fill=tk.X)

    self.btn_save = tk.Button(btn_col2, text="Save", command=self.save)
    self.btn_save.pack(fill=tk.X)
    self.btn_save.configure(state='disabled')

    def enabled():
        if not self.system:
            self.system = True
            self.rl.processing('./data/log_v1.txt')
            self.rl.training()
            self.btn_system.configure(text="Disabled System", bg='green')
        else:
            self.system = False
            self.btn_system.configure(text="Enabled System", bg='SystemButtonFace')

    str_sys = 'Enabled System'
    if self.system:
        str_sys = 'Disabled System'
    self.btn_system = tk.Button(panel_options, text=str_sys, command=enabled)
    self.btn_system.grid(row=2, column=0, columnspan=2, sticky=tk.NS)

    btn_col1.grid(row=1, column=0, sticky=tk.NSEW)
    btn_col2.grid(row=1, column=1, sticky=tk.NSEW)

    panel_options.grid(row=5, sticky=tk.EW, pady=15)


def create_buttons_simulation(self):
    font_titles = tk_font.Font(family=family1, size=14, weight="bold")

    panel_simulation = tk.Frame(self.panel, bg=color1)
    panel_simulation.columnconfigure(0, minsize=width_panel/2, weight=1)
    panel_simulation.columnconfigure(1, minsize=width_panel/2, weight=1)
    panel_title = tk.Label(panel_simulation, text="Simulation", font=font_titles, bg=color5)
    panel_title.grid(row=0, columnspan=2, sticky=tk.EW)

    btn_col1 = tk.Frame(panel_simulation)
    btn_col2 = tk.Frame(panel_simulation)

    self.btn_start = tk.Button(btn_col1, text="Start", command=self.start)
    self.btn_start.pack(fill=tk.X)
    self.btn_start.configure(state='disabled')

    self.btn_resume = tk.Button(btn_col1, text="Resume", command=self.resume)
    self.btn_resume.pack(fill=tk.X)
    self.btn_resume.configure(state='disabled')

    def show_coords():
        if self.coordsId:
            for pid in self.coordsId:
                self.canvas.delete(pid)
            self.coordsId = []
        else:
            for coord in self.coords:
                (x_end, y_end) = coord
                pid = self.canvas.create_text(x_end, y_end, text=str((x_end, y_end + up)))
                self.coordsId.append(pid)

    self.btn_stop = tk.Button(btn_col2, text="Stop", command=self.pause)
    self.btn_stop.pack(fill=tk.X)
    self.btn_stop.configure(state='disabled')

    self.btn_coord = tk.Button(btn_col2, text="Coord", command=lambda: show_coords())
    self.btn_coord.pack(fill=tk.X)
    self.btn_coord.configure(state='disabled')

    btn_col1.grid(row=1, column=0, sticky=tk.NSEW)
    btn_col2.grid(row=1, column=1, sticky=tk.NSEW)
    panel_simulation.grid(row=0, sticky=tk.EW)


def create_buttons_stations(self):

    font_titles = tk_font.Font(family=family1, size=14, weight="bold")
    font_info = tk_font.Font(family=family1, size=12)

    def show_info_station(station: Station):

        self.pause()
        self.canvas.itemconfig(station.id_object, fill='yellow')

        def on_closing():
            if not station.is_close():
                self.canvas.itemconfig(station.id_object, fill=station.color)
            else:
                self.canvas.itemconfig(station.id_object, fill='red')
            panel_station_window.destroy()

        panel_station_window = tk.Toplevel(self)
        panel_station_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux - 60))
        panel_station_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_station_window.columnconfigure(0, minsize=width_panel/2, weight=1)
        panel_station_window.columnconfigure(1, minsize=width_panel/2, weight=1)

        if station.get_type() == StationType.STATION:
            station_title = tk.Label(panel_station_window, text="Station {}".format(station.get_code()),
                                     font=font_titles, bg=color5)
            station_title.grid(row=0, columnspan=2, sticky=tk.EW)

            info_frame = tk.Frame(panel_station_window)

            passengers_info = tk.Label(info_frame, text="# Passengers:{}".format(station.get_use()), width=25,
                                       font=font_info)
            passengers_info.grid(row=0)
            capacity_info = tk.Label(info_frame, text="Max Capacity:{}".format(station.get_capacity()), width=25,
                                     font=font_info)
            capacity_info.grid(row=1)

            info_frame.grid(row=1, columnspan=2)

            txt = 'Close'
            if station.is_close():
                txt = 'Open'
            close_btn = tk.Button(panel_station_window, text=txt, width=13)
            station.btn_close = close_btn
            close_btn.configure(command=partial(self.close_station, station))
            close_btn.grid(row=2, columnspan=2)
        else:
            station_title = tk.Label(panel_station_window, text="Bus Spot {}".format(station.get_code()),
                                     font=font_titles, bg=color5)
            station_title.grid(row=0, columnspan=2, sticky=tk.EW)

            info_frame = tk.Frame(panel_station_window)

            passengers_info = tk.Label(info_frame, text="# Buses:{}".format(station.get_use()), width=25,
                                       font=font_info)
            passengers_info.grid(row=0)
            capacity_info = tk.Label(info_frame, text="Max Capacity:{}".format(station.get_capacity()), width=25,
                                     font=font_info)
            capacity_info.grid(row=1)

            info_frame.grid(row=1, columnspan=2)

    def create_station(type_stn: StationType):

        self.pause()

        create_station_window = tk.Toplevel(self)
        create_station_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux))

        create_station_window.columnconfigure(0, minsize=width_screen_aux / 2, weight=1)
        create_station_window.columnconfigure(1, minsize=width_screen_aux / 2, weight=1)

        tk.Label(create_station_window,
                 text="""Coordenates""",
                 justify=tk.LEFT,
                 padx=20).grid(row=0, columnspan=2)

        input_frame = tk.Frame(create_station_window)

        x_input_text = tk.Label(input_frame, text='X', font=font_info)
        x_input_text.grid(row=1, column=0)
        x_input = tk.Entry(input_frame, width=5)
        x_input.grid(row=1, column=1, sticky=tk.NSEW)

        y_input_text = tk.Label(input_frame, text='Y', font=font_info)
        y_input_text.grid(row=2, column=0)
        y_input = tk.Entry(input_frame, width=5, font=font_info)
        y_input.grid(row=2, column=1, sticky=tk.NSEW)

        if type_stn == StationType.STATION:
            use_input_text = tk.Label(input_frame, text='# Passengers', font=font_info)
        else:
            use_input_text = tk.Label(input_frame, text='# Buses', font=font_info)
        use_input_text.grid(row=3, column=0)
        use_input = tk.Entry(input_frame, width=5)
        use_input.grid(row=3, column=1, sticky=tk.NSEW)

        capacity_input_text = tk.Label(input_frame, text='Max Capacity')
        capacity_input_text.grid(row=4, column=0)
        capacity_input = tk.Entry(input_frame, width=5)
        capacity_input.grid(row=4, column=1, sticky=tk.NSEW)

        input_frame.grid(row=1, columnspan=2, pady=10)

        def complete():
            if x_input.get() and y_input.get() and use_input.get() and capacity_input.get():
                stn = Station(location=(int(x_input.get()), int(y_input.get())), use=int(use_input.get()),
                              capacity=int(capacity_input.get()), stn_type=type_stn,
                              code=len(self.generator.stations)+1)
                if type_stn == StationType.PARKING:
                    stn.color = 'black'
                self.generator.stations.append(stn)

                panel_stations.grid_forget()
                create_buttons_stations(self)
                self.refresh_canvas()
                self.show_notification(message='Station created')
            create_station_window.destroy()

        options_input_frame = tk.Frame(create_station_window)

        cancel_btn = tk.Button(options_input_frame, text="Cancel", command=lambda: create_station_window.destroy())
        cancel_btn.grid(row=2, column=0)
        complete_btn = tk.Button(options_input_frame, text="Complete", command=lambda: complete())
        complete_btn.grid(row=2, column=1)

        options_input_frame.grid(row=2, columnspan=2)

    panel_stations = tk.Frame(self.panel)
    panel_stations.columnconfigure(0, minsize=86, weight=1)
    panel_stations.columnconfigure(1, minsize=88, weight=1)
    panel_stations.columnconfigure(2, minsize=86, weight=1)

    panel_title = tk.Label(panel_stations, text="Stations", font=font_titles, bg=color5)
    panel_title.grid(row=0, columnspan=3, sticky=tk.EW)

    cant_btn = 0
    fin_i = 1
    stations = list(filter(lambda stn: stn.get_type().value == 'S', self.generator.stations))
    stations.sort(key=lambda stn_sort: stn_sort.get_code())
    if len(stations) != 0:
        for i in range(1, mt.ceil(len(stations) / 3) + 1):
            fin_i += 1
            for j in range(0, 3):
                if cant_btn < len(stations):
                    btn = tk.Button(panel_stations, text="Station {}".format(stations[cant_btn].get_code()),
                                    command=partial(show_info_station, stations[cant_btn]))
                    btn.grid(row=i, column=j, sticky='ew')
                    stations[cant_btn].btn_id = btn
                    cant_btn += 1
    else:
        msg_aux = tk.Label(panel_stations, text="There're not stations",
                           font=tk_font.Font(family=family1, size=8))
        msg_aux.grid(row=1, column=1, sticky=tk.EW)
        fin_i += 1

    # Panel de las estaciones de bus
    panel_parkings = tk.Frame(self.panel)
    panel_parkings.columnconfigure(0, minsize=86, weight=1)
    panel_parkings.columnconfigure(1, minsize=88, weight=1)
    panel_parkings.columnconfigure(2, minsize=86, weight=1)

    fin_i2 = fin_i + 1
    cant_btn2 = 0
    panel_title_bus_spot = tk.Label(panel_parkings, text="Bus Spot", font=font_titles, bg=color5)
    panel_title_bus_spot.grid(row=fin_i2, columnspan=3, sticky=tk.EW)

    parkings = list(filter(lambda stn: stn.get_type().value == 'P', self.generator.stations))
    parkings.sort(key=lambda stn_sort: stn_sort.get_code())

    if len(parkings) != 0:
        for i in range(fin_i2 + 1, mt.ceil(len(parkings) / 3) + 1 + fin_i2 + 1):
            fin_i2 += 1
            for j in range(0, 3):
                if cant_btn2 < len(parkings):
                    btn = tk.Button(panel_parkings, text="Station {}".format(parkings[cant_btn2].get_code()),
                                    command=partial(show_info_station, parkings[cant_btn2]))
                    btn.grid(row=i, column=j, sticky='ew')
                    parkings[cant_btn2].btn_id = btn
                    cant_btn2 += 1
    else:
        msg_aux_spot = tk.Label(panel_parkings, text="There're not bus spot", font=tk_font.Font(family=family1, size=8))
        fin_i2 += 1
        msg_aux_spot.grid(row=fin_i2, column=1, sticky=tk.EW)
        fin_i2 += 1

    btn = tk.Button(panel_parkings, text="Add", command=lambda: create_station(type_stn=StationType.PARKING))
    btn.grid(row=fin_i2, column=1, sticky='ew')

    btn = tk.Button(panel_stations, text="Add", command=lambda: create_station(type_stn=StationType.STATION))
    btn.grid(row=fin_i, column=1, sticky='ew')

    panel_stations.grid(row=2, sticky=tk.EW)
    panel_parkings.grid(row=3, sticky=tk.EW, pady=15)


def create_buttons_buses(self):

    font_titles = tk_font.Font(family=family1, size=14, weight="bold")
    font_info = tk_font.Font(family=family1, size=10)

    def show_info_bus(p_bus: Bus):

        self.pause()

        def change_route():
            routes = self.generator.routes

            panel_bus_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux + len(routes)*40 + 25))
            change_route_frame = tk.Frame(panel_bus_window)
            v = tk.IntVar()
            v.set(0)

            tk.Label(change_route_frame,
                     text="""Choose the route""",
                     justify=tk.LEFT,
                     padx=20).pack()

            for index_route in range(0, len(routes)):
                tk.Radiobutton(change_route_frame,
                               text="Route {}".format(index_route + 1),
                               padx=20,
                               variable=v,
                               value=index_route).pack(anchor=tk.W)

            def cancel_change_route():
                change_route_frame.destroy()
                panel_bus_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux+40))

            def change():
                bus.set_route(routes[v.get()])
                route_info.configure(text="Route:{}".format(bus.get_route().get_code()))
                cancel_change_route()

            change_route_options_frame = tk.Frame(change_route_frame)

            complete = tk.Button(change_route_options_frame, text="Complete", command=lambda: change())
            complete.grid(row=0, column=1, sticky=tk.EW)
            cancel = tk.Button(change_route_options_frame, text="Cancel", command=lambda: cancel_change_route())
            cancel.grid(row=0, column=0, sticky=tk.EW)

            change_route_options_frame.pack(expand=tk.YES)

            change_route_frame.grid(row=3, columnspan=2)

        def change_parking():
            parkings = list(filter(lambda stn: stn.get_type().value == 'P', self.generator.stations))

            panel_bus_window.geometry("{}x{}+600+300".format(width_screen_aux,
                                                             height_screen_aux + len(parkings)*40 + 25))
            change_parking_frame = tk.Frame(panel_bus_window)
            v = tk.IntVar()
            v.set(0)

            tk.Label(change_parking_frame,
                     text="""Choose the Bus Station""",
                     justify=tk.LEFT,
                     padx=20).pack()

            for index_route in range(0, len(parkings)):
                tk.Radiobutton(change_parking_frame,
                               text="Parking {}".format(parkings[index_route].get_code()),
                               padx=20,
                               variable=v,
                               value=index_route).pack(anchor=tk.W)

            def cancel_change_parking():
                change_parking_frame.destroy()
                panel_bus_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux+40))

            def change():
                bus.set_parking(parkings[v.get()])
                parking_info.configure(text="Parking:{}".format(bus.get_parking().get_code()))
                cancel_change_parking()

            change_parking_options_frame = tk.Frame(change_parking_frame)

            complete = tk.Button(change_parking_options_frame, text="Complete", command=lambda: change())
            complete.grid(row=0, column=1, sticky=tk.EW)
            cancel = tk.Button(change_parking_options_frame, text="Cancel", command=lambda: cancel_change_parking())
            cancel.grid(row=0, column=0, sticky=tk.EW)

            change_parking_options_frame.pack(expand=tk.YES)

            change_parking_frame.grid(row=3, columnspan=2)

        bus = p_bus
        self.canvas.itemconfig(bus.get_id(), fill='yellow')

        def on_closing():
            self.canvas.itemconfig(bus.get_id(), fill=bus.get_color())
            panel_bus_window.destroy()

        panel_bus_window = tk.Toplevel(self)
        panel_bus_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux+40))
        panel_bus_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_bus_window.columnconfigure(0, minsize=width_panel/2, weight=1)
        panel_bus_window.columnconfigure(1, minsize=width_panel/2, weight=1)

        bus_title = tk.Label(panel_bus_window, text="Bus {}".format(bus.get_code()), font=font_titles, bg=color5)
        bus_title.grid(row=0, columnspan=2, sticky=tk.EW)

        info_frame = tk.Frame(panel_bus_window)

        speed_info = tk.Label(info_frame, text="Speed: {}".format(bus.get_speed()), width=25, font=font_info)
        speed_info.grid(row=0)
        capacity_info = tk.Label(info_frame, text="Capacity: {}".format(bus.get_capacity()), width=25, font=font_info)
        capacity_info.grid(row=1)
        passengers_info = tk.Label(info_frame, text="# Passengers:{}".format(bus.get_use()), width=25, font=font_info)
        passengers_info.grid(row=2)
        parking_info = tk.Label(info_frame, text="Parking:{}".format(bus.get_parking().get_code()), width=25,
                                font=font_info)
        parking_info.grid(row=3)
        route_info = tk.Label(info_frame, text="Route:{}".format(bus.get_route().get_code()), width=25, font=font_info)
        route_info.grid(row=4)

        info_frame.grid(row=1, columnspan=2)

        options_frame = tk.Frame(panel_bus_window)

        options_frame_change = tk.Frame(options_frame)
        change_route_btn = tk.Button(options_frame_change, text="Change Route", command=lambda: change_route(),
                                     width=13)
        change_route_btn.grid(row=0, column=0)

        change_parking_btn = tk.Button(options_frame_change, text="Change Parking", command=lambda: change_parking(),
                                       width=13)
        change_parking_btn.grid(row=0, column=1)
        options_frame_change.grid(row=0, columnspan=2)

        def finish_route_bus(finish_p_bus: Bus):
            finish_p_bus.get_route().block()
            route_info.configure(text="Route: Canceled")

        def del_bus(del_p_bus: Bus):
            self.generator.buses.remove(del_p_bus)
            panel_bus_window.destroy()
            panel_buses.grid_forget()
            create_buttons_buses(self)

        terminate_route = tk.Button(options_frame, text="Finish Route", command=partial(finish_route_bus, bus),
                                    width=13)
        terminate_route.grid(row=1, column=0)

        del_bus_btn = tk.Button(options_frame, text="Delete", command=partial(del_bus, bus), width=13)
        del_bus_btn.grid(row=1, column=1)

        options_frame.grid(row=2, columnspan=2)

        options_frame2 = tk.Frame(panel_bus_window)

        block_btn_text = 'Close'
        if bus.is_block():
            block_btn_text = 'Open'
        block_bus_btn = tk.Button(options_frame2, text=block_btn_text, width=13)
        bus.btn_close = block_bus_btn
        block_bus_btn.configure(command=partial(self.close_bus, bus))
        block_bus_btn.grid(row=0, column=0)

        options_frame2.grid(row=3, columnspan=2)

    def create_bus():

        self.pause()

        create_bus_window = tk.Toplevel(self)
        create_bus_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux))

        frame1 = tk.Frame(create_bus_window)
        frame2 = tk.Frame(create_bus_window)

        v = tk.IntVar()
        v.set(0)

        routes = self.generator.routes

        def show_choice():
            print(v.get())

        tk.Label(frame1,
                 text="""Choose the route""",
                 justify=tk.LEFT,
                 padx=20, pady=10).pack()

        for index_route in range(0, len(routes)):
            tk.Radiobutton(frame1,
                           text="Route {}".format(routes[index_route].get_code()),
                           padx=20,
                           variable=v,
                           command=show_choice,
                           value=index_route).pack(anchor=tk.W)

        if len(routes) == 0:
            msg_aux_stn = tk.Label(frame1, text="There're not Routes",
                                   font=tk_font.Font(family=family1, size=8))
            msg_aux_stn.pack(anchor=tk.CENTER)

        v2 = tk.IntVar()
        v2.set(0)

        parkings = list(filter(lambda stn: stn.get_type().value == 'P', self.generator.stations))

        tk.Label(frame2,
                 text="""Choose the Parking""",
                 justify=tk.LEFT,
                 padx=20, pady=10).pack()

        for index_route in range(0, len(parkings)):
            tk.Radiobutton(frame2,
                           text="Parking {}".format(parkings[index_route].get_code()),
                           padx=20,
                           variable=v2,
                           value=index_route).pack(anchor=tk.W)

        if len(parkings) == 0:
            msg_aux_stn = tk.Label(frame2, text="There're not Parkings",
                                   font=tk_font.Font(family=family1, size=8))
            msg_aux_stn.pack(anchor=tk.CENTER)

        speed_input_frame = tk.Frame(create_bus_window)

        speed_input_text = tk.Label(speed_input_frame, text='Speed')
        speed_input_text.grid(row=1, column=0)
        speed_input = tk.Entry(speed_input_frame, width=5)
        speed_input.grid(row=1, column=1)

        speed_input_frame.grid(row=1, columnspan=2, pady=10)

        def complete():
            def r():
                return random.randint(0, 255)
            if speed_input.get() and v.get() and v2.get():
                color_bus = '#%02X%02X%02X' % (r(), r(), r())

                bus = Bus(parking=parkings[v2.get()], capacity=50,
                          use=0, speed=int(speed_input.get()), color=color_bus, code=len(self.generator.buses)+1,
                          route=routes[v.get()])
                self.generator.buses.append(bus)
                panel_buses.grid_forget()
                create_buttons_buses(self)
                self.show_notification(message='Station created')
            create_bus_window.destroy()

        options_input_frame = tk.Frame(create_bus_window)

        cancel_btn = tk.Button(options_input_frame, text="Cancel", command=lambda: create_bus_window.destroy())
        cancel_btn.grid(row=2, column=0)
        complete_btn = tk.Button(options_input_frame, text="Complete", command=lambda: complete())
        complete_btn.grid(row=2, column=1)

        options_input_frame.grid(row=2, columnspan=2)

        frame1.grid(row=0, column=0, sticky=tk.EW)
        frame2.grid(row=0, column=1, sticky=tk.EW)

    panel_buses = tk.Frame(self.panel)
    panel_buses.columnconfigure(0, minsize=86, weight=1)
    panel_buses.columnconfigure(1, minsize=88, weight=1)
    panel_buses.columnconfigure(2, minsize=86, weight=1)

    panel_title = tk.Label(panel_buses, text="Buses", font=font_titles, bg=color5)
    panel_title.grid(row=0, columnspan=3, sticky=tk.EW)

    cant_btn = 0
    fin_i = 1
    buses = self.generator.buses
    buses.sort(key=lambda bus_sort: bus_sort.get_code())
    if len(buses) != 0:
        for i in range(1, mt.ceil(len(buses) / 3) + 1):
            fin_i += 1
            for j in range(0, 3):
                if cant_btn < len(buses):
                    btn = tk.Button(panel_buses, text="Bus {}".format(buses[cant_btn].get_code()),
                                    command=partial(show_info_bus, buses[cant_btn]))
                    btn.grid(row=i, column=j, sticky='ew')
                    buses[cant_btn].btn_id = btn
                    cant_btn += 1
    else:
        msg_aux = tk.Label(panel_buses, text="There're not buses",
                           font=tk_font.Font(family=family1, size=8))
        msg_aux.grid(row=1, column=1, sticky=tk.EW)
        fin_i += 1

    add_bus_frame = tk.Frame(panel_buses)
    btn = tk.Button(add_bus_frame, text="Add bus", command=lambda: create_bus())
    btn.pack(fill=tk.X)
    add_bus_frame.grid(row=fin_i, column=1, sticky=tk.EW)

    panel_buses.grid(row=1, sticky=tk.EW, pady=15)


def create_buttons_routes(self):

    font_titles = tk_font.Font(family=family1, size=14, weight="bold")

    def show_info_route(index):

        self.pause()

        route: Route = self.generator.routes[index]

        lines_ids = []

        def r():
            return random.randint(0, 255)
        color_line = '#%02X%02X%02X' % (r(), r(), r())

        for path in route.get_paths():
            (x_init, y_init) = path.get_start_point()
            (x_final, y_final) = path.get_end_point()
            pid = self.canvas.create_line(x_init, y_init, x_final, y_final, fill=color_line, width=3, arrow=tk.LAST)
            lines_ids.append(pid)

        def on_closing():
            for pid2 in lines_ids:
                self.canvas.delete(pid2)
            panel_route_window.destroy()

        panel_route_window = tk.Toplevel(self)
        panel_route_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux))
        panel_route_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_route_window.columnconfigure(0, minsize=width_panel/2, weight=1)
        panel_route_window.columnconfigure(1, minsize=width_panel/2, weight=1)

        route_title = tk.Label(panel_route_window, text="Route {}".format(index + 1), font=font_titles, bg=color5)
        route_title.grid(row=0, columnspan=2, sticky=tk.EW)

        def block_route(p_route: Route):
            if p_route.is_block():
                p_route.unblock()
                block_btn.configure(text='Block')
            else:
                p_route.block()
                block_btn.configure(text='Unblock')

        block_btn = tk.Button(panel_route_window, text="Block", command=partial(block_route, route), width=13)
        block_btn.grid(row=2, column=0)

        def del_route(p_route: Route):
            for pid2 in lines_ids:
                self.canvas.delete(pid2)
            self.generator.routes.remove(p_route)
            panel_route_window.destroy()
            panel_routes.grid_forget()
            create_buttons_routes(self)

        del_route_btn = tk.Button(panel_route_window, text="Delete", command=partial(del_route, route), width=13)
        del_route_btn.grid(row=2, column=1)

    def create_route():

        self.pause()

        create_route_window = tk.Toplevel(self)
        create_route_window.geometry("{}x{}+600+300".format(width_screen_aux + 30, height_screen_aux))

        frame1 = tk.Frame(create_route_window)
        frame2 = tk.Frame(create_route_window)
        create_route_window.columnconfigure(0, minsize=width_screen_aux / 2, weight=1)
        create_route_window.columnconfigure(1, minsize=width_screen_aux / 2, weight=1)

        x_input_text = tk.Label(frame1, text='Point Coordenates', font=font_titles, padx=15)
        x_input_text.grid(row=0, columnspan=2)

        x_input_text = tk.Label(frame1, text='X')
        x_input_text.grid(row=1, column=0)
        x_input = tk.Entry(frame1, width=5)
        x_input.grid(row=1, column=1)

        y_input_text = tk.Label(frame1, text='Y')
        y_input_text.grid(row=2, column=0)
        y_input = tk.Entry(frame1, width=5)
        y_input.grid(row=2, column=1)

        scrollbar = tk.Scrollbar(frame2)
        scrollbar.pack(side='right', fill='y')
        listbox = tk.Listbox(frame2, yscrollcommand=scrollbar.set)
        listbox.pack(side='left', fill='both')

        scrollbar.config(command=listbox.yview)

        def add_point(value1: tk.Entry, value2: tk.Entry):
            if value1.get() and value2.get():
                val1 = int(value1.get())
                val2 = int(value2.get())
                listbox.insert(tk.END, str((val1, val2)))
                value1.delete(first=0, last=5)
                value2.delete(first=0, last=5)

        def show_stn(add: tk.Button):
            frame3 = tk.Frame(create_route_window)
            frame3.grid(row=1, columnspan=2)
            add.configure(state='disabled')
            tk.Label(frame3,
                     text="""Choose the station""",
                     justify=tk.LEFT,
                     padx=20, pady=6).pack()

            v = tk.IntVar()
            v.set(0)

            stations = self.generator.stations

            def add_stn():
                station: Station = self.generator.stations[v.get()]
                (stn_x, stn_y) = station.get_location()
                listbox.insert(tk.END, str((stn_x, stn_y, 'Station {}'.format(v.get()+1), v.get())))
                frame3.grid_forget()
                add.configure(command=partial(add_point, x_input, y_input))
                add.configure(state='active')
                create_route_window.geometry("{}x{}+600+300".format(width_screen_aux + 20, height_screen_aux))

            create_route_window.geometry("{}x{}+600+300".format(width_screen_aux + 20, height_screen_aux +
                                                                len(stations) * 23 + 75))
            stations.sort(key=lambda stn_sort: stn_sort.get_code())
            for index_route in range(0, len(stations)):
                station_title = 'Station {}'
                if stations[index_route].get_type() == StationType.PARKING:
                    station_title = 'Parking {}'
                tk.Radiobutton(frame3,
                               text=station_title.format(stations[index_route].get_code()),
                               padx=20,
                               variable=v,
                               value=index_route).pack(anchor=tk.W)

            if len(stations) == 0:
                msg_aux_stn = tk.Label(frame3, text="There're not Stations",
                                       font=tk_font.Font(family=family1, size=8))
                msg_aux_stn.pack(anchor=tk.CENTER)

            def cancel():
                frame3.destroy()
                create_route_window.geometry("{}x{}+600+300".format(width_screen_aux + 20, height_screen_aux))
                add.configure(state='active')

            options_station_frame = tk.Frame(frame3)

            cancel = tk.Button(options_station_frame, text="Cancel", width=9, command=partial(cancel))
            cancel.grid(row=0, column=0)

            complete_stn_btn = tk.Button(options_station_frame, text="Add", command=partial(add_stn), width=9)
            complete_stn_btn.grid(row=0, column=1)
            if len(stations) == 0:
                complete_stn_btn.configure(state='disabled')

            options_station_frame.pack(anchor=tk.W)

            frame3.grid(row=1, columnspan=2)

        def complete():
            if listbox.size() > 0:
                route = Route(code=len(self.generator.routes)+1)
                start_point = None
                for index in range(0, listbox.size()):
                    arr = listbox.get(first=index).replace(')', "")
                    arr = arr.replace('(', "")
                    arr = arr.replace(' ', "")
                    arr = arr.split(',')
                    if not start_point:
                        start_point = (int(arr[0]), int(arr[1]))
                    else:
                        new_path = Path(code=len(self.generator.paths)+1, start=start_point, end=(int(arr[0]), int(arr[1])))
                        if len(arr) > 2:
                            new_path = Path(code=len(self.generator.paths)+1, start=start_point,
                                            end=(int(arr[0]), int(arr[1])), station=self.generator.stations[int(arr[3])])
                        start_point = (int(arr[0]), int(arr[1]))
                        self.generator.paths.append(new_path)
                        route.add_path(new_path)
                self.generator.routes.append(route)
                panel_routes.grid_forget()
                create_buttons_routes(self)
            create_route_window.destroy()

        add_options_input_frame = tk.Frame(frame1)

        add_btn = tk.Button(add_options_input_frame, text="Add Point", command=partial(add_point, x_input, y_input),
                            width=9)
        add_btn.grid(row=0, column=0)
        add_stn_btn = tk.Button(add_options_input_frame, text="Add Stop", command=partial(show_stn, add_btn), width=9)
        add_stn_btn.grid(row=0, column=1)

        add_options_input_frame.grid(row=3, columnspan=2, pady=10)

        options_input_frame = tk.Frame(frame1)

        cancel_btn = tk.Button(options_input_frame, text="Cancel", command=lambda: create_route_window.destroy(),
                               width=9)
        cancel_btn.grid(row=2, column=0)
        complete_btn = tk.Button(options_input_frame, text="Complete", command=lambda: complete(), width=9)
        complete_btn.grid(row=2, column=1)

        options_input_frame.grid(row=4, columnspan=2)

        frame1.grid(row=0, column=0)
        frame2.grid(row=0, column=1)

    def block_path():
        panel_block_window = tk.Toplevel(self)
        panel_block_window.geometry("{}x{}+600+300".format(width_screen_aux, height_screen_aux))

        panel_block_window.columnconfigure(0, minsize=width_panel / 2, weight=1)
        panel_block_window.columnconfigure(1, minsize=width_panel / 2, weight=1)

        block_title = tk.Label(panel_block_window, text="Block Path", font=font_titles, bg=color5)
        block_title.grid(row=0, columnspan=2, sticky=tk.EW)

        start_path_frame = tk.Frame(panel_block_window, pady=8)

        x0_input_text = tk.Label(start_path_frame, text='X1')
        x0_input_text.grid(row=0, column=0)
        x0_input = tk.Entry(start_path_frame, width=5)
        x0_input.grid(row=0, column=1)

        y0_input_text = tk.Label(start_path_frame, text='Y1')
        y0_input_text.grid(row=1, column=0)
        y0_input = tk.Entry(start_path_frame, width=5)
        y0_input.grid(row=1, column=1)

        start_path_frame.grid(row=1, column=0)

        end_path_frame = tk.Frame(panel_block_window, pady=8)

        x1_input_text = tk.Label(end_path_frame, text='X2')
        x1_input_text.grid(row=0, column=0)
        x1_input = tk.Entry(end_path_frame, width=5)
        x1_input.grid(row=0, column=1)

        y1_input_text = tk.Label(end_path_frame, text='Y2')
        y1_input_text.grid(row=1, column=0)
        y1_input = tk.Entry(end_path_frame, width=5)
        y1_input.grid(row=1, column=1)

        end_path_frame.grid(row=1, column=1)

        options_station_frame = tk.Frame(panel_block_window, pady=8)
        options_station_frame.columnconfigure(0, minsize=44, weight=1)
        options_station_frame.columnconfigure(1, minsize=86, weight=1)
        options_station_frame.columnconfigure(2, minsize=86, weight=1)
        options_station_frame.columnconfigure(3, minsize=44, weight=1)

        def block():
            if x0_input.get() and x1_input.get() and y0_input.get() and y1_input.get():
                for path in self.generator.paths:
                    (x_start_path, y_start_path) = path.get_start_point()
                    (x_end_path, y_end_path) = path.get_end_point()
                    if (x_start_path == int(x0_input.get()) or x_end_path == int(x0_input.get())) and \
                            (y_start_path == int(y0_input.get()) or y_end_path == int(y0_input.get())):
                        if (x_start_path == int(x1_input.get()) or x_end_path == int(x1_input.get())) and \
                                (y_start_path == int(y1_input.get()) or y_end_path == int(y1_input.get())):
                            if path.is_block():
                                path.unblock()
                            else:
                                path.block()
                            break
                self.show_notification(message='Path blocked')
            panel_block_window.destroy()

        cancel = tk.Button(options_station_frame, text="Cancel", width=9, command=lambda: panel_block_window.destroy())
        cancel.grid(row=0, column=1, sticky=tk.EW)

        complete_block_btn = tk.Button(options_station_frame, text="Block", command=partial(block), width=9)
        complete_block_btn.grid(row=0, column=2, sticky=tk.EW)

        options_station_frame.grid(row=2, columnspan=2, sticky=tk.EW)

    panel_routes = tk.Frame(self.panel)
    panel_routes.columnconfigure(0, minsize=86, weight=1)
    panel_routes.columnconfigure(1, minsize=88, weight=1)
    panel_routes.columnconfigure(2, minsize=86, weight=1)

    panel_title = tk.Label(panel_routes, text="Routes", font=font_titles, bg=color5)
    panel_title.grid(row=0, columnspan=3, sticky=tk.EW)

    cant_btn = 0
    fin_i = 1
    routes = self.generator.routes

    if len(routes) != 0:
        for i in range(1, mt.ceil(len(routes) / 3) + 1):
            fin_i += 1
            for j in range(0, 3):
                if cant_btn < len(routes):
                    btn = tk.Button(panel_routes, text="Route {}".format(cant_btn + 1),
                                    command=partial(show_info_route, cant_btn))
                    btn.grid(row=i, column=j, sticky='ew')
                    cant_btn += 1
    else:
        msg_aux = tk.Label(panel_routes, text="There're not routes",
                           font=tk_font.Font(family=family1, size=8))
        msg_aux.grid(row=1, column=1, sticky=tk.EW)
        fin_i += 1

    options_route_frame = tk.Frame(panel_routes)
    options_route_frame.columnconfigure(0, minsize=44, weight=1)
    options_route_frame.columnconfigure(1, minsize=86, weight=1)
    options_route_frame.columnconfigure(2, minsize=86, weight=1)
    options_route_frame.columnconfigure(3, minsize=44, weight=1)

    btn = tk.Button(options_route_frame, text="Add Route", command=lambda: create_route())
    btn.grid(row=fin_i, column=1, sticky='ew')

    btn_block = tk.Button(options_route_frame, text="Block Path", command=lambda: block_path())
    btn_block.grid(row=fin_i, column=2, sticky='ew')

    options_route_frame.grid(row=fin_i, columnspan=3, sticky='ew')

    panel_routes.grid(row=4, sticky=tk.EW)
