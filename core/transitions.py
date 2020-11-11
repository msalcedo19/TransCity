from core.animationObj import AnimationObject
import math as mt
from entities.path import *
from entities.station import *
from entities.bus import *
from copy import copy
from core.envButtons import Action


def animate_route(app, animation_object: AnimationObject, fun=None):

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

    def verify_station(p_station: Station, p_bus: Bus):
        """
        Se verifica si alguno de los usuarios dentro del bus se bajan en la estación pasada por parámetro. Luego se
        verifica si alguno de los usuarios dentro de la estación debe subirse al bus actual.
        :param p_station: Estación donde se encuentra el bus actualmente
        :param p_bus: Bus actual
        :return: None
        """

        def send_bus(full_station: Station):
            bus_available = list(filter(lambda b: not b.is_active() and b.get_parking() == p_bus.get_parking(),
                                        app.generator.buses))
            if bus_available:
                new_route = copy(p_bus.get_route())
                for path_in in new_route.get_paths():
                    if path_in.get_station() and path_in.get_station() == full_station:
                        break
                    else:
                        path_in.set_station(stn=None)
                bus_available[0].set_route(new_route)
                app.launch_bus(bus=bus_available[0])
                app.generator.log(Action.SEND_BUS)

        if p_station and p_station.get_type() == StationType.STATION:

            # Usuarios se bajan del bus
            for user in copy(p_bus.users()):
                if user.get_dest() == p_station and app.active:
                    p_bus.del_user(user)
                    user.end_trip()
                    if p_bus.is_block() and p_bus.get_use() <= p_bus.get_capacity() * 0.7:
                        p_bus.btn_id.configure(bg='SystemButtonFace')
                        app.show_notification('Bus: {}\n Capacity < 70%'.format(p_bus.get_code()))

            # Usuarios se suben al bus
            for user in copy(p_station.users()):
                if user.get_src() == p_station and user.get_route() == p_bus.get_route() and \
                        app.active:
                    p_bus.add_user(user)
                    p_station.del_user(user)
                    app.canvas.itemconfig(p_station.id_text_object, text=p_station.get_use())

                    if p_station.is_close() and p_station.get_use() <= p_station.get_capacity()*0.7:
                        app.show_notification('Station: {}\n Capacity < 70%'.format(p_station.get_code()))
                        p_station.btn_id.configure(bg='SystemButtonFace')

                    if p_bus.get_capacity() == p_bus.get_use():
                        p_bus.btn_id.configure(bg='red')
                        app.show_notification(message='Bus: {}\n Full'.format(p_bus.get_code()))
                        send_bus(full_station=p_station)

        elif p_station and p_station.get_type() == StationType.PARKING:
            station_aux = path.get_station()
            station_aux.increase_user()
            p_bus.deactivate()
            app.canvas.itemconfig(station_aux.id_text_object, text=str(station_aux.get_use()))
            app.canvas.delete(id_image)

    if app.active:
        # Atributos necesarios para realizar la animación
        id_image = animation_object.id_object
        x = animation_object.x
        y = animation_object.y
        path = animation_object.actual_path
        bus = animation_object.actual_bus
        if fun is not None:
            fun(id_image)

        # Se verifica si ya esta en el punto de destino del camino, entra al if si aún no ha llegado
        if path.path_state(x, y) and not path.is_block():
            (x_final, y_final) = path.get_end_point()
            if path.get_type_move() == MoveTypeV2.VERTICAL_ARRIBA:
                if animation_object.actual_type_path != MoveTypeV2.VERTICAL_ARRIBA:
                    app.canvas.coords(id_image, x + 2, y, x + 7, y, x + 7, y + 9, x + 2, y + 9)
                    animation_object.actual_type_path = MoveTypeV2.VERTICAL_ARRIBA
                animation_object.set_value(x=x, y=y - 1)
                app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                          lambda pid: app.canvas.move(pid, 0, -1))
            elif path.get_type_move() == MoveTypeV2.VERTICAL_ABAJO:
                if animation_object.actual_type_path != MoveTypeV2.VERTICAL_ABAJO:
                    app.canvas.coords(id_image, x - 1, y, x - 6, y, x - 6, y + 9, x - 1, y + 9)
                    animation_object.actual_type_path = MoveTypeV2.VERTICAL_ABAJO
                animation_object.set_value(x=x, y=y + 1)
                app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                          lambda pid: app.canvas.move(pid, 0, 1))
            elif path.get_type_move() == MoveTypeV2.HORIZONTAL_IZQUIERDA:
                if animation_object.actual_type_path != MoveTypeV2.HORIZONTAL_IZQUIERDA:
                    app.canvas.coords(id_image, x, y - 1, x + 9, y - 1, x + 9, y - 6, x, y - 6)
                    animation_object.actual_type_path = MoveTypeV2.HORIZONTAL_IZQUIERDA
                animation_object.set_value(x=x - 1, y=y)
                app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                          lambda pid: app.canvas.move(pid, -1, 0))
            elif path.get_type_move() == MoveTypeV2.HORIZONTAL_DERECHA:
                if animation_object.actual_type_path != MoveTypeV2.HORIZONTAL_DERECHA and \
                        animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ARR and \
                        animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ABJ:
                    app.canvas.coords(id_image, x, y + 2, x + 9, y + 2, x + 9, y + 7, x, y + 7)
                    animation_object.actual_type_path = MoveTypeV2.HORIZONTAL_DERECHA
                animation_object.set_value(x=x + 1, y=y)
                app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                          lambda pid: app.canvas.move(pid, 1, 0))
            else:
                (x_inicial, y_inicial) = path.get_start_point()
                alpha = get_alpha(x_inicial, y_inicial, x_final, y_final)
                vy = mt.sin(alpha) * 0.7071068
                vx = mt.cos(alpha) * 0.7071068
                if path.get_type_move() == MoveTypeV2.DIAG_IZQ_ARR:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_IZQ_ARR:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_IZQ_ARR
                    animation_object.set_value(x=x - vx, y=y - vy)
                    app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                              lambda pid: app.canvas.move(pid, -vx, -vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_IZQ_ABJ:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_IZQ_ABJ:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_IZQ_ABJ
                    animation_object.set_value(x=x - vx, y=y + vy)
                    app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                              lambda pid: app.canvas.move(pid, -vx, vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ARR:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ARR:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_DER_ARR
                    animation_object.set_value(x=x + vx, y=y - vy)
                    app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                              lambda pid: app.canvas.move(pid, vx, -vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ABJ:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ABJ:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_DER_ABJ
                    animation_object.set_value(x=x + vx, y=y + vy)
                    app.after(int(1000 / bus.get_speed()), animate_route, app, animation_object,
                              lambda pid: app.canvas.move(pid, vx, vy))
        elif path.path_state(x, y) and path.is_block():
            # como el camino esta bloqueado el bus se envia a su parqueadero de buses
            station = bus.get_parking()
            station.increase_user()
            app.canvas.itemconfig(station.id_text_object, text=str(station.get_use()))
            app.canvas.delete(id_image)
        else:
            station = path.get_station()
            print(station)
            verify_station(p_station=station, p_bus=bus)

            paths = animation_object.paths_left
            # Si la cantidad de caminos es mayor a cero significa que la ruta aún no ha terminado
            if len(paths) > 0:
                path = paths[0]
                (path_x1, path_y1) = path.get_start_point()
                del paths[0]
                animation_object.set_value(x=path_x1, y=path_y1, actual_path=path, paths_left=paths, actual_bus=bus)
                if station and station.get_type() == StationType.STATION and not station.is_close():
                    app.after(1000, animate_route, app, animation_object)
                else:
                    animate_route(app, animation_object)
    else:
        app.data_resume['resume'].append(animation_object)
