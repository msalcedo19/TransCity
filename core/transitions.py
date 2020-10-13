from core.animationObj import AnimationObject
import math as mt
from entities.path import *
from entities.station import *


def animate_route(self, animation_object: AnimationObject, fun=None):

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

    def rotate(points, angle, center):
        angle = mt.radians(angle)
        cos_val = mt.cos(angle)
        sin_val = mt.sin(angle)
        cx, cy = center

        x0_old = points[0]
        y0_old = points[1]
        x0_old -= cx
        y0_old -= cy
        x0_new = x0_old * cos_val - y0_old * sin_val
        y0_new = x0_old * sin_val + y0_old * cos_val

        x1_old = points[2]
        y1_old = points[3]
        x1_old -= cx
        y1_old -= cy
        x1_new = x1_old * cos_val - y1_old * sin_val
        y1_new = x1_old * sin_val + y1_old * cos_val

        x2_old = points[2]
        y2_old = points[3]
        x2_old -= cx
        y2_old -= cy
        x2_new = x2_old * cos_val - y2_old * sin_val
        y2_new = x2_old * sin_val + y2_old * cos_val

        x3_old = points[2]
        y3_old = points[3]
        x3_old -= cx
        y3_old -= cy
        x3_new = x3_old * cos_val - y3_old * sin_val
        y3_new = x3_old * sin_val + y3_old * cos_val

        return [x0_new, y0_new, x1_new, y1_new, x2_new, y2_new, x3_new, y3_new]

    if self.active:
        # Atributos necesarios para realizar la animación
        id_image = animation_object.id_object
        x = animation_object.x
        y = animation_object.y
        path = animation_object.actual_path
        bus = animation_object.actual_bus
        if fun is not None:
            fun(id_image)
        # print("{} {} {} {}".format(x,y,x_final,y_final))
        # Se verifica si ya esta en el punto de destino del camino, entra al if si aún no ha llegado
        if path.path_state(x, y) and not bus.get_route().is_block():
            (x_final, y_final) = path.get_end_point()
            if path.get_type_move() == MoveTypeV2.VERTICAL_ARRIBA:
                if animation_object.actual_type_path != MoveTypeV2.VERTICAL_ARRIBA:
                    self.canvas.coords(id_image, x + 2, y, x + 7, y, x + 7, y + 9, x + 2, y + 9)
                    animation_object.actual_type_path = MoveTypeV2.VERTICAL_ARRIBA
                animation_object.set_value(x=x, y=y - 1)
                self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                           lambda pid: self.canvas.move(pid, 0, -1))
            elif path.get_type_move() == MoveTypeV2.VERTICAL_ABAJO:
                if animation_object.actual_type_path != MoveTypeV2.VERTICAL_ABAJO:
                    self.canvas.coords(id_image, x - 1, y, x - 6, y, x - 6, y + 9, x - 1, y + 9)
                    animation_object.actual_type_path = MoveTypeV2.VERTICAL_ABAJO
                animation_object.set_value(x=x, y=y + 1)
                self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                           lambda pid: self.canvas.move(pid, 0, 1))
            elif path.get_type_move() == MoveTypeV2.HORIZONTAL_IZQUIERDA:
                if animation_object.actual_type_path != MoveTypeV2.HORIZONTAL_IZQUIERDA:
                    self.canvas.coords(id_image, x, y - 1, x + 9, y - 1, x + 9, y - 6, x, y - 6)
                    animation_object.actual_type_path = MoveTypeV2.HORIZONTAL_IZQUIERDA
                animation_object.set_value(x=x - 1, y=y)
                self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                           lambda pid: self.canvas.move(pid, -1, 0))
            elif path.get_type_move() == MoveTypeV2.HORIZONTAL_DERECHA:
                if animation_object.actual_type_path != MoveTypeV2.HORIZONTAL_DERECHA and \
                        animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ARR and \
                        animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ABJ:
                    self.canvas.coords(id_image, x, y + 2, x + 9, y + 2, x + 9, y + 7, x, y + 7)
                    animation_object.actual_type_path = MoveTypeV2.HORIZONTAL_DERECHA
                animation_object.set_value(x=x + 1, y=y)
                self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                           lambda pid: self.canvas.move(pid, 1, 0))
            else:
                (x_inicial, y_inicial) = path.get_start_point()
                alpha = get_alpha(x_inicial, y_inicial, x_final, y_final)
                vy = mt.sin(alpha) * 0.7071068
                vx = mt.cos(alpha) * 0.7071068
                if path.get_type_move() == MoveTypeV2.DIAG_IZQ_ARR:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_IZQ_ARR:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_IZQ_ARR
                    animation_object.set_value(x=x - vx, y=y - vy)
                    self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                               lambda pid: self.canvas.move(pid, -vx, -vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_IZQ_ABJ:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_IZQ_ABJ:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_IZQ_ABJ
                    animation_object.set_value(x=x - vx, y=y + vy)
                    self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                               lambda pid: self.canvas.move(pid, -vx, vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ARR:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ARR:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_DER_ARR
                    animation_object.set_value(x=x + vx, y=y - vy)
                    self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                               lambda pid: self.canvas.move(pid, vx, -vy))
                elif path.get_type_move() == MoveTypeV2.DIAG_DER_ABJ:
                    if animation_object.actual_type_path != MoveTypeV2.DIAG_DER_ABJ:
                        animation_object.actual_type_path = MoveTypeV2.DIAG_DER_ABJ
                    animation_object.set_value(x=x + vx, y=y + vy)
                    self.after(int(1000 / bus.get_speed()), animate_route, self, animation_object,
                               lambda pid: self.canvas.move(pid, vx, vy))
        elif path.path_state(x, y) and bus.get_route().is_block():
            station = bus.get_parking()
            station.increase_use()
            self.canvas.itemconfig(station.id_text_object, text=str(station.get_use()))
            self.canvas.delete(id_image)
        else:
            station = path.get_station()
            if station and station.get_type() == StationType.STATION and not station.is_close():
                pass_in1 = bus.get_capacity() - bus.get_use()

                if pass_in1 > 0:
                    pass_in2 = station.get_use() - pass_in1
                    if pass_in2 > 0:
                        station.set_use(pass_in2)
                        bus.set_use(bus.get_use() + pass_in1)
                        self.canvas.itemconfig(station.id_text_object, text=station.get_use())
                    elif pass_in2 <= 0:
                        bus.set_use(bus.get_use() + station.get_use())
                        station.set_use(0)
                        self.canvas.itemconfig(station.id_text_object, text=station.get_use())
            elif station and station.get_type() == StationType.PARKING:
                station = path.get_station()
                station.increase_use()
                self.canvas.itemconfig(station.id_text_object, text=str(station.get_use()))
                self.canvas.delete(id_image)

            paths = animation_object.paths_left
            # Si la cantidad de caminos es mayor a cero significa que la ruta aún no ha terminado
            if len(paths) > 0:
                path = paths[0]
                (path_x1, path_y1) = path.get_start_point()
                # (path_x2, path_y2) = path.get_end_point()
                del paths[0]
                animation_object.set_value(x=path_x1, y=path_y1, actual_path=path, paths_left=paths, actual_bus=bus)
                if station and station.get_type() == StationType.STATION and not station.is_close():
                    self.after(1000, animate_route, self, animation_object)
                else:
                    animate_route(self, animation_object)
    else:
        self.data_resume['resume'].append(animation_object)
