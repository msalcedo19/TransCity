import tkinter as tk
from entities.station import *
from entities.bus import *
from entities.path import Path
from functools import partial
import math as mt
import tkinter.font as tk_font
from const import *
import random


def create_buttons_simulation(self):
    font_titles = tk_font.Font(family=family1, size=12, weight="bold")

    panel_simulation = tk.Frame(self.panel, bg=color1)
    panel_simulation.columnconfigure(0, minsize=width_panel/2, weight=1)
    panel_simulation.columnconfigure(1, minsize=width_panel/2, weight=1)
    panel_title = tk.Label(panel_simulation, text="Simulation", font=font_titles, bg=color5)
    panel_title.grid(row=0, columnspan=2, sticky=tk.EW)

    btn_col1 = tk.Frame(panel_simulation)
    btn_col2 = tk.Frame(panel_simulation)

    self.btn_start = tk.Button(btn_col1, text="Start", command=self.start)
    self.btn_start.pack(fill=tk.X)

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

    btn_coord = tk.Button(btn_col2, text="Coord", command=lambda: show_coords())
    btn_coord.pack(fill=tk.X)

    btn_log = tk.Button(btn_col1, text="Log", command=self.log)
    btn_log.pack(fill=tk.X)

    btn_save = tk.Button(btn_col2, text="Save", command=self.save)
    btn_save.pack(fill=tk.X)

    btn_col1.grid(row=1, column=0, sticky=tk.NSEW)
    btn_col2.grid(row=1, column=1, sticky=tk.NSEW)
    panel_simulation.grid(row=0, sticky=tk.EW)


def create_buttons_stations(self):

    font_titles = tk_font.Font(family=family1, size=12, weight="bold")
    font_info = tk_font.Font(family=family1, size=10)

    def show_info_station(index):

        self.pause()

        station = self.generator.stations[index]
        self.canvas.itemconfig(station.id_object, fill='yellow')

        def on_closing():
            self.canvas.itemconfig(station.id_object, fill=station.color)
            panel_station_window.destroy()

        panel_station_window = tk.Toplevel(self)
        panel_station_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))
        panel_station_window.protocol("WM_DELETE_WINDOW", on_closing)

        panel_station_window.columnconfigure(0, minsize=width_panel/2, weight=1)
        panel_station_window.columnconfigure(1, minsize=width_panel/2, weight=1)

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

        """options_frame = tk.Frame(panel_bus_window)
        
        options_frame_change = tk.Frame(options_frame)
        change_route_btn = tk.Button(options_frame_change, text="Change Route", command=lambda: change_route(),
                                     width=13)
        change_route_btn.grid(row=0, column=0)

        change_parking_btn = tk.Button(options_frame_change, text="Change Parking", command=lambda: change_parking(),
                                       width=13)
        change_parking_btn.grid(row=0, column=1)
        options_frame_change.grid(row=0, columnspan=2)"""

        def close_station(p_station: Station):
            if p_station.is_close():
                p_station.open()
                p_station.color = '#4571EC'
                close_btn.configure(text="Close")
            else:
                p_station.close()
                p_station.color = 'red'
                close_btn.configure(text="Open")

        txt = 'Close'
        if station.is_close():
            txt = 'Open'
        close_btn = tk.Button(panel_station_window, text=txt, command=partial(close_station, station), width=13)
        close_btn.grid(row=2, columnspan=2)

        # options_frame.grid(row=2, columnspan=2)

    def create_station():

        self.pause()

        create_station_window = tk.Toplevel(self)
        create_station_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

        create_station_window.columnconfigure(0, minsize=width_screen_route/2, weight=1)
        create_station_window.columnconfigure(1, minsize=width_screen_route/2, weight=1)

        tk.Label(create_station_window,
                 text="""Coordenates""",
                 justify=tk.LEFT,
                 padx=20).grid(row=0, columnspan=2)

        input_frame = tk.Frame(create_station_window)

        x_input_text = tk.Label(input_frame, text='X', font=font_info)
        x_input_text.grid(row=1, column=0)
        x_input = tk.Entry(input_frame, width=5)
        x_input.grid(row=1, column=1)

        y_input_text = tk.Label(input_frame, text='Y', font=font_info)
        y_input_text.grid(row=2, column=0)
        y_input = tk.Entry(input_frame, width=5, font=font_info)
        y_input.grid(row=2, column=1)

        use_input_text = tk.Label(input_frame, text='# Passengers', font=font_info)
        use_input_text.grid(row=3, column=0)
        use_input = tk.Entry(input_frame, width=5)
        use_input.grid(row=3, column=1)

        capacity_input_text = tk.Label(input_frame, text='Max Capacity')
        capacity_input_text.grid(row=4, column=0)
        capacity_input = tk.Entry(input_frame, width=5)
        capacity_input.grid(row=4, column=1)

        input_frame.grid(row=1, columnspan=2, pady=10)

        def complete():
            stn = Station(location=(int(x_input.get()), int(y_input.get())), use=int(use_input.get()),
                          capacity=int(capacity_input.get()), stn_type=StationType.STATION,
                          code=len(self.generator.stations)+1)
            self.generator.stations.append(stn)

            create_station_window.destroy()
            panel_stations.grid_forget()
            create_buttons_stations(self)
            self.refresh()

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
    stations = self.generator.stations

    if len(stations) != 0:
        for i in range(1, mt.ceil(len(stations) / 3) + 1):
            fin_i += 1
            for j in range(0, 3):
                if cant_btn < len(stations):
                    btn = tk.Button(panel_stations, text="Station {}".format(stations[cant_btn].get_code()),
                                    command=partial(show_info_station, cant_btn))
                    btn.grid(row=i, column=j, sticky='ew')
                    cant_btn += 1
    else:
        msg_aux = tk.Label(panel_stations, text="There're not stations",
                           font=tk_font.Font(family=family1, size=8))
        msg_aux.grid(row=1, column=1, sticky=tk.EW)
        fin_i += 1

    btn = tk.Button(panel_stations, text="Add", command=lambda: create_station())
    btn.grid(row=fin_i, column=1, sticky='ew')

    panel_stations.grid(row=2, sticky=tk.EW)


def create_buttons_buses(self):

    font_titles = tk_font.Font(family=family1, size=12, weight="bold")
    font_info = tk_font.Font(family=family1, size=10)

    def show_info_bus(index):

        self.pause()

        def change_route():
            panel_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route+150))
            change_route_frame = tk.Frame(panel_bus_window)
            v = tk.IntVar()
            v.set(0)

            routes = self.generator.routes

            def show_choice():
                print(v.get())

            tk.Label(change_route_frame,
                     text="""Choose the route""",
                     justify=tk.LEFT,
                     padx=20).pack()

            for index_route in range(0, len(routes)):
                tk.Radiobutton(change_route_frame,
                               text="Route {}".format(index_route + 1),
                               padx=20,
                               variable=v,
                               command=show_choice,
                               value=index_route).pack(anchor=tk.W)

            def change():
                bus.set_route(routes[v.get()])
                change_route_frame.destroy()
                panel_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

            complete = tk.Button(change_route_frame, text="Complete", command=lambda: change())
            complete.pack(expand="yes")

            change_route_frame.grid(row=3, columnspan=2)

        def change_parking():
            panel_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route+150))
            change_parking_frame = tk.Frame(panel_bus_window)
            v = tk.IntVar()
            v.set(0)

            parkings = self.generator.parking_lot

            def show_choice():
                print(v.get())

            tk.Label(change_parking_frame,
                     text="""Choose the Bus Station""",
                     justify=tk.LEFT,
                     padx=20).pack()

            for index_route in range(0, len(parkings)):
                tk.Radiobutton(change_parking_frame,
                               text="Station {}".format(index_route + 1),
                               padx=20,
                               variable=v,
                               command=show_choice,
                               value=index_route).pack(anchor=tk.W)

            def change():
                bus.set_parking(parkings[v.get()])
                change_parking_frame.destroy()
                panel_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

            complete = tk.Button(change_parking_frame, text="Complete", command=lambda: change())
            complete.pack(expand="yes")

            change_parking_frame.grid(row=3, columnspan=2)

        bus = self.generator.buses[index]
        self.canvas.itemconfig(bus.get_id(), fill='yellow')

        def on_closing():
            self.canvas.itemconfig(bus.get_id(), fill=bus.get_color())
            panel_bus_window.destroy()

        panel_bus_window = tk.Toplevel(self)
        panel_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))
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
        passengers_info = tk.Label(info_frame, text="Parking:{}".format(bus.get_parking().get_code()), width=25,
                                   font=font_info)
        passengers_info.grid(row=3)

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

        def finish_route_bus(p_bus: Bus):
            p_bus.get_route().block()

        def del_bus(p_bus: Bus):
            self.generator.buses.remove(p_bus)
            panel_bus_window.destroy()
            panel_buses.grid_forget()
            create_buttons_buses(self)

        terminate_route = tk.Button(options_frame, text="Finish Route", command=partial(finish_route_bus, bus),
                                    width=13)
        terminate_route.grid(row=1, column=0)

        del_bus_btn = tk.Button(options_frame, text="Delete", command=partial(del_bus, bus), width=13)
        del_bus_btn.grid(row=1, column=1)

        options_frame.grid(row=2, columnspan=2)

    def create_bus():

        self.pause()

        create_bus_window = tk.Toplevel(self)
        create_bus_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

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
                           text="Route {}".format(index_route + 1),
                           padx=20,
                           variable=v,
                           command=show_choice,
                           value=index_route).pack(anchor=tk.W)

        v2 = tk.IntVar()
        v2.set(0)

        parkings = self.generator.parking_lot

        tk.Label(frame2,
                 text="""Choose the Parking""",
                 justify=tk.LEFT,
                 padx=20, pady=10).pack()

        for index_route in range(0, len(parkings)):
            tk.Radiobutton(frame2,
                           text="Parking {}".format(index_route + 1),
                           padx=20,
                           variable=v2,
                           value=index_route).pack(anchor=tk.W)

        speed_input_frame = tk.Frame(create_bus_window)

        speed_input_text = tk.Label(speed_input_frame, text='Speed')
        speed_input_text.grid(row=1, column=0)
        speed_input = tk.Entry(speed_input_frame, width=5)
        speed_input.grid(row=1, column=1)

        speed_input_frame.grid(row=1, columnspan=2, pady=10)

        def complete():
            def r():
                return random.randint(0, 255)
            color_bus = '#%02X%02X%02X' % (r(), r(), r())

            bus = Bus(parking=self.generator.parking_lot[v2.get()], capacity=50,
                      use=15, speed=int(speed_input.get()), color=color_bus, code=len(self.generator.buses)+1,
                      route=routes[v.get()])
            self.generator.buses.append(bus)
            panel_buses.grid_forget()
            create_bus_window.destroy()
            panel_buses.grid_forget()
            create_buttons_buses(self)

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
    if len(buses) != 0:
        for i in range(1, mt.ceil(len(buses) / 3) + 1):
            fin_i += 1
            for j in range(0, 3):
                if cant_btn < len(buses):
                    btn = tk.Button(panel_buses, text="Bus {}".format(cant_btn+1),
                                    command=partial(show_info_bus, cant_btn))
                    btn.grid(row=i, column=j, sticky='ew')
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

    panel_buses.grid(row=1, sticky=tk.EW, pady=10)


def create_buttons_routes(self):

    font_titles = tk_font.Font(family=family1, size=12, weight="bold")

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
        panel_route_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))
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
        create_route_window.geometry("{}x{}+600+300".format(width_screen_route+20, height_screen_route))

        frame1 = tk.Frame(create_route_window)
        frame2 = tk.Frame(create_route_window)
        frame3 = tk.Frame(create_route_window)
        create_route_window.columnconfigure(0, minsize=width_screen_route / 2, weight=1)
        create_route_window.columnconfigure(1, minsize=width_screen_route / 2, weight=1)

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
            val1 = int(value1.get())
            val2 = int(value2.get())
            listbox.insert(tk.END, str((val1, val2)))
            value1.delete(first=0, last=5)
            value2.delete(first=0, last=5)

        def show_stn(add: tk.Button):
            frame3.grid(row=1, columnspan=2)
            add.configure(state='disabled')
            tk.Label(frame3,
                     text="""Choose the station""",
                     justify=tk.LEFT,
                     padx=20, pady=10).pack()

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
                create_route_window.geometry("{}x{}+600+300".format(width_screen_route+20, height_screen_route))

            create_route_window.geometry("{}x{}+600+300".format(width_screen_route+20, height_screen_route +
                                                                len(stations)*30 + 15))

            for index_route in range(0, len(stations)):
                tk.Radiobutton(frame3,
                               text="Station {}".format(index_route + 1),
                               padx=20,
                               variable=v,
                               command=add_stn,
                               value=index_route).pack(anchor=tk.W)

            def cancel():
                create_route_window.geometry("{}x{}+600+300".format(width_screen_route+20, height_screen_route))
                frame3.grid_forget()

            options_station_frame = tk.Frame(frame3)

            cancel = tk.Button(options_station_frame, text="Cancel", width=9, command=partial(cancel))
            cancel.grid(row=0, column=0)

            complete_stn_btn = tk.Button(options_station_frame, text="Add", command=partial(add_stn), width=9)
            complete_stn_btn.grid(row=0, column=1)

            options_station_frame.pack(anchor=tk.W)

        def complete():
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
                    new_path = Path(start=start_point, end=(int(arr[0]), int(arr[1])))
                    if len(arr) > 2:
                        new_path = Path(start=start_point, end=(int(arr[0]), int(arr[1])),
                                        station=self.generator.stations[int(arr[3])])
                    start_point = (int(arr[0]), int(arr[1]))
                    route.add_path(new_path)
            self.generator.routes.append(route)
            panel_routes.grid_forget()
            create_buttons_routes(self)
            create_route_window.destroy()

        add_options_input_frame = tk.Frame(frame1)

        add_btn = tk.Button(add_options_input_frame, text="Add Route", command=partial(add_point, x_input, y_input),
                            width=9)
        add_btn.grid(row=0, column=0)
        add_stn_btn = tk.Button(add_options_input_frame, text="Station", command=partial(show_stn, add_btn), width=9)
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
        frame3.grid(row=1, columnspan=2)

    def block_path():
        panel_block_window = tk.Toplevel(self)
        panel_block_window.geometry("{}x{}+600+300".format(width_screen_route, height_screen_route))

        panel_block_window.columnconfigure(0, minsize=width_panel / 2, weight=1)
        panel_block_window.columnconfigure(1, minsize=width_panel / 2, weight=1)

        block_title = tk.Label(panel_block_window, text="Block Path", font=font_titles, bg=color5)
        block_title.grid(row=0, columnspan=2, sticky=tk.EW)

        start_path_frame = tk.Frame(panel_block_window)

        x0_input_text = tk.Label(start_path_frame, text='X')
        x0_input_text.grid(row=0, column=0)
        x0_input = tk.Entry(start_path_frame, width=5)
        x0_input.grid(row=0, column=1)

        y0_input_text = tk.Label(start_path_frame, text='Y')
        y0_input_text.grid(row=1, column=0)
        y0_input = tk.Entry(start_path_frame, width=5)
        y0_input.grid(row=1, column=1)

        start_path_frame.grid(row=1, column=0)

        end_path_frame = tk.Frame(panel_block_window)

        x1_input_text = tk.Label(end_path_frame, text='X')
        x1_input_text.grid(row=0, column=0)
        x1_input = tk.Entry(end_path_frame, width=5)
        x1_input.grid(row=0, column=1)

        y1_input_text = tk.Label(end_path_frame, text='Y')
        y1_input_text.grid(row=1, column=0)
        y1_input = tk.Entry(end_path_frame, width=5)
        y1_input.grid(row=1, column=1)

        end_path_frame.grid(row=1, column=1)

        options_station_frame = tk.Frame(panel_block_window)
        options_station_frame.columnconfigure(0, minsize=44, weight=1)
        options_station_frame.columnconfigure(1, minsize=86, weight=1)
        options_station_frame.columnconfigure(2, minsize=86, weight=1)
        options_station_frame.columnconfigure(3, minsize=44, weight=1)

        def block():
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

    btn_block = tk.Button(options_route_frame, text="Block", command=lambda: block_path())
    btn_block.grid(row=fin_i, column=2, sticky='ew')

    options_route_frame.grid(row=fin_i, columnspan=3, sticky='ew')

    panel_routes.grid(row=3, sticky=tk.EW, pady=10)
